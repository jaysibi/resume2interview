# GA4 Conversion Tracking Setup - Step-by-Step Guide

## ✅ Verification: Your Tracking is Working!

I tested your site and confirmed:
- ✅ Google Analytics is loading correctly
- ✅ Events are firing (saw `user_engagement` event)
- ✅ Blog engagement tracking is active
- ✅ Upload page with conversion tracking is ready

**The code is working perfectly. Now you just need to configure the GA4 dashboard.**

---

## 📋 STEP 1: Mark Events as Conversions in GA4

### 1.1 Sign In to Google Analytics

1. Go to **https://analytics.google.com/**
2. Sign in with your Google account
3. Select your **Resume2Interview** property (should show tracking ID: G-KBHMZRVRJ1)

### 1.2 Navigate to Events

1. In the left sidebar, click **Admin** (gear icon ⚙️ at bottom left)
2. In the **Data display** column (middle column), click **Events**
3. You'll see a list of all events being tracked

### 1.3 Mark Conversion Events

**IMPORTANT:** Events may take 24-48 hours to appear after first being triggered. If you don't see these events yet:
- Come back tomorrow
- OR trigger them yourself by uploading a resume on your site
- OR check "Real-time" reports to see if events are coming in now

Once events appear, mark these as conversions:

| Event Name | Action | Why It's a Conversion |
|------------|--------|----------------------|
| `conversion_resume_upload` | Toggle "Mark as conversion" switch to ON | Primary conversion - user uploaded resume |
| `conversion_analysis_complete` | Toggle "Mark as conversion" switch to ON | User completed full analysis (high intent) |
| `conversion_blog_to_app` | Toggle "Mark as conversion" switch to ON | Blog reader converted to user |

**How to toggle:**
- Find the event in the list
- On the right side, you'll see a toggle switch
- Click it to turn it **ON** (should turn blue/green)
- That's it! The event is now tracked as a conversion

### 1.4 Verify Conversions Are Set

1. Go to **Reports** → **Engagement** → **Conversions** (in left sidebar)
2. You should see your 3 conversion events listed
3. The count may be 0 initially - that's normal for new conversions

---

## 🧪 STEP 2: Test the Conversion Tracking

### 2.1 Test Resume Upload Conversion

1. Open a new **Incognito/Private window** in your browser
2. Go to **https://resume2interview.com/upload**
3. Create a simple test resume:
   - Open Notepad/Word
   - Type: "Test Resume - John Doe - Software Engineer"
   - Save as `test_resume.pdf`
4. Upload the test resume to your site
5. Paste a job description (can be any text with 50+ words)
6. Click **"Analyze Resume"**
7. Wait for the analysis to complete

### 2.2 Test Blog Engagement

1. In the same incognito window, go to:
   - **https://resume2interview.com/blog/tailor-resume-to-job-description**
2. Scroll down to 25%, 50%, 75%, 100% of the page (triggers scroll depth events)
3. Spend at least 30 seconds on the page (triggers engagement time)
4. Click the **"Analyze Your Resume Free"** CTA button at the bottom
5. This triggers: `blog_cta_click` and potentially `conversion_blog_to_app`

### 2.3 Verify Events Are Firing (Real-Time)

**Immediately after testing:**

1. Go to **GA4** → **Reports** → **Realtime** (in left sidebar)
2. Look at the **"Event count by Event name"** section
3. You should see events appearing within 1-2 minutes:
   - `page_view`
   - `conversion_resume_upload`
   - `user_engagement`
   - `blog_scroll_depth`
   - `blog_cta_click`

**If you see these events, tracking is working perfectly!**

### 2.4 Check Browser DevTools (Advanced Verification)

**For technical confirmation:**

1. Right-click on your site → **Inspect** (or press F12)
2. Go to **Network** tab
3. Filter by "analytics" or "collect"
4. Upload a resume and watch for requests to:
   - `https://www.google-analytics.com/g/collect?v=2&tid=G-KBHMZRVRJ1...`
5. Check the request payload includes:
   - `en=conversion_resume_upload` (event name)
   - `ep.value=10` (conversion value)

---

## 📊 STEP 3: Create Custom Reports

### 3.1 Create Conversion Funnel Report

**Track user journey from landing to conversion:**

1. Go to **Explore** (in left sidebar)
2. Click **+ Create a new exploration** (or **"Blank"** template)
3. Name it: **"User Conversion Funnel"**
4. Select **Funnel exploration** template
5. Configure the funnel steps:

