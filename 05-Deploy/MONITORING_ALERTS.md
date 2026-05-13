# Monitoring & Alerting - Resume2Interview

This document outlines monitoring setup, alerting configuration, and operational dashboards for production.

---

## 📊 Monitoring Overview

### What We Monitor

| Category | Metrics | Tools | Alert Threshold |
|----------|---------|-------|-----------------|
| **Backend Health** | Response time, error rate, uptime | Railway Logs | >5% error rate |
| **Frontend Health** | Page load time, JS errors, uptime | Vercel Analytics | >3s load time |
| **Database** | Query time, connections, storage | Railway PostgreSQL | >80% capacity |
| **API Usage** | OpenAI API calls, tokens, costs | OpenAI Dashboard | >$50/day |
| **Business Metrics** | Resume uploads, analyses, exports | Custom Dashboard | N/A (informational) |

---

## 🚨 Alerting Strategy

### Alert Severity Levels

**P0 - Critical** (Immediate Response):
- Service completely down
- Database unavailable
- 100% error rate
- Data loss detected

**P1 - High** (Response within 30 minutes):
- Error rate >25%
- Response time >5 seconds
- Database connections >90%
- OpenAI API failures

**P2 - Medium** (Response within 2 hours):
- Error rate >10%
- Response time >3 seconds
- Database storage >80%
- High API costs

**P3 - Low** (Review next business day):
- Elevated error rate (5-10%)
- Slow queries
- Increased costs
- Usage pattern anomalies

---

## 🔧 Railway Monitoring

### Backend Service Monitoring

**Access**: https://railway.app → Project → Backend Service → Observability

**Key Metrics**:

1. **CPU Usage**:
   - Target: <50% average
   - Alert: >80% for 5 minutes
   - Action: Scale up or optimize code

2. **Memory Usage**:
   - Target: <75% of allocated
   - Alert: >90% for 5 minutes
   - Action: Increase memory or find memory leaks

3. **Request Rate**:
   - Monitor: Requests per minute
   - Baseline: [Establish after 1 week]
   - Alert: Sudden spike (>3x baseline)

4. **Response Time**:
   - Target: <500ms average
   - Warning: >1s for 10% of requests
   - Critical: >5s for any request

5. **Error Rate**:
   - Target: <1%
   - Warning: 1-5%
   - Critical: >5%

**View Metrics**:
```powershell
# Railway Dashboard → Service → Metrics tab
# Shows:
# - CPU/Memory over time (24h/7d/30d)
# - Request rate graph
# - Deployment history with performance impact
```

---

### Railway Logs

**Access**: Railway Dashboard → Backend Service → Logs

**Log Retention**: Last 7 days (free plan) or 30 days (paid)

**Key Log Patterns to Monitor**:

**Successful resume analysis**:
```
INFO: POST /api/analyze-resume - Status: 200 - Duration: 1.2s
INFO: OpenAI API call successful - Tokens: 1200
INFO: Application saved to database - ID: abc123
```

**Error patterns**:
```
ERROR: Database connection failed - psycopg2.OperationalError
ERROR: OpenAI API rate limit exceeded - Status: 429
ERROR: Resume parsing failed - PDF corrupt or password protected
WARNING: Slow query detected - Duration: 3.5s
```

**Search logs**:
```powershell
# In Railway Logs → Search box:
# - "ERROR" → Find all errors
# - "POST /api/analyze" → Track resume analyses
# - "Database" → Database-related logs
# - "429" → Rate limit errors
```

**Export logs** (for analysis):
```powershell
# Railway CLI
railway logs --environment production > logs-$(Get-Date -Format 'yyyy-MM-dd').txt
```

---

### Database Monitoring

**Access**: Railway Dashboard → PostgreSQL Service → Observability

**Metrics to Track**:

1. **Storage Usage**:
   - Target: <80% capacity
   - Alert: >85%
   - Action: Clean old data or upgrade storage

2. **Connection Count**:
   - Target: <50 connections
   - Alert: >90 connections
   - Action: Check for connection leaks

3. **Query Performance**:
   - Slow queries: >1 second
   - Monitor via logs
   - Optimize with indexes

**Database Health Check**:
```sql
-- Run in Railway PostgreSQL → Data tab → Query

-- Check table sizes
SELECT 
  schemaname,
  tablename,
  pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- Check connection count
SELECT count(*) FROM pg_stat_activity;

-- Check slow queries (last hour)
SELECT query, calls, mean_exec_time, max_exec_time
FROM pg_stat_statements
WHERE mean_exec_time > 1000  -- >1 second
ORDER BY mean_exec_time DESC
LIMIT 10;

-- Check database size
SELECT pg_size_pretty(pg_database_size('railway'));
```

