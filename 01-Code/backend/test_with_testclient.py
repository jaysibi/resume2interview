"""Test using FastAPI TestClient (bypasses HTTP layer)"""
from fastapi.testclient import TestClient
from main import app
import time

client = TestClient(app)

print("="*60)
print("TESTING WITH FastAPI TestClient")
print("="*60)

# Test 1: GET endpoint (known to work)
print("\n[TEST 1] GET /resume/5")
response = client.get("/resume/5")
print(f"Status: {response.status_code}")
if response.status_code == 200:
    print("✅ PASS")
else:
    print(f"❌ FAIL: {response.text[:200]}")

# Test 2: POST with query params (the failing one)
print("\n[TEST 2] POST /gap-analysis/ with query params")
start = time.time()
response = client.post("/gap-analysis/", params={"resume_id": 5, "jd_id": 4})
elapsed = time.time() - start
print(f"Status: {response.status_code}")
print(f"Time: {elapsed:.2f}s")
if response.status_code == 200:
    data = response.json()
    print(f"Match Score: {data.get('analysis', {}).get('match_score')}%")
    print("✅ PASS")
else:
    print(f"Response: {response.text[:300]}")
    print(f"❌ FAIL")

# Test 3: Simple test endpoint
print("\n[TEST 3] POST /gap-analysis-test with query params")
response = client.post("/gap-analysis-test", params={"resume_id": 5, "jd_id": 4})
print(f"Status: {response.status_code}")
if response.status_code == 200:
    print(f"Response: {response.json()}")
    print("✅ PASS")
else:
    print(f"❌ FAIL: {response.text[:200]}")

print("\n" + "="*60)
