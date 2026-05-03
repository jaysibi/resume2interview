"""Test script for V2 fetch-jd-from-url endpoint"""
import sys
sys.path.insert(0, '.')

from job_scraper import fetch_jd_from_url

# Test with a LinkedIn URL (mock - won't actually fetch)
test_url = "https://www.linkedin.com/jobs/view/1234567890/"

print("Testing job scraper...")
print(f"URL: {test_url}")

try:
    result = fetch_jd_from_url(test_url)
    if result:
        print("\n✅ Successfully fetched JD:")
        print(f"  Title: {result.get('title', 'N/A')}")
        print(f"  Company: {result.get('company', 'N/A')}")
        print(f"  Raw Text (first 200 chars): {result.get('raw_text', '')[:200]}...")
    else:
        print("\n❌ Failed to fetch JD - returned None")
except Exception as e:
    print(f"\n❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()
