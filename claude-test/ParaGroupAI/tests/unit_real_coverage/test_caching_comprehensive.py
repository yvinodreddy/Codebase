#!/usr/bin/env python3
"""
Comprehensive tests for infrastructure/caching.py
Target: 95%+ code coverage with REAL CODE tests (not mocks)
"""
import pytest
import sys
from pathlib import Path

# Add parent directory to path so we can import the module
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from infrastructure.caching import SimpleCache, cache


class TestSimpleCache:
    """Test the SimpleCache class with real code execution"""

    def test_initialization(self):
        """Test that SimpleCache initializes with empty cache"""
        test_cache = SimpleCache()
        assert test_cache._cache == {}

    def test_set_and_get_basic(self):
        """Test basic set and get operations"""
        test_cache = SimpleCache()
        test_cache.set("key1", "value1")

        assert test_cache.get("key1") == "value1"

    def test_set_with_ttl_parameter(self):
        """Test set operation with TTL parameter (currently ignored but should accept it)"""
        test_cache = SimpleCache()

        # TTL is accepted but not enforced in simple implementation
        test_cache.set("key_with_ttl", "value_with_ttl", ttl=1800)

        assert test_cache.get("key_with_ttl") == "value_with_ttl"

    def test_set_default_ttl(self):
        """Test set operation uses default TTL when not specified"""
        test_cache = SimpleCache()

        # Should work with default TTL (3600)
        test_cache.set("default_ttl_key", "default_ttl_value")

        assert test_cache.get("default_ttl_key") == "default_ttl_value"

    def test_get_nonexistent_key(self):
        """Test get returns None for non-existent keys"""
        test_cache = SimpleCache()

        result = test_cache.get("nonexistent")

        assert result is None

    def test_get_empty_cache(self):
        """Test get on empty cache returns None"""
        test_cache = SimpleCache()

        assert test_cache.get("any_key") is None

    def test_set_overwrites_existing_value(self):
        """Test that set overwrites existing value for same key"""
        test_cache = SimpleCache()
        test_cache.set("key", "value1")
        test_cache.set("key", "value2")

        assert test_cache.get("key") == "value2"

    def test_delete_existing_key(self):
        """Test delete removes existing key"""
        test_cache = SimpleCache()
        test_cache.set("key_to_delete", "value")

        test_cache.delete("key_to_delete")

        assert test_cache.get("key_to_delete") is None

    def test_delete_nonexistent_key(self):
        """Test delete on non-existent key doesn't raise error"""
        test_cache = SimpleCache()

        # Should not raise error
        test_cache.delete("nonexistent")

        # Cache should still be empty
        assert test_cache._cache == {}

    def test_delete_from_empty_cache(self):
        """Test delete on empty cache doesn't raise error"""
        test_cache = SimpleCache()

        # Should not raise error
        test_cache.delete("any_key")

        assert test_cache._cache == {}

    def test_multiple_keys(self):
        """Test cache handles multiple keys correctly"""
        test_cache = SimpleCache()
        test_cache.set("key1", "value1")
        test_cache.set("key2", "value2")
        test_cache.set("key3", "value3")

        assert test_cache.get("key1") == "value1"
        assert test_cache.get("key2") == "value2"
        assert test_cache.get("key3") == "value3"

    def test_cache_isolation(self):
        """Test that different cache instances are isolated"""
        cache1 = SimpleCache()
        cache2 = SimpleCache()

        cache1.set("key", "value1")
        cache2.set("key", "value2")

        assert cache1.get("key") == "value1"
        assert cache2.get("key") == "value2"

    def test_empty_string_value(self):
        """Test cache can store empty string"""
        test_cache = SimpleCache()
        test_cache.set("empty", "")

        assert test_cache.get("empty") == ""

    def test_special_characters_in_key(self):
        """Test cache handles special characters in keys"""
        test_cache = SimpleCache()
        special_key = "key:with:colons:and-dashes_and.dots"

        test_cache.set(special_key, "value")

        assert test_cache.get(special_key) == "value"

    def test_special_characters_in_value(self):
        """Test cache handles special characters in values"""
        test_cache = SimpleCache()
        special_value = "value!@#$%^&*()_+-=[]{}|;':\",./<>?"

        test_cache.set("key", special_value)

        assert test_cache.get("key") == special_value

    def test_unicode_in_key_and_value(self):
        """Test cache handles unicode characters"""
        test_cache = SimpleCache()
        unicode_key = "key_你好_🌍"
        unicode_value = "value_世界_🎉"

        test_cache.set(unicode_key, unicode_value)

        assert test_cache.get(unicode_key) == unicode_value

    def test_very_long_value(self):
        """Test cache handles very long values"""
        test_cache = SimpleCache()
        long_value = "x" * 10000

        test_cache.set("long", long_value)

        assert test_cache.get("long") == long_value
        assert len(test_cache.get("long")) == 10000


class TestGlobalCacheInstance:
    """Test the global cache instance"""

    def test_global_cache_exists(self):
        """Test that global cache instance is created"""
        from infrastructure.caching import cache

        assert isinstance(cache, SimpleCache)

    def test_global_cache_is_singleton(self):
        """Test that multiple imports get same cache instance"""
        from infrastructure.caching import cache as cache1
        from infrastructure.caching import cache as cache2

        assert cache1 is cache2

    def test_global_cache_functionality(self):
        """Test global cache works correctly"""
        from infrastructure.caching import cache

        # Clear any existing data
        cache._cache.clear()

        cache.set("test_key", "test_value")
        assert cache.get("test_key") == "test_value"

        cache.delete("test_key")
        assert cache.get("test_key") is None


class TestMainBlock:
    """Test the main block command-line interface"""

    def test_main_via_subprocess(self):
        """Test main block execution via subprocess"""
        import subprocess

        result = subprocess.run(
            [sys.executable, 'infrastructure/caching.py'],
            capture_output=True,
            text=True,
            cwd='/home/user01/claude-test/ClaudePrompt'
        )

        assert result.returncode == 0
        assert "Cache:" in result.stdout
        assert "value" in result.stdout


class TestEdgeCases:
    """Test edge cases and boundary conditions"""

    def test_numeric_string_as_value(self):
        """Test cache stores numeric strings as strings"""
        test_cache = SimpleCache()
        test_cache.set("number", "12345")

        result = test_cache.get("number")

        assert result == "12345"
        assert isinstance(result, str)

    def test_whitespace_only_value(self):
        """Test cache handles whitespace-only values"""
        test_cache = SimpleCache()
        test_cache.set("whitespace", "   \t\n   ")

        assert test_cache.get("whitespace") == "   \t\n   "

    def test_newlines_in_value(self):
        """Test cache preserves newlines in values"""
        test_cache = SimpleCache()
        multiline_value = "line1\nline2\nline3"

        test_cache.set("multiline", multiline_value)

        assert test_cache.get("multiline") == multiline_value

    def test_sequential_operations(self):
        """Test sequential cache operations"""
        test_cache = SimpleCache()

        test_cache.set("key1", "value1")
        test_cache.set("key2", "value2")
        assert test_cache.get("key1") == "value1"

        test_cache.delete("key1")
        assert test_cache.get("key1") is None
        assert test_cache.get("key2") == "value2"

        test_cache.set("key1", "new_value")
        assert test_cache.get("key1") == "new_value"
