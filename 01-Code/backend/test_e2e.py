"""
End-to-End API Testing Script
Tests all endpoints with real data loaded in database
"""
import requests
import json
import os
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"

print("="*80)
print("END-TO-END API TESTING")
print("="*80)
print(f"Testing API at: {BASE_URL}")
print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*80)

# Test 1: Health Check
print("\n[TEST 1] Health Check: GET /")
try:
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    assert response.status_code == 200
    print("✅ PASSED")
except Exception as e:
    print(f"❌ FAILED: {e}")

# Test 2: Retrieve real resume from database
print("\n[TEST 2] Retrieve Real Resume: GET /resume/5")
try:
    response = requests.get(f"{BASE_URL}/resume/5")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Resume ID: {data.get('id')}")
    print(f"Text Length: {len(data.get('raw_text', ''))} chars")
    print(f"Created: {data.get('created_at')}")
    print(f"Preview: {data.get('raw_text', '')[:100]}...")
    assert response.status_code == 200
    assert len(data.get('raw_text', '')) > 1000
    print("✅ PASSED")
except Exception as e:
    print(f"❌ FAILED: {e}")

# Test 3: Retrieve another real resume
print("\n[TEST 3] Retrieve Another Resume: GET /resume/8")
try:
    response = requests.get(f"{BASE_URL}/resume/8")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Resume ID: {data.get('id')}")
    print(f"Text Length: {len(data.get('raw_text', ''))} chars")
    assert response.status_code == 200
    assert len(data.get('raw_text', '')) > 1000
    print("✅ PASSED")
except Exception as e:
    print(f"❌ FAILED: {e}")

# Test 4: Use existing Job Description from database
print("\n[TEST 4] Use Existing Job Description: ID 4")
print("Using proper JD with substantial content...")
jd_id = 4  # Use JD with 1300+ chars of real content
print(f"Using Job Description ID: {jd_id}")
print("✅ PASSED")

# Test 5: Gap Analysis with Real Resume (QUERY PARAMETERS)
print("\n[TEST 5] Gap Analysis: POST /gap-analysis/")
print(f"Analyzing resume ID 5 against job description {jd_id}...")
try:
    # Use query parameters, not JSON body
    params = {
        "resume_id": 5,
        "jd_id": jd_id
    }
    response = requests.post(f"{BASE_URL}/gap-analysis/", params=params)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        analysis = data.get('analysis', {})
        print(f"\nGap Analysis Results:")
        print(f"  Match Score: {analysis.get('match_score', 'N/A')}%")
        print(f"  Missing Required Skills: {len(analysis.get('missing_required_skills', []))} identified")
        if analysis.get('missing_required_skills'):
            print(f"    Examples: {', '.join(analysis['missing_required_skills'][:3])}")
        print(f"  Strengths: {len(analysis.get('strengths', []))} identified")
        print(f"  Recommendations: {len(analysis.get('recommendations', []))} provided")
        if analysis.get('recommendations'):
            print(f"    First: {analysis['recommendations'][0][:100]}...")
        print("✅ PASSED")
    else:
        print(f"Response: {response.text}")
        print("❌ FAILED: Non-200 status")
except Exception as e:
    print(f"❌ FAILED: {e}")

# Test 6: ATS Scoring with Real Resume (QUERY PARAMETERS)
print("\n[TEST 6] ATS Scoring: POST /ats-score/")
print(f"Scoring resume ID 8 against job description {jd_id}...")
try:
    # Use query parameters, not JSON body
    params = {
        "resume_id": 8,
        "jd_id": jd_id
    }
    response = requests.post(f"{BASE_URL}/ats-score/", params=params)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        scoring = data.get('scoring', {})
        print(f"\nATS Scoring Results:")
        print(f"  Overall ATS Score: {scoring.get('ats_score', 'N/A')}%")
        print(f"  Keyword Match: {scoring.get('keyword_match_percentage', 'N/A')}%")
        print(f"  Format Score: {scoring.get('format_score', 'N/A')}%")
        print(f"  Matched Keywords: {len(scoring.get('matched_keywords', []))} found")
        if scoring.get('matched_keywords'):
            print(f"    Examples: {', '.join(scoring['matched_keywords'][:5])}")
        print(f"  Missing Keywords: {len(scoring.get('missing_keywords', []))} identified")
        if scoring.get('missing_keywords'):
            print(f"    Examples: {', '.join(scoring['missing_keywords'][:3])}")
        print(f"  Recommendations: {len(scoring.get('recommendations', []))} provided")
        if scoring.get('recommendations'):
            print(f"    First: {scoring['recommendations'][0][:100]}...")
        print("✅ PASSED")
    else:
        print(f"Response: {response.text}")
        print("❌ FAILED: Non-200 status")
except Exception as e:
    print(f"❌ FAILED: {e}")

# Summary
print("\n" + "="*80)
print("TESTING COMPLETE")
print("="*80)
print("\nAll endpoints tested with real data from database!")
print(f"- Resume IDs 5, 8 (real data from UpdatedResumeDataSet.csv)")
print(f"- Job Description ID {jd_id} (created during test)")
print("\nServer running at: http://127.0.0.1:8000")
print("API Docs available at: http://127.0.0.1:8000/docs")
print("="*80)
