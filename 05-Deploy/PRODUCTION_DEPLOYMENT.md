# Production Deployment Guide - Resume2Interview

**⚠️ CRITICAL**: Complete [PRE_DEPLOYMENT_CHECKLIST.md](PRE_DEPLOYMENT_CHECKLIST.md) before proceeding.

---

## 🎯 Deployment Overview

**Production URL**: https://resume2interview.com  
**Estimated Duration**: 45-60 minutes  
**Team Required**: 1 engineer + 1 backup for support  
**Best Time**: Tuesday-Thursday, 10 AM - 2 PM PST  

---

## 📋 Deployment Steps

### Phase 1: Pre-Deployment Preparation (10 minutes)

#### Step 1.1: Verify Staging Environment
```powershell
# Check staging deployment status
$stagingFrontend = Invoke-WebRequest -Uri "https://resume2interview-staging.vercel.app" -UseBasicParsing
if ($stagingFrontend.StatusCode -eq 200) {
    Write-Host "✅ Staging frontend is up"
} else {
    Write-Host "❌ Staging frontend is down - STOP"
    exit 1
}

# Check staging backend
$stagingBackend = Invoke-WebRequest -Uri "https://graceful-exploration-staging.up.railway.app/docs" -UseBasicParsing
if ($stagingBackend.StatusCode -eq 200) {
    Write-Host "✅ Staging backend is up"
} else {
    Write-Host "❌ Staging backend is down - STOP"
    exit 1
}
```

#### Step 1.2: Take Pre-Deployment Snapshot
```powershell
# Document current production state (if exists)
cd C:\Projects\ResumeTailor
git log -1 --oneline > 05-Deploy\pre-deployment-snapshot.txt
date >> 05-Deploy\pre-deployment-snapshot.txt

Write-Host "✅ Pre-deployment snapshot saved"
```

#### Step 1.3: Have Rollback Plan Ready
- [ ] Open Vercel dashboard in separate tab
- [ ] Open Railway dashboard in separate tab
- [ ] Have `ROLLBACK_PROCEDURE.md` open
- [ ] Team on standby

---

### Phase 2: Backend Deployment (Railway) (15-20 minutes)

#### Step 2.1: Create/Verify Production Service in Railway

**Option A: If production service doesn't exist yet**

1. Go to https://railway.app
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose `jaysibi/resume2interview`
5. Service name: `graceful-exploration-production`
6. Click "Add variables" → "New Variable"

**Option B: If production service already exists**

1. Go to https://railway.app
2. Select existing production service
3. Verify it's pointing to correct GitHub repo

#### Step 2.2: Add Production PostgreSQL Database

1. In Railway project, click "New" → "Database" → "PostgreSQL"
2. Database will be auto-provisioned
3. `DATABASE_URL` environment variable automatically added
4. Wait for database to be ready (green status)

```powershell
# Verify database is accessible
# (Do this from Railway dashboard → Database → Connect)
# Connection string will be like:
# postgresql://postgres:***@containers-us-west-XXX.railway.app:XXXX/railway
```

#### Step 2.3: Set Production Environment Variables

In Railway dashboard → Service Settings → Variables:

```bash
# Required Variables
OPENAI_API_KEY=sk-proj-[PRODUCTION_KEY_HERE]  # NOT staging key
ANALYTICS_PASSWORD=[STRONG_PASSWORD_HERE]      # NOT Railwayismessy
CORS_ORIGINS=https://resume2interview.com      # Production domain only
ENVIRONMENT=production
PORT=8080

# Auto-injected by Railway (verify it exists)
DATABASE_URL=postgresql://postgres:***@[railway-host]/railway
```

✅ **Verification**:
- [ ] All 5 environment variables set
- [ ] OpenAI key is production key (not staging)
- [ ] Analytics password is strong (16+ chars)
- [ ] CORS only includes production domain
- [ ] DATABASE_URL auto-populated

#### Step 2.4: Configure Build Settings

In Railway dashboard → Service Settings:

- **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- **Root Directory**: (Let Railway auto-detect → should be `01-Code/backend`)
- **Builder**: nixpacks (default)

#### Step 2.5: Disable Auto-Deploy (CRITICAL)

In Railway dashboard → Service Settings → Deployment:

