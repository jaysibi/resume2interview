from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from models import Resume, JobDescription
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)

# ============= Resume CRUD Operations =============

def create_resume(db: Session, filename: str, parsed: Dict[str, Any]) -> Resume:
    """Create a new resume record in the database"""
    try:
        resume = Resume(
            filename=filename,
            raw_text=parsed.get("raw_text", ""),
            skills=parsed.get("skills", []),
            experience=parsed.get("experience", []),
            education=parsed.get("education", []),
            tools=parsed.get("tools", [])
        )
        db.add(resume)
        db.commit()
        db.refresh(resume)
        logger.info(f"Created resume with ID: {resume.id}")
        return resume
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Integrity error creating resume: {e}")
        raise
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error creating resume: {e}")
        raise

def get_resume(db: Session, resume_id: int) -> Optional[Resume]:
    """Retrieve a resume by ID"""
    try:
        return db.query(Resume).filter(Resume.id == resume_id).first()
    except SQLAlchemyError as e:
        logger.error(f"Database error retrieving resume {resume_id}: {e}")
        raise

def get_resumes(db: Session, skip: int = 0, limit: int = 100) -> List[Resume]:
    """Retrieve a list of resumes with pagination"""
    try:
        return db.query(Resume).offset(skip).limit(limit).all()
    except SQLAlchemyError as e:
        logger.error(f"Database error retrieving resumes: {e}")
        raise

def update_resume(db: Session, resume_id: int, updates: Dict[str, Any]) -> Optional[Resume]:
    """Update a resume by ID"""
    try:
        resume = db.query(Resume).filter(Resume.id == resume_id).first()
        if not resume:
            return None
        
        for key, value in updates.items():
            if hasattr(resume, key):
                setattr(resume, key, value)
        
        db.commit()
        db.refresh(resume)
        logger.info(f"Updated resume with ID: {resume_id}")
        return resume
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Integrity error updating resume {resume_id}: {e}")
        raise
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error updating resume {resume_id}: {e}")
        raise

def delete_resume(db: Session, resume_id: int) -> bool:
    """Delete a resume by ID"""
    try:
        resume = db.query(Resume).filter(Resume.id == resume_id).first()
        if not resume:
            return False
        
        db.delete(resume)
        db.commit()
        logger.info(f"Deleted resume with ID: {resume_id}")
        return True
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error deleting resume {resume_id}: {e}")
        raise

# ============= Job Description CRUD Operations =============

def create_jd(db: Session, filename: str, parsed: Dict[str, Any]) -> JobDescription:
    """Create a new job description record in the database"""
    try:
        jd = JobDescription(
            filename=filename,
            raw_text=parsed.get("raw_text", ""),
            mandatory_skills=parsed.get("mandatory_skills", []),
            preferred_skills=parsed.get("preferred_skills", []),
            keywords=parsed.get("keywords", [])
        )
        db.add(jd)
        db.commit()
        db.refresh(jd)
        logger.info(f"Created JD with ID: {jd.id}")
        return jd
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Integrity error creating JD: {e}")
        raise
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error creating JD: {e}")
        raise

def get_jd(db: Session, jd_id: int) -> Optional[JobDescription]:
    """Retrieve a job description by ID"""
    try:
        return db.query(JobDescription).filter(JobDescription.id == jd_id).first()
    except SQLAlchemyError as e:
        logger.error(f"Database error retrieving JD {jd_id}: {e}")
        raise

def get_jds(db: Session, skip: int = 0, limit: int = 100) -> List[JobDescription]:
    """Retrieve a list of job descriptions with pagination"""
    try:
        return db.query(JobDescription).offset(skip).limit(limit).all()
    except SQLAlchemyError as e:
        logger.error(f"Database error retrieving JDs: {e}")
        raise

def update_jd(db: Session, jd_id: int, updates: Dict[str, Any]) -> Optional[JobDescription]:
    """Update a job description by ID"""
    try:
        jd = db.query(JobDescription).filter(JobDescription.id == jd_id).first()
        if not jd:
            return None
        
        for key, value in updates.items():
            if hasattr(jd, key):
                setattr(jd, key, value)
        
        db.commit()
        db.refresh(jd)
        logger.info(f"Updated JD with ID: {jd_id}")
        return jd
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Integrity error updating JD {jd_id}: {e}")
        raise
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error updating JD {jd_id}: {e}")
        raise

def delete_jd(db: Session, jd_id: int) -> bool:
    """Delete a job description by ID"""
    try:
        jd = db.query(JobDescription).filter(JobDescription.id == jd_id).first()
        if not jd:
            return False
        
        db.delete(jd)
        db.commit()
        logger.info(f"Deleted JD with ID: {jd_id}")
        return True
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error deleting JD {jd_id}: {e}")
        raise
