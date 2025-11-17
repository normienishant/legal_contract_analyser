# Setup Notes

## Important: Environment Configuration

Since `.env.example` could not be created automatically, please create a `.env` file in the `backend/` directory with the following content:

```env
# Backend Configuration
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
ENVIRONMENT=development

# Database
DATABASE_URL=sqlite:///./contract_analyzer.db

# ML Configuration
ML_MODE=rules
# Options: "ml" or "rules"
MODEL_PATH=./models/risk_classifier
USE_GPU=false

# Security
API_KEY=your_api_key_here
MAX_UPLOAD_SIZE_MB=10
ALLOWED_EXTENSIONS=pdf,docx,txt

# Hugging Face (optional, for model downloads)
# HF_TOKEN=your_huggingface_token_here

# Logging
LOG_LEVEL=INFO
```

**Note**: Start with `ML_MODE=rules` if you haven't trained the ML model yet. The system will use rule-based analysis as a fallback.

## Quick Test Commands

After setting up, test with these commands:

### 1. Start Backend
```bash
cd backend
python -m uvicorn app.main:app --reload
```

### 2. Start Frontend (in another terminal)
```bash
cd frontend
npm install
npm run dev
```

### 3. Test Upload
```bash
curl -F "file=@./ml_data/sample_contract.txt" http://localhost:8000/api/upload
```

Or using PowerShell (Windows):
```powershell
curl.exe -F "file=@./ml_data/sample_contract.txt" http://localhost:8000/api/upload
```

## First-Time Setup Checklist

- [ ] Create `.env` file in `backend/` directory
- [ ] Install Python dependencies: `pip install -r backend/requirements.txt`
- [ ] Install Node.js dependencies: `cd frontend && npm install`
- [ ] (Optional) Generate training data: `cd ml_data && python generate_sample_data.py`
- [ ] (Optional) Train ML model: `cd backend && python -m app.ml.train --data ../ml_data/training_data.csv`
- [ ] Test backend: `cd backend && pytest tests/ -v`
- [ ] Start services and test upload

## Docker Alternative

If you prefer Docker:

```bash
docker-compose up --build
```

This will start both backend and frontend services automatically.

