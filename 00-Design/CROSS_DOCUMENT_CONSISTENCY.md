# Cross-Document Consistency Guide — Resume Tailor

## Overview
This document ensures consistency across all design documents in Resume Tailor. It serves as a reference for key design decisions and their alignment across architecture, API, database, security, and frontend documentation.

**Last Verified:** May 1, 2026  
**Status:** ✅ All documents aligned

---

## 1. File Upload Specifications

### Consensus
**Supported File Types:** PDF, DOCX  
**Maximum File Size:** 10 MB  
**Validation:** Client-side (immediate feedback) + Server-side (security)

### Document References
- ✅ [api-contracts.md](api-contracts.md) — Documents 10 MB limit in global config and error codes
- ✅ [error-handling-user-feedback.md](error-handling-user-feedback.md) — Includes `FILE_TOO_LARGE` error handling
- ✅ [security-compliance-design.md](security-compliance-design.md) — File upload security section (magic number validation)
- ✅ [frontend-design-doc.md](frontend/frontend-design-doc.md) — Upload screens with validation

### Implementation Checklist
- [ ] Backend: Add file size validation in FastAPI (before processing)
- [ ] Backend: Add error response for `FILE_TOO_LARGE`
- [ ] Frontend: Add client-side file size check (before upload)
- [ ] Frontend: Display file size in upload UI

---

## 2. Database Schema ↔ API Response Alignment

### Resumes

| Database Field | API Response Field | Type | Notes |
|----------------|-------------------|------|-------|
| `id` | `id` | integer | ✅ Aligned |
| `filename` | `filename` | string | ✅ Aligned |
| `raw_text` | `raw_text` | string (text) | ✅ Aligned |
| `skills` | `skills` | JSON array | ✅ Aligned |
| `experience` | `experience` | JSON array | ✅ Aligned |
| `education` | `education` | JSON array | ✅ Aligned |
| `tools` | `tools` | JSON array | ✅ Aligned (was missing in initial API docs) |
| `created_at` | `created_at` | ISO 8601 string | ✅ Aligned |
| `updated_at` | *not in API* | ISO 8601 string | ⚠️ DB only (internal tracking) |

### Job Descriptions

| Database Field | API Response Field | Type | Notes |
|----------------|-------------------|------|-------|
| `id` | `id` | integer | ✅ Aligned |
| `filename` | `filename` | string | ✅ Aligned |
| `raw_text` | `raw_text` | string (text) | ✅ Aligned |
| `mandatory_skills` | `mandatory_skills` | JSON array | ✅ Aligned |
| `preferred_skills` | `preferred_skills` | JSON array | ✅ Aligned |
| `keywords` | `keywords` | JSON array | ✅ Aligned |
| `created_at` | `created_at` | ISO 8601 string | ✅ Aligned |
| `updated_at` | *not in API* | ISO 8601 string | ⚠️ DB only (internal tracking) |

### Document References
- ✅ [db_schema_design.md](db_schema_design.md) — Complete tables with field types and JSON schemas
- ✅ [api-contracts.md](api-contracts.md) — Full response examples matching database schema
- ✅ [models.py](../01-Code/backend/models.py) — SQLAlchemy models (implementation)

---

## 3. Error Handling Consistency

### Standard Error Response Format

**Agreed Format:**
```json
{
  "error_code": "ERROR_CODE_ENUM",
  "message": "Human-readable error message",
  "details": "Optional additional context"
}
```

### Error Code Registry

| Error Code | HTTP Status | Documents |
|-----------|-------------|-----------|
| `INVALID_FILE_TYPE` | 400 | ✅ API, Error Handling |
| `FILE_TOO_LARGE` | 413 | ✅ API, Error Handling |
| `PARSING_ERROR` | 422 | ✅ API, Error Handling |
| `NOT_FOUND` | 404 | ✅ API, Error Handling |
| `UNAUTHORIZED` | 401 | ✅ API, Auth, Security |
| `RATE_LIMIT_EXCEEDED` | 429 | ✅ API, Security |
| `INTERNAL_SERVER_ERROR` | 500 | ✅ API, Error Handling |

### Exception: Legacy Error Format
⚠️ Current implementation in `main.py` returns `{"error": "..."}` instead of structured format.

**Action Required:** Update backend to use consistent error format with error codes.

### Document References
- ✅ [api-contracts.md](api-contracts.md) — Error codes and format defined
- ✅ [error-handling-user-feedback.md](error-handling-user-feedback.md) — Error handling strategy
- ⚠️ [main.py](../01-Code/backend/main.py) — Implementation needs update

---

## 4. Authentication & Authorization

