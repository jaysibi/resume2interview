#!/usr/bin/env node

/**
 * One-Click Setup Script
 * Installs all dependencies and configures the video generator
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

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

function step(title) {
  log(`\n${'='.repeat(60)}`, 'blue');
  log(title, 'bright');
  log(`${'='.repeat(60)}`, 'blue');
}

function exec(command, description) {
  log(`\n${description}...`, 'blue');
  try {
    execSync(command, { stdio: 'inherit' });
    log(`✅ ${description} complete`, 'green');
    return true;
  } catch (error) {
    log(`❌ ${description} failed`, 'red');
    return false;
  }
}

async function main() {
  log('\n' + '🚀'.repeat(30), 'bright');
  log('AUTOMATED VIDEO GENERATOR SETUP', 'bright');
  log('🚀'.repeat(30) + '\n', 'bright');
  
  step('Step 1: Node.js Dependencies');
  exec('npm install', 'Installing Node.js packages');
  
  step('Step 2: Playwright Browser');
  exec('npx playwright install chromium', 'Installing Chromium browser');
  
  step('Step 3: Python Dependencies');
  exec('pip install -r requirements.txt', 'Installing Python packages');
  
  step('Step 4: Creating Configuration');
  
  // Create .env file if doesn't exist
  const envPath = path.join(__dirname, '.env');
  if (!fs.existsSync(envPath)) {
    const envTemplate = `# Video Generator Configuration

SITE_URL=https://resume2interview.com
SAMPLE_RESUME_PATH=../../DEMO_VIDEO_SAMPLES.md
SAMPLE_JD_PATH=../../DEMO_VIDEO_SAMPLES.md
OUTPUT_DIR=./output

# Voice Provider: gtts (free) or elevenlabs (paid, better quality)
VOICE_PROVIDER=gtts

# ElevenLabs (optional, for premium voices)
# ELEVENLABS_API_KEY=your_key_here
# ELEVENLABS_VOICE_ID=21m00Tcm4TlvDq8ikWAM
`;
    fs.writeFileSync(envPath, envTemplate);
    log('✅ Created .env configuration file', 'green');
  } else {
    log('⚠️  .env file already exists, skipping', 'yellow');
  }
  
  // Create config.json if doesn't exist
  const configPath = path.join(__dirname, 'config.json');
  if (!fs.existsSync(configPath)) {
    const config = {
      recording: {
        width: 1920,
        height: 1080,
        fps: 30,
        bitrate: "5M"
      },
      brand_colors: {
        primary: "#2563EB",
        secondary: "#FFFFFF"
      },
      text_overlays: {
        font: "Arial-Bold",
        size: 48,
        position: "bottom-center",
        color: "#FFFFFF",
        outline_color: "#000000"
      },
      logo: {
        enabled: false,
        path: "../../frontend/public/logo.png",
        position: "top-right",
        size: 100
      },
      audio: {
        background_music_volume: 0.15,
        voiceover_volume: 1.0
      }
    };
    fs.writeFileSync(configPath, JSON.stringify(config, null, 2));
    log('✅ Created config.json', 'green');
  } else {
    log('⚠️  config.json already exists, skipping', 'yellow');
  }
  
  // Create output directory
  const outputDir = path.join(__dirname, 'output');
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
    log('✅ Created output directory', 'green');
  }
  
  step('Setup Complete!');
  
  log('\n📋 Next Steps:', 'blue');
  log('   Generate your video:', 'green');
  log('      node generate-video.js\n', 'bright');
  
  log('   What happens:', 'yellow');
  log('      • Records 90-second demo (automated)');
  log('      • Generates AI voiceover');
  log('      • Compiles video with overlays');
  log('      • Copies to frontend/public/demo-video.mp4');
  log('      • Commits and pushes to GitHub');
  log('      • Vercel auto-deploys in 2-3 min');
  
  log('\n💡 Optional: Premium Voice (ElevenLabs)', 'yellow');
  log('   • Get API key: https://elevenlabs.io/');
  log('   • Add to .env: ELEVENLABS_API_KEY=your_key');
  log('   • Cost: ~$0.30 per video (much better quality)\n');
  
  log('✨ Setup complete! Ready to generate your demo video.', 'bright');
}

main();
