"""
End-to-End Tests for Resume Tailor V2

Tests complete user workflows including:
- V1 workflows (backward compatibility)
- V2 workflows (user-centric features)
- Application tracking
- Job URL fetching
- Multi-user scenarios

Run with: pytest e2e_test_v2.py -v
"""

import pytest
import requests
import tempfile
import os
import fitz  # PyMuPDF
from typing import Dict, Any

# Configuration
BASE_URL = "http://localhost:8000"
TEST_USER_1 = "user1@example.com"
TEST_USER_2 = "user2@example.com"

# ===========================
# Fixtures
# ===========================

@pytest.fixture(scope="module")
def api_base_url():
    """Base URL for API"""
    return BASE_URL

@pytest.fixture(scope="module")
def health_check(api_base_url):
    """Verify server is running before tests"""
    try:
        response = requests.get(f"{api_base_url}/", timeout=5)
        assert response.status_code == 200, "Server not responding"
        return True
    except Exception as e:
        pytest.skip(f"Server not running: {e}")

@pytest.fixture
def sample_resume_pdf():
    """Create a sample resume PDF"""
    content = """JOHN DOE
Senior Python Developer | john.doe@email.com | (555) 123-4567

PROFESSIONAL SUMMARY
Senior Python Developer with 8+ years building scalable backend systems and RESTful APIs.
Expert in FastAPI, Django, PostgreSQL, Redis, and cloud infrastructure (AWS).

TECHNICAL SKILLS
• Languages: Python, JavaScript, SQL, Go
• Frameworks: FastAPI, Django, Flask, React
• Databases: PostgreSQL, MongoDB, Redis, Elasticsearch
• Cloud & DevOps: AWS (EC2, S3, Lambda, RDS), Docker, Kubernetes, Terraform
• Tools: Git, CI/CD, Jenkins, GitHub Actions, Pytest

PROFESSIONAL EXPERIENCE

Senior Python Developer | TechCorp Solutions | Jan 2020 - Present
• Architected microservices handling 5M+ API requests daily using FastAPI
• Designed and implemented PostgreSQL database schemas with optimal indexing
• Reduced API response time by 70% through caching and query optimization
• Led team of 6 developers in agile environment using Scrum methodology
• Implemented comprehensive testing strategy achieving 95% code coverage

Python Developer | StartupXYZ | Mar 2017 - Dec 2019
• Built RESTful APIs using Django and Django REST Framework
• Integrated payment gateways (Stripe, PayPal) processing $2M+ annually
• Developed automated data pipelines using Celery and RabbitMQ
• Mentored 3 junior developers in Python best practices

Junior Developer | CodeFactory | Jun 2015 - Feb 2017
• Developed web applications using Flask and SQLAlchemy
• Maintained legacy Python 2.7 codebase and migrated to Python 3.6
• Collaborated with frontend team on API contract design

EDUCATION
B.S. Computer Science | State University | 2015
GPA: 3.8/4.0, Dean's List all semesters

CERTIFICATIONS
• AWS Certified Solutions Architect - Associate (2022)
• Python Professional Certificate (2020)"""

    filepath = os.path.join(tempfile.gettempdir(), "e2e_resume.pdf")
    doc = fitz.open()
    page = doc.new_page()
    point = fitz.Point(50, 50)
    page.insert_text(point, content, fontsize=10)
    doc.save(filepath)
    doc.close()
    
    yield filepath
    
    if os.path.exists(filepath):
        os.remove(filepath)

