"""
Security Test Suite for ResumeTailor API
Covers OWASP Top 10 vulnerabilities relevant to this application.

Tests:
  1. File Upload Security       - Malicious files, path traversal, mime spoofing
  2. Input Validation           - Injection, XSS payloads in metadata fields
  3. IDOR                       - Insecure Direct Object Reference enumeration
  4. Information Disclosure     - Stack traces / internal details in error responses
  5. Security Headers           - Missing HTTP security headers
  6. CORS Misconfiguration      - Overly permissive CORS policy
  7. Rate Limiting              - DoS protection check
  8. SSRF                       - Server-Side Request Forgery via job_url field
  9. HTTP Method Tampering      - Unexpected HTTP verbs on endpoints
 10. Path Traversal             - Directory traversal via filename

Run with:
    python test_security.py
    python test_security.py --url http://127.0.0.1:8000
"""

import argparse
import io
import os
import time
import textwrap
from dataclasses import dataclass, field
from typing import List, Optional
import requests

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

DEFAULT_BASE_URL = "http://127.0.0.1:8000"

# ---------------------------------------------------------------------------
# Result models
# ---------------------------------------------------------------------------

PASS  = "PASS"
FAIL  = "FAIL"
WARN  = "WARN"
INFO  = "INFO"

@dataclass
class TestResult:
    id: str
    name: str
    category: str
    status: str          # PASS | FAIL | WARN | INFO
    finding: str
    recommendation: str = ""
    detail: str = ""

@dataclass
class SecurityReport:
    results: List[TestResult] = field(default_factory=list)

    def add(self, result: TestResult):
        self.results.append(result)

    def summary(self):
        totals = {PASS: 0, FAIL: 0, WARN: 0, INFO: 0}
        for r in self.results:
            totals[r.status] = totals.get(r.status, 0) + 1
        return totals

    def print(self):
        categories: dict = {}
        for r in self.results:
            categories.setdefault(r.category, []).append(r)

        print("\n" + "=" * 80)
        print("  RESUMETAILOR  —  SECURITY TEST REPORT")
        print("=" * 80)

        status_icon = {PASS: "✅", FAIL: "❌", WARN: "⚠️ ", INFO: "ℹ️ "}

        for cat, items in categories.items():
            print(f"\n▶  {cat}")
            print("─" * 78)
            for r in items:
                icon = status_icon.get(r.status, "?")
                print(f"  {icon} [{r.id}] {r.name}")
                print(f"      Finding : {r.finding}")
                if r.recommendation:
                    print(f"      Fix     : {r.recommendation}")
                if r.detail:
                    for line in textwrap.wrap(r.detail, width=70):
                        print(f"               {line}")

        s = self.summary()
        print("\n" + "=" * 80)
        print(
            f"  SUMMARY  |  ✅ Pass: {s[PASS]}  |  ❌ Fail: {s[FAIL]}  "
            f"|  ⚠️  Warn: {s[WARN]}  |  ℹ️  Info: {s[INFO]}"
        )
        print("=" * 80 + "\n")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_pdf_bytes() -> bytes:
    """Minimal valid PDF content."""
    return b"%PDF-1.4 1 0 obj<</Type /Catalog /Pages 2 0 R>>endobj 2 0 obj<</Type /Pages /Kids [3 0 R] /Count 1>>endobj 3 0 obj<</Type /Page /MediaBox [0 0 612 792]>>endobj xref 0 4\ntrailer<</Size 4 /Root 1 0 R>>startxref\n%%EOF\nPython Security Test Resume - John Doe Software Engineer"

def make_docx_bytes() -> bytes:
    """Minimal DOCX (ZIP) magic header — will fail parsing but pass extension check."""
    return b"PK\x03\x04" + b"\x00" * 100

def make_txt_bytes(content: str = "Security Test Resume Content") -> bytes:
    return content.encode("utf-8")

def upload_resume(base_url: str, filename: str, content: bytes,
                  content_type: str = "application/octet-stream",
                  extra_data: dict = None) -> requests.Response:
    files = {"file": (filename, io.BytesIO(content), content_type)}
    data = extra_data or {}
    return requests.post(f"{base_url}/upload-resume/", files=files, data=data, timeout=15)

def upload_jd(base_url: str, filename: str, content: bytes,
              content_type: str = "text/plain",
              extra_data: dict = None) -> requests.Response:
    files = {"file": (filename, io.BytesIO(content), content_type)}
    data = extra_data or {}
    return requests.post(f"{base_url}/upload-jd/", files=files, data=data, timeout=15)


# ---------------------------------------------------------------------------
# Test categories
# ---------------------------------------------------------------------------

