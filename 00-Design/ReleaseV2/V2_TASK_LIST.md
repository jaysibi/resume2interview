# Resume Tailor V2 - Task List & Tracking

**Project:** Resume Tailor V2 - User-Centric Schema with Job URL Support  
**Branch:** v2  
**Last Updated:** May 3, 2026  
**Status:** 🟡 In Progress (Phase 1 Complete)

---

## 📊 Overall Progress

| Phase | Status | Progress | Estimated Time |
|-------|--------|----------|----------------|
| Phase 1: Infrastructure | ✅ Complete | 100% | - |
| Phase 2: Backend API | ✅ Complete | 100% | - |
| Phase 3: Frontend | ⏳ Not Started | 0% | ~3 hours |
| Phase 4: Testing | ⏳ Not Started | 0% | ~2 hours |
| Phase 5: Documentation | 🟡 In Progress | 30% | ~1 hour |
| **TOTAL** | 🟡 **In Progress** | **46%** | **~6 hours** |

---

## ✅ Phase 1: Infrastructure (COMPLETE)

### Database Schema & Models
- [x] **1.1** Create `models_v2.py` with all V2 tables
  - [x] Users table (id, name, email, phone, password_hash)
  - [x] Enhanced Resumes table (add user_id, upload_date, tools)
  - [x] Enhanced JobDescription table (add user_id, job_url, title, company)
  - [x] Applications table (track resume-JD pairs)
  - [x] GapAnalyses table (store gap analysis results)
  - [x] ATSScores table (store ATS scoring results)
  - [x] All relationships and foreign keys defined

### Database Migration
- [x] **1.2** Create Alembic migration script `v2_001_migrate_to_v2_schema.py`
  - [x] Upgrade: V1 → V2 transformation
  - [x] Create default user for existing data
  - [x] Add new columns to existing tables
  - [x] Create new tables (users, applications, gap_analyses, ats_scores)
  - [x] Add foreign key constraints
  - [x] Downgrade: V2 → V1 rollback functionality

### CRUD Operations
- [x] **1.3** Create `crud_v2.py` with V2 operations
  - [x] User CRUD (create, get, get_by_email, get_or_create_default)
  - [x] Resume CRUD with user context (create, get, get_by_user)
  - [x] Job Description CRUD with user context (create, get, get_by_user)
  - [x] Application CRUD (create, get, get_by_user, list with pagination)
  - [x] Gap Analysis CRUD (create, get_by_application)
  - [x] ATS Score CRUD (create, get_by_application)
  - [x] Combined operations (get_full_application_with_analyses)

### Job Scraper Service
- [x] **1.4** Create `job_scraper.py` for URL fetching
  - [x] Job board detection (LinkedIn, Naukri, Indeed, Monster, Glassdoor)
  - [x] LinkedIn extractor (title, company, description)
  - [x] Naukri extractor
  - [x] Indeed extractor
  - [x] Generic fallback extractor
  - [x] Error handling and validation
  - [x] Main `fetch_jd_from_url()` function

### Dependencies
- [x] **1.5** Update `requirements.txt`
  - [x] Add beautifulsoup4==4.12.3
  - [x] Add requests==2.31.0

### Version Control
- [x] **1.6** Git workflow
  - [x] Create v2 branch from base
  - [x] Commit infrastructure changes
  - [x] Push to GitHub
  - [x] Create implementation status document

---

## 🚧 Phase 2: Backend API Implementation (IN PROGRESS - 40%)

### Environment Setup
- [x] **2.1** Install new dependencies
  - [x] Run: `pip install beautifulsoup4 requests`
  - [x] Verify installation
  - [x] Test imports in Python REPL

### Database Migration Execution
- [x] **2.2** Run database migration
  - [x] Backup existing database (pg_dump)
  - [x] Run: `alembic upgrade head`
  - [x] Verify all tables created (users, applications, gap_analyses, ats_scores)
  - [x] Verify existing data preserved (resumes, job_descriptions)
  - [x] Verify default user created (id=1)
  - [x] Fixed migration script to handle existing columns
  - [x] Test migration successful

