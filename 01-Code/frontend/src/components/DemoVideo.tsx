import { useState, useRef } from 'react';
import { trackEvent } from '../services/analytics';

interface DemoVideoProps {
  title?: string;
  showCTA?: boolean;
}

export default function DemoVideo({ 
  title = "See How Resume2Interview Works",
  showCTA = true 
}: DemoVideoProps) {
  const [hasPlayed, setHasPlayed] = useState(false);
  const [videoExists, setVideoExists] = useState(true);
  const videoRef = useRef<HTMLVideoElement>(null);

  const handlePlay = () => {
    if (!hasPlayed) {
      trackEvent('video_play', {
        video_name: 'demo_tutorial',
        video_source: 'self_hosted',
        location: 'landing_page'
      });
      setHasPlayed(true);
    }
  };

  const handleError = () => {
    setVideoExists(false);
  };

  // If video doesn't exist yet, show placeholder
  if (!videoExists) {
    return (
      <section className="py-20 bg-gradient-to-b from-white to-blue-50">
        <div className="max-w-6xl mx-auto px-6">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              {title}
            </h2>
            <p className="text-xl text-gray-600">
              Watch how AI analyzes your resume in 60 seconds
            </p>
          </div>
          
          <div className="aspect-video max-w-4xl mx-auto rounded-2xl overflow-hidden shadow-2xl bg-gray-200 flex items-center justify-center">
            <div className="text-center p-8">
              <div className="w-24 h-24 bg-gray-300 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-12 h-12 text-gray-400" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M8 5v14l11-7z"/>
                </svg>
              </div>
              <p className="text-gray-500 text-lg font-medium">Demo video coming soon</p>
              <p className="text-gray-400 text-sm mt-2">Generating your demo video...</p>
            </div>
          </div>
          
          {showCTA && (
            <div className="text-center mt-8">
              <a
                href="/upload"
                className="inline-block bg-blue-600 hover:bg-blue-700 text-white px-8 py-4 rounded-xl text-lg font-semibold shadow-lg transition-colors"
              >
                Try It Free Now →
              </a>
            </div>
          )}
        </div>
      </section>
    );
  }

  // Video exists, show HTML5 video player
  return (
    <section className="py-20 bg-gradient-to-b from-white to-blue-50">
      <div className="max-w-6xl mx-auto px-6">
        <div className="text-center mb-12">
          <h2 className="text-4xl font-bold text-gray-900 mb-4">
            {title}
          </h2>
          <p className="text-xl text-gray-600">
            Watch how AI analyzes your resume in 60 seconds
          </p>
        </div>
        
        <div className="aspect-video max-w-4xl mx-auto rounded-2xl overflow-hidden shadow-2xl bg-black">
          <video
            ref={videoRef}
            className="w-full h-full"
            controls
            preload="metadata"
            poster="/demo-thumbnail.jpg"
            onPlay={handlePlay}
            onError={handleError}
          >
            <source src="/demo-video.mp4" type="video/mp4" />
            Your browser does not support the video tag.
          </video>
        </div>
        
        <div className="max-w-4xl mx-auto mt-8">
          <div className="bg-white rounded-xl p-6 shadow-md">
            <div className="grid md:grid-cols-3 gap-6 text-center">
              <div>
                <div className="text-3xl font-bold text-blue-600 mb-2">60 sec</div>
                <div className="text-sm text-gray-600">Average analysis time</div>
              </div>
              <div>
                <div className="text-3xl font-bold text-blue-600 mb-2">15+</div>
                <div className="text-sm text-gray-600">Actionable recommendations</div>
              </div>
              <div>
                <div className="text-3xl font-bold text-blue-600 mb-2">100%</div>
                <div className="text-sm text-gray-600">Free, no credit card</div>
              </div>
            </div>
          </div>
        </div>
        
        {showCTA && (
          <div className="text-center mt-8">
            <a
              href="/upload"
              onClick={() => trackEvent('cta_click', { 
                cta_name: 'try_after_video', 
                location: 'video_section' 
              })}
              className="inline-block bg-blue-600 hover:bg-blue-700 text-white px-8 py-4 rounded-xl text-lg font-semibold shadow-lg transition-colors"
            >
              Analyze Your Resume Free →
            </a>
            <p className="text-sm text-gray-500 mt-4">
              No signup required • Results in 60 seconds • 100% Free
            </p>
          </div>
        )}
      </div>
    </section>
  );
}