- [ ] **Uncheck "Enable automatic deployments"**
- [ ] Verify auto-deploy is OFF (prevents accidental deployments)

#### Step 2.6: Deploy Backend Manually

**Option A: Deploy from Railway Dashboard**
1. Railway dashboard → Deployments tab
2. Click "Deploy from latest commit"
3. Select commit/tag to deploy (e.g., `v1.0.0`)
4. Click "Deploy"

**Option B: Deploy from Railway CLI**
```powershell
cd C:\Projects\ResumeTailor\01-Code\backend
railway up --service graceful-exploration-production
```

#### Step 2.7: Monitor Backend Deployment

```powershell
# Watch deployment logs in Railway dashboard
# Wait for "Application startup complete" message
# Typical deployment time: 3-5 minutes
```

✅ **Success indicators**:
- Deploy status: "Success" (green)
- Logs show: "Application startup complete"
- Service status: "Running"
- No errors in recent logs

#### Step 2.8: Verify Backend Health

```powershell
# Get production Railway URL from dashboard
$productionBackendUrl = "https://[production-railway-url].up.railway.app"

# Check API documentation
Invoke-WebRequest -Uri "$productionBackendUrl/docs" -UseBasicParsing

# Expected: HTTP 200, OpenAPI docs page
```

#### Step 2.9: Run Database Migrations

```powershell
# Connect to Railway backend via terminal (if needed)
railway run -s graceful-exploration-production alembic upgrade head

# OR run from Railway dashboard Shell:
# alembic upgrade head
```

✅ **Verify migration success**:
```powershell
# Check database has 8 tables
# Should see: users, resumes, job_descriptions, applications, gap_analyses, ats_scores, usage_logs, alembic_version
```

#### Step 2.10: Test Backend Endpoints

```powershell
$backendUrl = "https://[production-railway-url].up.railway.app"
$analyticsPassword = "[YOUR_PRODUCTION_PASSWORD]"

# Test analytics endpoint (password-protected)
$headers = @{ 'X-Analytics-Password' = $analyticsPassword }
$response = Invoke-RestMethod -Uri "$backendUrl/api/analytics/usage-stats" -Headers $headers

if ($response.success) {
    Write-Host "✅ Backend analytics endpoint working"
} else {
    Write-Host "❌ Backend test failed - STOP"
    exit 1
}
```

---

### Phase 3: Frontend Deployment (Vercel) (15-20 minutes)

#### Step 3.1: Update Frontend Code for Production

**CRITICAL**: Update backend URL in frontend code

```powershell
# Open file for editing
code C:\Projects\ResumeTailor\01-Code\frontend\src\pages\Analytics.tsx
```

Update line ~118:
```typescript
// CHANGE THIS:
const backendUrl = 'https://graceful-exploration-staging.up.railway.app';

// TO THIS (use actual production Railway URL):
const backendUrl = 'https://[production-railway-url].up.railway.app';
```

Commit the change:
```powershell
cd C:\Projects\ResumeTailor
git add 01-Code/frontend/src/pages/Analytics.tsx
git commit -m "Production: Update backend URL to production Railway service"
git push origin main
```

#### Step 3.2: Create/Verify Production Vercel Project

**Option A: If production project doesn't exist**

1. Go to https://vercel.com
2. Click "Add New..." → "Project"
3. Import `jaysibi/resume2interview` repository
4. Project name: `resume2interview-production`
5. Root Directory: `01-Code/frontend`
6. Framework: `Vite` (auto-detected)
7. DO NOT deploy yet (configure settings first)

**Option B: If production project exists**

1. Go to https://vercel.com/[your-profile]/resume2interview-production
2. Verify Git connection is correct

#### Step 3.3: Configure Vercel Project Settings

Navigate to: Settings → General

**Build & Development Settings**:
- Root Directory: `01-Code/frontend`
- Framework Preset: `Vite`
- Build Command: `npm run build`
- Output Directory: `dist`
- Install Command: `npm install`

**Git Configuration**:
- Production Branch: `main`
- **Disable automatic deployments** (manual only)

#### Step 3.4: Add Custom Domain

Navigate to: Settings → Domains

1. Click "Add"
2. Enter: `resume2interview.com`
3. Click "Add"
4. Vercel will provide DNS configuration

**Note**: You'll configure GoDaddy DNS in step 3.6

#### Step 3.5: Deploy Frontend to Vercel

