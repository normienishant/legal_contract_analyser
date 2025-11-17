# Train ML Model Script
Write-Host "Training ML Model..." -ForegroundColor Green

# Generate realistic training data
Write-Host "`nGenerating realistic training data..." -ForegroundColor Yellow
Set-Location ml_data
python generate_realistic_data.py --output realistic_training_data.csv --samples 100
Set-Location ..

# Activate virtual environment
Write-Host "`nActivating virtual environment..." -ForegroundColor Yellow
Set-Location backend
& "venv\Scripts\Activate.ps1"

# Train model
Write-Host "`nTraining model (this may take a while)..." -ForegroundColor Yellow
Write-Host "Using realistic contract data..." -ForegroundColor Cyan
python -m app.ml.train --data ../ml_data/realistic_training_data.csv --output ./models/risk_classifier --epochs 5 --batch-size 16

Write-Host "`n✅ Model training complete!" -ForegroundColor Green
Write-Host "`nUpdate backend\.env and set ML_MODE=ml to use the trained model" -ForegroundColor Cyan

Set-Location ..

