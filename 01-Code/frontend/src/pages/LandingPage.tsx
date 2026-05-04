import { Link } from 'react-router-dom';
import Layout from '../components/Layout';

export default function LandingPage() {
  return (
    <Layout navigationVariant="transparent">
      <div className="min-h-screen bg-gradient-to-br from-primary-50 via-white to-purple-50">
        {/* Hero Section */}
        <div className="container mx-auto px-4 py-24">
          <div className="max-w-5xl mx-auto text-center">
            {/* Main Headline - Larger, Bolder */}
            <h1 className="text-6xl md:text-7xl font-bold text-gray-900 mb-6 leading-tight">
              Beat the Bots.<br />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary-600 to-purple-600">
                Land Interviews.
              </span>
            </h1>
            
            {/* Enhanced Tagline */}
            <p className="text-xl md:text-2xl text-gray-600 mb-12 max-w-3xl mx-auto leading-relaxed">
              AI-powered resume analysis that shows exactly what hiring managers 
              and ATS systems want to see—in seconds.
            </p>

            {/* CTA Buttons - Enhanced with shadow */}
            <div className="flex flex-col sm:flex-row gap-6 justify-center mb-16">
              <Link
                to="/upload"
                className="btn-primary text-lg px-10 py-4 shadow-lg hover:shadow-xl transform hover:-translate-y-1 transition-all"
              >
                Get Started Free →
              </Link>
              <a
                href="#features"
                className="btn-secondary text-lg px-10 py-4 shadow-md hover:shadow-lg transition-all"
              >
                See How It Works
              </a>
            </div>

            {/* Key Benefits - Icon-based */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-16 max-w-4xl mx-auto">
              <div className="flex flex-col items-center text-center">
                <div className="w-14 h-14 bg-gradient-to-br from-green-400 to-green-600 rounded-2xl flex items-center justify-center mb-4 shadow-lg">
                  <span className="text-3xl">🎯</span>
                </div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Instant ATS Score</h3>
                <p className="text-sm text-gray-600">Know if your resume will pass screening</p>
              </div>
              
              <div className="flex flex-col items-center text-center">
                <div className="w-14 h-14 bg-gradient-to-br from-blue-400 to-blue-600 rounded-2xl flex items-center justify-center mb-4 shadow-lg">
                  <span className="text-3xl">📊</span>
                </div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Gap Analysis</h3>
                <p className="text-sm text-gray-600">See missing skills recruiters look for</p>
              </div>
              
              <div className="flex flex-col items-center text-center">
                <div className="w-14 h-14 bg-gradient-to-br from-purple-400 to-purple-600 rounded-2xl flex items-center justify-center mb-4 shadow-lg">
                  <span className="text-3xl">✨</span>
                </div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Smart Recommendations</h3>
                <p className="text-sm text-gray-600">Get actionable advice to improve</p>
              </div>
            </div>

            {/* Stats - More prominent */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-3xl mx-auto">
              <div className="bg-white/60 backdrop-blur-sm rounded-2xl p-6 text-center shadow-md hover:shadow-lg transition-shadow">
                <div className="text-5xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-primary-600 to-purple-600 mb-2">2.6K+</div>
                <div className="text-gray-700 font-medium">Resumes Optimized</div>
              </div>
              <div className="bg-white/60 backdrop-blur-sm rounded-2xl p-6 text-center shadow-md hover:shadow-lg transition-shadow">
                <div className="text-5xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-green-600 to-emerald-600 mb-2">95%</div>
                <div className="text-gray-700 font-medium">Match Accuracy</div>
              </div>
              <div className="bg-white/60 backdrop-blur-sm rounded-2xl p-6 text-center shadow-md hover:shadow-lg transition-shadow">
                <div className="text-5xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-orange-600 to-red-600 mb-2">&lt;30s</div>
                <div className="text-gray-700 font-medium">Analysis Time</div>
              </div>
            </div>
          </div>
        </div>

        {/* Features Section */}
        <div id="features" className="container mx-auto px-4 py-20">
          <div className="max-w-6xl mx-auto">
            <h2 className="text-4xl md:text-5xl font-bold text-center text-gray-900 mb-4">
              How It Works
            </h2>
            <p className="text-xl text-gray-600 text-center mb-16 max-w-2xl mx-auto">
              Three simple steps to optimize your resume and land more interviews
            </p>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-10">
              {/* Feature 1 */}
              <div className="card hover:shadow-xl transition-all transform hover:-translate-y-2 text-center">
                <div className="w-20 h-20 bg-gradient-to-br from-primary-400 to-primary-600 rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-lg">
                  <svg className="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                  </svg>
                </div>
                <h3 className="text-2xl font-bold text-gray-900 mb-3">
                  1. Upload Your Resume
                </h3>
                <p className="text-gray-600 text-lg leading-relaxed">
                  Upload your resume in PDF or DOCX format. Our AI will instantly parse your skills and experience.
                </p>
              </div>

              {/* Feature 2 */}
              <div className="card hover:shadow-xl transition-all transform hover:-translate-y-2 text-center">
                <div className="w-20 h-20 bg-gradient-to-br from-green-400 to-green-600 rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-lg">
                  <svg className="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                </div>
                <h3 className="text-2xl font-bold text-gray-900 mb-3">
                  2. Add Job Description
                </h3>
                <p className="text-gray-600 text-lg leading-relaxed">
                  Paste or upload the job description you're targeting for precise skill matching.
                </p>
              </div>

              {/* Feature 3 */}
              <div className="card hover:shadow-xl transition-all transform hover:-translate-y-2 text-center">
                <div className="w-20 h-20 bg-gradient-to-br from-purple-400 to-purple-600 rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-lg">
                  <svg className="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                  </svg>
                </div>
                <h3 className="text-2xl font-bold text-gray-900 mb-3">
                  3. Get Insights
                </h3>
                <p className="text-gray-600 text-lg leading-relaxed">
                  Receive your ATS score, detailed gap analysis, and actionable recommendations instantly.
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Final CTA */}
        <div className="container mx-auto px-4 py-20">
          <div className="max-w-4xl mx-auto">
            <div className="relative overflow-hidden rounded-3xl bg-gradient-to-r from-primary-600 via-purple-600 to-pink-600 p-12 text-center shadow-2xl">
              {/* Decorative elements */}
              <div className="absolute top-0 right-0 -mt-4 -mr-4 h-32 w-32 rounded-full bg-white opacity-10"></div>
              <div className="absolute bottom-0 left-0 -mb-8 -ml-8 h-40 w-40 rounded-full bg-white opacity-10"></div>
              
              <div className="relative z-10">
                <h2 className="text-4xl md:text-5xl font-bold mb-6 text-white">
                  Ready to Land Your Dream Job?
                </h2>
                <p className="text-xl mb-10 text-white/90 max-w-2xl mx-auto leading-relaxed">
                  Join thousands of professionals who've optimized their resumes and landed more interviews.
                </p>
                <Link
                  to="/upload"
                  className="inline-block px-10 py-5 bg-white text-primary-600 font-bold text-lg rounded-xl hover:bg-gray-50 transform hover:scale-105 transition-all shadow-xl hover:shadow-2xl"
                >
                  Analyze Your Resume Now — It's Free
                </Link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
}
