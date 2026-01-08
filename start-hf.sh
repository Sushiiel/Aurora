#!/bin/bash

# AURORA Hugging Face Spaces Startup Script
set -e

echo "========================================="
echo "🚀 Starting AURORA on Hugging Face"
echo "========================================="
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Create credentials file from environment variable if provided
if [ ! -z "$GOOGLE_APPLICATION_CREDENTIALS_JSON" ]; then
    echo -e "${BLUE}Setting up GCP credentials...${NC}"
    echo "$GOOGLE_APPLICATION_CREDENTIALS_JSON" > /app/credentials.json
    export GOOGLE_APPLICATION_CREDENTIALS=/app/credentials.json
    echo -e "${GREEN}✓ GCP credentials configured${NC}"
fi

# Set environment variables with defaults
export DATABASE_URL=${DATABASE_URL:-"sqlite:///./aurora.db"}
export API_PORT=${API_PORT:-8000}
export PORT=${PORT:-7860}
export ENVIRONMENT=${ENVIRONMENT:-production}
export LOG_LEVEL=${LOG_LEVEL:-INFO}

echo ""
echo -e "${BLUE}Environment Configuration:${NC}"
echo "  PORT: $PORT"
echo "  API_PORT: $API_PORT"
echo "  ENVIRONMENT: $ENVIRONMENT"
echo "  DATABASE: $DATABASE_URL"
echo ""

# Initialize database
echo -e "${BLUE}Initializing database...${NC}"
cd /app
python scripts/init_db.py
echo -e "${GREEN}✓ Database initialized${NC}"
echo ""

# Start nginx
echo -e "${BLUE}Starting nginx...${NC}"
nginx -t
nginx
echo -e "${GREEN}✓ Nginx started on port $PORT${NC}"
echo ""

# Start FastAPI backend
echo -e "${BLUE}Starting FastAPI backend...${NC}"
cd /app
python -m uvicorn backend.main:app \
    --host 0.0.0.0 \
    --port $API_PORT \
    --log-level info &

BACKEND_PID=$!
echo -e "${GREEN}✓ Backend started (PID: $BACKEND_PID)${NC}"
echo ""

# Wait for backend to be ready
echo -e "${BLUE}Waiting for backend to be ready...${NC}"
for i in {1..30}; do
    if curl -s http://localhost:$API_PORT/health > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Backend is ready${NC}"
        break
    fi
    if [ $i -eq 30 ]; then
        echo -e "${RED}✗ Backend failed to start${NC}"
        exit 1
    fi
    sleep 1
done
echo ""

echo -e "${GREEN}========================================="
echo "✅ AURORA is running!"
echo "=========================================${NC}"
echo ""
echo "Access points:"
echo "  🌐 Application: https://YOUR_SPACE.hf.space"
echo "  🔌 API:         https://YOUR_SPACE.hf.space/api"
echo "  📚 API Docs:    https://YOUR_SPACE.hf.space/docs"
echo "  ❤️  Health:      https://YOUR_SPACE.hf.space/health"
echo ""
echo -e "${YELLOW}Logs are available in the Hugging Face Space logs tab${NC}"
echo ""

# Keep the script running and monitor the backend
while true; do
    if ! ps -p $BACKEND_PID > /dev/null; then
        echo -e "${RED}Backend process died, restarting...${NC}"
        python -m uvicorn backend.main:app \
            --host 0.0.0.0 \
            --port $API_PORT \
            --log-level info &
        BACKEND_PID=$!
    fi
    sleep 10
done
