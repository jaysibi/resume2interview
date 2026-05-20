# Automated Demo Video Generator for Resume2Interview

This tool automatically creates, edits, and uploads your demo video to YouTube with zero manual intervention.

## Features

✅ **Automated Screen Recording** - Navigates your site and records interactions
✅ **AI-Generated Voiceover** - Converts script to natural speech
✅ **Automatic Video Editing** - Adds text overlays, transitions, timing
✅ **YouTube Auto-Upload** - Uploads with optimized metadata
✅ **Website Auto-Update** - Updates your landing page with video ID

## Tech Stack

- **Playwright** - Automated browser control and recording
- **FFmpeg** - Video processing and editing
- **gTTS/ElevenLabs** - Text-to-speech voiceover
- **YouTube Data API v3** - Automatic upload
- **MoviePy** - Video composition and effects

## Installation

```bash
# Navigate to project root
cd C:\Projects\ResumeTailor\01-Code

# Install Node.js dependencies
npm install playwright @playwright/test ffmpeg-static
npx playwright install chromium

# Install Python dependencies
pip install moviepy gTTS google-api-python-client google-auth-oauthlib Pillow
```

## Setup

### 1. YouTube API Credentials

1. Go to: https://console.cloud.google.com/
2. Create new project: "Resume2Interview"
3. Enable **YouTube Data API v3**
4. Create **OAuth 2.0 credentials**
5. Download credentials as `youtube_credentials.json`
6. Place in: `01-Code/tools/video-generator/youtube_credentials.json`

### 2. Configuration

Create `.env` file in `01-Code/tools/video-generator/`:

```env
SITE_URL=https://resume2interview.com
SAMPLE_RESUME_PATH=../../DEMO_VIDEO_SAMPLES.md
SAMPLE_JD_PATH=../../DEMO_VIDEO_SAMPLES.md
OUTPUT_DIR=./output
YOUTUBE_CREDENTIALS=./youtube_credentials.json
VOICE_PROVIDER=gtts
# Options: gtts (free), elevenlabs (paid, better quality)
ELEVENLABS_API_KEY=your_key_here
```

## Usage

### Quick Start (One Command)

```bash
cd 01-Code/tools/video-generator
node generate-video.js
```

This will:
1. ✅ Record your site demo
2. ✅ Generate voiceover
3. ✅ Edit video with overlays
4. ✅ Upload to YouTube
5. ✅ Update your landing page
6. ✅ Commit and push changes

**Estimated time:** 10-15 minutes

### Step-by-Step (Manual Control)

```bash
# Step 1: Record screen interactions
node record-demo.js

# Step 2: Generate voiceover
python generate-voiceover.py

# Step 3: Compile final video
python compile-video.py

# Step 4: Upload to YouTube
python upload-to-youtube.py

# Step 5: Update website
node update-website.js
```

## How It Works

### Phase 1: Recording (2-3 minutes)

The script:
1. Opens Playwright browser in headless mode
2. Navigates to resume2interview.com
3. Performs these actions automatically:
   - Loads landing page (2 seconds)
   - Navigates to /upload (2 seconds)
   - Uploads sample resume file (3 seconds)
   - Pastes sample job description (3 seconds)
   - Clicks "Analyze Resume" (1 second)
   - Waits for results to load (10 seconds)
   - Scrolls through results (5 seconds)
   - Returns to landing page (2 seconds)
4. Captures video at 30fps (1920x1080)

**Output:** `output/screen-recording.mp4` (30 seconds)

### Phase 2: Voiceover Generation (1 minute)

The script:
1. Reads script from DEMO_VIDEO_GUIDE.md
2. Splits script into timestamps:
   ```
   [0-8s]: "Applying to jobs but getting rejected..."
   [8-15s]: "Most Applicant Tracking Systems..."
   [15-22s]: "Resume2Interview uses AI..."
   ```
3. Generates speech using gTTS or ElevenLabs
4. Normalizes audio levels
5. Adds subtle background music (royalty-free)

**Output:** `output/voiceover.mp3` (90 seconds)

### Phase 3: Video Compilation (2-3 minutes)

The script:
1. Syncs screen recording with voiceover
2. Speeds up slow sections (loading screens at 2x)
3. Adds text overlays at key moments:
   - "Only 25% of resumes pass ATS" (8s)
   - "ATS Score: 78/100" (55s)
   - "15 Actionable Recommendations" (65s)
   - "Try FREE at resume2interview.com" (85s)
4. Adds intro/outro cards
5. Adds subtle fade transitions
6. Renders final video (1920x1080, 30fps, H.264)

**Output:** `output/resume2interview-demo-final.mp4` (90 seconds)

### Phase 4: YouTube Upload (2 minutes)

The script:
1. Authenticates with YouTube API (OAuth)
2. Uploads video with metadata from YOUTUBE_UPLOAD_INSTRUCTIONS.md
3. Generates thumbnail automatically:
   - Screenshots results page
   - Adds text: "AI Resume Analyzer"
   - Adds "FREE" badge
