# 🚀 Backend Hosting - Complete Step by Step Guide

## 📋 Overview

Yeh guide me aapko **ek-ek step** me bataya jayega:
1. Kaha `.env` file banani hai
2. `.env` file me kya kya dalna hai
3. Har value kaise milegi
4. Render pe kaise deploy karna hai

---

## 🎯 PART 1: Local .env File Setup

### Step 1: .env File Kaha Banani Hai?

**Location:** `backend/.env`

**Path:** 
```
C:\Users\nisha\OneDrive\Desktop\ai doc anal\backend\.env
```

**How to Create:**
1. `backend` folder me jao
2. New file banayein
3. Name rakhein: `.env` (exactly yeh name, kuch aur nahi)
4. Save karein

---

### Step 2: .env File Me Kya Kya Dalna Hai?

`.env` file me yeh sab dalo:

```env
PORT=8000
ENVIRONMENT=development
DATABASE_URL=sqlite:///./contract_analyzer.db
ML_MODE=ml
SECRET_KEY=change-this-to-random-32-characters
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
LOG_LEVEL=INFO
MAX_UPLOAD_SIZE_MB=10
ALLOWED_EXTENSIONS=pdf,docx,txt
```

---

### Step 3: Har Value Kaise Milegi? (Ek-Ek Karke)

#### 1. PORT
**Kya hai:** Server ka port number
**Value:** `8000`
**Kaise milega:** 
- Bas type karo: `8000`
- Yeh default port hai

---

#### 2. ENVIRONMENT
**Kya hai:** Development ya production
**Value:** `development`
**Kaise milega:**
- Local testing ke liye: `development`
- Production ke liye: `production` (Render me add karenge)

---

#### 3. DATABASE_URL
**Kya hai:** Database connection string
**Value (Local):** `sqlite:///./contract_analyzer.db`
**Kaise milega:**
- **Local ke liye:** Bas yeh value copy-paste karo
- SQLite automatically create ho jayega
- Kuch setup nahi karna

**Value (Production - Render):**
- Render PostgreSQL service se milega (baad me batayenge)

---

#### 4. ML_MODE
**Kya hai:** ML model use karna hai ya nahi
**Value:** `ml`
**Kaise milega:**
- `ml` = ML model use karega
- `rules` = Sirf rule-based (ML nahi)
- Bas type karo: `ml`

---

#### 5. SECRET_KEY
**Kya hai:** Security ke liye secret key
**Value:** Random 32 characters
**Kaise milega:**

**Method 1: PowerShell (Recommended)**
```powershell
-join ((48..57) + (65..90) + (97..122) | Get-Random -Count 32 | ForEach-Object {[char]$_})
```
1. PowerShell open karo
2. Yeh command run karo
3. Output copy karo
4. `.env` file me paste karo

**Method 2: Online**
1. Website: https://randomkeygen.com/
2. "CodeIgniter Encryption Keys" section me jao
3. 32 character wala key copy karo
4. `.env` file me paste karo

**Example Output:**
```
aB3dE5fG7hI9jK1lM3nO5pQ7rS9tU1vW3xY5zA7bC9dE1
```

**Important:**
- ✅ Har baar naya generate karo
- ✅ Production me alag key use karo
- ✅ Kisi ko share mat karo

---

#### 6. ALLOWED_ORIGINS
**Kya hai:** Kaunse frontend URLs backend ko access kar sakte hain
**Value (Local):** `http://localhost:3000,http://127.0.0.1:3000`
**Kaise milega:**
- **Local:** Bas yeh value copy-paste karo
- `localhost:3000` = Local frontend
- `127.0.0.1:3000` = Same thing, different format

**Value (Production):**
- Frontend Vercel pe deploy hone ke baad milega
- Format: `https://your-app.vercel.app,http://localhost:3000`
- Abhi ke liye local value hi rakho

---

