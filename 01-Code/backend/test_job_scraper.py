"""
Test script to diagnose job scraping issues
Tests the scraper directly with various job board URLs
"""
import sys
import logging
from job_scraper import fetch_jd_from_url, detect_job_board

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] %(levelname)s: %(message)s'
)

# Test URLs from different job boards
test_urls = {
    "LinkedIn": "https://www.linkedin.com/jobs/view/3847234567",
    "Indeed": "https://www.indeed.com/viewjob?jk=test123",
    "Naukri": "https://www.naukri.com/job-listings-software-engineer-xyz-company-bangalore",
    "Generic": "https://example.com/jobs/test"
}

def test_scraper_with_url(name, url):
    """Test scraper with a specific URL"""
    print(f"\n{'='*80}")
    print(f"Testing: {name}")
    print(f"URL: {url}")
    print(f"{'='*80}")
    
    # Detect job board
    job_board = detect_job_board(url)
    print(f"Detected job board: {job_board}")
    
    # Try to fetch JD
    print("\nFetching job description...")
    result = fetch_jd_from_url(url)
    
    # Display results
    print(f"\nResult:")
    print(f"  Success: {result.get('success', False)}")
    
    if result.get('success'):
        print(f"  Title: {result.get('title', 'N/A')}")
        print(f"  Company: {result.get('company', 'N/A')}")
        print(f"  Job Board: {result.get('job_board', 'N/A')}")
        text_preview = result.get('raw_text', '')[:200]
        print(f"  Text Preview: {text_preview}...")
    else:
        print(f"  Error: {result.get('error', 'Unknown error')}")
    
    return result

def main():
    """Run all tests"""
    print("Job Scraper Diagnostic Test")
    print("="*80)
    
    results = {}
    for name, url in test_urls.items():
        try:
            result = test_scraper_with_url(name, url)
            results[name] = result
        except Exception as e:
            print(f"\nEXCEPTION while testing {name}: {str(e)}")
            import traceback
            traceback.print_exc()
            results[name] = {"success": False, "error": str(e)}
    
    # Summary
    print(f"\n\n{'='*80}")
    print("SUMMARY")
    print(f"{'='*80}")
    for name, result in results.items():
        status = "✓ SUCCESS" if result.get('success') else "✗ FAILED"
        error = f" - {result.get('error', 'Unknown error')}" if not result.get('success') else ""
        print(f"{name:15} {status}{error}")

if __name__ == "__main__":
    main()
