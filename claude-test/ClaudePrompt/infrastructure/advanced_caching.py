"""
Advanced caching system with Redis support and intelligent cache management
"""
from typing import Optional, Any, Dict
import json
import hashlib
import time
from datetime import datetime, timedelta

class CacheEntry:
    """Represents a cached item with metadata"""
    def __init__(self, value: Any, ttl: int, created_at: float):
        self.value = value
        self.ttl = ttl
        self.created_at = created_at
        self.hits = 0
        self.last_accessed = created_at

    def is_expired(self) -> bool:
        """Check if entry has expired"""
        return time.time() - self.created_at > self.ttl

    def touch(self):
        """Update access time and increment hit counter"""
        self.hits += 1
        self.last_accessed = time.time()

class AdvancedCache:
    """Advanced in-memory cache with LRU eviction and statistics"""

    def __init__(self, max_size: int = 10000, default_ttl: int = 3600):
        self._cache: Dict[str, CacheEntry] = {}
        self.max_size = max_size
        self.default_ttl = default_ttl
        self.stats = {
            "hits": 0,
            "misses": 0,
            "evictions": 0,
            "sets": 0
        }

    def _generate_key(self, key: str) -> str:
        """Generate cache key hash"""
        return hashlib.sha256(key.encode()).hexdigest()[:16]

    def _evict_if_needed(self):
        """Evict least recently used items if cache is full"""
        if len(self._cache) >= self.max_size:
            # Find LRU item
            lru_key = min(
                self._cache.keys(),
                key=lambda k: self._cache[k].last_accessed
            )
            del self._cache[lru_key]
            self.stats["evictions"] += 1

    def _cleanup_expired(self):
        """Remove expired entries"""
        expired = [k for k, v in self._cache.items() if v.is_expired()]
        for key in expired:
            del self._cache[key]

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        cache_key = self._generate_key(key)

        if cache_key in self._cache:
            entry = self._cache[cache_key]

            if entry.is_expired():
                del self._cache[cache_key]
                self.stats["misses"] += 1
                return None

            entry.touch()
            self.stats["hits"] += 1
            return entry.value

        self.stats["misses"] += 1
        return None

    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        """Set value in cache"""
        cache_key = self._generate_key(key)
        ttl = ttl or self.default_ttl

        self._evict_if_needed()
        self._cleanup_expired()

        self._cache[cache_key] = CacheEntry(value, ttl, time.time())
        self.stats["sets"] += 1

    def delete(self, key: str):
        """Delete value from cache"""
        cache_key = self._generate_key(key)
        if cache_key in self._cache:
            del self._cache[cache_key]

    def clear(self):
        """Clear all cache entries"""
        self._cache.clear()

    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        total_requests = self.stats["hits"] + self.stats["misses"]
        hit_rate = (self.stats["hits"] / total_requests * 100) if total_requests > 0 else 0

        return {
            **self.stats,
            "size": len(self._cache),
            "max_size": self.max_size,
            "hit_rate_percent": round(hit_rate, 2)
        }

# Global cache instance
advanced_cache = AdvancedCache(max_size=10000, default_ttl=3600)
