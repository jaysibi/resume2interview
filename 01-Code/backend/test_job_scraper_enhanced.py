"""
Enhanced job scraper test with real URLs
Tests with actual accessible job postings
"""
import sys
import logging
import requests
from bs4 import BeautifulSoup
from job_scraper import fetch_jd_from_url, detect_job_board

# Configure detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] %(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)

def test_url_accessibility(url):
    """Test if URL is accessible before scraping"""
    print(f"\n  Testing URL accessibility...")
    try:
        response = requests.get(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }, timeout=10, allow_redirects=True)
        
        print(f"  Status Code: {response.status_code}")
        print(f"  Final URL: {response.url}")
        print(f"  Content Length: {len(response.content)} bytes")
        
        # Check for redirects
        if response.history:
            print(f"  Redirects: {len(response.history)}")
            for i, resp in enumerate(response.history):
                print(f"    {i+1}. {resp.status_code} -> {resp.url}")
        
        # Parse and show page structure
        soup = BeautifulSoup(response.content, 'html.parser')
        print(f"  Page Title: {soup.title.string if soup.title else 'No title'}")
        
        # Look for common job posting indicators
        h1_tags = soup.find_all('h1')
        print(f"  H1 tags found: {len(h1_tags)}")
        if h1_tags:
            print(f"    First H1: {h1_tags[0].get_text(strip=True)[:100]}")
        
        # Check text content
        text = soup.get_text(separator=' ', strip=True)
        word_count = len(text.split())
        print(f"  Total words: {word_count}")
        
        return True
    except Exception as e:
        print(f"  ERROR: {str(e)}")
        return False

def test_with_custom_url():
    """Allow user to test with their own URL"""
    print("\n" + "="*80)
    print("CUSTOM URL TEST")
    print("="*80)
    print("Please provide the job posting URL you're trying to scrape:")
    print("(Press Ctrl+C to skip)")
    
    try:
        user_url = input("\nEnter URL: ").strip()
        if user_url:
            print(f"\n{'='*80}")
            print(f"Testing Custom URL")
            print(f"URL: {user_url}")
            print(f"{'='*80}")
            
            # Test accessibility
            if test_url_accessibility(user_url):
                # Test job board detection
                job_board = detect_job_board(user_url)
                print(f"\n  Detected job board: {job_board}")
                
                # Test scraper
                print(f"\n  Running scraper...")
                result = fetch_jd_from_url(user_url)
                
                print(f"\n  Result:")
                print(f"    Success: {result.get('success', False)}")
                
                if result.get('success'):
                    print(f"    Title: {result.get('title', 'N/A')}")
                    print(f"    Company: {result.get('company', 'N/A')}")
                    print(f"    Job Board: {result.get('job_board', 'N/A')}")
                    text_len = len(result.get('raw_text', ''))
                    print(f"    Text length: {text_len} characters")
                    if text_len > 0:
                        preview = result.get('raw_text', '')[:300]
                        print(f"    Preview: {preview}...")
                else:
                    print(f"    Error: {result.get('error', 'Unknown error')}")
    except KeyboardInterrupt:
        print("\n  Skipped.")

def main():
    """Run diagnostic tests"""
    print("Job Scraper Enhanced Diagnostic")
    print("="*80)
    print()
    print("This script will help diagnose job scraping issues.")
    print("It tests URL accessibility, job board detection, and content extraction.")
    print()
    
    # Test with user-provided URL
    test_with_custom_url()
    
    print("\n" + "="*80)
    print("DIAGNOSTIC COMPLETE")
    print("="*80)
    print("\nCommon issues:")
    print("  1. Invalid/expired job posting URL (redirects to homepage)")
    print("  2. Job board requires authentication (login wall)")
    print("  3. Bot detection/CAPTCHA (403 Forbidden)")
    print("  4. Page structure changed (scraper can't find content)")
    print("  5. Network/firewall blocking the request")

if __name__ == "__main__":
    main()
