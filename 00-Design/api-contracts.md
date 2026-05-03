# API Contracts (OpenAPI/Swagger) — Resume Tailor

## Overview
This document defines the API contracts for all backend endpoints in the Resume Tailor system. These contracts ensure clear communication between frontend and backend, and support automated documentation and testing.

**Base URL:** `http://localhost:8000` (development)  
**API Version:** v1 (current endpoints at root, future versions will use `/v1/` prefix)  
**Content-Type:** `application/json` (except file uploads)  
**Max File Size:** 10 MB

---

## Global Configuration

### CORS Policy
- **Allowed Origins:** `*` (development), specific domains in production
- **Allowed Methods:** GET, POST, PUT, DELETE, OPTIONS
- **Allowed Headers:** Content-Type, Authorization

### Authentication (Future Implementation)
All endpoints (except health check) will require JWT authentication:
- **Header:** `Authorization: Bearer <JWT_TOKEN>`
- **Token Expiry:** Access token (15 minutes), Refresh token (7 days)
- **Unauthorized Response (401):**
```json
{
  "error_code": "UNAUTHORIZED",
  "message": "Authentication required",
  "details": null
}
```

### Standard Error Response Format
All errors return JSON with consistent structure:
```json
{
  "error_code": "ERROR_CODE_ENUM",
  "message": "Human-readable error message",
  "details": "Optional additional context or field-level errors"
}
```

### Error Codes
- `INVALID_FILE_TYPE` — File type not supported (must be PDF or DOCX)
- `FILE_TOO_LARGE` — File exceeds 10 MB limit
- `PARSING_ERROR` — Failed to parse file content
- `NOT_FOUND` — Resource not found
- `UNAUTHORIZED` — Authentication required or invalid token
- `RATE_LIMIT_EXCEEDED` — Too many requests
- `INTERNAL_SERVER_ERROR` — Unexpected server error

---

## Endpoints

### 1. Health Check

**`GET /`**

Health check endpoint to verify API availability.

**Request:**
- No parameters required

**Response (200 OK):**
```json
{
  "message": "Resume Tailor API is running."
}
```

**cURL Example:**
```bash
curl -X GET http://localhost:8000/
```

---

### 2. Upload Resume

**`POST /upload-resume/`**

Upload and parse a resume file (PDF or DOCX). The file is parsed to extract text and placeholder structures for skills, experience, education, and tools.

**Request:**
- **Content-Type:** `multipart/form-data`
- **Headers:** 
  - `Authorization: Bearer <JWT_TOKEN>` (future)
- **Body:**
  - `file` (binary): Resume file (PDF or DOCX, max 10 MB)

**Response (200 OK):**
```json
{
  "id": 123,
  "filename": "john_doe_resume.pdf",
  "parsed": {
    "raw_text": "John Doe\nSoftware Engineer\n...",
    "skills": [],
    "experience": [],
    "education": [],
    "tools": []
  }
}
```

**Response Fields:**
- `id` (integer): Database ID of stored resume
- `filename` (string): Original filename
- `parsed` (object): Parsed resume data
  - `raw_text` (string): Full text extracted from file
  - `skills` (array): List of skills (currently empty, future: extracted skills)
  - `experience` (array): Work experience entries (currently empty)
  - `education` (array): Education entries (currently empty)
  - `tools` (array): Tools/technologies (currently empty)

**Error Responses:**

**400 Bad Request** — Invalid file type
```json
{
  "error": "Unsupported file type"
}
```

**413 Payload Too Large** — File exceeds size limit
```json
{
  "error_code": "FILE_TOO_LARGE",
  "message": "File size exceeds 10 MB limit",
  "details": "Received: 15.2 MB"
}
```

**422 Unprocessable Entity** — Parsing error
```json
{
  "error_code": "PARSING_ERROR",
  "message": "Failed to parse resume content",
  "details": "Corrupted PDF or unsupported encoding"
}
```

**500 Internal Server Error** — Unexpected error
```json
{
  "error_code": "INTERNAL_SERVER_ERROR",
  "message": "An unexpected error occurred",
  "details": null
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:8000/upload-resume/ \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/resume.pdf"
```

---

### 3. Upload Job Description

**`POST /upload-jd/`**

Upload and parse a job description file (PDF or DOCX). The file is parsed to extract text and placeholder structures for skills and keywords.

**Request:**
- **Content-Type:** `multipart/form-data`
- **Headers:** 
  - `Authorization: Bearer <JWT_TOKEN>` (future)
- **Body:**
  - `file` (binary): Job description file (PDF or DOCX, max 10 MB)

**Response (200 OK):**
```json
{
  "id": 456,
  "filename": "senior_qa_engineer_jd.pdf",
  "parsed": {
    "raw_text": "Senior QA Engineer\nRequirements: 5+ years...",
    "mandatory_skills": [],
    "preferred_skills": [],
    "keywords": []
  }
}
```

**Response Fields:**
- `id` (integer): Database ID of stored job description
- `filename` (string): Original filename
- `parsed` (object): Parsed JD data
  - `raw_text` (string): Full text extracted from file
  - `mandatory_skills` (array): Required skills (currently empty, future: extracted)
  - `preferred_skills` (array): Preferred/nice-to-have skills (currently empty)
  - `keywords` (array): ATS keywords (currently empty)

**Error Responses:**
Same as `/upload-resume/` (400, 413, 422, 500)

**cURL Example:**
```bash
curl -X POST http://localhost:8000/upload-jd/ \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/job_description.pdf"
```

