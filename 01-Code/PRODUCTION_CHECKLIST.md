# Resume2Interview - Production Deployment Checklist

## \ud83c\udfaf Environment Configuration Summary

### Staging Environment
| Component | Platform | URL | Branch |
|-----------|----------|-----|--------|
| Frontend | Vercel | `resume2interview-staging.vercel.app` | `ui-ux-redesign` |
| Backend | Railway | `staging-backend.up.railway.app` | `ui-ux-redesign` |
| Database | Railway | PostgreSQL (staging) | - |

### Production Environment
| Component | Platform | URL | Branch |
|-----------|----------|-----|--------|
| Frontend | Vercel | `www.resume2interview.com` | `main` |
| Backend | Railway | `api.resume2interview.com` (or Railway URL) | `main` |
| Database | Railway | PostgreSQL (production) | - |

---

## Step 1: Domain Configuration

### A. Purchase Domain (If Not Done)
- Domain: `resume2interview.com`
- Registrar: GoDaddy / Namecheap / Google Domains / Cloudflare

### B. DNS Configuration

**At Your Domain Registrar:**

#### For www.resume2interview.com (Vercel Frontend)
```
Type: CNAME
Name: www
Value: cname.vercel-dns.com
TTL: 3600
```

#### For Apex Domain (resume2interview.com)
```
Type: A
Name: @
Value: 76.76.21.21
TTL: 3600
```

#### For API Subdomain (Optional - Recommended)
```
Type: CNAME
Name: api
Value: (Get from Railway after setup)
TTL: 3600
```

**DNS Propagation**: Wait 5-60 minutes

---

## Step 2: Deploy Staging Environment

### 2.1 Staging Backend (Railway)

1. **Login to Railway**: https://railway.app
2. **New Project** \u2192 "Deploy from GitHub repo"
3. **Select**: `jaysibi/resume2interview`
4. **Service Configuration**:
   - **Name**: `resume2interview-backend-staging`
   - **Root Directory**: `01-Code/backend`
   - **Branch**: `ui-ux-redesign`

5. **Add PostgreSQL Database**:
   - Click "+ New" \u2192 "Database" \u2192 "PostgreSQL"
   - **Name**: `staging-database`
   - Railway auto-connects `DATABASE_URL`

6. **Environment Variables**:
   ```bash
   # Required
   OPENAI_API_KEY=sk-proj-your-openai-key-here
   DATABASE_URL=(auto-set by Railway)
   
   # CORS Configuration
   CORS_ORIGINS=https://resume2interview-staging.vercel.app,https://*.vercel.app
   
   # Environment Identifier
   ENVIRONMENT=staging
   ```

7. **Generate Domain**:
   - Settings \u2192 Networking \u2192 "Generate Domain"
   - **Copy URL**: `https://resume2interview-staging.up.railway.app`

8. **Run Database Migrations**:
   ```powershell
   cd C:\Projects\ResumeTailor\01-Code\backend
   
   # Set DATABASE_URL from Railway
   $env:DATABASE_URL = "postgresql://postgres:password@host.railway.app:5432/railway"
   
   # Run migrations
   alembic upgrade head
   ```

### 2.2 Staging Frontend (Vercel)

1. **Login to Vercel**: https://vercel.com/dashboard
2. **Add New Project** \u2192 "Import Git Repository"
3. **Select**: `jaysibi/resume2interview`
4. **Project Configuration**:
   ```
   Project Name: resume2interview-staging
   Root Directory: 01-Code/frontend
   Framework Preset: Vite
   Build Command: npm run build
   Output Directory: dist
   Install Command: npm install
   ```

5. **Git Configuration**:
   - **Production Branch**: `ui-ux-redesign` (for staging)
   - Auto-deploy: Enabled

6. **Environment Variables**:
   ```bash
   # Backend API URL (use Railway URL from step 2.1.7)
   VITE_API_URL=https://resume2interview-staging.up.railway.app
   
   # Environment identifier
   VITE_ENV=staging
   ```

7. **Click "Deploy"**
8. **Copy Staging URL**: `https://resume2interview-staging.vercel.app`

### 2.3 Update Staging Backend CORS

Go back to Railway staging service and update `CORS_ORIGINS`:
```bash
CORS_ORIGINS=https://resume2interview-staging.vercel.app
```

---

## Step 3: Test Staging Environment

### Pre-Production Testing Checklist

