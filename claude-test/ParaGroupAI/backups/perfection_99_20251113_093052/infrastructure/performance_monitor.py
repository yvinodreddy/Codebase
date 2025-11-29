"""
Advanced performance monitoring and profiling
"""
import time
import functools
from typing import Dict, List, Any
from collections import defaultdict
import statistics

class PerformanceMonitor:
    """Track and analyze performance metrics"""

    def __init__(self):
        self.metrics: Dict[str, List[float]] = defaultdict(list)
        self.call_counts: Dict[str, int] = defaultdict(int)

    def measure(self, operation_name: str):
        """Decorator to measure operation performance"""
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                start = time.time()
                try:
                    result = func(*args, **kwargs)
                    return result
                finally:
                    duration = time.time() - start
                    self.record(operation_name, duration)
            return wrapper
        return decorator

    def record(self, operation: str, duration: float):
        """Record a performance measurement"""
        self.metrics[operation].append(duration)
        self.call_counts[operation] += 1

    def get_stats(self, operation: str) -> Dict[str, Any]:
        """Get statistics for an operation"""
        if operation not in self.metrics or not self.metrics[operation]:
            return {}

        durations = self.metrics[operation]
        return {
            "count": self.call_counts[operation],
            "mean": statistics.mean(durations),
            "median": statistics.median(durations),
            "min": min(durations),
            "max": max(durations),
            "stdev": statistics.stdev(durations) if len(durations) > 1 else 0,
            "p95": statistics.quantiles(durations, n=20)[18] if len(durations) > 19 else max(durations),
            "p99": statistics.quantiles(durations, n=100)[98] if len(durations) > 99 else max(durations)
        }

    def get_all_stats(self) -> Dict[str, Dict[str, Any]]:
        """Get statistics for all operations"""
        return {op: self.get_stats(op) for op in self.metrics.keys()}

# Global monitor instance
performance_monitor = PerformanceMonitor()