#### 7. LOG_LEVEL
**Kya hai:** Kitna logging chahiye
**Value:** `INFO`
**Kaise milega:**
- Bas type karo: `INFO`
- Options: `DEBUG`, `INFO`, `WARNING`, `ERROR`
- Normal use ke liye: `INFO`

---

#### 8. MAX_UPLOAD_SIZE_MB
**Kya hai:** Maximum file size upload kar sakte ho
**Value:** `10`
**Kaise milega:**
- Bas type karo: `10` (10 MB)
- Agar zyada chahiye: `20`, `50`, etc.

---

#### 9. ALLOWED_EXTENSIONS
**Kya hai:** Kaunse file types upload kar sakte ho
**Value:** `pdf,docx,txt`
**Kaise milega:**
- Bas type karo: `pdf,docx,txt`
- Comma-separated, no spaces
- Agar aur chahiye: `pdf,docx,txt,doc`

---

## ✅ PART 1 Complete: .env File Ready!

Ab aapka `.env` file ready hai:
- Location: `backend/.env`
- All values filled
- Local development ke liye ready

---

## 🚀 PART 2: Render Pe Backend Deploy

### Step 1: Render Account Banayein

1. **Website:** https://dashboard.render.com
2. **Click:** "Get Started for Free"
3. **Sign up:**
   - GitHub se (recommended), ya
   - Email se
4. **Verify email** (agar required ho)

---

### Step 2: PostgreSQL Database Banayein

1. **Render Dashboard me:**
   - Click **"New +"** (top right)
   - Click **"PostgreSQL"**

2. **Form Fill Karein:**
   - **Name:** `contract-analyzer-db`
   - **Region:** `Oregon (US West)` (ya closest)
   - **PostgreSQL Version:** `18` (latest)
   - **Plan:** **Free**

3. **Click:** "Create Database"

4. **Wait:** 2-3 minutes (database create hone tak)

---

### Step 3: Database URL Copy Karein

1. **Database service me jao:**
   - Dashboard me database service click karo

2. **"Connect" button click karo:**
   - Top right me "Connect" button hai
   - Dropdown arrow ke saath

3. **"Internal Database URL" copy karo:**
   - Format: `postgresql://user:password@host:port/database`
   - Example: `postgresql://contract_analyzer_db_user:abc123@dpg-xxxxx.oregon-postgres.render.com/contract_analyzer_db`
   - **⚠️ IMPORTANT:** Internal URL use karo (External nahi)

4. **Save karo:** Kisi safe jagah (notepad me)

---

### Step 4: Backend Web Service Deploy Karein

1. **Render Dashboard me:**
   - Click **"New +"** (top right)
   - Click **"Web Service"**

2. **GitHub Connect Karein:**
   - **"Connect GitHub"** click karo (agar pehle se connected nahi hai)
   - Authorize Render
   - Repository select karo: `normienishant/legal_contract_analyser`
   - Click **"Connect"**

3. **Service Configure Karein:**
   - **Name:** `contract-analyzer-backend`
   - **Region:** Same as database (e.g., `Oregon (US West)`)
   - **Branch:** `master` ⚠️ **IMPORTANT!**
   - **Root Directory:** `backend` ⚠️ **CRITICAL!**
   - **Runtime:** `Python 3` (NOT Docker)
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

---

### Step 5: Environment Variables Add Karein (Render Me)

1. **Service me jao:**
   - Service create hone ke baad, service me click karo

2. **"Environment" tab:**
   - Left sidebar me "Environment" tab click karo