**Automated Monitoring Script**:
```python
# File: 01-Code/backend/scripts/check_db_health.py
import psycopg2
import os
from datetime import datetime

def check_database_health():
    conn = psycopg2.connect(os.getenv('DATABASE_URL'))
    cursor = conn.cursor()
    
    # Check storage
    cursor.execute("SELECT pg_database_size('railway');")
    size_bytes = cursor.fetchone()[0]
    size_gb = size_bytes / (1024**3)
    
    # Check connections
    cursor.execute("SELECT count(*) FROM pg_stat_activity;")
    connections = cursor.fetchone()[0]
    
    # Check slow queries (requires pg_stat_statements extension)
    cursor.execute("""
        SELECT count(*) FROM pg_stat_statements 
        WHERE mean_exec_time > 1000;
    """)
    slow_queries = cursor.fetchone()[0]
    
    print(f"[{datetime.now()}] Database Health:")
    print(f"  Size: {size_gb:.2f} GB")
    print(f"  Connections: {connections}")
    print(f"  Slow queries (last period): {slow_queries}")
    
    # Alerts
    if size_gb > 8:  # Assuming 10GB limit
        print("  ⚠️  WARNING: Database >80% capacity!")
    if connections > 90:
        print("  ⚠️  WARNING: High connection count!")
    if slow_queries > 10:
        print("  ⚠️  WARNING: Many slow queries detected!")
    
    cursor.close()
    conn.close()

if __name__ == '__main__':
    check_database_health()
```

Run manually or schedule:
```powershell
# Run once
python 01-Code/backend/scripts/check_db_health.py

# Schedule (Windows Task Scheduler or cron)
# Every 6 hours
```

---

## 📈 Vercel Monitoring

### Frontend Analytics

**Access**: https://vercel.com → Project → Analytics

**Key Metrics** (Vercel Analytics):

1. **Page Load Time**:
   - Target: <2 seconds (p95)
   - Warning: >3 seconds
   - Critical: >5 seconds

2. **Real User Monitoring (RUM)**:
   - First Contentful Paint (FCP): <1.8s
   - Largest Contentful Paint (LCP): <2.5s
   - Cumulative Layout Shift (CLS): <0.1
   - Time to Interactive (TTI): <3.8s

3. **Visitor Metrics**:
   - Unique visitors per day
   - Page views
   - Session duration
   - Bounce rate

**Enable Web Vitals**:
```typescript
// File: 01-Code/frontend/src/main.tsx
import { getCLS, getFID, getFCP, getLCP, getTTFB } from 'web-vitals';

function sendToAnalytics(metric: any) {
  // Send to your analytics endpoint
  console.log(metric);
}

getCLS(sendToAnalytics);
getFID(sendToAnalytics);
getFCP(sendToAnalytics);
getLCP(sendToAnalytics);
getTTFB(sendToAnalytics);
```

---

### Vercel Logs

**Access**: Vercel Dashboard → Project → Logs

**Log Types**:
- **Build Logs**: Deployment build output
- **Function Logs**: Serverless function execution (if any)
- **Edge Logs**: CDN and routing logs

**Key Events to Monitor**:
```
[Build] ✓ Build completed successfully (45s)
[Deploy] ✓ Deployment ready at resume2interview.com
[Error] Build failed: npm install error
[Warning] Large bundle size detected: index.js (2.5MB)
```

**Download logs**:
```powershell
# Vercel CLI
vercel logs resume2interview-production --follow
```

---

## 🎯 Custom Application Metrics

### Analytics Dashboard

**Built-in monitoring**: Resume2Interview has a custom analytics dashboard

**Access**: https://resume2interview.com/analytics
- Username: `admin`
- Password: [ANALYTICS_PASSWORD from environment variables]

**Metrics Available**:

1. **Usage Statistics**:
   - Total resumes analyzed
   - Successful analyses
   - Failed analyses
   - Average analysis time

2. **User Behavior**:
   - Uploads per day/week/month
   - Peak usage hours
   - Return user rate

3. **Performance**:
   - Average processing time
   - OpenAI API response time
   - Database query time

4. **Error Tracking**:
   - Error types and frequency
   - Failed uploads
   - API failures

**Excel Export**:
- Click "Export to Excel" on analytics page
- Includes all application records
- Use for deeper analysis in Excel/Power BI

---

### Health Check Endpoint

**Endpoint**: `https://[backend-url]/health`

