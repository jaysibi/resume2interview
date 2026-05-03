"""Test database dependency directly"""
from db import SessionLocal, engine
from sqlalchemy import text
import traceback

print("Testing database connection...")

try:
    # Test 1: Engine connection
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("✅ Engine connection works")
    
    # Test 2: SessionLocal
    db = SessionLocal()
    try:
        result = db.execute(text("SELECT COUNT(*) FROM resumes"))
        count = result.scalar()
        print(f"✅ SessionLocal works - Resume count: {count}")
    finally:
        db.close()
    
    # Test 3: Generator pattern (like Depends)
    def get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()
    
    gen = get_db()
    db = next(gen)
    try:
        result = db.execute(text("SELECT COUNT(*) FROM job_descriptions"))
        count = result.scalar()
        print(f"✅ Generator pattern works - JD count: {count}")
    finally:
        try:
            next(gen)
        except StopIteration:
            pass
    
    print("\n✅ All database dependency tests PASSED")
    
except Exception as e:
    print(f"\n❌ Database test FAILED: {e}")
    traceback.print_exc()
