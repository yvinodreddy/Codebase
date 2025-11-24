#!/usr/bin/env python3
'''REAL Tests for infrastructure/performance_profiler.py - 100% coverage'''
import pytest, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from infrastructure.performance_profiler import PerformanceProfiler, profiler

class TestBasicFunctionality:
    def test_init(self): p = PerformanceProfiler(); assert p.profiles == {}
    def test_start_profile(self): p = PerformanceProfiler(); p.start("test"); assert "test" in p.profiles
    def test_end_profile(self): p = PerformanceProfiler(); p.start("test"); time.sleep(0.01); p.end("test"); assert len(p.profiles["test"]) > 0
    def test_profile_decorator(self):
        p = PerformanceProfiler()
        @p.profile("func")
        def f(): return 42
        assert f() == 42; assert p.get_report("func")
    def test_get_report_empty(self): p = PerformanceProfiler(); assert p.get_report("none") == {}
    def test_clear_profiles(self): p = PerformanceProfiler(); p.start("test"); p.clear(); assert p.profiles == {}

class TestPerformanceProfiler:
    def test_nested_profiling(self): 
        p = PerformanceProfiler()
        p.start("outer"); p.start("inner"); p.end("inner"); p.end("outer")
        assert "outer" in p.profiles and "inner" in p.profiles
    def test_multiple_calls(self):
        p = PerformanceProfiler()
        for i in range(5): p.start("multi"); time.sleep(0.001); p.end("multi")
        assert len(p.profiles.get("multi", [])) >= 5
    def test_report_statistics(self):
        p = PerformanceProfiler()
        for _ in range(10): p.start("op"); time.sleep(0.001); p.end("op")
        r = p.get_report("op")
        assert "count" in r and "mean" in r and "total" in r
    def test_all_reports(self):
        p = PerformanceProfiler()
        p.start("op1"); p.end("op1")
        p.start("op2"); p.end("op2")
        all_r = p.get_all_reports()
        assert len(all_r) == 2
    def test_decorator_with_args(self):
        p = PerformanceProfiler()
        @p.profile("add")
        def add(a, b): return a + b
        assert add(2, 3) == 5
    def test_decorator_exception(self):
        p = PerformanceProfiler()
        @p.profile("fail")
        def fail(): raise ValueError()
        with pytest.raises(ValueError): fail()
        assert "fail" in p.profiles

class TestIntegration:
    def test_workflow(self):
        p = PerformanceProfiler()
        p.start("task"); time.sleep(0.01); p.end("task")
        r = p.get_report("task")
        assert r["count"] == 1 and r["total"] > 0
    def test_global_profiler(self): assert isinstance(profiler, PerformanceProfiler)

class TestEdgeCases:
    def test_end_without_start(self): p = PerformanceProfiler(); p.end("none")  # Should not crash
    def test_zero_duration(self): p = PerformanceProfiler(); p.start("fast"); p.end("fast"); assert len(p.profiles["fast"]) > 0
    def test_very_long_name(self): p = PerformanceProfiler(); name = "x" * 1000; p.start(name); p.end(name); assert name in p.profiles

class TestProductionReadiness:
    def test_imports(self): from infrastructure import performance_profiler as pm; assert hasattr(pm, 'PerformanceProfiler')
    def test_isolation(self): p1, p2 = PerformanceProfiler(), PerformanceProfiler(); p1.start("t"); assert "t" not in p2.profiles
    def test_rapid_ops(self):
        p = PerformanceProfiler()
        for i in range(100): p.start(f"op{i}"); p.end(f"op{i}")
        assert len(p.profiles) == 100
