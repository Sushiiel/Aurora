# 🚀 Deploying AURORA to Hugging Face Spaces

This guide will help you deploy AURORA to Hugging Face Spaces (free tier).

## Prerequisites

1. A Hugging Face account (free)
2. Git installed on your machine
3. Your AURORA project ready

## Step 1: Create a Hugging Face Space

1. Go to [Hugging Face Spaces](https://huggingface.co/spaces)
2. Click **"Create new Space"**
3. Configure your Space:
   - **Name**: `aurora-ai-system` (or your preferred name)
   - **License**: Apache 2.0
   - **SDK**: Docker
   - **Hardware**: CPU basic (free tier)
   - **Visibility**: Public or Private

## Step 2: Prepare Your Repository

The repository is already configured with:
- `Dockerfile.huggingface` - Optimized Docker configuration for HF Spaces
- `start-hf.sh` - Startup script for the deployed environment
- Updated frontend with dynamic API URL detection
- Environment-based port configuration

## Step 3: Set Up Environment Variables

In your Hugging Face Space settings, add these **Repository Secrets**:

### Required Variables:
```
GCP_PROJECT_ID=your-project-id
GOOGLE_APPLICATION_CREDENTIALS_JSON=<paste your service account JSON here>
```

### Optional Variables (with defaults):
```
VERTEX_AI_MODEL=gemini-pro
LOG_LEVEL=INFO
ENVIRONMENT=production
```

### Firebase Configuration (if using Firebase Auth):
```
VITE_FIREBASE_API_KEY=your-api-key
VITE_FIREBASE_AUTH_DOMAIN=your-domain
VITE_FIREBASE_PROJECT_ID=your-project-id
VITE_FIREBASE_STORAGE_BUCKET=your-bucket
VITE_FIREBASE_MESSAGING_SENDER_ID=your-sender-id
VITE_FIREBASE_APP_ID=your-app-id
```

## Step 4: Deploy to Hugging Face

### Option A: Using Git (Recommended)

```bash
# Add Hugging Face as a remote
git remote add hf https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME

# Push to Hugging Face
git push hf main
```

### Option B: Using Hugging Face CLI

```bash
# Install Hugging Face CLI
pip install huggingface_hub

# Login to Hugging Face
huggingface-cli login

# Upload your space
huggingface-cli upload YOUR_USERNAME/YOUR_SPACE_NAME . --repo-type=space
```

## Step 5: Verify Deployment

1. Wait for the build to complete (5-10 minutes)
2. Your app will be available at: `https://YOUR_USERNAME-YOUR_SPACE_NAME.hf.space`
3. Check the logs in the Space's "Logs" tab for any issues

## Architecture on Hugging Face

```
┌─────────────────────────────────────┐
│   Hugging Face Space Container      │
│                                     │
│  ┌──────────────┐  ┌─────────────┐ │
│  │   Nginx      │  │   FastAPI   │ │
│  │   (Port 7860)│──│   Backend   │ │
│  │              │  │             │ │
│  │   Serves:    │  └─────────────┘ │
│  │   - Frontend │                  │
│  │   - API Proxy│                  │
│  └──────────────┘                  │
│                                     │
│  ┌──────────────┐                  │
│  │   SQLite DB  │                  │
│  │   (Ephemeral)│                  │
│  └──────────────┘                  │
└─────────────────────────────────────┘
```

## Important Notes

### Port Configuration
- Hugging Face Spaces **requires** port **7860**
- The deployment automatically configures this
- No manual port configuration needed

### Database Persistence
- **Free tier uses ephemeral storage** - data resets on restart
- For persistent storage, consider:
  - Upgrading to persistent storage (paid)
  - Using external database (PostgreSQL, etc.)
  - Exporting/importing data via API

### API URLs
- Frontend automatically detects the deployment URL
- No hardcoded localhost references
- Uses `window.location.origin` for API calls

### Resource Limits (Free Tier)
- **CPU**: 2 vCPUs
- **RAM**: 16 GB
- **Storage**: 50 GB (ephemeral)
- **Sleep**: Inactive spaces sleep after 48 hours

## Troubleshooting

### Build Fails
- Check the build logs in HF Space
- Verify all dependencies in `requirements.txt`
- Ensure Dockerfile syntax is correct

### App Not Loading
- Check if port 7860 is exposed
- Verify nginx configuration
- Check backend logs

### API Errors
- Verify environment variables are set
- Check GCP credentials are valid
- Review backend logs for errors

### Database Issues
- Remember: free tier storage is ephemeral
- Check if database initialization completed
- Verify SQLite permissions

## Updating Your Deployment

```bash
# Make changes locally
git add .
git commit -m "Update: description of changes"

# Push to Hugging Face
git push hf main
```

The Space will automatically rebuild and redeploy.

## Monitoring

- **Logs**: Available in the Space's "Logs" tab
- **Metrics**: Check the "Analytics" section
- **Health Check**: Visit `https://your-space.hf.space/health`

## Cost Optimization

The free tier is sufficient for:
- Development and testing
- Small-scale deployments
- Demo purposes

For production:
- Consider upgrading to persistent storage
- Use external managed database
- Monitor resource usage

## Support

- [Hugging Face Spaces Documentation](https://huggingface.co/docs/hub/spaces)
- [AURORA GitHub Issues](https://github.com/your-repo/issues)
- [Hugging Face Community](https://discuss.huggingface.co/)
