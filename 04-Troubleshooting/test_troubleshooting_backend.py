"""
ResumeTailor Backend Diagnostic Tests
======================================
Covers Checklist Sections 1-3, 6-7 (Environment, Build, API, Database).

Run from project root or this folder:
    cd C:\\Projects\\ResumeTailor\\04-Troubleshooting
    pytest test_troubleshooting_backend.py -v

Requirements: pytest, httpx, psycopg2-binary, python-dotenv
All packages are already in backend/requirements.txt.
"""

import os
import sys
import subprocess
import importlib
import importlib.util
from pathlib import Path

import pytest
import httpx

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BACKEND_DIR = Path("C:/Projects/ResumeTailor/01-Code/backend")
FRONTEND_DIR = Path("C:/Projects/ResumeTailor/01-Code/frontend")
TESTING_DIR = Path("C:/Projects/ResumeTailor/03-Testing")
ENV_FILE = BACKEND_DIR / ".env"
ENV_EXAMPLE_FILE = BACKEND_DIR / ".env.example"
REQUIREMENTS_FILE = BACKEND_DIR / "requirements.txt"
BACKEND_MAIN = BACKEND_DIR / "main.py"

BACKEND_URL = "http://127.0.0.1:8000"


# ===========================================================================
# Section 1 – Issue Identification (Environment sanity)
# ===========================================================================
class TestIssueIdentification:
    """Confirm diagnostic tooling and environment metadata are accessible."""

    def test_python_version_is_310_or_higher(self):
        """Python 3.10+ is required by the project."""
        major, minor = sys.version_info.major, sys.version_info.minor
        assert major == 3 and minor >= 10, (
            f"Python 3.10+ required. Found {major}.{minor}. "
            "Activate the correct virtual environment."
        )

    def test_backend_directory_exists(self):
        """backend/ source directory must be present."""
        assert BACKEND_DIR.exists(), f"Backend directory not found: {BACKEND_DIR}"

    def test_frontend_directory_exists(self):
        """frontend/ source directory must be present."""
        assert FRONTEND_DIR.exists(), f"Frontend directory not found: {FRONTEND_DIR}"

    def test_test_assets_directory_exists(self):
        """03-Testing/ directory with shared test assets must exist."""
        assert TESTING_DIR.exists(), f"Testing assets directory not found: {TESTING_DIR}"

    def test_resume_test_file_exists(self):
        """Sample resume .docx must be present for E2E tests."""
        resume = TESTING_DIR / "Resume - Jayendra Sibi (1).docx"
        assert resume.exists(), f"Resume test file missing: {resume}"


# ===========================================================================
# Section 2 – Environment & Dependency Verification
# ===========================================================================
class TestDependencyVerification:
    """Confirm all required Python packages are importable."""

    REQUIRED_PACKAGES = [
        "fastapi",
        "uvicorn",
        "sqlalchemy",
        "psycopg2",
        "alembic",
        "openai",
        "pdfplumber",
        "docx",          # python-docx exposes as 'docx'
        "bs4",           # beautifulsoup4
        "slowapi",
        "httpx",
        "pytest",
        "dotenv",        # python-dotenv
        "pydantic",
    ]

    @pytest.mark.parametrize("package", REQUIRED_PACKAGES)
    def test_required_package_importable(self, package):
        """Every required package must be importable."""
        spec = importlib.util.find_spec(package)
        assert spec is not None, (
            f"Package '{package}' is not installed. "
            f"Run: pip install -r {REQUIREMENTS_FILE}"
        )

    def test_requirements_file_exists(self):
        """requirements.txt must exist in the backend directory."""
        assert REQUIREMENTS_FILE.exists(), f"requirements.txt not found: {REQUIREMENTS_FILE}"

    def test_env_file_exists(self):
        """Backend .env file must be present (it is gitignored)."""
        assert ENV_FILE.exists(), (
            f".env file not found at {ENV_FILE}. "
            "Copy .env.example and fill in your credentials."
        )

    def test_env_example_file_exists(self):
        """.env.example must be committed so new developers can onboard."""
        assert ENV_EXAMPLE_FILE.exists(), f".env.example not found: {ENV_EXAMPLE_FILE}"

    def test_env_contains_openai_api_key(self):
        """OPENAI_API_KEY must be set in .env."""
        if not ENV_FILE.exists():
            pytest.skip(".env not found — skipping key check")
        content = ENV_FILE.read_text()
        assert "OPENAI_API_KEY=" in content, (
            "OPENAI_API_KEY is missing from .env. AI analysis calls will fail."
        )
        # Ensure it is not an empty value
        for line in content.splitlines():
            if line.startswith("OPENAI_API_KEY="):
                value = line.split("=", 1)[1].strip()
                assert value, "OPENAI_API_KEY is defined but has no value in .env"

    def test_env_contains_database_url(self):
        """DATABASE_URL must be set in .env."""
        if not ENV_FILE.exists():
            pytest.skip(".env not found — skipping key check")
        content = ENV_FILE.read_text()
        assert "DATABASE_URL=" in content, (
            "DATABASE_URL is missing from .env. Database connections will fail."
        )
        for line in content.splitlines():
            if line.startswith("DATABASE_URL="):
                value = line.split("=", 1)[1].strip()
                assert value, "DATABASE_URL is defined but has no value in .env"


