import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Layout from '../components/Layout';
import api from '../services/api';
import type { UploadProgress } from '../types';
import { trackResumeUpload, trackJobDescriptionUpload, trackError } from '../services/analytics';
import SEO from '../components/SEO';

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
    if (!jdText.trim()) return;

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
              // Text paste mode
              <>
                <div className="mb-4">
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Job Description Text
                  </label>
                  <textarea
                    value={jdText}
                    onChange={(e) => setJdText(e.target.value)}
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
                    className="w-full h-64 px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 font-mono text-sm"
                  />
                  <p className="text-xs text-gray-500 mt-2">
                    Copy the job description from any job board and paste it here
                  </p>
                </div>

                {jdText.trim() && (
                  <div className="mb-4">
                    <p className="text-sm text-gray-600 mb-2">
                      Characters: <span className="font-medium">{jdText.length}</span>
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
