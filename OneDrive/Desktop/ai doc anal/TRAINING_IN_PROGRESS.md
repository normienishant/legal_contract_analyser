# Model Training In Progress

## Current Status: Training Started

### What's Being Done:

1. **Improved Training Data Created**
   - 5000 samples from real legal contract patterns
   - 60% LOW risk (standard boilerplate)
   - 25% MEDIUM risk
   - 15% HIGH risk
   - Many more LOW risk boilerplate examples added

2. **Model Training**
   - Training on improved dataset
   - 5 epochs
   - Batch size: 16
   - This will take approximately 1-2 hours

3. **Improvements Made:**
   - Added 30+ more LOW risk boilerplate templates
   - Better classification logic for standard contract language
   - More variations of party identification clauses
   - Better balance in dataset

### Expected Results:

After training completes, the model should:
- Correctly identify standard boilerplate as LOW risk
- Better distinguish between LOW, MEDIUM, and HIGH risk clauses
- Handle your example clause correctly: "THIS AGREEMENT has been made..." → LOW

### Next Steps After Training:

1. Test the model with your example clause
2. Verify accuracy on standard boilerplate
3. If needed, fine-tune further

### Training Command:

```powershell
cd backend
.\venv\Scripts\Activate.ps1
python -m app.ml.train --data ../ml_data/improved_real_legal_data.csv --output ./models/risk_classifier --epochs 5 --batch-size 16
```

Training is running in the background. Check back in 1-2 hours!