# ===========================================================================
# Section 3 – Build & Startup Checks
# ===========================================================================
class TestBuildAndStartup:
    """Confirm backend source files are importable and structurally sound."""

    REQUIRED_BACKEND_FILES = [
        "main.py",
        "models.py",
        "models_v2.py",
        "crud_v2.py",
        "db.py",
        "ai_service.py",
        "ai_models.py",
        "job_scraper.py",
        "prompts.py",
        "alembic.ini",
        "requirements.txt",
    ]

    @pytest.mark.parametrize("filename", REQUIRED_BACKEND_FILES)
    def test_required_backend_file_exists(self, filename):
        """All core backend source files must be present."""
        filepath = BACKEND_DIR / filename
        assert filepath.exists(), f"Required backend file missing: {filepath}"

    def test_parsers_directory_exists(self):
        """parsers/ directory must exist with resume and JD parsers."""
        parsers_dir = BACKEND_DIR / "parsers"
        assert parsers_dir.exists(), f"parsers/ directory missing: {parsers_dir}"

    def test_resume_parser_exists(self):
        resume_parser = BACKEND_DIR / "parsers" / "resume_parser.py"
        assert resume_parser.exists(), f"resume_parser.py missing: {resume_parser}"

    def test_jd_parser_exists(self):
        jd_parser = BACKEND_DIR / "parsers" / "jd_parser.py"
        assert jd_parser.exists(), f"jd_parser.py missing: {jd_parser}"

    def test_migrations_directory_exists(self):
        """Alembic migrations directory must be present."""
        migrations = BACKEND_DIR / "migrations"
        assert migrations.exists(), f"migrations/ directory missing: {migrations}"

    def test_alembic_env_exists(self):
        """migrations/env.py must be present for Alembic to work."""
        alembic_env = BACKEND_DIR / "migrations" / "env.py"
        assert alembic_env.exists(), f"migrations/env.py missing: {alembic_env}"


# ===========================================================================
# Section 6 – API / Backend Connectivity
# ===========================================================================
class TestBackendConnectivity:
    """
    Live connectivity tests — require backend to be running on port 8000.
    Start backend: cd 01-Code/backend && python -m uvicorn main:app --port 8000

    Tests are skipped automatically if the backend is not reachable.
    """

    @pytest.fixture(autouse=True)
    def skip_if_backend_down(self):
        """Skip all live tests gracefully if backend is not running."""
        try:
            httpx.get(f"{BACKEND_URL}/", timeout=3)
        except (httpx.ConnectError, httpx.TimeoutException):
            pytest.skip(
                f"Backend not reachable at {BACKEND_URL}. "
                "Start with: cd 01-Code/backend && python -m uvicorn main:app --port 8000"
            )

    def test_backend_root_returns_200(self):
        """Root endpoint must return HTTP 200."""
        response = httpx.get(f"{BACKEND_URL}/", timeout=5)
        assert response.status_code == 200, (
            f"Expected 200 from {BACKEND_URL}/, got {response.status_code}"
        )

    def test_docs_endpoint_accessible(self):
        """Swagger UI at /docs must return 200 so the API is explorable."""
        response = httpx.get(f"{BACKEND_URL}/docs", timeout=5)
        assert response.status_code == 200, (
            f"Swagger docs at /docs returned {response.status_code}"
        )

    def test_openapi_schema_accessible(self):
        """/openapi.json must be accessible and valid JSON."""
        response = httpx.get(f"{BACKEND_URL}/openapi.json", timeout=5)
        assert response.status_code == 200
        schema = response.json()
        assert "paths" in schema, "openapi.json has no 'paths' key — schema may be corrupt"

    def test_upload_resume_endpoint_exists(self):
        """/upload-resume endpoint must be registered in the OpenAPI schema."""
        response = httpx.get(f"{BACKEND_URL}/openapi.json", timeout=5)
        paths = response.json().get("paths", {})
        assert any("upload" in p for p in paths), (
            "/upload-resume (or similar) endpoint not found in OpenAPI schema"
        )

    def test_analyze_endpoint_exists(self):
        """/analyze endpoint must be registered in the OpenAPI schema."""
        response = httpx.get(f"{BACKEND_URL}/openapi.json", timeout=5)
        paths = response.json().get("paths", {})
        assert any("analyze" in p for p in paths), (
            "/analyze endpoint not found in OpenAPI schema"
        )

    def test_fetch_jd_endpoint_exists(self):
        """/fetch-jd endpoint must be registered in the OpenAPI schema."""
        response = httpx.get(f"{BACKEND_URL}/openapi.json", timeout=5)
        paths = response.json().get("paths", {})
        assert any("jd" in p or "fetch" in p for p in paths), (
            "/fetch-jd (or similar) endpoint not found in OpenAPI schema"
        )

    def test_cors_header_present_for_frontend_origin(self):
        """
        Backend must include CORS headers allowing the frontend origin.
        This prevents 'CORS error' failures in the browser.
        """
        headers = {"Origin": "http://localhost:5173"}
        response = httpx.options(
            f"{BACKEND_URL}/",
            headers=headers,
            timeout=5
        )
        acao = response.headers.get("access-control-allow-origin", "")
        assert acao in ("*", "http://localhost:5173"), (
            f"CORS header 'access-control-allow-origin' is '{acao}'. "
            "Frontend at http://localhost:5173 will be blocked. "
            "Update CORSMiddleware in main.py."
        )


