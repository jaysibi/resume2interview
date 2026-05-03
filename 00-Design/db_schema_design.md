# Database Schema Design for Resume Tailor (PostgreSQL)

## Entities & Relationships

### 1. `resumes` Table

Stores uploaded resumes and their parsed data.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique resume identifier |
| `filename` | VARCHAR(255) | NOT NULL | Original filename (e.g., "john_doe_resume.pdf") |
| `raw_text` | TEXT | NOT NULL | Full text extracted from resume file |
| `skills` | JSON | DEFAULT '[]' | Extracted skills (array of strings or objects) |
| `experience` | JSON | DEFAULT '[]' | Work experience entries (array of objects) |
| `education` | JSON | DEFAULT '[]' | Education entries (array of objects) |
| `tools` | JSON | DEFAULT '[]' | Tools and technologies (array of strings) |
| `created_at` | TIMESTAMP WITH TIME ZONE | DEFAULT NOW() | Timestamp of resume upload |
| `updated_at` | TIMESTAMP WITH TIME ZONE | DEFAULT NOW(), ON UPDATE NOW() | Timestamp of last update |

**Indexes:**
- Primary key on `id` (automatically indexed)
- Index on `created_at` for time-based queries
- Optional: Full-text search index on `raw_text` for search functionality

---

### 2. `job_descriptions` Table

Stores uploaded job descriptions and their parsed data.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique job description identifier |
| `filename` | VARCHAR(255) | NOT NULL | Original filename (e.g., "senior_qa_jd.pdf") |
| `raw_text` | TEXT | NOT NULL | Full text extracted from JD file |
| `mandatory_skills` | JSON | DEFAULT '[]' | Required skills (array of strings) |
| `preferred_skills` | JSON | DEFAULT '[]' | Preferred/nice-to-have skills (array of strings) |
| `keywords` | JSON | DEFAULT '[]' | ATS keywords (array of strings) |
| `created_at` | TIMESTAMP WITH TIME ZONE | DEFAULT NOW() | Timestamp of JD upload |
| `updated_at` | TIMESTAMP WITH TIME ZONE | DEFAULT NOW(), ON UPDATE NOW() | Timestamp of last update |

**Indexes:**
- Primary key on `id` (automatically indexed)
- Index on `created_at` for time-based queries
- Optional: Full-text search index on `raw_text` for search functionality

---

## JSON Field Schemas

### `skills` Field (resumes table)
Array of skill objects or strings. Future implementation will standardize to objects.

**Current Format:**
```json
[]
```

**Future Format (with AI extraction):**
```json
[
  {
    "name": "Python",
    "proficiency": "expert",
    "years": 5
  },
  {
    "name": "FastAPI",
    "proficiency": "intermediate",
    "years": 2
  }
]
```

---

### `experience` Field (resumes table)
Array of work experience objects.

**Current Format:**
```json
[]
```

**Future Format:**
```json
[
  {
    "title": "Senior QA Engineer",
    "company": "Tech Corp",
    "location": "San Francisco, CA",
    "start_date": "2020-01",
    "end_date": "2024-12",
    "current": false,
    "bullets": [
      "Led automation testing for enterprise app",
      "Reduced defects by 40% through comprehensive test strategies"
    ]
  }
]
```

---

### `education` Field (resumes table)
Array of education objects.

**Current Format:**
```json
[]
```

**Future Format:**
```json
[
  {
    "degree": "Bachelor of Science",
    "field": "Computer Science",
    "institution": "University of California",
    "graduation_year": 2016,
    "gpa": 3.8
  }
]
```

---

### `tools` Field (resumes table)
Array of tools and technologies.

**Current Format:**
```json
[]
```

**Future Format:**
```json
["Selenium", "Postman", "Jenkins", "Docker", "Kubernetes"]
```

---

### `mandatory_skills` & `preferred_skills` Fields (job_descriptions table)
Arrays of required and preferred skills.

**Current Format:**
```json
[]
```

**Future Format:**
```json
["Python", "SQL", "API Testing", "Agile Methodology"]
```

---

### `keywords` Field (job_descriptions table)
Array of ATS-relevant keywords extracted from job description.

**Current Format:**
```json
[]
```

**Future Format:**
```json
["automation", "testing", "CI/CD", "quality assurance", "SDLC"]
```

---

## Design Rationale

### Why JSON Fields?
- **Flexibility:** Resume structures vary widely; JSON allows semi-structured data without rigid schema
- **Schema Evolution:** Easy to add new fields without database migrations
- **Performance:** PostgreSQL has native JSON support with indexing and querying capabilities
- **Future-Proof:** As AI extraction improves, JSON can accommodate richer data structures

### Timestamps
- `created_at`: Tracks when resume/JD was uploaded (immutable)
- `updated_at`: Tracks last modification (future use for re-parsing or editing)

### Separation of Tables
- Independent management of resumes and job descriptions
- Allows linking through future junction table for match history
- Easier to scale and optimize separately

---

## Relationships (Future)

