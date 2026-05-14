"""
In-Memory Rate Limiter for Resume Tailor
Tracks daily API usage per IP address with automatic reset at midnight UTC
"""
from datetime import datetime, timedelta
from typing import Dict, Tuple
from fastapi import Request, HTTPException
from collections import defaultdict
import threading
import time


class InMemoryRateLimiter:
    """
    Simple in-memory rate limiter with daily reset
    Stores counters per IP address per day
    """
    
    def __init__(self, daily_limit: int = 5):
        self.daily_limit = daily_limit
        # Format: {date_str: {ip: count}}
        self.counters: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        self.lock = threading.Lock()
        self._start_cleanup_thread()
    
    def _get_current_date_key(self) -> str:
        """Get current date as string key (UTC)"""
        return datetime.utcnow().strftime("%Y-%m-%d")
    
    def _start_cleanup_thread(self):
        """Start background thread to clean up old date entries"""
        def cleanup():
            while True:
                time.sleep(3600)  # Check every hour
                with self.lock:
                    current_date = self._get_current_date_key()
                    # Remove entries older than current date
                    old_dates = [date for date in self.counters.keys() if date != current_date]
                    for old_date in old_dates:
                        del self.counters[old_date]
        
        thread = threading.Thread(target=cleanup, daemon=True)
        thread.start()
    
    def get_client_ip(self, request: Request) -> str:
        """Extract client IP from request, considering proxies"""
        # Check for X-Forwarded-For header (common with proxies/load balancers)
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            # Take first IP in chain
            return forwarded.split(",")[0].strip()
        
        # Check for X-Real-IP header
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip
        
        # Fall back to direct client IP
        if request.client:
            return request.client.host
        
        return "unknown"
    
    def check_limit(self, ip: str) -> Tuple[bool, int, int]:
        """
        Check if IP has exceeded daily limit
        
        Returns:
            (is_allowed, current_count, remaining)
        """
        date_key = self._get_current_date_key()
        
        with self.lock:
            current_count = self.counters[date_key][ip]
            remaining = max(0, self.daily_limit - current_count)
            is_allowed = current_count < self.daily_limit
            
            return is_allowed, current_count, remaining
    
    def increment(self, ip: str) -> int:
        """
        Increment counter for IP address
        
        Returns:
            new_count
        """
        date_key = self._get_current_date_key()
        
        with self.lock:
            self.counters[date_key][ip] += 1
            return self.counters[date_key][ip]
    
    def get_usage_stats(self) -> Dict:
        """Get current usage statistics for analytics"""
        date_key = self._get_current_date_key()
        
        with self.lock:
            today_data = self.counters.get(date_key, {})
            
            total_requests = sum(today_data.values())
            unique_ips = len(today_data)
            at_limit = sum(1 for count in today_data.values() if count >= self.daily_limit)
            
            return {
                "date": date_key,
                "total_requests": total_requests,
                "unique_ips": unique_ips,
                "ips_at_limit": at_limit,
                "daily_limit": self.daily_limit,
                "top_ips": sorted(today_data.items(), key=lambda x: x[1], reverse=True)[:10]
            }
    
    async def check_rate_limit(self, request: Request) -> None:
        """
        Middleware-compatible rate limit checker
        Raises HTTPException if limit exceeded
        """
        ip = self.get_client_ip(request)
        is_allowed, current_count, remaining = self.check_limit(ip)
        
        if not is_allowed:
            raise HTTPException(
                status_code=429,
                detail={
                    "error": "rate_limit_exceeded",
                    "message": "You've reached today's free analysis limit. Try Again Tomorrow",
                    "limit": self.daily_limit,
                    "current": current_count,
                    "reset_at": self._get_next_reset_time()
                }
            )
        
        # Increment counter after check passes
        self.increment(ip)
        
        # Add rate limit info to response headers
        request.state.rate_limit_info = {
            "limit": self.daily_limit,
            "remaining": remaining - 1,  # -1 because we just incremented
            "used": current_count + 1
        }
    
    def _get_next_reset_time(self) -> str:
        """Calculate next midnight UTC reset time"""
        now = datetime.utcnow()
        tomorrow = now + timedelta(days=1)
        midnight = tomorrow.replace(hour=0, minute=0, second=0, microsecond=0)
        return midnight.isoformat() + "Z"


# Global rate limiter instance
# Increased limit for production testing/launch period
rate_limiter = InMemoryRateLimiter(daily_limit=100)
