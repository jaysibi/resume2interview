# Resume Tailor V1 → V2 Migration Guide

## 📋 Table of Contents

1. [Pre-Migration Checklist](#pre-migration-checklist)
2. [Backup Procedures](#backup-procedures)
3. [Migration Steps](#migration-steps)
4. [Verification & Testing](#verification--testing)
5. [API Changes](#api-changes)
6. [Frontend Updates](#frontend-updates)
7. [Rollback Procedures](#rollback-procedures)
8. [Post-Migration Tasks](#post-migration-tasks)
9. [Common Issues](#common-issues)
10. [Support](#support)

---

## Pre-Migration Checklist

### System Requirements

- ✅ Python 3.9+ installed
- ✅ PostgreSQL database running
- ✅ Current V1 instance fully functional
- ✅ Database credentials available
- ✅ Sufficient disk space (estimate: 2x current database size)
- ✅ Git repository access
- ✅ 30-60 minutes maintenance window

### Pre-Migration Assessment

Run this query to check your V1 data:

```sql
-- Connect to database
psql -U postgres -d resume_tailor_db

-- Check current data
SELECT 
    (SELECT COUNT(*) FROM resumes) as resumes,
    (SELECT COUNT(*) FROM job_descriptions) as job_descriptions,
    (SELECT COUNT(*) FROM gap_analyses) as gap_analyses,
    (SELECT COUNT(*) FROM ats_scores) as ats_scores;
```

**Expected Output:**
```
 resumes | job_descriptions | gap_analyses | ats_scores
---------+------------------+--------------+-----------
    2557 |               23 |            7 |          4
```

### Risk Assessment

**Low Risk:**
- Small dataset (<1000 resumes, <100 JDs)
- Single user environment
- Test/development instance

**Medium Risk:**
- Large dataset (1000-5000 resumes)
- Multiple users (2-10)
- Staging environment

**High Risk:**
- Very large dataset (>5000 resumes)
- Many users (>10)
- Production environment with active users

**Recommendation:** For high-risk migrations, consider migrating to a separate V2 instance first and running parallel for 1-2 weeks.

---

## Backup Procedures

### 1. Database Backup

#### Full Database Backup
```bash
# Create backup directory
mkdir -p ~/backups/resume_tailor_v1
cd ~/backups/resume_tailor_v1

# Backup entire database
pg_dump -U postgres -d resume_tailor_db -F c -f resume_tailor_v1_backup_$(date +%Y%m%d).dump

# Verify backup was created
ls -lh resume_tailor_v1_backup_*.dump
```

#### SQL Script Backup (Alternative)
```bash
# Plain SQL backup
pg_dump -U postgres -d resume_tailor_db > resume_tailor_v1_backup_$(date +%Y%m%d).sql

# Compress backup
gzip resume_tailor_v1_backup_$(date +%Y%m%d).sql
```

### 2. File System Backup

```bash
# Backup backend code
cd c:/Projects/ResumeTailor/01-Code
tar -czf ~/backups/resume_tailor_v1/backend_v1_$(date +%Y%m%d).tar.gz backend/

# Backup frontend code
tar -czf ~/backups/resume_tailor_v1/frontend_v1_$(date +%Y%m%d).tar.gz frontend/

# Backup environment file (if exists)
cp backend/.env ~/backups/resume_tailor_v1/.env.backup
```

### 3. Git Backup

```bash
# Ensure all changes are committed
cd c:/Projects/ResumeTailor
git status

# Create v1-stable tag before migration
git tag -a v1.0.0-stable -m "V1 stable before V2 migration"
git push origin v1.0.0-stable

# Verify tag was created
git tag -l
```

### 4. Verify Backups

```bash
# Test database backup integrity
pg_restore -U postgres -d postgres -l resume_tailor_v1_backup_$(date +%Y%m%d).dump | head -20

# Check file backups exist
ls -lh ~/backups/resume_tailor_v1/
```

**Expected output:**
```
-rw-r--r-- 1 user user  45M Jan 15 10:30 resume_tailor_v1_backup_20250115.dump
-rw-r--r-- 1 user user 2.1M Jan 15 10:31 backend_v1_20250115.tar.gz
-rw-r--r-- 1 user user 1.5M Jan 15 10:31 frontend_v1_20250115.tar.gz
-rw-r--r-- 1 user user  256 Jan 15 10:32 .env.backup
```

---

## Migration Steps

### Step 1: Stop Services

```bash
# Stop backend
# Press Ctrl+C in terminal running uvicorn
# Or if using systemd:
sudo systemctl stop resume-tailor-backend

# Stop frontend
# Press Ctrl+C in terminal running npm dev
# Or if using PM2:
pm2 stop resume-tailor-frontend

# Verify services stopped
curl http://localhost:8000/
# Should: Connection refused
```

### Step 2: Switch to V2 Branch

```bash
cd c:/Projects/ResumeTailor

# Fetch latest changes
git fetch origin

# Switch to v2 branch
git checkout v2

# Pull latest v2 code
git pull origin v2

# Verify branch
git branch
# Should show: * v2
```

### Step 3: Update Dependencies

```bash
# Backend dependencies
cd 01-Code/backend
pip install -r requirements.txt

# Verify new dependencies
pip list | grep -E "beautifulsoup4|requests|PyMuPDF"
# Should show:
#   beautifulsoup4==4.12.3
#   requests==2.31.0
#   PyMuPDF==...

# Frontend dependencies
cd ../frontend
npm install

# Verify no errors
npm list --depth=0
```

### Step 4: Run Database Migration

```bash
cd ../backend

# Run V2 migration script
python migrations/v2_001_migrate_to_v2_schema.py
```

**Expected Output:**
```
Starting V2 schema migration...

✓ Creating 'users' table...
✓ Creating 'applications' table...
✓ Adding 'user_id' to 'resumes' table...
✓ Adding 'tools' and 'upload_date' to 'resumes' table...
✓ Adding 'user_id', 'job_url', 'title', 'company' to 'job_descriptions' table...
✓ Adding 'application_id' to 'gap_analyses' table...
✓ Adding 'application_id' to 'ats_scores' table...
✓ Creating indexes...
✓ Updating Alembic version stamp...

✅ V2 schema migration completed successfully!

Database Statistics:
  - Resumes: 2557
  - Job Descriptions: 23
  - Gap Analyses: 7
  - ATS Scores: 4
  - Users: 0 (to be created on first use)
  - Applications: 0 (to be created on first use)

Next Steps:
  1. Verify migration: python verify_v2_schema.py
  2. Run tests: pytest test_v2_integration.py -v
  3. Start backend: uvicorn main:app --reload
```

**If migration fails:**
```bash
# Check error message
# Most common issues:
#   1. Database connection failed → Check DATABASE_URL
#   2. Table already exists → Already migrated, skip to verification
#   3. Permission denied → Check database user permissions
```

### Step 5: Verify Migration

```bash
# Run verification script
python verify_v2_schema.py
```

**Expected Output:**
```
Resume Tailor V2 Schema Verification
====================================

Running 7 comprehensive checks...

1. ✅ Tables Exist
   All 7 required tables are present:
   - users
   - resumes
   - job_descriptions
   - applications
   - gap_analyses
   - ats_scores
   - alembic_version

2. ✅ Columns Complete
   All expected columns present in all tables
   
3. ✅ Foreign Keys
   All 7 foreign key relationships verified:
   - resumes.user_id → users.id
   - job_descriptions.user_id → users.id
   - applications.user_id → users.id
   - applications.resume_id → resumes.id
   - applications.jd_id → job_descriptions.id
   - gap_analyses.application_id → applications.id
   - ats_scores.application_id → applications.id

4. ✅ Indexes
   All 4 critical indexes present:
   - idx_users_email
   - idx_resumes_user_id
   - idx_jds_user_id
   - idx_applications_user_id

5. ✅ Data Integrity
   Database contents:
   - Users: 0
   - Resumes: 2557 (0 orphaned)
   - Job Descriptions: 23 (0 orphaned)
   - Applications: 0
   - Gap Analyses: 7 (0 orphaned)
   - ATS Scores: 4 (0 orphaned)

6. ✅ Relationships
   All ORM relationships working correctly

7. ✅ V2 Enhancements
   All V2-specific columns present:
   - resumes: user_id, tools, upload_date
   - job_descriptions: user_id, job_url, title, company

====================================
🎉 ALL CHECKS PASSED (7/7)

Database V2 schema is correctly configured!
Your V1 data has been successfully migrated.
====================================
```

**If verification fails:**
- Review the specific check that failed
- Check migration logs for errors
- Consult [Common Issues](#common-issues) section
- Consider rollback if critical failures

### Step 6: Run Integration Tests

```bash
# Run all V2 integration tests
pytest test_v2_integration.py -v

# Run V1 backward compatibility tests
pytest e2e_test_v2.py::TestV1WorkflowBackwardCompatibility -v
```

**Expected Output:**
```
test_v2_integration.py::test_database_schema_v2 PASSED                  [  9%]
test_v2_integration.py::test_upload_resume_v2 PASSED                    [ 18%]
test_v2_integration.py::test_upload_jd_v2 PASSED                        [ 27%]
test_v2_integration.py::test_gap_analysis_v2 PASSED                     [ 36%]
test_v2_integration.py::test_gap_analysis_with_application PASSED       [ 45%]
test_v2_integration.py::test_ats_score_v2 PASSED                        [ 54%]
test_v2_integration.py::test_fetch_jd_from_url PASSED                   [ 63%]
test_v2_integration.py::test_applications_list PASSED                   [ 72%]
test_v2_integration.py::test_application_detail PASSED                  [ 81%]
test_v2_integration.py::test_create_user PASSED                         [ 90%]
test_v2_integration.py::test_create_application PASSED                  [100%]

================================= 11 passed in 15.2s =================================

e2e_test_v2.py::TestV1WorkflowBackwardCompatibility::test_v1_resume_upload PASSED
e2e_test_v2.py::TestV1WorkflowBackwardCompatibility::test_v1_gap_analysis PASSED
e2e_test_v2.py::TestV1WorkflowBackwardCompatibility::test_v1_ats_score PASSED

================================= 3 passed in 8.5s ===================================
```

**If tests fail:**
- Note specific failing test
- Check test output for error details
- Verify environment variables set (DATABASE_URL, OPENAI_API_KEY)
- Run individual test for details: `pytest test_v2_integration.py::test_name -v -s`

### Step 7: Start Services

```bash
# Start backend
cd 01-Code/backend
uvicorn main:app --reload

# Wait for startup message:
# INFO:     Application startup complete.
# INFO:     Uvicorn running on http://127.0.0.1:8000

# In new terminal, start frontend
cd 01-Code/frontend
npm run dev

# Wait for startup:
# ➜  Local:   http://localhost:5173/
```

### Step 8: Smoke Test

```bash
# Test health endpoint
curl http://localhost:8000/
# Expected: {"status":"healthy","version":"2.0"}

# Test V2 endpoint
curl http://localhost:8000/v2/applications/?user_email=test@example.com
# Expected: {"total":0,"applications":[]}

# Test frontend loads
curl http://localhost:5173/
# Expected: HTML content with "Resume Tailor" title
```

---

## Verification & Testing

### Manual API Testing

Use the provided manual testing script:

```bash
cd 01-Code/backend
python test_v2_api_manual.py
```

**Expected Output:**
```
Resume Tailor V2 - Manual API Testing
======================================

Test 1: Health Check
-------------------
✅ Health check passed
Response: {"status":"healthy","version":"2.0"}

Test 2: Resume Upload (V2)
---------------------------
Creating test resume PDF...
Uploading resume with user context...
✅ Resume upload passed
Resume ID: 2558

Test 3: JD Upload (V2)
----------------------
Creating test JD PDF...
Uploading JD with metadata...
✅ JD upload passed
JD ID: 24

Test 4: Gap Analysis with Application
--------------------------------------
Running gap analysis with create_application=true...
✅ Gap analysis passed
Match Score: 85%
Application ID: 1

Test 5: Fetch JD from URL
--------------------------
Fetching from LinkedIn URL...
✅ JD fetch passed
Title: Senior Software Engineer
Company: TechCorp

Test 6: Applications List
--------------------------
Getting all applications for user...
✅ Applications list passed
Total: 1 application

Test 7: Application Details
----------------------------
Getting details for application 1...
✅ Application details passed
Job: Senior Software Engineer at TechCorp

Test 8: ATS Score
-----------------
Getting ATS score...
✅ ATS score passed
Score: 78/100

======================================
All 8 tests passed! ✅
```

### Frontend Testing

Use the frontend testing checklist:

1. Open [V2_FRONTEND_TESTING_CHECKLIST.md](V2_FRONTEND_TESTING_CHECKLIST.md)
2. Follow each test scenario:
   - ✅ Test 1: File Upload (V1 compatibility)
   - ✅ Test 2: URL Fetch (V2 feature)
   - ✅ Test 3: Applications List
   - ✅ Test 4: Application Details
   - ✅ Test 5: Navigation
   - ✅ Test 6: Responsive Design
   - ✅ Test 7: Error Handling
   - ✅ Test 8: Loading States
   - ✅ Test 9: Data Consistency
   - ✅ Test 10: Browser Compatibility

### Data Integrity Check

```sql
-- Connect to database
psql -U postgres -d resume_tailor_db

-- Check for orphaned records
SELECT 
    'Orphaned Resumes' as check_type,
    COUNT(*) as count
FROM resumes 
WHERE user_id IS NOT NULL 
    AND user_id NOT IN (SELECT id FROM users)

UNION ALL

SELECT 
    'Orphaned Job Descriptions',
    COUNT(*)
FROM job_descriptions 
WHERE user_id IS NOT NULL 
    AND user_id NOT IN (SELECT id FROM users)

UNION ALL

SELECT 
    'Orphaned Gap Analyses',
    COUNT(*)
FROM gap_analyses 
WHERE application_id IS NOT NULL 
    AND application_id NOT IN (SELECT id FROM applications);
```

**Expected Result:** All counts should be 0.

---

## API Changes

### Breaking Changes

#### 1. Required Parameter: `user_email`

**V1 API Call:**
```bash
curl -X POST http://localhost:8000/upload-resume/ \
  -F "file=@resume.pdf"
```

**V2 API Call:**
```bash
curl -X POST http://localhost:8000/upload-resume/ \
  -F "file=@resume.pdf" \
  -F "user_email=john@example.com"  # ← Required in V2
```

**Migration Action:**
- Update all API clients to include `user_email`
- Add email input to frontend forms
- Update integration tests with user_email

#### 2. New Response Fields

**Gap Analysis V1 Response:**
```json
{
  "match_score": 85,
  "matching_skills": [...],
  "missing_skills": [...],
  "recommendations": "..."
}
```

**Gap Analysis V2 Response (with create_application=true):**
```json
{
  "match_score": 85,
  "matching_skills": [...],
  "missing_skills": [...],
  "recommendations": "...",
  "application_id": 1  # ← New field
}
```

**Migration Action:**
- Update response parsing to handle optional `application_id`
- Don't break if field is missing (backward compatible)

### New Endpoints

#### 1. `POST /v2/fetch-jd-from-url/`

**Usage:**
```bash
curl -X POST http://localhost:8000/v2/fetch-jd-from-url/ \
  -H "Content-Type: application/json" \
  -d '{"job_url": "https://www.linkedin.com/jobs/view/123456"}'
```

**Integration:**
```python
# Add to your API client
def fetch_jd_from_url(self, job_url):
    response = requests.post(
        f"{self.base_url}/v2/fetch-jd-from-url/",
        json={"job_url": job_url}
    )
    return response.json()
```

#### 2. `GET /v2/applications/`

**Usage:**
```bash
curl "http://localhost:8000/v2/applications/?user_email=john@example.com"
```

**Integration:**
```python
def list_applications(self, user_email):
    response = requests.get(
        f"{self.base_url}/v2/applications/",
        params={"user_email": user_email}
    )
    return response.json()
```

#### 3. `GET /v2/applications/{app_id}/`

**Usage:**
```bash
curl http://localhost:8000/v2/applications/1/
```

**Integration:**
```python
def get_application(self, app_id):
    response = requests.get(
        f"{self.base_url}/v2/applications/{app_id}/"
    )
    return response.json()
```

### Deprecated Endpoints

**None.** All V1 endpoints are maintained with V2 enhancements.

---

## Frontend Updates

### Required Changes

#### 1. Add Email Input to Forms

**Before (V1):**
```jsx
<form onSubmit={handleUpload}>
  <input type="file" name="resume" />
  <button>Upload</button>
</form>
```

**After (V2):**
```jsx
<form onSubmit={handleUpload}>
  <input type="email" name="userEmail" required />  {/* ← Add this */}
  <input type="file" name="resume" />
  <button>Upload</button>
</form>
```

#### 2. Update API Calls

**Before (V1):**
```javascript
const formData = new FormData();
formData.append('file', file);

await axios.post('/upload-resume/', formData);
```

**After (V2):**
```javascript
const formData = new FormData();
formData.append('file', file);
formData.append('user_email', userEmail);  // ← Add this

await axios.post('/upload-resume/', formData);
```

#### 3. Add New Pages

Create these new components:

**1. Fetch from URL Page:**
```javascript
// src/pages/FetchFromURL.jsx
import { useState } from 'react';
import axios from 'axios';

export default function FetchFromURL() {
  const [jobUrl, setJobUrl] = useState('');
  const [userEmail, setUserEmail] = useState('');
  const [result, setResult] = useState(null);
  
  const handleFetch = async () => {
    const response = await axios.post('/v2/fetch-jd-from-url/', {
      job_url: jobUrl
    });
    setResult(response.data);
  };
  
  return (
    <div>
      <input 
        type="url" 
        value={jobUrl} 
        onChange={(e) => setJobUrl(e.target.value)}
        placeholder="Job posting URL"
      />
      <input 
        type="email" 
        value={userEmail} 
        onChange={(e) => setUserEmail(e.target.value)}
        placeholder="Your email"
      />
      <button onClick={handleFetch}>Fetch JD</button>
      {result && <div>{result.title} at {result.company}</div>}
    </div>
  );
}
```

**2. Applications Dashboard:**
```javascript
// src/pages/Applications.jsx
import { useState, useEffect } from 'react';
import axios from 'axios';

export default function Applications() {
  const [applications, setApplications] = useState([]);
  const [userEmail, setUserEmail] = useState('');
  
  const loadApplications = async () => {
    const response = await axios.get('/v2/applications/', {
      params: { user_email: userEmail }
    });
    setApplications(response.data.applications);
  };
  
  return (
    <div>
      <input 
        type="email"value={userEmail}
        onChange={(e) => setUserEmail(e.target.value)}
        placeholder="Your email"
      />
      <button onClick={loadApplications}>Load Applications</button>
      
      <div>
        {applications.map(app => (
          <div key={app.id}>
            <h3>{app.job_title} at {app.company}</h3>
            <p>Match Score: {app.match_score}%</p>
            <p>Created: {new Date(app.created_at).toLocaleDateString()}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
```

#### 4. Update Routing

**Before (V1):**
```javascript
// src/App.jsx
<Routes>
  <Route path="/" element={<Home />} />
</Routes>
```

**After (V2):**
```javascript
// src/App.jsx
<Routes>
  <Route path="/" element={<Home />} />
  <Route path="/fetch-url" element={<FetchFromURL />} />  {/* ← Add */}
  <Route path="/applications" element={<Applications />} />  {/* ← Add */}
</Routes>
```

---

## Rollback Procedures

### When to Rollback

Roll back to V1 if:
- ❌ Migration verification fails (>2 checks failed)
- ❌ Integration tests fail (>30% failure rate)
- ❌ Critical data loss detected
- ❌ Production system unavailable for >15 minutes
- ❌ Unforeseen critical issues

### Rollback Steps

#### 1. Stop V2 Services

```bash
# Stop backend (Ctrl+C or)
sudo systemctl stop resume-tailor-backend

# Stop frontend
pm2 stop resume-tailor-frontend
```

#### 2. Restore Database

```bash
# Drop V2 database
psql -U postgres
DROP DATABASE resume_tailor_db;
CREATE DATABASE resume_tailor_db;
\q

# Restore V1 backup
pg_restore -U postgres -d resume_tailor_db ~/backups/resume_tailor_v1/resume_tailor_v1_backup_YYYYMMDD.dump

# Or if using SQL backup:
gunzip -c ~/backups/resume_tailor_v1/resume_tailor_v1_backup_YYYYMMDD.sql.gz | psql -U postgres -d resume_tailor_db
```

#### 3. Restore Code

```bash
cd c:/Projects/ResumeTailor

# Switch back to V1
git checkout main  # or v1.0.0-stable tag

# Restore dependencies
cd 01-Code/backend
pip install -r requirements.txt

cd ../frontend
npm install
```

#### 4. Verify V1 Restoration

```bash
# Check database
psql -U postgres -d resume_tailor_db -c "SELECT COUNT(*) FROM resumes;"

# Start backend
cd 01-Code/backend
uvicorn main:app --reload

# Test health
curl http://localhost:8000/
# Expected: {"status":"healthy"}
```

#### 5. Document Rollback

Create rollback report:
```bash
cat > ~/rollback_report_$(date +%Y%m%d).txt << EOF
Rollback Report - Resume Tailor V2 Migration

Date: $(date)
Reason: [DESCRIBE REASON]
V2 Migration Date: [DATE]
Rollback Completion: $(date)

Issues Encountered:
- [LIST ISSUES]

V1 Restoration Status:
- Database: $(psql -U postgres -d resume_tailor_db -c "SELECT COUNT(*) FROM resumes;" -t)
- Backend: [RUNNING/STOPPED]
- Frontend: [RUNNING/STOPPED]

Next Steps:
- [ACTIONS TO INVESTIGATE ISSUES]
- [PLAN FOR RETRY]
EOF
```

---

## Post-Migration Tasks

### 1. Monitor System

**First 24 Hours:**
- Check logs every 2 hours
- Monitor disk space
- Watch for errors in application logs
- Track API response times

**First Week:**
- Daily health checks
- Review user feedback
- Monitor database performance
- Check error rates

### 2. Update Documentation

- ✅ Update README with V2 features
- ✅ Share V2 user guide with users
- ✅ Update API documentation links
- ✅ Add V2 examples to wikis/docs

### 3. User Communication

**Notification Template:**
```
Subject: Resume Tailor V2 - New Features Available!

Hi [User],

We've successfully upgraded Resume Tailor to Version 2! 🎉

New Features:
- Multi-user support with email-based accounts
- Application tracking dashboard
- Automatic job description fetching from URLs
- Enhanced metadata and analytics

What You Need to Know:
- All your V1 data is preserved
- You'll now enter your email when uploading resumes
- New "Applications" page to track all your job applications
- New "Fetch from URL" feature for easy JD extraction

Getting Started:
1. Visit http://your-server:5173
2. Upload a resume with your email
3. Try the new URL fetch feature!

Questions? Check out our User Guide: [LINK]

Thanks,
The Resume Tailor Team
```

### 4. Performance Optimization

```bash
# Analyze query performance
psql -U postgres -d resume_tailor_db

-- Check slow queries
SELECT query, calls, total_time, mean_time
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 10;

-- Vacuum and analyze
VACUUM ANALYZE;

-- Reindex if needed
REINDEX DATABASE resume_tailor_db;
```

### 5. Backup Schedule

Set up automated backups:

```bash
# Create backup script
cat > ~/backup_resume_tailor_v2.sh << 'EOF'
#!/bin/bash
BACKUP_DIR=~/backups/resume_tailor_v2
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Database backup
pg_dump -U postgres -d resume_tailor_db -F c -f $BACKUP_DIR/db_backup_$DATE.dump

# Rotate old backups (keep last 7 days)
find $BACKUP_DIR -name "db_backup_*.dump" -mtime +7 -delete

echo "Backup completed: db_backup_$DATE.dump"
EOF

chmod +x ~/backup_resume_tailor_v2.sh

# Add to crontab (daily at 2 AM)
(crontab -l ; echo "0 2 * * * ~/backup_resume_tailor_v2.sh") | crontab -
```

---

## Common Issues

### Issue 1: Migration Script Fails

**Error:** `Table 'users' already exists`

**Cause:** Migration already run or partial completion

**Solution:**
```sql
-- Check migration status
psql -U postgres -d resume_tailor_db
SELECT * FROM alembic_version;

-- If shows V2 version, migration already complete
-- Skip migration, proceed to verification
```

---

### Issue 2: Foreign Key Constraint Violations

**Error:** `Foreign key violation: user_id does not exist`

**Cause:** Trying to use old resume without user_email

**Solution:**
```bash
# Create user first
curl -X POST http://localhost:8000/upload-resume/ \
  -F "file=@any_resume.pdf" \
  -F "user_email=john@example.com"

# User is created automatically, resume linked
# Now old resumes can be accessed with this email
```

---

### Issue 3: Tests Failing

**Error:** `test_v2_integration.py::test_upload_resume_v2 FAILED`

**Cause:** Missing dependencies or environment variables

**Solution:**
```bash
# Install test dependencies
pip install pytest PyMuPDF requests

# Set environment variables
export DATABASE_URL="postgresql://postgres:password@localhost/resume_tailor_db"
export OPENAI_API_KEY="sk-your-key"

# Run tests again
pytest test_v2_integration.py -v
```

---

### Issue 4: Frontend Not Loading V2 Features

**Error:** Applications page shows 404

**Cause:** Frontend not updated or routing not configured

**Solution:**
```bash
# Ensure on v2 branch
cd 01-Code/frontend
git branch  # Should show * v2

# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install

# Clear cache and restart
npm run dev -- --force
```

---

### Issue 5: Job URL Fetch Not Working

**Error:** `Failed to fetch job description from URL`

**Cause:** Unsupported platform or network issue

**Solution:**
1. Verify URL is from supported platform (LinkedIn, Indeed, Glassdoor, AngelList, YC)
2. Check network connectivity
3. Try URL in browser first
4. Fallback to manual JD upload if persist

---

## Support

### Self-Service Resources

1. **Documentation:**
   - [USER_GUIDE_V2.md](USER_GUIDE_V2.md) - Complete user guide
   - [API_DOCUMENTATION_V2.md](API_DOCUMENTATION_V2.md) - API reference
   - [RELEASE_NOTES_V2.md](RELEASE_NOTES_V2.md) - What's new in V2

2. **Testing:**
   - Run verification: `python verify_v2_schema.py`
   - Run integration tests: `pytest test_v2_integration.py -v`
   - Run manual tests: `python test_v2_api_manual.py`

3. **Logs:**
   - Backend logs: Check uvicorn terminal output
   - Database logs: `tail -f /var/log/postgresql/postgresql-*.log`
   - Frontend logs: Browser console (F12)

### Getting Help

If issues persist after consulting documentation:

1. **Collect Information:**
   ```bash
   # System info
   python --version
   psql --version
   
   # Database status
   python verify_v2_schema.py > migration_status.txt
   
   # Test results
   pytest test_v2_integration.py -v > test_results.txt
   
   # Logs
   # Include last 50 lines of logs
   ```

2. **Review Common Issues** section above

3. **Check Git Issues:** Look for similar problems in repository issues

4. **Rollback if Critical:** Use rollback procedure if production impacted

---

## Summary Checklist

Use this checklist to track migration progress:

```
Pre-Migration:
☐ System requirements met
☐ Database backup completed
☐ Code backup completed
☐ Git tag created
☐ Maintenance window scheduled

Migration:
☐ Services stopped
☐ V2 branch checked out
☐ Dependencies updated
☐ Migration script run successfully
☐ Schema verification passed (7/7)
☐ Integration tests passed (11/11)
☐ Services restarted
☐ Smoke tests passed

Post-Migration:
☐ Manual API tests passed
☐ Frontend tests completed
☐ Data integrity verified
☐ Documentation updated
☐ Users notified
☐ Monitoring enabled
☐ Backup schedule configured

Sign-off:
☐ Migration approved by: ________________
☐ Date: ________________
☐ V2 Status: Production Ready ✅
```

---

**Migration Guide Version:** 2.0.0  
**Last Updated:** January 2025  
**Status:** Complete ✅

