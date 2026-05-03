"""
Pydantic models for AI/LLM response validation
"""
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from enum import Enum


class SkillCategory(str, Enum):
    """Valid skill categories"""
    PROGRAMMING_LANGUAGE = "Programming Language"
    FRAMEWORK = "Framework"
    TOOL = "Tool"
    DATABASE = "Database"
    SOFT_SKILL = "Soft Skill"
    OTHER = "Other"


class ProficiencyLevel(str, Enum):
    """Valid proficiency levels"""
    BEGINNER = "Beginner"
    INTERMEDIATE = "Intermediate"
    ADVANCED = "Advanced"
    EXPERT = "Expert"


class Skill(BaseModel):
    """Individual skill extracted from resume"""
    name: str = Field(..., min_length=1, max_length=100, description="Skill name")
    category: str = Field(..., min_length=1, max_length=50, description="Skill category")
    proficiency: str = Field(..., description="Proficiency level")

    @field_validator('proficiency')
    @classmethod
    def validate_proficiency(cls, v):
        valid_levels = ["Beginner", "Intermediate", "Advanced", "Expert"]
        if v not in valid_levels:
            # Default to Intermediate if invalid
            return "Intermediate"
        return v


class Experience(BaseModel):
    """Work experience entry"""
    title: str = Field(..., min_length=1, description="Job title")
    company: str = Field(..., min_length=1, description="Company name")
    duration: str = Field(..., description="Time period (e.g., '2020-2023')")
    description: Optional[str] = Field(None, description="Role description")
    key_achievements: List[str] = Field(default_factory=list, description="List of achievements")


class Education(BaseModel):
    """Educational background entry"""
    degree: str = Field(..., min_length=1, description="Degree name")
    institution: str = Field(..., min_length=1, description="School/university name")
    graduation_year: str = Field(..., description="Graduation year")
    gpa: Optional[str] = Field(None, description="GPA if mentioned")


class SkillExtractionResponse(BaseModel):
    """Complete response from skill extraction LLM call"""
    skills: List[Skill] = Field(default_factory=list)
    experience: List[Experience] = Field(default_factory=list)
    education: List[Education] = Field(default_factory=list)

    @field_validator('skills', 'experience', 'education', mode='before')
    @classmethod
    def validate_lists(cls, v):
        """Ensure lists are not None"""
        if v is None:
            return []
        return v


class IssueSeverity(str, Enum):
    """Severity levels for issues"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class IssueType(str, Enum):
    """Types of ATS issues"""
    KEYWORD = "keyword"
    FORMATTING = "formatting"
    STRUCTURE = "structure"


class ATSIssue(BaseModel):
    """Individual ATS compatibility issue"""
    type: str = Field(..., description="Issue type")
    description: str = Field(..., min_length=1, description="Detailed description")
    severity: str = Field(..., description="Issue severity")


class ATSScoringResponse(BaseModel):
    """ATS scoring analysis response"""
    ats_score: int = Field(..., ge=0, le=100, description="Overall ATS score (0-100)")
    keyword_match_percentage: int = Field(..., ge=0, le=100, description="Keyword match percentage")
    format_score: int = Field(..., ge=0, le=100, description="Format quality score")
    matched_keywords: List[str] = Field(default_factory=list, description="Keywords found in resume")
    missing_keywords: List[str] = Field(default_factory=list, description="Keywords missing from resume")
    issues: List[ATSIssue] = Field(default_factory=list, description="List of issues found")
    recommendations: List[str] = Field(default_factory=list, description="Improvement recommendations")


class GapAnalysisResponse(BaseModel):
    """Gap analysis comparing resume to job description"""
    match_score: int = Field(..., ge=0, le=100, description="Overall match score (0-100)")
    missing_required_skills: List[str] = Field(default_factory=list, description="Required skills not found")
    missing_preferred_skills: List[str] = Field(default_factory=list, description="Preferred skills not found")
    strengths: List[str] = Field(default_factory=list, description="Candidate strengths")
    weak_areas: List[str] = Field(default_factory=list, description="Areas needing improvement")
    recommendations: List[str] = Field(default_factory=list, description="Actionable recommendations")

    @field_validator('match_score')
    @classmethod
    def validate_match_score(cls, v):
        """Ensure match score is in valid range"""
        if v < 0:
            return 0
        if v > 100:
            return 100
        return v


# Exception classes for AI service errors
class AIServiceError(Exception):
    """Base exception for AI service errors"""
    pass


class InvalidJSONError(AIServiceError):
    """Raised when LLM returns invalid JSON"""
    pass


class SchemaValidationError(AIServiceError):
    """Raised when LLM response doesn't match expected schema"""
    pass


class RateLimitExceededError(AIServiceError):
    """Raised when API rate limit is exceeded"""
    pass


class InsufficientCreditsError(AIServiceError):
    """Raised when API quota is exhausted"""
    pass
