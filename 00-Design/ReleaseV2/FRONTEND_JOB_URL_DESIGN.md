# Resume Tailor Frontend - Job Posting URL Integration Design

## Overview
This document describes the design for adding a feature to the frontend that allows users to enter a job posting URL (e.g., Naukri, LinkedIn, Indeed) instead of uploading a job description file. The system will fetch and parse the job description from the provided URL, extract the relevant text, and use it for analysis.

---

## 1. User Flow

1. User navigates to the Upload page.
2. User sees two options for "Job Description":
   - Upload a file (existing)
   - Enter a job posting URL (new)
3. If the user enters a URL, the system fetches and parses the job description from the web page.
4. The extracted job description is displayed for user confirmation/editing (optional).
5. The analysis proceeds as usual using the extracted JD text.

---

## 2. UI/UX Changes

### **UploadPage.tsx**
- Add a toggle or tabs for "Upload JD File" vs. "Paste Job URL"
- If "Paste Job URL" is selected:
  - Show an input field for the URL
  - Show a "Fetch" button
  - Show a loading indicator while fetching
  - Display the extracted JD text in a textarea for review/editing
  - Show error messages if fetch fails or the URL is unsupported
- If "Upload JD File" is selected:
  - Show the existing file upload UI

---

## 3. API/Backend Changes
- Add a new endpoint: `POST /fetch-jd-from-url/`
  - Input: `{ url: string }`
  - Output: `{ raw_text: string, title?: string, error?: string }`
- The backend will:
  - Validate the URL (support Naukri, LinkedIn, Indeed, etc.)
  - Fetch the web page
  - Parse and extract the job description text
  - Return the extracted text to the frontend

---

## 4. Frontend Logic
- On "Fetch" button click:
  - Call the new API endpoint with the entered URL
  - Show loading state
  - On success, display the extracted JD text in a textarea
  - Allow user to edit/confirm the text
  - On confirmation, proceed as if a JD file was uploaded (store as a virtual JD)

---

## 5. Data Model Changes
- Add a new field in the frontend state: `jdUrl: string`
- Add a new field: `jdRawText: string` (for extracted JD text)
- When using a URL, create a temporary JD object for analysis

---

## 6. Error Handling
- Show clear error messages for:
  - Invalid/unsupported URLs
  - Network errors
  - Failed extraction (e.g., page structure not recognized)

---

## 7. Accessibility & UX
- All new UI elements must be keyboard accessible
- Provide clear instructions and feedback
- Allow user to switch between file upload and URL entry at any time

---

## 8. Future Enhancements
- Support more job boards (Monster, Glassdoor, etc.)
- Auto-detect job board from URL
- Auto-fill job title/company fields
- Save frequently used URLs for registered users

---

## 9. Example UI Mockup (Text)

```
[Job Description]
( ) Upload File   (•) Paste Job URL

[ URL: ____________________________ ] [Fetch]

[Loading spinner]

[Extracted JD Text]
|------------------------------------------------|
| [Editable textarea with extracted JD text]      |
|------------------------------------------------|

[Confirm & Analyze]
```

---

## 10. Impact
- Improves user experience for job seekers who prefer to use online job postings
- Reduces friction (no need to download/copy JD files)
- Enables future automation and analytics on job board sources

---

**End of Design Document**
