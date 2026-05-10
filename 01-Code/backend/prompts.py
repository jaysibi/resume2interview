# AI Service - Prompt Templates
# All LLM prompts used in the Resume Tailor application

SKILL_EXTRACTION_PROMPT = """
You are an expert resume analyzer. Extract structured information from the following resume text.

RESUME TEXT:
{resume_text}

Extract the following information and return as valid JSON:

0. **contact_info**: Contact information (extract if available, otherwise leave null)
   - name: full name from resume
   - email: email address (if present)
   - phone: phone number (if present)
   - current_title: current or most recent job title
   - current_company: current or most recent company/employer

1. **skills**: List of technical and soft skills
   - name: skill name
   - category: Programming Language | Framework | Tool | Database | Soft Skill | Other
   - proficiency: Beginner | Intermediate | Advanced | Expert (infer from context)

2. **experience**: Work experience entries
   - title: job title
   - company: company name
   - duration: time period (e.g., "2020-2023" or "2 years")
   - description: brief role description
   - key_achievements: list of quantified achievements (extract metrics if present)

3. **education**: Educational background
   - degree: degree name
   - institution: school/university name
   - graduation_year: year (string)
   - gpa: if mentioned (optional)

**Rules**:
- Extract contact information from the header/top section of resume
- For current_title and current_company, use the MOST RECENT position from experience
- Extract ALL skills mentioned (technical and soft skills)
- Include tools, frameworks, languages, methodologies
- Infer proficiency from years of experience or context clues (if no clear indicator, use "Intermediate")
- For experience, focus on measurable achievements
- Return empty arrays if no information found in that category
- Use null for contact fields if not found
- Do NOT invent information - only extract what is explicitly stated or clearly implied

Return ONLY valid JSON matching this exact structure:
{{
  "contact_info": {{
    "name": "...",
    "email": "...",
    "phone": "...",
    "current_title": "...",
    "current_company": "..."
  }},
  "skills": [
    {{"name": "...", "category": "...", "proficiency": "..."}}
  ],
  "experience": [
    {{"title": "...", "company": "...", "duration": "...", "description": "...", "key_achievements": []}}
  ],
  "education": [
    {{"degree": "...", "institution": "...", "graduation_year": "...", "gpa": null}}
  ]
}}
"""

GAP_ANALYSIS_PROMPT = """
You are an expert career advisor and resume consultant. Compare the candidate's resume against the job description and provide a detailed gap analysis.

CANDIDATE RESUME:
Skills: {resume_skills}
Experience Summary: {resume_experience}
Education: {resume_education}

JOB DESCRIPTION:
{jd_text}

Provide a comprehensive analysis in valid JSON format:

1. **match_score** (0-100): Overall match percentage based on skills, experience level, and qualifications
2. **missing_required_skills**: Critical skills mentioned in JD but not found in resume
3. **missing_preferred_skills**: Preferred/nice-to-have skills candidate lacks
4. **strengths**: 3-5 specific areas where candidate strongly aligns with requirements
5. **weak_areas**: 2-4 areas needing improvement or gaps in qualification
6. **recommendations**: 4-7 actionable, specific recommendations for improving candidacy

**Analysis Guidelines**:
- Be honest but constructive in feedback
- Focus on actionable, specific recommendations
- Consider transferable skills and related experience
- Account for experience level mentioned in JD
- Prioritize required over preferred skills in scoring
- Look for keyword matches and semantic similarities

Return ONLY valid JSON matching this structure:
{{
  "match_score": 75,
  "missing_required_skills": ["skill1", "skill2"],
  "missing_preferred_skills": ["skill3"],
  "strengths": ["point1", "point2", "point3"],
  "weak_areas": ["gap1", "gap2"],
  "recommendations": ["rec1", "rec2", "rec3", "rec4"]
}}
"""

ATS_SCORING_PROMPT = """
You are an ATS (Applicant Tracking System) expert. Evaluate how well this resume would perform in automated screening systems when matched against the job description.

RESUME TEXT:
{resume_text}

JOB DESCRIPTION:
{jd_text}

Analyze the resume for ATS compatibility and keyword matching. Provide a detailed report in valid JSON format:

1. **ats_score** (0-100): Overall ATS compatibility score
2. **keyword_match_percentage** (0-100): Percentage of important JD keywords found in resume
3. **format_score** (0-100): Resume formatting quality for ATS parsing
4. **matched_keywords**: List of important keywords from JD that appear in resume
5. **missing_keywords**: List of important keywords from JD that are missing from resume
6. **issues**: List of ATS parsing problems found
   - Each issue: {{"type": "keyword|formatting|structure", "description": "...", "severity": "low|medium|high"}}
7. **recommendations**: 3-6 specific, actionable improvements to boost ATS score

**ATS Evaluation Criteria**:
- Keyword matching: skills, tools, qualifications, technologies from JD
- Standard section headers: Work Experience, Education, Skills, Summary
- Simple formatting: avoid tables, columns, text boxes, graphics
- Contact information: clearly stated and parseable
- Proper use of industry-standard terminology
- File format compatibility indicators

Return ONLY valid JSON matching this structure:
{{
  "ats_score": 82,
  "keyword_match_percentage": 75,
  "format_score": 89,
  "matched_keywords": ["Python", "FastAPI", "SQL"],
  "missing_keywords": ["Kubernetes", "Docker"],
  "issues": [
    {{"type": "keyword", "description": "Missing 'Docker' keyword", "severity": "medium"}}
  ],
  "recommendations": ["Add Docker experience", "Use standard 'Work Experience' header"]
}}
"""

BULLET_REWRITE_PROMPT = """
You are an expert resume writer specializing in impactful, ATS-optimized bullet points. Rewrite the following bullet point to make it more compelling and keyword-rich.

ORIGINAL BULLET POINT:
{original_bullet}

TARGET JOB KEYWORDS:
{jd_keywords}

REWRITING GUIDELINES:
1. Use STAR method (Situation, Task, Action, Result) or XYZ format (Accomplished X by doing Y resulting in Z)
2. Include quantifiable metrics wherever possible (percentages, numbers, time savings, scale)
3. Start with a strong action verb (Architected, Spearheaded, Optimized, Implemented, Led, Drove, etc.)
4. Incorporate relevant keywords from the job description naturally - don't force them
5. Keep it concise: aim for 1-2 lines, under 150 characters if possible
6. Focus on impact and measurable results, not just responsibilities or tasks
7. Use industry-standard terminology

Return ONLY the rewritten bullet point, nothing else. No explanations, no metadata, just the improved bullet point text.
"""
