# Features Page (`/features`)

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Features | Resume Tailor</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-white text-gray-900 font-sans">

  <!-- Navbar -->
  <nav class="flex items-center justify-between px-8 py-5 border-b">
    <div class="flex items-center gap-3">
      <img src="logo.png" alt="Resume Tailor" class="h-12">
      <div>
        <h1 class="text-2xl font-bold">Resume <span class="text-blue-600">Tailor</span></h1>
        <p class="text-sm text-gray-500">Get more interview calls with job-matched resumes</p>
      </div>
    </div>

    <div class="flex gap-6 text-gray-700 font-medium">
      <a href="index.html">Home</a>
      <a href="features.html" class="text-blue-600">Features</a>
      <a href="faq.html">FAQ</a>
      <a href="blog.html">Blog</a>
    </div>
  </nav>

  <!-- Hero -->
  <section class="max-w-6xl mx-auto py-20 px-6 text-center">
    <h1 class="text-5xl font-bold leading-tight">
      Features Designed to Get You Interview Calls
    </h1>

    <p class="mt-6 text-xl text-gray-600 max-w-3xl mx-auto">
      Resume Tailor helps your resume pass ATS filters and align with what recruiters are actively searching for.
    </p>
  </section>

  <!-- Features -->
  <section class="max-w-5xl mx-auto px-6 pb-20 space-y-16">

    <div class="border rounded-2xl p-8 shadow-sm">
      <h2 class="text-3xl font-semibold">ATS Match Score</h2>
      <p class="mt-4 text-gray-600 text-lg">
        Get a clear score showing how well your resume matches a specific job description.
      </p>

      <ul class="mt-6 space-y-3 list-disc ml-6 text-gray-700 text-lg">
        <li>Keyword match analysis</li>
        <li>Skill alignment scoring</li>
        <li>Section-level evaluation</li>
        <li>Role-specific optimization insights</li>
      </ul>
    </div>

    <div class="border rounded-2xl p-8 shadow-sm">
      <h2 class="text-3xl font-semibold">Missing Keywords Detection</h2>
      <p class="mt-4 text-gray-600 text-lg">
        Identify critical ATS and recruiter keywords missing from your resume.
      </p>

      <ul class="mt-6 space-y-3 list-disc ml-6 text-gray-700 text-lg">
        <li>ATS-relevant keyword extraction</li>
        <li>Recruiter search terminology</li>
        <li>Technical skills gap analysis</li>
        <li>Keyword prioritization</li>
      </ul>
    </div>

    <div class="border rounded-2xl p-8 shadow-sm">
      <h2 class="text-3xl font-semibold">AI Resume Optimization</h2>
      <p class="mt-4 text-gray-600 text-lg">
        We optimize your resume strategically — not just grammatically.
      </p>

      <ul class="mt-6 space-y-3 list-disc ml-6 text-gray-700 text-lg">
        <li>Achievement-focused bullet rewrites</li>
        <li>Improved recruiter readability</li>
        <li>Action-oriented phrasing</li>
        <li>Professional summary optimization</li>
      </ul>
    </div>

    <div class="border rounded-2xl p-8 shadow-sm">
      <h2 class="text-3xl font-semibold">Job-Specific Resume Versions</h2>
      <p class="mt-4 text-gray-600 text-lg">
        Different jobs require different positioning. Resume Tailor helps customize resumes for each role.
      </p>

      <ul class="mt-6 space-y-3 list-disc ml-6 text-gray-700 text-lg">
        <li>Customized summaries</li>
        <li>Reordered experience sections</li>
        <li>Role-specific emphasis</li>
        <li>Targeted resume tailoring</li>
      </ul>
    </div>

    <div class="border rounded-2xl p-8 shadow-sm">
      <h2 class="text-3xl font-semibold">Recruiter Perspective Analysis</h2>
      <p class="mt-4 text-gray-600 text-lg">
        Understand how recruiters and hiring managers evaluate your resume.
      </p>

      <ul class="mt-6 space-y-3 list-disc ml-6 text-gray-700 text-lg">
        <li>Weakness identification</li>
        <li>Clarity improvements</li>
        <li>Visibility recommendations</li>
        <li>Positioning feedback</li>
      </ul>
    </div>

    <div class="text-center pt-10">
      <button class="bg-blue-600 hover:bg-blue-700 text-white px-8 py-4 rounded-xl text-lg font-medium">
        Check Your ATS Score Now
      </button>
    </div>

  </section>

