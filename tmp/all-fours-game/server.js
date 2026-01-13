const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
const path = require('path');

// Load shared utilities
const {
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
    getRandomAvatar
} = require('./utils.js');

const app = express();
const server = http.createServer(app);
const io = socketIo(server, {
    cors: {
        origin: "*",
        methods: ["GET", "POST"]
    }
});

// Serve static files
app.use(express.static(path.join(__dirname)));

// Parse JSON requests
app.use(express.json());

// Import AI modules for leaderboard data (when available)
let Leaderboard = null;
try {
    const { Leaderboard: LeaderboardClass } = require('./src/currency/leaderboard.js');
    Leaderboard = LeaderboardClass;
} catch (e) {
    console.log('Leaderboard module not yet available');
}

// API Endpoints
app.get('/api/leaderboard', (req, res) => {
    const sortBy = req.query.sort || 'elo';
    const limit = parseInt(req.query.limit) || 50;

    if (!Leaderboard) {
        return res.json({
            leaderboard: [],
            statistics: {
                totalPlayers: 0,
                totalGamesPlayed: 0,
                totalTokensIssued: 0,
                averageELO: 1600
            },
            queue: {
                waitingPlayers: 0,
                activeMatches: 0
            }
        });
    }

    try {
        const leaderboard = Leaderboard.getByELO(limit);
        const stats = Leaderboard.getStatistics();
        
        res.json({
            leaderboard,
            statistics: stats,
            queue: {
                waitingPlayers: 0,
                activeMatches: 0
            }
        });
    } catch (error) {
        console.error('Error fetching leaderboard:', error);
        res.status(500).json({ error: 'Failed to fetch leaderboard' });
    }
});

app.get('/api/leaderboard/elo', (req, res) => {
    const limit = parseInt(req.query.limit) || 50;
    if (!Leaderboard) return res.json([]);
    
    try {
        const data = Leaderboard.getByELO(limit);
        res.json(data);
    } catch (error) {
        res.status(500).json({ error: 'Failed to fetch ELO leaderboard' });
    }
});

app.get('/api/leaderboard/winrate', (req, res) => {
    const limit = parseInt(req.query.limit) || 50;
    const minGames = parseInt(req.query.minGames) || 5;
    if (!Leaderboard) return res.json([]);
    
    try {
        const data = Leaderboard.getByWinRate(limit, minGames);
        res.json(data);
    } catch (error) {
        res.status(500).json({ error: 'Failed to fetch win rate leaderboard' });
    }
});

app.get('/api/leaderboard/tokens', (req, res) => {
    const limit = parseInt(req.query.limit) || 50;
    if (!Leaderboard) return res.json([]);
    
    try {
        const data = Leaderboard.getByTokens(limit);
        res.json(data);
    } catch (error) {
        res.status(500).json({ error: 'Failed to fetch tokens leaderboard' });
    }
});

app.get('/api/players/:playerId/rank', (req, res) => {
    const { playerId } = req.params;
    const sortBy = req.query.sort || 'elo';
    
    if (!Leaderboard) {
        return res.json({ rank: null, player: null });
    }
    
    try {
        const rank = Leaderboard.getPlayerRank(playerId, sortBy);
        res.json({ rank });
    } catch (error) {
        res.status(500).json({ error: 'Failed to fetch player rank' });
    }
});

app.get('/api/stats', (req, res) => {
    if (!Leaderboard) {
        return res.json({
            totalPlayers: 0,
            totalGamesPlayed: 0,
            totalTokensIssued: 0,
            averageELO: 1600
        });
    }
    
    try {
        const stats = Leaderboard.getStatistics();
        res.json(stats);
    } catch (error) {
        res.status(500).json({ error: 'Failed to fetch statistics' });
    }
});

