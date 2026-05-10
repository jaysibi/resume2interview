# Staging Deployment Progress

## Current Status: 🟡 IN PROGRESS

### ✅ Completed
- [x] Vercel CLI installed and authenticated
- [x] Railway website opened
- [x] Deployment scripts created
- [x] Documentation prepared

### 🔄 In Progress
- [ ] **STEP 1: Railway Backend Setup** ← YOU ARE HERE

---

## STEP 1: Railway Backend (Web Interface)

### Actions Required:
1. ✅ Opened Railway.app in browser
2. ⏳ **Sign in with GitHub** (jaysibi account)
3. ⏳ **Create New Project** → Deploy from GitHub repo
4. ⏳ Select repository: `jaysibi/resume2interview`
5. ⏳ Configure service:
   - Root Directory: `01-Code/backend`
   - Branch: `ui-ux-redesign`
6. ⏳ Add PostgreSQL database
7. ⏳ Set environment variables:
   ```
   OPENAI_API_KEY=sk-proj-...
   CORS_ORIGINS=https://resume2interview-staging.vercel.app,https://*.vercel.app
   ENVIRONMENT=staging
   ```
8. ⏳ Generate domain
9. ⏳ **COPY THE RAILWAY URL**

### What You'll Get:
- Backend URL: `https://something.up.railway.app`
- Database URL: (automatically set in Railway)

---

## STEP 2: Deploy Frontend to Vercel (Automated)

### Once Railway is ready:

1. **Edit the deployment script**:
   ```powershell
   notepad C:\Projects\ResumeTailor\deploy-staging-frontend.ps1
   ```
   
2. **Replace this line**:
   ```powershell
   $BACKEND_URL = "REPLACE_WITH_RAILWAY_URL"
   ```
   With your Railway URL:
   ```powershell
   $BACKEND_URL = "https://your-backend.up.railway.app"
   ```

3. **Run the script**:
   ```powershell
   cd C:\Projects\ResumeTailor
   .\deploy-staging-frontend.ps1
   ```

4. **Follow prompts**:
   - Project name: `resume2interview-staging`
   - Setup: Yes
   - Scope: Select your account
   - Link to existing: No
   - Directory: `./` (already in frontend)
   - Override settings: No

5. **Copy the Vercel URL** from the output

---

## STEP 3: Update Railway CORS

1. Go back to Railway dashboard
2. Click your backend service
3. Go to "Variables" tab
4. Update `CORS_ORIGINS`:
   ```
   CORS_ORIGINS=https://your-actual-frontend.vercel.app
   ```
   (Replace with the URL you got from Vercel)
5. Service will auto-redeploy

---

## STEP 4: Run Database Migrations

1. **Get DATABASE_URL from Railway**:
   - Railway dashboard → Your service → Variables tab
   - Copy the `DATABASE_URL` value

2. **Edit migration script**:
   ```powershell
   notepad C:\Projects\ResumeTailor\run-migrations-staging.ps1
   ```

3. **Replace this line**:
   ```powershell
   $DATABASE_URL = "REPLACE_WITH_DATABASE_URL"
   ```
   With your Railway database URL:
   ```powershell
   $DATABASE_URL = "postgresql://postgres:...@railway.app:5432/railway"
   ```

4. **Run migrations**:
   ```powershell
   cd C:\Projects\ResumeTailor
   .\run-migrations-staging.ps1
   ```

---

## STEP 5: Test Staging Environment

### Backend Test:
```powershell
# Replace with your Railway URL
Invoke-WebRequest -Uri "https://your-backend.railway.app/docs"
```
Should show FastAPI documentation

### Frontend Test:
```powershell
# Replace with your Vercel URL
Start-Process "https://your-frontend.vercel.app"
```
Should load Resume2Interview homepage

### Full E2E Test:
1. Visit your Vercel staging URL
2. Upload a resume (PDF or DOCX)
3. Upload a job description
4. Click "Analyze Resume"
5. Verify results appear

---

## Environment URLs (Fill in as you deploy)

```
STAGING ENVIRONMENT:
├─ Frontend: https://_________________________.vercel.app
├─ Backend:  https://_________________________.railway.app
└─ Database: (Railway manages this)
```

---

## Troubleshooting

### Issue: Railway deployment fails
- Check build logs in Railway dashboard
- Verify `requirements.txt` exists
- Verify `Procfile` exists

### Issue: Frontend can't connect to backend
- Check `VITE_API_URL` in Vercel (Settings → Environment Variables)
- Check `CORS_ORIGINS` in Railway includes your Vercel URL
- Check browser console for errors

### Issue: Database migrations fail
- Verify `DATABASE_URL` is correct
- Check if database is running in Railway
- Ensure you're in the backend directory

---

## Quick Reference Commands

```powershell
# Check Vercel login
vercel whoami

# Deploy frontend manually
cd C:\Projects\ResumeTailor\01-Code\frontend
vercel

# Check Railway service status
# (via web dashboard)

# Run migrations
cd C:\Projects\ResumeTailor\01-Code\backend
$env:DATABASE_URL = "postgresql://..."
alembic upgrade head

# Open Railway dashboard
Start-Process "https://railway.app/dashboard"

# Open Vercel dashboard  
Start-Process "https://vercel.com/dashboard"
```

---

## Next Steps After Staging Works

1. Test thoroughly on staging
2. Fix any issues
3. Commit fixes to `ui-ux-redesign` branch
4. Deploy to production (follow PRODUCTION_CHECKLIST.md)

---

## Need Help?

- Railway Docs: https://docs.railway.app
- Vercel Docs: https://vercel.com/docs
- Project Docs: `01-Code/QUICK_DEPLOY.md`
