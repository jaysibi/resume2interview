# Deploy Frontend to Vercel Staging
# Run this after Railway backend is deployed

# This script will:
# 1. Set the backend API URL
# 2. Deploy to Vercel staging
# 3. Configure for ui-ux-redesign branch

# REPLACE THIS with your Railway backend URL:
$BACKEND_URL = "REPLACE_WITH_RAILWAY_URL"

Write-Host "==================================" -ForegroundColor Cyan
Write-Host "Deploying Frontend to Vercel Staging" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

# Navigate to frontend directory
Push-Location C:\Projects\ResumeTailor\01-Code\frontend

# Create staging environment file
Write-Host "Creating .env.staging with backend URL..." -ForegroundColor Yellow
@"
VITE_API_URL=$BACKEND_URL
VITE_ENV=staging
"@ | Out-File -FilePath .env.staging -Encoding utf8 -Force

Write-Host "✓ Environment file created" -ForegroundColor Green
Write-Host ""

# Deploy to Vercel
Write-Host "Deploying to Vercel..." -ForegroundColor Yellow
Write-Host "(You may need to answer some questions)" -ForegroundColor Gray
Write-Host ""

vercel --yes

Write-Host ""
Write-Host "==================================" -ForegroundColor Green
Write-Host "Deployment Complete!" -ForegroundColor Green
Write-Host "==================================" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Copy the Vercel URL from above" -ForegroundColor White
Write-Host "2. Update Railway CORS_ORIGINS with this URL" -ForegroundColor White
Write-Host "3. Run database migrations" -ForegroundColor White

Pop-Location
