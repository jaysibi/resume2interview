import { Link } from 'react-router-dom';
import Layout from '../components/Layout';
import SEO from '../components/SEO';

export default function Features() {
  return (
    <Layout navigationVariant="solid">
      <SEO 
        title="Resume Tailoring Features - AI-Powered ATS Optimization Tools"
        description="Discover our AI resume optimization features: instant ATS compatibility score, keyword gap analysis, job description matching, and personalized improvement recommendations."
        keywords="resume tailoring features, ATS optimization tools, resume keyword matching, job description analyzer, AI resume recommendations, resume scoring"
        canonicalUrl="https://resume2interview.com/features"
      />
      <div className="min-h-screen bg-white">
        
        {/* Hero */}
        <section className="max-w-6xl mx-auto py-20 px-6 text-center">
          <h1 className="text-5xl font-bold leading-tight text-gray-900">
            Features Designed to Get You Interview Calls
          </h1>

          <p className="mt-6 text-xl text-gray-600 max-w-3xl mx-auto">
            Resume2Interview helps your resume pass ATS filters and align with what recruiters are actively searching for.
          </p>
        </section>

        {/* Features */}
        <section className="max-w-5xl mx-auto px-6 pb-20 space-y-16">

          <div className="border rounded-2xl p-8 shadow-sm">
            <h2 className="text-3xl font-semibold text-gray-900">ATS Match Score</h2>
            <p className="mt-4 text-gray-600 text-lg">
              Get a clear score showing how well your resume matches a specific job description.
            </p>

            <ul className="mt-6 space-y-3 list-disc ml-6 text-gray-700 text-lg">
              <li>Keyword match analysis</li>
              <li>Skill alignment scoring</li>
              <li>Section-level evaluation</li>
              <li>Role-specific optimization insights</li>
            </ul>
          </div>

          <div className="border rounded-2xl p-8 shadow-sm">
            <h2 className="text-3xl font-semibold text-gray-900">Missing Keywords Detection</h2>
            <p className="mt-4 text-gray-600 text-lg">
              Identify critical ATS and recruiter keywords missing from your resume.
            </p>

            <ul className="mt-6 space-y-3 list-disc ml-6 text-gray-700 text-lg">
              <li>ATS-relevant keyword extraction</li>
              <li>Recruiter search terminology</li>
              <li>Technical skills gap analysis</li>
              <li>Keyword prioritization</li>
            </ul>
          </div>

          <div className="border rounded-2xl p-8 shadow-sm">
            <h2 className="text-3xl font-semibold text-gray-900">AI Resume Optimization</h2>
            <p className="mt-4 text-gray-600 text-lg">
              We optimize your resume strategically - not just grammatically.
            </p>

            <ul className="mt-6 space-y-3 list-disc ml-6 text-gray-700 text-lg">
              <li>Achievement-focused bullet rewrites</li>
              <li>Improved recruiter readability</li>
              <li>Action-oriented phrasing</li>
              <li>Professional summary optimization</li>
            </ul>
          </div>

          <div className="border rounded-2xl p-8 shadow-sm">
            <h2 className="text-3xl font-semibold text-gray-900">Job-Specific Resume Versions</h2>
            <p className="mt-4 text-gray-600 text-lg">
              Different jobs require different positioning. Resume2Interview helps customize resumes for each role.
            </p>

            <ul className="mt-6 space-y-3 list-disc ml-6 text-gray-700 text-lg">
              <li>Customized summaries</li>
              <li>Reordered experience sections</li>
              <li>Role-specific emphasis</li>
              <li>Targeted resume tailoring</li>
            </ul>
          </div>

          <div className="border rounded-2xl p-8 shadow-sm">
            <h2 className="text-3xl font-semibold text-gray-900">Recruiter Perspective Analysis</h2>
            <p className="mt-4 text-gray-600 text-lg">
              Understand how recruiters and hiring managers evaluate your resume.
            </p>

            <ul className="mt-6 space-y-3 list-disc ml-6 text-gray-700 text-lg">
              <li>Weakness identification</li>
              <li>Clarity improvements</li>
              <li>Visibility recommendations</li>
              <li>Positioning feedback</li>
            </ul>
          </div>

          <div className="text-center pt-10">
            <Link
              to="/upload"
              className="inline-block bg-blue-600 hover:bg-blue-700 text-white px-8 py-4 rounded-xl text-lg font-semibold shadow-lg transition-colors"
            >
              Check Your ATS Score Now
            </Link>
          </div>

        </section>

      </div>
    </Layout>
  );
}
