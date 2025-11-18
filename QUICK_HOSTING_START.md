# ⚡ Quick Hosting Start - Frontend First!

## 🎯 Step 1: Frontend on Vercel (5 minutes)

### 1. GitHub pe code push:
```powershell
git add .
git commit -m "Ready for hosting"
git push origin main
```

### 2. Vercel pe deploy:
1. Go to: https://vercel.com
2. Sign up with GitHub
3. Click "Add New" → "Project"
4. Select your repo
5. Settings:
   - **Root Directory:** `frontend`
   - **Framework:** Next.js (auto)
   - **Build Command:** `npm run build` (auto)
6. Environment Variables:
   - `NEXT_PUBLIC_API_URL` = `http://localhost:8000` (temporary, update after backend)
7. Click "Deploy"
8. Wait 2-3 minutes
9. **Frontend URL:** `https://your-app.vercel.app` ✅

---

## 🎯 Step 2: Backend on Render (10 minutes)

### 1. Create Database:
1. Go to: https://render.com
2. Sign up with GitHub
3. Click "New" → "PostgreSQL"
4. Name: `contract-analyzer-db`
5. Plan: **Free**
6. Click "Create"
7. **Copy Internal Database URL** (you'll need it!)

### 2. Create Backend Service:
1. Click "New" → "Web Service"
2. Connect GitHub repo
3. Settings:
   ```
   Name: contract-analyzer-backend
   Root Directory: backend
   Runtime: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
   Plan: Free
   ```

### 3. Environment Variables:
Click "Environment" and add:
```
DATABASE_URL = <paste-database-url>
ML_MODE = ml
MODEL_PATH = ./models/risk_classifier
USE_GPU = false
SECRET_KEY = <generate-random-64-chars>
ALLOWED_ORIGINS = https://your-app.vercel.app
UPLOADS_DIR = ./uploads
MAX_FILE_SIZE = 10485760
LOG_LEVEL = INFO
```

### 4. Deploy:
- Click "Create Web Service"
- Wait 5-10 minutes
- **Backend URL:** `https://contract-analyzer-backend.onrender.com` ✅

---

## 🎯 Step 3: Update Frontend URL

1. Go back to Vercel
2. Settings → Environment Variables
3. Update:
   ```
   NEXT_PUBLIC_API_URL = https://contract-analyzer-backend.onrender.com
   ```
4. Redeploy frontend

---

## 🎯 Step 4: Upload ML Model

**Option 1: Git LFS (Best)**
```powershell
git lfs install
git lfs track "backend/models/**/*"
git add .gitattributes backend/models/
git commit -m "Add ML model"
git push
```

**Option 2: After Deploy (Quick)**
- Render Shell tab se manually upload karo
- Ya first request pe auto-download hoga

---

## ✅ Done!

- Frontend: `https://your-app.vercel.app`
- Backend: `https://contract-analyzer-backend.onrender.com`

**Test karo aur batao!** 🚀

