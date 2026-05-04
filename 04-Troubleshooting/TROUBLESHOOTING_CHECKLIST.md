# ResumeTailor Troubleshooting Checklist

**Purpose:** Systematic root-cause diagnosis guide for the ResumeTailor project. Developer agents must execute each applicable step, record findings, and update this document as new issues are discovered.

**Project Layout:**
```
C:\Projects\ResumeTailor\
  01-Code\
    backend\          ← FastAPI app (port 8000), Python 3.x
    frontend\         ← React 19 + Vite app (port 5173)
  03-Testing\         ← Shared test assets (resume .docx, JD .txt)
  04-Troubleshooting\ ← This file + diagnostic test scripts
```

**Associated automated tests:** `test_troubleshooting_backend.py` (pytest) and `test_troubleshooting_frontend.spec.ts` (Playwright) in this folder.

---

## 1. Issue Identification

**Goal:** Capture the full context of the problem before any changes are made.

- [ ] Record the exact error message, including the full stack trace or terminal output.
- [ ] Note the component affected: `[ ] Backend` `[ ] Frontend` `[ ] DB` `[ ] E2E Tests`.
- [ ] Identify what changed recently: code, config, dependency version, environment variable, or port.
- [ ] Confirm the issue is reproducible — run the failing step twice to rule out transient errors.
- [ ] Check if the issue is environment-specific (dev vs. test vs. prod).

**Known recurring issues:**
- `index.html` `<title>` defaults to `frontend` — must be set to `Resume Tailor`.
- Backend `uvicorn` launch fails when port 8000 is already in use — use port 8001 or kill the existing process.
- `tailwind.config.js` missing causes styles to fail silently.

---

## 2. Environment & Dependency Verification

**Goal:** Confirm the runtime environment matches project requirements.

### Python / Backend
- [ ] Verify Python version: `python --version` → expect `3.10+`
- [ ] Verify venv is activated before running backend commands.
- [ ] Install/verify dependencies: `pip install -r C:\Projects\ResumeTailor\01-Code\backend\requirements.txt`
- [ ] Key packages must be present: `fastapi`, `uvicorn`, `sqlalchemy`, `psycopg2-binary`, `alembic`, `openai`, `pdfplumber`, `python-docx`, `beautifulsoup4`, `slowapi`
- [ ] Confirm `.env` exists at `C:\Projects\ResumeTailor\01-Code\backend\.env` and contains:
  - `OPENAI_API_KEY=...`
  - `DATABASE_URL=postgresql://...`
- [ ] Confirm `.env.example` is committed but `.env` is gitignored.

### Node / Frontend
- [ ] Verify Node version: `node --version` → expect `18+`
- [ ] Install/verify dependencies: `cd C:\Projects\ResumeTailor\01-Code\frontend; npm install`
- [ ] Key packages must be present in `node_modules/`: `react`, `react-router-dom`, `axios`, `@tanstack/react-query`
- [ ] Dev dependencies: `vite`, `@vitejs/plugin-react`, `tailwindcss`, `@tailwindcss/postcss`, `typescript`

### Playwright (E2E)
- [ ] Confirm Playwright is installed at root: `cd C:\Projects\ResumeTailor; npm install`
- [ ] Confirm browser binaries are installed: `npx playwright install chromium`

---

## 3. Build & Startup Checks

**Goal:** Confirm both services start without errors.

### Backend
- [ ] Start from the correct directory:
  ```powershell
  cd C:\Projects\ResumeTailor\01-Code\backend
  python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
  ```
- [ ] Expected output: `Uvicorn running on http://127.0.0.1:8000`
- [ ] If port 8000 is in use: `netstat -ano | findstr :8000` to find the PID, then `taskkill /PID <pid> /F`
- [ ] Confirm `main.py` imports cleanly (no `ModuleNotFoundError`).
- [ ] Confirm database tables are created: run `python init_db.py` if tables are missing.
- [ ] Run migrations if schema is out of date: `alembic upgrade head`

