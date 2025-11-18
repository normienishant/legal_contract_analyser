# 🚀 Frontend Hosting on Vercel - Step by Step

## ✅ Prerequisites

- ✅ Code GitHub pe push ho gaya
- ✅ Repository: `legal_contract_analyser`
- ✅ Frontend folder ready

---

## 📋 Step-by-Step Guide

### Step 1: Vercel Account Banao

1. **Go to Vercel:**
   - Visit: https://vercel.com
   - Click "Sign Up"

2. **Login with GitHub:**
   - Click "Continue with GitHub"
   - Authorize Vercel
   - Account ready! ✅

---

### Step 2: Create New Project

1. **Dashboard pe:**
   - Click "Add New" → "Project"

2. **Repository Select:**
   - GitHub repositories list se `legal_contract_analyser` select karo
   - Click "Import"

---

### Step 3: Configure Project Settings

**IMPORTANT Settings:**

```
Framework Preset: Next.js (auto-detect hoga)
Root Directory: frontend  ⚠️ MUST SET THIS!
Build Command: npm run build (auto)
Output Directory: .next (auto)
Install Command: npm install (auto)
```

**Root Directory set karna zaroori hai:**
- "Root Directory" field me `frontend` type karo
- Ya "Edit" button click karo
- Root Directory: `frontend` select karo

---

### Step 4: Environment Variables

1. **Environment Variables section:**
   - Click "Environment Variables"

2. **Add Variable:**
   ```
   Name: NEXT_PUBLIC_API_URL
   Value: http://localhost:8000
   ```
   - (Backend deploy ke baad update karenge)

3. **Click "Add"**

---

### Step 5: Deploy!

1. **Click "Deploy" button**
2. **Wait 2-3 minutes**
3. **Deployment complete!** ✅

---

### Step 6: Get Your URL

After deployment:
- **Frontend URL:** `https://your-app-name.vercel.app`
- Copy this URL (backend deploy ke baad use karenge)

---

## ✅ After Deployment

### Test Frontend:
1. Frontend URL open karo
2. Homepage load hona chahiye
3. Navigation check karo
4. (Backend connect nahi hoga abhi - expected)

---

## 🔧 Troubleshooting

### Build Fails:
- Check Root Directory: `frontend` set hai?
- Check `package.json` exists in frontend folder
- Check build logs in Vercel dashboard

### Environment Variable Not Working:
- Variable name: `NEXT_PUBLIC_API_URL` (exact)
- Redeploy after adding variable

---

## 📝 Next Steps (After Frontend Deploy)

1. ✅ Frontend deployed
2. ⏳ Backend deploy karenge (Render pe)
3. ⏳ Frontend environment variable update karenge
4. ⏳ Test complete setup

---

**Ready? Vercel pe jao aur deploy start karo!** 🚀