**Response** (healthy):
```json
{
  "status": "healthy",
  "timestamp": "2024-05-12T10:30:00Z",
  "database": "connected",
  "openai_api": "available",
  "version": "1.2.0"
}
```

**Response** (unhealthy):
```json
{
  "status": "unhealthy",
  "timestamp": "2024-05-12T10:30:00Z",
  "database": "connection_failed",
  "openai_api": "available",
  "version": "1.2.0",
  "error": "psycopg2.OperationalError: connection refused"
}
```

**Monitor with PowerShell**:
```powershell
# Single check
$response = Invoke-RestMethod -Uri "https://[backend-url]/health"
if ($response.status -eq "healthy") {
    Write-Host "✅ Backend is healthy" -ForegroundColor Green
} else {
    Write-Host "❌ Backend is unhealthy: $($response.error)" -ForegroundColor Red
}

# Continuous monitoring (every 5 minutes)
while ($true) {
    try {
        $response = Invoke-RestMethod -Uri "https://[backend-url]/health"
        $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        
        if ($response.status -eq "healthy") {
            Write-Host "[$timestamp] ✅ Status: Healthy" -ForegroundColor Green
        } else {
            Write-Host "[$timestamp] ❌ Status: Unhealthy - $($response.error)" -ForegroundColor Red
            # Send alert (implement notification logic)
        }
    } catch {
        Write-Host "[$timestamp] ❌ Health check failed: $_" -ForegroundColor Red
    }
    
    Start-Sleep -Seconds 300  # 5 minutes
}
```

---

## 💰 OpenAI API Monitoring

### Cost Tracking

**Access**: https://platform.openai.com/usage

**Key Metrics**:

1. **Daily Usage**:
   - API calls per day
   - Tokens consumed
   - Cost per day

2. **Rate Limits**:
   - Requests per minute (RPM)
   - Tokens per minute (TPM)
   - Current usage vs limits

**Set Budget Alerts**:
1. Go to https://platform.openai.com/account/billing/limits
2. Set hard limit (e.g., $100/month)
3. Set soft limit (e.g., $50/month) for email alert
4. Enable email notifications

**Monitor usage**:
```powershell
# Check OpenAI usage via API
$headers = @{
    "Authorization" = "Bearer $env:OPENAI_API_KEY"
}

$response = Invoke-RestMethod -Uri "https://api.openai.com/v1/usage" -Headers $headers
$response | ConvertTo-Json
```

**Cost Calculation**:
- GPT-4: $0.03 per 1K prompt tokens, $0.06 per 1K completion tokens
- GPT-3.5-turbo: $0.0015 per 1K prompt tokens, $0.002 per 1K completion tokens
- Average resume analysis: ~2000 tokens = $0.06-$0.18 per analysis

---

## 🔔 Alert Configuration

### Railway Alerts (Built-in)

**Setup**:
1. Railway Dashboard → Project → Settings → Notifications
2. Enable notifications for:
   - Deployment failures
   - Service crashes
   - Resource limit warnings
3. Add notification channels:
   - Email: your-email@example.com
   - Webhook: [Slack webhook URL]

---

### Slack Notifications

**Setup Slack Webhook**:
1. Go to https://api.slack.com/apps
2. Create new app → "Resume2Interview Monitoring"
3. Add "Incoming Webhooks"
4. Activate webhooks → Add webhook to workspace
5. Copy webhook URL

**Send alert to Slack**:
```powershell
# PowerShell function to send Slack alert
function Send-SlackAlert {
    param(
        [string]$Message,
        [string]$Severity = "info"  # info, warning, error, critical
    )
    
    $webhookUrl = "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
    
    $color = switch ($Severity) {
        "info" { "#36a64f" }      # Green
        "warning" { "#ff9900" }   # Orange
        "error" { "#ff0000" }     # Red
        "critical" { "#8b0000" }  # Dark Red
        default { "#808080" }     # Gray
    }
    
    $emoji = switch ($Severity) {
        "info" { ":white_check_mark:" }
        "warning" { ":warning:" }
        "error" { ":x:" }
        "critical" { ":rotating_light:" }
        default { ":information_source:" }
    }
    
    $payload = @{
        text = "$emoji Resume2Interview Alert"
        attachments = @(
            @{
                color = $color
                text = $Message
                footer = "Resume2Interview Monitoring"
                ts = [int][double]::Parse((Get-Date -UFormat %s))
            }
        )
    } | ConvertTo-Json -Depth 4
    
    Invoke-RestMethod -Uri $webhookUrl -Method Post -Body $payload -ContentType 'application/json'
}

# Usage examples:
Send-SlackAlert -Message "Production deployment completed successfully" -Severity "info"
Send-SlackAlert -Message "Error rate exceeded 10% in last 5 minutes" -Severity "warning"
Send-SlackAlert -Message "Backend service is down!" -Severity "critical"
```

