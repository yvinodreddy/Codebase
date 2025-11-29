#!/usr/bin/env python3
"""
Unit Tests for agent_framework/rate_limiter.py
Tests token bucket rate limiting for API calls.

Test Coverage Target: 90%+
"""

import pytest
import sys
import time
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agent_framework.rate_limiter import RateLimiter


# ==========================================
# INITIALIZATION TESTS
# ==========================================

class TestRateLimiterInit:
    """Test RateLimiter initialization."""

    def test_init_with_defaults(self):
        """RateLimiter should use config defaults."""
        limiter = RateLimiter()
        # Should use values from Config
        assert limiter.max_calls > 0
        assert limiter.time_window > 0
        assert len(limiter.calls) == 0

    def test_init_with_custom_values(self):
        """RateLimiter should accept custom values."""
        limiter = RateLimiter(max_calls=100, time_window=60)
        assert limiter.max_calls == 100
        assert limiter.time_window == 60

    def test_init_max_calls_only(self):
        """RateLimiter should accept max_calls only."""
        limiter = RateLimiter(max_calls=200)
        assert limiter.max_calls == 200
        assert limiter.time_window > 0  # From config

    def test_init_time_window_only(self):
        """RateLimiter should accept time_window only."""
        limiter = RateLimiter(time_window=120)
        assert limiter.max_calls > 0  # From config
        assert limiter.time_window == 120

    def test_calls_deque_initialized_empty(self):
        """Calls deque should be initialized empty."""
        limiter = RateLimiter()
        assert len(limiter.calls) == 0


# ==========================================
# WAIT_IF_NEEDED TESTS
# ==========================================

class TestWaitIfNeeded:
    """Test wait_if_needed method."""

    def test_first_call_no_wait(self):
        """First call should not wait."""
        limiter = RateLimiter(max_calls=5, time_window=10)
        wait_time = limiter.wait_if_needed()
        assert wait_time == 0.0

    def test_below_limit_no_wait(self):
        """Calls below limit should not wait."""
        limiter = RateLimiter(max_calls=5, time_window=10)

        for _ in range(4):  # 4 calls, below limit of 5
            wait_time = limiter.wait_if_needed()
            assert wait_time == 0.0

    def test_at_limit_waits(self):
        """Call at limit should wait."""
        limiter = RateLimiter(max_calls=3, time_window=2)

        # Make 3 calls (at limit)
        for _ in range(3):
            limiter.wait_if_needed()

        # 4th call should wait
        start = time.time()
        wait_time = limiter.wait_if_needed()
        elapsed = time.time() - start

        assert wait_time > 0
        assert elapsed >= wait_time * 0.9  # Allow 10% tolerance

    def test_verbose_mode_output(self):
        """Verbose mode should print messages."""
        limiter = RateLimiter(max_calls=2, time_window=10)

        with patch('sys.stdout') as mock_stdout:
            limiter.wait_if_needed(verbose=True)
            # Should print status message

    def test_calls_recorded(self):
        """Each call should be recorded."""
        limiter = RateLimiter(max_calls=10, time_window=60)

        assert len(limiter.calls) == 0
        limiter.wait_if_needed()
        assert len(limiter.calls) == 1
        limiter.wait_if_needed()
        assert len(limiter.calls) == 2

    def test_old_calls_removed(self):
        """Old calls outside time window should be removed."""
        limiter = RateLimiter(max_calls=5, time_window=1)  # 1 second window

        # Make first call
        limiter.wait_if_needed()
        assert len(limiter.calls) == 1

        # Wait for window to expire
        time.sleep(1.1)

        # Make another call - should clean up old call
        limiter.wait_if_needed()
        assert len(limiter.calls) == 1  # Only new call


# ==========================================
# GET_CURRENT_USAGE TESTS
# ==========================================

class TestGetCurrentUsage:
    """Test get_current_usage method."""

    def test_initial_usage_zero(self):
        """Initial usage should be zero."""
        limiter = RateLimiter(max_calls=100, time_window=60)
        stats = limiter.get_current_usage()

        assert stats['current_calls'] == 0
        assert stats['max_calls'] == 100
        assert stats['calls_remaining'] == 100
        assert stats['usage_percent'] == 0.0
        assert stats['time_window_seconds'] == 60

    def test_usage_after_calls(self):
        """Usage should reflect actual calls."""
        limiter = RateLimiter(max_calls=10, time_window=60)

        # Make 3 calls
        for _ in range(3):
            limiter.wait_if_needed()

        stats = limiter.get_current_usage()
        assert stats['current_calls'] == 3
        assert stats['calls_remaining'] == 7
        assert stats['usage_percent'] == 30.0

    def test_usage_at_limit(self):
        """Usage at limit should be 100%."""
        limiter = RateLimiter(max_calls=5, time_window=60)

        # Make 5 calls (at limit)
        for _ in range(5):
            limiter.wait_if_needed()

        stats = limiter.get_current_usage()
        assert stats['current_calls'] == 5
        assert stats['calls_remaining'] == 0
        assert stats['usage_percent'] == 100.0

    def test_rate_calculation(self):
        """Rate per minute should be calculated correctly."""
        limiter = RateLimiter(max_calls=100, time_window=60)
        stats = limiter.get_current_usage()

        # Max rate should be 100 calls per 60 seconds = 100 calls/min
        assert stats['max_rate_per_minute'] == 100.0

    def test_stats_keys_present(self):
        """All expected keys should be present in stats."""
        limiter = RateLimiter()
        stats = limiter.get_current_usage()

        expected_keys = [
            'current_calls',
            'max_calls',
            'calls_remaining',
            'usage_percent',
            'time_window_seconds',
            'current_rate_per_minute',
            'max_rate_per_minute',
        ]

        for key in expected_keys:
            assert key in stats

    def test_stats_cleans_old_calls(self):
        """get_current_usage should clean up old calls."""
        limiter = RateLimiter(max_calls=10, time_window=1)

        # Make call
        limiter.wait_if_needed()
        assert limiter.get_current_usage()['current_calls'] == 1

        # Wait for window to expire
        time.sleep(1.1)

        # Stats should show 0 calls
        stats = limiter.get_current_usage()
        assert stats['current_calls'] == 0


