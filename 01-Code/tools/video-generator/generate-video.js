#!/usr/bin/env node

/**
 * Automated Demo Video Generator
 * Orchestrates full video creation pipeline
 */

const { execSync } = require('child_process');
const fs = require('fs-extra');
const path = require('path');
require('dotenv').config();

const OUTPUT_DIR = path.join(__dirname, 'output');
const CONFIG_FILE = path.join(__dirname, 'config.json');

// ANSI color codes for terminal output
const colors = {
  reset: '\x1b[0m',
  bright: '\x1b[1m',
  green: '\x1b[32m',
  blue: '\x1b[34m',
  yellow: '\x1b[33m',
  red: '\x1b[31m',
};

function log(message, color = 'reset') {
  console.log(`${colors[color]}${message}${colors.reset}`);
}

function step(number, title) {
  log(`\n${'='.repeat(60)}`, 'blue');
  log(`STEP ${number}: ${title}`, 'bright');
  log(`${'='.repeat(60)}`, 'blue');
}

async function checkPrerequisites() {
  step(0, 'Checking Prerequisites');
  
  const checks = [
    { name: 'Node.js', command: 'node --version' },
    { name: 'Python', command: 'python --version' },
    { name: 'FFmpeg', command: 'ffmpeg -version' },
    { name: 'Playwright', command: 'npx playwright --version' },
  ];

  for (const check of checks) {
    try {
      const result = execSync(check.command, { encoding: 'utf-8' });
      log(`✅ ${check.name}: ${result.split('\n')[0]}`, 'green');
    } catch (error) {
      log(`❌ ${check.name}: NOT FOUND`, 'red');
      log(`   Install: See README.md for installation instructions`, 'yellow');
      process.exit(1);
    }
  }
  
  // Check Python packages
  log('\nChecking Python packages...', 'blue');
  const pythonPackages = ['moviepy', 'gtts', 'google-api-python-client'];
  
  for (const pkg of pythonPackages) {
    try {
      execSync(`python -c "import ${pkg.replace('-', '_')}"`, { stdio: 'ignore' });
      log(`✅ ${pkg}`, 'green');
    } catch (error) {
      log(`❌ ${pkg}: NOT FOUND`, 'red');
      log(`   Install: pip install ${pkg}`, 'yellow');
      process.exit(1);
    }
  }
}

async function setupOutputDirectory() {
  step(1, 'Setting Up Output Directory');
  
  if (fs.existsSync(OUTPUT_DIR)) {
    log('Output directory exists, cleaning...', 'yellow');
    fs.emptyDirSync(OUTPUT_DIR);
  } else {
    log('Creating output directory...', 'blue');
    fs.mkdirSync(OUTPUT_DIR, { recursive: true });
  }
  
  log(`✅ Output directory ready: ${OUTPUT_DIR}`, 'green');
}

async function recordDemo() {
  step(2, 'Recording Screen Demo');
  
  log('Starting Playwright browser automation...', 'blue');
  log('This will take 2-3 minutes...', 'yellow');
  
  try {
    execSync('node record-demo.js', { 
      stdio: 'inherit',
      cwd: __dirname 
    });
    log('✅ Screen recording complete!', 'green');
  } catch (error) {
    log('❌ Recording failed', 'red');
    throw error;
  }
}

async function generateVoiceover() {
  step(3, 'Generating AI Voiceover');
  
  log('Converting script to speech...', 'blue');
  log('This will take 1-2 minutes...', 'yellow');
  
  try {
    execSync('python generate-voiceover.py', {
      stdio: 'inherit',
      cwd: __dirname
    });
    log('✅ Voiceover generated!', 'green');
  } catch (error) {
    log('❌ Voiceover generation failed', 'red');
    throw error;
  }
}

async function compileVideo() {
  step(4, 'Compiling Final Video');
  
  log('Adding voiceover, overlays, and effects...', 'blue');
  log('This will take 3-5 minutes...', 'yellow');
  
  try {
    execSync('python compile-video.py', {
      stdio: 'inherit',
      cwd: __dirname
    });
    log('✅ Video compilation complete!', 'green');
  } catch (error) {
    log('❌ Video compilation failed', 'red');
    throw error;
  }
}

