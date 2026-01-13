/**
 * Leaderboard - Track player rankings and statistics
 */

class Leaderboard {
  constructor() {
    this.players = new Map();
  }

  /**
   * Update player in leaderboard
   */
  updatePlayer(player) {
    this.players.set(player.id, {
      id: player.id,
      name: player.name,
      model: `${player.modelType}/${player.modelName}`,
      eloRating: player.rating,
      gamesPlayed: player.gamesPlayed,
      gamesWon: player.gamesWon,
      winRate: player.gamesPlayed > 0 ? (player.gamesWon / player.gamesPlayed * 100).toFixed(2) : 0,
      totalPoints: player.totalPoints,
      averagePoints: player.gamesPlayed > 0 ? (player.totalPoints / player.gamesPlayed).toFixed(2) : 0,
      tokens: player.tokens || 0,
      lastPlayed: new Date()
    });
  }

  /**
   * Get leaderboard ranked by ELO
   */
  getByELO(limit = 100) {
    return Array.from(this.players.values())
      .sort((a, b) => b.eloRating - a.eloRating)
      .slice(0, limit)
      .map((p, idx) => ({
        rank: idx + 1,
        ...p
      }));
  }

  /**
   * Get leaderboard by win rate
   */
  getByWinRate(limit = 100, minGames = 5) {
    return Array.from(this.players.values())
      .filter(p => p.gamesPlayed >= minGames)
      .sort((a, b) => b.winRate - a.winRate)
      .slice(0, limit)
      .map((p, idx) => ({
        rank: idx + 1,
        ...p
      }));
  }

  /**
   * Get leaderboard by tokens earned
   */
  getByTokens(limit = 100) {
    return Array.from(this.players.values())
      .sort((a, b) => b.tokens - a.tokens)
      .slice(0, limit)
      .map((p, idx) => ({
        rank: idx + 1,
        ...p
      }));
  }

  /**
   * Get player rank
   */
  getPlayerRank(playerId, sortBy = 'elo') {
    let leaderboard;
    if (sortBy === 'tokens') {
      leaderboard = this.getByTokens();
    } else if (sortBy === 'winrate') {
      leaderboard = this.getByWinRate();
    } else {
      leaderboard = this.getByELO();
    }

    const player = leaderboard.find(p => p.id === playerId);
    return player ? player.rank : null;
  }

  /**
   * Get statistics
   */
  getStatistics() {
    const players = Array.from(this.players.values());
    if (players.length === 0) {
      return { totalPlayers: 0 };
    }

    const totalGames = players.reduce((sum, p) => sum + p.gamesPlayed, 0);
    const totalTokens = players.reduce((sum, p) => sum + p.tokens, 0);
    const avgELO = (players.reduce((sum, p) => sum + p.eloRating, 0) / players.length).toFixed(2);

    return {
      totalPlayers: players.length,
      totalGamesPlayed: totalGames,
      totalTokensIssued: totalTokens,
      averageELO: avgELO,
      highestELO: Math.max(...players.map(p => p.eloRating)),
      lowestELO: Math.min(...players.map(p => p.eloRating))
    };
  }
}

module.exports = Leaderboard;
