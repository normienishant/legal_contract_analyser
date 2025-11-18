# Check ML Model Training Progress
Write-Host "=== ML MODEL TRAINING PROGRESS ===" -ForegroundColor Green
Write-Host ""

$checkpointDir = "backend\models\risk_classifier"
$datasetFile = "ml_data\large_real_legal_dataset.csv"

# Check dataset
if (Test-Path $datasetFile) {
    $dataset = Import-Csv $datasetFile
    Write-Host "Dataset: large_real_legal_dataset.csv" -ForegroundColor Cyan
    Write-Host "  Total Samples: $($dataset.Count)" -ForegroundColor White
    $low = ($dataset | Where-Object { $_.label -eq "LOW" }).Count
    $medium = ($dataset | Where-Object { $_.label -eq "MEDIUM" }).Count
    $high = ($dataset | Where-Object { $_.label -eq "HIGH" }).Count
    Write-Host "  LOW: $low | MEDIUM: $medium | HIGH: $high" -ForegroundColor White
    Write-Host ""
}

# Check latest checkpoint
$checkpoints = Get-ChildItem "$checkpointDir\checkpoint-*" -Directory -ErrorAction SilentlyContinue | Sort-Object { [int]($_.Name -replace 'checkpoint-', '') } -Descending

if ($checkpoints) {
    $latest = $checkpoints[0]
    $stateFile = Join-Path $latest.FullName "trainer_state.json"
    
    if (Test-Path $stateFile) {
        $state = Get-Content $stateFile -Raw | ConvertFrom-Json
        $progress = ($state.epoch / $state.num_train_epochs) * 100
        
        Write-Host "Latest Checkpoint: $($latest.Name)" -ForegroundColor Cyan
        Write-Host "  Epoch: $($state.epoch) / $($state.num_train_epochs)" -ForegroundColor White
        Write-Host "  Progress: $([math]::Round($progress, 1))%" -ForegroundColor $(if ($progress -eq 100) { "Green" } else { "Yellow" })
        Write-Host "  Global Step: $($state.global_step) / $($state.max_steps)" -ForegroundColor White
        Write-Host "  Last Modified: $($latest.LastWriteTime.ToString('yyyy-MM-dd HH:mm:ss'))" -ForegroundColor White
        
        # Get latest evaluation
        $finalEval = $state.log_history | Where-Object { $_.eval_accuracy } | Select-Object -Last 1
        if ($finalEval) {
            Write-Host ""
            Write-Host "Latest Evaluation Metrics:" -ForegroundColor Cyan
            Write-Host "  Accuracy: $([math]::Round($finalEval.eval_accuracy * 100, 2))%" -ForegroundColor Green
            Write-Host "  F1-Score: $([math]::Round($finalEval.eval_f1, 4))" -ForegroundColor Green
            Write-Host "  Precision: $([math]::Round($finalEval.eval_precision * 100, 2))%" -ForegroundColor Green
            Write-Host "  Recall: $([math]::Round($finalEval.eval_recall * 100, 2))%" -ForegroundColor Green
        }
        
        Write-Host ""
        if ($state.epoch -eq $state.num_train_epochs) {
            Write-Host "Status: COMPLETE" -ForegroundColor Green
            Write-Host "Model is ready to use!" -ForegroundColor Green
        } else {
            Write-Host "Status: IN PROGRESS" -ForegroundColor Yellow
            $remaining = $state.num_train_epochs - $state.epoch
            Write-Host "  Remaining Epochs: $remaining" -ForegroundColor Yellow
            Write-Host "  Estimated remaining time: ~$($remaining * 15) minutes" -ForegroundColor Yellow
        }
    }
} else {
    Write-Host "No checkpoints found. Training may not have started yet." -ForegroundColor Yellow
}

# Check for active training process
Write-Host ""
$process = Get-Process python -ErrorAction SilentlyContinue | Where-Object { $_.CPU -gt 50 } | Sort-Object CPU -Descending | Select-Object -First 1
if ($process) {
    Write-Host "Active Training Process:" -ForegroundColor Green
    Write-Host "  PID: $($process.Id)" -ForegroundColor White
    Write-Host "  CPU Time: $([math]::Round($process.CPU / 60, 1)) minutes" -ForegroundColor Cyan
    Write-Host "  Memory: $([math]::Round($process.WorkingSet / 1MB, 1)) MB" -ForegroundColor Cyan
} else {
    Write-Host "No active training process found." -ForegroundColor Yellow
}

Write-Host ""

