# 🎬 Video Generator Tool - Complete Setup

## ✅ What Was Created

Your **fully automated video generator** is now complete! Here are all the files:

### Core Files (9 total)

1. **`setup.js`** - One-click dependency installer
   - Installs Node.js packages
   - Installs Playwright browser
   - Installs Python packages
   - Creates configuration files
   - Sets up output directory

2. **`generate-video.js`** - Main orchestrator (270 lines)
   - Coordinates all 7 steps
   - Handles errors and logging
   - Provides progress updates
   - Tracks execution time

3. **`record-demo.js`** - Browser automation (330 lines)
   - Opens your site automatically
   - Uploads sample resume
   - Pastes job description
   - Records 90-second screen capture
   - Saves as 1920x1080 video

4. **`generate-voiceover.py`** - Text-to-speech (180 lines)
   - Reads DEMO_VIDEO_GUIDE.md script
   - Creates voiceover with gTTS (free) or ElevenLabs (premium)
   - Outputs clear MP3 audio
   - Estimates duration

5. **`compile-video.py`** - Video editor (280 lines)
   - Combines screen recording + voiceover
   - Adds text overlays ("ATS Score: 78/100", "100% FREE")
   - Adds fade in/out transitions
   - Syncs audio/video timing
   - Generates YouTube thumbnail
   - Exports final 1080p MP4

6. **`upload-to-youtube.py`** - YouTube uploader (240 lines)
   - Handles OAuth authentication (one-time)
   - Uploads video with optimized metadata
   - Sets title, description, tags automatically
   - Uploads custom thumbnail
   - Returns video ID and URL

7. **`package.json`** - Node.js dependencies
   - playwright
   - @playwright/test
   - dotenv
   - fs-extra

8. **`requirements.txt`** - Python dependencies
   - moviepy (video editing)
   - gTTS (text-to-speech)
   - google-api-python-client (YouTube API)
   - Pillow (thumbnail generation)
   - requests (ElevenLabs API)
   - pydub (audio processing)

9. **`README.md`** - Complete documentation (300+ lines)
   - Installation instructions
   - Usage guide
   - Troubleshooting
   - Cost breakdown
   - Advanced options

### Supporting Files

10. **`QUICKSTART.md`** - Simplified 3-step guide
11. **`.env.example`** - Environment variables template (created by setup.js)
12. **`config.json.example`** - Configuration template (created by setup.js)

---

## 🚀 How To Use (Quick Version)

### Step 1: Install FFmpeg (if not already installed)

**Windows (PowerShell as Administrator):**
```powershell
choco install ffmpeg
```

If you don't have Chocolatey, download from: https://ffmpeg.org/download.html

**Verify installation:**
```bash
ffmpeg -version
```

### Step 2: Run Setup (One Time)

```bash
cd C:\Projects\ResumeTailor\01-Code\tools\video-generator
node setup.js
```

This will:
- Install all Node.js packages (~2 min)
- Download Playwright browser (~1 min)
- Install all Python packages (~2 min)
- Create `.env` and `config.json` files
- Create `output/` directory

**Total time: ~5 minutes**

### Step 3: Get YouTube Credentials (One Time)

1. Go to https://console.cloud.google.com/
2. Create project: "Resume2Interview"
3. Enable API: "YouTube Data API v3"
4. Create OAuth credentials (Desktop app)
5. Download JSON file
6. Rename to `youtube_credentials.json`
7. Place in `C:\Projects\ResumeTailor\01-Code\tools\video-generator\`

**Total time: ~5 minutes**

### Step 4: Generate Video (Fully Automated)

```bash
node generate-video.js
```

**Go make coffee ☕ for 10-15 minutes while it runs!**

The script will:
1. ✅ Check all prerequisites
2. ✅ Open browser and record demo (90 seconds)
3. ✅ Generate AI voiceover
4. ✅ Compile video with overlays
5. ✅ Upload to YouTube with metadata
6. ✅ Update your website code
7. ✅ Commit and push to GitHub

**When done, you'll see:**
```
🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉
VIDEO GENERATION COMPLETE!
🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉

