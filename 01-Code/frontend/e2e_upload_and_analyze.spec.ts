import { test, expect } from '@playwright/test';
import path from 'path';

// Path to the resume file in the shared test folder
const resumePath = path.resolve('C:/Projects/ResumeTailor/03-Testing/Resume - Jayendra Sibi (1).docx');
const jobUrl = 'https://www.naukri.com/job-listings-quality-analyst-charles-river-tata-consultancy-services-noida-chennai-bengaluru-8-to-10-years-210426031187?src=jobsearchDesk&sid=1777768086260882&xp=2&px=1';

// Main E2E test for Resume2Interview V2 frontend

test.describe('Resume2Interview V2 E2E', () => {
  test('Upload resume, fetch JD from URL, analyze, and verify results', async ({ page }) => {
    // 1. Launch the application
    await page.goto('http://localhost:5173/');
    await expect(page).toHaveTitle(/Resume2Interview|Upload/i);

    // 2. Upload the resume file
    const fileInput = await page.locator('input[type="file"]').first();
    await fileInput.setInputFiles(resumePath);
    await expect(fileInput).toHaveValue(/Jayendra Sibi/i);

    // 3. Enter the job URL
    const urlInput = await page.locator('input[type="url"]');
    await urlInput.fill(jobUrl);
    await expect(urlInput).toHaveValue(jobUrl);

    // 4. Hit Submit/Analyze
    const submitBtn = await page.getByRole('button', { name: /analyze|submit/i });
    await expect(submitBtn).toBeEnabled();
    await submitBtn.click();

    // 5. Wait for loading and analyze output
    await expect(page.locator('text=Fetching job description')).not.toBeVisible({ timeout: 15000 });
    await expect(page.locator('text=Match Score')).toBeVisible({ timeout: 20000 });
    await expect(page.locator('text=Gap Analysis')).toBeVisible();
    await expect(page.locator('text=ATS Score')).toBeVisible();

    // Additional verification & checkpoints
    // Check that the match score is displayed and is a number
    const matchScore = await page.locator('text=Match Score').textContent();
    expect(matchScore).toMatch(/\d+%/);

    // Check that skills comparison is visible
    await expect(page.locator('text=Matching Skills')).toBeVisible();
    await expect(page.locator('text=Missing Skills')).toBeVisible();

    // Check that application is created in backend (Applications link visible)
    await expect(page.getByRole('link', { name: /applications/i })).toBeVisible();

    // Go to Applications page and verify the new application appears
    await page.getByRole('link', { name: /applications/i }).click();
    await expect(page).toHaveURL(/applications/);
    await expect(page.locator('text=Quality Analyst')).toBeVisible();
    await expect(page.locator('text=Jayendra Sibi')).toBeVisible();

    // Open application detail and verify details
    await page.getByRole('button', { name: /view details/i }).first().click();
    await expect(page).toHaveURL(/applications\/[0-9]+/);
    await expect(page.locator('text=Gap Analysis')).toBeVisible();
    await expect(page.locator('text=ATS Score')).toBeVisible();
    await expect(page.locator('text=Job URL')).toContainText('naukri.com');
  });
});
