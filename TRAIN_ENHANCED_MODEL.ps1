# Script to create enhanced dataset and train new model

Write-Host "=== ENHANCED MODEL TRAINING (20,000 SAMPLES) ===" -ForegroundColor Green
Write-Host ""

# Step 1: Create enhanced dataset
Write-Host "[1/2] Creating enhanced legal dataset (20,000 samples)..." -ForegroundColor Cyan
Write-Host "   This will take 5-10 minutes..." -ForegroundColor Yellow
Write-Host ""

cd "C:\Users\nisha\OneDrive\Desktop\ai doc anal\ml_data"

if (-not (Test-Path "create_enhanced_legal_dataset.py")) {
    Write-Host "❌ Script not found!" -ForegroundColor Red
    exit 1
}

python create_enhanced_legal_dataset.py --output enhanced_legal_dataset.csv --samples 20000

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Dataset creation failed!" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path "enhanced_legal_dataset.csv")) {
    Write-Host "❌ Dataset file not created!" -ForegroundColor Red
    exit 1
}

$file = Get-Item "enhanced_legal_dataset.csv"
$lines = (Get-Content "enhanced_legal_dataset.csv" | Measure-Object -Line).Lines
$samples = $lines - 1

Write-Host ""
Write-Host "✅ Dataset created successfully!" -ForegroundColor Green
Write-Host "   File: enhanced_legal_dataset.csv" -ForegroundColor White
Write-Host "   Size: $([math]::Round($file.Length / 1MB, 2)) MB" -ForegroundColor White
Write-Host "   Samples: $samples" -ForegroundColor Green
Write-Host ""

# Step 2: Train model
Write-Host "[2/2] Training model on enhanced dataset..." -ForegroundColor Cyan
Write-Host "   This will take 60-120 minutes..." -ForegroundColor Yellow
Write-Host "   Dataset: enhanced_legal_dataset.csv ($samples samples)" -ForegroundColor White
Write-Host "   Epochs: 5" -ForegroundColor White
Write-Host "   Batch Size: 16" -ForegroundColor White
Write-Host ""

cd "C:\Users\nisha\OneDrive\Desktop\ai doc anal\backend"

if (Test-Path "venv\Scripts\Activate.ps1") {
    .\venv\Scripts\Activate.ps1
    
    Write-Host "Starting training..." -ForegroundColor Green
    Write-Host ""
    
    python -m app.ml.train --data ../ml_data/enhanced_legal_dataset.csv --output ./models/risk_classifier --epochs 5 --batch-size 16
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "=== TRAINING COMPLETE ===" -ForegroundColor Green
        Write-Host "✅ Enhanced model trained successfully!" -ForegroundColor Green
        Write-Host "   Model saved to: backend/models/risk_classifier/" -ForegroundColor White
    } else {
        Write-Host ""
        Write-Host "❌ Training failed!" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "❌ Virtual environment not found!" -ForegroundColor Red
    Write-Host "   Please setup backend first" -ForegroundColor Yellow
    exit 1
}

