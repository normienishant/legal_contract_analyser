# Start Frontend Server
Write-Host "Starting Frontend Server..." -ForegroundColor Green

Set-Location frontend

# Check if node_modules exists
if (-not (Test-Path "node_modules")) {
    Write-Host "Installing dependencies..." -ForegroundColor Yellow
    npm install
}

Write-Host "Frontend starting on http://localhost:3000" -ForegroundColor Cyan
npm run dev

