#!/bin/bash
# KisanMitra AI - Setup and Execution Script
# This script automates the installation and running of both backend and frontend

set -e

echo "==============================================="
echo "  KisanMitra AI - Setup and Installation"
echo "==============================================="
echo ""

# Check prerequisites
echo "Checking prerequisites..."
if ! command -v python &> /dev/null; then
    echo "❌ Python is not installed. Please install Python 3.9+"
    exit 1
fi

if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install Node.js 16+"
    exit 1
fi

echo "✓ Python version: $(python --version)"
echo "✓ npm version: $(npm --version)"
echo ""

# Setup Backend
echo "==============================================="
echo "Setting up Backend..."
echo "==============================================="

cd backend

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/Scripts/activate 2>/dev/null || source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install -q -r requirements.txt

# Create .env file from template
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  NOTE: Please edit backend/.env and add your Groq API key"
    echo "   LLM_API_KEY=gsk_your_api_key_here"
fi

echo "✓ Backend setup complete"
echo ""

# Setup Frontend
echo "==============================================="
echo "Setting up Frontend..."
echo "==============================================="

cd ../frontend

# Install dependencies
echo "Installing npm dependencies..."
npm install --silent

echo "✓ Frontend setup complete"
echo ""

# Print instructions
echo "==============================================="
echo "  Setup Complete!"
echo "==============================================="
echo ""
echo "📝 NEXT STEPS:"
echo ""
echo "1. Edit backend/.env and add your Groq API key:"
echo "   LLM_API_KEY=gsk_..."
echo ""
echo "2. Start Backend Server (in a new terminal):"
echo "   cd backend"
echo "   source venv/bin/activate  # or venv\\Scripts\\activate on Windows"
echo "   uvicorn app.main:app --reload --port 8000"
echo ""
echo "3. Start Frontend Dev Server (in another terminal):"
echo "   cd frontend"
echo "   npm run dev"
echo ""
echo "4. Open http://localhost:5173 in your browser"
echo ""
echo "📚 Full instructions are in README.md"
