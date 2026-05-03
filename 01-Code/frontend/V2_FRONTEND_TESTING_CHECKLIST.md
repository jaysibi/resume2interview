# Frontend V2 Features Testing Guide

## Prerequisites

1. **Start Backend Server**
   ```bash
   cd c:\Projects\ResumeTailor\01-Code\backend
   python -m uvicorn main:app --port 8000
   ```

2. **Start Frontend Dev Server**
   ```bash
   cd c:\Projects\ResumeTailor\01-Code\frontend
   npm run dev
   ```

3. **Access Application**
   - Open browser to: http://localhost:5173

---

## Test Checklist

### ✅ Test 1: Upload Page - File Upload Mode (V1 Compatibility)

**Steps:**
1. Navigate to home page (/)
2. Select a Resume PDF file
3. Select a Job Description PDF file
4. Click "Analyze Match"

**Expected Results:**
- ✅ Files upload successfully
- ✅ Loading indicator appears
- ✅ Results page shows gap analysis
- ✅ Match score is displayed
- ✅ Skills comparison is visible
- ✅ ATS score section is shown

**Pass/Fail:** ___________

---

### ✅ Test 2: Upload Page - Job URL Fetch Mode (V2 NEW)

**Steps:**
1. Navigate to home page (/)
2. Toggle to "Fetch from URL" mode
3. Select a Resume PDF file
4. Enter job URL: `https://www.linkedin.com/jobs/view/3849876543`
5. Optional: Fill in Job Title and Company Name
6. Click "Analyze Match"

**Expected Results:**
- ✅ Toggle switches between modes smoothly
- ✅ URL input field appears
- ✅ File upload and URL fields are properly validated
- ✅ "Fetching job description..." loading state appears
- ✅ Job description is fetched from URL
- ✅ Analysis proceeds with fetched JD
- ✅ Application is created in the backend
- ✅ Results display correctly

**Pass/Fail:** ___________

**Known Issues:**
- If URL fetching fails (403/blocked), try a different job URL or use file upload mode

---

### ✅ Test 3: Applications List Page (V2 NEW)

**Steps:**
1. After completing Test 2, click "View All Applications" button
2. Or navigate directly to /applications

**Expected Results:**
- ✅ Page loads without errors
- ✅ List of applications is displayed in a table format
- ✅ Each application shows:
  - Job Title
  - Company Name
  - Resume filename
  - Status badge (color-coded)
  - Created date
  - Match score
  - "View Details" button
- ✅ Pagination appears if > 10 applications
- ✅ Empty state message shown if no applications

**Pass/Fail:** ___________

---

### ✅ Test 4: Application Detail Page (V2 NEW)

**Steps:**
1. From Applications List page, click "View Details" on any application
2. Or navigate directly to /applications/{id}

**Expected Results:**
- ✅ Page loads without errors
- ✅ Application header shows:
  - Job Title
  - Company Name
  - Status badge
  - Application date
- ✅ Resume section displays:
  - Filename
  - Upload date
  - Skills list (if available)
- ✅ Job Description section displays:
  - Filename or "Fetched from URL"
  - Job URL (if available)
  - Required/Preferred skills
- ✅ Gap Analysis section displays:
  - Match score with color indicator
  - Strengths list
  - Missing required skills
  - Missing preferred skills
  - Recommendations
- ✅ ATS Score section displays:
  - Overall ATS score with color indicator
  - Keyword match percentage
  - Format score
  - Matched keywords list
  - Missing keywords list
  - Issues and recommendations
- ✅ "Back to Applications" button works

**Pass/Fail:** ___________

---

### ✅ Test 5: Navigation and Routing

**Steps:**
1. Test navigation between all pages:
   - / (Home/Upload)
   - /applications (List)
   - /applications/{id} (Detail)
2. Use browser back/forward buttons
3. Refresh page on each route

**Expected Results:**
- ✅ All routes load correctly
- ✅ Browser back/forward works properly
- ✅ Page refresh maintains state
- ✅ No 404 errors
- ✅ No console errors

**Pass/Fail:** ___________

---

### ✅ Test 6: Responsive Design

**Steps:**
1. Test on different screen sizes:
   - Desktop (1920x1080)
   - Tablet (768x1024)
   - Mobile (375x667)
2. Resize browser window
3. Check layout on each page

**Expected Results:**
- ✅ Layout adapts to screen size
- ✅ All content remains accessible
- ✅ No horizontal scrolling (except tables on mobile)
- ✅ Buttons and inputs are touch-friendly on mobile
- ✅ Tables scroll horizontally on mobile if needed

**Pass/Fail:** ___________

---

### ✅ Test 7: Error Handling

**Steps:**
1. Try uploading invalid file types (.txt, .exe)
2. Submit form with missing required fields
3. Enter invalid job URL
4. Access non-existent application (/applications/999999)
5. Stop backend server and try to upload

**Expected Results:**
- ✅ Appropriate error messages displayed
- ✅ Form validation prevents submission
- ✅ Network errors show user-friendly messages
- ✅ 404 page or error state for invalid routes
- ✅ No application crashes

**Pass/Fail:** ___________

---

### ✅ Test 8: Loading States

**Steps:**
1. Upload resume and JD (observe loading states)
2. Fetch JD from URL (observe fetching state)
3. Navigate to applications list while loading
4. Open application details

**Expected Results:**
- ✅ Loading spinners/indicators appear
- ✅ UI is disabled during loading
- ✅ Loading messages are clear
- ✅ Loading completes or shows error

**Pass/Fail:** ___________

---

### ✅ Test 9: Data Consistency

**Steps:**
1. Create 3-5 applications using different resumes and JDs
2. Verify each application appears in the list
3. Click into each application detail
4. Verify data matches what was uploaded

**Expected Results:**
- ✅ All applications appear in list
- ✅ Application counts are accurate
- ✅ Details match uploaded data
- ✅ Scores and analyses are consistent
- ✅ No duplicate or missing data

**Pass/Fail:** ___________

---

### ✅ Test 10: Browser Compatibility

**Test Browsers:**
- [ ] Chrome/Edge (Chromium)
- [ ] Firefox
- [ ] Safari (if on Mac)

**For Each Browser:**
1. Complete Tests 1-4 (basic functionality)
2. Check for console errors
3. Verify layout and styling

**Expected Results:**
- ✅ All features work in all browsers
- ✅ No browser-specific bugs
- ✅ Styling is consistent

**Pass/Fail:** ___________

---

## Test Summary

**Total Tests:** 10
**Passed:** _____ / 10
**Failed:** _____ / 10

**Critical Issues Found:**
1. ________________________________
2. ________________________________
3. ________________________________

**Minor Issues Found:**
1. ________________________________
2. ________________________________
3. ________________________________

**Notes:**
_________________________________________________________________________
_________________________________________________________________________
_________________________________________________________________________

---

## Post-Testing Actions

If all tests pass:
- [ ] Mark Task 5 as complete
- [ ] Proceed to Phase 5: Documentation
- [ ] Prepare for production deployment

If tests fail:
- [ ] Document all failures
- [ ] Create bug tickets
- [ ] Fix critical issues before documentation
- [ ] Re-run failed tests

---

## Automated Frontend Testing (Future Enhancement)

For production, consider adding:
- Playwright/Cypress E2E tests
- React Testing Library unit tests
- Visual regression testing
- Accessibility testing (a11y)
