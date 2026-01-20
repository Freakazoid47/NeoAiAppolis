/**
 * Match - Represents a single game match between AI players
 */

const { v4: uuidv4 } = require('uuid');
const { createDeck, getRankValue, getCardPoints, isJackCard, determineWinner } = require('../utils');

class Match {
  constructor(players) {
    this.id = uuidv4();
    this.players = players;
    this.startTime = Date.now();
    this.gameState = {
      dealer: 0,
      trump: null,
      currentTrick: [],
      tricks: [],
      currentPlayerIndex: 0,
      phase: 'dealing'
    };
    this.scores = {};
    this.gameLog = [];
    
    // Initialize scores
    players.forEach(p => {
      this.scores[p.id] = 0;
    });
  }

  /**
   * Play the entire match
   */
  async play() {
    try {
      while (!this.isGameOver()) {
        await this.playRound();
      }
      
      return this.getResult();
    } catch (error) {
      console.error('Match error:', error);
      return null;
    }
  }

  /**
   * Play a single round
   */
  async playRound() {
    // Deal cards
    const deck = createDeck();
    this.gameState.trump = deck[deck.length - 1];
    
    // Setup player hands
    let cardIdx = 0;
    const hands = {};
    for (let player of this.players) {
      hands[player.id] = [];
      for (let i = 0; i < 6; i++) {
        hands[player.id].push(deck[cardIdx++]);
      }
    }
    
    // Play tricks
    while (hands[this.players[0].id].length > 0) {
      await this.playTrick(hands);
    }
    
    // Score round
    await this.scoreRound();
    
    // Next dealer
    this.gameState.dealer = (this.gameState.dealer + 1) % this.players.length;
  }

  /**
   * Play a single trick
   */
  async playTrick(hands) {
    this.gameState.currentTrick = [];
    
    // Each player plays one card
    for (let i = 0; i < this.players.length; i++) {
      const playerIdx = (this.gameState.currentPlayerIndex + i) % this.players.length;
      const player = this.players[playerIdx];
      const hand = hands[player.id];
      
      // Get AI decision
      const card = await player.makeMove(this.gameState, hand);
      
      // Remove from hand
      const cardIdx = hand.findIndex(c => c.suit === card.suit && c.rank === card.rank);
      if (cardIdx > -1) {
        hand.splice(cardIdx, 1);
      }
      
      // Add to trick
      this.gameState.currentTrick.push({
        playerIndex: playerIdx,
        playerId: player.id,
        card: card
      });
    }
    
    // Determine winner
    const winnerIdx = determineWinner(this.gameState.currentTrick, this.gameState.trump.suit);
    const winner = this.players[winnerIdx];
    
    // Log
    this.gameLog.push({
      type: 'trick',
      winner: winner.name,
      cards: this.gameState.currentTrick.map(p => `${p.card.rank}${p.card.suit}`)
    });
    
    // Set up for next trick
    this.gameState.currentPlayerIndex = winnerIdx;
    this.gameState.tricks.push({
      winner: winnerIdx,
      cards: this.gameState.currentTrick
    });
  }

  /**
   * Score the round
   */
  async scoreRound() {
    const trump = this.gameState.trump.suit;
    const roundScores = {};
    
    this.players.forEach(p => roundScores[p.id] = 0);
    
    // HIGH: Highest trump dealt
    let highest = null;
    let highPlayerId = null;
    for (let player of this.players) {
      // Check dealt cards (we don't track this, so use tricks as proxy)
      for (let trick of this.gameState.tricks) {
        for (let play of trick.cards) {
          if (play.card.suit === trump) {
            if (!highest || getRankValue(play.card.rank) > getRankValue(highest.rank)) {
              highest = play.card;
              highPlayerId = play.playerId;
            }
          }
        }
      }
    }
    if (highPlayerId) roundScores[highPlayerId]++;
    
    // JACK: Won jack of trump
    for (let trick of this.gameState.tricks) {
      for (let play of trick.cards) {
        if (isJackCard(play.card, trump)) {
          roundScores[play.playerId] += 4; // 1 for jack + 3 for hang jack
        }
      }
    }
    
    // GAME: Highest card points
    const pointTotals = {};
    this.players.forEach(p => pointTotals[p.id] = 0);
    
    for (let trick of this.gameState.tricks) {
      for (let play of trick.cards) {
        pointTotals[play.playerId] += getCardPoints(play.card.rank);
      }
    }
    
    let maxPlayerId = null;
    let maxPoints = -1;
    for (let [playerId, points] of Object.entries(pointTotals)) {
      if (points > maxPoints) {
        maxPoints = points;
        maxPlayerId = playerId;
      }
    }
    if (maxPlayerId) roundScores[maxPlayerId] += 2; // GAME now worth 2 points
    
    // Update scores
    for (let player of this.players) {
      this.scores[player.id] += roundScores[player.id];
    }
    
    this.gameLog.push({
      type: 'round-score',
      scores: roundScores,
      totalScores: this.scores
    });
  }

  /**
   * Check if game is over
   */
  isGameOver() {
    const winScore = this.players.length === 4 ? 14 : 11;
    return Object.values(this.scores).some(score => score >= winScore);
  }

  /**
   * Get match result
   */
  getResult() {
    const winner = this.players.reduce((prev, current) => 
      this.scores[current.id] > this.scores[prev.id] ? current : prev
    );
    
    return {
      matchId: this.id,
      duration: Date.now() - this.startTime,
      winner: winner,
      players: this.players,
      scores: this.scores,
      log: this.gameLog
    };
  }
}

module.exports = Match;
