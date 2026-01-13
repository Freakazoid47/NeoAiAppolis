/**
 * Shared Utility Functions for All Fours Game
 * Used across: game.js, server.js, socket-client.js, bot-demo.js
 */

// ===== CARD DECK FUNCTIONS =====
function createDeck() {
    const suits = ['♠', '♥', '♦', '♣'];
    const ranks = ['A', 'K', 'Q', 'J', '10', '9', '8', '7', '6', '5', '4', '3', '2'];
    const deck = [];
    
    for (let suit of suits) {
        for (let rank of ranks) {
            deck.push({ suit, rank });
        }
    }
    
    // Shuffle using Fisher-Yates
    for (let i = deck.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [deck[i], deck[j]] = [deck[j], deck[i]];
    }
    
    return deck;
}

function shuffleDeck(deck) {
    const shuffled = [...deck];
    for (let i = shuffled.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
    }
    return shuffled;
}

// ===== CARD COMPARISON & CONVERSION =====
function cardToString(card) {
    return card.rank + card.suit;
}

function cardsEqual(card1, card2) {
    if (!card1 || !card2) return false;
    return card1.suit === card2.suit && card1.rank === card2.rank;
}

// ===== CARD VALUE & POINTS =====
// Card rank values for determining winner (higher = beats lower of same suit)
function getRankValue(rank) {
    const values = {
        'A': 14, 'K': 13, 'Q': 12, 'J': 11, 
        '10': 10, '9': 9, '8': 8, '7': 7, 
        '6': 6, '5': 5, '4': 4, '3': 3, '2': 2
    };
    return values[rank] || 0;
}

// Card point values for GAME scoring (10, 5, 4, 3, 2, 1)
function getCardPoints(rank) {
    const points = {
        '10': 10, 'K': 4, 'Q': 3, 'J': 2, 'A': 1
    };
    return points[rank] || 0;
}

// ===== CARD IDENTIFICATION =====
function isHighCard(card, trump) {
    return card.suit === trump && card.rank === 'A';
}

function isLowCard(card, trump) {
    return card.suit === trump && card.rank === '2';
}

function isJackCard(card, trump) {
    return card.suit === trump && card.rank === 'J';
}

// ===== GAME RULES =====
function canPlayCard(card, currentTrick, playerHand, trump) {
    // First card in trick - can play anything
    if (currentTrick.length === 0) return true;
    
    const leadCard = currentTrick[0].card;
    
    // Must follow suit if possible
    const sameSuitCards = playerHand.filter(c => c.suit === leadCard.suit);
    if (sameSuitCards.length > 0 && card.suit !== leadCard.suit) {
        return false; // Has led suit but playing different suit
    }
    
    // If trump was led, must follow trump if possible
    if (leadCard.suit === trump && card.suit !== trump) {
        const trumpCards = playerHand.filter(c => c.suit === trump);
        if (trumpCards.length > 0) {
            return false; // Has trump but playing non-trump
        }
    }
    
    return true;
}

function determineWinner(trick, trump) {
    if (trick.length === 0) return null;
    
    const leadCard = trick[0].card;
    let winner = trick[0];
    let highestValue = getRankValue(leadCard.rank);
    
    for (let i = 1; i < trick.length; i++) {
        const current = trick[i];
        const currentCard = current.card || current;
        const currentValue = getRankValue(currentCard.rank);
        
        // Trump beats non-trump
        if (currentCard.suit === trump && winner.card.suit !== trump) {
            winner = current;
            highestValue = currentValue;
        }
        // Same suit: higher rank wins
        else if (currentCard.suit === winner.card.suit && currentValue > highestValue) {
            winner = current;
            highestValue = currentValue;
        }
    }
    
    // Return playerIndex if available, otherwise return the trick item itself
    return winner.playerIndex !== undefined ? winner.playerIndex : winner;
}

// ===== AVATARS =====
function getRandomAvatar() {
    const avatars = [
        '🦜', '🦅', '🦉', '🦚', '🦆', '🦢', '🦩', '🦣', '🦁', '🐯',
        '🐻', '🐨', '🐼', '🦊', '🦝', '🦌', '🦓', '🦏', '🐘', '🦛',
        '🧙', '🧚', '🧛', '🧟', '🧔', '👨', '👩', '🤖', '👽', '👾'
    ];
    return avatars[Math.floor(Math.random() * avatars.length)];
}

// ===== COLOR HELPERS =====
// ===== COLOR HELPERS =====
function getSkillColor(skill) {
    if (skill <= 2) return '#00FF00'; // Green - easy
    if (skill <= 3) return '#FFB703'; // Gold - medium
    if (skill <= 4) return '#FF6B35'; // Coral - hard
    return '#FF00FF'; // Magenta - expert
}

function getReasoningColor(reasoning) {
    if (reasoning <= 2) return '#00D9FF'; // Cyan - low
    if (reasoning <= 3) return '#00FF00'; // Green - medium
    if (reasoning <= 4) return '#FFB703'; // Gold - high
    return '#FF6B35'; // Coral - expert
}

// ===== HELPER FUNCTIONS =====
function isRedSuit(suit) {
    return suit === '♥' || suit === '♦';
}

function getTrumpSuit(trump) {
    return typeof trump === 'object' ? trump.suit : trump;
}

// Export for Node.js/CommonJS (server.js, bot-demo.js)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        createDeck,
        shuffleDeck,
        cardToString,
        cardsEqual,
        getRankValue,
        getCardPoints,
        isHighCard,
        isLowCard,
        isJackCard,
        canPlayCard,
        determineWinner,
        getRandomAvatar,
        getSkillColor,
        getReasoningColor,
        isRedSuit,
        getTrumpSuit
    };
}
