# 🚀 FRONTEND DEPLOYMENT - VERCEL

## ✅ Backend Done!
Your backend is live at: `https://contract-analyzer-backend-171j.onrender.com`

---

## 📋 STEP 1: VERCEL ACCOUNT SETUP

1. Go to **https://vercel.com**
2. Click **"Sign Up"** → Login with **GitHub**
3. Authorize Vercel to access your GitHub

---

## 📋 STEP 2: DEPLOY FRONTEND

### A. Import Project

1. Click **"Add New Project"** (or **"Import Project"**)
2. Select your GitHub repository: `normienishant/legal_contract_analyser`
3. Click **"Import"**

### B. Configure Project

**Project Settings:**

```
Framework Preset: Next.js (auto-detected)
Root Directory: frontend
Build Command: npm run build (auto-detected)
Output Directory: .next (auto-detected)
Install Command: npm install (auto-detected)
```

**IMPORTANT:** 
- Click **"Edit"** next to **"Root Directory"**
- Type: `frontend`
- Click **"Continue"**

### C. Environment Variables

1. Click **"Environment Variables"** section
2. Click **"Add"** button
3. Add this variable:

```
Name: NEXT_PUBLIC_API_URL
Value: https://contract-analyzer-backend-171j.onrender.com
```

**Note:** Replace with your actual backend URL if different!

4. Click **"Add"** to save

### D. Deploy

1. Click **"Deploy"** button
2. Wait 2-3 minutes
3. Frontend will be deployed!

---

## 📋 STEP 3: UPDATE BACKEND CORS

After frontend is deployed, you'll get a URL like:
`https://contract-analyzer-frontend.vercel.app`

### Update Backend ALLOWED_ORIGINS:

1. Go to **Render Dashboard** → Backend Service
2. Click **"Environment"** tab
3. Find **"ALLOWED_ORIGINS"** variable
4. Click **"Edit"**
5. Update value to:
   ```
   https://your-frontend-url.vercel.app,http://localhost:3000
   ```
   (Replace `your-frontend-url` with actual Vercel URL)
6. Click **"Save Changes"**
7. **Manual Redeploy** backend

---

## ✅ TESTING

### Backend Test:
- Open: `https://contract-analyzer-backend-171j.onrender.com/health`
- Should show: `{"status":"healthy","ml_mode":"ml"}`

### Frontend Test:
- Open your Vercel URL
- App should load
- Try uploading a document

---

## 🎉 DONE!

Once frontend is deployed:
1. ✅ Backend on Render
2. ✅ Frontend on Vercel
3. ✅ Connected and working!

---

**Ab Vercel me frontend deploy karo!**

