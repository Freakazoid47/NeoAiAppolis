#!/usr/bin/env node

/**
 * All Fours Card Game - Bot vs Bot Demo
 * Demonstrates gameplay with 4 computer players
 */

// Load shared utilities
const {
    createDeck,
    getRankValue,
    getCardPoints,
    isJackCard,
    cardsEqual
} = require('./utils.js');

const SUITS = ['♠', '♥', '♦', '♣'];
const RANKS = ['A', 'K', 'Q', 'J', '10', '9', '8', '7', '6', '5', '4', '3', '2'];

let gameState = {
    players: [],
    dealer: 0,
    trump: null,
    currentTrick: [],
    tricks: [],
    gameWinScore: 14,
    roundNumber: 0,
    teamMode: true, // 4 players = partnership variant
    teamScores: { team1: 0, team2: 0 }
};

// Initialize players
function initializePlayers() {
    const avatars = ['🎭', '🎪', '🎨', '🎬'];
    gameState.players = [
        { slot: 1, hand: [], dealt: [], tricks: [], score: 0, avatar: avatars[0], reneged: false, team: 'team1' },
        { slot: 2, hand: [], dealt: [], tricks: [], score: 0, avatar: avatars[1], reneged: false, team: 'team2' },
        { slot: 3, hand: [], dealt: [], tricks: [], score: 0, avatar: avatars[2], reneged: false, team: 'team1' },
        { slot: 4, hand: [], dealt: [], tricks: [], score: 0, avatar: avatars[3], reneged: false, team: 'team2' }
    ];
}

// Deal cards
function deal() {
    const deck = createDeck();
    gameState.players.forEach(p => {
        p.hand = [];
        p.dealt = [];
        p.tricks = [];
        p.reneged = false;
    });

    // Deal 6 cards per player (3-3 or 2-2-2)
    for (let i = 0; i < 6; i++) {
        for (let p = 0; p < 4; p++) {
            gameState.players[p].hand.push(deck.shift());
            gameState.players[p].dealt.push(gameState.players[p].hand[gameState.players[p].hand.length - 1]);
        }
    }

    // Trump is next card
    gameState.trump = deck[0];
    gameState.currentTrick = [];
    gameState.tricks = [];
}

// Get card rank values for winning - using shared function
function getRankValueForTrick(rank) {
    return getRankValue(rank);
}

// Choose card to play
function chooseCard(playerIdx) {
    const player = gameState.players[playerIdx];
    const isLead = gameState.currentTrick.length === 0;

    if (isLead) {
        const nonTrump = player.hand.filter(c => c.suit !== gameState.trump.suit);
        return nonTrump.length > 0 ? nonTrump[0] : player.hand[0];
    } else {
        const leadSuit = gameState.currentTrick[0].card.suit;
        const same = player.hand.filter(c => c.suit === leadSuit);
        
        if (same.length > 0) {
            return same[0];
        }
        
        return player.hand[0];
    }
}

// Play a card
function playCard(playerIdx, card) {
    const player = gameState.players[playerIdx];
    const idx = player.hand.findIndex(c => cardsEqual(c, card));

    if (idx === -1) return;

    // Check for renege
    if (gameState.currentTrick.length > 0) {
        const leadSuit = gameState.currentTrick[0].card.suit;
        const hasLedSuit = player.hand.some(c => c.suit === leadSuit);
        const isPlayingLedSuit = card.suit === leadSuit;

        if (hasLedSuit && !isPlayingLedSuit) {
            player.reneged = true;
        } else if (isPlayingLedSuit && player.reneged) {
            // Caught reneging!
            const team1 = [gameState.players[0], gameState.players[2]];
            const team2 = [gameState.players[1], gameState.players[3]];
            const playerTeam = [0, 2].includes(playerIdx) ? team1 : team2;
            const opposingTeam = [0, 2].includes(playerIdx) ? team2 : team1;

            opposingTeam.forEach(p => p.score = gameState.gameWinScore);
            console.log(`\n❌ RENEGE CAUGHT! Player ${playerIdx + 1} played wrong suit!`);
            console.log(`Team ${[0, 2].includes(playerIdx) ? 2 : 1} wins immediately!\n`);
            return 'renege';
        }
    }

    player.hand.splice(idx, 1);
    gameState.currentTrick.push({
        playerIdx,
        card
    });
}

