#!/bin/bash
echo "🚀 Starting Local AI Model Simulation..."
cd "$(dirname "$0")"

# Install requests if missing
pip install requests > /dev/null 2>&1

# Run the integration script
python3 demo_ai_integration.py
