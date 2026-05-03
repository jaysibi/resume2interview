"""
Manual API Testing Script for Resume Tailor V2

Tests all V2 endpoints with real API calls.
Run this with the backend server running on http://localhost:8000

Usage:
    python test_v2_api_manual.py
"""

import requests
import json
import os
from pathlib import Path
import fitz  # PyMuPDF
import tempfile

# API Base URL
BASE_URL = "http://localhost:8000"

# Test data
TEST_USER_EMAIL = "testuser@example.com"
TEST_JOB_URL = "https://www.linkedin.com/jobs/view/123456"
TEST_JOB_TITLE = "Senior Python Developer"
TEST_COMPANY = "Tech Innovations Inc."

def create_test_pdf(content: str, filename: str) -> str:
    """Create a test PDF file"""
    filepath = os.path.join(tempfile.gettempdir(), filename)
    doc = fitz.open()
    page = doc.new_page()
    point = fitz.Point(50, 50)
    page.insert_text(point, content, fontsize=11)
    doc.save(filepath)
    doc.close()
    return filepath

def print_section(title: str):
    """Print a formatted section header"""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80)

def print_result(endpoint: str, status: int, data: dict = None, error: str = None):
    """Print formatted test result"""
    status_symbol = "✅" if 200 <= status < 300 else "❌"
    print(f"\n{status_symbol} {endpoint}")
    print(f"   Status: {status}")
    if data:
        print(f"   Response: {json.dumps(data, indent=2)[:500]}...")
    if error:
        print(f"   Error: {error}")

# ===========================
# Test 1: Health Check
# ===========================
def test_health():
    print_section("TEST 1: Health Check")
    try:
        response = requests.get(f"{BASE_URL}/")
        print_result("GET /", response.status_code, response.json())
        return response.status_code == 200
    except Exception as e:
        print_result("GET /", 0, error=str(e))
        return False

# ===========================
# Test 2: Upload Resume (V2)
# ===========================
def test_upload_resume():
    print_section("TEST 2: Upload Resume with User Email (V2)")
    
    resume_content = """John Doe
Senior Python Developer
Email: john.doe@email.com | Phone: (555) 123-4567

PROFESSIONAL SUMMARY
Senior Python Developer with 7+ years of experience in building scalable backend systems,
RESTful APIs, and cloud-native applications. Expert in FastAPI, Django, PostgreSQL, and AWS.

TECHNICAL SKILLS
- Languages: Python, JavaScript, SQL
- Frameworks: FastAPI, Django, Flask, React
- Databases: PostgreSQL, MongoDB, Redis
- Cloud: AWS (EC2, S3, Lambda, RDS), Docker, Kubernetes
- Tools: Git, CI/CD, Jenkins, GitHub Actions

PROFESSIONAL EXPERIENCE

Senior Python Developer | Tech Solutions Inc. | 2021 - Present
- Architected and developed RESTful APIs using FastAPI serving 1M+ requests/day
- Implemented microservices architecture with Docker and Kubernetes
- Optimized database queries reducing response time by 60%
- Led team of 4 developers in agile environment

Python Developer | StartupXYZ | 2018 - 2021
- Built backend systems using Django and PostgreSQL
- Integrated third-party APIs and payment gateways
- Implemented automated testing with pytest (95% coverage)

EDUCATION
B.S. Computer Science | State University | 2017"""

    pdf_path = create_test_pdf(resume_content, "test_resume.pdf")
    
    try:
        with open(pdf_path, "rb") as f:
            files = {"file": ("test_resume.pdf", f, "application/pdf")}
            data = {"user_email": TEST_USER_EMAIL}
            response = requests.post(f"{BASE_URL}/upload-resume/", files=files, data=data)
        
        result = response.json()
        print_result("POST /upload-resume/", response.status_code, result)
        
        if response.status_code == 200:
            resume_id = result.get('id')
            print(f"\n   📝 Resume ID: {resume_id}")
            print(f"   👤 User ID: {result.get('user_id')}")
            print(f"   🎯 Skills extracted: {len(result.get('extracted', {}).get('skills', []))}")
            return resume_id
        return None
    except Exception as e:
        print_result("POST /upload-resume/", 0, error=str(e))
        return None
    finally:
        if os.path.exists(pdf_path):
            os.remove(pdf_path)