### Frontend
- [ ] Start from the correct directory:
  ```powershell
  cd C:\Projects\ResumeTailor\01-Code\frontend
  npm run dev
  ```
- [ ] Expected output: `VITE v*.* ready` and a local URL (default `http://localhost:5173`)
- [ ] If TypeScript compile errors appear, fix them before proceeding.
- [ ] If port 5173 is in use, Vite will auto-increment to 5174, 5175, etc. — update E2E test `baseURL` accordingly.

---

## 4. Static Asset & Entry Point Validation

**Goal:** Confirm the HTML entry point and static assets are correct before React boots.

- [ ] Open `C:\Projects\ResumeTailor\01-Code\frontend\index.html`.
  - `<title>` must be `Resume Tailor` (not the default `frontend`).
  - `<div id="root"></div>` must be present.
  - `<script type="module" src="/src/main.tsx"></script>` must be present.
- [ ] Confirm `C:\Projects\ResumeTailor\01-Code\frontend\src\main.tsx` renders `<App />` into `#root`.
- [ ] Confirm `public/favicon.svg` exists (referenced in `index.html`).
- [ ] Confirm `tailwind.config.js` exists at `C:\Projects\ResumeTailor\01-Code\frontend\tailwind.config.js`.
- [ ] Confirm `postcss.config.js` references `@tailwindcss/postcss`.

---

## 5. Frontend Rendering & Routing

**Goal:** Confirm the React app renders the expected UI in the browser.

- [ ] Open `http://localhost:5173/` in Chrome.
- [ ] Page `<title>` in browser tab must show `Resume Tailor` — not `frontend`.
- [ ] Landing page must render branding, headline, and a "Get Started" / CTA button.
- [ ] Browser DevTools Console must show zero red errors on initial load.
- [ ] Network tab must show no failed requests (no 404s on JS/CSS chunks).
- [ ] React HMR must be active (check Vite terminal output for `[vite] HMR ready`).
- [ ] Verify routes render correct components:
  | Route | Component |
  |---|---|
  | `/` | `LandingPage` |
  | `/upload` | `UploadPage` |
  | `/results` | `ResultsPage` |
  | `/applications` | `ApplicationsPage` |
  | `/applications/:id` | `ApplicationDetailPage` |
- [ ] Navigate to `/upload` and confirm the file upload input and URL input are visible.

---

## 6. API / Backend Connectivity

**Goal:** Confirm the frontend can reach the backend and key endpoints are healthy.

- [ ] Confirm backend is running on `http://127.0.0.1:8000`.
- [ ] Hit the health endpoint: `GET http://127.0.0.1:8000/` → expect `200 OK`.
- [ ] Check Swagger docs are accessible: `http://127.0.0.1:8000/docs`.
- [ ] Test resume upload endpoint: `POST /upload-resume` with a `.docx` file.
- [ ] Test JD fetch endpoint: `POST /fetch-jd` with a valid job URL.
- [ ] Test analysis endpoint: `POST /analyze` with `resume_id` and `job_description`.
- [ ] Verify CORS: frontend origin `http://localhost:5173` must be allowed in `main.py` `CORSMiddleware`.
- [ ] Check request headers in DevTools — no `CORS` or `Network Error` failures.
- [ ] Confirm `OPENAI_API_KEY` is loaded (check uvicorn startup logs for no `AuthenticationError`).

---

## 7. Database Connectivity & Schema

**Goal:** Confirm PostgreSQL is reachable and schema is up to date.

- [ ] Verify PostgreSQL is running: `pg_isready` or check service in Windows Services.
- [ ] Confirm `DATABASE_URL` in `.env` is correct and accessible.
- [ ] Run schema verification: `cd C:\Projects\ResumeTailor\01-Code\backend; python verify_v2_schema.py`
- [ ] Run data validation: `python validate_data.py`
- [ ] Check DB contents: `python check_db_contents.py`
- [ ] Run pending Alembic migrations if schema is missing tables: `alembic upgrade head`
- [ ] Confirm all V2 tables exist: `resumes`, `job_descriptions`, `analyses`, `applications`

