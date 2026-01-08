# 🚀 Hugging Face Deployment Checklist

Use this checklist to ensure a smooth deployment to Hugging Face Spaces.

## Pre-Deployment Checklist

### 1. Hugging Face Account Setup
- [ ] Created a Hugging Face account at https://huggingface.co
- [ ] Verified email address
- [ ] Set up Git credentials for Hugging Face

### 2. Create Your Space
- [ ] Navigate to https://huggingface.co/spaces
- [ ] Click "Create new Space"
- [ ] Configure Space:
  - **Name**: `aurora-ai-system` (or your choice)
  - **License**: Apache 2.0
  - **SDK**: Docker
  - **Hardware**: CPU basic (free)
  - **Visibility**: Public or Private

### 3. Prepare Environment Variables
Gather these credentials before deployment:

#### Required (if using GCP/Vertex AI):
- [ ] `GCP_PROJECT_ID` - Your Google Cloud project ID
- [ ] `GOOGLE_APPLICATION_CREDENTIALS_JSON` - Service account JSON content

#### Optional:
- [ ] `VERTEX_AI_MODEL` - Default: gemini-pro
- [ ] `LOG_LEVEL` - Default: INFO
- [ ] `ENVIRONMENT` - Default: production

#### Firebase (if using):
- [ ] `VITE_FIREBASE_API_KEY`
- [ ] `VITE_FIREBASE_AUTH_DOMAIN`
- [ ] `VITE_FIREBASE_PROJECT_ID`
- [ ] `VITE_FIREBASE_STORAGE_BUCKET`
- [ ] `VITE_FIREBASE_MESSAGING_SENDER_ID`
- [ ] `VITE_FIREBASE_APP_ID`

## Deployment Steps

### Option A: Using Deployment Script (Recommended)

1. **Run the deployment script**:
   ```bash
   ./deploy-hf.sh
   ```

2. **Enter your Space name** when prompted:
   ```
   username/space-name
   ```

3. **Wait for completion** - The script will:
   - Add Hugging Face remote
   - Prepare deployment files
   - Commit and push changes
   - Restore local files

### Option B: Manual Deployment

1. **Add Hugging Face remote**:
   ```bash
   git remote add hf https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME
   ```

2. **Prepare files**:
   ```bash
   # Copy Hugging Face specific files
   cp README_HF.md README.md
   cp Dockerfile.huggingface Dockerfile
   ```

3. **Commit changes**:
   ```bash
   git add .
   git commit -m "Deploy to Hugging Face Spaces"
   ```

4. **Push to Hugging Face**:
   ```bash
   git push hf main
   ```

## Post-Deployment Configuration

### 1. Set Environment Variables

1. Go to your Space settings
2. Navigate to "Repository secrets"
3. Add each environment variable:
   - Click "New secret"
   - Enter name and value
   - Click "Add secret"

**Critical**: Add `GOOGLE_APPLICATION_CREDENTIALS_JSON` with your full service account JSON

### 2. Monitor Build

1. Go to your Space page
2. Click "Logs" tab
3. Watch the build progress
4. Build typically takes 5-10 minutes

### 3. Verify Deployment

Once build completes:

- [ ] Visit your Space URL: `https://YOUR_USERNAME-YOUR_SPACE_NAME.hf.space`
- [ ] Check homepage loads
- [ ] Navigate to Dashboard
- [ ] Test API at `/docs`
- [ ] Check health endpoint at `/health`
- [ ] Try connecting a test model

## Troubleshooting

### Build Fails

**Check build logs**:
1. Go to Space → Logs
2. Look for error messages
3. Common issues:
   - Missing dependencies in requirements.txt
   - Syntax errors in Dockerfile
   - Port configuration issues

**Solutions**:
- Verify all files are committed
- Check Dockerfile syntax
- Ensure port 7860 is exposed

### Application Not Loading

**Symptoms**: Space shows running but page doesn't load

**Check**:
- [ ] Port 7860 is exposed in Dockerfile
- [ ] Nginx is configured correctly
- [ ] Backend health check passes

**Debug**:
```bash
# Check logs for:
- "Nginx started on port 7860"
- "Backend is ready"
- "AURORA is running!"
```

### API Errors

**Symptoms**: Frontend loads but API calls fail

**Check**:
- [ ] Environment variables are set correctly
- [ ] GCP credentials are valid
- [ ] Backend logs show no errors

**Solutions**:
1. Verify `GOOGLE_APPLICATION_CREDENTIALS_JSON` is set
2. Check GCP project permissions
3. Review backend logs for specific errors

### Database Issues

**Symptoms**: Data doesn't persist or errors on startup

**Remember**: Free tier uses ephemeral storage
- Data resets on container restart
- For persistence, upgrade to persistent storage

**Workaround**:
- Use external database (PostgreSQL)
- Export/import data via API

## Performance Optimization

### Free Tier Limits
- **CPU**: 2 vCPUs
- **RAM**: 16 GB
- **Storage**: 50 GB (ephemeral)
- **Sleep**: After 48 hours of inactivity

### Tips
- [ ] Monitor resource usage in Space analytics
- [ ] Optimize database queries
- [ ] Use caching where appropriate
- [ ] Consider upgrading for production use

## Updating Your Deployment

To update your deployed Space:

```bash
# Make changes locally
git add .
git commit -m "Update: description"

# Push to Hugging Face
git push hf main
```

The Space will automatically rebuild.

## Rollback

If deployment fails:

```bash
# Revert to previous commit
git revert HEAD
git push hf main --force
```

## Support Resources

- [ ] Read [Hugging Face Spaces Docs](https://huggingface.co/docs/hub/spaces)
- [ ] Check [AURORA Documentation](README_HF_DEPLOYMENT.md)
- [ ] Visit [Hugging Face Community](https://discuss.huggingface.co/)
- [ ] Review [Docker Documentation](https://docs.docker.com/)

## Success Criteria

Your deployment is successful when:

- ✅ Space shows "Running" status
- ✅ Homepage loads at your Space URL
- ✅ Dashboard displays without errors
- ✅ API documentation accessible at `/docs`
- ✅ Health check returns 200 OK
- ✅ Test model connection works
- ✅ No errors in logs

## Next Steps

After successful deployment:

1. **Test thoroughly**:
   - Send test metrics
   - Query memory store
   - Check agent decisions

2. **Integrate your models**:
   - Use provided Python code
   - Update API endpoints
   - Monitor in Dashboard

3. **Monitor performance**:
   - Check Space analytics
   - Review logs regularly
   - Watch for errors

4. **Share your Space**:
   - Update README with your info
   - Add screenshots
   - Share on social media

---

## Quick Reference

**Your Space URL**: `https://YOUR_USERNAME-YOUR_SPACE_NAME.hf.space`

**API Endpoints**:
- Health: `/health`
- Metrics: `/api/metrics`
- Decisions: `/api/decisions`
- Memory: `/api/memory/search`
- Docs: `/docs`

**Logs Location**: Space → Logs tab

**Settings**: Space → Settings → Repository secrets

---

**Need Help?** Check the [deployment guide](README_HF_DEPLOYMENT.md) or open an issue on GitHub.
