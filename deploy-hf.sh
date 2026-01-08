#!/bin/bash

# AURORA Hugging Face Deployment Script
# This script prepares and deploys AURORA to Hugging Face Spaces

echo "🚀 AURORA Hugging Face Deployment"
echo "=================================="
echo ""

# Configuration
USER_EMAIL="sushiielanand8@gmail.com"
N8N_WEBHOOK="https://aurora123.app.n8n.cloud/webhook/expense-alert"

echo "📧 Email configured: $USER_EMAIL"
echo "🔗 n8n Webhook: $N8N_WEBHOOK"
echo ""

# Test n8n webhook
echo "🧪 Testing n8n webhook..."
curl -X POST $N8N_WEBHOOK \
  -H "Content-Type: application/json" \
  -d "{
    \"to\": \"$USER_EMAIL\",
    \"subject\": \"🚀 AURORA Deployment Test\",
    \"category\": \"Deployment\",
    \"spent\": 100.00,
    \"limit\": 50.00,
    \"percentage\": 200.0,
    \"message\": \"Testing n8n integration before Hugging Face deployment\"
  }" \
  -s -o /dev/null -w "Status: %{http_code}\n"

echo ""
echo "✅ n8n webhook test complete"
echo "📧 Check $USER_EMAIL for test email"
echo ""

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "❌ Git repository not initialized"
    echo "Run: git init"
    exit 1
fi

# Check for uncommitted changes
if [[ `git status --porcelain` ]]; then
    echo "📝 Uncommitted changes detected"
    echo ""
    read -p "Commit changes? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git add .
        git commit -m "Deploy to Hugging Face with n8n integration for $USER_EMAIL"
        echo "✅ Changes committed"
    fi
fi

echo ""
echo "🎯 Deployment Options:"
echo "1. Deploy to existing Hugging Face Space"
echo "2. Create new Hugging Face Space"
echo "3. Test Docker build locally first"
echo "4. Exit"
echo ""

read -p "Choose option (1-4): " option

case $option in
    1)
        echo ""
        read -p "Enter your Hugging Face username: " hf_username
        read -p "Enter your Space name: " space_name
        
        # Add Hugging Face remote if not exists
        if ! git remote | grep -q "^hf$"; then
            git remote add hf https://huggingface.co/spaces/$hf_username/$space_name
            echo "✅ Added Hugging Face remote"
        fi
        
        echo ""
        echo "🚀 Pushing to Hugging Face..."
        git push hf main
        
        echo ""
        echo "✅ Deployment initiated!"
        echo "🔗 View your Space at: https://huggingface.co/spaces/$hf_username/$space_name"
        echo ""
        echo "⚠️  Don't forget to set environment variables in Space settings:"
        echo "   N8N_WEBHOOK_URL=$N8N_WEBHOOK"
        echo "   USER_EMAIL=$USER_EMAIL"
        ;;
        
    2)
        echo ""
        echo "📝 Create a new Space at: https://huggingface.co/new-space"
        echo ""
        echo "Settings:"
        echo "  - SDK: Docker"
        echo "  - License: Apache 2.0"
        echo ""
        echo "After creating, run this script again and choose option 1"
        ;;
        
    3)
        echo ""
        echo "🐳 Testing Docker build locally..."
        docker build -f Dockerfile.huggingface -t aurora-hf-test .
        
        if [ $? -eq 0 ]; then
            echo ""
            echo "✅ Docker build successful!"
            echo ""
            read -p "Run container locally? (y/n) " -n 1 -r
            echo ""
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                echo "🚀 Starting container on port 7860..."
                docker run -p 7860:7860 \
                    -e N8N_WEBHOOK_URL=$N8N_WEBHOOK \
                    -e USER_EMAIL=$USER_EMAIL \
                    aurora-hf-test
            fi
        else
            echo "❌ Docker build failed"
            echo "Check the error messages above"
        fi
        ;;
        
    4)
        echo "👋 Deployment cancelled"
        exit 0
        ;;
        
    *)
        echo "❌ Invalid option"
        exit 1
        ;;
esac

echo ""
echo "🎉 Deployment script complete!"
