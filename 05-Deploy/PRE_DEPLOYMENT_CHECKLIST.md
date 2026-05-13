# Pre-Deployment Checklist - Resume2Interview

## 🎯 Purpose

This checklist ensures all prerequisites are met before deploying to production. Complete ALL items before proceeding with deployment.

---

## ✅ Code Readiness

### Repository Status
- [ ] All code committed to Git
- [ ] Working on `main` branch (or release branch)
- [ ] No uncommitted changes (`git status` clean)
- [ ] All merge conflicts resolved
- [ ] Code review completed and approved
- [ ] No linting errors (`npm run lint` in frontend)
- [ ] No TypeScript errors (`npm run build` successful)

### Version Control
- [ ] Release version tagged (e.g., `v1.0.0`)
- [ ] CHANGELOG.md updated with release notes
- [ ] Git tag pushed to remote (`git push origin v1.0.0`)

### Testing
- [ ] All unit tests pass locally
- [ ] Integration tests pass
- [ ] Manual testing completed in local environment
- [ ] No console errors in browser developer tools

---

## 🧪 Staging Validation

### Deployment Status
- [ ] Code deployed to staging environment
- [ ] Staging deployment successful (no build errors)
- [ ] Staging has been stable for 24-48 hours minimum

### Functional Testing in Staging
- [ ] **Upload Page**: Can upload resume (PDF/DOCX)
- [ ] **Analysis**: Gap analysis generates successfully
- [ ] **ATS Score**: ATS scoring completes
- [ ] **Results**: Results page displays correctly
- [ ] **Database**: Applications saved to database
- [ ] **Analytics**: Analytics dashboard loads (with password)
- [ ] **Excel Export**: Excel export downloads successfully
- [ ] **Error Handling**: 404 page displays for bad routes
- [ ] **Mobile**: Site is responsive on mobile devices

### Performance Testing in Staging
- [ ] Page load time < 3 seconds
- [ ] API response time < 2 seconds
- [ ] Resume analysis completes < 30 seconds
- [ ] No memory leaks (check browser performance tab)
- [ ] No excessive API calls (check network tab)

### Data Validation in Staging
- [ ] Check database for test application records
- [ ] Verify analytics shows correct data
- [ ] Confirm exported Excel has all columns
- [ ] Test with multiple resume formats (PDF, DOCX)
- [ ] Test with various job descriptions

### Security Testing in Staging
- [ ] Analytics password protection works
- [ ] No sensitive data in frontend bundle
- [ ] CORS configured correctly (no console CORS errors)
- [ ] Rate limiting functional (test excessive requests)

---

## 🔧 Environment Configuration

### Railway Production Backend

#### Service Setup
- [ ] Production Railway service created
- [ ] Service name: `graceful-exploration-production` (or similar)
- [ ] Service separated from staging
- [ ] Git repository connected
- [ ] **Auto-deploy DISABLED** (manual deploy only)

#### Database Setup
- [ ] Production PostgreSQL database created in Railway
- [ ] Database is **separate instance** from staging
- [ ] Database backups enabled (automatic Railway feature)
- [ ] Database credentials stored securely

#### Environment Variables Set
- [ ] `DATABASE_URL` (auto-injected by Railway PostgreSQL)
- [ ] `OPENAI_API_KEY` (production key, NOT staging key)
- [ ] `ANALYTICS_PASSWORD` (strong password, NOT `Railwayismessy`)
- [ ] `CORS_ORIGINS` (production frontend URL only: `https://resume2interview.com`)
- [ ] `PORT` (set to 8080 or auto-detect)
- [ ] `ENVIRONMENT` (set to `production`)

#### Build Configuration
- [ ] Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- [ ] Root Directory: Auto-detected (`01-Code/backend`)
- [ ] Python version: 3.11 or 3.12
- [ ] Dependencies: All listed in `requirements.txt`

#### Verify No Debug Endpoints (Optional but Recommended)
- [ ] Consider removing `/debug/db-config` endpoint
- [ ] Consider removing `/debug/env-check` endpoint
- [ ] Consider removing `/debug/password-check` endpoint
- [ ] OR ensure they require production password

### Vercel Production Frontend

