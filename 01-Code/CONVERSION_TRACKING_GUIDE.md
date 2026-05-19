# Google Analytics 4 Conversion Tracking Setup

## Overview

This document explains how to configure conversion tracking in Google Analytics 4 for Resume2Interview. All the necessary event tracking code has been implemented in the application. You just need to mark specific events as "conversions" in the GA4 dashboard.

## 🎯 Key Conversion Events

We've implemented the following conversion events with assigned values:

### Primary Conversions

| Event Name | Description | Value | When Triggered |
|------------|-------------|-------|----------------|
| `conversion_resume_upload` | User uploads their first resume | 10 | First resume uploaded via UploadPage |
| `conversion_analysis_complete` | User completes gap analysis or ATS score | 20 | Analysis results displayed |
| `conversion_blog_to_app` | User came from blog and uploaded resume | 12 | Blog visitor converts to user |

### Secondary Conversions

| Event Name | Description | Value | When Triggered |
| `conversion_signup` | User creates an account (if implemented) | 15 | Account created |

## 🔧 How to Configure Conversions in GA4

### Step 1: Access GA4 Property

1. Go to [Google Analytics](https://analytics.google.com/)
2. Select your **Resume2Interview** property (G-KBHMZRVRJ1)
3. Click **Admin** (gear icon in bottom left)

### Step 2: Mark Events as Conversions

1. In the **Admin** section, under **Data display**, click **Events**
2. Wait for the event list to load (you may need to wait 24-48 hours after deployment for events to appear)
3. Find each conversion event in the list:
   - `conversion_resume_upload`
   - `conversion_analysis_complete`
   - `conversion_blog_to_app`
   - `conversion_signup` (once user signup is implemented)
4. Toggle the **"Mark as conversion"** switch to **ON** for each event

**Important:** Events won't appear in the list until they've been triggered at least once. You may need to test the site yourself to generate initial events.

### Step 3: Verify Conversion Tracking

1. Go to **Reports** → **Engagement** → **Conversions**
2. You should see your marked conversion events appearing
3. Check that conversion counts match your expectations

## 📊 Additional Engagement Events

Beyond conversions, we track these engagement metrics:

### Blog Engagement
- `blog_scroll_depth` - How far users scroll through blog posts (25%, 50%, 75%, 100%)
- `blog_reading_time` - Time spent reading blog content
- `blog_cta_click` - Clicks on "Try It Now" CTAs from blog posts
- `blog_share` - Social media shares of blog posts

### User Journey
- `user_journey_step` - Tracks user progression through the funnel
- `funnel_drop_off` - Identifies where users abandon the process
- `return_visitor` - Tracks returning users

### Feature Usage
- `upload_resume` - Resume file uploads (all uploads, not just conversions)
- `upload_job_description` - JD uploads
- `gap_analysis_request` / `gap_analysis_complete` - Analysis flow
- `ats_score_request` / `ats_score_complete` - ATS scoring flow

### Errors & Issues
- `error_occurred` - Application errors for debugging
- `rate_limit_hit` - When users hit rate limits

## 📈 Custom Reports to Create

### 1. Conversion Funnel Report

Track user journey from landing to conversion:

1. Go to **Explore** → **Create a new exploration**
2. Select **Funnel exploration**
3. Configure steps:
   - Step 1: `page_view` (landing page)
   - Step 2: `upload_resume`
   - Step 3: `upload_job_description`
   - Step 4: `conversion_analysis_complete`
4. Save as "User Conversion Funnel"

### 2. Blog Performance Report

Track which blog posts drive conversions:

1. Go to **Explore** → **Create a new exploration**
2. Select **Free form**
3. Add dimensions: `post_title`, `page_path`
4. Add metrics: 
   - `blog_cta_click` (event count)
   - `conversion_blog_to_app` (conversions)
   - Average `blog_reading_time`
   - `blog_scroll_depth` (100% completions)
5. Save as "Blog Post Effectiveness"

### 3. Traffic Source Conversion Report

Understand which traffic sources convert best:

1. Go to **Reports** → **Acquisition** → **Traffic acquisition**
2. Add secondary dimension: **Session source/medium**
3. Add custom metrics for conversion events
4. Compare conversion rates across sources (organic, direct, social, referral)

## 🎨 Custom Dimensions to Configure (Optional)

For more detailed tracking, configure these custom dimensions:

1. Go to **Admin** → **Custom definitions** → **Create custom dimension**

| Dimension Name | Event Parameter | Scope |
|----------------|-----------------|-------|
| Analysis Type | `analysis_type` | Event |
| Blog Post Title | `post_title` | Event |
| Traffic Source | `traffic_source` | Event |
| Match Score | `match_score` | Event |
| ATS Score | `ats_score` | Event |

## 🚀 Goals & Targets

### Short-term Goals (First Month)
- **50+ Resume Uploads** (`conversion_resume_upload`)
- **30+ Completed Analyses** (`conversion_analysis_complete`)
- **10% Blog-to-App Conversion** (blog visitors who upload resume)

### Medium-term Goals (First Quarter)
- **500+ Resume Uploads**
- **300+ Completed Analyses**
- **60% Analysis Completion Rate** (users who upload both resume + JD)
- **15% Return Visitor Rate**

### Acquisition Goals
- **Track which directories drive traffic** - Use UTM parameters when submitting to directories
- **Measure Product Hunt launch impact** - Compare traffic/conversions before/during/after launch
- **Monitor organic search growth** - Track blog posts ranking and driving traffic

## 🔗 UTM Parameter Strategy

When submitting to directories or sharing links, use UTM parameters:

### Directory Submissions
```
https://resume2interview.com/?utm_source=alternativeto&utm_medium=listing&utm_campaign=directory_launch
https://resume2interview.com/?utm_source=theresanaiforthat&utm_medium=listing&utm_campaign=directory_launch
https://resume2interview.com/?utm_source=saashub&utm_medium=listing&utm_campaign=directory_launch
```

### Product Hunt Launch
```
https://resume2interview.com/?utm_source=producthunt&utm_medium=launch&utm_campaign=ph_launch_2026
```

### Social Media Posts
```
https://resume2interview.com/?utm_source=linkedin&utm_medium=social&utm_campaign=founder_post
https://resume2interview.com/?utm_source=reddit&utm_medium=social&utm_campaign=cscareerquestions
```

### Blog Posts (for tracking which posts drive conversions)
The blog post URL slug is automatically tracked in `post_title` parameter, but you can also use:
```
https://resume2interview.com/upload?utm_source=blog&utm_medium=cta&utm_campaign=tailor_resume_guide
```

## 📱 Real-Time Monitoring

### View Live Conversions
1. Go to **Reports** → **Realtime**
2. Check **Event count by Event name**
3. Look for your conversion events firing in real-time
4. Useful for testing and launch day monitoring

### Debug Events
1. Use **Chrome DevTools** → **Network** tab
2. Filter for "google-analytics.com/g/collect"
3. Check that event parameters are being sent correctly
4. Verify `en` (event name) parameters match expected values

## 🔍 Troubleshooting

### Events Not Appearing in GA4

**Possible causes:**
1. **Delay:** Events can take 24-48 hours to appear in GA4 interface
2. **Ad blockers:** Test in incognito mode or with ad blockers disabled
3. **Incorrect GA4 ID:** Verify `G-KBHMZRVRJ1` is correct in `index.html`

**How to check:**
1. Open browser DevTools → Network tab
2. Filter for "google-analytics.com"
3. Look for requests to `/g/collect?`
4. Verify events are being sent (even if not showing in dashboard yet)

### Conversions Not Counting

**Possible causes:**
1. **Event not marked as conversion:** Toggle conversion switch in Admin → Events
2. **Events not firing:** Check DevTools Network tab for GA requests
3. **User blocked tracking:** Some users block analytics (expected ~10-30% loss)

### Low Conversion Rates

**Normal ranges:**
- **Landing → Resume Upload:** 5-15% (SaaS average)
- **Resume Upload → Analysis Complete:** 70-85% (should be high since they already engaged)
- **Blog → Resume Upload:** 1-5% (content marketing average)

If rates are lower, analyze:
1. **Funnel drop-off report** - Where are users abandoning?
2. **Error events** - Are technical issues blocking users?
3. **Device/browser breakdown** - Is something broken on mobile?

## 📊 Weekly Review Checklist

Every Monday, check these metrics:

- [ ] Total conversions last 7 days vs previous 7 days
- [ ] Conversion rate from landing page → resume upload
- [ ] Top traffic sources and their conversion rates
- [ ] Blog post views and blog-to-app conversions
- [ ] Any error spikes or rate limit hits
- [ ] Return visitor rate
- [ ] Average time to complete analysis (should be < 2 minutes)

## 🎯 Optimization Actions Based on Data

### If conversion rate is low (<5%):
1. Check for errors in error_occurred events
2. Review funnel drop-off report
3. Test user experience on different devices
4. Simplify upload process

### If blog engagement is low:
1. Review blog_scroll_depth - are people reading?
2. Check blog_reading_time - spending enough time?
3. Optimize blog CTAs for better visibility
4. A/B test CTA wording

### If returning visitors are low (<10%):
1. Add email capture for results delivery
2. Implement save/bookmark functionality
3. Send follow-up emails encouraging return visits

## 🚀 Next Steps

1. **Wait 24-48 hours** after deployment for events to populate
2. **Test the site yourself** to generate initial events
3. **Mark events as conversions** in GA4 Admin
4. **Create custom funnel report** to track user journey
5. **Set up weekly reporting** - Calendar reminder every Monday
6. **Use UTM parameters** when submitting to directories and launching on Product Hunt
7. **Monitor Product Hunt launch** closely on launch day using Real-time reports

## 🎓 Learning Resources

- [GA4 Conversion Events Guide](https://support.google.com/analytics/answer/9267568)
- [Creating Custom Funnels](https://support.google.com/analytics/answer/9327974)
- [UTM Parameter Builder](https://ga-dev-tools.google/campaign-url-builder/)
- [GA4 Event Tracking Best Practices](https://support.google.com/analytics/topic/9756175)

---

**Questions or Issues?** Check GA4 Real-time reports first, then verify browser DevTools is showing analytics requests being sent.
