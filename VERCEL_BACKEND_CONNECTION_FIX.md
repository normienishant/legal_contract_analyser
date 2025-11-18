# 🔧 Vercel Frontend - Render Backend Connection Fix

## ❌ Error: "Failed to fetch"

**Problem:** Frontend (Vercel) cannot connect to Backend (Render)

---

## ✅ Quick Fix Steps

### Step 1: Check Render Backend Status

1. Go to **Render Dashboard** → Your Backend Service
2. Check **Logs** tab
3. Look for:
   - ✅ "Application is live" message
   - ✅ No errors in recent logs
   - ✅ Service shows "Live" status

**If backend is still deploying:**
- Wait 2-5 minutes
- Check logs for completion

---

### Step 2: Get Render Backend URL

1. Render Dashboard → Your Backend Service
2. Copy the **Service URL** (e.g., `https://your-backend.onrender.com`)
3. **Important:** NO trailing slash!

---

### Step 3: Set Vercel Environment Variable

1. Go to **Vercel Dashboard** → Your Project
2. Click **Settings** → **Environment Variables**
3. Add/Update:
   - **Key:** `NEXT_PUBLIC_API_URL`
   - **Value:** `https://your-backend.onrender.com` (your Render URL)
   - **Environment:** Production, Preview, Development (select all)
4. Click **Save**

---

### Step 4: Redeploy Vercel

**Option A: Automatic (after env var change)**
- Vercel will auto-redeploy when you save env vars

**Option B: Manual**
1. Vercel Dashboard → Your Project
2. Click **Deployments** tab
3. Click **⋯** (three dots) on latest deployment
4. Click **Redeploy**

---

### Step 5: Verify CORS on Render

1. Render Dashboard → Your Backend Service → **Environment** tab
2. Check `ALLOWED_ORIGINS`:
   ```
   https://legal-contract-risk-analyser.vercel.app,http://localhost:3000
   ```
3. **Important:**
   - ✅ NO trailing slash after `.app`
   - ✅ Comma-separated (no spaces)
   - ✅ Includes your Vercel URL

---

## 🔍 Debug Checklist

- [ ] Render backend is **Live** (not deploying)
- [ ] Render backend URL is accessible (open in browser → should show JSON)
- [ ] Vercel has `NEXT_PUBLIC_API_URL` set correctly
- [ ] Vercel deployment completed successfully
- [ ] `ALLOWED_ORIGINS` on Render includes Vercel URL
- [ ] No trailing slashes in URLs

---

## 🧪 Test Backend Connection

**Test Render Backend:**
```bash
# Open in browser or use curl
https://your-backend.onrender.com/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "ml_mode": "ml"
}
```

**If this fails:**
- Backend is not running
- Check Render logs for errors

---

## 🚨 Common Issues

### Issue 1: Backend Still Deploying
**Solution:** Wait 2-5 minutes, check Render logs

### Issue 2: Wrong API URL in Vercel
**Solution:** Update `NEXT_PUBLIC_API_URL` in Vercel env vars

### Issue 3: CORS Error
**Solution:** Update `ALLOWED_ORIGINS` on Render (no trailing slash!)

### Issue 4: Backend Crashed
**Solution:** Check Render logs, fix errors, redeploy

---

## ✅ Success Indicators

After fixing:
- ✅ No "Failed to fetch" error
- ✅ Settings page shows "Backend Connected"
- ✅ Can upload and analyze documents
- ✅ History page loads data

---

## 📝 Quick Reference

**Vercel Env Var:**
```
NEXT_PUBLIC_API_URL=https://your-backend.onrender.com
```

**Render Env Var:**
```
ALLOWED_ORIGINS=https://legal-contract-risk-analyser.vercel.app,http://localhost:3000
```

**Test URLs:**
- Frontend: `https://legal-contract-risk-analyser.vercel.app`
- Backend Health: `https://your-backend.onrender.com/health`

