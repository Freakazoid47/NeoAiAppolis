# All Fours Game - Architecture Documentation

## System Overview

```
┌─────────────────┐
│   Web Browser   │
│  (Player 1)     │
└────────┬────────┘
         │ HTTP/WebSocket
         │
    ┌────▼────────────────────┐
    │  Express.js Server      │
    │  ├─ Static Files        │
    │  ├─ Socket.io Server    │
    │  └─ Game Logic          │
    └────┬───────────────────┘
         │
    ┌────▼──────────────────┐
    │  In-Memory Game State │
    │  ├─ Players           │
    │  ├─ Cards             │
    │  └─ Scores            │
    └───────────────────────┘
```

## Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | Vanilla JS, HTML5, CSS3 | User interface & interactions |
| **Real-time** | Socket.io | WebSocket communication |
| **Backend** | Node.js + Express | HTTP server & game logic |
| **Data** | In-memory (future: MongoDB/PostgreSQL) | Game state storage |
| **Hosting** | Docker-ready (Railway/Heroku/DigitalOcean) | Production deployment |

## Project Structure

```
all-fours-game/
├── server.js                    # Entry point - Express app setup
├── game.js                      # Game logic (currently client-side)
├── socket-client.js             # Client-side Socket.io logic
│
├── public/                      # Static files served to browser
│   ├── index.html              # HTML structure & UI
│   ├── style.css               # Jujutsu Kaisen theme styling
│   ├── game.js                 # Game logic & mechanics
│   └── socket-client.js        # Real-time game communication
│
├── .env.example                # Environment variables template
├── Dockerfile                  # Docker containerization
├── Procfile                    # Heroku/Railway configuration
├── package.json                # Dependencies & scripts
│
├── docs/
│   ├── PRODUCTION_ROADMAP.md   # Full launch roadmap
│   ├── DEPLOYMENT.md           # Deployment guides
│   └── ARCHITECTURE.md         # This file
│
└── tests/ (coming soon)
    ├── unit/
    ├── integration/
    └── e2e/
```

## Current Architecture (MVP)

### 1. Frontend (Client-Side)

**Entry Point:** `public/index.html`

Components:
- **Menu Screen** - Game selection
- **Lobby Screen** - Player selection (local mode)
- **Game Screen** - Active gameplay
- **Scoreboard** - Real-time score tracking

**Technologies:**
- Vanilla JavaScript (no frameworks)
- CSS3 with Jujutsu Kaisen theming
- Socket.io client for multiplayer

### 2. Game Logic

**File:** `public/game.js`

Core Functions:
```javascript
// Game State
gameState = {
  players: [],
  currentPlayerIndex: 0,
  dealer: 0,
  trump: null,
  currentTrick: [],
  phase: 'lobby' | 'dealing' | 'playing' | 'scoring'
}

// Main Functions
dealRound()        // Deal cards
playRound()        // Execute round
playCard()         // Card selection logic
scoreRound()       // Calculate points
```

**Game Logic Flow:**
```
1. Lobby (Player Selection)
   ↓
2. Deal (Distribute 6 cards each)
   ↓
3. Play (4 tricks, follow suit rules)
   ↓
4. Score (High, Low, Jack, Game)
   ↓
5. Check Win (First to 11 points)
   ↓
6. Loop or Game Over
```

### 3. Backend Server

**File:** `server.js`

```javascript
const express = require('express');
const http = require('http');
const socketIo = require('socket.io');

// Express app setup
app.use(express.static('public')); // Serve frontend
app.get('/', (req, res) => {...}); // Root route

// Socket.io for real-time communication
io.on('connection', (socket) => {
  socket.on('play-card', ...)
  socket.on('join-game', ...)
  socket.on('game-over', ...)
})
```

**Current Features:**
- Serves static files from `/public`
- WebSocket server for multiplayer
- In-memory game state (not persisted)

## Data Flow

### Single Player Game
```
User Input → game.js → UI Update → localStorage (optional)
```

### Multiplayer Game (Future)
```
Player 1 Input
    ↓
socket.emit('play-card', card)
    ↓
Server validates & updates state
    ↓
socket.emit('card-played') → All players
    ↓
Client updates UI
```

## Real-Time Communication (Socket.io)

Current events (to be implemented):
```javascript
// Client to Server
socket.emit('create-game')
socket.emit('join-game', {roomCode, playerData})
socket.emit('play-card', {card, playerIndex})
socket.emit('start-game', {roomCode})

// Server to Client
socket.on('game-started', (gameState) => {})
socket.on('card-played', (trick) => {})
socket.on('round-over', (scores) => {})
socket.on('game-over', (winner) => {})
```

## Styling & Theme

**File:** `public/style.css`

```css
:root {
  --primary: #FF1744;         /* Blood red */
  --secondary: #1A0E2E;       /* Dark purple */
  --accent: #A90E4A;          /* Deep magenta */
  --gold: #FFD700;            /* Curse energy */
  --curse-dark: #0D0221;      /* Darkest */
  --curse-purple: #6B2C72;    /* Purple haze */
  --curse-red: #D00000;       /* Curse mark */
}
```

**Theme Inspiration:** Jujutsu Kaisen anime
- Dark color palette (curses/darkness)
- Glowing effects (curse energy)
- Smooth animations (combat style)

## Game Rules Implementation

