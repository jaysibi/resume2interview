import Layout from '../components/Layout';

export default function PrivacyPolicyPage() {
  return (
    <Layout>
      <div className="min-h-screen bg-gray-50 py-12">
        <div className="container mx-auto px-4 max-w-4xl">
          <h1 className="text-4xl font-bold text-gray-900 mb-8">Privacy Policy</h1>
          
          <div className="bg-white rounded-xl shadow-sm p-8 space-y-8">
            <section>
              <p className="text-sm text-gray-500 mb-6">
                <strong>Effective Date:</strong> May 4, 2026<br />
                <strong>Last Updated:</strong> May 4, 2026
              </p>
            </section>

            <section>
              <h2 className="text-2xl font-semibold text-gray-900 mb-4">1. Introduction</h2>
              <p className="text-gray-700 leading-relaxed mb-4">
                ResumeTailor ("we," "our," or "us") is committed to protecting your privacy and ensuring the security of your personal information. This Privacy Policy explains how we collect, use, disclose, and safeguard your information when you use our resume analysis platform.
              </p>
              <p className="text-gray-700 leading-relaxed">
                This Privacy Policy is designed to comply with the Information Technology Act, 2000, and the Information Technology (Reasonable Security Practices and Procedures and Sensitive Personal Data or Information) Rules, 2011 ("SPDI Rules") of India, as well as international best practices.
              </p>
            </section>

            <section>
              <h2 className="text-2xl font-semibold text-gray-900 mb-4">2. Information We Collect</h2>
              
              <h3 className="text-xl font-semibold text-gray-800 mb-3 mt-4">2.1 Personal Information</h3>
              <p className="text-gray-700 leading-relaxed mb-3">
                We may collect the following types of personal information:
              </p>
              <ul className="list-disc list-inside text-gray-700 space-y-2 ml-4">
                <li>Resume content including your name, contact details, work experience, education, and skills</li>
                <li>Job description information you provide for analysis</li>
                <li>Email address (if you choose to provide it)</li>
                <li>Usage data and analytics</li>
              </ul>

              <h3 className="text-xl font-semibold text-gray-800 mb-3 mt-4">2.2 Technical Information</h3>
              <p className="text-gray-700 leading-relaxed mb-3">
                We automatically collect certain technical information when you use our service:
              </p>
              <ul className="list-disc list-inside text-gray-700 space-y-2 ml-4">
                <li>IP address and device information</li>
                <li>Browser type and version</li>
                <li>Operating system</li>
                <li>Access times and dates</li>
                <li>Pages viewed and interactions with our platform</li>
              </ul>
            </section>

            <section>
              <h2 className="text-2xl font-semibold text-gray-900 mb-4">3. How We Use Your Information</h2>
              <p className="text-gray-700 leading-relaxed mb-3">
                We use the collected information for the following purposes:
              </p>
              <ul className="list-disc list-inside text-gray-700 space-y-2 ml-4">
                <li><strong>Resume Analysis:</strong> To analyze your resume against job descriptions and provide ATS score, gap analysis, and recommendations</li>
                <li><strong>Service Improvement:</strong> To improve our AI models, algorithms, and user experience</li>
                <li><strong>Communication:</strong> To respond to your inquiries and provide customer support</li>
                <li><strong>Analytics:</strong> To understand usage patterns and optimize our platform</li>
                <li><strong>Legal Compliance:</strong> To comply with applicable laws and regulations</li>
              </ul>
            </section>

            <section>
              <h2 className="text-2xl font-semibold text-gray-900 mb-4">4. Data Processing and AI</h2>
              <p className="text-gray-700 leading-relaxed mb-3">
                Your resume and job description data are processed using artificial intelligence (OpenAI GPT models) to provide analysis and recommendations. This processing involves:
              </p>
              <ul className="list-disc list-inside text-gray-700 space-y-2 ml-4">
                <li>Extracting skills and keywords from your resume</li>
                <li>Comparing your qualifications against job requirements</li>
                <li>Generating personalized recommendations</li>
              </ul>
              <p className="text-gray-700 leading-relaxed mt-3">
                We ensure that third-party AI services we use comply with data protection standards and do not retain your data beyond processing.
              </p>
            </section>

            <section>
              <h2 className="text-2xl font-semibold text-gray-900 mb-4">5. Data Sharing and Disclosure</h2>
              <p className="text-gray-700 leading-relaxed mb-3">
                We do not sell, trade, or rent your personal information to third parties. We may share your information only in the following circumstances:
              </p>
              <ul className="list-disc list-inside text-gray-700 space-y-2 ml-4">
                <li><strong>Service Providers:</strong> With trusted third-party service providers (e.g., OpenAI for AI processing, cloud hosting providers) who assist in operating our platform</li>
                <li><strong>Legal Requirements:</strong> When required by law, court order, or government regulation</li>
                <li><strong>Protection of Rights:</strong> To protect our rights, property, or safety, or that of our users or the public</li>
                <li><strong>Business Transfers:</strong> In connection with a merger, acquisition, or sale of assets (with prior notice to you)</li>
              </ul>
            </section>

            <section>
              <h2 className="text-2xl font-semibold text-gray-900 mb-4">6. Data Security</h2>
              <p className="text-gray-700 leading-relaxed mb-3">
                We implement appropriate technical and organizational security measures to protect your personal information, including:
              </p>
              <ul className="list-disc list-inside text-gray-700 space-y-2 ml-4">
                <li>Encryption of data in transit (HTTPS/TLS)</li>
                <li>Secure database storage with access controls</li>
                <li>Rate limiting and security headers to prevent attacks</li>
                <li>Regular security audits and updates</li>
                <li>UUID-based resource identification to prevent enumeration</li>
              </ul>
              <p className="text-gray-700 leading-relaxed mt-3">
                However, no method of transmission over the internet or electronic storage is 100% secure. While we strive to protect your information, we cannot guarantee absolute security.
              </p>
            </section>

            <section>
              <h2 className="text-2xl font-semibold text-gray-900 mb-4">7. Data Retention</h2>
              <p className="text-gray-700 leading-relaxed">
                We retain your personal information for as long as necessary to provide our services and comply with legal obligations. Resume and job description data are stored indefinitely unless you request deletion. You may request deletion of your data at any time by contacting us.
              </p>
            </section>

            <section>
              <h2 className="text-2xl font-semibold text-gray-900 mb-4">8. Your Rights Under Indian Law</h2>
              <p className="text-gray-700 leading-relaxed mb-3">
                Under the SPDI Rules and IT Act, 2000, you have the following rights:
              </p>
              <ul className="list-disc list-inside text-gray-700 space-y-2 ml-4">
                <li><strong>Right to Access:</strong> You may request access to the personal information we hold about you</li>
                <li><strong>Right to Correction:</strong> You may request correction of inaccurate or incomplete information</li>
                <li><strong>Right to Withdrawal:</strong> You may withdraw consent for data processing at any time</li>
                <li><strong>Right to Delete:</strong> You may request deletion of your personal information, subject to legal requirements</li>
                <li><strong>Right to Opt-Out:</strong> You may opt out of marketing communications (if applicable)</li>
              </ul>
              <p className="text-gray-700 leading-relaxed mt-4">
                To exercise any of these rights, please contact us at the email provided in Section 12.
              </p>
            </section>

            <section>
              <h2 className="text-2xl font-semibold text-gray-900 mb-4">9. Cookies and Tracking Technologies</h2>
              <p className="text-gray-700 leading-relaxed">
                We may use cookies and similar tracking technologies to enhance your experience. These technologies help us understand how you use our platform and improve functionality. You can control cookie preferences through your browser settings.
              </p>
            </section>

            <section>
              <h2 className="text-2xl font-semibold text-gray-900 mb-4">10. International Data Transfers</h2>
              <p className="text-gray-700 leading-relaxed">
                Your data may be processed in servers located outside India, including in countries where third-party service providers operate. We ensure that such transfers comply with applicable data protection laws and that adequate safeguards are in place.
              </p>
            </section>

            <section>
              <h2 className="text-2xl font-semibold text-gray-900 mb-4">11. Children's Privacy</h2>
              <p className="text-gray-700 leading-relaxed">
                Our service is not intended for individuals under the age of 18. We do not knowingly collect personal information from children. If you believe we have inadvertently collected information from a minor, please contact us immediately.
              </p>
            </section>

            <section>
              <h2 className="text-2xl font-semibold text-gray-900 mb-4">12. Contact Information</h2>
              <p className="text-gray-700 leading-relaxed mb-3">
                If you have any questions, concerns, or requests regarding this Privacy Policy or our data practices, please contact us:
              </p>
              <div className="bg-gray-50 p-6 rounded-lg">
                <p className="text-gray-800 font-semibold mb-2">ResumeTailor</p>
                <p className="text-gray-700">Email: <a href="mailto:privacy@resumetailor.com" className="text-primary-600 hover:text-primary-700">privacy@resumetailor.com</a></p>
                <p className="text-gray-700">Response Time: We will respond to your inquiry within 30 days</p>
              </div>
            </section>

            <section>
              <h2 className="text-2xl font-semibold text-gray-900 mb-4">13. Grievance Officer</h2>
              <p className="text-gray-700 leading-relaxed mb-3">
                In accordance with the Information Technology Act, 2000, and rules made thereunder, the name and contact details of the Grievance Officer are provided below:
              </p>
              <div className="bg-gray-50 p-6 rounded-lg">
                <p className="text-gray-800 font-semibold mb-2">Grievance Officer</p>
                <p className="text-gray-700">Name: Data Protection Officer</p>
                <p className="text-gray-700">Email: <a href="mailto:grievance@resumetailor.com" className="text-primary-600 hover:text-primary-700">grievance@resumetailor.com</a></p>
                <p className="text-gray-700 mt-2">The Grievance Officer will address complaints within one month from the date of receipt.</p>
              </div>
            </section>

            <section>
              <h2 className="text-2xl font-semibold text-gray-900 mb-4">14. Changes to This Privacy Policy</h2>
              <p className="text-gray-700 leading-relaxed">
                We may update this Privacy Policy from time to time to reflect changes in our practices or legal requirements. We will notify you of any material changes by posting the updated policy on our platform with a new "Last Updated" date. Your continued use of our service after such changes constitutes acceptance of the updated policy.
              </p>
            </section>

            <section>
              <h2 className="text-2xl font-semibold text-gray-900 mb-4">15. Consent</h2>
              <p className="text-gray-700 leading-relaxed">
                By using ResumeTailor, you consent to the collection, use, and processing of your information as described in this Privacy Policy. If you do not agree with this policy, please discontinue use of our services.
              </p>
            </section>

            <section className="border-t border-gray-200 pt-8">
              <p className="text-sm text-gray-500 italic">
                This Privacy Policy has been prepared in accordance with the provisions of the Information Technology Act, 2000 and the Information Technology (Reasonable Security Practices and Procedures and Sensitive Personal Data or Information) Rules, 2011.
              </p>
            </section>
          </div>

          {/* Back to Home */}
          <div className="mt-8 text-center">
            <a href="/" className="text-primary-600 hover:text-primary-700 font-medium">
              ← Back to Home
            </a>
          </div>
        </div>
      </div>
    </Layout>
  );
}
