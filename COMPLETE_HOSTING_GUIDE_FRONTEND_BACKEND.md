# 🚀 Complete Hosting Guide - Frontend + Backend

## 📋 Overview

Yeh guide me aapko **ek-ek step** me bataya jayega:
1. **Backend hosting** on Render
2. **Frontend hosting** on Vercel
3. **Connection** between them
4. **Testing** everything

---

## 🎯 PART 1: BACKEND HOSTING (Render)

### Step 1: Render Account Setup

1. **Website:** https://dashboard.render.com
2. **Sign up:** GitHub se (recommended) ya email se
3. **Verify email** (if required)

---

### Step 2: PostgreSQL Database Create

1. **Render Dashboard:**
   - Click **"New +"** → **"PostgreSQL"**

2. **Form Fill:**
   - **Name:** `contract-analyzer-db`
   - **Region:** `Oregon (US West)` (ya closest)
   - **PostgreSQL Version:** `18`
   - **Plan:** **Free**

3. **Click:** "Create Database"
4. **Wait:** 2-3 minutes

---

### Step 3: Database URL Copy

1. **Database service me jao**
2. **"Connect" button click karo** (top right)
3. **"Internal Database URL" copy karo**
   - Format: `postgresql://user:password@host:port/database`
   - **⚠️ IMPORTANT:** Internal URL use karo (External nahi)
4. **Save karo** - backend me use hoga

---

### Step 4: Backend Service Deploy

1. **Render Dashboard:**
   - Click **"New +"** → **"Web Service"**

2. **GitHub Connect:**
   - **"Connect GitHub"** click karo
   - Authorize Render
   - Repository: `normienishant/legal_contract_analyser`
   - Click **"Connect"**

3. **Service Configure:**
   - **Name:** `contract-analyzer-backend`
   - **Region:** Same as database
   - **Branch:** `master` ⚠️
   - **Root Directory:** `backend` ⚠️ **CRITICAL!**
   - **Runtime:** `Python 3` (NOT Docker)
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

4. **Click:** "Create Web Service"

---

### Step 5: Environment Variables Add (Backend)

1. **Service me jao** → **"Environment" tab**

2. **Add Variables:**

   **a) DATABASE_URL:**
   ```
   Key: DATABASE_URL
   Value: <paste-internal-database-url-from-step-3>
   ```

   **b) ML_MODE:**
   ```
   Key: ML_MODE
   Value: ml
   ```

   **c) SECRET_KEY:**
   ```
   Key: SECRET_KEY
   Value: <generate-random-32-chars>
   ```
   **Generate:**
   ```powershell
   -join ((48..57) + (65..90) + (97..122) | Get-Random -Count 32 | ForEach-Object {[char]$_})
   ```

   **d) ALLOWED_ORIGINS:**
   ```
   Key: ALLOWED_ORIGINS
   Value: https://your-frontend.vercel.app,http://localhost:3000
   ```
   **Note:** Frontend deploy hone ke baad update karna hoga

   **e) ENVIRONMENT:**
   ```
   Key: ENVIRONMENT
   Value: production
   ```

   **f) LOG_LEVEL:**
   ```
   Key: LOG_LEVEL
   Value: INFO
   ```

3. **Save** each variable

---

### Step 6: Backend Deploy Wait

1. **"Deployments" tab** check karo
2. **Logs dekho:**
   - Build process
   - Dependencies install
   - App start
3. **Wait:** 5-10 minutes
4. **Success:** Status "Live" ya "Running"

---

### Step 7: Backend URL Get

1. **Service** → **"Settings" tab**
2. **"Domains" section:**
   - **"Generate Domain"** click karo (if not auto-generated)
   - URL copy karo
3. **Backend URL:**
   - Format: `https://contract-analyzer-backend.onrender.com`
   - Ya: `https://<random-name>.onrender.com`
   - **Save karo** - frontend me use hoga

---

### Step 8: Backend Test

1. **Health Check:**
   - Visit: `https://your-backend.onrender.com/health`
   - Should return: `{"status": "healthy", "ml_mode": "ml"}`

2. **API Docs:**
   - Visit: `https://your-backend.onrender.com/docs`
   - Swagger UI dikhna chahiye

✅ **Backend Deployed!**

---

## 🎯 PART 2: FRONTEND HOSTING (Vercel)

### Step 1: Vercel Account Setup

1. **Website:** https://vercel.com
2. **Sign up:** GitHub se (recommended)
3. **Authorize Vercel** to access GitHub

---

### Step 2: New Project Create

1. **Vercel Dashboard:**
   - Click **"Add New..."** → **"Project"**

2. **Repository Select:**
   - **Import Git Repository**
   - Select: `normienishant/legal_contract_analyser`
   - Click **"Import"**

---

### Step 3: Project Configure

1. **Framework Preset:**
   - Auto-detect: **Next.js** ✅
   - (Agar nahi detect hua, manually select "Next.js")

