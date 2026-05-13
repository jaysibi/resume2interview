# Rollback Procedure - Resume2Interview

**🚨 EMERGENCY PROCEDURE** - Use when production deployment fails or critical issues detected

**⏱️ Target Time**: Complete rollback in < 15 minutes

---

## 🎯 When to Rollback

### Immediate Rollback Triggers (Execute Immediately)

- [ ] **Service completely down** - Production unreachable > 5 minutes
- [ ] **Critical functionality broken** - Resume analysis failing
- [ ] **Database data loss detected** - Missing user data
- [ ] **Security breach** - Credentials exposed, injection vulnerability
- [ ] **Error rate > 25%** - More than 1 in 4 requests failing
- [ ] **Deployment build failed** - Service won't start

### Delayed Rollback Triggers (Evaluate First)

- [ ] **Error rate 10-25%** - Assess impact before rolling back
- [ ] **Performance degraded** - Response times > 10 seconds
- [ ] **Minor feature broken** - Analytics export not working
- [ ] **UI issues** - Layout problems, missing images

---

## 🚀 Quick Rollback Commands

### Frontend Rollback (Vercel)
```powershell
# Option 1: Via Dashboard (Fastest)
# 1. Go to: https://vercel.com/[profile]/resume2interview-production/deployments
# 2. Find last working deployment (check timestamp)
# 3. Click "..." menu → "Promote to Production"
# 4. Confirm promotion
# ✅ Site rolls back in ~30 seconds

# Option 2: Via CLI
cd C:\Projects\ResumeTailor\01-Code\frontend
vercel rollback  # Rolls back to previous production deploy
```

### Backend Rollback (Railway)
```powershell
# Option 1: Via Dashboard (Recommended)
# 1. Go to: https://railway.app → Production Service → Deployments
# 2. Find last working deployment (green "Success" status)
# 3. Click deployment → "Redeploy"
# 4. Confirm redeploy
# ✅ Service rolls back in ~3-5 minutes

# Option 2: Deploy Specific Commit
railway up --service graceful-exploration-production --commit [COMMIT_HASH]
```

---

## 📋 Full Rollback Procedure

### Phase 1: Assessment & Decision (2 minutes)

#### Step 1.1: Confirm Rollback Needed

**Gather evidence**:
```powershell
# Check error rate
$testUrl = "https://resume2interview.com"
for ($i=1; $i -le 10; $i++) {
    try {
        $response = Invoke-WebRequest -Uri $testUrl -UseBasicParsing
        Write-Host "✅ Request $i : $($response.StatusCode)"
    } catch {
        Write-Host "❌ Request $i : Failed"
    }
    Start-Sleep -Seconds 1
}

# If > 2 failures out of 10: Consider rollback
```

**Check logs**:
- Railway dashboard → Logs (look for ERROR, CRITICAL)
- Vercel dashboard → Functions → Errors
- User reports (support tickets, social media)

#### Step 1.2: Identify Last Working Deployment

**Frontend (Vercel)**:
1. Vercel dashboard → Deployments
2. Look for last deployment with:
   - Status: "Ready" (green)
   - Created: Before current broken deployment
   - No reported issues during that time

**Backend (Railway)**:
1. Railway dashboard → Deployments
2. Find last "Success" deployment
3. Note commit hash or deployment ID

#### Step 1.3: Notify Team

```powershell
# Send alert to team
# - Slack: "@channel Production rollback initiated"
# - Email: Technical lead, DevOps
# - Status page: Update with "Investigating"
```

**Template message**:
```
🚨 PRODUCTION ROLLBACK IN PROGRESS

Issue: [Brief description]
Severity: [Critical/High]
Started: [Time]
ETA: 15 minutes

Rolling back to:
- Frontend: Deployment [ID] from [Time]
- Backend: Deployment [ID] from [Time]

Status updates will follow.
```

---

### Phase 2: Frontend Rollback (5 minutes)

#### Step 2.1: Promote Previous Deployment

**Via Vercel Dashboard**:
1. Navigate to https://vercel.com/[profile]/resume2interview-production/deployments
2. Find last working deployment
3. Click deployment to open details
4. Click "..." menu (top right)
5. Select "Promote to Production"
6. Confirm: "Yes, promote to production"

**Via Vercel CLI**:
```powershell
cd C:\Projects\ResumeTailor\01-Code\frontend

# Rollback to previous
vercel rollback

# OR deploy specific deployment:
vercel alias set [deployment-url] resume2interview.com --yes
```

#### Step 2.2: Verify Frontend Rollback

```powershell
# Wait 30 seconds for deployment
Start-Sleep -Seconds 30

# Check bundle version
$html = Invoke-WebRequest -Uri "https://resume2interview.com" -UseBasicParsing
if ($html.Content -match 'src="(/assets/index-([^"]+)\.js)"') {
    Write-Host "Rolled back to bundle: $($Matches[1])"
}

# Test homepage loads
if ($html.StatusCode -eq 200) {
    Write-Host "✅ Frontend rollback successful"
} else {
    Write-Host "❌ Frontend rollback failed - escalate"
}
```

#### Step 2.3: Test Critical User Flow

