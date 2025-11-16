"""
T4: Performance Benchmark Tests
Tests performance optimizations and detects regressions

COVERAGE:
- P1: Parallel guardrails benchmarks
- P2: Token counting performance
- P3: Overlapped iterations benchmarks
- Rate limiter performance
- Context manager performance
"""

import pytest
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from agent_framework.context_manager import ContextManager
from agent_framework.context_manager_optimized import OptimizedContextManager
from agent_framework.rate_limiter import RateLimiter


# ==========================================
# T4.1: P2 TOKEN COUNTING BENCHMARKS
# ==========================================

class TestTokenCountingPerformance:
    """Benchmark P2: Incremental token counting"""

    def test_token_counting_10_messages(self):
        """Benchmark token counting with 10 messages"""
        original = ContextManager(max_tokens=100000, compact_threshold=0.99)
        optimized = OptimizedContextManager(max_tokens=100000, compact_threshold=0.99)

        # Add 10 messages
        for i in range(10):
            original.add_message("user", f"Message {i} " * 50)
            optimized.add_message("user", f"Message {i} " * 50)

        # Benchmark original (O(n))
        start = time.time()
        for _ in range(100):
            _ = original.get_total_tokens()
        duration_original = time.time() - start

        # Benchmark optimized (O(1))
        start = time.time()
        for _ in range(100):
            _ = optimized.get_total_tokens()
        duration_optimized = time.time() - start

        # Calculate speedup
        speedup = duration_original / duration_optimized if duration_optimized > 0 else 1

        print(f"\n  10 messages, 100 calls:")
        print(f"    Original: {duration_original*1000:.2f}ms")
        print(f"    Optimized: {duration_optimized*1000:.2f}ms")
        print(f"    Speedup: {speedup:.1f}x")

        # Should be at least 5x faster
        assert speedup >= 5

    def test_token_counting_100_messages(self):
        """Benchmark token counting with 100 messages"""
        original = ContextManager(max_tokens=1000000, compact_threshold=0.99)
        optimized = OptimizedContextManager(max_tokens=1000000, compact_threshold=0.99)

        # Add 100 messages
        for i in range(100):
            original.add_message("user", f"Message {i} " * 20)
            optimized.add_message("user", f"Message {i} " * 20)

        # Benchmark
        start = time.time()
        for _ in range(100):
            _ = original.get_total_tokens()
        duration_original = time.time() - start

        start = time.time()
        for _ in range(100):
            _ = optimized.get_total_tokens()
        duration_optimized = time.time() - start

        speedup = duration_original / duration_optimized if duration_optimized > 0 else 1

        print(f"\n  100 messages, 100 calls:")
        print(f"    Original: {duration_original*1000:.2f}ms")
        print(f"    Optimized: {duration_optimized*1000:.2f}ms")
        print(f"    Speedup: {speedup:.1f}x")

        # Should be at least 50x faster
        assert speedup >= 50

    def test_token_counting_scalability(self):
        """Test token counting scales linearly with O(1)"""
        optimized = OptimizedContextManager(max_tokens=1000000, compact_threshold=0.99)

        # Add different numbers of messages and measure
        results = []

        for n_messages in [10, 50, 100, 200]:
            # Add messages
            for i in range(n_messages):
                optimized.add_message("user", f"Message {i}")

            # Benchmark token counting
            start = time.time()
            for _ in range(1000):
                _ = optimized.get_total_tokens()
            duration = time.time() - start

            results.append((n_messages, duration))
            print(f"  {n_messages} messages: {duration*1000:.2f}ms for 1000 calls")

        # With O(1), time should be relatively constant
        # Max variance should be < 2x
        durations = [d for _, d in results]
        min_duration = min(durations)
        max_duration = max(durations)
        variance = max_duration / min_duration if min_duration > 0 else 1

        print(f"  Variance: {variance:.2f}x (should be < 2x for O(1))")
        assert variance < 2


