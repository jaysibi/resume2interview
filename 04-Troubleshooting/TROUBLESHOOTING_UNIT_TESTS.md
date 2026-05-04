# ResumeTailor Troubleshooting Unit Tests

**Purpose:** Executable diagnostic tests for each section of the Troubleshooting Checklist.
These are not generic templates — they are runnable test scripts targeting actual project paths, ports, and known failure modes.

---

## Test Files

| File | Runner | Covers Checklist Sections |
|---|---|---|
| `test_troubleshooting_backend.py` | `pytest` (Python) | 1 – Issue ID, 2 – Env/Deps, 3 – Build/Files, 6 – API, 7 – Database |
| `test_troubleshooting_frontend.spec.ts` | `playwright` (TypeScript) | 4 – Static Assets, 5 – Rendering/Routing, 6 – API CORS, 7 – Styles, 9 – E2E Readiness |

---

## Prerequisites

### Backend Tests
```powershell
# Activate your Python virtual environment first
cd C:\Projects\ResumeTailor\01-Code\backend
pip install -r requirements.txt

# (Optional) Start backend for live connectivity tests
python -m uvicorn main:app --host 127.0.0.1 --port 8000
```

### Frontend Tests
```powershell
# Install root-level Playwright (already done if node_modules exists)
cd C:\Projects\ResumeTailor
npm install

# Install browser binaries
npx playwright install chromium

# Start frontend dev server (keep running in background)
cd C:\Projects\ResumeTailor\01-Code\frontend
npm run dev
```

---

## How to Run

### Run backend diagnostics
```powershell
cd C:\Projects\ResumeTailor\04-Troubleshooting
pytest test_troubleshooting_backend.py -v
```

### Run frontend diagnostics
```powershell
cd C:\Projects\ResumeTailor\04-Troubleshooting
npx playwright test test_troubleshooting_frontend.spec.ts --reporter=list
```

### Run both together
```powershell
cd C:\Projects\ResumeTailor\04-Troubleshooting
pytest test_troubleshooting_backend.py -v
npx playwright test test_troubleshooting_frontend.spec.ts --reporter=list
```

---

## Test Coverage Map

### `test_troubleshooting_backend.py`

| Class | Tests | Checklist Item |
|---|---|---|
| `TestIssueIdentification` | Python version ≥ 3.10, backend/frontend/testing dirs exist, resume asset exists | §1 – Issue ID |
| `TestDependencyVerification` | All 14 required packages importable, `.env` exists + has `OPENAI_API_KEY` + `DATABASE_URL`, `requirements.txt` exists | §2 – Env/Deps |
| `TestBuildAndStartup` | 11 core backend files exist, `parsers/` dir, `resume_parser.py`, `jd_parser.py`, `migrations/` dir | §3 – Build |
| `TestBackendConnectivity` | Root 200, `/docs` 200, `/openapi.json` valid, `/upload-resume` endpoint exists, `/analyze` endpoint exists, `/fetch-jd` endpoint exists, CORS header for frontend origin | §6 – API |
| `TestDatabaseConnectivity` | `DATABASE_URL` configured, PostgreSQL reachable, V2 tables exist (`resumes`, `job_descriptions`, `analyses`, `applications`), `resumes` table has seed data | §7 – DB |

### `test_troubleshooting_frontend.spec.ts`

| Describe Block | Tests | Checklist Item |
|---|---|---|
| Static Asset Validation | `index.html` exists, title is `Resume Tailor`, `#root` div, `main.tsx` script tag, `tailwind.config.js`, `postcss.config.js`, `vite.config.ts`, resume asset, `package.json` deps | §4 – Assets |
| Frontend Rendering & Routing | Dev server 200, title check, `#root` not empty, visible content, zero JS errors, zero 404s, `/` renders landing page CTA, `/upload` has file input + URL input + submit button, `/applications` renders, unknown route doesn't crash | §5 – Rendering |
| Style & Asset Loading | Tailwind utility classes applied, no CSS/JS 404s | §7 – Styles |
| Backend API Connectivity | Root 200, `/openapi.json` valid, CORS header present | §6 – API (browser-side) |
| E2E Test Readiness | Playwright in `package.json`, spec file exists, frontend accessible, upload page navigable from CTA | §9 – E2E |

---

## Interpreting Results

| Outcome | Action |
|---|---|
| `PASSED` | That checklist item is confirmed healthy. |
| `FAILED` | Root cause identified — read the assertion message for the exact fix. |
| `SKIPPED` | Prerequisite not met (e.g. backend not running). Start the dependency and re-run. |

---

## Notes on Live Tests
- **Backend connectivity tests** (`TestBackendConnectivity`, `Section 6 – Backend API`) are automatically `SKIPPED` if the backend is not running. Start uvicorn first, then re-run.
- **Database tests** (`TestDatabaseConnectivity`) are automatically `SKIPPED` if `DATABASE_URL` is not configured or PostgreSQL is unreachable.
- This design means you can run the full suite at any time without false failures from missing services.

---

## Version History
- v1.0 (2026-05-04): Generic test template placeholders created.
- v2.0 (2026-05-04): Replaced with actual executable test files covering all checklist sections with project-specific paths, commands, and known failure modes.
