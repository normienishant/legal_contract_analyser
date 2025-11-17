# 🚀 Training Status - 12,000 Sample Dataset

## Dataset Information

**File:** `ml_data/large_real_legal_dataset.csv`
**Total Samples:** 12,000
**Created:** 2025-11-16 14:33:06

### Distribution:
- **LOW:** 7,291 samples (60.8%)
- **MEDIUM:** 2,591 samples (21.6%)
- **HIGH:** 2,118 samples (17.6%)

## Training Status: 🟡 IN PROGRESS

**Command:**
```bash
cd backend
.\venv\Scripts\Activate.ps1
python -m app.ml.train --data ../ml_data/large_real_legal_dataset.csv --output ./models/risk_classifier --epochs 5 --batch-size 16
```

**Training Parameters:**
- Model: DistilBERT (distilbert-base-uncased)
- Epochs: 5
- Batch Size: 16
- Learning Rate: 2e-5
- Max Length: 512 tokens

**Expected Duration:** 45-90 minutes

## Progress Tracking

Check training progress:
```powershell
# Check latest checkpoint
Get-ChildItem backend\models\risk_classifier\checkpoint-*\trainer_state.json | Sort-Object LastWriteTime -Descending | Select-Object -First 1 | Get-Content | ConvertFrom-Json | Select-Object epoch, global_step

# Check active process
Get-Process python | Where-Object { $_.CPU -gt 100 }
```

## Expected Results

After training completes, you should see:
- High accuracy on HIGH risk clauses
- Better detection of unfair rental agreement terms
- Improved accuracy on Indian legal documents

## Next Steps

1. Wait for training to complete
2. Test with `rental_clauses.txt`
3. Verify accuracy improvements
4. Update ML_MODE to "ml" in settings