📊 Results:
   YouTube URL: https://youtube.com/watch?v=abc123xyz
   Video ID: abc123xyz
   Website: https://resume2interview.com

✨ Video is live and embedded on your landing page!
```

---

## 🎯 What You Get

### Outputs in `output/` folder:

1. **`screen-recording.webm`** - Raw browser recording
2. **`voiceover.mp3`** - AI-generated narration
3. **`resume2interview-demo-final.mp4`** - Final edited video
4. **`thumbnail.jpg`** - Auto-generated YouTube thumbnail
5. **`video-id.txt`** - YouTube video ID
6. **`youtube-upload-log.txt`** - Upload details

### Live Results:

- ✅ **YouTube video** published (public)
- ✅ **Landing page** updated with video embed
- ✅ **GA4 tracking** active for video plays
- ✅ **Code committed** and pushed to GitHub
- ✅ **Vercel deployment** triggered (live in 2-3 min)

---

## 💰 Cost Breakdown

### Free Option (Recommended for First Try):
- FFmpeg: FREE
- Node.js: FREE
- Python: FREE
- Playwright: FREE
- gTTS voiceover: FREE (robotic but clear)
- YouTube API: FREE (10,000 quota/day = 6 videos/day)
- **Total: $0** 💚

### Premium Option (Better Quality):
- Everything above: FREE
- ElevenLabs voiceover: $0.30/video (natural human-like voice)
- **Total: $0.30/video** 🌟

To use premium voice:
1. Get API key: https://elevenlabs.io/
2. Edit `.env`:
   ```
   VOICE_PROVIDER=elevenlabs
   ELEVENLABS_API_KEY=your_key_here
   ```

---

## ⚡ Execution Flow

When you run `node generate-video.js`, here's what happens:

```
┌─────────────────────────────────────────────────────┐
│ STEP 0: Check Prerequisites                        │
│ • Verify Node.js, Python, FFmpeg installed          │
│ • Check for required config files                   │
│ • Validate output directory                         │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ STEP 1: Setup Output Directory                     │
│ • Create/clean output folder                        │
│ • Prepare for new video generation                  │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ STEP 2: Record Screen Demo (90 seconds)            │
│ • Launch Playwright browser                         │
│ • Navigate to resume2interview.com                  │
│ • Upload sample resume                              │
│ • Paste job description                             │
│ • Click analyze button                              │
│ • Show results with scrolling                       │
│ • Save recording: screen-recording.webm             │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ STEP 3: Generate Voiceover (30 seconds)            │
│ • Read script from DEMO_VIDEO_GUIDE.md              │
│ • Convert to speech (gTTS or ElevenLabs)            │
│ • Save audio: voiceover.mp3                         │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ STEP 4: Compile Video (8-10 min)                   │
│ • Load screen recording                             │
│ • Load voiceover audio                              │
│ • Sync audio/video timing                           │
│ • Add text overlays:                                │
│   - "ATS Score: 78/100" at 30s                      │
│   - "15+ Missing Keywords" at 45s                   │
│   - "100% FREE" at 75s                              │
│   - "resume2interview.com" at 85s                   │
│ • Add fade in/out effects                           │
│ • Export: resume2interview-demo-final.mp4           │
│ • Generate thumbnail.jpg                            │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ STEP 5: Upload to YouTube (5 min)                  │
│ • Authenticate (OAuth - first time only)            │
│ • Upload video with metadata:                       │
│   - Title (60 chars, SEO-optimized)                 │
│   - Description (timestamps, hashtags)              │
│   - 25 tags                                         │
│   - Category: Education                             │
│   - Privacy: Public                                 │
│ • Upload custom thumbnail                           │
│ • Save video ID                                     │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ STEP 6: Update Website (1 min)                     │
│ • Update LandingPage.tsx with video ID              │
│ • Git add, commit, push to GitHub                   │
│ • Trigger Vercel deployment                         │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ STEP 7: Print Summary                              │
│ • Show YouTube URL                                  │
│ • Show video ID                                     │
│ • Show website URL                                  │
│ • Provide next steps                                │
└─────────────────────────────────────────────────────┘

