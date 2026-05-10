import { Link } from 'react-router-dom';
import Layout from '../components/Layout';
import { useState } from 'react';

export default function LandingPage() {
  const [, setResumeFile] = useState<File | null>(null);
  const [jobDescription, setJobDescription] = useState('');

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setResumeFile(e.target.files[0]);
    }
  };

  return (
    <Layout navigationVariant="solid">
      <div className="min-h-screen bg-white">
        
        {/* HERO SECTION */}
        <section className="py-2 px-6 max-w-7xl mx-auto">
          <div className="grid md:grid-cols-2 gap-12 items-center">
            {/* Left: Text Content */}
            <div>
              <h1 className="text-5xl md:text-6xl font-bold leading-tight text-gray-900">
                Get More<br />
                <span className="text-blue-600">Interview Calls</span>
              </h1>

              <p className="mt-6 text-lg text-gray-600 leading-relaxed">
                Your resume is being rejected by ATS before a recruiter even sees it.<br />
                We analyze your resume against job descriptions to improve ATS compatibility and recruiter visibility.
              </p>

              <div className="mt-8 flex flex-col sm:flex-row gap-4">
                <Link
                  to="/upload"
                  className="bg-blue-600 text-white px-8 py-4 rounded-xl font-semibold text-lg hover:bg-blue-700 transition-colors shadow-lg inline-flex items-center justify-center"
                >
                  Check My ATS Score (Free) →
                </Link>

                <Link
                  to="/upload"
                  className="border-2 border-gray-300 text-gray-700 px-8 py-4 rounded-xl font-semibold text-lg hover:border-gray-400 hover:bg-gray-50 transition-colors inline-flex items-center justify-center"
                >
                  Upload Resume & JD
                </Link>
              </div>

              {/* Trust Badges */}
              <div className="mt-8 flex flex-wrap gap-6 text-sm text-gray-600">
                <div className="flex items-center gap-2">
                  <span className="text-green-600 text-xl">✓</span>
                  <span>Free ATS Score</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-green-600 text-xl">✓</span>
                  <span>Instant Results</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-green-600 text-xl">✓</span>
                  <span>No Credit Card Required</span>
                </div>
              </div>
            </div>

            {/* Right: Illustration */}
            <div className="relative">
              <div className="bg-gradient-to-br from-blue-50 to-purple-50 rounded-3xl p-8 shadow-xl">
                {/* Mock Resume Card */}
                <div className="bg-white rounded-2xl p-6 shadow-lg">
                  <div className="flex items-start gap-4 mb-6">
                    <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center">
                      <svg className="w-10 h-10 text-blue-600" fill="currentColor" viewBox="0 0 24 24">
                        <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
                      </svg>
                    </div>
                    <div className="flex-1">
                      <div className="h-3 bg-gray-200 rounded w-3/4 mb-2"></div>
                      <div className="h-3 bg-gray-200 rounded w-1/2"></div>
                    </div>
                  </div>

                  <div className="space-y-4 mb-6">
                    <div>
                      <div className="text-xs font-semibold text-gray-500 mb-2">SKILLS</div>
                      <div className="h-2 bg-gray-200 rounded w-full mb-1"></div>
                      <div className="h-2 bg-gray-200 rounded w-5/6"></div>
                    </div>
                    <div>
                      <div className="text-xs font-semibold text-gray-500 mb-2">EXPERIENCE</div>
                      <div className="h-2 bg-gray-200 rounded w-full mb-1"></div>
                      <div className="h-2 bg-gray-200 rounded w-4/5"></div>
                    </div>
                  </div>

                  {/* ATS Score Badge */}
                  <div className="absolute -right-4 top-1/2 transform -translate-y-1/2">
                    <div className="bg-white rounded-2xl p-6 shadow-2xl">
                      <div className="relative w-32 h-32">
                        <svg className="transform -rotate-90 w-32 h-32">
                          <circle cx="64" cy="64" r="56" stroke="#e5e7eb" strokeWidth="8" fill="none" />
                          <circle cx="64" cy="64" r="56" stroke="#22c55e" strokeWidth="8" fill="none" 
                            strokeDasharray="351.86" strokeDashoffset="70" strokeLinecap="round" />
                        </svg>
                        <div className="absolute inset-0 flex flex-col items-center justify-center">
                          <div className="text-3xl font-bold text-gray-900">85<span className="text-lg">/100</span></div>
                          <div className="text-xs text-gray-500 font-medium">Excellent</div>
                        </div>
                      </div>
                      <div className="text-xs font-semibold text-gray-700 mt-4 text-center">ATS SCORE</div>
                    </div>
                  </div>
                </div>

                {/* Match Quality Checklist */}
                <div className="mt-6 bg-white rounded-xl p-4 shadow-md">
                  <div className="text-sm font-semibold text-gray-700 mb-3">MATCH QUALITY</div>
                  <div className="space-y-2 text-sm">
                    <div className="flex items-center gap-2">
                      <span className="text-green-600">✓</span>
                      <span className="text-gray-700">Skills Match</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="text-green-600">✓</span>
                      <span className="text-gray-700">Keyword Match</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="text-green-600">✓</span>
                      <span className="text-gray-700">Content Quality</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="text-green-600">✓</span>
                      <span className="text-gray-700">Format Check</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* PROBLEM SECTION */}
        <section className="bg-gray-50 py-16 px-6">
          <div className="max-w-6xl mx-auto">
            <h2 className="text-4xl font-bold text-center text-gray-900 mb-12">
              Why You're Not Getting Interview Calls
            </h2>

            <div className="grid md:grid-cols-4 gap-6 mb-8">
              <div className="bg-white rounded-xl p-6 text-center shadow-sm hover:shadow-md transition-shadow">
                <div className="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <svg className="w-8 h-8 text-red-600" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                  </svg>
                </div>
                <h3 className="font-bold text-gray-900 mb-2">Same Resume</h3>
                <p className="text-sm text-gray-600">Using the same resume for every job.</p>
              </div>

              <div className="bg-white rounded-xl p-6 text-center shadow-sm hover:shadow-md transition-shadow">
                <div className="w-16 h-16 bg-orange-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <svg className="w-8 h-8 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                  </svg>
                </div>
                <h3 className="font-bold text-gray-900 mb-2">Missing Keywords</h3>
                <p className="text-sm text-gray-600">Missing critical keywords from job descriptions.</p>
              </div>

              <div className="bg-white rounded-xl p-6 text-center shadow-sm hover:shadow-md transition-shadow">
                <div className="w-16 h-16 bg-yellow-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <svg className="w-8 h-8 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                  </svg>
                </div>
                <h3 className="font-bold text-gray-900 mb-2">Weak Content</h3>
                <p className="text-sm text-gray-600">Weak achievement statements.</p>
              </div>

              <div className="bg-white rounded-xl p-6 text-center shadow-sm hover:shadow-md transition-shadow">
                <div className="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <svg className="w-8 h-8 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </div>
                <h3 className="font-bold text-gray-900 mb-2">ATS Rejection</h3>
                <p className="text-sm text-gray-600">ATS systems rejecting your resume silently.</p>
              </div>
            </div>

            <p className="text-center text-lg text-gray-600">
              Most resumes never reach a human recruiter.
            </p>
          </div>
        </section>

        {/* HOW IT WORKS */}
        <section id="how-it-works" className="py-16 px-6">
          <div className="max-w-6xl mx-auto">
            <h2 className="text-4xl font-bold text-center text-gray-900 mb-12">
              How Resume2Interview Works
            </h2>

            <div className="grid md:grid-cols-4 gap-8">
              <div className="text-center">
                <div className="w-20 h-20 bg-blue-100 rounded-2xl flex items-center justify-center mx-auto mb-4">
                  <svg className="w-10 h-10 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                  </svg>
                </div>
                <div className="w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center mx-auto mb-3 font-bold">1</div>
                <h3 className="font-bold text-gray-900 mb-2">Upload</h3>
                <p className="text-sm text-gray-600">Upload your resume (PDF / DOCX)</p>
              </div>

              <div className="text-center">
                <div className="w-20 h-20 bg-blue-100 rounded-2xl flex items-center justify-center mx-auto mb-4">
                  <svg className="w-10 h-10 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                </div>
                <div className="w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center mx-auto mb-3 font-bold">2</div>
                <h3 className="font-bold text-gray-900 mb-2">Paste Job Description</h3>
                <p className="text-sm text-gray-600">Paste the job description of the role you want.</p>
              </div>

              <div className="text-center">
                <div className="w-20 h-20 bg-blue-100 rounded-2xl flex items-center justify-center mx-auto mb-4">
                  <svg className="w-10 h-10 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <div className="w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center mx-auto mb-3 font-bold">3</div>
                <h3 className="font-bold text-gray-900 mb-2">Get ATS Score</h3>
                <p className="text-sm text-gray-600">Get instant ATS score and detailed analysis.</p>
              </div>

              <div className="text-center">
                <div className="w-20 h-20 bg-green-100 rounded-2xl flex items-center justify-center mx-auto mb-4">
                  <svg className="w-10 h-10 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <div className="w-8 h-8 bg-green-600 text-white rounded-full flex items-center justify-center mx-auto mb-3 font-bold">4</div>
                <h3 className="font-bold text-gray-900 mb-2">Get Resume Improvement Insights</h3>
                <p className="text-sm text-gray-600">Identify exactly what needs to change to improve your ATS match and recruiter visibility.</p>
              </div>
            </div>
          </div>
        </section>

        {/* WHAT YOU GET */}
        <section id="features" className="bg-gray-50 py-16 px-6">
          <div className="max-w-6xl mx-auto">
            <h2 className="text-4xl font-bold text-center text-gray-900 mb-12">
              What You Get
            </h2>

            <div className="grid md:grid-cols-3 gap-8">
              <div className="bg-white rounded-xl p-6 text-center shadow-sm hover:shadow-md transition-shadow">
                <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-3xl">85</span>
                </div>
                <h3 className="font-bold text-gray-900 mb-2">ATS Match Score</h3>
                <p className="text-sm text-gray-600">Score from 0-100 showing how well your job-fit and ATS match.</p>
              </div>

              <div className="bg-white rounded-xl p-6 text-center shadow-sm hover:shadow-md transition-shadow">
                <div className="w-16 h-16 bg-orange-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <svg className="w-8 h-8 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                  </svg>
                </div>
                <h3 className="font-bold text-gray-900 mb-2">Missing Keywords</h3>
                <p className="text-sm text-gray-600">See important keywords you're missing.</p>
              </div>

              <div className="bg-white rounded-xl p-6 text-center shadow-sm hover:shadow-md transition-shadow">
                <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <svg className="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                  </svg>
                </div>
                <h3 className="font-bold text-gray-900 mb-2">Resume Improvement Suggestions</h3>
                <p className="text-sm text-gray-600">Detailed recommendations to strengthen your resume for the target job description.</p>
              </div>

              <div className="bg-white rounded-xl p-6 text-center shadow-sm hover:shadow-md transition-shadow">
                <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <svg className="w-8 h-8 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                  </svg>
                </div>
                <h3 className="font-bold text-gray-900 mb-2">Better Bullet Points</h3>
                <p className="text-sm text-gray-600">Achievement-focused content that stands out to recruiters.</p>
              </div>

              <div className="bg-white rounded-xl p-6 text-center shadow-sm hover:shadow-md transition-shadow">
                <div className="w-16 h-16 bg-pink-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <svg className="w-8 h-8 text-pink-600" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
                  </svg>
                </div>
                <h3 className="font-bold text-gray-900 mb-2">Recruiter Feedback</h3>
                <p className="text-sm text-gray-600">Recruiter-style tips to improve clarity and impact.</p>
              </div>

              <div className="bg-white rounded-xl p-6 text-center shadow-sm hover:shadow-md transition-shadow">
                <div className="w-16 h-16 bg-indigo-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <svg className="w-8 h-8 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
                  </svg>
                </div>
                <h3 className="font-bold text-gray-900 mb-2">IT Focused</h3>
                <p className="text-sm text-gray-600">Built specifically for IT professionals and technical roles.</p>
              </div>
            </div>
          </div>
        </section>

        {/* BEFORE VS AFTER */}
        <section className="py-16 px-6">
          <div className="max-w-5xl mx-auto">
            <h2 className="text-4xl font-bold text-center text-gray-900 mb-12">
              Before vs After
            </h2>

            <div className="grid md:grid-cols-2 gap-8">
              <div className="bg-red-50 border-2 border-red-200 rounded-xl p-6">
                <div className="text-sm font-bold text-red-600 mb-4">BEFORE</div>
                <p className="text-gray-700">
                  Worked on automation testing using Selenium and created test scripts.
                </p>
              </div>

              <div className="bg-green-50 border-2 border-green-200 rounded-xl p-6">
                <div className="text-sm font-bold text-green-600 mb-4">AFTER</div>
                <p className="text-gray-700">
                  Built Selenium-based automation framework reducing regression effort by 60% and improving test coverage by 35%.
                </p>
              </div>
            </div>

            <p className="text-center text-gray-600 mt-8 text-lg">
              Same experience. Better positioning. More interview calls.
            </p>
          </div>
        </section>

        {/* ATS FREE TOOL */}
        <section className="bg-blue-50 py-16 px-6">
          <div className="max-w-4xl mx-auto">
            <h2 className="text-4xl font-bold text-center text-gray-900 mb-4">
              Get Your ATS Score — <span className="text-blue-600">Free</span>
            </h2>
            <p className="text-center text-gray-600 mb-12">
              Find out why your resume is not getting shortlisted.
            </p>

            <div className="bg-white rounded-2xl p-8 shadow-lg">
              <div className="grid md:grid-cols-2 gap-6 mb-6">
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    Upload Your Resume
                  </label>
                  <div className="border-2 border-dashed border-gray-300 rounded-xl p-8 text-center hover:border-blue-400 transition-colors cursor-pointer">
                    <input
                      type="file"
                      accept=".pdf,.docx"
                      onChange={handleFileChange}
                      className="hidden"
                      id="resume-upload"
                    />
                    <label htmlFor="resume-upload" className="cursor-pointer">
                      <svg className="w-12 h-12 text-gray-400 mx-auto mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                      </svg>
                      <p className="text-sm text-gray-600">
                        Click to upload or drag and drop<br />
                        <span className="text-xs text-gray-500">PDF or DOCX (Max 10MB)</span>
                      </p>
                    </label>
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    Paste Job Description
                  </label>
                  <textarea
                    value={jobDescription}
                    onChange={(e) => setJobDescription(e.target.value)}
                    placeholder="Paste the job description here..."
                    className="w-full h-full border-2 border-gray-300 rounded-xl p-4 text-sm resize-none focus:border-blue-400 focus:outline-none transition-colors"
                    rows={6}
                  />
                </div>
              </div>

              <Link
                to="/upload"
                className="w-full bg-blue-600 text-white py-4 rounded-xl font-bold text-lg hover:bg-blue-700 transition-colors flex items-center justify-center shadow-md"
              >
                Analyze My Resume →
              </Link>


            </div>
          </div>
        </section>

        {/* FREE LIMITED TIME */}
        <section id="pricing" className="py-16 px-6">
          <div className="max-w-5xl mx-auto">
            <h2 className="text-4xl font-bold text-center text-gray-900 mb-4">
              Free for a Limited Time
            </h2>
            <p className="text-center text-gray-600 mb-12 max-w-3xl mx-auto">
              We're offering Resume2Interview completely free while we refine the product with early users. 
              Get your ATS score and optimized resume at no cost.
            </p>

            <div className="bg-blue-50 border-2 border-blue-200 rounded-2xl p-8">
              <h3 className="text-2xl font-bold text-gray-900 mb-6 text-center">
                What You Get (Free Access)
              </h3>

              <div className="grid md:grid-cols-2 gap-4 mb-8">
                <div className="flex items-center gap-3">
                  <span className="text-green-600 text-xl">✅</span>
                  <span className="text-gray-700">ATS Match Score (0–100)</span>
                </div>
                <div className="flex items-center gap-3">
                  <span className="text-green-600 text-xl">✅</span>
                  <span className="text-gray-700">Achievement Rewrites</span>
                </div>
                <div className="flex items-center gap-3">
                  <span className="text-green-600 text-xl">✅</span>
                  <span className="text-gray-700">Missing Keywords Report</span>
                </div>
                <div className="flex items-center gap-3">
                  <span className="text-green-600 text-xl">✅</span>
                  <span className="text-gray-700">Recruiter Feedback</span>
                </div>
                <div className="flex items-center gap-3">
                  <span className="text-green-600 text-xl">✅</span>
                  <span className="text-gray-700">Resume Optimization</span>
                </div>
                <div className="flex items-center gap-3">
                  <span className="text-green-600 text-xl">✅</span>
                  <span className="text-gray-700">Job-Specific Tailoring</span>
                </div>
              </div>

              <div className="text-center">
                <Link
                  to="/upload"
                  className="inline-block bg-blue-600 text-white px-10 py-4 rounded-xl font-bold text-lg hover:bg-blue-700 transition-colors shadow-lg"
                >
                  Get Free ATS Analysis
                </Link>
                <p className="text-sm text-gray-500 mt-4">
                  ⚡ Limited-time early access. Pricing will be introduced soon.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* TRUST SECTION */}
        <section className="bg-gray-50 py-16 px-6">
          <div className="max-w-4xl mx-auto text-center">
            <div className="flex justify-center mb-6">
              <svg className="w-20 h-20 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
            </div>
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              Built by IT Professionals Who Understand Hiring
            </h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              We know how ATS systems work. We know what recruiters look for.
            </p>
          </div>
        </section>

        {/* FINAL CTA */}
        <section className="bg-blue-600 text-white py-16 px-6">
          <div className="max-w-4xl mx-auto text-center">
            <h2 className="text-4xl md:text-5xl font-bold mb-6">
              Stop Getting Rejected by ATS
            </h2>
            <p className="text-xl mb-8 opacity-90">
              Start getting interview calls.
            </p>
            <Link
              to="/upload"
              className="inline-block bg-white text-blue-600 px-10 py-4 rounded-xl font-bold text-lg hover:bg-gray-100 transition-colors shadow-lg"
            >
              Check Your ATS Score Now →
            </Link>
          </div>
        </section>

      </div>
    </Layout>
  );
}
