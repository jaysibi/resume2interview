"""
V2 Integration Tests for Resume Tailor API

Tests all V2 endpoints and functionality:
- Database V2 schema validation
- Job URL fetching (mocked)
- V2 upload endpoints with user context
- Application creation and tracking
- Applications list and detail endpoints
"""

import sys
import os
import pytest
from unittest.mock import patch, MagicMock
from sqlalchemy.orm import Session
import fitz  # PyMuPDF
import tempfile
from pathlib import Path

# Add backend directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi.testclient import TestClient
from main import app
from db import SessionLocal
import crud_v2
from models_v2 import User, Resume, JobDescription, Application, GapAnalysis, ATSScore

# Test client
client = TestClient(app)

# ===========================
# PDF Creation Helpers
# ===========================

def create_test_pdf(content: str, filename: str = "test.pdf") -> str:
    """Create a test PDF file with the given content"""
    temp_dir = tempfile.gettempdir()
    filepath = os.path.join(temp_dir, filename)
    
    # Create PDF with PyMuPDF
    doc = fitz.open()
    page = doc.new_page()
    
    # Add text to the page
    text = content
    point = fitz.Point(50, 50)
    page.insert_text(point, text, fontsize=11)
    
    # Save the PDF
    doc.save(filepath)
    doc.close()
    
    return filepath

# ===========================
# Test Fixtures
# ===========================

@pytest.fixture
def db():
    """Get a database session for testing"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def test_user(db):
    """Create a test user"""
    user = crud_v2.get_or_create_default_user(db)
    return user


@pytest.fixture
def test_resume_file():
    """Create a test resume PDF file"""
    content = """John Doe
Senior Software Engineer
Email: john@example.com
Phone: 555-1234

EXPERIENCE
- 5 years Python development
- 3 years FastAPI
- Expert in REST APIs

SKILLS
Python, FastAPI, PostgreSQL, React"""
    
    filepath = create_test_pdf(content, "test_resume.pdf")
    
    try:
        with open(filepath, "rb") as f:
            file_content = f.read()
        yield ("test_resume.pdf", file_content, "application/pdf")
    finally:
        # Cleanup
        if os.path.exists(filepath):
            os.remove(filepath)


@pytest.fixture
def test_jd_file():
    """Create a test JD PDF file"""
    content = """Senior Software Engineer

We are seeking a Senior Software Engineer with:
- 5+ years Python experience
- FastAPI expertise
- PostgreSQL knowledge
- React skills