2. **Root Directory:**
   - Click **"Edit"** next to Root Directory
   - Set to: `frontend` ⚠️ **IMPORTANT!**

3. **Build Settings:**
   - **Build Command:** `npm run build` (auto)
   - **Output Directory:** `.next` (auto)
   - **Install Command:** `npm install` (auto)

---

### Step 4: Environment Variables Add (Frontend)

1. **"Environment Variables" section:**
   - Click **"Add"** or expand section

2. **Add Variable:**

   **NEXT_PUBLIC_API_URL:**
   ```
   Key: NEXT_PUBLIC_API_URL
   Value: https://your-backend.onrender.com
   ```
   **⚠️ IMPORTANT:**
   - Backend URL from Step 7 (PART 1) use karo
   - `http://` ya `https://` include karo
   - Trailing slash (`/`) mat lagao

   **Example:**
   ```
   NEXT_PUBLIC_API_URL = https://contract-analyzer-backend.onrender.com
   ```

3. **Environment:**
   - Select: **Production, Preview, Development** (all three)
   - Ya at least **Production**

4. **Click:** "Add" or "Save"

---

### Step 5: Deploy

1. **Click:** "Deploy" button
2. **Wait:** 2-5 minutes
3. **Watch build logs:**
   - Installing dependencies
   - Building Next.js app
   - Deploying

---

### Step 6: Frontend URL Get

1. **Deployment complete hone ke baad:**
   - Vercel automatically URL generate karta hai
2. **Frontend URL:**
   - Format: `https://legal-contract-analyser.vercel.app`
   - Ya: `https://<random-name>.vercel.app`
   - **Save karo**

---

### Step 7: Update Backend CORS

1. **Render Dashboard** me jao
2. **Backend service** → **"Environment" tab**
3. **ALLOWED_ORIGINS update karo:**
   ```
   Key: ALLOWED_ORIGINS
   Value: https://your-frontend.vercel.app,http://localhost:3000
   ```
   - Frontend URL add karo (Step 6 se)
   - `localhost:3000` bhi rakho (local testing ke liye)
4. **Save** karo
5. **Service auto-redeploy** hoga

---

### Step 8: Frontend Test

1. **Visit frontend URL:**
   - `https://your-frontend.vercel.app`

2. **Check:**
   - ✅ Page loads
   - ✅ No errors in console
   - ✅ Can upload file
   - ✅ Can connect to backend

---

## ✅ PART 3: CONNECTION & TESTING

### Step 1: Full Flow Test

1. **Frontend me jao:**
   - Upload a test document
   - Check if it connects to backend
   - Check if analysis works

2. **Backend logs check:**
   - Render → Backend service → "Logs" tab
   - Check for requests
   - Check for errors

---

### Step 2: Troubleshooting

**Issue: Frontend can't connect to backend**
- ✅ Check `NEXT_PUBLIC_API_URL` is correct
- ✅ Check backend URL is accessible
- ✅ Check `ALLOWED_ORIGINS` includes frontend URL
- ✅ Check CORS settings

**Issue: CORS errors**
- ✅ Update `ALLOWED_ORIGINS` in backend
- ✅ Ensure no trailing slashes
- ✅ Check frontend URL is correct

**Issue: 404 errors**
- ✅ Check backend is running
- ✅ Check backend URL is correct
- ✅ Check routes are correct

---

## 📝 Complete Checklist

### Backend (Render):
- [ ] Render account created
- [ ] PostgreSQL database created
- [ ] Internal Database URL copied
- [ ] Backend service created
- [ ] Root Directory: `backend`
- [ ] Branch: `master`
- [ ] All environment variables added
- [ ] Backend deployed successfully
- [ ] Backend URL noted
- [ ] Health check passed

### Frontend (Vercel):
- [ ] Vercel account created
- [ ] Project created from GitHub
- [ ] Root Directory: `frontend`
- [ ] Framework: Next.js
- [ ] `NEXT_PUBLIC_API_URL` environment variable added
- [ ] Frontend deployed successfully
- [ ] Frontend URL noted

### Connection:
- [ ] Backend `ALLOWED_ORIGINS` updated with frontend URL
- [ ] Frontend can connect to backend
- [ ] Full flow tested
- [ ] Everything working!

---

## 🎯 URLs Summary

After deployment, you'll have:

**Backend:**
- URL: `https://contract-analyzer-backend.onrender.com`
- Health: `https://contract-analyzer-backend.onrender.com/health`
- Docs: `https://contract-analyzer-backend.onrender.com/docs`

**Frontend:**
- URL: `https://legal-contract-analyser.vercel.app`
- (Ya Vercel ka auto-generated URL)

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

## 🎉 Done!

Ab aapka complete application live hai:
- ✅ Backend on Render
- ✅ Frontend on Vercel
- ✅ Connected and working!

**Koi question ho toh pucho!** 🚀



