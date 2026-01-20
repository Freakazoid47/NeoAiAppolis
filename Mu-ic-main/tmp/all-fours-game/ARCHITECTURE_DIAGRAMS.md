# 🎴 All Fours AI System - Architecture Diagram

## System Overview

```
┌──────────────────────────────────────────────────────────────────────────┐
│                         All Fours AI Tournament                          │
└──────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                          Web Dashboard                                  │
│  public/dashboard/index.html                                           │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │ • Leaderboard Display (ELO, Win Rate, Tokens)                 │  │
│  │ • Statistics Cards (Players, Games, Tokens, Avg ELO)          │  │
│  │ • Queue Status (Waiting, Active Matches)                      │  │
│  │ • Auto-refresh every 5 seconds                                │  │
│  └─────────────────────────────────────────────────────────────────┘  │
└────────────────────┬────────────────────────────────────────────────────┘
                     │
        ┌────────────▼────────────┐
        │   API Endpoints         │
        │  (server.js)            │
        │ ┌──────────────────────┐│
        │ │ GET /api/leaderboard ││
        │ │ GET /api/stats       ││
        │ │ GET /health          ││
        │ └──────────────────────┘│
        └────────────┬────────────┘
                     │
        ┌────────────▼────────────┐
        │  Leaderboard System     │
        │ src/currency/           │
        │ leaderboard.js          │
        │ ┌──────────────────────┐│
        │ │ getByELO()           ││
        │ │ getByWinRate()       ││
        │ │ getByTokens()        ││
        │ │ getStatistics()      ││
        │ └──────────────────────┘│
        └────────────┬────────────┘
                     │
           ┌─────────┴─────────┐
           │                   │
    ┌──────▼──────┐    ┌──────▼──────┐
    │   Players   │    │   Matches   │
    │  (AIPlayer) │    │  (Match)    │
    └──────▲──────┘    └──────▲──────┘
           │                   │
           │                   │
    ┌──────┴───────────┬───────┴──────┐
    │                  │               │
┌───▼────┐      ┌─────▼────┐    ┌────▼────┐
│ AI     │      │   Match  │    │Currency │
│Adapter │      │  Queue   │    │Reward   │
│        │      │          │    │System   │
│OpenAI  │      │BullMQ    │    │         │
│Claude  │      │Job Queue │    │ELO Calc │
│Local   │      │          │    │Tokens   │
└────────┘      └──────────┘    └─────────┘
```

## Component Interactions

### 1. Match Lifecycle

```
Player Enrollment
       │
       ▼
Queue in Leaderboard System
       │
       ▼
Match Queue (BullMQ)
       │
       ▼
Automatic Matching (2-4 players)
       │
       ▼
┌─────────────────────────────────┐
│      Game Simulation            │
│                                 │
│  1. Deal cards                  │
│  2. Set trump suit              │
│  3. For each round:             │
│     - AI decisions via Adapter  │
│     - Trick resolution          │
│     - Scoring                   │
│  4. Continue until 21 points    │
└─────────────────────────────────┘
       │
       ▼
Result Processing
       │
       ▼
┌─────────────────────────────────┐
│   Currency & ELO Update         │
│                                 │
│  For each player:               │
│  • Calculate ELO change         │
│  • Calculate token reward       │
│  • Update leaderboard           │
│  • Store match result           │
└─────────────────────────────────┘
       │
       ▼
Dashboard Update (via API)
```

### 2. AI Decision Flow

```
Game State
(trump, cards played, hand)
       │
       ▼
AIAdapter.chooseCard()
       │
       ├─────────────────────┐
       │                     │
   Is Model?                 │
   │     │     │             │
GPT │Claude│Local            │
   │     │     │             │
   ▼     ▼     ▼             │
  API   API  Local Model     │
   │     │     │             │
   └─────┴─────┘             │
       │                     │
       ▼                     │
buildPrompt()               │
(detailed game context)     │
       │                     │
       ▼                     │
Parse Response
       │
       ├─ Success: Return card
       │
       └─ Failure: Return first playable card
```

### 3. Reward Calculation Flow

```
Match Results
(winner, points, participants)
       │
       ▼
calculateReward()
       │
       ├─ Base Reward: 100 tokens
       │
       ├─ Points Bonus: points × 5
       │
       ├─ ELO Multiplier: (avgOpp - playerELO) × 0.1
       │
       ├─ Win/Loss Multiplier: 1.5× / 0.5×
       │
       ├─ Streak Bonus: 50 × wins (after 3-win streak)
       │
       └─ Placement Bonus: 1000/500/250/100 (1st-4th)
           │
           ▼
       Total Tokens = Weighted Sum
           │
           ▼
       Update Player Token Balance
       Update ELO Rating
       Update Leaderboard
```

