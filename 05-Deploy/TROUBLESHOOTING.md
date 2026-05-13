# Troubleshooting Guide - Resume2Interview

This guide documents common issues encountered during deployment and their solutions, based on real-world staging deployment experience.

---

## 🎯 Quick Reference

| Issue | Severity | Solution Page |
|-------|----------|---------------|
| Analytics 401 errors | High | [Issue 1](#issue-1-analytics-401-unauthorized) |
| Vercel proxy not working | High | [Issue 2](#issue-2-vercel-proxy-failure) |
| Railway deployment fails | Critical | [Issue 3](#issue-3-railway-deployment-failure) |
| Application tracking missing | High | [Issue 4](#issue-4-application-records-not-saving) |
| Auto-deploy not triggering | Medium | [Issue 5](#issue-5-vercel-auto-deploy-not-triggering) |
| Frontend shows old code | High | [Issue 6](#issue-6-frontend-deployment-not-updating) |
| Database connection error | Critical | [Issue 7](#issue-7-database-connection-errors) |
| OpenAI API errors | Critical | [Issue 8](#issue-8-openai-api-failures) |
| CORS errors | High | [Issue 9](#issue-9-cors-errors-in-browser) |
| SSL certificate issues | High | [Issue 10](#issue-10-ssl-certificate-problems) |

---

## 🔍 Diagnostic Commands

### Check Service Health
```powershell
# Frontend (Vercel)
Invoke-WebRequest -Uri "https://resume2interview.com" -UseBasicParsing

# Backend (Railway)
$backendUrl = "https://[railway-url].up.railway.app"
Invoke-WebRequest -Uri "$backendUrl/docs" -UseBasicParsing

# Database (via backend)
Invoke-RestMethod -Uri "$backendUrl/debug/db-config"
```

### Check Deployment Status
```powershell
# Vercel - Check current bundle
$html = Invoke-WebRequest -Uri "https://resume2interview.com" -UseBasicParsing
if ($html.Content -match 'src="(/assets/index-[^"]+\.js)"') {
    Write-Host "Current bundle: $($Matches[1])"
}

# Railway - Check logs
# (View in Railway dashboard → Logs tab)
```

### Check Database
```powershell
# Railway dashboard → PostgreSQL → Data
# - Click "Data" tab
# - Select table to view
# - Check for records
```

---

## 📋 Common Issues

### Issue 1: Analytics 401 Unauthorized

**Symptom**:
- Analytics dashboard shows "Failed to load analytics data"
- Browser console shows: `401 Unauthorized` errors
- Password entered correctly

**Causes**:
1. Analytics password mismatch between frontend and backend
2. Wrong password in environment variables
3. CORS headers not allowing `X-Analytics-Password` header
4. Password contains special characters causing encoding issues

**Diagnosis**:
```powershell
# Test authentication directly
$backendUrl = "https://[railway-url].up.railway.app"
$password = "YourPassword"  # Use actual password
$headers = @{ 'X-Analytics-Password' = $password }

try {
    $response = Invoke-RestMethod -Uri "$backendUrl/api/analytics/usage-stats" -Headers $headers
    Write-Host "✅ Password works: $($response.success)"
} catch {
    Write-Host "❌ Error: $($_.Exception.Response.StatusCode.value__)"
}

# Check what backend expects
Invoke-RestMethod -Uri "$backendUrl/debug/password-check" -Headers $headers
```

**Solutions**:

**Solution A: Verify Environment Variable**
1. Railway dashboard → Service → Variables
2. Check `ANALYTICS_PASSWORD` value
3. Ensure no extra spaces or quotes
4. Must match exactly (case-sensitive)

**Solution B: Check CORS Headers**
```python
# In backend main.py, verify:
allow_headers = [
    "Content-Type",
    "X-Analytics-Password",  # ← Must be present
    ...
]
```

**Solution C: Check Frontend Code**
```typescript
// In Analytics.tsx, verify:
const headers = {
  'X-Analytics-Password': password  // ← Check header name exactly
};
```

**Solution D: Password Special Characters**
- Avoid quotes in password: `ANALYTICS_PASSWORD=MyPass123` (not `"MyPass123"`)
- Avoid spaces
- Stick to alphanumeric + basic symbols (@, #, !, %, -)

**Prevention**:
- Use debug endpoint: `/debug/password-check`
- Test password authentication before deploying
- Document actual password in secure vault

---

### Issue 2: Vercel Proxy Failure

**Symptom**:
- API calls return HTML instead of JSON
- Browser shows 200 OK but data is wrong
- HAR file shows Vercel returning frontend HTML for API calls

**Cause**:
- **Vercel free plan does NOT support external URL rewrites**
- Proxy configuration ignored on free tier
- API calls proxied through Vercel failing silently

**Diagnosis**:
```powershell
# Check if API call returns HTML
$response = Invoke-WebRequest -Uri "https://resume2interview.com/api/analytics/usage-stats" -UseBasicParsing
if($response.Content -match "<!doctype html>") {
    Write-Host "❌ Receiving HTML instead of JSON - Proxy not working"
}
```

**Solution**:
**Do NOT use Vercel proxy. Call Railway backend directly.**

```typescript
// File: Analytics.tsx
// WRONG (doesn't work on free plan):
const backendUrl = '/api';  // Tries to proxy through Vercel

// CORRECT:
const backendUrl = 'https://[railway-url].up.railway.app';
```

Update frontend code:
```typescript
const backendUrl = 'https://graceful-exploration-production.up.railway.app';

const [currentResponse, historyResponse, appResponse] = await Promise.all([
  fetch(`${backendUrl}/api/analytics/usage-stats`, { headers }),
  fetch(`${backendUrl}/api/analytics/usage-logs?days=7&limit=50`, { headers }),
  fetch(`${backendUrl}/api/analytics/application-stats?days=30`, { headers })
]);
```

**Prevention**:
- If on Vercel free plan, always call backend directly
- If upgrading to Vercel Pro, proxy will work
- Test in staging before production

---

### Issue 3: Railway Deployment Failure

**Symptom**:
- Railway build fails with "No such file or directory"
- Healthcheck timeouts
- Service won't start

**Causes**:
1. `railway.toml` conflicts with auto-detection
2. Wrong root directory
3. Missing dependencies in `requirements.txt`
4. Port binding issues

**Diagnosis**:
```bash
# Check Railway logs (in dashboard):
# Look for:
# - "No such file or directory"
# - "cd: can't cd to /app/01-Code/backend"
# - "Module not found"
```

**Solutions**:

**Solution A: Remove railway.toml (Recommended)**
```bash
# If railway.toml exists, remove it
git rm railway.toml
git commit -m "Remove railway.toml - let Railway auto-detect"
git push origin main
```

Railway auto-detection is BETTER than manual configuration.

**Solution B: Fix Root Directory**
1. Railway dashboard → Service Settings
2. Root Directory: Leave EMPTY or set to `/01-Code/backend`
3. Do NOT include `cd` commands in Start Command

**Solution C: Verify Dependencies**
```bash
# Ensure all packages in requirements.txt
cd 01-Code/backend
pip freeze > requirements-current.txt

# Compare with requirements.txt
# Add missing packages
```

**Solution D: Fix Port Binding**
```python
# Start command must use Railway's $PORT
# In Railway dashboard:
Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT

# NOT:
# uvicorn main:app --port 8000  ← Will fail
```

**Prevention**:
- Don't use `railway.toml` unless necessary
- Let Railway auto-detect configuration
- Test deployments in staging first

---

### Issue 4: Application Records Not Saving

**Symptom**:
- Resume analysis works
- Database shows 0 applications
- Analytics dashboard empty

**Cause**:
- `createApplication` parameter defaults to `false`
- Frontend not passing `true` to enable tracking

**Diagnosis**:
```powershell
# Check database
$response = Invoke-RestMethod -Uri "[backend-url]/v2/applications/?limit=10"
Write-Host "Total applications: $($response.data.total)"

# Should show > 0 after uploading resumes
# If 0: Application tracking not enabled
```

**Solution**:
Update ResultsPage.tsx:
```typescript
// File: 01-Code/frontend/src/pages/ResultsPage.tsx

// BEFORE (broken):
const [gapData, atsData] = await Promise.all([
  api.getGapAnalysis(resumeId, jdId),  // ← Missing createApplication parameter
  api.getATSScore(resumeId, jdId),
]);

// AFTER (fixed):
const [gapData, atsData] = await Promise.all([
  api.getGapAnalysis(resumeId, jdId, undefined, true),  // ← Enable tracking
  api.getATSScore(resumeId, jdId),
]);
```

**Verification**:
```powershell
# After fix, upload new resume
# Check database again:
$response = Invoke-RestMethod -Uri "[backend-url]/v2/applications/?limit=10"
Write-Host "Total applications: $($response.data.total)"
# Should now show 1 or more
```

**Prevention**:
- Always pass `createApplication: true` in production
- Add automated test for database persistence
- Monitor application count after deployment

---

### Issue 5: Vercel Auto-Deploy Not Triggering

**Symptom**:
- Git push succeeds
- No new deployment in Vercel dashboard
- Webhook not firing

**Causes**:
1. Git repository mismatch
2. Wrong branch configured
3. Vercel CLI linked to different project
4. Auto-deploy disabled in settings

**Diagnosis**:
```powershell
# Check local Vercel config
cd 01-Code/frontend
Get-Content .vercel\project.json | ConvertFrom-Json

# Check if projectName matches dashboard project
# If mismatch: This is the problem
```

**Solutions**:

**Solution A: Verify Git Connection**
1. Vercel dashboard → Settings → Git
2. Check "Connected Git Repository"
3. Should show: `jaysibi/resume2interview`
4. If wrong or missing: Disconnect and reconnect

**Solution B: Fix Project Linking**
```powershell
cd 01-Code/frontend
rm -r .vercel  # Remove old config
vercel link  # Re-link to correct project
```

**Solution C: Check Branch Configuration**
1. Vercel dashboard → Settings → Git
2. Production Branch: Should be `main`
3. If wrong: Update to correct branch

**Solution D: Manual Deploy (Workaround)**
```powershell
cd 01-Code/frontend
vercel --prod --yes
```

**Prevention**:
- Document which project CLI is linked to
- For production: Disable auto-deploy (manual only)
- Test git push triggers deployment in staging

---

### Issue 6: Frontend Deployment Not Updating

**Symptom**:
- Deployment succeeds in Vercel
- Site still shows old version
- Bundle hash unchanged

**Causes**:
1. CDN cache not invalidated
2. Browser cache
3. Deployment went to wrong environment

**Diagnosis**:
```powershell
# Check current bundle
$html = Invoke-WebRequest -Uri "https://resume2interview.com" -UseBasicParsing
if ($html.Content -match 'src="(/assets/index-([^"]+)\.js)"') {
    Write-Host "Bundle: $($Matches[1])"
}

# Compare to previous bundle hash
# If same: Deployment didn't update
```

**Solutions**:

**Solution A: Clear CDN Cache**
1. Vercel dashboard → Deployments
2. Find latest deployment
3. Click "..." menu → "Redeploy"
4. Check "Clear cache" if option available

**Solution B: Hard Refresh Browser**
- Windows: `Ctrl + Shift + R`
- Mac: `Cmd + Shift + R`
- This bypasses browser cache

**Solution C: Verify Deployment Environment**
```powershell
# Check Vercel dashboard
# - Ensure deployment is marked "Production"
# - Not just "Preview"
# - Check deployment URL matches domain
```

**Solution D: Wait for DNS Propagation**
- DNS changes take 5-10 minutes
- CDN takes 1-2 minutes to reflect changes
- Be patient after deployment

**Prevention**:
- Always verify bundle hash after deployment
- Use incognito/private browsing for testing
- Document expected bundle hash in deployment notes

---

### Issue 7: Database Connection Errors

**Symptom**:
- Backend starts but can't query database
- Logs show: "Connection refused" or "No route to host"
- API calls fail with 500 errors

**Causes**:
1. Wrong DATABASE_URL
2. Database not started
3. Network/firewall issues
4. Database credentials expired

**Diagnosis**:
```powershell
# Check via Railway dashboard
# Navigate to: PostgreSQL service → Status
# Should be: "Running" (green)

# Check DATABASE_URL exists
# Navigate to: Backend service → Variables
# Verify DATABASE_URL is set
```

**Solutions**:

**Solution A: Restart Database**
1. Railway dashboard → PostgreSQL
2. Click "Restart"
3. Wait for status: Running
4. Backend will auto-reconnect

**Solution B: Verify DATABASE_URL**
```python
# Check environment variable format:
# Should look like:
# postgresql://postgres:PASSWORD@HOST:PORT/railway

# In Railway dashboard → Backend → Variables
# DATABASE_URL should be auto-injected (green icon)
```

**Solution C: Check Database Service Linking**
1. Railway dashboard → Project → Services
2. Backend service must be in same project as PostgreSQL
3. If not linked: Add PostgreSQL to project

**Solution D: Manual Connection Test**
```bash
# In Railway dashboard Shell (PostgreSQL service):
psql $DATABASE_URL

# Should connect successfully
# Run: \dt to list tables
```

**Prevention**:
- Always create database BEFORE deploying backend
- Never manually edit DATABASE_URL (let Railway inject it)
- Monitor database status after deployments

---

### Issue 8: OpenAI API Failures

**Symptom**:
- Resume analysis hangs or fails
- Error: "OpenAI API error"
- 500 errors from `/gap-analysis` endpoint

**Causes**:
1. Invalid API key
2. API key quota exceeded
3. OpenAI service outage
4. Rate limiting

**Diagnosis**:
```powershell
# Check backend logs in Railway
# Look for:
# - "OpenAI API error: 401"  → Invalid key
# - "OpenAI API error: 429"  → Rate limit
# - "OpenAI API error: 503"  → Service down

# Test API key directly:
$apiKey = "[YOUR_KEY]"
$headers = @{
    'Authorization' = "Bearer $apiKey"
    'Content-Type' = 'application/json'
}
$body = @{
    model = "gpt-3.5-turbo"
    messages = @(
        @{ role = "user"; content = "Test" }
    )
} | ConvertTo-Json

Invoke-RestMethod -Uri "https://api.openai.com/v1/chat/completions" -Method Post -Headers $headers -Body $body
```

**Solutions**:

**Solution A: Verify API Key**
1. Railway dashboard → Backend → Variables
2. Check `OPENAI_API_KEY` value
3. Verify it starts with `sk-proj-` or `sk-`
4. Regenerate key if invalid (https://platform.openai.com/api-keys)

**Solution B: Check Quota**
1. Visit https://platform.openai.com/account/usage
2. Check current usage vs limits
3. If exceeded: Add credits or wait for reset
4. Consider upgrading OpenAI plan

**Solution C: Handle Rate Limits**
```python
# In backend code, add retry logic:
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
def call_openai_api():
    # API call here
    pass
```

**Solution D: Use Different Model**
```python
# If gpt-4 is rate-limited, fall back to gpt-3.5-turbo
# Check current model in backend code
# Consider using faster, cheaper model for high traffic
```

**Prevention**:
- Monitor OpenAI usage dashboard daily
- Set up billing alerts in OpenAI account
- Implement request caching to reduce API calls
- Add retry logic with exponential backoff

---

### Issue 9: CORS Errors in Browser

**Symptom**:
- Browser console: "CORS policy: No 'Access-Control-Allow-Origin'"
- Fetch requests fail
- Network tab shows failed requests

**Causes**:
1. Wrong CORS_ORIGINS configuration
2. Missing origin in backend allow list
3. Trying to access from unexpected domain

**Diagnosis**:
```javascript
// In browser console (F12):
fetch('https://[backend-url]/api/analytics/usage-stats')
  .then(r => console.log('Success'))
  .catch(e => console.error('CORS Error:', e))

// If fails: CORS misconfigured
```

**Solutions**:

**Solution A: Check CORS_ORIGINS Variable**
```bash
# Railway dashboard → Backend → Variables
# CORS_ORIGINS should include production domain:
CORS_ORIGINS=https://resume2interview.com

# NOT:
# CORS_ORIGINS=https://resume2interview-staging.vercel.app  ← Staging URL
# CORS_ORIGINS=http://localhost:5173  ← Dev URL
```

**Solution B: Multiple Origins (Dev + Prod)**
```bash
# For local development + production:
CORS_ORIGINS=https://resume2interview.com,http://localhost:5173

# Comma-separated, no spaces
```

**Solution C: Verify Backend Code**
```python
# File: main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # ← Should include your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=[
        "Content-Type",
        "X-Analytics-Password",
    ],
)
```

**Prevention**:
- Always include production domain in CORS_ORIGINS
- Test cross-origin requests before deployment
- Never use `allow_origins=["*"]` in production

---

### Issue 10: SSL Certificate Problems

**Symptom**:
- Browser shows "Not secure" warning
- Certificate expired or invalid
- Mixed content warnings

**Causes**:
1. SSL certificate not provisioned by Vercel
2. DNS not pointing to Vercel
3. Certificate pending verification
4. Mixed HTTP/HTTPS content

**Diagnosis**:
```powershell
# Check certificate
$response = Invoke-WebRequest -Uri "https://resume2interview.com"
# If fails with SSL error: Certificate issue

# Check DNS
nslookup resume2interview.com
# Should return Vercel IP
```

**Solutions**:

**Solution A: Wait for Certificate Provisioning**
1. Vercel dashboard → Settings → Domains
2. Check certificate status
3. If "Pending": Wait 5-10 minutes
4. If "Failed": Check DNS configuration

**Solution B: Verify DNS**
1. GoDaddy → Domain → DNS
2. A Record → Value: Vercel IP (76.76.21.21)
3. CNAME Record → www → cname.vercel-dns.com
4. Save changes, wait for propagation

**Solution C: Force Certificate Renewal**
1. Vercel dashboard → Settings → Domains
2. Click domain → "Refresh"
3. Vercel will re-provision certificate

**Solution D: Fix Mixed Content**
```typescript
// Ensure all resources use HTTPS:
// WRONG:
const imageUrl = 'http://example.com/image.jpg';

// CORRECT:
const imageUrl = 'https://example.com/image.jpg';
```

**Prevention**:
- Always use HTTPS URLs in code
- Let Vercel auto-manage certificates
- Monitor certificate expiry (auto-renewed, but verify)

---

## 🔧 Advanced Troubleshooting

### Debug Endpoints (Use in Staging Only)

**Check Database Configuration**:
```
GET /debug/db-config
```
Returns database connection details and table list.

**Check Environment Variables**:
```
GET /debug/env-check
```
Returns which env vars are set (values hidden).

**Check Analytics Password**:
```
GET /debug/password-check
Headers: X-Analytics-Password: yourpassword
```
Returns whether password matches.

⚠️ **Disable these endpoints in production** or require admin authentication.

---

## 📞 Escalation Path

### When to Escalate

**Immediate Escalation** (Critical Issues):
- Production down > 5 minutes
- Database data loss
- Security breach suspected
- OpenAI API key leaked

**2-Hour Escalation** (High Priority):
- Major feature broken (resume analysis)
- High error rate (> 10%)
- Performance degradation (> 5s load times)

**Next Business Day** (Medium Priority):
- Minor UI issues
- Analytics export broken
- Mobile layout issues

### Who to Contact

1. **Technical Lead**: First point of contact
2. **DevOps Engineer**: Infrastructure issues
3. **On-Call Engineer**: After-hours emergencies
4. **Security Team**: Security incidents

---

## 📝 Post-Incident Process

After resolving any issue:

1. **Document the incident**:
   - What happened
   - When it happened
   - How it was detected
   - How it was fixed
   - Time to resolution

2. **Update this guide**:
   - Add issue to Common Issues section
   - Document solution steps
   - Add prevention measures

3. **Schedule post-mortem** (for critical issues):
   - Root cause analysis
   - Prevention strategies
   - Process improvements

4. **Update monitoring**:
   - Add alerts for similar issues
   - Improve detection time
   - Automate fixes if possible

---

## 🎓 Lessons Learned

Based on staging deployment experience:

1. **Always test in staging first** - Caught 90% of issues
2. **Vercel free plan limitations** - Know what features are available
3. **Railway auto-detection is better** - Don't fight it with railway.toml
4. **Application tracking must be explicit** - Default is false for safety
5. **Project naming matters** - CLI and dashboard must match
6. **Manual deploys for production** - Auto-deploy too risky

These issues are now documented and preventable! 🎉