---

### Email Alerts

**Setup SMTP** (for custom alerts):
```python
# File: 01-Code/backend/scripts/send_email_alert.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email_alert(subject, body, to_email):
    from_email = "alerts@resume2interview.com"
    smtp_server = "smtp.gmail.com"  # or your SMTP server
    smtp_port = 587
    smtp_user = "your-email@gmail.com"
    smtp_password = "your-app-password"
    
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = f"[Resume2Interview] {subject}"
    
    msg.attach(MIMEText(body, 'html'))
    
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_user, smtp_password)
    server.send_message(msg)
    server.quit()

# Usage:
if error_rate > 0.10:
    send_email_alert(
        subject="High Error Rate Detected",
        body="Error rate exceeded 10% threshold<br>Current: 12.5%<br>Action required.",
        to_email="oncall@example.com"
    )
```

---

## 🛠️ Monitoring Setup Checklist

### Initial Setup (Do Once)

**Railway**:
- [ ] Enable deployment notifications
- [ ] Configure webhook to Slack
- [ ] Set resource usage alerts
- [ ] Review default log retention

**Vercel**:
- [ ] Enable Vercel Analytics (free tier)
- [ ] Enable deployment notifications
- [ ] Configure custom domain monitoring
- [ ] Review performance budgets

**OpenAI**:
- [ ] Set hard spending limit
- [ ] Set soft spending alert
- [ ] Enable email notifications
- [ ] Review usage weekly

**Custom**:
- [ ] Test analytics dashboard access
- [ ] Verify Excel export functionality
- [ ] Set up health check monitoring script
- [ ] Configure Slack webhooks

---

### Daily Monitoring Tasks

**Morning Check** (5 minutes):
- [ ] Review Railway dashboard for errors
- [ ] Check Vercel analytics for unusual traffic
- [ ] Verify health check endpoint responds
- [ ] Scan logs for ERROR/CRITICAL messages

**Actions**:
```powershell
# Quick morning health check script
Write-Host "🌅 Daily Health Check - $(Get-Date)" -ForegroundColor Cyan

# 1. Backend health
try {
    $health = Invoke-RestMethod -Uri "https://[backend-url]/health"
    Write-Host "✅ Backend: $($health.status)" -ForegroundColor Green
} catch {
    Write-Host "❌ Backend: FAILED" -ForegroundColor Red
}

# 2. Frontend health
try {
    $frontend = Invoke-WebRequest -Uri "https://resume2interview.com" -Method Head
    Write-Host "✅ Frontend: HTTP $($frontend.StatusCode)" -ForegroundColor Green
} catch {
    Write-Host "❌ Frontend: FAILED" -ForegroundColor Red
}

# 3. Check for recent errors (last 24h in Railway logs)
Write-Host "📋 Check Railway logs for errors in last 24h"

# 4. Check OpenAI usage
Write-Host "💰 Review OpenAI usage at: https://platform.openai.com/usage"
```

---

### Weekly Monitoring Tasks

**Weekly Review** (30 minutes):
- [ ] Review error trends (types, frequency)
- [ ] Check database growth rate
- [ ] Analyze performance trends (response times)
- [ ] Review OpenAI API costs
- [ ] Check storage usage (Railway, Vercel)
- [ ] Review user analytics (uploads, exports)

**Generate Weekly Report**:
```powershell
# Weekly report script
$startDate = (Get-Date).AddDays(-7).ToString("yyyy-MM-dd")
$endDate = (Get-Date).ToString("yyyy-MM-dd")

Write-Host "📊 Weekly Report: $startDate to $endDate" -ForegroundColor Cyan

# Get data from analytics dashboard
Write-Host "`n1. Export analytics data from: https://resume2interview.com/analytics"
Write-Host "2. Download Railway logs for analysis"
Write-Host "3. Check OpenAI usage dashboard"

