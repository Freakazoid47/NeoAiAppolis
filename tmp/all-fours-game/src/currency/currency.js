/**
 * Currency System - Tracks and manages currency rewards
 */

class Currency {
  constructor() {
    // Base reward structure
    this.baseReward = 100; // Base tokens per win
    this.bonusPerPoint = 5; // Bonus per point scored
    this.ratingMultiplier = 0.1; // Multiplier based on ELO advantage
  }

  /**
   * Calculate reward for a player after a match
   */
  async calculateReward(player, isWinner, pointsScored, opponentRatings) {
    let reward = 0;

    // Base reward for win
    if (isWinner) {
      reward += this.baseReward;
    }

    // Points bonus
    reward += pointsScored * this.bonusPerPoint;

    // ELO-based multiplier
    const avgOpponentRating = opponentRatings.reduce((a, b) => a + b, 0) / opponentRatings.length;
    const ratingDiff = avgOpponentRating - player.rating;
    const ratingBonus = Math.max(0, ratingDiff * this.ratingMultiplier);
    
    reward += ratingBonus;

    // Performance multiplier (win vs loss)
    if (isWinner) {
      reward = Math.round(reward * 1.5); // 1.5x for winning
    } else {
      reward = Math.round(reward * 0.5); // 0.5x for losing
    }

    return Math.max(10, Math.round(reward)); // Minimum 10 tokens
  }

  /**
   * Calculate bonus for streak
   */
  calculateStreakBonus(winStreak) {
    if (winStreak < 3) return 0;
    return (winStreak - 2) * 50; // 50 bonus per win after 3-win streak
  }

  /**
   * Calculate tournament bonus
   */
  calculateTournamentBonus(placement, totalParticipants) {
    const bonuses = {
      1: 1000, // 1st place
      2: 500,  // 2nd place
      3: 250,  // 3rd place
      4: 100   // 4th place
    };
    return bonuses[placement] || 0;
  }

  /**
   * Get currency summary
   */
  getSummary() {
    return {
      baseReward: this.baseReward,
      bonusPerPoint: this.bonusPerPoint,
      ratingMultiplier: this.ratingMultiplier,
      description: `Base: ${this.baseReward} tokens + ${this.bonusPerPoint} per point + ELO bonus`
    };
  }
}

module.exports = Currency;
