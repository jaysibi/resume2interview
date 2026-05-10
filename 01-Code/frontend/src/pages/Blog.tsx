import { Link } from 'react-router-dom';
import Layout from '../components/Layout';

export default function Blog() {
  return (
    <Layout navigationVariant="solid">
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

          <article className="bg-white border rounded-2xl p-8 shadow-sm hover:shadow-md transition">
            <h2 className="text-2xl font-semibold leading-snug text-gray-900">
              Why Your Resume Is Not Getting Shortlisted
            </h2>

            <p className="mt-4 text-gray-600 leading-7">
              Most resumes fail before reaching a recruiter. Learn the common ATS mistakes job seekers make.
            </p>

            <button className="mt-6 text-blue-600 font-medium">
              Read More →
            </button>
          </article>

          <article className="bg-white border rounded-2xl p-8 shadow-sm hover:shadow-md transition">
            <h2 className="text-2xl font-semibold leading-snug text-gray-900">
              How ATS Systems Actually Work
            </h2>

            <p className="mt-4 text-gray-600 leading-7">
              Understand how recruiters search resumes and how ATS platforms rank candidates.
            </p>

            <button className="mt-6 text-blue-600 font-medium">
              Read More →
            </button>
          </article>

          <article className="bg-white border rounded-2xl p-8 shadow-sm hover:shadow-md transition">
            <h2 className="text-2xl font-semibold leading-snug text-gray-900">
              5 Resume Mistakes IT Professionals Make
            </h2>

            <p className="mt-4 text-gray-600 leading-7">
              Discover the most common resume problems reducing interview calls for IT professionals.
            </p>

            <button className="mt-6 text-blue-600 font-medium">
              Read More →
            </button>
          </article>

        </section>

        {/* Featured Blog */}
        <section className="max-w-4xl mx-auto px-6 pb-24">

          <div className="bg-white border rounded-2xl p-10 shadow-sm">

            <h1 className="text-4xl font-bold leading-tight text-gray-900">
              Why Your Resume Is Not Getting Shortlisted
            </h1>

            <p className="mt-6 text-gray-600 text-lg leading-8">
              If you're applying to jobs but not getting interview calls, your resume may not even be reaching recruiters.
            </p>

            <h2 className="mt-10 text-2xl font-semibold text-gray-900">
              1. No Keyword Matching
            </h2>

            <p className="mt-4 text-gray-600 text-lg leading-8">
              ATS systems scan resumes for keywords from job descriptions. If your resume lacks those keywords, your chances of getting shortlisted decrease significantly.
            </p>

            <h2 className="mt-10 text-2xl font-semibold text-gray-900">
              2. Weak Achievement Statements
            </h2>

            <p className="mt-4 text-gray-600 text-lg leading-8">
              Recruiters look for impact and measurable outcomes. Generic statements like "worked on automation testing" do not stand out.
            </p>

            <h2 className="mt-10 text-2xl font-semibold text-gray-900">
              3. Generic Resume for Every Job
            </h2>

            <p className="mt-4 text-gray-600 text-lg leading-8">
              Using the same resume for every application reduces your chances dramatically. Every role prioritizes different skills and experiences.
            </p>

            <div className="mt-12 text-center">
              <Link
                to="/upload"
                className="inline-block bg-blue-600 hover:bg-blue-700 text-white px-8 py-4 rounded-xl text-lg font-semibold shadow-lg transition-colors"
              >
                Check Your ATS Score
              </Link>
            </div>

          </div>

        </section>

      </div>
    </Layout>
  );
}