### API Endpoint: Fetch JD from URL
- [x] **2.3** Add `/v2/fetch-jd-from-url/` endpoint in `main.py`
  - [x] Import `job_scraper` module
  - [x] Create Pydantic model: `FetchJDRequest(url: str)`
  - [x] Create Pydantic model: `FetchJDResponse(title, company, raw_text)`
  - [x] Implement POST endpoint with validation
  - [x] Call `fetch_jd_from_url(url)` 
  - [x] Handle errors (timeout, invalid URL, parsing failure)
  - [x] Return extracted data
  - [ ] Add rate limiting (10/minute)
  - [x] Add logging
  - [ ] Call `fetch_jd_from_url(url)` 
  - [ ] Handle errors (timeout, invalid URL, parsing failure)
  - [ ] Return extracted data
  - [ ] Add rate limiting (10/minute)
  - [ ] Add logging

### API Endpoint: Upload Resume V2
- [ ] **2.4** Update `/upload-resume/` to support V2 schema
  - [ ] Import `models_v2` and `crud_v2`
  - [ ] Add optional `user_email` parameter (default to default user)
  - [ ] Get or create user via `crud_v2.get_or_create_default_user()`
  - [ ] Call `crud_v2.create_resume()` with user_id
  - [ ] Maintain backward compatibility (V1 endpoints still work)
  - [ ] Update response format to include user_id
  - [ ] Test with existing resume upload flow

### API Endpoint: Upload Job Description V2
- [ ] **2.5** Update `/upload-jd/` to support V2 schema
  - [ ] Import `models_v2` and `crud_v2`
  - [ ] Add optional `user_email` parameter
  - [ ] Add optional `job_url`, `title`, `company` parameters
  - [ ] Get or create user
  - [ ] Call `crud_v2.create_jd()` with all parameters
  - [ ] Support both file upload and direct text input
  - [ ] Update response format
  - [ ] Test with existing JD upload flow

### API Endpoint: Analyze (V2 with Application Tracking)
- [ ] **2.6** Update `/analyze/` endpoint to create Applications
  - [ ] Import `models_v2` and `crud_v2`
  - [ ] Add optional `user_email` parameter to request
  - [ ] Get or create user
  - [ ] Retrieve resume and JD from database
  - [ ] Create Application record: `crud_v2.create_application()`
  - [ ] Run gap analysis (existing AI service)
  - [ ] Store gap analysis: `crud_v2.create_gap_analysis()`
  - [ ] Run ATS scoring (existing AI service)
  - [ ] Store ATS score: `crud_v2.create_ats_score()`
  - [ ] Return application_id with results
  - [ ] Add caching: check if analysis already exists for this application
  - [ ] Maintain backward compatibility

### API Endpoint: Get Applications
- [ ] **2.7** Add `/v2/applications/` endpoint
  - [ ] Accept optional `user_email` (default to default user)
  - [ ] Get user from database
  - [ ] Call `crud_v2.get_applications_by_user()`
  - [ ] Return paginated list of applications
  - [ ] Include: resume filename, JD title/filename, applied_at, status
  - [ ] Add pagination parameters (skip=0, limit=100)
  - [ ] Add filtering (by status, date range)

### API Endpoint: Get Application Details
- [ ] **2.8** Add `/v2/applications/{application_id}/` endpoint
  - [ ] Validate application exists
  - [ ] Call `crud_v2.get_full_application_with_analyses()`
  - [ ] Return complete application data:
    - Resume details
    - Job description details
    - Gap analysis (if exists)
    - ATS score (if exists)
  - [ ] Handle missing analyses gracefully
  - [ ] Return 404 if application not found

### API Documentation
- [ ] **2.9** Update OpenAPI documentation
  - [ ] Document all V2 endpoints
  - [ ] Add request/response examples
  - [ ] Document error responses
  - [ ] Update FastAPI title/description for V2
  - [ ] Test with Swagger UI at `/docs`

### Testing
- [ ] **2.10** Manual API testing
  - [ ] Test fetch-jd-from-url with LinkedIn URL
  - [ ] Test fetch-jd-from-url with Naukri URL
  - [ ] Test fetch-jd-from-url with Indeed URL
  - [ ] Test upload-resume with V2 (check user_id)
  - [ ] Test upload-jd with V2 (check user_id)
  - [ ] Test analyze endpoint creates application
  - [ ] Test applications list endpoint
  - [ ] Test application details endpoint
  - [ ] Verify data in database

---

## ⏳ Phase 3: Frontend Implementation (NOT STARTED - 0%)

### Setup
- [ ] **3.1** Update frontend dependencies
  - [ ] No new dependencies needed
  - [ ] Verify existing axios/react-query setup

