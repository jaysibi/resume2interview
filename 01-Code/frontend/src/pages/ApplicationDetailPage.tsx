import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api, { ApplicationDetail } from '../services/api';

export default function ApplicationDetailPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  
  const [application, setApplication] = useState<ApplicationDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (id) {
      loadApplicationDetail(parseInt(id));
    }
  }, [id]);

  const loadApplicationDetail = async (applicationId: number) => {
    try {
      setLoading(true);
      setError(null);
      const data = await api.getApplicationDetails(applicationId);
      setApplication(data);
    } catch (err) {
      console.error('Error loading application details:', err);
      setError(err instanceof Error ? err.message : 'Failed to load application details');
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 py-12">
        <div className="container mx-auto px-4 max-w-6xl">
          <div className="flex justify-center items-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
          </div>
        </div>
      </div>
    );
  }

  if (error || !application) {
    return (
      <div className="min-h-screen bg-gray-50 py-12">
        <div className="container mx-auto px-4 max-w-6xl">
          <div className="bg-red-50 border border-red-200 rounded-lg p-6">
            <div className="flex items-start">
              <svg className="w-6 h-6 text-red-600 mr-3 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <div>
                <h3 className="text-red-800 font-semibold mb-1">Error Loading Application</h3>
                <p className="text-red-700 text-sm">{error || 'Application not found'}</p>
              </div>
            </div>
            <button
              onClick={() => navigate('/applications')}
              className="mt-4 text-red-700 hover:text-red-900 font-medium"
            >
              ← Back to Applications
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="container mx-auto px-4 max-w-6xl">
        {/* Header */}
        <div className="mb-8">
          <button
            onClick={() => navigate('/applications')}
            className="text-primary-600 hover:text-primary-700 font-medium mb-4 inline-flex items-center"
          >
            <svg className="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
            Back to Applications
          </button>
          
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            {application.job_description?.title || 'Application Details'}
          </h1>
          <p className="text-lg text-gray-600">
            {application.job_description?.company || 'Unknown Company'} • 
            Applied {formatDate(application.application.applied_at)}
          </p>
        </div>

        {/* Application Info Card */}
        <div className="card mb-6">
          <h2 className="text-2xl font-semibold text-gray-900 mb-4">Application Information</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div>
              <span className="text-sm text-gray-500">Status</span>
              <p className="text-lg font-medium text-gray-900 capitalize">{application.application.status}</p>
            </div>
            <div>
              <span className="text-sm text-gray-500">Resume</span>
              <p className="text-lg font-medium text-gray-900">{application.resume?.filename || 'N/A'}</p>
            </div>
            <div>
              <span className="text-sm text-gray-500">Job URL</span>
              {application.job_description?.job_url ? (
                <a 
                  href={application.job_description.job_url} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="text-lg font-medium text-primary-600 hover:text-primary-700"
                >
                  View Posting →
                </a>
              ) : (
                <p className="text-lg font-medium text-gray-400">N/A</p>
              )}
            </div>
            <div>
              <span className="text-sm text-gray-500">Application ID</span>
              <p className="text-lg font-medium text-gray-900">#{application.application.id}</p>
            </div>
          </div>
        </div>

        {/* Gap Analysis Results */}
        {application.gap_analysis && (
          <div className="card mb-6">
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">Gap Analysis</h2>
            
            {/* Match Score */}
            <div className="mb-6">
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm font-medium text-gray-700">Match Score</span>
                <span className="text-2xl font-bold text-primary-600">{application.gap_analysis.match_score}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-3">
                <div 
                  className="bg-primary-600 h-3 rounded-full transition-all duration-500"
                  style={{ width: `${application.gap_analysis.match_score}%` }}
                ></div>
              </div>
            </div>

            {/* Strengths */}
            {application.gap_analysis.strengths.length > 0 && (
              <div className="mb-4">
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Strengths</h3>
                <ul className="list-disc list-inside space-y-1">
                  {application.gap_analysis.strengths.map((strength, idx) => (
                    <li key={idx} className="text-gray-700">{strength}</li>
                  ))}
                </ul>
              </div>
            )}

            {/* Weak Areas */}
            {application.gap_analysis.weak_areas.length > 0 && (
              <div className="mb-4">
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Areas for Improvement</h3>
                <ul className="list-disc list-inside space-y-1">
                  {application.gap_analysis.weak_areas.map((area, idx) => (
                    <li key={idx} className="text-gray-700">{area}</li>
                  ))}
                </ul>
              </div>
            )}

            {/* Missing Skills */}
            {(application.gap_analysis.missing_required_skills.length > 0 || 
              application.gap_analysis.missing_preferred_skills.length > 0) && (
              <div className="mb-4">
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Missing Skills</h3>
                {application.gap_analysis.missing_required_skills.length > 0 && (
                  <div className="mb-2">
                    <span className="text-sm font-medium text-red-600">Required:</span>
                    <div className="flex flex-wrap gap-2 mt-1">
                      {application.gap_analysis.missing_required_skills.map((skill, idx) => (
                        <span key={idx} className="px-3 py-1 bg-red-100 text-red-800 rounded-full text-sm">
                          {skill}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
                {application.gap_analysis.missing_preferred_skills.length > 0 && (
                  <div>
                    <span className="text-sm font-medium text-yellow-600">Preferred:</span>
                    <div className="flex flex-wrap gap-2 mt-1">
                      {application.gap_analysis.missing_preferred_skills.map((skill, idx) => (
                        <span key={idx} className="px-3 py-1 bg-yellow-100 text-yellow-800 rounded-full text-sm">
                          {skill}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* Recommendations */}
            {application.gap_analysis.recommendations.length > 0 && (
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Recommendations</h3>
                <ul className="list-decimal list-inside space-y-1">
                  {application.gap_analysis.recommendations.map((rec, idx) => (
                    <li key={idx} className="text-gray-700">{rec}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}

        {/* ATS Score */}
        {application.ats_score && (
          <div className="card">
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">ATS Compatibility Score</h2>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
              <div>
                <span className="text-sm text-gray-500">Overall ATS Score</span>
                <p className="text-3xl font-bold text-primary-600">{application.ats_score.ats_score}%</p>
              </div>
              <div>
                <span className="text-sm text-gray-500">Keyword Match</span>
                <p className="text-3xl font-bold text-blue-600">{application.ats_score.keyword_match_percentage}%</p>
              </div>
              <div>
                <span className="text-sm text-gray-500">Format Score</span>
                <p className="text-3xl font-bold text-green-600">{application.ats_score.format_score}%</p>
              </div>
            </div>

            {/* Matched Keywords */}
            {application.ats_score.matched_keywords.length > 0 && (
              <div className="mb-4">
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Matched Keywords</h3>
                <div className="flex flex-wrap gap-2">
                  {application.ats_score.matched_keywords.map((keyword, idx) => (
                    <span key={idx} className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm">
                      {keyword}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* Missing Keywords */}
            {application.ats_score.missing_keywords.length > 0 && (
              <div className="mb-4">
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Missing Keywords</h3>
                <div className="flex flex-wrap gap-2">
                  {application.ats_score.missing_keywords.map((keyword, idx) => (
                    <span key={idx} className="px-3 py-1 bg-red-100 text-red-800 rounded-full text-sm">
                      {keyword}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* Recommendations */}
            {application.ats_score.recommendations.length > 0 && (
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">ATS Recommendations</h3>
                <ul className="list-decimal list-inside space-y-1">
                  {application.ats_score.recommendations.map((rec, idx) => (
                    <li key={idx} className="text-gray-700">{rec}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}

        {/* No Analysis Available */}
        {!application.gap_analysis && !application.ats_score && (
          <div className="card text-center py-12">
            <svg className="mx-auto h-12 w-12 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
            </svg>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">No Analysis Available</h3>
            <p className="text-gray-600">
              Analysis results have not been generated for this application yet.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
