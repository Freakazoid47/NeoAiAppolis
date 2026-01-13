# Contributing to All Fours Card Game

We welcome contributions! Here's how to get started.

## Getting Started

1. **Fork** the repository
2. **Clone** your fork: `git clone https://github.com/YOUR-USERNAME/all-fours-game.git`
3. **Create a branch**: `git checkout -b feature/your-feature-name`
4. **Install dependencies**: `npm install`
5. **Start development**: `npm start`

## Development Setup

```bash
# Install dependencies
npm install

# Start the server (opens http://localhost:3000)
npm start

# Run bot demo
node src/bot-demo.js

# Run play game demo
node src/play-game-demo.js
```

## Project Structure

```
all-fours-game/
├── src/                    # Game logic and server code
│   ├── server.js          # Express/Socket.io server
│   ├── game.js            # Single-player game logic
│   ├── socket-client.js   # Online multiplayer client
│   ├── utils.js           # Shared utilities
│   ├── bot-demo.js        # Bot AI demo
│   └── play-game-demo.js  # Game play demo
├── public/                # Frontend assets
│   ├── index.html         # Main game interface
│   ├── live-demo.html     # Live demo page
│   └── style.css          # Styling
├── config/                # Deployment & configuration
│   ├── Dockerfile         # Docker configuration
│   ├── Procfile           # Heroku deployment
│   └── .dockerignore      # Docker ignore rules
├── docs/                  # Documentation
│   ├── ARCHITECTURE.md    # System architecture
│   ├── DEPLOYMENT.md      # Deployment guide
│   └── RULES_QUICK_REFERENCE.md
└── package.json           # Dependencies & scripts
```

## Code Style

- Use consistent indentation (2 spaces)
- Add comments for complex game logic
- Follow existing naming conventions
- Test your changes before submitting

## Game Rules

The project implements **All Fours** card game with support for:
- **Individual Mode** (2-3 players, first to 11 points)
- **Partnership Mode** (4 players, first team to 14 points)

Key scoring:
- **HIGH** (4pts) - Highest trump dealt
- **LOW** (1pt) - Lowest trump dealt  
- **JACK** (1pt) + **HANG JACK** (3pt bonus) - Winning Jack of trump
- **GAME** (2pts) - Highest card points total

## Making Changes

### For Bug Fixes
1. Describe the bug in your PR
2. Reference any related issues
3. Test the fix in both single-player and multiplayer modes

### For Features
1. Create an issue to discuss first
2. Implement feature with tests
3. Update documentation if needed

## Testing

Test your changes:
- **Single-player**: `npm start` then play locally
- **Multiplayer**: Open multiple browser windows to test socket connections
- **Bot AI**: Run `node src/bot-demo.js` to verify AI logic

## Submitting Changes

1. **Push** your branch: `git push origin feature/your-feature-name`
2. **Create a Pull Request** with a clear description
3. **Link any related issues**: `Fixes #123`
4. **Wait for review** and address feedback

## Pull Request Checklist

- [ ] Code follows project style
- [ ] Changes tested in-game
- [ ] Documentation updated (if needed)
- [ ] No console errors or warnings
- [ ] Commit messages are descriptive

## Questions?

- Check existing [Issues](../../issues)
- Review [Documentation](docs/)
- Open a new discussion

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
