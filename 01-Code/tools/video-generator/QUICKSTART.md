# 🎬 Quick Start: Automated Video Generation

Generate your demo video with **ZERO manual work** in 3 commands!

## Prerequisites

You need installed (probably already have):
- ✅ Node.js (v18+)
- ✅ Python (v3.8+)
- ❌ FFmpeg - **Only missing requirement for most users**

### Install FFmpeg (Windows)

**Option 1: Chocolatey (Easiest)**
```bash
choco install ffmpeg
```

**Option 2: Manual Install**
1. Download: https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip
2. Extract to `C:\ffmpeg`
3. Add to PATH: `C:\ffmpeg\bin`
4. Restart terminal

---

## Step 1: Setup (One Time Only)

```bash
cd C:\Projects\ResumeTailor\01-Code\tools\video-generator
node setup.js
```

**Time:** 2-3 minutes  
**What it does:** Installs all dependencies automatically

---

## Step 2: Get YouTube Credentials (One Time Only)

### Quick Version:
1. Go to: https://console.cloud.google.com/
2. **Create Project:** "Resume2Interview"
3. **Enable API:** Search "YouTube Data API v3" → Enable
4. **Create Credentials:**
   - Click "Create Credentials" → "OAuth 2.0 Client ID"
   - Application type: "Desktop app"
   - Name: "Video Generator"
5. **Download:** Click download icon (⬇️) → Save as `youtube_credentials.json`
6. **Move file:** Place in `C:\Projects\ResumeTailor\01-Code\tools\video-generator\`

**Time:** 5 minutes  
**Cost:** FREE (10,000 quota/day = 6 video uploads/day)

### Need Help?
See detailed guide: https://developers.google.com/youtube/v3/quickstart/python

---

## Step 3: Generate Video (Fully Automated)

```bash
cd C:\Projects\ResumeTailor\01-Code\tools\video-generator
node generate-video.js
```

**Time:** 10-15 minutes  
**What happens:**
1. ✅ Opens your site in browser (automated)
2. ✅ Records demo (uploads resume, shows analysis)
3. ✅ Generates AI voiceover (text-to-speech)
4. ✅ Edits video (adds overlays, transitions)
5. ✅ Uploads to YouTube (auto-fills metadata)
6. ✅ Updates your website (auto-commits code)

**That's it!** Go make coffee ☕ and come back to a published video.

---

## What You'll Get

### Outputs:
- ✅ **YouTube Video:** 90 seconds, 1080p, optimized metadata
- ✅ **Auto-Generated Thumbnail:** Professional design
- ✅ **Website Updated:** Video embedded on landing page
- ✅ **GA4 Tracking:** Automatic video play tracking

### Video Quality:
- Resolution: 1920x1080 (Full HD)
- Frame rate: 30fps  
- Audio: Clear AI voiceover
- Text overlays: Professional
- Length: ~90 seconds

---

## First Run: OAuth Authentication

During **first upload** only, browser will open:

1. Google asks: "Resume2Interview wants to access your YouTube"
2. Click **"Allow"**
3. Done! Credentials saved for future runs

**Never asks again** unless you delete `token.pickle`

---

## Monitoring Progress

Watch the terminal output:

```
🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬
AUTOMATED DEMO VIDEO GENERATOR
🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬

============================================================
STEP 2: Recording Screen Demo
============================================================
Starting Playwright browser automation...
✅ Screen recording complete!

============================================================
STEP 3: Generating AI Voiceover
============================================================
Converting script to speech...
✅ Voiceover generated!

... (continues for all steps)

🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉
VIDEO GENERATION COMPLETE!
🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉

📊 Results:
   YouTube URL: https://youtube.com/watch?v=YOUR_VIDEO_ID
   Website: https://resume2interview.com

✨ Done! Video is live and tracking in GA4.
```

---

## Troubleshooting

### "FFmpeg not found"
**Solution:**
```bash
# Check if installed
ffmpeg -version

