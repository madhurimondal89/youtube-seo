import time
import threading

class TokenBucketRateLimiter:
    """
    Token bucket rate limiter to prevent abuse and adhere to polite request pacing.
    No Redis required; operates in-memory.
    """
    def __init__(self, rate_per_minute: int = 60, burst_capacity: int = 10):
        self.rate_per_sec = rate_per_minute / 60.0
        self.capacity = float(burst_capacity)
        self.tokens = float(burst_capacity)
        self.last_update = time.time()
        self.lock = threading.Lock()

    def acquire(self, tokens: float = 1.0) -> bool:
        with self.lock:
            now = time.time()
            elapsed = now - self.last_update
            self.last_update = now
            self.tokens = min(self.capacity, self.tokens + elapsed * self.rate_per_sec)

            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            return False

rate_limiter = TokenBucketRateLimiter(rate_per_minute=60, burst_capacity=15)
