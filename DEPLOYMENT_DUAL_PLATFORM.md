# 🚀 Dual Platform Deployment Guide
## Railway + Render Setup

This guide will help you deploy your Contract Analyzer on both **Railway** and **Render** for redundancy and reliability.

---

## 📋 Prerequisites

1. **GitHub Repository** (already set up)
2. **Railway Account**: https://railway.app (Sign up with GitHub)
3. **Render Account**: https://render.com (Sign up with GitHub)

---

## 🚂 Railway Deployment

### Step 1: Create Railway Project

1. Go to https://railway.app
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Choose your repository: `normienishant/legal_contract_analyser`
5. Select branch: `master`

### Step 2: Add PostgreSQL Database

1. In your Railway project, click **"+ New"**
2. Select **"Database"** → **"Add PostgreSQL"**
3. Wait for database to provision
4. Copy the **DATABASE_URL** from the database service

### Step 3: Configure Backend Service

1. Railway will auto-detect your `railway.json` config
2. If not auto-detected, click **"+ New"** → **"GitHub Repo"**
3. Select your repository
4. **Root Directory**: `backend`
5. **Build Command**: (auto-detected from railway.json)
6. **Start Command**: (auto-detected from railway.json)

### Step 4: Set Environment Variables (Railway)

Go to your backend service → **Variables** tab → Add:

```env
# Database
DATABASE_URL=${{Postgres.DATABASE_URL}}
# (Railway auto-injects this if you link the database)

# ML Configuration
ML_MODE=ml
MODEL_PATH=./models/risk_classifier

# Server
PORT=${{PORT}}
# (Railway auto-injects PORT)

# Security
SECRET_KEY=your-secret-key-here-generate-random
ALLOWED_ORIGINS=https://your-railway-app.railway.app,https://your-render-app.onrender.com

# Optional
ENVIRONMENT=production
LOG_LEVEL=INFO
MAX_UPLOAD_SIZE_MB=10
```

**To link database:**
1. Go to backend service → **Variables** tab
2. Click **"+ New Variable"**
3. Select **"Reference"** tab
4. Choose your PostgreSQL service
5. Select **DATABASE_URL**

### Step 5: Deploy Frontend on Railway (Optional)

1. Click **"+ New"** → **"GitHub Repo"**
2. Select your repository
3. **Root Directory**: `frontend`
4. **Build Command**: `npm install && npm run build`
5. **Start Command**: `npm start`
6. **Environment Variables**:
   ```env
   NEXT_PUBLIC_API_URL=https://your-railway-backend.railway.app
   ```

### Step 6: Get Railway URLs

- Backend: `https://your-app-name.railway.app`
- Frontend: `https://your-frontend-name.railway.app`

---

## 🎨 Render Deployment

### Step 1: Create Render Account & Connect GitHub

1. Go to https://render.com
2. Sign up with GitHub
3. Connect your repository: `normienishant/legal_contract_analyser`

### Step 2: Deploy Backend on Render

1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository
3. **Settings**:
   - **Name**: `contract-analyzer-backend`
   - **Root Directory**: `backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: `Free` (or `Starter` for better performance)

### Step 3: Add PostgreSQL Database on Render

1. Click **"New +"** → **"PostgreSQL"**
2. **Name**: `contract-analyzer-db`
3. **Plan**: `Free` (or `Starter`)
4. **Region**: Choose closest to you
5. Click **"Create Database"**
6. Copy the **Internal Database URL** and **External Database URL**

### Step 4: Set Environment Variables (Render)

Go to your backend service → **Environment** tab → Add:

```env
# Database
DATABASE_URL=<your-render-postgres-internal-url>

# ML Configuration
ML_MODE=ml
MODEL_PATH=./models/risk_classifier

# Server
PORT=$PORT
# (Render auto-injects PORT)

# Security
SECRET_KEY=your-secret-key-here-generate-random
ALLOWED_ORIGINS=https://contract-analyzer-backend-xxxx.onrender.com,https://your-railway-app.railway.app

