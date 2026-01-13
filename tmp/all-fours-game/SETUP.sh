#!/bin/bash

# All Fours AI System - Quick Start Guide
# This script helps set up the AI tournament system for local development

set -e  # Exit on error

echo "🎴 All Fours AI System - Setup"
echo "======================================"

# Check Node.js version
NODE_VERSION=$(node -v)
echo "✓ Node.js version: $NODE_VERSION"

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
else
    echo "✓ Dependencies already installed"
fi

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..."
    cat > .env << 'EOF'
# All Fours AI System Configuration

# Server
PORT=3000
NODE_ENV=development

# AI Model APIs
OPENAI_API_KEY=sk-your-key-here
ANTHROPIC_API_KEY=sk-ant-your-key-here

# Database (optional - uses in-memory without this)
DATABASE_URL=postgresql://user:password@localhost:5432/all_fours_ai
REDIS_URL=redis://localhost:6379

# AI Configuration
DEFAULT_AI_TEMP=0.3
DEFAULT_K_FACTOR=32
DEFAULT_STARTING_ELO=1600
EOF
    echo "✓ .env created - update with your API keys"
else
    echo "✓ .env file exists"
fi

# Check for AI module files
echo ""
echo "🤖 Checking AI modules..."
if [ -f "src/ai/adapter.js" ]; then
    echo "✓ AI Adapter installed"
else
    echo "⚠ AI Adapter not found"
fi

if [ -f "src/currency/leaderboard.js" ]; then
    echo "✓ Leaderboard system installed"
else
    echo "⚠ Leaderboard system not found"
fi

if [ -f "public/dashboard/index.html" ]; then
    echo "✓ Dashboard UI installed"
else
    echo "⚠ Dashboard UI not found"
fi

# Show available commands
echo ""
echo "📋 Available Commands:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "  npm start"
echo "    Start the game server (port 3000)"
echo ""
echo "  npm run build:ai"
echo "    Build AI system components"
echo ""
echo "  npm run db:migrate"
echo "    Run database migrations (requires PostgreSQL)"
echo ""
echo "🌐 Access Points:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "  Game: http://localhost:3000/index.html"
echo "  Dashboard: http://localhost:3000/public/dashboard/"
echo "  API: http://localhost:3000/api/leaderboard"
echo ""
echo "📊 API Endpoints:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "  GET /api/leaderboard - Full leaderboard with stats"
echo "  GET /api/leaderboard/elo - ELO ranking"
echo "  GET /api/leaderboard/winrate - Win rate ranking"
echo "  GET /api/leaderboard/tokens - Token earnings ranking"
echo "  GET /api/stats - Global tournament statistics"
echo "  GET /api/players/:id/rank - Individual player rank"
echo "  GET /health - Health check"
echo ""
echo "🚀 Next Steps:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "  1. Update .env with your AI API keys"
echo "  2. (Optional) Set up PostgreSQL database"
echo "  3. Run: npm start"
echo "  4. Visit dashboard at http://localhost:3000/public/dashboard/"
echo ""
echo "✅ Setup complete! Ready to go."
