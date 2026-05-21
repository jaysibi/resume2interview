#!/usr/bin/env node

/**
 * PLAYWRIGHT SCREEN RECORDER
 * Automates browser interactions and records screen demo
 */

const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs-extra');
require('dotenv').config();

const SITE_URL = process.env.SITE_URL || 'https://resume2interview.com';
const OUTPUT_DIR = path.join(__dirname, 'output');
const VIDEO_PATH = path.join(OUTPUT_DIR, 'screen-recording.webm');

// Sample data from DEMO_VIDEO_SAMPLES.md
const SAMPLE_RESUME = `Alex Morgan
Senior Software Engineer | San Francisco, CA | alex.morgan@email.com | 555-0123

PROFESSIONAL SUMMARY
Results-driven Senior Software Engineer with 5+ years of experience building scalable web applications. 
Proficient in React, Node.js, Python, and cloud technologies. Strong problem-solver with proven track 
record of delivering high-quality code in fast-paced environments.

TECHNICAL SKILLS
• Languages: JavaScript, TypeScript, Python, Java
• Frontend: React, Redux, Next.js, TailwindCSS
• Backend: Node.js, Express, Django, FastAPI
• Databases: PostgreSQL, MongoDB, Redis
• Tools: Git, Docker, AWS, CI/CD

PROFESSIONAL EXPERIENCE

Software Engineer | TechStart Solutions | 2020 - Present
• Developed RESTful APIs using Node.js serving 100K+ daily users
• Built responsive React dashboards improving user engagement by 40%
• Implemented automated testing reducing production bugs by 35%
• Collaborated with cross-functional teams in Agile environment

Junior Developer | Digital Innovations | 2018 - 2020
• Created web applications using JavaScript and Python
• Maintained legacy codebases and improved performance
• Participated in code reviews and sprint planning

EDUCATION
Bachelor of Science in Computer Science | University of California | 2018

CERTIFICATIONS
AWS Certified Developer - Associate`;

const SAMPLE_JD = `Senior Full-Stack Engineer
InnovateTech | San Francisco, CA | Full-time

About the Role:
We're seeking a talented Senior Full-Stack Engineer to join our growing engineering team. You'll be 
responsible for building and maintaining our core product platform, working with modern technologies 
to deliver exceptional user experiences.

Requirements:
• 5+ years of software development experience
• Strong proficiency in React, TypeScript, and Node.js
• Experience with modern frontend frameworks (Next.js, Vue, or Angular)
• Backend development with Python or Node.js
• Database design and optimization (PostgreSQL, MongoDB)
• RESTful API development and microservices architecture
• Cloud platforms (AWS, Azure, or GCP)
• Docker and containerization
• GraphQL experience preferred
• CI/CD pipelines and DevOps practices
• Excellent problem-solving and communication skills
• Bachelor's degree in Computer Science or related field

Nice to Have:
• Kubernetes experience
• Machine Learning / AI integration
• Open-source contributions
• Experience with high-traffic applications
• System design expertise

What We Offer:
• Competitive salary and equity
• Remote-first culture
• Health, dental, and vision insurance
• 401(k) matching
• Professional development budget
• Flexible PTO

InnovateTech is building the future of enterprise software. Join us!`;

