import Layout from '../components/Layout';

export default function PrivacyPolicyPage() {
  return (
    <Layout>
      <div className="min-h-screen bg-white py-12">
        <div className="container mx-auto px-6 max-w-5xl">
          <h1 className="text-5xl font-bold text-gray-900 mb-6">
            Privacy Policy
          </h1>
          
          <p className="text-gray-600 text-lg mb-8">
            Last Updated: May 7, 2026
          </p>

          <p className="text-gray-700 text-lg leading-8 mb-14">
            Resume2Interview ("we", "our", or "us") values your privacy and is committed to protecting your information.
            This Privacy Policy explains how we collect, use, store, and protect information when you use our platform and services.
          </p>

          {/* Information We Collect */}
          <section className="mb-14">
            <h2 className="text-3xl font-semibold text-gray-900 mb-6">
              Information We Collect
            </h2>

            <p className="text-gray-700 text-lg leading-8 mb-6">
              We may collect information you voluntarily provide when using Resume2Interview, including:
            </p>

            <ul className="space-y-3 list-disc ml-6 text-gray-700 text-lg mb-6">
              <li>Name</li>
              <li>Email address</li>
              <li>Phone number</li>
              <li>Resume and uploaded documents</li>
              <li>Job descriptions and related content</li>
              <li>Usage and interaction information</li>
            </ul>

            <p className="text-gray-700 text-lg leading-8">
              We may also collect technical information such as browser type, device information, IP address, session activity, and diagnostic data to improve platform performance and security.
            </p>
          </section>

          {/* How We Use Information */}
          <section className="mb-14">
            <h2 className="text-3xl font-semibold text-gray-900 mb-6">
              How We Use Information
            </h2>

            <p className="text-gray-700 text-lg leading-8 mb-6">
              We use collected information to:
            </p>

            <ul className="space-y-3 list-disc ml-6 text-gray-700 text-lg">
              <li>Provide ATS analysis and resume insights</li>
              <li>Improve platform functionality and user experience</li>
              <li>Maintain system reliability and security</li>
              <li>Respond to support or service requests</li>
              <li>Develop new features, tools, and services</li>
              <li>Communicate product updates and platform information</li>
              <li>Analyze usage trends and improve performance</li>
            </ul>
          </section>

          {/* Information Sharing */}
          <section className="mb-14">
            <h2 className="text-3xl font-semibold text-gray-900 mb-6">
              Information Sharing
            </h2>

            <p className="text-gray-700 text-lg leading-8 mb-6">
              We do not sell personal information directly to third parties for independent marketing purposes.
            </p>

            <p className="text-gray-700 text-lg leading-8 mb-6">
              We may share information with trusted service providers, infrastructure partners, analytics providers, or affiliated entities that support the operation, improvement, and delivery of Resume2Interview services.
            </p>

            <p className="text-gray-700 text-lg leading-8 mb-6">
              Information may also be disclosed:
            </p>

            <ul className="space-y-3 list-disc ml-6 text-gray-700 text-lg">
              <li>To comply with legal obligations</li>
              <li>To protect platform integrity and security</li>
              <li>As part of a merger, acquisition, restructuring, or business transition</li>
            </ul>
          </section>

          {/* Data Storage & Security */}
          <section className="mb-14">
            <h2 className="text-3xl font-semibold text-gray-900 mb-6">
              Data Storage & Security
            </h2>

            <p className="text-gray-700 text-lg leading-8 mb-6">
              We use commercially reasonable safeguards designed to protect user information from unauthorized access, misuse, or disclosure.
            </p>

            <p className="text-gray-700 text-lg leading-8">
              While we strive to protect information, no internet-based service can guarantee absolute security.
            </p>
          </section>

          {/* Data Retention */}
          <section className="mb-14">
            <h2 className="text-3xl font-semibold text-gray-900 mb-6">
              Data Retention
            </h2>

            <p className="text-gray-700 text-lg leading-8">
              Information may be retained for operational, analytical, security, legal, and service improvement purposes for a reasonable period of time.
            </p>
          </section>

          {/* Cookies & Analytics */}
          <section className="mb-14">
            <h2 className="text-3xl font-semibold text-gray-900 mb-6">
              Cookies & Analytics
            </h2>

            <p className="text-gray-700 text-lg leading-8">
              Resume2Interview may use cookies, analytics tools, and similar technologies to understand platform usage, improve functionality, and enhance user experience.
            </p>
          </section>

          {/* Your Choices */}
          <section className="mb-14">
            <h2 className="text-3xl font-semibold text-gray-900 mb-6">
              Your Choices
            </h2>

            <p className="text-gray-700 text-lg leading-8">
              You may contact us to request access, updates, or deletion of certain personal information, subject to applicable legal and operational requirements.
            </p>
          </section>

          {/* Policy Updates */}
          <section className="mb-14">
            <h2 className="text-3xl font-semibold text-gray-900 mb-6">
              Policy Updates
            </h2>

            <p className="text-gray-700 text-lg leading-8">
              We may update this Privacy Policy periodically. Continued use of Resume2Interview after updates constitutes acceptance of the revised policy.
            </p>
          </section>

          {/* Contact */}
          <section className="border-t border-gray-200 pt-10">
            <h2 className="text-3xl font-semibold text-gray-900 mb-6">
              Contact
            </h2>

            <p className="text-gray-700 text-lg leading-8 mb-4">
              For questions regarding this Privacy Policy, please contact:
            </p>

            <p className="text-blue-600 text-lg">
              support@resumetailor.ai
            </p>
          </section>
        </div>
      </div>
    </Layout>
  );
}
