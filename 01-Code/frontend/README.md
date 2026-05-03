# Resume Tailor Frontend - V2

Modern React application for Resume Tailor V2 with multi-user support, application tracking, and job URL fetching.

## ✨ What's New in V2

- **Multi-User Support:** Email-based user identification and data isolation
- **Application Dashboard:** Track all job applications in one place
- **Job URL Fetching:** Extract job descriptions directly from LinkedIn, Indeed, Glassdoor, and more
- **Responsive Design:** Works seamlessly on desktop, tablet, and mobile
- **Enhanced Metadata:** Track tools, companies, job titles, and upload dates

## 🚀 Quick Start

### Prerequisites

- Node.js 18+
- npm or yarn
- Backend API running on [http://localhost:8000](http://localhost:8000)

### Installation

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Open browser to http://localhost:5173
```

### Build for Production

```bash
# Create production build
npm run build

# Preview production build
npm run preview
```

## 📁 Project Structure

```
frontend/
├── src/
│   ├── pages/
│   │   ├── Home.tsx                 # Resume/JD upload and gap analysis
│   │   ├── FetchFromURL.tsx         # Job URL fetching interface (V2)
│   │   └── Applications.tsx         # Application tracking dashboard (V2)
│   ├── components/
│   │   ├── Navigation.tsx           # Main navigation bar
│   │   ├── ResumeUpload.tsx         # Resume upload form
│   │   ├── JDUpload.tsx             # JD upload form
│   │   ├── GapAnalysis.tsx          # Gap analysis display
│   │   ├── ApplicationCard.tsx      # Application list item (V2)
│   │   └── ApplicationDetail.tsx    # Application detail view (V2)
│   ├── services/
│   │   └── api.ts                   # API client for backend
│   ├── App.tsx                      # Main app component with routing
│   ├── main.tsx                     # Entry point
│   └── index.css                    # Tailwind CSS v4 styles
├── public/                          # Static assets
├── index.html                       # HTML template
├── vite.config.ts                   # Vite configuration
└── package.json                     # Dependencies and scripts
```

## 🎨 Technology Stack

- **React 18.2:** Latest React with hooks and concurrent features
- **TypeScript:** Type-safe development
- **Vite 5.x:** Fast build tool and dev server
- **Tailwind CSS v4:** Utility-first CSS framework
- **React Router 6.x:** Client-side routing
- **Axios:** HTTP client for API calls

## 📖 Pages Overview

### 1. Home Page (`/`)

**Features:**
- Upload resumes (PDF/DOCX) with user email
- Add tools/technologies metadata
- Upload job descriptions (PDF/TXT) or enter job URL
- Add company and title metadata
- Run gap analysis between resume and JD
- Create application records
- Get ATS scores

**V2 Enhancements:**
- User email field (required)
- Tools input for resume metadata
- Company and title fields for JD
- "Create Application" checkbox
- Enhanced result display with application ID

### 2. Fetch from URL (`/fetch-url`)

**Features (V2 New):**
- Paste job posting URL
- Auto-extract job title, company, and description
- Support for 5 major platforms:
  - LinkedIn
  - Indeed
  - Glassdoor
  - AngelList
  - Y Combinator Work at a Startup
- Save extracted JD to library

**Use Cases:**
- Quick JD extraction without copy-paste
- Automatic metadata population
- Consistent JD formatting

### 3. Applications Dashboard (`/applications`)

**Features (V2 New):**
- View all applications for a user
- Sort by match score or date
- Filter by company or job title
- See application status (gap analysis, ATS score)
- Click to view detailed application info

**Application List Displays:**
- Job title and company
- Resume filename
- Match score (color-coded)
- Created date
- Analysis status badges

**Application Detail Shows:**
- Complete resume information
- Full job description
- Gap analysis results (match score, skills, recommendations)
- ATS score and feedback

## 🔗 API Integration

### API Client (`src/services/api.ts`)

```typescript
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

export const api = {
  // Resume upload
  uploadResume: (file: File, userEmail: string, tools?: string) => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('user_email', userEmail);
    if (tools) formData.append('tools', tools);
    return axios.post(`${API_BASE_URL}/upload-resume/`, formData);
  },

  // JD upload
  uploadJD: (file: File, userEmail: string, jobUrl?: string, title?: string, company?: string) => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('user_email', userEmail);
    if (jobUrl) formData.append('job_url', jobUrl);
    if (title) formData.append('title', title);
    if (company) formData.append('company', company);
    return axios.post(`${API_BASE_URL}/upload-jd/`, formData);
  },

  // V2: Fetch JD from URL
  fetchJDFromURL: (jobUrl: string) => {
    return axios.post(`${API_BASE_URL}/v2/fetch-jd-from-url/`, { job_url: jobUrl });
  },

  // Gap analysis
  gapAnalysis: (resumeId: number, jdId: number, userEmail: string, createApp: boolean) => {
    return axios.post(`${API_BASE_URL}/gap-analysis/`, null, {
      params: { resume_id: resumeId, jd_id: jdId, user_email: userEmail, create_application: createApp }
    });
  },

  // V2: List applications
  listApplications: (userEmail: string) => {
    return axios.get(`${API_BASE_URL}/v2/applications/`, {
      params: { user_email: userEmail }
    });
  },

  // V2: Get application details
  getApplication: (appId: number) => {
    return axios.get(`${API_BASE_URL}/v2/applications/${appId}/`);
  },

  // ATS score
  atsScore: (resumeId: number, jdId: number) => {
    return axios.post(`${API_BASE_URL}/ats-score/`, null, {
      params: { resume_id: resumeId, jd_id: jdId }
    });
  }
};
```

## 🧪 Testing

### Manual Testing Checklist

Follow [V2_FRONTEND_TESTING_CHECKLIST.md](../backend/V2_FRONTEND_TESTING_CHECKLIST.md) for comprehensive testing:

**Test Scenarios:**
1. File Upload (V1 compatibility)
2. URL Fetch (V2 feature)
3. Applications List
4. Application Details
5. Navigation
6. Responsive Design
7. Error Handling
8. Loading States
9. Data Consistency
10. Browser Compatibility

### Running Tests

```bash
# Start backend (required)
cd ../backend
uvicorn main:app --reload

