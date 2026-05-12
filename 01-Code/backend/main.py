
import os
import shutil
import tempfile
import logging
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, Request, status, Form, BackgroundTasks, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from pydantic import BaseModel, HttpUrl, Field

from parsers.resume_parser import parse_resume
from parsers.jd_parser import parse_jd
from db import SessionLocal
import crud_v2
from job_scraper import fetch_jd_from_url
from ai_service import get_ai_service
from ai_models import AIServiceError
from rate_limiter import rate_limiter
from models_v2 import UsageLog

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
)
logger = logging.getLogger(__name__)

# Constants
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
ALLOWED_EXTENSIONS = ["pdf", "docx", "txt"]
ALLOWED_MIME_TYPES = {
    "pdf": [b"%PDF"],
    "docx": [b"PK\x03\x04"]  # ZIP file signature (DOCX is a ZIP)
    # Note: TXT files don't have a magic number, so we skip validation for them
}

app = FastAPI(
    title="Resume2Interview API",
    description="AI-powered resume optimization engine.",
    version="1.0.0"
)

# Rate limiting — protects against DoS and brute-force attacks
# default_limits applies to every route
limiter = Limiter(key_func=get_remote_address, default_limits=["60/minute"])
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CORS — explicit allowlist; never use '*' with credentials
# In development the frontend runs on localhost:5173 (Vite default)
# Set CORS_ORIGINS env var in production to your actual frontend URL(s)
_raw_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173")
ALLOWED_ORIGINS = [o.strip() for o in _raw_origins.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "Accept", "X-Analytics-Password"],
)

# Security headers middleware
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Content-Security-Policy"] = (
        "default-src 'none'; frame-ancestors 'none'"
    )
    return response

# Daily rate limiting middleware
@app.middleware("http")
async def daily_rate_limit_middleware(request: Request, call_next):
    """Apply daily rate limits to analysis endpoints"""
    # Only apply to analysis endpoints
    rate_limited_paths = ["/upload-resume/", "/gap-analysis/", "/ats-score/"]
    
    if any(request.url.path.startswith(path) for path in rate_limited_paths):
        try:
            await rate_limiter.check_rate_limit(request)
        except HTTPException as e:
            # Log rate limit event
            db = SessionLocal()
            try:
                ip = rate_limiter.get_client_ip(request)
                usage_log = UsageLog(
                    ip_address=ip,
                    user_agent=request.headers.get("user-agent"),
                    endpoint=request.url.path,
                    method=request.method,
                    status_code=429,
                    rate_limited=1
                )
                db.add(usage_log)
                db.commit()
            except Exception as log_error:
                logger.error(f"Failed to log rate limit event: {log_error}")
            finally:
                db.close()
            raise e
    
    response = await call_next(request)
    
    # Add rate limit headers if available
    if hasattr(request.state, "rate_limit_info"):
        info = request.state.rate_limit_info
        response.headers["X-RateLimit-Limit"] = str(info["limit"])
        response.headers["X-RateLimit-Remaining"] = str(info["remaining"])
        response.headers["X-RateLimit-Used"] = str(info["used"])
    
    return response

# Usage logging middleware
@app.middleware("http")
async def usage_logging_middleware(request: Request, call_next):
    """Log all API requests for analytics"""
    response = await call_next(request)
    
    # Log successful requests to analysis endpoints
    rate_limited_paths = ["/upload-resume/", "/gap-analysis/", "/ats-score/"]
    if any(request.url.path.startswith(path) for path in rate_limited_paths) and response.status_code < 400:
        db = SessionLocal()
        try:
            ip = rate_limiter.get_client_ip(request)
            usage_log = UsageLog(
                ip_address=ip,
                user_agent=request.headers.get("user-agent"),
                endpoint=request.url.path,
                method=request.method,
                status_code=response.status_code,
                rate_limited=0
            )
            db.add(usage_log)
            db.commit()
        except Exception as e:
            logger.error(f"Failed to log usage: {e}")
        finally:
            db.close()
    
    return response

# Middleware for request/response logging - TEMPORARILY DISABLED FOR DEBUGGING
# @app.middleware("http")
# async def log_requests(request: Request, call_next):
#     logger.info(f"{request.method} {request.url}")
#     response = await call_next(request)
#     logger.info(f"Status: {response.status_code}")
#     return response

# Helper function for standardized error responses
def error_response(error_code: str, message: str, details: Any = None) -> Dict[str, Any]:
    """Create standardized error response matching design specification"""
    return {
        "error_code": error_code,
        "message": message,
        "details": details
    }

# ===========================
# V2 Pydantic Models
# ===========================
class FetchJDRequest(BaseModel):
    """Request model for fetching JD from URL"""
    job_url: str = Field(..., description="URL of the job posting")
    
    class Config:
        json_schema_extra = {
            "example": {
                "job_url": "https://www.linkedin.com/jobs/view/1234567890/"
            }
        }

class FetchJDResponse(BaseModel):
    """Response model for fetched JD"""
    title: str
    company: str
    raw_text: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "Senior Software Engineer",
                "company": "Google",
                "raw_text": "We are looking for a Senior Software Engineer..."
            }
        }


# File validation functions
def validate_file_size(content: bytes, filename: str) -> None:
    """Validate file size does not exceed limit"""
    file_size = len(content)
    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=error_response(
                "FILE_TOO_LARGE",
                f"File size exceeds {MAX_FILE_SIZE / 1024 / 1024:.0f} MB limit",
                f"Received: {file_size / 1024 / 1024:.1f} MB"
            )
        )
    logger.info(f"File size validated: {filename} ({file_size / 1024:.1f} KB)")