### Card Validity
```javascript
canPlayCard(card, currentTrick, playerHand, trump) {
  // Must follow suit if able
  // Must play trump if trumped and able
  // Otherwise play any card
}
```

### Winner Determination
```javascript
determineWinner(trick, trump) {
  // Highest card of led suit wins
  // Or highest trump if trump played
  // Return winning player index
}
```

### Point Calculation
```javascript
scoreRound() {
  // High: highest trump in dealt hand (4 pts)
  // Low: lowest trump in dealt hand (1 pt)
  // Jack: won Jack of trump (1 pt)
  // Game: highest total card points (1 pt)
}
```

## Scaling Strategy

### Phase 1 (MVP - Current)
- Single server instance
- In-memory game state
- Local multiplayer only
- No persistence

### Phase 2 (Beta - Near Term)
- Database (MongoDB/PostgreSQL)
- User authentication
- Game history storage
- Leaderboards
- Load balancer (if needed)

### Phase 3 (Production)
- Microservices architecture
- Redis caching
- CDN for static assets
- Message queue (RabbitMQ/Redis)
- Multiple server instances

```
┌──────────────┐
│ Load Balancer│
└──────┬───────┘
       │
   ┌───┴───┬───────┬───────┐
   │       │       │       │
┌──▼──┐ ┌─▼──┐ ┌──▼──┐ ┌─▼──┐
│ Srv1│ │Srv2│ │Srv3│ │Srv4│  (Node servers)
└──┬──┘ └─┬──┘ └──┬──┘ └─┬──┘
   │      │      │      │
   └──────┴──────┴──────┘
          │
     ┌────▼────┐
     │  Redis  │  Cache + Queue
     └────┬────┘
     ┌────▼──────┐
     │ Database  │
     └───────────┘
```

## Performance Considerations

### Current Bottlenecks
1. No database (state lost on server restart)
2. No caching layer
3. No CDN for static assets
4. No load balancing

### Optimizations (Roadmap)
- Implement Redis caching
- Compress game state transfers
- Lazy-load player cards
- Minimize socket.io messages
- Use WebSocket compression

### Expected Performance
- Player latency: <100ms
- Server can handle 100+ concurrent games
- Database queries: <50ms with proper indexing

## Security Architecture

### Current Level
- Basic input validation
- No authentication

### Required for Production
```
┌─────────────┐
│  HTTPS/SSL  │
└──────┬──────┘
       │
├─ Session Management (JWT)
├─ Input Validation
├─ Rate Limiting
├─ CORS Configuration
├─ Game Logic Validation
└─ Secure Headers
```

### Implementation
```javascript
// Helmet for security headers
app.use(helmet());

// Rate limiting
app.use(rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100
}));

// CORS
app.use(cors({
  origin: process.env.SOCKET_ORIGIN,
  credentials: true
}));

// Input validation
validateCardPlay(card, playerHand)
```

## Testing Strategy

```
Unit Tests (game logic)
├─ Card validity rules
├─ Score calculation
├─ Winner determination
└─ Hand mechanics

Integration Tests
├─ Game flow
├─ Multi-player sync
├─ Socket.io communication
└─ Database operations

E2E Tests
├─ Full game flow
├─ User interactions
├─ Error handling
└─ Performance
```

## Deployment Architecture

### Development
```
Local Machine
├─ npm start
├─ localhost:3000
└─ In-memory state
```

### Production
```
┌──────────────────┐
│  Git Repository  │
└────────┬─────────┘
         │
    ┌────▼──────────┐
    │ CI/CD Pipeline │
    │ (GitHub Actions)
    └────┬──────────┘
         │
  ┌──────▼──────────┐
  │ Docker Image    │
  └────────┬────────┘
         │
  ┌──────▼──────────────┐
  │ Cloud Hosting       │
  │ (Railway/Heroku/DO) │
  └────────┬────────────┘
         │
  ┌──────▼──────────────┐
  │ Load Balancer       │
  │ Custom Domain       │
  │ SSL Certificate     │
  └─────────────────────┘
```

## Monitoring & Observability

### Metrics to Track
- Request/Response times
- Player count & sessions
- Game duration
- Error rates
- Database query times
- WebSocket latency

### Tools
- **Logging:** Winston/Pino
- **Error Tracking:** Sentry
- **Monitoring:** DataDog/New Relic
- **Analytics:** Google Analytics
- **Uptime:** UptimeRobot

## Future Architecture Improvements

1. **Microservices**
   - Auth Service
   - Game Service
   - Leaderboard Service
   - Notification Service

2. **Event-Driven Architecture**
   - Replace direct calls with events
   - Implement message queue
   - Better decoupling

3. **API Versioning**
   - `/api/v1/*` endpoints
   - Backwards compatibility

4. **GraphQL Option**
   - Replace REST with GraphQL
   - Better type safety
   - Reduced over-fetching

## Glossary

| Term | Definition |
|------|-----------|
| **Trump** | The card suit chosen for the current deal |
| **Trick** | One round of 4 cards (one per player) |
| **Hand** | Cards a player holds |
| **Dealt** | Cards originally dealt (for scoring) |
| **High** | Highest trump card in dealt hand |
| **Low** | Lowest trump card in dealt hand |
| **Jack** | The Jack of the trump suit (1 point if won) |
| **Game** | Highest total point value in tricks |

---

**Last Updated:** January 2026
**Status:** MVP Complete, Production Roadmap Defined
