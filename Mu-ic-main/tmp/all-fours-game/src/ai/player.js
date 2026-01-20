/**
 * AI Player - Represents an AI-controlled player in the game
 */

const AIAdapter = require('./adapter');
const { v4: uuidv4 } = require('uuid');

class AIPlayer {
  constructor(options = {}) {
    this.id = uuidv4();
    this.name = options.name || 'AI Player';
    this.modelType = options.modelType || 'openai';
    this.modelName = options.modelName || 'gpt-4';
    this.skill = options.skill || 3; // 1-5 rating
    this.reasoning = options.reasoning || 3;
    
    // Initialize AI adapter
    this.adapter = new AIAdapter(this.modelType, options.apiKey, this.modelName);
    
    // Stats
    this.gamesPlayed = 0;
    this.gamesWon = 0;
    this.totalPoints = 0;
    this.rating = 1600; // ELO rating
  }

  /**
   * Get the AI's decision on which card to play
   */
  async makeMove(gameState, hand) {
    try {
      const card = await this.adapter.chooseCard(gameState, hand);
      
      // Log decision for analysis
      this.logDecision(gameState, hand, card);
      
      return card;
    } catch (error) {
      console.error(`Error in AI move (${this.name}):`, error);
      // Fallback to first playable card
      return hand[0];
    }
  }

  logDecision(gameState, hand, chosenCard) {
    // Could be stored in database for analysis
    if (process.env.DEBUG) {
      console.log(`[${this.name}] Hand: ${hand.map(c => `${c.rank}${c.suit}`).join(', ')}`);
      console.log(`[${this.name}] Chose: ${chosenCard.rank}${chosenCard.suit}`);
    }
  }

  /**
   * Update player stats after game
   */
  updateStats(isWon, pointsScored, opponentRatings) {
    this.gamesPlayed++;
    if (isWon) this.gamesWon++;
    this.totalPoints += pointsScored;
    
    // Update ELO rating
    this.updateELO(isWon, opponentRatings);
  }

  /**
   * Calculate ELO rating change
   */
  updateELO(isWon, opponentRatings) {
    const K = 32; // K factor
    const avgOpponentRating = opponentRatings.reduce((a, b) => a + b, 0) / opponentRatings.length;
    
    // Expected score
    const expectedScore = 1 / (1 + Math.pow(10, (avgOpponentRating - this.rating) / 400));
    
    // Actual score (1 for win, 0 for loss)
    const actualScore = isWon ? 1 : 0;
    
    // New rating
    this.rating = Math.round(this.rating + K * (actualScore - expectedScore));
  }

  /**
   * Get player summary
   */
  getSummary() {
    return {
      id: this.id,
      name: this.name,
      model: {
        type: this.modelType,
        name: this.modelName
      },
      stats: {
        gamesPlayed: this.gamesPlayed,
        gamesWon: this.gamesWon,
        winRate: this.gamesPlayed > 0 
          ? (this.gamesWon / this.gamesPlayed * 100).toFixed(2) + '%'
          : '0%',
        totalPoints: this.totalPoints,
        averagePoints: this.gamesPlayed > 0 
          ? (this.totalPoints / this.gamesPlayed).toFixed(2)
          : '0',
        eloRating: this.rating
      }
    };
  }
}

module.exports = AIPlayer;
