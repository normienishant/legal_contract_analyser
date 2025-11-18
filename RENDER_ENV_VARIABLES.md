# 🔧 Render Environment Variables - Complete List

## ✅ Required Environment Variables

Add these in Render → Your Service → "Environment" tab:

---

## 📋 Environment Variables List

### 1. DATABASE_URL (Required)
```
DATABASE_URL = postgresql://user:password@host:port/database
```
**Value:** Copy from PostgreSQL service → "Connect" → "Internal Database URL"

---

### 2. ML_MODE (Required)
```
ML_MODE = ml
```
**Value:** `ml` (to use ML model) or `rules` (rule-based only)

---

### 3. SECRET_KEY (Required)
```
SECRET_KEY = <generate-random-32-chars>
```
**Generate SECRET_KEY:**
```powershell
-join ((48..57) + (65..90) + (97..122) | Get-Random -Count 32 | ForEach-Object {[char]$_})
```
**Example:** `aB3dE5fG7hI9jK1lM3nO5pQ7rS9tU1vW3xY5zA7bC9dE1`

---

### 4. ALLOWED_ORIGINS (Required)
```
ALLOWED_ORIGINS = https://your-frontend.vercel.app,http://localhost:3000
```
**Value:** 
- Add your frontend URL (after Vercel deployment)
- Keep `http://localhost:3000` for local testing
- **No spaces** after commas

**Example:**
```
ALLOWED_ORIGINS = https://contract-analyzer.vercel.app,http://localhost:3000
```

---

### 5. ENVIRONMENT (Required)
```
ENVIRONMENT = production
```
**Value:** `production` (for deployed app)

---

### 6. LOG_LEVEL (Optional but Recommended)
```
LOG_LEVEL = INFO
```
**Value:** `INFO`, `DEBUG`, `WARNING`, or `ERROR`

---

### 7. PORT (Auto-set by Render)
```
PORT = $PORT
```
**Note:** Render automatically sets this - you don't need to add it manually!

---

## 📝 Complete Example

Here's what all your environment variables should look like:

```
DATABASE_URL = postgresql://contract_analyzer_db_user:xxxxx@dpg-d4dm343e5dus73b3squ0-a.oregon-postgres.render.com/contract_analyzer_db
ML_MODE = ml
SECRET_KEY = aB3dE5fG7hI9jK1lM3nO5pQ7rS9tU1vW3xY5zA7bC9dE1
ALLOWED_ORIGINS = https://your-frontend.vercel.app,http://localhost:3000
ENVIRONMENT = production
LOG_LEVEL = INFO
```

---

## 🎯 How to Add in Render

### Step 1: Go to Your Service
1. Click on your backend service
2. Go to **"Environment"** tab

### Step 2: Add Variables
1. Click **"Add Environment Variable"**
2. Enter **Key** and **Value**
3. Click **"Save"**
4. Repeat for each variable

### Step 3: Deploy
- Service will auto-redeploy after adding variables
- Or click **"Manual Deploy"** → **"Deploy latest commit"**

---

## ⚠️ Important Notes

### DATABASE_URL:
- ✅ Use **Internal Database URL** (not External)
- ✅ Copy from PostgreSQL service → "Connect" button
- ✅ Format: `postgresql://user:password@host:port/database`

### ALLOWED_ORIGINS:
- ✅ Add frontend URL after Vercel deployment
- ✅ Keep `localhost:3000` for local testing
- ✅ **No spaces** after commas
- ✅ Can add multiple URLs (comma-separated)

### SECRET_KEY:
- ✅ Generate random 32 characters
- ✅ Use only once (don't share)
- ✅ Keep it secret!

---

## 🔍 Verify Variables

After adding, check:
1. All variables are saved
2. No typos in variable names
3. Values are correct (especially DATABASE_URL)
4. Service redeployed successfully

---

## 🐛 Troubleshooting

### Service Won't Start:
- Check if all required variables are added
- Verify DATABASE_URL is correct
- Check logs for specific errors

### CORS Errors:
- Verify ALLOWED_ORIGINS includes frontend URL
- Check no spaces after commas
- Ensure frontend URL is correct

### Database Connection Error:
- Verify DATABASE_URL is Internal URL (not External)
- Check database service is running
- Ensure database and backend are in same region

---

## ✅ Quick Checklist

- [ ] DATABASE_URL (from PostgreSQL service)
- [ ] ML_MODE = ml
- [ ] SECRET_KEY (generate 32 chars)
- [ ] ALLOWED_ORIGINS (frontend URL + localhost)
- [ ] ENVIRONMENT = production
- [ ] LOG_LEVEL = INFO
- [ ] PORT = $PORT (auto-set, don't add manually)

---

**Add all these variables in Render → Environment tab!** 🚀

