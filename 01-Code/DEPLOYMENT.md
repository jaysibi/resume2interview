# Resume2Interview - Comprehensive Deployment Guide

## 🎯 Multi-Environment Architecture

### Environment Strategy

| Environment | Purpose | URL | Auto-Deploy |
|------------|---------|-----|-------------|
| **Staging** | Testing & QA | `resume2interview-staging.vercel.app` | Yes (ui-ux-redesign branch) |
| **Production** | Live Production | `www.resume2interview.com` | Yes (main branch) |

### Infrastructure Overview

```
┌─────────────────────────────────────────────────────────┐
│                    GitHub Repository                     │
│              jaysibi/resume2interview                    │
└──────────────────┬─────────────────┬────────────────────┘
                   │                 │
          ┌────────▼────────┐   ┌───▼──────────┐
          │  ui-ux-redesign │   │     main     │
          │     branch       │   │    branch    │
          └────────┬────────┘   └───┬──────────┘
                   │                 │
      ┌────────────┴────────┐   ┌───┴──────────────┐
      │                     │   │                  │
┌─────▼─────────┐  ┌────────▼───▼───┐  ┌──────────▼────────┐
│   STAGING     │  │   STAGING       │  │   PRODUCTION      │
│   Frontend    │  │   Backend       │  │   Frontend        │
│   (Vercel)    │  │   (Railway)     │  │   (Vercel)        │
│               │  │                 │  │                   │
│ staging-*.    │  │ staging-api.    │  │ www.resume2       │
│ vercel.app    │  │ railway.app     │  │ interview.com     │
└───────────────┘  └─────────────────┘  └───────────────────┘
                            │                     │
                   ┌────────▼────────┐  ┌────────▼────────┐
                   │  STAGING DB     │  │ PRODUCTION DB   │
                   │  (PostgreSQL)   │  │ (PostgreSQL)    │
                   │  Railway        │  │ Railway         │
                   └─────────────────┘  └─────────────────┘
                            │                     │
                   ┌────────▼────────┐  ┌────────▼────────┐
                   │ PRODUCTION      │  │ PRODUCTION API  │
                   │ Backend         │  │ (Optional)      │
                   │ (Railway)       │  │ api.resume2     │
                   │                 │  │ interview.com   │
                   │ prod-api.       │  └─────────────────┘
                   │ railway.app     │
                   └─────────────────┘
```

### Technology Stack

- **Frontend**: React 19 + Vite 8 + TypeScript + Tailwind CSS v4 → Vercel
- **Backend**: FastAPI + Python 3.13 + SQLAlchemy → Railway/Render
- **Database**: PostgreSQL 16 → Railway Database
- **AI**: OpenAI GPT-4o-mini API

---

## 🚀 Complete Multi-Environment Setup

### Prerequisites