## Data Flow Diagram

```
┌──────────────────────────────────────────────────────────────────┐
│                    Real-Time Tournament                          │
└──────────────────────────────────────────────────────────────────┘
         ▲                                                    ▲
         │                                                    │
    ┌────┴──────────────────────┬─────────────────────┬──────┴────┐
    │                           │                     │           │
┌───▼───┐              ┌────────▼────┐      ┌────────▼───┐   ┌───▼──┐
│Player1│              │   AI Queue   │      │  Matches   │   │Stats │
│(GPT4) │              │   (2-4 pts)  │      │  Running   │   │DB    │
└───┬───┘              └────────▲────┘      └────────┬───┘   └───┬──┘
    │                          │                      │            │
    │ Register with ELO 1600   │                      │ Results    │
    ├─────────────────────────►│                      │            │
    │                          │                      │            │
    │                          │ Match 1:            │            │
    │                          │ P1 vs P3 vs P5     │            │
    │                          │                     ▼            │
    │                          │                  ┌──────────┐    │
    │                          │                  │Play Game │    │
    │                          │                  │& Score  │    │
    │                          │                  └────┬─────┘    │
    │                          │                       │           │
    │                          │                       ▼           │
    │                          │                  ┌──────────────┐ │
    │                          └──────────────────►│ Rewards &   │ │
    │                                              │ ELO Update  ├─┤
    │                                              │             │ │
    │                                              │ P1: +25 ELO │ │
    │                                              │     +250 tk │ │
    │                                              └────┬────────┘ │
    │                                                    │          │
    │                                              ┌─────▼──────┐  │
    │                                              │Leaderboard │  │
    │                                              │ Updated    │  │
    │                                              └────┬───────┘  │
    │                                                    │          │
    └────────────────────────────────────────────────────┼──────────┘
                                                         │
                                                    ┌────▼─────┐
                                                    │ Dashboard│
                                                    │ Refreshes│
                                                    └──────────┘
```

## Class Relationships

```
┌─────────────────┐
│   AIAdapter     │
│ (src/ai/)       │
├─────────────────┤
│ - modelType     │
│ - modelName     │
│ - temperature   │
├─────────────────┤
│ chooseCard()    │
│ callOpenAI()    │
│ callAnthropic() │
│ parseCard()     │
└────────┬────────┘
         │ uses
         │
┌────────▼────────┐          ┌──────────────┐
│   AIPlayer      │          │  Leaderboard │
│ (src/ai/)       │          │ (src/currency)
├─────────────────┤          ├──────────────┤
│ - id            │          │ - players{}  │
│ - eloRating     │          │ - stats      │
│ - gamesPlayed   │          ├──────────────┤
│ - tokensEarned  │          │ getByELO()   │
├─────────────────┤          │ getByWinRate()
│ makeMove()      │          │ getByTokens()│
│ updateELO()     │          └──────────────┘
│ getSummary()    │               ▲
└────────┬────────┘               │ contains
         │ participates           │
         │                        │
┌────────▼──────────────────────┐ │
│   Match                       │ │
│ (src/match/)                  │ │
├────────────────────────────────┤ │
│ - players: AIPlayer[]          │ │
│ - gameState                    │ │
│ - currentRound                 │ │
├────────────────────────────────┤ │
│ play()                         │ │
│ playRound()                    │ │
│ playTrick()                    │─┘
│ scoreRound()                   │
└────────┬──────────────────────┘
         │ managed by
         │
┌────────▼──────────────┐
│ MatchQueue           │
│ (src/match/)         │
├───────────────────────┤
│ - queue: Player[]     │
│ - activeMatches: Map  │
│ - bullQueue (BullMQ)  │
├───────────────────────┤
│ queuePlayer()         │
│ tryMatchPlayers()     │
│ handleMatchResult()   │
└───────────────────────┘
         │ uses
         │
┌────────▼──────────────┐
│ Currency             │
│ (src/currency/)      │
├───────────────────────┤
│ calculateReward()     │
│ calculateStreakBonus()│
│ calculateTournament() │
└───────────────────────┘
```

## Request/Response Flow (API)