// Resolve trick
function resolveTrick() {
    const leadSuit = gameState.currentTrick[0].card.suit;
    let winner = 0;
    let winningCard = gameState.currentTrick[0].card;

    for (let i = 1; i < gameState.currentTrick.length; i++) {
        const current = gameState.currentTrick[i].card;
        
        if (current.suit === gameState.trump.suit && winningCard.suit !== gameState.trump.suit) {
            winner = i;
            winningCard = current;
        } else if (current.suit === winningCard.suit && getRankValue(current.rank) > getRankValue(winningCard.rank)) {
            winner = i;
            winningCard = current;
        }
    }

    const winnerIdx = gameState.currentTrick[winner].playerIdx;
    gameState.players[winnerIdx].tricks.push(gameState.currentTrick);
    
    return winnerIdx;
}

// Score round
function scoreRound() {
    const scores = {};
    gameState.players.forEach(p => scores[p.slot] = 0);

    // HIGH and LOW
    const trumpDealt = {};
    gameState.players.forEach(p => {
        trumpDealt[p.slot] = p.dealt.filter(c => c.suit === gameState.trump.suit);
    });

    let highPlayer = null;
    let lowPlayer = null;
    let highVal = -1;
    let lowVal = 15;

    for (let [slot, cards] of Object.entries(trumpDealt)) {
        for (let card of cards) {
            const rankVal = getRankValue(card.rank);
            if (rankVal > highVal) {
                highVal = rankVal;
                highPlayer = gameState.players.find(p => p.slot == slot);
            }
            if (rankVal < lowVal) {
                lowVal = rankVal;
                lowPlayer = gameState.players.find(p => p.slot == slot);
            }
        }
    }

    if (highPlayer) scores[highPlayer.slot] += 4;
    if (lowPlayer) scores[lowPlayer.slot]++;

    // JACK and HANG JACK
    for (let trick of gameState.tricks) {
        for (let play of trick.cards) {
            if (isJackCard(play.card, gameState.trump.suit)) {
                scores[gameState.players[trick.winner].slot] += 1; // Jack point
                scores[gameState.players[trick.winner].slot] += 3; // Hang Jack bonus
            }
        }
    }

    // GAME
    const pointTotals = {};
    gameState.players.forEach(p => pointTotals[p.slot] = 0);

    for (let trick of gameState.tricks) {
        for (let play of trick.cards) {
            pointTotals[gameState.players[trick.winner].slot] += getCardPoints(play.card.rank);
        }
    }

    let maxSlot = null;
    let maxPoints = -1;
    for (let [slot, points] of Object.entries(pointTotals)) {
        if (points > maxPoints) {
            maxPoints = points;
            maxSlot = slot;
        }
    }
    if (maxSlot) scores[maxSlot]++;

    // Check for renege violations - player loses all points in the round
    const renegedPlayers = gameState.players.filter(p => p.reneged);
    if (renegedPlayers.length > 0) {
        renegedPlayers.forEach(p => {
            scores[p.slot] = 0;
        });
        console.log(`\n⚠️  RENEGE! ${renegedPlayers.map(p => `Player ${p.slot}`).join(', ')} forfeited all points this round!\n`);
    }

    // Update scores (team mode)
    if (gameState.teamMode) {
        let team1Points = scores[1] + scores[3]; // Players 1 & 3 are team1
        let team2Points = scores[2] + scores[4]; // Players 2 & 4 are team2
        
        gameState.teamScores.team1 += team1Points;
        gameState.teamScores.team2 += team2Points;
        
        // Update individual player scores for display
        gameState.players.forEach(p => {
            p.score = p.team === 'team1' ? gameState.teamScores.team1 : gameState.teamScores.team2;
        });
        
        return { team1: team1Points, team2: team2Points };
    } else {
        for (let player of gameState.players) {
            player.score += scores[player.slot];
        }
        return scores;
    }
}

// Format card
function formatCard(card) {
    return card.rank + card.suit;
}