#### Project Setup
- [ ] Production Vercel project created
- [ ] Project name: `resume2interview-production` (or similar)
- [ ] Git repository connected: `jaysibi/resume2interview`
- [ ] **Auto-deploy DISABLED** (manual deploy only)
- [ ] Production branch: `main` (or release tag)

#### Domain Configuration
- [ ] Custom domain added: `resume2interview.com`
- [ ] Domain verified in Vercel
- [ ] SSL certificate auto-provisioned by Vercel
- [ ] DNS configured in GoDaddy (see DNS section below)

#### Build Configuration
- [ ] Root Directory: `01-Code/frontend`
- [ ] Framework Preset: `Vite`
- [ ] Build Command: `npm run build`
- [ ] Output Directory: `dist`
- [ ] Node Version: 18.x or 20.x

#### Environment Variables Set
- [ ] **None required** for frontend (API URL hardcoded)
- [ ] Verify `Analytics.tsx` uses production backend URL
  ```typescript
  const backendUrl = 'https://[production-railway-url].up.railway.app';
  ```

### GoDaddy DNS Configuration

#### DNS Records Required
- [ ] **A Record**: 
  - Name: `@` (root domain)
  - Value: Vercel IP (check Vercel dashboard)
  - TTL: 600 seconds
- [ ] **CNAME Record**:
  - Name: `www`
  - Value: `cname.vercel-dns.com`
  - TTL: 600 seconds

#### DNS Verification
- [ ] DNS propagation complete (use `nslookup resume2interview.com`)
- [ ] Root domain (`resume2interview.com`) resolves to Vercel
- [ ] WWW subdomain (`www.resume2interview.com`) redirects to root

---

## 📦 Dependencies & Prerequisites

### Required Access
- [ ] GitHub repository write access
- [ ] Vercel production project admin access
- [ ] Railway production service admin access
- [ ] GoDaddy domain DNS management access
- [ ] OpenAI API account with production key

### API Keys & Credentials
- [ ] OpenAI API key (production) validated and working
- [ ] OpenAI API key has sufficient credits/quota
- [ ] Analytics password generated (16+ characters, complex)
- [ ] Database credentials available (auto-provided by Railway)

### Tools Installed Locally
- [ ] Git CLI
- [ ] Node.js (v18+ or v20+)
- [ ] npm or yarn
- [ ] Vercel CLI (`npm install -g vercel`)
- [ ] Railway CLI (optional: `npm install -g @railway/cli`)

---

## 🗄️ Database Preparation

### Database Migration
- [ ] Alembic migrations created for all schema changes
- [ ] Migrations tested in staging environment
- [ ] Migration rollback plan documented
- [ ] Database backup created before migration

### Database Verification
- [ ] Can connect to production database (via Railway dashboard)
- [ ] Database has correct schema (8 tables expected)
- [ ] Alembic version table exists
- [ ] No data in production database (fresh start) OR data migrated correctly

### Expected Tables
- [ ] `users`
- [ ] `resumes`
- [ ] `job_descriptions`
- [ ] `applications`
- [ ] `gap_analyses`
- [ ] `ats_scores`
- [ ] `usage_logs`
- [ ] `alembic_version`

---

## 📋 Code Changes Required

### Frontend Changes for Production

#### Update Backend URL in Analytics.tsx
```typescript
// File: 01-Code/frontend/src/pages/Analytics.tsx
// Line: ~118

// BEFORE (staging):
const backendUrl = 'https://graceful-exploration-staging.up.railway.app';

// AFTER (production):
const backendUrl = 'https://[production-railway-url].up.railway.app';
```

#### Verify Application Tracking Enabled
```typescript
// File: 01-Code/frontend/src/pages/ResultsPage.tsx
// Line: ~28

// Ensure this line passes 'true' for createApplication:
api.getGapAnalysis(resumeId, jdId, undefined, true)
```

### Backend Changes for Production

#### Update CORS Origins
```python
# File: 01-Code/backend/main.py
# Environment variable CORS_ORIGINS should be:
# Production only: https://resume2interview.com
```

#### Strengthen Analytics Password
```python
# Environment variable ANALYTICS_PASSWORD:
# NOT "Railwayismessy" (staging password)
# Use strong password like: "Prod2024!SecureAnalytics#789"
```

