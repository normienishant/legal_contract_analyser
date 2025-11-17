# 🚀 Backend Deployment - Quick Start

## ✅ Backend Ready!

All changes made:
- ✅ CORS configured for production
- ✅ Environment variables support
- ✅ Database URL from environment
- ✅ PORT from Render
- ✅ Health endpoint ready

---

## 📋 Quick Deployment Steps

### 1. Push to GitHub
```powershell
git add .
git commit -m "Backend ready for Render deployment"
git push origin main
```

### 2. Go to Render
👉 **[https://dashboard.render.com](https://dashboard.render.com)**

### 3. Create Database
- Click **"New +"** → **"PostgreSQL"**
- Name: `contract-analyzer-db`
- Plan: **Free**
- Region: Choose closest
- **Copy Internal Database URL**

### 4. Deploy Backend
- Click **"New +"** → **"Web Service"**
- Connect GitHub repo
- **Root Directory:** `backend` ⚠️ **IMPORTANT!**
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### 5. Add Environment Variables
```
DATABASE_URL = <paste-internal-db-url>
ML_MODE = ml
SECRET_KEY = <generate-random-32-chars>
ALLOWED_ORIGINS = https://your-frontend.vercel.app,http://localhost:3000
ENVIRONMENT = production
LOG_LEVEL = INFO
```

**Generate SECRET_KEY:**
```powershell
-join ((48..57) + (65..90) + (97..122) | Get-Random -Count 32 | ForEach-Object {[char]$_})
```

### 6. Deploy!
- Click **"Create Web Service"**
- Wait 5-10 minutes
- Check logs for success

### 7. Test
- Visit: `https://your-backend.onrender.com/health`
- Should return: `{"status": "healthy"}`

---

## 📚 Full Guide
See `RENDER_BACKEND_DEPLOY.md` for detailed instructions.

---

## 🎯 After Deployment
1. Note your backend URL
2. Update frontend `NEXT_PUBLIC_API_URL`
3. Deploy frontend on Vercel

**Ready to deploy!** 🚀