\u2610 **Frontend Loads**
   - Visit: `https://resume2interview-staging.vercel.app`
   - Homepage displays correctly
   - Navigation works
   - All pages load

\u2610 **Backend API Available**
   - Visit: `https://resume2interview-staging.up.railway.app/docs`
   - Swagger documentation loads
   - Test endpoints respond

\u2610 **Core Features**
   - [ ] Upload resume (PDF/DOCX)
   - [ ] Upload job description
   - [ ] Gap analysis generates
   - [ ] ATS score calculates
   - [ ] Results display correctly

\u2610 **Application Management**
   - [ ] View applications list
   - [ ] View application details
   - [ ] Delete single application
   - [ ] Bulk delete applications
   - [ ] Confirmation modal appears

\u2610 **Rate Limiting**
   - [ ] Rate limit modal displays after 5 requests
   - [ ] Countdown timer works
   - [ ] Can't submit during cooldown

\u2610 **Browser Testing**
   - [ ] Chrome
   - [ ] Firefox
   - [ ] Safari
   - [ ] Edge

\u2610 **Responsive Design**
   - [ ] Mobile phone
   - [ ] Tablet
   - [ ] Desktop

\u2610 **Console Errors**
   - [ ] No JavaScript errors
   - [ ] No CORS errors
   - [ ] No 404s for assets

---

## Step 4: Deploy Production Environment

### 4.1 Create Production Branch

```powershell
cd C:\Projects\ResumeTailor\01-Code

# Checkout main branch
git checkout main

# Merge staging branch (if not already done)
git merge ui-ux-redesign

# Push to origin
git push origin main
```

### 4.2 Production Backend (Railway)

1. **Create New Project** in Railway (or add service to existing)
2. **New** \u2192 "GitHub Repo" \u2192 `jaysibi/resume2interview`
3. **Service Configuration**:
   - **Name**: `resume2interview-backend-prod`
   - **Root Directory**: `01-Code/backend`
   - **Branch**: `main`

4. **Add PostgreSQL Database**:
   - Click "+ New" \u2192 "Database" \u2192 "PostgreSQL"
   - **Name**: `production-database`

5. **Environment Variables**:
   ```bash
   # Required
   OPENAI_API_KEY=sk-proj-your-openai-key-here
   DATABASE_URL=(auto-set by Railway)
   
   # CORS Configuration
   CORS_ORIGINS=https://www.resume2interview.com,https://resume2interview.com
   
   # Environment Identifier
   ENVIRONMENT=production
   ```

6. **Add Custom Domain** (Recommended):
   - Settings \u2192 Networking \u2192 "Custom Domain"
   - Enter: `api.resume2interview.com`
   - Railway provides CNAME target
   - Add to your DNS:
     ```
     Type: CNAME
     Name: api
     Value: <railway-provided-value>
     ```

7. **Or Generate Railway Domain**:
   - If not using custom domain
   - Settings \u2192 Networking \u2192 "Generate Domain"
   - **Copy URL**: `https://resume2interview-prod.up.railway.app`

8. **Run Production Database Migrations**:
   ```powershell
   cd C:\Projects\ResumeTailor\01-Code\backend
   
   # Set production DATABASE_URL from Railway
   $env:DATABASE_URL = "postgresql://postgres:password@prod-host.railway.app:5432/railway"
   
   # Run migrations
   alembic upgrade head
   ```

### 4.3 Production Frontend (Vercel)

1. **Add New Project** in Vercel
2. **Import**: `jaysibi/resume2interview`
3. **Project Configuration**:
   ```
   Project Name: resume2interview-production
   Root Directory: 01-Code/frontend
   Framework Preset: Vite
   Build Command: npm run build
   Output Directory: dist
   Install Command: npm install
   ```

4. **Git Configuration**:
   - **Production Branch**: `main`
   - Auto-deploy: Enabled

5. **Environment Variables**:
   ```bash
   # Backend API URL (use custom domain or Railway URL)
   VITE_API_URL=https://api.resume2interview.com
   # Or: VITE_API_URL=https://resume2interview-prod.up.railway.app
   
   # Environment identifier
   VITE_ENV=production
   ```

6. **Deploy**

### 4.4 Add Custom Domain to Vercel

1. **Project Settings** \u2192 "Domains"
2. **Add Domain**:
   - Enter: `www.resume2interview.com`
   - Click "Add"