</body>
</html>
```

---

# FAQ Page (`/faq`)

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>FAQ | Resume Tailor</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-white text-gray-900 font-sans">

  <!-- Navbar -->
  <nav class="flex items-center justify-between px-8 py-5 border-b">
    <div class="flex items-center gap-3">
      <img src="logo.png" alt="Resume Tailor" class="h-12">
      <div>
        <h1 class="text-2xl font-bold">Resume <span class="text-blue-600">Tailor</span></h1>
        <p class="text-sm text-gray-500">Get more interview calls with job-matched resumes</p>
      </div>
    </div>

    <div class="flex gap-6 text-gray-700 font-medium">
      <a href="index.html">Home</a>
      <a href="features.html">Features</a>
      <a href="faq.html" class="text-blue-600">FAQ</a>
      <a href="blog.html">Blog</a>
    </div>
  </nav>

  <!-- Hero -->
  <section class="max-w-4xl mx-auto py-20 px-6 text-center">
    <h1 class="text-5xl font-bold">Frequently Asked Questions</h1>

    <p class="mt-6 text-xl text-gray-600">
      Everything you need to know about Resume Tailor and ATS optimization.
    </p>
  </section>

  <!-- FAQs -->
  <section class="max-w-4xl mx-auto px-6 pb-20 space-y-10">

    <div class="border rounded-2xl p-8 shadow-sm">
      <h2 class="text-2xl font-semibold">What is ATS and why does it matter?</h2>

      <p class="mt-4 text-gray-600 text-lg leading-8">
        ATS (Applicant Tracking Systems) are software platforms used by companies to filter resumes before recruiters review them. These systems scan resumes for keywords, formatting, and relevance to the job description.
      </p>

      <p class="mt-4 text-gray-600 text-lg leading-8">
        If your resume doesn’t match the expected terminology or structure, it may never reach a human recruiter.
      </p>
    </div>

    <div class="border rounded-2xl p-8 shadow-sm">
      <h2 class="text-2xl font-semibold">How is Resume Tailor different from resume builders?</h2>

      <p class="mt-4 text-gray-600 text-lg leading-8">
        Most resume builders help you create visually appealing resumes. Resume Tailor focuses specifically on helping your resume match a job description and pass ATS screening.
      </p>

      <p class="mt-4 text-gray-600 text-lg leading-8">
        The goal is not just formatting — it is increasing your chances of getting shortlisted.
      </p>
    </div>

    <div class="border rounded-2xl p-8 shadow-sm">
      <h2 class="text-2xl font-semibold">Is my resume data safe?</h2>

      <p class="mt-4 text-gray-600 text-lg leading-8">
        Yes. Resume data is processed securely and is not shared with third parties.
      </p>

      <p class="mt-4 text-gray-600 text-lg leading-8">
        We only retain data temporarily for analysis and product improvement purposes.
      </p>
    </div>

    <div class="border rounded-2xl p-8 shadow-sm">
      <h2 class="text-2xl font-semibold">Do I need to customize my resume for every job?</h2>

      <p class="mt-4 text-gray-600 text-lg leading-8">
        Yes. Different companies and roles prioritize different skills and keywords.
      </p>

      <p class="mt-4 text-gray-600 text-lg leading-8">
        Tailoring your resume significantly improves your chances of getting shortlisted.
      </p>
    </div>

    <div class="border rounded-2xl p-8 shadow-sm">
      <h2 class="text-2xl font-semibold">Is Resume Tailor really free?</h2>

      <p class="mt-4 text-gray-600 text-lg leading-8">
        Resume Tailor is currently free for early users while we improve the platform and gather feedback.
      </p>

      <p class="mt-4 text-gray-600 text-lg leading-8">
        Pricing may be introduced later as we expand features and capabilities.
      </p>
    </div>

  </section>

</body>
</html>
```

---

