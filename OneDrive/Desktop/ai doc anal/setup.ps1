Write-Host "Setting up AI Contract Analyzer..." -ForegroundColor Green

Write-Host "`nChecking Python..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Python not found! Please install Python 3.11+" -ForegroundColor Red
    exit 1
}
Write-Host "Found: $pythonVersion" -ForegroundColor Green

# Create virtual environment
Write-Host "`nCreating virtual environment..." -ForegroundColor Yellow
if (Test-Path "backend\venv") {
    Write-Host "Virtual environment already exists" -ForegroundColor Yellow
} else {
    python -m venv backend\venv
    Write-Host "Virtual environment created" -ForegroundColor Green
}

# Activate virtual environment
Write-Host "`nActivating virtual environment..." -ForegroundColor Yellow
& "backend\venv\Scripts\Activate.ps1"

# Upgrade pip
Write-Host "`nUpgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

# Install backend dependencies
Write-Host "`nInstalling backend dependencies..." -ForegroundColor Yellow
Set-Location backend
pip install -r requirements.txt
Set-Location ..

Write-Host "`nInstalling frontend dependencies..." -ForegroundColor Yellow
Set-Location frontend
npm install
Set-Location ..

Write-Host "`nSetting up environment..." -ForegroundColor Yellow
if (-not (Test-Path "backend\.env")) {
    @"
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
ENVIRONMENT=development
DATABASE_URL=sqlite:///./contract_analyzer.db
ML_MODE=rules
MODEL_PATH=./models/risk_classifier
USE_GPU=false
API_KEY=your_api_key_here
MAX_UPLOAD_SIZE_MB=10
ALLOWED_EXTENSIONS=pdf,docx,txt
LOG_LEVEL=INFO
"@ | Out-File -FilePath "backend\.env" -Encoding utf8
    Write-Host ".env file created" -ForegroundColor Green
}

New-Item -ItemType Directory -Force -Path "backend\uploads" | Out-Null
New-Item -ItemType Directory -Force -Path "backend\models" | Out-Null

Write-Host "`nSetup complete! 🎉" -ForegroundColor Green
Write-Host "`nTo start the backend, run:" -ForegroundColor Cyan
Write-Host "  cd backend" -ForegroundColor White
Write-Host "  .\venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "  python -m uvicorn app.main:app --reload" -ForegroundColor White
Write-Host "`nTo start the frontend (in another terminal):" -ForegroundColor Cyan
Write-Host "  cd frontend" -ForegroundColor White
Write-Host "  npm run dev" -ForegroundColor White