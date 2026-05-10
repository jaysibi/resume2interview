import { Link } from 'react-router-dom';
import Layout from '../components/Layout';

export default function FAQ() {
  return (
    <Layout navigationVariant="solid">
      <div className="min-h-screen bg-white">
        
        {/* Hero */}
        <section className="max-w-4xl mx-auto py-20 px-6 text-center">
          <h1 className="text-5xl font-bold text-gray-900">Frequently Asked Questions</h1>

          <p className="mt-6 text-xl text-gray-600">
            Everything you need to know about Resume2Interview and ATS optimization.
          </p>
        </section>

        {/* FAQs */}
        <section className="max-w-4xl mx-auto px-6 pb-20 space-y-10">

          <div className="border rounded-2xl p-8 shadow-sm">
            <h2 className="text-2xl font-semibold text-gray-900">What is ATS and why does it matter?</h2>

            <p className="mt-4 text-gray-600 text-lg leading-8">
              ATS (Applicant Tracking Systems) are software platforms used by companies to filter resumes before recruiters review them. These systems scan resumes for keywords, formatting, and relevance to the job description.
            </p>

            <p className="mt-4 text-gray-600 text-lg leading-8">
              If your resume doesn't match the expected terminology or structure, it may never reach a human recruiter.
            </p>
          </div>

          <div className="border rounded-2xl p-8 shadow-sm">
            <h2 className="text-2xl font-semibold text-gray-900">How is Resume2Interview different from resume builders?</h2>

            <p className="mt-4 text-gray-600 text-lg leading-8">
              Most resume builders help you create visually appealing resumes. Resume2Interview focuses specifically on helping your resume match a job description and pass ATS screening.
            </p>

            <p className="mt-4 text-gray-600 text-lg leading-8">
              The goal is not just formatting - it is increasing your chances of getting shortlisted.
            </p>
          </div>

          <div className="border rounded-2xl p-8 shadow-sm">
            <h2 className="text-2xl font-semibold text-gray-900">Do I need to customize my resume for every job?</h2>

            <p className="mt-4 text-gray-600 text-lg leading-8">
              Yes. Different companies and roles prioritize different skills and keywords.
            </p>

            <p className="mt-4 text-gray-600 text-lg leading-8">
              Tailoring your resume significantly improves your chances of getting shortlisted.
            </p>
          </div>

          <div className="border rounded-2xl p-8 shadow-sm">
            <h2 className="text-2xl font-semibold text-gray-900">Is Resume2Interview really free?</h2>

            <p className="mt-4 text-gray-600 text-lg leading-8">
              Resume2Interview is currently free for early users while we improve the platform and gather feedback.
            </p>

            <p className="mt-4 text-gray-600 text-lg leading-8">
              Pricing may be introduced later as we expand features and capabilities.
            </p>
          </div>

        </section>

      </div>
    </Layout>
  );
}
