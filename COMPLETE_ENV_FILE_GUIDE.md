# 🔐 Complete .env File Guide - Everything You Need to Know

## 📋 What is .env File?

`.env` file stores environment variables (secrets, API keys, database URLs, etc.)
- ✅ **Local development** ke liye use hota hai
- ✅ **Production** me Render ke environment variables me add karte hain
- ✅ **Never commit** `.env` to GitHub (already in .gitignore)

---

## 🎯 Two Places to Add Variables

### 1. Local Development (.env file)
- Location: `backend/.env`
- For: Testing on your computer

### 2. Production (Render Environment Variables)
- Location: Render Dashboard → Service → Environment tab
- For: Live deployed backend

---

## 📝 Complete .env File Template

Create file: `backend/.env`

```env
# ============================================
# SERVER CONFIGURATION
# ============================================
PORT=8000
ENVIRONMENT=development

# ============================================
# DATABASE CONFIGURATION
# ============================================
# For Local Development (SQLite):
DATABASE_URL=sqlite:///./contract_analyzer.db

# For Production (PostgreSQL on Render):
# DATABASE_URL=postgresql://user:password@host:port/database
# Copy from Render PostgreSQL service → Connect → Internal Database URL

# ============================================
# ML MODEL CONFIGURATION
# ============================================
ML_MODE=ml
# Options: "ml" (use ML model) or "rules" (rule-based only)
MODEL_PATH=./models/risk_classifier

# ============================================
# SECURITY
# ============================================
SECRET_KEY=your-secret-key-here-change-this-in-production
# Generate random 32 characters (see below)

# ============================================
# CORS (Cross-Origin Resource Sharing)
# ============================================
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
# Add your frontend URLs (comma-separated, no spaces)
# For production, add: https://your-frontend.vercel.app

# ============================================
# LOGGING
# ============================================
LOG_LEVEL=INFO
# Options: DEBUG, INFO, WARNING, ERROR

# ============================================
# FILE UPLOAD
# ============================================
MAX_UPLOAD_SIZE_MB=10
ALLOWED_EXTENSIONS=pdf,docx,txt

# ============================================
# HUGGING FACE (Optional)
# ============================================
# HF_TOKEN=your-huggingface-token-here
# Only if using Hugging Face models
```

---

## 🔑 How to Get Each Key/Value

