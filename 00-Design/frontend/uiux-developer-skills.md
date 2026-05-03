# UI/UX Developer (Frontend Developer) — Skills Profile for Resume Tailor
**Role:** UI/UX Developer / Frontend Developer  
**Project:** Resume Tailor - ATS Resume Optimization Platform  
**Date:** May 2, 2026

---

## Role Overview

The UI/UX Developer will implement the user interface for Resume Tailor, a web-based SaaS platform for resume optimization. This role focuses on translating design mockups into responsive, accessible, performant web applications using modern frontend frameworks and best practices. The developer will work closely with designers, backend engineers, and product managers to deliver a seamless user experience.

---

## Core Technical Skills Required

### 1. **Frontend Frameworks & Libraries**

#### React.js (Recommended Primary Framework)
**Required Skills:**
- **Core React**: Components, Props, State, Lifecycle methods, Hooks (useState, useEffect, useContext, useRef)
- **React Router**: Client-side routing, nested routes, route protection
- **State Management**: 
  - Context API (for simple state)
  - Redux Toolkit (for complex state management)
  - Zustand or Jotai (lightweight alternatives)
- **React Query** (TanStack Query): Server state management, API caching, data fetching
- **Form Handling**: 
  - React Hook Form (recommended - lightweight, performant)
  - Formik (alternative)
- **File Upload**: React Dropzone or custom file upload components
- **Testing**: Jest, React Testing Library, Cypress (E2E)

**Why React for Resume Tailor:**
- Large ecosystem and community support
- Component reusability (upload forms, result cards, score gauges)
- Excellent performance with virtual DOM
- Strong TypeScript support
- Seamless integration with FastAPI backend via RESTful APIs

#### Alternative Frameworks (Nice to Know)
- **Vue.js 3**: Composition API, Vuex/Pinia, Vue Router
- **Svelte/SvelteKit**: Lightweight, no virtual DOM, great performance
- **Next.js**: React-based framework with SSR/SSG (for SEO-heavy pages like landing page)
- **Angular**: (Less recommended for MVP due to complexity)

### 2. **Core Web Technologies**

#### HTML5 (Semantic & Accessible)
- Semantic HTML elements (`<header>, <nav>, <main>, <section>, <article>, <aside>, <footer>`)
- Form elements (`<input>, <textarea>, <select>, <button>`)
- File inputs (`<input type="file">`)
- ARIA attributes for accessibility (`aria-label, aria-describedby, role`)
- Metadata tags for SEO (`<meta>, <title>, <link>`)

#### CSS3 & Styling
**Required:**
- **Modern CSS Features**: 
  - Flexbox (for 1D layouts)
  - CSS Grid (for 2D layouts)
  - CSS Variables (for theming)
  - Media Queries (responsive design)
  - Transitions & Animations
- **CSS Preprocessors**: 
  - Sass/SCSS (variables, mixins, nesting)
  - PostCSS (autoprefixer, minification)
- **CSS-in-JS** (if using React):
  - Styled Components
  - Emotion
  - CSS Modules
- **Utility-First CSS**:
  - **Tailwind CSS** (highly recommended for rapid development)
  - Bootstrap (alternative, less customizable)

**Why Tailwind for Resume Tailor:**
- Rapid prototyping with utility classes
- Consistent design system
- Built-in responsive utilities (`sm:, md:, lg:`)
- Dark mode support
- Smaller bundle size with PurgeCSS

#### JavaScript/TypeScript (ES6+)
**Required JavaScript Skills:**
- ES6+ syntax (arrow functions, destructuring, spread/rest, template literals)
- Promises, async/await
- Array methods (map, filter, reduce, find, some, every)
- Fetch API / Axios for HTTP requests
- Local Storage / Session Storage
- Error handling (try/catch, error boundaries)
- Event handling and delegation
- DOM manipulation (though React minimizes direct DOM access)

**TypeScript (Highly Recommended):**
- Type annotations and interfaces
- Generics
- Union and intersection types
- Type guards and narrowing
- Integration with React (typing props, state, events)

**Why TypeScript:**
- Catch errors at compile time
- Better IDE autocomplete and intellisense
- Self-documenting code
- Easier refactoring
- Recommended for production-grade applications

### 3. **API Integration & Data Handling**

#### RESTful API Integration
- **HTTP Methods**:GET, POST, PUT, PATCH, DELETE
- **Axios** (recommended) or **Fetch API**
- **Request/Response Handling**: 
  - Content-Type: application/json
  - File uploads: multipart/form-data
  - Error handling (4xx, 5xx status codes)
