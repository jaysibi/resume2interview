"""
Database Models for Resume Tailor V2
User-centric schema with full application tracking and analytics support
"""
from sqlalchemy import Column, Integer, String, Text, JSON, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from db import Base
import uuid


def _new_uuid() -> str:
    return str(uuid.uuid4())


class User(Base):
    """User (job seeker) table"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    phone = Column(String(50), nullable=True)
    password_hash = Column(String(255), nullable=True)  # For future authentication
    
    # Contact and professional information extracted from resume
    last_title = Column(String(255), nullable=True)  # Current/most recent job title
    last_company = Column(String(255), nullable=True)  # Current/most recent company
    job_applying_for = Column(String(255), nullable=True)  # Target job title
    ats_summary_score = Column(Integer, nullable=True)  # Latest ATS score
    missing_skills = Column(JSON, default=list, server_default='[]')  # Skills gap
    last_analysis_date = Column(DateTime(timezone=True), nullable=True)  # Last resume analysis date
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    resumes = relationship("Resume", back_populates="user", cascade="all, delete-orphan")
    job_descriptions = relationship("JobDescription", back_populates="user", cascade="all, delete-orphan")
    applications = relationship("Application", back_populates="user", cascade="all, delete-orphan")


class Resume(Base):
    """Resume documents table"""
    __tablename__ = "resumes"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    public_id = Column(String(36), default=_new_uuid, unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    filename = Column(String(255), nullable=False)
    raw_text = Column(Text, nullable=False)
    skills = Column(JSON, default=list, server_default='[]')
    experience = Column(JSON, default=list, server_default='[]')
    education = Column(JSON, default=list, server_default='[]')
    tools = Column(JSON, default=list, server_default='[]')
    upload_date = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="resumes")
    applications = relationship("Application", back_populates="resume")


class JobDescription(Base):
    """Job description documents table"""
    __tablename__ = "job_descriptions"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    public_id = Column(String(36), default=_new_uuid, unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    filename = Column(String(255), nullable=True)  # Nullable for URL-fetched JDs
    job_url = Column(String(1000), nullable=True)  # Job posting URL if fetched
    raw_text = Column(Text, nullable=False)
    title = Column(String(500), nullable=True)  # Job title
    company = Column(String(500), nullable=True)  # Company name
    mandatory_skills = Column(JSON, default=list, server_default='[]')
    preferred_skills = Column(JSON, default=list, server_default='[]')
    keywords = Column(JSON, default=list, server_default='[]')
    upload_date = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="job_descriptions")
    applications = relationship("Application", back_populates="job_description")


class Application(Base):
    """Application tracking table - links user, resume, and job"""
    __tablename__ = "applications"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.id", ondelete="CASCADE"), nullable=False, index=True)
    jd_id = Column(Integer, ForeignKey("job_descriptions.id", ondelete="CASCADE"), nullable=False, index=True)
    applied_at = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String(50), default="analyzed")  # analyzed, applied, interview, offer, rejected, etc.
    notes = Column(Text, nullable=True)  # Optional user notes
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="applications")
    resume = relationship("Resume", back_populates="applications")
    job_description = relationship("JobDescription", back_populates="applications")
    gap_analysis = relationship("GapAnalysis", back_populates="application", uselist=False, cascade="all, delete-orphan")
    ats_score = relationship("ATSScore", back_populates="application", uselist=False, cascade="all, delete-orphan")
    
    # Composite index for querying applications by user and date
    __table_args__ = (
        Index('idx_user_applied_at', 'user_id', 'applied_at'),
    )


class GapAnalysis(Base):
    """Gap analysis results table"""
    __tablename__ = "gap_analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    match_score = Column(Integer, nullable=False)  # 0-100
    missing_required_skills = Column(JSON, default=list, server_default='[]')
    missing_preferred_skills = Column(JSON, default=list, server_default='[]')
    strengths = Column(JSON, default=list, server_default='[]')
    weak_areas = Column(JSON, default=list, server_default='[]')
    recommendations = Column(JSON, default=list, server_default='[]')
    detailed_analysis = Column(Text, nullable=True)  # Full AI analysis text
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    application = relationship("Application", back_populates="gap_analysis")


class ATSScore(Base):
    """ATS scoring results table"""
    __tablename__ = "ats_scores"
    
    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    ats_score = Column(Integer, nullable=False)  # 0-100
    keyword_match_percentage = Column(Integer, nullable=False)  # 0-100
    format_score = Column(Integer, nullable=False)  # 0-100
    matched_keywords = Column(JSON, default=list, server_default='[]')
    missing_keywords = Column(JSON, default=list, server_default='[]')
    issues = Column(JSON, default=list, server_default='[]')
    recommendations = Column(JSON, default=list, server_default='[]')
    detailed_analysis = Column(Text, nullable=True)  # Full AI analysis text
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    application = relationship("Application", back_populates="ats_score")


class UsageLog(Base):
    """Usage tracking for rate limiting and analytics"""
    __tablename__ = "usage_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    ip_address = Column(String(50), nullable=False, index=True)
    user_agent = Column(Text, nullable=True)
    endpoint = Column(String(255), nullable=False)
    method = Column(String(10), nullable=False)
    status_code = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    rate_limited = Column(Integer, default=0)  # 1 if request was rate limited
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    # Relationships
    user = relationship("User")
    
    # Composite index for date-based queries
    __table_args__ = (
        Index('idx_ip_date', 'ip_address', 'created_at'),
        Index('idx_date_endpoint', 'created_at', 'endpoint'),
    )
