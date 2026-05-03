// API Base Configuration
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

// Types for API responses
export interface Resume {
  id: number;
  filename: string;
  raw_text: string;
  upload_date: string;
}

export interface JobDescription {
  id: number;
  filename: string;
  raw_text: string;
  upload_date: string;
}

export interface GapAnalysisResponse {
  resume_id: number;
  jd_id: number;
  match_percentage: number;
  missing_skills: string[];
  recommendations: string[];
  analysis_timestamp: string;
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
async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      ...options,
      headers: {
        ...options.headers,
      },
    });

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
    if (error instanceof APIError) {
      throw error;
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
  async uploadResume(file: File): Promise<Resume> {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('filename', file.name);

    return apiRequest('/upload-resume/', {
      method: 'POST',
      body: formData,
    });
  },

  async getResume(id: number): Promise<Resume> {
    return apiRequest(`/resume/${id}`);
  },

  async listResumes(): Promise<Resume[]> {
    return apiRequest('/resumes/');
  },

  // Job Description Endpoints
  async uploadJobDescription(file: File): Promise<JobDescription> {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('filename', file.name);

    return apiRequest('/upload-jd/', {
      method: 'POST',
      body: formData,
    });
  },

  async getJobDescription(id: number): Promise<JobDescription> {
    return apiRequest(`/jd/${id}`);
  },

  async listJobDescriptions(): Promise<JobDescription[]> {
    return apiRequest('/jds/');
  },

  // Analysis Endpoints
  async getGapAnalysis(
    resumeId: number,
    jdId: number
  ): Promise<GapAnalysisResponse> {
    // Backend returns nested structure: {resume_id, jd_id, analysis: {...}}
    // We need to flatten it for the frontend
    const response = await apiRequest<{
      resume_id: number;
      jd_id: number;
      analysis: {
        match_score: number;
        missing_required_skills: string[];
        missing_preferred_skills: string[];
        strengths: string[];
        weak_areas: string[];
        recommendations: string[];
      };
    }>(`/gap-analysis/?resume_id=${resumeId}&jd_id=${jdId}`, {
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
    };
  },

  async getATSScore(
    resumeId: number,
    jdId: number
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
};

export default api;
