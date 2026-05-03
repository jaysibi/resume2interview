# AI Features Setup & Usage Guide

## Prerequisites

1. **OpenAI API Key**: Sign up at https://platform.openai.com/ and get your API key
2. **Python packages**: Install all dependencies from requirements.txt
3. **Database**: PostgreSQL with resumetailor database

## Environment Setup

### 1. Create .env file

Copy the example environment file and fill in your values:

```bash
cd c:\Projects\ResumeTailor\01-Code\backend
copy .env.example .env
```

### 2. Add your OpenAI API Key

Edit `.env` and add your API key:

```bash
OPENAI_API_KEY=sk-proj-your-actual-api-key-here
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Key new packages:
- `openai==1.12.0` - OpenAI Python SDK
- `pydantic-settings==2.1.0` - Configuration management
- `alembic==1.13.1` - Database migrations

### 4. Apply Database Migrations

```bash
python -m alembic upgrade head
```

## Running the Application

```bash
cd c:\Projects\ResumeTailor\01-Code\backend
uvicorn main:app --reload
```

Server will start at: http://localhost:8000

## API Endpoints

### 1. Upload Resume (with AI Skill Extraction)

**Endpoint**: `POST /upload-resume/`

**Request**:
```bash
curl -X POST "http://localhost:8000/upload-resume/" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@resume.pdf"
```

**Response**:
```json
{
  "id": 1,
  "filename": "resume.pdf",
  "parsed": {
    "raw_text": "...",
    "skills": [],
    "experience": [],
    "education": [],
    "tools": []
  },
  "extracted": {
    "skills": [
      {
        "name": "Python",
        "category": "Programming Language",
        "proficiency": "Advanced"
      }
    ],
    "experience": [...],
    "education": [...]
  }
}
```

**What Happens**:
1. File is validated (size, type, content)
2. Resume is parsed (PDF/DOCX → text)
3. Stored in database
4. **AI extracts skills, experience, education** using OpenAI GPT-4o-mini
5. Database updated with extracted data
6. Returns enriched resume data

### 2. Gap Analysis

**Endpoint**: `POST /gap-analysis/?resume_id={id}&jd_id={id}`

**Request**:
```bash
curl -X POST "http://localhost:8000/gap-analysis/?resume_id=1&jd_id=1"
```

**Response**:
```json
{
  "resume_id": 1,
  "jd_id": 1,
  "analysis": {
    "match_score": 75,
    "missing_required_skills": ["Kubernetes", "Docker"],
    "missing_preferred_skills": ["AWS Lambda"],
    "strengths": [
      "Strong Python background matches primary requirement",
      "Database experience aligns with tech stack"
    ],
    "weak_areas": [
      "Limited DevOps experience",
      "No mention of cloud infrastructure"
    ],
    "recommendations": [
      "Add Kubernetes projects to demonstrate container orchestration skills",
      "Highlight any cloud deployment experience"
    ]
  }
}
```

**What It Does**:
- Compares resume skills/experience against job description
- Identifies missing required and preferred skills
- Highlights candidate strengths
- Provides actionable recommendations
- Uses OpenAI GPT-4o for better reasoning

### 3. ATS Scoring

**Endpoint**: `POST /ats-score/?resume_id={id}&jd_id={id}`

**Request**:
```bash
curl -X POST "http://localhost:8000/ats-score/?resume_id=1&jd_id=1"
```

**Response**:
```json
{
  "resume_id": 1,
  "jd_id": 1,
  "scoring": {
    "ats_score": 85,
    "keyword_match_percentage": 78,
    "format_score": 92,
    "matched_keywords": ["Python", "FastAPI", "PostgreSQL"],
    "missing_keywords": ["Kubernetes", "Docker"],
    "issues": [
      {
        "type": "keyword",
        "description": "Missing 'Docker' keyword",
        "severity": "medium"
      }
    ],
    "recommendations": [
      "Add 'Docker' keyword in experience section",
      "Use standard section headers: Work Experience, Education, Skills"
    ]
  }
}
```

**What It Does**:
- Analyzes resume for ATS compatibility
- Calculates keyword match percentage
- Evaluates formatting for machine readability
- Identifies missing keywords
- Provides specific improvement recommendations

## Testing the AI Features

### Using cURL

```bash
# 1. Upload a resume
curl -X POST "http://localhost:8000/upload-resume/" \
  -F "file=@sample_resume.pdf" \
  > resume_response.json

# Extract resume ID from response
RESUME_ID=$(cat resume_response.json | jq -r '.id')

# 2. Upload a job description
curl -X POST "http://localhost:8000/upload-jd/" \
  -F "file=@job_description.pdf" \
  > jd_response.json

# Extract JD ID
JD_ID=$(cat jd_response.json | jq -r '.id')

# 3. Get gap analysis
curl -X POST "http://localhost:8000/gap-analysis/?resume_id=${RESUME_ID}&jd_id=${JD_ID}" \
  | jq

# 4. Get ATS score
curl -X POST "http://localhost:8000/ats-score/?resume_id=${RESUME_ID}&jd_id=${JD_ID}" \
  | jq
```

### Using Python

```python
import requests

BASE_URL = "http://localhost:8000"

# Upload resume
with open("resume.pdf", "rb") as f:
    response = requests.post(
        f"{BASE_URL}/upload-resume/",
        files={"file": f}
    )
resume_data = response.json()
resume_id = resume_data["id"]

