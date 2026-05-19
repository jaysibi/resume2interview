/**
 * Google Analytics 4 Event Tracking Service
 * Provides typed event tracking for Resume2Interview
 */

// Extend Window interface to include gtag
declare global {
  interface Window {
    gtag?: (...args: any[]) => void;
    dataLayer?: any[];
  }
}

/**
 * Track a custom event in Google Analytics
 */
export const trackEvent = (
  eventName: string,
  eventParams?: Record<string, any>
) => {
  if (typeof window !== 'undefined' && window.gtag) {
    window.gtag('event', eventName, eventParams);
  }
};

/**
 * Track resume upload event
 */
export const trackResumeUpload = (filename: string, fileSize: number) => {
  trackEvent('upload_resume', {
    filename,
    file_size_kb: Math.round(fileSize / 1024),
  });
};

/**
 * Track job description upload event
 */
export const trackJobDescriptionUpload = (
  filename: string,
  fileSize: number,
  hasUrl?: boolean
) => {
  trackEvent('upload_job_description', {
    filename,
    file_size_kb: Math.round(fileSize / 1024),
    has_url: hasUrl || false,
  });
};

/**
 * Track gap analysis request
 */
export const trackGapAnalysisRequest = (
  resumeId: string,
  jdId: string,
  matchScore?: number
) => {
  trackEvent('gap_analysis_request', {
    resume_id: resumeId,
    jd_id: jdId,
    match_score: matchScore,
  });
};

/**
 * Track gap analysis completion
 */
export const trackGapAnalysisComplete = (
  matchScore: number,
  missingSkillsCount: number,
  recommendationsCount: number
) => {
  trackEvent('gap_analysis_complete', {
    match_score: matchScore,
    missing_skills_count: missingSkillsCount,
    recommendations_count: recommendationsCount,
  });
};

/**
 * Track ATS score request
 */
export const trackATSScoreRequest = (
  resumeId: string,
  jdId: string,
  atsScore?: number
) => {
  trackEvent('ats_score_request', {
    resume_id: resumeId,
    jd_id: jdId,
    ats_score: atsScore,
  });
};

/**
 * Track ATS score completion
 */
export const trackATSScoreComplete = (
  atsScore: number,
  keywordMatchPercentage: number,
  formatScore: number
) => {
  trackEvent('ats_score_complete', {
    ats_score: atsScore,
    keyword_match_percentage: keywordMatchPercentage,
    format_score: formatScore,
  });
};

/**
 * Track application error
 */
export const trackError = (
  errorType: string,
  errorMessage: string,
  page?: string
) => {
  trackEvent('error_occurred', {
    error_type: errorType,
    error_message: errorMessage,
    page,
  });
};

/**
 * Track rate limit hit
 */
export const trackRateLimitHit = (
  currentCount: number,
  limit: number,
  resetTime: string
) => {
  trackEvent('rate_limit_hit', {
    current_count: currentCount,
    limit,
    reset_time: resetTime,
  });
};

/**
 * Track page view (manual tracking for SPAs)
 */
export const trackPageView = (path: string, title?: string) => {
  if (typeof window !== 'undefined' && window.gtag) {
    window.gtag('event', 'page_view', {
      page_path: path,
      page_title: title || document.title,
    });
  }
};

/**
 * Track navigation to specific features
 */
export const trackNavigation = (destination: string) => {
  trackEvent('navigation', {
    destination,
  });
};

/**
 * Track CTA button clicks
 */
export const trackCTAClick = (ctaName: string, location: string) => {
  trackEvent('cta_click', {
    cta_name: ctaName,
    location,
  });
};

// ============================================================================
// CONVERSION TRACKING
// ============================================================================

/**
 * Track resume upload conversion (primary conversion)
 * This should be marked as a key conversion event in GA4
 */
export const trackResumeUploadConversion = (
  filename: string,
  fileSize: number,
  source?: string
) => {
  trackEvent('conversion_resume_upload', {
    filename,
    file_size_kb: Math.round(fileSize / 1024),
    traffic_source: source || 'direct',
    value: 10, // Assign value to conversion
  });
};

/**
 * Track analysis completion conversion (secondary conversion)
 * User has completed their first analysis
 */
export const trackAnalysisCompletionConversion = (
  analysisType: 'gap_analysis' | 'ats_score',
  matchScore: number,
  timeToComplete: number
) => {
  trackEvent('conversion_analysis_complete', {
    analysis_type: analysisType,
    match_score: matchScore,
    time_to_complete_seconds: Math.round(timeToComplete),
    value: 20, // Higher value for completed analysis
  });
};

/**
 * Track user signup/account creation (if implemented)
 */
export const trackSignupConversion = (method: string, userId?: string) => {
  trackEvent('conversion_signup', {
    signup_method: method,
    user_id: userId,
    value: 15,
  });
};

/**
 * Track blog to app conversion
 * User came from blog and uploaded a resume
 */
export const trackBlogToAppConversion = (
  blogPost: string,
  timeOnBlog: number
) => {
  trackEvent('conversion_blog_to_app', {
    blog_post: blogPost,
    time_on_blog_seconds: Math.round(timeOnBlog),
    value: 12,
  });
};

