# Resume2Interview - Multi-Environment Deployment Guide

## 🎯 Deployment Strategy

**Two Environments:**
- **Staging**: For testing and preview (Vercel auto-generated URL)
- **Production**: Live at www.resume2interview.com

**Architecture:**
```
GitHub (ui-ux-redesign branch)
    ↓
┌───────────────────────┬────────────────────────┐
│    STAGING            │     PRODUCTION         │
├───────────────────────┼────────────────────────┤
│ Frontend (Vercel)     │ Frontend (Vercel)      │
│ staging-*.vercel.app  │ www.resume2interview.com│
│         ↓             │          ↓             │
│ Backend (Railway)     │ Backend (Railway)      │
│ staging-api.railway   │ api-prod.railway       │
│         ↓             │          ↓             │
│ PostgreSQL (Railway)  │ PostgreSQL (Railway)   │
└───────────────────────┴────────────────────────┘
```

---

## 🚀 Step-by-Step Deployment

### Phase 1: Deploy Staging Environment

#### 1.1 Deploy Staging Backend to Railway

1. **Go to Railway**: https://railway.app
2. **Create New Project**: Click "New Project" → "Deploy from GitHub repo"
3. **Select Repository**: `jaysibi/resume2interview`
4. **Configure Service**:
   - Name: `resume2interview-backend-staging`
   - Root Directory: `01-Code/backend`
   - Branch: `ui-ux-redesign`
5. **Add PostgreSQL Database**:
   - Click "New" → "Database" → "PostgreSQL"
   - Name it: `resume2interview-db-staging`
6. **Set Environment Variables**:
   ```
   OPENAI_API_KEY=sk-proj-your-key-here
   CORS_ORIGINS=https://resume2interview-staging.vercel.app,https://*.vercel.app
   ENVIRONMENT=staging
   ```
7. **Generate Domain**:
   - Settings → Networking → Generate Domain
   - Copy URL (e.g., `https://resume2interview-staging.up.railway.app`)

#### 1.2 Deploy Staging Frontend to Vercel

1. **Go to Vercel**: https://vercel.com/new
2. **Import Repository**: `jaysibi/resume2interview`
3. **Configure Project**:
   ```
   Project Name: resume2interview-staging
   Root Directory: 01-Code/frontend
   Framework: Vite
   Build Command: npm run build
   Output Directory: dist
   Branch: ui-ux-redesign
   ```
4. **Add Environment Variables**:
   ```
   VITE_API_URL=https://resume2interview-staging.up.railway.app
   VITE_ENV=staging
   ```
5. **Deploy** → Get staging URL (e.g., `resume2interview-staging.vercel.app`)

#### 1.3 Update CORS in Staging Backend

Go back to Railway staging service and update:
```
CORS_ORIGINS=https://resume2interview-staging.vercel.app
```

---

### Phase 2: Deploy Production Environment

#### 2.1 Deploy Production Backend to Railway

1. **Create Another Project** in Railway
2. **Or Add New Service** to existing project:
   - Click "New" → "GitHub Repo"
   - Select same repo
3. **Configure Service**:
   - Name: `resume2interview-backend-prod`
   - Root Directory: `01-Code/backend`
   - Branch: `main` (or `ui-ux-redesign` for now)
4. **Add PostgreSQL Database**:
   - Click "New" → "Database" → "PostgreSQL"
   - Name: `resume2interview-db-prod`
5. **Set Environment Variables**:
   ```
   OPENAI_API_KEY=sk-proj-your-key-here
   CORS_ORIGINS=https://www.resume2interview.com,https://resume2interview.com
   ENVIRONMENT=production
   ```
6. **Add Custom Domain** (Optional but recommended):
   - Settings → Networking → Custom Domain
   - Add: `api.resume2interview.com`
   - Configure DNS:
     - Type: CNAME
     - Name: api
     - Value: (Railway provides this)
7. **Or use Railway domain**: `https://resume2interview-prod.up.railway.app`

#### 2.2 Deploy Production Frontend to Vercel

