import { useState } from 'react';
import { trackEvent } from '../services/analytics';

interface DemoVideoProps {
  videoId?: string; // YouTube video ID (e.g., "dQw4w9WgXcQ")
  title?: string;
  showCTA?: boolean;
}

export default function DemoVideo({ 
  videoId = "YOUR_VIDEO_ID_HERE", 
  title = "See How Resume2Interview Works",
  showCTA = true 
}: DemoVideoProps) {
  const [hasPlayed, setHasPlayed] = useState(false);

  const handlePlay = () => {
    if (!hasPlayed) {
      trackEvent('video_play', {
        video_name: 'demo_tutorial',
        video_id: videoId,
        location: 'landing_page'
      });
      setHasPlayed(true);
    }
  };

  // If no video uploaded yet, show placeholder
  if (videoId === "YOUR_VIDEO_ID_HERE") {
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
              <p className="text-gray-400 text-sm mt-2">Upload your video to YouTube and add the video ID here</p>
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

  // Video is uploaded, show embedded YouTube player
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
        
        <div className="aspect-video max-w-4xl mx-auto rounded-2xl overflow-hidden shadow-2xl">
          <iframe
            width="100%"
            height="100%"
            src={`https://www.youtube.com/embed/${videoId}?rel=0`}
            title="Resume2Interview Tutorial - How to Optimize Your Resume for ATS"
            frameBorder="0"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowFullScreen
            onLoad={handlePlay}
            className="w-full h-full"
          ></iframe>
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
