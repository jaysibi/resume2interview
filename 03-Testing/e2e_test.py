"""
End-to-End Test Suite for Resume Tailor Application
Executes comprehensive QA testing after each deployment

Test Coverage:
1. Backend API Health Check
2. Frontend Server Availability
3. Resume Upload
4. Job Description Upload
5. Gap Analysis
6. ATS Scoring
7. Data Validation

Usage: python e2e_test.py
"""

import os
import sys
import time
import json
import requests
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, Tuple

# Configuration
BACKEND_URL = "http://127.0.0.1:8000"
FRONTEND_URL = "http://localhost:5173"
TEST_DATA_DIR = Path(__file__).parent
RESUME_FILE = TEST_DATA_DIR / "Resume - Jayendra Sibi (1).docx"
JD_FILE = TEST_DATA_DIR / "Job Description.txt"

# Test Configuration
REQUEST_TIMEOUT = 30
RETRY_COUNT = 3
RETRY_DELAY = 2

# ANSI Color Codes for Terminal Output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'


class TestResult:
    """Store test execution results"""
    def __init__(self):
        self.total = 0
        self.passed = 0
        self.failed = 0
        self.skipped = 0
        self.failures = []
        self.start_time = datetime.now()
    
    def add_pass(self, test_name: str):
        self.total += 1
        self.passed += 1
        print(f"{Colors.GREEN}✓{Colors.END} {test_name}")
    
    def add_fail(self, test_name: str, error: str):
        self.total += 1
        self.failed += 1
        self.failures.append((test_name, error))
        print(f"{Colors.RED}✗{Colors.END} {test_name}")
        print(f"  {Colors.RED}Error: {error}{Colors.END}")
    
    def add_skip(self, test_name: str, reason: str):
        self.total += 1
        self.skipped += 1
        print(f"{Colors.YELLOW}⊘{Colors.END} {test_name} (Skipped: {reason})")
    
    def summary(self):
        duration = (datetime.now() - self.start_time).total_seconds()
        print(f"\n{Colors.BOLD}{'='*80}{Colors.END}")
        print(f"{Colors.BOLD}TEST SUMMARY{Colors.END}")
        print(f"{Colors.BOLD}{'='*80}{Colors.END}")
        print(f"Total Tests: {self.total}")
        print(f"{Colors.GREEN}Passed: {self.passed}{Colors.END}")
        print(f"{Colors.RED}Failed: {self.failed}{Colors.END}")
        print(f"{Colors.YELLOW}Skipped: {self.skipped}{Colors.END}")
        print(f"Duration: {duration:.2f}s")
        
        if self.failures:
            print(f"\n{Colors.RED}{Colors.BOLD}FAILURES:{Colors.END}")
            for i, (test, error) in enumerate(self.failures, 1):
                print(f"{i}. {test}")
                print(f"   {error}")
        
        print(f"\n{Colors.BOLD}{'='*80}{Colors.END}")
        return self.failed == 0


