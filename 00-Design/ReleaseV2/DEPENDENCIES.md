# Resume Tailor Backend - Dependency & Impact Analysis

## Overview
This document lists all major dependencies (Python packages, system requirements, external services) for the backend, their purpose, and the impact of changes or failures. It also highlights integration points with the frontend and other system components.

---

## 1. Python Package Dependencies

### **Core Framework & API**
- **fastapi**: Main web framework for building RESTful APIs
- **uvicorn**: ASGI server for running FastAPI
- **pydantic**: Data validation and serialization (used by FastAPI)
- **python-dotenv**: Loads environment variables from `.env` files

### **Database & ORM**
- **sqlalchemy**: ORM for database models and queries
- **alembic**: Database migrations
- **psycopg2**: PostgreSQL database driver

### **AI & NLP**
- **openai**: OpenAI API client for GPT-4o-mini integration
- **python-docx**: DOCX file parsing (resume/JD extraction)
- **PyPDF2**: PDF file parsing (resume extraction)
- **nltk**: Natural Language Toolkit (tokenization, stopwords, etc.)

### **Utilities & Support**
- **requests**: HTTP requests (internal/external API calls)
- **loguru**: Advanced logging
- **python-multipart**: File upload support for FastAPI
- **passlib**: Password hashing (for future user auth)
- **bcrypt**: Password hashing backend
- **email-validator**: Email validation for user registration
- **pytest**: Testing framework

---

## 2. System & Environment Dependencies
- **Python 3.8+**: Required runtime
- **PostgreSQL**: Database server
- **OpenAI API Key**: For AI-powered features
- **.env file**: For environment variables (DB URL, API keys)

---

## 3. External Service Dependencies
- **OpenAI API**: All AI analysis (gap, ATS) depends on this
- **SMTP/Email** (future): For notifications

---

## 4. Integration Points
- **Frontend**: Communicates via REST API (CORS enabled)
- **E2E Testing**: Python-based test suite calls backend endpoints
- **Database**: All persistent data (resumes, JDs, users, analyses)

---

## 5. Impact Analysis

### **Critical Dependencies**
- **OpenAI API**: If unavailable, all AI analysis endpoints fail (gap analysis, ATS scoring)
- **PostgreSQL**: If unavailable, no data can be stored or retrieved
- **sqlalchemy/alembic**: Model or migration errors can break DB access
- **fastapi/uvicorn**: Core API will not run if these fail

### **File Parsing**
- **python-docx/PyPDF2**: If broken, resume/JD uploads will fail for DOCX/PDF

### **Security**
- **passlib/bcrypt**: Needed for secure password storage (future user auth)
- **python-dotenv**: If missing, environment variables may not load, breaking DB/API access

### **Testing**
- **pytest**: Needed for automated test execution

---

## 6. Change/Upgrade Impact
- **Major version upgrades** (FastAPI, SQLAlchemy, OpenAI, etc.) may require code changes
- **Database schema changes** require Alembic migrations and data migration planning
- **OpenAI API changes** may break AI integration or require prompt/model updates
- **Dependency vulnerabilities** (e.g., in requests, passlib) can impact security

---

## 7. Recommendations
- Pin dependency versions in `requirements.txt`
- Regularly update and test dependencies in a staging environment
- Monitor OpenAI API status and usage
- Use Alembic for all DB schema changes
- Add health checks for all critical services
- Document all integration points and environment variables

---

**End of Backend Dependency & Impact Analysis**
