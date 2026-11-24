import time
from typing import Any, Optional
import threading

class InMemoryTTLCache:
    """
    Stateless thread-safe in-memory cache with time-to-live expiration.
    No Redis or persistent database required.
    """
    def __init__(self, default_ttl_seconds: int = 900):
        self._cache: dict[str, tuple[float, Any]] = {}
        self._default_ttl = default_ttl_seconds
        self._lock = threading.Lock()

    def get(self, key: str) -> Optional[Any]:
        with self._lock:
            if key not in self._cache:
                return None
            expires_at, val = self._cache[key]
            if time.time() > expires_at:
                del self._cache[key]
                return None
            return val

    def set(self, key: str, value: Any, ttl_seconds: Optional[int] = None) -> None:
        ttl = ttl_seconds if ttl_seconds is not None else self._default_ttl
        expires_at = time.time() + ttl
        with self._lock:
            self._cache[key] = (expires_at, value)

    def delete(self, key: str) -> bool:
        with self._lock:
            if key in self._cache:
                del self._cache[key]
                return True
            return False

    def clear(self) -> None:
        with self._lock:
            self._cache.clear()

    def cleanup_expired(self) -> int:
        now = time.time()
        removed = 0
        with self._lock:
            expired_keys = [k for k, (exp, _) in self._cache.items() if now > exp]
            for k in expired_keys:
                del self._cache[k]
                removed += 1
        return removed

    def size(self) -> int:
        with self._lock:
            return len(self._cache)

cache = InMemoryTTLCache()
