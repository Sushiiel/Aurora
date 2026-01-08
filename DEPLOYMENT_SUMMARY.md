# 🎉 AURORA Hugging Face Deployment - Complete Setup

## What Was Done

I've successfully prepared your AURORA application for deployment to Hugging Face Spaces with **dynamic port and URL configuration**. All localhost references have been removed and replaced with environment-aware configurations.

## 📁 New Files Created

### 1. **Deployment Configuration**
- ✅ `Dockerfile.huggingface` - Optimized Docker setup for HF Spaces (port 7860)
- ✅ `nginx.conf` - Nginx configuration to serve frontend and proxy API
- ✅ `start-hf.sh` - Startup script for the deployed environment
- ✅ `.dockerignore` - Optimized Docker build context

### 2. **Documentation**
- ✅ `README_HF.md` - Hugging Face Space README with metadata
- ✅ `README_HF_DEPLOYMENT.md` - Comprehensive deployment guide
- ✅ `DEPLOYMENT_CHECKLIST.md` - Step-by-step deployment checklist

### 3. **Deployment Tools**
- ✅ `deploy-hf.sh` - Automated deployment script

## 🔧 Modified Files

### Backend Changes
- ✅ `backend/config.py` - Dynamic port configuration using `PORT` env variable
  - Automatically uses port 7860 on HF Spaces
  - Falls back to 8000 for local development
  - Made GCP credentials optional

### Frontend Changes
- ✅ `web/src/utils/api.ts` - **NEW** API utility for dynamic URL detection
- ✅ `web/vite.config.ts` - Added API proxy for development
- ✅ `web/src/pages/Dashboard.tsx` - Uses dynamic API URLs
- ✅ `web/src/pages/Connect.tsx` - Uses dynamic API URLs

## 🚀 How It Works

### Development (localhost)
```
Frontend (port 3000) → Vite Proxy → Backend (port 8000)
```
- Uses relative URLs (`/api/...`)
- Vite proxy forwards to localhost:8000
- No CORS issues

### Production (Hugging Face)
```
User → Nginx (port 7860) → {
  Frontend (static files)
  API Proxy → Backend (port 8000)
}
```
- Frontend served as static files
- API requests proxied to backend
- Single port (7860) for everything

## 📊 Architecture

```
┌─────────────────────────────────────────┐
│   Hugging Face Space (Port 7860)        │
│                                         │
│  ┌──────────────┐    ┌──────────────┐  │
│  │    Nginx     │────│   FastAPI    │  │
│  │              │    │   Backend    │  │
│  │  Serves:     │    │  (port 8000) │  │
│  │  - Frontend  │    │              │  │
│  │  - /api/*    │────│              │  │
│  │  - /health   │    │              │  │
│  │  - /docs     │    │              │  │
│  └──────────────┘    └──────────────┘  │
│                                         │
│  ┌──────────────┐                      │
│  │  SQLite DB   │                      │
│  │ (ephemeral)  │                      │
│  └──────────────┘                      │
└─────────────────────────────────────────┘
```

## 🎯 Key Features

### 1. **Dynamic Port Detection**
- Automatically detects Hugging Face's required port 7860
- Falls back to 8000 for local development
- No manual configuration needed

### 2. **Dynamic API URLs**
- Frontend automatically detects correct API endpoint
- Works in both development and production
- No hardcoded localhost references

### 3. **Environment-Based Configuration**
```javascript
// Development
getApiUrl() → '' (uses Vite proxy)

// Production
getApiUrl() → window.location.origin
```

### 4. **Unified Deployment**
- Single Dockerfile for entire application
- Nginx serves frontend and proxies API
- All on port 7860 as required by HF

## 📝 Quick Start Guide

### Step 1: Create Hugging Face Space
1. Go to https://huggingface.co/spaces
2. Click "Create new Space"
3. Choose:
   - **SDK**: Docker
   - **Hardware**: CPU basic (free)

### Step 2: Deploy Using Script
```bash
# Run the automated deployment script
./deploy-hf.sh

# Enter your Space name when prompted
# Format: username/space-name
```