3. **Variables Add Karein:**

   Click **"Add Environment Variable"** for each:

   **a) DATABASE_URL:**
   - **Key:** `DATABASE_URL`
   - **Value:** Paste Internal Database URL (Step 3 se)
   - Example: `postgresql://contract_analyzer_db_user:abc123@dpg-xxxxx.oregon-postgres.render.com/contract_analyzer_db`

   **b) ML_MODE:**
   - **Key:** `ML_MODE`
   - **Value:** `ml`

   **c) SECRET_KEY:**
   - **Key:** `SECRET_KEY`
   - **Value:** Naya generate karo (PowerShell command se)
   - **⚠️ IMPORTANT:** Local wale se alag hona chahiye

   **d) ALLOWED_ORIGINS:**
   - **Key:** `ALLOWED_ORIGINS`
   - **Value:** `https://your-frontend.vercel.app,http://localhost:3000`
   - **Note:** Frontend deploy hone ke baad update karna hoga

   **e) ENVIRONMENT:**
   - **Key:** `ENVIRONMENT`
   - **Value:** `production`

   **f) LOG_LEVEL:**
   - **Key:** `LOG_LEVEL`
   - **Value:** `INFO`

4. **Save Karein:**
   - Har variable ke baad "Save" click karo
   - Service automatically redeploy hoga

---

### Step 6: Deploy Wait Karein

1. **"Deployments" tab check karo:**
   - Left sidebar me "Deployments" tab
   - Latest deployment click karo

2. **Logs dekho:**
   - Build process dikhega
   - Dependencies install honge
   - App start hoga

3. **Wait:** 5-10 minutes (pehli baar)

4. **Success check:**
   - Logs me dikhega: `Application startup complete`
   - Status: "Live" ya "Running"

---

### Step 7: Backend URL Get Karein

1. **Service me jao:**
   - Service dashboard me

2. **"Settings" tab:**
   - Left sidebar me "Settings" tab

3. **"Domains" section:**
   - Scroll down to "Domains"
   - **"Generate Domain"** click karo (agar nahi hai)
   - Ya auto-generated URL copy karo

4. **Backend URL:**
   - Format: `https://contract-analyzer-backend.onrender.com`
   - Ya: `https://<random-name>.onrender.com`
   - **Save karo** - frontend me use hoga

---

### Step 8: Test Karein

1. **Health Check:**
   - Browser me jao: `https://your-backend.onrender.com/health`
   - Should return: `{"status": "healthy", "ml_mode": "ml"}`

2. **API Docs:**
   - Browser me jao: `https://your-backend.onrender.com/docs`
   - Swagger UI dikhna chahiye

3. **Root:**
   - Browser me jao: `https://your-backend.onrender.com/`
   - API info dikhna chahiye

---

## ✅ PART 2 Complete: Backend Deployed!

Ab aapka backend live hai:
- ✅ Render pe deployed
- ✅ Database connected
- ✅ Environment variables set
- ✅ URL ready

---

## 📝 Summary Checklist

### Local Setup:
- [ ] `.env` file created in `backend/` folder
- [ ] All values filled in `.env`
- [ ] SECRET_KEY generated
- [ ] Backend runs locally

### Render Setup:
- [ ] Render account created
- [ ] PostgreSQL database created
- [ ] Internal Database URL copied
- [ ] Backend service created
- [ ] Root Directory set to `backend`
- [ ] Branch set to `master`
- [ ] All environment variables added
- [ ] Service deployed successfully
- [ ] Backend URL noted
- [ ] Health check passed

---

## 🎯 Next Steps

1. ✅ Backend deployed
2. ⏭️ Frontend deploy karo (Vercel pe)
3. ⏭️ Frontend me backend URL update karo
4. ⏭️ Test full application

---

## 🐛 Common Issues & Solutions

### Issue 1: Build Fails
**Solution:**
- Check `requirements.txt` exists
- Check Root Directory is `backend`
- Check logs for specific errors

### Issue 2: Database Connection Error
**Solution:**
- Verify Internal Database URL (not External)
- Check database service is running
- Ensure same region

### Issue 3: Service Won't Start
**Solution:**
- Check Start Command uses `$PORT`
- Check all environment variables are set
- Check logs for errors

### Issue 4: CORS Errors
**Solution:**
- Update `ALLOWED_ORIGINS` with frontend URL
- Check no spaces after commas
- Verify frontend URL is correct

---

## 🎉 Done!

Ab aapka backend completely deployed hai! 

**Koi question ho toh pucho!** 🚀

