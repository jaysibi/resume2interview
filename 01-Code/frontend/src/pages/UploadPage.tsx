import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';
import type { UploadProgress } from '../types';

export default function UploadPage() {
  const navigate = useNavigate();
  
  const [resumeFile, setResumeFile] = useState<File | null>(null);
  const [jdFile, setJDFile] = useState<File | null>(null);
  
  // V2: Job URL fetch mode
  const [useJobUrl, setUseJobUrl] = useState(false);
  const [jobUrl, setJobUrl] = useState('');
  const [jobTitle, setJobTitle] = useState('');
  const [company, setCompany] = useState('');
  const [fetchingJd, setFetchingJd] = useState(false);
  
  const [resumeProgress, setResumeProgress] = useState<UploadProgress>({
    progress: 0,
    status: 'idle',
  });
  const [jdProgress, setJDProgress] = useState<UploadProgress>({
    progress: 0,
    status: 'idle',
  });
  const [resumeId, setResumeId] = useState<number | null>(null);
  const [jdId, setJDId] = useState<number | null>(null);

  // Handle resume file selection
  const handleResumeChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setResumeFile(file);
      setResumeProgress({ progress: 0, status: 'idle' });
    }
  };

  // Handle JD file selection
  const handleJDChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setJDFile(file);
      setJDProgress({ progress: 0, status: 'idle' });
    }
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
        message: `Resume uploaded successfully (ID: ${response.id})` 
      });
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
      
      setResumeProgress({
        progress: 0,
        status: 'error',
        message: errorMessage,
      });
    }
  };

  // Upload job description
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
        message: `Job description uploaded successfully (ID: ${response.id})` 
      });
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
      
      setJDProgress({
        progress: 0,
        status: 'error',
        message: errorMessage,
      });
    }
  };

  // V2: Fetch JD from URL
  const fetchJDFromUrl = async () => {
    if (!jobUrl) return;

    try {
      setFetchingJd(true);
      setJDProgress({ progress: 50, status: 'uploading' });
      
      // Fetch JD content from URL
      const jdData = await api.fetchJdFromUrl(jobUrl);
      
      // Create a text file from the fetched data
      const jdText = jdData.raw_text;
      const blob = new Blob([jdText], { type: 'text/plain' });
      const file = new File([blob], `${jdData.title || 'job'}.txt`, { type: 'text/plain' });
      
      // Upload the JD with metadata
      const response = await api.uploadJobDescription(
        file,
        undefined, // userEmail
        jobUrl,
        jdData.title || jobTitle,
        jdData.company || company
      );
      
      setJDId(response.id);
      setJobTitle(jdData.title || jobTitle);
      setCompany(jdData.company || company);
      setJDProgress({ 
        progress: 100, 
        status: 'success',
        message: `Job description fetched and uploaded successfully (ID: ${response.id})` 
      });
    } catch (error) {
      console.error('JD fetch error:', error);
      let errorMessage = 'Failed to fetch job description from URL';
      
      if (error instanceof Error) {
        errorMessage = error.message;
      }
      
      setJDProgress({
        progress: 0,
        status: 'error',
        message: errorMessage,
      });
    } finally {
      setFetchingJd(false);
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

            {resumeFile && (
              <div className="mb-4">
                <p className="text-sm text-gray-600 mb-2">
                  Selected: <span className="font-medium">{resumeFile.name}</span>
                </p>
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
            
            {/* V2: Toggle between file upload and URL fetch */}
            <div className="flex gap-2 mb-4">
              <button
                onClick={() => {
                  setUseJobUrl(false);
                  setJDProgress({ progress: 0, status: 'idle' });
                }}
                className={`flex-1 py-2 px-4 rounded-lg font-medium transition-colors ${
                  !useJobUrl
                    ? 'bg-primary-600 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                Upload File
              </button>
              <button
                onClick={() => {
                  setUseJobUrl(true);
                  setJDProgress({ progress: 0, status: 'idle' });
                }}
                className={`flex-1 py-2 px-4 rounded-lg font-medium transition-colors ${
                  useJobUrl
                    ? 'bg-primary-600 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                Fetch from URL
              </button>
            </div>

            {!useJobUrl ? (
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

                {jdFile && (
                  <div className="mb-4">
                    <p className="text-sm text-gray-600 mb-2">
                      Selected: <span className="font-medium">{jdFile.name}</span>
                    </p>
                    
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
              // URL fetch mode (V2)
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Job Posting URL *
                  </label>
                  <input
                    type="url"
                    placeholder="https://www.linkedin.com/jobs/view/..."
                    value={jobUrl}
                    onChange={(e) => setJobUrl(e.target.value)}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                  />
                  <p className="text-xs text-gray-500 mt-1">
                    Supports: LinkedIn, Naukri, Indeed, Monster, Glassdoor
                  </p>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Job Title (optional)
                  </label>
                  <input
                    type="text"
                    placeholder="Senior Software Engineer"
                    value={jobTitle}
                    onChange={(e) => setJobTitle(e.target.value)}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Company (optional)
                  </label>
                  <input
                    type="text"
                    placeholder="Google"
                    value={company}
                    onChange={(e) => setCompany(e.target.value)}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                  />
                </div>

                {jdProgress.status === 'idle' && (
                  <button 
                    onClick={fetchJDFromUrl}
                    disabled={!jobUrl || fetchingJd}
                    className="btn-primary w-full disabled:bg-gray-300 disabled:cursor-not-allowed"
                  >
                    {fetchingJd ? 'Fetching...' : 'Fetch Job Description'}
                  </button>
                )}
              </div>
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
  );
}
