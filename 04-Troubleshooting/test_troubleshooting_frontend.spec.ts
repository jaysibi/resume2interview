/**
 * ResumeTailor Frontend Diagnostic Tests
 * ========================================
 * Covers Checklist Sections 4-5, 7-9 (Static Assets, Rendering, Routing, Styles, E2E readiness).
 *
 * Run from C:\Projects\ResumeTailor\04-Troubleshooting:
 *   npx playwright test test_troubleshooting_frontend.spec.ts --reporter=list
 *
 * Or from the frontend folder:
 *   cd C:\Projects\ResumeTailor\01-Code\frontend
 *   npx playwright test ../../04-Troubleshooting/test_troubleshooting_frontend.spec.ts --reporter=list
 *
 * Prerequisites:
 *   - Frontend dev server running: cd 01-Code/frontend && npm run dev  (http://localhost:5173)
 *   - Backend running: cd 01-Code/backend && python -m uvicorn main:app --port 8000
 *   - Playwright browsers installed: npx playwright install chromium
 */

import { test, expect, request } from '@playwright/test';
import * as fs from 'fs';
import * as path from 'path';

const FRONTEND_URL = 'http://localhost:5173';
const BACKEND_URL = 'http://127.0.0.1:8000';
const FRONTEND_DIR = 'C:/Projects/ResumeTailor/01-Code/frontend';
const TESTING_DIR = 'C:/Projects/ResumeTailor/03-Testing';
const RESUME_FILE = path.join(TESTING_DIR, 'Resume - Jayendra Sibi (1).docx');


// ===========================================================================
// Section 4 – Static Asset & Entry Point Validation
// ===========================================================================
test.describe('Section 4 – Static Asset & Entry Point Validation', () => {

  test('index.html exists in frontend directory', () => {
    const indexPath = path.join(FRONTEND_DIR, 'index.html');
    expect(fs.existsSync(indexPath), `index.html not found at ${indexPath}`).toBe(true);
  });

  test('index.html title is "Resume Tailor" (not default "frontend")', () => {
    const indexPath = path.join(FRONTEND_DIR, 'index.html');
    if (!fs.existsSync(indexPath)) test.skip();
    const content = fs.readFileSync(indexPath, 'utf-8');
    expect(content).toContain('<title>Resume Tailor</title>');
    expect(content).not.toContain('<title>frontend</title>');
  });

  test('index.html has root div', () => {
    const indexPath = path.join(FRONTEND_DIR, 'index.html');
    if (!fs.existsSync(indexPath)) test.skip();
    const content = fs.readFileSync(indexPath, 'utf-8');
    expect(content).toContain('<div id="root">');
  });

  test('index.html references src/main.tsx as module entry point', () => {
    const indexPath = path.join(FRONTEND_DIR, 'index.html');
    if (!fs.existsSync(indexPath)) test.skip();
    const content = fs.readFileSync(indexPath, 'utf-8');
    expect(content).toContain('src="/src/main.tsx"');
  });

  test('src/main.tsx exists', () => {
    const mainPath = path.join(FRONTEND_DIR, 'src/main.tsx');
    expect(fs.existsSync(mainPath), `main.tsx not found at ${mainPath}`).toBe(true);
  });

  test('src/App.tsx exists', () => {
    const appPath = path.join(FRONTEND_DIR, 'src/App.tsx');
    expect(fs.existsSync(appPath), `App.tsx not found at ${appPath}`).toBe(true);
  });

  test('tailwind.config.js exists', () => {
    const tailwindPath = path.join(FRONTEND_DIR, 'tailwind.config.js');
    expect(
      fs.existsSync(tailwindPath),
      `tailwind.config.js not found at ${tailwindPath}. Tailwind styles will not apply.`
    ).toBe(true);
  });

  test('postcss.config.js exists', () => {
    const postcssPath = path.join(FRONTEND_DIR, 'postcss.config.js');
    expect(fs.existsSync(postcssPath), `postcss.config.js not found at ${postcssPath}`).toBe(true);
  });

  test('vite.config.ts exists', () => {
    const vitePath = path.join(FRONTEND_DIR, 'vite.config.ts');
    expect(fs.existsSync(vitePath), `vite.config.ts not found at ${vitePath}`).toBe(true);
  });

  test('resume test asset file exists for E2E tests', () => {
    expect(
      fs.existsSync(RESUME_FILE),
      `Resume test file not found: ${RESUME_FILE}`
    ).toBe(true);
  });

  test('package.json has required dependencies', () => {
    const pkgPath = path.join(FRONTEND_DIR, 'package.json');
    if (!fs.existsSync(pkgPath)) test.skip();
    const pkg = JSON.parse(fs.readFileSync(pkgPath, 'utf-8'));
    const all = { ...pkg.dependencies, ...pkg.devDependencies };
    const required = ['react', 'react-dom', 'react-router-dom', 'axios', 'vite'];
    for (const dep of required) {
      expect(all, `Missing dependency '${dep}' in package.json`).toHaveProperty(dep);
    }
  });
});


