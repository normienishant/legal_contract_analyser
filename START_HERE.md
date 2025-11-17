# 🚀 START HERE - Quick Setup Guide

## Step 1: Setup (Ek baar chalao)

PowerShell mein yeh command chalao:

```powershell
.\setup.ps1
```

Yeh automatically:
- Python virtual environment banayega
- Sab dependencies install karega
- Frontend dependencies install karega
- .env file banayega

## Step 2: Backend Start Karo

Nayi PowerShell window mein:

```powershell
.\start-backend.ps1
```

Ya manually:
```powershell
cd backend
.\venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload
```

Backend chalega: http://localhost:8000

## Step 3: Frontend Start Karo

Ek aur nayi PowerShell window mein:

```powershell
.\start-frontend.ps1
```

Ya manually:
```powershell
cd frontend
npm run dev
```

Frontend chalega: http://localhost:3000

## Step 4: ML Model Train Karo (Optional)

Agar real-world data pe model train karna hai:

```powershell
.\train-model.ps1
```

Yeh realistic contract data generate karega aur model train karega.

**Note**: Training mein 5-10 minutes lag sakte hain. Pehle rule-based mode use karo (default).

## Step 5: Test Karo

1. Browser mein jao: http://localhost:3000
2. "Upload Document" pe click karo
3. `ml_data/sample_contract.txt` upload karo
4. Analysis dekho!

## Features

✅ **Professional UI** - Modern, gradient design with animations
✅ **Real-world Training Data** - Realistic contract clauses
✅ **Export Reports** - JSON format mein download
✅ **Risk Visualization** - Charts aur color-coded badges
✅ **Smart Analysis** - ML + Rule-based fallback

## Troubleshooting

### Agar pip install fail ho:
```powershell
python -m pip install --upgrade pip
cd backend
python -m pip install -r requirements.txt
```

### Agar npm install fail ho:
```powershell
cd frontend
npm cache clean --force
npm install
```

### Backend start nahi ho raha:
- Check karo virtual environment activate hua ya nahi
- `backend\.env` file hai ya nahi

## Next Steps

1. ✅ Setup complete
2. ✅ Backend running
3. ✅ Frontend running
4. 🎉 Upload document aur test karo!

**Sab kuch ready hai! Ab bas upload karo aur analyze dekho! 🚀**

