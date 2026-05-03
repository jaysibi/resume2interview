# Database Migrations

## Overview
This folder contains SQL migration scripts for the Resume Tailor database schema changes.

## Migrations

### 001_add_updated_at_column.sql
- **Date**: 2026-05-01
- **Description**: Adds `updated_at` TIMESTAMP column to `resumes` and `job_descriptions` tables
- **Features**:
  - Adds column with `CURRENT_TIMESTAMP` default
  - Creates automatic update triggers for both tables
  - Includes verification query

## Running Migrations

### Method 1: Using Python Script
```bash
cd c:\Projects\ResumeTailor\01-Code\backend
python run_migration.py migrations/001_add_updated_at_column.sql
```

### Method 2: Direct SQL Execution
```bash
psql -U postgres -d resumetailor -f migrations/001_add_updated_at_column.sql
```

## Migration Naming Convention
Format: `XXX_description_of_change.sql`
- `XXX`: Sequential number (001, 002, etc.)
- Description: Brief, lowercase with underscores

## Future Improvements
Consider setting up Alembic for:
- Automatic migration generation from model changes
- Migration versioning and rollback support
- Migration history tracking
- Cross-environment consistency

## Database Connection
- **Host**: localhost
- **Port**: 5432
- **Database**: resumetailor
- **User**: postgres (configurable via POSTGRES_URL env variable)
