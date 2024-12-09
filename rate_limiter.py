# rate_limiter.py
import time
from functools import wraps
from typing import Callable, Any

class RateLimiter:
    """
    Advanced rate limiting mechanism to prevent request flooding.
    
    Supports configurable maximum calls per time period with sliding window.
    """
    def __init__(self, max_calls: int = 5, period: float = 1.0):
        """
        Initialize rate limiter.
        
        Args:
            max_calls (int): Maximum number of calls allowed
            period (float): Time window in seconds
        """
        self.max_calls = max_calls
        self.period = period
        self.calls = []

    def __call__(self, func: Callable) -> Callable:
        """
        Decorator to apply rate limiting to a function.
        
        Args:
            func (Callable): Function to be rate limited
        
        Returns:
            Callable: Wrapped function with rate limiting
        """
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            current_time = time.time()
            
            # Remove calls outside the current time window
            self.calls = [call for call in self.calls if current_time - call < self.period]
            
            # Check if we've exceeded max calls
            if len(self.calls) >= self.max_calls:
                # Calculate wait time
                oldest_call = min(self.calls)
                wait_time = self.period - (current_time - oldest_call)
                time.sleep(max(0, wait_time))
            
            # Record this call and execute function
            self.calls.append(current_time)
            return func(*args, **kwargs)
        
        return wrapper