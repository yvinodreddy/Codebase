"""
Caching infrastructure (Redis ready)
"""
from typing import Optional, Dict
import json

class SimpleCache:
    """Simple in-memory cache (can be replaced with Redis)"""
    def __init__(self):
        self._cache: Dict[str, str] = {}

    def get(self, key: str) -> Optional[str]:
        return self._cache.get(key)

    def set(self, key: str, value: str, ttl: int = 3600):
        self._cache[key] = value

    def delete(self, key: str):
        self._cache.pop(key, None)

# Global cache instance
cache = SimpleCache()

if __name__ == "__main__":
    cache.set("test", "value")
    print("Cache:", cache.get("test"))