- **Authentication**: 
  - JWT tokens (store in localStorage or httpOnly cookies)
  - Token refresh logic
  - Protected routes

#### API Endpoints to Integrate (Resume Tailor Backend)
```typescript
// Health Check
GET /

// Resume Upload & Retrieval
POST /upload-resume/ (multipart/form-data)
GET /resume/{resume_id}

// Job Description Upload & Retrieval
POST /upload-jd/ (multipart/form-data)
GET /jd/{jd_id}

// Analysis Endpoints
POST /gap-analysis/?resume_id=5&jd_id=4
POST /ats-score/?resume_id=8&jd_id=4
```

#### State Management for API Data
- **React Query / TanStack Query** (recommended):
  - Caching, automatic refetching
  - Loading and error states
  - Optimistic updates
- **Redux Toolkit Query** (alternative)
- **SWR** (Vercel's data fetching library)

### 4. **Responsive Design & Cross-Browser Compatibility**

#### Responsive Web Design (RWD)
- **Mobile-First Approach**: Design for mobile, then scale up
- **Breakpoints**: 
  - Mobile: 320px - 479px
  - Tablet: 480px - 768px
  - Desktop: 769px - 1024px
  - Large Desktop: 1025px+
- **Responsive Images**: `srcset`, `<picture>` element, lazy loading
- **Flexible Layouts**: Fluid grids, flexible images, media queries
- **Touch-Friendly**: Larger tap targets (minimum 44x44px)

#### Cross-Browser Testing
- **Target Browsers**: 
  - Chrome (latest 2 versions)
  - Firefox (latest 2 versions)
  - Safari (latest 2 versions)
  - Edge (Chromium-based)
- **Testing Tools**: 
  - BrowserStack or LambdaTest (cloud-based testing)
  - Chrome DevTools (responsive design mode)
- **CSS Prefixes**: Use Autoprefixer (PostCSS) for vendor prefixes

### 5. **UI Component Libraries & Design Systems**

#### Component Libraries (Choose One)
**Option 1: Material-UI (MUI)** (React)
- Pre-built components (buttons, forms, cards, modals)
- Themeable and customizable
- Good accessibility out of the box
- Large community

**Option 2: Ant Design** (React)
- Enterprise-grade UI components
- Comprehensive form components
- Good for dashboards and data-heavy UIs

**Option 3: Chakra UI** (React)
- Accessible by default
- Composable components
- Excellent TypeScript support
- Easy theming

**Option 4: Headless UI** (React)
- Unstyled, accessible components
- Full design control with Tailwind CSS
- Smaller bundle size

**Recommendation for Resume Tailor:**
- **Tailwind CSS + Headless UI** for maximum flexibility and small bundle size
- **OR Chakra UI** for faster development with pre-styled components

### 6. **File Upload & Handling**

#### File Upload Implementation
- **React Dropzone**: Drag-and-drop file upload
- **HTML File Input**: `<input type="file" accept=".pdf,.docx">`
- **Validation**: 
  - File type checking (PDF, DOCX)
  - File size limits (e.g., max 5MB)
  - Client-side validation before upload
- **Progress Indicators**: 
  - Upload progress bar
  - Parsing status (uploading → parsing → complete)
- **Preview**: Show file name, size, and upload status
- **Error Handling**: Display user-friendly error messages

#### FormData API
```javascript
const formData = new FormData();
formData.append('file', selectedFile);
formData.append('filename', selectedFile.name);

axios.post('/upload-resume/', formData, {
  headers: { 'Content-Type': 'multipart/form-data' },
  onUploadProgress: (progressEvent) => {
    const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
    setUploadProgress(percentCompleted);
  }
});
```

### 7. **Data Visualization**

#### Charts & Graphs for ATS Scoring
**Recommended Libraries:**
- **Recharts** (React): Simple, composable charts
- **Chart.js with react-chartjs-2**: Flexible, widely used
- **Nivo**: Beautiful, responsive charts
- **Victory**: Modular charting library
- **D3.js** (advanced): Maximum flexibility, steep learning curve

**Visualizations Needed for Resume Tailor:**
- **ATS Score Gauge**: Radial gauge or semi-circle progress indicator
- **Keyword Match Bar Chart**: Show matched vs missing keywords
- **Skills Comparison**: Side-by-side bar chart (resume skills vs JD requirements)
- **Gap Analysis Dashboard**: Multiple visualizations in one view

### 8. **Accessibility (a11y)**

#### WCAG 2.1 AA Compliance
- **Keyboard Navigation**: All interactive elements accessible via Tab, Enter, Space
- **Screen Reader Support**: 
  - Semantic HTML
  - ARIA labels and roles (`aria-label, role="button"`)
  - Alt text for images
- **Color Contrast**: Minimum 4.5:1 ratio for normal text, 3:1 for large text
- **Focus Indicators**: Visible focus states for all interactive elements
- **Form Labels**: Proper `<label>` elements or `aria-label`
- **Error Messages**: Announce errors to screen readers (`aria-live="polite"`)

#### Testing Tools
- **axe DevTools**: Browser extension for accessibility audits
- **Lighthouse**: Chrome DevTools accessibility audit
- **NVDA / JAWS**: Screen reader testing (Windows)
- **VoiceOver**: Screen reader testing (macOS)

### 9. **Performance Optimization**

#### Frontend Performance Best Practices
- **Code Splitting**: 
  - React.lazy() and Suspense for route-based code splitting
  - Dynamic imports for large components
- **Bundle Size Optimization**: 
  - Tree shaking (remove unused code)
  - Minification and compression (Webpack, Vite)
  - Analyze bundle size (webpack-bundle-analyzer)
- **Image Optimization**: 
  - Use WebP format
  - Lazy loading (`loading="lazy"`)
  - Responsive images with srcset
- **Caching Strategies**: 
  - Service Workers (for offline support)
  - Cache API responses with React Query
- **Lighthouse Score**: 
  - Performance: >90
  - Accessibility: 100
  - Best Practices: >90
  - SEO: >90

### 10. **Build Tools & Development Environment**

#### Build Tools
- **Vite** (recommended): Lightning-fast development server, optimized builds
- **Create React App (CRA)**: Zero-config React setup (being phased out)
- **Webpack**: Highly configurable (if custom build needed)
- **Parcel**: Zero-config alternative

#### Package Managers
- **npm** (default)
- **yarn** (faster, better workspace support)
- **pnpm** (disk-efficient)

#### Version Control
- **Git**: Branching, merging, pull requests
- **GitHub / GitLab / Bitbucket**: Code hosting and collaboration
- **Git Workflows**: Feature branches, main branch protection

#### Development Tools
- **VS Code** (recommended): Extensions for React, ESLint, Prettier, Tailwind IntelliSense
- **ESLint**: Code linting for JavaScript/TypeScript
- **Prettier**: Code formatting
- **Husky + lint-staged**: Pre-commit hooks for linting/formatting
- **Chrome DevTools**: Debugging, performance profiling, network analysis

---

## Project-Specific Implementation Requirements

### 1. **Key Features to Implement**

#### Landing Page
- Hero section with value proposition
- "Upload Resume" and "Upload Job Description" CTAs
- Responsive navigation (mobile menu)
- Footer with links (privacy policy, terms, contact)

#### Resume Upload Flow
```tsx
// Example React component structure
<ResumeUpload>
  <FileDropzone onFileSelect={handleFileUpload} />
  <UploadProgress progress={uploadProgress} />
  <ValidationErrors errors={errors} />
  <SuccessMessage resume={parsedResume} />
</ResumeUpload>
```
- Drag-and-drop file upload
- File validation (PDF/DOCX, max 5MB)
- Progress indicator with upload percentage
- Display parsed resume data (skills, experience)
- Error handling with user-friendly messages

#### Job Description Upload Flow
- Similar to resume upload
- Additional option: Paste JD text directly
- URL input to fetch JD from job boards (future feature)

#### Results Dashboard
```tsx
<ResultsDashboard>
  <ATSScoreCard score={atsScore} />
  <GapAnalysis gaps={missingSkills} />
  <KeywordComparison resumeKeywords={...} jdKeywords={...} />
  <SuggestionsList suggestions={recommendations} />
  <ExportButtons resumeId={resumeId} jdId={jdId} />
</ResultsDashboard>
```
- Display ATS score with visual gauge
- Gap analysis with missing skills highlighted
- Keyword comparison (side-by-side or Venn diagram)
- Actionable suggestions for improvement
- Download optimized resume (PDF/DOCX)

#### Loading & Error States
- Skeleton loaders for content loading
- Spinner for API requests
- Error boundaries for graceful error handling
- Toast notifications for success/error messages

### 2. **State Management Strategy**

#### Global State (Redux Toolkit or Context API)
```typescript
interface AppState {
  user: User | null;
  uploadedResume: Resume | null;
  uploadedJD: JobDescription | null;
  analysisResults: AnalysisResults | null;
  isLoading: boolean;
  errors: string[];
}
```

#### Local Component State (useState)
- Form inputs
- UI toggles (modals, dropdowns)
- Temporary validation errors

#### Server State (React Query)
- API data fetching and caching
- Automatic refetching on focus/reconnect

### 3. **Routing Structure**

```typescript
// React Router v6 structure
<BrowserRouter>
  <Routes>
    <Route path="/" element={<LandingPage />} />
    <Route path="/upload-resume" element={<ResumeUpload />} />
    <Route path="/upload-jd" element={<JDUpload />} />
    <Route path="/results" element={<ResultsDashboard />} />
    <Route path="/resume/:id" element={<ResumeDetail />} />
    <Route path="/jd/:id" element={<JDDetail />} />
    <Route path="*" element={<NotFound />} />
  </Routes>
</BrowserRouter>
```

---

## Testing & Quality Assurance

### Unit Testing
- **Jest**: JavaScript testing framework
- **React Testing Library**: Test React components (user-centric approach)
- **Coverage Target**: >80% code coverage for critical components

### Integration Testing
- **React Testing Library**: Test component interactions
- **MSW (Mock Service Worker)**: Mock API responses

### End-to-End Testing
- **Cypress** (recommended): Visual E2E testing, time travel debugging
- **Playwright** (alternative): Cross-browser E2E testing
- **Test Scenarios**: 
  - Upload resume → view results → export
  - Upload JD → analyze gap → download report

### Accessibility Testing
- **axe DevTools**: Automated accessibility audits
- **Manual Testing**: Keyboard navigation, screen reader testing

---

## Collaboration & Workflow

### Agile Development
- Work in 2-week sprints
- Daily standups (15 minutes)
- Sprint planning, review, and retrospectives
- Use Jira, Trello, or Linear for task tracking

### Communication with Design Team
- Clarify design specifications and edge cases
- Provide feedback on design feasibility
- Request design assets in developer-friendly formats (SVGs, PNG @2x, design tokens)

### Communication with Backend Team
- Understand API contracts and data structures
- Request API documentation (Swagger/OpenAPI spec)
- Coordinate on error handling and validation
- Align on authentication and authorization flow

### Code Review
- Submit pull requests (PRs) for all code changes
- Peer review for code quality, best practices, and maintainability
- Address feedback and iterate

---

## Deliverables Expected

### Phase 1: Setup & Scaffolding (Week 1)
- [ ] Initialize React project with Vite or CRA
- [ ] Set up folder structure (components, pages, utils, services)
- [ ] Configure ESLint, Prettier, TypeScript
- [ ] Install core dependencies (React Router, Axios, Tailwind CSS)
- [ ] Set up Git repository and CI/CD pipeline

### Phase 2: Core UI Implementation (Week 2-3)
- [ ] Implement landing page (responsive, pixel-perfect)
- [ ] Build resume upload component with drag-and-drop
- [ ] Build JD upload component
- [ ] Integrate with backend APIs (upload, retrieve)
- [ ] Implement loading states and error handling

### Phase 3: Results Dashboard (Week 4-5)
- [ ] Build ATS score visualization
- [ ] Implement gap analysis display
- [ ] Create keyword comparison view
- [ ] Add suggestions and recommendations section
- [ ] Implement export functionality (download resume/reports)

### Phase 4: Testing & Optimization (Week 6)
- [ ] Write unit tests for critical components
- [ ] Conduct E2E testing with Cypress
- [ ] Accessibility audit and fixes
- [ ] Performance optimization (Lighthouse score >90)
- [ ] Cross-browser testing

### Phase 5: Deployment & Monitoring (Week 7)
- [ ] Deploy to staging environment (Vercel, Netlify, AWS S3)
- [ ] Set up error monitoring (Sentry)
- [ ] Configure analytics (Google Analytics, Mixpanel)
- [ ] Final QA and bug fixes
- [ ] Production deployment

---

## Nice-to-Have Skills

- **Next.js**: Server-side rendering (SSR) for SEO (if landing page needs SEO)
- **PWA**: Progressive Web App features (offline, install prompt)
- **Animations**: Framer Motion, React Spring for advanced animations
- **Internationalization (i18n)**: React i18next for multi-language support
- **Design Skills**: Basic understanding of Figma to interpret designs
- **Backend Knowledge**: Basic understanding of FastAPI, REST APIs
- **DevOps**: Docker, CI/CD (GitHub Actions, GitLab CI)
- **SEO**: Semantic HTML, meta tags, structured data

---

## Success Metrics for UI/UX Developer

### Code Quality
- **Code Coverage**: >80% for critical components
- **Lighthouse Score**: Performance >90, Accessibility 100
- **Zero Critical Bugs**: No P0/P1 bugs in production
- **Code Review Pass Rate**: >90% first-pass approval

### Performance
- **Page Load Time**: <2 seconds on 3G network
- **Time to Interactive (TTI)**: <3 seconds
- **Bundle Size**: <300KB (main bundle gzipped)

### User Experience
- **Zero Accessibility Violations**: WCAG 2.1 AA compliant
- **Cross-Browser Compatibility**: Works on Chrome, Firefox, Safari, Edge
- **Mobile Responsiveness**: Works seamlessly on all screen sizes

---

## Sample Interview Questions for UI/UX Developer

1. **React**: Explain the difference between `useState` and `useRef`. When would you use each?
2. **Performance**: How would you optimize a React app that's experiencing slow re-renders?
3. **API Integration**: Walk through how you'd implement file upload with progress tracking in React.
4. **Accessibility**: How do you ensure keyboard navigation works for a custom dropdown component?
5. **State Management**: When would you choose Redux over Context API? Or React Query?
6. **TypeScript**: How do you type a React component that accepts children and additional props?
7. **Testing**: What's the difference between unit tests and E2E tests? How do you decide what to test?
8. **CSS**: How would you implement a responsive layout that works on mobile, tablet, and desktop?
9. **Problem Solving**: A user reports that file upload isn't working on Safari. How would you debug this?
10. **Collaboration**: Describe how you collaborate with designers to implement pixel-perfect UI.

---

## Recommended Experience Level

### Junior Developer (1-2 years)
- Built 2-3 React applications (personal or work projects)
- Comfortable with HTML, CSS, JavaScript (ES6+)
- Basic understanding of REST APIs and Axios
- Can implement UI from existing designs with supervision
- Eager to learn and grow

### Mid-Level Developer (3-5 years)
- Built 5+ production React applications
- Proficient in React, TypeScript, CSS-in-JS or Tailwind
- Experience with state management (Redux, Context API)
- Can architect component structure independently
- Understands performance optimization and accessibility
- Comfortable with testing (Jest, React Testing Library)

### Senior Developer (5+ years)
- Extensive experience building complex React applications
- Expert in React, TypeScript, modern frontend tooling
- Led frontend architecture for multiple projects
- Strong understanding of design systems and reusable components
- Mentors junior developers
- Contributes to technical decision-making

---

## Technology Stack Summary

### Core Stack (Recommended)
```yaml
Framework: React 18 with TypeScript
Styling: Tailwind CSS + Headless UI
Routing: React Router v6
State: Context API + React Query (TanStack Query)
Forms: React Hook Form
HTTP Client: Axios
Build Tool: Vite
Testing: Jest + React Testing Library + Cypress
Deployment: Vercel or Netlify
```

### Alternative Stack Options
```yaml
# Option 2: Vue.js
Framework: Vue 3 with TypeScript
Styling: Tailwind CSS
Routing: Vue Router
State: Pinia
Build Tool: Vite

# Option 3: Svelte
Framework: SvelteKit
Styling: Tailwind CSS
Build Tool: Vite (built-in)
```

---

## Tools & Software Checklist

### Must Have
- [ ] Node.js (v18+ LTS)
- [ ] npm/yarn/pnpm
- [ ] VS Code with extensions (ESLint, Prettier, Tailwind IntelliSense)
- [ ] Git
- [ ] Chrome DevTools
- [ ] Postman or Insomnia (API testing)

### Nice to Have
- [ ] Figma/Adobe XD (design access)
- [ ] Docker (if running backend locally)
- [ ] BrowserStack (cross-browser testing)
- [ ] Sentry (error monitoring)

---

## References & Resources

### Learning Resources
- **React**: Official React Docs (beta.reactjs.org), React TypeScript Cheatsheet
- **TypeScript**: TypeScript Handbook, Matt Pocock's TypeScript Tips
- **Tailwind CSS**: Official Tailwind Docs, Tailwind UI Components
- **Accessibility**: W3C WCAG Guidelines, A11y Project, Inclusive Components

### Design Systems & Component Libraries
- **Material-UI (MUI)**: mui.com
- **Chakra UI**: chakra-ui.com
- **Headless UI**: headlessui.com
- **Ant Design**: ant.design

### Performance & Optimization
- **Web Vitals**: web.dev/vitals
- **Lighthouse**: Chrome DevTools → Lighthouse
- **Webpack Bundle Analyzer**: visualize bundle size

---

*This skills profile should be used for hiring, onboarding, and setting clear expectations for the UI/UX Developer (Frontend Developer) role on the Resume Tailor project.*
