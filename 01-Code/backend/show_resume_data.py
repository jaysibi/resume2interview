"""
Script to display parsed resume data from database
"""
import sys
from sqlalchemy.orm import Session
from db import SessionLocal
import crud_v2
import json

def show_resume_data(resume_id: int):
    """Display all parsed data for a resume"""
    db = SessionLocal()
    try:
        resume = crud_v2.get_resume(db, resume_id)
        
        if not resume:
            print(f"❌ Resume ID {resume_id} not found in database")
            return
        
        print("=" * 80)
        print(f"RESUME DATA FOR ID: {resume_id}")
        print("=" * 80)
        
        print(f"\n📄 BASIC INFO:")
        print(f"   Filename: {resume.filename}")
        print(f"   User ID: {resume.user_id}")
        print(f"   Upload Date: {resume.upload_date}")
        print(f"   Updated At: {resume.updated_at}")
        
        print(f"\n📝 RAW TEXT (first 500 chars):")
        print("-" * 80)
        print(resume.raw_text[:500] + "..." if len(resume.raw_text) > 500 else resume.raw_text)
        print("-" * 80)
        print(f"   Total length: {len(resume.raw_text)} characters")
        
        print(f"\n💼 SKILLS ({len(resume.skills)} found):")
        if resume.skills:
            for skill in resume.skills:
                print(f"   • {skill.get('name', 'N/A')} - Category: {skill.get('category', 'N/A')}, Proficiency: {skill.get('proficiency', 'N/A')}")
        else:
            print("   (No skills extracted)")
        
        print(f"\n🏢 EXPERIENCE ({len(resume.experience)} entries):")
        if resume.experience:
            for i, exp in enumerate(resume.experience, 1):
                print(f"\n   {i}. {exp.get('title', 'N/A')} at {exp.get('company', 'N/A')}")
                print(f"      Duration: {exp.get('duration', 'N/A')}")
                if exp.get('description'):
                    print(f"      Description: {exp['description'][:100]}...")
                if exp.get('key_achievements'):
                    print(f"      Achievements: {len(exp['key_achievements'])} listed")
                    for achievement in exp['key_achievements'][:3]:  # Show first 3
                        print(f"         - {achievement[:80]}...")
        else:
            print("   (No experience extracted)")
        
        print(f"\n🎓 EDUCATION ({len(resume.education)} entries):")
        if resume.education:
            for i, edu in enumerate(resume.education, 1):
                print(f"\n   {i}. {edu.get('degree', 'N/A')}")
                print(f"      Institution: {edu.get('institution', 'N/A')}")
                print(f"      Graduation Year: {edu.get('graduation_year', 'N/A')}")
                if edu.get('gpa'):
                    print(f"      GPA: {edu['gpa']}")
        else:
            print("   (No education extracted)")
        
        print(f"\n🔧 TOOLS:")
        if resume.tools:
            print(f"   {', '.join(resume.tools)}")
        else:
            print("   (No tools listed)")
        
        print("\n" + "=" * 80)
        
    except Exception as e:
        print(f"❌ Error retrieving resume: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        resume_id = int(sys.argv[1])
    else:
        # Use most recent resume ID
        resume_id = 2560
    
    show_resume_data(resume_id)
