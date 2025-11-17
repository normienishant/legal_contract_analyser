# Test Backend Script
Write-Host "Testing Backend..." -ForegroundColor Green

Set-Location "C:\Users\nisha\OneDrive\Desktop\ai doc anal\backend"

# Activate virtual environment
Write-Host "`nActivating virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv\Scripts\Activate.ps1") {
    & "venv\Scripts\Activate.ps1"
    Write-Host "Virtual environment activated" -ForegroundColor Green
} else {
    Write-Host "ERROR: Virtual environment not found!" -ForegroundColor Red
    Write-Host "Run setup.ps1 first!" -ForegroundColor Yellow
    exit 1
}

# Check if uvicorn is installed
Write-Host "`nChecking uvicorn..." -ForegroundColor Yellow
$uvicornCheck = python -c "import uvicorn; print('OK')" 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "uvicorn is installed" -ForegroundColor Green
} else {
    Write-Host "ERROR: uvicorn not installed!" -ForegroundColor Red
    Write-Host "Installing uvicorn..." -ForegroundColor Yellow
    python -m pip install uvicorn fastapi
}

# Check if app can be imported
Write-Host "`nChecking app imports..." -ForegroundColor Yellow
$importCheck = python -c "from app.main import app; print('OK')" 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "App imports OK" -ForegroundColor Green
} else {
    Write-Host "ERROR: App import failed!" -ForegroundColor Red
    Write-Host $importCheck -ForegroundColor Yellow
    exit 1
}

# Start server
Write-Host "`nStarting backend server..." -ForegroundColor Green
Write-Host "Backend will be available at: http://localhost:8000" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop" -ForegroundColor Yellow
Write-Host ""

python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