async function recordDemo() {
  console.log('\n🎥 Starting browser automation and screen recording...\n');
  
  let browser;
  let context;
  
  try {
    // Launch browser with recording
    browser = await chromium.launch({
      headless: false, // Show browser so we can see what's happening
      args: ['--window-size=1920,1080']
    });
    
    // Create context with video recording
    context = await browser.newContext({
      viewport: { width: 1920, height: 1080 },
      recordVideo: {
        dir: OUTPUT_DIR,
        size: { width: 1920, height: 1080 }
      },
      deviceScaleFactor: 1
    });
    
    const page = await context.newPage();
    
    // ============================================================
    // SCENE 1: Landing Page (5 seconds)
    // ============================================================
    console.log('▶ Scene 1: Landing page...');
    await page.goto(SITE_URL, { waitUntil: 'networkidle' });
    await page.waitForTimeout(5000); // Let landing page show
    
    // ============================================================
    // SCENE 2: Navigate to Upload (2 seconds)
    // ============================================================
    console.log('▶ Scene 2: Navigating to upload...');
    
    // Click "Get Started" or navigate to /upload
    try {
      // Try to find Get Started button
      const getStartedButton = await page.locator('text=/Get Started|Try.*Free|Start.*Now/i').first();
      if (await getStartedButton.isVisible({ timeout: 2000 }).catch(() => false)) {
        await getStartedButton.click();
      } else {
        // Direct navigation fallback
        await page.goto(`${SITE_URL}/upload`);
      }
    } catch (e) {
      // Fallback: navigate directly
      await page.goto(`${SITE_URL}/upload`);
    }
    
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(2000);
    
    // ============================================================
    // SCENE 3: Upload Resume (15 seconds)
    // ============================================================
    console.log('▶ Scene 3: Uploading resume...');
    
    // Create temporary resume file
    const tempResumeFile = path.join(OUTPUT_DIR, 'temp-resume.txt');
    await fs.writeFile(tempResumeFile, SAMPLE_RESUME);
    
    // Find and interact with file upload
    const fileInput = await page.locator('input[type="file"]').first();
    await fileInput.setInputFiles(tempResumeFile);
    
    console.log('   File selected, waiting for UI update...');
    await page.waitForTimeout(2000);
    
    // Click "Upload Resume" button
    console.log('   Clicking Upload Resume button...');
    try {
      const uploadResumeButton = await page.locator('button:has-text("Upload Resume")').first();
      await uploadResumeButton.waitFor({ state: 'visible', timeout: 5000 });
      await uploadResumeButton.click();
      console.log('   Resume upload started...');
    } catch (error) {
      console.log('   ⚠️ Upload Resume button not found, may already be uploaded');
    }
    
    // Wait for resume upload to complete
    console.log('   Waiting for resume processing...');
    await page.waitForTimeout(8000); // Give time for API call and processing
    
    // ============================================================
    // SCENE 4: Paste Job Description (15 seconds)
    // ============================================================
    console.log('▶ Scene 4: Pasting job description...');
    
    // Find job description textarea (might be in a tab)
    await page.waitForTimeout(1000);
    
    const jdTextarea = await page.locator('textarea').first();
    await jdTextarea.click();
    await page.waitForTimeout(500);
    
    // Type the JD text (more realistic than instant fill)
    console.log('   Typing job description...');
    await jdTextarea.fill(SAMPLE_JD);
    
    await page.waitForTimeout(2000);
    
    // Click "Upload" button for JD text
    console.log('   Clicking Upload JD button...');
    try {
      // Look for button with text like "Upload", "Submit", etc near the textarea
      const uploadJDButton = await page.locator('button:has-text("Upload")').last(); // Use last() to get JD upload button
      await uploadJDButton.waitFor({ state: 'visible', timeout: 5000 });
      await uploadJDButton.click();
      console.log('   JD upload started...');
    } catch (error) {
      console.log('   ⚠️ Upload JD button not found, trying alternative...');
      // Try finding by button near form
      await page.locator('button').filter({ hasText: /Upload|Submit/i }).last().click();
    }
    
    // Wait for JD upload to complete
    console.log('   Waiting for JD processing...');
    await page.waitForTimeout(6000);
    
    // ============================================================
    // SCENE 5: Wait for Button to Enable & Click (5 seconds)
    // ============================================================
    console.log('▶ Scene 5: Waiting for analyze button...');
    
    // Wait for button to become enabled (not disabled)
    const analyzeButton = await page.locator('button:has-text("Analyze")').first();
    
    try {
      // Wait up to 15 seconds for button to be enabled
      await analyzeButton.waitFor({ state: 'visible', timeout: 5000 });
      
      // Check if button is still disabled, wait a bit more
      let attempts = 0;
      while (attempts < 15) {
        const isDisabled = await analyzeButton.evaluate(btn => btn.hasAttribute('disabled'));
        if (!isDisabled) {
          console.log('   ✅ Button is enabled!');
          break;
        }
        console.log(`   Button still disabled, waiting... (attempt ${attempts + 1}/15)`);
        await page.waitForTimeout(1000);
        attempts++;
      }
      
      // Click the button
      console.log('   Clicking analyze button...');
      await analyzeButton.click({ timeout: 5000 });
      
    } catch (error) {
      console.log('   ❌ Could not click analyze button:', error.message);
      throw new Error('Analyze button did not become enabled. Check if uploads completed successfully.');
    }
    
    await page.waitForTimeout(2000);
    
    // ============================================================
    // SCENE 6: Loading State (5 seconds)
    // ============================================================
    console.log('▶ Scene 6: Waiting for analysis...');
    
    // Wait for results page or loading indicator
    try {
      await page.waitForURL('**/results*', { timeout: 30000 });
    } catch (e) {
      console.log('  ⚠ Results page not detected, waiting 5 seconds...');
    }
    
    await page.waitForTimeout(5000);
    
    // ============================================================
    // SCENE 7: Results (30 seconds)
    // ============================================================
    console.log('▶ Scene 7: Showing results...');
    
    // Scroll to show different sections
    await page.evaluate(() => window.scrollTo(0, 0));
    await page.waitForTimeout(5000);
    
    // Scroll to ATS score
    await page.evaluate(() => window.scrollTo(0, 300));
    await page.waitForTimeout(4000);
    
    // Scroll to recommendations
    await page.evaluate(() => window.scrollTo(0, 800));
    await page.waitForTimeout(5000);
    
    // Scroll further
    await page.evaluate(() => window.scrollTo(0, 1500));
    await page.waitForTimeout(4000);
    
    // Scroll back to top for closing
    await page.evaluate(() => window.scrollTo(0, 0));
    await page.waitForTimeout(3000);
    
    // ============================================================
    // SCENE 8: Call to Action (5 seconds)
    // ============================================================
    console.log('▶ Scene 8: Final CTA...');
    
    // Stay on results or navigate back to landing
    await page.waitForTimeout(5000);
    
    console.log('\n✅ Recording complete!\n');
    
    // Close context to save video
    await context.close();
    await browser.close();
    
    // Find the recorded video file
    const files = await fs.readdir(OUTPUT_DIR);
    const videoFile = files.find(f => f.endsWith('.webm'));
    
    if (videoFile) {
      const sourcePath = path.join(OUTPUT_DIR, videoFile);
      const targetPath = path.join(OUTPUT_DIR, 'screen-recording.webm');
      
      // Rename to standard name
      await fs.move(sourcePath, targetPath, { overwrite: true });
      
      console.log('📹 Video saved to: output/screen-recording.webm');
      console.log('   Duration: ~85-90 seconds');
      console.log('   Resolution: 1920x1080');
      
      // Clean up temp files
      await fs.remove(tempResumeFile).catch(() => {});
      
      return targetPath;
    } else {
      throw new Error('Video file not found in output directory');
    }
    
  } catch (error) {
    console.error('\n❌ Recording failed:', error.message);
    
    // Clean up
    if (context) await context.close().catch(() => {});
    if (browser) await browser.close().catch(() => {});
    
    throw error;
  }
}

// Run if called directly
if (require.main === module) {
  recordDemo()
    .then(() => {
      console.log('\n🎉 Screen recording successful!\n');
      process.exit(0);
    })
    .catch((error) => {
      console.error('\n💥 Fatal error:', error);
      process.exit(1);
    });
}

module.exports = { recordDemo };