1. **Create New Project** in Vercel
2. **Import Repository**: `jaysibi/resume2interview`
3. **Configure Project**:
   ```
   Project Name: resume2interview-production
   Root Directory: 01-Code/frontend
   Framework: Vite
   Build Command: npm run build
   Output Directory: dist
   Branch: main (or specify production branch)
   ```
4. **Add Environment Variables**:
   ```
   VITE_API_URL=https://api.resume2interview.com
   (or: https://resume2interview-prod.up.railway.app)
   VITE_ENV=production
   ```
5. **Deploy**

#### 2.3 Add Custom Domain to Vercel

1. **In Vercel Project Settings**:
   - Go to "Domains"
   - Click "Add"
   - Enter: `www.resume2interview.com`
   - Click "Add" again for apex domain: `resume2interview.com`

2. **Configure DNS at Your Domain Registrar**:
   
   **For www subdomain:**
   ```
   Type: CNAME
   Name: www
   Value: cname.vercel-dns.com
   ```
   
   **For apex domain (resume2interview.com):**
   ```
   Type: A
   Name: @
   Value: 76.76.21.21
   ```
   
   **And:**
   ```
   Type: CNAME
   Name: @
   Value: cname.vercel-dns.com
   ```

3. **Wait for DNS propagation** (5-60 minutes)

4. **Vercel will auto-provision SSL certificate**

---

### Phase 3: Database Migrations

#### Staging Database
```bash
cd C:\Projects\ResumeTailor\01-Code\backend

# Get DATABASE_URL from Railway staging
$env:DATABASE_URL="postgresql://postgres:...@staging-host.railway.app:5432/railway"

# Run migrations
alembic upgrade head
```

#### Production Database
```bash
# Get DATABASE_URL from Railway production
$env:DATABASE_URL="postgresql://postgres:...@prod-host.railway.app:5432/railway"

# Run migrations
alembic upgrade head
```

---

## 🔄 Deployment Workflow

### Development → Staging → Production

1. **Make changes locally** on `ui-ux-redesign` branch
2. **Push to GitHub**:
   ```bash
   git push origin ui-ux-redesign
   ```
3. **Staging auto-deploys** (Vercel + Railway watch the branch)
4. **Test on staging**: `https://resume2interview-staging.vercel.app`
5. **If tests pass, merge to main**:
   ```bash
   git checkout main
   git merge ui-ux-redesign
   git push origin main
   ```
6. **Production auto-deploys** to `www.resume2interview.com`

### Manual Deployment (Alternative)

If you prefer manual control:

**Disable Auto-Deploy:**
- **Vercel**: Project Settings → Git → Enable "Production Branch" = `main` only
- **Railway**: Service Settings → Disable auto-deploy

**Manual Deploy:**
```bash
# Deploy to Vercel production
cd C:\Projects\ResumeTailor\01-Code\frontend
vercel --prod

# Railway deploys automatically on push, or trigger manually in dashboard
```

---

## 🧪 Testing Checklist

### Staging Environment
Before promoting to production:

- [ ] Frontend loads: `https://resume2interview-staging.vercel.app`
- [ ] Backend API: `https://staging-backend.railway.app/docs`
- [ ] Upload resume works
- [ ] Upload job description works
- [ ] Gap analysis generates correctly
- [ ] ATS score calculates
- [ ] Applications page shows data
- [ ] Delete functionality works
- [ ] Rate limiting triggers correctly
- [ ] No console errors
- [ ] Mobile responsive

### Production Environment
After deployment:

- [ ] Domain resolves: `www.resume2interview.com`
- [ ] SSL certificate valid (🔒 in browser)
- [ ] Backend API accessible
- [ ] All features work end-to-end
- [ ] Performance is acceptable
- [ ] Monitor logs for errors

---

### Quick Staging-Only Setup (Original Guide)

1. **Go to Railway**: https://railway.app

2. **Create New Project**:
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose: `jaysibi/resume2interview`

3. **Configure Service**:
   - Root Directory: `01-Code/backend`
   - Railway will auto-detect Python and use Procfile

4. **Add PostgreSQL Database**:
   - Click "New" in your project
   - Select "Database" → "PostgreSQL"
   - Railway auto-sets `DATABASE_URL`

