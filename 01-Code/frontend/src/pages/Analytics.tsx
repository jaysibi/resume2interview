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

export default function Analytics() {
  const [currentStats, setCurrentStats] = useState<UsageStats | null>(null);
  const [historicalStats, setHistoricalStats] = useState<HistoricalStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchUsageData();
    // Refresh every 30 seconds
    const interval = setInterval(fetchUsageData, 30000);
    return () => clearInterval(interval);
  }, []);

  const fetchUsageData = async () => {
    try {
      // Fetch current day stats from rate limiter
      const currentResponse = await fetch('/api/analytics/usage-stats');
      const currentData = await currentResponse.json();
      
      // Fetch historical stats from database
      const historyResponse = await fetch('/api/analytics/usage-logs?days=7&limit=50');
      const historyData = await historyResponse.json();
      
      if (currentData.success) {
        setCurrentStats(currentData.data);
      }
      
      if (historyData.success) {
        setHistoricalStats(historyData.data);
      }
      
      setLoading(false);
    } catch (err) {
      setError('Failed to load analytics data');
      setLoading(false);
    }
  };

  if (loading) {
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
              onClick={fetchUsageData}
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
          <div className="mb-8">
            <h1 className="text-4xl font-bold text-gray-900 mb-2">Usage Analytics</h1>
            <p className="text-gray-600">Real-time and historical usage statistics</p>
          </div>

          {/* Current Day Stats */}
          {currentStats && (
            <div className="mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">Today's Activity</h2>
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

              {/* Top IPs Today */}
              {currentStats.top_ips.length > 0 && (
                <div className="mt-6 bg-white rounded-xl p-6 shadow-sm border border-gray-200">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">Top IPs Today</h3>
                  <div className="space-y-3">
                    {currentStats.top_ips.slice(0, 5).map(([ip, count], index) => (
                      <div key={ip} className="flex items-center justify-between">
                        <div className="flex items-center gap-3">
                          <span className="text-sm font-medium text-gray-500">#{index + 1}</span>
                          <span className="font-mono text-sm text-gray-900">{ip}</span>
                        </div>
                        <span className="text-sm font-semibold text-blue-600">{count} requests</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Historical Stats */}
          {historicalStats && (
            <div className="mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">Last 7 Days</h2>
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
                  <div className="text-sm font-medium text-gray-500 mb-2">Unique Users</div>
                  <div className="text-3xl font-bold text-blue-600">{historicalStats.unique_ips}</div>
                </div>
              </div>

              {/* Endpoint Distribution */}
              {historicalStats.endpoint_distribution.length > 0 && (
                <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200 mb-6">
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

              {/* Recent Activity Log */}
              {historicalStats.recent_logs.length > 0 && (
                <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Activity</h3>
                  <div className="overflow-x-auto">
                    <table className="w-full text-sm">
                      <thead className="bg-gray-50 border-b border-gray-200">
                        <tr>
                          <th className="text-left py-3 px-4 font-semibold text-gray-700">Time</th>
                          <th className="text-left py-3 px-4 font-semibold text-gray-700">IP Address</th>
                          <th className="text-left py-3 px-4 font-semibold text-gray-700">Endpoint</th>
                          <th className="text-center py-3 px-4 font-semibold text-gray-700">Status</th>
                          <th className="text-center py-3 px-4 font-semibold text-gray-700">Rate Limited</th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-gray-200">
                        {historicalStats.recent_logs.slice(0, 20).map((log) => (
                          <tr key={log.id} className="hover:bg-gray-50">
                            <td className="py-3 px-4 text-gray-600">
                              {new Date(log.created_at).toLocaleString()}
                            </td>
                            <td className="py-3 px-4 font-mono text-gray-900">{log.ip_address}</td>
                            <td className="py-3 px-4 font-mono text-gray-700">{log.endpoint}</td>
                            <td className="py-3 px-4 text-center">
                              <span className={`inline-flex px-2 py-1 rounded-full text-xs font-semibold ${
                                log.status_code < 400
                                  ? 'bg-green-100 text-green-800'
                                  : log.status_code === 429
                                  ? 'bg-orange-100 text-orange-800'
                                  : 'bg-red-100 text-red-800'
                              }`}>
                                {log.status_code}
                              </span>
                            </td>
                            <td className="py-3 px-4 text-center">
                              {log.rate_limited ? (
                                <span className="text-red-600">✕</span>
                              ) : (
                                <span className="text-green-600">✓</span>
                              )}
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
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
