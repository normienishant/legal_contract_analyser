# 🚂 Railway Deployment Guide

## Quick Start

### 1. Connect Repository
1. Go to [Railway.app](https://railway.app)
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your repository

### 2. Configure Service

Railway will auto-detect your `Dockerfile` and `railway.json`.

**Important Settings:**

#### Root Directory
- If your repo root is `ai_cti/`, set Root Directory to: `ai_cti`
- If Railway detects the repo correctly, leave empty

#### Build Settings
- **Builder**: Dockerfile (auto-detected)
- **Dockerfile Path**: `Dockerfile` (or `ai_cti/Dockerfile` if root is different)

#### Start Command
- Auto-detected from `railway.json`: `python -m uvicorn api.main:app --host 0.0.0.0 --port $PORT`

### 3. Environment Variables

Add these in Railway dashboard → Service → Variables:

```bash
# Server (Railway auto-injects PORT)
PORT=${{PORT}}

# Database (if using PostgreSQL)
# Add PostgreSQL service first, then reference:
DATABASE_URL=${{Postgres.DATABASE_URL}}

# Security
SECRET_KEY=your-secret-key-here-generate-random-string

# CORS - Add your frontend URLs
ALLOWED_ORIGINS=https://your-frontend.vercel.app,https://your-frontend.onrender.com

# Optional
ENVIRONMENT=production
LOG_LEVEL=INFO
```

### 4. Add PostgreSQL (Optional)

If you need a database:

1. Click "+ New" in Railway dashboard
2. Select "Database" → "Add PostgreSQL"
3. Wait for database to provision
4. In your service, go to "Variables" tab
5. Click "+ New Variable" → "Reference"
6. Select PostgreSQL service → `DATABASE_URL`
7. This will auto-link the database

### 5. Deploy

1. Railway will automatically start building
2. Watch build logs in "Deployments" tab
3. Once complete, your service will be live
4. Copy the generated URL: `https://your-app.railway.app`

### 6. Test

Visit your Railway URL:
- Health check: `https://your-app.railway.app/`
- API docs: `https://your-app.railway.app/docs`

Expected response:
```json
{
  "status": "ok",
  "service": "AI-CTI API",
  "docs": "/docs"
}
```

## Troubleshooting

### Build Fails
- Check Dockerfile path is correct
- Verify `requirements.txt` exists
- Check build logs for specific errors

### Service Won't Start
- Verify `PORT` environment variable is set (Railway auto-injects this)
- Check start command matches your app structure
- Review logs in Railway dashboard

### Database Connection Issues
- Ensure PostgreSQL service is linked
- Verify `DATABASE_URL` is set correctly
- Check database is running (not paused)

### CORS Errors
- Add frontend URL to `ALLOWED_ORIGINS`
- Redeploy after adding environment variable

## Railway.json Configuration

The `railway.json` file configures:
- Build method (Dockerfile)
- Start command
- Restart policy

Current configuration:
```json
{
  "build": {
    "builder": "DOCKERFILE",
    "dockerfilePath": "Dockerfile"
  },
  "deploy": {
    "startCommand": "python -m uvicorn api.main:app --host 0.0.0.0 --port $PORT",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

## Free Tier Limits

Railway free tier includes:
- $5 credit per month
- 500 hours of usage
- Automatic sleep after inactivity

**Note**: For production/interviews, consider:
- Paid plan ($5/month) for always-on
- Or use Render as backup (failover system handles this)

## Next Steps

After Railway is deployed:
1. Copy Railway URL
2. Deploy to Render (backup)
3. Configure frontend with both URLs
4. Test failover system

See `FAILOVER_SETUP.md` for complete dual-platform setup.




