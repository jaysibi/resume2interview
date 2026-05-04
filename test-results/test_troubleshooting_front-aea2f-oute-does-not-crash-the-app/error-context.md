# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: test_troubleshooting_frontend.spec.ts >> Section 5 – Frontend Rendering & Routing >> unknown route does not crash the app
- Location: test_troubleshooting_frontend.spec.ts:191:7

# Error details

```
Error: Unhandled JS error on unknown route: The requested module '/src/services/api.ts?t=1777808205324' does not provide an export named 'Application'

expect(received).toHaveLength(expected)

Expected length: 0
Received length: 1
Received array:  ["The requested module '/src/services/api.ts?t=1777808205324' does not provide an export named 'Application'"]
```

# Test source

```ts
  95  |   });
  96  | 
  97  |   test('package.json has required dependencies', () => {
  98  |     const pkgPath = path.join(FRONTEND_DIR, 'package.json');
  99  |     if (!fs.existsSync(pkgPath)) test.skip();
  100 |     const pkg = JSON.parse(fs.readFileSync(pkgPath, 'utf-8'));
  101 |     const all = { ...pkg.dependencies, ...pkg.devDependencies };
  102 |     const required = ['react', 'react-dom', 'react-router-dom', 'axios', 'vite'];
  103 |     for (const dep of required) {
  104 |       expect(all, `Missing dependency '${dep}' in package.json`).toHaveProperty(dep);
  105 |     }
  106 |   });
  107 | });
  108 | 
  109 | 
  110 | // ===========================================================================
  111 | // Section 5 – Frontend Rendering & Routing
  112 | // ===========================================================================
  113 | test.describe('Section 5 – Frontend Rendering & Routing', () => {
  114 | 
  115 |   test('frontend dev server is running and returns 200', async ({ page }) => {
  116 |     const response = await page.goto(FRONTEND_URL, { waitUntil: 'domcontentloaded', timeout: 10000 })
  117 |       .catch(() => null);
  118 |     expect(response, `Frontend dev server not running at ${FRONTEND_URL}. Run: npm run dev`).not.toBeNull();
  119 |     expect(response!.status()).toBe(200);
  120 |   });
  121 | 
  122 |   test('page title is "Resume Tailor" (not "frontend")', async ({ page }) => {
  123 |     await page.goto(FRONTEND_URL, { waitUntil: 'networkidle', timeout: 15000 });
  124 |     const title = await page.title();
  125 |     expect(title).toMatch(/Resume Tailor/i);
  126 |     expect(title).not.toBe('frontend');
  127 |   });
  128 | 
  129 |   test('root div #root contains rendered React content', async ({ page }) => {
  130 |     await page.goto(FRONTEND_URL, { waitUntil: 'networkidle', timeout: 15000 });
  131 |     const root = page.locator('#root');
  132 |     await expect(root).not.toBeEmpty();
  133 |   });
  134 | 
  135 |   test('landing page renders visible content (not blank)', async ({ page }) => {
  136 |     await page.goto(FRONTEND_URL, { waitUntil: 'networkidle', timeout: 15000 });
  137 |     // At least one heading or button must be visible
  138 |     const hasContent = await page.locator('h1, h2, button, a').count();
  139 |     expect(hasContent, 'Landing page appears blank — React may not be mounting').toBeGreaterThan(0);
  140 |   });
  141 | 
  142 |   test('no JavaScript errors on landing page load', async ({ page }) => {
  143 |     const jsErrors: string[] = [];
  144 |     page.on('pageerror', (err) => jsErrors.push(err.message));
  145 |     await page.goto(FRONTEND_URL, { waitUntil: 'networkidle', timeout: 15000 });
  146 |     expect(jsErrors, `JavaScript errors on load: ${jsErrors.join(', ')}`).toHaveLength(0);
  147 |   });
  148 | 
  149 |   test('no failed network requests (no 404s) on landing page load', async ({ page }) => {
  150 |     const failedRequests: string[] = [];
  151 |     page.on('requestfailed', (req) => failedRequests.push(req.url()));
  152 |     await page.goto(FRONTEND_URL, { waitUntil: 'networkidle', timeout: 15000 });
  153 |     // Filter out known non-critical requests (e.g. favicon might 404 in dev)
  154 |     const critical = failedRequests.filter(url => !url.includes('favicon'));
  155 |     expect(critical, `Failed requests: ${critical.join(', ')}`).toHaveLength(0);
  156 |   });
  157 | 
  158 |   test('route / renders LandingPage content', async ({ page }) => {
  159 |     await page.goto(`${FRONTEND_URL}/`, { waitUntil: 'networkidle', timeout: 15000 });
  160 |     // Should contain a CTA link or button pointing to /upload
  161 |     const uploadLink = page.getByRole('link', { name: /get started|upload|tailor/i });
  162 |     await expect(uploadLink.first()).toBeVisible({ timeout: 5000 });
  163 |   });
  164 | 
  165 |   test('route /upload renders UploadPage with file input', async ({ page }) => {
  166 |     await page.goto(`${FRONTEND_URL}/upload`, { waitUntil: 'networkidle', timeout: 15000 });
  167 |     const fileInput = page.locator('input[type="file"]');
  168 |     await expect(fileInput.first()).toBeAttached({ timeout: 5000 });
  169 |   });
  170 | 
  171 |   test('route /upload renders URL input field', async ({ page }) => {
  172 |     await page.goto(`${FRONTEND_URL}/upload`, { waitUntil: 'networkidle', timeout: 15000 });
  173 |     const urlInput = page.locator('input[type="url"], input[placeholder*="url" i], input[placeholder*="job" i]');
  174 |     await expect(urlInput.first()).toBeVisible({ timeout: 5000 });
  175 |   });
  176 | 
  177 |   test('route /upload renders a submit/analyze button', async ({ page }) => {
  178 |     await page.goto(`${FRONTEND_URL}/upload`, { waitUntil: 'networkidle', timeout: 15000 });
  179 |     const btn = page.getByRole('button', { name: /analyze|submit/i });
  180 |     await expect(btn.first()).toBeVisible({ timeout: 5000 });
  181 |   });
  182 | 
  183 |   test('route /applications renders ApplicationsPage', async ({ page }) => {
  184 |     await page.goto(`${FRONTEND_URL}/applications`, { waitUntil: 'networkidle', timeout: 15000 });
  185 |     // Page should not be blank and should not navigate away
  186 |     expect(page.url()).toContain('/applications');
  187 |     const content = await page.locator('body').textContent();
  188 |     expect(content!.length, 'Applications page appears empty').toBeGreaterThan(10);
  189 |   });
  190 | 
  191 |   test('unknown route does not crash the app', async ({ page }) => {
  192 |     const jsErrors: string[] = [];
  193 |     page.on('pageerror', (err) => jsErrors.push(err.message));
  194 |     await page.goto(`${FRONTEND_URL}/this-route-does-not-exist`, { waitUntil: 'networkidle', timeout: 15000 });
> 195 |     expect(jsErrors, `Unhandled JS error on unknown route: ${jsErrors.join(', ')}`).toHaveLength(0);
      |                                                                                     ^ Error: Unhandled JS error on unknown route: The requested module '/src/services/api.ts?t=1777808205324' does not provide an export named 'Application'
  196 |   });
  197 | });
  198 | 
  199 | 
  200 | // ===========================================================================
  201 | // Section 7 – Style & Asset Loading
  202 | // ===========================================================================
  203 | test.describe('Section 7 – Style & Asset Loading', () => {
  204 | 
  205 |   test('Tailwind utility classes are present in computed styles', async ({ page }) => {
  206 |     await page.goto(FRONTEND_URL, { waitUntil: 'networkidle', timeout: 15000 });
  207 |     // Check that at least one element has a Tailwind class applied with a non-default style
  208 |     // We check that an element with text-* or bg-* class has computed color styles
  209 |     const hasStyledElement = await page.evaluate(() => {
  210 |       const styled = document.querySelector('[class*="text-"], [class*="bg-"], [class*="flex"], [class*="grid"]');
  211 |       return styled !== null;
  212 |     });
  213 |     expect(hasStyledElement, 'No Tailwind-styled elements found. Tailwind CSS may not be loading.').toBe(true);
  214 |   });
  215 | 
  216 |   test('no CSS/JS assets return 404', async ({ page }) => {
  217 |     const failedAssets: string[] = [];
  218 |     page.on('response', (res) => {
  219 |       const url = res.url();
  220 |       if (res.status() === 404 && (url.includes('.css') || url.includes('.js'))) {
  221 |         failedAssets.push(url);
  222 |       }
  223 |     });
  224 |     await page.goto(FRONTEND_URL, { waitUntil: 'networkidle', timeout: 15000 });
  225 |     expect(failedAssets, `CSS/JS assets returning 404: ${failedAssets.join(', ')}`).toHaveLength(0);
  226 |   });
  227 | });
  228 | 
  229 | 
  230 | // ===========================================================================
  231 | // Section 6 – API / Backend Connectivity (from browser context)
  232 | // ===========================================================================
  233 | test.describe('Section 6 – Backend API Connectivity', () => {
  234 | 
  235 |   test('backend root endpoint returns 200', async () => {
  236 |     const ctx = await request.newContext();
  237 |     let response;
  238 |     try {
  239 |       response = await ctx.get(`${BACKEND_URL}/`, { timeout: 5000 });
  240 |     } catch {
  241 |       test.skip(); // Backend not running — skip gracefully
  242 |       return;
  243 |     }
  244 |     expect(response.status(), `Backend root returned ${response.status()}`).toBe(200);
  245 |     await ctx.dispose();
  246 |   });
  247 | 
  248 |   test('backend /openapi.json returns valid schema', async () => {
  249 |     const ctx = await request.newContext();
  250 |     let response;
  251 |     try {
  252 |       response = await ctx.get(`${BACKEND_URL}/openapi.json`, { timeout: 5000 });
  253 |     } catch {
  254 |       test.skip();
  255 |       return;
  256 |     }
  257 |     expect(response.status()).toBe(200);
  258 |     const schema = await response.json();
  259 |     expect(schema).toHaveProperty('paths');
  260 |     await ctx.dispose();
  261 |   });
  262 | 
  263 |   test('backend sends CORS header allowing frontend origin', async () => {
  264 |     const ctx = await request.newContext();
  265 |     let response;
  266 |     try {
  267 |       response = await ctx.fetch(`${BACKEND_URL}/`, {
  268 |         method: 'OPTIONS',
  269 |         headers: { 'Origin': 'http://localhost:5173' },
  270 |         timeout: 5000,
  271 |       });
  272 |     } catch {
  273 |       test.skip();
  274 |       return;
  275 |     }
  276 |     const acao = response.headers()['access-control-allow-origin'] ?? '';
  277 |     expect(
  278 |       ['*', 'http://localhost:5173'].includes(acao),
  279 |       `CORS header 'access-control-allow-origin' is '${acao}'. Frontend requests will be blocked.`
  280 |     ).toBe(true);
  281 |     await ctx.dispose();
  282 |   });
  283 | });
  284 | 
  285 | 
  286 | // ===========================================================================
  287 | // Section 9 – E2E Test Readiness
  288 | // ===========================================================================
  289 | test.describe('Section 9 – E2E Test Readiness', () => {
  290 | 
  291 |   test('Playwright config or package.json has playwright configured', () => {
  292 |     const rootPkg = 'C:/Projects/ResumeTailor/package.json';
  293 |     const localPkg = path.join(FRONTEND_DIR, 'package.json');
  294 | 
  295 |     let found = false;
```