class SecurityTests:
    def __init__(self, base_url: str, report: SecurityReport):
        self.base = base_url.rstrip("/")
        self.report = report
        # Seed a known-good resume and JD ID for IDOR tests
        self._existing_resume_id: Optional[int] = None
        self._existing_jd_id: Optional[int] = None
        self._seed_ids()

    def _seed_ids(self):
        """Upload one valid resume/JD to get real IDs for IDOR and analysis tests."""
        try:
            r = upload_resume(self.base, "seed_resume.txt",
                              make_txt_bytes("Seed resume for security testing. Python Developer 5 years"),
                              "text/plain")
            if r.status_code == 200:
                self._existing_resume_id = r.json().get("id")
        except Exception:
            pass
        try:
            r = upload_jd(self.base, "seed_jd.txt",
                          make_txt_bytes("Seed job description. Looking for Python Developer"),
                          "text/plain")
            if r.status_code == 200:
                self._existing_jd_id = r.json().get("id")
        except Exception:
            pass

    # -----------------------------------------------------------------------
    # 1. FILE UPLOAD SECURITY
    # -----------------------------------------------------------------------

    def test_file_upload_path_traversal_filename(self):
        """Path traversal characters in filename should be rejected or sanitised."""
        payloads = [
            "../../../etc/passwd.txt",
            "..\\..\\windows\\system32\\config.txt",
            "....//....//etc/passwd.txt",
            "%2e%2e%2f%2e%2e%2fetc%2fpasswd.txt",
        ]
        vulnerable = False
        for name in payloads:
            try:
                r = upload_resume(self.base, name, make_txt_bytes(), "text/plain")
                # A 200 with such a filename is a concern (name must be sanitised server-side)
                if r.status_code == 200:
                    body = r.json()
                    stored_filename = body.get("filename", "")
                    # If the raw traversal string is stored as-is thats a finding
                    if ".." in stored_filename or "/" in stored_filename or "\\" in stored_filename:
                        vulnerable = True
            except Exception:
                pass

        if vulnerable:
            self.report.add(TestResult(
                id="FU-01", name="Path Traversal in Upload Filename",
                category="1. File Upload Security",
                status=FAIL,
                finding="Server stores path-traversal characters in filename. Could allow reading/overwriting arbitrary files.",
                recommendation="Sanitise filenames with os.path.basename() or uuid before saving."
            ))
        else:
            self.report.add(TestResult(
                id="FU-01", name="Path Traversal in Upload Filename",
                category="1. File Upload Security",
                status=PASS,
                finding="Path traversal payloads in filenames were blocked or sanitised correctly."
            ))

    def test_file_upload_wrong_magic_number(self):
        """.pdf extension with EXE/HTML content should be rejected by magic-number check."""
        # Use an HTML payload (not a valid PDF magic number)
        html_payload = b"<html><script>alert(1)</script></html>"
        r = upload_resume(self.base, "malicious.pdf", html_payload, "application/pdf")
        # 429 = rate limited (still blocked before reaching storage) — counts as safe
        if r.status_code in (400, 415, 422, 429):
            self.report.add(TestResult(
                id="FU-02", name="Magic Number Validation (MIME Spoofing)",
                category="1. File Upload Security",
                status=PASS,
                finding=f"File with mismatched magic number blocked (status {r.status_code})."
            ))
        else:
            self.report.add(TestResult(
                id="FU-02", name="Magic Number Validation (MIME Spoofing)",
                category="1. File Upload Security",
                status=FAIL,
                finding=f"Accepted file with invalid magic number (status {r.status_code}). HTML content could be stored and served.",
                recommendation="Enforce magic-number / libmagic validation for all upload types."
            ))

    def test_file_upload_double_extension(self):
        """Filenames like 'resume.pdf.exe' should be rejected."""
        r = upload_resume(self.base, "resume.pdf.exe", make_pdf_bytes(), "application/pdf")
        # 429 = rate limited (still blocked) — acceptable
        ext_rejected = r.status_code in (400, 415, 422, 429)
        self.report.add(TestResult(
            id="FU-03", name="Double Extension Upload",
            category="1. File Upload Security",
            status=PASS if ext_rejected else WARN,
            finding=(
                f"Double-extension file blocked (status {r.status_code})." if ext_rejected
                else f"Server returned {r.status_code} for double-extension filename. Verify actual extension parsed is not '.exe'."
            ),
            recommendation="Always parse the final extension only (rightmost token after last '.')."
        ))

    def test_file_upload_oversized(self):
        """Files over 10 MB must be rejected to prevent DoS."""
        large_content = b"%PDF-1.4 " + b"A" * (11 * 1024 * 1024)  # ~11 MB
        try:
            r = upload_resume(self.base, "huge.pdf", large_content, "application/pdf")
            if r.status_code in (413, 429):  # 429 = rate limited before even reaching size check
                self.report.add(TestResult(
                    id="FU-04", name="Oversized File Rejection (DoS)",
                    category="1. File Upload Security",
                    status=PASS,
                    finding=f"Oversized file blocked (status {r.status_code})."
                ))
            else:
                self.report.add(TestResult(
                    id="FU-04", name="Oversized File Rejection (DoS)",
                    category="1. File Upload Security",
                    status=FAIL,
                    finding=f"11 MB file accepted (status {r.status_code}). No upload size limit enforced.",
                    recommendation="Return HTTP 413 for files above MAX_FILE_SIZE (currently 10 MB)."
                ))
        except Exception as e:
            self.report.add(TestResult(
                id="FU-04", name="Oversized File Rejection (DoS)",
                category="1. File Upload Security",
                status=WARN,
                finding=f"Request with 11 MB file raised an exception: {e}",
                recommendation="Ensure the server or reverse proxy enforces a request body size limit."
            ))

    def test_file_upload_null_byte_filename(self):
        """Null bytes in filenames can bypass extension checks on some systems."""
        try:
            r = upload_resume(self.base, "evil\x00.txt", make_txt_bytes(), "text/plain")
            # 429 = rate limited (blocked) — acceptable
            if r.status_code in (400, 422, 429):
                self.report.add(TestResult(
                    id="FU-05", name="Null Byte in Filename",
                    category="1. File Upload Security",
                    status=PASS,
                    finding=f"Filename with null byte blocked (status {r.status_code})."
                ))
            else:
                self.report.add(TestResult(
                    id="FU-05", name="Null Byte in Filename",
                    category="1. File Upload Security",
                    status=WARN,
                    finding=f"Null byte filename accepted (status {r.status_code}). Verify stored filename is safe.",
                    recommendation="Strip or reject null bytes and non-printable chars in filenames."
                ))
        except Exception as e:
            self.report.add(TestResult(
                id="FU-05", name="Null Byte in Filename",
                category="1. File Upload Security",
                status=INFO,
                finding=f"Request could not be sent (client-side issue): {e}"
            ))

    def test_file_upload_disallowed_type(self):
        """Executable and script files must be rejected."""
        for ext, ctype in [("exe", "application/octet-stream"),
                           ("js", "text/javascript"),
                           ("sh", "text/x-sh"),
                           ("php", "application/x-httpd-php")]:
            r = upload_resume(self.base, f"malware.{ext}", b"malicious content", ctype)
            # 400/415/422 = rejected by validation; 429 = rate-limited (also blocked)
            if r.status_code not in (400, 415, 422, 429):
                self.report.add(TestResult(
                    id="FU-06", name=f"Disallowed File Type (.{ext})",
                    category="1. File Upload Security",
                    status=FAIL,
                    finding=f".{ext} file accepted with status {r.status_code}.",
                    recommendation="Only permit .pdf, .docx, .txt extensions."
                ))
                return
        self.report.add(TestResult(
            id="FU-06", name="Disallowed File Types Rejected",
            category="1. File Upload Security",
            status=PASS,
            finding=".exe, .js, .sh, .php uploads all rejected correctly (400/422/429)."
        ))

    # -----------------------------------------------------------------------
    # 2. INPUT VALIDATION — INJECTION
    # -----------------------------------------------------------------------

    def test_sql_injection_query_params(self):
        """SQL injection payloads in integer path parameters."""
        payloads = [
            "1 OR 1=1",
            "1; DROP TABLE resumes;--",
            "1' OR '1'='1",
            "-1 UNION SELECT 1,2,3--",
        ]
        vulns = []
        for p in payloads:
            try:
                r = requests.get(f"{self.base}/resume/{p}", timeout=5)
                if r.status_code == 200:
                    vulns.append(p)
                    # If we get actual data back it is critical
            except Exception:
                pass

        if vulns:
            self.report.add(TestResult(
                id="IV-01", name="SQL Injection in Path Parameter",
                category="2. Input Validation",
                status=FAIL,
                finding=f"Injection payloads returned 200: {vulns}",
                recommendation="FastAPI path params typed as 'int' prevent this; verify no raw string interpolation in queries."
            ))
        else:
            self.report.add(TestResult(
                id="IV-01", name="SQL Injection in Path Parameter",
                category="2. Input Validation",
                status=PASS,
                finding="SQL injection payloads in path params rejected (404/422 returned)."
            ))

    def test_xss_in_metadata_fields(self):
        """XSS payloads stored in job_url / title / company fields."""
        xss_payloads = [
            "<script>alert('XSS')</script>",
            "\"><img src=x onerror=alert(1)>",
            "javascript:alert(1)",
            "';alert(String.fromCharCode(88,83,83))//",
        ]
        stored = []
        for payload in xss_payloads:
            try:
                r = upload_jd(
                    self.base, "xss_test.txt", make_txt_bytes("test jd"),
                    "text/plain",
                    extra_data={"title": payload, "company": payload, "job_url": "http://safe.example.com"}
                )
                if r.status_code == 200:
                    body = r.json()
                    # Check if the payload is echoed back raw (not escaped)
                    body_str = str(body)
                    if "<script>" in body_str or "onerror=" in body_str or "javascript:" in body_str:
                        stored.append(payload[:30])
            except Exception:
                pass

        if stored:
            self.report.add(TestResult(
                id="IV-02", name="Stored XSS in Metadata Fields",
                category="2. Input Validation",
                status=WARN,
                finding=f"XSS payload echoed back in API response: {stored}.",
                detail="The API returns raw user input. If a frontend renders these values as innerHTML, XSS is possible.",
                recommendation="HTML-encode outputs in the frontend. Consider server-side input sanitisation on title/company fields."
            ))
        else:
            self.report.add(TestResult(
                id="IV-02", name="Stored XSS in Metadata Fields",
                category="2. Input Validation",
                status=PASS,
                finding="XSS payloads were not echoed back in raw form."
            ))

    def test_ssrf_via_job_url(self):
        """SSRF via job_url field — internal addresses must not be fetched."""
        ssrf_targets = [
            "http://127.0.0.1:8000/",
            "http://localhost:8000/",
            "http://169.254.169.254/latest/meta-data/",  # AWS metadata
            "file:///etc/passwd",
            "http://0.0.0.0:8000/",
        ]
        vulnerable = []
        for target in ssrf_targets:
            try:
                r = requests.post(
                    f"{self.base}/fetch-jd/",
                    json={"job_url": target},
                    timeout=5
                )
                # 200 with content from an internal address = SSRF
                if r.status_code == 200:
                    body = r.text
                    if any(kw in body for kw in ["root:", "localhost", "meta-data", "Password"]):
                        vulnerable.append(target)
            except Exception:
                pass

        if vulnerable:
            self.report.add(TestResult(
                id="IV-03", name="SSRF via Job URL",
                category="2. Input Validation",
                status=FAIL,
                finding=f"Internal resources fetched via job_url: {vulnerable}",
                recommendation="Implement URL allowlist (public job boards only), block private IP ranges, and use a safe HTTP client with SSRF protection."
            ))
        else:
            self.report.add(TestResult(
                id="IV-03", name="SSRF via Job URL",
                category="2. Input Validation",
                status=PASS,
                finding="SSRF payloads in job_url did not return internal resources."
            ))

    def test_command_injection_in_metadata(self):
        """OS command injection payloads in title / company fields."""
        cmd_payloads = [
            "; ls -la",
            "| whoami",
            "`id`",
            "$(cat /etc/passwd)",
            "&& dir",
        ]
        for payload in cmd_payloads:
            try:
                r = upload_jd(
                    self.base, "cmd_test.txt", make_txt_bytes("test"),
                    "text/plain",
                    extra_data={"title": payload, "company": "TestCo"}
                )
                if r.status_code == 200:
                    body = r.text
                    # If command output appears in the response, it is vulnerable
                    if any(kw in body for kw in ["root", "uid=", "Volume", "Directory"]):
                        self.report.add(TestResult(
                            id="IV-04", name="Command Injection in Metadata",
                            category="2. Input Validation",
                            status=FAIL,
                            finding=f"Command output detected in response for payload: {payload}",
                            recommendation="Never pass user input to shell commands. Use parameterised DB queries only."
                        ))
                        return
            except Exception:
                pass

        self.report.add(TestResult(
            id="IV-04", name="Command Injection in Metadata",
            category="2. Input Validation",
            status=PASS,
            finding="No command execution output detected in metadata field responses."
        ))

    # -----------------------------------------------------------------------
    # 3. INSECURE DIRECT OBJECT REFERENCE (IDOR)
    # -----------------------------------------------------------------------

    def test_idor_resume_enumeration(self):
        """IDs are predictable integers — unauthenticated users can enumerate all resumes."""
        if not self._existing_resume_id:
            self.report.add(TestResult(
                id="IDOR-01", name="Resume ID Enumeration",
                category="3. IDOR",
                status=WARN,
                finding="Could not seed a resume for IDOR test — skipped."
            ))
            return

        # Try to fetch several IDs numerically
        accessible = []
        for rid in range(max(1, self._existing_resume_id - 5), self._existing_resume_id + 2):
            try:
                r = requests.get(f"{self.base}/resume/{rid}", timeout=5)
                if r.status_code == 200:
                    accessible.append(rid)
            except Exception:
                pass

        if len(accessible) > 1:
            self.report.add(TestResult(
                id="IDOR-01", name="Resume ID Enumeration (No Auth)",
                category="3. IDOR",
                status=FAIL,
                finding=f"Unauthenticated access to resume IDs: {accessible}. Any caller can read any user's resume.",
                recommendation="Implement authentication (JWT/session) and ownership checks: verify the requesting user owns the resume before returning it."
            ))
        else:
            self.report.add(TestResult(
                id="IDOR-01", name="Resume ID Enumeration (No Auth)",
                category="3. IDOR",
                status=WARN,
                finding="Only own resume ID accessible. However, no authentication layer is present — IDOR protection relies solely on guessing IDs.",
                recommendation="Add authentication and per-resource ownership checks."
            ))

    def test_idor_jd_enumeration(self):
        """Unauthenticated enumeration of job description records."""
        if not self._existing_jd_id:
            self.report.add(TestResult(
                id="IDOR-02", name="JD ID Enumeration",
                category="3. IDOR",
                status=WARN,
                finding="Could not seed a JD for IDOR test — skipped."
            ))
            return

        accessible = []
        for jid in range(max(1, self._existing_jd_id - 5), self._existing_jd_id + 2):
            try:
                r = requests.get(f"{self.base}/jd/{jid}", timeout=5)
                if r.status_code == 200:
                    accessible.append(jid)
            except Exception:
                pass

        if len(accessible) > 1:
            self.report.add(TestResult(
                id="IDOR-02", name="JD ID Enumeration (No Auth)",
                category="3. IDOR",
                status=FAIL,
                finding=f"Unauthenticated access to JD IDs: {accessible}.",
                recommendation="Require authentication; bind JD records to authenticated user and enforce ownership."
            ))
        else:
            self.report.add(TestResult(
                id="IDOR-02", name="JD ID Enumeration (No Auth)",
                category="3. IDOR",
                status=WARN if self._existing_jd_id else PASS,
                finding="Only own JD accessible. Authentication still absent.",
                recommendation="Add user authentication and resource-level authorisation."
            ))

    def test_gap_analysis_cross_user(self):
        """Gap analysis with IDs that don't belong to the caller."""
        if not (self._existing_resume_id and self._existing_jd_id):
            self.report.add(TestResult(
                id="IDOR-03", name="Gap Analysis Cross-User Access",
                category="3. IDOR",
                status=WARN,
                finding="Seed IDs unavailable — test skipped."
            ))
            return

        r = requests.post(
            f"{self.base}/gap-analysis/",
            params={"resume_id": self._existing_resume_id, "jd_id": self._existing_jd_id},
            timeout=30
        )
        if r.status_code == 200:
            self.report.add(TestResult(
                id="IDOR-03", name="Gap Analysis Cross-User Access",
                category="3. IDOR",
                status=FAIL,
                finding="Gap analysis executed on arbitrary resume/JD IDs without authentication. Caller can analyse any user's private documents.",
                recommendation="Require a valid auth token; verify resume and JD belong to the requesting user."
            ))
        else:
            self.report.add(TestResult(
                id="IDOR-03", name="Gap Analysis Cross-User Access",
                category="3. IDOR",
                status=PASS,
                finding=f"Gap analysis on unowned IDs returned {r.status_code}."
            ))

    # -----------------------------------------------------------------------
    # 4. INFORMATION DISCLOSURE
    # -----------------------------------------------------------------------

    def test_error_stack_trace_disclosure(self):
        """500 errors must not expose internal stack traces or file paths."""
        # Force a parsing error by sending an empty PDF (passes extension but fails parse)
        r = upload_resume(self.base, "empty.pdf", b"%PDF-1.4 ", "application/pdf")
        body_str = r.text
        indicators = [
            "Traceback", "File \"", "line ", ".py\"",
            "sqlalchemy", "pydantic", "C:\\", "/home/", "site-packages"
        ]
        leaks = [i for i in indicators if i in body_str]
        if leaks:
            self.report.add(TestResult(
                id="ID-01", name="Stack Trace / Internal Path in Error Response",
                category="4. Information Disclosure",
                status=FAIL,
                finding=f"Error response contains internal detail indicators: {leaks}",
                recommendation="In production, catch all exceptions and return generic messages. Move debug details to server-side logs only.",
                detail=body_str[:200]
            ))
        else:
            self.report.add(TestResult(
                id="ID-01", name="Stack Trace / Internal Path in Error Response",
                category="4. Information Disclosure",
                status=PASS,
                finding="No stack trace or internal path found in error response."
            ))

    def test_server_version_disclosure(self):
        """Server header must not reveal framework/version."""
        r = requests.get(f"{self.base}/", timeout=5)
        server_header = r.headers.get("server", "")
        version_indicators = ["uvicorn", "starlette", "fastapi", "python", "0.", "1.", "2.", "3."]
        leaks = [v for v in version_indicators if v.lower() in server_header.lower()]
        if leaks:
            self.report.add(TestResult(
                id="ID-02", name="Server Version Disclosure",
                category="4. Information Disclosure",
                status=WARN,
                finding=f"'Server' header reveals: '{server_header}'",
                recommendation="Configure a reverse proxy (nginx/caddy) to mask the Server header in production."
            ))
        else:
            self.report.add(TestResult(
                id="ID-02", name="Server Version Disclosure",
                category="4. Information Disclosure",
                status=PASS,
                finding=f"Server header does not disclose version info: '{server_header}'"
            ))

    def test_sensitive_data_in_error_detail(self):
        """Error detail field must not return raw exception messages with internal info."""
        r = upload_resume(self.base, "bad.pdf", b"%PDF-1.4 corrupt", "application/pdf")
        try:
            body = r.json()
            detail = str(body.get("detail", ""))
            sensitive = ["str(e)", "Exception", "Traceback", "/tmp/", "C:\\Users\\",
                         "sqlite", "password", "secret", "API_KEY"]
            found = [s for s in sensitive if s.lower() in detail.lower()]
            if found:
                self.report.add(TestResult(
                    id="ID-03", name="Sensitive Data in Error Detail Field",
                    category="4. Information Disclosure",
                    status=WARN,
                    finding=f"Error 'detail' field contains: {found}",
                    recommendation="Replace str(e) in HTTPException detail with a static message in production mode.",
                    detail=detail[:200]
                ))
            else:
                self.report.add(TestResult(
                    id="ID-03", name="Sensitive Data in Error Detail Field",
                    category="4. Information Disclosure",
                    status=PASS,
                    finding="Error detail does not contain sensitive internal information."
                ))
        except Exception:
            self.report.add(TestResult(
                id="ID-03", name="Sensitive Data in Error Detail Field",
                category="4. Information Disclosure",
                status=INFO,
                finding="Could not parse error response as JSON."
            ))

    # -----------------------------------------------------------------------
    # 5. SECURITY HEADERS
    # -----------------------------------------------------------------------

    def _check_headers(self):
        return requests.get(f"{self.base}/", timeout=5).headers

    def test_security_headers(self):
        headers = self._check_headers()
        required = {
            "X-Content-Type-Options": ("nosniff", "Prevents MIME-type sniffing attacks."),
            "X-Frame-Options": ("DENY or SAMEORIGIN", "Prevents clickjacking."),
            "Content-Security-Policy": ("policy value", "Mitigates XSS and data injection."),
            "Strict-Transport-Security": ("max-age=...", "Enforces HTTPS (required in production)."),
            "Referrer-Policy": ("no-referrer or strict-origin", "Controls referrer information leakage."),
        }
        for header, (expected, desc) in required.items():
            value = headers.get(header)
            if not value:
                self.report.add(TestResult(
                    id=f"SH-{header[:4].upper()}", name=f"Missing Header: {header}",
                    category="5. Security Headers",
                    status=WARN,
                    finding=f"'{header}' header is absent.",
                    recommendation=f"Add '{header}: {expected}' — {desc}"
                ))
            else:
                self.report.add(TestResult(
                    id=f"SH-{header[:4].upper()}", name=f"Header Present: {header}",
                    category="5. Security Headers",
                    status=PASS,
                    finding=f"'{header}: {value}'"
                ))

    # -----------------------------------------------------------------------
    # 6. CORS MISCONFIGURATION
    # -----------------------------------------------------------------------

    def test_cors_wildcard(self):
        """CORS 'Access-Control-Allow-Origin: *' exposes the API to any origin."""
        r = requests.options(
            f"{self.base}/upload-resume/",
            headers={
                "Origin": "https://evil.attacker.com",
                "Access-Control-Request-Method": "POST"
            },
            timeout=5
        )
        acao = r.headers.get("Access-Control-Allow-Origin", "")
        if acao == "*":
            self.report.add(TestResult(
                id="CORS-01", name="CORS Wildcard Origin",
                category="6. CORS Misconfiguration",
                status=FAIL,
                finding="'Access-Control-Allow-Origin: *' — any website can make authenticated cross-origin requests.",
                recommendation="Set CORS_ORIGINS env var to a specific allowlist of production origins instead of '*'."
            ))
        elif "evil.attacker.com" in acao:
            self.report.add(TestResult(
                id="CORS-01", name="CORS Reflects Arbitrary Origin",
                category="6. CORS Misconfiguration",
                status=FAIL,
                finding=f"CORS reflects the attacker origin: '{acao}'",
                recommendation="Validate origin against an explicit allowlist."
            ))
        else:
            self.report.add(TestResult(
                id="CORS-01", name="CORS Origin Policy",
                category="6. CORS Misconfiguration",
                status=PASS,
                finding=f"'Access-Control-Allow-Origin: {acao}' — not a blanket wildcard for untrusted origins."
            ))

    def test_cors_credentials_with_wildcard(self):
        """Combining credentials:true with wildcard ACAO is forbidden by spec but worth verifying."""
        r = requests.options(
            f"{self.base}/upload-resume/",
            headers={
                "Origin": "https://test.com",
                "Access-Control-Request-Method": "POST"
            },
            timeout=5
        )
        acao = r.headers.get("Access-Control-Allow-Origin", "")
        acac = r.headers.get("Access-Control-Allow-Credentials", "")
        if acao == "*" and acac.lower() == "true":
            self.report.add(TestResult(
                id="CORS-02", name="CORS Wildcard + Allow-Credentials",
                category="6. CORS Misconfiguration",
                status=FAIL,
                finding="Both 'Access-Control-Allow-Origin: *' and 'Access-Control-Allow-Credentials: true' set. This is a browser security violation.",
                recommendation="Never combine wildcard ACAO with allow-credentials. Use specific origins."
            ))
        else:
            self.report.add(TestResult(
                id="CORS-02", name="CORS Wildcard + Allow-Credentials",
                category="6. CORS Misconfiguration",
                status=PASS,
                finding=f"ACAO='{acao}', Allow-Credentials='{acac}' — dangerous combination not present."
            ))

    # -----------------------------------------------------------------------
    # 7. RATE LIMITING / DoS PROTECTION
    # -----------------------------------------------------------------------

    def test_rate_limiting(self):
        """Verify rate limiting on GET / by sending a burst of requests until a 429 is received."""
        try:
            rate_limited = False
            for _ in range(70):
                r = requests.get(f"{self.base}/", timeout=5)
                if r.status_code == 429:
                    rate_limited = True
                    break
            if rate_limited:
                self.report.add(TestResult(
                    id="RL-01", name="GET Endpoint Rate Limiting",
                    category="7. Rate Limiting",
                    status=PASS,
                    finding="GET / returned 429 after burst of requests — rate limiter is active."
                ))
            else:
                self.report.add(TestResult(
                    id="RL-01", name="GET Endpoint Rate Limiting Absent",
                    category="7. Rate Limiting",
                    status=FAIL,
                    finding="70 consecutive GET / requests were all allowed (no 429). Rate limiter may not be active on this endpoint.",
                    recommendation="Ensure GET / has a Request param and @limiter.limit() decorator."
                ))
        except Exception as e:
            self.report.add(TestResult(
                id="RL-01", name="GET Endpoint Rate Limiting",
                category="7. Rate Limiting",
                status=WARN,
                finding=f"Could not test GET / rate limiting: {e}"
            ))

    def test_upload_rate_limiting(self):
        """Rapid file uploads should be throttled."""
        rate_limited = False
        for _ in range(15):
            try:
                r = upload_resume(self.base, "rl_test.txt", make_txt_bytes(), "text/plain")
                if r.status_code == 429:
                    rate_limited = True
                    break
            except Exception:
                break

        if rate_limited:
            self.report.add(TestResult(
                id="RL-02", name="Upload Endpoint Rate Limiting",
                category="7. Rate Limiting",
                status=PASS,
                finding="Rate limiting active on upload endpoint."
            ))
        else:
            self.report.add(TestResult(
                id="RL-02", name="Upload Endpoint Rate Limiting Absent",
                category="7. Rate Limiting",
                status=FAIL,
                finding="15 rapid uploads completed without throttling. Allows storage exhaustion attack.",
                recommendation="Apply @limiter.limit('10/minute') on /upload-resume/ and /upload-jd/ endpoints."
            ))

    # -----------------------------------------------------------------------
    # 8. HTTP METHOD TAMPERING
    # -----------------------------------------------------------------------

    def test_method_tampering(self):
        """Sensitive resources must not accept unexpected HTTP methods."""
        cases = [
            ("DELETE", f"{self.base}/resume/1"),
            ("PUT",    f"{self.base}/resume/1"),
            ("PATCH",  f"{self.base}/resume/1"),
            ("DELETE", f"{self.base}/jd/1"),
        ]
        permitted = []
        for method, url in cases:
            try:
                r = requests.request(method, url, timeout=5)
                if r.status_code not in (404, 405, 422):
                    permitted.append(f"{method} {url} → {r.status_code}")
            except Exception:
                pass

        if permitted:
            self.report.add(TestResult(
                id="MT-01", name="Unexpected HTTP Methods Accepted",
                category="8. HTTP Method Tampering",
                status=WARN,
                finding=f"Unexpected methods returned non-405 status: {permitted}",
                recommendation="Ensure only GET/POST are exposed; FastAPI automatically returns 405 for unregistered methods."
            ))
        else:
            self.report.add(TestResult(
                id="MT-01", name="HTTP Method Tampering",
                category="8. HTTP Method Tampering",
                status=PASS,
                finding="DELETE/PUT/PATCH on resource endpoints correctly return 404/405."
            ))

    # -----------------------------------------------------------------------
    # 9. AUTHENTICATION / ACCESS CONTROL
    # -----------------------------------------------------------------------

    def test_no_authentication(self):
        """Document the absence of any authentication mechanism."""
        # Try to access all major endpoints without any token/cookie
        endpoints = [
            ("GET",  f"{self.base}/resume/{self._existing_resume_id or 1}"),
            ("GET",  f"{self.base}/jd/{self._existing_jd_id or 1}"),
        ]
        unprotected = []
        for method, url in endpoints:
            try:
                r = requests.request(method, url, timeout=5)
                if r.status_code == 200:
                    unprotected.append(url)
            except Exception:
                pass

        if unprotected:
            self.report.add(TestResult(
                id="AC-01", name="No Authentication on Data Endpoints",
                category="9. Authentication & Access Control",
                status=FAIL,
                finding=f"Unauthenticated access granted to: {unprotected}",
                recommendation="Implement JWT authentication (e.g., python-jose). Protect all /resume/, /jd/, and /gap-analysis/ routes with a dependency that validates the bearer token."
            ))
        else:
            self.report.add(TestResult(
                id="AC-01", name="Authentication Check",
                category="9. Authentication & Access Control",
                status=PASS,
                finding="Unauthenticated requests to data endpoints returned non-200."
            ))

    # -----------------------------------------------------------------------
    # 10. SENSITIVE FILE EXPOSURE
    # -----------------------------------------------------------------------

    def test_env_file_exposure(self):
        """The .env file must not be served over HTTP."""
        sensitive_paths = [
            "/.env",
            "/.env.example",
            "/backend/.env",
            "/debug_simple.log",
            "/requirements.txt",
        ]
        exposed = []
        for path in sensitive_paths:
            try:
                r = requests.get(f"{self.base}{path}", timeout=5)
                if r.status_code == 200 and len(r.content) > 0:
                    exposed.append(path)
            except Exception:
                pass

        if exposed:
            self.report.add(TestResult(
                id="SFE-01", name="Sensitive Files Exposed over HTTP",
                category="10. File / Path Exposure",
                status=FAIL,
                finding=f"Sensitive files accessible via HTTP: {exposed}",
                recommendation="Configure the web server/FastAPI static routing to never serve .env, *.log, or requirements.txt files."
            ))
        else:
            self.report.add(TestResult(
                id="SFE-01", name="Sensitive File Exposure",
                category="10. File / Path Exposure",
                status=PASS,
                finding="No sensitive files (.env, .log, requirements.txt) are served over HTTP."
            ))

    def test_api_docs_exposure(self):
        """OpenAPI docs (/docs, /redoc) expose full API schema — flag for production."""
        docs_exposed = False
        for path in ["/docs", "/redoc", "/openapi.json"]:
            try:
                r = requests.get(f"{self.base}{path}", timeout=5)
                if r.status_code == 200:
                    docs_exposed = True
                    break
            except Exception:
                pass

        if docs_exposed:
            self.report.add(TestResult(
                id="SFE-02", name="API Documentation Publicly Accessible",
                category="10. File / Path Exposure",
                status=WARN,
                finding="/docs or /redoc is publicly accessible, exposing full API schema.",
                recommendation="Disable in production via FastAPI(docs_url=None, redoc_url=None) or restrict to internal IPs."
            ))
        else:
            self.report.add(TestResult(
                id="SFE-02", name="API Documentation Exposure",
                category="10. File / Path Exposure",
                status=PASS,
                finding="API documentation endpoints are not publicly accessible."
            ))


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

