# Start Everything - AI Contract Analyzer
Write-Host "🚀 Starting AI Contract Analyzer..." -ForegroundColor Green
Write-Host ""

# Check if backend venv exists
if (-not (Test-Path "backend\venv\Scripts\Activate.ps1")) {
    Write-Host "❌ Backend virtual environment not found!" -ForegroundColor Red
    Write-Host "   Run: .\setup.ps1 first" -ForegroundColor Yellow
    exit 1
}

# Check if model exists
if (-not (Test-Path "backend\models\risk_classifier\config.json")) {
    Write-Host "⚠️  ML model not found!" -ForegroundColor Yellow
    Write-Host "   Model will use rule-based fallback" -ForegroundColor Yellow
} else {
    Write-Host "✅ ML model found" -ForegroundColor Green
}

Write-Host ""
Write-Host "Starting Backend Server..." -ForegroundColor Cyan
Write-Host "Backend will run on: http://localhost:8000" -ForegroundColor Cyan
Write-Host ""
Write-Host "Starting Frontend Server..." -ForegroundColor Cyan
Write-Host "Frontend will run on: http://localhost:3000" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop both servers" -ForegroundColor Yellow
Write-Host ""

# Start backend in new window
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$PWD\backend'; .\venv\Scripts\Activate.ps1; python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

# Wait a bit for backend to start
Start-Sleep -Seconds 3

# Start frontend in new window
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$PWD\frontend'; npm run dev"

Write-Host "✅ Both servers started in separate windows!" -ForegroundColor Green
Write-Host ""
Write-Host "📝 Open your browser to: http://localhost:3000" -ForegroundColor Cyan
Write-Host ""