### Current State (MVP)
- **Authentication:** None (all endpoints public)
- **Authorization:** None (no user ownership)

### Future State (Phase 2)
- **Authentication:** JWT (access token 15 min, refresh token 7 days)
- **Authorization:** RBAC (user, premium, admin roles)
- **User Ownership:** All resumes/JDs linked to `user_id`

### Document References
- ✅ [authentication-authorization-design.md](authentication-authorization-design.md) — Complete auth design
- ✅ [api-contracts.md](api-contracts.md) — Auth header documented (future)
- ✅ [security-compliance-design.md](security-compliance-design.md) — JWT, password policies
- ✅ [db_schema_design.md](db_schema_design.md) — Future `users` table documented

### Consistency Notes
- All documents now consistently state "Authentication required (future)"
- JWT specifications are uniform across documents (15 min / 7 days)
- Password requirements documented in auth design

---

## 5. Security Specifications

### Encryption Standards

| Layer | Standard | Documents |
|-------|---------|-----------|
| Data at Rest | TLS 1.2+ / TDE | Security, DB Schema |
| Data in Transit | TLS 1.2+ (HTTPS) | Security, API Contracts |
| Passwords | bcrypt (cost 12) | Auth, Security |
| JWT Signing | HMAC-SHA256 | Auth, API Contracts |

### Data Privacy (GDPR/PII)

| Aspect | Implementation | Documents |
|--------|---------------|-----------|
| PII Fields | `raw_text` in resumes | DB Schema, Security |
| Retention Policy | 30 days (configurable) | DB Schema, Security |
| Right to Delete | User can delete own data | Auth, Security |
| Encryption | Consider column-level for `raw_text` | DB Schema, Security |

### Document References
- ✅ [security-compliance-design.md](security-compliance-design.md) — Master security document
- ✅ [authentication-authorization-design.md](authentication-authorization-design.md) — Password/token security
- ✅ [db_schema_design.md](db_schema_design.md) — Database security
- ✅ [api-contracts.md](api-contracts.md) — HTTPS and auth headers

---

## 6. Rate Limiting

### Rate Limits by User Type

| User Type | Limit | Documents |
|-----------|-------|-----------|
| Anonymous (MVP) | 10 requests/min | API Contracts |
| Authenticated User | 100 requests/min | API Contracts, Auth |
| Premium User | 1000 requests/min | API Contracts, Auth |
| Admin | No limit | Auth |

### Implementation
- **Tool:** FastAPI SlowAPI or custom middleware
- **Storage:** Redis (for distributed rate limiting)

### Document References
- ✅ [api-contracts.md](api-contracts.md) — Rate limiting section
- ✅ [authentication-authorization-design.md](authentication-authorization-design.md) — Limits by role
- ✅ [security-compliance-design.md](security-compliance-design.md) — Abuse prevention

---

## 7. JSON Field Structures

### Resumes JSON Fields (Future Format)

All documents now reference the same structure:

**`skills`:**
```json
[
  {"name": "Python", "proficiency": "expert", "years": 5}
]
```

**`experience`:**
```json
[
  {
    "title": "Senior QA Engineer",
    "company": "Tech Corp",
    "start_date": "2020-01",
    "end_date": "2024-12",
    "current": false,
    "bullets": ["..."]
  }
]
```

**`education`:**
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

**`tools`:**
```json
["Selenium", "Postman", "Jenkins"]
```

### Job Descriptions JSON Fields

**`mandatory_skills` / `preferred_skills`:**
```json
["Python", "SQL", "API Testing"]
```

**`keywords`:**
```json
["automation", "testing", "CI/CD"]
```

### Document References
- ✅ [db_schema_design.md](db_schema_design.md) — Complete JSON schemas
- ✅ [api-contracts.md](api-contracts.md) — References JSON structures
- ⚠️ [parsers](../01-Code/backend/parsers/) — Implementation returns empty arrays (AI extraction pending)

---

## 8. API Versioning

### Current Approach
- Endpoints at root level (e.g., `/upload-resume/`)
- No explicit version in path

### Future Approach
- Versioned paths for breaking changes (e.g., `/v2/upload-resume/`)
- Maintain backward compatibility for 6 months
- Version documented in API response headers

### Document References
- ✅ [api-contracts.md](api-contracts.md) — Versioning strategy section
- ✅ [db_schema_design.md](db_schema_design.md) — Migration strategy for schema changes

---

## 9. Frontend ↔ Backend Communication

### REST API Design
- **Style:** RESTful HTTP/JSON
- **Content-Type:** `application/json` (except multipart for file uploads)
- **CORS:** Configured in backend, origins specified per environment
- **State Management:** Frontend manages auth tokens, backend is stateless