print(f"Resume uploaded: ID {resume_id}")
print(f"Extracted {len(resume_data['extracted']['skills'])} skills")

# Upload JD
with open("job_description.pdf", "rb") as f:
    response = requests.post(
        f"{BASE_URL}/upload-jd/",
        files={"file": f}
    )
jd_data = response.json()
jd_id = jd_data["id"]

# Gap analysis
response = requests.post(
    f"{BASE_URL}/gap-analysis/",
    params={"resume_id": resume_id, "jd_id": jd_id}
)
gap_analysis = response.json()

print(f"\nMatch Score: {gap_analysis['analysis']['match_score']}%")
print(f"Missing Skills: {gap_analysis['analysis']['missing_required_skills']}")

# ATS scoring
response = requests.post(
    f"{BASE_URL}/ats-score/",
    params={"resume_id": resume_id, "jd_id": jd_id}
)
ats_score = response.json()

print(f"\nATS Score: {ats_score['scoring']['ats_score']}%")
print(f"Keyword Match: {ats_score['scoring']['keyword_match_percentage']}%")
```

## Cost Management

### Estimated Costs (per API call)

Based on OpenAI pricing:

| Operation | Model | Avg Tokens | Cost per Call |
|-----------|-------|------------|---------------|
| Skill Extraction | GPT-4o-mini | 2000 | $0.00053 |
| Gap Analysis | GPT-4o | 2800 | $0.022 |
| ATS Scoring | GPT-4o-mini | 3100 | $0.00075 |

**Daily Budget Example** (100 users):
- 100 resumes with skill extraction: $0.053
- 50 gap analyses: $1.10
- 30 ATS scores: $0.023
- **Total**: ~$1.18/day = **$35/month**

### Monitoring Usage

Check OpenAI dashboard for:
- Total API calls
- Token usage
- Costs

Set up budget alerts at https://platform.openai.com/settings/organization/billing/limits

### Cost Optimization Tips

1. **Enable Caching** (future enhancement)
   - Cache results for 1 hour
   - Avoid redundant API calls

2. **Smart Model Selection**
   - Use GPT-4o-mini for extraction ($0.15/1M tokens)
   - Use GPT-4o only for complex reasoning ($5/1M tokens)

3. **User Quotas**
   - Free tier: 3 analyses per day
   - Paid tier: Unlimited

## Error Handling

### Common Errors

**1. Missing API Key**
```
ValueError: OPENAI_API_KEY environment variable not set
```
**Solution**: Add `OPENAI_API_KEY` to your `.env` file

**2. AI Service Unavailable (503)**
```json
{
  "detail": {
    "error_code": "AI_SERVICE_UNAVAILABLE",
    "message": "Failed to perform gap analysis. Please try again."
  }
}
```
**Causes**: 
- Rate limit exceeded
- Network connectivity issues
- OpenAI API outage

**Solution**: Wait and retry. The system has automatic retry logic with exponential backoff.

**3. Invalid Resume Text**
```json
{
  "detail": {
    "error_code": "PARSING_ERROR",
    "message": "Failed to parse resume content"
  }
}
```
**Solution**: Ensure resume has readable text (not just images)

## Rate Limiting

**Current Limits**:
- Upload endpoints: 10 requests/minute
- Gap analysis: 20 requests/minute
- ATS scoring: 20 requests/minute

**Exceeding Limit**:
```json
{
  "error": "Rate limit exceeded: 10 per 1 minute"
}
```

## Features Roadmap

### ✅ Completed
- Skill extraction with AI
- Gap analysis endpoint
- ATS scoring endpoint
- Comprehensive error handling
- Retry logic with exponential backoff

### 🚧 In Progress
- Response caching (Redis)
- Integration tests for AI endpoints

### 📋 Planned
- Bullet point rewriting endpoint
- Resume optimization suggestions
- Interview question generation
- Multi-language support
- Alternative LLM providers (Claude, Gemini)

## Troubleshooting

### AI extraction returns empty arrays

**Check**:
1. Resume has sufficient text (min 50 characters)
2. Text is in English (or supported language)
3. API key is valid and has credits

**Debug**:
```bash
# Check logs
tail -f logs/app.log

# Look for:
# "Extracting skills from resume (XXX chars)"
# "Skills extracted: N skills, M experience entries"
```

### Slow response times

**Normal latencies**:
- Skill extraction: 2-4 seconds
- Gap analysis: 3-6 seconds
- ATS scoring: 3-5 seconds

**If slower**:
- Check internet connection
- Check OpenAI API status: https://status.openai.com/
- Reduce resume text length (max 10,000 chars recommended)

## Support & Documentation

- **AI/ML Design Doc**: [00-Design/ai-ml-integration-design.md](../../00-Design/ai-ml-integration-design.md)
- **Alembic Migrations**: [alembic/README.md](alembic/README.md)
- **API Documentation**: http://localhost:8000/docs (when server running)
- **OpenAI Docs**: https://platform.openai.com/docs

## Quick Start Checklist

- [ ] Created `.env` file with `OPENAI_API_KEY`
- [ ] Installed dependencies: `pip install -r requirements.txt`
- [ ] Applied migrations: `python -m alembic upgrade head`
- [ ] Started server: `uvicorn main:app --reload`
- [ ] Tested health check: `curl http://localhost:8000/`
- [ ] Uploaded test resume with AI extraction
- [ ] Ran gap analysis
- [ ] Checked ATS score

**You're ready to go! 🚀**
