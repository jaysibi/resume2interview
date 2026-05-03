"""
Expand Test Database with More Resume Data
Loads additional resumes from CSV for comprehensive testing
"""
import os
import sys
import csv
import logging
from pathlib import Path
from collections import defaultdict
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from db import SessionLocal
import crud

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Paths
DATA_DIR = Path(r"C:\Projects\ResumeTailor\02-Data")
CSV_FILE = DATA_DIR / "UpdatedResumeDataSet.csv"


def get_current_resume_count():
    """Get current number of resumes in database"""
    db = SessionLocal()
    try:
        from models import Resume
        count = db.query(Resume).count()
        return count
    finally:
        db.close()


def load_diverse_resumes(target_total: int = 100, categories_per_type: int = 10):
    """
    Load diverse resumes from different categories
    
    Args:
        target_total: Target total number of resumes in database
        categories_per_type: Number of resumes per category to load
    """
    current_count = get_current_resume_count()
    logger.info(f"Current resume count in database: {current_count}")
    
    if current_count >= target_total:
        logger.info(f"Database already has {current_count} resumes (target: {target_total})")
        logger.info("No additional loading needed.")
        return
    
    resumes_to_load = target_total - current_count
    logger.info(f"Target: {target_total} resumes. Need to load: {resumes_to_load} more.")
    
    if not CSV_FILE.exists():
        logger.error(f"CSV file not found: {CSV_FILE}")
        return
    
    db = SessionLocal()
    
    # Track resumes by category for diversity
    category_counts = defaultdict(int)
    resumes_by_category = defaultdict(list)
    
    # First pass: Read all resumes and categorize
    logger.info("Reading CSV file and categorizing resumes...")
    try:
        with open(CSV_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for idx, row in enumerate(reader):
                category = row.get("Category", "Unknown")
                resume_text = row.get("Resume", "")
                
                # Filter out short or empty resumes
                if not resume_text or len(resume_text.strip()) < 100:
                    continue
                
                resumes_by_category[category].append({
                    "index": idx,
                    "category": category,
                    "text": resume_text
                })
        
        logger.info(f"Found {len(resumes_by_category)} categories")
        for cat, resumes in resumes_by_category.items():
            logger.info(f"  {cat}: {len(resumes)} resumes")
    
    except Exception as e:
        logger.error(f"Error reading CSV: {e}")
        db.close()
        return
    
    # Second pass: Load resumes evenly across categories
    logger.info(f"\nLoading {resumes_to_load} resumes across categories...")
    loaded_count = 0
    category_list = list(resumes_by_category.keys())
    category_index = 0
    
    try:
        # Start from index after the ones already loaded (skip first 5)
        resume_offset = current_count if current_count <= 10 else 5
        
        while loaded_count < resumes_to_load:
            # Round-robin through categories
            category = category_list[category_index % len(category_list)]
            
            # Get next resume from this category
            if category_counts[category] < len(resumes_by_category[category]):
                resume_data = resumes_by_category[category][category_counts[category]]
                
                try:
                    # Create unique filename
                    filename = f"{category.replace(' ', '_')}_resume_{resume_data['index']}.txt"
                    result = {
                        "raw_text": resume_data['text'],
                        "skills": [],
                        "experience": [],
                        "education": [],
                        "tools": []
                    }
                    
                    resume = crud.create_resume(db, filename, result)
                    loaded_count += 1
                    category_counts[category] += 1
                    
                    if loaded_count % 10 == 0:
                        logger.info(f"Progress: {loaded_count}/{resumes_to_load} resumes loaded")
                    
                except Exception as e:
                    logger.error(f"Failed to load resume from {category}: {e}")
            
            category_index += 1
            
            # Safety check: if we've cycled through all categories and can't load more
            if category_index > len(category_list) * 100:
                logger.warning("Reached maximum iterations, stopping")
                break
        
        logger.info(f"\n✅ Successfully loaded {loaded_count} resumes!")
        logger.info(f"Total resumes in database: {current_count + loaded_count}")
        
        # Show distribution
        logger.info("\nResumes loaded by category:")
        for cat, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
            if count > 0:
                logger.info(f"  {cat}: {count} resumes")
        
    except Exception as e:
        logger.error(f"Error loading resumes: {e}")
    finally:
        db.close()


def show_database_stats():
    """Display current database statistics"""
    db = SessionLocal()
    try:
        from models import Resume, JobDescription
        
        resume_count = db.query(Resume).count()
        jd_count = db.query(JobDescription).count()
        
        logger.info("="*80)
        logger.info("DATABASE STATISTICS")
        logger.info("="*80)
        logger.info(f"Total Resumes: {resume_count}")
        logger.info(f"Total Job Descriptions: {jd_count}")
        
        if resume_count > 0:
            resumes = db.query(Resume).limit(10).all()
            logger.info("\nFirst 10 resumes:")
            for r in resumes:
                logger.info(f"  ID {r.id}: {r.filename[:50]}... ({len(r.raw_text)} chars)")
        
        logger.info("="*80)
        
    finally:
        db.close()


def main():
    """Main workflow"""
    print("\n" + "="*80)
    print("EXPAND TEST DATABASE")
    print("="*80)
    print("\nThis script loads additional resumes for comprehensive testing.")
    print("It ensures diversity by loading resumes from multiple categories.")
    print("="*80)
    
    # Show current stats
    show_database_stats()
    
    print("\nOptions:")
    print("1. Load resumes to reach 50 total")
    print("2. Load resumes to reach 100 total")
    print("3. Load resumes to reach 200 total")
    print("4. Custom target")
    print("5. Show stats only (no loading)")
    print("="*80)
    
    choice = input("\nEnter choice (1-5): ").strip()
    
    if choice == "1":
        load_diverse_resumes(target_total=50)
        show_database_stats()
    elif choice == "2":
        load_diverse_resumes(target_total=100)
        show_database_stats()
    elif choice == "3":
        load_diverse_resumes(target_total=200)
        show_database_stats()
    elif choice == "4":
        try:
            target = int(input("Enter target total: ").strip())
            if target > 0:
                load_diverse_resumes(target_total=target)
                show_database_stats()
            else:
                print("Invalid target number")
        except ValueError:
            print("Invalid input")
    elif choice == "5":
        show_database_stats()
    else:
        print("Invalid choice")


if __name__ == "__main__":
    main()
