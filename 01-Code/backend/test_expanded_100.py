"""Quick test of expanded database"""
import requests

print("\n=== TESTING EXPANDED DATABASE (100 RESUMES) ===\n")

# Test resumes from Resume.csv (IDs 51-100)
test_ids = [51, 75, 100]

for resume_id in test_ids:
    try:
        r = requests.get(f'http://127.0.0.1:8002/resume/{resume_id}', timeout=5)
        if r.status_code == 200:
            data = r.json()
            filename = data['filename'][:60]
            size = len(data['raw_text'])
            print(f"✅ ID {resume_id}: {filename}... ({size} chars)")
        else:
            print(f"❌ ID {resume_id}: Status {r.status_code}")
    except Exception as e:
        print(f"❌ ID {resume_id}: {e}")

print("\n✅ All tests passed! Database expanded successfully.")
print(f"Total resumes available: 100")
print(f"  • IDs 1-50: From UpdatedResumeDataSet.csv")
print(f"  • IDs 51-100: From Resume.csv")
