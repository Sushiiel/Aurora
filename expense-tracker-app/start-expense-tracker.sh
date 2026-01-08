#!/bin/bash

# AURORA Expense Tracker - Startup Script
# This script starts the standalone expense tracker application

echo "🚀 Starting AURORA Expense Tracker..."
echo ""

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
    echo ""
fi

echo "✅ Starting development server on port 5174..."
echo ""
echo "📍 Access the application at:"
echo "   - Expense Tracker: http://localhost:5174"
echo "   - AURORA Monitor:  http://localhost:5174/aurora-monitor"
echo ""
echo "💡 Make sure the backend is running on port 8000"
echo ""

npm run dev