# Blog Page (`/blog`)

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Blog | Resume Tailor</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50 text-gray-900 font-sans">

  <!-- Navbar -->
  <nav class="bg-white flex items-center justify-between px-8 py-5 border-b">
    <div class="flex items-center gap-3">
      <img src="logo.png" alt="Resume Tailor" class="h-12">
      <div>
        <h1 class="text-2xl font-bold">Resume <span class="text-blue-600">Tailor</span></h1>
        <p class="text-sm text-gray-500">Get more interview calls with job-matched resumes</p>
      </div>
    </div>

    <div class="flex gap-6 text-gray-700 font-medium">
      <a href="index.html">Home</a>
      <a href="features.html">Features</a>
      <a href="faq.html">FAQ</a>
      <a href="blog.html" class="text-blue-600">Blog</a>
    </div>
  </nav>

  <!-- Hero -->
  <section class="max-w-6xl mx-auto py-20 px-6 text-center">
    <h1 class="text-5xl font-bold">Resume & Career Insights</h1>

    <p class="mt-6 text-xl text-gray-600 max-w-3xl mx-auto">
      Learn how ATS systems work, how recruiters evaluate resumes, and how to improve your chances of getting interview calls.
    </p>
  </section>

  <!-- Blog Grid -->
  <section class="max-w-6xl mx-auto px-6 pb-20 grid md:grid-cols-3 gap-8">

    <article class="bg-white border rounded-2xl p-8 shadow-sm hover:shadow-md transition">
      <h2 class="text-2xl font-semibold leading-snug">
        Why Your Resume Is Not Getting Shortlisted
      </h2>

      <p class="mt-4 text-gray-600 leading-7">
        Most resumes fail before reaching a recruiter. Learn the common ATS mistakes job seekers make.
      </p>

      <button class="mt-6 text-blue-600 font-medium">
        Read More →
      </button>
    </article>

    <article class="bg-white border rounded-2xl p-8 shadow-sm hover:shadow-md transition">
      <h2 class="text-2xl font-semibold leading-snug">
        How ATS Systems Actually Work
      </h2>

      <p class="mt-4 text-gray-600 leading-7">
        Understand how recruiters search resumes and how ATS platforms rank candidates.
      </p>

      <button class="mt-6 text-blue-600 font-medium">
        Read More →
      </button>
    </article>

    <article class="bg-white border rounded-2xl p-8 shadow-sm hover:shadow-md transition">
      <h2 class="text-2xl font-semibold leading-snug">
        5 Resume Mistakes IT Professionals Make
      </h2>

      <p class="mt-4 text-gray-600 leading-7">
        Discover the most common resume problems reducing interview calls for IT professionals.
      </p>

      <button class="mt-6 text-blue-600 font-medium">
        Read More →
      </button>
    </article>

  </section>

  <!-- Featured Blog -->
  <section class="max-w-4xl mx-auto px-6 pb-24">

    <div class="bg-white border rounded-2xl p-10 shadow-sm">

      <h1 class="text-4xl font-bold leading-tight">
        Why Your Resume Is Not Getting Shortlisted
      </h1>

      <p class="mt-6 text-gray-600 text-lg leading-8">
        If you're applying to jobs but not getting interview calls, your resume may not even be reaching recruiters.
      </p>

      <h2 class="mt-10 text-2xl font-semibold">
        1. No Keyword Matching
      </h2>

      <p class="mt-4 text-gray-600 text-lg leading-8">
        ATS systems scan resumes for keywords from job descriptions. If your resume lacks those keywords, your chances of getting shortlisted decrease significantly.
      </p>

      <h2 class="mt-10 text-2xl font-semibold">
        2. Weak Achievement Statements
      </h2>

      <p class="mt-4 text-gray-600 text-lg leading-8">
        Recruiters look for impact and measurable outcomes. Generic statements like “worked on automation testing” do not stand out.
      </p>

      <h2 class="mt-10 text-2xl font-semibold">
        3. Generic Resume for Every Job
      </h2>

      <p class="mt-4 text-gray-600 text-lg leading-8">
        Using the same resume for every application reduces your chances dramatically. Every role prioritizes different skills and experiences.
      </p>

      <div class="mt-12 text-center">
        <button class="bg-blue-600 hover:bg-blue-700 text-white px-8 py-4 rounded-xl text-lg font-medium">
          Check Your ATS Score
        </button>
      </div>

    </div>

  </section>

</body>
</html>
```