// Health check endpoint
app.get('/health', (req, res) => {
    res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// Game rooms storage
const gameRooms = new Map();

// Player sockets storage
const playerSockets = new Map();

// Room rules storage
const roomRules = new Map();

// Generate random room code
function generateRoomCode() {
    return Math.random().toString(36).substring(2, 8).toUpperCase();
}

// Game room logic
class GameRoom {
    constructor(roomCode) {
        this.roomCode = roomCode;
        this.players = [];
        this.status = 'waiting'; // waiting, playing, finished
        this.gameState = {
            players: [],
            dealer: 0,
            trump: null,
            currentTrick: [],
            tricks: [],
            currentPlayerIndex: 0,
            phase: 'dealing' // dealing, playing, scoring
        };
    }
    
    addPlayer(playerData) {
        if (this.players.length >= 4) return false;
        
        const playerIndex = this.players.length;
        this.players.push({
            ...playerData,
            index: playerIndex,
            socketId: null,
            score: 0
        });
        
        return playerIndex;
    }
    
    startGame() {
        if (this.players.length < 2) return false;
        
        this.status = 'playing';
        this.gameState.players = this.players.map((p, idx) => ({
            index: idx,
            playerIndex: idx,
            name: p.name,
            avatar: p.avatar,
            skill: p.skill,
            reasoning: p.reasoning,
            hand: [],
            dealt: [],
            tricks: [],
            score: 0
        }));
        
        this.dealRound();
        return true;
    }
    
    dealRound() {
        const deck = createDeck();
        const trump = deck[deck.length - 1];
        this.gameState.trump = trump;
        
        // Deal 6 cards to each player (3 at a time in All Fours)
        let deckIndex = 0;
        const cardsPerPlayer = 6;
        
        for (let i = 0; i < cardsPerPlayer; i++) {
            for (let j = 0; j < this.gameState.players.length; j++) {
                if (deckIndex < deck.length) {
                    this.gameState.players[j].hand.push(deck[deckIndex]);
                    this.gameState.players[j].dealt.push(deck[deckIndex]);
                    deckIndex++;
                }
            }
        }
        
        this.gameState.phase = 'playing';
        this.gameState.currentPlayerIndex = (this.gameState.dealer + 1) % this.gameState.players.length;
        this.gameState.currentTrick = [];
    }
    
    playCard(playerIndex, card) {
        const player = this.gameState.players[playerIndex];
        
        // Validate card is in hand
        const cardIndex = player.hand.findIndex(c => cardsEqual(c, card));
        if (cardIndex === -1) return { success: false, error: 'Card not in hand' };
        
        // Validate can play this card
        if (!canPlayCard(card, this.gameState.currentTrick, player.hand, this.gameState.trump.suit)) {
            return { success: false, error: 'Invalid play - must follow suit' };
        }
        
        // Remove from hand
        player.hand.splice(cardIndex, 1);
        
        // Add to current trick
        this.gameState.currentTrick.push({
            playerIndex: playerIndex,
            card: card
        });
        
        // Check if trick is complete
        if (this.gameState.currentTrick.length === this.gameState.players.length) {
            this.resolveTrick();
        } else {
            this.gameState.currentPlayerIndex = (this.gameState.currentPlayerIndex + 1) % this.gameState.players.length;
        }
        
        return { success: true };
    }
    
    resolveTrick() {
        const winnerTrick = determineWinner(this.gameState.currentTrick, this.gameState.trump.suit);
        const winnerPlayerIndex = typeof winnerTrick === 'number' ? winnerTrick : winnerTrick.playerIndex;
        
        this.gameState.players[winnerPlayerIndex].tricks.push(this.gameState.currentTrick);
        
        this.gameState.currentTrick = [];
        this.gameState.currentPlayerIndex = winnerPlayerIndex;
        
        // Check if round is over (no more cards)
        if (this.gameState.players[0].hand.length === 0) {
            this.roundOver();
        }
    }
    
    roundOver() {
        this.scoreRound();
        
        // Reset for next round
        this.gameState.players.forEach(p => {
            p.tricks = [];
            p.hand = [];
            p.dealt = [];
        });
        
        this.gameState.dealer = (this.gameState.dealer + 1) % this.gameState.players.length;
        this.gameState.phase = 'scoring';
    }
    
    scoreRound() {
        const trump = this.gameState.trump.suit;
        const roundScores = {};
        
        // Initialize scores
        this.gameState.players.forEach(p => roundScores[p.playerIndex] = 0);
        
        // HIGH: Highest trump dealt
        const highPlayer = this.getHighCardPlayer(trump);
        if (highPlayer) roundScores[highPlayer.playerIndex]++;
        
        // LOW: Lowest trump dealt
        const lowPlayer = this.getLowCardPlayer(trump);
        if (lowPlayer) roundScores[lowPlayer.playerIndex]++;
        
        // JACK: Won jack of trump in tricks
        for (let player of this.gameState.players) {
            for (let trick of player.tricks) {
                for (let play of trick) {
                    if (isJackCard(play.card, trump)) {
                        roundScores[player.playerIndex]++;
                        roundScores[player.playerIndex] += 3; // Hang Jack bonus
                    }
                }
            }
        }
        
        // GAME: Highest card points total
        const gamePlayer = this.getGamePointsPlayer();
        if (gamePlayer) roundScores[gamePlayer]++;
        
        // Update player scores
        for (let player of this.gameState.players) {
            player.score += roundScores[player.playerIndex];
        }
    }
    
    getHighCardPlayer(trump) {
        let highest = null;
        let highPlayer = null;
        for (let player of this.gameState.players) {
            for (let card of player.dealt) {
                if (card.suit === trump) {
                    if (!highest || getRankValue(card.rank) > getRankValue(highest.rank)) {
                        highest = card;
                        highPlayer = player;
                    }
                }
            }
        }
        return highPlayer;
    }
    
    getLowCardPlayer(trump) {
        let lowest = null;
        let lowPlayer = null;
        for (let player of this.gameState.players) {
            for (let card of player.dealt) {
                if (card.suit === trump) {
                    if (!lowest || getRankValue(card.rank) < getRankValue(lowest.rank)) {
                        lowest = card;
                        lowPlayer = player;
                    }
                }
            }
        }
        return lowPlayer;
    }
    
    getGamePointsPlayer() {
        const pointTotals = {};
        this.gameState.players.forEach(p => pointTotals[p.playerIndex] = 0);
        
        for (let player of this.gameState.players) {
            for (let trick of player.tricks) {
                for (let play of trick) {
                    pointTotals[player.playerIndex] += getCardPoints(play.card.rank);
                }
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
        return maxSlot;
    }
}

// Socket.io event handlers
io.on('connection', (socket) => {
    console.log('New player connected:', socket.id);
    
    socket.on('create-game', (playerData) => {
        const roomCode = generateRoomCode();
        const room = new GameRoom(roomCode);
        const playerIndex = room.addPlayer(playerData);
        
        gameRooms.set(roomCode, room);
        playerSockets.set(socket.id, { roomCode, playerIndex });
        
        socket.join(roomCode);
        socket.emit('game-created', { 
            roomCode, 
            playerIndex,
            players: room.players 
        });
    });
    
    socket.on('join-game', (data) => {
        const { roomCode, playerData } = data;
        const room = gameRooms.get(roomCode);
        
        if (!room) {
            socket.emit('join-error', 'Room not found');
            return;
        }
        
        if (room.players.length >= 4) {
            socket.emit('join-error', 'Game is full');
            return;
        }
        
        const playerIndex = room.addPlayer(playerData);
        playerSockets.set(socket.id, { roomCode, playerIndex });
        
        socket.join(roomCode);
        io.to(roomCode).emit('player-joined', { 
            playerIndex,
            playerData,
            players: room.players,
            rules: roomRules.get(roomCode)
        });
    });
    
    socket.on('update-rules', (data) => {
        const { roomCode, rules } = data;
        if (!gameRooms.has(roomCode)) return;
        
        // Store rules
        roomRules.set(roomCode, rules);
        
        // Broadcast to all players in room
        io.to(roomCode).emit('rules-updated', { rules });
    });
    
    socket.on('start-game', (data) => {
        const { roomCode } = data;
        const room = gameRooms.get(roomCode);
        
        if (!room) return;
        if (room.players.length < 2) {
            socket.emit('start-error', 'Need at least 2 players');
            return;
        }
        
        room.startGame();
        io.to(roomCode).emit('game-started', room.gameState);
    });
    
    socket.on('play-card', (data) => {
        const { roomCode, card } = data;
        const room = gameRooms.get(roomCode);
        const playerInfo = playerSockets.get(socket.id);
        
        if (!room || !playerInfo) return;
        
        const result = room.playCard(playerInfo.playerIndex, card);
        
        if (result.success) {
            io.to(roomCode).emit('game-state', room.gameState);
        } else {
            socket.emit('play-error', result.error);
        }
    });

    socket.on('add-ai-player', (data) => {
        const { roomCode, aiData } = data;
        const room = gameRooms.get(roomCode);
        
        if (!room) {
            socket.emit('error', 'Room not found');
            return;
        }
        
        if (room.players.length >= 4) {
            socket.emit('error', 'Game is full (4 players max)');
            return;
        }
        
        // Add the AI player to the room
        const playerIndex = room.addPlayer(aiData);
        
        // Broadcast to all players in room that an AI player joined
        io.to(roomCode).emit('ai-player-added', {
            playerIndex: playerIndex,
            playerData: aiData,
            players: room.players
        });
    });
    
    socket.on('disconnect', () => {
        const playerInfo = playerSockets.get(socket.id);
        if (playerInfo) {
            const room = gameRooms.get(playerInfo.roomCode);
            if (room) {
                io.to(playerInfo.roomCode).emit('player-disconnected', {
                    playerIndex: playerInfo.playerIndex
                });
            }
            playerSockets.delete(socket.id);
        }
        console.log('Player disconnected:', socket.id);
    });
});

const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
    console.log(`All Fours server running on http://localhost:${PORT}`);
});
