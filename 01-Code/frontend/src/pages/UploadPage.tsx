import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Layout from '../components/Layout';
import api from '../services/api';
import type { UploadProgress } from '../types';
import { trackResumeUpload, trackJobDescriptionUpload, trackError } from '../services/analytics';
import SEO from '../components/SEO';
import {
  validateFile,
  validateJobDescriptionText,
  sanitizeFileName,
  formatFileSize,
} from '../utils/fileValidation';

export default function UploadPage() {
  const navigate = useNavigate();
  
  const [resumeFile, setResumeFile] = useState<File | null>(null);
  const [jdFile, setJDFile] = useState<File | null>(null);
  
  // JD input mode: 'file' or 'text'
  const [jdInputMode, setJdInputMode] = useState<'file' | 'text'>('text');
  const [jdText, setJdText] = useState('');
  
  // Optional metadata fields
  const [jobUrl, setJobUrl] = useState('');
  const [jobTitle, setJobTitle] = useState('');
  const [company, setCompany] = useState('');
  
  const [resumeProgress, setResumeProgress] = useState<UploadProgress>({
    progress: 0,
    status: 'idle',
  });
  const [jdProgress, setJDProgress] = useState<UploadProgress>({
    progress: 0,
    status: 'idle',
  });
  const [resumeId, setResumeId] = useState<string | null>(null);
  const [jdId, setJDId] = useState<string | null>(null);
  
  // Validation error states
  const [resumeError, setResumeError] = useState<string | null>(null);
  const [jdError, setJDError] = useState<string | null>(null);
  const [jdTextError, setJDTextError] = useState<string | null>(null);

  // Handle resume file selection with validation
  const handleResumeChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      // Validate file
      const validation = validateFile(file);
      if (!validation.valid) {
        setResumeError(validation.error || 'Invalid file');
        setResumeFile(null);
        e.target.value = ''; // Clear input
        return;
      }
      
      setResumeError(null);
      setResumeFile(file);
      setResumeProgress({ progress: 0, status: 'idle' });
      setResumeId(null); // Reset upload if changing file
    }
  };

  // Handle JD file selection with validation
  const handleJDChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      // Validate file
      const validation = validateFile(file);
      if (!validation.valid) {
        setJDError(validation.error || 'Invalid file');
        setJDFile(null);
        e.target.value = ''; // Clear input
        return;
      }
      
      setJDError(null);
      setJDFile(file);
      setJDProgress({ progress: 0, status: 'idle' });
      setJDId(null); // Reset upload if changing file
    }
  };
  
  // Validate JD text input
  const handleJDTextChange = (text: string) => {
    setJdText(text);
    setJDTextError(null);
    
    // Clear error when user starts typing
    if (text.length > 0) {
      setJDError(null);
    }
  };
  
  // Remove resume file
  const removeResumeFile = () => {
    setResumeFile(null);
    setResumeProgress({ progress: 0, status: 'idle' });
    setResumeId(null);
    setResumeError(null);
    // Clear file input
    const fileInput = document.getElementById('resume-upload') as HTMLInputElement;
    if (fileInput) fileInput.value = '';
  };
  
  // Remove JD file
  const removeJDFile = () => {
    setJDFile(null);
    setJDProgress({ progress: 0, status: 'idle' });
    setJDId(null);
    setJDError(null);
    // Clear file input
    const fileInput = document.getElementById('jd-upload') as HTMLInputElement;
    if (fileInput) fileInput.value = '';
  };
  
  // Clear JD text
  const clearJDText = () => {
    setJdText('');
    setJDProgress({ progress: 0, status: 'idle' });
    setJDId(null);
    setJDTextError(null);
    setJDError(null);
  };

  // Upload resume
  const uploadResume = async () => {
    if (!resumeFile) return;

    try {
      setResumeProgress({ progress: 50, status: 'uploading' });
      const response = await api.uploadResume(resumeFile);
      setResumeId(response.id);
      setResumeProgress({ 
        progress: 100, 
        status: 'success',
        message: 'Resume uploaded successfully' 
      });
      
      // Track successful upload
      trackResumeUpload(resumeFile.name, resumeFile.size);
    } catch (error) {
      console.error('Resume upload error:', error);
      let errorMessage = 'Upload failed';
      
      if (error instanceof Error) {
        errorMessage = error.message;
      } else if (typeof error === 'string') {
        errorMessage = error;
      } else if (error && typeof error === 'object') {
        errorMessage = JSON.stringify(error);
      }
      
      // Track error
      trackError('resume_upload_failed', errorMessage, 'UploadPage');
      
      setResumeProgress({
        progress: 0,
        status: 'error',
        message: errorMessage,
      });
    }
  };

  // Upload job description from file
  const uploadJD = async () => {
    if (!jdFile) return;

    try {
      setJDProgress({ progress: 50, status: 'uploading' });
      // V2: Pass job URL, title, and company if available
      const response = await api.uploadJobDescription(
        jdFile, 
        undefined, // userEmail
        jobUrl || undefined, 
        jobTitle || undefined, 
        company || undefined
      );
      setJDId(response.id);
      setJDProgress({ 
        progress: 100, 
        status: 'success',
        message: 'Job description uploaded successfully' 
      });
      
      // Track successful upload
      trackJobDescriptionUpload(jdFile.name, jdFile.size, !!jobUrl);
    } catch (error) {
      console.error('JD upload error:', error);
      let errorMessage = 'Upload failed';
      
      if (error instanceof Error) {
        errorMessage = error.message;
      } else if (typeof error === 'string') {
        errorMessage = error;
      } else if (error && typeof error === 'object') {
        errorMessage = JSON.stringify(error);
      }
      
      // Track error
      trackError('jd_upload_failed', errorMessage, 'UploadPage');
      
      setJDProgress({
        progress: 0,
        status: 'error',
        message: errorMessage,
      });
    }
  };

  // Upload job description from pasted text
  const uploadJDFromText = async () => {
    if (!jdText.trim()) {
      setJDTextError('Job description cannot be empty');
      return;
    }

    // Validate text content
    const validation = validateJobDescriptionText(jdText);
    if (!validation.valid) {
      setJDTextError(validation.error || 'Invalid content');
      if (validation.warnings) {
        console.warn('Security warnings:', validation.warnings);
      }
      trackError('jd_text_validation_failed', validation.error || 'Validation failed', 'UploadPage');
      return;
    }
    
    setJDTextError(null);

    try {
      setJDProgress({ progress: 50, status: 'uploading' });
      
      // Create a text file from the pasted content
      const filename = jobTitle ? `${jobTitle}.txt` : 'job_description.txt';
      const blob = new Blob([jdText], { type: 'text/plain' });
      const file = new File([blob], filename, { type: 'text/plain' });
      
      // Upload the JD with metadata
      const response = await api.uploadJobDescription(
        file,
        undefined, // userEmail
        jobUrl || undefined,
        jobTitle || undefined,
        company || undefined
      );
      
      setJDId(response.id);
      setJDProgress({ 
        progress: 100, 
        status: 'success',
        message: 'Job description uploaded successfully' 
      });
      
      // Track successful upload (text mode)
      trackJobDescriptionUpload(filename, jdText.length, !!jobUrl);
    } catch (error) {
      console.error('JD upload error:', error);
      let errorMessage = 'Upload failed';
      
      if (error instanceof Error) {
        errorMessage = error.message;
      } else if (typeof error === 'string') {
        errorMessage = error;
      } else if (error && typeof error === 'object') {
        errorMessage = JSON.stringify(error);
      }
      
      // Track error
      trackError('jd_text_upload_failed', errorMessage, 'UploadPage');
      
      setJDProgress({
        progress: 0,
        status: 'error',
        message: errorMessage,
      });
    }
  };



  // Analyze both
  const handleAnalyze = () => {
    if (resumeId && jdId) {
      navigate(`/results?resumeId=${resumeId}&jdId=${jdId}`);
    }
  };

  const canAnalyze = resumeProgress.status === 'success' && jdProgress.status === 'success';

  return (
    <Layout>
      <SEO 
        title="Free Resume ATS Checker - Upload Resume & Job Description"
        description="Upload your resume and paste any job description to get instant ATS compatibility score, keyword gap analysis, and tailoring recommendations. 100% free resume checker."
        keywords="free ATS checker, upload resume analyzer, job description matcher, resume compatibility test, ATS score calculator, free resume optimization"
        canonicalUrl="https://resume2interview.com/upload"
      />
      <div className="min-h-screen bg-gray-50 py-12">
        <div className="container mx-auto px-4 max-w-4xl">
          {/* Header */}
          <div className="text-center mb-12">
            <h1 className="text-4xl font-bold text-gray-900 mb-4">
              Upload Your Documents
            </h1>
            <p className="text-lg text-gray-600">
              Upload your resume and the job description to get started
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {/* Resume Upload */}
          <div className="card">
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">
              Resume Upload
            </h2>
            
            <div className="mb-4">
              <label 
                htmlFor="resume-upload"
                className="flex flex-col items-center justify-center w-full h-48 border-2 border-gray-300 border-dashed rounded-lg cursor-pointer bg-gray-50 hover:bg-gray-100 transition-colors"
              >
                <div className="flex flex-col items-center justify-center pt-5 pb-6">
                  <svg className="w-12 h-12 mb-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                  </svg>
                  <p className="mb-2 text-sm text-gray-500">
                    <span className="font-semibold">Click to upload</span> or drag and drop
                  </p>
                  <p className="text-xs text-gray-500">PDF or DOCX (MAX. 5MB)</p>
                </div>
                <input
                  id="resume-upload"
                  type="file"
                  className="hidden"
                  accept=".pdf,.docx"
                  onChange={handleResumeChange}
                />
              </label>
            </div>

            {/* Validation Error */}
            {resumeError && (
              <div className="mb-4 bg-red-50 border border-red-200 rounded-lg p-3">
                <p className="text-red-800 text-sm flex items-start gap-2">
                  <svg className="w-5 h-5 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                  </svg>
                  {resumeError}
                </p>
              </div>
            )}

            {resumeFile && !resumeError && (
              <div className="mb-4">
                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                  <div className="flex items-start justify-between gap-2">
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium text-gray-900 truncate">
                        {sanitizeFileName(resumeFile.name)}
                      </p>
                      <p className="text-xs text-gray-600 mt-1">
                        {formatFileSize(resumeFile.size)} • {resumeFile.type.split('/')[1]?.toUpperCase() || 'File'}
                      </p>
                    </div>
                    {resumeProgress.status === 'idle' && (
                      <button
                        onClick={removeResumeFile}
                        className="flex-shrink-0 text-red-600 hover:text-red-800 p-1"
                        title="Remove file"
                      >
                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                        </svg>
                      </button>
                    )}
                  </div>
                </div>
                {resumeProgress.status === 'idle' && (
                  <button 
                    onClick={uploadResume}
                    className="btn-primary w-full"
                  >
                    Upload Resume
                  </button>
                )}
              </div>
            )}

            {/* Progress/Status */}
            {resumeProgress.status !== 'idle' && (
              <div className="mt-4">
                {resumeProgress.status === 'uploading' && (
                  <div className="text-center">
                    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600 mx-auto"></div>
                    <p className="text-sm text-gray-600 mt-2">Uploading...</p>
                  </div>
                )}
                {resumeProgress.status === 'success' && (
                  <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                    <p className="text-green-800 text-sm">{resumeProgress.message}</p>
                  </div>
                )}
                {resumeProgress.status === 'error' && (
                  <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                    <p className="text-red-800 text-sm">{resumeProgress.message}</p>
                  </div>
                )}
              </div>
            )}
          </div>

          {/* Job Description Upload */}
          <div className="card">
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">
              Job Description
            </h2>
            
            {/* Toggle between file upload and text paste */}
            <div className="flex gap-2 mb-4">
              <button
                onClick={() => {
                  setJdInputMode('file');
                  setJDProgress({ progress: 0, status: 'idle' });
                }}
                className={`flex-1 py-2 px-4 rounded-lg font-medium transition-colors ${
                  jdInputMode === 'file'
                    ? 'bg-primary-600 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                Upload File
              </button>
              <button
                onClick={() => {
                  setJdInputMode('text');
                  setJDProgress({ progress: 0, status: 'idle' });
                }}
                className={`flex-1 py-2 px-4 rounded-lg font-medium transition-colors ${
                  jdInputMode === 'text'
                    ? 'bg-primary-600 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                Paste Text
              </button>
            </div>

            {jdInputMode === 'file' ? (
              // File upload mode
              <>
                <div className="mb-4">
                  <label 
                    htmlFor="jd-upload"
                    className="flex flex-col items-center justify-center w-full h-48 border-2 border-gray-300 border-dashed rounded-lg cursor-pointer bg-gray-50 hover:bg-gray-100 transition-colors"
                  >
                    <div className="flex flex-col items-center justify-center pt-5 pb-6">
                      <svg className="w-12 h-12 mb-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                      </svg>
                      <p className="mb-2 text-sm text-gray-500">
                        <span className="font-semibold">Click to upload</span> or drag and drop
                      </p>
                      <p className="text-xs text-gray-500">PDF, DOCX, or TXT</p>
                    </div>
                    <input
                      id="jd-upload"
                      type="file"
                      className="hidden"
                      accept=".pdf,.docx,.txt"
                      onChange={handleJDChange}
                    />
                  </label>
                </div>

                {/* Validation Error */}
                {jdError && (
                  <div className="mb-4 bg-red-50 border border-red-200 rounded-lg p-3">
                    <p className="text-red-800 text-sm flex items-start gap-2">
                      <svg className="w-5 h-5 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                      </svg>
                      {jdError}
                    </p>
                  </div>
                )}

                {jdFile && !jdError && (
                  <div className="mb-4">
                    <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-3">
                      <div className="flex items-start justify-between gap-2">
                        <div className="flex-1 min-w-0">
                          <p className="text-sm font-medium text-gray-900 truncate">
                            {sanitizeFileName(jdFile.name)}
                          </p>
                          <p className="text-xs text-gray-600 mt-1">
                            {formatFileSize(jdFile.size)} • {jdFile.type.split('/')[1]?.toUpperCase() || 'File'}
                          </p>
                        </div>
                        {jdProgress.status === 'idle' && (
                          <button
                            onClick={removeJDFile}
                            className="flex-shrink-0 text-red-600 hover:text-red-800 p-1"
                            title="Remove file"
                          >
                            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                            </svg>
                          </button>
                        )}
                      </div>
                    </div>
                    
                    {/* Optional metadata fields */}
                    <div className="space-y-2 mb-4">
                      <input
                        type="text"
                        placeholder="Job URL (optional)"
                        value={jobUrl}
                        onChange={(e) => setJobUrl(e.target.value)}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                      />
                      <input
                        type="text"
                        placeholder="Job Title (optional)"
                        value={jobTitle}
                        onChange={(e) => setJobTitle(e.target.value)}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                      />
                      <input
                        type="text"
                        placeholder="Company (optional)"
                        value={company}
                        onChange={(e) => setCompany(e.target.value)}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                      />
                    </div>
                    
                    {jdProgress.status === 'idle' && (
                      <button 
                        onClick={uploadJD}
                        className="btn-primary w-full"
                      >
                        Upload Job Description
                      </button>
                    )}
                  </div>
                )}
              </>
            ) : (
              // Text paste mode
              <>
                <div className="mb-4">
                  <div className="flex items-center justify-between mb-2">
                    <label className="block text-sm font-medium text-gray-700">
                      Job Description Text
                    </label>
                    {jdText.trim() && jdProgress.status === 'idle' && (
                      <button
                        onClick={clearJDText}
                        className="text-sm text-red-600 hover:text-red-800 flex items-center gap-1"
                      >
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                        </svg>
                        Clear
                      </button>
                    )}
                  </div>
                  <textarea
                    value={jdText}
                    onChange={(e) => handleJDTextChange(e.target.value)}
                    placeholder="Paste the job description text here...

Example:
Job Title: Senior Software Engineer
Company: Tech Corp
Location: Remote

Responsibilities:
- Design and develop scalable applications
- Lead technical discussions
- Mentor junior developers

Requirements:
- 5+ years of experience with Python/Java
- Strong understanding of cloud platforms (AWS/Azure)
- Excellent communication skills"
                    className={`w-full h-64 px-4 py-3 border rounded-lg focus:outline-none focus:ring-2 font-mono text-sm ${
                      jdTextError ? 'border-red-300 focus:ring-red-500' : 'border-gray-300 focus:ring-primary-500'
                    }`}
                    disabled={jdProgress.status === 'uploading' || jdProgress.status === 'success'}
                  />
                  <div className="flex items-center justify-between mt-2">
                    <p className="text-xs text-gray-500">
                      Copy the job description from any job board and paste it here
                    </p>
                    <p className={`text-xs ${jdText.length > 45000 ? 'text-orange-600 font-medium' : 'text-gray-500'}`}>
                      {jdText.length.toLocaleString()} / 50,000 characters
                    </p>
                  </div>
                </div>

                {/* Validation Error for text */}
                {jdTextError && (
                  <div className="mb-4 bg-red-50 border border-red-200 rounded-lg p-3">
                    <p className="text-red-800 text-sm flex items-start gap-2">
                      <svg className="w-5 h-5 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                      </svg>
                      {jdTextError}
                    </p>
                  </div>
                )}

                {jdText.trim() && !jdTextError && (
                  <div className="mb-4">
                    <div className="bg-blue-50 border border-blue-200 rounded-lg p-3 mb-3">
                      <p className="text-sm text-gray-700">
                        ✓ Text ready ({jdText.split(/\s+/).filter(w => w.length > 0).length} words, {jdText.split('\n').length} lines)
                      </p>
                    </div>
                    
                    {/* Optional metadata fields */}
                    <div className="space-y-2 mb-4">
                      <input
                        type="text"
                        placeholder="Job URL (optional)"
                        value={jobUrl}
                        onChange={(e) => setJobUrl(e.target.value)}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                      />
                      <input
                        type="text"
                        placeholder="Job Title (optional)"
                        value={jobTitle}
                        onChange={(e) => setJobTitle(e.target.value)}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                      />
                      <input
                        type="text"
                        placeholder="Company (optional)"
                        value={company}
                        onChange={(e) => setCompany(e.target.value)}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                      />
                    </div>
                    
                    {jdProgress.status === 'idle' && (
                      <button 
                        onClick={uploadJDFromText}
                        className="btn-primary w-full"
                      >
                        Upload Job Description
                      </button>
                    )}
                  </div>
                )}
              </>
            )}

            {/* Progress/Status */}
            {jdProgress.status !== 'idle' && (
              <div className="mt-4">
                {jdProgress.status === 'uploading' && (
                  <div className="text-center">
                    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600 mx-auto"></div>
                    <p className="text-sm text-gray-600 mt-2">Uploading...</p>
                  </div>
                )}
                {jdProgress.status === 'success' && (
                  <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                    <p className="text-green-800 text-sm">{jdProgress.message}</p>
                  </div>
                )}
                {jdProgress.status === 'error' && (
                  <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                    <p className="text-red-800 text-sm">{jdProgress.message}</p>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>

        {/* Analyze Button */}
        <div className="mt-12 text-center">
          <button
            onClick={handleAnalyze}
            disabled={!canAnalyze}
            className={`px-12 py-4 text-lg font-semibold rounded-lg transition-colors ${
              canAnalyze
                ? 'bg-primary-600 text-white hover:bg-primary-700'
                : 'bg-gray-300 text-gray-500 cursor-not-allowed'
            }`}
          >
            Analyze Resume →
          </button>
          {!canAnalyze && (
            <p className="text-sm text-gray-500 mt-2">
              Upload both documents to continue
            </p>
          )}
        </div>
      </div>
    </div>
    </Layout>
  );
}