def validate_file_extension(filename: str) -> str:
    """Validate file extension and return it"""
    if not filename or "." not in filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_response(
                "INVALID_FILE_TYPE",
                "File must have a valid extension",
                "Supported: PDF, DOCX, TXT"
            )
        )
    
    ext = filename.split('.')[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_response(
                "INVALID_FILE_TYPE",
                "Only PDF, DOCX, and TXT files are supported",
                f"Received: .{ext}"
            )
        )
    return ext

def validate_file_content(content: bytes, expected_ext: str, filename: str) -> None:
    """Validate file content matches expected type (magic number validation)"""
    if expected_ext not in ALLOWED_MIME_TYPES:
        return
    
    magic_numbers = ALLOWED_MIME_TYPES[expected_ext]
    is_valid = any(content.startswith(magic) for magic in magic_numbers)
    
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_response(
                "INVALID_FILE_TYPE",
                f"File content does not match .{expected_ext} format",
                "File may be corrupted or have incorrect extension"
            )
        )
    logger.info(f"File content validated: {filename} is valid {expected_ext.upper()}")

@app.get("/")
@limiter.limit("60/minute")
def read_root(request: Request):
    """Health check endpoint"""
    return {"message": "Resume2Interview API is running."}


@app.get("/debug/db-config")
def debug_db_config():
    """Show database configuration for debugging Railway deployment"""
    import db
    from sqlalchemy import inspect, text
    
    # Get environment variables
    database_url = os.getenv("DATABASE_URL", "NOT_SET")
    postgres_url = os.getenv("POSTGRES_URL", "NOT_SET")
    
    # Mask password for security
    def mask_password(url: str) -> str:
        if url == "NOT_SET":
            return url
        try:
            parts = url.split("@")
            if len(parts) == 2:
                user_pass = parts[0].split("//")[1]
                if ":" in user_pass:
                    user = user_pass.split(":")[0]
                    return f"postgresql://{user}:***@{parts[1]}"
            return url[:20] + "***"
        except:
            return "ERROR_PARSING_URL"
    
    # Check what's actually being used
    actual_url = str(db.engine.url)
    
    # Check tables
    try:
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        table_count = len(tables)
    except Exception as e:
        tables = []
        table_count = f"ERROR: {str(e)}"
    
    # Try to query alembic_version
    alembic_version = "N/A"
    try:
        with db.engine.connect() as conn:
            result = conn.execute(text("SELECT version_num FROM alembic_version"))
            version_row = result.fetchone()
            if version_row:
                alembic_version = version_row[0]
    except Exception as e:
        alembic_version = f"ERROR: {str(e)}"
    
    return {
        "environment_variables": {
            "DATABASE_URL": mask_password(database_url),
            "POSTGRES_URL": mask_password(postgres_url),
        },
        "actual_connection": mask_password(actual_url),
        "database": {
            "table_count": table_count,
            "tables": tables,
            "alembic_version": alembic_version
        }
    }