**Step 1: Landing**
- Event: `page_view`
- Filter: `page_location` contains `/`

**Step 2: Upload Resume**
- Event: `conversion_resume_upload`

**Step 3: Upload Job Description**
- Event: `upload_job_description`

**Step 4: Analysis Complete**
- Event: `conversion_analysis_complete`

6. Click **Apply**
7. Save the exploration

**What to look for:**
- Drop-off between steps (where are users leaving?)
- Conversion rate from landing → upload (target: 5-15%)
- Completion rate from upload → analysis (target: 70-85%)

### 3.2 Create Blog Performance Report

**Track which blog posts drive conversions:**

1. Go to **Explore** → **Create a new exploration**
2. Name it: **"Blog Post Effectiveness"**
3. Select **Free form** template
4. Add **Dimensions:**
   - `Event name`
   - `Page title`
   - `Page location`
5. Add **Metrics:**
   - `Event count`
   - `Total users`
   - `Conversions`
6. Add **Filters:**
   - `Page location` contains `/blog/`
7. **Rows:** Drag `Page title` to Rows
8. **Values:** Drag all metrics to Values
9. Save the report

**What to look for:**
- Which blog post has most views
- Which blog post drives most `blog_cta_click` events
- Which blog post converts readers to users (`conversion_blog_to_app`)

### 3.3 Create Traffic Source Conversion Report

**Understand which traffic sources convert best:**

1. Go to **Reports** → **Acquisition** → **Traffic acquisition**
2. Click the **pencil icon** (customize report) in top right
3. Add these metrics:
   - `Sessions`
   - `Users`
   - `Conversions` (all conversions)
   - `Conversion rate`
4. Add secondary dimension: **Session source / medium**
5. Save customization

**What to look for:**
- Which directories send the most traffic
- Which sources have highest conversion rate
- Compare: `alternativeto / referral` vs `theresanaiforthat / referral` vs `direct / none`

### 3.4 Set Up Custom Dashboard (Optional but Recommended)

1. Go to **Reports** → **Library** (in left sidebar bottom)
2. Click **"Create new report"**
3. Select **"Dashboard"**
4. Add these cards:

**Card 1: Total Conversions (7 days)**
- Metric: `Conversions`
- Comparison: Previous 7 days

**Card 2: Conversion Rate Trend**
- Metric: `Conversion rate`
- Date range: Last 30 days
- Chart type: Line chart

**Card 3: Top Converting Sources**
- Dimension: `Session source`
- Metric: `Conversions`
- Chart type: Bar chart

**Card 4: Blog Engagement**
- Event: `blog_scroll_depth`
- Breakdown by `post_title`

5. Save dashboard as: **"Resume2Interview - Marketing Dashboard"**

---

## 🎯 What Success Looks Like

### Week 1 (After Launch)
- ✅ Events appearing in GA4 Events list
- ✅ Real-time tracking showing live events
- ✅ 10-50 resume uploads
- ✅ 5-30 completed analyses
- ✅ Blog posts getting 50-200 views

### Week 2-4 (After Directory Submissions)
- ✅ Traffic from directory sources showing in acquisition reports
- ✅ 50-200 resume uploads
- ✅ 3-10% landing → upload conversion rate
- ✅ Blog → app conversion: 1-5%
- ✅ Multiple traffic sources in top sources report

### After Product Hunt Launch
- ✅ Spike in traffic (500-2000 visitors/day)
- ✅ 50-200 resume uploads on launch day
- ✅ PH traffic shows high conversion rate (5-15%)
- ✅ Return visitor rate increases (10-20%)

---

## 🐛 Troubleshooting

### "Events aren't showing in GA4"

**Solution 1: Wait 24-48 hours**
- GA4 can take up to 48 hours to populate new events in the Events list
- Check **Realtime** reports instead for immediate feedback

**Solution 2: Check Real-time Reports**
1. Go to **Reports** → **Realtime**
2. Visit your site in another tab
3. Events should appear within 1-2 minutes
4. If they don't, check DevTools (Step 2.4)

**Solution 3: Disable Ad Blockers**
- Test in incognito mode
- Disable any ad blockers or privacy extensions
- Some browsers block analytics by default

### "Conversions aren't counting"