# ===========================================================================
# Section 7 – Database Connectivity & Schema
# ===========================================================================
class TestDatabaseConnectivity:
    """
    Tests database reachability and schema completeness.
    Requires DATABASE_URL in .env with a live PostgreSQL instance.
    """

    def _get_database_url(self):
        """Read DATABASE_URL from .env file."""
        if not ENV_FILE.exists():
            return None
        for line in ENV_FILE.read_text().splitlines():
            if line.startswith("DATABASE_URL="):
                return line.split("=", 1)[1].strip()
        return None

    def test_database_url_is_configured(self):
        """DATABASE_URL must be set and non-empty."""
        url = self._get_database_url()
        assert url, (
            "DATABASE_URL is not set in .env. "
            "Set it to your PostgreSQL connection string."
        )

    def test_database_is_reachable(self):
        """PostgreSQL must accept connections using the configured URL."""
        url = self._get_database_url()
        if not url:
            pytest.skip("DATABASE_URL not configured")
        try:
            import psycopg2
            # Parse URL: postgresql://user:pass@host:port/dbname
            conn = psycopg2.connect(url, connect_timeout=5)
            conn.close()
        except Exception as exc:
            pytest.fail(
                f"Cannot connect to PostgreSQL: {exc}\n"
                "Check that PostgreSQL is running and DATABASE_URL is correct."
            )

    def test_required_tables_exist(self):
        """All V2 database tables must exist after migrations are applied."""
        url = self._get_database_url()
        if not url:
            pytest.skip("DATABASE_URL not configured")
        try:
            import psycopg2
            conn = psycopg2.connect(url, connect_timeout=5)
            cur = conn.cursor()
            cur.execute(
                "SELECT tablename FROM pg_tables WHERE schemaname = 'public';"
            )
            tables = {row[0] for row in cur.fetchall()}
            conn.close()
        except Exception as exc:
            pytest.skip(f"Could not query tables: {exc}")

        required_tables = {"resumes", "job_descriptions", "analyses", "applications"}
        missing = required_tables - tables
        assert not missing, (
            f"Missing database tables: {missing}. "
            "Run: cd 01-Code/backend && alembic upgrade head"
        )

    def test_resumes_table_has_rows(self):
        """resumes table should have at least one row (seed data loaded)."""
        url = self._get_database_url()
        if not url:
            pytest.skip("DATABASE_URL not configured")
        try:
            import psycopg2
            conn = psycopg2.connect(url, connect_timeout=5)
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM resumes;")
            count = cur.fetchone()[0]
            conn.close()
        except Exception as exc:
            pytest.skip(f"Could not query resumes table: {exc}")

        assert count > 0, (
            "resumes table is empty. "
            "Run: cd 01-Code/backend && python load_all_resumes.py"
        )