# Start frontend
npm run dev

# Open browser to http://localhost:5173
# Follow manual testing checklist
```

## 🎨 Styling

### Tailwind CSS v4

Using Tailwind CSS v4 for utility-first styling:

```css
/* src/index.css */
@import "tailwindcss";

/* Custom styles */
.btn-primary {
  @apply bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded;
}

.card {
  @apply bg-white shadow-md rounded-lg p-6;
}
```

### Responsive Design

All pages are fully responsive:
- **Desktop:** Full 3-column layouts
- **Tablet:** 2-column layouts with stack on overflow
- **Mobile:** Single column, touch-friendly buttons

### Color Scheme

- **Primary:** Blue shades for main actions
- **Success:** Green for positive results (high match scores)
- **Warning:** Yellow/Orange for medium scores
- **Danger:** Red for low scores or errors
- **Neutral:** Gray for secondary information

## 🔧 Configuration

### Environment Variables

Create `.env` file:

```env
VITE_API_BASE_URL=http://localhost:8000
```

Access in code:

```typescript
const API_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
```

### Vite Configuration

```typescript
// vite.config.ts
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': 'http://localhost:8000'
    }
  }
})
```

## 🚀 Deployment

### Build

```bash
npm run build
# Output: dist/
```

### Serve

**Option 1: Static Hosting (Netlify, Vercel)**
```bash
# Deploy dist/ folder
# Configure API base URL in environment
```

**Option 2: Nginx**
```nginx
server {
    listen 80;
    server_name resume-tailor.example.com;
    
    root /path/to/dist;
    index index.html;
    
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    location /api/ {
        proxy_pass http://localhost:8000/;
    }
}
```

**Option 3: Docker**
```dockerfile
FROM node:18-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

## 📚 Documentation

- **[Backend API Docs](../backend/API_DOCUMENTATION_V2.md)** - Complete API reference
- **[User Guide](../backend/USER_GUIDE_V2.md)** - End-user documentation
- **[Release Notes](../backend/RELEASE_NOTES_V2.md)** - V2 changes and features
- **[Migration Guide](../backend/MIGRATION_GUIDE_V2.md)** - V1 to V2 upgrade

## 🐛 Troubleshooting

### Common Issues

**Issue: "Failed to fetch"**
- Check backend is running: `curl http://localhost:8000/`
- Verify CORS settings in backend
- Check browser console for errors

**Issue: "Cannot read property of undefined"**
- Check API response structure matches frontend expectations
- Add null checks: `data?.applications || []`
- Review backend API documentation

**Issue: "File upload failed"**
- Check file size (default limit: 10MB)
- Verify file type (PDF, DOCX, TXT)
- Ensure user_email is provided

**Issue: "Application not found"**
- Verify user_email matches resume/JD upload
- Check application was created (create_application=true)
- Use applications list to get valid IDs

## 🤝 Contributing

1. Follow existing code style
2. Use TypeScript for type safety
3. Add comments for complex logic
4. Test on multiple browsers
5. Update documentation for new features

## 📝 License

Same as parent project.

---

**Version:** 2.0.0  
**Last Updated:** January 2025  
**Status:** Production Ready ✅
import reactDom from 'eslint-plugin-react-dom'

export default defineConfig([
  globalIgnores(['dist']),
  {
    files: ['**/*.{ts,tsx}'],
    extends: [
      // Other configs...
      // Enable lint rules for React
      reactX.configs['recommended-typescript'],
      // Enable lint rules for React DOM
      reactDom.configs.recommended,
    ],
    languageOptions: {
      parserOptions: {
        project: ['./tsconfig.node.json', './tsconfig.app.json'],
        tsconfigRootDir: import.meta.dirname,
      },
      // other options...
    },
  },
])
```
