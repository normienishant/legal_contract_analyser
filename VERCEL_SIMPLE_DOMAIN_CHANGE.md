# 🔗 VERCEL DOMAIN CHANGE - SIMPLE STEPS

## 🎯 Current URL (Bekar)
`https://legal-contract-analyser-qz22.vercel.app`

## ✅ Target URL (Achha)
`https://contract-analyzer.vercel.app`

---

## 📋 STEP-BY-STEP GUIDE

### Step 1: Vercel Dashboard
1. Open **https://vercel.com**
2. Login karo
3. Click on project: **legal-contract-analyser**

### Step 2: Settings
1. Left sidebar me **"Settings"** click karo
2. Top me **"General"** tab (already selected hoga)

### Step 3: Project Name Change
1. Scroll down to **"Project Name"** section
2. **"Edit"** button click karo (right side me)
3. Current name: `legal-contract-analyser`
4. **Delete karo** aur type karo: `contract-analyzer`
   - **NO spaces**
   - **NO special characters**
   - **Only lowercase letters and hyphens**
5. **"Save"** button click karo

### Step 4: Wait
- 10-20 seconds wait karo
- Automatic redeploy ho jayega

### Step 5: New URL
- New URL: `https://contract-analyzer.vercel.app`
- Old URL bhi kaam karega (redirect ho jayega)

---

## 🔄 BACKEND CORS UPDATE (IMPORTANT!)

After domain change, backend me CORS update karo:

### Step 1: Render Dashboard
1. Open **https://dashboard.render.com**
2. Backend service click karo

### Step 2: Environment Variables
1. **"Environment"** tab click karo
2. **"ALLOWED_ORIGINS"** variable find karo
3. **"Edit"** click karo

### Step 3: Update Value
**Current:**
```
https://legal-contract-analyser-qz22.vercel.app,http://localhost:3000
```

**New (Update karo):**
```
https://contract-analyzer.vercel.app,http://localhost:3000
```

4. **"Save Changes"** click karo

### Step 4: Redeploy Backend
1. **"Manual Deploy"** tab
2. **"Deploy latest commit"** click karo
3. Wait 5-10 minutes

---

## ✅ DONE!

Ab:
- ✅ New URL: `https://contract-analyzer.vercel.app`
- ✅ Old URL redirect ho jayega
- ✅ Backend CORS updated
- ✅ Sab kuch kaam karega!

---

## 🎯 OTHER GOOD NAME OPTIONS

Agar `contract-analyzer` available nahi ho, try these:

1. `contract-ai` ⭐ (Short & sweet)
2. `risk-analyzer`
3. `legal-ai`
4. `contract-check`
5. `ai-contract-analyzer`

---

**Ab Vercel me project name change karo!**