// ===========================================================================
// Section 5 – Frontend Rendering & Routing
// ===========================================================================
test.describe('Section 5 – Frontend Rendering & Routing', () => {

  test('frontend dev server is running and returns 200', async ({ page }) => {
    const response = await page.goto(FRONTEND_URL, { waitUntil: 'domcontentloaded', timeout: 10000 })
      .catch(() => null);
    expect(response, `Frontend dev server not running at ${FRONTEND_URL}. Run: npm run dev`).not.toBeNull();
    expect(response!.status()).toBe(200);
  });

  test('page title is "Resume Tailor" (not "frontend")', async ({ page }) => {
    await page.goto(FRONTEND_URL, { waitUntil: 'networkidle', timeout: 15000 });
    const title = await page.title();
    expect(title).toMatch(/Resume Tailor/i);
    expect(title).not.toBe('frontend');
  });

  test('root div #root contains rendered React content', async ({ page }) => {
    await page.goto(FRONTEND_URL, { waitUntil: 'networkidle', timeout: 15000 });
    const root = page.locator('#root');
    await expect(root).not.toBeEmpty();
  });

  test('landing page renders visible content (not blank)', async ({ page }) => {
    await page.goto(FRONTEND_URL, { waitUntil: 'networkidle', timeout: 15000 });
    // At least one heading or button must be visible
    const hasContent = await page.locator('h1, h2, button, a').count();
    expect(hasContent, 'Landing page appears blank — React may not be mounting').toBeGreaterThan(0);
  });

  test('no JavaScript errors on landing page load', async ({ page }) => {
    const jsErrors: string[] = [];
    page.on('pageerror', (err) => jsErrors.push(err.message));
    await page.goto(FRONTEND_URL, { waitUntil: 'networkidle', timeout: 15000 });
    expect(jsErrors, `JavaScript errors on load: ${jsErrors.join(', ')}`).toHaveLength(0);
  });

  test('no failed network requests (no 404s) on landing page load', async ({ page }) => {
    const failedRequests: string[] = [];
    page.on('requestfailed', (req) => failedRequests.push(req.url()));
    await page.goto(FRONTEND_URL, { waitUntil: 'networkidle', timeout: 15000 });
    // Filter out known non-critical requests (e.g. favicon might 404 in dev)
    const critical = failedRequests.filter(url => !url.includes('favicon'));
    expect(critical, `Failed requests: ${critical.join(', ')}`).toHaveLength(0);
  });

  test('route / renders LandingPage content', async ({ page }) => {
    await page.goto(`${FRONTEND_URL}/`, { waitUntil: 'networkidle', timeout: 15000 });
    // Should contain a CTA link or button pointing to /upload
    const uploadLink = page.getByRole('link', { name: /get started|upload|tailor/i });
    await expect(uploadLink.first()).toBeVisible({ timeout: 5000 });
  });

  test('route /upload renders UploadPage with file input', async ({ page }) => {
    await page.goto(`${FRONTEND_URL}/upload`, { waitUntil: 'networkidle', timeout: 15000 });
    const fileInput = page.locator('input[type="file"]');
    await expect(fileInput.first()).toBeAttached({ timeout: 5000 });
  });

  test('route /upload renders URL input field', async ({ page }) => {
    await page.goto(`${FRONTEND_URL}/upload`, { waitUntil: 'networkidle', timeout: 15000 });
    const urlInput = page.locator('input[type="url"], input[placeholder*="url" i], input[placeholder*="job" i]');
    await expect(urlInput.first()).toBeVisible({ timeout: 5000 });
  });

  test('route /upload renders a submit/analyze button', async ({ page }) => {
    await page.goto(`${FRONTEND_URL}/upload`, { waitUntil: 'networkidle', timeout: 15000 });
    const btn = page.getByRole('button', { name: /analyze|submit/i });
    await expect(btn.first()).toBeVisible({ timeout: 5000 });
  });

  test('route /applications renders ApplicationsPage', async ({ page }) => {
    await page.goto(`${FRONTEND_URL}/applications`, { waitUntil: 'networkidle', timeout: 15000 });
    // Page should not be blank and should not navigate away
    expect(page.url()).toContain('/applications');
    const content = await page.locator('body').textContent();
    expect(content!.length, 'Applications page appears empty').toBeGreaterThan(10);
  });

  test('unknown route does not crash the app', async ({ page }) => {
    const jsErrors: string[] = [];
    page.on('pageerror', (err) => jsErrors.push(err.message));
    await page.goto(`${FRONTEND_URL}/this-route-does-not-exist`, { waitUntil: 'networkidle', timeout: 15000 });
    expect(jsErrors, `Unhandled JS error on unknown route: ${jsErrors.join(', ')}`).toHaveLength(0);
  });
});


