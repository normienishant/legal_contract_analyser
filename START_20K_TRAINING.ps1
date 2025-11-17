# Start 20K Model Training

Write-Host "=== ML MODEL TRAINING (20K SAMPLES) ===" -ForegroundColor Green
Write-Host ""

cd "C:\Users\nisha\OneDrive\Desktop\ai doc anal\backend"

if (Test-Path "venv\Scripts\Activate.ps1") {
    .\venv\Scripts\Activate.ps1
    
    Write-Host "Dataset: enhanced_legal_dataset.csv (20,000 samples)" -ForegroundColor Cyan
    Write-Host "Epochs: 5" -ForegroundColor White
    Write-Host "Batch Size: 16" -ForegroundColor White
    Write-Host "Expected Time: 60-120 minutes" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Starting training..." -ForegroundColor Green
    Write-Host ""
    
    python -m app.ml.train --data ../ml_data/enhanced_legal_dataset.csv --output ./models/risk_classifier --epochs 5 --batch-size 16
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "=== TRAINING COMPLETE ===" -ForegroundColor Green
        Write-Host "Model saved to: backend/models/risk_classifier/" -ForegroundColor Green
    } else {
        Write-Host ""
        Write-Host "Training failed!" -ForegroundColor Red
    }
} else {
    Write-Host "Virtual environment not found!" -ForegroundColor Red
}

Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