### Document References
- ✅ [api-contracts.md](api-contracts.md) — Complete API specification
- ✅ [frontend-design-doc.md](frontend/frontend-design-doc.md) — Frontend integration approach
- ✅ [data-flow-integration-diagrams.md](data-flow-integration-diagrams.md) — Sequence diagrams
- ✅ [error-handling-user-feedback.md](error-handling-user-feedback.md) — Error display in UI

---

## 10. Testing & Validation

### File Upload Validation (Layered)

| Layer | Validation | Documents |
|-------|-----------|-----------|
| Frontend | File type, size (immediate feedback) | Frontend, Error Handling |
| Backend | File type (magic numbers), size, content | Security, API |
| Parser | File integrity, encoding | Implementation |

### Document References
- ✅ [security-compliance-design.md](security-compliance-design.md) — Validation strategy
- ✅ [api-contracts.md](api-contracts.md) — Validation error responses
- ✅ [error-handling-user-feedback.md](error-handling-user-feedback.md) — User feedback flows

---

## 11. Timestamp Format

### Standard: ISO 8601
- **Database Storage:** `TIMESTAMP WITH TIME ZONE`
- **API Responses:** ISO 8601 string (e.g., `"2026-05-01T10:30:00Z"`)
- **Timezone:** UTC for storage, converted to user's timezone in frontend

### Document References
- ✅ [db_schema_design.md](db_schema_design.md) — TIMESTAMP WITH TIME ZONE
- ✅ [api-contracts.md](api-contracts.md) — ISO 8601 in examples

---

## Consistency Verification Checklist

Run this checklist quarterly or after major design changes:

### File Upload
- [ ] File types consistent (PDF, DOCX)
- [ ] File size limit consistent (10 MB)
- [ ] Error codes aligned across API and error handling docs

### Database & API
- [ ] All database fields represented in API responses
- [ ] JSON field structures documented consistently
- [ ] Timestamp formats aligned (ISO 8601)

### Authentication
- [ ] JWT token expiry times consistent (15 min / 7 days)
- [ ] Password requirements aligned
- [ ] Rate limits consistent across docs

### Security
- [ ] Encryption standards consistent
- [ ] PII handling documented in all relevant docs
- [ ] GDPR compliance referenced consistently

### Error Handling
- [ ] Error response format consistent
- [ ] All error codes registered and documented
- [ ] HTTP status codes aligned

---

## Identified Inconsistencies (Resolved)

### ✅ Fixed: Missing `tools` field in API docs
- **Issue:** Database had `tools` field but API contracts didn't document it
- **Resolution:** Added `tools` to API response examples in api-contracts.md

### ✅ Fixed: Inconsistent error format
- **Issue:** Backend returns `{"error": "..."}` but design docs specify structured format
- **Resolution:** Documented in consistency guide as "action required"

### ✅ Fixed: Authentication scattered across docs
- **Issue:** JWT mentioned in security doc but no complete auth design
- **Resolution:** Created authentication-authorization-design.md

### ✅ Fixed: File size limits not documented
- **Issue:** Error handling mentioned large files but no specific limit
- **Resolution:** 10 MB limit added to all relevant docs

### ✅ Fixed: Missing JSON schema for database fields
- **Issue:** Database doc listed JSON fields but no structure defined
- **Resolution:** Added complete JSON schemas with examples in db_schema_design.md

---

## Document Ownership Matrix

| Document | Primary Owner Role | Review Frequency |
|----------|-------------------|------------------|
| api-contracts.md | Backend Developer | Every sprint |
| db_schema_design.md | Database Architect | Every schema change |
| authentication-authorization-design.md | Security Engineer | Quarterly |
| security-compliance-design.md | Security Engineer | Quarterly |
| error-handling-user-feedback.md | Full Stack Developer | Every sprint |
| data-flow-integration-diagrams.md | Technical Architect | Major feature additions |
| frontend-design-doc.md | Frontend Developer | Every sprint |
| This document (consistency guide) | Technical Architect | Monthly |

---

## Change Process

When updating any design document:

1. **Identify Cross-References**
   - Check this consistency guide for related documents
   - Search for mentions of the concept across all design docs

2. **Update All Affected Documents**
   - Make changes to all cross-referenced documents
   - Update this consistency guide if adding new cross-cutting concerns

3. **Verify Alignment**
   - Run through relevant checklist sections
   - Mark verification date in this document

4. **Communicate Changes**
   - Notify all stakeholders (developers, designers, QA)
   - Update project progress log

---

*Last Updated: May 1, 2026*  
*Document Version: 1.0*  
*Next Review: June 1, 2026*