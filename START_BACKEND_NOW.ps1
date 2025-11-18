# Start Backend - Final Working Version
Write-Host "Starting Backend Server..." -ForegroundColor Green

Set-Location "C:\Users\nisha\OneDrive\Desktop\ai doc anal\backend"

# Activate virtual environment
& "venv\Scripts\Activate.ps1"

Write-Host "Backend starting on http://localhost:8000" -ForegroundColor Cyan
Write-Host "API docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop" -ForegroundColor Yellow
Write-Host ""

python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

