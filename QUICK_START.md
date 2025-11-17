# Quick Start Guide

## Test Commands

After setting up the project, run these commands to test the system:

### 1. Start Backend

```bash
cd backend
python -m uvicorn app.main:app --reload
```

Backend will be available at: http://localhost:8000

### 2. Start Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend will be available at: http://localhost:3000

### 3. Test Upload Endpoint

```bash
curl -F "file=@./ml_data/sample_contract.txt" http://localhost:8000/api/upload
```

Or using PowerShell (Windows):
```powershell
curl.exe -F "file=@./ml_data/sample_contract.txt" http://localhost:8000/api/upload
```

### 4. Full Pipeline Test

```bash
# Upload file
UPLOAD_RESPONSE=$(curl -F "file=@./ml_data/sample_contract.txt" http://localhost:8000/api/upload)
FILE_ID=$(echo $UPLOAD_RESPONSE | jq -r '.file_id')

# Extract text
curl "http://localhost:8000/api/extract?file_id=$FILE_ID"

# Analyze document
curl -X POST "http://localhost:8000/api/analyze?file_id=$FILE_ID"
```

## Docker Compose Quick Start

```bash
# Start all services
docker-compose up --build

# Or use the script
bash scripts/run_local.sh
```

## Generate Training Data

```bash
cd ml_data
python generate_sample_data.py --output training_data.csv --samples 50
```

## Train ML Model

```bash
cd backend
python -m app.ml.train --data ../ml_data/training_data.csv --output ./models/risk_classifier --epochs 3
```

## Run Tests

```bash
cd backend
pytest tests/ -v
```

