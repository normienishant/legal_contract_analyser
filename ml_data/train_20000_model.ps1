# PowerShell script to generate 20000 samples and train model

Write-Host "🚀 Starting 20000 Sample Model Training Pipeline" -ForegroundColor Green
Write-Host ""

# Step 1: Generate 20000 samples
Write-Host "Step 1: Generating 20000 training samples..." -ForegroundColor Cyan
python generate_20000_samples.py

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to generate samples" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Samples generated successfully" -ForegroundColor Green
Write-Host ""

# Step 2: Train model
Write-Host "Step 2: Training model with 20000 samples..." -ForegroundColor Cyan
Write-Host "This may take 30-60 minutes depending on your hardware..." -ForegroundColor Yellow
Write-Host ""

cd ..
python -m backend.app.ml.train `
    --data "ml_data/training_data_20000.csv" `
    --output "./backend/models/risk_classifier" `
    --epochs 3 `
    --batch-size 16 `
    --learning-rate 2e-5 `
    --test-split 0.2

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Training failed" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "✅ Model training completed!" -ForegroundColor Green
Write-Host "Model saved to: backend/models/risk_classifier" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Test the model with: python -m backend.app.ml.predict" -ForegroundColor White
Write-Host "2. Update backend to use new model" -ForegroundColor White