### 1. PORT
**What:** Server port number
**Local:** `8000` (default)
**Production:** `$PORT` (Render automatically sets this)
**How to get:** 
- Local: Use `8000`
- Production: Render sets automatically (don't add manually)

---

### 2. ENVIRONMENT
**What:** Current environment (development/production)
**Local:** `development`
**Production:** `production`
**How to get:** 
- Just type: `development` or `production`

---

### 3. DATABASE_URL

#### For Local Development (SQLite):
```
DATABASE_URL=sqlite:///./contract_analyzer.db
```
**How to get:** 
- Just use this value (SQLite file will be created automatically)
- No setup needed!

#### For Production (PostgreSQL on Render):
```
DATABASE_URL=postgresql://user:password@host:port/database
```
**How to get:**
1. Go to Render Dashboard
2. Click on your PostgreSQL database service
3. Click **"Connect"** button (top right)
4. Copy **"Internal Database URL"**
5. Paste it here

**Example:**
```
DATABASE_URL=postgresql://contract_analyzer_db_user:abc123xyz@dpg-d4dm343e5dus73b3squ0-a.oregon-postgres.render.com/contract_analyzer_db
```

---

### 4. ML_MODE
**What:** Use ML model or rule-based analysis
**Value:** `ml` or `rules`
**How to get:**
- Use `ml` to use trained ML model
- Use `rules` for rule-based only (no ML)

---

### 5. SECRET_KEY
**What:** Secret key for security (encryption, sessions, etc.)
**How to generate:**

**PowerShell:**
```powershell
-join ((48..57) + (65..90) + (97..122) | Get-Random -Count 32 | ForEach-Object {[char]$_})
```

**Python:**
```python
import secrets
print(secrets.token_urlsafe(32))
```

**Online:**
- Go to: https://randomkeygen.com/
- Use "CodeIgniter Encryption Keys" (32 characters)

**Example:**
```
SECRET_KEY=aB3dE5fG7hI9jK1lM3nO5pQ7rS9tU1vW3xY5zA7bC9dE1
```

**Important:**
- ✅ Generate a new one for production
- ✅ Keep it secret (never share)
- ✅ Use different keys for local and production

---

### 6. ALLOWED_ORIGINS
**What:** Frontend URLs that can access your backend
**Local:**
```
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```
**Production:**
```
ALLOWED_ORIGINS=https://your-frontend.vercel.app,http://localhost:3000
```
**How to get:**
1. **Local:** Use `http://localhost:3000` (your local frontend)
2. **Production:** 
   - Deploy frontend on Vercel
   - Get your Vercel URL (e.g., `https://contract-analyzer.vercel.app`)
   - Add it here
   - Keep `localhost:3000` for local testing

**Format:**
- Comma-separated
- No spaces after commas
- Include `http://` or `https://`

---

### 7. LOG_LEVEL
**What:** How much logging you want
**Options:** `DEBUG`, `INFO`, `WARNING`, `ERROR`
**How to get:**
- Use `INFO` for normal use
- Use `DEBUG` for detailed logs (development)
- Use `ERROR` for only errors (production)

---

### 8. MAX_UPLOAD_SIZE_MB
**What:** Maximum file upload size
**Value:** `10` (10 MB)
**How to get:**
- Just use `10` (or any number you want)

---

### 9. ALLOWED_EXTENSIONS
**What:** File types allowed for upload
**Value:** `pdf,docx,txt`
**How to get:**
- List file extensions you want to allow
- Comma-separated, no spaces

---

### 10. HF_TOKEN (Optional)
**What:** Hugging Face API token (if using HF models)
**How to get:**
1. Go to: https://huggingface.co/settings/tokens
2. Create new token
3. Copy and paste here
**Note:** Only needed if using Hugging Face models (you're not, so skip this)

---

## 📁 Create .env File

### Step 1: Create File
Create file: `backend/.env`

### Step 2: Copy Template
Copy the template above and paste in `backend/.env`

### Step 3: Fill Values
Replace placeholder values with your actual values:
- Generate `SECRET_KEY`
- Add `DATABASE_URL` (SQLite for local)
- Update `ALLOWED_ORIGINS` (add frontend URL after deployment)

### Step 4: Save
Save the file

---

## 🚀 For Production (Render)

### Don't Use .env File!
Instead, add variables in Render Dashboard:

1. Go to Render Dashboard
2. Click your backend service
3. Go to **"Environment"** tab
4. Click **"Add Environment Variable"**
5. Add each variable:

```
DATABASE_URL = <from-postgresql-service>
ML_MODE = ml
SECRET_KEY = <generate-new-one>
ALLOWED_ORIGINS = https://your-frontend.vercel.app,http://localhost:3000
ENVIRONMENT = production
LOG_LEVEL = INFO
```

---

## ✅ Quick Checklist

### Local Development (.env file):
- [ ] PORT=8000
- [ ] ENVIRONMENT=development
- [ ] DATABASE_URL=sqlite:///./contract_analyzer.db
- [ ] ML_MODE=ml
- [ ] SECRET_KEY=<generate-32-chars>
- [ ] ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
- [ ] LOG_LEVEL=INFO

### Production (Render Environment Variables):
- [ ] DATABASE_URL=<from-postgresql>
- [ ] ML_MODE=ml
- [ ] SECRET_KEY=<generate-new-32-chars>
- [ ] ALLOWED_ORIGINS=https://your-frontend.vercel.app,http://localhost:3000
- [ ] ENVIRONMENT=production
- [ ] LOG_LEVEL=INFO

---

## 🔒 Security Notes

### Never Commit .env to GitHub:
- ✅ Already in `.gitignore`
- ✅ Contains secrets
- ✅ Keep it local only

### Use Different Keys:
- ✅ Different `SECRET_KEY` for local and production
- ✅ Different `DATABASE_URL` (SQLite vs PostgreSQL)
- ✅ Different `ALLOWED_ORIGINS`

---

## 🐛 Troubleshooting

### .env File Not Working:
1. Check file is named exactly `.env` (not `.env.txt`)
2. Check file is in `backend/` directory
3. Restart your backend server
4. Check no spaces around `=` sign

### Variables Not Loading:
1. Verify `.env` file format (KEY=VALUE, no spaces)
2. Check backend is reading from correct location
3. Restart backend server

---

## 📚 Summary

**Local Development:**
- Create `backend/.env` file
- Add all variables with local values
- Use SQLite database

**Production (Render):**
- Don't use .env file
- Add variables in Render Dashboard → Environment tab
- Use PostgreSQL database URL

**All keys explained above!** 🎯

