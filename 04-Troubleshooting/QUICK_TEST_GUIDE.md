# Quick Test Instructions

## To Diagnose Your Specific Job URL Issue:

### Step 1: Run the diagnostic script
```powershell
cd C:\Projects\ResumeTailor\01-Code\backend
python test_job_scraper_enhanced.py
```

### Step 2: When prompted, paste your Naukri job URL
Example: `https://www.naukri.com/job-listings-software-engineer-...`

### Step 3: Review the output
The script will show you:
- ✓ HTTP status code (200 = OK, 404 = Not Found, 403 = Blocked)
- ✓ Any redirects (indicates invalid/expired URL)
- ✓ Page title and content stats
- ✓ Whether scraping succeeded
- ✓ Specific error message if it failed

## Common Results & Solutions:

### Result: "404 Not Found"
**Problem**: Job posting doesn't exist or URL is wrong
**Solution**: 
1. Open the URL in your browser
2. Verify it shows the job posting (not a 404 page)
3. Copy the correct URL from browser address bar
4. Try again

### Result: "403 Forbidden"  
**Problem**: Website is blocking automated access
**Solution**:
**Use file upload instead:**
1. Open job posting in browser
2. Select and copy all job description text
3. Save it as `job_description.txt`
4. Upload via "File Upload" option (not URL)

### Result: "Redirected to homepage"
**Problem**: Job posting expired or removed
**Solution**:
1. Verify the job is still active on the website
2. If expired, find a different active job posting
3. Or use file upload method

### Result: "Could not extract sufficient text"
**Problem**: Page structure incompatible or login required
**Solution**:
**Use file upload method:**
1. Copy job description from browser
2. Paste into a text editor
3. Save as `.txt` file
4. Upload via file option

## Recommended: Use File Upload

**Instead of URL scraping, we recommend file upload:**

### Why?
- ✅ Always works (no bot detection)
- ✅ Works with any job board  
- ✅ No dependency on URL validity
- ✅ More reliable and faster

### How?
1. Open job posting in your browser
2. Ctrl+A to select all text (or select just job description)
3. Ctrl+C to copy
4. Paste into Notepad/text editor
5. Save as `job_description.txt`
6. Upload via the "File Upload" tab in the application

---

## Example Test Output

```
Testing Custom URL
URL: https://www.naukri.com/job-listings-software-engineer-xyz-bangalore
================================================================================

  Testing URL accessibility...
  Status Code: 301
  Final URL: https://www.naukri.com/
  Redirects: 1
    1. 301 -> https://www.naukri.com/job-listings-software-engineer-xyz-bangalore
  Page Title: Naukri.com - Job Search
  H1 tags found: 3
  Total words: 450

  Detected job board: naukri

  Running scraper...

  Result:
    Success: False
    Error: Job posting not found - URL redirected to homepage. The job may have been removed or the URL is invalid.
```

**Interpretation**: The URL redirected to Naukri homepage, meaning the job posting doesn't exist anymore. Solution: Find an active job posting or use file upload.

---

**Need Help?** Check the full report: `C:\Projects\ResumeTailor\04-Troubleshooting\JOB_SCRAPER_DIAGNOSIS.md`