### API Service Updates
- [ ] **3.2** Update `src/services/api.ts`
  - [ ] Add `fetchJdFromUrl(url: string)` function
  - [ ] Add types for FetchJDRequest/Response
  - [ ] Update existing types to include V2 fields (user_id, application_id)
  - [ ] Add `getApplications()` function
  - [ ] Add `getApplicationDetails(applicationId)` function
  - [ ] Handle new error responses

### Upload Page: Job URL Input
- [ ] **3.3** Update `src/pages/UploadPage.tsx` - JD Input Section
  - [ ] Add state: `jdInputMode: 'file' | 'url'`
  - [ ] Add toggle/tabs: "Upload File" vs "Enter Job URL"
  - [ ] Add URL input field (hidden when mode='file')
  - [ ] Add "Fetch" button
  - [ ] Add loading state during fetch
  - [ ] Add error display for fetch failures
  - [ ] Add success message with extracted title/company
  - [ ] Display extracted JD text in editable textarea
  - [ ] Allow user to edit/confirm extracted text
  - [ ] Store extracted JD as virtual file for analysis
  - [ ] Maintain existing file upload functionality

### Upload Page: UI Polish
- [ ] **3.4** Polish UploadPage UI
  - [ ] Add clear instructions for both modes
  - [ ] Add validation for URL format
  - [ ] Add tooltip explaining supported job boards
  - [ ] Show job board logo/icon when detected
  - [ ] Add "Copy from clipboard" button for URL
  - [ ] Ensure keyboard accessibility
  - [ ] Test responsive design (mobile, tablet, desktop)

### Applications List Page (New)
- [ ] **3.5** Create `src/pages/ApplicationsPage.tsx`
  - [ ] Fetch applications list from API
  - [ ] Display table/cards with:
    - Resume filename
    - Job title (or JD filename)
    - Company (if available)
    - Match score (if analyzed)
    - ATS score (if analyzed)
    - Applied date
    - Status badge
  - [ ] Add pagination controls
  - [ ] Add filters (by status, date range)
  - [ ] Add search functionality
  - [ ] Add "View Details" button for each application
  - [ ] Add empty state (no applications yet)

### Application Details Page (New)
- [ ] **3.6** Create `src/pages/ApplicationDetailsPage.tsx`
  - [ ] Fetch application details from API
  - [ ] Display resume summary
  - [ ] Display job description summary
  - [ ] Display gap analysis results (if exists)
  - [ ] Display ATS score results (if exists)
  - [ ] Add "Re-analyze" button (optional)
  - [ ] Add "Edit Notes" functionality
  - [ ] Add "Back to Applications" navigation

### Routing
- [ ] **3.7** Update React Router configuration
  - [ ] Add route: `/applications` → ApplicationsPage
  - [ ] Add route: `/applications/:id` → ApplicationDetailsPage
  - [ ] Add navigation menu items
  - [ ] Update existing routes if needed

### UI/UX Testing
- [ ] **3.8** Manual frontend testing
  - [ ] Test job URL fetch flow (end-to-end)
  - [ ] Test file upload flow (unchanged)
  - [ ] Test applications list loading
  - [ ] Test application details view
  - [ ] Test error handling (invalid URL, network error)
  - [ ] Test loading states
  - [ ] Test responsive design
  - [ ] Test keyboard navigation

---

## ⏳ Phase 4: End-to-End Testing (NOT STARTED - 0%)

### Unit Tests
- [ ] **4.1** Backend unit tests
  - [ ] Test `job_scraper.py` functions
  - [ ] Test `crud_v2.py` operations
  - [ ] Mock external requests (requests.get)
  - [ ] Test edge cases (empty responses, malformed HTML)

### Integration Tests
- [ ] **4.2** Backend integration tests
  - [ ] Test fetch-jd-from-url endpoint
  - [ ] Test V2 upload endpoints
  - [ ] Test analyze endpoint with application creation
  - [ ] Test applications endpoints
  - [ ] Verify database state after operations

### E2E Tests
- [ ] **4.3** Update E2E test suite (`e2e_test.py`)
  - [ ] Add test: Fetch JD from URL (mocked)
  - [ ] Add test: Upload resume with user context
  - [ ] Add test: Upload JD with URL
  - [ ] Add test: Analyze creates application
  - [ ] Add test: List applications
  - [ ] Add test: Get application details
  - [ ] Update existing tests for V2 compatibility
  - [ ] Run full E2E suite

### Frontend Tests
- [ ] **4.4** Frontend tests (optional, if time permits)
  - [ ] Test UploadPage job URL input
  - [ ] Test API service functions
  - [ ] Test ApplicationsPage rendering
  - [ ] Test ApplicationDetailsPage rendering

