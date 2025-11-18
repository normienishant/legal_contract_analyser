# 🚀 Step-by-Step Hosting Guide

## Frontend: Vercel (Free) - Start Here!

### Step 1: Prepare Frontend

1. **Check `next.config.js`:**
   - Make sure it's configured correctly
   - Check `NEXT_PUBLIC_API_URL` environment variable

2. **GitHub pe code push:**
   ```powershell
   git add .
   git commit -m "Ready for hosting - User isolation complete"
   git push origin main
   ```

---

### Step 2: Deploy Frontend on Vercel

1. **Go to Vercel:**
   - Visit: https://vercel.com
   - Click "Sign Up" → Login with GitHub

2. **Create New Project:**
   - Click "Add New" → "Project"
   - Select your GitHub repository
   - Click "Import"

3. **Configure Project:**
   ```
   Framework Preset: Next.js (auto-detected)
   Root Directory: frontend
   Build Command: npm run build (auto)
   Output Directory: .next (auto)
   Install Command: npm install (auto)
   ```

4. **Environment Variables:**
   - Click "Environment Variables"
   - Add:
     ```
     NEXT_PUBLIC_API_URL = https://your-backend.onrender.com
     ```
   - (Backend URL add karenge after backend deploy)

5. **Deploy:**
   - Click "Deploy"
   - Wait 2-3 minutes
   - Frontend URL mil jayega: `https://your-app.vercel.app`

---

## Backend: Render (Free) - After Frontend

### Step 1: Prepare Backend

1. **Check `requirements.txt`:**
   - All dependencies listed

2. **Check `.env` file:**
   - Don't commit `.env` to GitHub
   - Use Render's environment variables instead

---

### Step 2: Deploy Backend on Render

1. **Go to Render:**
   - Visit: https://render.com
   - Click "Get Started" → Login with GitHub

2. **Create PostgreSQL Database:**
   - Click "New" → "PostgreSQL"
   - Name: `contract-analyzer-db`
   - Plan: Free
   - Region: Singapore (or nearest to India)
   - Click "Create Database"
   - **Copy Internal Database URL** (you'll need it)

3. **Create Web Service (Backend):**
   - Click "New" → "Web Service"
   - Connect your GitHub repository
   - Settings:
     ```
     Name: contract-analyzer-backend
     Region: Singapore
     Branch: main
     Root Directory: backend
     Runtime: Python 3
     Build Command: pip install -r requirements.txt
     Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
     Plan: Free
     ```

4. **Environment Variables:**
   - Click "Environment" tab
   - Add these variables:
     ```
     DATABASE_URL = <paste-internal-database-url-from-step-2>
     ML_MODE = ml
     MODEL_PATH = ./models/risk_classifier
     USE_GPU = false
     SECRET_KEY = <generate-random-64-chars>
     ALLOWED_ORIGINS = https://your-app.vercel.app
     UPLOADS_DIR = ./uploads
     MAX_FILE_SIZE = 10485760
     LOG_LEVEL = INFO
     ```

5. **Deploy:**
   - Click "Create Web Service"
   - Wait 5-10 minutes for first deploy
   - Backend URL mil jayega: `https://contract-analyzer-backend.onrender.com`

---

### Step 3: Update Frontend Environment Variable

1. **Go back to Vercel:**
   - Open your project
   - Go to "Settings" → "Environment Variables"
   - Update:
     ```
     NEXT_PUBLIC_API_URL = https://contract-analyzer-backend.onrender.com
     ```
   - Click "Save"
   - Go to "Deployments" → Click "Redeploy" (latest)

---

## Step 4: Upload ML Model to Render

**Important:** ML model files need to be uploaded to Render.

### Option 1: Git LFS (Recommended)
```powershell
# Install Git LFS
git lfs install

# Track model files
git lfs track "backend/models/**/*.bin"
git lfs track "backend/models/**/*.safetensors"

# Add and commit
git add .gitattributes
git add backend/models/
git commit -m "Add ML model files"
git push origin main
```

### Option 2: Manual Upload (After Deploy)
1. Go to Render dashboard
2. Open your backend service
3. Go to "Shell" tab
4. Run:
   ```bash
   mkdir -p models/risk_classifier
   # Then upload files via Render's file manager or use curl
   ```

### Option 3: Download on First Request (Quick Fix)
- Model will download automatically on first request (if using HuggingFace)
- But better to upload directly

---

## Step 5: Test Everything

1. **Frontend:**
   - Visit: `https://your-app.vercel.app`
   - Should load without errors

2. **Backend Health:**
   - Visit: `https://contract-analyzer-backend.onrender.com/health`
   - Should return: `{"status": "healthy", "ml_mode": "ml"}`

3. **Test Upload:**
   - Upload a test contract
   - Check if analysis works

---

## Important Notes

### Render Free Tier Limitations:
- ⚠️ Service sleeps after 15 minutes of inactivity
- ⚠️ First request after sleep takes ~30 seconds (cold start)
- ✅ Solution: Use UptimeRobot (free) to ping every 10 minutes

### UptimeRobot Setup (Keep Backend Awake):
1. Go to: https://uptimerobot.com
2. Sign up (free)
3. Click "Add New Monitor"
4. Settings:
   ```
   Monitor Type: HTTP(s)
   Friendly Name: Contract Analyzer Backend
   URL: https://contract-analyzer-backend.onrender.com/health
   Monitoring Interval: 5 minutes
   ```
5. Click "Create Monitor"
6. Backend will stay awake! ✅

---

## Quick Commands

### Generate SECRET_KEY:
```powershell
-join ((48..57) + (65..90) + (97..122) | Get-Random -Count 64 | ForEach-Object {[char]$_})
```

### Check Deployment Status:
- Vercel: Dashboard → Deployments
- Render: Dashboard → Your Service → Logs

---

## Troubleshooting

### Frontend can't connect to backend:
- Check `NEXT_PUBLIC_API_URL` in Vercel
- Check backend is running (Render dashboard)
- Check CORS settings (`ALLOWED_ORIGINS`)

### Backend not starting:
- Check Render logs
- Check environment variables
- Check `requirements.txt` is correct

### Model not loading:
- Check model files are uploaded
- Check `MODEL_PATH` environment variable
- Check Render logs for errors

---

**Ready to start? Let's begin with frontend on Vercel!** 🚀

