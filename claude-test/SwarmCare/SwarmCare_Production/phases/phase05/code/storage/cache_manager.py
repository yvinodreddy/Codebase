"""
Audio Cache Manager
In-memory and disk caching for frequently accessed audio
"""

from typing import Optional, Dict
from dataclasses import dataclass
from datetime import datetime, timedelta
import hashlib
import logging

logger = logging.getLogger(__name__)


@dataclass
class CacheEntry:
    """Cache entry"""
    key: str
    data: bytes
    created_at: datetime
    accessed_at: datetime
    access_count: int
    size_bytes: int
    ttl_seconds: int


class CacheManager:
    """
    Two-tier cache manager for audio files

    Tiers:
    1. Memory cache (hot data, fast access)
    2. Disk cache (warm data, moderate access)
    """

    def __init__(self, max_memory_mb: int = 100, max_disk_gb: int = 10, default_ttl: int = 3600):
        self.max_memory_bytes = max_memory_mb * 1024 * 1024
        self.max_disk_bytes = max_disk_gb * 1024 * 1024 * 1024
        self.default_ttl = default_ttl
        self.memory_cache: Dict[str, CacheEntry] = {}
        self.disk_cache: Dict[str, CacheEntry] = {}
        self.logger = logging.getLogger(__name__)

    def get(self, key: str) -> Optional[bytes]:
        """
        Get audio from cache

        Args:
            key: Cache key

        Returns:
            Audio data or None if not found
        """
        # Check memory cache first
        if key in self.memory_cache:
            entry = self.memory_cache[key]
            if not self._is_expired(entry):
                entry.accessed_at = datetime.now()
                entry.access_count += 1
                self.logger.debug(f"Memory cache HIT: {key}")
                return entry.data
            else:
                del self.memory_cache[key]

        # Check disk cache
        if key in self.disk_cache:
            entry = self.disk_cache[key]
            if not self._is_expired(entry):
                entry.accessed_at = datetime.now()
                entry.access_count += 1
                # Promote to memory cache if frequently accessed
                if entry.access_count > 5:
                    self._promote_to_memory(key, entry)
                self.logger.debug(f"Disk cache HIT: {key}")
                return entry.data
            else:
                del self.disk_cache[key]

        self.logger.debug(f"Cache MISS: {key}")
        return None

    def set(self, key: str, data: bytes, ttl: Optional[int] = None):
        """
        Store audio in cache

        Args:
            key: Cache key
            data: Audio data
            ttl: Time to live in seconds
        """
        ttl = ttl or self.default_ttl
        entry = CacheEntry(
            key=key,
            data=data,
            created_at=datetime.now(),
            accessed_at=datetime.now(),
            access_count=0,
            size_bytes=len(data),
            ttl_seconds=ttl
        )

        # Try memory cache first
        if self._can_fit_in_memory(len(data)):
            self.memory_cache[key] = entry
            self.logger.debug(f"Cached in memory: {key} ({len(data)} bytes)")
        # Otherwise use disk cache
        elif self._can_fit_in_disk(len(data)):
            self.disk_cache[key] = entry
            self.logger.debug(f"Cached on disk: {key} ({len(data)} bytes)")
        else:
            self.logger.warning(f"Cache full, evicting LRU entries")
            self._evict_lru()
            self.set(key, data, ttl)  # Retry after eviction

    def delete(self, key: str):
        """Delete from cache"""
        if key in self.memory_cache:
            del self.memory_cache[key]
        if key in self.disk_cache:
            del self.disk_cache[key]

    def clear(self):
        """Clear all caches"""
        self.memory_cache.clear()
        self.disk_cache.clear()
        self.logger.info("Cache cleared")

    def get_stats(self) -> Dict:
        """Get cache statistics"""
        memory_size = sum(e.size_bytes for e in self.memory_cache.values())
        disk_size = sum(e.size_bytes for e in self.disk_cache.values())

        return {
            'memory_entries': len(self.memory_cache),
            'disk_entries': len(self.disk_cache),
            'memory_size_mb': memory_size / (1024 * 1024),
            'disk_size_mb': disk_size / (1024 * 1024),
            'memory_utilization_pct': (memory_size / self.max_memory_bytes) * 100,
            'disk_utilization_pct': (disk_size / self.max_disk_bytes) * 100
        }

    def _is_expired(self, entry: CacheEntry) -> bool:
        """Check if entry is expired"""
        age = (datetime.now() - entry.created_at).total_seconds()
        return age > entry.ttl_seconds

    def _can_fit_in_memory(self, size: int) -> bool:
        """Check if data can fit in memory cache"""
        current_size = sum(e.size_bytes for e in self.memory_cache.values())
        return (current_size + size) <= self.max_memory_bytes

    def _can_fit_in_disk(self, size: int) -> bool:
        """Check if data can fit in disk cache"""
        current_size = sum(e.size_bytes for e in self.disk_cache.values())
        return (current_size + size) <= self.max_disk_bytes

    def _promote_to_memory(self, key: str, entry: CacheEntry):
        """Promote entry from disk to memory cache"""
        if self._can_fit_in_memory(entry.size_bytes):
            self.memory_cache[key] = entry
            del self.disk_cache[key]
            self.logger.debug(f"Promoted to memory: {key}")

    def _evict_lru(self):
        """Evict least recently used entries"""
        # Evict from memory cache
        if self.memory_cache:
            lru_key = min(self.memory_cache.keys(),
                         key=lambda k: self.memory_cache[k].accessed_at)
            del self.memory_cache[lru_key]
            self.logger.debug(f"Evicted from memory: {lru_key}")

        # Evict from disk cache
        if self.disk_cache:
            lru_key = min(self.disk_cache.keys(),
                         key=lambda k: self.disk_cache[k].accessed_at)
            del self.disk_cache[lru_key]
            self.logger.debug(f"Evicted from disk: {lru_key}")

    def cleanup_expired(self) -> int:
        """Remove expired entries"""
        removed = 0

        # Clean memory cache
        expired_memory = [k for k, v in self.memory_cache.items() if self._is_expired(v)]
        for key in expired_memory:
            del self.memory_cache[key]
            removed += 1

        # Clean disk cache
        expired_disk = [k for k, v in self.disk_cache.items() if self._is_expired(v)]
        for key in expired_disk:
            del self.disk_cache[key]
            removed += 1

        if removed > 0:
            self.logger.info(f"Cleaned up {removed} expired cache entries")

        return removed
