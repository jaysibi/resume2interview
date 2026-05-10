import React from 'react';
import Navigation from './Navigation';

interface LayoutProps {
  children: React.ReactNode;
  showNavigation?: boolean;
  showFooter?: boolean;
  navigationVariant?: 'transparent' | 'solid';
  navigationShowCTA?: boolean;
}

export default function Layout({ 
  children, 
  showNavigation = true,
  showFooter = true,
  navigationVariant = 'solid',
  navigationShowCTA = true
}: LayoutProps) {
  return (
    <div className="min-h-screen flex flex-col">
      {showNavigation && (
        <Navigation 
          variant={navigationVariant}
          showCTA={navigationShowCTA}
        />
      )}
      
      {/* Main Content - add padding-top to account for fixed navigation */}
      <main className="flex-grow pt-20">
        {children}
      </main>

      {showFooter && (
        <footer className="bg-gray-900 text-gray-300 py-12 mt-auto">
          <div className="container mx-auto px-4 max-w-6xl">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-8">
              {/* Brand Section */}
              <div>
                <div className="flex items-center space-x-3 mb-4">
                  <div className="w-8 h-8 bg-gradient-to-br from-primary-600 to-primary-700 rounded-lg flex items-center justify-center">
                    <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                  </div>
                  <span className="text-xl font-bold text-white">Resume2Interview</span>
                </div>
                <p className="text-sm text-gray-400">
                  AI-powered resume optimization for ATS success
                </p>
              </div>

              {/* Quick Links */}
              <div>
                <h3 className="text-white font-semibold mb-4">Quick Links</h3>
                <ul className="space-y-2 text-sm">
                  <li>
                    <a href="/" className="hover:text-white transition-colors">Home</a>
                  </li>
                  <li>
                    <a href="/upload" className="hover:text-white transition-colors">Upload Resume</a>
                  </li>
                  <li>
                    <a href="/applications" className="hover:text-white transition-colors">My Applications</a>
                  </li>
                </ul>
              </div>

              {/* Resources */}
              <div>
                <h3 className="text-white font-semibold mb-4">Legal</h3>
                <ul className="space-y-2 text-sm">
                  <li>
                    <a href="/#features" className="hover:text-white transition-colors">How It Works</a>
                  </li>
                  <li>
                    <a href="/privacy" className="hover:text-white transition-colors">Privacy Policy</a>
                  </li>
                </ul>
              </div>
            </div>

            {/* Copyright */}
            <div className="border-t border-gray-800 pt-8 text-center text-sm text-gray-500">
              <p>&copy; {new Date().getFullYear()} Resume2Interview. All rights reserved.</p>
            </div>
          </div>
        </footer>
      )}
    </div>
  );
}
