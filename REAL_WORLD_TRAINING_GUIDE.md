# Real-World Data Training Guide 🎯

## Current Status

**Abhi kya chal raha hai:**
- ✅ **Rule-based analyzer** - Basic keywords pe kaam karta hai
- ✅ **Synthetic training data** - Testing ke liye
- ⚠️ **ML model** - Abhi trained nahi hai real data pe

## Real-World Data Pe Kaam Karne Ke Liye

### Option 1: Rule-Based (Abhi Kaam Kar Raha Hai) ✅

**Pros:**
- ✅ Abhi se kaam karta hai
- ✅ Fast aur reliable
- ✅ No training needed

**Cons:**
- ⚠️ Limited accuracy
- ⚠️ Only keyword-based detection
- ⚠️ Complex clauses miss ho sakte hain

**Best for:** Quick testing, basic contracts

### Option 2: ML Model (Better Accuracy) 🚀

**Pros:**
- ✅ Much better accuracy
- ✅ Context understanding
- ✅ Complex patterns detect karta hai
- ✅ Real-world contracts pe trained

**Cons:**
- ⚠️ Training time lagta hai (5-10 min)
- ⚠️ Real data chahiye

**Best for:** Production use, real contracts

## Real-World Data Se Model Train Karne Ka Process

### Step 1: Real Contracts Collect Karo

1. **Actual contracts collect karo:**
   - Service agreements
   - Employment contracts
   - Vendor agreements
   - NDA documents
   - etc.

2. **Clauses extract karo:**
   - Har contract se individual clauses nikaalo
   - Manual ya automated segmentation

### Step 2: Data Label Karo

**CSV format mein data prepare karo:**

```csv
clause_text,label,explanation
"The Service Provider shall indemnify...",HIGH,"Contains unlimited indemnification"
"Either party may terminate...",MEDIUM,"Standard termination clause"
"This Agreement shall commence...",LOW,"Standard commencement clause"
```

**Required columns:**
- `clause_text` - The actual clause text
- `label` - HIGH, MEDIUM, or LOW
- `explanation` (optional) - Why this label

### Step 3: Training Data Prepare Karo

**Minimum data needed:**
- **HIGH risk:** At least 50-100 clauses
- **MEDIUM risk:** At least 50-100 clauses  
- **LOW risk:** At least 50-100 clauses

**Better results ke liye:**
- **HIGH risk:** 200+ clauses
- **MEDIUM risk:** 200+ clauses
- **LOW risk:** 200+ clauses

### Step 4: Model Train Karo

```powershell
# Real data se train karo
cd backend
.\venv\Scripts\Activate.ps1
python -m app.ml.train --data ../ml_data/real_world_data.csv --output ./models/risk_classifier --epochs 5
```

### Step 5: Model Use Karo

`.env` file mein update karo:
```env
ML_MODE=ml
MODEL_PATH=./models/risk_classifier
```

Backend restart karo - ab ML model use hoga!

## Quick Start: Real Data Se Training

### Method 1: Manual Data Collection

1. **Contracts collect karo** (PDF/DOCX/TXT)
2. **Clauses manually extract karo**
3. **Labels assign karo** (HIGH/MEDIUM/LOW)
4. **CSV file banayo:**

```python
import pandas as pd

data = [
    {"clause_text": "Your clause 1", "label": "HIGH"},
    {"clause_text": "Your clause 2", "label": "MEDIUM"},
    # ... more clauses
]

df = pd.DataFrame(data)
df.to_csv("real_world_data.csv", index=False)
```

### Method 2: Use Existing Contracts

Agar aapke paas already analyzed contracts hain:

1. **Upload contracts** to the system
2. **Manual review** karke labels assign karo
3. **Export data** from database
4. **CSV format** mein convert karo
5. **Train model**

## Data Quality Tips

### ✅ Good Data:
- Clear, complete clauses
- Accurate labels
- Diverse contract types
- Balanced distribution (equal HIGH/MEDIUM/LOW)

### ❌ Bad Data:
- Incomplete clauses
- Wrong labels
- Too much of one type
- Very short clauses (< 20 chars)

## Expected Results

### Rule-Based (Current):
- Accuracy: ~60-70%
- Good for: Basic detection
- Fast: < 1 second

### ML Model (After Training):
- Accuracy: ~85-95% (real data pe trained)
- Good for: Production use
- Fast: 1-2 seconds per document

## Testing Real-World Contracts

### Test Process:

1. **Upload real contract**
2. **Check analysis results**
3. **Compare with manual review**
4. **If wrong, add to training data**
5. **Re-train model**

### Continuous Improvement:

- **More data = Better model**
- **Regular re-training** recommended
- **Domain-specific training** for better results

## Example: Real Data CSV

```csv
clause_text,label
"The Service Provider shall indemnify, defend, and hold harmless the Client from any and all claims, damages, losses, liabilities, costs, and expenses arising out of or relating to the Services, without limitation.",HIGH
"Either party may terminate this Agreement upon 60 days written notice to the other party in the event of a material breach that remains uncured after such notice period.",MEDIUM
"This Agreement shall commence on the Effective Date and continue until terminated in accordance with its terms.",LOW
```

## Quick Commands

### Generate Sample Data (Testing):
```powershell
cd ml_data
python generate_realistic_data.py --output training_data.csv --samples 100
```

### Train on Real Data:
```powershell
cd backend
.\venv\Scripts\Activate.ps1
python -m app.ml.train --data ../ml_data/real_world_data.csv --output ./models/risk_classifier --epochs 5
```

### Switch to ML Mode:
```env
# backend/.env
ML_MODE=ml
```

## Summary

**Abhi:**
- ✅ Rule-based analyzer kaam kar raha hai
- ✅ Basic contracts analyze kar sakta hai
- ⚠️ Limited accuracy

**Real-world data pe:**
- 🚀 ML model train karo
- 🚀 Much better accuracy
- 🚀 Production-ready

**Recommendation:**
1. **Pehle rule-based se test karo**
2. **Real contracts collect karo**
3. **ML model train karo**
4. **Production mein use karo**

Real-world data se training karne ke liye sab ready hai! Bas data collect karo aur train karo! 🎯