5. **Add Environment Variables**:
   ```
   OPENAI_API_KEY=sk-proj-your-key-here
   CORS_ORIGINS=https://your-frontend.vercel.app
   ```

6. **Generate Domain**:
   - Go to Settings → Networking
   - Click "Generate Domain"
   - Copy the URL (e.g., `https://your-app.railway.app`)

7. **Run Database Migrations**:
   - In Railway dashboard → your service
   - Go to "Variables" tab
   - Copy the `DATABASE_URL`
   - Locally run:
     ```bash
     cd C:\Projects\ResumeTailor\01-Code\backend
     $env:DATABASE_URL="postgresql://..."
     alembic upgrade head
     ```

8. **Redeploy** if needed

---

### Update Frontend with Backend URL

1. **Go Back to Vercel Dashboard**

2. **Update Environment Variable**:
   - Your Project → Settings → Environment Variables
   - Update `VITE_API_URL` with Railway URL
   - Click "Save"

3. **Redeploy**:
   - Go to Deployments tab
   - Click "..." on latest deployment
   - Click "Redeploy"

---

## ✅ Verification

1. **Backend Health Check**:
   Visit: `https://your-backend.railway.app/docs`
   (Should see FastAPI Swagger docs)

2. **Frontend Check**:
   Visit: `https://your-frontend.vercel.app`
   (Should load Resume2Interview homepage)

3. **Test Upload**:
   - Upload a resume and job description
   - Click "Analyze Resume"
   - Should get analysis results

---

## 🔧 Troubleshooting

### CORS Error in Browser Console

**Fix**: Update Railway environment variable:
```
CORS_ORIGINS=https://your-frontend.vercel.app,https://*.vercel.app
```

### "Failed to fetch" API Error

**Check**:
1. Backend is running: Visit `/docs` endpoint
2. `VITE_API_URL` is set correctly in Vercel
3. No typos in the URL

### Database Connection Error

**Check**:
1. PostgreSQL is running in Railway
2. `DATABASE_URL` is set automatically
3. Migrations were run successfully

---

## 💰 Costs

- **Vercel**: Free (personal projects)
- **Railway**: 
  - $5/month (500 hours)
  - Or free trial with credit card

**Total**: ~$5/month

---

## 📝 Alternative: Use Render (Free Tier)

Both frontend and backend can be hosted on Render **for free**:

1. **Go to**: https://render.com
2. **New Web Service** (for backend)
   - Connect GitHub repo
   - Root Directory: `01-Code/backend`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
3. **New Static Site** (for frontend)
   - Connect GitHub repo
   - Root Directory: `01-Code/frontend`
   - Build Command: `npm install && npm run build`
   - Publish Directory: `dist`
4. **Add PostgreSQL** (free tier available)

**Note**: Free tier has limitations:
- ⚠️ Services sleep after 15 mins of inactivity
- ⚠️ Slower cold starts (30-60 seconds)
- ✅ Good for testing/demos

---

## 🎯 Production Readiness Checklist

Before going live:

- [ ] Set strong `SECRET_KEY` in backend
- [ ] Enable rate limiting (already implemented)
- [ ] Set up monitoring/logging
- [ ] Configure custom domain (optional)
- [ ] Set up database backups
- [ ] Enable HTTPS (auto on Vercel/Railway)
- [ ] Test all features end-to-end
- [ ] Set up error tracking (Sentry, etc.)
- [ ] Configure CDN for static assets
- [ ] Review and update CORS origins

---

## 📚 Platform Documentation

- [Vercel Deployment Docs](https://vercel.com/docs/deployments/overview)
- [Railway Deployment Guide](https://docs.railway.app/deploy/deployments)
- [Render Deploy Guide](https://render.com/docs/deploy-fastapi)

---

## 🆘 Need Help?

1. Check deployment logs in platform dashboards
2. Review error messages carefully
3. Test locally first: `npm run dev` and `uvicorn main:app --reload`
4. Check environment variables are set correctly
5. Verify database connection strings

---

**Ready to deploy? Start with Vercel + Railway combo! 🚀**