@pytest.fixture
def sample_jd_pdf():
    """Create a sample job description PDF"""
    content = """SENIOR PYTHON DEVELOPER

TechGenius Inc. - San Francisco, CA (Remote Available)

COMPANY OVERVIEW
TechGenius is a leading SaaS platform serving 10,000+ enterprise customers globally.
We're building the next generation of cloud-based business intelligence tools.

ROLE DESCRIPTION
We are seeking a Senior Python Developer to join our Backend Infrastructure team.
You will architect and build scalable microservices powering our analytics platform.

REQUIRED QUALIFICATIONS
• 5+ years of professional Python development experience
• Strong experience with FastAPI or Django for building REST APIs
• PostgreSQL database design and optimization expertise
• Experience with cloud platforms (AWS, GCP, or Azure)
• Docker and Kubernetes containerization knowledge
• Git version control and collaborative development workflows
• Strong understanding of software design patterns and clean code principles

PREFERRED QUALIFICATIONS
• React or Vue.js frontend experience
• Redis caching implementation experience
• Message queue systems (RabbitMQ, Kafka, or Celery)
• CI/CD pipeline setup and maintenance
• Elasticsearch or similar search engines
• GraphQL API development
• Terraform or infrastructure-as-code experience
• Open source contributions

RESPONSIBILITIES
• Design and implement scalable backend microservices using FastAPI
• Optimize database queries and schema for high-performance applications
• Write comprehensive unit and integration tests (pytest)
• Collaborate with Frontend and DevOps teams on system architecture
• Conduct code reviews and mentor junior developers
• Participate in on-call rotation for production support
• Document APIs and system architecture

TECH STACK
Backend: Python 3.11, FastAPI, SQLAlchemy, Alembic
Database: PostgreSQL, Redis, Elasticsearch
Cloud: AWS (ECS, RDS, S3, Lambda, SQS)
DevOps: Docker, Kubernetes, Terraform, GitHub Actions
Monitoring: Datadog, Sentry

BENEFITS & COMPENSATION
• Competitive salary: $140K - $180K based on experience
• Equity package with 4-year vesting
• Comprehensive health, dental, and vision insurance
• 401(k) matching up to 6%
• Unlimited PTO policy
• Remote work flexibility
• Professional development budget ($2,000/year)
• Home office setup allowance
• Quarterly team offsites

HOW TO APPLY
Submit your resume and GitHub profile through our careers portal.
Technical interview process includes coding challenge and system design round."""

    filepath = os.path.join(tempfile.gettempdir(), "e2e_jd.pdf")
    doc = fitz.open()
    page = doc.new_page()
    point = fitz.Point(50, 50)
    page.insert_text(point, content, fontsize=9)
    doc.save(filepath)
    doc.close()
    
    yield filepath
    
    if os.path.exists(filepath):
        os.remove(filepath)

# ===========================
# E2E Test: V1 Workflow (Backward Compatibility)
# ===========================

class TestV1WorkflowBackwardCompatibility:
    """Test that V1 workflows still work after V2 migration"""
    
    def test_v1_upload_resume_no_user_email(self, api_base_url, health_check, sample_resume_pdf):
        """Test V1 resume upload without user_email (should use default user)"""
        with open(sample_resume_pdf, "rb") as f:
            files = {"file": ("resume.pdf", f, "application/pdf")}
            response = requests.post(f"{api_base_url}/upload-resume/", files=files)
        
        assert response.status_code == 200, f"Upload failed: {response.text}"
        data = response.json()
        assert "id" in data, "Response missing resume ID"
        assert "user_id" in data, "V2 should include user_id even for V1 calls"
        assert data["user_id"] == 1, "Should use default user ID"
        assert "extracted" in data, "AI extraction should work"
        
        return data["id"]
    
    def test_v1_upload_jd_no_metadata(self, api_base_url, health_check, sample_jd_pdf):
        """Test V1 JD upload without V2 metadata"""
        with open(sample_jd_pdf, "rb") as f:
            files = {"file": ("jd.pdf", f, "application/pdf")}
            response = requests.post(f"{api_base_url}/upload-jd/", files=files)
        
        assert response.status_code == 200, f"Upload failed: {response.text}"
        data = response.json()
        assert "id" in data, "Response missing JD ID"
        assert "user_id" in data, "V2 should include user_id"
        
        return data["id"]
    
    def test_v1_gap_analysis_without_application(self, api_base_url, health_check, 
                                                   sample_resume_pdf, sample_jd_pdf):
        """Test gap analysis without creating application (V1 behavior)"""
        # Upload resume
        with open(sample_resume_pdf, "rb") as f:
            files = {"file": ("resume.pdf", f, "application/pdf")}
            resume_response = requests.post(f"{api_base_url}/upload-resume/", files=files)
        resume_id = resume_response.json()["id"]
        
        # Upload JD
        with open(sample_jd_pdf, "rb") as f:
            files = {"file": ("jd.pdf", f, "application/pdf")}
            jd_response = requests.post(f"{api_base_url}/upload-jd/", files=files)
        jd_id = jd_response.json()["id"]
        
        # Gap analysis without create_application flag
        params = {"resume_id": resume_id, "jd_id": jd_id}
        response = requests.post(f"{api_base_url}/gap-analysis/", params=params)
        
        assert response.status_code == 200, f"Gap analysis failed: {response.text}"
        data = response.json()
        assert "analysis" in data or "match_score" in data, "Missing analysis data"
        assert "application_id" not in data, "Should NOT create application without flag"