# ===========================
# Test 3: Upload JD (V2)
# ===========================
def test_upload_jd():
    print_section("TEST 3: Upload Job Description with Metadata (V2)")
    
    jd_content = """Senior Python Developer

Tech Innovations Inc. is seeking a Senior Python Developer to join our growing team.

REQUIREMENTS:
- 5+ years of Python development experience
- Strong experience with FastAPI or Django
- PostgreSQL database expertise
- RESTful API design and implementation
- Experience with Docker and Kubernetes
- Cloud platforms (AWS preferred)
- Git version control

NICE TO HAVE:
- React or Vue.js experience
- CI/CD pipeline setup
- Microservices architecture
- Redis caching
- Message queues (RabbitMQ, Celery)

RESPONSIBILITIES:
- Design and develop scalable backend APIs
- Write clean, maintainable, tested code
- Collaborate with frontend and DevOps teams
- Participate in code reviews
- Mentor junior developers"""

    pdf_path = create_test_pdf(jd_content, "test_jd.pdf")
    
    try:
        with open(pdf_path, "rb") as f:
            files = {"file": ("test_jd.pdf", f, "application/pdf")}
            data = {
                "user_email": TEST_USER_EMAIL,
                "job_url": TEST_JOB_URL,
                "title": TEST_JOB_TITLE,
                "company": TEST_COMPANY
            }
            response = requests.post(f"{BASE_URL}/upload-jd/", files=files, data=data)
        
        result = response.json()
        print_result("POST /upload-jd/", response.status_code, result)
        
        if response.status_code == 200:
            jd_id = result.get('id')
            print(f"\n   📝 JD ID: {jd_id}")
            print(f"   👤 User ID: {result.get('user_id')}")
            print(f"   🏢 Company: {result.get('company')}")
            print(f"   💼 Title: {result.get('title')}")
            print(f"   🔗 Job URL: {result.get('job_url')}")
            return jd_id
        return None
    except Exception as e:
        print_result("POST /upload-jd/", 0, error=str(e))
        return None
    finally:
        if os.path.exists(pdf_path):
            os.remove(pdf_path)

# ===========================
# Test 4: Gap Analysis with Application Creation (V2)
# ===========================
def test_gap_analysis(resume_id: int, jd_id: int):
    print_section("TEST 4: Gap Analysis with Application Creation (V2)")
    
    if not resume_id or not jd_id:
        print("⚠️  Skipping gap analysis - missing resume_id or jd_id")
        return None
    
    try:
        params = {
            "resume_id": resume_id,
            "jd_id": jd_id,
            "user_email": TEST_USER_EMAIL,
            "create_application": "true"
        }
        response = requests.post(f"{BASE_URL}/gap-analysis/", params=params)
        result = response.json()
        print_result("POST /gap-analysis/", response.status_code, result)
        
        if response.status_code == 200:
            app_id = result.get('application_id')
            print(f"\n   📝 Application ID: {app_id}")
            print(f"   📊 Match Score: {result.get('match_score', 'N/A')}")
            print(f"   ✅ Strengths: {len(result.get('strengths', []))}")
            print(f"   ⚠️  Missing Skills: {len(result.get('missing_required_skills', []))}")
            return app_id
        return None
    except Exception as e:
        print_result("POST /gap-analysis/", 0, error=str(e))
        return None

# ===========================
# Test 5: Fetch JD from URL (V2)
# ===========================
def test_fetch_jd_from_url():
    print_section("TEST 5: Fetch JD from URL (V2)")
    
    try:
        payload = {"job_url": "https://www.linkedin.com/jobs/view/3849876543"}
        response = requests.post(f"{BASE_URL}/v2/fetch-jd-from-url/", json=payload)
        result = response.json()
        print_result("POST /v2/fetch-jd-from-url/", response.status_code, result)
        
        if response.status_code == 200:
            print(f"\n   🏢 Company: {result.get('company', 'N/A')}")
            print(f"   💼 Title: {result.get('title', 'N/A')}")
            print(f"   📄 Text Length: {len(result.get('raw_text', ''))} chars")
        return response.status_code == 200
    except Exception as e:
        print_result("POST /v2/fetch-jd-from-url/", 0, error=str(e))
        return False

