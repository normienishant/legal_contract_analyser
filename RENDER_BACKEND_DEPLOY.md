# 🚀 Backend Hosting on Render - Complete Guide

## ✅ Pre-Deployment Checklist

- [x] Backend code ready
- [x] `requirements.txt` exists
- [x] ML model files in `backend/models/risk_classifier/`
- [x] CORS updated for production
- [x] Environment variables configured
- [ ] GitHub repository pushed
- [ ] Render account created

---

## 📝 Step-by-Step Deployment

### Step 1: Push Code to GitHub

```powershell
# Make sure all changes are committed
git add .
git commit -m "Ready for Render deployment"
git push origin main
```

---

### Step 2: Create Render Account

1. Go to **[https://dashboard.render.com](https://dashboard.render.com)**
2. Click **"Get Started for Free"**
3. Sign up with **GitHub** (recommended) or email
4. Verify email if needed

---

### Step 3: Create PostgreSQL Database

1. In Render Dashboard, click **"New +"** → **"PostgreSQL"**
2. Fill in:
   - **Name:** `contract-analyzer-db`
   - **Database:** `contract_analyzer`
   - **User:** Auto-generated
   - **Region:** `Oregon (US West)` or closest to you
   - **PostgreSQL Version:** `16`
   - **Plan:** **Free**
3. Click **"Create Database"**
4. **Wait 2-3 minutes** for creation
5. **Copy the Internal Database URL** (looks like: `postgresql://user:pass@host:port/db`)

---

### Step 4: Deploy Backend Web Service

1. Click **"New +"** → **"Web Service"**

2. **Connect Repository:**
   - Click **"Connect GitHub"** (if first time)
   - Authorize Render
   - Select repository: `ai doc anal` (or your repo name)
   - Click **"Connect"**

3. **Configure Service:**
   - **Name:** `contract-analyzer-backend`
   - **Region:** Same as database
   - **Branch:** `master` (or `main` if you renamed it)
   - **Root Directory:** `backend` ⚠️ **CRITICAL!**
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

4. **Environment Variables:**
   Click **"Advanced"** → Add these:

   | Key | Value | Notes |
   |-----|-------|-------|
   | `DATABASE_URL` | `<paste-internal-db-url>` | From Step 3 |
   | `ML_MODE` | `ml` | Use ML model |
   | `SECRET_KEY` | `<random-32-chars>` | Generate below |
   | `ALLOWED_ORIGINS` | `https://your-frontend.vercel.app,http://localhost:3000` | Update with your frontend URL |
   | `ENVIRONMENT` | `production` | |
   | `LOG_LEVEL` | `INFO` | |
   | `PORT` | `$PORT` | Auto-set by Render |

   **Generate SECRET_KEY:**
   ```powershell
   -join ((48..57) + (65..90) + (97..122) | Get-Random -Count 32 | ForEach-Object {[char]$_})
   ```

5. Click **"Create Web Service"**

6. **Wait 5-10 minutes** for first deployment

---

### Step 5: Monitor Deployment

1. Go to your service → **"Logs"** tab
2. Watch for:
   - ✅ `Application startup complete`
   - ✅ `Starting application in production mode`
   - ❌ Any errors (red text)

---

### Step 6: Verify Deployment

1. **Health Check:**
   - Visit: `https://your-backend-name.onrender.com/health`
   - Should return: `{"status": "healthy", "ml_mode": "ml"}`

2. **API Docs:**
   - Visit: `https://your-backend-name.onrender.com/docs`
   - Should show Swagger UI

3. **Root Endpoint:**
   - Visit: `https://your-backend-name.onrender.com/`
   - Should return API info

---

## 🔧 Important Notes

### Model Files
- Model files are in `backend/models/risk_classifier/`
- They'll be deployed with code (if repo size < 100MB)
- If model is too large, consider using Render Disk or external storage

### Database
- Use **Internal Database URL** (not External)
- Internal URL works within Render network
- External URL is for outside access (not needed)

### CORS
- Backend now reads `ALLOWED_ORIGINS` from environment
- Add your frontend URL to `ALLOWED_ORIGINS`
- Format: `https://your-app.vercel.app,http://localhost:3000`

### Free Tier Limits
- **Web Service:** Spins down after 15 min inactivity
- **Database:** 90 days free, then $7/month
- **Disk:** 1GB free
- **Build Time:** 10 min max

---

## 🐛 Troubleshooting

### Build Fails
- Check `requirements.txt` - all packages compatible?
- Check Python version (3.9+)
- Check build logs for specific errors

### Service Crashes
- Check logs for errors
- Verify `DATABASE_URL` is correct
- Check if model files are accessible
- Verify `PORT` is used (not hardcoded 8000)

### Database Connection Error
- Verify `DATABASE_URL` is Internal URL
- Check database is running (Render dashboard)
- Ensure database and service are in same region

### CORS Errors
- Verify `ALLOWED_ORIGINS` includes frontend URL
- Check frontend is using correct backend URL
- Ensure no trailing slashes in URLs

### Model Not Found
- Verify model files are in `backend/models/risk_classifier/`
- Check file paths in code
- Check disk space (if using Render Disk)

---

## 📊 After Deployment

1. ✅ Note your backend URL: `https://your-backend-name.onrender.com`
2. ✅ Test all endpoints
3. ✅ Update frontend `NEXT_PUBLIC_API_URL` with backend URL
4. ✅ Proceed to frontend deployment

---

## 🎉 Next Steps

After backend is live:
1. Deploy frontend on Vercel
2. Update frontend environment variables
3. Test full application
4. Share your app! 🚀

---

**Ready? Follow the steps above and your backend will be live!** 

**Questions? Check Render logs or documentation.**

