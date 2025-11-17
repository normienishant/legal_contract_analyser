# 🚀 Backend Hosting on Render - Step by Step Guide

## 📋 Prerequisites

1. ✅ GitHub repository setup (code pushed to GitHub)
2. ✅ Render account (free tier available)
3. ✅ Backend code ready

---

## 🎯 Step 1: Prepare Backend for Deployment

### Check Current Setup:
- ✅ Backend code is ready
- ✅ `requirements.txt` exists
- ✅ Model files are in `backend/models/risk_classifier/`
- ✅ Database migration script ready

---

## 🌐 Step 2: Create Render Account

1. Go to **[Render Dashboard](https://dashboard.render.com)**
2. Sign up with GitHub (recommended) or email
3. Verify your email if needed

---

## 🗄️ Step 3: Create PostgreSQL Database (Free)

1. In Render Dashboard, click **"New +"** → **"PostgreSQL"**
2. Fill in:
   - **Name:** `contract-analyzer-db` (or any name)
   - **Database:** `contract_analyzer`
   - **User:** `contract_user` (auto-generated)
   - **Region:** Choose closest to you (e.g., `Oregon (US West)`)
   - **PostgreSQL Version:** `16` (latest)
   - **Plan:** **Free** (for testing)
3. Click **"Create Database"**
4. **Wait 2-3 minutes** for database to be created
5. **Copy the Internal Database URL** (you'll need it later)
   - Format: `postgresql://user:password@host:port/database`

---

## 🚀 Step 4: Deploy Backend Web Service

1. In Render Dashboard, click **"New +"** → **"Web Service"**

2. **Connect Repository:**
   - Click **"Connect GitHub"** (if not connected)
   - Authorize Render
   - Select your repository: `ai doc anal` (or your repo name)
   - Click **"Connect"**

3. **Configure Service:**
   - **Name:** `contract-analyzer-backend` (or any name)
   - **Region:** Same as database (e.g., `Oregon (US West)`)
   - **Branch:** `main` (or your main branch)
   - **Root Directory:** `backend` ⚠️ **IMPORTANT!**
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

4. **Environment Variables:**
   Click **"Advanced"** → **"Add Environment Variable"** and add:
   
   ```
   DATABASE_URL = <paste-internal-database-url-from-step-3>
   ML_MODE = ml
   SECRET_KEY = <generate-random-string-32-chars>
   ALLOWED_ORIGINS = https://your-frontend-domain.vercel.app,http://localhost:3000
   ENVIRONMENT = production
   LOG_LEVEL = INFO
   ```
   
   **How to generate SECRET_KEY:**
   ```powershell
   # Run in PowerShell
   -join ((48..57) + (65..90) + (97..122) | Get-Random -Count 32 | ForEach-Object {[char]$_})
   ```

5. **Add Disk (for ML Model):**
   - Click **"Advanced"** → **"Add Disk"**
   - **Name:** `model-storage`
   - **Mount Path:** `/opt/render/project/src/models`
   - **Size:** `1 GB` (free tier allows up to 1GB)

6. Click **"Create Web Service"**

7. **Wait 5-10 minutes** for first deployment

---

## 📦 Step 5: Upload ML Model to Render

Since Render's free tier has limited disk space, we have two options:

### Option A: Include Model in Git (if < 100MB)
- Model files are already in `backend/models/risk_classifier/`
- They'll be deployed automatically with code

### Option B: Upload Model After Deployment (Recommended)
1. After deployment, go to your service
2. Click **"Shell"** tab
3. Run:
   ```bash
   mkdir -p models/risk_classifier
   # Then upload model files via Render's file manager or use git
   ```

**For now, we'll use Option A** (model is already in repo)

---

## ✅ Step 6: Verify Deployment

1. **Check Build Logs:**
   - Go to your service → **"Logs"** tab
   - Look for: `Application startup complete`
   - Check for any errors

2. **Test Health Endpoint:**
   - Your backend URL: `https://contract-analyzer-backend.onrender.com`
   - Visit: `https://your-backend-url.onrender.com/health`
   - Should return: `{"status": "healthy"}`

3. **Test API:**
   - Visit: `https://your-backend-url.onrender.com/docs`
   - Should show Swagger UI

---

## 🔧 Step 7: Update CORS Settings

After deployment, update `backend/app/main.py` to include your Render URL:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://your-frontend.vercel.app",  # Add your frontend URL
        "https://*.onrender.com",  # Allow all Render subdomains
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Then commit and push - Render will auto-deploy.

---

## 📝 Step 8: Environment Variables Summary

Make sure these are set in Render:

| Variable | Value | Example |
|----------|-------|---------|
| `DATABASE_URL` | From PostgreSQL service | `postgresql://user:pass@host:port/db` |
| `ML_MODE` | `ml` | `ml` |
| `SECRET_KEY` | Random 32-char string | `aB3dE5fG7hI9jK1lM3nO5pQ7rS9tU1vW3` |
| `ALLOWED_ORIGINS` | Frontend URLs | `https://your-app.vercel.app` |
| `ENVIRONMENT` | `production` | `production` |
| `LOG_LEVEL` | `INFO` | `INFO` |
| `PORT` | Auto-set by Render | `$PORT` |

---

## 🐛 Troubleshooting

### Build Fails:
- Check `requirements.txt` - all packages compatible?
- Check Python version (should be 3.9+)
- Check build logs for specific errors

### Service Crashes:
- Check logs for errors
- Verify `DATABASE_URL` is correct
- Check if model files are accessible
- Verify `PORT` environment variable is used

### Database Connection Error:
- Verify `DATABASE_URL` is correct
- Check if database is running (Render dashboard)
- Use **Internal Database URL** (not External)

### Model Not Found:
- Verify model files are in `backend/models/risk_classifier/`
- Check disk mount path
- Check file permissions

---

## 🎉 Next Steps

After backend is deployed:
1. ✅ Note your backend URL (e.g., `https://contract-analyzer-backend.onrender.com`)
2. ✅ Test all endpoints
3. ✅ Proceed to frontend deployment on Vercel
4. ✅ Update frontend `NEXT_PUBLIC_API_URL` with backend URL

---

## 📞 Support

If you face issues:
1. Check Render logs
2. Check Render status page
3. Verify all environment variables
4. Test locally first

**Ready to deploy? Follow the steps above!** 🚀