---

### 4. Get Resume by ID

**`GET /resume/{resume_id}`**

Retrieve a previously uploaded and parsed resume by its database ID.

**Request:**
- **Path Parameters:**
  - `resume_id` (integer, required): Resume database ID
- **Headers:** 
  - `Authorization: Bearer <JWT_TOKEN>` (future)

**Response (200 OK):**
```json
{
  "id": 123,
  "filename": "john_doe_resume.pdf",
  "raw_text": "John Doe\nSoftware Engineer\n...",
  "skills": [],
  "experience": [],
  "education": [],
  "tools": [],
  "created_at": "2026-05-01T10:30:00Z"
}
```

**Response Fields:**
- `id` (integer): Database ID
- `filename` (string): Original filename
- `raw_text` (string): Full extracted text
- `skills` (array): Extracted skills (JSON array)
- `experience` (array): Work experience (JSON array)
- `education` (array): Education entries (JSON array)
- `tools` (array): Tools/technologies (JSON array)
- `created_at` (string, ISO 8601): Timestamp of upload

**Error Responses:**

**404 Not Found** — Resume doesn't exist
```json
{
  "detail": "Resume not found"
}
```

**cURL Example:**
```bash
curl -X GET http://localhost:8000/resume/123
```

---

### 5. Get Job Description by ID

**`GET /jd/{jd_id}`**

Retrieve a previously uploaded and parsed job description by its database ID.

**Request:**
- **Path Parameters:**
  - `jd_id` (integer, required): Job description database ID
- **Headers:** 
  - `Authorization: Bearer <JWT_TOKEN>` (future)

**Response (200 OK):**
```json
{
  "id": 456,
  "filename": "senior_qa_engineer_jd.pdf",
  "raw_text": "Senior QA Engineer\nRequirements: 5+ years...",
  "mandatory_skills": [],
  "preferred_skills": [],
  "keywords": [],
  "created_at": "2026-05-01T11:00:00Z"
}
```

**Response Fields:**
- `id` (integer): Database ID
- `filename` (string): Original filename
- `raw_text` (string): Full extracted text
- `mandatory_skills` (array): Required skills (JSON array)
- `preferred_skills` (array): Preferred skills (JSON array)
- `keywords` (array): ATS keywords (JSON array)
- `created_at` (string, ISO 8601): Timestamp of upload

**Error Responses:**

**404 Not Found** — Job description doesn't exist
```json
{
  "detail": "Job Description not found"
}
```

**cURL Example:**
```bash
curl -X GET http://localhost:8000/jd/456
```

---

## Future Endpoints (Planned)

### 6. Extract Skills

**`POST /extract-skills/`**

AI-powered skill extraction from resume or JD text using LLM.

**Request:**
```json
{
  "text": "5 years Python, FastAPI, PostgreSQL...",
  "context": "resume"
}
```

**Response:**
```json
{
  "skills": ["Python", "FastAPI", "PostgreSQL"],
  "confidence_scores": [0.95, 0.92, 0.89]
}
```

---

### 7. Gap Analysis

**`POST /gap-analysis/`**

Compare resume against job description to identify missing skills and keywords.

**Request:**
```json
{
  "resume_id": 123,
  "jd_id": 456
}
```

**Response:**
```json
{
  "missing_skills": ["Kubernetes", "AWS"],
  "matched_skills": ["Python", "FastAPI"],
  "match_percentage": 75,
  "recommendations": ["Add Kubernetes experience", "Highlight AWS projects"]
}
```

---

### 8. ATS Score

**`POST /ats-score/`**

Calculate ATS compatibility score for resume-JD pair.

**Request:**
```json
{
  "resume_id": 123,
  "jd_id": 456
}
```

**Response:**
```json
{
  "ats_score": 82,
  "keyword_match": 78,
  "format_score": 90,
  "suggestions": ["Add more quantifiable achievements", "Include missing keywords: CI/CD, Docker"]
}
```

---

### 9. Rewrite Bullets

**`POST /rewrite-bullets/`**

AI-powered resume bullet point enhancement.

**Request:**
```json
{
  "bullet": "Worked on testing",
  "context": "QA Engineer, 5 years experience"
}
```

**Response:**
```json
{
  "original": "Worked on testing",
  "rewritten": "Designed and executed comprehensive test strategies for enterprise applications, reducing production defects by 40%",
  "improvements": ["Added quantifiable metric", "More action-oriented", "Industry-specific language"]
}
```

---

## OpenAPI/Swagger Documentation

The FastAPI backend auto-generates interactive API documentation:
- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`
- **OpenAPI JSON:** `http://localhost:8000/openapi.json`

These docs are automatically synced with code and provide a testing interface.

---

## Rate Limiting (Future)

To prevent abuse, rate limiting will be implemented:
- **Anonymous users:** 10 requests/minute
- **Authenticated users:** 100 requests/minute
- **Premium users:** 1000 requests/minute

**Rate Limit Exceeded (429):**
```json
{
  "error_code": "RATE_LIMIT_EXCEEDED",
  "message": "Too many requests",
  "details": "Limit: 100/min, Retry after: 30s"
}
```

---

## Versioning Strategy

Current endpoints are at root level. Future major changes will use versioned paths:
- Current: `/upload-resume/`
- Future: `/v2/upload-resume/`

Breaking changes will be introduced in new versions while maintaining backward compatibility for at least 6 months.

---

*Last Updated: May 1, 2026*  
*Document Version: 2.0*
