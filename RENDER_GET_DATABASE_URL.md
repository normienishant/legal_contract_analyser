# 🔗 Get Database URL from Render

## ✅ Database Created!

- ✅ Name: `contract-analyzer-db`
- ✅ PostgreSQL Version: 18
- ✅ Region: Oregon (US West)
- ⏳ Status: "Unknown" (still provisioning - wait 1-2 minutes)

---

## 🎯 Step 1: Wait for Database to be Ready

1. **Wait 1-2 minutes** for database to provision
2. **Refresh the page** if needed
3. Status should change from "Unknown" to "Available" or "Running"

---

## 🔗 Step 2: Get Internal Database URL

### Method 1: Using "Connect" Button

1. Click the **"Connect"** button (top right, with dropdown arrow)
2. You'll see connection options:
   - **Internal Database URL** ⚠️ **USE THIS ONE!**
   - External Database URL (ignore for now)
3. **Copy the Internal Database URL**
   - Format: `postgresql://user:password@host:port/database`
   - Looks like: `postgresql://contract_analyzer_db_user:xxxxx@dpg-d4dm343e5dus73b3squ0-a.oregon-postgres.render.com/contract_analyzer_db`

### Method 2: From Info Section

1. Scroll down to **"Connection"** or **"Database"** section
2. Look for **"Internal Database URL"**
3. Click **copy icon** next to it
4. **Save it** - you'll need it for backend!

---

## ⚠️ Important Notes

### Use Internal Database URL:
- ✅ Works within Render network
- ✅ Faster connection
- ✅ More secure
- ✅ **This is what you need!**

### Don't Use External Database URL:
- ❌ For outside access only
- ❌ Slower
- ❌ Not needed for backend on Render

---

## 📋 Step 3: Save Database URL

**Copy and save this URL somewhere safe:**
```
postgresql://user:password@host:port/database
```

You'll paste this in backend environment variables as:
```
DATABASE_URL = <paste-url-here>
```

---

## 🚀 Step 4: Deploy Backend

Once you have the Internal Database URL:

1. Go to Render Dashboard
2. Click **"New +"** → **"Web Service"**
3. Connect GitHub: `normienishant/legal_contract_analyser`
4. Configure:
   - Root Directory: `backend`
   - Branch: `master`
   - Build: `pip install -r requirements.txt`
   - Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add Environment Variables:
   ```
   DATABASE_URL = <paste-internal-database-url>
   ML_MODE = ml
   SECRET_KEY = <generate-32-chars>
   ALLOWED_ORIGINS = https://your-frontend.vercel.app,http://localhost:3000
   ENVIRONMENT = production
   LOG_LEVEL = INFO
   ```
6. Deploy!

---

## ⏰ Database Expiration Notice

You'll see: **"Your database will expire on December 17, 2025"**

**What this means:**
- ✅ Database is **free for 90 days**
- ⚠️ After 90 days, you need to:
  - Pay $7/month, OR
  - Switch to SQLite (free forever)

**For now:** Don't worry - you have 90 days! Use it and enjoy! 🎉

---

## ✅ Next Steps

1. ✅ Wait for database status to be "Available"
2. ✅ Click "Connect" button
3. ✅ Copy Internal Database URL
4. ✅ Deploy backend with DATABASE_URL
5. ✅ Test endpoints

---

**Database ready hone ke baad "Connect" button se Internal Database URL copy karo!** 🚀

