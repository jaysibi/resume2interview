# Run Database Migrations on Railway Staging
# Run this after Railway backend is deployed

# REPLACE THIS with your Railway DATABASE_URL:
$DATABASE_URL = "REPLACE_WITH_DATABASE_URL"

Write-Host "==================================" -ForegroundColor Cyan
Write-Host "Running Database Migrations" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

# Navigate to backend directory
Push-Location C:\Projects\ResumeTailor\01-Code\backend

# Set the database URL
$env:DATABASE_URL = $DATABASE_URL

Write-Host "Database URL configured" -ForegroundColor Green
Write-Host "Running Alembic migrations..." -ForegroundColor Yellow
Write-Host ""

# Run migrations
alembic upgrade head

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "==================================" -ForegroundColor Green
    Write-Host "✓ Migrations Complete!" -ForegroundColor Green
    Write-Host "==================================" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "==================================" -ForegroundColor Red
    Write-Host "✗ Migration Failed!" -ForegroundColor Red
    Write-Host "==================================" -ForegroundColor Red
    Write-Host "Check the error messages above" -ForegroundColor Yellow
}

Pop-Location
