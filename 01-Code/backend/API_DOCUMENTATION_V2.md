# Resume Tailor V2 - API Documentation

## Base URL
```
http://localhost:8000
```

## Table of Contents
1. [Authentication](#authentication)
2. [Core Endpoints](#core-endpoints)
3. [V2 Endpoints](#v2-endpoints)
4. [Error Handling](#error-handling)
5. [Rate Limiting](#rate-limiting)

---

## Authentication
Currently, Resume Tailor V2 uses email-based user identification without authentication. Future versions will implement JWT-based authentication.

---

## Core Endpoints

### 1. Health Check
Get server status.

**Endpoint:** `GET /`

**Response:**
```json
{
  "status": "ok",
  "message": "Resume Tailor API is running"
}
```

---

### 2. Upload Resume
Upload and parse a resume file with AI-powered skill extraction.

**Endpoint:** `POST /upload-resume/`

**Parameters:**
- `file` (file, required): Resume file (PDF or DOCX, max 10 MB)
- `user_email` (string, optional): User email for V2 multi-user support

**Request (multipart/form-data):**
```bash
curl -X POST "http://localhost:8000/upload-resume/" \
  -F "file=@resume.pdf" \
  -F "user_email=user@example.com"
```

**Response (200 OK):**
```json
{
  "id": 123,
  "filename": "resume.pdf",
  "user_id": 1,
  "parsed": {
    "raw_text": "Resume content...",
    "skills": [],
    "experience": [],
    "education": []
  },
  "extracted": {
    "skills": [
      {
        "name": "Python",
        "category": "Programming Language",
        "proficiency": "Expert"
      }
    ],
    "experience": [...],
    "education": [...]
  }
}
```

**Error Responses:**
- `400`: Invalid file type
- `413`: File too large
- `500`: AI extraction or database error

---

### 3. Upload Job Description
Upload and parse a job description file.

**Endpoint:** `POST /upload-jd/`

**Parameters:**
- `file` (file, required): JD file (PDF or DOCX, max 10 MB)
- `user_email` (string, optional): User email for V2 multi-user support
- `job_url` (string, optional): URL of the job posting
- `title` (string, optional): Job title
- `company` (string, optional): Company name

**Request (multipart/form-data):**
```bash
curl -X POST "http://localhost:8000/upload-jd/" \
  -F "file=@job_description.pdf" \
  -F "user_email=user@example.com" \
  -F "job_url=https://www.linkedin.com/jobs/view/123456" \
  -F "title=Senior Python Developer" \
  -F "company=TechCorp Inc."
```

**Response (200 OK):**
```json
{
  "id": 456,
  "filename": "job_description.pdf",
  "user_id": 1,
  "job_url": "https://www.linkedin.com/jobs/view/123456",
  "title": "Senior Python Developer",
  "company": "TechCorp Inc.",
  "parsed": {
    "raw_text": "Job description content...",
    "mandatory_skills": ["Python", "FastAPI"],
    "preferred_skills": ["React", "Docker"],
    "keywords": [...]
  }
}
```

---

### 4. Gap Analysis
Analyze gap between resume and job description.

**Endpoint:** `POST /gap-analysis/`

**Parameters:**
- `resume_id` (integer, required): Resume ID from upload
- `jd_id` (integer, required): JD ID from upload
- `user_email` (string, optional): User email for V2 tracking
- `create_application` (boolean, optional): Create application record (V2)

**Request:**
```bash
curl -X POST "http://localhost:8000/gap-analysis/?resume_id=123&jd_id=456&user_email=user@example.com&create_application=true"
```

**Response (200 OK):**
```json
{
  "resume_id": 123,
  "jd_id": 456,
  "application_id": 789,
  "match_score": 85,
  "missing_required_skills": ["Docker"],
  "missing_preferred_skills": ["Kubernetes"],
  "strengths": [
    "Strong Python programming experience",
    "FastAPI expertise matches job requirements"
  ],
  "weak_areas": [
    "Limited containerization experience"
  ],
  "recommendations": [
    "Highlight any Docker projects or coursework",
    "Consider taking a Kubernetes certification"
  ],
  "analysis": "Detailed analysis text..."
}
```

---

### 5. ATS Score
Calculate Applicant Tracking System compatibility score.

**Endpoint:** `POST /ats-score/`

**Parameters:**
- `resume_id` (integer, required): Resume ID
- `jd_id` (integer, required): JD ID

**Request:**
```bash
curl -X POST "http://localhost:8000/ats-score/?resume_id=123&jd_id=456"
```

**Response (200 OK):**
```json
{
  "resume_id": 123,
  "jd_id": 456,
  "ats_score": 78,
  "keyword_match_percentage": 82,
  "format_score": 75,
  "matched_keywords": [
    "Python", "FastAPI", "PostgreSQL"
  ],
  "missing_keywords": [
    "Docker", "Kubernetes"
  ],
  "issues": [
    "Resume lacks specific version information"
  ],
  "recommendations": [
    "Add Docker and Kubernetes to skills section",
    "Include specific technology versions"
  ]
}
```

---

### 6. Get Resume
Retrieve a previously uploaded resume.

**Endpoint:** `GET /resume/{resume_id}`

**Response (200 OK):**
```json
{
  "id": 123,
  "filename": "resume.pdf",
  "raw_text": "...",
  "skills": [...],
  "experience": [...],
  "education": [...],
  "created_at": "2026-05-03T10:30:00Z",
  "updated_at": "2026-05-03T10:30:00Z"
}
```

---

### 7. Get Job Description
Retrieve a previously uploaded job description.

**Endpoint:** `GET /jd/{jd_id}`

**Response (200 OK):**
```json
{
  "id": 456,
  "filename": "job_description.pdf",
  "raw_text": "...",
  "mandatory_skills": [...],
  "preferred_skills": [...],
  "keywords": [...],
  "created_at": "2026-05-03T10:35:00Z",
  "updated_at": "2026-05-03T10:35:00Z"
}
```

---

## V2 Endpoints

### 1. Fetch JD from URL
Fetch and parse job description from a job posting URL.

**Endpoint:** `POST /v2/fetch-jd-from-url/`

**Supported Platforms:**
- LinkedIn Jobs
- Naukri.com
- Indeed
- Monster
- Glassdoor

**Request:**
```bash
curl -X POST "http://localhost:8000/v2/fetch-jd-from-url/" \
  -H "Content-Type: application/json" \
  -d '{
    "job_url": "https://www.linkedin.com/jobs/view/3849876543"
  }'
```

**Response (200 OK):**
```json
{
  "title": "Senior Python Developer",
  "company": "TechCorp Inc.",
  "location": "San Francisco, CA",
  "raw_text": "Full job description text...",
  "platform": "linkedin"
}
```

**Error Responses:**
- `400`: Invalid or unsupported URL format
- `403`: Access forbidden (blocked by website)
- `404`: Job posting not found
- `500`: Scraping error

---

### 2. Get Applications List
Get list of applications for a user.

**Endpoint:** `GET /v2/applications/`

**Parameters:**
- `user_email` (string, optional): User email (defaults to default user)
- `skip` (integer, optional): Number of records to skip (default: 0)
- `limit` (integer, optional): Max records to return (default: 10, max: 100)

**Request:**
```bash
curl -X GET "http://localhost:8000/v2/applications/?user_email=user@example.com&skip=0&limit=10"
```

**Response (200 OK):**
```json
{
  "user_id": 1,
  "user_email": "user@example.com",
  "total": 25,
  "skip": 0,
  "limit": 10,
  "applications": [
    {
      "id": 789,
      "resume_id": 123,
      "jd_id": 456,
      "status": "analyzed",
      "applied_at": "2026-05-03T10:40:00Z",
      "resume_filename": "resume.pdf",
      "jd_filename": "job_description.pdf",
      "job_title": "Senior Python Developer",
      "company": "TechCorp Inc.",
      "job_url": "https://www.linkedin.com/jobs/view/123456",
      "match_score": 85
    }
  ]
}
```

---

### 3. Get Application Details
Get detailed information about a specific application.

**Endpoint:** `GET /v2/applications/{application_id}/`

**Request:**
```bash
curl -X GET "http://localhost:8000/v2/applications/789/"
```

**Response (200 OK):**
```json
{
  "application": {
    "id": 789,
    "user_id": 1,
    "resume_id": 123,
    "jd_id": 456,
    "status": "analyzed",
    "applied_at": "2026-05-03T10:40:00Z",
    "notes": null,
    "created_at": "2026-05-03T10:40:00Z",
    "updated_at": "2026-05-03T10:40:00Z"
  },
  "resume": {
    "id": 123,
    "filename": "resume.pdf",
    "upload_date": "2026-05-03T10:30:00Z",
    "skills": [...]
  },
  "job_description": {
    "id": 456,
    "filename": "job_description.pdf",
    "title": "Senior Python Developer",
    "company": "TechCorp Inc.",
    "job_url": "https://www.linkedin.com/jobs/view/123456",
    "upload_date": "2026-05-03T10:35:00Z",
    "mandatory_skills": [...]
  },
  "gap_analysis": {
    "id": 100,
    "match_score": 85,
    "missing_required_skills": ["Docker"],
    "missing_preferred_skills": ["Kubernetes"],
    "strengths": [...],
    "weak_areas": [...],
    "recommendations": [...],
    "created_at": "2026-05-03T10:40:00Z"
  },
  "ats_score": {
    "id": 50,
    "ats_score": 78,
    "keyword_match_percentage": 82,
    "format_score": 75,
    "matched_keywords": [...],
    "missing_keywords": [...],
    "issues": [...],
    "recommendations": [...],
    "created_at": "2026-05-03T10:41:00Z"
  }
}
```

---

## Error Handling

All endpoints return errors in a consistent format:

```json
{
  "detail": {
    "error_code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": "Additional error context (optional)"
  }
}
```

### Common Error Codes:
- `INVALID_FILE_TYPE`: File must be PDF or DOCX
- `FILE_TOO_LARGE`: File exceeds 10 MB limit
- `NOT_FOUND`: Resource not found (404)
- `INTERNAL_SERVER_ERROR`: Unexpected server error (500)
- `AI_SERVICE_ERROR`: OpenAI API error
- `DATABASE_ERROR`: Database operation failed
- `VALIDATION_ERROR`: Request validation failed

---

## Rate Limiting

Rate limiting is currently disabled for development. In production:
- Default limit: 10 requests per minute per IP address
- Headers returned:
  - `X-RateLimit-Limit`: Maximum requests allowed
  - `X-RateLimit-Remaining`: Remaining requests
  - `X-RateLimit-Reset`: Time when limit resets

---

## Examples

### Complete Workflow Example (V2)

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

# 2. Upload JD with metadata
with open("job_description.pdf", "rb") as f:
    jd_response = requests.post(
        f"{BASE_URL}/upload-jd/",
        files={"file": f},
        data={
            "user_email": USER_EMAIL,
            "job_url": "https://www.linkedin.com/jobs/view/123456",
            "title": "Senior Python Developer",
            "company": "TechCorp Inc."
        }
    )
    jd_id = jd_response.json()["id"]

# 3. Gap Analysis with Application Creation
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

# 4. Get Application Details
app_response = requests.get(f"{BASE_URL}/v2/applications/{app_id}/")
print(app_response.json())

# 5. Get All Applications for User
list_response = requests.get(
    f"{BASE_URL}/v2/applications/",
    params={"user_email": USER_EMAIL}
)
print(f"Total applications: {list_response.json()['total']}")
```

---

## Testing

### Manual Testing Script
```bash
cd backend
python test_v2_api_manual.py
```

### Integration Tests
```bash
cd backend
python -m pytest test_v2_integration.py -v
```

### E2E Tests
```bash
cd backend
python -m pytest e2e_test_v2.py -v
```

---

## Notes

- All timestamps are in ISO 8601 format with timezone (UTC)
- File uploads use multipart/form-data encoding
- JSON payloads use application/json content type
- Maximum file size: 10 MB
- Supported file types: PDF (.pdf), DOCX (.docx)
- OpenAI API key required for AI features (gap analysis, ATS scoring, skill extraction)
