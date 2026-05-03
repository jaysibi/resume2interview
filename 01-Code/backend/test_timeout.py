"""Test endpoint with longer timeout"""
import requests
import time

start = time.time()
try:
    response = requests.post('http://127.0.0.1:8000/gap-analysis/?resume_id=5&jd_id=4', timeout=30)
    elapsed = time.time() - start
    print(f'Status: {response.status_code}')
    print(f'Time: {elapsed:.1f} seconds')
    if response.status_code == 200:
        data = response.json()
        print(f'Match Score: {data.get("analysis", {}).get("match_score")}%')
        print(f'✅ SUCCESS!')
    else:
        print(f'Response: {response.json()}')
except requests.exceptions.Timeout:
    elapsed = time.time() - start
    print(f'❌ TIMEOUT after {elapsed:.1f} seconds')
except Exception as e:
    elapsed = time.time() - start
    print(f'❌ ERROR after {elapsed:.1f} seconds: {e}')
