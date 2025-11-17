# Quick script to check training status
Write-Host "=== ML MODEL TRAINING STATUS ===" -ForegroundColor Cyan
Write-Host ""

# Check if training process is running
$procs = Get-Process python -ErrorAction SilentlyContinue
if ($procs) {
    Write-Host "✅ Training Process: RUNNING" -ForegroundColor Green
    $procs | ForEach-Object {
        Write-Host "   PID: $($_.Id), CPU Time: $([math]::Round($_.CPU, 2))s" -ForegroundColor Gray
    }
} else {
    Write-Host "❌ Training Process: NOT RUNNING" -ForegroundColor Red
}

Write-Host ""

# Check latest checkpoint
$checkpoints = Get-ChildItem -Path "backend\models\risk_classifier" -Directory -Filter "checkpoint-*" -ErrorAction SilentlyContinue
if ($checkpoints) {
    $latest = $checkpoints | Sort-Object LastWriteTime -Descending | Select-Object -First 1
    Write-Host "Latest Checkpoint: $($latest.Name)" -ForegroundColor Yellow
    Write-Host "Last Updated: $($latest.LastWriteTime)" -ForegroundColor Gray
    
    # Try to read training state
    $stateFile = Join-Path $latest.FullName "trainer_state.json"
    if (Test-Path $stateFile) {
        try {
            $state = Get-Content $stateFile | ConvertFrom-Json
            Write-Host ""
            Write-Host "Training Progress:" -ForegroundColor Cyan
            Write-Host "  Epoch: $($state.epoch) / 5.0" -ForegroundColor White
            Write-Host "  Global Step: $($state.global_step)" -ForegroundColor White
            $progress = [math]::Round(($state.epoch / 5.0) * 100, 1)
            Write-Host "  Progress: $progress%" -ForegroundColor Green
            
            if ($state.epoch -ge 5.0) {
                Write-Host ""
                Write-Host "🎉 TRAINING COMPLETED!" -ForegroundColor Green
            }
        } catch {
            Write-Host "  (Could not read training state)" -ForegroundColor Gray
        }
    }
} else {
    Write-Host "No checkpoints found yet" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Dataset: improved_real_legal_data.csv (5000 samples)" -ForegroundColor Cyan
Write-Host "Expected Total Time: 2-3 hours" -ForegroundColor Yellow