3. **Add Apex Domain**:
   - Enter: `resume2interview.com`
   - Click "Add"
4. **Verify DNS**:
   - Vercel shows DNS configuration status
   - Green checkmark when configured correctly
5. **SSL Certificate**:
   - Vercel auto-provisions SSL (takes 5-10 minutes)
   - Look for \ud83d\udd12 icon next to domain

---

## Step 5: Post-Deployment Verification

### Production Testing Checklist

\u2610 **Domain Resolution**
   - [ ] `resume2interview.com` resolves
   - [ ] `www.resume2interview.com` resolves
   - [ ] Both redirect to www (if configured)
   - [ ] SSL certificate valid (\ud83d\udd12 in browser)

\u2610 **API Connectivity**
   - [ ] `api.resume2interview.com` (if using custom domain)
   - [ ] Backend health check successful
   - [ ] `/docs` endpoint accessible

\u2610 **Full E2E Test**
   - [ ] Visit www.resume2interview.com
   - [ ] Complete resume upload flow
   - [ ] Generate gap analysis
   - [ ] View results
   - [ ] Test applications CRUD
   - [ ] Verify rate limiting

\u2610 **Performance**
   - [ ] Page load < 3 seconds
   - [ ] API responses < 2 seconds
   - [ ] No timeout errors

\u2610 **Monitoring**
   - [ ] Check Railway logs (backend)
   - [ ] Check Vercel logs (frontend)
   - [ ] No error spikes
   - [ ] Database connections stable

---

## Step 6: Environment Variables Reference

### Backend Environment Variables (Railway)

#### Staging
```bash
OPENAI_API_KEY=sk-proj-your-key-here
DATABASE_URL=postgresql://... (auto-set)
CORS_ORIGINS=https://resume2interview-staging.vercel.app
ENVIRONMENT=staging
```

#### Production
```bash
OPENAI_API_KEY=sk-proj-your-key-here
DATABASE_URL=postgresql://... (auto-set)
CORS_ORIGINS=https://www.resume2interview.com,https://resume2interview.com
ENVIRONMENT=production
```

### Frontend Environment Variables (Vercel)

#### Staging
```bash
VITE_API_URL=https://resume2interview-staging.up.railway.app
VITE_ENV=staging
```

#### Production
```bash
VITE_API_URL=https://api.resume2interview.com
# Or: VITE_API_URL=https://resume2interview-prod.up.railway.app
VITE_ENV=production
```

---

## Step 7: Deployment Workflow

### Day-to-Day Development

```bash
# 1. Make changes locally
git checkout ui-ux-redesign
# ... make changes ...

# 2. Commit and push
git add .
git commit -m "feat: add new feature"
git push origin ui-ux-redesign

# 3. Staging auto-deploys
# Test at: https://resume2interview-staging.vercel.app

# 4. If tests pass, merge to production
git checkout main
git merge ui-ux-redesign
git push origin main

# 5. Production auto-deploys
# Live at: https://www.resume2interview.com
```

### Rollback Procedure

If production deployment fails:

**Vercel:**
1. Go to project \u2192 "Deployments"
2. Find last working deployment
3. Click "..." \u2192 "Promote to Production"

**Railway:**
1. Service \u2192 "Deployments"
2. Find last working deployment
3. Click "..." \u2192 "Rollback"

**Git:**
```bash
# Revert to previous commit
git revert HEAD
git push origin main
```

---

## Step 8: Monitoring & Maintenance

### Health Check Endpoints

**Staging:**
- Frontend: `https://resume2interview-staging.vercel.app`
- Backend: `https://resume2interview-staging.up.railway.app/docs`

**Production:**
- Frontend: `https://www.resume2interview.com`
- Backend: `https://api.resume2interview.com/docs`

### Logs Access

**Vercel:**
- Project \u2192 "Deployments" \u2192 Select deployment \u2192 "View Function Logs"
- Real-time logs: Vercel CLI `vercel logs`

**Railway:**
- Service \u2192 "Deployments" \u2192 Click deployment \u2192 "View Logs"
- Real-time: Railway CLI `railway logs`

### Database Backups

**Railway PostgreSQL:**
1. Service \u2192 Database \u2192 "Backups"
2. Automated daily backups
3. Manual backup: Click "Create Backup"
4. Restore: Select backup \u2192 "Restore"

---

## Step 9: Security Checklist