# ==========================================
# RESET TESTS
# ==========================================

class TestReset:
    """Test reset method."""

    def test_reset_clears_calls(self):
        """Reset should clear all calls."""
        limiter = RateLimiter(max_calls=10, time_window=60)

        # Make some calls
        for _ in range(5):
            limiter.wait_if_needed()

        assert len(limiter.calls) == 5

        # Reset
        limiter.reset()

        assert len(limiter.calls) == 0

    def test_reset_allows_immediate_calls(self):
        """After reset, calls should be allowed immediately."""
        limiter = RateLimiter(max_calls=2, time_window=60)

        # Fill up limit
        for _ in range(2):
            limiter.wait_if_needed()

        # Reset
        limiter.reset()

        # Should be able to make calls immediately
        wait_time = limiter.wait_if_needed()
        assert wait_time == 0.0

    def test_reset_usage_zero(self):
        """After reset, usage should be zero."""
        limiter = RateLimiter(max_calls=10, time_window=60)

        # Make calls
        for _ in range(5):
            limiter.wait_if_needed()

        # Reset
        limiter.reset()

        # Check usage
        stats = limiter.get_current_usage()
        assert stats['current_calls'] == 0
        assert stats['usage_percent'] == 0.0


# ==========================================
# INTEGRATION TESTS
# ==========================================

class TestRateLimiterIntegration:
    """Test real-world rate limiting scenarios."""

    def test_burst_then_wait(self):
        """Test burst of calls followed by waiting."""
        limiter = RateLimiter(max_calls=3, time_window=2)

        # Burst 3 calls (should be instant)
        for i in range(3):
            wait_time = limiter.wait_if_needed()
            assert wait_time == 0.0

        # 4th call should wait
        wait_time = limiter.wait_if_needed()
        assert wait_time > 0

    def test_sliding_window_behavior(self):
        """Test sliding window allows calls as old ones expire."""
        limiter = RateLimiter(max_calls=2, time_window=1)

        # Make 2 calls
        limiter.wait_if_needed()
        limiter.wait_if_needed()

        # Wait for half the window
        time.sleep(0.6)

        # Third call should still wait (window hasn't fully expired)
        start = time.time()
        limiter.wait_if_needed()
        elapsed = time.time() - start
        assert elapsed > 0.3  # Should wait ~0.4s more

    def test_sustained_rate(self):
        """Test sustained call rate stays within limits."""
        limiter = RateLimiter(max_calls=5, time_window=1)

        call_times = []

        # Make 10 calls
        for _ in range(10):
            start = time.time()
            limiter.wait_if_needed()
            call_times.append(time.time() - start)

        # First 5 should be instant, next 5 should wait
        assert sum(call_times[:5]) < 0.1  # First 5 fast
        assert sum(call_times[5:]) > 0.5  # Next 5 had to wait

    def test_concurrent_usage_stats(self):
        """Test getting stats while making calls."""
        limiter = RateLimiter(max_calls=10, time_window=60)

        for i in range(1, 6):
            limiter.wait_if_needed()
            stats = limiter.get_current_usage()
            assert stats['current_calls'] == i
            assert stats['calls_remaining'] == 10 - i

    def test_zero_calls_remaining_blocks(self):
        """Test that zero calls remaining causes blocking."""
        limiter = RateLimiter(max_calls=2, time_window=2)

        # Fill limit
        limiter.wait_if_needed()
        limiter.wait_if_needed()

        stats = limiter.get_current_usage()
        assert stats['calls_remaining'] == 0

        # Next call should wait
        wait_time = limiter.wait_if_needed()
        assert wait_time > 0


# ==========================================
# EDGE CASE TESTS
# ==========================================

class TestRateLimiterEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_single_call_limit(self):
        """Test with max_calls=1."""
        limiter = RateLimiter(max_calls=1, time_window=1)

        limiter.wait_if_needed()

        # Second call should wait
        wait_time = limiter.wait_if_needed()
        assert wait_time > 0

    def test_very_short_window(self):
        """Test with very short time window."""
        limiter = RateLimiter(max_calls=2, time_window=0.5)

        limiter.wait_if_needed()
        limiter.wait_if_needed()

        # Third should wait
        wait_time = limiter.wait_if_needed()
        assert wait_time > 0

    def test_large_limit(self):
        """Test with large limit (shouldn't wait)."""
        limiter = RateLimiter(max_calls=1000, time_window=60)

        # Make 10 calls (well below limit)
        for _ in range(10):
            wait_time = limiter.wait_if_needed()
            assert wait_time == 0.0

    def test_multiple_resets(self):
        """Test multiple consecutive resets."""
        limiter = RateLimiter(max_calls=5, time_window=60)

        for _ in range(3):
            limiter.wait_if_needed()

        limiter.reset()
        limiter.reset()  # Second reset

        assert len(limiter.calls) == 0


# Pytest marker for unit tests
pytestmark = pytest.mark.unit


if __name__ == "__main__":
    # Allow running tests directly
    pytest.main([__file__, "-v"])
