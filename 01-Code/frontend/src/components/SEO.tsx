import { Helmet } from 'react-helmet-async';

interface SEOProps {
  title?: string;
  description?: string;
  keywords?: string;
  canonicalUrl?: string;
  ogImage?: string;
  ogType?: string;
  schemaData?: Record<string, any>;
}

export default function SEO({
  title = 'Resume2Interview - AI-Powered Resume Tailoring & ATS Optimization',
  description = 'Optimize your resume for ATS and get more interview calls. AI-powered analysis matches your resume to job descriptions instantly. Free ATS score check.',
  keywords = 'resume tailoring, ATS optimization, resume analysis, job application, AI resume, interview preparation, applicant tracking system, resume keywords',
  canonicalUrl = 'https://resume2interview.com',
  ogImage = 'https://resume2interview.com/og-image.png',
  ogType = 'website',
  schemaData,
}: SEOProps) {
  return (
    <Helmet>
      {/* Basic Meta Tags */}
      <title>{title}</title>
      <meta name="description" content={description} />
      <meta name="keywords" content={keywords} />
      <link rel="canonical" href={canonicalUrl} />

      {/* Open Graph (Facebook, LinkedIn) */}
      <meta property="og:title" content={title} />
      <meta property="og:description" content={description} />
      <meta property="og:type" content={ogType} />
      <meta property="og:url" content={canonicalUrl} />
      <meta property="og:image" content={ogImage} />
      <meta property="og:site_name" content="Resume2Interview" />

      {/* Twitter Card */}
      <meta name="twitter:card" content="summary_large_image" />
      <meta name="twitter:title" content={title} />
      <meta name="twitter:description" content={description} />
      <meta name="twitter:image" content={ogImage} />

      {/* Additional SEO */}
      <meta name="robots" content="index, follow" />
      <meta name="author" content="Resume2Interview" />
      <meta name="viewport" content="width=device-width, initial-scale=1.0" />

      {/* Structured Data */}
      {schemaData && (
        <script type="application/ld+json">
          {JSON.stringify(schemaData)}
        </script>
      )}
    </Helmet>
  );
}

// Predefined schema helpers
export const organizationSchema = {
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Resume2Interview",
  "url": "https://resume2interview.com",
  "logo": "https://resume2interview.com/logo.png",
  "description": "AI-powered resume tailoring and ATS optimization platform that helps job seekers get more interview calls.",
  "sameAs": [
    "https://twitter.com/resume2interview",
    "https://linkedin.com/company/resume2interview"
  ],
  "contactPoint": {
    "@type": "ContactPoint",
    "contactType": "Customer Support",
    "email": "support@resume2interview.com"
  }
};

export const websiteSchema = {
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "Resume2Interview",
  "url": "https://resume2interview.com",
  "description": "AI-powered resume optimization for ATS and recruiters",
  "potentialAction": {
    "@type": "SearchAction",
    "target": "https://resume2interview.com/upload?q={search_term_string}",
    "query-input": "required name=search_term_string"
  }
};

export const softwareApplicationSchema = {
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "Resume2Interview",
  "applicationCategory": "BusinessApplication",
  "operatingSystem": "Web",
  "offers": {
    "@type": "Offer",
    "price": "0",
    "priceCurrency": "USD"
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.8",
    "ratingCount": "127"
  },
  "description": "AI-powered resume tailoring tool that helps job seekers optimize resumes for ATS and get more interview calls."
};

export const faqSchema = (faqs: { question: string; answer: string }[]) => ({
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": faqs.map(faq => ({
    "@type": "Question",
    "name": faq.question,
    "acceptedAnswer": {
      "@type": "Answer",
      "text": faq.answer
    }
  }))
});
