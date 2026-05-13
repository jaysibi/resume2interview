# Environment Configuration - Resume2Interview

This document details all environment variables and configuration settings for each environment.

---

## 🌍 Environment Overview

| Environment | Frontend | Backend | Database | Purpose |
|------------|----------|---------|----------|---------|
| **Local** | localhost:5173 | localhost:8000 | SQLite/Local PostgreSQL | Development |
| **Staging** | resume2interview-staging.vercel.app | graceful-exploration-staging.up.railway.app | Railway PostgreSQL (staging) | Testing/QA |
| **Production** | resume2interview.com | [production-railway-url].up.railway.app | Railway PostgreSQL (production) | Live users |

---

## ⚙️ Backend Configuration (Railway)

### Common Variables (All Environments)

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DATABASE_URL` | ✅ Yes | Auto-injected | PostgreSQL connection string (Railway provides) |
| `OPENAI_API_KEY` | ✅ Yes | None | OpenAI API key for GPT analysis |
| `ANALYTICS_PASSWORD` | ✅ Yes | None | Password for `/analytics` dashboard |
| `CORS_ORIGINS` | ✅ Yes | None | Comma-separated allowed origins |
| `PORT` | No | 8080 | Port for FastAPI server (Railway auto-sets) |
| `ENVIRONMENT` | No | development | Environment name (development/staging/production) |

---

### Local Development Configuration

**Location**: `01-Code/backend/.env`

```bash
# Database (Option 1: SQLite)
DATABASE_URL=sqlite:///./resume_tailor.db

# Database (Option 2: Local PostgreSQL)
DATABASE_URL=postgresql://postgres:password@localhost:5432/resumetailor

# OpenAI API Key (Personal/Dev Key)
OPENAI_API_KEY=sk-proj-YOUR_DEV_KEY_HERE

# Analytics Password (Weak for dev)
ANALYTICS_PASSWORD=dev123

# CORS (Allow localhost)
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# Environment Identifier
ENVIRONMENT=development

# Port (Optional)
PORT=8000
```

**Setup instructions**:
```powershell
cd C:\Projects\ResumeTailor\01-Code\backend

# Create .env file
@"
DATABASE_URL=sqlite:///./resume_tailor.db
OPENAI_API_KEY=sk-proj-YOUR_KEY
ANALYTICS_PASSWORD=dev123
CORS_ORIGINS=http://localhost:5173
ENVIRONMENT=development
"@ | Out-File -FilePath .env -Encoding UTF8

# Install dependencies
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Start server
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

---

### Staging Configuration (Railway)

**Location**: Railway Dashboard → `graceful-exploration-staging` → Variables

```bash
# Database (Auto-injected by Railway PostgreSQL)
DATABASE_URL=postgresql://postgres:***@maglev.proxy.rlwy.net:22595/railway

# OpenAI API Key (Shared Test Key - Lower Rate Limits OK)
OPENAI_API_KEY=sk-proj-[STAGING_KEY]

# Analytics Password (Test Password - Document in team notes)
ANALYTICS_PASSWORD=Railwayismessy

# CORS (Staging domain + localhost for testing)
CORS_ORIGINS=https://resume2interview-staging.vercel.app,http://localhost:5173

# Environment
ENVIRONMENT=staging

# Port (Auto-set by Railway)
PORT=8080
```

**How to set**:
1. Go to https://railway.app
2. Select project → `graceful-exploration-staging`
3. Click "Variables" tab
4. Click "New Variable"
5. Enter name and value
6. Click "Add"
7. Deployment automatically redeploys with new variables

**Notes**:
- ✅ `DATABASE_URL` is auto-injected when PostgreSQL service added
- ⚠️ Staging password is intentionally weak for testing
- ⚠️ OpenAI key can have lower rate limits (for cost control)
- ✅ CORS includes localhost for local frontend testing

---

### Production Configuration (Railway)

**Location**: Railway Dashboard → `graceful-exploration-production` → Variables