# Optional
ENVIRONMENT=production
LOG_LEVEL=INFO
MAX_UPLOAD_SIZE_MB=10
```

### Step 5: Deploy Frontend on Render

1. Click **"New +"** → **"Static Site"**
2. Connect your GitHub repository
3. **Settings**:
   - **Name**: `contract-analyzer-frontend`
   - **Root Directory**: `frontend`
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: `.next`
   - **Environment Variables**:
     ```env
     NEXT_PUBLIC_API_URL=https://contract-analyzer-backend-xxxx.onrender.com
     ```

### Step 6: Get Render URLs

- Backend: `https://contract-analyzer-backend-xxxx.onrender.com`
- Frontend: `https://contract-analyzer-frontend.onrender.com`

---

## 🔄 Using Both Platforms

### Option 1: Primary/Backup Setup

- **Primary**: Railway (better free tier limits)
- **Backup**: Render (when Railway has issues)

Update frontend `NEXT_PUBLIC_API_URL` to point to Railway, but keep Render as backup.

### Option 2: Load Balancing

Use both backends and switch between them in frontend:

```typescript
// frontend/lib/api.ts
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 
  (Math.random() > 0.5 
    ? 'https://your-railway-backend.railway.app'
    : 'https://contract-analyzer-backend-xxxx.onrender.com');
```

### Option 3: Different Environments

- **Railway**: Production
- **Render**: Staging/Development

---

## 🔧 Troubleshooting

### Railway Issues

1. **Build Fails**:
   - Check `railway.json` is in root
   - Verify `backend/requirements.txt` exists
   - Check build logs in Railway dashboard

2. **Database Connection**:
   - Ensure DATABASE_URL is linked correctly
   - Check database service is running

3. **Port Issues**:
   - Railway auto-injects `$PORT`, don't hardcode

### Render Issues

1. **Build Blocked (Pipeline Minutes)**:
   - Wait for monthly reset
   - Upgrade to paid plan
   - Use Railway as primary

2. **Service Spins Down**:
   - Free tier spins down after 15 min inactivity
   - First request takes 50+ seconds
   - Upgrade to paid plan to avoid this

3. **Database Connection**:
   - Use **Internal Database URL** for backend
   - External URL is for local connections

---

## 📊 Comparison

| Feature | Railway | Render |
|---------|---------|--------|
| Free Tier | ✅ Yes | ✅ Yes |
| Auto-Deploy | ✅ Yes | ✅ Yes |
| PostgreSQL | ✅ Free tier | ✅ Free tier |
| Pipeline Minutes | ✅ 500/month | ⚠️ 750/month (limited) |
| Spin Down | ❌ No | ⚠️ Yes (15 min inactivity) |
| Custom Domain | ✅ Yes | ✅ Yes |
| SSL | ✅ Auto | ✅ Auto |

---

## ✅ Deployment Checklist

### Railway
- [ ] Project created
- [ ] PostgreSQL database added
- [ ] Backend service configured
- [ ] Environment variables set
- [ ] Database linked
- [ ] Frontend deployed (optional)
- [ ] URLs tested

### Render
- [ ] Account created
- [ ] Repository connected
- [ ] PostgreSQL database added
- [ ] Backend service configured
- [ ] Environment variables set
- [ ] Frontend deployed
- [ ] URLs tested

### Both
- [ ] CORS configured (ALLOWED_ORIGINS)
- [ ] Database migrations run
- [ ] Health check endpoints working
- [ ] Frontend pointing to correct backend

---

## 🎯 Quick Commands

### Check Railway Status
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Link project
railway link

# View logs
railway logs
```

### Check Render Status
- Visit https://dashboard.render.com
- Check service status and logs

---

## 📝 Notes

1. **Database**: Each platform needs its own database (data won't sync)
2. **Model Files**: ML models need to be uploaded to both platforms
3. **Environment Variables**: Keep them in sync between platforms
4. **CORS**: Update `ALLOWED_ORIGINS` to include both frontend URLs

---

## 🚀 Next Steps

1. Deploy on Railway first (better free tier)
2. Deploy on Render as backup
3. Test both deployments
4. Update frontend to use Railway as primary
5. Monitor both services

---

**Need Help?** Check the logs in each platform's dashboard for detailed error messages.

