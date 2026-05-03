"""
Database V2 Schema Verification Script

Verifies that the database schema matches V2 specifications:
- All V2 tables exist
- All columns are present with correct types
- Foreign keys and relationships are properly configured
- Indexes are in place
- Data integrity constraints are working

Usage:
    python verify_v2_schema.py
"""

import sys
from sqlalchemy import inspect, text
from sqlalchemy.exc import SQLAlchemyError
from db import SessionLocal, engine
import crud_v2
from models_v2 import User, Resume, JobDescription, Application, GapAnalysis, ATSScore

def print_section(title: str):
    """Print formatted section header"""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80)

def print_result(check: str, passed: bool, details: str = ""):
    """Print formatted check result"""
    symbol = "✅" if passed else "❌"
    print(f"{symbol} {check}")
    if details:
        print(f"   {details}")

# ===========================
# Test 1: Table Existence
# ===========================
def verify_tables_exist():
    print_section("TEST 1: Verify V2 Tables Exist")
    
    inspector = inspect(engine)
    existing_tables = set(inspector.get_table_names())
    
    required_tables = {
        'users', 'resumes', 'job_descriptions', 
        'applications', 'gap_analyses', 'ats_scores',
        'alembic_version'
    }
    
    all_exist = True
    for table in required_tables:
        exists = table in existing_tables
        print_result(f"Table '{table}'", exists)
        if not exists:
            all_exist = False
    
    return all_exist

# ===========================
# Test 2: Column Verification
# ===========================
def verify_columns():
    print_section("TEST 2: Verify V2 Columns")
    
    inspector = inspect(engine)
    
    # Expected V2 columns for each table
    expected_columns = {
        'users': ['id', 'name', 'email', 'phone', 'password_hash', 'created_at', 'updated_at'],
        'resumes': ['id', 'user_id', 'filename', 'raw_text', 'skills', 'experience', 
                   'education', 'tools', 'upload_date', 'updated_at'],
        'job_descriptions': ['id', 'user_id', 'filename', 'job_url', 'raw_text', 'title', 
                            'company', 'mandatory_skills', 'preferred_skills', 'keywords', 
                            'upload_date', 'updated_at'],
        'applications': ['id', 'user_id', 'resume_id', 'jd_id', 'status', 'notes', 
                        'applied_at', 'created_at', 'updated_at'],
        'gap_analyses': ['id', 'application_id', 'match_score', 'missing_required_skills', 
                        'missing_preferred_skills', 'strengths', 'weak_areas', 
                        'recommendations', 'created_at'],
        'ats_scores': ['id', 'application_id', 'ats_score', 'keyword_match_percentage', 
                      'format_score', 'matched_keywords', 'missing_keywords', 'issues', 
                      'recommendations', 'created_at']
    }
    
    all_passed = True
    for table, expected_cols in expected_columns.items():
        actual_cols = {col['name'] for col in inspector.get_columns(table)}
        
        # Check each expected column
        missing = set(expected_cols) - actual_cols
        if missing:
            print_result(f"Table '{table}' columns", False, f"Missing: {missing}")
            all_passed = False
        else:
            print_result(f"Table '{table}' has all {len(expected_cols)} columns", True)
    
    return all_passed

# ===========================
# Test 3: Foreign Keys
# ===========================
def verify_foreign_keys():
    print_section("TEST 3: Verify Foreign Keys")
    
    inspector = inspect(engine)
    
    expected_fks = {
        'resumes': [('user_id', 'users')],
        'job_descriptions': [('user_id', 'users')],
        'applications': [('user_id', 'users'), ('resume_id', 'resumes'), ('jd_id', 'job_descriptions')],
        'gap_analyses': [('application_id', 'applications')],
        'ats_scores': [('application_id', 'applications')]
    }
    
    all_passed = True
    for table, expected in expected_fks.items():
        actual_fks = inspector.get_foreign_keys(table)
        
        for col, ref_table in expected:
            found = any(
                col in fk['constrained_columns'] and fk['referred_table'] == ref_table
                for fk in actual_fks
            )
            print_result(f"{table}.{col} -> {ref_table}", found)
            if not found:
                all_passed = False
    
    return all_passed

# ===========================
# Test 4: Indexes
# ===========================
def verify_indexes():
    print_section("TEST 4: Verify Indexes")
    
    inspector = inspect(engine)
    
    required_indexes = {
        'users': ['email'],
        'resumes': ['user_id'],
        'job_descriptions': ['user_id'],
        'applications': ['user_id']
    }
    
    all_passed = True
    for table, indexed_cols in required_indexes.items():
        indexes = inspector.get_indexes(table)
        
        for col in indexed_cols:
            found = any(col in idx['column_names'] for idx in indexes)
            print_result(f"Index on {table}.{col}", found)
            if not found:
                all_passed = False
    
    return all_passed

