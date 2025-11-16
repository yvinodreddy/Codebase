#!/usr/bin/env python3
"""
Response Caching with diskcache
High-performance disk-based cache for API responses (<50ms access time)
"""
import hashlib
import json
from typing import Any, Optional, Callable
from functools import wraps
import time
try:
    from diskcache import Cache
except ImportError:
    print("⚠️  diskcache not installed. Run: pip install diskcache")
    Cache = None


class ResponseCache:
    """
    High-performance disk cache for API responses

    Features:
    - Sub-50ms access time
    - Automatic eviction (LRU)
    - TTL support
    - Size limits

    Example:
        cache = ResponseCache(cache_dir=".cache")

        @cache.cached(ttl=3600)
        def expensive_operation(prompt):
            return call_api(prompt)
    """

    def __init__(
        self,
        cache_dir: str = ".cache/responses",
        size_limit: int = 1_000_000_000,  # 1GB
        eviction_policy: str = "least-recently-used"
    ):
        if Cache is None:
            raise ImportError("diskcache not installed")

        self.cache = Cache(
            cache_dir,
            size_limit=size_limit,
            eviction_policy=eviction_policy
        )

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        start = time.time()
        value = self.cache.get(key)
        duration = (time.time() - start) * 1000  # Convert to ms

        if value is not None and duration > 50:
            print(f"⚠️  Cache access took {duration:.1f}ms (target: <50ms)")

        return value

    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        """Set value in cache with optional TTL"""
        self.cache.set(key, value, expire=ttl)

    def delete(self, key: str):
        """Delete key from cache"""
        self.cache.delete(key)

    def clear(self):
        """Clear entire cache"""
        self.cache.clear()

    def cached(self, ttl: Optional[int] = 3600):
        """
        Decorator to cache function results

        Args:
            ttl: Time-to-live in seconds (default: 1 hour)

        Example:
            @cache.cached(ttl=3600)
            def expensive_function(arg1, arg2):
                return do_work(arg1, arg2)
        """
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs):
                # Generate cache key from function name and arguments
                key_data = {
                    "func": func.__name__,
                    "args": args,
                    "kwargs": kwargs
                }
                key_str = json.dumps(key_data, sort_keys=True)
                cache_key = hashlib.sha256(key_str.encode()).hexdigest()

                # Try to get from cache
                cached_value = self.get(cache_key)
                if cached_value is not None:
                    return cached_value

                # Execute function and cache result
                result = func(*args, **kwargs)
                self.set(cache_key, result, ttl=ttl)
                return result

            return wrapper
        return decorator

    def stats(self) -> dict:
        """Get cache statistics"""
        return {
            "size": len(self.cache),
            "volume": self.cache.volume(),
            "hits": getattr(self.cache, "hits", 0),
            "misses": getattr(self.cache, "misses", 0),
        }


# Global cache instance
_global_cache = None


def get_cache() -> ResponseCache:
    """Get global cache instance"""
    global _global_cache
    if _global_cache is None:
        _global_cache = ResponseCache()
    return _global_cache
