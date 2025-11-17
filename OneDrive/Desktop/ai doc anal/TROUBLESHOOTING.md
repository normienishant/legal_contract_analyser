# Troubleshooting Guide

## "Failed to extract text" Error

Agar yeh error aa raha hai, to yeh steps follow karo:

### Step 1: Check Backend Running

Backend terminal mein check karo ki backend running hai:
- Terminal mein `INFO:     Uvicorn running on http://0.0.0.0:8000` dikhna chahiye
- Agar nahi dikh raha, backend start karo:
  ```powershell
  cd backend
  .\venv\Scripts\Activate.ps1
  python -m uvicorn app.main:app --reload
  ```

### Step 2: Check Backend Logs

Backend terminal mein error logs check karo. Kuch aisa dikhega:
```
ERROR: Error extracting text: [actual error message]
```

### Step 3: Test Backend Directly

Browser mein directly test karo:
```
http://localhost:8000/health
```

Agar JSON response aaye, backend running hai.

### Step 4: Check File Upload

Backend terminal mein check karo ki file upload ho rahi hai:
- `File uploaded: [filename]` message dikhna chahiye
- `backend/uploads/` folder mein file honi chahiye

### Step 5: Common Issues

#### Issue: File not found
**Fix:** Check karo ki `backend/uploads/` folder exist karta hai:
```powershell
Test-Path "backend\uploads"
```

#### Issue: Permission error
**Fix:** Check karo ki backend ko file read karne ki permission hai.

#### Issue: Encoding error (TXT files)
**Fix:** TXT file UTF-8 encoding mein honi chahiye.

### Step 6: Manual Test

PowerShell mein manually test karo:
```powershell
# Upload file
$file = Get-Item "ml_data\sample_contract.txt"
$formData = @{
    file = $file
}
Invoke-WebRequest -Uri "http://localhost:8000/api/upload" -Method POST -Form $formData

# Extract (file_id use karo jo upload response mein aaya)
Invoke-WebRequest -Uri "http://localhost:8000/api/extract?file_id=YOUR_FILE_ID" -Method POST
```

## Backend Not Starting

### Error: "No module named uvicorn"
**Fix:**
```powershell
cd backend
.\venv\Scripts\Activate.ps1
python -m pip install uvicorn fastapi
```

### Error: Import errors
**Fix:** Sab dependencies install karo:
```powershell
cd backend
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Frontend Not Connecting

### Error: "Failed to fetch"
**Fix:**
1. Backend running hai ya nahi check karo
2. Browser console mein check karo (F12)
3. CORS error ho sakta hai - backend mein CORS already configured hai

### Error: CORS error
**Fix:** Backend mein CORS settings check karo `backend/app/main.py` mein.

## Still Not Working?

1. **Backend logs check karo** - Terminal mein actual error message dikhega
2. **Browser console check karo** (F12) - Frontend errors dikhenge
3. **Network tab check karo** - API calls successful hain ya nahi

## Quick Fixes

### Restart Everything
```powershell
# Stop backend (Ctrl+C)
# Stop frontend (Ctrl+C)

# Start backend
cd backend
.\venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload

# Start frontend (new terminal)
cd frontend
npm run dev
```

### Clear and Reinstall
```powershell
# Backend
cd backend
Remove-Item -Recurse -Force venv
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt

# Frontend
cd frontend
Remove-Item -Recurse -Force node_modules
npm install
```