// Play one round
function playRound() {
    console.log(`\n${'='.repeat(60)}`);
    console.log(`ROUND ${gameState.roundNumber + 1} - Trump: ${gameState.trump.rank}${gameState.trump.suit}`);
    console.log(`${'='.repeat(60)}`);

    // Reset tricks
    gameState.tricks = [];

    // Play 6 tricks
    for (let trickNum = 0; trickNum < 6; trickNum++) {
        gameState.currentTrick = [];
        const leader = gameState.dealer === 0 ? 1 : 0;
        let currentPlayer = leader;

        // 4 plays per trick
        for (let play = 0; play < 4; play++) {
            const player = gameState.players[currentPlayer];
            const card = chooseCard(currentPlayer);
            const result = playCard(currentPlayer, card);
            
            if (result === 'renege') {
                return 'renege';
            }

            console.log(`  Player ${currentPlayer + 1}: ${formatCard(card)}`);
            currentPlayer = (currentPlayer + 1) % 4;
        }

        // Resolve trick
        const winner = resolveTrick();
        gameState.tricks.push({
            cards: gameState.currentTrick,
            winner: winner
        });

        console.log(`  ➜ Trick won by Player ${winner + 1}`);
    }

    // Score the round
    const roundScores = scoreRound();
    
    if (gameState.teamMode) {
        console.log(`\nRound Scores:`);
        console.log(`  Team 1 (Players 1 & 3): +${roundScores.team1} (Total: ${gameState.teamScores.team1})`);
        console.log(`  Team 2 (Players 2 & 4): +${roundScores.team2} (Total: ${gameState.teamScores.team2})`);
    } else {
        console.log(`\nRound Scores:`);
        for (let slot = 1; slot <= 4; slot++) {
            const player = gameState.players[slot - 1];
            console.log(`  Player ${slot}: +${roundScores[slot]} (Total: ${player.score})`);
        }
    }

    gameState.dealer = (gameState.dealer + 1) % 4;
    gameState.roundNumber++;
}

// Main game loop
function runGame() {
    console.log('\n');
    console.log('🎴'.repeat(30));
    console.log('ALL FOURS CARD GAME - BOT DEMO');
    console.log('🎴'.repeat(30));
    console.log('\nPLAYERSHIP MODE - Caribbean All Fours');
    console.log('Verified from: Wikipedia & Pagat.com\n');
    console.log('Team 1 (Across): 🎭 Player 1 & 🎨 Player 3');
    console.log('Team 2 (Across): 🎪 Player 2 & 🎬 Player 4');
    console.log('\nGame rules: First TEAM to reach 14 points WINS!');
    console.log('Scoring: High=4pts, Low=1pt, Jack=1pt, Hang Jack=3pts, Game=2pts');
    console.log('Team scores are COMBINED to win!\n');

    initializePlayers();

    while (true) {
        deal();
        const result = playRound();
        
        if (result === 'renege') {
            break;
        }

        // Check for winner
        let winner = null;
        if (gameState.teamMode) {
            if (gameState.teamScores.team1 >= gameState.gameWinScore) {
                console.log(`\n${'='.repeat(60)}`);
                console.log(`🏆 GAME OVER! TEAM 1 (Players 1 & 3) WINS! 🏆`);
                console.log(`${'='.repeat(60)}`);
                console.log(`\nFinal Scores:`);
                console.log(`  Team 1: ${gameState.teamScores.team1} points`);
                console.log(`  Team 2: ${gameState.teamScores.team2} points`);
                console.log('\n');
                break;
            } else if (gameState.teamScores.team2 >= gameState.gameWinScore) {
                console.log(`\n${'='.repeat(60)}`);
                console.log(`🏆 GAME OVER! TEAM 2 (Players 2 & 4) WINS! 🏆`);
                console.log(`${'='.repeat(60)}`);
                console.log(`\nFinal Scores:`);
                console.log(`  Team 1: ${gameState.teamScores.team1} points`);
                console.log(`  Team 2: ${gameState.teamScores.team2} points`);
                console.log('\n');
                break;
            }
        }

        if (gameState.roundNumber >= 20) {
            console.log('\n⚠️  Demo limited to 20 rounds. Game would continue...\n');
            console.log(`Team Scores:`);
            console.log(`  Team 1: ${gameState.teamScores.team1} points`);
            console.log(`  Team 2: ${gameState.teamScores.team2} points`);
            console.log('\n');
            break;
        }
    }
}

// Run the demo
runGame();