# ==========================================
# T4.2: RATE LIMITER PERFORMANCE
# ==========================================

class TestRateLimiterPerformance:
    """Benchmark rate limiter overhead"""

    def test_rate_limiter_overhead_under_limit(self):
        """Test rate limiter overhead when under limit"""
        limiter = RateLimiter(max_calls=1000, time_window=1)

        # Benchmark 1000 calls under limit
        start = time.time()
        for i in range(1000):
            limiter.wait_if_needed(verbose=False)
        duration = time.time() - start

        overhead_per_call = (duration / 1000) * 1000  # ms per call

        print(f"\n  1000 calls under limit:")
        print(f"    Total: {duration*1000:.2f}ms")
        print(f"    Per call: {overhead_per_call:.3f}ms")

        # Should be < 0.1ms per call
        assert overhead_per_call < 0.1

    def test_rate_limiter_blocking_accuracy(self):
        """Test rate limiter blocking is accurate"""
        limiter = RateLimiter(max_calls=10, time_window=1)

        # Use up limit
        for i in range(10):
            limiter.wait_if_needed()

        # Next call should block for ~1 second
        start = time.time()
        limiter.wait_if_needed()
        wait_duration = time.time() - start

        print(f"\n  Rate limit blocking:")
        print(f"    Expected: ~1.0s")
        print(f"    Actual: {wait_duration:.2f}s")

        # Should wait close to 1 second (±0.2s)
        assert 0.8 <= wait_duration <= 1.2


# ==========================================
# T4.3: CONTEXT COMPACTION PERFORMANCE
# ==========================================

class TestContextCompactionPerformance:
    """Benchmark context compaction"""

    def test_compaction_performance(self):
        """Test context compaction is fast"""
        context = OptimizedContextManager(
            max_tokens=5000,
            compact_threshold=0.7,
            keep_recent=5
        )

        # Add messages until compaction triggers
        n_messages = 0
        start = time.time()

        while len(context.compaction_log) == 0 and n_messages < 100:
            context.add_message("user", "Test message " * 20)
            n_messages += 1

        duration = time.time() - start

        print(f"\n  Context compaction:")
        print(f"    Messages added: {n_messages}")
        print(f"    Compactions: {len(context.compaction_log)}")
        print(f"    Duration: {duration*1000:.2f}ms")

        # Should compact within reasonable time
        assert duration < 0.5  # < 500ms

    def test_cache_validity_after_compaction(self):
        """Test cache remains valid after compaction"""
        context = OptimizedContextManager(
            max_tokens=1000,
            compact_threshold=0.6,
            keep_recent=3
        )

        # Trigger multiple compactions
        for i in range(50):
            context.add_message("user", "Test " * 20)

            # Cache should always be valid
            assert context.validate_cache()

        print(f"\n  Cache validity:")
        print(f"    Messages: 50")
        print(f"    Compactions: {len(context.compaction_log)}")
        print(f"    Cache valid: ✅")


# ==========================================
# T4.4: MEMORY USAGE BENCHMARKS
# ==========================================

class TestMemoryUsage:
    """Test memory efficiency"""

    def test_context_memory_with_compaction(self):
        """Test compaction reduces memory usage"""
        context = OptimizedContextManager(
            max_tokens=5000,
            compact_threshold=0.7,
            keep_recent=5
        )

        # Add many messages
        for i in range(100):
            context.add_message("user", "Test message " * 50)

        # Check compaction occurred
        assert len(context.compaction_log) > 0

        # Messages should be reduced
        assert len(context.messages) < 100

        print(f"\n  Memory efficiency:")
        print(f"    Messages added: 100")
        print(f"    Messages retained: {len(context.messages)}")
        print(f"    Reduction: {100 - len(context.messages)} messages")

    def test_rate_limiter_memory_efficiency(self):
        """Test rate limiter doesn't leak memory"""
        limiter = RateLimiter(max_calls=100, time_window=60)

        # Make many calls
        for i in range(1000):
            limiter.wait_if_needed()

        # Call deque should not grow unbounded
        # It should only store calls within window
        call_count = len(limiter.calls)

        print(f"\n  Rate limiter memory:")
        print(f"    Total calls: 1000")
        print(f"    Calls stored: {call_count}")
        print(f"    Expected: ~100 (within window)")

        # Should store roughly max_calls worth
        assert call_count <= 150  # Some margin