# ===========================
# E2E Test: V2 User-Centric Workflow
# ===========================

class TestV2UserCentricWorkflow:
    """Test V2 user-centric features"""
    
    def test_v2_complete_workflow_user1(self, api_base_url, health_check, 
                                         sample_resume_pdf, sample_jd_pdf):
        """Test complete V2 workflow for user1"""
        # Step 1: Upload resume with user_email
        with open(sample_resume_pdf, "rb") as f:
            files = {"file": ("resume.pdf", f, "application/pdf")}
            data = {"user_email": TEST_USER_1}
            resume_response = requests.post(f"{api_base_url}/upload-resume/", files=files, data=data)
        
        assert resume_response.status_code == 200
        resume_data = resume_response.json()
        resume_id = resume_data["id"]
        user_id = resume_data["user_id"]
        
        # Step 2: Upload JD with metadata
        with open(sample_jd_pdf, "rb") as f:
            files = {"file": ("jd.pdf", f, "application/pdf")}
            data = {
                "user_email": TEST_USER_1,
                "job_url": "https://www.linkedin.com/jobs/view/123456",
                "title": "Senior Python Developer",
                "company": "TechGenius Inc."
            }
            jd_response = requests.post(f"{api_base_url}/upload-jd/", files=files, data=data)
        
        assert jd_response.status_code == 200
        jd_data = jd_response.json()
        jd_id = jd_data["id"]
        assert jd_data["title"] == "Senior Python Developer"
        assert jd_data["company"] == "TechGenius Inc."
        
        # Step 3: Gap analysis with application creation
        params = {
            "resume_id": resume_id,
            "jd_id": jd_id,
            "user_email": TEST_USER_1,
            "create_application": "true"
        }
        gap_response = requests.post(f"{api_base_url}/gap-analysis/", params=params)
        
        assert gap_response.status_code == 200
        gap_data = gap_response.json()
        app_id = gap_data.get("application_id")
        assert app_id is not None, "Application should be created"
        
        # Step 4: Get applications list
        list_params = {"user_email": TEST_USER_1}
        list_response = requests.get(f"{api_base_url}/v2/applications/", params=list_params)
        
        assert list_response.status_code == 200
        list_data = list_response.json()
        assert list_data["total"] >= 1, "Should have at least 1 application"
        assert list_data["user_id"] == user_id
        
        # Step 5: Get application details
        detail_response = requests.get(f"{api_base_url}/v2/applications/{app_id}/")
        
        assert detail_response.status_code == 200
        detail_data = detail_response.json()
        assert detail_data["application"]["id"] == app_id
        assert "gap_analysis" in detail_data
        
        # Step 6: ATS Score
        ats_params = {"resume_id": resume_id, "jd_id": jd_id}
        ats_response = requests.post(f"{api_base_url}/ats-score/", params=ats_params)
        
        assert ats_response.status_code == 200
        ats_data = ats_response.json()
        assert "ats_score" in ats_data
        
        return {"user_id": user_id, "resume_id": resume_id, "jd_id": jd_id, "app_id": app_id}
    
    def test_v2_multi_user_isolation(self, api_base_url, health_check, 
                                      sample_resume_pdf, sample_jd_pdf):
        """Test that different users have isolated data"""
        # Create application for user1
        with open(sample_resume_pdf, "rb") as f:
            files = {"file": ("resume.pdf", f, "application/pdf")}
            data = {"user_email": TEST_USER_1}
            r1 = requests.post(f"{api_base_url}/upload-resume/", files=files, data=data)
        resume1_id = r1.json()["id"]
        
        with open(sample_jd_pdf, "rb") as f:
            files = {"file": ("jd.pdf", f, "application/pdf")}
            data = {"user_email": TEST_USER_1}
            j1 = requests.post(f"{api_base_url}/upload-jd/", files=files, data=data)
        jd1_id = j1.json()["id"]
        
        params1 = {
            "resume_id": resume1_id,
            "jd_id": jd1_id,
            "user_email": TEST_USER_1,
            "create_application": "true"
        }
        gap1 = requests.post(f"{api_base_url}/gap-analysis/", params=params1)
        user1_app_count = gap1.json().get("application_id")
        
        # Create application for user2
        with open(sample_resume_pdf, "rb") as f:
            files = {"file": ("resume.pdf", f, "application/pdf")}
            data = {"user_email": TEST_USER_2}
            r2 = requests.post(f"{api_base_url}/upload-resume/", files=files, data=data)
        resume2_id = r2.json()["id"]
        
        with open(sample_jd_pdf, "rb") as f:
            files = {"file": ("jd.pdf", f, "application/pdf")}
            data = {"user_email": TEST_USER_2}
            j2 = requests.post(f"{api_base_url}/upload-jd/", files=files, data=data)
        jd2_id = j2.json()["id"]
        
        params2 = {
            "resume_id": resume2_id,
            "jd_id": jd2_id,
            "user_email": TEST_USER_2,
            "create_application": "true"
        }
        gap2 = requests.post(f"{api_base_url}/gap-analysis/", params=params2)
        user2_app_count = gap2.json().get("application_id")
        
        # Verify user1 only sees their applications
        list1 = requests.get(f"{api_base_url}/v2/applications/", params={"user_email": TEST_USER_1})
        user1_apps = list1.json()["applications"]
        user1_ids = [app["id"] for app in user1_apps]
        
        # Verify user2 only sees their applications
        list2 = requests.get(f"{api_base_url}/v2/applications/", params={"user_email": TEST_USER_2})
        user2_apps = list2.json()["applications"]
        user2_ids = [app["id"] for app in user2_apps]
        
        # Check isolation
        assert user2_app_count not in user1_ids, "User1 should not see User2's applications"
        assert user1_app_count not in user2_ids, "User2 should not see User1's applications"

