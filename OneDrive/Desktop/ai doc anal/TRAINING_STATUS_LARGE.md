# 🚀 Large Real Legal Document Training Status

## Dataset Created ✅

**File:** `ml_data/large_real_legal_dataset.csv`
**Total Samples:** 12,000
**Date:** 2025-01-16

### Dataset Composition:

- **LOW Risk:** 7,291 samples (60.8%)
- **MEDIUM Risk:** 2,591 samples (21.6%)
- **HIGH Risk:** 2,118 samples (17.6%)

### Key Features:

1. **More Balanced Distribution:**
   - More MEDIUM and HIGH risk samples for better accuracy
   - Better representation of risky clauses

2. **Comprehensive Coverage:**
   - Indian legal documents (rental, employment, service agreements)
   - International legal documents
   - Real-world contract patterns

3. **HIGH Risk Clauses Include:**
   - Unilateral amendment rights
   - Entry without notice
   - Indemnification including own negligence
   - Distant/exclusive jurisdiction
   - Short termination notices
   - Automatic renewal
   - Excessive penalties
   - Non-refundable fees
   - Unlimited liability
   - Waiver of rights

4. **MEDIUM Risk Clauses Include:**
   - Security deposit deductions
   - Late payment fees
   - Subletting restrictions
   - Rent escalation
   - Termination with liability
   - Arbitration clauses
   - Confidentiality
   - Liability limits

5. **LOW Risk Clauses Include:**
   - Standard boilerplate
   - Agreement headers
   - Recitals
   - Standard payment terms
   - Maintenance clauses
   - Utilities
   - Insurance requirements
   - Force majeure

## Training Status: 🟡 IN PROGRESS

**Command:**
```bash
cd backend
.\venv\Scripts\Activate.ps1
python -m app.ml.train --data ../ml_data/large_real_legal_dataset.csv --output ./models/risk_classifier --epochs 5 --batch-size 16
```

**Expected Duration:** 45-90 minutes (depending on hardware)

**Training Parameters:**
- Model: DistilBERT (distilbert-base-uncased)
- Epochs: 5
- Batch Size: 16
- Learning Rate: 2e-5
- Max Length: 512 tokens
- Optimizer: AdamW

## Expected Improvements:

1. ✅ **Better Accuracy on HIGH Risk Clauses:**
   - Unilateral amendment detection
   - Entry without notice detection
   - Indemnification including own negligence
   - Distant jurisdiction detection

2. ✅ **Better Accuracy on MEDIUM Risk Clauses:**
   - Security deposit clauses
   - Late payment fees
   - Subletting restrictions
   - Rent escalation

3. ✅ **Better Overall Performance:**
   - More balanced training data
   - Better generalization
   - Improved accuracy on rental agreements

## Adding Real Documents:

To add your own PDF, DOCX, or TXT files:

1. **Copy files to:** `ml_data/real_documents/`
2. **Supported formats:** .pdf, .docx, .doc, .txt
3. **Re-run dataset creation:**
   ```bash
   cd ml_data
   python create_real_document_dataset.py --samples 12000 --output large_real_legal_dataset.csv
   ```

The script will:
- Extract text from PDF/DOCX files
- Segment into clauses
- Classify by risk level
- Add to training dataset

## Next Steps:

1. ✅ Wait for training to complete
2. ✅ Test the model with `rental_clauses.txt`
3. ✅ Verify accuracy improvements
4. ✅ Update ML_MODE to "ml" in settings

## Check Training Progress:

```powershell
# Check if training is running
Get-Process python | Where-Object {$_.CommandLine -like "*train*"}

# Check for model files
Get-ChildItem backend\models\risk_classifier\ -Recurse

# Check training logs (if available)
Get-Content backend\models\training.log -Tail 20 -ErrorAction SilentlyContinue
```

## Model Location:

After training completes, the model will be saved to:
```
backend/models/risk_classifier/
```

Files:
- `config.json` - Model configuration
- `pytorch_model.bin` or `model.safetensors` - Model weights
- `tokenizer_config.json` - Tokenizer configuration
- `vocab.txt` - Vocabulary
- `label_map.json` - Label mappings

