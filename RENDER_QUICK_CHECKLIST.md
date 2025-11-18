# ✅ Render Backend Deployment - Quick Checklist

## 🚀 Quick Steps

### 1. New Render Account
- [ ] Open new browser/incognito
- [ ] Go to [dashboard.render.com](https://dashboard.render.com)
- [ ] Sign up with GitHub or email

### 2. Deploy Backend
- [ ] Click "New +" → "Web Service"
- [ ] Connect GitHub: `normienishant/legal_contract_analyser`
- [ ] Settings:
  - [ ] Name: `contract-analyzer-backend`
  - [ ] Branch: `master`
  - [ ] Root Directory: `backend` ⚠️
  - [ ] Build: `pip install -r requirements.txt`
  - [ ] Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### 3. Environment Variables
- [ ] `ML_MODE` = `ml`
- [ ] `SECRET_KEY` = `<generate-32-chars>`
- [ ] `ALLOWED_ORIGINS` = `https://your-frontend.vercel.app,http://localhost:3000`
- [ ] `ENVIRONMENT` = `production`
- [ ] `LOG_LEVEL` = `INFO`
- [ ] `PORT` = `$PORT`

### 4. Add Disk (For SQLite)
- [ ] Name: `sqlite-storage`
- [ ] Mount: `/opt/render/project/src`
- [ ] Size: `1 GB`

### 5. Deploy
- [ ] Click "Create Web Service"
- [ ] Wait 5-10 minutes
- [ ] Check logs

### 6. Test
- [ ] Visit: `https://your-backend.onrender.com/health`
- [ ] Should return: `{"status": "healthy"}`

---

## 📝 Generate SECRET_KEY

```powershell
-join ((48..57) + (65..90) + (97..122) | Get-Random -Count 32 | ForEach-Object {[char]$_})
```

---

## 🎯 After Deployment

1. Note backend URL
2. Update frontend `NEXT_PUBLIC_API_URL`
3. Deploy frontend on Vercel

---

**Full guide:** See `RENDER_COMPLETE_BACKEND_GUIDE.md`

