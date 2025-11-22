# 🔄 Automatic Failover Setup Guide

## Overview
Your AI-CTI backend now has **automatic failover** between Railway (primary) and Render (backup). If Railway goes down or runs out of minutes, it automatically switches to Render - **your backend will never go down during interviews!**

## How It Works

1. **Primary**: Railway (tries first)
2. **Backup**: Render (if Railway fails)
3. **Fallback**: Local/configured URL (if both fail)

### Features
- ✅ Automatic health checking
- ✅ Smart caching (5 minutes)
- ✅ Seamless switching (user doesn't notice)
- ✅ Retry logic with exponential backoff
- ✅ Works with all API endpoints

## Setup Instructions

### Step 1: Deploy to Railway

1. Go to [Railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Railway will auto-detect the Dockerfile

#### Configure Railway Service:

**Root Directory**: Leave empty (or set to `ai_cti` if repo root is different)

**Environment Variables**:
```bash
# Database (if using PostgreSQL)
DATABASE_URL=${{Postgres.DATABASE_URL}}

# Server
PORT=${{PORT}}

# Security
SECRET_KEY=your-secret-key-here

# CORS (add your frontend URLs)
ALLOWED_ORIGINS=https://your-frontend.vercel.app,https://your-frontend.onrender.com

# Optional
ENVIRONMENT=production
LOG_LEVEL=INFO
```

5. Wait for deployment to complete
6. Copy your Railway URL: `https://your-app.railway.app`

### Step 2: Deploy to Render (Backup)

1. Go to [Render.com](https://render.com)
2. Click "New" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: `ai-cti-backend`
   - **Root Directory**: `ai_cti` (or leave empty if repo root)
   - **Environment**: `Docker`
   - **Dockerfile Path**: `Dockerfile`
   - **Start Command**: (auto-detected from Dockerfile)

5. Add Environment Variables (same as Railway)
6. Deploy
7. Copy your Render URL: `https://your-app.onrender.com`

### Step 3: Configure Frontend (Vercel)

1. Go to your Vercel project settings
2. Navigate to "Environment Variables"
3. Add these variables:

```bash
# Primary Backend (Railway)
NEXT_PUBLIC_RAILWAY_API_URL=https://your-app.railway.app

# Backup Backend (Render)
NEXT_PUBLIC_RENDER_API_URL=https://your-app.onrender.com

# Fallback (optional, for local dev)
NEXT_PUBLIC_API_URL=http://localhost:8000
```

4. Redeploy your frontend

### Step 4: Test Failover

1. **Test Railway**: 
   - Visit your frontend
   - Check browser console - should see Railway URL being used

2. **Test Failover**:
   - Stop Railway service (or let it run out of minutes)
   - Make a request from frontend
   - Should automatically switch to Render
   - Check console - should see "trying next backend"

3. **Verify**:
   - Both backends should respond to `/` health check
   - Frontend should seamlessly switch between them

## How Failover Works

### Request Flow:
```
1. Frontend makes API request
2. Check cached backend (if valid, use it)
3. Try Railway (primary)
   ├─ Success → Cache & return
   └─ Fail → Try Render
      ├─ Success → Cache & return
      └─ Fail → Try fallback/local
```

### Health Check:
- Checks `/` endpoint
- 5 second timeout
- Looks for `status: "ok"` or `status: "healthy"`

### Caching:
- Working backend cached for 5 minutes
- Cache cleared on failure
- Prevents unnecessary health checks

## Monitoring

### Check Current Backend:
The failover system logs which backend is being used:
- Check browser console (client-side)
- Check Vercel logs (server-side API routes)

### Logs to Look For:
```
[api-failover] Backend returned 502, trying next backend...
[api-failover] Network error, trying next backend...
```

## Troubleshooting

### Issue: Both backends failing
**Solution**: Check environment variables, ensure both services are running

### Issue: Failover not working
**Solution**: 
1. Verify environment variables are set in Vercel
2. Check that both Railway and Render URLs are correct
3. Ensure both backends respond to `/` health check

### Issue: Slow responses
**Solution**: 
- Health checks add ~5s on first request
- Subsequent requests use cached backend (fast)
- Consider reducing health check timeout if needed

## Production Checklist

- [ ] Railway deployed and running
- [ ] Render deployed and running
- [ ] Environment variables set in Vercel
- [ ] Both backends respond to `/` endpoint
- [ ] Frontend redeployed with new env vars
- [ ] Failover tested (stop Railway, verify Render works)
- [ ] CORS configured on both backends

## Interview Ready! 🎯

Your backend now has:
- ✅ High availability (Railway + Render)
- ✅ Automatic failover
- ✅ Zero downtime
- ✅ Production-ready setup

**Perfect for interviews!** You can confidently say:
- "I implemented automatic failover for high availability"
- "Backend never goes down - Railway primary, Render backup"
- "Seamless switching with zero user impact"