```
Dashboard Browser Request
        │
        ▼
GET /api/leaderboard?sort=elo&limit=50
        │
        ▼
Express Server (server.js)
        │
        ▼
┌───────────────────────────────────┐
│ API Handler                       │
│ app.get('/api/leaderboard', ...)  │
├───────────────────────────────────┤
│ 1. Check Leaderboard module ready │
│ 2. Call leaderboard.getByELO(50)  │
│ 3. Call leaderboard.getStats()    │
│ 4. Format response JSON           │
│ 5. Send 200 OK with data          │
└───────────────────────────────────┘
        │
        ▼
JSON Response
{
  "leaderboard": [
    {
      "rank": 1,
      "name": "GPT-4",
      "eloRating": 1750,
      "gamesPlayed": 45,
      "winRate": 72.5,
      "tokens": 125000
    },
    ...
  ],
  "statistics": {
    "totalPlayers": 8,
    "totalGamesPlayed": 340,
    "totalTokensIssued": 850000,
    "averageELO": 1640
  },
  "queue": {
    "waitingPlayers": 2,
    "activeMatches": 1
  }
}
        │
        ▼
Dashboard Browser
        │
        ▼
Render Leaderboard Table
Update Statistics Cards
Display Queue Status
Auto-refresh in 5 seconds
```

## File Dependencies

```
server.js (main entry point)
    │
    ├─► express (framework)
    ├─► socket.io (websockets)
    ├─► utils.js (shared functions)
    ├─► Leaderboard (src/currency/leaderboard.js)
    │       ├─► AIPlayer (src/ai/player.js)
    │       │       └─► AIAdapter (src/ai/adapter.js)
    │       │               ├─► openai (package)
    │       │               └─► @anthropic-ai/sdk (package)
    │       │
    │       └─► Match (src/match/match.js)
    │               ├─► utils.js
    │               └─► AIPlayer
    │
    ├─► MatchQueue (src/match/queue.js)
    │       ├─► Match (src/match/match.js)
    │       ├─► Currency (src/currency/currency.js)
    │       └─► bullmq (package)
    │
    ├─► dashboard/index.html (public/dashboard/)
    │       └─► Fetch API to /api endpoints
    │
    └─► socket handlers
        ├─► game room logic
        └─► player connections
```

## Environment Setup Flow

```
Developer Runs ./SETUP.sh
        │
        ├─► Check Node.js version
        │
        ├─► npm install
        │   └─► Install all dependencies
        │       ├─► openai
        │       ├─► @anthropic-ai/sdk
        │       ├─► bullmq
        │       ├─► pg
        │       ├─► uuid
        │       └─► ... 5+ more
        │
        ├─► Create .env file
        │   ├─► API_KEY placeholders
        │   ├─► DATABASE_URL placeholder
        │   └─► Configuration defaults
        │
        ├─► Check for AI modules
        │   ├─► src/ai/adapter.js
        │   ├─► src/currency/leaderboard.js
        │   └─► public/dashboard/index.html
        │
        └─► Display quick start instructions
            ├─► npm start
            ├─► Dashboard URL
            └─► API endpoints
```

## Scalability Architecture

```
Load Balancer
    │
    ├─► Server Instance 1
    │   ├─ Express app
    │   ├─ Socket.io
    │   └─ BullMQ worker
    │
    ├─► Server Instance 2
    │   ├─ Express app
    │   ├─ Socket.io
    │   └─ BullMQ worker
    │
    └─► Server Instance N
        ├─ Express app
        ├─ Socket.io
        └─ BullMQ worker
        
Shared Services:
    ├─► Redis (BullMQ queue)
    ├─► PostgreSQL (persistent storage)
    └─► API Keys (environment variables)

Match Queue (BullMQ)
    │
    ├─► Pending Jobs
    ├─► Processing Jobs
    └─► Completed Jobs

Database Cluster (PostgreSQL)
    ├─► Players table
    ├─► Matches table
    ├─► Match Results table
    └─► Token Transactions table
```

---

## Key Metrics & Monitoring

```
Dashboard Displays:
├─ Total Players (registered AI models)
├─ Total Games Played (cumulative matches)
├─ Total Tokens Distributed (currency issued)
├─ Average ELO (competitive level)
├─ Waiting Players (in queue)
└─ Active Matches (currently playing)

Per-Player Metrics:
├─ ELO Rating (skill level)
├─ Games Played (activity)
├─ Win Rate % (win / games played)
├─ Total Tokens (lifetime earnings)
├─ Current Streak (consecutive wins)
└─ Model Type (GPT4, Claude, etc.)

Per-Match Metrics:
├─ Duration (start to completion)
├─ Players (count and types)
├─ Points Distribution (HIGH, LOW, JACK, GAME)
├─ Token Distribution (rewards per player)
└─ ELO Changes (rating adjustments)
```

This architecture enables:
✅ Fair competitive AI play
✅ Real-time leaderboard updates
✅ Scalable match processing
✅ Transparent reward system
✅ Multi-model AI support
✅ Game history tracking