// ============================================================================
// BLOG ENGAGEMENT TRACKING
// ============================================================================

/**
 * Track blog post scroll depth
 */
export const trackBlogScrollDepth = (
  postTitle: string,
  scrollPercentage: number
) => {
  // Only track at milestones: 25%, 50%, 75%, 100%
  const milestone = Math.floor(scrollPercentage / 25) * 25;
  trackEvent('blog_scroll_depth', {
    post_title: postTitle,
    scroll_percentage: milestone,
  });
};

/**
 * Track blog post reading time
 */
export const trackBlogReadingTime = (
  postTitle: string,
  timeSpentSeconds: number
) => {
  trackEvent('blog_reading_time', {
    post_title: postTitle,
    time_spent_seconds: Math.round(timeSpentSeconds),
    engaged_reading: timeSpentSeconds > 60, // More than 1 minute
  });
};

/**
 * Track blog CTA clicks (e.g., "Try It Now" from blog)
 */
export const trackBlogCTAClick = (
  postTitle: string,
  ctaText: string,
  ctaLocation: string
) => {
  trackEvent('blog_cta_click', {
    post_title: postTitle,
    cta_text: ctaText,
    cta_location: ctaLocation,
  });
};

/**
 * Track blog post share
 */
export const trackBlogShare = (
  postTitle: string,
  platform: 'twitter' | 'linkedin' | 'facebook' | 'copy_link'
) => {
  trackEvent('blog_share', {
    post_title: postTitle,
    platform,
  });
};

// ============================================================================
// ENHANCED ENGAGEMENT TRACKING
// ============================================================================

/**
 * Track external link clicks
 */
export const trackExternalLinkClick = (
  url: string,
  linkText: string,
  location: string
) => {
  trackEvent('external_link_click', {
    url,
    link_text: linkText,
    location,
  });
};

/**
 * Track file downloads/exports
 */
export const trackDownload = (
  fileType: 'resume' | 'analysis_report' | 'recommendations',
  fileName: string
) => {
  trackEvent('file_download', {
    file_type: fileType,
    file_name: fileName,
  });
};

/**
 * Track user engagement time on page
 */
export const trackEngagementTime = (
  page: string,
  engagementTimeSeconds: number
) => {
  trackEvent('user_engagement', {
    page,
    engagement_time_seconds: Math.round(engagementTimeSeconds),
    engaged_session: engagementTimeSeconds > 30,
  });
};

/**
 * Track feature discovery
 */
export const trackFeatureDiscovery = (featureName: string, howDiscovered: string) => {
  trackEvent('feature_discovery', {
    feature_name: featureName,
    how_discovered: howDiscovered,
  });
};

// ============================================================================
// USER JOURNEY TRACKING
// ============================================================================

/**
 * Track user journey steps
 */
export const trackJourneyStep = (
  step: 'landing' | 'upload_resume' | 'upload_jd' | 'view_analysis' | 'download_results',
  stepNumber: number,
  previousStep?: string
) => {
  trackEvent('user_journey_step', {
    step,
    step_number: stepNumber,
    previous_step: previousStep,
  });
};

/**
 * Track funnel drop-off
 */
export const trackFunnelDropOff = (
  stage: string,
  reason?: string
) => {
  trackEvent('funnel_drop_off', {
    stage,
    reason,
  });
};

/**
 * Track return visitor
 */
export const trackReturnVisitor = (daysSinceLastVisit: number) => {
  trackEvent('return_visitor', {
    days_since_last_visit: daysSinceLastVisit,
    is_regular_user: daysSinceLastVisit < 7,
  });
};

// ============================================================================
// SCROLL DEPTH TRACKING (PAGE-LEVEL)
// ============================================================================

let scrollDepthTracked = {
  '25': false,
  '50': false,
  '75': false,
  '100': false,
};

/**
 * Initialize scroll depth tracking for current page
 * Call this on page load
 */
export const initScrollTracking = (pageName: string) => {
  // Reset tracking for new page
  scrollDepthTracked = {
    '25': false,
    '50': false,
    '75': false,
    '100': false,
  };

  const handleScroll = () => {
    const scrollPercentage = Math.round(
      ((window.scrollY + window.innerHeight) / document.documentElement.scrollHeight) * 100
    );

    // Track milestones
    if (scrollPercentage >= 25 && !scrollDepthTracked['25']) {
      scrollDepthTracked['25'] = true;
      trackEvent('scroll_depth', { page: pageName, depth: 25 });
    }
    if (scrollPercentage >= 50 && !scrollDepthTracked['50']) {
      scrollDepthTracked['50'] = true;
      trackEvent('scroll_depth', { page: pageName, depth: 50 });
    }
    if (scrollPercentage >= 75 && !scrollDepthTracked['75']) {
      scrollDepthTracked['75'] = true;
      trackEvent('scroll_depth', { page: pageName, depth: 75 });
    }
    if (scrollPercentage >= 100 && !scrollDepthTracked['100']) {
      scrollDepthTracked['100'] = true;
      trackEvent('scroll_depth', { page: pageName, depth: 100 });
    }
  };

  window.addEventListener('scroll', handleScroll);
  
  // Return cleanup function
  return () => window.removeEventListener('scroll', handleScroll);
};