@app.get("/debug/env-check")
def debug_env_check():
    """Check all critical environment variables"""
    def mask_value(key: str, value: str) -> str:
        if value == "NOT_SET":
            return value
        # Mask sensitive values
        if any(x in key.upper() for x in ["PASSWORD", "KEY", "SECRET", "TOKEN", "URL"]):
            if len(value) > 10:
                return f"{value[:8]}***{value[-4:]}"
            return "***"
        return value
    
    critical_vars = [
        "DATABASE_URL",
        "POSTGRES_URL", 
        "CORS_ORIGINS",
        "ANALYTICS_PASSWORD",
        "OPENAI_API_KEY",
        "PORT",
        "RAILWAY_ENVIRONMENT"
    ]
    
    env_status = {}
    for var in critical_vars:
        value = os.getenv(var, "NOT_SET")
        env_status[var] = {
            "set": value != "NOT_SET",
            "value": mask_value(var, value),
            "length": len(value) if value != "NOT_SET" else 0
        }
    
    return {
        "variables": env_status,
        "all_env_count": len(os.environ),
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/debug/password-check")
def debug_password_check(x_analytics_password: str = Header(None)):
    """Debug endpoint to check password matching"""
    expected = os.getenv("ANALYTICS_PASSWORD", "admin123")
    received = x_analytics_password or "NOT_PROVIDED"
    
    return {
        "expected_password": {
            "length": len(expected),
            "first_char": expected[0] if expected else None,
            "last_char": expected[-1] if expected else None,
            "value_hash": hash(expected)
        },
        "received_password": {
            "provided": x_analytics_password is not None,
            "length": len(received) if x_analytics_password else 0,
            "first_char": received[0] if received and len(received) > 0 else None,
            "last_char": received[-1] if received and len(received) > 0 else None,
            "value_hash": hash(received) if x_analytics_password else None
        },
        "comparison": {
            "match": x_analytics_password == expected if x_analytics_password else False,
            "lengths_match": len(received) == len(expected) if x_analytics_password else False
        },
        "timestamp": datetime.utcnow().isoformat()
    }


@app.post("/test-simple/")
def test_simple():
    """Ultra simple test endpoint with no dependencies"""
    with open("debug_simple.log", "a") as f:
        f.write("SIMPLE ENDPOINT CALLED\n")
    return {"status": "success", "message": "Simple endpoint works"}


def _extract_resume_ai(resume_id: int, raw_text: str) -> None:
    """Background task: run AI skill/experience/education extraction after the upload response is sent."""
    db = SessionLocal()
    try:
        ai_service = get_ai_service()
        logger.info(f"[BG] Extracting skills for resume {resume_id}")
        extracted_data = ai_service.extract_skills(raw_text)

        # Update resume with extracted skills, experience, and education
        if extracted_data.skills:
            skills_list = [{"name": s.name, "category": s.category, "proficiency": s.proficiency} for s in extracted_data.skills]
            crud_v2.update_resume(db, resume_id, {"skills": skills_list})
            logger.info(f"[BG] Updated {len(skills_list)} skills for resume {resume_id}")

        if extracted_data.experience:
            experience_list = [e.model_dump() for e in extracted_data.experience]
            crud_v2.update_resume(db, resume_id, {"experience": experience_list})
            logger.info(f"[BG] Updated {len(experience_list)} experience entries for resume {resume_id}")

        if extracted_data.education:
            education_list = [e.model_dump() for e in extracted_data.education]
            crud_v2.update_resume(db, resume_id, {"education": education_list})
            logger.info(f"[BG] Updated {len(education_list)} education entries for resume {resume_id}")

        # Update user table with extracted contact information
        if extracted_data.contact_info:
            resume = crud_v2.get_resume(db, resume_id)
            if resume and resume.user_id:
                user_updates = {}
                contact = extracted_data.contact_info
                
                # Update name if provided and not already set
                if contact.name:
                    user_updates["name"] = contact.name
                
                # Update email if provided and different from current
                if contact.email:
                    user_updates["email"] = contact.email
                
                # Update phone if provided
                if contact.phone:
                    user_updates["phone"] = contact.phone
                
                # Update last title/company from most recent position
                if contact.current_title:
                    user_updates["last_title"] = contact.current_title
                
                if contact.current_company:
                    user_updates["last_company"] = contact.current_company
                
                # Update user if there are any changes
                if user_updates:
                    # Add timestamp for when analysis was performed
                    user_updates["last_analysis_date"] = datetime.now(timezone.utc)
                    crud_v2.update_user(db, resume.user_id, user_updates)
                    logger.info(f"[BG] Updated user {resume.user_id} with contact info: {list(user_updates.keys())}")

    except AIServiceError as e:
        logger.error(f"[BG] AI extraction failed for resume {resume_id}: {str(e)}")
    except Exception as e:
        logger.error(f"[BG] Unexpected error during AI extraction for resume {resume_id}: {str(e)}")
    finally:
        db.close()


@app.post("/upload-resume/")
@limiter.limit("30/minute")
async def upload_resume(
    request: Request,
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    user_email: Optional[str] = Form(None),  # V2: Optional user context
    db: Session = Depends(get_db)
):
    """
    Upload and parse a resume file (PDF or DOCX).
    Returns parsed resume data with database ID.
    
    V2: Supports optional user_email parameter for user-centric tracking.
    
    - **file**: Resume file (PDF or DOCX, max 10 MB)
    - **user_email**: (Optional) User email for V2 multi-user support
    """
    try:
        # Validate filename
        if not file.filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_response("INVALID_FILE_TYPE", "No filename provided", None)
            )
        
        # Read file content
        file_content = await file.read()
        
        # Validate file size
        validate_file_size(file_content, file.filename)
        
        # Validate file extension
        ext = validate_file_extension(file.filename)
        
        # Validate file content (magic numbers)
        validate_file_content(file_content, ext, file.filename)
        
        # Save to temporary file for parsing
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{ext}") as tmp:
            tmp.write(file_content)
            temp_path = tmp.name
        
        try:
            # Parse resume
            logger.info(f"Parsing resume: {file.filename}")
            result = parse_resume(temp_path, ext)
            
            # V2: Get or create user if user_email provided
            user_id = None
            if user_email:
                user = crud_v2.get_user_by_email(db, user_email)
                if not user:
                    user = crud_v2.get_or_create_default_user(db)
                    logger.info(f"Using default user for resume upload (email not found: {user_email})")
                user_id = user.id
                
                # Store in database using V2 CRUD
                resume = crud_v2.create_resume(db, user_id, file.filename, result)
                logger.info(f"Resume stored with ID: {resume.id} for user: {user_id}")
            else:
                # V1 compatibility: Use default user
                user = crud_v2.get_or_create_default_user(db)
                user_id = user.id
                resume = crud_v2.create_resume(db, user.id, file.filename, result)
                logger.info(f"Resume stored with ID: {resume.id} (V1 mode)")
            
            # Schedule AI extraction as a background task so response returns immediately
            background_tasks.add_task(_extract_resume_ai, resume.id, result["raw_text"])
            logger.info(f"[BG] AI extraction queued for resume {resume.id}")

            return {
                "id": resume.public_id,
                "filename": resume.filename,
                "parsed": result,
                "user_id": user_id,
                "extracted": None,
                "ai_status": "processing"
            }
                
        except ValueError as e:
            # Parsing errors
            logger.error(f"Parsing error for {file.filename}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=error_response(
                    "PARSING_ERROR",
                    "Failed to parse resume content",
                    str(e)
                )
            )
        except Exception as e:
            # Unexpected errors
            logger.error(f"Unexpected error processing {file.filename}: {str(e)}")
            logger.exception("Full traceback:")  # Log full stack trace
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=error_response(
                    "INTERNAL_SERVER_ERROR",
                    "An unexpected error occurred while processing your file",
                    str(e)  # Include error details for debugging
                )
            )
        finally:
            # Always cleanup temp file
            if os.path.exists(temp_path):
                os.remove(temp_path)
                
    except HTTPException:
        # Re-raise HTTP exceptions (already have proper status codes)
        raise
    except Exception as e:
        # Catch any other unexpected errors
        logger.error(f"Unexpected error in upload_resume: {str(e)}")
        logger.exception("Full traceback:")  # Log full stack trace
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response(
                "INTERNAL_SERVER_ERROR",
                "An unexpected error occurred",
                str(e)  # Include error details for debugging
            )
        )