Total Time: 15-20 minutes
Human Intervention: 0 minutes (after initial setup)
```

---

## 🔍 What's Automated

### ZERO manual work required:

- ✅ Browser navigation and interaction
- ✅ Form filling (resume upload, JD paste)
- ✅ Screen recording at 1080p
- ✅ Voiceover generation from script
- ✅ Video editing and effects
- ✅ Text overlay timing and positioning
- ✅ Thumbnail design and generation
- ✅ YouTube metadata optimization
- ✅ Video upload with authentication
- ✅ Website code update
- ✅ Git commit and push
- ✅ Analytics tracking setup

### One-time manual setup (10 minutes total):

- Install FFmpeg (5 min)
- Get YouTube API credentials (5 min)

That's it! After setup, it's **100% hands-off**. 🙌

---

## 🐛 Troubleshooting

### "FFmpeg not found"

**Windows:**
```powershell
choco install ffmpeg
# OR download from https://ffmpeg.org/download.html and add to PATH
```

**Verify:**
```bash
ffmpeg -version
```

### "Playwright browser not installed"

```bash
npx playwright install chromium
```

### "Python package not found"

```bash
pip install -r requirements.txt
```

### "YouTube quota exceeded"

YouTube API has daily quota limits:
- Default: 10,000 points/day
- 1 video upload = 1,600 points
- **You can upload 6 videos/day**

If exceeded, wait 24 hours or request quota increase from Google.

### "OAuth authentication failed"

1. Delete `token.pickle` file
2. Re-run `node generate-video.js`
3. Browser will open for re-authentication
4. Click "Allow" to authorize

### "Video compilation taking too long"

This is normal! Video rendering is CPU-intensive:
- Expected time: 8-12 minutes for 90-second video
- Uses FFmpeg and MoviePy
- Progress shown in terminal

**Tip:** Close other applications to speed up encoding.

### "Website not updating"

1. Check git push succeeded (look for "✅ Changes deployed")
2. Wait 2-3 minutes for Vercel deployment
3. Check build logs: https://vercel.com/your-project/deployments
4. Hard refresh browser: Ctrl+Shift+R

---

## 🎨 Customization

### Change Video Resolution

Edit `config.json`:
```json
{
  "recording": {
    "width": 1920,
    "height": 1080,
    "fps": 30
  }
}
```

Options: 720p, 1080p, 1440p, 2160p

### Change Text Overlays

Edit `compile-video.py`, find the overlays section:
```python
# Overlay 1: "ATS Score: 78/100" (appears at ~30 seconds)
ats_text = TextClip(
    "YOUR TEXT HERE",
    fontsize=60,
    color='white'
).set_start(30).set_duration(5)
```

### Change Brand Colors

Edit `config.json`:
```json
{
  "brand": {
    "primaryColor": "#2563EB",
    "secondaryColor": "#22C55E"
  }
}
```

### Use Different Sample Data

Edit `record-demo.js`, find `SAMPLE_RESUME` and `SAMPLE_JD` constants at the top.

### Change Voiceover Script

Edit `/DEMO_VIDEO_GUIDE.md` - the script is automatically read from there.

---

## 📊 Expected Results

### Video Specs:
- **Duration:** ~90 seconds
- **Resolution:** 1920x1080 (Full HD)
- **Frame Rate:** 30fps
- **Audio:** Clear voiceover (gTTS or ElevenLabs)
- **File Size:** ~50-80 MB
- **Format:** MP4 (H.264 video, AAC audio)

### YouTube Optimization:
- **Title:** 60 characters (SEO-optimized)
- **Description:** 800+ characters with timestamps
- **Tags:** 25 relevant tags
- **Thumbnail:** Custom 1280x720 image
- **Category:** Education
- **Privacy:** Public

### Website Integration:
- **Embed:** YouTube iframe on landing page
- **Tracking:** GA4 video_play event
- **CTA:** "Try FREE" button below video
- **Stats:** "60 sec analysis" badge

---

## 📈 Next Steps After Video is Live

1. ✅ **Verify video on YouTube** - Check quality, thumbnail, description
2. ✅ **Check website embed** - Visit https://resume2interview.com
3. ✅ **Test GA4 tracking** - Play video, check Real-time reports
4. ✅ **Share on social media:**
   - LinkedIn (ready-to-post text in output)
   - Twitter/X
   - Reddit (r/cscareerquestions, r/resumes)
   - Indie Hackers
5. ✅ **Update directory submissions** - Add video link to listings
6. ✅ **Prepare Product Hunt launch** - Video is #1 requirement ✅

---

## 🎉 Success Metrics

After running the tool, you should have:

- ✅ Professional 90-second demo video
- ✅ Published on YouTube (public)
- ✅ Embedded on landing page
- ✅ GA4 tracking active
- ✅ SEO-optimized metadata
- ✅ Custom thumbnail
- ✅ Shareable on social media
- ✅ Ready for directory submissions
- ✅ Product Hunt launch-ready

**Total cost:** $0 (or $0.30 for premium voice)  
**Total time:** 15-20 minutes (automated)  
**Human effort:** 10 minutes (one-time setup only)

---

## 💡 Pro Tips

1. **Run overnight:** Script is fully automated - start before bed, wake up to published video
2. **Test with private first:** Change `PRIVACY_STATUS = "private"` in `upload-to-youtube.py` for testing
3. **Re-generate anytime:** Edit script, re-run `node generate-video.js` to create updated version
4. **Manual fallback:** All files saved in `output/` - can upload manually if automation fails
5. **Monitor quota:** Check YouTube API quota: https://console.cloud.google.com/apis/dashboard
6. **Premium voice worth it:** $0.30 for natural-sounding voice significantly improves video quality

---

## 📁 File Structure

```
tools/video-generator/
├── generate-video.js           ← Main script (run this!)
├── setup.js                    ← One-time setup
├── record-demo.js              ← Browser automation
├── generate-voiceover.py       ← Text-to-speech
├── compile-video.py            ← Video editing
├── upload-to-youtube.py        ← YouTube upload
├── package.json                ← Node dependencies
├── requirements.txt            ← Python dependencies
├── README.md                   ← Full documentation
├── QUICKSTART.md               ← This file
├── COMPLETE_SETUP.md           ← Detailed guide
├── .env                        ← Config (created by setup)
├── config.json                 ← Settings (created by setup)
├── youtube_credentials.json    ← YouTube OAuth (you provide)
├── token.pickle                ← Saved auth (auto-created)
└── output/                     ← Generated files
    ├── screen-recording.webm
    ├── voiceover.mp3
    ├── resume2interview-demo-final.mp4
    ├── thumbnail.jpg
    ├── video-id.txt
    └── youtube-upload-log.txt
```

---

## ✅ Pre-Flight Checklist

Before running `node generate-video.js`:

- [ ] FFmpeg installed (`ffmpeg -version` works)
- [ ] Run `node setup.js` successfully
- [ ] `youtube_credentials.json` file present
- [ ] `.env` file exists with `SITE_URL=https://resume2interview.com`
- [ ] Internet connection active
- [ ] YouTube account ready
- [ ] ~15 GB free disk space (for video processing)
- [ ] Close CPU-intensive apps (to speed up encoding)

If all checked, you're ready! Run:

```bash
node generate-video.js
```

---

## 🆘 Need Help?

1. **Check `output/error-log.txt`** - Detailed error info
2. **Read `README.md`** - Full troubleshooting guide
3. **Test individual scripts:**
   ```bash
   node record-demo.js
   python generate-voiceover.py
   python compile-video.py
   python upload-to-youtube.py
   ```
4. **Manual fallback:** Upload `output/resume2interview-demo-final.mp4` to YouTube manually

---

**Ready? Let's generate your video!** 🚀

```bash
cd C:\Projects\ResumeTailor\01-Code\tools\video-generator
node generate-video.js
```

Go make coffee ☕ and come back in 15 minutes to a published video!
