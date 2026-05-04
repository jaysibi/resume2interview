# Job Scraper Troubleshooting Report

## Issue Summary
**Problem**: Getting "Not Found" error when pasting job URLs in the Job Posting URL field.

## Root Cause Analysis

### Diagnostic Test Results
Ran comprehensive tests on the job scraper with multiple job boards:

1. **LinkedIn** - 404 Not Found (test URLs were invalid)
2. **Indeed** - 403 Forbidden (bot detection/blocking)
3. **Naukri** - Redirect to homepage → insufficient content extracted
4. **Generic** - 404 Not Found (expected for test URLs)

### Why Job Scraping Fails

#### 1. **Invalid or Expired URLs**
- Job postings get taken down, expire, or change URLs
- When a URL is invalid, job boards redirect to homepage
- Homepage doesn't have job description content → error

#### 2. **Bot Detection & Anti-Scraping**
- Many job boards (Indeed, Glassdoor) actively block scrapers
- Returns 403 Forbidden or requires CAPTCHA
- User-Agent header alone isn't sufficient

#### 3. **Authentication Requirements**
- Some job boards require login to view full details
- Scraper can't bypass login walls

#### 4. **Page Structure Changes**
- Job boards frequently update their HTML structure
- Scraper uses specific CSS selectors that may break

## Code Flow Analysis

```
Frontend (UploadPage.tsx)
  ↓
  api.fetchJdFromUrl(jobUrl)
  ↓
POST /v2/fetch-jd-from-url/
  { "job_url": "https://..." }
  ↓
Backend (main.py) - fetch_jd_from_url_endpoint()
  ↓
job_scraper.fetch_jd_from_url(url)
  ↓
  1. Detect job board
  2. Fetch page with requests
  3. Parse HTML with BeautifulSoup
  4. Extract title, company, description
  5. Validate content (min 100 chars)
  ↓
Return results or error
```

## Solutions

### Immediate Fix: Test with Valid URLs

Run the enhanced diagnostic script to test with real job URLs:

```powershell
cd C:\Projects\ResumeTailor\01-Code\backend
python test_job_scraper_enhanced.py
```

**What it does:**
- Tests URL accessibility
- Shows HTTP status, redirects, content length
- Extracts page structure info
- Runs the scraper and shows detailed results

**When prompted, paste the actual Naukri (or other) job URL** you're trying to use.

### Quick Validation Checklist

Before scraping a job URL, verify:

1. ✓ URL is valid and accessible in a browser
2. ✓ Job posting is still active (not expired/removed)
3. ✓ URL doesn't redirect to homepage or login
4. ✓ Full job description is visible without login
5. ✓ Not blocked by CAPTCHA

### Recommended Approach: FILE UPLOAD

**Best practice**: Instead of scraping, copy the job description text and save it as a `.txt` file, then upload it.

**Why?**
- ✓ 100% reliable - no scraping failures
- ✓ No bot detection issues
- ✓ Works with any job board
- ✓ Preserves exact job description content
- ✓ No dependency on URL validity

**How to:**
1. Open the job posting in a browser
2. Select and copy the job description text
3. Save it as `job_description.txt`
4. Upload via the "File Upload" option instead of "URL"

### Long-term Solutions (Development)

If scraping is essential, consider these enhancements:

#### A. Add Browser Automation (Selenium/Playwright)
```python
# Use real browser to bypass bot detection
from playwright.sync_api import sync_playwright

def scrape_with_browser(url):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)
        content = page.content()
        browser.close()
        return content
```

**Pros**: Bypasses most bot detection, handles JavaScript
**Cons**: Slower, requires browser installation

#### B. Add Proxy Rotation & Headers
```python
# Rotate user agents and IPs
HEADERS = {
    'User-Agent': random.choice(USER_AGENTS),
    'Accept': 'text/html,application/xhtml+xml',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://www.google.com/'
}

response = requests.get(url, headers=HEADERS, proxies=proxy)
```

#### C. Add Manual Text Input Option
Add a textarea in the UI for users to paste job description text directly:

```typescript
// In UploadPage.tsx
const [manualJdText, setManualJdText] = useState('');
const [useManualText, setUseManualText] = useState(false);

// UI component
{useManualText && (
  <textarea
    value={manualJdText}
    onChange={(e) => setManualJdText(e.target.value)}
    placeholder="Paste job description here..."
  />
)}
```

#### D. Improve Error Messages
Update the scraper to provide more specific error messages:

```python
# In job_scraper.py
def fetch_jd_from_url(url: str) -> Dict[str, any]:
    # ... existing code ...
    
    # Add detailed error messages
    if response.status_code == 403:
        return {
            'success': False,
            'error': 'Access blocked by job board (bot detection). Please try copying the job description text and uploading as a file instead.'
        }
    
    if response.status_code == 404:
        return {
            'success': False,
            'error': 'Job posting not found. The URL may be expired or invalid. Please verify the URL in your browser.'
        }
    
    # Check for homepage redirect
    if response.history and len(response.history) > 0:
        return {
            'success': False,
            'error': f'URL redirected to: {response.url}. The job posting may have been removed or the URL is invalid.'
        }
```

## Testing Instructions

### Test Case 1: Valid URL
1. Find an active job posting on Naukri/LinkedIn
2. Run: `python test_job_scraper_enhanced.py`
3. Paste the URL when prompted
4. Review results

### Test Case 2: Invalid URL
1. Use an expired or fake job URL
2. Run the diagnostic script
3. Observe the redirect behavior
4. Confirm proper error handling

### Test Case 3: File Upload  
1. Copy job description from any job board
2. Save as `test_job.txt`
3. Upload via frontend file upload option
4. Verify successful processing

## Current Status

✅ **Completed:**
- Diagnosed scraping issues
- Tested multiple job boards
- Created diagnostic scripts
- Traced complete code flow
- Identified root causes

⚠️ **Known Limitations:**
- Indeed blocks scrapers (403 Forbidden)
- Invalid URLs redirect to homepage
- No CAPTCHA handling
- No JavaScript rendering

🔧 **Recommended Next Steps:**
1. Test with valid, active job URLs
2. Use file upload method for reliability
3. Consider browser automation if scraping is critical
4. Add manual text input as fallback option

## Error Messages Explained

| Error | Meaning | Solution |
|-------|---------|----------|
| "404 Not Found" | URL doesn't exist or job expired | Verify URL in browser |
| "403 Forbidden" | Bot detection/blocking | Use file upload instead |
| "Could not extract sufficient job description text" | Redirected to homepage or content too short | Check if URL is valid and active |
| "Request timed out" | Network issue or site slow | Retry or check connectivity |

## Files Created for Diagnosis

1. `test_job_scraper.py` - Basic diagnostic with test URLs
2. `test_job_scraper_enhanced.py` - Interactive diagnostic with user URLs

Run either script to diagnose specific issues with your job URLs.

---

**Next Action**: Run `python test_job_scraper_enhanced.py` and test with the actual Naukri URL you're trying to scrape.
