"""
AI Service Module - OpenAI Integration for Resume Analysis
Handles all LLM interactions with error handling and retry logic
"""
import os
import json
import time
import logging
from typing import Dict, Any, Optional
from functools import wraps
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from openai import OpenAI, RateLimitError, APIConnectionError, APITimeoutError
from pydantic import ValidationError

from ai_models import (
    SkillExtractionResponse,
    GapAnalysisResponse,
    ATSScoringResponse,
    AIServiceError,
    InvalidJSONError,
    SchemaValidationError,
    RateLimitExceededError
)
from prompts import (
    SKILL_EXTRACTION_PROMPT,
    GAP_ANALYSIS_PROMPT,
    ATS_SCORING_PROMPT,
    BULLET_REWRITE_PROMPT
)

logger = logging.getLogger(__name__)


def retry_with_exponential_backoff(
    max_retries: int = 3,
    initial_delay: float = 1.0,
    exponential_base: float = 2.0
):
    """
    Decorator to retry function with exponential backoff on transient errors
    
    Args:
        max_retries: Maximum number of retry attempts
        initial_delay: Initial delay in seconds before first retry
        exponential_base: Multiplier for delay on each retry
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            delay = initial_delay
            
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except (RateLimitError, APIConnectionError, APITimeoutError) as e:
                    if attempt == max_retries - 1:
                        logger.error(f"Max retries reached for {func.__name__}: {e}")
                        raise AIServiceError(f"Failed after {max_retries} attempts: {str(e)}")
                    
                    logger.warning(f"Attempt {attempt + 1} failed for {func.__name__}: {e}. Retrying in {delay}s...")
                    time.sleep(delay)
                    delay *= exponential_base
            
        return wrapper
    return decorator


class AIService:
    """
    Centralized AI service for all LLM interactions
    Provides skill extraction, gap analysis, ATS scoring, and bullet rewriting
    """
    
    def __init__(self):
        """Initialize OpenAI client and configuration"""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        
        self.client = OpenAI(api_key=api_key)
        self.default_model = os.getenv("OPENAI_MODEL_DEFAULT", "gpt-4o-mini")
        self.advanced_model = os.getenv("OPENAI_MODEL_ADVANCED", "gpt-4o")
        self.max_retries = 3
        self.timeout = int(os.getenv("OPENAI_TIMEOUT", "30"))
        self.max_tokens = int(os.getenv("OPENAI_MAX_TOKENS", "2000"))
        
        logger.info(f"AIService initialized with default model: {self.default_model}")
    
    @retry_with_exponential_backoff(max_retries=3)
    def _call_llm(
        self,
        prompt: str,
        model: Optional[str] = None,
        use_json_mode: bool = True,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Generic LLM call wrapper with error handling and retry logic
        
        Args:
            prompt: The prompt to send to the LLM
            model: Model to use (defaults to gpt-4o-mini)
            use_json_mode: Enable JSON mode for structured output
            temperature: Creativity level (0-2, lower = more deterministic)
            max_tokens: Maximum response length
        
        Returns:
            str: LLM response text
        
        Raises:
            AIServiceError: If the API call fails after retries
        """
        model = model or self.default_model
        max_tokens = max_tokens or self.max_tokens
        
        try:
            # Prepare request parameters
            request_params = {
                "model": model,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that provides structured, accurate responses in JSON format."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": temperature,
                "max_tokens": max_tokens,
                "timeout": self.timeout
            }
            
            # Add JSON mode if requested
            if use_json_mode:
                request_params["response_format"] = {"type": "json_object"}
            
            # Make API call
            response = self.client.chat.completions.create(**request_params)
            
            content = response.choices[0].message.content
            tokens_used = response.usage.total_tokens
            
            logger.info(
                f"LLM call successful. Model: {model}, Tokens: {tokens_used}, "
                f"JSON mode: {use_json_mode}"
            )
            
            return content
            
        except RateLimitError as e:
            logger.error(f"Rate limit exceeded: {e}")
            raise RateLimitExceededError(f"OpenAI rate limit exceeded: {str(e)}")
        except (APIConnectionError, APITimeoutError) as e:
            logger.error(f"Connection/timeout error: {e}")
            raise  # Will be caught by retry decorator
        except Exception as e:
            logger.error(f"Unexpected error in LLM call: {e}")
            raise AIServiceError(f"Failed to get LLM response: {str(e)}")
    
    def extract_skills(self, resume_text: str) -> SkillExtractionResponse:
        """
        Extract skills, experience, and education from resume text
        
        Args:
            resume_text: Raw resume text content
        
        Returns:
            SkillExtractionResponse: Validated structured data
        
        Raises:
            AIServiceError: If extraction fails
        """
        if not resume_text or len(resume_text.strip()) < 50:
            raise ValueError("Resume text is too short or empty")
        
        logger.info(f"Extracting skills from resume ({len(resume_text)} chars)")
        
        # Format prompt with resume text
        prompt = SKILL_EXTRACTION_PROMPT.format(resume_text=resume_text[:10000])
        
        try:
            # Call LLM with JSON mode
            response_text = self._call_llm(
                prompt=prompt,
                model=self.default_model,
                use_json_mode=True,
                temperature=0.3  # Lower temperature for more consistent extraction
            )
            
            # Parse and validate response
            response_data = json.loads(response_text)
            validated_response = SkillExtractionResponse(**response_data)
            
            logger.info(
                f"Skills extracted: {len(validated_response.skills)} skills, "
                f"{len(validated_response.experience)} experience entries, "
                f"{len(validated_response.education)} education entries"
            )
            
            return validated_response
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            raise InvalidJSONError(f"LLM returned invalid JSON: {str(e)}")
        except ValidationError as e:
            logger.error(f"Response validation failed: {e}")
            raise SchemaValidationError(f"Response doesn't match expected schema: {str(e)}")
        except Exception as e:
            logger.error(f"Skill extraction failed: {e}")
            raise AIServiceError(f"Failed to extract skills: {str(e)}")
    
    def analyze_gap(
        self,
        resume_skills: list,
        resume_experience: str,
        resume_education: list,
        jd_text: str
    ) -> GapAnalysisResponse:
        """
        Analyze gap between resume and job description
        
        Args:
            resume_skills: List of candidate skills
            resume_experience: Summary of experience
            resume_education: Educational background
            jd_text: Job description text
        
        Returns:
            GapAnalysisResponse: Validated gap analysis
        
        Raises:
            AIServiceError: If analysis fails
        """
        logger.info("Performing gap analysis")
        
        # Format data for prompt
        skills_str = ", ".join([s.get("name", s) if isinstance(s, dict) else s for s in resume_skills])
        education_str = ", ".join([
            e.get("degree", str(e)) if isinstance(e, dict) else str(e) 
            for e in resume_education
        ])
        
        # Format prompt
        prompt = GAP_ANALYSIS_PROMPT.format(
            resume_skills=skills_str[:500],
            resume_experience=resume_experience[:1000],
            resume_education=education_str[:300],
            jd_text=jd_text[:3000]
        )
        
        try:
            # Call LLM - use advanced model for better reasoning
            response_text = self._call_llm(
                prompt=prompt,
                model=self.advanced_model,
                use_json_mode=True,
                temperature=0.5
            )
            
            # Parse and validate
            response_data = json.loads(response_text)
            validated_response = GapAnalysisResponse(**response_data)
            
            logger.info(
                f"Gap analysis complete: Match score {validated_response.match_score}%, "
                f"{len(validated_response.missing_required_skills)} missing required skills"
            )
            
            return validated_response
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            raise InvalidJSONError(f"LLM returned invalid JSON: {str(e)}")
        except ValidationError as e:
            logger.error(f"Response validation failed: {e}")
            raise SchemaValidationError(f"Response doesn't match expected schema: {str(e)}")
        except Exception as e:
            logger.error(f"Gap analysis failed: {e}")
            raise AIServiceError(f"Failed to analyze gap: {str(e)}")
    
    def score_ats_compatibility(
        self,
        resume_text: str,
        jd_text: str
    ) -> ATSScoringResponse:
        """
        Score resume for ATS compatibility against job description
        
        Args:
            resume_text: Full resume text
            jd_text: Job description text
        
        Returns:
            ATSScoringResponse: Validated ATS scoring analysis
        
        Raises:
            AIServiceError: If scoring fails
        """
        logger.info("Scoring ATS compatibility")
        
        # Format prompt
        prompt = ATS_SCORING_PROMPT.format(
            resume_text=resume_text[:8000],
            jd_text=jd_text[:3000]
        )
        
        try:
            # Call LLM
            response_text = self._call_llm(
                prompt=prompt,
                model=self.default_model,
                use_json_mode=True,
                temperature=0.4
            )
            
            # Parse and validate
            response_data = json.loads(response_text)
            validated_response = ATSScoringResponse(**response_data)
            
            logger.info(
                f"ATS scoring complete: Score {validated_response.ats_score}%, "
                f"Keyword match {validated_response.keyword_match_percentage}%"
            )
            
            return validated_response
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            raise InvalidJSONError(f"LLM returned invalid JSON: {str(e)}")
        except ValidationError as e:
            logger.error(f"Response validation failed: {e}")
            raise SchemaValidationError(f"Response doesn't match expected schema: {str(e)}")
        except Exception as e:
            logger.error(f"ATS scoring failed: {e}")
            raise AIServiceError(f"Failed to score ATS compatibility: {str(e)}")
    
    def rewrite_bullet(
        self,
        original_bullet: str,
        jd_keywords: str
    ) -> str:
        """
        Rewrite resume bullet point for better impact and ATS optimization
        
        Args:
            original_bullet: Original bullet point text
            jd_keywords: Relevant keywords from job description
        
        Returns:
            str: Rewritten bullet point
        
        Raises:
            AIServiceError: If rewriting fails
        """
        logger.info("Rewriting bullet point")
        
        # Format prompt
        prompt = BULLET_REWRITE_PROMPT.format(
            original_bullet=original_bullet,
            jd_keywords=jd_keywords[:200]
        )
        
        try:
            # Call LLM - use advanced model for better writing quality
            rewritten_text = self._call_llm(
                prompt=prompt,
                model=self.advanced_model,
                use_json_mode=False,  # Plain text response
                temperature=0.8,  # Higher creativity for writing
                max_tokens=150
            )
            
            logger.info("Bullet point rewritten successfully")
            
            return rewritten_text.strip()
            
        except Exception as e:
            logger.error(f"Bullet rewriting failed: {e}")
            raise AIServiceError(f"Failed to rewrite bullet: {str(e)}")


# Global AI service instance (singleton pattern)
_ai_service_instance = None


def get_ai_service() -> AIService:
    """
    Get or create AI service singleton instance
    
    Returns:
        AIService: Singleton AI service instance
    """
    global _ai_service_instance
    
    if _ai_service_instance is None:
        _ai_service_instance = AIService()
    
    return _ai_service_instance