def print_header(title: str):
    """Print formatted section header"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{title}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.END}")


def check_server(url: str, name: str) -> bool:
    """Check if server is running"""
    try:
        response = requests.get(url, timeout=5)
        return response.status_code == 200
    except:
        return False


def test_backend_health(results: TestResult) -> bool:
    """Test 1: Backend API Health Check"""
    test_name = "Backend API Health Check"
    try:
        response = requests.get(f"{BACKEND_URL}/", timeout=REQUEST_TIMEOUT)
        
        if response.status_code != 200:
            results.add_fail(test_name, f"Status code: {response.status_code}")
            return False
        
        data = response.json()
        if "message" not in data:
            results.add_fail(test_name, "Response missing 'message' field")
            return False
        
        results.add_pass(test_name)
        return True
    except Exception as e:
        results.add_fail(test_name, str(e))
        return False


def test_frontend_available(results: TestResult) -> bool:
    """Test 2: Frontend Server Availability"""
    test_name = "Frontend Server Availability"
    try:
        response = requests.get(FRONTEND_URL, timeout=REQUEST_TIMEOUT)
        
        if response.status_code != 200:
            results.add_fail(test_name, f"Status code: {response.status_code}")
            return False
        
        results.add_pass(test_name)
        return True
    except Exception as e:
        results.add_fail(test_name, str(e))
        return False


def test_resume_upload(results: TestResult) -> Optional[int]:
    """Test 3: Resume Upload"""
    test_name = "Resume Upload from 03-Testing folder"
    
    # Validate file exists
    if not RESUME_FILE.exists():
        results.add_fail(test_name, f"Resume file not found: {RESUME_FILE}")
        return None
    
    # Validate file size
    file_size = RESUME_FILE.stat().st_size
    if file_size == 0:
        results.add_fail(test_name, "Resume file is empty")
        return None
    
    if file_size > 10 * 1024 * 1024:  # 10MB
        results.add_fail(test_name, f"Resume file too large: {file_size / 1024 / 1024:.2f}MB")
        return None
    
    try:
        with open(RESUME_FILE, 'rb') as f:
            files = {'file': (RESUME_FILE.name, f, 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')}
            data = {'filename': RESUME_FILE.name}
            
            response = requests.post(
                f"{BACKEND_URL}/upload-resume/",
                files=files,
                data=data,
                timeout=REQUEST_TIMEOUT
            )
        
        if response.status_code != 200:
            error_detail = response.json().get('detail', response.text)
            results.add_fail(test_name, f"Status {response.status_code}: {error_detail}")
            return None
        
        data = response.json()
        
        # Validate response structure
        if 'id' not in data:
            results.add_fail(test_name, "Response missing 'id' field")
            return None
        
        if 'filename' not in data or data['filename'] != RESUME_FILE.name:
            results.add_fail(test_name, f"Filename mismatch: {data.get('filename')}")
            return None
        
        if 'parsed' not in data or 'raw_text' not in data['parsed']:
            results.add_fail(test_name, "Response missing parsed data")
            return None
        
        # Validate parsed text is not empty
        raw_text = data['parsed']['raw_text']
        if len(raw_text) < 10:
            results.add_fail(test_name, f"Parsed text too short: {len(raw_text)} chars")
            return None
        
        resume_id = data['id']
        results.add_pass(test_name + f" (ID: {resume_id}, {file_size / 1024:.1f}KB, {len(raw_text)} chars)")
        return resume_id
        
    except requests.exceptions.Timeout:
        results.add_fail(test_name, "Request timeout")
        return None
    except Exception as e:
        results.add_fail(test_name, str(e))
        return None


def test_jd_upload(results: TestResult) -> Optional[int]:
    """Test 4: Job Description Upload"""
    test_name = "Job Description Upload from 03-Testing folder"
    
    # Validate file exists
    if not JD_FILE.exists():
        results.add_fail(test_name, f"JD file not found: {JD_FILE}")
        return None
    
    # Read JD file content
    try:
        with open(JD_FILE, 'r', encoding='utf-8') as f:
            jd_content = f.read()
    except:
        results.add_fail(test_name, "Failed to read JD file")
        return None
    
    if len(jd_content) < 10:
        results.add_fail(test_name, "JD content too short")
        return None
    
    # Convert TXT to DOCX for upload (backend only accepts PDF/DOCX)
    try:
        from docx import Document
        doc = Document()
        doc.add_paragraph(jd_content)
        
        # Save to temp docx
        temp_jd_path = TEST_DATA_DIR / "temp_jd.docx"
        doc.save(temp_jd_path)
        
        with open(temp_jd_path, 'rb') as f:
            files = {'file': ('job_description.docx', f, 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')}
            data = {'filename': 'job_description.docx'}
            
            response = requests.post(
                f"{BACKEND_URL}/upload-jd/",
                files=files,
                data=data,
                timeout=REQUEST_TIMEOUT
            )
        
        # Clean up temp file
        if temp_jd_path.exists():
            temp_jd_path.unlink()
        
        if response.status_code != 200:
            error_detail = response.json().get('detail', response.text)
            results.add_fail(test_name, f"Status {response.status_code}: {error_detail}")
            return None
        
        data = response.json()
        
        # Validate response structure
        if 'id' not in data:
            results.add_fail(test_name, "Response missing 'id' field")
            return None
        
        if 'parsed' not in data or 'raw_text' not in data['parsed']:
            results.add_fail(test_name, "Response missing parsed data")
            return None
        
        jd_id = data['id']
        results.add_pass(test_name + f" (ID: {jd_id})")
        return jd_id
        
    except ImportError:
        results.add_fail(test_name, "python-docx not installed")
        return None
    except Exception as e:
        results.add_fail(test_name, str(e))
        return None


def test_gap_analysis(results: TestResult, resume_id: int, jd_id: int) -> Optional[Dict]:
    """Test 5: Gap Analysis"""
    test_name = "Gap Analysis Execution"
    
    try:
        response = requests.post(
            f"{BACKEND_URL}/gap-analysis/",
            params={'resume_id': resume_id, 'jd_id': jd_id},
            timeout=REQUEST_TIMEOUT
        )
        
        if response.status_code != 200:
            error_detail = response.json().get('detail', response.text)
            results.add_fail(test_name, f"Status {response.status_code}: {error_detail}")
            return None
        
        data = response.json()
        
        # Validate top-level response structure (backend returns nested structure)
        required_fields = ['resume_id', 'jd_id', 'analysis']
        for field in required_fields:
            if field not in data:
                results.add_fail(test_name, f"Response missing '{field}' field")
                return None
        
        # Validate nested analysis object
        analysis = data['analysis']
        required_analysis_fields = ['match_score', 'missing_required_skills', 'missing_preferred_skills',
                                     'strengths', 'weak_areas', 'recommendations']
        for field in required_analysis_fields:
            if field not in analysis:
                results.add_fail(test_name, f"Analysis missing '{field}' field")
                return None
        
        # Validate data types
        if not isinstance(analysis['match_score'], (int, float)):
            results.add_fail(test_name, f"Invalid match_score type: {type(analysis['match_score'])}")
            return None
        
        if not isinstance(analysis['missing_required_skills'], list):
            results.add_fail(test_name, f"Invalid missing_required_skills type: {type(analysis['missing_required_skills'])}")
            return None
        
        if not isinstance(analysis['missing_preferred_skills'], list):
            results.add_fail(test_name, f"Invalid missing_preferred_skills type: {type(analysis['missing_preferred_skills'])}")
            return None
        
        if not isinstance(analysis['recommendations'], list):
            results.add_fail(test_name, f"Invalid recommendations type: {type(analysis['recommendations'])}")
            return None
        
        # Validate ranges
        if not (0 <= analysis['match_score'] <= 100):
            results.add_fail(test_name, f"Invalid match_score: {analysis['match_score']}")
            return None
        
        match_score = analysis['match_score']
        missing_req = len(analysis['missing_required_skills'])
        missing_pref = len(analysis['missing_preferred_skills'])
        recs = len(analysis['recommendations'])
        
        results.add_pass(test_name + f" (Match: {match_score}%, Missing Required: {missing_req}, Missing Preferred: {missing_pref}, Recommendations: {recs})")
        return data
        
    except Exception as e:
        results.add_fail(test_name, str(e))
        return None


def test_ats_scoring(results: TestResult, resume_id: int, jd_id: int) -> Optional[Dict]:
    """Test 6: ATS Scoring"""
    test_name = "ATS Scoring Execution"
    
    try:
        response = requests.post(
            f"{BACKEND_URL}/ats-score/",
            params={'resume_id': resume_id, 'jd_id': jd_id},
            timeout=REQUEST_TIMEOUT
        )
        
        if response.status_code != 200:
            error_detail = response.json().get('detail', response.text)
            results.add_fail(test_name, f"Status {response.status_code}: {error_detail}")
            return None
        
        data = response.json()
        
        # Validate top-level response structure (backend returns nested structure)
        required_fields = ['resume_id', 'jd_id', 'scoring']
        for field in required_fields:
            if field not in data:
                results.add_fail(test_name, f"Response missing '{field}' field")
                return None
        
        # Validate nested scoring object
        scoring = data['scoring']
        required_scoring_fields = ['ats_score', 'keyword_match_percentage', 'format_score',
                                   'matched_keywords', 'missing_keywords', 'issues', 'recommendations']
        for field in required_scoring_fields:
            if field not in scoring:
                results.add_fail(test_name, f"Scoring missing '{field}' field")
                return None
        
        # Validate data types and ranges
        for score_field in ['ats_score', 'keyword_match_percentage', 'format_score']:
            if not isinstance(scoring[score_field], (int, float)):
                results.add_fail(test_name, f"Invalid {score_field} type: {type(scoring[score_field])}")
                return None
            
            if not (0 <= scoring[score_field] <= 100):
                results.add_fail(test_name, f"Invalid {score_field}: {scoring[score_field]}")
                return None
        
        if not isinstance(scoring['missing_keywords'], list):
            results.add_fail(test_name, f"Invalid missing_keywords type: {type(scoring['missing_keywords'])}")
            return None
        
        if not isinstance(scoring['matched_keywords'], list):
            results.add_fail(test_name, f"Invalid matched_keywords type: {type(scoring['matched_keywords'])}")
            return None
        
        if not isinstance(scoring['issues'], list):
            results.add_fail(test_name, f"Invalid issues type: {type(scoring['issues'])}")
            return None
        
        ats = scoring['ats_score']
        kw = scoring['keyword_match_percentage']
        fmt = scoring['format_score']
        missing = len(scoring['missing_keywords'])
        matched = len(scoring['matched_keywords'])
        issues = len(scoring['issues'])
        
        results.add_pass(test_name + f" (ATS: {ats}%, Keywords: {kw}%, Format: {fmt}%, Matched KW: {matched}, Missing KW: {missing}, Issues: {issues})")
        return data
        
    except Exception as e:
        results.add_fail(test_name, str(e))
        return None


def generate_test_report(results: TestResult, gap_data: Optional[Dict], ats_data: Optional[Dict]):
    """Generate detailed test report"""
    report_path = TEST_DATA_DIR / f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("RESUME TAILOR - E2E TEST REPORT\n")
        f.write("="*80 + "\n")
        f.write(f"Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Total Tests: {results.total}\n")
        f.write(f"Passed: {results.passed}\n")
        f.write(f"Failed: {results.failed}\n")
        f.write(f"Skipped: {results.skipped}\n")
        f.write(f"Success Rate: {(results.passed / results.total * 100):.1f}%\n")
        f.write("\n")
        
        if results.failures:
            f.write("FAILURES:\n")
            f.write("-"*80 + "\n")
            for test, error in results.failures:
                f.write(f"Test: {test}\n")
                f.write(f"Error: {error}\n\n")
        
        if gap_data:
            f.write("\n")
            f.write("GAP ANALYSIS RESULTS:\n")
            f.write("-"*80 + "\n")
            # Backend returns nested structure
            analysis = gap_data.get('analysis', {})
            f.write(f"Match Score: {analysis.get('match_score', 'N/A')}%\n")
            
            missing_req = analysis.get('missing_required_skills', [])
            missing_pref = analysis.get('missing_preferred_skills', [])
            all_missing = missing_req + missing_pref
            f.write(f"Missing Required Skills: {', '.join(missing_req) if missing_req else 'None'}\n")
            f.write(f"Missing Preferred Skills: {', '.join(missing_pref) if missing_pref else 'None'}\n")
            
            f.write(f"Strengths: {', '.join(analysis.get('strengths', [])) if analysis.get('strengths') else 'None'}\n")
            f.write(f"Weak Areas: {', '.join(analysis.get('weak_areas', [])) if analysis.get('weak_areas') else 'None'}\n")
            
            recommendations = analysis.get('recommendations', [])
            f.write(f"Recommendations:\n")
            for i, rec in enumerate(recommendations, 1):
                f.write(f"  {i}. {rec}\n")
        
        if ats_data:
            f.write("\n")
            f.write("ATS SCORING RESULTS:\n")
            f.write("-"*80 + "\n")
            # Backend returns nested structure
            scoring = ats_data.get('scoring', {})
            f.write(f"ATS Score: {scoring.get('ats_score', 'N/A')}%\n")
            f.write(f"Keyword Match: {scoring.get('keyword_match_percentage', 'N/A')}%\n")
            f.write(f"Format Score: {scoring.get('format_score', 'N/A')}%\n")
            
            matched_kw = scoring.get('matched_keywords', [])
            missing_kw = scoring.get('missing_keywords', [])
            f.write(f"Matched Keywords: {', '.join(matched_kw) if matched_kw else 'None'}\n")
            f.write(f"Missing Keywords: {', '.join(missing_kw) if missing_kw else 'None'}\n")
            
            issues = scoring.get('issues', [])
            if issues:
                f.write(f"Issues Found ({len(issues)}):\n")
                for i, issue in enumerate(issues, 1):
                    f.write(f"  {i}. [{issue.get('severity', 'UNKNOWN')}] {issue.get('description', 'No description')}\n")
            
            recommendations = scoring.get('recommendations', [])
            if recommendations:
                f.write(f"Recommendations:\n")
                for i, rec in enumerate(recommendations, 1):
                    f.write(f"  {i}. {rec}\n")
        
        f.write("\n")
        f.write("="*80 + "\n")
    
    print(f"\n{Colors.BLUE}Test report saved: {report_path}{Colors.END}")


def main():
    """Main test execution"""
    print(f"{Colors.BOLD}{Colors.CYAN}")
    print("="*80)
    print("RESUME TAILOR - END-TO-END TEST SUITE")
    print("="*80)
    print(f"{Colors.END}")
    print(f"Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Backend URL: {BACKEND_URL}")
    print(f"Frontend URL: {FRONTEND_URL}")
    print(f"Resume: {RESUME_FILE.name}")
    print(f"Job Description: {JD_FILE.name}")
    
    results = TestResult()
    gap_data = None
    ats_data = None
    
    # Pre-flight checks
    print_header("PRE-FLIGHT CHECKS")
    
    if not check_server(BACKEND_URL, "Backend"):
        print(f"{Colors.RED}✗ Backend server not running at {BACKEND_URL}{Colors.END}")
        print(f"{Colors.YELLOW}Please start backend: cd backend && python -m uvicorn main:app --host 127.0.0.1 --port 8000{Colors.END}")
        sys.exit(1)
    print(f"{Colors.GREEN}✓{Colors.END} Backend server is running")
    
    if not check_server(FRONTEND_URL, "Frontend"):
        print(f"{Colors.YELLOW}⚠ Frontend server not running at {FRONTEND_URL}{Colors.END}")
        print(f"{Colors.YELLOW}Please start frontend: cd frontend && npm run dev{Colors.END}")
    else:
        print(f"{Colors.GREEN}✓{Colors.END} Frontend server is running")
    
    # Execute tests
    print_header("EXECUTING TESTS")
    
    # Test 1: Backend Health
    backend_ok = test_backend_health(results)
    
    # Test 2: Frontend Availability
    test_frontend_available(results)
    
    if not backend_ok:
        print(f"\n{Colors.RED}Backend not healthy. Stopping tests.{Colors.END}")
        results.summary()
        sys.exit(1)
    
    # Test 3: Resume Upload
    resume_id = test_resume_upload(results)
    
    # Test 4: JD Upload
    jd_id = test_jd_upload(results)
    
    # Test 5 & 6: Analysis (only if uploads succeeded)
    if resume_id and jd_id:
        gap_data = test_gap_analysis(results, resume_id, jd_id)
        ats_data = test_ats_scoring(results, resume_id, jd_id)
    else:
        results.add_skip("Gap Analysis", "Resume or JD upload failed")
        results.add_skip("ATS Scoring", "Resume or JD upload failed")
    
    # Summary
    success = results.summary()
    
    # Generate report
    generate_test_report(results, gap_data, ats_data)
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
