# Train Production Model with Comprehensive Data
Write-Host "🚀 Training Production Model for 95%+ Accuracy..." -ForegroundColor Green
Write-Host ""

# Step 1: Generate comprehensive training data
Write-Host "Step 1: Generating comprehensive training data..." -ForegroundColor Yellow
Set-Location ml_data
python generate_comprehensive_data.py --output comprehensive_training_data.csv --samples 500
Set-Location ..

# Step 2: Activate virtual environment
Write-Host "`nStep 2: Activating virtual environment..." -ForegroundColor Yellow
Set-Location backend
& "venv\Scripts\Activate.ps1"

# Step 3: Train model with optimized settings
Write-Host "`nStep 3: Training ML model (this will take 10-15 minutes)..." -ForegroundColor Yellow
Write-Host "Using comprehensive dataset with optimized hyperparameters..." -ForegroundColor Cyan
Write-Host ""

python -m app.ml.train `
    --data ../ml_data/comprehensive_training_data.csv `
    --output ./models/risk_classifier `
    --epochs 5 `
    --batch-size 16 `
    --learning-rate 2e-5

# Step 4: Check if model was created
Write-Host "`nStep 4: Verifying model..." -ForegroundColor Yellow
if (Test-Path "models\risk_classifier\config.json") {
    Write-Host "✅ Model trained successfully!" -ForegroundColor Green
    Write-Host "`nStep 5: Update configuration..." -ForegroundColor Yellow
    
    # Update .env file
    $envContent = Get-Content ".env" -Raw
    $envContent = $envContent -replace "ML_MODE=rules", "ML_MODE=ml"
    $envContent | Out-File -FilePath ".env" -Encoding utf8 -NoNewline
    
    Write-Host "✅ Configuration updated to use ML model" -ForegroundColor Green
    Write-Host "`n🎉 Training Complete!" -ForegroundColor Green
    Write-Host "`nNext steps:" -ForegroundColor Cyan
    Write-Host "1. Restart backend: python -m uvicorn app.main:app --reload" -ForegroundColor White
    Write-Host "2. Test with real contracts" -ForegroundColor White
    Write-Host "3. Check accuracy in backend logs" -ForegroundColor White
} else {
    Write-Host "❌ Model training failed. Check errors above." -ForegroundColor Red
}

Set-Location ..

