# Resume Tailor Backend - V2

FastAPI backend for Resume Tailor with user-centric application tracking, job URL scraping, and AI-powered resume analysis.

## ✨ What's New in V2

### User-Centric Features
- 🎯 **Multi-User Support** - Track applications per user with email-based identification
- 📊 **Application Dashboard** - Centralized view of all job applications with status tracking
- 🔗 **Job URL Fetching** - Automatically scrape job descriptions from LinkedIn, Indeed, Naukri, Monster, Glassdoor
- 📝 **Enhanced Metadata** - Store job titles, company names, and job URLs with applications

### New V2 Endpoints
- ✅ **POST /v2/fetch-jd-from-url/** - Fetch job description from URL
- ✅ **GET /v2/applications/** - List all applications for a user (with pagination)
- ✅ **GET /v2/applications/{id}/** - Get detailed application view with analyses

### Enhanced Existing Endpoints
- ✅ **POST /upload-resume/** - Now accepts optional `user_email` parameter
- ✅ **POST /upload-jd/** - Now accepts `user_email`, `job_url`, `title`, `company` parameters
- ✅ **POST /gap-analysis/** - Now can create application records with `create_application=true`

### V1 Compatibility
All V1 workflows remain fully functional. Endpoints without user_email automatically use the default user.

## Features

### Core Endpoints (V1 + V2)
- ✅ **Resume Upload & Parsing** - PDF/DOCX support with AI-powered skill extraction (GPT-4o-mini)
- ✅ **Job Description Upload & Parsing** - Extract requirements and keywords with AI
- ✅ **Job URL Scraping** - Fetch JD directly from job posting URLs (V2)
- ✅ **Gap Analysis** - AI-powered resume vs JD comparison with match scoring
- ✅ **ATS Scoring** - Applicant tracking system compatibility analysis
- ✅ **Application Tracking** - Complete application history with analytics (V2)

### Technical Features
- OpenAI GPT-4o-mini integration for intelligent analysis
- PostgreSQL database with V2 schema (7 tables with relationships)
- User-centric data architecture with cascade deletes
- Comprehensive error handling and validation
- Rate limiting support (currently disabled for development)
- CORS configuration for frontend integration
- Alembic database migrations with V2 schema

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

### 4. Run Database Migration (First Time)
```bash
# Migrate to V2 schema
python migrations/v2_001_migrate_to_v2_schema.py

# Verify schema
python verify_v2_schema.py
```

## Quick Start - V2 Workflow

### Python Example
```python
import requests

BASE_URL = "http://localhost:8000"
USER_EMAIL = "user@example.com"

# 1. Upload Resume
with open("resume.pdf", "rb") as f:
    resume_response = requests.post(
        f"{BASE_URL}/upload-resume/",
        files={"file": f},
        data={"user_email": USER_EMAIL}
    )
    resume_id = resume_response.json()["id"]

# 2. Fetch JD from URL
jd_response = requests.post(
    f"{BASE_URL}/v2/fetch-jd-from-url/",
    json={"job_url": "https://www.linkedin.com/jobs/view/123456"}
)
jd_data = jd_response.json()

# 3. Upload JD with fetched data
jd_upload = requests.post(
    f"{BASE_URL}/upload-jd/",
    files={"file": open("temp_jd.txt", "wb").write(jd_data["raw_text"].encode())},
    data={
        "user_email": USER_EMAIL,
        "job_url": "https://www.linkedin.com/jobs/view/123456",
        "title": jd_data["title"],
        "company": jd_data["company"]
    }
)
jd_id = jd_upload.json()["id"]

# 4. Gap Analysis with Application Creation
gap_response = requests.post(
    f"{BASE_URL}/gap-analysis/",
    params={
        "resume_id": resume_id,
        "jd_id": jd_id,
        "user_email": USER_EMAIL,
        "create_application": "true"
    }
)
app_id = gap_response.json()["application_id"]
print(f"Application created: {app_id}")
print(f"Match score: {gap_response.json()['match_score']}%")

# 5. View All Applications
apps_response = requests.get(
    f"{BASE_URL}/v2/applications/",
    params={"user_email": USER_EMAIL}
)
print(f"Total applications: {apps_response.json()['total']}")

# 6. View Application Details
detail_response = requests.get(f"{BASE_URL}/v2/applications/{app_id}/")
print(detail_response.json())
```

## Documentation

- 📘 **[API Documentation](API_DOCUMENTATION_V2.md)** - Complete V2 API reference
- 📋 **[Validation Guide](DATA_VALIDATION_GUIDE.md)** - Data validation and testing procedures
- 🤖 **[AI Features Guide](AI_FEATURES_GUIDE.md)** - OpenAI integration and prompts
- ✅ **[Validation Results](VALIDATION_RESULTS.md)** - Test results and metrics

## Project Structure
```
backend/
├── main.py                      # FastAPI app with all V1 + V2 endpoints
├── db.py                        # Database configuration and session management
├── models_v2.py                 # V2 SQLAlchemy ORM models (7 tables)
├── crud_v2.py                   # V2 database CRUD operations
├── job_scraper.py               # Web scraping for job URLs (V2)
├── ai_service.py                # OpenAI GPT-4o-mini integration
├── ai_models.py                 # Pydantic models for AI responses
├── prompts.py                   # LLM prompt templates
├── parsers/                     # Resume and JD parsing modules
│   ├── resume_parser.py         # PDF/DOCX resume parsing
│   └── jd_parser.py             # PDF/DOCX JD parsing
├── migrations/                  # Alembic database migrations
│   └── v2_001_migrate_to_v2_schema.py  # V2 schema migration
├── test_v2_integration.py       # V2 integration tests (11 tests)
├── test_v2_api_manual.py        # Manual API testing script
├── e2e_test_v2.py               # End-to-end V2 workflow tests
├── verify_v2_schema.py          # Database schema verification
├── requirements.txt             # Python dependencies
├── .env                         # Environment variables (API keys)
├── API_DOCUMENTATION_V2.md      # Complete V2 API documentation
└── README.md                    # This file
```

## Database Schema (V2)

### Tables
1. **users** - User accounts (email-based identification)
2. **resumes** - Resume documents with parsed data
3. **job_descriptions** - Job descriptions with metadata
4. **applications** - Application tracking (links users, resumes, JDs)
5. **gap_analyses** - Gap analysis results per application
6. **ats_scores** - ATS scoring results per application
7. **alembic_version** - Migration version tracking

### Relationships
- User → Resumes (one-to-many, cascade delete)
- User → JobDescriptions (one-to-many, cascade delete)
- User → Applications (one-to-many, cascade delete)
- Resume → Applications (one-to-many)
- JobDescription → Applications (one-to-many)
- Application → GapAnalysis (one-to-one, cascade delete)
- Application → ATSScore (one-to-one, cascade delete)

## Testing

### V2 Integration Tests (Comprehensive)
Tests all V2 endpoints, database schema, and CRUD operations.
```bash
python -m pytest test_v2_integration.py -v
```

**Coverage:**
- ✅ Database schema validation (7 tables)
- ✅ V2 columns and relationships
- ✅ Foreign keys and indexes
- ✅ Job URL fetching (mocked)
- ✅ Resume/JD upload with V2 parameters
- ✅ Gap analysis with application creation
- ✅ Applications list and detail endpoints
- ✅ Complete CRUD operations

**Results:** 11/11 tests passing ✅

### Manual API Testing Script
Interactive script that tests all V2 endpoints with real API calls.
```bash
# Start backend server first
python -m uvicorn main:app --port 8000

# In another terminal
python test_v2_api_manual.py
```

### E2E Tests (Full Workflows)
Tests complete V1 and V2 user workflows.
```bash
python -m pytest e2e_test_v2.py -v
```

**Test Coverage:**
- V1 backward compatibility
- V2 user-centric workflows
- Multi-user data isolation
- Job URL fetching
- Error handling
- Application tracking

### Database Schema Verification
Verify V2 database schema integrity.
```bash
python verify_v2_schema.py
```

**Checks:**
- ✅ All V2 tables exist
- ✅ Columns complete and correctly typed
- ✅ Foreign keys properly configured
- ✅ Indexes in place
- ✅ Data integrity (no orphaned records)
- ✅ ORM relationships working
- ✅ V2 enhancements present

**Results:** 7/7 checks passing 🎉

### Test Individual Endpoints (cURL)
```bash
# Upload resume with user context (V2)
curl -X POST "http://localhost:8000/upload-resume/" \
  -F "file=@resume.pdf" \
  -F "user_email=user@example.com"

# Upload JD with metadata (V2)
curl -X POST "http://localhost:8000/upload-jd/" \
  -F "file=@jd.pdf" \
  -F "user_email=user@example.com" \
  -F "job_url=https://www.linkedin.com/jobs/view/123" \
  -F "title=Senior Developer" \
  -F "company=TechCorp"

# Fetch JD from URL (V2)
curl -X POST "http://localhost:8000/v2/fetch-jd-from-url/" \
  -H "Content-Type: application/json" \
  -d '{"job_url": "https://www.linkedin.com/jobs/view/123"}'

# Get applications list (V2)
curl "http://localhost:8000/v2/applications/?user_email=user@example.com"

# Gap analysis with application creation (V2)
curl -X POST "http://localhost:8000/gap-analysis/?resume_id=1&jd_id=1&user_email=user@example.com&create_application=true"
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