Responsibilities:
- Build REST APIs
- Design database schemas
- Collaborate with frontend team"""
    
    filepath = create_test_pdf(content, "test_jd.pdf")
    
    try:
        with open(filepath, "rb") as f:
            file_content = f.read()
        yield ("test_jd.pdf", file_content, "application/pdf")
    finally:
        # Cleanup
        if os.path.exists(filepath):
            os.remove(filepath)


# ===========================
# Database Schema Tests
# ===========================

def test_v2_schema_exists(db):
    """Test that all V2 tables exist"""
    from sqlalchemy import inspect
    
    inspector = inspect(db.bind)
    tables = inspector.get_table_names()
    
    # Verify all V2 tables exist
    assert 'users' in tables, "Users table does not exist"
    assert 'resumes' in tables, "Resumes table does not exist"
    assert 'job_descriptions' in tables, "Job descriptions table does not exist"
    assert 'applications' in tables, "Applications table does not exist"
    assert 'gap_analyses' in tables, "Gap analyses table does not exist"
    assert 'ats_scores' in tables, "ATS scores table does not exist"
    
    print("✅ All V2 tables exist")


def test_v2_columns_exist(db):
    """Test that V2 columns exist in enhanced tables"""
    from sqlalchemy import inspect
    
    inspector = inspect(db.bind)
    
    # Check resumes table has V2 columns
    resume_columns = {col['name'] for col in inspector.get_columns('resumes')}
    assert 'user_id' in resume_columns, "resumes.user_id does not exist"
    assert 'upload_date' in resume_columns, "resumes.upload_date does not exist"
    assert 'tools' in resume_columns, "resumes.tools does not exist"
    
    # Check job_descriptions table has V2 columns
    jd_columns = {col['name'] for col in inspector.get_columns('job_descriptions')}
    assert 'user_id' in jd_columns, "job_descriptions.user_id does not exist"
    assert 'job_url' in jd_columns, "job_descriptions.job_url does not exist"
    assert 'title' in jd_columns, "job_descriptions.title does not exist"
    assert 'company' in jd_columns, "job_descriptions.company does not exist"
    
    print("✅ All V2 columns exist")


def test_default_user_exists(db):
    """Test that default user exists"""
    user = crud_v2.get_or_create_default_user(db)
    
    assert user is not None, "Default user not created"
    assert user.id == 1, "Default user ID is not 1"
    assert user.email == "default@resumetailor.local", "Default user email incorrect"
    
    print(f"✅ Default user exists: {user.email}")


# ===========================
# V2 Endpoint Tests
# ===========================

@patch('job_scraper.requests.get')
def test_fetch_jd_from_url(mock_get):
    """Test V2 fetch-jd-from-url endpoint"""
    # Mock LinkedIn response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = """
    <html>
        <h1>Senior Software Engineer</h1>
        <h2>Google</h2>
        <div class="description">
            We are looking for a Senior Software Engineer with Python and FastAPI experience.
        </div>
    </html>
    """
    mock_get.return_value = mock_response
    
    # Test fetch endpoint
    response = client.post(
        "/v2/fetch-jd-from-url/",
        json={"job_url": "https://www.linkedin.com/jobs/view/123456"}
    )
    
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    
    assert 'title' in data, "Response missing title"
    assert 'company' in data, "Response missing company"
    assert 'raw_text' in data, "Response missing raw_text"
    
    print(f"✅ Fetch JD from URL successful: {data.get('title', 'N/A')}")


def test_upload_resume_v2(test_resume_file):
    """Test V2 upload-resume with user_email parameter"""
    filename, file_content, content_type = test_resume_file
    
    from io import BytesIO
    response = client.post(
        "/upload-resume/",
        files={"file": (filename, BytesIO(file_content), content_type)},
        data={"user_email": "test@example.com"}
    )
    
    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
    data = response.json()
    
    assert 'id' in data, "Response missing resume ID"
    assert 'filename' in data, "Response missing filename"
    # V2 should include user_id in response when user_email is provided
    assert 'user_id' in data or 'id' in data, "Response missing user context"
    
    print(f"✅ V2 Resume upload successful: ID {data['id']}")
    return data['id']


def test_upload_jd_v2(test_jd_file):
    """Test V2 upload-jd with V2 parameters"""
    filename, file_content, content_type = test_jd_file
    
    from io import BytesIO
    response = client.post(
        "/upload-jd/",
        files={"file": (filename, BytesIO(file_content), content_type)},
        data={
            "user_email": "test@example.com",
            "job_url": "https://www.linkedin.com/jobs/view/123456",
            "title": "Senior Software Engineer",
            "company": "Google"
        }
    )
    
    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
    data = response.json()
    
    assert 'id' in data, "Response missing JD ID"
    assert 'filename' in data, "Response missing filename"
    # V2 should include metadata in response
    assert data.get('title') == "Senior Software Engineer", "Title not preserved"
    assert data.get('company') == "Google", "Company not preserved"
    
    print(f"✅ V2 JD upload successful: ID {data['id']}, Title: {data.get('title')}")
    return data['id']


def test_gap_analysis_with_application(test_resume_file, test_jd_file):
    """Test gap analysis with application creation (V2)"""
    from io import BytesIO
    
    # Upload resume
    filename_r, file_content_r, content_type_r = test_resume_file
    resume_response = client.post(
        "/upload-resume/",
        files={"file": (filename_r, BytesIO(file_content_r), content_type_r)}
    )
    assert resume_response.status_code == 200, f"Resume upload failed: {resume_response.text}"
    resume_id = resume_response.json()['id']
    
    # Upload JD
    filename_j, file_content_j, content_type_j = test_jd_file
    jd_response = client.post(
        "/upload-jd/",
        files={"file": (filename_j, BytesIO(file_content_j), content_type_j)}
    )
    assert jd_response.status_code == 200, f"JD upload failed: {jd_response.text}"
    jd_id = jd_response.json()['id']
    
    # Run gap analysis with application creation
    response = client.post(
        f"/gap-analysis/?resume_id={resume_id}&jd_id={jd_id}&create_application=true&user_email=test@example.com"
    )
    
    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
    data = response.json()
    
    assert 'resume_id' in data, "Response missing resume_id"
    assert 'jd_id' in data, "Response missing jd_id"
    assert 'analysis' in data, "Response missing analysis"
    assert 'application_id' in data, "Response missing application_id (V2)"
    
    print(f"✅ Gap analysis with application creation successful: Application ID {data['application_id']}")
    return data['application_id']


def test_get_applications_list():
    """Test V2 applications list endpoint"""
    response = client.get("/v2/applications/")
    
    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
    data = response.json()
    
    assert 'applications' in data, "Response missing applications list"
    assert 'total' in data, "Response missing total count"
    assert 'user_id' in data, "Response missing user_id"
    assert 'user_email' in data, "Response missing user_email"
    
    print(f"✅ Applications list successful: {data['total']} applications found")


def test_get_application_details(db):
    """Test V2 application details endpoint"""
    # First, create an application to test with
    user = crud_v2.get_or_create_default_user(db)
    
    # Create test resume
    resume = crud_v2.create_resume(db, user.id, "test_resume.txt", {
        "raw_text": "Test resume content",
        "skills": [],
        "experience": [],
        "education": []
    })
    
    # Create test JD
    jd = crud_v2.create_jd(db, user.id, "test_jd.txt", {
        "raw_text": "Test JD content",
        "mandatory_skills": [],
        "preferred_skills": [],
        "keywords": []
    }, title="Test Job", company="Test Company")
    
    # Create application
    app = crud_v2.create_application(db, user.id, resume.id, jd.id, status="analyzed")
    
    # Test endpoint
    response = client.get(f"/v2/applications/{app.id}/")
    
    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
    data = response.json()
    
    assert 'application' in data, "Response missing application"
    assert 'resume' in data, "Response missing resume"
    assert 'job_description' in data, "Response missing job_description"
    assert 'gap_analysis' in data, "Response should include gap_analysis field"
    assert 'ats_score' in data, "Response should include ats_score field"
    
    print(f"✅ Application details successful: Application ID {app.id}")


# ===========================
# CRUD V2 Tests
# ===========================

def test_crud_v2_user_operations(db):
    """Test V2 user CRUD operations"""
    # Create user with unique email
    import uuid
    unique_email = f"test_{uuid.uuid4().hex[:8]}@example.com"
    user = crud_v2.create_user(db, "Test User", unique_email, "555-1234")
    assert user.id is not None, "User ID not generated"
    assert user.email == unique_email, "User email incorrect"
    
    # Get user by email
    fetched_user = crud_v2.get_user_by_email(db, unique_email)
    assert fetched_user is not None, "User not found by email"
    assert fetched_user.id == user.id, "Fetched user ID mismatch"
    
    # Get user by ID
    fetched_by_id = crud_v2.get_user(db, user.id)
    assert fetched_by_id is not None, "User not found by ID"
    
    print(f"✅ V2 User CRUD operations successful")


def test_crud_v2_application_workflow(db):
    """Test complete V2 application workflow"""
    # Get default user
    user = crud_v2.get_or_create_default_user(db)
    
    # Create resume
    resume = crud_v2.create_resume(db, user.id, "workflow_resume.txt", {
        "raw_text": "Workflow test resume",
        "skills": [{"name": "Python", "category": "Programming"}],
        "experience": [],
        "education": []
    })
    
    # Create JD
    jd = crud_v2.create_jd(db, user.id, "workflow_jd.txt", {
        "raw_text": "Workflow test JD",
        "mandatory_skills": ["Python"],
        "preferred_skills": [],
        "keywords": ["Python", "Backend"]
    }, job_url="https://example.com/job/123", title="Python Developer", company="Example Corp")
    
    # Create application
    app = crud_v2.create_application(db, user.id, resume.id, jd.id, status="analyzed")
    assert app.id is not None, "Application ID not generated"
    
    # Create gap analysis
    gap_data = {
        "match_score": 85,
        "missing_required_skills": [],
        "missing_preferred_skills": ["FastAPI"],
        "strengths": ["Strong Python skills"],
        "weak_areas": ["Limited FastAPI experience"],
        "recommendations": ["Practice FastAPI"]
    }
    gap = crud_v2.create_gap_analysis(db, app.id, gap_data)
    assert gap.id is not None, "Gap analysis ID not generated"
    assert gap.match_score == 85, "Match score incorrect"
    
    # Create ATS score
    ats_data = {
        "ats_score": 78,
        "keyword_match_percentage": 80,
        "format_score": 75,
        "matched_keywords": ["Python"],
        "missing_keywords": ["FastAPI"],
        "issues": [],
        "recommendations": ["Add more keywords"]
    }
    ats = crud_v2.create_ats_score(db, app.id, ats_data)
    assert ats.id is not None, "ATS score ID not generated"
    assert ats.ats_score == 78, "ATS score incorrect"
    
    # Retrieve full application
    full_app = crud_v2.get_full_application_with_analyses(db, app.id)
    assert full_app is not None, "Full application not retrieved"
    assert full_app['application'].id == app.id, "Application ID mismatch"
    assert full_app['gap_analysis'].match_score == 85, "Gap analysis not included"
    assert full_app['ats_score'].ats_score == 78, "ATS score not included"
    
    print(f"✅ V2 Application workflow complete: Application ID {app.id}")


# ===========================
# Run Tests
# ===========================

if __name__ == "__main__":
    print("\n" + "="*60)
    print("RESUME TAILOR V2 - INTEGRATION TESTS")
    print("="*60 + "\n")
    
    # Get database session
    db = SessionLocal()
    
    try:
        print("📋 Phase 1: Database Schema Tests")
        print("-" * 60)
        test_v2_schema_exists(db)
        test_v2_columns_exist(db)
        test_default_user_exists(db)
        
        print("\n📋 Phase 2: CRUD V2 Tests")
        print("-" * 60)
        test_crud_v2_user_operations(db)
        test_crud_v2_application_workflow(db)
        
        print("\n📋 Phase 3: V2 API Endpoint Tests")
        print("-" * 60)
        test_fetch_jd_from_url()
        test_upload_resume_v2(("test_v2_resume.txt", open("test_v2_resume.txt", "wb").write(b"Test resume content") or open("test_v2_resume.txt", "rb"), "text/plain"))
        test_get_applications_list()
        test_get_application_details(db)
        
        print("\n" + "="*60)
        print("✅ ALL TESTS PASSED!")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        
    finally:
        db.close()
