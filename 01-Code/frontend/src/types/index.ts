// Re-export types from API service
export type {
  Resume,
  JobDescription,
  GapAnalysisResponse,
  ATSScoreResponse,
} from '../services/api';

// Upload state types
export interface UploadProgress {
  progress: number;
  status: 'idle' | 'uploading' | 'processing' | 'success' | 'error';
  message?: string;
}

// Analysis state types
export interface AnalysisState {
  isLoading: boolean;
  gapAnalysis: GapAnalysisResponse | null;
  atsScore: ATSScoreResponse | null;
  error: string | null;
}

// Upload response data
export interface UploadResponse {
  resumeId?: number;
  jdId?: number;
  error?: string;
}

// Import the GapAnalysisResponse for reference
import type { GapAnalysisResponse, ATSScoreResponse } from '../services/api';
