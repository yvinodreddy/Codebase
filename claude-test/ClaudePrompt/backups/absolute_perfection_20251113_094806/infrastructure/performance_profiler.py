#!/usr/bin/env python3
"""
Performance Profiling with cProfile
Profile code performance and identify bottlenecks
"""
import cProfile
import pstats
import io
from functools import wraps
from typing import Callable, Optional
import time


class PerformanceProfiler:
    """
    Performance profiler for identifying bottlenecks

    Example:
        profiler = PerformanceProfiler()

        @profiler.profile()
        def slow_function():
            # ... code ...

        # Or use as context manager
        with profiler:
            slow_function()

        profiler.print_stats()
    """

    def __init__(self):
        self.profiler = cProfile.Profile()
        self.is_profiling = False

    def start(self):
        """Start profiling"""
        self.profiler.enable()
        self.is_profiling = True

    def stop(self):
        """Stop profiling"""
        self.profiler.disable()
        self.is_profiling = False

    def print_stats(self, sort_by: str = "cumulative", limit: int = 20):
        """
        Print profiling statistics

        Args:
            sort_by: Sort method (cumulative, time, calls, etc.)
            limit: Number of functions to show
        """
        s = io.StringIO()
        stats = pstats.Stats(self.profiler, stream=s)
        stats.sort_stats(sort_by)
        stats.print_stats(limit)
        print(s.getvalue())

    def save_stats(self, filename: str):
        """Save stats to file"""
        self.profiler.dump_stats(filename)

    def profile(self):
        """
        Decorator to profile a function

        Example:
            @profiler.profile()
            def my_function():
                pass
        """
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs):
                self.start()
                try:
                    result = func(*args, **kwargs)
                    return result
                finally:
                    self.stop()
            return wrapper
        return decorator

    def __enter__(self):
        """Context manager entry"""
        self.start()
        return self

    def __exit__(self, *args):
        """Context manager exit"""
        self.stop()


def benchmark(func: Callable) -> Callable:
    """
    Simple benchmark decorator

    Example:
        @benchmark
        def my_function():
            pass
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start
        print(f"⏱️  {func.__name__} took {duration:.3f}s")
        return result
    return wrapper
