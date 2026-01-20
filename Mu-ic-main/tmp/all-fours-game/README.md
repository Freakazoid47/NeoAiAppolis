# ♠️ All Fours Card Game - Online Multiplayer Edition

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Node.js](https://img.shields.io/badge/Node.js-18%2B-green)](package.json)
[![Express.js](https://img.shields.io/badge/Express.js-4.18-blue)](package.json)
[![Socket.io](https://img.shields.io/badge/Socket.io-4.5-purple)](package.json)

> A fully-featured, beautifully-themed online multiplayer card game with intelligent AI opponents, real-time gameplay, and both individual and partnership modes.

## 🎮 Features

- ♠️ **Classic All Fours Gameplay** - Authentic card game rules with High, Low, Jack, and Game scoring
- 👥 **Multiplayer Support** - Online real-time gameplay with 2-4 players via Socket.io
- 🤖 **Intelligent AI Opponents** - Adaptive bot players with skill levels and reasoning modes
- 🏆 **Individual & Partnership Modes** - Play solo (2-3 players) or team-based (4 players)
- 🎨 **Modern UI** - Clean, responsive interface with real-time game state updates
- 🔧 **Optimized Code** - Well-structured, consolidated utilities for maintainability
- 📦 **Production Ready** - Docker support, Heroku deployment, environment config

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- npm or yarn

### Local Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/all-fours-game.git
cd all-fours-game

# Install dependencies
npm install

# Start the server
npm start

# Open http://localhost:3000 in your browser
```

### Development Commands

```bash
# Run bot AI demo (shows AI decision-making)
node src/bot-demo.js

# Run game play demo (shows full game simulation)
node src/play-game-demo.js
```

## 📋 Game Rules

### Overview
**All Fours** is a classic trick-taking card game where players compete for points based on High, Low, Jack, and Game scoring.

### Objective
- **Individual Mode** (2-3 players): First to **11 points** wins
- **Partnership Mode** (4 players): First **team** to **14 points** wins

### Card Deal
- Standard 52-card deck
- Each player receives 6 cards (dealt in two packets of 3)
- Next card in deck becomes the trump suit

### Scoring (Per Deal)

| Scoring Component | Points | Condition |
|---|---|---|
| **HIGH** | 4 | Hold highest trump in original hand |
| **LOW** | 1 | Hold lowest trump in original hand |
| **JACK** | 1 | Win the trick with Jack of trump |
| **HANG JACK** | 3 | Bonus for winning Jack (4 pts total) |
| **GAME** | 2 | Win tricks with most card points |

**Card Values for GAME Scoring:**
- Ten = 10 points
- Ace = 4 points
- King = 3 points
- Queen = 2 points
- Jack = 1 point

### Playing Rules
1. Leader plays first card (any card)
2. Other players must **follow suit** if possible
3. If trump is led, must play trump if available
4. Highest card of led suit wins (trump beats all)
5. Winner of trick leads next
6. **Renege**: Failing to follow suit when able forfeits all points that round

## 🏗️ Project Structure

```
all-fours-game/
├── src/                        # Game logic & server
│   ├── server.js              # Express/Socket.io server
│   ├── game.js                # Single-player game logic
│   ├── socket-client.js       # Online multiplayer client
│   ├── utils.js               # Shared utilities
│   ├── bot-demo.js            # AI bot demonstration
│   └── play-game-demo.js      # Full game simulation demo
├── public/                     # Frontend assets
│   ├── index.html             # Main game interface
│   ├── live-demo.html         # Live demo page
│   └── style.css              # Game styling
├── config/                     # Deployment configuration
│   ├── Dockerfile             # Docker setup
│   ├── Procfile               # Heroku deployment
│   └── .dockerignore          # Docker ignore rules
├── docs/                       # Documentation
│   ├── ARCHITECTURE.md        # System design
│   ├── CODE_CONSOLIDATION.md  # Code optimization
│   ├── DEPLOYMENT.md          # Deployment guide
│   ├── OPTIMIZATION_SUMMARY.md# Recent optimizations
│   └── RULES_QUICK_REFERENCE.md
├── package.json               # Dependencies & scripts
├── LICENSE                    # MIT License
└── CONTRIBUTING.md            # Contribution guidelines
```

## 🔧 Tech Stack

### Backend
- **Node.js** - Server runtime
- **Express.js** - Web framework
- **Socket.io** - Real-time communication

### Frontend
- **Vanilla JavaScript** - Game logic & UI
- **HTML5** - Markup
- **CSS3** - Styling & animations

### Deployment
- **Docker** - Containerization
- **Heroku** - Cloud hosting

## 📈 Code Quality

### Recent Optimizations (v1.1)
- ✅ Consolidated 60+ lines of duplicate scoring logic
- ✅ Extracted reusable card utility functions
- ✅ Reduced code duplication by 92% in card operations
- ✅ Improved maintainability with semantic function names

### File Sizes (Optimized)
- **game.js** - 683 lines
- **server.js** - 382 lines
- **socket-client.js** - 441 lines
- **utils.js** - 185 lines
- **Total** - 2,245 lines

## 🚀 Deployment

### Docker
```bash
docker build -t all-fours-game .
docker run -p 3000:3000 all-fours-game
```

### Heroku
```bash
heroku create your-app-name
git push heroku main
heroku open
```

See [Deployment Guide](docs/DEPLOYMENT.md) for detailed instructions.

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on:
- Setting up development environment
- Code style conventions
- Testing requirements
- Pull request process

## 📚 Documentation

- [Architecture](docs/ARCHITECTURE.md) - System design and game flow
- [Deployment Guide](docs/DEPLOYMENT.md) - Production deployment
- [Code Consolidation](docs/CODE_CONSOLIDATION.md) - Bug fixes & refactoring
- [Optimization Report](docs/OPTIMIZATION_SUMMARY.md) - Recent improvements
- [Rules Reference](docs/RULES_QUICK_REFERENCE.md) - Complete game rules

## 🎯 Roadmap

- [ ] Mobile app (React Native)
- [ ] Chat functionality during gameplay
- [ ] Player statistics & leaderboards
- [ ] Custom game variants & house rules
- [ ] Spectator mode
- [ ] Tournament support

## 📝 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

- Classic All Fours card game rules
- Socket.io real-time communication
- Express.js web framework

## 💬 Support

- Open an [Issue](../../issues) for bug reports
- Check [Discussions](../../discussions) for Q&A
- Review [Documentation](docs/) for setup help

---

**Made with ❤️ by the All Fours Game Community**

Give us a ⭐ if you enjoy the game!
