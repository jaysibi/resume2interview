import { useEffect, useRef } from 'react';
import {
  trackBlogScrollDepth,
  trackBlogReadingTime,
  trackEngagementTime,
  initScrollTracking,
} from '../services/analytics';

/**
 * Custom hook for tracking blog post engagement
 * Automatically tracks reading time, scroll depth, and engagement metrics
 * 
 * @param postTitle - The title of the blog post for tracking
 * @param postSlug - URL slug of the post (e.g., 'tailor-resume-to-job-description')
 */
export const useBlogAnalytics = (postTitle: string, postSlug: string) => {
  const startTimeRef = useRef<number>(Date.now());
  const scrollMilestonesRef = useRef<Set<number>>(new Set());
  const hasTrackedReadingTimeRef = useRef(false);

  useEffect(() => {
    // Reset start time when component mounts
    startTimeRef.current = Date.now();

    // Initialize scroll tracking
    const cleanupScroll = initScrollTracking(`blog/${postSlug}`);

    // Track scroll depth for blog-specific milestones
    const handleScroll = () => {
      const scrollHeight = document.documentElement.scrollHeight - window.innerHeight;
      const scrolled = window.scrollY;
      const scrollPercentage = Math.round((scrolled / scrollHeight) * 100);

      // Track blog scroll milestones: 25%, 50%, 75%, 100%
      [25, 50, 75, 100].forEach((milestone) => {
        if (scrollPercentage >= milestone && !scrollMilestonesRef.current.has(milestone)) {
          scrollMilestonesRef.current.add(milestone);
          trackBlogScrollDepth(postTitle, milestone);
        }
      });
    };

    // Track time spent on page when user leaves
    const handleVisibilityChange = () => {
      if (document.hidden && !hasTrackedReadingTimeRef.current) {
        const timeSpent = Math.floor((Date.now() - startTimeRef.current) / 1000);
        if (timeSpent > 5) { // Only track if spent more than 5 seconds
          trackBlogReadingTime(postTitle, timeSpent);
          hasTrackedReadingTimeRef.current = true;
        }
      }
    };

    // Track engagement time when component unmounts
    const trackEngagementOnUnmount = () => {
      const engagementTime = Math.floor((Date.now() - startTimeRef.current) / 1000);
      if (engagementTime > 5 && !hasTrackedReadingTimeRef.current) {
        trackBlogReadingTime(postTitle, engagementTime);
        trackEngagementTime(`blog/${postSlug}`, engagementTime);
      }
    };

    window.addEventListener('scroll', handleScroll);
    document.addEventListener('visibilitychange', handleVisibilityChange);
    window.addEventListener('beforeunload', trackEngagementOnUnmount);

    // Cleanup
    return () => {
      trackEngagementOnUnmount();
      window.removeEventListener('scroll', handleScroll);
      document.removeEventListener('visibilitychange', handleVisibilityChange);
      window.removeEventListener('beforeunload', trackEngagementOnUnmount);
      cleanupScroll();
    };
  }, [postTitle, postSlug]);

  return {
    startTime: startTimeRef.current,
  };
};
