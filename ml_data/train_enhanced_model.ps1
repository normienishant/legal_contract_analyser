# PowerShell script to create enhanced legal dataset and train model

Write-Host "=== ENHANCED LEGAL DATA TRAINING ===" -ForegroundColor Green
Write-Host ""

# Step 1: Create enhanced dataset
Write-Host "[1/2] Creating enhanced legal dataset..." -ForegroundColor Cyan
Write-Host "   This will generate 20,000+ samples with extensive Indian legal data" -ForegroundColor Yellow
Write-Host ""

cd "C:\Users\nisha\OneDrive\Desktop\ai doc anal\ml_data"

python create_enhanced_legal_dataset.py --output enhanced_legal_dataset.csv --samples 20000

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error creating dataset!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "[2/2] Training model on enhanced legal data..." -ForegroundColor Cyan
Write-Host ""

cd "C:\Users\nisha\OneDrive\Desktop\ai doc anal\backend"

if (Test-Path "venv\Scripts\Activate.ps1") {
    .\venv\Scripts\Activate.ps1
    
    Write-Host "Dataset: enhanced_legal_dataset.csv (20,000 samples)" -ForegroundColor White
    Write-Host "Epochs: 5" -ForegroundColor White
    Write-Host "Batch Size: 16" -ForegroundColor White
    Write-Host "Expected Time: 60-120 minutes" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Starting training..." -ForegroundColor Green
    Write-Host ""
    
    python -m app.ml.train --data ../ml_data/enhanced_legal_dataset.csv --output ./models/risk_classifier --epochs 5 --batch-size 16
    
    Write-Host ""
    Write-Host "=== TRAINING COMPLETE ===" -ForegroundColor Green
} else {
    Write-Host "Virtual environment not found!" -ForegroundColor Red
}

