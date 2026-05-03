"""
Direct test of AI service functionality
"""
from dotenv import load_dotenv
load_dotenv()

from ai_service import get_ai_service
from db import SessionLocal
import crud

# Get database contents
db = SessionLocal()
resume = crud.get_resume(db, 5)
jd = crud.get_jd(db, 4)

print(f"Resume ID 5: {len(resume.raw_text)} chars")
print(f"JD ID 4: {len(jd.raw_text)} chars")

# Test AI service
try:
    ai_service = get_ai_service()
    print("\n✅ AI Service initialized successfully")
    print(f"Default model: {ai_service.default_model}")
    
    # Try gap analysis
    print("\n[Testing Gap Analysis]")
    analysis = ai_service.analyze_gap(
        resume_skills=resume.skills if resume.skills else [],
        resume_experience=resume.raw_text[:1500],
        resume_education=resume.education if resume.education else [],
        jd_text=jd.raw_text
    )
    
    print(f"✅ Gap Analysis successful!")
    print(f"Match Score: {analysis.match_score}")
    print(f"Missing Required Skills: {len(analysis.missing_required_skills)}")
    print(f"Strengths: {len(analysis.strengths)}")
    print(f"Recommendations: {len(analysis.recommendations)}")
    
except Exception as e:
    print(f"\n❌ Error: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()

finally:
    db.close()
