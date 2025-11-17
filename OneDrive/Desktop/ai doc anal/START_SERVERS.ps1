# Start Both Backend and Frontend Servers
Write-Host "=== Starting Contract Analyzer Servers ===" -ForegroundColor Green
Write-Host ""

# Start Backend
Write-Host "1. Starting Backend Server..." -ForegroundColor Cyan
Set-Location "C:\Users\nisha\OneDrive\Desktop\ai doc anal\backend"

if (Test-Path "venv\Scripts\Activate.ps1") {
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; .\venv\Scripts\Activate.ps1; Write-Host 'Backend starting on http://localhost:8000' -ForegroundColor Green; python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
    Write-Host "   ✅ Backend starting in new window..." -ForegroundColor Green
} else {
    Write-Host "   ❌ Virtual environment not found!" -ForegroundColor Red
}

Start-Sleep -Seconds 2

# Start Frontend
Write-Host ""
Write-Host "2. Starting Frontend Server..." -ForegroundColor Cyan
Set-Location "C:\Users\nisha\OneDrive\Desktop\ai doc anal\frontend"

if (Test-Path "node_modules") {
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; Write-Host 'Frontend starting on http://localhost:3000' -ForegroundColor Green; npm run dev"
    Write-Host "   ✅ Frontend starting in new window..." -ForegroundColor Green
} else {
    Write-Host "   ❌ node_modules not found! Run 'npm install' first." -ForegroundColor Red
}

Set-Location "C:\Users\nisha\OneDrive\Desktop\ai doc anal"

Write-Host ""
Write-Host "=== Servers Starting ===" -ForegroundColor Yellow
Write-Host ""
Write-Host "Backend:  http://localhost:8000" -ForegroundColor Cyan
Write-Host "Frontend: http://localhost:3000" -ForegroundColor Cyan
Write-Host ""
Write-Host "Wait 10-15 seconds for servers to start, then:" -ForegroundColor Yellow
Write-Host "1. Open browser: http://localhost:3000" -ForegroundColor White
Write-Host "2. Check backend: http://localhost:8000/health" -ForegroundColor White
Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