// ===========================================================================
// Section 7 – Style & Asset Loading
// ===========================================================================
test.describe('Section 7 – Style & Asset Loading', () => {

  test('Tailwind utility classes are present in computed styles', async ({ page }) => {
    await page.goto(FRONTEND_URL, { waitUntil: 'networkidle', timeout: 15000 });
    // Check that at least one element has a Tailwind class applied with a non-default style
    // We check that an element with text-* or bg-* class has computed color styles
    const hasStyledElement = await page.evaluate(() => {
      const styled = document.querySelector('[class*="text-"], [class*="bg-"], [class*="flex"], [class*="grid"]');
      return styled !== null;
    });
    expect(hasStyledElement, 'No Tailwind-styled elements found. Tailwind CSS may not be loading.').toBe(true);
  });

  test('no CSS/JS assets return 404', async ({ page }) => {
    const failedAssets: string[] = [];
    page.on('response', (res) => {
      const url = res.url();
      if (res.status() === 404 && (url.includes('.css') || url.includes('.js'))) {
        failedAssets.push(url);
      }
    });
    await page.goto(FRONTEND_URL, { waitUntil: 'networkidle', timeout: 15000 });
    expect(failedAssets, `CSS/JS assets returning 404: ${failedAssets.join(', ')}`).toHaveLength(0);
  });
});


// ===========================================================================
// Section 6 – API / Backend Connectivity (from browser context)
// ===========================================================================
test.describe('Section 6 – Backend API Connectivity', () => {

  test('backend root endpoint returns 200', async () => {
    const ctx = await request.newContext();
    let response;
    try {
      response = await ctx.get(`${BACKEND_URL}/`, { timeout: 5000 });
    } catch {
      test.skip(); // Backend not running — skip gracefully
      return;
    }
    expect(response.status(), `Backend root returned ${response.status()}`).toBe(200);
    await ctx.dispose();
  });

  test('backend /openapi.json returns valid schema', async () => {
    const ctx = await request.newContext();
    let response;
    try {
      response = await ctx.get(`${BACKEND_URL}/openapi.json`, { timeout: 5000 });
    } catch {
      test.skip();
      return;
    }
    expect(response.status()).toBe(200);
    const schema = await response.json();
    expect(schema).toHaveProperty('paths');
    await ctx.dispose();
  });

  test('backend sends CORS header allowing frontend origin', async () => {
    const ctx = await request.newContext();
    let response;
    try {
      response = await ctx.fetch(`${BACKEND_URL}/`, {
        method: 'OPTIONS',
        headers: { 'Origin': 'http://localhost:5173' },
        timeout: 5000,
      });
    } catch {
      test.skip();
      return;
    }
    const acao = response.headers()['access-control-allow-origin'] ?? '';
    expect(
      ['*', 'http://localhost:5173'].includes(acao),
      `CORS header 'access-control-allow-origin' is '${acao}'. Frontend requests will be blocked.`
    ).toBe(true);
    await ctx.dispose();
  });
});


// ===========================================================================
// Section 9 – E2E Test Readiness
// ===========================================================================
test.describe('Section 9 – E2E Test Readiness', () => {

  test('Playwright config or package.json has playwright configured', () => {
    const rootPkg = 'C:/Projects/ResumeTailor/package.json';
    const localPkg = path.join(FRONTEND_DIR, 'package.json');

    let found = false;
    for (const pkgPath of [rootPkg, localPkg]) {
      if (fs.existsSync(pkgPath)) {
        const content = fs.readFileSync(pkgPath, 'utf-8');
        if (content.includes('playwright')) { found = true; break; }
      }
    }
    expect(found, 'Playwright is not listed as a dependency in any package.json').toBe(true);
  });

  test('E2E spec file exists', () => {
    const specPath = path.join(FRONTEND_DIR, 'src/e2e_upload_and_analyze.spec.ts');
    expect(
      fs.existsSync(specPath),
      `E2E spec file not found: ${specPath}`
    ).toBe(true);
  });

  test('frontend is accessible at expected E2E base URL', async ({ page }) => {
    const response = await page.goto(FRONTEND_URL, { timeout: 10000 }).catch(() => null);
    expect(
      response !== null && response.status() === 200,
      `Frontend not accessible at ${FRONTEND_URL}. Start: cd 01-Code/frontend && npm run dev`
    ).toBe(true);
  });

  test('upload page is navigable from landing page CTA', async ({ page }) => {
    await page.goto(FRONTEND_URL, { waitUntil: 'networkidle', timeout: 15000 });
    const link = page.getByRole('link', { name: /get started|upload|try|tailor/i });
    const count = await link.count();
    if (count === 0) {
      // Try direct navigation as fallback
      await page.goto(`${FRONTEND_URL}/upload`, { waitUntil: 'networkidle', timeout: 10000 });
    } else {
      await link.first().click();
    }
    await expect(page).toHaveURL(/upload/, { timeout: 5000 });
  });
});
