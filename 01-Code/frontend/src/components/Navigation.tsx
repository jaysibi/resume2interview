import { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';

interface NavigationProps {
  variant?: 'transparent' | 'solid';
  showCTA?: boolean;
  ctaText?: string;
  ctaLink?: string;
}

export default function Navigation({ 
  variant = 'solid',
  showCTA = true,
  ctaText = 'Get Started',
  ctaLink = '/upload'
}: NavigationProps) {
  const [isScrolled, setIsScrolled] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const location = useLocation();

  // Handle scroll for sticky header effect
  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 20);
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  // Close mobile menu when route changes
  useEffect(() => {
    setIsMobileMenuOpen(false);
  }, [location]);

  const isActive = (path: string) => {
    return location.pathname === path;
  };

  const baseClasses = variant === 'transparent' && !isScrolled
    ? 'bg-transparent'
    : 'bg-white/90 backdrop-blur-md border-b border-gray-200 shadow-sm';

  return (
    <nav className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${baseClasses}`}>
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-20">
          {/* Logo / Brand */}
          <Link 
            to="/" 
            className="flex items-center group"
          >
            <img 
              src="/logo.png" 
              alt="Resume2Interview - Get more interview calls" 
              className="h-auto w-72 md:w-[480px]"
            />
          </Link>

          {/* Desktop Navigation Links */}
          <div className="hidden md:flex items-center space-x-8">
            <Link
              to="/features"
              className="text-base font-medium text-gray-700 hover:text-blue-600 transition-colors"
            >
              Features
            </Link>
            <Link
              to="/faq"
              className="text-base font-medium text-gray-700 hover:text-blue-600 transition-colors"
            >
              FAQ
            </Link>
            <Link
              to="/blog"
              className="text-base font-medium text-gray-700 hover:text-blue-600 transition-colors"
            >
              Blog
            </Link>

            <Link
              to="/upload"
              className="bg-blue-600 text-white px-6 py-2.5 rounded-lg font-medium hover:bg-blue-700 transition-colors shadow-sm"
            >
              Get Started Free
            </Link>
          </div>

          {/* Mobile Menu Button */}
          <button
            onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
            className="md:hidden p-2 rounded-lg text-gray-600 hover:bg-gray-100 transition-colors"
            aria-label="Toggle menu"
          >
            {isMobileMenuOpen ? (
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            ) : (
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            )}
          </button>
        </div>

        {/* Mobile Menu */}
        {isMobileMenuOpen && (
          <div className="md:hidden py-4 border-t border-gray-200 bg-white">
            <div className="flex flex-col space-y-4">
              <Link
                to="/"
                className={`text-base font-medium px-4 py-2 rounded-lg transition-colors ${
                  isActive('/')
                    ? 'bg-primary-50 text-primary-600'
                    : 'text-gray-700 hover:bg-gray-50'
                }`}
              >
                Home
              </Link>
              <Link
                to="/features"
                className={`text-base font-medium px-4 py-2 rounded-lg transition-colors ${
                  isActive('/features')
                    ? 'bg-primary-50 text-primary-600'
                    : 'text-gray-700 hover:bg-gray-50'
                }`}
              >
                Features
              </Link>
              <Link
                to="/faq"
                className={`text-base font-medium px-4 py-2 rounded-lg transition-colors ${
                  isActive('/faq')
                    ? 'bg-primary-50 text-primary-600'
                    : 'text-gray-700 hover:bg-gray-50'
                }`}
              >
                FAQ
              </Link>
              <Link
                to="/blog"
                className={`text-base font-medium px-4 py-2 rounded-lg transition-colors ${
                  isActive('/blog')
                    ? 'bg-primary-50 text-primary-600'
                    : 'text-gray-700 hover:bg-gray-50'
                }`}
              >
                Blog
              </Link>
              <Link
                to="/upload"
                className={`text-base font-medium px-4 py-2 rounded-lg transition-colors ${
                  isActive('/upload')
                    ? 'bg-primary-50 text-primary-600'
                    : 'text-gray-700 hover:bg-gray-50'
                }`}
              >
                Upload
              </Link>
              {showCTA && (
                <Link
                  to={ctaLink}
                  className="btn-primary mx-4"
                >
                  {ctaText}
                </Link>
              )}
            </div>
          </div>
        )}
      </div>
    </nav>
  );
}
