# 🚀 Complete Hosting Steps - Frontend + Backend

## 📋 Overview

Yeh guide me **ek-ek step** me bataya jayega:
- ✅ Backend hosting on Render
- ✅ Frontend hosting on Vercel
- ✅ Connection setup
- ✅ Testing

---

## 🎯 PART 1: BACKEND HOSTING (Render)

### Step 1: Render Account
1. Go to: https://dashboard.render.com
2. Sign up with GitHub (recommended)
3. Verify email

### Step 2: PostgreSQL Database
1. Click **"New +"** → **"PostgreSQL"**
2. Fill:
   - Name: `contract-analyzer-db`
   - Region: `Oregon (US West)`
   - Version: `18`
   - Plan: **Free**
3. Click **"Create Database"**
4. Wait 2-3 minutes

### Step 3: Get Database URL
1. Database service → **"Connect"** button
2. Copy **"Internal Database URL"**
3. Save it (format: `postgresql://user:pass@host:port/db`)

### Step 4: Deploy Backend
1. Click **"New +"** → **"Web Service"**
2. Connect GitHub: `normienishant/legal_contract_analyser`
3. Configure:
   - Name: `contract-analyzer-backend`
   - Branch: `master`
   - **Root Directory:** `backend` ⚠️
   - Runtime: `Python 3`
   - Build: `pip install -r requirements.txt`
   - Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Click **"Create Web Service"**

### Step 5: Add Environment Variables (Backend)
Service → **"Environment"** tab → Add:

```
DATABASE_URL = <paste-internal-database-url>
ML_MODE = ml
SECRET_KEY = <generate-32-chars>
ALLOWED_ORIGINS = https://your-frontend.vercel.app,http://localhost:3000
ENVIRONMENT = production
LOG_LEVEL = INFO
```

**Generate SECRET_KEY:**
```powershell
-join ((48..57) + (65..90) + (97..122) | Get-Random -Count 32 | ForEach-Object {[char]$_})
```

### Step 6: Wait for Deploy
1. Check **"Deployments"** tab
2. Watch logs
3. Wait 5-10 minutes
4. Status should be "Live"

### Step 7: Get Backend URL
1. Service → **"Settings"** → **"Domains"**
2. Copy URL: `https://your-backend.onrender.com`
3. **Save it** - frontend me use hoga

### Step 8: Test Backend
- Visit: `https://your-backend.onrender.com/health`
- Should return: `{"status": "healthy"}`

✅ **Backend Done!**

---

## 🎯 PART 2: FRONTEND HOSTING (Vercel)

### Step 1: Vercel Account
1. Go to: https://vercel.com
2. Sign up with GitHub
3. Authorize Vercel

### Step 2: Create Project
1. Click **"Add New..."** → **"Project"**
2. Import: `normienishant/legal_contract_analyser`
3. Click **"Import"**

### Step 3: Configure Project
1. **Root Directory:** Set to `frontend` ⚠️ **IMPORTANT!**
   - Click **"Edit"** next to Root Directory
   - Type: `frontend`
2. **Framework:** Next.js (auto-detect)
3. **Build Settings:** Auto (don't change)

### Step 4: Add Environment Variable (Frontend)
1. **"Environment Variables"** section
2. Click **"Add"**
3. Add:
   ```
   Key: NEXT_PUBLIC_API_URL
   Value: https://your-backend.onrender.com
   ```
   **⚠️ IMPORTANT:**
   - Backend URL from Step 7 (PART 1) use karo
   - `https://` include karo
   - Trailing slash (`/`) mat lagao
4. **Environment:** Select **Production, Preview, Development** (all)
5. Click **"Add"**

### Step 5: Deploy
1. Click **"Deploy"**
2. Wait 2-5 minutes
3. Watch build logs

### Step 6: Get Frontend URL
1. Deployment complete
2. Vercel auto-generates URL
3. Format: `https://legal-contract-analyser.vercel.app`
4. **Save it**

### Step 7: Update Backend CORS
1. **Render Dashboard** → Backend service
2. **"Environment"** tab
3. Update `ALLOWED_ORIGINS`:
   ```
   ALLOWED_ORIGINS = https://your-frontend.vercel.app,http://localhost:3000
   ```
   - Frontend URL add karo (Step 6 se)
4. **Save** - service auto-redeploys

### Step 8: Test Frontend
1. Visit frontend URL
2. Check page loads
3. Try uploading a file
4. Check if it connects to backend

✅ **Frontend Done!**

---

## ✅ PART 3: TESTING & VERIFICATION

### Test Complete Flow:
1. Frontend me jao
2. Upload a test document
3. Check if analysis works
4. Check backend logs (Render → Logs tab)

### Verify:
- ✅ Frontend loads
- ✅ Can upload files
- ✅ Backend responds
- ✅ Analysis works
- ✅ No CORS errors

---

## 📝 Complete Checklist

### Backend (Render):
- [ ] Render account created
- [ ] PostgreSQL database created
- [ ] Database URL copied
- [ ] Backend service created
- [ ] Root Directory: `backend`
- [ ] Branch: `master`
- [ ] All env variables added
- [ ] Backend deployed
- [ ] Backend URL saved
- [ ] Health check passed

### Frontend (Vercel):
- [ ] Vercel account created
- [ ] Project created
- [ ] Root Directory: `frontend`
- [ ] `NEXT_PUBLIC_API_URL` added
- [ ] Frontend deployed
- [ ] Frontend URL saved

### Connection:
- [ ] Backend `ALLOWED_ORIGINS` updated
- [ ] Frontend connects to backend
- [ ] Full flow tested
- [ ] Everything working!

---

## 🔧 Environment Variables Summary

### Backend (Render):
```
DATABASE_URL = <from-postgresql>
ML_MODE = ml
SECRET_KEY = <generate-32-chars>
ALLOWED_ORIGINS = https://your-frontend.vercel.app,http://localhost:3000
ENVIRONMENT = production
LOG_LEVEL = INFO
```

### Frontend (Vercel):
```
NEXT_PUBLIC_API_URL = https://your-backend.onrender.com
```

---

## 🐛 Troubleshooting

### Frontend can't connect:
- ✅ Check `NEXT_PUBLIC_API_URL` is correct
- ✅ Check backend is running
- ✅ Check `ALLOWED_ORIGINS` includes frontend URL

### CORS errors:
- ✅ Update `ALLOWED_ORIGINS` in backend
- ✅ No trailing slashes
- ✅ Check URLs are correct

### 404 errors:
- ✅ Check backend is running
- ✅ Check backend URL is correct
- ✅ Check routes

---

## 🎉 Done!

Ab aapka complete application live hai:
- ✅ Backend: Render
- ✅ Frontend: Vercel
- ✅ Connected and working!

**Koi question ho toh pucho!** 🚀



