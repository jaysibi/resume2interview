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
