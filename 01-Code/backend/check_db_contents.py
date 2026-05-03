"""Quick script to check database contents"""
import sys
sys.path.insert(0, '.')
from db import SessionLocal
from models import Resume, JobDescription

db = SessionLocal()

# Count records
resume_count = db.query(Resume).count()
jd_count = db.query(JobDescription).count()

print("\n" + "="*60)
print("DATABASE CONTENTS")
print("="*60)
print(f"Total Resumes: {resume_count}")
print(f"Total Job Descriptions: {jd_count}")

if resume_count > 0:
    print("\nResumes in DB:")
    resumes = db.query(Resume).all()
    for r in resumes:
        created = r.created_at.strftime('%Y-%m-%d %H:%M') if r.created_at else 'N/A'
        print(f"  • ID {r.id}: {len(r.raw_text)} chars, created {created}")

if jd_count > 0:
    print("\nJob Descriptions in DB:")
    jds = db.query(JobDescription).all()
    for j in jds:
        created = j.created_at.strftime('%Y-%m-%d %H:%M') if j.created_at else 'N/A'
        print(f"  • ID {j.id}: {len(j.raw_text)} chars, created {created}")

print("\n" + "="*60)
print("NOTE: These are test records from earlier endpoint testing.")
print("Real data from 02-Data folder has NOT been loaded yet.")
print("Run Option 4 in validate_data.py to load sample data.")
print("="*60 + "\n")

db.close()
