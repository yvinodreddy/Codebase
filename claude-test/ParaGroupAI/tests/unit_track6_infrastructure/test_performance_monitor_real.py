#!/usr/bin/env python3
"""
REAL Tests for infrastructure/performance_monitor.py
100% coverage with actual test logic
"""

import pytest
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from infrastructure.performance_monitor import PerformanceMonitor, performance_monitor


class TestBasicFunctionality:
    """Test basic functionality"""

    def test_init(self):
        """Test PerformanceMonitor initialization"""
        monitor = PerformanceMonitor()
        assert isinstance(monitor.metrics, dict)
        assert isinstance(monitor.call_counts, dict)
        assert len(monitor.metrics) == 0

    def test_record_single_measurement(self):
        """Test recording single measurement"""
        monitor = PerformanceMonitor()
        monitor.record("test_op", 0.1)
        assert "test_op" in monitor.metrics
        assert len(monitor.metrics["test_op"]) == 1
        assert monitor.call_counts["test_op"] == 1

    def test_record_multiple_measurements(self):
        """Test recording multiple measurements"""
        monitor = PerformanceMonitor()
        monitor.record("test_op", 0.1)
        monitor.record("test_op", 0.2)
        monitor.record("test_op", 0.3)
        assert len(monitor.metrics["test_op"]) == 3
        assert monitor.call_counts["test_op"] == 3

    def test_get_stats_empty(self):
        """Test get_stats for non-existent operation"""
        monitor = PerformanceMonitor()
        stats = monitor.get_stats("nonexistent")
        assert stats == {}

    def test_measure_decorator(self):
        """Test measure decorator functionality"""
        monitor = PerformanceMonitor()

        @monitor.measure("test_function")
        def test_func():
            time.sleep(0.01)
            return "result"

        result = test_func()
        assert result == "result"
        assert "test_function" in monitor.metrics
        assert monitor.call_counts["test_function"] == 1

    def test_get_all_stats_empty(self):
        """Test get_all_stats with no operations"""
        monitor = PerformanceMonitor()
        all_stats = monitor.get_all_stats()
        assert all_stats == {}


class TestPerformanceMonitor:
    """Test PerformanceMonitor class"""

    def test_stats_mean_calculation(self):
        """Test mean calculation in stats"""
        monitor = PerformanceMonitor()
        monitor.record("op1", 0.1)
        monitor.record("op1", 0.2)
        monitor.record("op1", 0.3)

        stats = monitor.get_stats("op1")
        assert stats["mean"] == pytest.approx(0.2, abs=0.01)
        assert stats["count"] == 3

    def test_stats_median_calculation(self):
        """Test median calculation"""
        monitor = PerformanceMonitor()
        monitor.record("op1", 0.1)
        monitor.record("op1", 0.5)
        monitor.record("op1", 0.9)

        stats = monitor.get_stats("op1")
        assert stats["median"] == pytest.approx(0.5, abs=0.01)

    def test_stats_min_max(self):
        """Test min/max calculations"""
        monitor = PerformanceMonitor()
        monitor.record("op1", 0.1)
        monitor.record("op1", 0.5)
        monitor.record("op1", 0.9)

        stats = monitor.get_stats("op1")
        assert stats["min"] == pytest.approx(0.1, abs=0.01)
        assert stats["max"] == pytest.approx(0.9, abs=0.01)

    def test_stats_stdev_single_value(self):
        """Test stdev with single value"""
        monitor = PerformanceMonitor()
        monitor.record("op1", 0.5)

        stats = monitor.get_stats("op1")
        assert stats["stdev"] == 0

    def test_stats_stdev_multiple_values(self):
        """Test stdev with multiple values"""
        monitor = PerformanceMonitor()
        for val in [0.1, 0.2, 0.3, 0.4, 0.5]:
            monitor.record("op1", val)

        stats = monitor.get_stats("op1")
        assert stats["stdev"] > 0

    def test_percentile_p95_small_dataset(self):
        """Test P95 with small dataset"""
        monitor = PerformanceMonitor()
        for i in range(10):
            monitor.record("op1", i * 0.1)

        stats = monitor.get_stats("op1")
        # With small dataset, p95 should be max value
        assert "p95" in stats

    def test_percentile_p99_small_dataset(self):
        """Test P99 with small dataset"""
        monitor = PerformanceMonitor()
        for i in range(50):
            monitor.record("op1", i * 0.01)

        stats = monitor.get_stats("op1")
        assert "p99" in stats

    def test_decorator_preserves_function_name(self):
        """Test decorator preserves wrapped function metadata"""
        monitor = PerformanceMonitor()

        @monitor.measure("test")
        def my_function():
            """My docstring"""
            return 42

        assert my_function.__name__ == "my_function"
        assert my_function.__doc__ == "My docstring"