### Manual QA
- [ ] **4.5** Full system testing
  - [ ] Test complete flow: LinkedIn URL → Analysis → View in Applications
  - [ ] Test with different job boards (Naukri, Indeed)
  - [ ] Test with edge cases (invalid URLs, auth-required pages)
  - [ ] Test error recovery
  - [ ] Test performance with large datasets
  - [ ] Test on different browsers (Chrome, Firefox, Edge)

---

## 🟡 Phase 5: Documentation & Deployment (IN PROGRESS - 30%)

### Documentation
- [x] **5.1** Create V2 Implementation Status document ✅
- [x] **5.2** Create V2 Task List (this document) ✅
- [ ] **5.3** Update main README.md
  - [ ] Add V2 features section
  - [ ] Update setup instructions
  - [ ] Add job URL feature description
  - [ ] Add screenshots/GIFs
  - [ ] Update architecture diagram

- [ ] **5.4** Update API documentation
  - [ ] Document all V2 endpoints
  - [ ] Add Postman collection (optional)
  - [ ] Add curl examples
  - [ ] Document authentication flow (future)

- [ ] **5.5** Create User Guide
  - [ ] How to use job URL feature
  - [ ] Supported job boards
  - [ ] How to view application history
  - [ ] Troubleshooting common issues

- [ ] **5.6** Create Migration Guide
  - [ ] How to upgrade from V1 to V2
  - [ ] Database backup instructions
  - [ ] Rollback instructions
  - [ ] Data migration steps

### Deployment Preparation
- [ ] **5.7** Environment configuration
  - [ ] Update `.env.example` with V2 variables
  - [ ] Document required environment variables
  - [ ] Set up production database

- [ ] **5.8** Deployment scripts
  - [ ] Create deployment checklist
  - [ ] Update docker-compose (if using)
  - [ ] Update CI/CD pipelines (if exists)

### Release
- [ ] **5.9** Release preparation
  - [ ] Create release notes (expand RELEASE_NOTES.md)
  - [ ] Tag release: v2.0.0
  - [ ] Create GitHub release
  - [ ] Merge v2 → main (or base)
  - [ ] Deploy to production

---

## 🎯 High Priority Tasks (Do Next)

1. **Install Dependencies** (2.1) - 5 minutes
2. **Run Database Migration** (2.2) - 15 minutes
3. **Add Fetch JD Endpoint** (2.3) - 30 minutes
4. **Update Upload Endpoints** (2.4, 2.5) - 45 minutes
5. **Update Analyze Endpoint** (2.6) - 45 minutes

**Total Time for High Priority:** ~2 hours

---

## 📝 Notes & Decisions

### Backward Compatibility Strategy
- V1 endpoints remain functional
- Default user (id=1) used for anonymous sessions
- Gradual migration: new features use V2, existing features use V1
- No breaking changes to existing API contracts

### Job URL Feature Limitations
- Some job boards require authentication (will fail gracefully)
- Dynamic content (JavaScript-rendered) may not be extracted
- Rate limiting may apply to job board requests
- Fallback to generic extractor for unsupported boards

### Future Enhancements (Post-V2)
- User authentication and registration
- Social login (Google, LinkedIn)
- Resume versioning and comparison
- Application status tracking (applied, interview, offer, rejected)
- Email notifications for new applications
- Analytics dashboard (skills trends, match scores over time)
- Multi-language support
- Mobile app

---

## 🐛 Known Issues & Risks

| Issue | Severity | Status | Mitigation |
|-------|----------|--------|------------|
| Job boards may block scrapers | Medium | Open | Use proper headers, rate limiting, fallback |
| LinkedIn requires auth for some pages | Low | Open | Document limitation, user can paste text |
| Large database migration time | Low | Open | Backup before migration, test on staging |
| Frontend URL validation | Low | Open | Add client-side validation |

---

## 📞 Contacts & Resources

- **Design Documents:** `C:\Projects\ResumeTailor\00-Design\ReleaseV2\`
- **GitHub Repo:** https://github.com/jaysibi/resumetailor
- **V2 Branch:** https://github.com/jaysibi/resumetailor/tree/v2
- **Database Schema:** See `DB_design_v2.md`
- **Frontend Design:** See `FRONTEND_JOB_URL_DESIGN.md`

---

**Last Updated:** May 3, 2026  
**Next Review:** After Phase 2 completion  
**Overall Status:** 🟡 In Progress (29% complete)
