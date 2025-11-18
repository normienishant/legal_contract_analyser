# 🚀 Railway Backend - Quick Start

## ✅ Why Railway?

- ✅ GitHub se code automatically
- ✅ $5 free credit/month
- ✅ Super easy - 5 minutes!
- ✅ Auto-deploy on push

---

## 🎯 Quick Steps

### 1. Sign Up
- Go to [railway.app](https://railway.app)
- Click "Login with GitHub"
- Authorize Railway

### 2. Deploy
- Click "New Project"
- Select "Deploy from GitHub repo"
- Select: `normienishant/legal_contract_analyser`
- **Root Directory:** `backend` ⚠️
- Click "Deploy Now"

### 3. Configure
- Go to service → "Variables" tab
- Add:
  ```
  ML_MODE=ml
  SECRET_KEY=<generate-32-chars>
  ALLOWED_ORIGINS=https://your-frontend.vercel.app,http://localhost:3000
  ENVIRONMENT=production
  LOG_LEVEL=INFO
  ```

### 4. Settings
- Service → "Settings" tab
- **Root Directory:** `backend`
- **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### 5. Get URL
- Service → "Settings" → "Domains"
- Click "Generate Domain"
- Your URL: `https://your-service.up.railway.app`

### 6. Test
- Visit: `https://your-service.up.railway.app/health`
- Should return: `{"status": "healthy"}`

---

## 📝 Generate SECRET_KEY

```powershell
-join ((48..57) + (65..90) + (97..122) | Get-Random -Count 32 | ForEach-Object {[char]$_})
```

---

## 🎉 Done!

Backend is live! Update frontend with Railway URL.

**Full guide:** See `RAILWAY_BACKEND_DEPLOY.md`

