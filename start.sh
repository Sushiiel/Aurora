#!/bin/bash

# AURORA Quick Start Script
# This script sets up and runs AURORA locally

set -e

echo "=================================="
echo "🚀 AURORA Quick Start"
echo "=================================="
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python version
echo -e "${BLUE}Checking Python version...${NC}"
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python $python_version"
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo -e "${BLUE}Creating virtual environment...${NC}"
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment exists"
fi
echo ""

# Activate virtual environment
echo -e "${BLUE}Activating virtual environment...${NC}"
source venv/bin/activate
echo "✓ Activated"
echo ""

# Install dependencies
echo -e "${BLUE}Installing dependencies...${NC}"
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt
echo "✓ Dependencies installed"
echo ""

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}Creating .env file...${NC}"
    cp .env.example .env
    
    # Set default SQLite database
    sed -i '' 's|DATABASE_URL=postgresql://user:password@localhost:5432/aurora|DATABASE_URL=sqlite:///./aurora.db|g' .env
    
    echo "✓ .env created with SQLite database"
    echo ""
    echo -e "${YELLOW}⚠️  Please edit .env and add your GCP credentials${NC}"
    echo ""
else
    echo "✓ .env file exists"
    echo ""
fi

# Initialize database
echo -e "${BLUE}Initializing database...${NC}"
python scripts/init_db.py
echo "✓ Database initialized"
echo ""

# Start services
echo -e "${GREEN}=================================="
echo "Starting AURORA Services"
echo "==================================${NC}"
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo -e "${YELLOW}Shutting down services...${NC}"
    kill $BACKEND_PID 2>/dev/null || true
    kill $FRONTEND_PID 2>/dev/null || true
    echo "✓ Services stopped"
    exit 0
}

trap cleanup SIGINT SIGTERM

# Start backend
echo -e "${BLUE}Starting FastAPI backend...${NC}"
python -m backend.main > backend.log 2>&1 &
BACKEND_PID=$!
sleep 3

if ps -p $BACKEND_PID > /dev/null; then
    echo "✓ Backend running on http://localhost:8000"
else
    echo "✗ Backend failed to start. Check backend.log"
    exit 1
fi
echo ""

# Start frontend
# Start frontend
echo -e "${BLUE}Starting Vite frontend...${NC}"
cd web
npm install > /dev/null 2>&1
npm run dev > ../frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..
sleep 5

if ps -p $FRONTEND_PID > /dev/null; then
    echo "✓ Frontend running on http://localhost:3000"
else
    echo "✗ Frontend failed to start. Check frontend.log"
    kill $BACKEND_PID
    exit 1
fi
echo ""

echo -e "${GREEN}=================================="
echo "✅ AURORA is running!"
echo "==================================${NC}"
echo ""
echo "Access points:"
echo "  📊 Dashboard:  http://localhost:3000"
echo "  🔌 API:        http://localhost:8000"
echo "  📚 API Docs:   http://localhost:8000/docs"
echo ""
echo "Logs:"
echo "  Backend:  tail -f backend.log"
echo "  Frontend: tail -f frontend.log"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop all services${NC}"
echo ""

# Wait for processes
wait
