# Deployment Strategy - Resume2Interview

## 🎯 Overview

Resume2Interview uses a **multi-environment, continuous deployment** strategy with automated staging and manual production releases.

## 🏗️ Architecture

### Frontend (Vercel)
- **Staging**: `resume2interview-staging.vercel.app`
- **Production**: `resume2interview.com` (GoDaddy domain)
- **Framework**: React + Vite
- **Deployment**: Git-based automatic + CLI manual

### Backend (Railway)
- **Staging**: `graceful-exploration-staging.up.railway.app`
- **Production**: `graceful-exploration-production.up.railway.app` (TBD)
- **Framework**: FastAPI + PostgreSQL
- **Deployment**: Git-based automatic

## 📋 Deployment Environments

### 1. Local Development
- **Purpose**: Feature development and testing
- **Database**: SQLite or local PostgreSQL
- **Backend**: `http://localhost:8000`
- **Frontend**: `http://localhost:5173`
- **OpenAI**: Personal API key

### 2. Staging Environment
- **Purpose**: Integration testing and QA
- **Frontend**: https://resume2interview-staging.vercel.app
- **Backend**: https://graceful-exploration-staging.up.railway.app
- **Database**: Railway PostgreSQL (staging)
- **Auto-deploy**: Enabled on `main` branch push
- **Analytics Password**: `Railwayismessy` (change for prod)

### 3. Production Environment
- **Purpose**: Live user-facing application
- **Frontend**: https://resume2interview.com
- **Backend**: Railway production service (separate from staging)
- **Database**: Railway PostgreSQL (production - separate instance)
- **Auto-deploy**: **DISABLED** - Manual approval required
- **Analytics Password**: **Strong password** (not staging value)

## 🔄 Deployment Flow

```
Developer → GitHub (main branch)
              ↓
         Auto-deploy to STAGING
              ↓
         QA & Validation
              ↓
         Manual approval
              ↓
         Deploy to PRODUCTION
              ↓
         Post-deployment validation
```

## 🚀 Deployment Methods

### Method 1: Git-Based Auto-Deploy (Staging Only)
```bash
# Code changes automatically deploy to staging
git add .
git commit -m "Feature: description"
git push origin main
# Staging auto-deploys via Vercel + Railway webhooks
```

**Advantages:**
- ✅ Fast deployment (< 2 minutes)
- ✅ No manual intervention needed
- ✅ Automatic rollback on build failure

**Disadvantages:**
- ❌ No approval gate
- ❌ Risk of deploying untested code

### Method 2: CLI Manual Deploy (Production)
```bash
# Frontend (Vercel)
cd 01-Code/frontend
vercel --prod --yes

# Backend (Railway)
railway up --service production-backend
```

**Advantages:**
- ✅ Full control over deployment timing
- ✅ Can deploy specific commits
- ✅ Approval gate before production

**Disadvantages:**
- ❌ Slower than auto-deploy
- ❌ Requires manual intervention

### Method 3: Tagged Release Deploy (Recommended for Production)
```bash
# Create release tag
git tag -a v1.0.0 -m "Production release v1.0.0"
git push origin v1.0.0

# Deploy frontend
cd 01-Code/frontend
vercel --prod --yes

# Deploy backend via Railway dashboard
# Select deployment from tag v1.0.0
```

**Advantages:**
- ✅ Version control
- ✅ Easy rollback to specific version
- ✅ Audit trail

## 🎛️ Deployment Configuration

### Vercel Configuration

**Staging Project:**
- Project: `resume2interview-staging`
- Git: Auto-deploy from `main` branch
- Root Directory: `01-Code/frontend`
- Build Command: `npm run build`
- Output Directory: `dist`

**Production Project:**
- Project: `resume2interview-production`
- Git: **Manual deploy only** (no auto-deploy)
- Root Directory: `01-Code/frontend`
- Domain: `resume2interview.com` (GoDaddy)
- Build Command: `npm run build`
- Output Directory: `dist`

### Railway Configuration

**Staging Service:**
- Service: `graceful-exploration-staging`
- Git: Auto-deploy from `main` branch
- Root Directory: Auto-detected (`01-Code/backend`)
- Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

**Production Service:**
- Service: `graceful-exploration-production`
- Git: **Manual deploy only**
- Root Directory: Auto-detected (`01-Code/backend`)
- Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- Database: Separate PostgreSQL instance

## 🔐 Security Considerations

### Staging Environment
- ✅ Use test data only
- ✅ Weak analytics password acceptable (for testing)
- ✅ OpenAI rate limits can be lower
- ✅ CORS includes localhost for development

### Production Environment
- ⚠️ **NEVER** use staging database credentials
- ⚠️ Strong analytics password (16+ characters, complex)
- ⚠️ OpenAI production API key (separate from staging)
- ⚠️ CORS restricted to production domain only
- ⚠️ Remove debug endpoints (`/debug/*`)
- ⚠️ Enable rate limiting (stricter than staging)

## 📊 Deployment Metrics

### Success Criteria
- ✅ Build completes without errors
- ✅ All tests pass in staging
- ✅ Zero critical errors in logs (30 mins post-deploy)
- ✅ Analytics endpoint responds (password-protected)
- ✅ Application tracking saves to database
- ✅ Response times < 2s (95th percentile)