---

## 8. Style & Asset Loading

**Goal:** Confirm Tailwind and CSS are loading correctly.

- [ ] Confirm `tailwind.config.js` has `content` paths targeting `./src/**/*.{ts,tsx}`.
- [ ] Confirm `postcss.config.js` uses `@tailwindcss/postcss` (Tailwind v4 pattern).
- [ ] In browser DevTools, inspect any element — Tailwind utility classes must be applied.
- [ ] Confirm `src/index.css` contains `@import "tailwindcss"` or equivalent directive.
- [ ] Check that no CSS chunk is returning 404 in the network tab.
- [ ] Verify no CSS-in-JS or runtime style errors appear in the console.

---

## 9. E2E Test Execution

**Goal:** Confirm the full user workflow passes end-to-end.

- [ ] Start backend on port 8000 and frontend on port 5173 before running tests.
- [ ] Confirm test resume file exists: `C:\Projects\ResumeTailor\03-Testing\Resume - Jayendra Sibi (1).docx`
- [ ] Run the Playwright E2E script from the correct directory:
  ```powershell
  cd C:\Projects\ResumeTailor\01-Code
  npx playwright test src/e2e_upload_and_analyze.spec.ts --reporter=list
  ```
- [ ] Expected: all steps pass — title check, file upload, URL input, submit, match score visible.
- [ ] On failure: capture screenshot at failure point (`await page.screenshot({ path: 'failure.png' })`).
- [ ] Run backend diagnostic tests:
  ```powershell
  cd C:\Projects\ResumeTailor\04-Troubleshooting
  pytest test_troubleshooting_backend.py -v
  ```
- [ ] Run frontend diagnostic tests:
  ```powershell
  cd C:\Projects\ResumeTailor\04-Troubleshooting
  npx playwright test test_troubleshooting_frontend.spec.ts --reporter=list
  ```

---

## 10. Logs & Error Reporting

**Goal:** Capture all diagnostic evidence before escalating.

- [ ] Copy full terminal output (uvicorn + npm dev) to a timestamped `.txt` file in `04-Troubleshooting/`.
- [ ] Export browser console errors (right-click Console → Save as).
- [ ] Capture network tab as HAR file for API failures.
- [ ] Record: Python version, Node version, OS, all relevant env vars (mask secrets).
- [ ] Save Playwright test output: `npx playwright test --reporter=html` then open `playwright-report/index.html`.

---

## 11. Escalation & Documentation

**Goal:** If unresolved after all steps above, escalate with complete evidence.

- [ ] Create an issue entry in `C:\Projects\ResumeTailor\project-progress-log.md` with:
  - Date and developer name
  - Exact symptoms and steps to reproduce
  - All steps taken from this checklist
  - Attached logs and screenshots
  - Current hypothesis for root cause
- [ ] Update this checklist with any new patterns discovered.
- [ ] If a fix is found, add it to the **Known Recurring Issues** section of Step 1.

---

## Known Issues Log

| Date | Component | Symptom | Root Cause | Fix |
|---|---|---|---|---|
| 2026-05-04 | Frontend | Page stuck on `frontend` title | `index.html` title not updated; React not mounting | Set `<title>Resume Tailor</title>` in `index.html`; confirm `#root` div and `main.tsx` `ReactDOM.createRoot` |
| 2026-05-04 | Frontend | Tailwind styles not applied | `tailwind.config.js` missing | Create `tailwind.config.js` with correct `content` paths |
| 2026-05-04 | Backend | `uvicorn` exits with code 1 | Port 8000 already bound by a previous process | Kill existing process: `netstat -ano \| findstr :8000` then `taskkill /PID <pid> /F` |
| 2026-05-04 | Backend | `pip install` fails | Python venv not activated | Activate venv before running `pip` commands |

---

## Version History
- v1.0 (2026-05-04): Initial generic checklist created.
- v2.0 (2026-05-04): Rebuilt with project-specific paths, commands, expected outputs, and known issues log.