```powershell
# Manual test in browser (incognito):
# 1. Navigate to https://resume2interview.com
# 2. Upload test resume
# 3. Analyze resume
# 4. Verify results display

# If any step fails: Continue to backend rollback
```

---

### Phase 3: Backend Rollback (5 minutes)

#### Step 3.1: Redeploy Previous Version

**Via Railway Dashboard**:
1. Navigate to https://railway.app → Production Service
2. Click "Deployments" tab
3. Find last "Success" deployment (green)
4. Click deployment row
5. Click "Redeploy" button (top right)
6. Confirm redeploy

**Via Railway CLI**:
```powershell
# Deploy specific commit
cd C:\Projects\ResumeTailor
$lastWorkingCommit = "[COMMIT_HASH]"  # Get from git log
railway up --service graceful-exploration-production --commit $lastWorkingCommit
```

#### Step 3.2: Monitor Backend Deployment

```powershell
# Watch Railway logs in dashboard
# Wait for "Application startup complete"
# Typical time: 3-5 minutes

# Status indicators:
# - Build: Running → Success
# - Deploy: Deploying → Running
# - Health: Healthy (green)
```

#### Step 3.3: Verify Backend Health

```powershell
# Wait for deployment to complete
Start-Sleep -Seconds 180  # 3 minutes

$backendUrl = "https://[production-railway-url].up.railway.app"

# Test API health
try {
    $response = Invoke-WebRequest -Uri "$backendUrl/docs" -UseBasicParsing
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ Backend rollback successful"
    }
} catch {
    Write-Host "❌ Backend rollback failed - escalate immediately"
    Write-Host "Error: $($_.Exception.Message)"
}

# Test analytics endpoint
$headers = @{ 'X-Analytics-Password' = '[PRODUCTION_PASSWORD]' }
$response = Invoke-RestMethod -Uri "$backendUrl/api/analytics/usage-stats" -Headers $headers
if ($response.success) {
    Write-Host "✅ Backend API functional"
}
```

---

### Phase 4: Verification (3 minutes)

#### Step 4.1: End-to-End Test

**Critical path test**:
```powershell
# Automated test script
$testResults = @{
    HomePage = $false
    Upload = $false
    Analysis = $false
    Results = $false
}

# Test homepage
try {
    $response = Invoke-WebRequest -Uri "https://resume2interview.com" -UseBasicParsing
    $testResults.HomePage = ($response.StatusCode -eq 200)
} catch { }

# Manual tests (perform in browser):
# 1. Upload test resume ✓
# 2. Paste job description ✓
# 3. Click "Analyze" ✓
# 4. Verify results display ✓

Write-Host "Test Results:"
$testResults | Format-Table -AutoSize
```

#### Step 4.2: Check Error Rates

```powershell
# Monitor for 5 minutes post-rollback
# Railway logs should show:
# - No ERROR level logs
# - Successful API calls (200, 201 responses)
# - Normal traffic patterns

# Vercel logs should show:
# - No function errors
# - Page loads successful
```

#### Step 4.3: Verify Database State

```powershell
# Railway dashboard → PostgreSQL → Data
# - Check applications table
# - Verify no data loss
# - Check record count matches expectations

# If data loss detected: CRITICAL - Escalate to DBA
```

---

### Phase 5: Communication & Cleanup (2 minutes)

#### Step 5.1: Update Team

**Template message**:
```
✅ PRODUCTION ROLLBACK COMPLETE

Issue: [Brief description]
Resolution: Rolled back to previous stable version
Downtime: [X] minutes

Current status:
- Frontend: Rolled back to deployment [ID]
- Backend: Rolled back to deployment [ID]
- Service: Fully operational
- Error rate: < 1%

Next steps:
- Continue monitoring for 24 hours
- Root cause analysis scheduled
- Fix in progress for next release
```

#### Step 5.2: Update Status Page

```powershell
# If you have status page (e.g., status.resume2interview.com):
# Update: "All systems operational"
# Post-mortem: Schedule and publish within 48 hours
```

#### Step 5.3: Document Incident

Create incident report:
```markdown
# Incident Report: [Date]

## Summary
- **Time**: [Start] - [End]
- **Duration**: [X] minutes
- **Severity**: [Critical/High/Medium]
- **Impact**: [Description]

## Timeline
- [Time]: Deployment started
- [Time]: Issue detected
- [Time]: Rollback initiated
- [Time]: Rollback completed
- [Time]: Service restored

## Root Cause
[Description]

## Resolution
[What was done]

## Prevention
[How to prevent in future]

## Action Items
- [ ] Fix root cause
- [ ] Update deployment process
- [ ] Add monitoring/alerts
- [ ] Update documentation
```

---

## 🗄️ Database Rollback (Use with EXTREME Caution)

### ⚠️ WARNING

**DO NOT rollback database without DBA approval**

Database rollback can cause:
- Data loss
- Referential integrity issues
- Application crashes
- User data corruption

### When Database Rollback is Needed

Only in these scenarios:
- [ ] Schema migration caused critical failure
- [ ] Data corruption during deployment
- [ ] Accidental data deletion
- [ ] Database performance severely degraded