**Option A: Deploy from Vercel CLI (Recommended)**
```powershell
cd C:\Projects\ResumeTailor\01-Code\frontend

# Login to Vercel (if not already logged in)
vercel login

# Link to production project
vercel link
# Select: resume2interview-production

# Deploy to production
vercel --prod --yes
```

Expected output:
```
🔍  Inspect: https://vercel.com/[...]/[deployment-id]
✅  Production: https://resume2interview-production.vercel.app
🔗  Aliased: https://resume2interview.com
```

**Option B: Deploy from Vercel Dashboard**
1. Vercel dashboard → Deployments
2. Click "Deploy from latest commit"
3. Wait for build to complete

#### Step 3.6: Configure GoDaddy DNS

**CRITICAL**: Final step to point domain to Vercel

1. Go to https://godaddy.com → My Products → Domains
2. Click "DNS" next to `resume2interview.com`
3. **Delete** any existing A or CNAME records for `@` and `www`
4. Add new records:

**A Record** (for root domain):
```
Type: A
Name: @
Value: 76.76.21.21  (Vercel IP - verify in Vercel dashboard)
TTL: 600
```

**CNAME Record** (for www):
```
Type: CNAME
Name: www
Value: cname.vercel-dns.com
TTL: 600
```

5. Click "Save"
6. Wait 5-10 minutes for DNS propagation

#### Step 3.7: Verify DNS Propagation

```powershell
# Check DNS resolution
nslookup resume2interview.com

# Should return Vercel IP address (76.76.21.21)

# Check www subdomain
nslookup www.resume2interview.com

# Should return CNAME to vercel-dns.com
```

#### Step 3.8: Verify SSL Certificate

1. Vercel dashboard → Settings → Domains
2. Check `resume2interview.com` status
3. Should show: ✅ Valid Certificate

Wait ~5 minutes if showing "Pending" or "Provisioning"

#### Step 3.9: Test Production Frontend

```powershell
# Test root domain
$response = Invoke-WebRequest -Uri "https://resume2interview.com" -UseBasicParsing

if ($response.StatusCode -eq 200 -and $response.Content -match "Resume2Interview") {
    Write-Host "✅ Production frontend is live"
} else {
    Write-Host "❌ Frontend test failed"
}

# Check bundle version (should be new)
$response.Content -match 'src="(/assets/index-[^"]+\.js)"'
$bundleName = $Matches[1]
Write-Host "Production bundle: $bundleName"
```

---

### Phase 4: End-to-End Verification (10 minutes)

#### Step 4.1: Test Complete User Flow

1. **Open browser** (incognito/private mode)
2. **Navigate** to https://resume2interview.com
3. **Upload** a test resume (PDF or DOCX)
4. **Paste** a job description
5. **Click** "Analyze My Resume"
6. **Verify** results page loads with scores
7. **Check** application saved to database

#### Step 4.2: Verify Database Integration

```powershell
# Check production database via Railway dashboard
# Navigate to: Railway → Production Service → PostgreSQL → Data

# Should see new application record in 'applications' table
# Verify gap_analyses and ats_scores tables have records
```

#### Step 4.3: Test Analytics Dashboard

1. Navigate to https://resume2interview.com/analytics
2. Enter production analytics password
3. Verify data displays:
   - Usage stats
   - Application stats (should show 1 test application)
   - Excel export button visible

#### Step 4.4: Test Excel Export

1. On analytics dashboard, click "Export to Excel"
2. File should download: `applications_export_[timestamp].xlsx`
3. Open file and verify columns:
   - User Name
   - User Email
   - Resume Filename
   - Company
   - Job Title
   - Match Score (%)
   - ATS Score (%)
   - Applied Date
4. Verify test application data is present

#### Step 4.5: Test Error Handling

1. Navigate to https://resume2interview.com/nonexistent-page
2. Should show 404 page (not blank screen)

#### Step 4.6: Mobile Testing

1. Open https://resume2interview.com on mobile device or Chrome DevTools mobile view
2. Verify responsive layout
3. Test upload and analysis flow

---

### Phase 5: Monitoring & Smoke Testing (10 minutes)

#### Step 5.1: Check Railway Logs

