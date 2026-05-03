# Alembic Database Migrations

## Overview

Alembic is our database migration tool for managing schema changes in a version-controlled manner. It allows us to:
- Track database schema changes over time
- Apply migrations incrementally
- Roll back changes if needed
- Auto-generate migrations from model changes
- Maintain consistency across development, staging, and production

## Setup

Alembic has been initialized and configured for this project. The configuration includes:
- **alembic.ini**: Main configuration file with database URL
- **alembic/env.py**: Environment configuration that imports our SQLAlchemy models
- **alembic/versions/**: Directory containing migration scripts

## Common Commands

### 1. Create a New Migration (Auto-generate)

Alembic can automatically detect changes in your SQLAlchemy models and generate migrations:

```bash
cd c:\Projects\ResumeTailor\01-Code\backend
python -m alembic revision --autogenerate -m "Description of changes"
```

**Example**:
```bash
python -m alembic revision --autogenerate -m "Add user authentication table"
```

This compares your current models against the database schema and generates a migration script in `alembic/versions/`.

### 2. Create a Migration Manually

For custom migrations (e.g., data migrations, complex schema changes):

```bash
python -m alembic revision -m "Description of migration"
```

This creates an empty migration template that you can edit manually.

### 3. Apply Migrations (Upgrade)

Apply all pending migrations to bring your database up to date:

```bash
python -m alembic upgrade head
```

Apply migrations up to a specific revision:

```bash
python -m alembic upgrade <revision_id>
```

**Example**:
```bash
python -m alembic upgrade ae1027a6acf5
```

### 4. Rollback Migrations (Downgrade)

Roll back the last migration:

```bash
python -m alembic downgrade -1
```

Roll back to a specific revision:

```bash
python -m alembic downgrade <revision_id>
```

Roll back all migrations:

```bash
python -m alembic downgrade base
```

### 5. View Migration History

See current database revision:

```bash
python -m alembic current
```

View all migrations:

```bash
python -m alembic history
```

View pending migrations:

```bash
python -m alembic history --verbose
```

## Migration Workflow

### Step-by-Step Process

1. **Make Changes to Models**
   - Edit `models.py` to add/modify database tables
   - Example: Add new column, create new table, change column type

2. **Generate Migration**
   ```bash
   python -m alembic revision --autogenerate -m "Add new field to Resume model"
   ```

3. **Review Generated Migration**
   - Open the generated file in `alembic/versions/`
   - Verify the `upgrade()` and `downgrade()` functions
   - Make manual edits if needed

4. **Apply Migration**
   ```bash
   python -m alembic upgrade head
   ```

5. **Verify Changes**
   - Check database schema
   - Run tests to ensure everything works

6. **Commit Migration**
   ```bash
   git add alembic/versions/<new_migration_file>.py
   git commit -m "Add migration: description"
   ```

## Migration Script Structure

Each migration file has two main functions:

```python
def upgrade() -> None:
    """
    Apply changes to move forward
    """
    op.add_column('resumes', sa.Column('new_field', sa.String(255)))

def downgrade() -> None:
    """
    Revert changes to move backward
    """
    op.drop_column('resumes', 'new_field')
```

## Common Operations

### Add Column

```python
def upgrade():
    op.add_column('resumes', 
        sa.Column('resume_score', sa.Integer(), nullable=True)
    )

def downgrade():
    op.drop_column('resumes', 'resume_score')
```

### Modify Column

```python
def upgrade():
    op.alter_column('resumes', 'filename',
        existing_type=sa.String(length=255),
        type_=sa.String(length=500)
    )

def downgrade():
    op.alter_column('resumes', 'filename',
        existing_type=sa.String(length=500),
        type_=sa.String(length=255)
    )
```

### Create Table

```python
def upgrade():
    op.create_table('user_sessions',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('token', sa.String(255), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False)
    )

def downgrade():
    op.drop_table('user_sessions')
```

### Create Index

```python
def upgrade():
    op.create_index('idx_resumes_filename', 'resumes', ['filename'])

def downgrade():
    op.drop_index('idx_resumes_filename', 'resumes')
```

## Environment Variables

Alembic respects the `POSTGRES_URL` environment variable for database connection:

```bash
export POSTGRES_URL=postgresql+psycopg2://user:pass@host:port/dbname
python -m alembic upgrade head
```

If not set, it uses the default from `alembic.ini`:
```
postgresql+psycopg2://postgres:postgres@localhost:5432/resumetailor
```

## Best Practices

1. **Always Review Auto-Generated Migrations**
   - Alembic doesn't detect everything (e.g., renames vs add+drop)
   - Verify the operations make sense

2. **Test Migrations Before Committing**
   - Apply migration: `alembic upgrade head`
   - Test application
   - Roll back: `alembic downgrade -1`
   - Verify rollback works
   - Reapply: `alembic upgrade head`

3. **Include Data Migrations When Needed**
   - Sometimes schema changes require data transformations
   - Use `op.execute()` for SQL commands

4. **One Logical Change Per Migration**
   - Makes debugging easier
   - Easier to roll back specific changes

5. **Never Edit Applied Migrations**
   - Once a migration is in production, create a new migration to fix it
   - Editing existing migrations can cause issues with revision history

6. **Document Complex Migrations**
   - Add comments explaining the reasoning
   - Link to related issues/tickets

## Troubleshooting

### "Target database is not up to date"

Database has migrations that aren't in your codebase. Options:
- Pull latest code with migrations
- Downgrade database to common revision
- Stamp database to current HEAD (if you know what you're doing)

```bash
python -m alembic stamp head
```

### "Can't locate revision identified by '<id>'"

Migration file is missing. Check:
- Did you pull latest migrations from git?
- Is the file in `alembic/versions/`?

### Alembic Can't Detect Table Changes

Auto-generate has limitations. It doesn't detect:
- Table or column renames (sees as drop + add)
- Check constraints changes
- Enum type changes

Solution: Create manual migration

### Multiple Database Heads

Happens when multiple people create migrations in parallel:

```bash
python -m alembic heads
```

Fix by creating a merge migration:

```bash
python -m alembic merge heads -m "Merge database heads"
python -m alembic upgrade head
```

## Example: Full Migration Cycle

```bash
# 1. Check current state
python -m alembic current
# Output: <base> (no revisions)

# 2. Make changes to models.py (e.g., add field)
# Add: resume_score = Column(Integer, nullable=True)

# 3. Generate migration
python -m alembic revision --autogenerate -m "Add resume_score field"
# Output: Generating alembic\versions\abc123_add_resume_score_field.py ... done

# 4. Review generated migration
# Edit alembic/versions/abc123_add_resume_score_field.py if needed

# 5. Apply migration
python -m alembic upgrade head
# Output: INFO  [alembic.runtime.migration] Running upgrade  -> abc123, Add resume_score field

# 6. Verify
python -m alembic current
# Output: abc123 (head)

# 7. If needed, rollback
python -m alembic downgrade -1
# Output: INFO  [alembic.runtime.migration] Running downgrade abc123 -> , Add resume_score field
```

## Integration with CI/CD

### In Deployment Scripts

```bash
# Apply migrations automatically during deployment
cd /path/to/backend
source venv/bin/activate
export POSTGRES_URL="${DATABASE_URL}"
python -m alembic upgrade head
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

### Docker

```dockerfile
# In Dockerfile
RUN pip install -r requirements.txt

# In docker-entrypoint.sh
python -m alembic upgrade head
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Comparison with Manual Migrations

### Old Approach (migrations/*.sql)
- ✅ Simple, easy to understand
- ❌ No automatic tracking
- ❌ Manual version management
- ❌ Risk of applying same migration twice
- ❌ No rollback support

### Alembic Approach
- ✅ Automatic revision tracking
- ✅ Built-in rollback support
- ✅ Auto-generate from models
- ✅ Version control friendly
- ✅ Supports branching and merging

## Additional Resources

- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [Alembic Tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)

## Support

For questions or issues with migrations:
1. Check this README
2. Review Alembic documentation
3. Check migration history: `python -m alembic history --verbose`
4. Contact the development team
