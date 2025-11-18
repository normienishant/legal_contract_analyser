# 🚀 COMPLETE HOSTING GUIDE - EK BAAR ME

## ✅ PRE-CHECKS (Sab ready hai?)

1. ✅ GitHub repo connected
2. ✅ Backend code pushed
3. ✅ Frontend code pushed
4. ✅ All fixes done

---

## 📋 STEP 1: BACKEND HOSTING (RENDER)

### A. PostgreSQL Database Create Karo

1. **Render Dashboard** → https://dashboard.render.com
2. **"New +"** → **"PostgreSQL"**
3. Settings:
   - **Name:** `contract-analyzer-db`
   - **Database:** `contract_analyzer_db`
   - **User:** `contract_analyzer_db_user`
   - **Region:** `Oregon` (or closest)
   - **Plan:** `Free`
4. **"Create Database"**
5. Wait 2-3 minutes
6. **Database ready hone ke baad:**
   - Click on database name
   - Go to **"Connect"** tab
   - Copy **"Internal Database URL"** (yeh chahiye)
   - Example: `postgresql://user:pass@host:5432/dbname`

---

### B. Backend Service Create Karo

1. **Render Dashboard** → **"New +"** → **"Web Service"**
2. **Connect GitHub:**
   - Select your repository
   - Click **"Connect"**
3. **Settings Fill Karo:**

   ```
   Name: contract-analyzer-backend
   Region: Oregon (or closest)
   Branch: master (or main)
   Root Directory: backend
   Runtime: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT
   Instance Type: Free
   ```

4. **Environment Variables Add Karo:**

   Click **"Add Environment Variable"** and add these one by one:

   ```
   KEY: DATABASE_URL
   VALUE: <paste-internal-database-url-from-step-A>
   ```

   ```
   KEY: ML_MODE
   VALUE: ml
   ```

   ```
   KEY: SECRET_KEY
   VALUE: <generate-random-32-chars>
   ```
   
   **SECRET_KEY Generate Karo:**
   - PowerShell me run karo:
   ```powershell
   -join ((48..57) + (65..90) + (97..122) | Get-Random -Count 32 | ForEach-Object {[char]$_})
   ```
   - Copy output and paste as VALUE

   ```
   KEY: ALLOWED_ORIGINS
   VALUE: http://localhost:3000
   ```
   (Pehle localhost rakho, frontend deploy ke baad update karenge)

   ```
   KEY: ENVIRONMENT
   VALUE: production
   ```

   ```
   KEY: LOG_LEVEL
   VALUE: INFO
   ```

5. **"Create Web Service"** click karo
6. **Wait 5-10 minutes** (build ho raha hai)
7. **Check Logs:**
   - "Logs" tab me dekho
   - Agar error aaye, batana
8. **Backend URL Copy Karo:**
   - Service ready hone ke baad
   - URL mil jayega: `https://contract-analyzer-backend.onrender.com`
   - **Yeh URL copy karo** (frontend me chahiye)

---

## 📋 STEP 2: FRONTEND HOSTING (VERCEL)

### A. Vercel Account Setup

1. **Vercel** → https://vercel.com
2. **"Sign Up"** → GitHub se login karo
3. **"Add New Project"** click karo

---

### B. Frontend Deploy Karo

1. **Import Project:**
   - GitHub repo select karo
   - Click **"Import"**

2. **Project Settings:**

   ```
   Framework Preset: Next.js
   Root Directory: frontend
   Build Command: npm run build (auto-detect hoga)
   Output Directory: .next (auto-detect hoga)
   Install Command: npm install (auto-detect hoga)
   ```

3. **Environment Variables:**

   Click **"Environment Variables"** → Add:

   ```
   KEY: NEXT_PUBLIC_API_URL
   VALUE: <paste-backend-url-from-step-1>
   ```
   
   Example: `https://contract-analyzer-backend.onrender.com`

4. **"Deploy"** click karo
5. **Wait 2-3 minutes**
6. **Frontend URL Copy Karo:**
   - Deploy complete hone ke baad
   - URL mil jayega: `https://contract-analyzer-frontend.vercel.app`
   - **Yeh URL copy karo**

---

## 📋 STEP 3: FINAL CONFIGURATION

### A. Backend me Frontend URL Add Karo

1. **Render Dashboard** → Backend service → **"Environment"** tab
2. **ALLOWED_ORIGINS** variable edit karo:
   - Click on **ALLOWED_ORIGINS**
   - **Value update karo:**
   ```
   https://contract-analyzer-frontend.vercel.app,http://localhost:3000
   ```
   (Comma se separate, no spaces)
3. **"Save Changes"**
4. **Manual Redeploy:**
   - **"Manual Deploy"** → **"Deploy latest commit"**

---

## ✅ TESTING

### Backend Test:
1. Browser me open karo: `https://your-backend-url.onrender.com/health`
2. Response: `{"status":"healthy","ml_mode":"ml"}` aana chahiye

### Frontend Test:
1. Browser me open karo: `https://your-frontend-url.vercel.app`
2. App load honi chahiye
3. Upload test karo

---

## 🐛 COMMON ERRORS & FIXES

### Error 1: Backend 502 Bad Gateway
**Fix:**
- Render logs check karo
- Agar `psycopg2` error → Already fixed (requirements.txt me hai)
- Agar build fail → Logs me exact error dekho

### Error 2: Frontend can't connect to backend
**Fix:**
- `NEXT_PUBLIC_API_URL` correct hai?
- Backend URL me `/api` mat add karo (just base URL)
- Backend health check karo: `/health` endpoint

### Error 3: CORS Error
**Fix:**
- Backend me `ALLOWED_ORIGINS` me frontend URL add karo
- Comma se separate, no spaces
- Redeploy backend

---

## 📝 QUICK CHECKLIST

### Backend (Render):
- [ ] PostgreSQL database created
- [ ] Database URL copied
- [ ] Backend service created
- [ ] Root Directory: `backend`
- [ ] Build Command: `pip install -r requirements.txt`
- [ ] Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- [ ] Environment variables added (6 variables)
- [ ] Backend URL copied

### Frontend (Vercel):
- [ ] Project imported from GitHub
- [ ] Root Directory: `frontend`
- [ ] Environment variable: `NEXT_PUBLIC_API_URL` added
- [ ] Frontend URL copied

### Final:
- [ ] Backend me `ALLOWED_ORIGINS` updated with frontend URL
- [ ] Backend redeployed
- [ ] Both URLs tested

---

## 🎉 DONE!

Agar koi error aaye, logs share karo - fix kar dunga!

