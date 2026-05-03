# AI/ML Integration Design Document

**Version**: 1.0  
**Date**: 2026-05-01  
**Status**: Draft  
**Author**: Technical Architect

---

## Table of Contents
1. [Overview](#overview)
2. [AI/ML Provider Selection](#aiml-provider-selection)
3. [Architecture & Data Flow](#architecture--data-flow)
4. [Core AI Features](#core-ai-features)
5. [Prompt Engineering Strategy](#prompt-engineering-strategy)
6. [API Integration](#api-integration)
7. [Error Handling & Resilience](#error-handling--resilience)
8. [Cost Management](#cost-management)
9. [Security & Privacy](#security--privacy)
10. [Testing Strategy](#testing-strategy)
11. [Performance & Scalability](#performance--scalability)
12. [Implementation Roadmap](#implementation-roadmap)

---

## 1. Overview

### Purpose
This document defines the AI/ML integration strategy for the Resume Tailor application, focusing on LLM-powered features for resume analysis, skill extraction, gap analysis, and ATS scoring.

### Goals
- **Accurate Skill Extraction**: Extract skills, experience, and education from unstructured resume text
- **Intelligent Gap Analysis**: Compare resume content against job descriptions to identify missing qualifications
- **ATS Optimization**: Score and suggest improvements for Applicant Tracking System compatibility
- **Cost-Effective**: Minimize API costs while maintaining quality
- **Reliable**: Handle failures gracefully with retry logic and fallbacks

### Scope
- LLM integration for text analysis and generation
- Structured data extraction from resumes and job descriptions
- Resume-JD matching and scoring algorithms
- Prompt template management
- Response validation and post-processing

---

## 2. AI/ML Provider Selection

### Primary Provider: OpenAI GPT-4
**Rationale**:
- Industry-leading NLP capabilities
- Strong structured output support (JSON mode)
- Extensive context window (128K tokens)
- Reliable API with high uptime
- Well-documented Python SDK

**Alternative Providers** (for future consideration):
- **Anthropic Claude 3.5**: Superior reasoning, better privacy controls
- **Google Gemini**: Competitive pricing, multimodal capabilities
- **Azure OpenAI**: Enterprise compliance, regional data residency
- **Local Models** (LLaMA, Mistral): Cost reduction for production scale

### Model Selection Strategy
| Use Case | Model | Reasoning |
|----------|-------|-----------|
| Skill Extraction | GPT-4o-mini | Cost-effective, sufficient for structured extraction |
| Gap Analysis | GPT-4o | Better reasoning for nuanced comparisons |
| ATS Scoring | GPT-4o-mini | Rule-based + basic LLM assistance |
| Bullet Rewriting | GPT-4o | Higher quality output for user-facing text |

---

## 3. Architecture & Data Flow

### High-Level Architecture
```
┌─────────────────┐
│  FastAPI Server │
│                 │
│  ┌───────────┐  │
│  │ Resume/JD │  │
│  │  Upload   │  │
│  └─────┬─────┘  │
│        │        │
│  ┌─────▼─────┐  │
│  │  Parser   │  │
│  │ (PDF/DOCX)│  │
│  └─────┬─────┘  │
│        │        │
│  ┌─────▼─────┐  │
│  │ PostgreSQL│  │
│  │  Storage  │  │
│  └─────┬─────┘  │
│        │        │
│  ┌─────▼──────────────┐
│  │ AI Service Layer   │
│  │ ┌────────────────┐ │
│  │ │ Skill Extractor│ │
│  │ └────────────────┘ │
│  │ ┌────────────────┐ │
│  │ │  Gap Analyzer  │ │
│  │ └────────────────┘ │
│  │ ┌────────────────┐ │
│  │ │  ATS Scorer    │ │
│  │ └────────────────┘ │
│  │ ┌────────────────┐ │
│  │ │Bullet Rewriter │ │
│  │ └────────────────┘ │
│  └─────┬──────────────┘
│        │
│  ┌─────▼─────┐
│  │  OpenAI   │
│  │    API    │
│  └───────────┘
└─────────────────┘
```

### Data Flow Sequence

#### Skill Extraction Flow
```
1. User uploads resume → Parse to raw text
2. Store raw text in PostgreSQL
3. Call AI Service → skill_extractor(raw_text)
4. AI Service → OpenAI API with structured prompt
5. OpenAI returns JSON: {skills: [], experience: [], education: []}
6. Validate and post-process response
7. Update database with extracted data
8. Return enriched resume object to user
```

#### Gap Analysis Flow
```
1. User requests gap analysis (resume_id + jd_id)
2. Retrieve resume and JD from PostgreSQL
3. Call AI Service → gap_analyzer(resume, jd)
4. AI Service → OpenAI API with comparison prompt
5. OpenAI returns: {missing_skills: [], weak_areas: [], recommendations: []}
6. Cache results in PostgreSQL (gap_analysis table)
7. Return analysis to user
```

---

## 4. Core AI Features

### 4.1 Skill Extraction

**Input**: Raw resume text (string)  
**Output**: Structured JSON with skills, experience, education

**Example Response**:
```json
{
  "skills": [
    {"name": "Python", "category": "Programming Language", "proficiency": "Advanced"},
    {"name": "FastAPI", "category": "Framework", "proficiency": "Intermediate"},
    {"name": "PostgreSQL", "category": "Database", "proficiency": "Intermediate"}
  ],
  "experience": [
    {
      "title": "Senior Software Engineer",
      "company": "Tech Corp",
      "duration": "2020-2023",
      "description": "Led backend development team",
      "key_achievements": ["Reduced API latency by 40%", "Mentored 5 junior developers"]
    }
  ],
  "education": [
    {
      "degree": "Bachelor of Science in Computer Science",
      "institution": "University of Technology",
      "graduation_year": "2019"
    }
  ]
}
```

**Implementation Strategy**:
- Use OpenAI JSON mode for guaranteed structured output
- Validate schema with Pydantic models
- Fallback to regex extraction if LLM fails

### 4.2 Gap Analysis

**Input**: Resume object + Job Description object  
**Output**: Gap analysis report

**Example Response**:
```json
{
  "match_score": 72,
  "missing_required_skills": [
    {"skill": "Kubernetes", "importance": "High", "found_in_jd": true},
    {"skill": "Docker", "importance": "High", "found_in_jd": true}
  ],
  "missing_preferred_skills": [
    {"skill": "AWS Lambda", "importance": "Medium"}
  ],
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
    "Highlight any cloud deployment experience",
    "Consider taking AWS certification"
  ]
}
```

### 4.3 ATS Scoring

**Input**: Resume object + Job Description object  
**Output**: ATS compatibility score and recommendations

**Example Response**:
```json
{
  "ats_score": 85,
  "keyword_match_percentage": 78,
  "format_score": 92,
  "issues": [
    {"type": "missing_keyword", "keyword": "agile methodology", "severity": "medium"},
    {"type": "formatting", "issue": "Tables may not parse correctly", "severity": "low"}
  ],
  "recommendations": [
    "Add 'agile' keyword in experience section",
    "Use standard section headers: Work Experience, Education, Skills",
    "Avoid headers and footers"
  ]
}
```

### 4.4 Bullet Point Rewriting

**Input**: Original bullet point + Target job description + Style preferences  
**Output**: Rewritten bullet point using STAR/XYZ format

**Example**:
- **Original**: "Worked on backend development"
- **Rewritten**: "Architected and implemented RESTful APIs using FastAPI, reducing response time by 40% and serving 10K+ daily requests across 15 microservices"

---

## 5. Prompt Engineering Strategy

### 5.1 Skill Extraction Prompt Template

```python
SKILL_EXTRACTION_PROMPT = """
You are an expert resume analyzer. Extract structured information from the following resume text.

RESUME TEXT:
{resume_text}

Extract the following information and return as valid JSON:

1. **skills**: List of technical and soft skills
   - name: skill name
   - category: Programming Language | Framework | Tool | Database | Soft Skill | Other
   - proficiency: Beginner | Intermediate | Advanced | Expert (infer from context)

2. **experience**: Work experience entries
   - title: job title
   - company: company name
   - duration: time period (e.g., "2020-2023" or "2 years")
   - description: brief role description
   - key_achievements: list of quantified achievements

3. **education**: Educational background
   - degree: degree name
   - institution: school/university name
   - graduation_year: year (string)
   - gpa: if mentioned

**Rules**:
- Extract ALL skills mentioned (technical and soft skills)
- Include tools, frameworks, languages, methodologies
- Infer proficiency from years of experience or context clues
- For experience, focus on measurable achievements
- Return empty arrays if no information found

Return ONLY valid JSON, no explanatory text.
"""
```

### 5.2 Gap Analysis Prompt Template

```python
GAP_ANALYSIS_PROMPT = """
You are an expert career advisor and resume consultant. Compare the candidate's resume against the job description and provide a detailed gap analysis.

CANDIDATE RESUME:
Skills: {resume_skills}
Experience: {resume_experience}
Education: {resume_education}

JOB DESCRIPTION:
{jd_text}
Required Skills: {jd_required_skills}
Preferred Skills: {jd_preferred_skills}

Provide a comprehensive analysis in valid JSON format:

1. **match_score** (0-100): Overall match percentage
2. **missing_required_skills**: Skills in JD but not in resume (critical for role)
3. **missing_preferred_skills**: Preferred skills candidate lacks
4. **strengths**: Areas where candidate strongly matches (2-5 points)
5. **weak_areas**: Areas needing improvement (2-5 points)
6. **recommendations**: Actionable advice for improving the resume (3-7 points)

**Analysis Guidelines**:
- Be honest but constructive
- Focus on actionable feedback
- Consider transferable skills
- Account for experience level
- Prioritize required over preferred skills

Return ONLY valid JSON, no explanatory text.
"""
```

### 5.3 ATS Scoring Prompt Template

```python
ATS_SCORING_PROMPT = """
You are an ATS (Applicant Tracking System) expert. Evaluate how well this resume would perform in automated screening systems.

RESUME TEXT:
{resume_text}

JOB DESCRIPTION:
{jd_text}

Analyze the resume for ATS compatibility and provide a detailed report in valid JSON format:

1. **ats_score** (0-100): Overall ATS compatibility score
2. **keyword_match_percentage**: Percentage of JD keywords found in resume
3. **format_score** (0-100): Resume formatting quality for ATS parsing
4. **issues**: List of problems ATS systems might encounter
   - type: missing_keyword | formatting | structure | other
   - description: what the issue is
   - severity: low | medium | high
5. **recommendations**: Specific improvements to boost ATS score

**ATS Evaluation Criteria**:
- Keyword matching (skills, tools, qualifications from JD)
- Standard section headers (Work Experience, Education, Skills)
- Simple formatting (no tables, columns, graphics)
- File format compatibility
- Contact information clarity
- Proper use of industry-standard terms

Return ONLY valid JSON, no explanatory text.
"""
```

### 5.4 Bullet Rewriting Prompt Template

```python
BULLET_REWRITE_PROMPT = """
You are an expert resume writer specializing in impactful bullet points. Rewrite the following bullet point to make it more compelling and ATS-friendly.

ORIGINAL BULLET POINT:
{original_bullet}

TARGET JOB DESCRIPTION:
{jd_keywords}

REWRITING GUIDELINES:
1. Use the STAR method (Situation, Task, Action, Result) or XYZ format (Accomplished X by doing Y resulting in Z)
2. Include quantifiable metrics (percentages, numbers, time savings)
3. Start with strong action verbs (Architected, Spearheaded, Optimized, Implemented)
4. Incorporate relevant keywords from the job description naturally
5. Keep it concise (1-2 lines, under 150 characters)
6. Focus on impact and results, not just responsibilities

Return ONLY the rewritten bullet point, nothing else.
"""
```

---

## 6. API Integration

### 6.1 OpenAI Client Setup

```python
# ai_service.py
from openai import OpenAI
import os
import json
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class AIService:
    """Centralized AI service for all LLM interactions"""
    
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.default_model = "gpt-4o-mini"
        self.advanced_model = "gpt-4o"
        self.max_retries = 3
        self.timeout = 30
    
    def call_llm(
        self,
        prompt: str,
        model: Optional[str] = None,
        response_format: Optional[Dict[str, str]] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> str:
        """
        Generic LLM call wrapper with error handling
        
        Args:
            prompt: The prompt to send to the LLM
            model: Model to use (defaults to gpt-4o-mini)
            response_format: {"type": "json_object"} for JSON mode
            temperature: Creativity (0-2, lower = more deterministic)
            max_tokens: Maximum response length
        
        Returns:
            str: LLM response text
        
        Raises:
            AIServiceError: If the API call fails after retries
        """
        model = model or self.default_model
        
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that provides structured, accurate responses."},
                    {"role": "user", "content": prompt}
                ],
                response_format=response_format,
                temperature=temperature,
                max_tokens=max_tokens,
                timeout=self.timeout
            )
            
            content = response.choices[0].message.content
            logger.info(f"LLM call successful. Model: {model}, Tokens: {response.usage.total_tokens}")
            
            return content
            
        except Exception as e:
            logger.error(f"LLM call failed: {str(e)}")
            raise AIServiceError(f"Failed to get LLM response: {str(e)}")
```

### 6.2 Configuration Management

```python
# config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # OpenAI Configuration
    OPENAI_API_KEY: str
    OPENAI_MODEL_DEFAULT: str = "gpt-4o-mini"
    OPENAI_MODEL_ADVANCED: str = "gpt-4o"
    OPENAI_MAX_TOKENS: int = 2000
    OPENAI_TEMPERATURE: float = 0.7
    OPENAI_TIMEOUT: int = 30
    
    # Rate Limiting
    AI_RATE_LIMIT_PER_MINUTE: int = 60
    AI_DAILY_BUDGET_USD: float = 10.0
    
    # Caching
    ENABLE_AI_RESPONSE_CACHE: bool = True
    CACHE_TTL_SECONDS: int = 3600
    
    class Config:
        env_file = ".env"

settings = Settings()
```

### 6.3 Environment Variables (.env.example)

```bash
# OpenAI Configuration
OPENAI_API_KEY=sk-proj-...your-api-key...
OPENAI_MODEL_DEFAULT=gpt-4o-mini
OPENAI_MODEL_ADVANCED=gpt-4o

# Database
POSTGRES_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/resumetailor

# Rate Limiting
AI_RATE_LIMIT_PER_MINUTE=60
AI_DAILY_BUDGET_USD=10.00

# Caching
ENABLE_AI_RESPONSE_CACHE=true
CACHE_TTL_SECONDS=3600
```

---

## 7. Error Handling & Resilience

### 7.1 Error Categories

| Error Type | Cause | Handling Strategy |
|------------|-------|-------------------|
| RateLimitError | Too many API calls | Exponential backoff + retry |
| InvalidRequestError | Malformed prompt | Validate input, log error |
| APIConnectionError | Network issues | Retry up to 3 times |
| APITimeoutError | Request too slow | Reduce max_tokens, retry |
| InsufficientQuotaError | No credits | Return graceful error to user |
| InvalidJSONError | LLM returned invalid JSON | Parse with fallback, retry with clarified prompt |

### 7.2 Retry Logic

```python
import time
from functools import wraps
from openai import RateLimitError, APIConnectionError, APITimeoutError

def retry_with_exponential_backoff(
    max_retries: int = 3,
    initial_delay: float = 1.0,
    exponential_base: float = 2.0
):
    """Decorator to retry function with exponential backoff"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            delay = initial_delay
            
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except (RateLimitError, APIConnectionError, APITimeoutError) as e:
                    if attempt == max_retries - 1:
                        raise
                    
                    logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay}s...")
                    time.sleep(delay)
                    delay *= exponential_base
            
        return wrapper
    return decorator
```

### 7.3 Fallback Strategies

```python
def extract_skills_with_fallback(resume_text: str) -> Dict[str, Any]:
    """
    Multi-level fallback for skill extraction:
    1. Try GPT-4o-mini with JSON mode
    2. If fails, try GPT-4o-mini without JSON mode + parse manually
    3. If fails, use regex-based extraction
    """
    try:
        # Level 1: Primary approach
        return extract_skills_with_llm(resume_text, json_mode=True)
    except InvalidJSONError:
        logger.warning("JSON mode failed, trying without JSON mode")
        try:
            # Level 2: Fallback
            return extract_skills_with_llm(resume_text, json_mode=False)
        except Exception as e:
            logger.error(f"LLM extraction failed: {e}. Using regex fallback")
            # Level 3: Last resort
            return extract_skills_with_regex(resume_text)
```

---

## 8. Cost Management

### 8.1 Cost Estimation

**GPT-4o Pricing** (as of May 2026):
- Input: $5.00 / 1M tokens
- Output: $15.00 / 1M tokens

**GPT-4o-mini Pricing**:
- Input: $0.15 / 1M tokens
- Output: $0.60 / 1M tokens

**Average Use Case Costs**:
| Operation | Avg Tokens | Model | Cost per Call |
|-----------|------------|-------|---------------|
| Skill Extraction | 1500 input + 500 output | GPT-4o-mini | $0.00053 |
| Gap Analysis | 2000 input + 800 output | GPT-4o | $0.022 |
| ATS Scoring | 2500 input + 600 output | GPT-4o-mini | $0.00075 |
| Bullet Rewrite | 300 input + 100 output | GPT-4o | $0.003 |

**Daily Volume Estimates** (100 users):
- 100 skill extractions: $0.053
- 50 gap analyses: $1.10
- 30 ATS scores: $0.023
- 200 bullet rewrites: $0.60
- **Total**: ~$1.78/day = **$53/month**

### 8.2 Cost Optimization Strategies

1. **Caching**: Cache LLM responses for 1 hour to avoid redundant calls
2. **Batching**: Combine multiple related operations in one prompt
3. **Smart Model Selection**: Use GPT-4o-mini for simple tasks, GPT-4o only when necessary
4. **Prompt Optimization**: Reduce unnecessary context to minimize tokens
5. **User Quotas**: Limit free tier users to N requests per day
6. **Pre-processing**: Use regex/rules to filter obvious cases before LLM

```python
# Example: Caching decorator
from functools import lru_cache
import hashlib

def cache_ai_response(ttl_seconds: int = 3600):
    """Cache AI responses based on input hash"""
    cache = {}
    
    def decorator(func):
        @wraps(func)
        def wrapper(text: str, *args, **kwargs):
            # Create cache key from input
            cache_key = hashlib.md5(text.encode()).hexdigest()
            
            # Check cache
            if cache_key in cache:
                cached_result, timestamp = cache[cache_key]
                if time.time() - timestamp < ttl_seconds:
                    logger.info("Returning cached AI response")
                    return cached_result
            
            # Call function and cache result
            result = func(text, *args, **kwargs)
            cache[cache_key] = (result, time.time())
            
            return result
        
        return wrapper
    return decorator
```

---

## 9. Security & Privacy

### 9.1 Data Privacy Considerations

**Sensitive Data Handling**:
- ✅ Resume contains PII (names, addresses, phone numbers, emails)
- ✅ Must comply with GDPR, CCPA
- ✅ User consent required for AI processing

**OpenAI Data Retention** (per their policy):
- API calls are NOT used for training by default
- Data retained for 30 days for abuse monitoring
- Zero data retention available for Enterprise tier

**Security Measures**:
1. **Anonymization**: Remove/mask PII before sending to LLM (optional feature)
2. **Encryption**: TLS for API calls, encrypted at rest in database
3. **API Key Management**: Store in environment variables, never commit to repo
4. **Audit Logging**: Log all AI API calls with user IDs for compliance
5. **User Consent**: Explicit opt-in for AI features with privacy notice

### 9.2 API Key Security

```python
# DO NOT hardcode API keys in code
# ❌ BAD
client = OpenAI(api_key="sk-proj-abc123...")

# ✅ GOOD
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Validate API key exists
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY environment variable not set")
```

### 9.3 Input Validation & Sanitization

```python
def validate_resume_text(text: str) -> str:
    """Validate and sanitize resume text before sending to LLM"""
    
    # Length validation
    if len(text) < 100:
        raise ValueError("Resume text too short (minimum 100 characters)")
    
    if len(text) > 50000:
        raise ValueError("Resume text too long (maximum 50,000 characters)")
    
    # Remove null bytes and control characters
    text = text.replace('\x00', '').replace('\r', '\n')
    
    # Optional: Remove/mask PII
    if settings.ANONYMIZE_PII:
        text = anonymize_pii(text)
    
    return text
```

---

## 10. Testing Strategy

### 10.1 Unit Tests

```python
# tests/test_ai_service.py

def test_skill_extraction_success(mock_openai_client):
    """Test successful skill extraction"""
    mock_response = {
        "skills": [{"name": "Python", "category": "Programming Language", "proficiency": "Advanced"}],
        "experience": [],
        "education": []
    }
    mock_openai_client.return_value = json.dumps(mock_response)
    
    result = extract_skills("Sample resume text with Python experience")
    
    assert len(result["skills"]) == 1
    assert result["skills"][0]["name"] == "Python"

def test_skill_extraction_invalid_json(mock_openai_client):
    """Test handling of invalid JSON response"""
    mock_openai_client.return_value = "This is not JSON"
    
    # Should fallback to regex extraction
    result = extract_skills("Sample resume with Python and Java")
    
    assert "skills" in result
    assert len(result["skills"]) >= 0  # May extract 0 or more skills

def test_skill_extraction_rate_limit(mock_openai_client):
    """Test rate limit handling"""
    mock_openai_client.side_effect = RateLimitError("Rate limit exceeded")
    
    with pytest.raises(RateLimitError):
        extract_skills("Sample resume text")

def test_gap_analysis_matching(mock_openai_client):
    """Test gap analysis with high match"""
    mock_response = {
        "match_score": 85,
        "missing_required_skills": [],
        "strengths": ["Strong Python skills"],
        "recommendations": []
    }
    mock_openai_client.return_value = json.dumps(mock_response)
    
    resume = {"skills": ["Python", "FastAPI"]}
    jd = {"required_skills": ["Python"]}
    
    result = analyze_gap(resume, jd)
    
    assert result["match_score"] >= 80
    assert len(result["missing_required_skills"]) == 0
```

### 10.2 Integration Tests

```python
# tests/test_ai_integration.py

@pytest.mark.integration
def test_end_to_end_skill_extraction():
    """Test full skill extraction flow with real API"""
    resume_text = """
    John Doe
    Senior Software Engineer
    
    Skills: Python, FastAPI, PostgreSQL, Docker, Kubernetes
    Experience: 5 years in backend development
    """
    
    result = extract_skills(resume_text)
    
    assert "skills" in result
    assert any(skill["name"].lower() == "python" for skill in result["skills"])
    assert "experience" in result
    assert "education" in result

@pytest.mark.integration
def test_gap_analysis_real_data():
    """Test gap analysis with real resume and JD"""
    # Use actual test data
    resume = load_test_resume("sample_backend_engineer.json")
    jd = load_test_jd("backend_engineer_jd.json")
    
    result = analyze_gap(resume, jd)
    
    assert 0 <= result["match_score"] <= 100
    assert isinstance(result["missing_required_skills"], list)
    assert isinstance(result["recommendations"], list)
```

### 10.3 LLM Response Validation

```python
from pydantic import BaseModel, Field, validator
from typing import List, Optional

class Skill(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    category: str = Field(..., min_length=1, max_length=50)
    proficiency: str = Field(..., pattern="^(Beginner|Intermediate|Advanced|Expert)$")

class Experience(BaseModel):
    title: str
    company: str
    duration: str
    description: Optional[str] = None
    key_achievements: List[str] = []

class Education(BaseModel):
    degree: str
    institution: str
    graduation_year: str
    gpa: Optional[str] = None

class SkillExtractionResponse(BaseModel):
    skills: List[Skill]
    experience: List[Experience]
    education: List[Education]
    
    @validator('skills')
    def validate_skills_not_empty(cls, v):
        # At least warn if no skills found
        if len(v) == 0:
            logger.warning("No skills extracted from resume")
        return v

def parse_and_validate_llm_response(response_text: str) -> SkillExtractionResponse:
    """Parse LLM response and validate against schema"""
    try:
        data = json.loads(response_text)
        return SkillExtractionResponse(**data)
    except json.JSONDecodeError as e:
        raise InvalidJSONError(f"Failed to parse JSON: {e}")
    except ValidationError as e:
        raise SchemaValidationError(f"Response doesn't match schema: {e}")
```

---

## 11. Performance & Scalability

### 11.1 Performance Targets

| Metric | Target | Current | Notes |
|--------|--------|---------|-------|
| Skill Extraction Latency | < 3s | TBD | P95 |
| Gap Analysis Latency | < 5s | TBD | P95 |
| ATS Scoring Latency | < 4s | TBD | P95 |
| API Success Rate | > 99% | TBD | Including retries |
| Cache Hit Rate | > 30% | TBD | For duplicate requests |

### 11.2 Async Processing

For operations that don't need immediate results:

```python
from celery import Celery

celery_app = Celery('tasks', broker='redis://localhost:6379/0')

@celery_app.task
def extract_skills_async(resume_id: int):
    """Background task for skill extraction"""
    # Fetch resume from database
    resume = get_resume(resume_id)
    
    # Extract skills with LLM
    extracted_data = extract_skills(resume.raw_text)
    
    # Update database
    update_resume_skills(resume_id, extracted_data)
    
    logger.info(f"Skills extracted for resume {resume_id}")

# Usage in API endpoint
@app.post("/upload-resume/")
async def upload_resume(file: UploadFile):
    # Save resume to database
    resume = create_resume(filename, raw_text)
    
    # Trigger async extraction
    extract_skills_async.delay(resume.id)
    
    return {"id": resume.id, "status": "processing"}
```

### 11.3 Caching Strategy

```python
import redis
import json
from typing import Optional

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def get_cached_analysis(cache_key: str) -> Optional[dict]:
    """Retrieve cached analysis result"""
    cached = redis_client.get(cache_key)
    if cached:
        logger.info(f"Cache hit: {cache_key}")
        return json.loads(cached)
    return None

def cache_analysis(cache_key: str, result: dict, ttl: int = 3600):
    """Cache analysis result with TTL"""
    redis_client.setex(cache_key, ttl, json.dumps(result))
    logger.info(f"Cached result: {cache_key}")

# Usage
def gap_analysis_with_cache(resume_id: int, jd_id: int):
    cache_key = f"gap_analysis:{resume_id}:{jd_id}"
    
    # Check cache
    cached_result = get_cached_analysis(cache_key)
    if cached_result:
        return cached_result
    
    # Perform analysis
    result = perform_gap_analysis(resume_id, jd_id)
    
    # Cache result
    cache_analysis(cache_key, result)
    
    return result
```

---

## 12. Implementation Roadmap

### Phase 1: Core AI Service (Week 2)
- [ ] Create `ai_service.py` module with OpenAI client wrapper
- [ ] Implement skill extraction with prompt template
- [ ] Add error handling and retry logic
- [ ] Create Pydantic models for response validation
- [ ] Write unit tests with mocked OpenAI responses
- [ ] Integration test with real OpenAI API

### Phase 2: Database Integration (Week 2)
- [ ] Update `models.py` to store AI-extracted data
- [ ] Create `enrichment.py` for post-processing LLM outputs
- [ ] Modify upload endpoints to trigger skill extraction
- [ ] Add caching layer (Redis or in-memory)

### Phase 3: Gap Analysis Feature (Week 3)
- [ ] Design gap analysis prompt template
- [ ] Implement `/gap-analysis/` endpoint
- [ ] Create response schema and validation
- [ ] Add tests for various resume-JD combinations
- [ ] Implement result caching

### Phase 4: ATS Scoring Feature (Week 3)
- [ ] Design ATS scoring algorithm (hybrid: rules + LLM)
- [ ] Implement `/ats-score/` endpoint
- [ ] Create keyword matching logic
- [ ] Add formatting analysis
- [ ] Write comprehensive tests

### Phase 5: Production Readiness (Week 4)
- [ ] Implement rate limiting for AI endpoints
- [ ] Add monitoring and alerting (API costs, latency, errors)
- [ ] Set up async processing with Celery
- [ ] Create admin dashboard for usage tracking
- [ ] Performance optimization and load testing
- [ ] Security audit and PII anonymization

### Phase 6: Advanced Features (Future)
- [ ] Bullet point rewriting endpoint
- [ ] Resume optimization suggestions
- [ ] Interview question generation
- [ ] Multi-language support
- [ ] Alternative LLM provider integration (Claude, Gemini)

---

## Appendix A: Sample API Request/Response

### Skill Extraction Endpoint

**Request**:
```http
POST /extract-skills/
Content-Type: application/json

{
  "resume_id": 123
}
```

**Response**:
```json
{
  "resume_id": 123,
  "extracted_data": {
    "skills": [
      {
        "name": "Python",
        "category": "Programming Language",
        "proficiency": "Advanced",
        "years_of_experience": 5
      },
      {
        "name": "FastAPI",
        "category": "Framework",
        "proficiency": "Intermediate",
        "years_of_experience": 2
      }
    ],
    "experience": [
      {
        "title": "Senior Backend Engineer",
        "company": "Tech Startup Inc.",
        "duration": "2021-2023",
        "location": "San Francisco, CA",
        "description": "Led backend development for SaaS platform",
        "key_achievements": [
          "Reduced API latency by 45% through optimization",
          "Mentored team of 3 junior developers",
          "Implemented CI/CD pipeline reducing deployment time by 60%"
        ],
        "technologies_used": ["Python", "FastAPI", "PostgreSQL", "Docker"]
      }
    ],
    "education": [
      {
        "degree": "Bachelor of Science in Computer Science",
        "institution": "Stanford University",
        "graduation_year": "2018",
        "gpa": "3.8"
      }
    ]
  },
  "processing_time_ms": 2341,
  "model_used": "gpt-4o-mini"
}
```

---

## Appendix B: Error Codes

| Error Code | HTTP Status | Description | User Message |
|------------|-------------|-------------|--------------|
| AI_SERVICE_UNAVAILABLE | 503 | OpenAI API down | "AI service temporarily unavailable. Please try again." |
| AI_RATE_LIMIT_EXCEEDED | 429 | Too many requests | "You've reached the rate limit. Please wait before trying again." |
| AI_INVALID_RESPONSE | 500 | LLM returned invalid data | "Failed to process your request. Our team has been notified." |
| AI_TIMEOUT | 504 | Request took too long | "Request timed out. Please try with a shorter document." |
| AI_INSUFFICIENT_CREDITS | 402 | No API quota remaining | "Service quota exceeded. Please upgrade your plan." |
| AI_INAPPROPRIATE_CONTENT | 400 | Content violates OpenAI policy | "Content cannot be processed due to policy restrictions." |

---

## Document Change Log

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-05-01 | Technical Architect | Initial draft - comprehensive AI/ML integration design |

---

**Review & Approval**:
- [ ] Technical Architect
- [ ] AI/ML Engineer
- [ ] Security Engineer
- [ ] Product Manager

**Next Steps**: Proceed with Phase 1 implementation (Core AI Service)