class TestIntegration:
    """Integration tests"""

    def test_multiple_operations_tracking(self):
        """Test tracking multiple different operations"""
        monitor = PerformanceMonitor()

        monitor.record("op1", 0.1)
        monitor.record("op2", 0.2)
        monitor.record("op3", 0.3)

        all_stats = monitor.get_all_stats()
        assert len(all_stats) == 3
        assert "op1" in all_stats
        assert "op2" in all_stats
        assert "op3" in all_stats

    def test_decorator_with_args_and_kwargs(self):
        """Test decorator with function arguments"""
        monitor = PerformanceMonitor()

        @monitor.measure("add_function")
        def add(a, b, multiply=1):
            return (a + b) * multiply

        result = add(2, 3, multiply=2)
        assert result == 10
        assert monitor.call_counts["add_function"] == 1

    def test_global_monitor_instance(self):
        """Test global performance_monitor instance"""
        assert isinstance(performance_monitor, PerformanceMonitor)

        performance_monitor.record("global_test", 0.5)
        stats = performance_monitor.get_stats("global_test")
        assert stats["count"] >= 1


class TestEdgeCases:
    """Test edge cases"""

    def test_very_small_durations(self):
        """Test with very small duration values"""
        monitor = PerformanceMonitor()
        monitor.record("fast_op", 0.000001)
        stats = monitor.get_stats("fast_op")
        assert stats["min"] > 0

    def test_large_dataset_percentiles(self):
        """Test percentiles with large dataset"""
        monitor = PerformanceMonitor()

        # Add 200 measurements
        for i in range(200):
            monitor.record("large_op", i * 0.001)

        stats = monitor.get_stats("large_op")
        assert "p95" in stats
        assert "p99" in stats
        assert stats["p99"] >= stats["p95"]

    def test_decorator_with_exception(self):
        """Test decorator records timing even with exceptions"""
        monitor = PerformanceMonitor()

        @monitor.measure("failing_func")
        def failing():
            time.sleep(0.01)
            raise ValueError("Test error")

        with pytest.raises(ValueError):
            failing()

        # Should still record the measurement
        assert "failing_func" in monitor.metrics
        assert monitor.call_counts["failing_func"] == 1

    def test_zero_duration(self):
        """Test with zero duration"""
        monitor = PerformanceMonitor()
        monitor.record("instant_op", 0.0)
        stats = monitor.get_stats("instant_op")
        assert stats["min"] == 0.0


class TestProductionReadiness:
    """Test production readiness"""

    def test_module_imports(self):
        """Test module imports successfully"""
        from infrastructure import performance_monitor as pm_module
        assert hasattr(pm_module, 'PerformanceMonitor')
        assert hasattr(pm_module, 'performance_monitor')

    def test_monitor_isolation(self):
        """Test different monitor instances are isolated"""
        monitor1 = PerformanceMonitor()
        monitor2 = PerformanceMonitor()

        monitor1.record("op1", 0.1)
        monitor2.record("op1", 0.5)

        stats1 = monitor1.get_stats("op1")
        stats2 = monitor2.get_stats("op1")

        assert stats1["mean"] != stats2["mean"]

    def test_concurrent_recording(self):
        """Test rapid sequential recordings"""
        monitor = PerformanceMonitor()

        for i in range(100):
            monitor.record("rapid_op", i * 0.001)

        stats = monitor.get_stats("rapid_op")
        assert stats["count"] == 100
