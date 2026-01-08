# 🚀 Hugging Face Deployment Guide

## ✅ Pre-Deployment Checklist

### 1. n8n Email Configuration
- [x] Webhook URL: https://aurora123.app.n8n.cloud/webhook/expense-alert
- [x] Test email sent to: sushiielanand8@gmail.com
- [x] Expense tracker stopped

### 2. Environment Variables to Set in Hugging Face

```bash
# n8n Configuration
N8N_WEBHOOK_URL=https://aurora123.app.n8n.cloud/webhook/expense-alert
USER_EMAIL=sushiielanand8@gmail.com

# Google Cloud (if using Vertex AI)
GCP_PROJECT_ID=your-project-id
GOOGLE_APPLICATION_CREDENTIALS_JSON=<your-service-account-json>

# Optional
VERTEX_AI_MODEL=gemini-pro
LOG_LEVEL=INFO
ENVIRONMENT=production
```

---

## 🚀 Deployment Steps

### Step 1: Prepare Repository

```bash
cd /Users/mymac/Desktop/AURORA

# Make sure all changes are committed
git add .
git commit -m "Prepare for Hugging Face deployment with n8n integration"
git push origin main
```

### Step 2: Create Hugging Face Space

1. Go to https://huggingface.co/spaces
2. Click "Create new Space"
3. Fill in details:
   - **Name**: aurora-ai-system (or your choice)
   - **License**: Apache 2.0
   - **SDK**: Docker
   - **Hardware**: CPU Basic (free) or upgrade if needed

### Step 3: Connect Repository

**Option A: Push to Hugging Face directly**
```bash
# Add Hugging Face as remote
git remote add hf https://huggingface.co/spaces/YOUR_USERNAME/aurora-ai-system

# Push to Hugging Face
git push hf main
```

**Option B: Link GitHub repository**
1. In Space settings, go to "Files and versions"
2. Click "Link a GitHub repository"
3. Select your AURORA repository

### Step 4: Configure Environment Variables

In your Hugging Face Space:
1. Go to "Settings" tab
2. Scroll to "Repository secrets"
3. Add these variables:

```
N8N_WEBHOOK_URL = https://aurora123.app.n8n.cloud/webhook/expense-alert
USER_EMAIL = sushiielanand8@gmail.com
```

### Step 5: Wait for Build

- Hugging Face will automatically build using `Dockerfile.huggingface`
- Build time: ~10-15 minutes
- Watch the build logs in the "Logs" tab

### Step 6: Verify Deployment

Once deployed, your Space will be at:
```
https://huggingface.co/spaces/YOUR_USERNAME/aurora-ai-system
```

Test:
- [ ] Homepage loads
- [ ] Dashboard accessible
- [ ] API health check: `/health`
- [ ] Add expense and check email

---

## 🔧 Quick Deploy Script

I'll create a deployment script for you:

```bash
cd /Users/mymac/Desktop/AURORA
./deploy-hf.sh
```

---

## 📊 What Gets Deployed

### Included:
- ✅ Backend API (FastAPI)
- ✅ Frontend (React)
- ✅ AURORA agents
- ✅ Expense tracking
- ✅ n8n integration
- ✅ Database (SQLite)

### Excluded:
- ❌ Expense tracker app (port 5174) - separate deployment
- ❌ Local development files
- ❌ node_modules (rebuilt during deployment)

---

## 🎯 Post-Deployment

### Test n8n Integration

1. Visit your deployed Space
2. Add an expense that exceeds budget
3. Check email: sushiielanand8@gmail.com
4. You should receive budget alert

### Monitor Performance

Visit AURORA Monitor:
```
https://YOUR_SPACE_URL/aurora-monitor
```

---

## 🐛 Troubleshooting

### Build Fails

**Check Dockerfile.huggingface**
```bash
# Test locally first
docker build -f Dockerfile.huggingface -t aurora-hf .
docker run -p 7860:7860 aurora-hf
```

### App Not Loading

**Check logs in Hugging Face:**
1. Go to your Space
2. Click "Logs" tab
3. Look for errors

**Common issues:**
- Missing environment variables
- Port 7860 not exposed
- nginx configuration

### n8n Not Working

**Verify webhook:**
```bash
curl -X POST https://aurora123.app.n8n.cloud/webhook/expense-alert \
  -H "Content-Type: application/json" \
  -d '{"to":"sushiielanand8@gmail.com","subject":"Test"}'
```

---

## 📚 Files Used for Deployment

```
AURORA/
├── Dockerfile.huggingface  ← Main deployment file
├── start-hf.sh            ← Startup script
├── nginx.conf             ← Web server config
├── README_HF.md           ← Space README
├── backend/               ← Python backend
├── web/                   ← React frontend
└── requirements.txt       ← Python dependencies
```

---

## 🎊 Success Criteria

Your deployment is successful when:

- [ ] Space builds without errors
- [ ] Homepage loads at your Space URL
- [ ] Dashboard shows AURORA interface
- [ ] API responds at `/health`
- [ ] Can add expenses
- [ ] Email alerts work (check sushiielanand8@gmail.com)
- [ ] AURORA monitor shows metrics

---

## 🚀 Ready to Deploy?

Run these commands:

```bash
cd /Users/mymac/Desktop/AURORA

# Commit changes
git add .
git commit -m "Deploy to Hugging Face with n8n integration"

# Push to GitHub (if linked)
git push origin main

# Or push directly to Hugging Face
git remote add hf https://huggingface.co/spaces/YOUR_USERNAME/aurora-ai-system
git push hf main
```

---

**Need help?** Check the logs in your Hugging Face Space or refer to:
- `README_HF_DEPLOYMENT.md` for detailed deployment guide
- `DEPLOYMENT_CHECKLIST.md` for step-by-step checklist

---

Built with ❤️ for deployment to Hugging Face Spaces