```bash
# Database (Auto-injected by Railway PostgreSQL)
DATABASE_URL=postgresql://postgres:***@containers-us-west-###.railway.app:####/railway

# OpenAI API Key (Production Key - High Rate Limits)
OPENAI_API_KEY=sk-proj-[PRODUCTION_KEY]

# Analytics Password (STRONG PASSWORD - 16+ characters)
ANALYTICS_PASSWORD=[GENERATE_STRONG_PASSWORD]

# CORS (Production domain ONLY - NO localhost)
CORS_ORIGINS=https://resume2interview.com

# Environment
ENVIRONMENT=production

# Port (Auto-set by Railway)
PORT=8080
```

**How to set** (same as staging but different values):
1. Go to https://railway.app
2. Select project → `graceful-exploration-production`
3. Click "Variables" tab
4. Add each variable with production values

**Critical Security Requirements**:

✅ **ANALYTICS_PASSWORD**:
- Minimum 16 characters
- Mix of uppercase, lowercase, numbers, symbols
- Generate with: `openssl rand -base64 24`
- Example: `Pr0d$2024!SecureAnal#789XyZ`
- **NEVER use staging password**

✅ **OPENAI_API_KEY**:
- Separate key from staging/development
- Production-tier API key with high rate limits
- Monitor usage at https://platform.openai.com/usage
- Set up billing alerts

✅ **CORS_ORIGINS**:
- **ONLY** production domain: `https://resume2interview.com`
- **DO NOT** include:
  - ❌ staging URLs
  - ❌ localhost
  - ❌ development domains
  - ❌ wildcard (`*`)

