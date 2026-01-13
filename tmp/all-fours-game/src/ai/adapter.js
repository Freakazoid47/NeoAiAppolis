/**
 * AI Adapter - Unified interface for multiple AI models
 * Supports: OpenAI, Anthropic Claude, Local models
 */

const OpenAI = require('openai');
const Anthropic = require('@anthropic-ai/sdk');

class AIAdapter {
  constructor(modelType, apiKey, modelName) {
    this.modelType = modelType; // 'openai', 'anthropic', 'local'
    this.modelName = modelName; // 'gpt-4', 'claude-3-opus', etc.
    this.apiKey = apiKey;
    
    this.initializeClient();
  }

  initializeClient() {
    if (this.modelType === 'openai') {
      this.client = new OpenAI({
        apiKey: this.apiKey || process.env.OPENAI_API_KEY
      });
    } else if (this.modelType === 'anthropic') {
      this.client = new Anthropic({
        apiKey: this.apiKey || process.env.ANTHROPIC_API_KEY
      });
    }
  }

  /**
   * Get AI decision for card play
   * @param {Object} gameState - Current game state
   * @param {Array} hand - Player's cards
   * @returns {Object} - Card to play
   */
  async chooseCard(gameState, hand) {
    const prompt = this.buildPrompt(gameState, hand);
    
    try {
      if (this.modelType === 'openai') {
        return await this.callOpenAI(prompt, gameState, hand);
      } else if (this.modelType === 'anthropic') {
        return await this.callAnthropic(prompt, gameState, hand);
      }
    } catch (error) {
      console.error(`AI Error (${this.modelName}):`, error.message);
      // Fallback: return first playable card
      return hand[0];
    }
  }

  async callOpenAI(prompt, gameState, hand) {
    const response = await this.client.chat.completions.create({
      model: this.modelName || 'gpt-4',
      messages: [
        {
          role: 'system',
          content: 'You are an expert All Fours card game player. Respond with ONLY the card to play in format: "Rank Suit" (e.g., "10 ♥")'
        },
        {
          role: 'user',
          content: prompt
        }
      ],
      temperature: 0.3, // Lower temperature for more consistent decisions
      max_tokens: 50
    });

    const cardStr = response.choices[0].message.content.trim();
    return this.parseCard(cardStr, hand);
  }

  async callAnthropic(prompt, gameState, hand) {
    const response = await this.client.messages.create({
      model: this.modelName || 'claude-3-opus-20240229',
      max_tokens: 50,
      messages: [
        {
          role: 'user',
          content: prompt
        }
      ],
      system: 'You are an expert All Fours card game player. Respond with ONLY the card to play in format: "Rank Suit" (e.g., "10 ♥")'
    });

    const cardStr = response.content[0].text.trim();
    return this.parseCard(cardStr, hand);
  }

  buildPrompt(gameState, hand) {
    const { trump, currentTrick, scores, dealer } = gameState;
    const trickInfo = currentTrick.length > 0
      ? currentTrick.map((p, i) => `Player ${p.playerIndex}: ${p.card.rank}${p.card.suit}`).join('\n')
      : 'No cards played yet (you lead)';

    return `
You are playing All Fours card game.

Your hand: ${hand.map(c => `${c.rank}${c.suit}`).join(', ')}

Game state:
- Trump suit: ${trump.suit}
- Current trick: ${trickInfo}
- Current scores: ${JSON.stringify(scores)}
- You are player ${gameState.currentPlayerIndex}

Rules:
- Must follow suit if possible
- If trump is led, must play trump if possible
- Jack of trump worth winning
- Highest card of led suit wins (trump beats all)

What card should you play? (Format: "Rank Suit", e.g., "10 ♥")
`;
  }

  parseCard(cardStr, hand) {
    // Parse AI response like "10 ♥" or "Ten of Hearts"
    const cleaned = cardStr.trim().toUpperCase();
    
    // Try exact match first
    for (let card of hand) {
      if (`${card.rank}${card.suit}` === cleaned) {
        return card;
      }
    }

    // Try partial match
    const parts = cleaned.split(/\s+/);
    if (parts.length >= 1) {
      const rank = parts[0];
      for (let card of hand) {
        if (card.rank === rank) {
          return card;
        }
      }
    }

    // Fallback: return first card
    return hand[0];
  }

  /**
   * Get model info
   */
  getInfo() {
    return {
      type: this.modelType,
      model: this.modelName,
      provider: this.modelType === 'openai' ? 'OpenAI' : 'Anthropic'
    };
  }
}

module.exports = AIAdapter;