# ===========================
# Test 6: Get Applications List (V2)
# ===========================
def test_get_applications():
    print_section("TEST 6: Get Applications List (V2)")
    
    try:
        params = {"user_email": TEST_USER_EMAIL, "skip": 0, "limit": 10}
        response = requests.get(f"{BASE_URL}/v2/applications/", params=params)
        result = response.json()
        print_result("GET /v2/applications/", response.status_code, result)
        
        if response.status_code == 200:
            total = result.get('total', 0)
            apps = result.get('applications', [])
            print(f"\n   📊 Total Applications: {total}")
            print(f"   📝 Returned: {len(apps)}")
            if apps:
                print(f"   🔍 First Application ID: {apps[0].get('id')}")
        return response.status_code == 200
    except Exception as e:
        print_result("GET /v2/applications/", 0, error=str(e))
        return False

# ===========================
# Test 7: Get Application Details (V2)
# ===========================
def test_get_application_details(app_id: int):
    print_section("TEST 7: Get Application Details (V2)")
    
    if not app_id:
        print("⚠️  Skipping application details - missing application_id")
        return False
    
    try:
        response = requests.get(f"{BASE_URL}/v2/applications/{app_id}/")
        result = response.json()
        print_result(f"GET /v2/applications/{app_id}/", response.status_code, result)
        
        if response.status_code == 200:
            app = result.get('application', {})
            gap = result.get('gap_analysis', {})
            ats = result.get('ats_score', {})
            
            print(f"\n   📝 Application: {app.get('id')} - Status: {app.get('status')}")
            print(f"   📊 Gap Analysis: Match Score {gap.get('match_score', 'N/A')}%")
            print(f"   🎯 ATS Score: {ats.get('ats_score', 'N/A')}%")
        return response.status_code == 200
    except Exception as e:
        print_result(f"GET /v2/applications/{app_id}/", 0, error=str(e))
        return False

# ===========================
# Test 8: ATS Score (V2)
# ===========================
def test_ats_score(resume_id: int, jd_id: int):
    print_section("TEST 8: ATS Score Analysis (V2)")
    
    if not resume_id or not jd_id:
        print("⚠️  Skipping ATS score - missing resume_id or jd_id")
        return False
    
    try:
        params = {"resume_id": resume_id, "jd_id": jd_id}
        response = requests.post(f"{BASE_URL}/ats-score/", params=params)
        result = response.json()
        print_result("POST /ats-score/", response.status_code, result)
        
        if response.status_code == 200:
            print(f"\n   🎯 ATS Score: {result.get('ats_score', 'N/A')}%")
            print(f"   🔍 Keyword Match: {result.get('keyword_match_percentage', 'N/A')}%")
            print(f"   📄 Format Score: {result.get('format_score', 'N/A')}%")
            print(f"   ✅ Matched Keywords: {len(result.get('matched_keywords', []))}")
            print(f"   ❌ Missing Keywords: {len(result.get('missing_keywords', []))}")
        return response.status_code == 200
    except Exception as e:
        print_result("POST /ats-score/", 0, error=str(e))
        return False

# ===========================
# Main Test Runner
# ===========================
def main():
    print("\n" + "╔" + "="*78 + "╗")
    print("║" + " "*20 + "RESUME TAILOR V2 - API TESTING" + " "*28 + "║")
    print("╚" + "="*78 + "╝")
    
    # Check if server is running
    if not test_health():
        print("\n❌ Server is not running on", BASE_URL)
        print("   Start the server with: cd backend && python -m uvicorn main:app --port 8000")
        return
    
    # Run V2 API tests
    resume_id = test_upload_resume()
    jd_id = test_upload_jd()
    app_id = test_gap_analysis(resume_id, jd_id)
    test_fetch_jd_from_url()
    test_get_applications()
    test_get_application_details(app_id)
    test_ats_score(resume_id, jd_id)
    
    # Summary
    print_section("TEST SUMMARY")
    print("\n✅ All V2 API endpoints tested")
    print("   - Resume upload with user context")
    print("   - JD upload with metadata (title, company, job_url)")
    print("   - Gap analysis with application creation")
    print("   - Job URL fetching")
    print("   - Applications list and details")
    print("   - ATS scoring")
    
    print("\n📊 Check the results above for any failures")
    print("   All endpoints should return 200 status codes\n")

if __name__ == "__main__":
    main()
