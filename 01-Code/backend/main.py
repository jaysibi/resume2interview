
import os
import shutil
import tempfile
import logging
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from parsers.resume_parser import parse_resume
from parsers.jd_parser import parse_jd
from db import SessionLocal
import crud
from ai_service import get_ai_service
from ai_models import AIServiceError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
)
logger = logging.getLogger(__name__)

# Constants
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
ALLOWED_EXTENSIONS = ["pdf", "docx"]
ALLOWED_MIME_TYPES = {
    "pdf": [b"%PDF"],
    "docx": [b"PK\x03\x04"]  # ZIP file signature (DOCX is a ZIP)
}

app = FastAPI(
    title="Resume Tailor API",
    description="AI-powered resume optimization engine.",
    version="1.0.0"
)

# Rate limiting - TEMPORARILY DISABLED FOR DEBUGGING
# limiter = Limiter(key_func=get_remote_address)
# app.state.limiter = limiter
# app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Environment-specific CORS configuration
ALLOWED_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
                "Supported: PDF, DOCX"
            )
        )
    
    ext = filename.split('.')[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_response(
                "INVALID_FILE_TYPE",
                "Only PDF and DOCX files are supported",
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
def read_root():
    """Health check endpoint"""
    return {"message": "Resume Tailor API is running."}


@app.post("/test-simple/")
def test_simple():
    """Ultra simple test endpoint with no dependencies"""
    with open("debug_simple.log", "a") as f:
        f.write("SIMPLE ENDPOINT CALLED\n")
    return {"status": "success", "message": "Simple endpoint works"}


@app.post("/upload-resume/")
# @limiter.limit("10/minute")  # Temporarily disabled for debugging
async def upload_resume(request: Request, file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Upload and parse a resume file (PDF or DOCX).
    Returns parsed resume data with database ID.
    
    - **file**: Resume file (PDF or DOCX, max 10 MB)
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
            
            # Store in database
            resume = crud.create_resume(db, file.filename, result)
            logger.info(f"Resume stored with ID: {resume.id}")
            
            # Extract skills, experience, and education using AI
            try:
                ai_service = get_ai_service()
                logger.info(f"Extracting skills for resume {resume.id}")
                extracted_data = ai_service.extract_skills(result["raw_text"])
                
                # Update database with extracted data
                if extracted_data.skills:
                    skills_list = [{"name": s.name, "category": s.category, "proficiency": s.proficiency} for s in extracted_data.skills]
                    crud.update_resume(db, resume.id, {"skills": skills_list})
                    logger.info(f"Updated {len(skills_list)} skills for resume {resume.id}")
                
                if extracted_data.experience:
                    experience_list = [e.model_dump() for e in extracted_data.experience]
                    crud.update_resume(db, resume.id, {"experience": experience_list})
                    logger.info(f"Updated {len(experience_list)} experience entries for resume {resume.id}")
                
                if extracted_data.education:
                    education_list = [e.model_dump() for e in extracted_data.education]
                    crud.update_resume(db, resume.id, {"education": education_list})
                    logger.info(f"Updated {len(education_list)} education entries for resume {resume.id}")
                
                # Return enriched data
                return {
                    "id": resume.id,
                    "filename": resume.filename,
                    "parsed": result,
                    "extracted": {
                        "skills": skills_list if extracted_data.skills else [],
                        "experience": experience_list if extracted_data.experience else [],
                        "education": education_list if extracted_data.education else []
                    }
                }
                
            except AIServiceError as e:
                # AI extraction failed - still return resume but log error
                logger.error(f"AI extraction failed for resume {resume.id}: {str(e)}")
                return {
                    "id": resume.id,
                    "filename": resume.filename,
                    "parsed": result,
                    "extracted": None,
                    "ai_error": "Skill extraction failed, but resume was saved successfully"
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
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=error_response(
                    "INTERNAL_SERVER_ERROR",
                    "An unexpected error occurred while processing your file",
                    None
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
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response(
                "INTERNAL_SERVER_ERROR",
                "An unexpected error occurred",
                None
            )
        )

@app.post("/upload-jd/")
# @limiter.limit("10/minute")  # Temporarily disabled for debugging
async def upload_jd(request: Request, file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Upload and parse a job description file (PDF or DOCX).
    Returns parsed JD data with database ID.
    
    - **file**: Job description file (PDF or DOCX, max 10 MB)
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
            
            # Store in database
            jd = crud.create_jd(db, file.filename, result)
            logger.info(f"JD stored with ID: {jd.id}")
            
            return {
                "id": jd.id,
                "filename": jd.filename,
                "parsed": result
            }
            
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
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=error_response(
                    "INTERNAL_SERVER_ERROR",
                    "An unexpected error occurred while processing your file",
                    None
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
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response(
                "INTERNAL_SERVER_ERROR",
                "An unexpected error occurred",
                None
            )
        )
@app.get("/resume/{resume_id}")
def get_resume(resume_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a previously uploaded resume by ID.
    
    - **resume_id**: Database ID of the resume
    """
    try:
        resume = crud.get_resume(db, resume_id)
        if not resume:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=error_response(
                    "NOT_FOUND",
                    f"Resume with ID {resume_id} not found",
                    None
                )
            )
        
        return {
            "id": resume.id,
            "filename": resume.filename,
            "raw_text": resume.raw_text,
            "skills": resume.skills,
            "experience": resume.experience,
            "education": resume.education,
            "tools": resume.tools,
            "created_at": resume.created_at.isoformat() if resume.created_at else None,
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

@app.get("/jd/{jd_id}")
def get_jd(jd_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a previously uploaded job description by ID.
    
    - **jd_id**: Database ID of the job description
    """
    try:
        jd = crud.get_jd(db, jd_id)
        if not jd:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=error_response(
                    "NOT_FOUND",
                    f"Job description with ID {jd_id} not found",
                    None
                )
            )
        
        return {
            "id": jd.id,
            "filename": jd.filename,
            "raw_text": jd.raw_text,
            "mandatory_skills": jd.mandatory_skills,
            "preferred_skills": jd.preferred_skills,
            "keywords": jd.keywords,
            "created_at": jd.created_at.isoformat() if jd.created_at else None,
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
def gap_analysis(resume_id: int, jd_id: int, db: Session = Depends(get_db)):
    """
    Analyze gaps between a resume and job description.
    Identifies missing skills, strengths, weaknesses, and provides recommendations.
    
    - **resume_id**: Database ID of the resume
    - **jd_id**: Database ID of the job description
    """
    try:
        # Retrieve resume and JD from database
        resume = crud.get_resume(db, resume_id)
        if not resume:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=error_response(
                    "NOT_FOUND",
                    f"Resume with ID {resume_id} not found",
                    None
                )
            )
        
        jd = crud.get_jd(db, jd_id)
        if not jd:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=error_response(
                    "NOT_FOUND",
                    f"Job description with ID {jd_id} not found",
                    None
                )
            )
        
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
            
            return {
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
# @limiter.limit("20/minute")  # Temporarily disabled for debugging
async def ats_score(request: Request, resume_id: int, jd_id: int, db: Session = Depends(get_db)):
    """
    Score a resume for ATS (Applicant Tracking System) compatibility.
    Analyzes keyword matching, formatting, and provides improvement recommendations.
    
    - **resume_id**: Database ID of the resume
    - **jd_id**: Database ID of the job description
    """
    try:
        # Retrieve resume and JD from database
        resume = crud.get_resume(db, resume_id)
        if not resume:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=error_response(
                    "NOT_FOUND",
                    f"Resume with ID {resume_id} not found",
                    None
                )
            )
        
        jd = crud.get_jd(db, jd_id)
        if not jd:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=error_response(
                    "NOT_FOUND",
                    f"Job description with ID {jd_id} not found",
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