# ==========================================
# T4.5: REGRESSION DETECTION
# ==========================================

class TestRegressionDetection:
    """Detect performance regressions"""

    def test_no_token_counting_regression(self):
        """Ensure O(1) token counting hasn't regressed"""
        context = OptimizedContextManager(max_tokens=100000, compact_threshold=0.99)

        # Add 50 messages
        for i in range(50):
            context.add_message("user", f"Message {i} " * 20)

        # 1000 token count calls should be < 5ms
        start = time.time()
        for _ in range(1000):
            _ = context.get_total_tokens()
        duration = time.time() - start

        duration_ms = duration * 1000

        print(f"\n  Regression check (1000 calls):")
        print(f"    Duration: {duration_ms:.2f}ms")
        print(f"    Threshold: 5ms")
        print(f"    Status: {'✅ PASS' if duration_ms < 5 else '❌ REGRESSION'}")

        assert duration_ms < 5, f"Performance regression detected: {duration_ms:.2f}ms > 5ms"

    def test_no_rate_limiter_regression(self):
        """Ensure rate limiter overhead hasn't regressed"""
        limiter = RateLimiter(max_calls=10000, time_window=60)

        # 1000 calls under limit should be < 50ms
        start = time.time()
        for _ in range(1000):
            limiter.wait_if_needed(verbose=False)
        duration = time.time() - start

        duration_ms = duration * 1000

        print(f"\n  Regression check (1000 calls):")
        print(f"    Duration: {duration_ms:.2f}ms")
        print(f"    Threshold: 50ms")
        print(f"    Status: {'✅ PASS' if duration_ms < 50 else '❌ REGRESSION'}")

        assert duration_ms < 50, f"Performance regression detected: {duration_ms:.2f}ms > 50ms"


# ==========================================
# T4.6: STRESS TESTS
# ==========================================

class TestStress:
    """Stress test performance under load"""

    def test_context_manager_stress(self):
        """Stress test context manager with rapid additions"""
        context = OptimizedContextManager(max_tokens=100000, compact_threshold=0.9)

        start = time.time()

        # Rapid fire 1000 messages
        for i in range(1000):
            context.add_message("user", f"Message {i}")
            if i % 100 == 0:
                _ = context.get_total_tokens()

        duration = time.time() - start

        print(f"\n  Stress test (1000 messages):")
        print(f"    Duration: {duration:.2f}s")
        print(f"    Msgs/sec: {1000/duration:.0f}")
        print(f"    Cache valid: {context.validate_cache()}")

        # Should handle 1000 messages in < 1 second
        assert duration < 1.0
        assert context.validate_cache()

    def test_rate_limiter_stress(self):
        """Stress test rate limiter with many calls"""
        limiter = RateLimiter(max_calls=100, time_window=1)

        start = time.time()

        # Make 1000 calls (will rate limit)
        for i in range(1000):
            limiter.wait_if_needed(verbose=False)

        duration = time.time() - start

        print(f"\n  Stress test (1000 calls, limit 100/s):")
        print(f"    Duration: {duration:.2f}s")
        print(f"    Expected: ~10s (100/s * 10)")

        # Should take roughly 10 seconds
        assert 9 <= duration <= 11


# ==========================================
# RUN TESTS
# ==========================================

if __name__ == "__main__":
    print("=" * 70)
    print("T4: RUNNING PERFORMANCE TESTS")
    print("=" * 70)
    pytest.main([__file__, "-v", "-s", "--tb=short"])
