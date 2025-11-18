# AI Contract Analyzer & Risk Detector

A complete production-ready application for analyzing contract documents and detecting potential risks using AI/ML and rule-based analysis.

## Features

- **Document Upload**: Support for PDF, DOCX, and TXT files
- **Text Extraction**: Automatic extraction and clause segmentation
- **Risk Analysis**: AI-powered and rule-based risk classification
- **Risk Scoring**: Clause-level and document-level risk scores
- **Mitigation Suggestions**: Actionable recommendations for risk reduction
- **Analysis History**: Track and review previous analyses
- **Modern UI**: Clean, responsive interface built with Next.js and Tailwind CSS

## Tech Stack

### Frontend
- Next.js 14 (App Router)
- TypeScript
- Tailwind CSS
- React 18

### Backend
- FastAPI (Python)
- SQLAlchemy (SQLite)
- PyMuPDF (PDF extraction)
- python-docx (DOCX extraction)

### ML/AI
- Hugging Face Transformers
- DistilBERT for risk classification
- Rule-based fallback analyzer

### Infrastructure
- Docker & Docker Compose
- GitHub Actions CI/CD
- SQLite database

## Project Structure

```
.
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── core/           # Configuration
│   │   ├── db/             # Database setup
│   │   ├── models/         # SQLAlchemy models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Business logic
│   │   └── ml/             # ML training & inference
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/               # Next.js frontend
│   ├── app/                # App router pages
│   ├── components/         # React components
│   ├── lib/                # API client
│   └── package.json
├── ml_data/                # Training data
├── tests/                  # Backend tests
├── scripts/                # Utility scripts
├── docker-compose.yml
└── README.md
```

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker & Docker Compose (optional)

### Option 1: Docker Compose (Recommended)

1. Clone the repository:
```bash
git clone <repo-url>
cd ai-doc-anal
```

2. Start services:
```bash
docker-compose up --build
```

3. Access the application:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Option 2: Local Development

#### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Start backend server:
```bash
python -m uvicorn app.main:app --reload
```

Backend will run on http://localhost:8000

#### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start development server:
```bash
npm run dev
```

Frontend will run on http://localhost:3000

## Training ML Model

1. Generate sample training data:
```bash
cd ml_data
python generate_sample_data.py --output training_data.csv --samples 50
```

2. Train the model:
```bash
cd backend
python -m app.ml.train --data ../ml_data/training_data.csv --output ./models/risk_classifier --epochs 3
```

3. Update configuration:
Set `ML_MODE=ml` in your `.env` file (or use default).

## Configuration

Create a `.env` file in the backend directory (see `.env.example`):

```env
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
DATABASE_URL=sqlite:///./contract_analyzer.db
ML_MODE=ml  # or "rules" for rule-based only
MODEL_PATH=./models/risk_classifier
MAX_UPLOAD_SIZE_MB=10
ALLOWED_EXTENSIONS=pdf,docx,txt
```

## API Endpoints

- `GET /health` - Health check
- `POST /api/upload` - Upload document
- `POST /api/extract` - Extract text and segment clauses
- `POST /api/analyze` - Analyze document for risks
- `GET /api/history` - Get analysis history
- `GET /api/history/{id}` - Get specific analysis

See http://localhost:8000/docs for interactive API documentation.

## Testing

### Backend Tests

```bash
cd backend
pytest tests/ -v
```

### Frontend Linting

```bash
cd frontend
npm run lint
```

## Usage

1. **Upload Document**: Navigate to `/upload` and select a PDF, DOCX, or TXT file
2. **Analysis**: The system automatically extracts text, segments clauses, and analyzes risks
3. **Review Results**: View risk scores, explanations, and mitigation suggestions
4. **History**: Access previous analyses from the history page

## Risk Scoring

See `EXPLAINER.md` for detailed information about the risk scoring algorithm.

## Security Considerations

- File upload validation (type and size)
- Path traversal prevention
- Input sanitization
- API key authentication (configure in production)

## Development

### Running Tests

```bash
# Backend
cd backend
pytest tests/ -v

# Frontend
cd frontend
npm run lint
```

### Building for Production

```bash
# Backend
cd backend
docker build -t contract-analyzer-backend:latest .

# Frontend
cd frontend
npm run build
docker build -t contract-analyzer-frontend:latest .
```

## Troubleshooting

### Backend won't start
- Check Python version (3.11+)
- Ensure all dependencies are installed
- Check database file permissions

### Frontend build errors
- Clear `node_modules` and reinstall: `rm -rf node_modules && npm install`
- Check Node.js version (18+)

### ML model not loading
- Ensure model is trained and saved to `./models/risk_classifier`
- Check `ML_MODE` setting (use "rules" for fallback)
- Verify model files exist

## License

MIT License - see LICENSE file for details

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## Support

For issues and questions, please open an issue on GitHub.

