import { useEffect, useState } from 'react';
import Layout from '../components/Layout';

interface UsageStats {
  date: string;
  total_requests: number;
  unique_ips: number;
  ips_at_limit: number;
  daily_limit: number;
  top_ips: [string, number][];
}

interface UsageLog {
  id: number;
  ip_address: string;
  endpoint: string;
  method: string;
  status_code: number;
  rate_limited: boolean;
  created_at: string;
}

interface HistoricalStats {
  period_days: number;
  total_requests: number;
  rate_limited_requests: number;
  unique_ips: number;
  top_ips: { ip: string; count: number }[];
  endpoint_distribution: { endpoint: string; count: number }[];
  recent_logs: UsageLog[];
}

interface ApplicationStats {
  period_days: number;
  total_applications: number;
  unique_users: number;
  avg_match_score: number;
  avg_ats_score: number;
  top_companies: { company: string; count: number }[];
  top_job_titles: { title: string; count: number }[];
  top_missing_skills: { skill: string; count: number }[];
  daily_trend: { date: string; count: number }[];
  score_distribution: {
    "0-20": number;
    "21-40": number;
    "41-60": number;
    "61-80": number;
    "81-100": number;
  };
}

export default function Analytics() {
  const [password, setPassword] = useState<string>('');
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
  const [passwordInput, setPasswordInput] = useState<string>('');
  const [authError, setAuthError] = useState<string>('');
  
  const [currentStats, setCurrentStats] = useState<UsageStats | null>(null);
  const [historicalStats, setHistoricalStats] = useState<HistoricalStats | null>(null);
  const [applicationStats, setApplicationStats] = useState<ApplicationStats | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Check for saved password on mount
  useEffect(() => {
    const savedPassword = sessionStorage.getItem('analytics_password');
    if (savedPassword) {
      setPassword(savedPassword);
      setIsAuthenticated(true);
    }
  }, []);

  // Fetch data when authenticated
  useEffect(() => {
    if (isAuthenticated && password) {
      fetchAllData();
      // Refresh every 30 seconds
      const interval = setInterval(fetchAllData, 30000);
      return () => clearInterval(interval);
    }
  }, [isAuthenticated, password]);

  const handleLogin = () => {
    if (!passwordInput.trim()) {
      setAuthError('Please enter a password');
      return;
    }
    
    setPassword(passwordInput);
    sessionStorage.setItem('analytics_password', passwordInput);
    setIsAuthenticated(true);
    setAuthError('');
  };

  const handleLogout = () => {
    setPassword('');
    setPasswordInput('');
    setIsAuthenticated(false);
    sessionStorage.removeItem('analytics_password');
    setCurrentStats(null);
    setHistoricalStats(null);
    setApplicationStats(null);
  };

  const fetchAllData = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const headers = {
        'X-Analytics-Password': password
      };

      // Call Railway backend directly (Vercel free plan doesn't support external rewrites)
      const backendUrl = 'https://resume2interview-production.up.railway.app';
      
      // Fetch all analytics data in parallel
      const [currentResponse, historyResponse, appResponse] = await Promise.all([
        fetch(`${backendUrl}/api/analytics/usage-stats`, { headers }),
        fetch(`${backendUrl}/api/analytics/usage-logs?days=7&limit=50`, { headers }),
        fetch(`${backendUrl}/api/analytics/application-stats?days=30`, { headers })
      ]);

      // Check for authentication errors
      if (currentResponse.status === 401 || historyResponse.status === 401 || appResponse.status === 401) {
        setAuthError('Invalid password. Please try again.');
        handleLogout();
        setLoading(false);
        return;
      }

      const currentData = await currentResponse.json();
      const historyData = await historyResponse.json();
      const appData = await appResponse.json();
      
      if (currentData.success) {
        setCurrentStats(currentData.data);
      }
      
      if (historyData.success) {
        setHistoricalStats(historyData.data);
      }

      if (appData.success) {
        setApplicationStats(appData.data);
      }
      
      setLoading(false);
    } catch (err) {
      setError('Failed to load analytics data');
      setLoading(false);
    }
  };

  const handleExportToExcel = async () => {
    try {
      const headers = {
        'X-Analytics-Password': password
      };

      const backendUrl = 'https://graceful-exploration-staging.up.railway.app';
      const response = await fetch(`${backendUrl}/api/analytics/export-applications?days=30`, {
        headers
      });

      if (response.status === 401) {
        setAuthError('Invalid password. Please try again.');
        handleLogout();
        return;
      }

      if (!response.ok) {
        throw new Error('Export failed');
      }

      // Get the filename from Content-Disposition header or use default
      const contentDisposition = response.headers.get('Content-Disposition');
      let filename = 'applications_export.xlsx';
      if (contentDisposition) {
        const filenameMatch = contentDisposition.match(/filename="?([^"]+)"?/);
        if (filenameMatch) {
          filename = filenameMatch[1];
        }
      }

      // Convert response to blob and download
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (err) {
      setError('Failed to export data to Excel');
    }
  };

  // Login screen
  if (!isAuthenticated) {
    return (
      <Layout navigationVariant="solid">
        <div className="min-h-screen bg-gray-50 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
          <div className="max-w-md w-full space-y-8">
            <div>
              <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
                Analytics Dashboard
              </h2>
              <p className="mt-2 text-center text-sm text-gray-600">
                Enter password to access analytics
              </p>
            </div>
            <div className="mt-8 space-y-6">
              <div className="rounded-md shadow-sm -space-y-px">
                <div>
                  <label htmlFor="password" className="sr-only">
                    Password
                  </label>
                  <input
                    id="password"
                    name="password"
                    type="password"
                    autoComplete="current-password"
                    required
                    className="appearance-none rounded-lg relative block w-full px-3 py-3 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm"
                    placeholder="Enter analytics password"
                    value={passwordInput}
                    onChange={(e) => setPasswordInput(e.target.value)}
                    onKeyDown={(e) => {
                      if (e.key === 'Enter') {
                        handleLogin();
                      }
                    }}
                  />
                </div>
              </div>

              {authError && (
                <div className="rounded-md bg-red-50 p-4">
                  <div className="flex">
                    <div className="ml-3">
                      <h3 className="text-sm font-medium text-red-800">{authError}</h3>
                    </div>
                  </div>
                </div>
              )}

              <div>
                <button
                  onClick={handleLogin}
                  className="group relative w-full flex justify-center py-3 px-4 border border-transparent text-sm font-medium rounded-lg text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                >
                  Access Dashboard
                </button>
              </div>
            </div>
          </div>
        </div>
      </Layout>
    );
  }

  if (loading && !currentStats && !applicationStats) {
    return (
      <Layout navigationVariant="solid">
        <div className="min-h-screen bg-gray-50 flex items-center justify-center">
          <div className="text-center">
            <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <p className="text-gray-600">Loading analytics...</p>
          </div>
        </div>
      </Layout>
    );
  }

  if (error) {
    return (
      <Layout navigationVariant="solid">
        <div className="min-h-screen bg-gray-50 flex items-center justify-center">
          <div className="text-center">
            <p className="text-red-600 text-lg">{error}</p>
            <button
              onClick={fetchAllData}
              className="mt-4 bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700"
            >
              Retry
            </button>
          </div>
        </div>
      </Layout>
    );
  }

  return (
    <Layout navigationVariant="solid">
      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-7xl mx-auto px-6">
          {/* Header */}
          <div className="mb-8 flex justify-between items-center">
            <div>
              <h1 className="text-4xl font-bold text-gray-900 mb-2">Analytics Dashboard</h1>
              <p className="text-gray-600">Comprehensive usage and application statistics</p>
            </div>
            <button
              onClick={handleLogout}
              className="bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700 text-sm font-medium"
            >
              Logout
            </button>
          </div>

          {/* Application Analytics Section */}
          {applicationStats && (
            <div className="mb-8">
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-2xl font-bold text-gray-900">Application Analytics (Last 30 Days)</h2>
                <button
                  onClick={handleExportToExcel}
                  className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 text-sm font-medium flex items-center gap-2"
                >
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                  Export to Excel
                </button>
              </div>
              
              {/* Key Metrics */}
              <div className="grid md:grid-cols-4 gap-6 mb-6">
                <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
                  <div className="text-sm font-medium text-gray-500 mb-2">Total Applications</div>
                  <div className="text-3xl font-bold text-blue-600">{applicationStats.total_applications}</div>
                </div>
                
                <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
                  <div className="text-sm font-medium text-gray-500 mb-2">Unique Users</div>
                  <div className="text-3xl font-bold text-purple-600">{applicationStats.unique_users}</div>
                </div>
                
                <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
                  <div className="text-sm font-medium text-gray-500 mb-2">Avg Match Score</div>
                  <div className="text-3xl font-bold text-green-600">{applicationStats.avg_match_score}%</div>
                </div>
                
                <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
                  <div className="text-sm font-medium text-gray-500 mb-2">Avg ATS Score</div>
                  <div className="text-3xl font-bold text-orange-600">{applicationStats.avg_ats_score}%</div>
                </div>
              </div>

              {/* Score Distribution */}
              <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200 mb-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Match Score Distribution</h3>
                <div className="space-y-3">
                  {Object.entries(applicationStats.score_distribution).map(([range, count]) => (
                    <div key={range} className="flex items-center justify-between">
                      <span className="text-sm font-medium text-gray-700">{range}</span>
                      <div className="flex items-center gap-3 flex-1 ml-4">
                        <div className="w-full bg-gray-200 rounded-full h-3">
                          <div
                            className="bg-gradient-to-r from-blue-500 to-blue-600 h-3 rounded-full"
                            style={{
                              width: `${applicationStats.total_applications > 0 ? (count / applicationStats.total_applications) * 100 : 0}%`
                            }}
                          ></div>
                        </div>
                        <span className="text-sm font-semibold text-gray-900 w-12 text-right">{count}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Top Missing Skills */}
              {applicationStats.top_missing_skills.length > 0 && (
                <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200 mb-6">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">Most Common Missing Skills</h3>
                  <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                    {applicationStats.top_missing_skills.slice(0, 12).map(({ skill, count }) => (
                      <div key={skill} className="flex items-center justify-between bg-red-50 rounded-lg p-3">
                        <span className="text-sm font-medium text-gray-900 capitalize">{skill}</span>
                        <span className="text-xs font-bold text-red-600 bg-white px-2 py-1 rounded-full">{count}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Top Companies and Job Titles */}
              <div className="grid md:grid-cols-2 gap-6 mb-6">
                {applicationStats.top_companies.length > 0 && (
                  <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
                    <h3 className="text-lg font-semibold text-gray-900 mb-4">Top Companies</h3>
                    <div className="space-y-2">
                      {applicationStats.top_companies.slice(0, 5).map(({ company, count }, index) => (
                        <div key={company} className="flex items-center justify-between">
                          <div className="flex items-center gap-3">
                            <span className="text-sm font-medium text-gray-500">#{index + 1}</span>
                            <span className="text-sm text-gray-900">{company}</span>
                          </div>
                          <span className="text-sm font-semibold text-blue-600">{count}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {applicationStats.top_job_titles.length > 0 && (
                  <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
                    <h3 className="text-lg font-semibold text-gray-900 mb-4">Top Job Titles</h3>
                    <div className="space-y-2">
                      {applicationStats.top_job_titles.slice(0, 5).map(({ title, count }, index) => (
                        <div key={title} className="flex items-center justify-between">
                          <div className="flex items-center gap-3">
                            <span className="text-sm font-medium text-gray-500">#{index + 1}</span>
                            <span className="text-sm text-gray-900">{title}</span>
                          </div>
                          <span className="text-sm font-semibold text-blue-600">{count}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>

              {/* Daily Trend */}
              {applicationStats.daily_trend.length > 0 && (
                <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">Daily Analysis Trend</h3>
                  <div className="space-y-2">
                    {applicationStats.daily_trend.slice(-14).map(({ date, count }) => (
                      <div key={date} className="flex items-center justify-between">
                        <span className="text-sm text-gray-700">{new Date(date).toLocaleDateString()}</span>
                        <div className="flex items-center gap-3 flex-1 ml-4 max-w-md">
                          <div className="w-full bg-gray-200 rounded-full h-2">
                            <div
                              className="bg-blue-600 h-2 rounded-full"
                              style={{
                                width: `${Math.max(10, (count / Math.max(...applicationStats.daily_trend.map(d => d.count))) * 100)}%`
                              }}
                            ></div>
                          </div>
                          <span className="text-sm font-semibold text-gray-900 w-8 text-right">{count}</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}

          {/* API Usage Section */}
          {currentStats && (
            <div className="mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">API Usage (Today)</h2>
              <div className="grid md:grid-cols-4 gap-6">
                <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
                  <div className="text-sm font-medium text-gray-500 mb-2">Total Requests</div>
                  <div className="text-3xl font-bold text-gray-900">{currentStats.total_requests}</div>
                </div>
                
                <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
                  <div className="text-sm font-medium text-gray-500 mb-2">Unique IPs</div>
                  <div className="text-3xl font-bold text-blue-600">{currentStats.unique_ips}</div>
                </div>
                
                <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
                  <div className="text-sm font-medium text-gray-500 mb-2">At Limit</div>
                  <div className="text-3xl font-bold text-orange-600">{currentStats.ips_at_limit}</div>
                </div>
                
                <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
                  <div className="text-sm font-medium text-gray-500 mb-2">Daily Limit</div>
                  <div className="text-3xl font-bold text-gray-900">{currentStats.daily_limit}</div>
                  <div className="text-xs text-gray-500 mt-1">per IP</div>
                </div>
              </div>
            </div>
          )}

          {/* Historical API Stats */}
          {historicalStats && (
            <div className="mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">API Usage (Last 7 Days)</h2>
              <div className="grid md:grid-cols-3 gap-6 mb-6">
                <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
                  <div className="text-sm font-medium text-gray-500 mb-2">Total Requests</div>
                  <div className="text-3xl font-bold text-gray-900">{historicalStats.total_requests}</div>
                </div>
                
                <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
                  <div className="text-sm font-medium text-gray-500 mb-2">Rate Limited</div>
                  <div className="text-3xl font-bold text-red-600">{historicalStats.rate_limited_requests}</div>
                  <div className="text-xs text-gray-500 mt-1">
                    {historicalStats.total_requests > 0
                      ? ((historicalStats.rate_limited_requests / historicalStats.total_requests) * 100).toFixed(1)
                      : 0}% of total
                  </div>
                </div>
                
                <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
                  <div className="text-sm font-medium text-gray-500 mb-2">Unique IPs</div>
                  <div className="text-3xl font-bold text-blue-600">{historicalStats.unique_ips}</div>
                </div>
              </div>

              {/* Endpoint Distribution */}
              {historicalStats.endpoint_distribution.length > 0 && (
                <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">Endpoint Usage</h3>
                  <div className="space-y-3">
                    {historicalStats.endpoint_distribution.map(({ endpoint, count }) => (
                      <div key={endpoint} className="flex items-center justify-between">
                        <span className="font-mono text-sm text-gray-700">{endpoint}</span>
                        <div className="flex items-center gap-3">
                          <div className="w-32 bg-gray-200 rounded-full h-2">
                            <div
                              className="bg-blue-600 h-2 rounded-full"
                              style={{
                                width: `${(count / historicalStats.total_requests) * 100}%`
                              }}
                            ></div>
                          </div>
                          <span className="text-sm font-semibold text-gray-900 w-16 text-right">{count}</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </Layout>
  );
}
