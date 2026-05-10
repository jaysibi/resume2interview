interface RateLimitModalProps {
  isOpen: boolean;
  onClose: () => void;
  resetAt?: string;
}

export default function RateLimitModal({ isOpen, onClose, resetAt }: RateLimitModalProps) {
  if (!isOpen) return null;

  const formatResetTime = (isoString?: string) => {
    if (!isoString) return 'tomorrow';
    try {
      const date = new Date(isoString);
      return date.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit' });
    } catch {
      return 'tomorrow';
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm">
      <div className="bg-yellow-50 border-2 border-yellow-200 rounded-2xl p-8 max-w-md mx-4 shadow-2xl">
        {/* Icon */}
        <div className="w-16 h-16 bg-yellow-100 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg className="w-10 h-10 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>

        {/* Title */}
        <h3 className="text-2xl font-bold text-yellow-800 text-center mb-4">
          Daily Free Limit Reached
        </h3>

        {/* Message */}
        <p className="text-yellow-700 leading-7 text-center mb-3">
          You've reached today's free analysis limit. Try Again Tomorrow
        </p>

        <p className="text-yellow-600 text-sm leading-6 text-center mb-6">
          We're currently offering limited free access while improving Resume2Interview for early users.
        </p>

        {/* Reset Time */}
        {resetAt && (
          <p className="text-yellow-600 text-sm text-center mb-6">
            Your limit resets at <span className="font-semibold">{formatResetTime(resetAt)}</span>
          </p>
        )}

        {/* Close Button */}
        <button
          onClick={onClose}
          className="w-full bg-blue-600 text-white px-6 py-3 rounded-xl font-semibold text-lg hover:bg-blue-700 transition-colors shadow-md"
        >
          Got It
        </button>

        {/* Info Text */}
        <p className="text-xs text-yellow-600 text-center mt-4">
          ⏰ Free limit: 5 analyses per day
        </p>
      </div>
    </div>
  );
}
