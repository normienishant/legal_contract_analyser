# 🚀 Backend Hosting on Railway - Complete Guide

## ✅ Why Railway?

- ✅ **$5 free credit/month** (enough for backend!)
- ✅ **GitHub integration** - auto-deploys from your repo
- ✅ **No credit card required** initially
- ✅ **Super easy setup** - 5 minutes!
- ✅ **PostgreSQL included** (free tier)
- ✅ **Auto-deploy** on every push
- ✅ **Great for FastAPI**

**Link:** [railway.app](https://railway.app)

---

## 📋 Prerequisites

1. ✅ GitHub repository: `normienishant/legal_contract_analyser`
2. ✅ Code pushed to GitHub (already done ✅)
3. ✅ Railway account (free signup)

---

## 🎯 Step 1: Create Railway Account

1. Go to **[railway.app](https://railway.app)**
2. Click **"Start a New Project"**
3. Sign up with **GitHub** (recommended)
   - Click **"Login with GitHub"**
   - Authorize Railway
   - Done!

---

## 🚀 Step 2: Deploy Backend

### 2.1 Create New Project

1. After login, click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Select repository: `normienishant/legal_contract_analyser`
4. Click **"Deploy Now"**

### 2.2 Configure Backend Service

Railway will auto-detect your project. Now configure:

1. **Service Settings:**
   - Click on the service (or "Add Service" → "GitHub Repo")
   - Select: `normienishant/legal_contract_analyser`
   - **Root Directory:** `backend` ⚠️ **IMPORTANT!**
   - Railway will auto-detect Python

2. **Build Settings:**
   - Railway auto-detects `requirements.txt`
   - Build Command: Auto (or `pip install -r requirements.txt`)
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

3. **Environment Variables:**
   Click **"Variables"** tab → Add:

   ```
   ML_MODE=ml
   SECRET_KEY=<generate-random-32-chars>
   ALLOWED_ORIGINS=https://your-frontend.vercel.app,http://localhost:3000
   ENVIRONMENT=production
   LOG_LEVEL=INFO
   PORT=$PORT
   ```

   **Generate SECRET_KEY:**
   ```powershell
   -join ((48..57) + (65..90) + (97..122) | Get-Random -Count 32 | ForEach-Object {[char]$_})
   ```

4. **Settings:**
   - **Root Directory:** `backend` ⚠️ **CRITICAL!**
   - Railway will auto-detect the rest

### 2.3 Deploy!

1. Railway will automatically:
   - Clone your repo
   - Install dependencies
   - Start your app
2. **Wait 2-5 minutes** for first deployment
3. Check **"Deployments"** tab for progress

---

## 🗄️ Step 3: Add PostgreSQL (Optional)

**Note:** You can use SQLite (no database needed) OR PostgreSQL

### If Adding PostgreSQL:

1. In your project, click **"New"** → **"Database"** → **"Add PostgreSQL"**
2. Railway will create database automatically
3. **Copy the DATABASE_URL** from the database service
4. Add to backend service variables:
   ```
   DATABASE_URL=<paste-database-url>
   ```
5. Backend will auto-redeploy

### If Using SQLite (Recommended):

- No database service needed!
- Backend uses SQLite automatically
- Database file stored in service

---

## ✅ Step 4: Get Your Backend URL

1. Go to your backend service
2. Click **"Settings"** tab
3. Scroll to **"Domains"**
4. Click **"Generate Domain"**
5. Your backend URL: `https://your-service-name.up.railway.app`

**Or Railway auto-generates:** `https://<random-name>.up.railway.app`

---

## 📊 Step 5: Monitor Deployment

### Check Logs:

1. Go to your service → **"Deployments"** tab
2. Click on latest deployment
3. Watch logs for:
   - ✅ `Installing dependencies...`
   - ✅ `Building...`
   - ✅ `Starting...`
   - ✅ `Application startup complete`
   - ✅ `Uvicorn running on http://0.0.0.0:PORT`

---

## ✅ Step 6: Verify Deployment

### Test Endpoints:

1. **Health Check:**
   - Visit: `https://your-service.up.railway.app/health`
   - Should return: `{"status": "healthy", "ml_mode": "ml"}`

2. **API Docs:**
   - Visit: `https://your-service.up.railway.app/docs`
   - Should show Swagger UI

3. **Root:**
   - Visit: `https://your-service.up.railway.app/`
   - Should return API info

---

## 🔧 Step 7: Configure Settings

### Update Root Directory (If Not Set):

1. Go to service → **"Settings"** tab
2. Scroll to **"Source"**
3. Set **"Root Directory"** to: `backend`
4. Click **"Save"**
5. Service will redeploy

### Update Start Command:

1. Go to service → **"Settings"** tab
2. Scroll to **"Deploy"**
3. Set **"Start Command"** to:
   ```
   uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```
4. Click **"Save"**

---

## 📝 Environment Variables Summary

### Required:

| Variable | Value | Notes |
|----------|-------|-------|
| `ML_MODE` | `ml` | Use ML model |
| `SECRET_KEY` | Random 32 chars | Generate above |
| `ALLOWED_ORIGINS` | Frontend URLs | Comma-separated |
| `ENVIRONMENT` | `production` | |
| `LOG_LEVEL` | `INFO` | |
| `PORT` | `$PORT` | Auto-set by Railway |

### Optional (If Using PostgreSQL):

| Variable | Value | Notes |
|----------|-------|-------|
| `DATABASE_URL` | From PostgreSQL service | Auto-provided |

---

## 🎯 Important Notes

### Free Tier:
- ✅ **$5 credit/month** (enough for backend!)
- ✅ **512MB RAM** per service
- ✅ **1GB disk** per service
- ✅ **PostgreSQL** included (free tier)
- ✅ **Auto-deploy** on push
- ⚠️ **Sleeps after inactivity** (wakes on request)

### Best Practices:
- ✅ Use SQLite for simplicity (no database service)
- ✅ Set Root Directory to `backend`
- ✅ Use `$PORT` in start command
- ✅ Update `ALLOWED_ORIGINS` with frontend URL
- ✅ Monitor usage in dashboard

---

## 🐛 Troubleshooting

### Service Won't Start:
1. Check **"Deployments"** → **"Logs"**
2. Verify **Root Directory** is `backend`
3. Check **Start Command** uses `$PORT`
4. Verify all dependencies in `requirements.txt`

### Build Fails:
1. Check logs for specific errors
2. Verify Python version (3.9+)
3. Check `requirements.txt` compatibility
4. Verify Root Directory is correct

### 404 Errors:
1. Verify Root Directory is `backend`
2. Check service is running (not sleeping)
3. Verify routes are correct

### CORS Errors:
1. Update `ALLOWED_ORIGINS` with frontend URL
2. Ensure no trailing slashes
3. Check frontend is using correct backend URL

---

## 🎉 After Deployment

1. ✅ Note your backend URL: `https://your-service.up.railway.app`
2. ✅ Test all endpoints
3. ✅ Update frontend `NEXT_PUBLIC_API_URL` with backend URL
4. ✅ Deploy frontend on Vercel
5. ✅ Test full application!

---

## 🚀 Auto-Deploy

Railway automatically deploys when you push to GitHub!

1. Make changes locally
2. Push to GitHub: `git push origin master`
3. Railway auto-deploys in 2-3 minutes
4. Done! 🎉

---

## 📚 Quick Reference

**Backend URL Format:**
```
https://<service-name>.up.railway.app
```

**Important Endpoints:**
- Health: `/health`
- API Docs: `/docs`
- Root: `/`

**Railway Dashboard:**
- [railway.app/dashboard](https://railway.app/dashboard)

---

## 🎯 Summary

**Railway is perfect because:**
- ✅ GitHub integration (no manual upload)
- ✅ $5 free credit/month
- ✅ Super easy setup
- ✅ Auto-deploy on push
- ✅ PostgreSQL included
- ✅ Great documentation

**Ready? Follow the steps above and your backend will be live in 5 minutes!** 🚀

