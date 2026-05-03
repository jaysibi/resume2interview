# Resume Tailor Database Design v2

## Overview
This design supports:
- Job seeker (user) details: name, email, phone
- Resume and job description uploads
- Job application tracking (which user applied to which job)
- ATS scoring and gap analysis storage
- Skills tracking (present and missing)
- Full reporting and analytics

---

## Entity-Relationship Diagram (ERD)

```
[users]───┬────────────┬───[resumes]
          │            └───[applications]───[job_descriptions]
          │                                 │
          │                                 ├──[gap_analyses]
          │                                 └──[ats_scores]
```

---

## Table Definitions

### 1. users
| Column         | Type         | Description                |
|---------------|--------------|----------------------------|
| id            | SERIAL (PK)  | Unique user ID             |
| name          | VARCHAR      | Full name                  |
| email         | VARCHAR      | Email address (unique)     |
| phone         | VARCHAR      | Phone number               |
| password_hash | VARCHAR      | Hashed password            |
| created_at    | TIMESTAMP    | Registration date          |

### 2. resumes
| Column      | Type         | Description                |
|-------------|--------------|----------------------------|
| id          | SERIAL (PK)  | Resume ID                  |
| user_id     | INT (FK)     | Owner (users.id)           |
| filename    | VARCHAR      | Original file name         |
| raw_text    | TEXT         | Extracted text             |
| skills      | JSON         | Extracted skills           |
| experience  | JSON         | Work experience            |
| education   | JSON         | Education history          |
| upload_date | TIMESTAMP    | Upload timestamp           |

### 3. job_descriptions
| Column      | Type         | Description                |
|-------------|--------------|----------------------------|
| id          | SERIAL (PK)  | JD ID                      |
| user_id     | INT (FK)     | Uploader (users.id)        |
| filename    | VARCHAR      | File name                  |
| raw_text    | TEXT         | JD text                    |
| upload_date | TIMESTAMP    | Upload timestamp           |

### 4. applications
| Column      | Type         | Description                |
|-------------|--------------|----------------------------|
| id          | SERIAL (PK)  | Application ID             |
| user_id     | INT (FK)     | Job seeker (users.id)      |
| resume_id   | INT (FK)     | Resume used                |
| jd_id       | INT (FK)     | Job applied to             |
| applied_at  | TIMESTAMP    | Application date           |
| status      | VARCHAR      | (optional) e.g. applied    |

### 5. gap_analyses
| Column                   | Type         | Description                |
|-------------------------|--------------|----------------------------|
| id                      | SERIAL (PK)  | Gap analysis ID            |
| application_id          | INT (FK)     | Application analyzed       |
| match_score             | INT          | 0-100 match %              |
| missing_required_skills | JSON         | List of missing skills     |
| missing_preferred_skills| JSON         | List of missing skills     |
| strengths               | JSON         | List of strengths          |
| weak_areas              | JSON         | List of weak areas         |
| recommendations         | JSON         | List of recommendations    |
| created_at              | TIMESTAMP    | Analysis date              |

### 6. ats_scores
| Column                | Type         | Description                |
|----------------------|--------------|----------------------------|
| id                   | SERIAL (PK)  | ATS score ID               |
| application_id       | INT (FK)     | Application analyzed       |
| ats_score            | INT          | 0-100 ATS %                |
| keyword_match_percentage | INT      | 0-100 keyword match %      |
| format_score         | INT          | 0-100 format score         |
| matched_keywords     | JSON         | List of matched keywords   |
| missing_keywords     | JSON         | List of missing keywords   |
| issues               | JSON         | List of issues             |
| recommendations      | JSON         | List of recommendations    |
| created_at           | TIMESTAMP    | Analysis date              |

---

## Example: Extracting a Report

To get a report for a user (job seeker):
- Join `users`, `applications`, `resumes`, `job_descriptions`, `gap_analyses`, `ats_scores`
- Example fields: name, email, phone, job title, resume skills, missing skills, ATS score, match score, recommendations

---

## Benefits
- **User-centric:** All data linked to users
- **History:** Track all applications and analyses
- **Reporting:** Easy to extract user/job/ATS/skills reports
- **Caching:** Avoid duplicate AI calls for same application
- **Analytics:** Track popular skills, job trends, user activity

---

## Future Extensions
- Add user roles (admin, recruiter, etc.)
- Add job status tracking (interview, offer, etc.)
- Add document versioning
- Add audit logs

---

**End of DB Design v2**
