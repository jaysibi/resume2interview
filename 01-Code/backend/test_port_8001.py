"""Test endpoint on port 8001 (without --reload)"""
import requests
import time

print("Testing on port 8001 (without --reload)...")
start = time.time()
try:
    response = requests.post(
        'http://127.0.0.1:8001/gap-analysis/', 
        params={'resume_id': 5, 'jd_id': 4},
        timeout=30
    )
    elapsed = time.time() - start
    print(f"Status: {response.status_code}")
    print(f"Time: {elapsed:.1f}s")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Match Score: {data.get('analysis', {}).get('match_score')}%")
        print("✅ SUCCESS!")
    else:
        print(f"Response: {response.text[:200]}")
        print("❌ FAIL")
except Exception as e:
    elapsed = time.time() - start
    print(f"❌ ERROR after {elapsed:.1f}s: {e}")
