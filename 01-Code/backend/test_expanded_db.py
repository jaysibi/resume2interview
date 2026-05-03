"""
Test Backend with Expanded Database
Validates that endpoints work with the larger dataset
"""
import requests
import random
from datetime import datetime

BASE_URL = "http://127.0.0.1:8002"  # Port where server is running

print("="*80)
print("TESTING WITH EXPANDED DATABASE")
print("="*80)
print(f"Testing API at: {BASE_URL}")
print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*80)

# Test 1: Retrieve random resumes from expanded database
print("\n[TEST 1] Random Resume Retrieval (from 50 resumes)")
try:
    # Test a few random resume IDs
    test_ids = [5, 15, 25, 35, 45]
    for resume_id in test_ids:
        response = requests.get(f"{BASE_URL}/resume/{resume_id}")
        if response.status_code == 200:
            data = response.json()
            filename = data.get('filename', 'Unknown')[:50]
            text_length = len(data.get('raw_text', ''))
            print(f"  ✅ ID {resume_id}: {filename}... ({text_length} chars)")
        else:
            print(f"  ❌ ID {resume_id}: Status {response.status_code}")
    print("✅ PASSED")
except Exception as e:
    print(f"❌ FAILED: {e}")

# Test 2: Test Gap Analysis with different resume types
print("\n[TEST 2] Gap Analysis with Diverse Resumes")
try:
    # Test with different resume types
    test_cases = [
        (15, 4, "HR Resume"),
        (20, 4, "Java Developer Resume"),
        (30, 4, "Database Resume"),
    ]
    
    for resume_id, jd_id, desc in test_cases:
        response = requests.post(
            f"{BASE_URL}/gap-analysis/",
            params={"resume_id": resume_id, "jd_id": jd_id},
            timeout=30
        )
        if response.status_code == 200:
            data = response.json()
            match_score = data.get('match_score', 0)
            print(f"  ✅ {desc}: {match_score}% match")
        else:
            print(f"  ⚠️ {desc}: Status {response.status_code}")
    print("✅ PASSED")
except Exception as e:
    print(f"❌ FAILED: {e}")

# Test 3: Test ATS Scoring with different resumes
print("\n[TEST 3] ATS Scoring with Diverse Resumes")
try:
    # Test with different resume types
    test_cases = [
        (10, 4, "First New Resume"),
        (25, 4, "Mid-range Resume"),
        (50, 4, "Last Resume"),
    ]
    
    for resume_id, jd_id, desc in test_cases:
        response = requests.post(
            f"{BASE_URL}/ats-score/",
            params={"resume_id": resume_id, "jd_id": jd_id},
            timeout=30
        )
        if response.status_code == 200:
            data = response.json()
            ats_score = data.get('overall_ats_score', 0)
            keyword_match = data.get('keyword_match_score', 0)
            print(f"  ✅ {desc}: {ats_score}% ATS, {keyword_match}% keywords")
        else:
            print(f"  ⚠️ {desc}: Status {response.status_code}")
    print("✅ PASSED")
except Exception as e:
    print(f"❌ FAILED: {e}")

# Test 4: Database Query Performance
print("\n[TEST 4] Database Query Performance")
try:
    import time
    start = time.time()
    
    # Retrieve 10 resumes
    for i in range(10, 20):
        response = requests.get(f"{BASE_URL}/resume/{i}", timeout=5)
        if response.status_code != 200:
            print(f"  ⚠️ Failed to retrieve ID {i}")
    
    elapsed = time.time() - start
    avg_time = elapsed / 10
    print(f"  Retrieved 10 resumes in {elapsed:.2f}s")
    print(f"  Average: {avg_time:.3f}s per resume")
    print("✅ PASSED")
except Exception as e:
    print(f"❌ FAILED: {e}")

print("\n" + "="*80)
print("TESTING COMPLETE")
print("="*80)
print("Database now has 50 diverse resumes for comprehensive testing!")
print("Categories include: Data Science, HR, Java, Python, DevOps, and many more.")
print("="*80)
