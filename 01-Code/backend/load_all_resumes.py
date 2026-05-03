"""
Load all remaining resumes from Resume.csv
Target: All 2,484 resumes from Resume.csv
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from load_from_resume_csv import load_from_resume_csv, show_database_stats, get_current_resume_count

print("\n" + "="*80)
print("LOADING ALL RESUMES FROM Resume.csv")
print("="*80)

current = get_current_resume_count()
print(f"\nCurrent database count: {current}")
print(f"Resume.csv has 2,484 total resumes")
print(f"Target: Load all remaining resumes")
print(f"This will take a few minutes...")
print("="*80)

# Load all resumes - set high target
# Resume.csv has 2,484 resumes, we already loaded 50, so need 2,434 more
# Current total is 100 (50 from UpdatedResumeDataSet + 50 from Resume.csv)
# Target should be 100 + 2,434 = 2,534 total
target_total = 2534

print(f"\nLoading to target: {target_total} total resumes...\n")

load_from_resume_csv(target_total=target_total)

print("\n" + "="*80)
print("LOADING COMPLETE!")
print("="*80)

show_database_stats()