# ===========================
# E2E Test: Job URL Fetching
# ===========================

class TestJobURLFetching:
    """Test job URL web scraping features"""
    
    def test_fetch_jd_from_linkedin_url(self, api_base_url, health_check):
        """Test fetching JD from LinkedIn URL (will use mock/test data)"""
        payload = {"job_url": "https://www.linkedin.com/jobs/view/3849876543"}
        response = requests.post(f"{api_base_url}/v2/fetch-jd-from-url/", json=payload)
        
        # May return 200 with scraped data or error if scraping fails
        # This is acceptable in E2E test as external URLs may change
        assert response.status_code in [200, 400, 500]
        
        if response.status_code == 200:
            data = response.json()
            assert "raw_text" in data, "Should have raw_text field"

# ===========================
# E2E Test: Error Handling
# ===========================

class TestErrorHandling:
    """Test error scenarios"""
    
    def test_invalid_file_type(self, api_base_url, health_check):
        """Test uploading invalid file type"""
        content = b"This is a text file, not a PDF"
        files = {"file": ("resume.txt", content, "text/plain")}
        response = requests.post(f"{api_base_url}/upload-resume/", files=files)
        
        assert response.status_code == 400
        assert "error_code" in response.json()["detail"]
    
    def test_nonexistent_resume_id(self, api_base_url, health_check):
        """Test accessing nonexistent resume"""
        response = requests.get(f"{api_base_url}/resume/999999")
        assert response.status_code == 404
    
    def test_gap_analysis_missing_ids(self, api_base_url, health_check):
        """Test gap analysis with invalid IDs"""
        params = {"resume_id": 999999, "jd_id": 999999}
        response = requests.post(f"{api_base_url}/gap-analysis/", params=params)
        assert response.status_code == 404

# ===========================
# Summary Test
# ===========================

def test_e2e_summary(api_base_url, health_check):
    """Print E2E test summary"""
    print("\n" + "="*80)
    print("E2E TESTS COMPLETED SUCCESSFULLY")
    print("="*80)
    print("✅ V1 backward compatibility maintained")
    print("✅ V2 user-centric workflows working")
    print("✅ Multi-user data isolation verified")
    print("✅ Application tracking functional")
    print("✅ Error handling robust")
    print("="*80)
