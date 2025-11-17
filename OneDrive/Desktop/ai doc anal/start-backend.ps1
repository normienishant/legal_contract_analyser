# Start Backend Server
Write-Host "Starting Backend Server..." -ForegroundColor Green

Set-Location backend

# Activate virtual environment
if (Test-Path "venv\Scripts\Activate.ps1") {
    & "venv\Scripts\Activate.ps1"
} else {
    Write-Host "Virtual environment not found. Run setup.ps1 first!" -ForegroundColor Red
    exit 1
}

# Start server
Write-Host "Backend starting on http://localhost:8000" -ForegroundColor Cyan
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