@app.post("/upload-jd/")
@limiter.limit("30/minute")
async def upload_jd(
    request: Request, 
    file: UploadFile = File(...), 
    user_email: Optional[str] = Form(None),  # V2: Optional user context
    job_url: Optional[str] = Form(None),  # V2: Optional job URL
    title: Optional[str] = Form(None),  # V2: Optional job title
    company: Optional[str] = Form(None),  # V2: Optional company name
    db: Session = Depends(get_db)
):
    """
    Upload and parse a job description file (PDF or DOCX).
    Returns parsed JD data with database ID.
    
    V2: Supports optional user_email, job_url, title, and company parameters.
    
    - **file**: Job description file (PDF or DOCX, max 10 MB)
    - **user_email**: (Optional) User email for V2 multi-user support
    - **job_url**: (Optional) URL of the job posting
    - **title**: (Optional) Job title
    - **company**: (Optional) Company name
    """
    try:
        # Validate filename
        if not file.filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_response("INVALID_FILE_TYPE", "No filename provided", None)
            )
        
        # Read file content
        file_content = await file.read()
        
        # Validate file size
        validate_file_size(file_content, file.filename)
        
        # Validate file extension
        ext = validate_file_extension(file.filename)
        
        # Validate file content (magic numbers)
        validate_file_content(file_content, ext, file.filename)
        
        # Save to temporary file for parsing
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{ext}") as tmp:
            tmp.write(file_content)
            temp_path = tmp.name
        
        try:
            # Parse job description
            logger.info(f"Parsing JD: {file.filename}")
            result = parse_jd(temp_path, ext)
            
            # V2: Get or create user if user_email provided
            user_id = None
            if user_email:
                user = crud_v2.get_user_by_email(db, user_email)
                if not user:
                    user = crud_v2.get_or_create_default_user(db)
                    logger.info(f"Using default user for JD upload (email not found: {user_email})")
                user_id = user.id
                
                # Store in database using V2 CRUD
                jd = crud_v2.create_jd(db, user_id, file.filename, result, 
                                      job_url=job_url, title=title, company=company)
                logger.info(f"JD stored with ID: {jd.id} for user: {user_id}")
            else:
                # V1 compatibility: Use default user
                user = crud_v2.get_or_create_default_user(db)
                user_id = user.id
                jd = crud_v2.create_jd(db, user.id, file.filename, result, 
                                      job_url=job_url, title=title, company=company)
                logger.info(f"JD stored with ID: {jd.id} (V1 mode)")
            
            response = {
                "id": jd.public_id,
                "filename": jd.filename,
                "parsed": result,
                "user_id": user_id
            }
            
            # V2: Include additional fields if available
            if job_url:
                response["job_url"] = job_url
            if title:
                response["title"] = title
            if company:
                response["company"] = company
                
            return response
            
        except ValueError as e:
            # Parsing errors
            logger.error(f"Parsing error for {file.filename}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=error_response(
                    "PARSING_ERROR",
                    "Failed to parse job description content",
                    str(e)
                )
            )
        except Exception as e:
            # Unexpected errors
            logger.error(f"Unexpected error processing {file.filename}: {str(e)}")
            logger.exception("Full traceback:")  # Log full stack trace
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=error_response(
                    "INTERNAL_SERVER_ERROR",
                    "An unexpected error occurred while processing your file",
                    str(e)  # Include error details for debugging
                )
            )
        finally:
            # Always cleanup temp file
            if os.path.exists(temp_path):
                os.remove(temp_path)
                
    except HTTPException:
        # Re-raise HTTP exceptions (already have proper status codes)
        raise
    except Exception as e:
        # Catch any other unexpected errors
        logger.error(f"Unexpected error in upload_jd: {str(e)}")
        logger.exception("Full traceback:")  # Log full stack trace
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response(
                "INTERNAL_SERVER_ERROR",
                "An unexpected error occurred",
                str(e)  # Include error details for debugging
            )
        )