async function uploadToYouTube() {
  step(5, 'Uploading to YouTube');
  
  log('Authenticating with YouTube API...', 'blue');
  log('This will take 2-3 minutes...', 'yellow');
  log('⚠️  Browser may open for OAuth authentication', 'yellow');
  
  try {
    execSync('python upload-to-youtube.py', {
      stdio: 'inherit',
      cwd: __dirname
    });
    log('✅ Video uploaded to YouTube!', 'green');
  } catch (error) {
    log('❌ YouTube upload failed', 'red');
    throw error;
  }
}

async function updateWebsite() {
  step(6, 'Updating Website');
  
  log('Reading video ID from YouTube...', 'blue');
  
  const videoIdFile = path.join(OUTPUT_DIR, 'video-id.txt');
  if (!fs.existsSync(videoIdFile)) {
    log('❌ Video ID not found. Upload may have failed.', 'red');
    return;
  }
  
  const videoId = fs.readFileSync(videoIdFile, 'utf-8').trim();
  log(`Video ID: ${videoId}`, 'blue');
  
  log('Updating landing page...', 'blue');
  
  try {
    execSync(`node update-website.js ${videoId}`, {
      stdio: 'inherit',
      cwd: __dirname
    });
    log('✅ Website updated!', 'green');
  } catch (error) {
    log('❌ Website update failed', 'red');
    throw error;
  }
}

async function printSummary() {
  step(7, 'Summary');
  
  const videoIdFile = path.join(OUTPUT_DIR, 'video-id.txt');
  const videoId = fs.existsSync(videoIdFile) 
    ? fs.readFileSync(videoIdFile, 'utf-8').trim()
    : 'N/A';
  
  const videoFile = path.join(OUTPUT_DIR, 'resume2interview-demo-final.mp4');
  const fileSize = fs.existsSync(videoFile)
    ? (fs.statSync(videoFile).size / (1024 * 1024)).toFixed(2)
    : 'N/A';
  
  log('\n' + '🎉'.repeat(30), 'green');
  log('VIDEO GENERATION COMPLETE!', 'bright');
  log('🎉'.repeat(30) + '\n', 'green');
  
  log('📊 Results:', 'blue');
  log(`   Video File: ${videoFile}`);
  log(`   File Size: ${fileSize} MB`);
  log(`   Video ID: ${videoId}`);
  log(`   YouTube URL: https://youtube.com/watch?v=${videoId}`, 'green');
  log(`   Website: https://resume2interview.com`, 'green');
  
  log('\n📋 Next Steps:', 'blue');
  log('   1. Visit https://resume2interview.com to see the video live');
  log('   2. Share on LinkedIn, Twitter, Reddit');
  log('   3. Add to Product Hunt submission');
  log('   4. Monitor GA4 for video_play events');
  
  log('\n💡 Pro Tips:', 'yellow');
  log('   • Check YouTube Analytics after 24 hours');
  log('   • A/B test different thumbnails');
  log('   • Share in relevant subreddits');
  log('   • Pin to top of social profiles');
  
  log('\n✨ Done! Video is live and tracking in GA4.', 'bright');
}

async function main() {
  const startTime = Date.now();
  
  log('\n' + '🎬'.repeat(30), 'bright');
  log('AUTOMATED DEMO VIDEO GENERATOR', 'bright');
  log('Resume2Interview', 'blue');
  log('🎬'.repeat(30) + '\n', 'bright');
  
  try {
    await checkPrerequisites();
    await setupOutputDirectory();
    await recordDemo();
    await generateVoiceover();
    await compileVideo();
    await uploadToYouTube();
    await updateWebsite();
    await printSummary();
    
    const duration = ((Date.now() - startTime) / 1000 / 60).toFixed(1);
    log(`\n⏱️  Total time: ${duration} minutes`, 'green');
    
  } catch (error) {
    log('\n❌ ERROR: Video generation failed', 'red');
    log(error.message, 'red');
    log('\n💡 Check error logs in output/error-log.txt', 'yellow');
    
    // Save error log
    fs.writeFileSync(
      path.join(OUTPUT_DIR, 'error-log.txt'),
      `${new Date().toISOString()}\n${error.stack}`
    );
    
    process.exit(1);
  }
}

// Run if called directly
if (require.main === module) {
  main();
}

module.exports = { main };