```powershell
# In Railway dashboard → Production Service → Logs
# Watch for errors in real-time
# Filter for: ERROR, WARNING, CRITICAL

# Should see normal request logs:
# "INFO: Application startup complete"
# "INFO: POST /api/gap-analysis - 200"
```

#### Step 5.2: Check Vercel Logs

```powershell
# Vercel dashboard → Production Project → Functions (or Runtime Logs)
# Look for any errors or warnings
# Should see successful page loads
```

#### Step 5.3: Monitor Performance

```powershell
# In Vercel dashboard → Analytics
# Check:
# - Core Web Vitals (should be green)
# - Response times (< 2s)
# - Error rate (should be 0%)
```

#### Step 5.4: Set Up Alerts (Optional but Recommended)

**Railway Alerts**:
1. Railway dashboard → Project Settings → Alerts
2. Enable: "Service down", "High error rate"
3. Add email/Slack notification

**Vercel Alerts**:
1. Vercel dashboard → Project Settings → Notifications
2. Enable: "Build errors", "High error rate"

---

## ✅ Deployment Completion Checklist

### Backend (Railway)
- [x] Production service created
- [x] PostgreSQL database provisioned
- [x] Environment variables set (5 variables)
- [x] Build deployed successfully
- [x] Service status: Running
- [x] Database migrations applied
- [x] API endpoints responding
- [x] Analytics endpoint password-protected

### Frontend (Vercel)
- [x] Production project created
- [x] Backend URL updated in code
- [x] Deployment successful
- [x] Custom domain added: resume2interview.com
- [x] DNS configured in GoDaddy
- [x] SSL certificate valid
- [x] Frontend accessible at https://resume2interview.com

### End-to-End
- [x] User can upload resume
- [x] Analysis completes successfully
- [x] Results display correctly
- [x] Application saved to database
- [x] Analytics dashboard accessible
- [x] Excel export works
- [x] Mobile responsive
- [x] No console errors

### Monitoring
- [x] Railway logs clean (no errors)
- [x] Vercel logs clean
- [x] Performance metrics green
- [x] Alerts configured (optional)

---

## 📊 Post-Deployment Status Report

**Deployment Date**: ________________  
**Deployed by**: ________________  
**Production URL**: https://resume2interview.com

### Deployment Summary
- **Backend status**: [ ] Success / [ ] Partial / [ ] Failed
- **Frontend status**: [ ] Success / [ ] Partial / [ ] Failed
- **Database status**: [ ] Success / [ ] Failed
- **Overall status**: [ ] Success / [ ] Rollback Required

### Service URLs
- **Production Frontend**: https://resume2interview.com
- **Production Backend**: https://[railway-url].up.railway.app
- **Analytics Dashboard**: https://resume2interview.com/analytics

### Known Issues
- [ ] None
- [ ] List any issues discovered:
  1. _______________
  2. _______________

### Post-Deployment Actions Required
- [ ] Monitor logs for 24 hours
- [ ] Execute POST_DEPLOYMENT_VALIDATION.md
- [ ] Update team on successful deployment
- [ ] Schedule follow-up review in 1 week

---

## 🚨 Rollback Instructions

**If deployment fails at any step**, immediately execute rollback:

1. **Stop deployment process**
2. Open `ROLLBACK_PROCEDURE.md`
3. Follow rollback steps for failed component (frontend/backend)
4. Document failure reason
5. Schedule post-mortem

**Rollback triggers**:
- Build failures
- Service won't start (Railway)
- High error rate (> 10% requests failing)
- Critical functionality broken
- Database connection failures
- SSL certificate issues

---

## 📞 Support Contacts

**During Deployment**:
- Technical Lead: [Contact]
- DevOps Engineer: [Contact]
- On-Call Engineer: [Pager]

**Post-Deployment**:
- Monitor for 2 hours minimum after deployment
- Team should remain on standby for 24 hours
- Escalate critical issues immediately

---

## 🎉 Success!

If all steps completed successfully:

1. ✅ Mark deployment as **SUCCESS** in status report
2. ✅ Proceed to `POST_DEPLOYMENT_VALIDATION.md`
3. ✅ Notify team of successful deployment
4. ✅ Begin 24-hour monitoring period
5. ✅ Celebrate! 🎊

**Next Steps**:
- Complete post-deployment validation
- Monitor production for 24-48 hours
- Address any minor issues discovered
- Schedule retrospective meeting