### Planned: `resume_jd_matches` Table
To track resume-JD comparisons and scoring history:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INTEGER | PRIMARY KEY | Unique match ID |
| `resume_id` | INTEGER | FOREIGN KEY → resumes.id | Resume being analyzed |
| `jd_id` | INTEGER | FOREIGN KEY → job_descriptions.id | Target job description |
| `ats_score` | INTEGER | CHECK (0-100) | ATS compatibility score |
| `keyword_match` | INTEGER | CHECK (0-100) | Keyword match percentage |
| `missing_skills` | JSON | | Skills present in JD but not in resume |
| `matched_skills` | JSON | | Skills matched between resume and JD |
| `created_at` | TIMESTAMP | DEFAULT NOW() | When analysis was performed |

**Relationships:**
```
resumes (1) ←→ (N) resume_jd_matches (N) ←→ (1) job_descriptions
```

---

## Security & Compliance

### Data Protection
- **Encryption at Rest:** Use PostgreSQL transparent data encryption (TDE) or OS-level encryption
- **Encryption in Transit:** Always use SSL/TLS for database connections
- **PII Handling:** `raw_text` contains personally identifiable information (names, contact info)
  - Consider encryption for `raw_text` column
  - Implement data retention policies (auto-delete after N days)
  - Support GDPR right-to-deletion

### Access Control
- Application connects with limited user permissions (no DROP/ALTER privileges)
- Separate read-only user for analytics queries
- Audit logging for data access and modifications

---

## Performance Optimization

### Indexing Strategy
```sql
-- Primary indexes (automatically created)
CREATE INDEX idx_resumes_created_at ON resumes(created_at DESC);
CREATE INDEX idx_jd_created_at ON job_descriptions(created_at DESC);

-- Full-text search (if needed)
CREATE INDEX idx_resumes_text_search ON resumes USING gin(to_tsvector('english', raw_text));
CREATE INDEX idx_jd_text_search ON job_descriptions USING gin(to_tsvector('english', raw_text));

-- JSON field indexes (for future queries)
CREATE INDEX idx_resumes_skills ON resumes USING gin(skills);
```

### Query Optimization
- Use connection pooling (SQLAlchemy handles this automatically)
- Limit result sets with pagination
- Use `EXPLAIN ANALYZE` for slow queries
- Consider materialized views for complex aggregations

---

## Backup & Recovery

### Backup Strategy
- **Full Backup:** Daily at 2 AM UTC
- **Incremental Backup:** Every 6 hours
- **Retention:** 30 days for daily backups, 7 days for incremental
- **Offsite Storage:** Replicate backups to cloud storage (S3/Azure Blob)

### Recovery Plan
- **RPO (Recovery Point Objective):** 6 hours max data loss
- **RTO (Recovery Time Objective):** 1 hour max downtime
- **Testing:** Monthly backup restoration tests

---

## Migration Strategy

### Using Alembic (SQLAlchemy's migration tool)

**Initialize migrations:**
```bash
alembic init alembic
```

**Create migration:**
```bash
alembic revision -m "Add updated_at to resumes and job_descriptions"
```

**Apply migration:**
```bash
alembic upgrade head
```

**Rollback:**
```bash
alembic downgrade -1
```

### Migration Best Practices
- All schema changes through migrations (never manual SQL)
- Test migrations in dev/staging before production
- Always write both `upgrade()` and `downgrade()` functions
- Version control all migration files

---

## Implementation Details

### Connection Configuration
- **Database Name:** `resumetailor`
- **Host:** `localhost` (development), managed service in production
- **Port:** `5432`
- **Username:** `postgres` (dev), separate app user in production
- **Password:** Environment variable `DB_PASSWORD`
- **Connection String:**
  ```
  postgresql+psycopg2://postgres:${DB_PASSWORD}@localhost:5432/resumetailor
  ```

### Connection Pool Settings (Production)
```python
engine = create_engine(
    DATABASE_URL,
    pool_size=20,          # Max connections in pool
    max_overflow=10,       # Max overflow connections
    pool_timeout=30,       # Timeout for getting connection
    pool_recycle=3600,     # Recycle connections after 1 hour
    pool_pre_ping=True     # Verify connection health before use
)
```

### Table Creation
Tables are created via SQLAlchemy ORM models in `models.py`. Initialize with:
```bash
cd 01-Code/backend
python init_db.py
```

---

## Future Extensions

### Phase 2 (Post-MVP)
1. **`users` table** — User accounts and authentication
2. **`resume_jd_matches` table** — Match history and scoring
3. **`audit_logs` table** — Track all data modifications
4. **`api_usage` table** — Track API calls for billing/analytics

### Phase 3 (Scaling)
1. Read replicas for analytics queries
2. Partitioning for large tables (by date)
3. Caching layer (Redis) for frequent queries
4. Archive old resumes to cold storage (S3 Glacier)

---

*Last Updated: May 1, 2026*  
*Document Version: 2.0*  
*Status: Implemented (Phase 1)*
