import docx
import fitz  # PyMuPDF
import pdfplumber
from typing import Dict, Any
import logging
import re

logger = logging.getLogger(__name__)


def parse_pdf(file_path: str) -> str:
    """Extract text from PDF file"""
    try:
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text
    except Exception as e:
        logger.error(f"Error parsing PDF: {e}")
        raise ValueError(f"Failed to parse PDF file: {str(e)}")


def parse_docx(file_path: str) -> str:
    """Extract text from DOCX file"""
    try:
        doc = docx.Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
        return text
    except Exception as e:
        logger.error(f"Error parsing DOCX: {e}")
        raise ValueError(f"Failed to parse DOCX file: {str(e)}")


def normalize_text(text: str) -> str:
    """Clean and normalize extracted text"""
    if not text:
        return ""
    
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters that might cause issues
    text = text.replace('\x00', '')  # Remove null bytes
    
    # Strip leading/trailing whitespace
    text = text.strip()
    
    return text


def parse_jd(file_path: str, file_type: str) -> Dict[str, Any]:
    """
    Parse a job description file and extract structured data.
    
    Args:
        file_path: Path to the JD file
        file_type: File extension (pdf or docx)
    
    Returns:
        Dictionary with parsed JD data
    
    Raises:
        ValueError: If file cannot be parsed or content is invalid
    """
    try:
        # Parse based on file type
        if file_type == "pdf":
            text = parse_pdf(file_path)
        elif file_type == "docx":
            text = parse_docx(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
        
        # Normalize text
        text = normalize_text(text)
        
        # Validate extracted text
        if not text or len(text) < 10:
            raise ValueError("Extracted text is empty or too short. File may be corrupted or unreadable.")
        
        logger.info(f"Successfully parsed JD: {len(text)} characters extracted")
        
        # TODO: Integrate AI/ML extraction logic here
        # For now, return raw text with empty structured fields
        return {
            "raw_text": text,
            "mandatory_skills": [],
            "preferred_skills": [],
            "keywords": []
        }
        
    except ValueError:
        # Re-raise ValueError (already has descriptive message)
        raise
    except Exception as e:
        logger.error(f"Unexpected error parsing JD: {e}")
        raise ValueError(f"Failed to parse job description: {str(e)}")