@app.get("/resume/{resume_public_id}")
@limiter.limit("60/minute")
def get_resume(request: Request, resume_public_id: str, db: Session = Depends(get_db)):
    """
    Retrieve a previously uploaded resume by public UUID.
    """
    try:
        resume = crud_v2.get_resume_by_public_id(db, resume_public_id)
        if not resume:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=error_response(
                    "NOT_FOUND",
                    f"Resume not found",
                    None
                )
            )
        
        return {
            "id": resume.public_id,
            "filename": resume.filename,
            "raw_text": resume.raw_text,
            "skills": resume.skills,
            "experience": resume.experience,
            "education": resume.education,
            "tools": resume.tools,
            "created_at": resume.upload_date.isoformat() if resume.upload_date else None,
            "updated_at": resume.updated_at.isoformat() if resume.updated_at else None
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving resume {resume_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response(
                "INTERNAL_SERVER_ERROR",
                "An unexpected error occurred",
                None
            )
        )

@app.get("/jd/{jd_public_id}")
@limiter.limit("60/minute")
def get_jd(request: Request, jd_public_id: str, db: Session = Depends(get_db)):
    """
    Retrieve a previously uploaded job description by public UUID.
    """
    try:
        jd = crud_v2.get_jd_by_public_id(db, jd_public_id)
        if not jd:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=error_response(
                    "NOT_FOUND",
                    f"Job description not found",
                    None
                )
            )
        
        return {
            "id": jd.public_id,
            "filename": jd.filename,
            "raw_text": jd.raw_text,
            "mandatory_skills": jd.mandatory_skills,
            "preferred_skills": jd.preferred_skills,
            "keywords": jd.keywords,
            "created_at": jd.upload_date.isoformat() if jd.upload_date else None,
            "updated_at": jd.updated_at.isoformat() if jd.updated_at else None
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving JD {jd_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response(
                "INTERNAL_SERVER_ERROR",
                "An unexpected error occurred",
                None
            )
        )


@app.post("/gap-analysis-test")
def gap_analysis_test(resume_id: int, jd_id: int):
    """Super simple test endpoint with zero dependencies"""
    return {
        "test": "success",
        "resume_id": resume_id,
        "jd_id": jd_id,
        "message": "Simple endpoint works"
    }


@app.post("/gap-analysis/")
@limiter.limit("20/minute")
def gap_analysis(
    request: Request,
    resume_id: str,
    jd_id: str,
    user_email: Optional[str] = None,  # V2: Optional user context
    create_application: bool = False,  # V2: Create application record
    db: Session = Depends(get_db)
):
    """
    Analyze gaps between a resume and job description.
    
    - **resume_id**: Public UUID of the resume
    - **jd_id**: Public UUID of the job description
    """
    try:
        # Retrieve resume and JD from database using public UUIDs
        resume = crud_v2.get_resume_by_public_id(db, resume_id)
        if not resume:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=error_response("NOT_FOUND", "Resume not found", None)
            )
        
        jd = crud_v2.get_jd_by_public_id(db, jd_id)
        if not jd:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=error_response("NOT_FOUND", "Job description not found", None)
            )
        
        # V2: Get or create user if create_application is True
        application_id = None
        if create_application:
            user = None
            if user_email:
                user = crud_v2.get_user_by_email(db, user_email)
            if not user:
                user = crud_v2.get_or_create_default_user(db)
                
            # Create application record
            application = crud_v2.create_application(
                db, 
                user_id=user.id, 
                resume_id=resume_id, 
                jd_id=jd_id,
                status="analyzed"
            )
            application_id = application.id
            logger.info(f"Created application {application_id} for user {user.id}")
        
        # Prepare data for AI analysis
        resume_skills = resume.skills if resume.skills else []
        resume_experience = resume.raw_text[:1500]  # Truncated summary
        resume_education = resume.education if resume.education else []
        
        # Perform gap analysis using AI
        try:
            ai_service = get_ai_service()
            logger.info(f"Analyzing gap: resume {resume_id} vs JD {jd_id}")
            
            analysis = ai_service.analyze_gap(
                resume_skills=resume_skills,
                resume_experience=resume_experience,
                resume_education=resume_education,
                jd_text=jd.raw_text
            )
            
            logger.info(f"Gap analysis complete: Match score {analysis.match_score}%")
            
            # V2: Store gap analysis if application was created
            if application_id:
                gap_analysis_data = {
                    "match_score": analysis.match_score,
                    "missing_required_skills": analysis.missing_required_skills,
                    "missing_preferred_skills": analysis.missing_preferred_skills,
                    "strengths": analysis.strengths,
                    "weak_areas": analysis.weak_areas,
                    "recommendations": analysis.recommendations
                }
                crud_v2.create_gap_analysis(db, application_id, gap_analysis_data)
                logger.info(f"Stored gap analysis for application {application_id}")
                
                # Update user with missing skills
                if resume.user_id:
                    all_missing_skills = analysis.missing_required_skills + analysis.missing_preferred_skills
                    user_updates = {
                        "missing_skills": all_missing_skills
                    }
                    crud_v2.update_user(db, resume.user_id, user_updates)
                    logger.info(f"Updated user {resume.user_id} with {len(all_missing_skills)} missing skills")
            
            response = {
                "resume_id": resume_id,
                "jd_id": jd_id,
                "analysis": {
                    "match_score": analysis.match_score,
                    "missing_required_skills": analysis.missing_required_skills,
                    "missing_preferred_skills": analysis.missing_preferred_skills,
                    "strengths": analysis.strengths,
                    "weak_areas": analysis.weak_areas,
                    "recommendations": analysis.recommendations
                }
            }
            
            # V2: Include application_id if created
            if application_id:
                response["application_id"] = application_id
                
            return response
            
        except AIServiceError as e:
            logger.error(f"AI gap analysis failed: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=error_response(
                    "AI_SERVICE_UNAVAILABLE",
                    "Failed to perform gap analysis. Please try again.",
                    str(e)
                )
            )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in gap analysis: {str(e)}")
        logger.exception("Full traceback:")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response(
                "INTERNAL_SERVER_ERROR",
                "An unexpected error occurred",
                str(e)
            )
        )


@app.post("/ats-score/")
@limiter.limit("20/minute")
async def ats_score(request: Request, resume_id: str, jd_id: str, db: Session = Depends(get_db)):
    """
    Score a resume for ATS (Applicant Tracking System) compatibility.
    
    - **resume_id**: Public UUID of the resume
    - **jd_id**: Public UUID of the job description
    """
    try:
        # Retrieve resume and JD from database using public UUIDs
        resume = crud_v2.get_resume_by_public_id(db, resume_id)
        if not resume:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=error_response("NOT_FOUND", "Resume not found", None)
            )
        
        jd = crud_v2.get_jd_by_public_id(db, jd_id)
        if not jd:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=error_response("NOT_FOUND", "Job description not found",
                    None
                )
            )
        
        # Perform ATS scoring using AI
        try:
            ai_service = get_ai_service()
            logger.info(f"Scoring ATS compatibility: resume {resume_id} vs JD {jd_id}")
            
            scoring = ai_service.score_ats_compatibility(
                resume_text=resume.raw_text,
                jd_text=jd.raw_text
            )
            
            logger.info(f"ATS scoring complete: Score {scoring.ats_score}%")
            
            # Update user with ATS summary score
            if resume.user_id:
                user_updates = {
                    "ats_summary_score": scoring.ats_score
                }
                crud_v2.update_user(db, resume.user_id, user_updates)
                logger.info(f"Updated user {resume.user_id} with ATS score: {scoring.ats_score}")
            
            return {
                "resume_id": resume_id,
                "jd_id": jd_id,
                "scoring": {
                    "ats_score": scoring.ats_score,
                    "keyword_match_percentage": scoring.keyword_match_percentage,
                    "format_score": scoring.format_score,
                    "matched_keywords": scoring.matched_keywords,
                    "missing_keywords": scoring.missing_keywords,
                    "issues": [
                        {
                            "type": issue.type,
                            "description": issue.description,
                            "severity": issue.severity
                        }
                        for issue in scoring.issues
                    ],
                    "recommendations": scoring.recommendations
                }
            }
            
        except AIServiceError as e:
            logger.error(f"AI ATS scoring failed: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=error_response(
                    "AI_SERVICE_UNAVAILABLE",
                    "Failed to perform ATS scoring. Please try again.",
                    str(e)
                )
            )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in ATS scoring: {str(e)}")
        logger.exception("Full traceback:")  # This will log the full stack trace
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response(
                "INTERNAL_SERVER_ERROR",
                "An unexpected error occurred",
                str(e)  # Include error details in development
            )
        )


