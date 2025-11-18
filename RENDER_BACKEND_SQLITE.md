# 🚀 Backend Deployment with SQLite (No Database Service Needed!)

## ✅ Solution: Use SQLite Instead

Since you already have 1 PostgreSQL database on Render (free tier limit), we'll use **SQLite** which:
- ✅ No separate database service needed
- ✅ Works perfectly for your app
- ✅ Already configured in backend
- ✅ Free and unlimited!

---

## 📝 Step-by-Step Deployment

### Step 1: Deploy Backend Web Service

1. In Render Dashboard, click **"New +"** → **"Web Service"**

2. **Connect Repository:**
   - Click **"Connect GitHub"** (if not connected)
   - Select repository: `normienishant/legal_contract_analyser`
   - Click **"Connect"**

3. **Configure Service:**
   - **Name:** `contract-analyzer-backend`
   - **Region:** `Oregon (US West)` (or any)
   - **Branch:** `master`
   - **Root Directory:** `backend` ⚠️ **CRITICAL!**
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

4. **Environment Variables:**
   Click **"Advanced"** → Add these:

   | Key | Value | Notes |
   |-----|-------|-------|
   | `ML_MODE` | `ml` | Use ML model |
   | `SECRET_KEY` | `<random-32-chars>` | Generate below |
   | `ALLOWED_ORIGINS` | `https://your-frontend.vercel.app,http://localhost:3000` | Update with your frontend URL |
   | `ENVIRONMENT` | `production` | |
   | `LOG_LEVEL` | `INFO` | |
   | `PORT` | `$PORT` | Auto-set by Render |

   **⚠️ IMPORTANT:** Do NOT add `DATABASE_URL` - SQLite will be used automatically!

   **Generate SECRET_KEY:**
   ```powershell
   -join ((48..57) + (65..90) + (97..122) | Get-Random -Count 32 | ForEach-Object {[char]$_})
   ```

5. **Add Persistent Disk (for SQLite database):**
   - Click **"Advanced"** → **"Add Disk"**
   - **Name:** `sqlite-storage`
   - **Mount Path:** `/opt/render/project/src`
   - **Size:** `1 GB` (free tier allows up to 1GB)

   This ensures your SQLite database persists across deployments.

6. Click **"Create Web Service"**

7. **Wait 5-10 minutes** for first deployment

---

## ✅ Advantages of SQLite

- ✅ No database service needed
- ✅ Works perfectly for your use case
- ✅ Simpler setup
- ✅ No connection strings needed
- ✅ Database file stored on disk

---

## 🔧 How It Works

- Backend will create `contract_analyzer.db` file automatically
- Database stored on persistent disk
- All features work the same!

---

## 📊 After Deployment

1. ✅ Test health endpoint: `https://your-backend.onrender.com/health`
2. ✅ Test API docs: `https://your-backend.onrender.com/docs`
3. ✅ Update frontend with backend URL
4. ✅ Deploy frontend on Vercel

---

## 🎉 That's It!

No PostgreSQL needed - SQLite works perfectly! 🚀