#### Rate Limiting Configuration (Optional)
```python
# Consider stricter rate limits for production
# Current: 100 requests/day per IP
# Production: Consider 50 requests/day or implement user-based limits
```

---

## 🔐 Security Checklist

### Credentials
- [ ] Production OpenAI API key is NOT the same as staging
- [ ] Analytics password is NOT the same as staging
- [ ] Database is separate production instance
- [ ] No hardcoded credentials in code

### Frontend Security
- [ ] No console.log statements with sensitive data
- [ ] No debug flags enabled
- [ ] Source maps disabled in production build (optional)
- [ ] Analytics password NOT hardcoded in frontend

### Backend Security
- [ ] Debug endpoints removed or password-protected
- [ ] CORS restricted to production domain only
- [ ] Rate limiting enabled
- [ ] SQL injection prevention (using SQLAlchemy ORM - built-in)
- [ ] Input validation on all endpoints

### Infrastructure Security
- [ ] HTTPS enabled (automatic with Vercel)
- [ ] Database connections encrypted (Railway default)
- [ ] Environment variables not exposed in logs
- [ ] Railway service set to private (not public internet access except via Vercel)

---

## 📊 Monitoring Setup

### Vercel Analytics
- [ ] Vercel Analytics enabled for production project
- [ ] Core Web Vitals monitoring active
- [ ] Real-time analytics dashboard accessible

### Railway Monitoring
- [ ] Railway logging enabled
- [ ] Log retention configured
- [ ] Can view logs in Railway dashboard

### Application Analytics
- [ ] Analytics dashboard accessible at `/analytics` with password
- [ ] Usage stats tracking functional
- [ ] Application stats tracking functional
- [ ] Excel export functional

### Error Tracking (Optional but Recommended)
- [ ] Sentry or similar error tracking configured
- [ ] Frontend errors captured
- [ ] Backend errors captured
- [ ] Alert notifications configured

---

## 📞 Communication & Documentation

### Team Notification
- [ ] Deployment scheduled and communicated to team
- [ ] Deployment window: Tuesday-Thursday, 10 AM - 2 PM PST
- [ ] Stakeholders notified of potential downtime
- [ ] Support team prepared for increased user issues

### Documentation
- [ ] Deployment runbook reviewed
- [ ] Rollback procedure documented and ready
- [ ] Post-deployment validation checklist prepared
- [ ] Known issues documented

### Rollback Plan
- [ ] Last working deployment identified in Vercel
- [ ] Last working deployment identified in Railway
- [ ] Database rollback plan (do NOT rollback DB without review)
- [ ] Rollback trigger criteria defined

---

## 🎯 Final Pre-Flight Checks

### 5 Minutes Before Deployment
- [ ] No incidents in staging in last 24 hours
- [ ] No critical bugs reported
- [ ] Team members available for support
- [ ] Rollback plan reviewed and ready
- [ ] Post-deployment validation checklist printed/opened

### Deployment Day Weather Check
- [ ] Not Friday (avoid weekend issues)
- [ ] Not before holiday or long weekend
- [ ] Time zone: Deployment during business hours PST
- [ ] Team available for 2 hours post-deployment monitoring

---

## ✋ Go/No-Go Decision

**If ANY critical items are unchecked, DO NOT DEPLOY.**

### Critical Blockers (Must be YES)
- [ ] All staging tests pass
- [ ] No critical bugs in staging
- [ ] Production environment variables set
- [ ] Database backups enabled
- [ ] Rollback plan ready
- [ ] Team available for support

### Proceed to Deployment?
- [ ] **YES** - All critical items checked, proceed with `PRODUCTION_DEPLOYMENT.md`
- [ ] **NO** - Address issues, reschedule deployment

---

## 📝 Sign-Off

**Reviewed by**: ________________  
**Date**: ________________  
**Approved for deployment**: [ ] YES / [ ] NO  
**Deployment scheduled for**: ________________  

---

## 🔄 Post-Review Actions

If deployment is **NOT APPROVED**:
1. Document reasons for delay
2. Create action items to address blockers
3. Reschedule deployment after issues resolved
4. Re-run this checklist before new deployment date

If deployment is **APPROVED**:
1. Proceed to `PRODUCTION_DEPLOYMENT.md`
2. Keep this checklist for audit trail
3. Mark deployment time in calendar
