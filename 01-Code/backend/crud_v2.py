"""
CRUD operations for Resume Tailor V2
Supports user-centric operations with application tracking
"""
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from models_v2 import User, Resume, JobDescription, Application, GapAnalysis, ATSScore
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)

# ============= User CRUD Operations =============

def create_user(db: Session, name: str, email: str, phone: Optional[str] = None, 
                password_hash: Optional[str] = None) -> User:
    """Create a new user"""
    try:
        user = User(
            name=name,
            email=email,
            phone=phone,
            password_hash=password_hash
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        logger.info(f"Created user with ID: {user.id}, Email: {email}")
        return user
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Integrity error creating user (email may already exist): {e}")
        raise
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error creating user: {e}")
        raise

def get_user(db: Session, user_id: int) -> Optional[User]:
    """Retrieve a user by ID"""
    try:
        return db.query(User).filter(User.id == user_id).first()
    except SQLAlchemyError as e:
        logger.error(f"Database error retrieving user {user_id}: {e}")
        raise

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Retrieve a user by email"""
    try:
        return db.query(User).filter(User.email == email).first()
    except SQLAlchemyError as e:
        logger.error(f"Database error retrieving user by email {email}: {e}")
        raise

def get_or_create_default_user(db: Session) -> User:
    """Get or create the default user for anonymous sessions"""
    default_email = "default@resumetailor.local"
    user = get_user_by_email(db, default_email)
    if not user:
        user = create_user(db, name="Default User", email=default_email)
    return user

# ============= Resume CRUD Operations =============

def create_resume(db: Session, user_id: int, filename: str, parsed: Dict[str, Any]) -> Resume:
    """Create a new resume record"""
    try:
        resume = Resume(
            user_id=user_id,
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
        logger.info(f"Created resume with ID: {resume.id} for user: {user_id}")
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

def get_resumes_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Resume]:
    """Retrieve resumes for a specific user"""
    try:
        return db.query(Resume).filter(Resume.user_id == user_id).offset(skip).limit(limit).all()
    except SQLAlchemyError as e:
        logger.error(f"Database error retrieving resumes for user {user_id}: {e}")
        raise

# ============= Job Description CRUD Operations =============

def create_jd(db: Session, user_id: int, filename: Optional[str], parsed: Dict[str, Any],
              job_url: Optional[str] = None, title: Optional[str] = None, 
              company: Optional[str] = None) -> JobDescription:
    """Create a new job description record"""
    try:
        jd = JobDescription(
            user_id=user_id,
            filename=filename,
            job_url=job_url,
            title=title,
            company=company,
            raw_text=parsed.get("raw_text", ""),
            mandatory_skills=parsed.get("mandatory_skills", []),
            preferred_skills=parsed.get("preferred_skills", []),
            keywords=parsed.get("keywords", [])
        )
        db.add(jd)
        db.commit()
        db.refresh(jd)
        logger.info(f"Created JD with ID: {jd.id} for user: {user_id}")
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

def get_jds_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[JobDescription]:
    """Retrieve job descriptions for a specific user"""
    try:
        return db.query(JobDescription).filter(JobDescription.user_id == user_id).offset(skip).limit(limit).all()
    except SQLAlchemyError as e:
        logger.error(f"Database error retrieving JDs for user {user_id}: {e}")
        raise

# ============= Application CRUD Operations =============

def create_application(db: Session, user_id: int, resume_id: int, jd_id: int, 
                       status: str = "analyzed", notes: Optional[str] = None) -> Application:
    """Create a new application record"""
    try:
        application = Application(
            user_id=user_id,
            resume_id=resume_id,
            jd_id=jd_id,
            status=status,
            notes=notes
        )
        db.add(application)
        db.commit()
        db.refresh(application)
        logger.info(f"Created application with ID: {application.id}")
        return application
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Integrity error creating application: {e}")
        raise
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error creating application: {e}")
        raise

def get_application(db: Session, application_id: int) -> Optional[Application]:
    """Retrieve an application by ID"""
    try:
        return db.query(Application).filter(Application.id == application_id).first()
    except SQLAlchemyError as e:
        logger.error(f"Database error retrieving application {application_id}: {e}")
        raise

def get_applications_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Application]:
    """Retrieve applications for a specific user"""
    try:
        return db.query(Application).filter(Application.user_id == user_id)\
            .order_by(Application.applied_at.desc()).offset(skip).limit(limit).all()
    except SQLAlchemyError as e:
        logger.error(f"Database error retrieving applications for user {user_id}: {e}")
        raise

# ============= Gap Analysis CRUD Operations =============

def create_gap_analysis(db: Session, application_id: int, analysis_data: Dict[str, Any]) -> GapAnalysis:
    """Create a new gap analysis record"""
    try:
        gap_analysis = GapAnalysis(
            application_id=application_id,
            match_score=analysis_data.get("match_score", 0),
            missing_required_skills=analysis_data.get("missing_required_skills", []),
            missing_preferred_skills=analysis_data.get("missing_preferred_skills", []),
            strengths=analysis_data.get("strengths", []),
            weak_areas=analysis_data.get("weak_areas", []),
            recommendations=analysis_data.get("recommendations", []),
            detailed_analysis=analysis_data.get("detailed_analysis", "")
        )
        db.add(gap_analysis)
        db.commit()
        db.refresh(gap_analysis)
        logger.info(f"Created gap analysis with ID: {gap_analysis.id} for application: {application_id}")
        return gap_analysis
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Integrity error creating gap analysis: {e}")
        raise
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error creating gap analysis: {e}")
        raise

def get_gap_analysis_by_application(db: Session, application_id: int) -> Optional[GapAnalysis]:
    """Retrieve gap analysis for a specific application"""
    try:
        return db.query(GapAnalysis).filter(GapAnalysis.application_id == application_id).first()
    except SQLAlchemyError as e:
        logger.error(f"Database error retrieving gap analysis for application {application_id}: {e}")
        raise

# ============= ATS Score CRUD Operations =============

def create_ats_score(db: Session, application_id: int, score_data: Dict[str, Any]) -> ATSScore:
    """Create a new ATS score record"""
    try:
        ats_score = ATSScore(
            application_id=application_id,
            ats_score=score_data.get("ats_score", 0),
            keyword_match_percentage=score_data.get("keyword_match_percentage", 0),
            format_score=score_data.get("format_score", 0),
            matched_keywords=score_data.get("matched_keywords", []),
            missing_keywords=score_data.get("missing_keywords", []),
            issues=score_data.get("issues", []),
            recommendations=score_data.get("recommendations", []),
            detailed_analysis=score_data.get("detailed_analysis", "")
        )
        db.add(ats_score)
        db.commit()
        db.refresh(ats_score)
        logger.info(f"Created ATS score with ID: {ats_score.id} for application: {application_id}")
        return ats_score
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Integrity error creating ATS score: {e}")
        raise
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error creating ATS score: {e}")
        raise

def get_ats_score_by_application(db: Session, application_id: int) -> Optional[ATSScore]:
    """Retrieve ATS score for a specific application"""
    try:
        return db.query(ATSScore).filter(ATSScore.application_id == application_id).first()
    except SQLAlchemyError as e:
        logger.error(f"Database error retrieving ATS score for application {application_id}: {e}")
        raise

# ============= Combined Analysis Operations =============

def get_full_application_with_analyses(db: Session, application_id: int) -> Optional[Dict[str, Any]]:
    """Retrieve application with all related data (resume, JD, gap analysis, ATS score)"""
    try:
        application = get_application(db, application_id)
        if not application:
            return None
        
        gap_analysis = get_gap_analysis_by_application(db, application_id)
        ats_score = get_ats_score_by_application(db, application_id)
        
        return {
            "application": application,
            "resume": application.resume,
            "job_description": application.job_description,
            "gap_analysis": gap_analysis,
            "ats_score": ats_score
        }
    except SQLAlchemyError as e:
        logger.error(f"Database error retrieving full application data for {application_id}: {e}")
        raise
