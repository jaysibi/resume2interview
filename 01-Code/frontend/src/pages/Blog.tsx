import { Link } from 'react-router-dom';
import Layout from '../components/Layout';
import SEO from '../components/SEO';

export default function Blog() {
  return (
    <Layout navigationVariant="solid">
      <SEO 
        title="Blog - Resume Tips & ATS Optimization Guide | Resume2Interview"
        description="Learn expert strategies for beating ATS systems, optimizing resumes for recruiters, and landing more interview calls. Free resume and career advice."
        keywords="resume tips, ATS optimization guide, career advice, job search tips, resume writing, interview preparation"
        canonicalUrl="https://resume2interview.com/blog"
        ogType="blog"
      />
      <div className="min-h-screen bg-gray-50">
        
        {/* Hero */}
        <section className="max-w-6xl mx-auto py-20 px-6 text-center">
          <h1 className="text-5xl font-bold text-gray-900">Resume & Career Insights</h1>

          <p className="mt-6 text-xl text-gray-600 max-w-3xl mx-auto">
            Learn how ATS systems work, how recruiters evaluate resumes, and how to improve your chances of getting interview calls.
          </p>
        </section>

        {/* Blog Grid */}
        <section className="max-w-6xl mx-auto px-6 pb-20 grid md:grid-cols-3 gap-8">

          <Link to="/blog/tailor-resume-to-job-description" className="bg-white border rounded-2xl p-8 shadow-sm hover:shadow-md transition">
            <h2 className="text-2xl font-semibold leading-snug text-gray-900">
              How to Tailor Your Resume to Job Description
            </h2>

            <p className="mt-4 text-gray-600 leading-7">
              Learn step-by-step how to customize your resume for each job application to beat ATS systems and get more interviews.
            </p>

            <span className="mt-6 text-blue-600 font-medium inline-block">
              Read More →
            </span>
          </Link>

          <Link to="/blog/ats-resume-optimization-guide" className="bg-white border rounded-2xl p-8 shadow-sm hover:shadow-md transition">
            <h2 className="text-2xl font-semibold leading-snug text-gray-900">
              ATS Resume Optimization Complete Guide
            </h2>

            <p className="mt-4 text-gray-600 leading-7">
              Master ATS optimization. Learn how applicant tracking systems work and how to format your resume to pass automated filters.
            </p>

            <span className="mt-6 text-blue-600 font-medium inline-block">
              Read More →
            </span>
          </Link>

          <Link to="/blog/resume-keywords-ats" className="bg-white border rounded-2xl p-8 shadow-sm hover:shadow-md transition">
            <h2 className="text-2xl font-semibold leading-snug text-gray-900">
              Resume Keywords That Get Past ATS
            </h2>

            <p className="mt-4 text-gray-600 leading-7">
              Discover which keywords ATS systems scan for and how to identify the right ones for your target job role.
            </p>

            <span className="mt-6 text-blue-600 font-medium inline-block">
              Read More →
            </span>
          </Link>

        </section>

        {/* CTA Section */}
        <section className="max-w-4xl mx-auto px-6 pb-24">
          <div className="bg-blue-50 border rounded-2xl p-10 text-center">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              Ready to Optimize Your Resume?
            </h2>
            <p className="text-lg text-gray-600 mb-8">
              Get instant ATS score and personalized recommendations for your resume
            </p>
            <Link
              to="/upload"
              className="inline-block bg-blue-600 hover:bg-blue-700 text-white px-8 py-4 rounded-xl text-lg font-semibold shadow-lg transition-colors"
            >
              Analyze Your Resume Free →
            </Link>
          </div>
        </section>

      </div>
    </Layout>
  );
}
