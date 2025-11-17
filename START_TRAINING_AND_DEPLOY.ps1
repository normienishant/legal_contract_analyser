# Complete script: Train model + Deploy application

Write-Host "=== COMPLETE SETUP: TRAINING + DEPLOYMENT ===" -ForegroundColor Green
Write-Host ""

# Step 1: Check if dataset exists, if not create it
Write-Host "[1/3] Checking dataset..." -ForegroundColor Cyan
$datasetPath = "ml_data\enhanced_legal_dataset.csv"

if (-not (Test-Path $datasetPath)) {
    Write-Host "   Dataset not found. Creating enhanced legal dataset..." -ForegroundColor Yellow
    Write-Host "   This will take 5-10 minutes..." -ForegroundColor Yellow
    Write-Host ""
    
    cd ml_data
    python create_enhanced_legal_dataset.py --output enhanced_legal_dataset.csv --samples 20000
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "   Error creating dataset!" -ForegroundColor Red
        exit 1
    }
    
    cd ..
    Write-Host "   ✅ Dataset created!" -ForegroundColor Green
} else {
    Write-Host "   ✅ Dataset already exists!" -ForegroundColor Green
}

Write-Host ""

# Step 2: Train model (if not already trained)
Write-Host "[2/3] Training ML model..." -ForegroundColor Cyan
Write-Host "   This will take 60-120 minutes..." -ForegroundColor Yellow
Write-Host "   You can check progress in the logs" -ForegroundColor Yellow
Write-Host ""

cd backend

if (Test-Path "venv\Scripts\Activate.ps1") {
    .\venv\Scripts\Activate.ps1
    
    Write-Host "   Dataset: enhanced_legal_dataset.csv (20,000 samples)" -ForegroundColor White
    Write-Host "   Epochs: 5" -ForegroundColor White
    Write-Host "   Batch Size: 16" -ForegroundColor White
    Write-Host ""
    Write-Host "   Starting training in background..." -ForegroundColor Green
    Write-Host "   (Training will continue even if you close this window)" -ForegroundColor Yellow
    Write-Host ""
    
    # Start training in background
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; .\venv\Scripts\Activate.ps1; Write-Host '=== ML MODEL TRAINING ===' -ForegroundColor Green; Write-Host ''; python -m app.ml.train --data ../ml_data/enhanced_legal_dataset.csv --output ./models/risk_classifier --epochs 5 --batch-size 16"
    
    Write-Host "   ✅ Training started in new window!" -ForegroundColor Green
    Write-Host "   You can monitor progress there." -ForegroundColor Yellow
} else {
    Write-Host "   ⚠️  Virtual environment not found!" -ForegroundColor Yellow
    Write-Host "   Please setup backend first: cd backend && python -m venv venv" -ForegroundColor Yellow
}

cd ..

Write-Host ""

# Step 3: Deploy application
Write-Host "[3/3] Deploying application..." -ForegroundColor Cyan
Write-Host ""

# Check if Docker is available
if (Get-Command docker -ErrorAction SilentlyContinue) {
    Write-Host "   Docker found. Starting deployment..." -ForegroundColor Green
    Write-Host ""
    
    # Create .env if doesn't exist
    if (-not (Test-Path ".env")) {
        if (Test-Path "env.example") {
            Copy-Item "env.example" ".env"
            Write-Host "   Created .env file from env.example" -ForegroundColor Yellow
            Write-Host "   ⚠️  Please update .env with your settings!" -ForegroundColor Yellow
        }
    }
    
    # Run deployment script
    if (Test-Path "deploy.ps1") {
        .\deploy.ps1
    } else {
        Write-Host "   deploy.ps1 not found. Running docker-compose directly..." -ForegroundColor Yellow
        docker-compose up -d --build
    }
} else {
    Write-Host "   ⚠️  Docker not found!" -ForegroundColor Yellow
    Write-Host "   For local development without Docker:" -ForegroundColor Yellow
    Write-Host "   1. Backend: cd backend && .\venv\Scripts\Activate.ps1 && uvicorn app.main:app --reload" -ForegroundColor White
    Write-Host "   2. Frontend: cd frontend && npm run dev" -ForegroundColor White
}

Write-Host ""
Write-Host "=== SETUP COMPLETE ===" -ForegroundColor Green
Write-Host ""
Write-Host "📊 Training Status: Running in background window" -ForegroundColor Cyan
Write-Host "🚀 Deployment Status: Check above" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "  1. Wait for training to complete (60-120 minutes)" -ForegroundColor White
Write-Host "  2. Access app at http://localhost:3000 (if deployed)" -ForegroundColor White
Write-Host "  3. Check training progress in the training window" -ForegroundColor White
Write-Host ""

