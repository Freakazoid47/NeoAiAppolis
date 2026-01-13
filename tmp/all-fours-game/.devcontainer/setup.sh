#!/bin/bash
# Setup script for AI development environment

echo "🚀 Setting up All Fours AI Codespace..."

# Install dependencies
echo "📦 Installing dependencies..."
npm install

# Install AI-related packages
echo "🤖 Installing AI packages..."
npm install openai @anthropic-ai/sdk axios dotenv bull bullmq pg

# Setup environment
echo "📝 Creating .env file..."
if [ ! -f .env ]; then
  cp .env.example .env
  echo "⚠️  Please add your API keys to .env"
fi

# Create database
echo "🗄️  Setting up PostgreSQL..."
npm run db:migrate

# Build AI components
echo "🔨 Building AI components..."
npm run build:ai

echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Add API keys to .env file"
echo "2. Run: npm start"
echo "3. Open http://localhost:3000"
