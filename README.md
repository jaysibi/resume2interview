# Resume2Interview - Multi-Environment Deployment

This project uses a multi-environment deployment strategy with staging and production environments.

## \ud83c\udf0d Environments

### Staging Environment
- **Purpose**: Testing and QA before production
- **URL**: https://resume2interview-staging.vercel.app
- **Branch**: `ui-ux-redesign`
- **Backend**: Railway (staging)
- **Database**: PostgreSQL (staging)

### Production Environment
- **Purpose**: Live production application
- **URL**: https://www.resume2interview.com
- **Branch**: `main`
- **Backend**: Railway (production) or Custom domain (api.resume2interview.com)
- **Database**: PostgreSQL (production)

## \ud83d\udce6 Project Structure

```
ResumeTailor/
\u251c\u2500\u2500 01-Code/
\u2502   \u251c\u2500\u2500 backend/                 # FastAPI backend application
\u2502   \u2502   \u251c\u2500\u2500 main.py              # API endpoints & application entry
\u2502   \u2502   \u251c\u2500\u2500 models_v2.py         # Database models
\u2502   \u2502   \u251c\u2500\u2500 crud_v2.py           # Database operations
\u2502   \u2502   \u251c\u2500\u2500 ai_models.py         # OpenAI integration
\u2502   \u2502   \u251c\u2500\u2500 rate_limiter.py      # Rate limiting logic
\u2502   \u2502   \u251c\u2500\u2500 alembic/            # Database migrations
\u2502   \u2502   \u251c\u2500\u2500 Procfile            # Railway deployment config
\u2502   \u2502   \u251c\u2500\u2500 railway.json        # Railway service config
\u2502   \u2502   \u2514\u2500\u2500 requirements.txt    # Python dependencies
\u2502   \u2502
\u2502   \u251c\u2500\u2500 frontend/                # React frontend application
\u2502   \u2502   \u251c\u2500\u2500 src/
\u2502   \u2502   \u2502   \u251c\u2500\u2500 pages/          # Page components
\u2502   \u2502   \u2502   \u251c\u2500\u2500 components/     # Reusable components
\u2502   \u2502   \u2502   \u251c\u2500\u2500 services/       # API client
\u2502   \u2502   \u2502   \u2514\u2500\u2500 App.tsx         # Main app component
\u2502   \u2502   \u251c\u2500\u2500 vercel.json         # Vercel deployment config
\u2502   \u2502   \u251c\u2500\u2500 .env.example        # Environment variables template
\u2502   \u2502   \u251c\u2500\u2500 .env.staging        # Staging environment config
\u2502   \u2502   \u251c\u2500\u2500 .env.production     # Production environment config
\u2502   \u2502   \u2514\u2500\u2500 package.json        # Node dependencies
\u2502   \u2502
\u2502   \u251c\u2500\u2500 DEPLOYMENT.md           # Comprehensive deployment guide
\u2502   \u251c\u2500\u2500 QUICK_DEPLOY.md         # Quick deployment reference
\u2502   \u2514\u2500\u2500 PRODUCTION_CHECKLIST.md # Step-by-step production deployment
\u2502
\u2514\u2500\u2500 README.md                   # This file
```

## \ud83d\ude80 Quick Start - Local Development

### Prerequisites
- Python 3.13
- Node.js 18+
- PostgreSQL 16
- OpenAI API Key

### Backend Setup
```powershell
cd C:\Projects\ResumeTailor\01-Code\backend

# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Create .env file
echo "OPENAI_API_KEY=your-key-here" > .env
echo "DATABASE_URL=postgresql://user:pass@localhost:5432/resume2interview" >> .env
echo "CORS_ORIGINS=http://localhost:5173" >> .env

# Run migrations
alembic upgrade head

# Start server
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

Backend will be available at: http://localhost:8000
API docs at: http://localhost:8000/docs

### Frontend Setup
```powershell
cd C:\Projects\ResumeTailor\01-Code\frontend

# Install dependencies
npm install

# Create .env file
echo "VITE_API_URL=http://localhost:8000" > .env.local

