"""
Load resumes from Resume.csv
This file has 2,484 resumes with ID, Resume_str, Resume_html, and Category columns
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
RESUME_CSV_FILE = DATA_DIR / "Resume.csv"


def get_current_resume_count():
    """Get current number of resumes in database"""
    db = SessionLocal()
    try:
        from models import Resume
        count = db.query(Resume).count()
        return count
    finally:
        db.close()


def load_from_resume_csv(target_total: int = 100):
    """
    Load resumes from Resume.csv
    
    Args:
        target_total: Target total number of resumes in database
    """
    current_count = get_current_resume_count()
    logger.info(f"Current resume count in database: {current_count}")
    
    if current_count >= target_total:
        logger.info(f"Database already has {current_count} resumes (target: {target_total})")
        logger.info("No additional loading needed.")
        return
    
    resumes_to_load = target_total - current_count
    logger.info(f"Target: {target_total} resumes. Need to load: {resumes_to_load} more.")
    
    if not RESUME_CSV_FILE.exists():
        logger.error(f"CSV file not found: {RESUME_CSV_FILE}")
        return
    
    db = SessionLocal()
    
    # Track resumes by category
    category_counts = defaultdict(int)
    resumes_by_category = defaultdict(list)
    
    # First pass: Read and categorize
    logger.info("Reading Resume.csv and categorizing...")
    try:
        with open(RESUME_CSV_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for idx, row in enumerate(reader):
                resume_id = row.get("ID", "")
                category = row.get("Category", "Unknown")
                resume_text = row.get("Resume_str", "")  # Use plain text version
                
                # Filter out short or empty resumes
                if not resume_text or len(resume_text.strip()) < 100:
                    continue
                
                resumes_by_category[category].append({
                    "id": resume_id,
                    "index": idx,
                    "category": category,
                    "text": resume_text
                })
        
        logger.info(f"Found {len(resumes_by_category)} categories in Resume.csv")
        for cat, resumes in sorted(resumes_by_category.items(), key=lambda x: len(x[1]), reverse=True)[:10]:
            logger.info(f"  {cat}: {len(resumes)} resumes")
    
    except Exception as e:
        logger.error(f"Error reading CSV: {e}")
        db.close()
        return
    
    # Second pass: Load resumes evenly across categories
    logger.info(f"\nLoading {resumes_to_load} resumes from Resume.csv...")
    loaded_count = 0
    category_list = list(resumes_by_category.keys())
    category_index = 0
    
    try:
        while loaded_count < resumes_to_load and category_list:
            # Round-robin through categories
            category = category_list[category_index % len(category_list)]
            
            # Get next resume from this category
            if category_counts[category] < len(resumes_by_category[category]):
                resume_data = resumes_by_category[category][category_counts[category]]
                
                try:
                    # Create unique filename with original ID
                    filename = f"{category.replace(' ', '_')}_ID{resume_data['id']}.txt"
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
                    
                    if loaded_count % 25 == 0:
                        logger.info(f"Progress: {loaded_count}/{resumes_to_load} resumes loaded")
                    
                except Exception as e:
                    logger.error(f"Failed to load resume ID {resume_data['id']}: {e}")
            
            category_index += 1
            
            # Safety check
            if category_index > len(category_list) * 200:
                logger.warning("Reached maximum iterations, stopping")
                break
        
        logger.info(f"\n✅ Successfully loaded {loaded_count} resumes from Resume.csv!")
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
            # Get size statistics
            resumes = db.query(Resume).all()
            sizes = [len(r.raw_text) for r in resumes]
            logger.info(f"\nResume Statistics:")
            logger.info(f"  Smallest: {min(sizes)} chars")
            logger.info(f"  Largest: {max(sizes)} chars")
            logger.info(f"  Average: {sum(sizes)//len(sizes)} chars")
            logger.info(f"  Total Data: {sum(sizes):,} chars")
        
        logger.info("="*80)
        
    finally:
        db.close()


def main():
    """Main workflow"""
    print("\n" + "="*80)
    print("LOAD RESUMES FROM Resume.csv")
    print("="*80)
    print("\nResume.csv contains 2,484 resumes with richer content.")
    print("This script loads additional resumes to expand your test database.")
    print("="*80)
    
    # Show current stats
    show_database_stats()
    
    print("\nOptions:")
    print("1. Load to reach 100 total resumes (50 more from Resume.csv)")
    print("2. Load to reach 200 total resumes (150 more from Resume.csv)")
    print("3. Load to reach 500 total resumes (450 more from Resume.csv)")
    print("4. Load to reach 1000 total resumes (950 more from Resume.csv)")
    print("5. Custom target")
    print("6. Show stats only (no loading)")
    print("="*80)
    
    choice = input("\nEnter choice (1-6): ").strip()
    
    if choice == "1":
        load_from_resume_csv(target_total=100)
        show_database_stats()
    elif choice == "2":
        load_from_resume_csv(target_total=200)
        show_database_stats()
    elif choice == "3":
        load_from_resume_csv(target_total=500)
        show_database_stats()
    elif choice == "4":
        load_from_resume_csv(target_total=1000)
        show_database_stats()
    elif choice == "5":
        try:
            target = int(input("Enter target total: ").strip())
            if target > 0:
                load_from_resume_csv(target_total=target)
                show_database_stats()
            else:
                print("Invalid target number")
        except ValueError:
            print("Invalid input")
    elif choice == "6":
        show_database_stats()
    else:
        print("Invalid choice")


if __name__ == "__main__":
    main()
