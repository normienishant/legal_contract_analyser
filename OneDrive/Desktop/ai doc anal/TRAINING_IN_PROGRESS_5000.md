# 🚀 ML Model Training - 5000 Dataset (IN PROGRESS)

## Training Started

### Dataset Information:
- **File:** `ml_data/improved_real_legal_data.csv`
- **Total Samples:** 5000
- **Distribution:**
  - LOW Risk: 4568 samples (91.4%)
  - MEDIUM Risk: 338 samples (6.8%)
  - HIGH Risk: 94 samples (1.9%)

### Training Configuration:
- **Base Model:** distilbert-base-uncased
- **Epochs:** 5
- **Batch Size:** 16
- **Learning Rate:** 2e-5
- **Output:** `backend/models/risk_classifier/`

### Estimated Time:
- **Total Time:** ~2-3 hours
- **Per Epoch:** ~30-40 minutes
- **Total Steps:** ~1560 steps (5000 samples ÷ 16 batch ÷ 0.8 train split × 5 epochs)

### Training Progress:
Training is running in the background. Check progress by:

1. **Check latest checkpoint:**
   ```powershell
   Get-ChildItem backend\models\risk_classifier\checkpoint-* | Sort-Object LastWriteTime -Descending | Select-Object -First 1
   ```

2. **Check training state:**
   ```powershell
   Get-Content backend\models\risk_classifier\checkpoint-XXX\trainer_state.json | ConvertFrom-Json | Select-Object epoch, global_step
   ```

3. **Check if process is running:**
   ```powershell
   Get-Process python -ErrorAction SilentlyContinue
   ```

### What to Expect:

After training completes, you'll have:
- ✅ Model trained on 5000 real-world contract samples
- ✅ Better accuracy on standard boilerplate clauses
- ✅ Improved LOW risk detection
- ✅ Better distinction between LOW, MEDIUM, and HIGH risk

### Training Command Used:

```powershell
cd backend
.\venv\Scripts\Activate.ps1
python -m app.ml.train --data ../ml_data/improved_real_legal_data.csv --output ./models/risk_classifier --epochs 5 --batch-size 16
```

### Notes:

- Training is running in background
- Model checkpoints are saved after each epoch
- Final model will be saved to `backend/models/risk_classifier/`
- Old checkpoints will remain for reference
- Training can be monitored by checking checkpoint timestamps

---

**Status:** 🟢 TRAINING IN PROGRESS

**Started:** $(Get-Date)

**Expected Completion:** ~2-3 hours from start time

