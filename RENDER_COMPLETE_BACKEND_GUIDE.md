# 🚀 Complete Backend Hosting on Render - Step by Step

## 📋 Prerequisites

1. ✅ New Render account (different browser/email)
2. ✅ GitHub repository: `normienishant/legal_contract_analyser`
3. ✅ Code pushed to GitHub (already done ✅)

---

## 🎯 Step 1: Create Render Account

1. Open **new browser** or **incognito window**
2. Go to **[https://dashboard.render.com](https://dashboard.render.com)**
3. Click **"Get Started for Free"**
4. Sign up with:
   - **GitHub** (recommended) - use different GitHub account OR
   - **Email** - use different email
5. Verify email if needed

---

## 🗄️ Step 2: Create PostgreSQL Database (Optional)

**Note:** Free tier allows 1 PostgreSQL database. If you want to use SQLite (simpler), skip this step!

### If Creating Database:
1. Click **"New +"** → **"PostgreSQL"**
2. Fill in:
   - **Name:** `contract-analyzer-db`
   - **Region:** `Oregon (US West)` (or closest)
   - **PostgreSQL Version:** `18`
   - **Plan:** **Free**
3. Click **"Create Database"**
4. Wait 2-3 minutes
5. **Copy Internal Database URL** (you'll need it)

### If Using SQLite (Recommended):
- Skip database creation
- Backend will use SQLite automatically
- No database service needed!

---

## 🚀 Step 3: Deploy Backend Web Service

### 3.1 Connect Repository

1. In Render Dashboard, click **"New +"** → **"Web Service"**

2. **Connect GitHub:**
   - Click **"Connect GitHub"** (if first time)
   - Authorize Render
   - Select repository: `normienishant/legal_contract_analyser`
   - Click **"Connect"**

### 3.2 Configure Service

Fill in these settings:

- **Name:** `contract-analyzer-backend`
- **Region:** `Oregon (US West)` (or same as database if created)
- **Branch:** `master` ⚠️ **IMPORTANT!**
- **Root Directory:** `backend` ⚠️ **CRITICAL!**
- **Runtime:** `Python 3`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### 3.3 Add Environment Variables

Click **"Advanced"** → **"Add Environment Variable"** and add:

#### If Using SQLite (Recommended):
```
ML_MODE = ml
SECRET_KEY = <generate-random-32-chars>
ALLOWED_ORIGINS = https://your-frontend.vercel.app,http://localhost:3000
ENVIRONMENT = production
LOG_LEVEL = INFO
PORT = $PORT
```

#### If Using PostgreSQL:
```
DATABASE_URL = <paste-internal-database-url>
ML_MODE = ml
SECRET_KEY = <generate-random-32-chars>
ALLOWED_ORIGINS = https://your-frontend.vercel.app,http://localhost:3000
ENVIRONMENT = production
LOG_LEVEL = INFO
PORT = $PORT
```

**Generate SECRET_KEY:**
```powershell
-join ((48..57) + (65..90) + (97..122) | Get-Random -Count 32 | ForEach-Object {[char]$_})
```

**Example SECRET_KEY:** `aB3dE5fG7hI9jK1lM3nO5pQ7rS9tU1vW3xY5zA7bC9dE1`

### 3.4 Add Persistent Disk (For SQLite)

**If using SQLite, add disk for database persistence:**

1. Click **"Advanced"** → **"Add Disk"**
2. Fill in:
   - **Name:** `sqlite-storage`
   - **Mount Path:** `/opt/render/project/src`
   - **Size:** `1 GB` (free tier max)
3. This ensures SQLite database persists across deployments

### 3.5 Deploy!

1. Click **"Create Web Service"**
2. **Wait 5-10 minutes** for first deployment
3. Watch the **"Logs"** tab for progress

---

## 📊 Step 4: Monitor Deployment

### Check Build Logs:

1. Go to your service → **"Logs"** tab
2. Watch for:
   - ✅ `Installing dependencies...`
   - ✅ `Building application...`
   - ✅ `Starting application...`
   - ✅ `Application startup complete`
   - ✅ `Uvicorn running on http://0.0.0.0:PORT`

### Common Issues:

- ❌ **Build fails:** Check `requirements.txt` compatibility
- ❌ **Import errors:** Check Python version (should be 3.9+)
- ❌ **Port error:** Make sure using `$PORT` in start command
- ❌ **Database error:** Check `DATABASE_URL` if using PostgreSQL

---

## ✅ Step 5: Verify Deployment

### Test Endpoints:

1. **Health Check:**
   - Visit: `https://your-backend-name.onrender.com/health`
   - Should return: `{"status": "healthy", "ml_mode": "ml"}`

2. **API Docs:**
   - Visit: `https://your-backend-name.onrender.com/docs`
   - Should show Swagger UI with all endpoints

3. **Root Endpoint:**
   - Visit: `https://your-backend-name.onrender.com/`
   - Should return: `{"message": "AI Contract Analyzer & Risk Detector API", ...}`

---

## 🔧 Step 6: Update CORS (If Needed)

After deployment, if frontend can't connect:

1. Go to your service → **"Environment"** tab
2. Update `ALLOWED_ORIGINS`:
   ```
   ALLOWED_ORIGINS = https://your-frontend.vercel.app,http://localhost:3000,https://your-backend.onrender.com
   ```
3. Click **"Save Changes"**
4. Service will auto-redeploy

---

## 📝 Environment Variables Summary

### Required Variables:

| Variable | Value | Notes |
|----------|-------|-------|
| `ML_MODE` | `ml` | Use ML model |
| `SECRET_KEY` | Random 32 chars | Generate above |
| `ALLOWED_ORIGINS` | Frontend URLs | Comma-separated |
| `ENVIRONMENT` | `production` | |
| `LOG_LEVEL` | `INFO` | |
| `PORT` | `$PORT` | Auto-set by Render |

### Optional (If Using PostgreSQL):

| Variable | Value | Notes |
|----------|-------|-------|
| `DATABASE_URL` | Internal DB URL | From PostgreSQL service |

---

## 🎯 Important Notes

### Free Tier Limits:
- ⚠️ **Web Service:** Spins down after 15 min inactivity
- ⚠️ **First request:** May take 30-60 seconds (cold start)
- ⚠️ **Database:** 1 PostgreSQL free (or use SQLite)
- ⚠️ **Disk:** 1GB free
- ⚠️ **Build Time:** 10 min max

### Best Practices:
- ✅ Use SQLite for simplicity (no database service needed)
- ✅ Add persistent disk for SQLite
- ✅ Use Internal Database URL (if PostgreSQL)
- ✅ Update `ALLOWED_ORIGINS` with frontend URL
- ✅ Monitor logs for errors

---

## 🐛 Troubleshooting

### Service Won't Start:
1. Check logs for errors
2. Verify `PORT` is `$PORT` (not hardcoded)
3. Check Python version compatibility
4. Verify all dependencies in `requirements.txt`

### Database Connection Error:
1. If PostgreSQL: Verify Internal Database URL
2. If SQLite: Check disk mount path
3. Check database service is running

### CORS Errors:
1. Update `ALLOWED_ORIGINS` with frontend URL
2. Ensure no trailing slashes
3. Check frontend is using correct backend URL

### Model Not Found:
1. Verify model files in `backend/models/risk_classifier/`
2. Check file paths in code
3. Verify disk space (if using Render Disk)

---

## 🎉 After Deployment

1. ✅ Note your backend URL: `https://your-backend-name.onrender.com`
2. ✅ Test all endpoints
3. ✅ Update frontend `NEXT_PUBLIC_API_URL` with backend URL
4. ✅ Deploy frontend on Vercel
5. ✅ Test full application!

---

## 📚 Quick Reference

**Backend URL Format:**
```
https://<service-name>.onrender.com
```

**Important Endpoints:**
- Health: `/health`
- API Docs: `/docs`
- Root: `/`

**Support:**
- Render Docs: [render.com/docs](https://render.com/docs)
- Render Status: [status.render.com](https://status.render.com)

---

## 🚀 You're Ready!

Follow these steps and your backend will be live on Render! 

**Questions? Check the logs or Render documentation!** 🎯

