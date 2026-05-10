// API Base Configuration
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

// Types for API responses
export interface Resume {
  id: string;
  filename: string;
  raw_text: string;
  upload_date: string;
  user_id?: number; // V2: Optional user context
}

export interface JobDescription {
  id: string;
  filename: string;
  raw_text: string;
  upload_date: string;
  user_id?: number; // V2: Optional user context
  job_url?: string; // V2: Job posting URL
  title?: string; // V2: Job title
  company?: string; // V2: Company name
}

export interface GapAnalysisResponse {
  resume_id: number;
  jd_id: number;
  match_percentage: number;
  missing_skills: string[];
  recommendations: string[];
  analysis_timestamp: string;
  application_id?: number; // V2: Optional application tracking
}

export interface ATSScoreResponse {
  resume_id: number;
  jd_id: number;
  ats_score: number;
  keyword_match_percentage: number;
  format_score: number;
  overall_feedback: string;
  missing_keywords: string[];
  analysis_timestamp: string;
}

// V2 Types
export interface FetchJDRequest {
  job_url: string;
}

export interface FetchJDResponse {
  title: string;
  company: string;
  raw_text: string;
}

export interface Application {
  application_id: number;
  resume_id: number;
  resume_filename: string;
  jd_id: number;
  jd_title: string;
  jd_company: string;
  applied_at: string;
  status: string;
  notes?: string;
}

export interface ApplicationDetail {
  application: {
    id: number;
    user_id: number;
    status: string;
    applied_at: string;
    notes?: string;
  };
  resume: {
    id: number;
    filename: string;
    skills: any[];
    experience: any[];
    education: any[];
    upload_date: string;
  } | null;
  job_description: {
    id: number;
    filename?: string;
    title?: string;
    company?: string;
    job_url?: string;
    mandatory_skills: any[];
    preferred_skills: any[];
    keywords: any[];
    upload_date: string;
  } | null;
  gap_analysis: {
    match_score: number;
    missing_required_skills: string[];
    missing_preferred_skills: string[];
    strengths: string[];
    weak_areas: string[];
    recommendations: string[];
    created_at: string;
  } | null;
  ats_score: {
    ats_score: number;
    keyword_match_percentage: number;
    format_score: number;
    matched_keywords: string[];
    missing_keywords: string[];
    issues: any[];
    recommendations: string[];
    created_at: string;
  } | null;
}

// API Error class
export class APIError extends Error {
  constructor(
    message: string,
    public status?: number,
    public data?: any
  ) {
    super(message);
    this.name = 'APIError';
  }
}

// Generic API request handler
// timeoutMs: how long to wait before aborting; 0 = no timeout (default 30s)
async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {},
  timeoutMs = 30_000
): Promise<T> {
  const controller = new AbortController();
  const timer = timeoutMs > 0 ? setTimeout(() => controller.abort(), timeoutMs) : null;
  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      ...options,
      signal: controller.signal,
      headers: {
        ...options.headers,
      },
    });
    if (timer) clearTimeout(timer);

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      
      // Handle different error response formats
      let errorMessage = `API Error: ${response.statusText}`;
      
      if (errorData.detail) {
        if (typeof errorData.detail === 'string') {
          errorMessage = errorData.detail;
        } else if (typeof errorData.detail === 'object') {
          // Handle nested error object with message and details
          errorMessage = errorData.detail.message || JSON.stringify(errorData.detail);
          if (errorData.detail.details) {
            errorMessage += `: ${errorData.detail.details}`;
          }
        }
      }
      
      throw new APIError(
        errorMessage,
        response.status,
        errorData
      );
    }

    return await response.json();
  } catch (error) {
    if (timer) clearTimeout(timer);
    if (error instanceof APIError) {
      throw error;
    }
    if (error instanceof DOMException && error.name === 'AbortError') {
      throw new APIError('The request timed out. The server is taking too long to respond — please try again.');
    }
    throw new APIError(
      error instanceof Error ? error.message : 'Network error occurred'
    );
  }
}

