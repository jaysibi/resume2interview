# Resume2Interview Deployment Reference Guide

**Complete deployment documentation for staging and production environments**

Last Updated: May 11, 2026  
Repository: https://github.com/jaysibi/resume2interview

---

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [Prerequisites](#prerequisites)
- [Staging Deployment (Completed)](#staging-deployment-completed)
- [Production Deployment Guide](#production-deployment-guide)
- [Environment Variables](#environment-variables)
- [Database Setup](#database-setup)
- [Troubleshooting](#troubleshooting)
- [Verification & Testing](#verification--testing)
- [Rollback Procedures](#rollback-procedures)

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    GitHub Repository                         │
│         https://github.com/jaysibi/resume2interview         │
│                  Branches: main, ui-ux-redesign             │
└────────────────┬────────────────────────────────────────────┘
                 │
          ┌──────┴───────┐
          │              │
┌─────────▼────────┐  ┌──▼──────────────────┐
│   STAGING        │  │   PRODUCTION         │
├──────────────────┤  ├─────────────────────┤
│ Frontend         │  │ Frontend             │
│ Vercel           │  │ Vercel               │
│ ├─ Repo: main    │  │ ├─ Repo: main        │
│ ├─ Node.js       │  │ ├─ Node.js           │
│ └─ React + Vite  │  │ └─ React + Vite      │
│                  │  │                      │
│ Backend          │  │ Backend              │
│ Railway          │  │ Railway              │
│ ├─ Repo: main    │  │ ├─ Repo: main        │
│ ├─ Python 3.12   │  │ ├─ Python 3.12       │
│ └─ FastAPI       │  │ └─ FastAPI           │
│                  │  │                      │
│ Database         │  │ Database             │
│ Railway.app      │  │ Railway.app          │
│ └─ PostgreSQL    │  │ └─ PostgreSQL        │
└──────────────────┘  └─────────────────────┘
```

---

## Prerequisites

### Required Accounts
- [x] GitHub account with repository access
- [x] Vercel account (authenticated as: sibijayendra-5216)
- [x] Railway account
- [x] OpenAI Platform account with API key

### Local Development Tools
- [x] Git (for repository management)
- [x] Vercel CLI v50.44.0 or later
- [x] PowerShell (Windows) or Bash (Linux/macOS)
- [x] Python 3.12+ (for local testing)
- [x] Node.js 18+ (for local frontend development)

### Repository Setup
```bash
# Clone repository
git clone https://github.com/jaysibi/resume2interview.git
cd resume2interview

# Verify branches
git branch -a
# Should show: main, ui-ux-redesign
```

---

## Staging Deployment (Completed)

### Overview
- **Frontend URL:** https://resume2interview-staging.vercel.app
- **Backend URL:** https://graceful-exploration-staging.up.railway.app
- **Database:** Railway PostgreSQL (maglev.proxy.rlwy.net:22595)
- **Deployment Date:** May 11, 2026
- **Status:** ✅ Live and operational

### Deployment Timeline

#### 1. Repository Configuration (Completed)

**Issue Resolved:** Repository pointer was incorrect (resumetailor vs resume2interview)

```powershell
# Updated remote URL
cd C:\Projects\ResumeTailor
git remote set-url origin https://github.com/jaysibi/resume2interview.git

# Verified remote
git remote -v
# Output:
# origin  https://github.com/jaysibi/resume2interview.git (fetch)
# origin  https://github.com/jaysibi/resume2interview.git (push)
```

#### 2. Branch Setup (Completed)

Created `main` branch from `ui-ux-redesign` for Railway/Vercel deployment:

```powershell
cd C:\Projects\ResumeTailor
git checkout -b main
git push -u origin main
```

**Branches:**
- `main` → Staging/Production deployments
- `ui-ux-redesign` → Active development
- `base` → Initial base code
- `v2` → Version 2 features

#### 3. Security Fix: Remove API Key from Git History (Completed)

**Issue:** GitHub detected OpenAI API key in commit history

```powershell
# Removed .env from tracking
git rm --cached 01-Code/backend/.env -f

# Committed removal
git commit -m "chore: Remove .env file from git tracking (contains secrets)"

# Note: .gitignore already had .env listed
```

**Action Taken:** Allowed secret push via GitHub security page, then regenerated API key.

**Security Best Practice:** API keys should NEVER be in git history. Always use:
- Environment variables on deployment platforms
- Local `.env` files (gitignored)
- Secret management services for production

#### 4. Python Version Pin (Critical Fix)

**Issue:** Railway auto-selected Python 3.13, but PyMuPDF 1.23.21 has no pre-built wheel for 3.13

**Solution:** Created `.python-version` file

```bash
# File: 01-Code/backend/.python-version
3.12
```

```powershell
# Committed and pushed
git add 01-Code/backend/.python-version
git commit -m "fix: Pin Python to 3.12 for Railway deployment (PyMuPDF compatibility)"
git push origin main
```

**Result:** Railway build succeeded with Python 3.12

#### 5. Frontend Deployment to Vercel (Completed)

**Fixed TypeScript Build Errors:**

Before deployment, resolved 5 TypeScript errors:

1. **FAQ.tsx:** Removed unused `Link` import
2. **LandingPage.tsx:** Changed `resumeFile` to anonymous parameter
3. **api.ts:** Already fixed (no changes needed)
4. **e2e test file:** Moved out of src folder

```powershell
# Built locally to verify
cd 01-Code/frontend
npm run build
# ✓ built in 3.31s (327.71 kB gzip: 91.11 kB)

# Deployed to Vercel staging
vercel --build-env VITE_API_URL="https://placeholder-backend.up.railway.app" --build-env VITE_ENV="staging" --yes

# Deployed to production alias
vercel --prod --build-env VITE_API_URL="https://placeholder-backend.up.railway.app" --build-env VITE_ENV="staging" --yes
```

**Initial URLs:**
- Preview: https://resume2interview-staging-5i1x0yvhp-sibijayendra-5216s-projects.vercel.app
- Production: https://resume2interview-staging.vercel.app

**Committed Changes:**
```powershell
git add -A
git commit -m "fix: Resolve TypeScript build errors for deployment"
git push origin ui-ux-redesign
```

#### 6. Railway Backend Deployment (Completed)

**Configuration:**

1. **New Project Created:** Resume2Interview Staging
2. **Repository Connected:** jaysibi/resume2interview
3. **Branch:** main
4. **Root Directory:** `01-Code/backend`
5. **Build Configuration:**
   - Detected by Nixpacks (Python)
   - Uses `requirements.txt`
   - Uses `.python-version` (3.12)
   - Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

**Files for Railway:**

```python
# File: 01-Code/backend/Procfile
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

```json
# File: 01-Code/backend/railway.json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "uvicorn main:app --host 0.0.0.0 --port $PORT",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

```
# File: 01-Code/backend/runtime.txt
python-3.13
```

```
# File: 01-Code/backend/.python-version
3.12
```

**Note:** Railway uses `.python-version` over `runtime.txt` when both exist.

#### 7. PostgreSQL Database Setup (Completed)

**Added via Railway:**

1. In Railway project dashboard → **"+ New"** → **"Database"** → **"Add PostgreSQL"**
2. Railway automatically provisioned database
3. Railway automatically set `DATABASE_URL` environment variable

**Connection Details:**
- Internal URL: `postgresql://postgres:slpQeQAthrcWAKFhDyzgzrhHTkqYqITQ@postgres.railway.internal:5432/railway`
- Public URL: `postgresql://postgres:slpQeQAthrcWAKFhDyzgzrhHTkqYqITQ@maglev.proxy.rlwy.net:22595/railway`

**Database Migrations:**

```powershell
# Set DATABASE_URL
$env:DATABASE_URL = "postgresql://postgres:slpQeQAthrcWAKFhDyzgzrhHTkqYqITQ@maglev.proxy.rlwy.net:22595/railway"

# Run migrations
cd 01-Code/backend
python -m alembic upgrade head

# Verify migration
python -m alembic current
# Output: v2_004 (head)
```

**Tables Created:**
- users
- resumes
- user_resumes
- analysis_history
- job_matches
- alembic_version (migration tracking)

#### 8. Environment Variables Configuration (Completed)

**Railway Backend Service Variables:**

```bash
OPENAI_API_KEY=sk-proj-[REGENERATED-KEY]
CORS_ORIGINS=https://resume2interview-staging.vercel.app
ENVIRONMENT=staging
DATABASE_URL=[AUTO-SET BY RAILWAY]
PORT=[AUTO-SET BY RAILWAY]
```

**Vercel Frontend Variables:**

```bash
VITE_API_URL=https://graceful-exploration-staging.up.railway.app
VITE_ENV=staging
```

**How to Update Vercel Environment Variables:**

```powershell
cd 01-Code/frontend

# Remove old variable (if exists)
vercel env rm VITE_API_URL production --yes

# Add new variable
echo "https://graceful-exploration-staging.up.railway.app" | vercel env add VITE_API_URL production

# Redeploy to apply changes
vercel --prod --yes
```

#### 9. Backend URL Update in Frontend (Completed)

After Railway backend was live, updated Vercel:

```powershell
# Updated VITE_API_URL to real backend
vercel env add VITE_API_URL production
# Entered: https://graceful-exploration-staging.up.railway.app

# Redeployed frontend
vercel --prod --yes
```

**Final Deployment URLs:**
- Production: https://resume2interview-staging-gsdw3rmaf-sibijayendra-5216s-projects.vercel.app
- Alias: https://resume2interview-staging.vercel.app

#### 10. Verification (Completed)

```powershell
# Test Backend Health
Invoke-WebRequest -Uri "https://graceful-exploration-staging.up.railway.app/" -Method Get -UseBasicParsing
# StatusCode: 200
# Content: {"message":"Resume2Interview API is running."}

# Test Frontend
Invoke-WebRequest -Uri "https://resume2interview-staging.vercel.app/" -Method Get -UseBasicParsing
# StatusCode: 200

# Test Database Connection (from Railway logs)
# ✓ Database connection successful
# ✓ All migrations applied
```

---

## Production Deployment Guide

### Prerequisites Checklist

- [ ] All staging tests passed
- [ ] OpenAI API key regenerated for production
- [ ] Custom domain DNS configured: www.resume2interview.com → Vercel
- [ ] Custom domain DNS configured: api.resume2interview.com → Railway
- [ ] Production environment variables prepared
- [ ] Database backup strategy defined
- [ ] Monitoring tools configured (optional: DataDog, Sentry)

### Step-by-Step Production Deployment

#### Step 1: Create Production Railway Service

```bash
# In Railway Dashboard:
1. Create New Project: "Resume2Interview Production"
2. Deploy from GitHub Repo: jaysibi/resume2interview
3. Branch: main
4. Root Directory: 01-Code/backend
5. Generate Domain (or use custom domain)
```

#### Step 2: Add Production PostgreSQL Database

```bash
# In Railway Project:
1. Click "+ New" → "Database" → "Add PostgreSQL"
2. Wait for provisioning
3. Note the DATABASE_URL (auto-set)
```

#### Step 3: Configure Production Environment Variables (Railway)

```bash
OPENAI_API_KEY=sk-proj-[PRODUCTION-KEY]
CORS_ORIGINS=https://www.resume2interview.com
ENVIRONMENT=production
DATABASE_URL=[AUTO-SET]
PORT=[AUTO-SET]
```

#### Step 4: Run Database Migrations (Production)

```powershell
# Connect to production database
$env:DATABASE_URL = "postgresql://[PRODUCTION-DATABASE-URL]"

# Run migrations
cd 01-Code/backend
python -m alembic upgrade head

# Verify
python -m alembic current
# Should show: v2_004 (head)
```

#### Step 5: Deploy Frontend to Vercel Production

```powershell
cd 01-Code/frontend

# Create production project (if not exists)
vercel --prod

# Add environment variables
vercel env add VITE_API_URL production
# Enter: https://api.resume2interview.com (or Railway production URL)

vercel env add VITE_ENV production

# Deploy
vercel --prod --yes
```

#### Step 6: Configure Custom Domains

**For Frontend (Vercel):**

1. Go to Vercel Project → Settings → Domains
2. Add domain: `www.resume2interview.com`
3. Add DNS records (provided by Vercel):
   ```
   Type: CNAME
   Name: www
   Value: cname.vercel-dns.com
   ```
4. Verify domain

**For Backend (Railway):**

1. Go to Railway Service → Settings → Networking
2. Click "Add Custom Domain"
3. Enter: `api.resume2interview.com`
4. Add DNS records:
   ```
   Type: CNAME
   Name: api
   Value: [provided by Railway]
   ```
5. Verify domain

#### Step 7: Update CORS in Railway

After frontend domain is live, update CORS:

```bash
# In Railway Variables:
CORS_ORIGINS=https://www.resume2interview.com
```

Railway will automatically redeploy.

#### Step 8: Production Verification

```powershell
# Test Backend
Invoke-WebRequest -Uri "https://api.resume2interview.com/" -Method Get
# Expected: 200 OK

# Test Frontend
Invoke-WebRequest -Uri "https://www.resume2interview.com/" -Method Get
# Expected: 200 OK

# Test End-to-End
# 1. Visit https://www.resume2interview.com
# 2. Upload a resume
# 3. Verify analysis works
# 4. Check database for new records
```

---

## Environment Variables

### Staging Environment

| Variable | Value | Location | Notes |
|----------|-------|----------|-------|
| `VITE_API_URL` | https://graceful-exploration-staging.up.railway.app | Vercel | Frontend API endpoint |
| `VITE_ENV` | staging | Vercel | Environment identifier |
| `OPENAI_API_KEY` | sk-proj-[STAGING-KEY] | Railway | OpenAI API access |
| `CORS_ORIGINS` | https://resume2interview-staging.vercel.app | Railway | Allowed frontend origin |
| `ENVIRONMENT` | staging | Railway | Backend environment |
| `DATABASE_URL` | postgresql://[AUTO] | Railway | Auto-set by Railway |
| `PORT` | [AUTO] | Railway | Auto-set by Railway |

### Production Environment (Template)

| Variable | Value | Location | Notes |
|----------|-------|----------|-------|
| `VITE_API_URL` | https://api.resume2interview.com | Vercel | Frontend API endpoint |
| `VITE_ENV` | production | Vercel | Environment identifier |
| `OPENAI_API_KEY` | sk-proj-[PRODUCTION-KEY] | Railway | **REGENERATE FOR PRODUCTION** |
| `CORS_ORIGINS` | https://www.resume2interview.com | Railway | Allowed frontend origin |
| `ENVIRONMENT` | production | Railway | Backend environment |
| `DATABASE_URL` | postgresql://[AUTO] | Railway | Auto-set by Railway |
| `PORT` | [AUTO] | Railway | Auto-set by Railway |

### Environment Variable Management

**Vercel CLI Commands:**

```powershell
# List all environment variables
vercel env ls

# Add environment variable
vercel env add VARIABLE_NAME production

# Remove environment variable
vercel env rm VARIABLE_NAME production --yes

# Pull environment variables to local .env
vercel env pull
```

**Railway:**
- Manage via Railway Dashboard → Service → Variables tab
- Changes trigger automatic redeployment
- Use Railway CLI for automation (optional)

---

## Database Setup

### Schema Management (Alembic)

**Migration Files Location:** `01-Code/backend/alembic/versions/`

**Current Migration:** `v2_004` (head)

**Common Alembic Commands:**

```powershell
cd 01-Code/backend

# Set database URL
$env:DATABASE_URL = "postgresql://[YOUR-DATABASE-URL]"

# Check current version
python -m alembic current

# Upgrade to latest
python -m alembic upgrade head

# Downgrade one version
python -m alembic downgrade -1

# View migration history
python -m alembic history

# Create new migration
python -m alembic revision --autogenerate -m "description"
```

### Database Backup (Production)

**Manual Backup:**

```powershell
# Using pg_dump (requires PostgreSQL client)
pg_dump "postgresql://[PRODUCTION-URL]" > backup_$(Get-Date -Format 'yyyy-MM-dd_HH-mm-ss').sql
```

**Railway Built-in Backups:**
- Railway Pro plan includes automatic backups
- Access via Railway Dashboard → Database → Backups

### Database Restore

```powershell
# Restore from backup
psql "postgresql://[PRODUCTION-URL]" < backup_2026-05-11_10-00-00.sql
```

---

## Troubleshooting

### Common Issues and Solutions

#### Issue 1: PyMuPDF Build Failure on Railway

**Symptoms:**
```
ERROR: Could not build wheels for PyMuPDF
C++ compilation errors during MuPDF wrapper generation
```

**Solution:**
Create `.python-version` file pinning to Python 3.12

```bash
# File: 01-Code/backend/.python-version
3.12
```

**Reason:** PyMuPDF 1.23.21 has no pre-built wheel for Python 3.13

---

#### Issue 2: CORS Errors on Frontend

**Symptoms:**
```
Access to fetch at 'https://backend.url' from origin 'https://frontend.url' 
has been blocked by CORS policy
```

**Solution:**
Update `CORS_ORIGINS` in Railway environment variables:

```bash
CORS_ORIGINS=https://resume2interview-staging.vercel.app
```

Ensure exact match (no trailing slash, correct protocol).

---

#### Issue 3: Database Connection Refused

**Symptoms:**
```
sqlalchemy.exc.OperationalError: could not connect to server
```

**Solution:**
1. Verify `DATABASE_URL` is set in Railway
2. Check database service is running in Railway
3. Use PUBLIC database URL for external connections
4. Use INTERNAL database URL only within Railway network

**Database URL Formats:**
- Internal: `postgresql://...@postgres.railway.internal:5432/railway`
- Public: `postgresql://...@maglev.proxy.rlwy.net:22595/railway`

---

#### Issue 4: Frontend Shows Placeholder Backend

**Symptoms:**
Frontend connects to `https://placeholder-backend.up.railway.app`

**Solution:**
Update Vercel environment variable and redeploy:

```powershell
cd 01-Code/frontend
vercel env rm VITE_API_URL production --yes
vercel env add VITE_API_URL production
# Enter real backend URL
vercel --prod --yes
```

---

#### Issue 5: Railway Build Gets Stuck

**Symptoms:**
Railway build hangs at "Installing dependencies"

**Solution:**
1. Check Railway build logs for specific error
2. Verify `requirements.txt` has no syntax errors
3. Try redeploying (sometimes transient network issues)
4. Check if private PyPI packages require authentication

---

#### Issue 6: Vercel Build TypeScript Errors

**Symptoms:**
```
TS6133: 'X' is declared but never read
TS2591: Cannot find name 'Y'
```

**Solution:**
Fix TypeScript errors locally first:

```powershell
cd 01-Code/frontend
npm run build
# Fix all errors shown
git commit -m "fix: TypeScript build errors"
git push
```

---

#### Issue 7: OpenAI API Key Invalid

**Symptoms:**
```
401 Unauthorized: Invalid API Key
```

**Solution:**
1. Verify API key in Railway Variables
2. Check key starts with `sk-proj-`
3. Regenerate key if compromised
4. Ensure no extra whitespace in environment variable

---

### Getting Deployment Logs

**Railway Logs:**

```bash
# Via Dashboard:
Railway Dashboard → Service → Deployments → Click deployment → View Logs

# Via CLI (optional):
railway logs
```

**Vercel Logs:**

```bash
# Via Dashboard:
Vercel Dashboard → Project → Deployments → Click deployment → View Logs

# Via CLI:
vercel logs [DEPLOYMENT_URL]
```

---

## Verification & Testing

### Backend Health Checks

```powershell
# Root endpoint
Invoke-WebRequest -Uri "https://graceful-exploration-staging.up.railway.app/" -Method Get
# Expected: {"message":"Resume2Interview API is running."}

# Database connection (check logs)
# Expected: No connection errors in Railway logs
```

### Frontend Verification

```powershell
# Homepage loads
Invoke-WebRequest -Uri "https://resume2interview-staging.vercel.app/" -Method Get
# Expected: Status 200

# Check browser console
# Expected: No CORS errors, API connection successful
```

### End-to-End Testing

**Manual Test Flow:**

1. Visit https://resume2interview-staging.vercel.app
2. Upload a sample resume PDF
3. Verify resume is parsed correctly
4. Check analysis results display
5. Verify data is saved in database

**Automated Testing (Future):**

```powershell
# Playwright E2E tests
cd 01-Code
npx playwright test
```

---

## Rollback Procedures

### Frontend Rollback (Vercel)

```powershell
# Via Dashboard:
1. Vercel Dashboard → Project → Deployments
2. Find previous working deployment
3. Click "..." → "Promote to Production"

# Via CLI:
vercel rollback [DEPLOYMENT_URL]
```

### Backend Rollback (Railway)

```bash
# Via Dashboard:
1. Railway Dashboard → Service → Deployments
2. Find previous working deployment
3. Click "Redeploy"

# Via Git:
git revert [COMMIT_HASH]
git push origin main
# Railway auto-redeploys
```

### Database Rollback

```powershell
# Downgrade migration
$env:DATABASE_URL = "postgresql://[DATABASE-URL]"
cd 01-Code/backend
python -m alembic downgrade -1

# Or restore from backup
psql "postgresql://[DATABASE-URL]" < backup_file.sql
```

---

## Post-Deployment Checklist

### Staging Environment

- [x] Frontend deployed to Vercel
- [x] Backend deployed to Railway
- [x] PostgreSQL database provisioned
- [x] Database migrations run successfully
- [x] Environment variables configured
- [x] CORS configured correctly
- [x] Backend health endpoint responding
- [x] Frontend loads and connects to backend
- [x] End-to-end functionality verified

### Production Environment (Template)

- [ ] Custom domains configured (www.resume2interview.com, api.resume2interview.com)
- [ ] SSL certificates verified
- [ ] Production OpenAI API key generated
- [ ] All environment variables set
- [ ] Database migrations run on production database
- [ ] CORS updated with production domain
- [ ] Load testing completed
- [ ] Error monitoring configured (Sentry/DataDog)
- [ ] Backup strategy implemented
- [ ] Documentation updated
- [ ] Team notified of deployment
- [ ] Smoke tests passed

---

## Cost Estimates

### Staging Environment (Current)

| Service | Plan | Cost |
|---------|------|------|
| Vercel | Hobby (Free) | $0/month |
| Railway | Free Tier | $0/month (500 hours) |
| OpenAI API | Pay-as-you-go | Variable (est. $5-20/month for testing) |
| **Total** | | **~$5-20/month** |

### Production Environment (Estimated)

| Service | Plan | Estimated Cost |
|---------|------|----------------|
| Vercel | Pro | $20/month |
| Railway | Pro | $20/month |
| OpenAI API | Pay-as-you-go | $50-200/month (depends on usage) |
| Custom Domain | (if not owned) | $12/year |
| **Total** | | **~$90-240/month** |

**Note:** OpenAI costs scale with usage. Monitor usage at https://platform.openai.com/usage

---

## Key Learnings & Best Practices

### Security

1. ✅ **Never commit API keys to Git**
   - Always use environment variables
   - Use `.gitignore` for `.env` files
   - Rotate keys if exposed

2. ✅ **Use HTTPS for all endpoints**
   - Vercel provides automatic SSL
   - Railway provides automatic SSL

3. ✅ **Limit CORS origins**
   - Only allow specific frontend domains
   - Never use wildcard (*) in production

### Deployment

1. ✅ **Pin Python version**
   - Use `.python-version` for consistency
   - Avoid auto-version selection issues

2. ✅ **Test locally before deploying**
   - Run `npm run build` before pushing
   - Fix TypeScript errors locally

3. ✅ **Use environment-specific configurations**
   - Separate staging and production variables
   - Use `ENVIRONMENT` variable to control behavior

### Database

1. ✅ **Always run migrations**
   - Don't rely on auto-migrations in production
   - Test migrations on staging first

2. ✅ **Backup before major changes**
   - Take manual backups before schema changes
   - Test restore procedures

3. ✅ **Use connection pooling**
   - FastAPI SQLAlchemy handles this
   - Monitor connection limits

---

## Support & Resources

### Documentation Links

- **Vercel Docs:** https://vercel.com/docs
- **Railway Docs:** https://docs.railway.app
- **FastAPI Docs:** https://fastapi.tiangolo.com
- **Alembic Docs:** https://alembic.sqlalchemy.org
- **React Docs:** https://react.dev

### Project Resources

- **GitHub Repository:** https://github.com/jaysibi/resume2interview
- **Staging Frontend:** https://resume2interview-staging.vercel.app
- **Staging Backend:** https://graceful-exploration-staging.up.railway.app

### Contact Information

- **Deployed By:** GitHub Copilot + sibijayendra-5216
- **Deployment Date:** May 11, 2026
- **Last Updated:** May 11, 2026

---

## Appendix

### File Structure

```
resume2interview/
├── 01-Code/
│   ├── backend/
│   │   ├── main.py                    # FastAPI application
│   │   ├── requirements.txt           # Python dependencies
│   │   ├── .python-version            # Python 3.12
│   │   ├── Procfile                   # Railway start command
│   │   ├── railway.json               # Railway configuration
│   │   ├── alembic/                   # Database migrations
│   │   │   └── versions/
│   │   │       └── v2_004_*.py       # Current migration
│   │   └── alembic.ini               # Alembic configuration
│   └── frontend/
│       ├── package.json               # Node.js dependencies
│       ├── vite.config.ts             # Vite configuration
│       ├── vercel.json                # Vercel configuration
│       └── src/
│           ├── pages/
│           │   ├── LandingPage.tsx
│           │   └── FAQ.tsx
│           └── services/
│               └── api.ts             # API client
├── DEPLOYMENT.md                      # Previous deployment guide
├── DEPLOYMENT_REFERENCE.md            # This file
├── QUICK_DEPLOY.md                    # Quick deployment steps
└── PRODUCTION_CHECKLIST.md            # Production deployment checklist
```

### Quick Command Reference

```powershell
# Frontend deployment
cd 01-Code/frontend
npm run build                          # Build locally
vercel --prod --yes                    # Deploy to production

# Backend deployment (automatic via Railway on git push)
git add .
git commit -m "Update backend"
git push origin main

# Database migrations
$env:DATABASE_URL = "postgresql://..."
python -m alembic upgrade head

# Environment variables
vercel env add VARIABLE_NAME production    # Add Vercel variable
vercel env ls                               # List Vercel variables

# Verification
Invoke-WebRequest -Uri "https://..." -Method Get   # Test endpoint
```

---

## Changelog

| Date | Version | Changes |
|------|---------|---------|
| May 11, 2026 | 1.0 | Initial staging deployment completed |
| May 11, 2026 | 1.1 | Added comprehensive deployment reference documentation |

---

**END OF DEPLOYMENT REFERENCE GUIDE**
