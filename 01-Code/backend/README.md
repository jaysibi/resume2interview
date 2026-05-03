# Resume Tailor Backend

This is the FastAPI backend for the Resume Tailor MVP. It provides endpoints for resume and job description upload, and is structured for future AI/ML integration.

## Features

### Core Endpoints
- ✅ **Resume Upload & Parsing** - PDF/DOCX support with AI-powered skill extraction
- ✅ **Job Description Upload & Parsing** - Extract requirements and keywords
- ✅ **Resume Retrieval** - GET /resume/{id} to fetch stored resumes
- ✅ **JD Retrieval** - GET /jd/{id} to fetch stored job descriptions
- ✅ **Gap Analysis** - POST /gap-analysis/ for resume vs JD comparison (65% avg match score)
- ✅ **ATS Scoring** - POST /ats-score/ for applicant tracking system compatibility analysis

### Technical Features
- OpenAI GPT-4o integration for intelligent analysis
- PostgreSQL database with connection pooling
- Comprehensive error handling and validation
- Rate limiting and CORS configuration
- Alembic database migrations

## Getting Started

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Server

**For Production:**
```bash
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --timeout-keep-alive 60
```

**For Development (Manual Restarts):**
```bash
python -m uvicorn main:app --port 8000 --timeout-keep-alive 60
```

**⚠️ IMPORTANT:** Do NOT use `--reload` flag with this application!
- The `--reload` flag causes issues with OpenAI client initialization on Windows
- AI endpoints (Gap Analysis, ATS Scoring) will fail with 500 errors when `--reload` is enabled
- Use manual server restarts during development instead

**Alternative for Development (if needed):**
```bash
# Run on alternative port for testing
python -m uvicorn main:app --port 8001 --timeout-keep-alive 60
```

### 3. Access the API
- API Documentation: [http://localhost:8000/docs](http://localhost:8000/docs)
- Health Check: [http://localhost:8000/](http://localhost:8000/)
- Alternative API: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Project Structure
```
backend/
├── main.py              # FastAPI app and all API endpoints
├── db.py                # Database configuration and session management
├── models.py            # SQLAlchemy ORM models (Resume, JobDescription)
├── crud.py              # Database CRUD operations
├── ai_service.py        # OpenAI integration and AI analysis logic
├── ai_models.py         # Pydantic models for AI responses
├── prompts.py           # LLM prompt templates
├── parsers/             # Resume and JD parsing modules
│   ├── resume_parser.py
│   └── jd_parser.py
├── migrations/          # Alembic database migrations
├── test_e2e.py          # End-to-end API tests
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (API keys)
└── README.md            # This file
```

## Testing

### Run End-to-End Tests
```bash
python test_e2e.py
```

### Test Individual Endpoints
```python
import requests

# Health check
response = requests.get('http://localhost:8000/')
print(response.json())

# Gap analysis
response = requests.post(
    'http://localhost:8000/gap-analysis/',
    params={'resume_id': 5, 'jd_id': 4}
)
print(response.json())
```

## Configuration

### Environment Variables (.env)
```bash
# Required
OPENAI_API_KEY=your-api-key-here

# Optional (defaults shown)
POSTGRES_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/resumetailor
CORS_ORIGINS=*
```

## Troubleshooting

### Issue: 500 Error on AI Endpoints
**Solution:** Ensure you're NOT using the `--reload` flag. Restart the server without it.

### Issue: Database Connection Error
**Solution:** Verify PostgreSQL is running and the connection string in `.env` is correct.

### Issue: OpenAI API Errors
**Solution:** Check your API key in `.env` and verify you have sufficient credits.

## Production Deployment

**Recommended Command:**
```bash
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4 --timeout-keep-alive 60
```

**Production Checklist:**
- ✅ Remove or comment out rate limiter in development
- ✅ Set appropriate CORS_ORIGINS (not `*`)
- ✅ Use environment variables for all secrets
- ✅ Enable HTTPS/TLS
- ✅ Set up proper logging and monitoring
- ✅ Configure database connection pooling
- ✅ Implement backup and disaster recovery
