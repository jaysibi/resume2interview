from sqlalchemy import Column, Integer, String, Text, JSON, DateTime, func
from db import Base

class Resume(Base):
    __tablename__ = "resumes"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    raw_text = Column(Text, nullable=False)
    skills = Column(JSON, default=list, server_default='[]')
    experience = Column(JSON, default=list, server_default='[]')
    education = Column(JSON, default=list, server_default='[]')
    tools = Column(JSON, default=list, server_default='[]')
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class JobDescription(Base):
    __tablename__ = "job_descriptions"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    raw_text = Column(Text, nullable=False)
    mandatory_skills = Column(JSON, default=list, server_default='[]')
    preferred_skills = Column(JSON, default=list, server_default='[]')
    keywords = Column(JSON, default=list, server_default='[]')
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
