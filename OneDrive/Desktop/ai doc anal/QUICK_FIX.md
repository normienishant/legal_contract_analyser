# Quick Fix - Backend Start Issue

## Problem
Backend start nahi ho raha ya "Failed to fetch" error aa raha hai.

## Solution

### Step 1: Backend Start Karo (Manually)

PowerShell mein yeh commands chalao:

```powershell
cd "C:\Users\nisha\OneDrive\Desktop\ai doc anal\backend"
.\venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Agar error aaye, to yeh check karo:

1. **Virtual environment activate hua?**
   - `(venv)` dikhna chahiye prompt mein

2. **Dependencies install hui?**
   ```powershell
   python -m pip list | Select-String "fastapi"
   ```

3. **.env file hai?**
   - `backend\.env` file check karo

### Step 2: Check Backend Running

Nayi PowerShell window mein:
```powershell
curl http://localhost:8000/health
```

Agar response aaye, matlab backend running hai!

### Step 3: Frontend Start Karo

Ek aur nayi PowerShell window:
```powershell
cd "C:\Users\nisha\OneDrive\Desktop\ai doc anal\frontend"
npm run dev
```

### Step 4: Test Karo

Browser mein: http://localhost:3000

## Common Errors

### Error: "No module named uvicorn"
**Fix:**
```powershell
cd backend
.\venv\Scripts\Activate.ps1
python -m pip install uvicorn fastapi
```

### Error: "Failed to fetch"
**Fix:**
- Backend running hai ya nahi check karo
- `http://localhost:8000/health` browser mein kholo
- Agar response aaye, backend running hai

### Error: CORS error
**Fix:**
- Backend mein CORS already configured hai
- Agar phir bhi error aaye, check karo `backend/app/main.py` mein CORS settings

## Quick Test

Backend test karne ke liye:
```powershell
# PowerShell mein
Invoke-WebRequest -Uri http://localhost:8000/health -Method GET
```

Ya browser mein directly kholo:
http://localhost:8000/health

Agar JSON response aaye, backend working hai! ✅