### Step 3: Configure Environment Variables
In your Space settings, add:
```bash
# Required (if using GCP)
GCP_PROJECT_ID=your-project-id
GOOGLE_APPLICATION_CREDENTIALS_JSON=<paste service account JSON>

# Optional
VERTEX_AI_MODEL=gemini-pro
LOG_LEVEL=INFO
ENVIRONMENT=production
```

### Step 4: Wait for Build
- Build takes 5-10 minutes
- Monitor in the "Logs" tab
- App will be at: `https://YOUR_USERNAME-YOUR_SPACE_NAME.hf.space`

## 🔍 Testing Locally

Before deploying, test the Docker setup locally:

```bash
# Build the Docker image
docker build -f Dockerfile.huggingface -t aurora-hf .

# Run the container
docker run -p 7860:7860 \
  -e GCP_PROJECT_ID=your-project \
  -e GOOGLE_APPLICATION_CREDENTIALS_JSON='{"type":"service_account",...}' \
  aurora-hf

# Access at http://localhost:7860
```

## 🛠️ Environment Variables

### Required for Full Functionality
| Variable | Description | Default |
|----------|-------------|---------|
| `GCP_PROJECT_ID` | Google Cloud project ID | None |
| `GOOGLE_APPLICATION_CREDENTIALS_JSON` | Service account JSON | None |

### Optional
| Variable | Description | Default |
|----------|-------------|---------|
| `PORT` | Application port | 7860 (HF), 8000 (local) |
| `API_PORT` | Backend port | 8000 |
| `VERTEX_AI_MODEL` | Gemini model | gemini-pro |
| `LOG_LEVEL` | Logging level | INFO |
| `ENVIRONMENT` | Environment | production |
| `DATABASE_URL` | Database URL | sqlite:///./aurora.db |

## 📚 Documentation Files

1. **README_HF_DEPLOYMENT.md** - Complete deployment guide
2. **DEPLOYMENT_CHECKLIST.md** - Step-by-step checklist
3. **README_HF.md** - Hugging Face Space README

## ✅ What's Fixed

### Before
- ❌ Hardcoded `localhost:8000` in frontend
- ❌ Fixed port 8000 (HF requires 7860)
- ❌ Separate frontend and backend servers
- ❌ CORS issues in production

### After
- ✅ Dynamic API URL detection
- ✅ Automatic port configuration (7860 on HF)
- ✅ Unified server with Nginx
- ✅ No CORS issues
- ✅ Works in both dev and production

## 🎨 API Utility Usage

The new `web/src/utils/api.ts` provides:

```typescript
// Get API base URL
const apiUrl = getApiUrl();

// Make API request
const response = await apiRequest('/api/metrics');

// Get API docs URL
const docsUrl = getApiDocsUrl();

// Check API health
const isHealthy = await checkApiHealth();
```

## 🚨 Important Notes

### Free Tier Limitations
- **Storage**: Ephemeral (resets on restart)
- **Sleep**: After 48 hours of inactivity
- **Resources**: 2 vCPUs, 16 GB RAM

### For Production
- Consider upgrading to persistent storage
- Use external database for data persistence
- Monitor resource usage

### Database
- SQLite is used by default (ephemeral on free tier)
- Data will be lost on container restart
- For persistence: use PostgreSQL or upgrade storage

## 🔗 Next Steps

1. **Deploy to Hugging Face**:
   ```bash
   ./deploy-hf.sh
   ```

2. **Set Environment Variables** in Space settings

3. **Monitor Build** in Logs tab

4. **Test Deployment**:
   - Visit your Space URL
   - Check `/health` endpoint
   - Test `/docs` API documentation
   - Try connecting a model

5. **Integrate Your Models**:
   - Use the code from Connect page
   - Update with your deployed URL
   - Monitor in Dashboard

## 📞 Support

- **Deployment Guide**: `README_HF_DEPLOYMENT.md`
- **Checklist**: `DEPLOYMENT_CHECKLIST.md`
- **HF Docs**: https://huggingface.co/docs/hub/spaces
- **Issues**: Open on GitHub

## 🎊 Success!

Your AURORA application is now ready for deployment to Hugging Face Spaces with:
- ✅ Dynamic port configuration
- ✅ Automatic URL detection
- ✅ Production-ready Docker setup
- ✅ Comprehensive documentation
- ✅ Automated deployment script

**Happy Deploying! 🚀**