// API Service Methods
export const api = {
  // Health Check
  async healthCheck(): Promise<{ message: string }> {
    return apiRequest('/');
  },

  // Resume Endpoints
  async uploadResume(file: File, userEmail?: string): Promise<Resume> {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('filename', file.name);
    
    // V2: Add optional user_email parameter
    if (userEmail) {
      formData.append('user_email', userEmail);
    }

    return apiRequest('/upload-resume/', {
      method: 'POST',
      body: formData,
    }, 120_000);
  },

  async getResume(id: number): Promise<Resume> {
    return apiRequest(`/resume/${id}`);
  },

  async listResumes(): Promise<Resume[]> {
    return apiRequest('/resumes/');
  },

  // Job Description Endpoints
  async uploadJobDescription(
    file: File, 
    userEmail?: string, 
    jobUrl?: string, 
    title?: string, 
    company?: string
  ): Promise<JobDescription> {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('filename', file.name);
    
    // V2: Add optional parameters
    if (userEmail) {
      formData.append('user_email', userEmail);
    }
    if (jobUrl) {
      formData.append('job_url', jobUrl);
    }
    if (title) {
      formData.append('title', title);
    }
    if (company) {
      formData.append('company', company);
    }

    return apiRequest('/upload-jd/', {
      method: 'POST',
      body: formData,
    }, 120_000);
  },

  async getJobDescription(id: number): Promise<JobDescription> {
    return apiRequest(`/jd/${id}`);
  },

  async listJobDescriptions(): Promise<JobDescription[]> {
    return apiRequest('/jds/');
  },

  // Analysis Endpoints
  async getGapAnalysis(
    resumeId: string,
    jdId: string,
    userEmail?: string,
    createApplication: boolean = false
  ): Promise<GapAnalysisResponse> {
    // Build query parameters
    const params = new URLSearchParams({ 
      resume_id: resumeId, 
      jd_id: jdId
    });
    
    // V2: Add optional parameters
    if (userEmail) {
      params.append('user_email', userEmail);
    }
    if (createApplication) {
      params.append('create_application', 'true');
    }
    
    // Backend returns nested structure: {resume_id, jd_id, analysis: {...}, application_id?: number}
    // We need to flatten it for the frontend
    const response = await apiRequest<{
      resume_id: number;
      jd_id: number;
      application_id?: number; // V2: Optional application tracking
      analysis: {
        match_score: number;
        missing_required_skills: string[];
        missing_preferred_skills: string[];
        strengths: string[];
        weak_areas: string[];
        recommendations: string[];
      };
    }>(`/gap-analysis/?${params.toString()}`, {
      method: 'POST',
    });
    
    // Transform nested response to flat structure
    return {
      resume_id: response.resume_id,
      jd_id: response.jd_id,
      match_percentage: response.analysis.match_score,
      missing_skills: [
        ...response.analysis.missing_required_skills,
        ...response.analysis.missing_preferred_skills
      ],
      recommendations: response.analysis.recommendations,
      analysis_timestamp: new Date().toISOString(),
      application_id: response.application_id, // V2: Include application ID if created
    };
  },

  async getATSScore(
    resumeId: string,
    jdId: string
  ): Promise<ATSScoreResponse> {
    // Backend returns nested structure: {resume_id, jd_id, scoring: {...}}
    // We need to flatten it for the frontend
    const response = await apiRequest<{
      resume_id: number;
      jd_id: number;
      scoring: {
        ats_score: number;
        keyword_match_percentage: number;
        format_score: number;
        matched_keywords: string[];
        missing_keywords: string[];
        issues: Array<{
          type: string;
          description: string;
          severity: string;
        }>;
        recommendations: string[];
      };
    }>(`/ats-score/?resume_id=${resumeId}&jd_id=${jdId}`, {
      method: 'POST',
    });
    
    // Transform nested response to flat structure
    // Generate overall feedback from issues
    let overall_feedback = "Your resume is ATS compatible.";
    if (response.scoring.issues.length > 0) {
      const highSeverity = response.scoring.issues.filter(i => i.severity === 'HIGH').length;
      if (highSeverity > 0) {
        overall_feedback = `${highSeverity} high-priority issues found that may affect ATS parsing.`;
      } else {
        overall_feedback = `${response.scoring.issues.length} minor issues found.`;
      }
    }
    
    return {
      resume_id: response.resume_id,
      jd_id: response.jd_id,
      ats_score: response.scoring.ats_score,
      keyword_match_percentage: response.scoring.keyword_match_percentage,
      format_score: response.scoring.format_score,
      overall_feedback: overall_feedback,
      missing_keywords: response.scoring.missing_keywords,
      analysis_timestamp: new Date().toISOString(),
    };
  },

  // ===========================
  // V2 API Endpoints
  // ===========================

  // Fetch JD from URL (V2 only)
  async fetchJdFromUrl(jobUrl: string): Promise<FetchJDResponse> {
    return apiRequest('/v2/fetch-jd-from-url/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ job_url: jobUrl }),
    });
  },

  // Get list of applications for a user (V2 only)
  async getApplications(
    userEmail?: string,
    skip: number = 0,
    limit: number = 100
  ): Promise<{
    user_id: number;
    user_email: string;
    total: number;
    skip: number;
    limit: number;
    applications: Application[];
  }> {
    const params = new URLSearchParams({ 
      skip: skip.toString(), 
      limit: limit.toString() 
    });
    
    if (userEmail) {
      params.append('user_email', userEmail);
    }
    
    return apiRequest(`/v2/applications/?${params.toString()}`);
  },

  // Get detailed information about a specific application (V2 only)
  async getApplicationDetails(applicationId: number): Promise<ApplicationDetail> {
    return apiRequest(`/v2/applications/${applicationId}/`);
  },

  // Delete a single application
  async deleteApplication(applicationId: number): Promise<{ success: boolean; message: string }> {
    return apiRequest(`/v2/applications/${applicationId}/`, {
      method: 'DELETE',
    });
  },

  // Delete multiple applications
  async deleteApplicationsBulk(applicationIds: number[]): Promise<{ success: boolean; deleted_count: number; message: string }> {
    return apiRequest('/v2/applications/bulk-delete/', {
      method: 'POST',
      body: JSON.stringify(applicationIds),
    });
  },
};

export default api;