4. Sets video to Public
5. Returns video URL and ID

**Output:** Video ID (e.g., `dQw4w9WgXcQ`)

### Phase 5: Website Update (30 seconds)

The script:
1. Updates `frontend/src/pages/LandingPage.tsx`
2. Changes `<DemoVideo />` to `<DemoVideo videoId="dQw4w9WgXcQ" />`
3. Commits: "Add demo video to landing page"
4. Pushes to GitHub
5. Vercel auto-deploys (2-3 minutes)

**Output:** Live video on resume2interview.com

## Advanced Options

### Custom Voiceover (Better Quality)

Use ElevenLabs for natural-sounding AI voice:

```bash
# In .env file
VOICE_PROVIDER=elevenlabs
ELEVENLABS_API_KEY=your_key_here
ELEVENLABS_VOICE_ID=21m00Tcm4TlvDq8ikWAM
```

**Cost:** ~$0.30 per video (330 characters at $0.30/1000 chars)

### Custom Background Music

Place MP3 file in `output/background-music.mp3`

The script will:
- Auto-detect tempo
- Lower volume to -20dB (subtle background)
- Sync with voiceover

### Custom Branding

Edit `config.json`:

```json
{
  "brand_colors": {
    "primary": "#2563EB",
    "secondary": "#FFFFFF"
  },
  "text_overlays": {
    "font": "Arial Bold",
    "size": 48,
    "position": "bottom-center"
  },
  "logo": {
    "path": "../../frontend/public/logo.png",
    "position": "top-right",
    "size": 100
  }
}
```

## Troubleshooting

### Issue: "YouTube quota exceeded"

YouTube API has daily quota (10,000 units, each upload = 1,600 units).

**Solution:** Wait 24 hours or request quota increase from Google.

### Issue: "Playwright browser not found"

```bash
npx playwright install chromium
```

### Issue: "FFmpeg not found"

**Windows:**
```bash
choco install ffmpeg
```

**Or:**
Download from https://ffmpeg.org/download.html and add to PATH.

### Issue: "OAuth authentication failed"

1. Delete `token.pickle` file
2. Re-run script
3. Browser will open for authentication
4. Grant YouTube upload permissions

### Issue: "Video quality is low"

Increase recording resolution in `config.json`:

```json
{
  "recording": {
    "width": 2560,
    "height": 1440,
    "fps": 60,
    "bitrate": "8M"
  }
}
```

## Performance

**On typical laptop (i5, 8GB RAM):**
- Recording: 2-3 minutes
- Voiceover: 1 minute
- Compilation: 2-3 minutes
- Upload: 2 minutes
- **Total: 10-15 minutes**

**On high-end machine (i7+, 16GB+ RAM):**
- **Total: 5-8 minutes**

## Output Files

After running, check `output/` folder:

```
output/
├── screen-recording.mp4       # Raw screen capture
├── voiceover.mp3             # Generated audio
├── resume2interview-demo-final.mp4  # Final video
├── thumbnail.jpg             # Auto-generated thumbnail
└── youtube-upload-log.txt    # Upload details
```

## YouTube Video Details

**Automatically set:**
- Title: "Resume2Interview Tutorial - AI Resume Tailoring for ATS (2026)"
- Description: Optimized with timestamps, links, hashtags
- Tags: 25 SEO-optimized tags
- Category: Science & Technology
- Visibility: Public
- Comments: Enabled
- Thumbnail: Custom generated

## Next Steps After Video is Live

The script will output:

```
✅ Video uploaded successfully!
📺 YouTube URL: https://youtube.com/watch?v=dQw4w9WgXcQ
🆔 Video ID: dQw4w9WgXcQ
🌐 Website updated: https://resume2interview.com
📊 GA4 tracking: Enabled

Next steps:
1. Share on LinkedIn: [Ready-made post]
2. Submit to Product Hunt: [Use this video]
3. Post on Reddit: [Include video link]
```

## Cost Analysis

**Free Option (gTTS voiceover):**
- Total cost: $0
- Quality: Good
- Voice: Robotic but clear

**Premium Option (ElevenLabs):**
- Total cost: ~$0.30 per video
- Quality: Excellent
- Voice: Natural, human-like

**YouTube:**
- Free (quota: 6 uploads/day)

## Maintenance

### Updating the Video

To create a new version:

```bash
# Edit script in DEMO_VIDEO_GUIDE.md
# Then regenerate
node generate-video.js --force

# This will:
# 1. Delete old video from YouTube (optional)
# 2. Generate new video
# 3. Upload and update website
```

### A/B Testing

Create multiple versions:

```bash
node generate-video.js --version=intro-focused
node generate-video.js --version=results-focused
```

Compare performance in YouTube Analytics.

## Support

If the automated tool fails, fallback to manual approach in DEMO_VIDEO_GUIDE.md.

**Command failed?** Check logs in `output/error-log.txt`

---

**Ready to generate?** Run:

```bash
cd 01-Code/tools/video-generator
node generate-video.js
```

Sit back and let the automation handle everything! ☕
