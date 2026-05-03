"""
Data Validation and Loading Script
Validates resume parsing and optionally loads data into the database for testing
"""
import os
import sys
import csv
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from db import SessionLocal, engine, Base
import crud
from parsers.resume_parser import parse_resume
from ai_service import get_ai_service
from ai_models import AIServiceError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler('data_validation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Paths
DATA_DIR = Path(r"C:\Projects\ResumeTailor\02-Data")
CSV_FILE = DATA_DIR / "UpdatedResumeDataSet.csv"
PDF_DIR = DATA_DIR / "Resumes PDF"


class DataValidator:
    """Validates resume parsing and AI extraction"""
    
    def __init__(self):
        self.results = {
            "total_processed": 0,
            "parsing_success": 0,
            "parsing_failures": 0,
            "ai_extraction_success": 0,
            "ai_extraction_failures": 0,
            "errors": []
        }
        self.ai_service = None
    
    def validate_csv_parsing(self, limit: Optional[int] = None) -> Dict[str, Any]:
        """
        Validate parsing of resumes from CSV file
        
        Args:
            limit: Maximum number of resumes to process (None = all)
        
        Returns:
            Dict with validation results
        """
        logger.info(f"Starting CSV validation from: {CSV_FILE}")
        
        if not CSV_FILE.exists():
            logger.error(f"CSV file not found: {CSV_FILE}")
            return {"error": "CSV file not found"}
        
        try:
            with open(CSV_FILE, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                for idx, row in enumerate(reader):
                    if limit and idx >= limit:
                        break
                    
                    self.results["total_processed"] += 1
                    category = row.get("Category", "Unknown")
                    resume_text = row.get("Resume", "")
                    
                    # Validate resume text
                    if not resume_text or len(resume_text.strip()) < 50:
                        self.results["parsing_failures"] += 1
                        self.results["errors"].append({
                            "row": idx + 1,
                            "category": category,
                            "error": "Resume text too short or empty"
                        })
                        continue
                    
                    # Simulate parsing (text is already extracted)
                    try:
                        # Basic validation
                        word_count = len(resume_text.split())
                        char_count = len(resume_text)
                        
                        logger.info(
                            f"Row {idx + 1} ({category}): "
                            f"{word_count} words, {char_count} chars"
                        )
                        
                        self.results["parsing_success"] += 1
                        
                    except Exception as e:
                        self.results["parsing_failures"] += 1
                        self.results["errors"].append({
                            "row": idx + 1,
                            "category": category,
                            "error": str(e)
                        })
            
            logger.info(f"CSV validation complete: {self.results['parsing_success']}/{self.results['total_processed']} successful")
            return self.results
            
        except Exception as e:
            logger.error(f"Error reading CSV: {e}")
            return {"error": str(e)}
    
    def validate_pdf_parsing(self, category: str, limit: Optional[int] = None) -> Dict[str, Any]:
        """
        Validate parsing of PDF files from a specific category
        
        Args:
            category: Category folder name (e.g., "Data Science")
            limit: Maximum number of PDFs to process
        
        Returns:
            Dict with validation results
        """
        category_dir = PDF_DIR / category
        
        if not category_dir.exists():
            logger.error(f"Category directory not found: {category_dir}")
            return {"error": "Category directory not found"}
        
        logger.info(f"Validating PDFs in: {category_dir}")
        
        pdf_files = list(category_dir.glob("*.pdf"))
        if not pdf_files:
            logger.warning(f"No PDF files found in {category_dir}")
            return {"warning": "No PDF files found"}
        
        logger.info(f"Found {len(pdf_files)} PDF files")
        
        for idx, pdf_path in enumerate(pdf_files):
            if limit and idx >= limit:
                break
            
            self.results["total_processed"] += 1
            
            try:
                logger.info(f"Processing: {pdf_path.name}")
                
                # Parse PDF
                result = parse_resume(str(pdf_path), "pdf")
                
                # Validate result
                if not result or not result.get("raw_text"):
                    raise ValueError("No text extracted from PDF")
                
                word_count = len(result["raw_text"].split())
                logger.info(f"  ✓ Extracted {word_count} words")
                
                self.results["parsing_success"] += 1
                
            except Exception as e:
                logger.error(f"  ✗ Failed: {str(e)}")
                self.results["parsing_failures"] += 1
                self.results["errors"].append({
                    "file": pdf_path.name,
                    "category": category,
                    "error": str(e)
                })
        
        logger.info(f"PDF validation complete: {self.results['parsing_success']}/{self.results['total_processed']} successful")
        return self.results
    
    def validate_ai_extraction(self, resume_texts: List[str]) -> Dict[str, Any]:
        """
        Validate AI skill extraction on sample resumes
        
        Args:
            resume_texts: List of resume text samples
        
        Returns:
            Dict with validation results
        """
        logger.info(f"Validating AI extraction on {len(resume_texts)} samples")
        
        try:
            self.ai_service = get_ai_service()
        except Exception as e:
            logger.error(f"Failed to initialize AI service: {e}")
            return {"error": "AI service initialization failed. Check OPENAI_API_KEY."}
        
        for idx, resume_text in enumerate(resume_texts):
            self.results["total_processed"] += 1
            
            try:
                logger.info(f"Extracting skills from sample {idx + 1}...")
                
                # Extract skills
                extracted = self.ai_service.extract_skills(resume_text[:10000])
                
                # Validate extraction
                skills_count = len(extracted.skills)
                experience_count = len(extracted.experience)
                education_count = len(extracted.education)
                
                logger.info(
                    f"  ✓ Extracted: {skills_count} skills, "
                    f"{experience_count} experience, {education_count} education"
                )
                
                self.results["ai_extraction_success"] += 1
                
            except AIServiceError as e:
                logger.error(f"  ✗ AI extraction failed: {str(e)}")
                self.results["ai_extraction_failures"] += 1
                self.results["errors"].append({
                    "sample": idx + 1,
                    "error": str(e)
                })
        
        logger.info(
            f"AI validation complete: {self.results['ai_extraction_success']}/"
            f"{self.results['total_processed']} successful"
        )
        return self.results
    
    def print_summary(self):
        """Print validation summary"""
        print("\n" + "="*80)
        print("VALIDATION SUMMARY")
        print("="*80)
        print(f"Total Processed: {self.results['total_processed']}")
        print(f"Parsing Success: {self.results['parsing_success']}")
        print(f"Parsing Failures: {self.results['parsing_failures']}")
        print(f"AI Extraction Success: {self.results['ai_extraction_success']}")
        print(f"AI Extraction Failures: {self.results['ai_extraction_failures']}")
        print(f"\nTotal Errors: {len(self.results['errors'])}")
        
        if self.results['errors']:
            print("\nFirst 10 Errors:")
            for error in self.results['errors'][:10]:
                print(f"  - {error}")
        
        print("="*80)


def load_sample_data_to_db(limit: int = 5):
    """
    Load sample resumes from CSV into database
    
    Args:
        limit: Number of resumes to load
    """
    logger.info(f"Loading {limit} sample resumes into database...")
    
    if not CSV_FILE.exists():
        logger.error(f"CSV file not found: {CSV_FILE}")
        return
    
    db = SessionLocal()
    loaded_count = 0
    
    try:
        with open(CSV_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for idx, row in enumerate(reader):
                if idx >= limit:
                    break
                
                category = row.get("Category", "Unknown")
                resume_text = row.get("Resume", "")
                
                if not resume_text or len(resume_text.strip()) < 50:
                    continue
                
                try:
                    # Create resume entry
                    filename = f"{category}_sample_{idx + 1}.txt"
                    result = {"raw_text": resume_text, "skills": [], "experience": [], "education": [], "tools": []}
                    
                    resume = crud.create_resume(db, filename, result)
                    logger.info(f"Loaded: {filename} (ID: {resume.id})")
                    
                    loaded_count += 1
                    
                except Exception as e:
                    logger.error(f"Failed to load resume {idx + 1}: {e}")
        
        logger.info(f"Successfully loaded {loaded_count} resumes into database")
        
    except Exception as e:
        logger.error(f"Error loading data: {e}")
    finally:
        db.close()


def main():
    """Main validation workflow"""
    print("\n" + "="*80)
    print("RESUME DATA VALIDATION TOOL")
    print("="*80)
    print("\nOptions:")
    print("1. Validate CSV parsing (quick check)")
    print("2. Validate PDF parsing (specific category)")
    print("3. Validate AI extraction (requires OpenAI API key)")
    print("4. Load sample data to database")
    print("5. Run full validation suite")
    print("="*80)
    
    choice = input("\nEnter choice (1-5): ").strip()
    
    validator = DataValidator()
    
    if choice == "1":
        limit = input("Number of resumes to validate (default 10): ").strip()
        limit = int(limit) if limit else 10
        validator.validate_csv_parsing(limit=limit)
        validator.print_summary()
    
    elif choice == "2":
        print("\nAvailable categories:")
        categories = [d.name for d in PDF_DIR.iterdir() if d.is_dir()]
        for i, cat in enumerate(categories[:10], 1):
            print(f"  {i}. {cat}")
        
        category = input("\nEnter category name: ").strip()
        limit = input("Number of PDFs to validate (default 5): ").strip()
        limit = int(limit) if limit else 5
        
        validator.validate_pdf_parsing(category, limit=limit)
        validator.print_summary()
    
    elif choice == "3":
        # Load sample texts from CSV
        logger.info("Loading sample resumes for AI validation...")
        sample_texts = []
        
        with open(CSV_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for idx, row in enumerate(reader):
                if idx >= 3:  # Test with 3 samples
                    break
                resume_text = row.get("Resume", "")
                if resume_text and len(resume_text.strip()) >= 50:
                    sample_texts.append(resume_text)
        
        if not sample_texts:
            logger.error("No valid resume texts found")
            return
        
        validator.validate_ai_extraction(sample_texts)
        validator.print_summary()
    
    elif choice == "4":
        limit = input("Number of resumes to load (default 5): ").strip()
        limit = int(limit) if limit else 5
        load_sample_data_to_db(limit=limit)
    
    elif choice == "5":
        logger.info("Running full validation suite...")
        
        # CSV validation
        validator.validate_csv_parsing(limit=10)
        
        # PDF validation (Data Science category)
        validator.validate_pdf_parsing("Data Science", limit=5)
        
        # AI validation (if API key is available)
        try:
            sample_texts = []
            with open(CSV_FILE, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for idx, row in enumerate(reader):
                    if idx >= 2:
                        break
                    resume_text = row.get("Resume", "")
                    if resume_text and len(resume_text.strip()) >= 50:
                        sample_texts.append(resume_text)
            
            if sample_texts:
                validator.validate_ai_extraction(sample_texts)
        except Exception as e:
            logger.warning(f"Skipping AI validation: {e}")
        
        validator.print_summary()
    
    else:
        print("Invalid choice")


if __name__ == "__main__":
    main()
