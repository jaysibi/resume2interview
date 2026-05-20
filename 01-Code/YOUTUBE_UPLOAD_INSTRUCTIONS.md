# YouTube Video Upload Instructions

## After You Record and Edit Your Video

### Step 1: Upload to YouTube

1. Go to: https://studio.youtube.com/
2. Click **Create** → **Upload videos**
3. Select your video file

---

## Video Metadata to Copy-Paste

### **Title (Exactly 60 characters)**
```
Resume2Interview Tutorial - AI Resume Tailoring for ATS (2026)
```

### **Description (Copy This Entire Block)**
```
🚀 Stop getting rejected by Applicant Tracking Systems! Resume2Interview is a FREE AI-powered tool that analyzes your resume against any job description in seconds.

✅ Get your ATS compatibility score (0-100)
✅ See exactly which keywords you're missing
✅ Receive specific recommendations to improve your match
✅ 100% Free - No credit card required

🔗 Try it FREE: https://resume2interview.com/?utm_source=youtube&utm_medium=video&utm_campaign=demo_tutorial

📋 Video Chapters:
00:00 - The Problem: Why resumes get rejected
00:15 - The Solution: AI-powered analysis in seconds
00:22 - Step 1: Upload your resume
00:35 - Step 2: Paste job description
00:48 - Step 3: View analysis & recommendations
01:10 - Call to action: Try it free

🎯 Perfect for:
→ Job seekers applying to multiple positions
→ Recent graduates entering the job market
→ Career changers updating their resumes
→ Anyone struggling to get interview calls

💡 Features shown in this video:
• ATS Score Calculator (0-100)
• Missing Skills Analyzer
• Keyword Gap Analysis
• Personalized Recommendations
• Match Percentage Scoring

📧 Questions? Visit: https://resume2interview.com/faq

--- 

#Resume #JobSearch #ATS #CareerAdvice #InterviewTips #ResumeOptimization #JobApplications #CareerGrowth #ApplicantTrackingSystem #ResumeTips #JobHunting #CareerDevelopment #GetHired #JobSearchTips #ATSResume
```

### **Tags (Copy All These)**
```
resume, ATS, job search, resume optimization, career, interview, AI tool, resume tailoring, job description, career advice, applicant tracking system, resume tips, job hunting, get hired, interview tips, career growth, resume analyzer, ATS checker, job application, professional resume, resume writing, career development, job seeker, employment, recruitment
```

### **Thumbnail Text Ideas**

Create thumbnail in Canva (1280x720px) with this text:

**Option 1:**
```
AI Resume Analyzer
Beat ATS in 60 Seconds
FREE
```

**Option 2:**
```
Get More Interviews
AI Resume Optimization
100% FREE
```

**Option 3:**
```
ATS Score: 85/100
Resume Tailoring Made Easy
TRY FREE
```

**Thumbnail Design Tips:**
- Use blue and white color scheme (brand colors)
- Include screenshot of ATS score
- Add your face or avatar (increases CTR by 30%)
- Use bold, easy-to-read fonts
- Add "FREE" badge in corner

---

### **Other Settings**

**Category:** Science & Technology (or Education)

**Audience:** No, it's not made for kids

**Comments:** Allow all comments

**Playlists:** Create playlist "Resume2Interview Tutorials"

**End Screen:** 
- Add subscribe button
- Add link to your website: https://resume2interview.com/

**Cards:**
- Add at 0:30: Link to resume2interview.com
- Add at 1:00: "Try it FREE" link

---

## Step 2: Get Your Video ID

After uploading:

1. Go to your YouTube Studio
2. Click on the video
3. Look at the URL: `https://studio.youtube.com/video/ABC123xyz/edit`
4. Copy the part after `/video/` - that's your video ID: **ABC123xyz**

---

## Step 3: Add Video ID to Your Website

### **Option A: Quick Update (No Code)**

1. Open file: `frontend/src/pages/LandingPage.tsx`
2. Find line with: `<DemoVideo />`
3. Change it to: `<DemoVideo videoId="YOUR_VIDEO_ID_HERE" />`
4. Replace `YOUR_VIDEO_ID_HERE` with your actual video ID

Example:
```tsx
{/* DEMO VIDEO SECTION */}
<DemoVideo videoId="dQw4w9WgXcQ" />
```

### **Option B: I'll Do It For You**

Send me your YouTube video ID and I'll update the code automatically.

---

## Step 4: Test the Video

1. After updating the code, commit and push:
   ```bash
   git add .
   git commit -m "Add demo video to landing page"
   git push origin main
   ```

2. Wait 2-3 minutes for Vercel deployment

3. Visit: https://resume2interview.com/

4. Video should appear after the "Problem" section

---

## Video Performance Tracking

Your video will automatically track:
- ✅ Play events in Google Analytics
- ✅ CTA clicks below video
- ✅ Where viewers came from (traffic sources)

Check GA4 → Events to see `video_play` events

---

## Optimization Tips After Launch

### Week 1:
- Check YouTube Analytics for:
  - Average view duration (target: 60%+)
  - Click-through rate on CTAs (target: 5%+)
  - Traffic sources (where viewers found it)

### If Performance is Low:

**Low views (<100 in first week)?**
- Share on LinkedIn, Twitter, Reddit
- Add to all directory submissions
- Pin to top of social media profiles

**Low watch time (<50%)?**
- Speed up the demo (show results faster)
- Add more dynamic cuts
- Improve voiceover energy

**Low CTR (<3%)?**
- Stronger CTA at end
- Add annotations pointing to site
- Create better thumbnail

---

## Once Video is Live - Marketing Uses

Use your video in:
- ✅ Landing page (done automatically)
- ✅ Product Hunt launch
- ✅ LinkedIn posts
- ✅ Reddit submissions
- ✅ Startup directory submissions
- ✅ Email signature
- ✅ Social media profiles
- ✅ Future paid ads (if you run them)

---

## Need Help?

If you have issues uploading or embedding, just send me:
1. Your YouTube video URL
2. Any error messages you see

I'll help you troubleshoot!

---

**Ready to record? Follow the script in DEMO_VIDEO_GUIDE.md and use the sample data in DEMO_VIDEO_SAMPLES.md. You've got this! 🎬**
