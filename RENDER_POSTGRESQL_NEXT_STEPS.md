# 🗄️ Render PostgreSQL - Next Steps

## ✅ Current Status

- ✅ PostgreSQL selected
- ✅ Ready to create database

---

## 🎯 Step 1: Create PostgreSQL Database

### Fill in the form:

1. **Name:** `contract-analyzer-db` (or any name)
2. **Region:** `Oregon (US West)` (or closest to you)
3. **PostgreSQL Version:** `18` (or latest)
4. **Plan:** **Free** (for testing)

### Click "Create Database"

- Wait 2-3 minutes for database to be created
- Database will be provisioned automatically

---

## 📋 Step 2: Copy Database URL

After database is created:

1. Go to your database service
2. Look for **"Internal Database URL"** ⚠️ **USE THIS ONE!**
3. **Copy the URL** - looks like:
   ```
   postgresql://user:password@host:port/database
   ```
4. **Save it** - you'll need it for backend!

**Important:**
- Use **Internal Database URL** (works within Render network)
- **NOT** External Database URL (for outside access)

---

## 🚀 Step 3: Deploy Backend

### 3.1 Create Web Service

1. In Render Dashboard, click **"New +"** → **"Web Service"**
2. **Connect GitHub:**
   - Click **"Connect GitHub"** (if first time)
   - Authorize Render
   - Select repository: `normienishant/legal_contract_analyser`
   - Click **"Connect"**

### 3.2 Configure Service

Fill in:

- **Name:** `contract-analyzer-backend`
- **Region:** Same as database (e.g., `Oregon (US West)`)
- **Branch:** `master` ⚠️ **IMPORTANT!**
- **Root Directory:** `backend` ⚠️ **CRITICAL!**
- **Runtime:** `Python 3`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### 3.3 Add Environment Variables

Click **"Advanced"** → **"Add Environment Variable"**:

```
DATABASE_URL = <paste-internal-database-url-from-step-2>
ML_MODE = ml
SECRET_KEY = <generate-random-32-chars>
ALLOWED_ORIGINS = https://your-frontend.vercel.app,http://localhost:3000
ENVIRONMENT = production
LOG_LEVEL = INFO
PORT = $PORT
```

**Generate SECRET_KEY:**
```powershell
-join ((48..57) + (65..90) + (97..122) | Get-Random -Count 32 | ForEach-Object {[char]$_})
```

### 3.4 Deploy!

1. Click **"Create Web Service"**
2. Wait 5-10 minutes for deployment
3. Check **"Logs"** tab for progress

---

## ✅ Step 4: Verify

### Test Endpoints:

1. **Health Check:**
   - Visit: `https://your-backend.onrender.com/health`
   - Should return: `{"status": "healthy", "ml_mode": "ml"}`

2. **API Docs:**
   - Visit: `https://your-backend.onrender.com/docs`
   - Should show Swagger UI

---

## ⚠️ Important Notes

### Database:
- ✅ **Free for 90 days**
- ⚠️ **Then $7/month** (or data gets deleted)
- ✅ Use **Internal Database URL** (not External)

### Backend:
- ✅ **Free forever** (but spins down after 15 min)
- ✅ First request takes 30-60 seconds (cold start)

---

## 🎯 Next Steps

1. ✅ Create database (wait 2-3 minutes)
2. ✅ Copy Internal Database URL
3. ✅ Deploy backend with DATABASE_URL
4. ✅ Test endpoints
5. ✅ Deploy frontend on Vercel

---

**Database create hone ke baad Internal Database URL copy karo aur backend deploy karo!** 🚀

