# 🔄 Automatic Failover Setup Guide

## Overview

Your Contract Analyzer now has **automatic failover** between Railway and Render. If Railway goes down or runs out of minutes, it automatically switches to Render - **your backend will never go down!**

---

## 🎯 How It Works

1. **Primary Backend**: Railway (tried first)
2. **Backup Backend**: Render (used if Railway fails)
3. **Automatic Detection**: System checks which backend is working
4. **Smart Caching**: Remembers working backend for 5 minutes
5. **Seamless Switching**: User doesn't notice the switch

---

## 📋 Setup Steps

### Step 1: Deploy on Railway

1. Go to https://railway.app
2. Create new project → Deploy from GitHub
3. Select your repository: `normienishant/legal_contract_analyser`
4. Add PostgreSQL database
5. Configure backend service (see `DEPLOYMENT_DUAL_PLATFORM.md`)
6. Get your Railway backend URL: `https://your-app.railway.app`

### Step 2: Deploy on Render

1. Go to https://render.com
2. Create new Web Service
3. Connect GitHub repository
4. Configure backend (see `DEPLOYMENT_DUAL_PLATFORM.md`)
5. Get your Render backend URL: `https://contract-analyzer-backend-xxxx.onrender.com`

### Step 3: Configure Frontend Environment Variables

In **Vercel** (or your frontend hosting):

Go to **Settings → Environment Variables** and add:

```env
# Railway (Primary)
NEXT_PUBLIC_RAILWAY_API_URL=https://your-app.railway.app

# Render (Backup)
NEXT_PUBLIC_RENDER_API_URL=https://contract-analyzer-backend-xxxx.onrender.com

# Legacy (optional fallback)
NEXT_PUBLIC_API_URL=https://your-app.railway.app
```

### Step 4: Update CORS on Both Backends

**Railway Backend Environment Variables:**
```env
ALLOWED_ORIGINS=https://legal-contract-risk-analyser.vercel.app,https://contract-analyzer-frontend.onrender.com
```

**Render Backend Environment Variables:**
```env
ALLOWED_ORIGINS=https://legal-contract-risk-analyser.vercel.app,https://contract-analyzer-frontend.onrender.com
```

### Step 5: Redeploy Frontend

After setting environment variables, redeploy your frontend on Vercel.

---

## ✅ Testing Failover

### Test 1: Check Both Backends Work

1. Open browser console (F12)
2. Go to Settings page
3. Check "Current Backend" shows Railway URL
4. Verify "Backend Connected" shows ✅

### Test 2: Simulate Railway Failure

1. Stop Railway service (or let it timeout)
2. Make an API request (upload file, view history)
3. Check console - should automatically switch to Render
4. Settings page should show Render URL

### Test 3: Railway Recovery

1. Start Railway service again
2. Wait 5 minutes (cache expires)
3. Make new request
4. Should automatically switch back to Railway

---

## 🔧 How Failover Works

### Request Flow

```
1. User makes API request
   ↓
2. Check cached working backend (if < 5 min old)
   ↓
3. Try cached backend first
   ↓
4. If fails, try Railway
   ↓
5. If Railway fails, try Render
   ↓
6. If Render fails, try fallback (localhost)
   ↓
7. Cache working backend for 5 minutes
```

### Health Check

- Each backend is checked via `/health` endpoint
- 3 second timeout per check
- If health check fails, tries next backend

### Caching

- Working backend URL stored in `localStorage`
- Cache expires after 5 minutes
- Cache cleared on browser refresh (optional)

---

## 📊 Monitoring

### Check Current Backend

1. Go to **Settings** page
2. Look at "Backend Connection Status"
3. Shows current backend URL
4. Shows "Automatic failover enabled" message

### Browser Console

```javascript
// Check current backend
localStorage.getItem('working_backend_url')

// Clear cache (force re-detection)
localStorage.removeItem('working_backend_url')
localStorage.removeItem('working_backend_url_time')
```

---

## 🚨 Troubleshooting

### Issue: Both Backends Failing

**Solution:**
1. Check Railway dashboard - is service running?
2. Check Render dashboard - is service running?
3. Check CORS settings on both backends
4. Verify environment variables in Vercel

### Issue: Stuck on One Backend

**Solution:**
1. Clear browser cache
2. Clear localStorage:
   ```javascript
   localStorage.removeItem('working_backend_url')
   localStorage.removeItem('working_backend_url_time')
   ```
3. Refresh page

### Issue: Slow Requests

**Solution:**
1. Railway might be cold-starting (first request slow)
2. Render free tier spins down after 15 min (50+ sec first request)
3. Consider upgrading to paid tier for faster response

---

## 💡 Best Practices

1. **Keep Both Backends Running**: Even if one is primary, keep both active
2. **Monitor Both**: Check both dashboards regularly
3. **Database Sync**: Note that each backend has its own database (data doesn't sync)
4. **Model Files**: Upload ML models to both backends
5. **Environment Variables**: Keep them in sync

---

## 🎯 Interview Talking Points

When showing your project:

1. **"I implemented automatic failover for high availability"**
   - "If Railway goes down, it automatically switches to Render"
   - "The backend never goes down, perfect for interviews"

2. **"Smart caching reduces latency"**
   - "Remembers working backend for 5 minutes"
   - "Only checks health when needed"

3. **"Seamless user experience"**
   - "Users don't notice the switch"
   - "No error messages, just works"

4. **"Production-ready architecture"**
   - "Redundancy at infrastructure level"
   - "Follows best practices for reliability"

---

## 📝 Code Structure

- `frontend/lib/api-failover.ts` - Failover logic
- `frontend/lib/api.ts` - Updated to use failover
- `frontend/components/Uploader.tsx` - Uses failover
- `frontend/app/settings/page.tsx` - Shows current backend

---

## ✅ Checklist

- [ ] Railway backend deployed
- [ ] Render backend deployed
- [ ] Environment variables set in Vercel
- [ ] CORS configured on both backends
- [ ] Frontend redeployed
- [ ] Tested failover (stop Railway, check Render works)
- [ ] Settings page shows correct backend
- [ ] Both backends have same ML model

---

**Your backend will never go down! Perfect for interviews! 🚀**