# ===========================
# V2 API Endpoints
# ===========================

@app.post("/v2/fetch-jd-from-url/", response_model=FetchJDResponse)
async def fetch_jd_from_url_endpoint(request: FetchJDRequest):
    """
    V2: Fetch job description from a URL.
    Supports LinkedIn, Naukri, Indeed, Monster, and Glassdoor.
    
    - **job_url**: URL of the job posting
    """
    try:
        logger.info(f"Fetching JD from URL: {request.job_url}")
        
        # Use the job scraper to fetch JD
        result = fetch_jd_from_url(request.job_url)
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=error_response(
                    "SCRAPING_ERROR",
                    "Failed to fetch job description from the provided URL",
                    "Unable to extract job information. The URL may be invalid or the site structure may have changed."
                )
            )
        
        logger.info(f"Successfully fetched JD: {result.get('title', 'Unknown')} at {result.get('company', 'Unknown')}")
        
        return FetchJDResponse(
            title=result.get("title", ""),
            company=result.get("company", ""),
            raw_text=result.get("raw_text", "")
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error fetching JD from URL: {str(e)}")
        logger.exception("Full traceback:")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response(
                "INTERNAL_SERVER_ERROR",
                "An unexpected error occurred while fetching the job description",
                str(e)
            )
        )