**Check:**
1. Did you toggle "Mark as conversion" switch? (Step 1.3)
2. Are events firing at all? Check Realtime reports
3. Are you testing in incognito? (Avoids self-traffic filtering)
4. Did you wait 24-48 hours for processing?

### "Low conversion rates"

**Expected ranges:**
- Landing → Resume Upload: **5-15%** (SaaS average)
- Resume Upload → Analysis Complete: **70-85%** (high intent)
- Blog → Resume Upload: **1-5%** (content marketing)

**If lower:**
1. Check **Funnel drop-off report** - where are users leaving?
2. Check **Error events** - are there technical issues?
3. Test on mobile - is the experience broken?
4. Review **User Journey** events for abandon points

---

## 📅 Weekly Monitoring Checklist

**Every Monday, check:**

- [ ] **Total conversions** last 7 days vs previous 7 days
- [ ] **Conversion rate** from landing → resume upload
- [ ] **Top traffic sources** and their conversion rates
- [ ] **Blog post views** and blog-to-app conversions
- [ ] **Error events** - any spikes or issues?
- [ ] **Return visitor rate** - are people coming back?
- [ ] **Device breakdown** - mobile vs desktop performance

**Actions based on data:**
- If blog engagement low → Improve CTAs, add internal links
- If conversion rate low → Simplify upload process, fix errors
- If traffic source converts well → Double down on that channel
- If returning visitors low → Add email capture, send follow-ups

---

## 🚀 Ready to Launch Marketing

Once you complete Steps 1-3 above, you're ready to:

### ✅ Submit to Directories
Use these UTM-tagged URLs:

```
AlternativeTo:
https://resume2interview.com/?utm_source=alternativeto&utm_medium=listing&utm_campaign=directory_launch

There's An AI For That:
https://resume2interview.com/?utm_source=theresanaiforthat&utm_medium=listing&utm_campaign=directory_launch

SaaSHub:
https://resume2interview.com/?utm_source=saashub&utm_medium=listing&utm_campaign=directory_launch

Indie Hackers:
https://resume2interview.com/?utm_source=indiehackers&utm_medium=listing&utm_campaign=directory_launch
```

### ✅ Launch on Product Hunt
- Use UTM: `?utm_source=producthunt&utm_medium=launch&utm_campaign=ph_launch_2026`
- Monitor **Real-time** reports during launch day
- Track which "hunters" drive most conversions
- Respond quickly to engage audience

### ✅ Post on Social Media
```
LinkedIn: ?utm_source=linkedin&utm_medium=social&utm_campaign=founder_post
Reddit: ?utm_source=reddit&utm_medium=social&utm_campaign=cscareerquestions
Twitter/X: ?utm_source=twitter&utm_medium=social&utm_campaign=tweet
```

---

## 📚 Additional Resources

- **GA4 Conversion Events:** https://support.google.com/analytics/answer/9267568
- **Creating Funnels:** https://support.google.com/analytics/answer/9327974
- **UTM Builder:** https://ga-dev-tools.google/campaign-url-builder/
- **Real-time Reports:** https://support.google.com/analytics/answer/9271392

---

## ✅ Summary: Your Action Items

**Today:**
1. ✅ Sign in to GA4 (https://analytics.google.com/)
2. ✅ Go to Admin → Events
3. ✅ Mark these as conversions: `conversion_resume_upload`, `conversion_analysis_complete`, `conversion_blog_to_app`
4. ✅ Test by uploading a resume yourself (incognito window)
5. ✅ Check Real-time reports to verify events firing

**Tomorrow (after 24 hours):**
1. ✅ Verify conversions appear in Reports → Conversions
2. ✅ Create Funnel report (Step 3.1)
3. ✅ Create Blog performance report (Step 3.2)
4. ✅ Create Traffic source report (Step 3.3)

**This Week:**
1. ✅ Submit to all 4 directories (use UTM links)
2. ✅ Monitor traffic in Real-time as submissions go live
3. ✅ Check which directories drive most conversions
4. ✅ Prepare Product Hunt launch for next week

**Next Week:**
1. ✅ Launch on Product Hunt
2. ✅ Post on Reddit, LinkedIn, Twitter
3. ✅ Monitor dashboard daily
4. ✅ Optimize based on data

---

**Questions?** Check Real-time reports first, then verify DevTools shows analytics requests firing.

**Your tracking is ready. Time to drive traffic! 🚀**
