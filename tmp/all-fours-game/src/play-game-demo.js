#!/usr/bin/env node

/**
 * All Fours Live Game Demo - Automated Gameplay
 * This script automates a complete game with 4 bots
 */

const io = require('socket.io-client');

const socket = io('http://localhost:3000', {
    reconnection: true,
    reconnectionDelay: 1000,
    reconnectionDelayMax: 5000,
    reconnectionAttempts: Infinity
});

let gameState = {
    roomCode: null,
    playerSlot: null,
    gameStarted: false,
    roundNumber: 0,
    teamScores: { team1: 0, team2: 0 }
};

// Game constants
const SUITS = ['♠', '♥', '♦', '♣'];
const RANKS = ['A', 'K', 'Q', 'J', '10', '9', '8', '7', '6', '5', '4', '3', '2'];

function log(message) {
    console.log(`[${new Date().toLocaleTimeString()}] ${message}`);
}

socket.on('connect', () => {
    log('✅ Connected to server!');
    
    // Create a game room
    socket.emit('create-room', { playerName: 'Demo Host' }, (response) => {
        if (response.success) {
            gameState.roomCode = response.roomCode;
            gameState.playerSlot = response.playerSlot;
            log(`✅ Room created: ${gameState.roomCode}`);
            log(`📍 You are Player ${gameState.playerSlot}`);
            
            // Wait a moment then add AI players
            setTimeout(() => {
                socket.emit('join-room', {
                    roomCode: gameState.roomCode,
                    playerSlot: 2,
                    playerName: 'Bot 2',
                    isAI: true
                });
                
                setTimeout(() => {
                    socket.emit('join-room', {
                        roomCode: gameState.roomCode,
                        playerSlot: 3,
                        playerName: 'Bot 3',
                        isAI: true
                    });
                    
                    setTimeout(() => {
                        socket.emit('join-room', {
                            roomCode: gameState.roomCode,
                            playerSlot: 4,
                            playerName: 'Bot 4',
                            isAI: true
                        });
                        
                        // Start game after all players join
                        setTimeout(() => {
                            log('🎮 Starting game with 4 players...');
                            socket.emit('start-game', { roomCode: gameState.roomCode });
                        }, 500);
                    }, 300);
                }, 300);
            }, 300);
        }
    });
});

socket.on('room-updated', (data) => {
    log(`👥 Room updated - Players in room: ${data.playerCount}`);
});

socket.on('game-started', (data) => {
    gameState.gameStarted = true;
    gameState.roundNumber++;
    log(`\n${'='.repeat(60)}`);
    log(`ROUND ${gameState.roundNumber} STARTED`);
    log(`Trump Suit: ${data.trump ? data.trump.suit : '?'}`);
    log(`${'='.repeat(60)}`);
});

socket.on('hand-dealt', (data) => {
    if (data.hand && data.hand.length > 0) {
        log(`🎴 Your hand: ${data.hand.map(c => c.rank + c.suit).join(', ')}`);
    }
});

socket.on('turn-to-play', (data) => {
    log(`➡️  Your turn to play`);
    
    // Auto-select and play a card
    if (data.hand && data.hand.length > 0) {
        const cardToPlay = data.hand[0];
        setTimeout(() => {
            socket.emit('play-card', {
                roomCode: gameState.roomCode,
                card: cardToPlay,
                playerSlot: gameState.playerSlot
            });
            log(`  Played: ${cardToPlay.rank}${cardToPlay.suit}`);
        }, 800);
    }
});

socket.on('card-played', (data) => {
    log(`  Player ${data.playerSlot} played: ${data.card.rank}${data.card.suit}`);
});

socket.on('trick-won', (data) => {
    log(`✅ Trick won by Player ${data.winnerSlot}`);
});

socket.on('round-scores', (data) => {
    log(`\n📊 ROUND SCORES:`);
    
    if (data.teamMode) {
        log(`Team 1 (Players 1 & 3): +${data.team1Score} points`);
        log(`Team 2 (Players 2 & 4): +${data.team2Score} points`);
        gameState.teamScores.team1 += data.team1Score;
        gameState.teamScores.team2 += data.team2Score;
        log(`\nCUMULATIVE TEAM SCORES:`);
        log(`Team 1: ${gameState.teamScores.team1} points`);
        log(`Team 2: ${gameState.teamScores.team2} points`);
    } else {
        for (let i = 1; i <= 4; i++) {
            const score = data[`player${i}Score`] || 0;
            log(`Player ${i}: +${score} points`);
        }
    }
    log('');
});

socket.on('game-over', (data) => {
    log(`\n${'='.repeat(60)}`);
    log(`🏆 GAME OVER! WINNER ANNOUNCED`);
    log(`${'='.repeat(60)}`);
    
    if (data.winnerTeam) {
        log(`🎉 ${data.winnerTeam.toUpperCase()} WINS!`);
        log(`Final Team Scores:`);
        log(`  Team 1: ${gameState.teamScores.team1} points`);
        log(`  Team 2: ${gameState.teamScores.team2} points`);
    } else if (data.winnerSlot) {
        log(`🎉 Player ${data.winnerSlot} WINS!`);
    }
    log(`${'='.repeat(60)}\n`);
    
    // Disconnect after game ends
    setTimeout(() => {
        log('Disconnecting from server...');
        socket.disconnect();
        process.exit(0);
    }, 2000);
});

socket.on('error', (error) => {
    log(`❌ Error: ${error}`);
});

socket.on('disconnect', () => {
    log('Disconnected from server');
});

socket.on('connect_error', (error) => {
    log(`❌ Connection error: ${error.message}`);
});

// Timeout failsafe
setTimeout(() => {
    log('Demo timeout - game did not complete within reasonable time');
    socket.disconnect();
    process.exit(1);
}, 120000); // 2 minute timeout