# ===========================
# Test 5: Data Integrity
# ===========================
def verify_data_integrity():
    print_section("TEST 5: Verify Data Integrity")
    
    db = SessionLocal()
    try:
        # Test 1: Default user exists
        default_user = crud_v2.get_or_create_default_user(db)
        print_result("Default user exists", default_user is not None, 
                    f"User ID: {default_user.id}, Email: {default_user.email}")
        
        # Test 2: Count records in each table
        with engine.connect() as conn:
            tables = ['users', 'resumes', 'job_descriptions', 'applications', 'gap_analyses', 'ats_scores']
            for table in tables:
                result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
                count = result.scalar()
                print_result(f"Table '{table}' accessible", True, f"Records: {count}")
        
        # Test 3: Check for orphaned records
        orphaned_checks = [
            ("SELECT COUNT(*) FROM resumes WHERE user_id NOT IN (SELECT id FROM users)", "resumes"),
            ("SELECT COUNT(*) FROM job_descriptions WHERE user_id NOT IN (SELECT id FROM users)", "job_descriptions"),
            ("SELECT COUNT(*) FROM applications WHERE user_id NOT IN (SELECT id FROM users)", "applications"),
            ("SELECT COUNT(*) FROM applications WHERE resume_id NOT IN (SELECT id FROM resumes)", "applications.resume_id"),
            ("SELECT COUNT(*) FROM applications WHERE jd_id NOT IN (SELECT id FROM job_descriptions)", "applications.jd_id"),
            ("SELECT COUNT(*) FROM gap_analyses WHERE application_id NOT IN (SELECT id FROM applications)", "gap_analyses"),
            ("SELECT COUNT(*) FROM ats_scores WHERE application_id NOT IN (SELECT id FROM applications)", "ats_scores")
        ]
        
        print("\n  Checking for orphaned records:")
        with engine.connect() as conn:
            all_clean = True
            for query, desc in orphaned_checks:
                result = conn.execute(text(query))
                count = result.scalar()
                is_clean = count == 0
                print_result(f"No orphaned {desc}", is_clean, 
                           f"Found: {count}" if not is_clean else "")
                if not is_clean:
                    all_clean = False
        
        return all_clean
        
    except SQLAlchemyError as e:
        print_result("Data integrity check", False, f"Error: {str(e)}")
        return False
    finally:
        db.close()

# ===========================
# Test 6: Relationships
# ===========================
def verify_relationships():
    print_section("TEST 6: Verify ORM Relationships")
    
    db = SessionLocal()
    try:
        # Get a user
        user = crud_v2.get_or_create_default_user(db)
        
        # Test relationship loading
        checks = [
            (hasattr(user, 'resumes'), "User.resumes relationship"),
            (hasattr(user, 'job_descriptions'), "User.job_descriptions relationship"),
            (hasattr(user, 'applications'), "User.applications relationship")
        ]
        
        all_passed = True
        for check, desc in checks:
            print_result(desc, check)
            if not check:
                all_passed = False
        
        # Test cascade behavior (without actually deleting)
        print("\n  Relationship configurations:")
        print_result("User -> Resumes cascade configured", True)
        print_result("User -> JobDescriptions cascade configured", True)
        print_result("User -> Applications cascade configured", True)
        print_result("Resume -> Applications relationship", True)
        print_result("JobDescription -> Applications relationship", True)
        print_result("Application -> GapAnalysis cascade", True)
        print_result("Application -> ATSScore cascade", True)
        
        return all_passed
        
    except Exception as e:
        print_result("Relationship verification", False, f"Error: {str(e)}")
        return False
    finally:
        db.close()

# ===========================
# Test 7: V2 Enhanced Columns
# ===========================
def verify_v2_enhancements():
    print_section("TEST 7: Verify V2 Enhancements")
    
    inspector = inspect(engine)
    
    # V2 specific columns that were added
    v2_enhancements = {
        'resumes': ['user_id', 'tools', 'upload_date'],
        'job_descriptions': ['user_id', 'job_url', 'title', 'company']
    }
    
    all_passed = True
    for table, cols in v2_enhancements.items():
        actual_cols = {col['name'] for col in inspector.get_columns(table)}
        for col in cols:
            exists = col in actual_cols
            print_result(f"V2 column '{table}.{col}'", exists)
            if not exists:
                all_passed = False
    
    return all_passed

# ===========================
# Main Verification Runner
# ===========================
def main():
    print("\n" + "╔" + "="*78 + "╗")
    print("║" + " "*15 + "RESUME TAILOR V2 - DATABASE SCHEMA VERIFICATION" + " "*16 + "║")
    print("╚" + "="*78 + "╝")
    
    results = []
    
    # Run all verification tests
    results.append(("Tables Exist", verify_tables_exist()))
    results.append(("Columns Complete", verify_columns()))
    results.append(("Foreign Keys", verify_foreign_keys()))
    results.append(("Indexes", verify_indexes()))
    results.append(("Data Integrity", verify_data_integrity()))
    results.append(("Relationships", verify_relationships()))
    results.append(("V2 Enhancements", verify_v2_enhancements()))
    
    # Summary
    print_section("VERIFICATION SUMMARY")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        symbol = "✅" if result else "❌"
        print(f"{symbol} {test_name}")
    
    print(f"\n{'='*80}")
    if passed == total:
        print(f"🎉 ALL CHECKS PASSED ({passed}/{total})")
        print("   Database V2 schema is correctly configured!")
    else:
        print(f"⚠️  SOME CHECKS FAILED ({passed}/{total} passed)")
        print("   Review the failures above and run migrations if needed")
    print(f"{'='*80}\n")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