# Start dev server
npm run dev
```

Frontend will be available at: http://localhost:5173

## \ud83c\udfaf Deployment

### Option 1: Quick Staging Deployment

See [QUICK_DEPLOY.md](01-Code/QUICK_DEPLOY.md) for fastest deployment to staging environment.

### Option 2: Full Multi-Environment Setup

See [PRODUCTION_CHECKLIST.md](01-Code/PRODUCTION_CHECKLIST.md) for complete staging + production deployment with custom domain.

### Option 3: Detailed Deployment Guide

See [DEPLOYMENT.md](01-Code/DEPLOYMENT.md) for comprehensive deployment documentation with all options.

## \ud83d\udcdd Deployment Workflow

### Day-to-Day Development

1. **Develop locally** on `ui-ux-redesign` branch
   ```bash
   git checkout ui-ux-redesign
   # ... make changes ...
   git add .
   git commit -m "feat: add feature"
   git push origin ui-ux-redesign
   ```

2. **Staging auto-deploys** - Test at staging URL

3. **If tests pass, promote to production**:
   ```bash
   git checkout main
   git merge ui-ux-redesign
   git push origin main
   ```

4. **Production auto-deploys** - Live at www.resume2interview.com

### Environment URLs

| Environment | Frontend | Backend | Database |
|------------|----------|---------|----------|
| **Local** | http://localhost:5173 | http://localhost:8000 | localhost:5432 |
| **Staging** | resume2interview-staging.vercel.app | Railway staging | Railway PostgreSQL |
| **Production** | www.resume2interview.com | api.resume2interview.com | Railway PostgreSQL |

## \ud83d\udee0\ufe0f Technology Stack

### Backend
- **Framework**: FastAPI 0.115.6
- **Language**: Python 3.13
- **Database**: PostgreSQL 16 + SQLAlchemy 2.0
- **Migrations**: Alembic
- **AI**: OpenAI GPT-4o-mini
- **Rate Limiting**: Custom in-memory implementation (5 req/day)

### Frontend
- **Framework**: React 19.2.5
- **Build Tool**: Vite 8.0.10
- **Language**: TypeScript 5.8.4
- **Styling**: Tailwind CSS v4.2.4
- **Routing**: React Router 7.14.2
- **HTTP Client**: Axios 1.15.2

### Infrastructure
- **Frontend Hosting**: Vercel
- **Backend Hosting**: Railway
- **Database Hosting**: Railway PostgreSQL
- **Custom Domain**: www.resume2interview.com
- **SSL**: Auto-provisioned by Vercel

## \ud83d\udcca Key Features

- \u2705 Resume upload and parsing (PDF, DOCX)
- \u2705 Job description analysis
- \u2705 Gap analysis (missing skills, recommendations)
- \u2705 ATS score calculation
- \u2705 Application tracking and management
- \u2705 Rate limiting (5 requests per day per IP)
- \u2705 Responsive design (mobile, tablet, desktop)
- \u2705 Multi-environment deployment
- \u2705 Delete functionality (single & bulk)
- \u2705 Custom domain support

## \ud83d\udd12 Security Features

- CORS protection (environment-specific origins)
- Rate limiting to prevent abuse
- Environment variable protection
- SSL/TLS encryption (HTTPS)
- Input validation and sanitization
- SQL injection protection (SQLAlchemy ORM)

## \ud83d\udcb0 Cost Estimate

| Service | Plan | Monthly Cost |
|---------|------|--------------|
| Vercel (Frontend) | Hobby | Free |
| Railway Staging | Developer | $5 |
| Railway Production | Developer | $5 |
| Domain Registration | Annual | ~$1/month |
| **Total** | | **~$11/month** |

## \ud83d\udcda Documentation

- [DEPLOYMENT.md](01-Code/DEPLOYMENT.md) - Comprehensive deployment guide with all options
- [QUICK_DEPLOY.md](01-Code/QUICK_DEPLOY.md) - Quick 5-minute deployment to staging
- [PRODUCTION_CHECKLIST.md](01-Code/PRODUCTION_CHECKLIST.md) - Step-by-step production deployment with custom domain

## \ud83d\udc65 Support

- **Repository**: https://github.com/jaysibi/resume2interview
- **Issues**: Create an issue on GitHub
- **Documentation**: See deployment guides above

## \ud83d\udce6 Version History

- **v2.0** (May 2026) - Complete rebranding to Resume2Interview, application management, multi-environment deployment
- **v1.0** (March 2026) - Initial ResumeTailor release

## \ud83d\udcdc License

[Add your license information here]

---

**Ready to deploy? Start with [QUICK_DEPLOY.md](01-Code/QUICK_DEPLOY.md)!**