# Manual analysis points:
Write-Host "`n📈 Analysis Points:"
Write-Host "  - Total resumes analyzed"
Write-Host "  - Success rate"
Write-Host "  - Average processing time"
Write-Host "  - Error count and types"
Write-Host "  - Database size growth"
Write-Host "  - OpenAI API costs"
Write-Host "  - Peak usage times"
```

---

## 📉 Creating Dashboards

### Custom Monitoring Dashboard

**Option 1: Grafana** (Advanced):
- Integrate Railway metrics
- Combine with custom application metrics
- Set up alerting rules
- Create visualizations

**Option 2: Simple Google Sheets Dashboard**:
1. Export analytics data to Excel weekly
2. Import to Google Sheets
3. Create charts:
   - Line chart: Resumes analyzed over time
   - Bar chart: Success vs failed analyses
   - Pie chart: Error types distribution
4. Share with team

**Option 3: Power BI** (If available):
1. Connect to PostgreSQL database directly
2. Create Power BI dashboard with:
   - KPIs: Total analyses, success rate, avg time
   - Time series: Usage trends
   - Geo map: User locations (if collected)
   - Error analysis: Types and trends

---

## 🚦 Real-Time Monitoring

### Uptime Monitoring (External)

Use free uptime monitoring services:

**1. UptimeRobot** (https://uptimerobot.com):
- Free: 50 monitors, 5-minute checks
- Monitor: https://resume2interview.com
- Monitor: https://[backend-url]/health
- Alerts: Email, Slack, SMS

**Setup**:
1. Create account at https://uptimerobot.com
2. Add monitor → HTTP(s)
3. URL: https://resume2interview.com
4. Check interval: 5 minutes
5. Add alert contact (email)
6. Repeat for backend health endpoint

**2. Pingdom** (https://www.pingdom.com):
- Free trial: Real user monitoring
- Uptime checks
- Performance analysis

**3. StatusCake** (https://www.statuscake.com):
- Free: Uptime monitoring
- SSL certificate monitoring
- Page speed monitoring

---

## 🔍 Debugging Tools

### Log Analysis Tools

**1. Railway CLI**:
```powershell
# Install
npm install -g @railway/cli

# Login
railway login

# View logs
railway logs --environment production

# Follow logs in real-time
railway logs --environment production --follow

# Filter logs
railway logs --environment production | Select-String "ERROR"
```

**2. jq for JSON log parsing**:
```powershell
# Windows: Install jq
choco install jq

# Parse JSON logs
railway logs --json | jq '.[] | select(.level=="ERROR")'
```

---

## 📞 On-Call Procedures

### On-Call Rotation

**Coverage**:
- Primary: [Name, Phone, Slack]
- Secondary: [Name, Phone, Slack]
- Escalation: [Manager/Lead, Phone]

**Response Times**:
- P0 (Critical): Immediate acknowledgment, 15 min response
- P1 (High): 30 minutes
- P2 (Medium): 2 hours
- P3 (Low): Next business day

---

### Incident Response Checklist

**When alert received**:
1. [ ] Acknowledge alert (Slack/Email)
2. [ ] Check service status (Railway + Vercel dashboards)
3. [ ] Review recent deployments (any changes in last 2 hours?)
4. [ ] Check health endpoint
5. [ ] Review logs for errors
6. [ ] Determine severity (P0/P1/P2/P3)
7. [ ] Start incident timeline (note times)
8. [ ] Begin troubleshooting (see TROUBLESHOOTING.md)
9. [ ] Communicate status updates (every 15-30 min)
10. [ ] Resolve or escalate
11. [ ] Post-incident review (document what happened)

---

## 📚 Monitoring Resources

**Documentation**:
- Railway Observability: https://docs.railway.app/reference/observability
- Vercel Analytics: https://vercel.com/docs/analytics
- OpenAI Usage: https://platform.openai.com/docs/guides/production-best-practices/monitoring

**Tools**:
- Railway CLI: https://docs.railway.app/develop/cli
- Vercel CLI: https://vercel.com/docs/cli
- UptimeRobot: https://uptimerobot.com
- Slack API: https://api.slack.com

**Related Documents**:
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Issue resolution
- [ROLLBACK_PROCEDURE.md](ROLLBACK_PROCEDURE.md) - Emergency procedures
- [POST_DEPLOYMENT_VALIDATION.md](POST_DEPLOYMENT_VALIDATION.md) - Validation tests

---

## ✅ Next Steps

After reading this document:
1. [ ] Set up Railway notifications
2. [ ] Configure Vercel analytics
3. [ ] Set OpenAI spending limits
4. [ ] Create Slack webhook
5. [ ] Set up uptime monitoring (UptimeRobot)
6. [ ] Test health check endpoint
7. [ ] Verify analytics dashboard access
8. [ ] Schedule weekly review meeting
9. [ ] Designate on-call rotation
10. [ ] Create runbook for common incidents

**Questions?** See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) or contact DevOps team.
