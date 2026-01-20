/**
 * Match Queue - Manages AI match queue and scheduling
 */

const { Queue } = require('bullmq');
const redis = require('redis');
const AIPlayer = require('../ai/player');
const Match = require('./match');
const Currency = require('../currency/currency');

class MatchQueue {
  constructor() {
    this.queue = new Queue('ai-matches', {
      connection: {
        host: process.env.REDIS_HOST || 'localhost',
        port: process.env.REDIS_PORT || 6379
      }
    });
    
    this.waitingPlayers = [];
    this.activeMatches = new Map();
    this.currency = new Currency();
    
    this.setupWorkers();
  }

  /**
   * Queue a player/AI for a match
   */
  async queuePlayer(playerConfig) {
    const player = new AIPlayer(playerConfig);
    
    // Add to queue
    await this.queue.add(`match-${player.id}`, {
      playerId: player.id,
      playerConfig: playerConfig,
      timestamp: Date.now()
    });
    
    this.waitingPlayers.push(player);
    console.log(`📋 ${player.name} queued for match`);
    
    // Try to match players
    await this.tryMatchPlayers();
    
    return player.id;
  }

  /**
   * Try to find matches between waiting players
   */
  async tryMatchPlayers() {
    // For simplicity: match first 2-4 available players
    if (this.waitingPlayers.length >= 2) {
      const numPlayers = Math.min(4, this.waitingPlayers.length);
      const players = this.waitingPlayers.splice(0, numPlayers);
      
      // Create match
      await this.createMatch(players);
    }
  }

  /**
   * Create a match between players
   */
  async createMatch(players) {
    const match = new Match(players);
    this.activeMatches.set(match.id, match);
    
    console.log(`🎮 Starting match: ${players.map(p => p.name).join(' vs ')}`);
    
    // Queue match for processing
    await this.queue.add(`process-match-${match.id}`, {
      matchId: match.id,
      playerIds: players.map(p => p.id)
    });
    
    return match;
  }

  /**
   * Setup workers to process matches
   */
  setupWorkers() {
    this.queue.process(async (job) => {
      if (job.name.startsWith('process-match-')) {
        const match = this.activeMatches.get(job.data.matchId);
        if (match) {
          const result = await match.play();
          await this.handleMatchResult(result);
        }
      }
    });
  }

  /**
   * Handle match completion and award currency
   */
  async handleMatchResult(result) {
    const { matchId, winner, players, scores } = result;
    
    console.log(`✅ Match complete: ${winner.name} wins!`);
    
    // Award currency
    for (let player of players) {
      const pointsScored = scores[player.id];
      const isWinner = player.id === winner.id;
      
      // Award currency based on performance
      const currency = await this.currency.calculateReward(
        player,
        isWinner,
        pointsScored,
        players.map(p => p.rating)
      );
      
      // Update player stats
      player.updateStats(isWinner, pointsScored, players.map(p => p.rating));
      
      console.log(`💰 ${player.name} earned ${currency} tokens`);
    }
    
    // Clean up
    this.activeMatches.delete(matchId);
    
    return result;
  }

  /**
   * Get queue status
   */
  async getStatus() {
    const waiting = this.waitingPlayers.length;
    const active = this.activeMatches.size;
    const jobCounts = await this.queue.getJobCounts();
    
    return {
      waitingPlayers: waiting,
      activeMatches: active,
      queuedJobs: jobCounts
    };
  }

  /**
   * Get leaderboard
   */
  async getLeaderboard(limit = 50) {
    // Get from all players that have played
    return this.waitingPlayers
      .sort((a, b) => b.rating - a.rating)
      .slice(0, limit)
      .map((p, idx) => ({
        rank: idx + 1,
        ...p.getSummary()
      }));
  }
}

module.exports = MatchQueue;