- [ ] GitHub repository: `jaysibi/resume2interview` (✅ Done)
- [ ] Domain purchased: `resume2interview.com` (Configure DNS)
- [ ] Railway account (https://railway.app)
- [ ] Vercel account (https://vercel.com)
- [ ] OpenAI API key

---

## Option 1: Deploy Multi-Environment to Vercel + Railway (Recommended)

### Step 1: Deploy Backend to Railway

Railway is perfect for FastAPI applications with PostgreSQL.

#### 1.1 Create Railway Account
1. Go to [Railway.app](https://railway.app)
2. Sign up with GitHub

#### 1.2 Deploy Backend
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login to Railway
railway login

# Navigate to backend directory
cd C:\Projects\ResumeTailor\01-Code\backend

# Initialize Railway project
railway init

# Link to your project
railway link
```

#### 1.3 Add PostgreSQL Database
1. In Railway dashboard, click "New" → "Database" → "PostgreSQL"
2. Railway will automatically set `DATABASE_URL` environment variable

#### 1.4 Set Environment Variables
In Railway dashboard, add:
```
OPENAI_API_KEY=your_openai_api_key_here
DATABASE_URL=postgresql://... (auto-set by Railway)
FRONTEND_URL=https://your-frontend.vercel.app
```

#### 1.5 Create Procfile (Railway will auto-detect)
Create `backend/Procfile`:
```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

#### 1.6 Deploy
```bash
railway up
```

Your backend will be available at: `https://your-app.railway.app`

---

### Step 2: Deploy Frontend to Vercel

#### 2.1 Install Vercel CLI
```bash
npm i -g vercel
```

#### 2.2 Login to Vercel
```bash
vercel login
```

#### 2.3 Configure API Base URL
Update `frontend/src/services/api.ts` to use Railway backend URL:
```typescript
const API_BASE_URL = import.meta.env.VITE_API_URL || 'https://your-backend.railway.app';
```

#### 2.4 Create `.env.production` in frontend directory
```bash
cd C:\Projects\ResumeTailor\01-Code\frontend
echo "VITE_API_URL=https://your-backend.railway.app" > .env.production
```

#### 2.5 Deploy to Vercel
```bash
# From frontend directory
vercel

# Follow prompts:
# - Set up and deploy? Yes
# - Which scope? (your account)
# - Link to existing project? No
# - Project name? resume2interview
# - Directory? ./
# - Override settings? No
```

#### 2.6 Set Environment Variables in Vercel Dashboard
1. Go to your project in Vercel dashboard
2. Settings → Environment Variables
3. Add: `VITE_API_URL` = `https://your-backend.railway.app`
4. Redeploy: `vercel --prod`

---

## Option 2: Deploy Both to Vercel (Serverless Functions)

⚠️ **Note**: This requires converting your FastAPI app to serverless functions. Not recommended for your current architecture due to:
- PostgreSQL connection pooling limitations
- Cold start delays
- OpenAI API timeout issues

If you still want to try:

### Create `api/index.py` (Vercel Serverless Function)
```python
from fastapi import FastAPI
from mangum import Mangum

app = FastAPI()

# Import your routes here
# ... (simplified version of your main.py)

handler = Mangum(app)
```

### Create `vercel.json` in root
```json
{
  "builds": [
    {
      "src": "frontend/package.json",
      "use": "@vercel/static-build",
      "config": {
        "distDir": "dist"
      }
    },
    {
      "src": "api/index.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "api/index.py"
    },
    {
      "src": "/(.*)",
      "dest": "frontend/$1"
    }
  ]
}
```

---

## Option 3: Deploy to Render (All-in-One)

Render can host both frontend and backend in one platform.

### 3.1 Create Render Account
Go to [Render.com](https://render.com)

### 3.2 Deploy Backend
1. New → Web Service
2. Connect GitHub repo
3. Settings:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Environment**: Python 3
4. Add Environment Variables (same as Railway)

### 3.3 Create PostgreSQL Database
1. New → PostgreSQL
2. Copy connection string to backend environment variables

### 3.4 Deploy Frontend
1. New → Static Site
2. Connect GitHub repo (frontend directory)
3. Settings:
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: `dist`
4. Add Environment Variable: `VITE_API_URL=https://your-backend.onrender.com`

---

## Quick Start: GitHub → Vercel Auto-Deploy

### 1. Push to GitHub (Already Done ✅)
```bash
# Your repo: https://github.com/jaysibi/resume2interview
```

### 2. Import to Vercel (Frontend Only)
1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click "Add New" → "Project"
3. Import `jaysibi/resume2interview`
4. **Root Directory**: `01-Code/frontend`
5. **Framework Preset**: Vite
6. **Build Command**: `npm run build`
7. **Output Directory**: `dist`
8. Click "Deploy"

### 3. Add Environment Variables
After deployment:
1. Project Settings → Environment Variables
2. Add `VITE_API_URL` with your backend URL
3. Redeploy

---

## Database Migration

Before deploying, run migrations on your production database:

```bash
# Set DATABASE_URL to production
export DATABASE_URL="postgresql://..."

# Run migrations
cd backend
alembic upgrade head
```

---

## Post-Deployment Checklist

- [ ] Backend deployed and accessible
- [ ] PostgreSQL database created and migrated
- [ ] Frontend deployed and accessible
- [ ] Environment variables configured:
  - [ ] `OPENAI_API_KEY` in backend
  - [ ] `DATABASE_URL` in backend
  - [ ] `FRONTEND_URL` in backend (for CORS)
  - [ ] `VITE_API_URL` in frontend
- [ ] CORS configured in backend:
  ```python
  app.add_middleware(
      CORSMiddleware,
      allow_origins=["https://your-frontend.vercel.app"],
      allow_credentials=True,
      allow_methods=["*"],
      allow_headers=["*"],
  )
  ```
- [ ] Test application end-to-end
- [ ] Monitor logs for errors

---

## Troubleshooting

### CORS Errors
Update `backend/main.py`:
```python
origins = [
    "https://your-frontend.vercel.app",
    "https://*.vercel.app",  # For preview deployments
]
```

### API Connection Failed
- Check `VITE_API_URL` is set correctly
- Verify backend is running (visit `https://your-backend.railway.app/docs`)
- Check browser console for errors

### Database Connection Issues
- Verify `DATABASE_URL` format: `postgresql://user:pass@host:5432/dbname`
- Check database is running and accessible
- Ensure migrations are applied

### Build Failures
- Check build logs in platform dashboard
- Verify all dependencies in `requirements.txt` (backend) and `package.json` (frontend)
- Check Node.js version compatibility

---

## Recommended: Railway + Vercel Setup

**Why this combination?**
- ✅ Railway: Best for Python/FastAPI apps with databases
- ✅ Vercel: Best for React/Vite frontends
- ✅ Free tiers available
- ✅ Auto-deploy from GitHub
- ✅ Built-in PostgreSQL support

**Cost Estimate:**
- Railway: $5/month (after free tier)
- Vercel: Free for personal projects
- Total: ~$5/month

---

## Need Help?

Review platform-specific documentation:
- [Vercel Docs](https://vercel.com/docs)
- [Railway Docs](https://docs.railway.app)
- [Render Docs](https://render.com/docs)