# If not found, install:
choco install ffmpeg
# OR download from https://ffmpeg.org/download.html
```

### "YouTube quota exceeded"
**What:** YouTube allows 10,000 quota points/day (1 upload = 1,600 points = 6 uploads/day max)  
**Solution:** Wait 24 hours or request quota increase from Google

### "Playwright browser failed"
**Solution:**
```bash
npx playwright install chromium
```

### "Python package not found"
**Solution:**
```bash
pip install -r requirements.txt
```

### "OAuth authentication failed"
1. Delete `token.pickle` file
2. Re-run `node generate-video.js`
3. Browser will re-open for authentication

---

## Advanced Options

### Premium Voice (Optional)

For natural-sounding voiceover (way better than free):

1. Get ElevenLabs API key: https://elevenlabs.io/
2. Edit `.env`:
   ```
   VOICE_PROVIDER=elevenlabs
   ELEVENLABS_API_KEY=your_key_here
   ```
3. **Cost:** ~$0.30 per video (worth it!)

### Custom Configuration

Edit `config.json` to customize:
- Video resolution (720p, 1080p, 1440p)
- Frame rate (30fps, 60fps)
- Text overlay styles
- Brand colors
- Logo overlay

---

## Cost Breakdown

### Free Option:
- Node.js: FREE
- Python: FREE
- FFmpeg: FREE
- Playwright: FREE
- gTTS voiceover: FREE
- YouTube API: FREE (quota limits)
- **Total: $0** 💚

### Premium Option:
- Everything above: FREE
- ElevenLabs voiceover: ~$0.30/video
- **Total: $0.30/video** 🌟

---

## What Happens After Generation?

1. **Video goes live immediately** on YouTube (Public)
2. **Website auto-updates** in 2-3 minutes (Vercel deployment)
3. **GA4 starts tracking** video plays automatically
4. **You can share** on social media instantly

### Recommended Next Steps:
1. ✅ Share on LinkedIn (ready-to-post text in output)
2. ✅ Add to Product Hunt submission
3. ✅ Post in r/cscareerquestions, r/resumes (with video link)
4. ✅ Pin to social media profiles

---

## Re-Generating Video

To create updated version (e.g., after script changes):

```bash
# Edit script in: ../../DEMO_VIDEO_GUIDE.md
# Then regenerate:
node generate-video.js
```

Deletes old video (optional) and uploads new one.

---

## Files Created

After running, check `output/` folder:

```
output/
├── screen-recording.mp4          # Raw screen capture
├── voiceover.mp3                 # AI-generated audio
├── resume2interview-demo-final.mp4  # Final video (upload this manually if auto-upload fails)
├── thumbnail.jpg                 # Auto-generated thumbnail
├── video-id.txt                  # YouTube video ID
└── youtube-upload-log.txt        # Upload details
```

---

## Support

**Something not working?**
1. Check `output/error-log.txt` for details
2. Try manual fallback: See `../DEMO_VIDEO_GUIDE.md`
3. Each script can run individually if needed

**Still stuck?** The tool generates all necessary files in `output/`. You can:
- Upload `resume2interview-demo-final.mp4` to YouTube manually
- Use the generated thumbnail
- Copy video ID to website manually

---

## Summary

### Total Setup Time: ~10 minutes
- Install FFmpeg: 2 min
- Run setup.js: 3 min
- Get YouTube credentials: 5 min

### Total Generation Time: ~15 minutes
- Automated, zero intervention required
- Can run while you do other tasks

### Total Cost: $0 (or $0.30 for premium voice)

---

**Ready?** Just run:

```bash
cd C:\Projects\ResumeTailor\01-Code\tools\video-generator
node setup.js
# Get YouTube credentials (5 min)
node generate-video.js
```

That's it! 🚀

---

**Pro Tip:** Run overnight if you want. The script handles everything and finishes with a complete summary. Wake up to a published video! 😴→📹
