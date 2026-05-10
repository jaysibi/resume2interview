# Resume2Interview - Quick Deployment Guide

## 🚀 Fastest Way to Deploy (5 minutes)

### Frontend to Vercel

1. **Go to Vercel Dashboard**: https://vercel.com/new

2. **Import Your GitHub Repository**:
   - Click "Import Git Repository"
   - Select: `jaysibi/resume2interview`
   - Click "Import"

3. **Configure Project**:
   ```
   Root Directory: 01-Code/frontend
   Framework Preset: Vite
   Build Command: npm run build
   Output Directory: dist
   Install Command: npm install
   ```

4. **Add Environment Variable**:
   - Click "Environment Variables"
   - Add: `VITE_API_URL` = `https://your-backend-url.railway.app`
   - (You'll get this URL after deploying backend)

5. **Click "Deploy"** ✅

---

### Backend to Railway

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
