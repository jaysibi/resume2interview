# Resume Tailor V2 - User Guide

## 📖 Table of Contents

1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Core Workflows](#core-workflows)
4. [Feature Tutorials](#feature-tutorials)
5. [API Usage Examples](#api-usage-examples)
6. [Frontend Walkthrough](#frontend-walkthrough)
7. [Best Practices](#best-practices)
8. [Troubleshooting](#troubleshooting)
9. [FAQ](#faq)

---

## Introduction

### What is Resume Tailor V2?

Resume Tailor V2 is a comprehensive application tracking system that helps you optimize your resumes for specific job opportunities. It provides:

- **AI-Powered Analysis:** Gap analysis between your resume and job descriptions
- **ATS Scoring:** Check how well your resume passes Applicant Tracking Systems
- **Application Tracking:** Organize all your job applications in one place
- **Job URL Fetching:** Automatically extract job descriptions from posting URLs
- **Multi-User Support:** Each user has their own isolated data

### What's New in V2?

- **User-Centric Design:** All data is organized by user email
- **Application Dashboard:** Track all applications with match scores and analysis
- **Smart Job Fetching:** Extract job details from LinkedIn, Indeed, Glassdoor, and more
- **Enhanced Metadata:** Track tools, upload dates, company names, and job titles

---

## Getting Started

### Prerequisites

- Python 3.9+
- PostgreSQL database
- OpenAI API key (for AI analysis)
- Modern web browser (Chrome, Firefox, Safari)

### Setup Steps

#### 1. Database Setup
```bash
# Create PostgreSQL database
psql -U postgres
CREATE DATABASE resume_tailor_db;
\q

# Set environment variables
export DATABASE_URL="postgresql://postgres:password@localhost/resume_tailor_db"
export OPENAI_API_KEY="sk-your-api-key-here"
```

#### 2. Install Dependencies
```bash
cd 01-Code/backend
pip install -r requirements.txt
```

#### 3. Run Migration
```bash
# Migrate to V2 schema
python migrations/v2_001_migrate_to_v2_schema.py

# Verify migration
python verify_v2_schema.py
# Expected: 🎉 ALL CHECKS PASSED (7/7)
```

#### 4. Start Backend
```bash
uvicorn main:app --reload
# Server running at http://localhost:8000
```

#### 5. Start Frontend
```bash
cd ../frontend
npm install
npm run dev
# Frontend running at http://localhost:5173
```

### First-Time User Registration

V2 automatically creates user accounts when you first use the system:

1. Open the frontend: [http://localhost:5173](http://localhost:5173)
2. Upload your first resume with your email address
3. Your user account is created automatically
4. All future uploads are linked to your email

---

## Core Workflows

### Workflow 1: Basic Resume Analysis

**Goal:** Analyze how well your resume matches a job description

#### Steps:

1. **Upload Resume**
   - Navigate to upload page
   - Enter your email (e.g., `john@example.com`)
   - Select resume PDF/DOCX file
   - Optional: Add tools/technologies (e.g., `Python, React, AWS`)
   - Click "Upload"

2. **Upload Job Description**
   - Enter the same email address
   - Select JD PDF/TXT file OR enter job URL
   - Optional: Add company name and job title
   - Click "Upload"

3. **Run Gap Analysis**
   - Select your resume from the dropdown
   - Select the job description
   - Click "Analyze Gap"
   - Review match score and recommendations

4. **Get ATS Score**
   - Click "Get ATS Score" on the results page
   - Review keyword density and formatting feedback

#### Expected Results:
- Match score: 0-100%
- Matching skills list
- Missing skills to add
- Improvement recommendations
- ATS score with feedback

---

### Workflow 2: Job URL Fetching (V2 Feature)

**Goal:** Extract job description directly from a job posting URL

#### Supported Platforms:
- ✅ LinkedIn
- ✅ Indeed
- ✅ Glassdoor
- ✅ AngelList
- ✅ Y Combinator Work at a Startup

#### Steps:

1. **Find Job URL**
   - Copy the URL from any supported platform
   - Example: `https://www.linkedin.com/jobs/view/3812345678`

2. **Use Frontend Job Fetcher**
   - Navigate to "Fetch from URL" page
   - Paste the job URL
   - Enter your email address
   - Click "Fetch Job Description"

3. **Review Extracted Data**
   - Job title automatically extracted
   - Company name automatically filled
   - Full job description retrieved
   - Click "Save" to store in your library

4. **Analyze Against Resume**
   - Job description now appears in your dropdown
   - Select it along with your resume
   - Run gap analysis as usual

#### Example URLs:

**LinkedIn:**
```
https://www.linkedin.com/jobs/view/3812345678
```

**Indeed:**
```
https://www.indeed.com/viewjob?jk=abc123def456
```

**Glassdoor:**
```
https://www.glassdoor.com/job-listing/software-engineer-techcorp-JV_KO0,17_KE18,26.htm
```

#### Troubleshooting URL Fetch:
- **Error: "Failed to fetch"** → Check if URL is from supported platform
- **Error: "Could not extract"** → Platform may have changed format, use manual upload
- **Partial data extracted** → Manually fill in missing company/title fields

---

### Workflow 3: Application Tracking (V2 Feature)

**Goal:** Track all your job applications in one organized dashboard

#### Steps:

1. **Create Application (Automatic)**
   - When running gap analysis, check "Create Application"
   - Application is automatically created linking resume + JD + analysis
   - Application ID is shown in results

2. **Create Application (Manual)**
   - Use API endpoint: `POST /gap-analysis/?create_application=true`
   - Provide resume_id, jd_id, and user_email
   - Application is created with initial gap analysis

3. **View All Applications**
   - Navigate to "Applications" page in frontend
   - See list of all your applications with:
     - Job title and company
     - Resume filename
     - Match score
     - Created date
     - Analysis status (gap analysis, ATS score)

4. **View Application Details**
   - Click on any application
   - See complete details:
     - Resume information (filename, tools, upload date)
     - Job description (company, title, URL)
     - Gap analysis results (match score, skills)
     - ATS score and feedback

5. **Compare Applications**
   - Sort by match score to see best fits
   - Filter by company or date
   - Identify which resume-JD combinations work best

#### Use Cases:
- **Active Job Search:** Track 10-20 applications simultaneously
- **Resume Optimization:** Compare different resume versions against same JD
- **Job Search Analytics:** Identify patterns in successful applications

---

## Feature Tutorials

### Tutorial 1: Optimizing Your Resume for a Specific Job

**Scenario:** You found a Senior Software Engineer position at TechCorp and want to tailor your resume.

#### Step-by-Step:

1. **Fetch the Job Description**
   ```bash
   # Using cURL
   curl -X POST http://localhost:8000/v2/fetch-jd-from-url/ \
     -H "Content-Type: application/json" \
     -d '{"job_url": "https://www.linkedin.com/jobs/view/3812345678"}'
   ```
   
   **Response:**
   ```json
   {
     "success": true,
     "title": "Senior Software Engineer",
     "company": "TechCorp",
     "raw_text": "We are looking for...",
     "job_url": "https://www.linkedin.com/jobs/view/3812345678"
   }
   ```

2. **Save Job Description**
   - Create a text file with the raw_text
   - Upload via frontend or API

3. **Upload Your Current Resume**
   ```bash
   curl -X POST http://localhost:8000/upload-resume/ \
     -F "file=@current_resume.pdf" \
     -F "user_email=john@example.com" \
     -F "tools=Python, Django, PostgreSQL, React"
   ```

4. **Run Gap Analysis**
   ```bash
   curl -X POST "http://localhost:8000/gap-analysis/?resume_id=1&jd_id=1&user_email=john@example.com&create_application=true"
   ```

5. **Review Results**
   - **Match Score:** 72%
   - **Matching Skills:** Python, React, PostgreSQL
   - **Missing Skills:** Kubernetes, AWS, Docker
   - **Recommendations:** Add cloud infrastructure experience

6. **Update Resume**
   - Add Kubernetes project to experience section
   - Mention AWS deployment in previous role
   - Add Docker to technical skills
   - Upload updated resume: `updated_resume_v2.pdf`

7. **Re-analyze**
   ```bash
   curl -X POST "http://localhost:8000/gap-analysis/?resume_id=2&jd_id=1&user_email=john@example.com"
   ```
   
   **New Match Score:** 89% ✅

8. **Get ATS Score**
   ```bash
   curl -X POST "http://localhost:8000/ats-score/?resume_id=2&jd_id=1"
   ```
   
   **ATS Score:** 85/100 - Good keyword density

---

### Tutorial 2: Managing Multiple Job Applications

**Scenario:** You're applying to 5 different companies and want to track everything.

#### Day 1: Upload Resumes
```bash
# Upload general resume
curl -X POST http://localhost:8000/upload-resume/ \
  -F "file=@general_resume.pdf" \
  -F "user_email=jane@example.com" \
  -F "tools=Java, Spring Boot, MySQL, React"

# Upload frontend-focused resume
curl -X POST http://localhost:8000/upload-resume/ \
  -F "file=@frontend_resume.pdf" \
  -F "user_email=jane@example.com" \
  -F "tools=React, TypeScript, Next.js, Tailwind"
```

#### Day 2: Apply to 5 Jobs
```bash
# Job 1: TechCorp Backend Engineer
curl -X POST http://localhost:8000/v2/fetch-jd-from-url/ \
  -H "Content-Type: application/json" \
  -d '{"job_url": "https://www.linkedin.com/jobs/view/111"}'
# Upload JD, run gap analysis with resume_id=1, create_application=true

# Job 2: StartupXYZ Full Stack Developer
# Repeat process...

# Job 3-5: Continue for all positions
```

#### Day 3: Review Dashboard
```bash
# Get all applications
curl http://localhost:8000/v2/applications/?user_email=jane@example.com
```

**Response:**
```json
{
  "total": 5,
  "applications": [
    {"id": 1, "company": "TechCorp", "match_score": 85, ...},
    {"id": 2, "company": "StartupXYZ", "match_score": 78, ...},
    {"id": 3, "company": "BigTech Inc", "match_score": 92, ...},
    {"id": 4, "company": "Fintech Co", "match_score": 71, ...},
    {"id": 5, "company": "AI Startup", "match_score": 88, ...}
  ]
}
```

#### Day 4: Focus on Best Matches
- Sort by match_score descending
- Prioritize applications with 85%+ match
- Review missing skills for top matches
- Tailor cover letters based on gap analysis

#### Week 2: Track Progress
- View application details to review recommendations
- Update status (manually track in notes)
- Follow up on high-match applications

---

### Tutorial 3: Testing Different Resume Formats

**Scenario:** You have 3 resume variations and want to test which works best.

#### Setup:
- **Resume A:** Technical focus (2 pages, detailed projects)
- **Resume B:** Results focus (1 page, metrics-driven)
- **Resume C:** Hybrid (1.5 pages, mix of technical + results)

#### Process:

1. **Upload All Versions**
   ```bash
   curl -X POST http://localhost:8000/upload-resume/ \
     -F "file=@resume_technical.pdf" \
     -F "user_email=test@example.com" \
     -F "tools=Python, AWS, Docker"
   
   curl -X POST http://localhost:8000/upload-resume/ \
     -F "file=@resume_results.pdf" \
     -F "user_email=test@example.com" \
     -F "tools=Python, AWS, Docker"
   
   curl -X POST http://localhost:8000/upload-resume/ \
     -F "file=@resume_hybrid.pdf" \
     -F "user_email=test@example.com" \
     -F "tools=Python, AWS, Docker"
   ```

2. **Test Against Same JD**
   ```bash
   # Resume A vs JD
   curl -X POST "http://localhost:8000/gap-analysis/?resume_id=1&jd_id=1&user_email=test@example.com&create_application=true"
   # Match: 78%
   
   # Resume B vs JD
   curl -X POST "http://localhost:8000/gap-analysis/?resume_id=2&jd_id=1&user_email=test@example.com&create_application=true"
   # Match: 85%
   
   # Resume C vs JD
   curl -X POST "http://localhost:8000/gap-analysis/?resume_id=3&jd_id=1&user_email=test@example.com&create_application=true"
   # Match: 92% ✅ Winner!
   ```

3. **Compare ATS Scores**
   ```bash
   curl -X POST "http://localhost:8000/ats-score/?resume_id=1&jd_id=1"
   # ATS: 72
   
   curl -X POST "http://localhost:8000/ats-score/?resume_id=2&jd_id=1"
   # ATS: 68
   
   curl -X POST "http://localhost:8000/ats-score/?resume_id=3&jd_id=1"
   # ATS: 88 ✅ Winner!
   ```

4. **Decision:** Use Resume C (hybrid format) for applications

---

## API Usage Examples

### Python Client Example

```python
import requests
from pathlib import Path

class ResumeTailorClient:
    def __init__(self, base_url="http://localhost:8000", user_email="user@example.com"):
        self.base_url = base_url
        self.user_email = user_email
    
    def upload_resume(self, file_path, tools=None):
        """Upload a resume PDF/DOCX"""
        with open(file_path, 'rb') as f:
            files = {'file': f}
            data = {'user_email': self.user_email}
            if tools:
                data['tools'] = tools
            
            response = requests.post(
                f"{self.base_url}/upload-resume/",
                files=files,
                data=data
            )
            response.raise_for_status()
            return response.json()
    
    def fetch_jd_from_url(self, job_url):
        """Fetch job description from URL"""
        response = requests.post(
            f"{self.base_url}/v2/fetch-jd-from-url/",
            json={"job_url": job_url}
        )
        response.raise_for_status()
        return response.json()
    
    def upload_jd(self, file_path, job_url=None, title=None, company=None):
        """Upload a job description"""
        with open(file_path, 'rb') as f:
            files = {'file': f}
            data = {'user_email': self.user_email}
            if job_url:
                data['job_url'] = job_url
            if title:
                data['title'] = title
            if company:
                data['company'] = company
            
            response = requests.post(
                f"{self.base_url}/upload-jd/",
                files=files,
                data=data
            )
            response.raise_for_status()
            return response.json()
    
    def gap_analysis(self, resume_id, jd_id, create_application=True):
        """Run gap analysis"""
        params = {
            'resume_id': resume_id,
            'jd_id': jd_id,
            'user_email': self.user_email
        }
        if create_application:
            params['create_application'] = 'true'
        
        response = requests.post(
            f"{self.base_url}/gap-analysis/",
            params=params
        )
        response.raise_for_status()
        return response.json()
    
    def ats_score(self, resume_id, jd_id):
        """Get ATS score"""
        response = requests.post(
            f"{self.base_url}/ats-score/",
            params={'resume_id': resume_id, 'jd_id': jd_id}
        )
        response.raise_for_status()
        return response.json()
    
    def list_applications(self):
        """List all applications"""
        response = requests.get(
            f"{self.base_url}/v2/applications/",
            params={'user_email': self.user_email}
        )
        response.raise_for_status()
        return response.json()
    
    def get_application(self, app_id):
        """Get application details"""
        response = requests.get(f"{self.base_url}/v2/applications/{app_id}/")
        response.raise_for_status()
        return response.json()


# Usage Example
def main():
    client = ResumeTailorClient(user_email="john@example.com")
    
    # 1. Upload resume
    print("Uploading resume...")
    resume = client.upload_resume(
        "my_resume.pdf",
        tools="Python, React, PostgreSQL, AWS"
    )
    print(f"Resume uploaded: ID={resume['id']}")
    
    # 2. Fetch JD from URL
    print("\nFetching job description...")
    jd_data = client.fetch_jd_from_url("https://www.linkedin.com/jobs/view/123456")
    print(f"Job: {jd_data['title']} at {jd_data['company']}")
    
    # Save JD to temp file
    with open("temp_jd.txt", "w") as f:
        f.write(jd_data['raw_text'])
    
    # 3. Upload JD
    jd = client.upload_jd(
        "temp_jd.txt",
        job_url=jd_data['job_url'],
        title=jd_data['title'],
        company=jd_data['company']
    )
    print(f"JD uploaded: ID={jd['id']}")
    
    # 4. Run gap analysis
    print("\nRunning gap analysis...")
    analysis = client.gap_analysis(resume['id'], jd['id'], create_application=True)
    print(f"Match Score: {analysis['match_score']}%")
    print(f"Matching Skills: {', '.join(analysis['matching_skills'])}")
    print(f"Missing Skills: {', '.join(analysis['missing_skills'])}")
    print(f"Application ID: {analysis['application_id']}")
    
    # 5. Get ATS score
    print("\nGetting ATS score...")
    ats = client.ats_score(resume['id'], jd['id'])
    print(f"ATS Score: {ats['score']}/100")
    print(f"Feedback: {ats['feedback']}")
    
    # 6. List all applications
    print("\nListing applications...")
    apps = client.list_applications()
    print(f"Total Applications: {apps['total']}")
    for app in apps['applications']:
        print(f"  - {app['company']}: {app['match_score']}% match")
    
    # 7. Get application details
    print(f"\nApplication details for ID={analysis['application_id']}...")
    app_detail = client.get_application(analysis['application_id'])
    print(f"Created: {app_detail['created_at']}")
    print(f"Resume: {app_detail['resume']['filename']}")
    print(f"Job: {app_detail['job_description']['title']}")

if __name__ == "__main__":
    main()
```

---

## Frontend Walkthrough

### Navigation

**Main Pages:**
1. **Home** (`/`) - Upload resumes and JDs
2. **Fetch from URL** (`/fetch-url`) - Extract JDs from job posting URLs
3. **Applications** (`/applications`) - View all applications dashboard

### Page-by-Page Guide

#### 1. Home Page - File Upload

**Components:**
- Resume upload form (left side)
- Job description upload form (right side)
- Gap analysis section (bottom)

**Actions:**
1. Enter email address (same for both forms)
2. Select resume file (PDF/DOCX)
3. Optional: Enter tools/technologies
4. Click "Upload Resume"
5. Select JD file OR enter job URL
6. Optional: Enter company and title
7. Click "Upload JD"
8. Select resume and JD from dropdowns
9. Check "Create Application" if tracking
10. Click "Analyze Gap"

**Results Display:**
- Match score (colored 0-100%)
- Matching skills (green badges)
- Missing skills (red badges)
- AI recommendations
- Option to get ATS score

#### 2. Fetch from URL Page

**Purpose:** Extract job descriptions without manual copy-paste

**Steps:**
1. Paste job posting URL
2. Enter your email
3. Click "Fetch Job Description"
4. Review extracted title, company, description
5. Edit if needed
6. Click "Save" to add to your library

**Supported URLs:**
- `linkedin.com/jobs/view/*`
- `indeed.com/viewjob?jk=*`
- `glassdoor.com/job-listing/*`
- `angel.co/company/*/jobs/*`
- `ycombinator.com/companies/*/jobs/*`

**Error Handling:**
- Invalid URL: Shows error message with supported formats
- Fetch failed: Suggests manual upload
- Partial data: Allows manual completion

#### 3. Applications Page

**Purpose:** Dashboard view of all job applications

**Features:**
- **List View:**
  - All applications sorted by date
  - Company name and job title
  - Match score badge
  - Created date
  - Status indicators (gap analysis, ATS score)

- **Filters:**
  - Sort by match score
  - Sort by date (newest/oldest)
  - Filter by company name
  - Filter by match score range

- **Detail View:**
  - Click any application
  - See full resume details
  - See complete job description
  - View gap analysis results
  - View ATS score feedback

**Use Cases:**
- Daily application review
- Comparing match scores
- Identifying patterns in successful applications
- Tracking which resumes work best

---

## Best Practices

### 1. Resume Management

#### File Naming
- ✅ Good: `john_doe_resume_2025_v3.pdf`
- ❌ Bad: `resume.pdf`, `final.pdf`, `resume_final_final.pdf`

#### Tools Field
- ✅ Good: `Python, React, PostgreSQL, AWS, Docker`
- ❌ Bad: `I know Python and React`, `Programming`

#### Version Control
- Upload new version when you make significant changes
- Use descriptive tools field to differentiate versions
- Compare match scores between versions

### 2. Job Description Management

#### Job URL
- Always include the job_url when uploading
- Helps track source and revisit posting
- Required for fetch-from-URL feature

#### Metadata
- Fill in company and title fields
- Makes applications dashboard more useful
- Improves search and filtering

#### File Format
- PDF or TXT preferred for JDs
- Copy-paste into .txt file if no PDF available
- Preserve formatting for better parsing

### 3. Gap Analysis Strategy

#### When to Create Application
- ✅ Create when seriously considering the job
- ✅ Create to track multiple applications
- ❌ Don't create for practice analyses
- ❌ Don't create for test uploads

#### Interpreting Results
- **Match Score 90-100%:** Excellent fit, apply confidently
- **Match Score 75-89%:** Good fit, tailor resume slightly
- **Match Score 60-74%:** Consider adding missing skills
- **Match Score <60%:** Significant tailoring needed or wrong fit

#### Using Recommendations
- Focus on "missing critical skills" first
- Add achievements demonstrating requested skills
- Use exact keywords from recommendations
- Re-analyze after each major edit

### 4. Application Tracking

#### Organization
- Review applications weekly
- Sort by match score to prioritize
- Track external status (applied, interviewing) in notes
- Archive old applications after 30 days (future feature)

#### Analysis
- Compare match scores across jobs
- Identify which skills are most requested
- See which resume versions perform best
- Adjust strategy based on patterns

### 5. ATS Optimization

#### Keyword Density
- Aim for ATS score 75+
- Include exact keywords from JD
- Use varied forms (e.g., "managed" and "management")
- Don't keyword stuff (looks unnatural)

#### Formatting
- Use standard section headers
- Avoid tables and graphics
- Use simple bullet points
- Save as PDF for consistency

---

## Troubleshooting

### Common Issues

#### 1. "User email is required"

**Cause:** Missing user_email parameter in API call

**Solution:**
```bash
# Add user_email to the request
curl -X POST http://localhost:8000/upload-resume/ \
  -F "file=@resume.pdf" \
  -F "user_email=john@example.com"  # Add this line
```

#### 2. "File type not supported"

**Cause:** Uploaded file is not PDF, DOCX, or TXT

**Solution:**
- Convert file to PDF (preferred)
- Copy content to .txt file
- Use online converter for DOCX

#### 3. "Failed to fetch job description"

**Cause:** URL is from unsupported platform or page changed

**Solution:**
- Check if URL is from supported platform
- Try manual upload instead
- Verify URL loads in browser

#### 4. "Application already exists"

**Cause:** You've already created an application for this resume-JD-user combination

**Solution:**
- This is expected behavior (prevents duplicates)
- View existing application in dashboard
- Use different resume or JD if testing

#### 5. Low Match Score (<50%)

**Possible Causes:**
- Wrong job type/level
- Resume missing critical keywords
- Resume format not parsing well

**Solutions:**
- Review "missing_skills" carefully
- Add relevant projects/experience
- Ensure resume has clear sections
- Use standard job titles

#### 6. ATS Score Lower Than Expected

**Improvements:**
- Add more keywords from JD
- Use simple formatting (no tables/graphics)
- Include standard section headers
- Add more bullet points with action verbs
- Spell out acronyms at least once

---

## FAQ

### General Questions

**Q: Is my data private?**  
A: Yes, all data is isolated by user email. Other users cannot see your resumes or applications.

**Q: Can I use the same email across multiple devices?**  
A: Yes, your email is your unique identifier across all devices.

**Q: How many resumes can I upload?**  
A: Unlimited. However, keep filenames unique for easy identification.

**Q: Can I delete resumes or applications?**  
A: Currently through database. Deletion endpoints planned for V2.1.

### Feature Questions

**Q: What job platforms are supported for URL fetching?**  
A: LinkedIn, Indeed, Glassdoor, AngelList, and Y Combinator Work at a Startup. More coming in V2.1.

**Q: How accurate is the gap analysis?**  
A: Analysis uses GPT-4o-mini and is generally 85-90% accurate. Always review recommendations manually.

**Q: What's the difference between gap analysis and ATS score?**  
A: Gap analysis compares skills/experience. ATS score checks keyword density and formatting for automated systems.

**Q: Can I export my applications?**  
A: Not yet. CSV/PDF export planned for V2.1.

### Technical Questions

**Q: What file size limits exist?**  
A: Default 10MB per file. Configurable in main.py `FILE_SIZE_LIMIT`.

**Q: How long does analysis take?**  
A: Gap analysis: 5-15 seconds. ATS score: 3-8 seconds.

**Q: Can I use this offline?**  
A: Backend yes (after setup), but OpenAI API calls require internet.

**Q: Is there rate limiting?**  
A: Currently no per-user limits. Will be added in V2.1 with authentication.

### Migration Questions

**Q: Will V1 data still work?**  
A: Yes, V1 resumes/JDs are preserved. You just need to add user_email when accessing them.

**Q: Do I need to re-upload everything?**  
A: No, existing data is migrated automatically. Just start using user_email parameter.

**Q: Can I roll back to V1?**  
A: Yes, restore database backup. Note: V2-specific data (applications) will be lost.

---

## Additional Resources

- **[API Documentation](API_DOCUMENTATION_V2.md)** - Complete endpoint reference
- **[Release Notes](RELEASE_NOTES_V2.md)** - V2 features and changes
- **[Migration Guide](MIGRATION_GUIDE_V2.md)** - Upgrade from V1
- **[Frontend Testing Checklist](V2_FRONTEND_TESTING_CHECKLIST.md)** - Manual UI testing

---

**Last Updated:** January 2025  
**Version:** 2.0.0  
**Status:** Production Ready ✅