### Rollback Triggers
- ❌ Build failures
- ❌ 500 error rate > 5%
- ❌ Response times > 5s consistently
- ❌ Database connection failures
- ❌ Critical functionality broken (upload, analysis)

## 🔄 Rollback Strategy

### Frontend Rollback (Vercel)
1. Vercel Dashboard → Deployments
2. Find last working deployment
3. Click "Promote to Production"
4. Verify deployment

### Backend Rollback (Railway)
1. Railway Dashboard → Deployments
2. Find last working deployment
3. Click "Redeploy"
4. Verify service health

### Database Rollback
- **DO NOT rollback database** without DBA review
- Use database migrations (Alembic)
- Restore from backup if critical

## 📅 Deployment Schedule

### Staging Deployments
- **Frequency**: Multiple times per day
- **Window**: Anytime (24/7)
- **Approval**: Not required

### Production Deployments
- **Frequency**: Weekly or bi-weekly
- **Window**: Tuesday-Thursday, 10 AM - 2 PM PST
- **Avoid**: Fridays, weekends, holidays
- **Approval**: Required from tech lead

## 🧪 Testing Requirements

### Before Staging Deploy
- ✅ Local tests pass
- ✅ Code review approved
- ✅ No linting errors

### Before Production Deploy
- ✅ Staging validation complete (24-48 hours)
- ✅ All integration tests pass
- ✅ Performance testing complete
- ✅ Security audit if major changes
- ✅ Database migration tested
- ✅ Rollback plan documented

## 🎯 Deployment Phases

### Phase 1: Pre-Production Setup (One-time)
1. Create Railway production service
2. Create Vercel production project
3. Configure GoDaddy DNS
4. Set up production environment variables
5. Create production database
6. Run initial database migrations
7. Configure monitoring alerts

### Phase 2: Initial Production Deployment
1. Deploy backend to Railway production
2. Verify backend health
3. Run database migrations
4. Deploy frontend to Vercel production
5. Update GoDaddy DNS to Vercel
6. Verify end-to-end functionality
7. Monitor for 24 hours

### Phase 3: Ongoing Deployments
1. Feature development in local
2. Push to GitHub → auto-deploy to staging
3. Validate in staging (24-48 hours)
4. Tag release version
5. Manual deploy to production
6. Post-deployment validation
7. Monitor for issues

## 🔍 Monitoring Strategy

### Real-Time Monitoring
- Vercel Analytics (frontend performance)
- Railway Logs (backend errors)
- Custom analytics dashboard (application metrics)

### Alerting
- 500 errors > 10 in 5 minutes
- Response time > 5s for 3 consecutive requests
- Database connection failures
- OpenAI API failures

### Metrics to Track
- Request volume
- Response times (p50, p95, p99)
- Error rates (4xx, 5xx)
- Application usage (resumes analyzed, applications created)
- OpenAI API usage and costs

## 📝 Change Management

### Small Changes (Hotfixes)
- Bug fixes, copy changes, minor UI tweaks
- Can deploy same day after staging validation
- Minimal rollback risk

### Medium Changes (Features)
- New features, API changes, database schema changes
- Requires 24-48 hours staging validation
- Rollback plan required

### Large Changes (Major Updates)
- Architecture changes, third-party integrations
- Requires 1 week staging validation
- Rollback plan + backup plan required
- Consider phased rollout

## 🎓 Lessons from Staging Deployment

### Issue 1: Vercel Free Plan Limitations
**Problem**: Vercel free plan doesn't support external URL rewrites  
**Solution**: Frontend calls Railway API directly  
**Production Impact**: Same solution applies, no proxy needed

### Issue 2: Railway Auto-Detection vs Manual Config
**Problem**: `railway.toml` conflicted with auto-detection  
**Solution**: Remove railway.toml, let Railway auto-detect  
**Production Impact**: Do not use railway.toml in production

### Issue 3: Application Tracking Not Enabled
**Problem**: Database not saving application records  
**Solution**: Pass `createApplication: true` parameter  
**Production Impact**: Verify this is enabled before deployment

### Issue 4: Vercel CLI vs Dashboard Mismatch
**Problem**: CLI linked to different project than expected  
**Solution**: Check `.vercel/project.json` configuration  
**Production Impact**: Verify CLI is linked to production project

### Issue 5: Auto-Deploy Not Triggering
**Problem**: Git pushes not triggering Vercel deployments  
**Solution**: Verify Git webhook configuration in dashboard  
**Production Impact**: Disable auto-deploy for production (manual only)

## 🚀 Future Improvements

1. **Blue-Green Deployment**: Zero-downtime deployments
2. **Canary Releases**: Gradual rollout to subset of users
3. **Automated Testing**: E2E tests in CI/CD pipeline
4. **Database Replication**: Read replicas for scalability
5. **CDN Optimization**: Cache static assets more aggressively
6. **API Gateway**: Rate limiting and request routing
7. **Disaster Recovery**: Multi-region failover

## 📞 Support Contacts

- **Technical Lead**: [Contact info]
- **DevOps**: [Contact info]
- **On-Call**: [Pager duty rotation]