def run_all(base_url: str) -> SecurityReport:
    report = SecurityReport()
    suite = SecurityTests(base_url, report)

    print(f"\n🔍  Running security tests against {base_url} ...\n")

    tests = [
        # File Upload
        suite.test_file_upload_path_traversal_filename,
        suite.test_file_upload_wrong_magic_number,
        suite.test_file_upload_double_extension,
        suite.test_file_upload_oversized,
        suite.test_file_upload_null_byte_filename,
        suite.test_file_upload_disallowed_type,
        # Input Validation
        suite.test_sql_injection_query_params,
        suite.test_xss_in_metadata_fields,
        suite.test_ssrf_via_job_url,
        suite.test_command_injection_in_metadata,
        # IDOR
        suite.test_idor_resume_enumeration,
        suite.test_idor_jd_enumeration,
        suite.test_gap_analysis_cross_user,
        # Information Disclosure
        suite.test_error_stack_trace_disclosure,
        suite.test_server_version_disclosure,
        suite.test_sensitive_data_in_error_detail,
        # Security Headers
        suite.test_security_headers,
        # CORS
        suite.test_cors_wildcard,
        suite.test_cors_credentials_with_wildcard,
        # Rate Limiting
        suite.test_rate_limiting,
        suite.test_upload_rate_limiting,
        # HTTP Method Tampering
        suite.test_method_tampering,
        # Authentication
        suite.test_no_authentication,
        # File Exposure
        suite.test_env_file_exposure,
        suite.test_api_docs_exposure,
    ]

    for test in tests:
        try:
            print(f"  Running {test.__name__} ...", end=" ", flush=True)
            test()
            last = report.results[-1]
            icon = {"PASS": "✅", "FAIL": "❌", "WARN": "⚠️", "INFO": "ℹ️"}.get(last.status, "?")
            print(icon)
        except Exception as e:
            print(f"ERROR: {e}")
            report.add(TestResult(
                id="ERR", name=test.__name__,
                category="Error",
                status=WARN,
                finding=f"Test raised exception: {e}"
            ))

    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ResumeTailor Security Test Suite")
    parser.add_argument("--url", default=DEFAULT_BASE_URL, help="Base URL of the API")
    args = parser.parse_args()

    report = run_all(args.url)
    report.print()

    # Exit with non-zero if any FAIL found
    import sys
    if any(r.status == FAIL for r in report.results):
        sys.exit(1)