✅ **DATABASE_URL**:
- Auto-injected by Railway (don't set manually)
- Separate database instance from staging
- Verify it's production database (not staging)

---

## 🌐 Frontend Configuration (Vercel)

### Environment Variables

**Frontend typically does NOT need environment variables** because:
- API URLs are hardcoded (not secret)
- No sensitive credentials in frontend
- Configuration via build-time settings

**If needed** (rare cases):
```bash
# Vercel Dashboard → Project → Settings → Environment Variables

# Example: Feature flags
VITE_FEATURE_ANALYTICS=true
VITE_FEATURE_EXPORT=true

# Example: API URL override (not recommended - use hardcoding)
VITE_API_URL=https://[backend-url].up.railway.app
```

**Note**: Vite exposes variables prefixed with `VITE_` to frontend code.

---

### Build Configuration

**Local Development**:
```json
// File: 01-Code/frontend/package.json
{
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  }
}
```

Run locally:
```powershell
cd C:\Projects\ResumeTailor\01-Code\frontend
npm install
npm run dev  # Starts on http://localhost:5173
```

---

**Staging Configuration (Vercel)**:

**Location**: Vercel Dashboard → `resume2interview-staging` → Settings

- **Root Directory**: `01-Code/frontend`
- **Framework**: Vite (auto-detected)
- **Build Command**: `npm run build`
- **Output Directory**: `dist`
- **Install Command**: `npm install`
- **Node Version**: 18.x or 20.x

**vercel.json** (in `01-Code/frontend/`):
```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "devCommand": "npm run dev",
  "installCommand": "npm install",
  "framework": "vite",
  "rewrites": [
    {
      "source": "/api/:path*",
      "destination": "https://graceful-exploration-staging.up.railway.app/api/:path*"
    },
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ],
  "headers": [
    {
      "source": "/assets/(.*)",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "public, max-age=31536000, immutable"
        }
      ]
    }
  ]
}
```

**Note**: Rewrites don't work on Vercel free plan (frontend calls backend directly).

---

**Production Configuration (Vercel)**:

**Location**: Vercel Dashboard → `resume2interview-production` → Settings

- **Root Directory**: `01-Code/frontend`
- **Framework**: Vite
- **Build Command**: `npm run build`
- **Output Directory**: `dist`
- **Custom Domain**: `resume2interview.com`

**Same vercel.json** - Update backend URL:
```json
{
  "rewrites": [
    {
      "source": "/api/:path*",
      "destination": "https://[production-railway-url].up.railway.app/api/:path*"
    }
    // ... rest same as staging
  ]
}
```

**Critical Code Changes for Production**:

Update backend URL in `Analytics.tsx`:
```typescript
// File: 01-Code/frontend/src/pages/Analytics.tsx
// Line: ~118

// STAGING:
const backendUrl = 'https://graceful-exploration-staging.up.railway.app';

// PRODUCTION (UPDATE THIS):
const backendUrl = 'https://[production-railway-url].up.railway.app';
```

---

## 🗄️ Database Configuration

### Local Database (SQLite)

**Configuration**:
```bash
DATABASE_URL=sqlite:///./resume_tailor.db
```

**Create database**:
```powershell
cd C:\Projects\ResumeTailor\01-Code\backend
alembic upgrade head
```

**View database**:
```powershell
# Install SQLite browser or use CLI
sqlite3 resume_tailor.db
.tables  # List tables
SELECT * FROM users;  # Query
```

---

### Staging Database (Railway PostgreSQL)

**Configuration**:
- Automatically provisioned by Railway
- `DATABASE_URL` auto-injected into backend service
- Connection string: `postgresql://postgres:***@maglev.proxy.rlwy.net:22595/railway`

**Access via Railway Dashboard**:
1. Railway dashboard → Project → PostgreSQL service
2. Click "Data" tab → View tables
3. Click "Connect" → Terminal access

**Run migrations**:
```bash
# In Railway backend service → Shell
alembic upgrade head
```

**Backup**:
- Railway provides automatic backups (daily)
- Go to: PostgreSQL service → Backups tab

---

### Production Database (Railway PostgreSQL)

**Configuration**:
- **Separate instance** from staging (critical!)
- New PostgreSQL service in production project
- `DATABASE_URL` auto-injected

**Best Practices**:
- ✅ Separate database (not shared with staging)
- ✅ Automatic backups enabled
- ✅ Monitor database size and performance
- ⚠️ Never manually delete data
- ⚠️ Always test migrations in staging first

**Connection Details**:
```
Host: containers-us-west-###.railway.app
Port: ####
Database: railway
User: postgres
Password: [auto-generated]
```

**Monitoring**:
- CPU usage < 50%
- Memory usage < 75%
- Storage < 80% capacity
- Connection count < 100

---

## 🌐 Domain & DNS Configuration

### GoDaddy DNS Settings

**For production domain**: resume2interview.com

**Required DNS Records**:

**A Record** (Root domain):
```
Type: A
Name: @ (or blank)
Value: 76.76.21.21  (Vercel IP - verify in Vercel dashboard)
TTL: 600 seconds (10 minutes)
```

**CNAME Record** (www subdomain):
```
Type: CNAME
Name: www
Value: cname.vercel-dns.com
TTL: 600 seconds
```

**How to configure**:
1. Go to https://godaddy.com → My Products → Domains
2. Click "DNS" next to resume2interview.com
3. Delete any existing A/CNAME records for @ and www
4. Add new records as above
5. Click "Save"
6. Wait 5-10 minutes for propagation

**Verification**:
```powershell
# Check DNS resolution
nslookup resume2interview.com
# Should return: 76.76.21.21 (or current Vercel IP)

nslookup www.resume2interview.com
# Should return: CNAME to vercel-dns.com
```

---

### SSL Certificate (Vercel)

**Configuration**: Automatic (Vercel manages)

**Verification**:
1. Vercel dashboard → Settings → Domains
2. Check `resume2interview.com` → Status: ✅ Valid Certificate
3. Certificate issued by: Let's Encrypt or Vercel

**If certificate issues**:
1. Verify DNS is pointing to Vercel
2. Wait 5-10 minutes for verification
3. Click "Refresh" in Vercel dashboard
4. Vercel will auto-renew certificates before expiry

---

## 🔐 Secrets Management

### Where to Store Secrets

| Secret | Storage Location | Access Control |
|--------|------------------|----------------|
| OpenAI API Key (dev) | Local `.env` file | Developer only |
| OpenAI API Key (prod) | Railway Variables | Admin only |
| Analytics Password (prod) | Password manager + Railway | Admin only |
| Database credentials | Railway auto-managed | Platform access |
| Domain credentials | GoDaddy account | Domain admin |

### Security Best Practices

✅ **DO**:
- Use different passwords/keys per environment
- Store production secrets in password manager (1Password, LastPass)
- Rotate API keys every 90 days
- Use strong passwords (16+ chars)
- Enable 2FA on all platforms

❌ **DON'T**:
- Commit `.env` files to Git (add to `.gitignore`)
- Share passwords via email/Slack
- Reuse staging passwords in production
- Use default/weak passwords
- Store secrets in code comments

---

## 📊 Configuration Checklist

### Pre-Deployment Configuration Verification

**Backend (Railway)**:
- [ ] `OPENAI_API_KEY` set and valid
- [ ] `ANALYTICS_PASSWORD` is strong (production)
- [ ] `CORS_ORIGINS` includes correct domain(s)
- [ ] `DATABASE_URL` is auto-injected (check green icon)
- [ ] `ENVIRONMENT` set correctly
- [ ] All variables have no extra spaces or quotes

**Frontend (Vercel)**:
- [ ] Root Directory: `01-Code/frontend`
- [ ] Framework: `Vite`
- [ ] Build/Output directories correct
- [ ] Custom domain added (production)
- [ ] SSL certificate valid

**Database (Railway)**:
- [ ] Separate database for production
- [ ] Backups enabled
- [ ] Migrations applied (`alembic upgrade head`)
- [ ] Can connect via Railway dashboard

**Domain (GoDaddy)**:
- [ ] A record points to Vercel IP
- [ ] CNAME record for www subdomain
- [ ] DNS propagation complete
- [ ] SSL certificate issued

---

## 🛠️ Configuration Management

### Making Configuration Changes

**Local changes**:
1. Edit `.env` file
2. Restart backend server
3. Changes apply immediately

**Staging/Production changes**:
1. Railway dashboard → Variables → Edit
2. Click "Redeploy" or wait for auto-redeploy
3. Verify changes in logs
4. Test affected functionality

### Configuration Version Control

**Track configuration in Git** (without secrets):
```json
// File: config/environments.json
{
  "staging": {
    "corsOrigins": "https://resume2interview-staging.vercel.app",
    "environment": "staging"
  },
  "production": {
    "corsOrigins": "https://resume2interview.com",
    "environment": "production"
  }
}
```

**Document secret values separately**:
- In password manager
- In secure team documentation
- NOT in Git

---

## 📝 Configuration Templates

### New Environment Setup Template

```bash
# Backend Environment Variables
DATABASE_URL=[auto-injected]
OPENAI_API_KEY=[get-from-openai-dashboard]
ANALYTICS_PASSWORD=[generate-strong-password]
CORS_ORIGINS=[frontend-url]
ENVIRONMENT=[environment-name]
PORT=8080

# Frontend Configuration
Root Directory: 01-Code/frontend
Framework: Vite
Build Command: npm run build
Output Directory: dist
Custom Domain: [if-production]

# Database Setup
1. Add PostgreSQL service in Railway
2. Run: alembic upgrade head
3. Verify: 8 tables created

# DNS Setup (if custom domain)
A Record: @ → Vercel IP
CNAME Record: www → cname.vercel-dns.com
```

---

## 🔍 Troubleshooting Configuration Issues

**Issue**: Environment variables not loading

**Solution**:
```powershell
# Check if variables are set (Railway)
# Dashboard → Service → Variables tab
# Verify each variable exists and has value

# Check backend logs for:
# "Environment variable X not found"
# "Using default value for X"
```

**Issue**: Database connection failed

**Solution**:
```powershell
# Verify DATABASE_URL is auto-injected
# Railway Dashboard → Backend → Variables
# Look for DATABASE_URL with green "Plugin" icon
# If missing: Re-add PostgreSQL service link
```

**Issue**: CORS errors

**Solution**:
```python
# Check CORS_ORIGINS includes frontend URL
# Staging: https://resume2interview-staging.vercel.app
# Production: https://resume2interview.com
# NO trailing slash
# NO http:// in production
```

---

## 📞 Configuration Support

For configuration issues:
1. Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. Verify all variables set correctly
3. Check logs for specific error messages
4. Contact DevOps team if unresolved

**Common pitfalls**:
- Extra spaces in environment variables
- Wrong domain in CORS_ORIGINS
- Missing DATABASE_URL (not auto-injected)
- Wrong OpenAI API key (staging vs production)
- Weak analytics password in production
