import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Layout from '../components/Layout';
import api from '../services/api';
import type { Application } from '../services/api';

export default function ApplicationsPage() {
  const navigate = useNavigate();
  
  const [applications, setApplications] = useState<Application[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [skip, setSkip] = useState(0);
  const [limit] = useState(20);
  const [total, setTotal] = useState(0);
  const [selectedIds, setSelectedIds] = useState<Set<number>>(new Set());
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
  const [deleteTarget, setDeleteTarget] = useState<'selected' | number | null>(null);
  const [deleting, setDeleting] = useState(false);

  useEffect(() => {
    loadApplications();
  }, [skip]);

  const loadApplications = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await api.getApplications(undefined, skip, limit);
      setApplications(response.applications);
      setTotal(response.total);
      setSelectedIds(new Set()); // Clear selection when loading new page
    } catch (err) {
      console.error('Error loading applications:', err);
      setError(err instanceof Error ? err.message : 'Failed to load applications');
    } finally {
      setLoading(false);
    }
  };

  const handleSelectAll = (checked: boolean) => {
    if (checked) {
      setSelectedIds(new Set(applications.map(app => app.application_id)));
    } else {
      setSelectedIds(new Set());
    }
  };

  const handleSelectOne = (id: number, checked: boolean) => {
    const newSelected = new Set(selectedIds);
    if (checked) {
      newSelected.add(id);
    } else {
      newSelected.delete(id);
    }
    setSelectedIds(newSelected);
  };

  const handleDeleteClick = (target: 'selected' | number) => {
    setDeleteTarget(target);
    setShowDeleteConfirm(true);
  };

  const handleConfirmDelete = async () => {
    try {
      setDeleting(true);
      
      if (deleteTarget === 'selected') {
        await api.deleteApplicationsBulk(Array.from(selectedIds));
      } else if (typeof deleteTarget === 'number') {
        await api.deleteApplication(deleteTarget);
      }
      
      setShowDeleteConfirm(false);
      setDeleteTarget(null);
      setSelectedIds(new Set());
      await loadApplications(); // Reload the list
    } catch (err) {
      console.error('Error deleting application(s):', err);
      alert('Failed to delete application(s). Please try again.');
    } finally {
      setDeleting(false);
    }
  };

  const handleViewDetails = (applicationId: number) => {
    navigate(`/applications/${applicationId}`);
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
      year: 'numeric', 
      month: 'short', 
      day: 'numeric' 
    });
  };

  const getStatusBadge = (status: string) => {
    const statusColors: Record<string, string> = {
      'analyzed': 'bg-green-100 text-green-800',
      'pending': 'bg-yellow-100 text-yellow-800',
      'applied': 'bg-blue-100 text-blue-800',
      'rejected': 'bg-red-100 text-red-800',
    };
    
    const colorClass = statusColors[status.toLowerCase()] || 'bg-gray-100 text-gray-800';
    
    return (
      <span className={`px-3 py-1 rounded-full text-xs font-medium ${colorClass}`}>
        {status.charAt(0).toUpperCase() + status.slice(1)}
      </span>
    );
  };

  const handlePreviousPage = () => {
    if (skip > 0) {
      setSkip(Math.max(0, skip - limit));
    }
  };

  const handleNextPage = () => {
    if (skip + limit < total) {
      setSkip(skip + limit);
    }
  };

  return (
    <Layout>
      <div className="min-h-screen bg-gray-50 py-12">
        <div className="container mx-auto px-4 max-w-6xl">
          {/* Header */}
          <div className="mb-8">
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-4xl font-bold text-gray-900 mb-2">
                  My Applications
                </h1>
                <p className="text-lg text-gray-600">
                  Track your resume analyses and job applications
                </p>
              </div>
              <div className="flex gap-3">
                {selectedIds.size > 0 && (
                  <button
                    onClick={() => handleDeleteClick('selected')}
                    className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors flex items-center gap-2"
                  >
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                    Delete Selected ({selectedIds.size})
                  </button>
                )}
                <button
                  onClick={() => navigate('/upload')}
                  className="btn-primary"
                >
                  + New Analysis
                </button>
              </div>
            </div>
          </div>

        {/* Loading State */}
        {loading && (
          <div className="flex justify-center items-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
          </div>
        )}

        {/* Error State */}
        {error && !loading && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-6 mb-8">
            <div className="flex items-start">
              <svg className="w-6 h-6 text-red-600 mr-3 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <div>
                <h3 className="text-red-800 font-semibold mb-1">Error Loading Applications</h3>
                <p className="text-red-700 text-sm">{error}</p>
              </div>
            </div>
          </div>
        )}

        {/* Applications List */}
        {!loading && !error && applications.length === 0 && (
          <div className="text-center py-12">
            <svg className="mx-auto h-16 w-16 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">No Applications Yet</h3>
            <p className="text-gray-600 mb-6">
              Start by uploading a resume and job description to create your first analysis.
            </p>
            <button
              onClick={() => navigate('/upload')}
              className="btn-primary"
            >
              Get Started
            </button>
          </div>
        )}

        {!loading && !error && applications.length > 0 && (
          <>
            {/* Applications Table */}
            <div className="bg-white rounded-lg shadow-sm overflow-hidden mb-6">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left">
                      <input
                        type="checkbox"
                        checked={selectedIds.size === applications.length && applications.length > 0}
                        onChange={(e) => handleSelectAll(e.target.checked)}
                        className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                      />
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Job Title / Company
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Resume
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Date
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Status
                    </th>
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Actions
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {applications.map((app) => (
                    <tr 
                      key={app.application_id} 
                      className="hover:bg-gray-50 transition-colors"
                    >
                      <td className="px-6 py-4" onClick={(e) => e.stopPropagation()}>
                        <input
                          type="checkbox"
                          checked={selectedIds.has(app.application_id)}
                          onChange={(e) => handleSelectOne(app.application_id, e.target.checked)}
                          className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                        />
                      </td>
                      <td 
                        className="px-6 py-4 cursor-pointer"
                        onClick={() => handleViewDetails(app.application_id)}
                      >
                        <div className="flex flex-col">
                          <span className="text-sm font-medium text-gray-900">
                            {app.jd_title || 'Untitled Job'}
                          </span>
                          <span className="text-sm text-gray-500">
                            {app.jd_company || 'Unknown Company'}
                          </span>
                        </div>
                      </td>
                      <td 
                        className="px-6 py-4 text-sm text-gray-900 cursor-pointer"
                        onClick={() => handleViewDetails(app.application_id)}
                      >
                        {app.resume_filename}
                      </td>
                      <td 
                        className="px-6 py-4 text-sm text-gray-500 cursor-pointer"
                        onClick={() => handleViewDetails(app.application_id)}
                      >
                        {formatDate(app.applied_at)}
                      </td>
                      <td 
                        className="px-6 py-4 cursor-pointer"
                        onClick={() => handleViewDetails(app.application_id)}
                      >
                        {getStatusBadge(app.status)}
                      </td>
                      <td className="px-6 py-4 text-right text-sm font-medium">
                        <div className="flex items-center justify-end gap-3">
                          <button
                            onClick={(e) => {
                              e.stopPropagation();
                              handleViewDetails(app.application_id);
                            }}
                            className="text-primary-600 hover:text-primary-900"
                          >
                            View Details →
                          </button>
                          <button
                            onClick={(e) => {
                              e.stopPropagation();
                              handleDeleteClick(app.application_id);
                            }}
                            className="text-red-600 hover:text-red-900"
                            title="Delete"
                          >
                            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                            </svg>
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {/* Pagination */}
            {total > limit && (
              <div className="flex items-center justify-between bg-white px-6 py-4 rounded-lg shadow-sm">
                <div className="text-sm text-gray-700">
                  Showing <span className="font-medium">{skip + 1}</span> to{' '}
                  <span className="font-medium">{Math.min(skip + limit, total)}</span> of{' '}
                  <span className="font-medium">{total}</span> applications
                </div>
                <div className="flex gap-2">
                  <button
                    onClick={handlePreviousPage}
                    disabled={skip === 0}
                    className="px-4 py-2 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                  >
                    Previous
                  </button>
                  <button
                    onClick={handleNextPage}
                    disabled={skip + limit >= total}
                    className="px-4 py-2 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                  >
                    Next
                  </button>
                </div>
              </div>
            )}
          </>
        )}
      </div>
    </div>

    {/* Delete Confirmation Modal */}
    {showDeleteConfirm && (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
        <div className="bg-white rounded-xl shadow-2xl max-w-md w-full p-6">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-12 h-12 bg-red-100 rounded-full flex items-center justify-center flex-shrink-0">
              <svg className="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
            </div>
            <div>
              <h3 className="text-xl font-bold text-gray-900">Confirm Delete</h3>
              <p className="text-sm text-gray-600">
                {deleteTarget === 'selected' 
                  ? `Delete ${selectedIds.size} selected application(s)?`
                  : 'Delete this application?'}
              </p>
            </div>
          </div>
          
          <p className="text-gray-700 mb-6">
            This action cannot be undone. All associated data including gap analysis and ATS scores will be permanently deleted.
          </p>
          
          <div className="flex gap-3 justify-end">
            <button
              onClick={() => {
                setShowDeleteConfirm(false);
                setDeleteTarget(null);
              }}
              disabled={deleting}
              className="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors disabled:opacity-50"
            >
              Cancel
            </button>
            <button
              onClick={handleConfirmDelete}
              disabled={deleting}
              className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors disabled:opacity-50 flex items-center gap-2"
            >
              {deleting ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                  Deleting...
                </>
              ) : (
                'Delete'
              )}
            </button>
          </div>
        </div>
      </div>
    )}
    </Layout>
  );
}