### Database Rollback Procedure

#### Option 1: Revert Migration (Preferred)

```bash
# Connect to Railway database
railway run -s graceful-exploration-production bash

# Downgrade Alembic migration
alembic downgrade -1  # Go back 1 migration

# OR go back to specific version:
alembic downgrade [revision_hash]

# Verify schema:
alembic current
psql $DATABASE_URL -c "\dt"  # List tables
```

#### Option 2: Restore from Backup

**Railway automatic backups**:
1. Railway dashboard → PostgreSQL → Backups
2. Find backup before deployment
3. Click "Restore"
4. **WARNING**: This will overwrite current data
5. Confirm restoration

**Manual backup restoration** (if you have SQL dump):
```bash
# Restore from backup file
psql $DATABASE_URL < backup-[date].sql

# Verify restoration:
psql $DATABASE_URL -c "SELECT COUNT(*) FROM applications;"
```

#### Step DB-3: Verify Data Integrity

```sql
-- Check table counts
SELECT 
    'users' as table_name, COUNT(*) as count FROM users
UNION ALL
SELECT 'resumes', COUNT(*) FROM resumes
UNION ALL
SELECT 'applications', COUNT(*) FROM applications;

-- Check for orphaned records
SELECT COUNT(*) FROM gap_analyses ga
LEFT JOIN applications a ON ga.application_id = a.id
WHERE a.id IS NULL;  -- Should be 0
```

---

## 🔄 Partial Rollback Scenarios

### Scenario 1: Backend OK, Frontend Broken

**Solution**: Rollback frontend only
```powershell
# Follow Phase 2 only
# Skip Phase 3 (backend rollback)
# Verify frontend connects to current backend
```

### Scenario 2: Frontend OK, Backend Broken

**Solution**: Rollback backend only
```powershell
# Skip Phase 2 (frontend rollback)
# Follow Phase 3 only
# Verify backend API works with current frontend
```

### Scenario 3: Database Migration Failed

**Solution**: Revert migration, keep code
```bash
# Downgrade database schema
alembic downgrade -1

# Keep backend code deployed
# Update code to work with old schema
```

---

## 📊 Post-Rollback Checklist

### Immediate (Within 1 hour)
- [ ] Service fully operational
- [ ] Error rate < 1%
- [ ] Response times normal (< 2s)
- [ ] Critical functionality tested
- [ ] Team notified
- [ ] Status page updated

### Short-term (Within 24 hours)
- [ ] Root cause identified
- [ ] Fix developed and tested in staging
- [ ] Post-mortem scheduled
- [ ] Incident report completed
- [ ] Monitoring enhanced (if needed)

### Long-term (Within 1 week)
- [ ] Post-mortem conducted
- [ ] Action items assigned
- [ ] Documentation updated
- [ ] Deployment process improved
- [ ] Training conducted (if needed)

---

## 🚫 Rollback Failed - Escalation

### If Rollback Does Not Resolve Issue

**Immediate actions**:
1. **STOP** - Do not attempt further rollbacks
2. **Escalate** to technical lead immediately
3. **Preserve logs** - Save all logs before they rotate
4. **Enable maintenance mode** if possible

**Emergency contacts**:
- Technical Lead: [Contact]
- DevOps Lead: [Contact]
- CTO/VP Engineering: [Contact]
- On-Call Hotline: [Number]

**Alternative recovery options**:
1. Deploy to backup/disaster recovery environment
2. Enable maintenance page
3. Partial service restoration (read-only mode)
4. Direct database queries for critical data

---

## 🎓 Lessons for Prevention

Based on staging experience:

1. **Always have rollback plan before deploying**
   - Document last working deployment IDs
   - Test rollback procedure in staging
   - Have team on standby

2. **Use feature flags**
   - Roll out features gradually
   - Disable broken features without full rollback
   - A/B test risky changes

3. **Staged rollouts**
   - Deploy to 10% of users first
   - Monitor for issues before full rollout
   - Automatic rollback on error spike

4. **Comprehensive monitoring**
   - Real-time error tracking
   - Automated alerts for anomalies
   - User impact metrics

5. **Better testing**
   - Staging must mirror production
   - Load testing before major releases
   - Automated E2E tests in CI/CD

---

## 📞 Support During Rollback

**If you need help during rollback**:

1. Don't panic - Follow steps methodically
2. Document what you're doing
3. Contact team immediately
4. Preserve all logs and evidence
5. Focus on service restoration first, investigation later

**Hotline numbers**:
- On-Call Engineer: [Number]
- Technical Lead: [Number]
- Emergency Pager: [Number]

---

## ✅ Rollback Success Criteria

Rollback is considered successful when ALL of these are true:

- [ ] Production site loads (https://resume2interview.com)
- [ ] Users can upload resumes
- [ ] Analysis completes successfully
- [ ] Results display correctly
- [ ] Database operations work
- [ ] Error rate < 1%
- [ ] Response times < 3 seconds
- [ ] No data loss
- [ ] Monitoring shows healthy status

**If all criteria met**: Rollback complete ✅

**If any criteria not met**: Continue troubleshooting or escalate
