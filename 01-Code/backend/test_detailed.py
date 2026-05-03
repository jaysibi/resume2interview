"""Detailed endpoint testing"""
import requests
import json

print("="*60)
print("DETAILED ENDPOINT TESTING")
print("="*60)

# Test 1: GET endpoints (known to work)
print("\n[TEST 1] GET /resume/5")
try:
    r = requests.get('http://127.0.0.1:8000/resume/5')
    print(f"Status: {r.status_code}")
    if r.status_code == 200:
        print("✅ PASS")
    else:
        print(f"❌ FAIL: {r.text[:200]}")
except Exception as e:
    print(f"❌ ERROR: {e}")

# Test 2: POST with query params (failing)
print("\n[TEST 2] POST /gap-analysis/ with query params")
try:
    r = requests.post('http://127.0.0.1:8000/gap-analysis/', params={'resume_id': 5, 'jd_id': 4})
    print(f"Status: {r.status_code}")
    print(f"Response: {r.text[:200]}")
    if r.status_code == 200:
        print("✅ PASS")
    else:
        print(f"❌ FAIL")
except Exception as e:
    print(f"❌ ERROR: {e}")

# Test 3: POST with JSON body
print("\n[TEST 3] POST /gap-analysis/ with JSON body")
try:
    r = requests.post('http://127.0.0.1:8000/gap-analysis/', json={'resume_id': 5, 'jd_id': 4})
    print(f"Status: {r.status_code}")
    print(f"Response: {r.text[:200]}")
    if r.status_code == 200:
        print("✅ PASS")
    else:
        print(f"❌ FAIL")
except Exception as e:
    print(f"❌ ERROR: {e}")

# Test 4: POST with form data
print("\n[TEST 4] POST /gap-analysis/ with form data")
try:
    r = requests.post('http://127.0.0.1:8000/gap-analysis/', data={'resume_id': 5, 'jd_id': 4})
    print(f"Status: {r.status_code}")
    print(f"Response: {r.text[:200]}")
    if r.status_code == 200:
        print("✅ PASS")
    else:
        print(f"❌ FAIL")
except Exception as e:
    print(f"❌ ERROR: {e}")

# Test 5: Simple test endpoint
print("\n[TEST 5] POST /gap-analysis-test with query params")
try:
    r = requests.post('http://127.0.0.1:8000/gap-analysis-test', params={'resume_id': 5, 'jd_id': 4})
    print(f"Status: {r.status_code}")
    print(f"Response: {r.text[:200]}")
    if r.status_code == 200:
        print("✅ PASS")
    else:
        print(f"❌ FAIL")
except Exception as e:
    print(f"❌ ERROR: {e}")

# Test 6: Check API docs
print("\n[TEST 6] GET /docs (OpenAPI docs)")
try:
    r = requests.get('http://127.0.0.1:8000/docs')
    print(f"Status: {r.status_code}")
    if r.status_code == 200:
        print("✅ API docs accessible")
    else:
        print(f"❌ FAIL")
except Exception as e:
    print(f"❌ ERROR: {e}")

print("\n" + "="*60)