@app.get("/v2/applications/")
async def get_applications(
    user_email: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    V2: Get list of applications for a user.
    Returns paginated list of applications with resume and JD details.
    
    - **user_email**: (Optional) User email, defaults to default user
    - **skip**: Pagination offset (default: 0)
    - **limit**: Pagination limit (default: 100)
    """
    try:
        # Get or create user
        if user_email:
            user = crud_v2.get_user_by_email(db, user_email)
        else:
            user = crud_v2.get_or_create_default_user(db)
            
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=error_response("NOT_FOUND", f"User with email {user_email} not found", None)
            )
        
        # Get applications for user
        applications = crud_v2.get_applications_by_user(db, user.id, skip=skip, limit=limit)
        
        # Format response
        result = []
        for app in applications:
            # Get resume and JD details
            resume = crud_v2.get_resume(db, app.resume_id)
            jd = crud_v2.get_jd(db, app.jd_id)
            
            result.append({
                "application_id": app.id,
                "resume_id": app.resume_id,
                "resume_filename": resume.filename if resume else "Unknown",
                "jd_id": app.jd_id,
                "jd_title": jd.title if jd and jd.title else (jd.filename if jd else "Unknown"),
                "jd_company": jd.company if jd and jd.company else "Unknown",
                "applied_at": app.applied_at.isoformat() if app.applied_at else None,
                "status": app.status,
                "notes": app.notes
            })
        
        return {
            "user_id": user.id,
            "user_email": user.email,
            "total": len(result),
            "skip": skip,
            "limit": limit,
            "applications": result
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error getting applications: {str(e)}")
        logger.exception("Full traceback:")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response(
                "INTERNAL_SERVER_ERROR",
                "An unexpected error occurred",
                str(e)
            )
        )


@app.get("/v2/applications/{application_id}/")
async def get_application_details(
    application_id: int,
    db: Session = Depends(get_db)
):
    """
    V2: Get detailed information about a specific application.
    Includes resume, JD, gap analysis, and ATS score if available.
    
    - **application_id**: Database ID of the application
    """
    try:
        # Get application
        application = crud_v2.get_application(db, application_id)
        if not application:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=error_response("NOT_FOUND", f"Application with ID {application_id} not found", None)
            )
        
        # Get resume and JD
        resume = crud_v2.get_resume(db, application.resume_id)
        jd = crud_v2.get_jd(db, application.jd_id)
        
        # Get gap analysis if exists
        gap_analysis = crud_v2.get_gap_analysis_by_application(db, application_id)
        
        # Get ATS score if exists
        ats_score = crud_v2.get_ats_score_by_application(db, application_id)
        
        # Format response
        response = {
            "application": {
                "id": application.id,
                "user_id": application.user_id,
                "status": application.status,
                "applied_at": application.applied_at.isoformat() if application.applied_at else None,
                "notes": application.notes
            },
            "resume": {
                "id": resume.id if resume else None,
                "filename": resume.filename if resume else None,
                "skills": resume.skills if resume else [],
                "experience": resume.experience if resume else [],
                "education": resume.education if resume else [],
                "upload_date": resume.upload_date.isoformat() if resume and resume.upload_date else None
            } if resume else None,
            "job_description": {
                "id": jd.id if jd else None,
                "filename": jd.filename if jd else None,
                "title": jd.title if jd else None,
                "company": jd.company if jd else None,
                "job_url": jd.job_url if jd else None,
                "mandatory_skills": jd.mandatory_skills if jd else [],
                "preferred_skills": jd.preferred_skills if jd else [],
                "keywords": jd.keywords if jd else [],
                "upload_date": jd.upload_date.isoformat() if jd and jd.upload_date else None
            } if jd else None,
            "gap_analysis": {
                "match_score": gap_analysis.match_score,
                "missing_required_skills": gap_analysis.missing_required_skills,
                "missing_preferred_skills": gap_analysis.missing_preferred_skills,
                "strengths": gap_analysis.strengths,
                "weak_areas": gap_analysis.weak_areas,
                "recommendations": gap_analysis.recommendations,
                "created_at": gap_analysis.created_at.isoformat() if gap_analysis.created_at else None
            } if gap_analysis else None,
            "ats_score": {
                "ats_score": ats_score.ats_score,
                "keyword_match_percentage": ats_score.keyword_match_percentage,
                "format_score": ats_score.format_score,
                "matched_keywords": ats_score.matched_keywords,
                "missing_keywords": ats_score.missing_keywords,
                "issues": ats_score.issues,
                "recommendations": ats_score.recommendations,
                "created_at": ats_score.created_at.isoformat() if ats_score.created_at else None
            } if ats_score else None
        }
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error getting application details: {str(e)}")
        logger.exception("Full traceback:")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response(
                "INTERNAL_SERVER_ERROR",
                "An unexpected error occurred",
                str(e)
            )
        )


@app.delete("/v2/applications/{application_id}/")
async def delete_application(
    application_id: int,
    db: Session = Depends(get_db)
):
    """
    V2: Delete a specific application.
    
    - **application_id**: ID of the application to delete
    """
    try:
        success = crud_v2.delete_application(db, application_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=error_response("NOT_FOUND", f"Application {application_id} not found", None)
            )
        
        return {
            "success": True,
            "message": f"Application {application_id} deleted successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error deleting application: {str(e)}")
        logger.exception("Full traceback:")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response(
                "INTERNAL_SERVER_ERROR",
                "An unexpected error occurred",
                str(e)
            )
        )


@app.post("/v2/applications/bulk-delete/")
async def delete_applications_bulk(
    application_ids: List[int],
    db: Session = Depends(get_db)
):
    """
    V2: Delete multiple applications at once.
    
    - **application_ids**: List of application IDs to delete
    """
    try:
        if not application_ids:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_response("BAD_REQUEST", "No application IDs provided", None)
            )
        
        deleted_count = crud_v2.delete_applications_bulk(db, application_ids)
        
        return {
            "success": True,
            "deleted_count": deleted_count,
            "message": f"Successfully deleted {deleted_count} application(s)"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error bulk deleting applications: {str(e)}")
        logger.exception("Full traceback:")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response(
                "INTERNAL_SERVER_ERROR",
                "An unexpected error occurred",
                str(e)
            )
        )


# ===========================
# Usage Analytics Endpoints
# ===========================

# Password protection for analytics
async def verify_analytics_password(x_analytics_password: str = Header(None)):
    """
    Verify analytics dashboard password from environment variable
    """
    # Get password from environment variable (default: admin123)
    analytics_password = os.getenv("ANALYTICS_PASSWORD", "admin123")
    
    if x_analytics_password is None or x_analytics_password != analytics_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=error_response("UNAUTHORIZED", "Invalid or missing analytics password", "Please provide X-Analytics-Password header")
        )
    return True


@app.get("/api/analytics/usage-stats", dependencies=[Depends(verify_analytics_password)])
async def get_usage_stats(db: Session = Depends(get_db)):
    """
    Get current usage statistics from in-memory rate limiter
    Returns real-time counters for today
    """
    try:
        stats = rate_limiter.get_usage_stats()
        return {
            "success": True,
            "data": stats
        }
    except Exception as e:
        logger.error(f"Error fetching usage stats: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response("INTERNAL_SERVER_ERROR", "Failed to fetch usage statistics", str(e))
        )


@app.get("/api/analytics/usage-logs", dependencies=[Depends(verify_analytics_password)])
async def get_usage_logs(
    days: int = 7,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get historical usage logs from database
    
    - **days**: Number of days to look back (default: 7)
    - **limit**: Maximum number of records to return (default: 100)
    """
    try:
        from datetime import datetime, timedelta
        from sqlalchemy import and_, func as sql_func
        
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        # Get recent logs
        logs = db.query(UsageLog).filter(
            UsageLog.created_at >= cutoff_date
        ).order_by(UsageLog.created_at.desc()).limit(limit).all()
        
        # Get aggregate stats
        total_requests = db.query(sql_func.count(UsageLog.id)).filter(
            UsageLog.created_at >= cutoff_date
        ).scalar()
        
        rate_limited_count = db.query(sql_func.count(UsageLog.id)).filter(
            and_(
                UsageLog.created_at >= cutoff_date,
                UsageLog.rate_limited == 1
            )
        ).scalar()
        
        unique_ips = db.query(sql_func.count(sql_func.distinct(UsageLog.ip_address))).filter(
            UsageLog.created_at >= cutoff_date
        ).scalar()
        
        # Top IPs
        top_ips = db.query(
            UsageLog.ip_address,
            sql_func.count(UsageLog.id).label('count')
        ).filter(
            UsageLog.created_at >= cutoff_date
        ).group_by(UsageLog.ip_address).order_by(
            sql_func.count(UsageLog.id).desc()
        ).limit(10).all()
        
        # Endpoint distribution
        endpoint_stats = db.query(
            UsageLog.endpoint,
            sql_func.count(UsageLog.id).label('count')
        ).filter(
            UsageLog.created_at >= cutoff_date
        ).group_by(UsageLog.endpoint).order_by(
            sql_func.count(UsageLog.id).desc()
        ).all()
        
        return {
            "success": True,
            "data": {
                "period_days": days,
                "total_requests": total_requests or 0,
                "rate_limited_requests": rate_limited_count or 0,
                "unique_ips": unique_ips or 0,
                "top_ips": [{"ip": ip, "count": count} for ip, count in top_ips],
                "endpoint_distribution": [{"endpoint": ep, "count": count} for ep, count in endpoint_stats],
                "recent_logs": [
                    {
                        "id": log.id,
                        "ip_address": log.ip_address,
                        "endpoint": log.endpoint,
                        "method": log.method,
                        "status_code": log.status_code,
                        "rate_limited": bool(log.rate_limited),
                        "created_at": log.created_at.isoformat() if log.created_at else None
                    }
                    for log in logs
                ]
            }
        }
    except Exception as e:
        logger.error(f"Error fetching usage logs: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response("INTERNAL_SERVER_ERROR", "Failed to fetch usage logs", str(e))
        )


@app.get("/api/analytics/application-stats", dependencies=[Depends(verify_analytics_password)])
async def get_application_stats(
    days: int = 30,
    db: Session = Depends(get_db)
):
    """
    Get application analysis statistics
    
    - **days**: Number of days to look back (default: 30)
    
    Returns:
    - Total applications analyzed
    - Average match scores (Gap Analysis)
    - Average ATS scores
    - Most common missing skills
    - Top companies/job titles
    - Daily analysis trends
    """
    try:
        from datetime import datetime, timedelta
        from sqlalchemy import and_, func as sql_func, desc
        from models_v2 import Application, GapAnalysis, ATSScore, JobDescription, User
        
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        # Total applications
        total_applications = db.query(sql_func.count(Application.id)).filter(
            Application.created_at >= cutoff_date
        ).scalar() or 0
        
        # Unique users who ran analyses
        unique_users = db.query(sql_func.count(sql_func.distinct(Application.user_id))).filter(
            Application.created_at >= cutoff_date
        ).scalar() or 0
        
        # Average match score from Gap Analysis
        avg_match_score = db.query(sql_func.avg(GapAnalysis.match_score)).join(
            Application, Application.id == GapAnalysis.application_id
        ).filter(
            Application.created_at >= cutoff_date
        ).scalar()
        avg_match_score = round(avg_match_score, 1) if avg_match_score else 0
        
        # Average ATS score
        avg_ats_score = db.query(sql_func.avg(ATSScore.ats_score)).join(
            Application, Application.id == ATSScore.application_id
        ).filter(
            Application.created_at >= cutoff_date
        ).scalar()
        avg_ats_score = round(avg_ats_score, 1) if avg_ats_score else 0
        
        # Top companies (from job descriptions)
        top_companies = db.query(
            JobDescription.company,
            sql_func.count(Application.id).label('count')
        ).join(
            Application, Application.jd_id == JobDescription.id
        ).filter(
            and_(
                Application.created_at >= cutoff_date,
                JobDescription.company.isnot(None),
                JobDescription.company != ''
            )
        ).group_by(JobDescription.company).order_by(
            desc('count')
        ).limit(10).all()
        
        # Top job titles
        top_job_titles = db.query(
            JobDescription.title,
            sql_func.count(Application.id).label('count')
        ).join(
            Application, Application.jd_id == JobDescription.id
        ).filter(
            and_(
                Application.created_at >= cutoff_date,
                JobDescription.title.isnot(None),
                JobDescription.title != ''
            )
        ).group_by(JobDescription.title).order_by(
            desc('count')
        ).limit(10).all()
        
        # Most common missing skills
        # Aggregate missing_required_skills from all gap analyses
        gap_analyses = db.query(GapAnalysis).join(
            Application, Application.id == GapAnalysis.application_id
        ).filter(
            Application.created_at >= cutoff_date
        ).all()
        
        missing_skills_counter = {}
        for gap in gap_analyses:
            if gap.missing_required_skills:
                for skill in gap.missing_required_skills:
                    if isinstance(skill, str) and skill.strip():
                        skill_clean = skill.strip().lower()
                        missing_skills_counter[skill_clean] = missing_skills_counter.get(skill_clean, 0) + 1
        
        # Sort by frequency
        top_missing_skills = sorted(missing_skills_counter.items(), key=lambda x: x[1], reverse=True)[:15]
        
        # Daily trend (applications per day)
        daily_trend = db.query(
            sql_func.date(Application.created_at).label('date'),
            sql_func.count(Application.id).label('count')
        ).filter(
            Application.created_at >= cutoff_date
        ).group_by(
            sql_func.date(Application.created_at)
        ).order_by('date').all()
        
        # Score distribution (Gap Analysis)
        score_ranges = {
            "0-20": 0,
            "21-40": 0,
            "41-60": 0,
            "61-80": 0,
            "81-100": 0
        }
        
        scores = db.query(GapAnalysis.match_score).join(
            Application, Application.id == GapAnalysis.application_id
        ).filter(
            Application.created_at >= cutoff_date
        ).all()
        
        for score_tuple in scores:
            score = score_tuple[0]
            if score is not None:
                if score <= 20:
                    score_ranges["0-20"] += 1
                elif score <= 40:
                    score_ranges["21-40"] += 1
                elif score <= 60:
                    score_ranges["41-60"] += 1
                elif score <= 80:
                    score_ranges["61-80"] += 1
                else:
                    score_ranges["81-100"] += 1
        
        return {
            "success": True,
            "data": {
                "period_days": days,
                "total_applications": total_applications,
                "unique_users": unique_users,
                "avg_match_score": avg_match_score,
                "avg_ats_score": avg_ats_score,
                "top_companies": [{"company": company, "count": count} for company, count in top_companies],
                "top_job_titles": [{"title": title, "count": count} for title, count in top_job_titles],
                "top_missing_skills": [{"skill": skill, "count": count} for skill, count in top_missing_skills],
                "daily_trend": [{"date": date.isoformat() if date else None, "count": count} for date, count in daily_trend],
                "score_distribution": score_ranges
            }
        }
    except Exception as e:
        logger.error(f"Error fetching application stats: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response("INTERNAL_SERVER_ERROR", "Failed to fetch application statistics", str(e))
        )
