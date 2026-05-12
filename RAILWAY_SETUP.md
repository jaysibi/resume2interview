# Railway Deployment Setup Guide

This guide will help you deploy ResumeTailor to Railway with minimal manual configuration.

## 🚀 Quick Setup (One-Time Only)

### 1. **Create Railway Project**
```bash
# Install Railway CLI (optional but recommended)
npm install -g @railway/cli

# Login to Railway
railway login

# Link this project to Railway
railway link
```

### 2. **Add PostgreSQL Service**
In Railway Dashboard:
1. Click **"+ New"** → **"Database"** → **"Add PostgreSQL"**
2. Railway will automatically create a PostgreSQL service
3. Railway auto-generates `DATABASE_URL` environment variable

### 3. **Connect Backend to PostgreSQL**
In Railway Dashboard:
1. Click on your **Backend service**
2. Go to **"Variables"** tab
3. Click **"+ New Variable"** → **"Add Reference"**
4. Select: **PostgreSQL service** → **DATABASE_URL**
5. This links the database to your backend automatically

### 4. **Add Required Environment Variables**
In Railway Dashboard → Backend Service → Variables:

#### **Add these manually (one-time setup):**

| Variable Name | Value | Required? |
|---------------|-------|-----------|
| `OPENAI_API_KEY` | `sk-proj-YOUR_KEY_HERE` | ✅ Yes (for resume analysis) |
| `CORS_ORIGINS` | `https://your-frontend.vercel.app,http://localhost:5173` | ✅ Yes (for frontend access) |
| `ANALYTICS_PASSWORD` | Your custom password | ✅ Yes (for analytics dashboard) |

**Note:** `DATABASE_URL` is automatically provided by Railway when you connect the PostgreSQL service (step 3).

---

## 🔧 Configuration Files

### **.env.example** (In backend folder)
Documents all environment variables needed for local development.

**Important:** Railway uses auto-detection to deploy the backend. No railway.toml is needed.

---

## 📦 Deployment Process

### **Automatic Deployment (No manual steps)**
Once setup is complete, every push to `main` branch auto-deploys:

```bash
git add .
git commit -m "Your changes"
git push origin main
```

Railway will:
1. ✅ Detect changes
2. ✅ Build backend with Nixpacks
3. ✅ Run database migrations (via Alembic)
4. ✅ Deploy to production
5. ✅ Update your backend URL

---

## 🔍 Troubleshooting

### **Check if variables are set:**
Visit: `https://your-backend.railway.app/debug/env-check`

Should show:
```json
{
  "variables": {
    "DATABASE_URL": { "set": true },
    "CORS_ORIGINS": { "set": true },
    "OPENAI_API_KEY": { "set": true }
  }
}
```

### **Check database connection:**
Visit: `https://your-backend.railway.app/debug/db-config`

Should show:
```json
{
  "database": {
    "table_count": 8,
    "alembic_version": "v2_004"
  }
}
```

### **Common Issues:**

#### **DATABASE_URL shows NOT_SET**
- **Cause:** PostgreSQL service not linked to backend
- **Fix:** Follow Step 3 above (Connect Backend to PostgreSQL)

#### **CORS errors in frontend**
- **Cause:** CORS_ORIGINS not set or wrong domain
- **Fix:** Add your Vercel URL to CORS_ORIGINS in Railway variables

#### **Analytics password doesn't work**
- **Cause:** ANALYTICS_PASSWORD not set, using default
- **Fix:** Try password `admin123` or set custom in Railway variables

---

## 🎯 Environment Variables Summary

### **Auto-Configured (by railway.toml)**
- ✅ CORS_ORIGINS (includes localhost for testing)
- ✅ ANALYTICS_PASSWORD (defaults to admin123)

### **Auto-Injected (by Railway)**
- ✅ DATABASE_URL (from PostgreSQL service)
- ✅ PORT (Railway assigns this)
- ✅ RAILWAY_ENVIRONMENT

### **Required Manual Setup (ONE TIME)**
- ❗ OPENAI_API_KEY (your OpenAI API key)
- ❗ CORS_ORIGINS (must include your production Vercel URL)

---

## ✅ Verification Checklist

After setup, verify these work:

- [ ] Backend health check: `https://your-backend.railway.app/`
- [ ] Database connected: `https://your-backend.railway.app/debug/db-config`
- [ ] Variables set: `https://your-backend.railway.app/debug/env-check`
- [ ] Frontend can reach backend (no CORS errors)
- [ ] Analytics login works: `https://your-frontend.vercel.app/analytics`
- [ ] Resume upload works: `https://your-frontend.vercel.app/upload`

---

## 🔐 Security Best Practices

### **DO:**
- ✅ Use Railway environment variables for sensitive data
- ✅ Keep .env file in .gitignore (already configured)
- ✅ Rotate OPENAI_API_KEY periodically
- ✅ Use strong ANALYTICS_PASSWORD in production

### **DON'T:**
- ❌ Commit .env file to Git
- ❌ Hardcode API keys in source code
- ❌ Share production DATABASE_URL publicly
- ❌ Use default passwords (admin123) in production

---

## 📞 Support

If deployment still fails after following this guide:
1. Check Railway logs: Railway Dashboard → Backend Service → Deployments → Click latest → View logs
2. Check diagnostic endpoints (URLs above)
3. Verify all environment variables are set in Railway dashboard
