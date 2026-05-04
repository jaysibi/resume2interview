import { useEffect, useState } from 'react';
import { useSearchParams, Link } from 'react-router-dom';
import Layout from '../components/Layout';
import api from '../services/api';
import type { GapAnalysisResponse, ATSScoreResponse } from '../types';

export default function ResultsPage() {
  const [searchParams] = useSearchParams();
  const resumeId = searchParams.get('resumeId');
  const jdId = searchParams.get('jdId');

  const [gapAnalysis, setGapAnalysis] = useState<GapAnalysisResponse | null>(null);
  const [atsScore, setATSScore] = useState<ATSScoreResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!resumeId || !jdId) {
      setError('Missing resume or job description ID');
      setIsLoading(false);
      return;
    }

    const fetchAnalysis = async () => {
      try {
        setIsLoading(true);
        const [gapData, atsData] = await Promise.all([
          api.getGapAnalysis(resumeId, jdId),
          api.getATSScore(resumeId, jdId),
        ]);
        setGapAnalysis(gapData);
        setATSScore(atsData);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch analysis');
      } finally {
        setIsLoading(false);
      }
    };

    fetchAnalysis();
  }, [resumeId, jdId]);

  // Loading state
  if (isLoading) {
    return (
      <Layout>
        <div className="min-h-screen bg-gray-50 flex items-center justify-center">
          <div className="text-center">
            <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-primary-600 mx-auto mb-4"></div>
            <p className="text-lg text-gray-600">Analyzing your resume...</p>
          </div>
        </div>
      </Layout>
    );
  }

  // Error state
  if (error) {
    return (
      <Layout>
        <div className="min-h-screen bg-gray-50 flex items-center justify-center">
          <div className="card max-w-md">
            <div className="text-red-600 text-5xl mb-4">⚠️</div>
            <h2 className="text-2xl font-bold text-gray-900 mb-2">Error</h2>
            <p className="text-gray-600 mb-4">{error}</p>
            <Link to="/upload" className="btn-primary">
              Try Again
            </Link>
          </div>
        </div>
      </Layout>
    );
  }

  // Helper function to get score color
  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600';
    if (score >= 60) return 'text-yellow-600';
    return 'text-red-600';
  };

  // Helper function to get score background
  const getScoreBg = (score: number) => {
    if (score >= 80) return 'bg-green-50 border-green-200';
    if (score >= 60) return 'bg-yellow-50 border-yellow-200';
    return 'bg-red-50 border-red-200';
  };

  return (
    <Layout>
      <div className="min-h-screen bg-gray-50 py-12">
        <div className="container mx-auto px-4 max-w-6xl">
          {/* Header */}
          <div className="text-center mb-12">
            <h1 className="text-4xl font-bold text-gray-900 mb-4">
              Analysis Results
            </h1>
            <p className="text-lg text-gray-600">
              Here's how your resume matches the job description
            </p>
          </div>

        {/* Main Results Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          {/* ATS Score Card */}
          {atsScore && (
            <div className={`card ${getScoreBg(atsScore.ats_score)}`}>
              <h2 className="text-2xl font-semibold text-gray-900 mb-6">
                ATS Score
              </h2>
              
              {/* Main Score */}
              <div className="text-center mb-6">
                <div className={`text-6xl font-bold ${getScoreColor(atsScore.ats_score)} mb-2`}>
                  {atsScore.ats_score}%
                </div>
                <p className="text-gray-600">Overall ATS Compatibility</p>
              </div>

              {/* Score Breakdown */}
              <div className="space-y-4">
                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span className="font-medium text-gray-700">Keyword Match</span>
                    <span className="font-semibold">{atsScore.keyword_match_percentage}%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div 
                      className="bg-primary-600 h-2 rounded-full transition-all duration-500"
                      style={{ width: `${atsScore.keyword_match_percentage}%` }}
                    ></div>
                  </div>
                </div>

                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span className="font-medium text-gray-700">Format Score</span>
                    <span className="font-semibold">{atsScore.format_score}%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div 
                      className="bg-primary-600 h-2 rounded-full transition-all duration-500"
                      style={{ width: `${atsScore.format_score}%` }}
                    ></div>
                  </div>
                </div>
              </div>

              {/* Feedback */}
              {atsScore.overall_feedback && (
                <div className="mt-6 p-4 bg-white rounded-lg">
                  <p className="text-sm text-gray-700">{atsScore.overall_feedback}</p>
                </div>
              )}
            </div>
          )}

          {/* Gap Analysis Card */}
          {gapAnalysis && (
            <div className={`card ${getScoreBg(gapAnalysis.match_percentage)}`}>
              <h2 className="text-2xl font-semibold text-gray-900 mb-6">
                Skills Match
              </h2>
              
              {/* Match Percentage */}
              <div className="text-center mb-6">
                <div className={`text-6xl font-bold ${getScoreColor(gapAnalysis.match_percentage)} mb-2`}>
                  {gapAnalysis.match_percentage}%
                </div>
                <p className="text-gray-600">Skills Match Rate</p>
              </div>

              {/* Missing Skills Count */}
              {gapAnalysis.missing_skills.length > 0 && (
                <div className="bg-white rounded-lg p-4 mb-4">
                  <div className="flex items-center justify-between">
                    <span className="text-gray-700 font-medium">Missing Skills</span>
                    <span className="text-2xl font-bold text-red-600">
                      {gapAnalysis.missing_skills.length}
                    </span>
                  </div>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Detailed Analysis Sections */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Missing Skills */}
          {gapAnalysis && gapAnalysis.missing_skills.length > 0 && (
            <div className="card">
              <h3 className="text-xl font-semibold text-gray-900 mb-4">
                Missing Skills
              </h3>
              <ul className="space-y-2">
                {gapAnalysis.missing_skills.map((skill, index) => (
                  <li 
                    key={index}
                    className="flex items-start"
                  >
                    <span className="text-red-500 mr-2">•</span>
                    <span className="text-gray-700">{skill}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Missing Keywords */}
          {atsScore && atsScore.missing_keywords.length > 0 && (
            <div className="card">
              <h3 className="text-xl font-semibold text-gray-900 mb-4">
                Missing Keywords
              </h3>
              <div className="flex flex-wrap gap-2">
                {atsScore.missing_keywords.map((keyword, index) => (
                  <span 
                    key={index}
                    className="px-3 py-1 bg-red-50 text-red-700 rounded-full text-sm border border-red-200"
                  >
                    {keyword}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Recommendations */}
          {gapAnalysis && gapAnalysis.recommendations.length > 0 && (
            <div className="card lg:col-span-2">
              <h3 className="text-xl font-semibold text-gray-900 mb-4">
                Recommendations
              </h3>
              <ul className="space-y-3">
                {gapAnalysis.recommendations.map((rec, index) => (
                  <li 
                    key={index}
                    className="flex items-start p-3 bg-blue-50 rounded-lg"
                  >
                    <span className="text-blue-600 mr-3 text-xl">💡</span>
                    <span className="text-gray-700">{rec}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>

        {/* Action Buttons */}
        <div className="mt-12 flex flex-col sm:flex-row gap-4 justify-center">
          <Link to="/upload" className="btn-primary text-center">
            Analyze Another Resume
          </Link>
          <button 
            onClick={() => window.print()}
            className="btn-secondary text-center"
          >
            Download Report
          </button>
        </div>

        {/* Timestamp */}
        {gapAnalysis && (
          <div className="mt-8 text-center text-sm text-gray-500">
            Analysis performed on {new Date(gapAnalysis.analysis_timestamp).toLocaleString()}
          </div>
        )}
      </div>
    </div>
    </Layout>
  );
}