\u2610 **Environment Variables**
   - [ ] OPENAI_API_KEY not exposed in frontend
   - [ ] DATABASE_URL not committed to git
   - [ ] .env files in .gitignore

\u2610 **CORS Configuration**
   - [ ] Only allow production domains
   - [ ] No wildcard (*) in production

\u2610 **SSL/TLS**
   - [ ] HTTPS enabled (Vercel auto)
   - [ ] Valid SSL certificate
   - [ ] HTTP redirects to HTTPS

\u2610 **Rate Limiting**
   - [ ] Implemented and tested (5 req/day)
   - [ ] IP-based tracking working

\u2610 **Database**
   - [ ] Strong passwords
   - [ ] Connection from Railway only
   - [ ] Backups enabled

---

## Step 10: Cost Monitoring

### Expected Monthly Costs

| Service | Tier | Cost | Notes |
|---------|------|------|-------|
| Vercel | Hobby | $0 | 100GB bandwidth, unlimited sites |
| Railway Staging | Developer | $5 | 500 execution hours |
| Railway Production | Developer | $5 | 500 execution hours |
| Domain | Annual | ~$12/year | Resume2interview.com |

**Total: ~$10/month + $1/month domain**

### Upgrade Triggers

**Vercel Pro ($20/month):**
- Need more bandwidth (>100GB)
- Team collaboration features
- Advanced analytics

**Railway Pro ($20/month per service):**
- Need more execution hours
- Vertical scaling requirements
- Priority support

---

## Troubleshooting Guide

### Issue: "Failed to fetch" API Error

**Check:**
1. Backend is running (visit /docs endpoint)
2. VITE_API_URL is correct in Vercel
3. CORS_ORIGINS includes frontend URL in Railway
4. No typos in URLs

**Fix:**
```bash
# Update Vercel environment variable
VITE_API_URL=https://correct-backend-url.railway.app

# Update Railway CORS
CORS_ORIGINS=https://www.resume2interview.com
```

### Issue: Domain Not Resolving

**Check:**
1. DNS propagation (use https://dnschecker.org)
2. CNAME/A records correct
3. Vercel domain status (green checkmark)

**Fix:**
- Wait 5-60 minutes for DNS propagation
- Verify DNS records at registrar
- Check Vercel domain configuration

### Issue: SSL Certificate Error

**Check:**
1. Domain properly verified in Vercel
2. DNS records pointing correctly
3. Certificate provisioning status

**Fix:**
- Vercel auto-provisions certificates
- Can take 5-10 minutes
- Remove and re-add domain if stuck

### Issue: Database Connection Failed

**Check:**
1. DATABASE_URL is set in Railway
2. Migrations ran successfully
3. PostgreSQL service running

**Fix:**
```bash
# Verify DATABASE_URL
echo $env:DATABASE_URL

# Re-run migrations
alembic upgrade head

# Restart backend service in Railway
```

### Issue: Rate Limit Not Working

**Check:**
1. Backend logs for rate limit enforcement
2. Frontend modal appears correctly
3. IP tracking in usage_logs table

**Fix:**
- Check rate_limiter.py implementation
- Verify usage_logs table exists
- Test with curl/Postman

---

## Success Criteria

\u2705 **Staging Environment**
- Accessible at staging URL
- Auto-deploys from ui-ux-redesign branch
- All features working
- Used for testing before production

\u2705 **Production Environment**
- Accessible at www.resume2interview.com
- SSL certificate valid
- Auto-deploys from main branch
- All features working
- Monitoring in place

\u2705 **Deployment Workflow**
- Changes pushed to ui-ux-redesign
- Tested in staging
- Merged to main for production
- Rollback procedures documented

---

## Quick Reference URLs

### Staging
- **Frontend**: https://resume2interview-staging.vercel.app
- **Backend**: https://resume2interview-staging.up.railway.app
- **API Docs**: https://resume2interview-staging.up.railway.app/docs

### Production
- **Frontend**: https://www.resume2interview.com
- **Backend**: https://api.resume2interview.com (or Railway URL)
- **API Docs**: https://api.resume2interview.com/docs

### Dashboards
- **Vercel**: https://vercel.com/dashboard
- **Railway**: https://railway.app/dashboard
- **GitHub**: https://github.com/jaysibi/resume2interview

---

**\ud83c\udf89 Deployment Complete!**

Your multi-environment setup is ready for production use.
