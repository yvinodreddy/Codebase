"""
Latency Tracking Module (Purpose 1 & 2 ONLY)
Purpose 1: Performance Regression Detection
Purpose 2: Bottleneck Identification
NOT Purpose 3: SLA Guarantees (rejected - can force quality compromises)
"""

import time
import json
import numpy as np
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict


@dataclass
class LatencyMetric:
    """Single latency measurement."""
    timestamp: str
    prompt_type: str
    time_to_99_percent: float  # NOT time to first response
    iterations_used: int
    final_confidence: float  # Always targeting 99.0%
    bottlenecks: Dict[str, float]  # Component timings


class LatencyTracker:
    """
    Track time to reach 99% confidence (NOT time to any response).

    Purpose 1: Detect performance regressions over time
    Purpose 2: Identify bottlenecks for optimization

    NOT tracking time to first response or SLA compliance.
    """

    def __init__(self, baseline_p99: Optional[float] = None):
        self.metrics: List[LatencyMetric] = []
        self.baseline_p99 = baseline_p99
        self.log_dir = Path("logs/latency")
        self.log_dir.mkdir(parents=True, exist_ok=True)

    def record_execution(
        self,
        prompt: str,
        time_to_99_percent: float,
        iterations: int,
        bottlenecks: Optional[Dict[str, float]] = None
    ):
        """Record how long it took to reach 99% confidence."""
        metric = LatencyMetric(
            timestamp=datetime.utcnow().isoformat(),
            prompt_type=self._classify_prompt(prompt),
            time_to_99_percent=time_to_99_percent,
            iterations_used=iterations,
            final_confidence=99.0,  # Always targeting 99%
            bottlenecks=bottlenecks or {}
        )
        self.metrics.append(metric)
        self._save_metric(metric)

    def get_percentiles(self) -> Dict[str, float]:
        """Calculate p50/p95/p99 for time to 99% confidence."""
        if not self.metrics:
            return {"p50": 0, "p95": 0, "p99": 0, "count": 0}

        times = [m.time_to_99_percent for m in self.metrics]
        return {
            "p50": float(np.percentile(times, 50)),  # Median
            "p95": float(np.percentile(times, 95)),
            "p99": float(np.percentile(times, 99)),
            "count": len(times)
        }

    def detect_regression(self) -> Optional[Dict[str, any]]:
        """
        Purpose 1: Detect if performance degraded vs baseline.
        Alert if current p99 is significantly worse.
        """
        if not self.baseline_p99 or not self.metrics:
            return None

        current = self.get_percentiles()
        current_p99 = current["p99"]

        # Alert if 50% slower than baseline
        if current_p99 > self.baseline_p99 * 1.5:
            return {
                "alert": "PERFORMANCE_REGRESSION",
                "baseline_p99": self.baseline_p99,
                "current_p99": current_p99,
                "degradation_percent": ((current_p99 / self.baseline_p99) - 1) * 100,
                "recommendation": "Investigate what changed. Profile execution to find bottleneck."
            }
        return None

    def identify_bottlenecks(self) -> Dict[str, Dict[str, float]]:
        """
        Purpose 2: Find which components are slow.
        Returns average time spent in each component.
        """
        if not self.metrics:
            return {}

        # Aggregate bottleneck timings
        component_times = {}
        for metric in self.metrics:
            for component, time_spent in metric.bottlenecks.items():
                if component not in component_times:
                    component_times[component] = []
                component_times[component].append(time_spent)

        # Calculate statistics
        bottleneck_stats = {}
        for component, times in component_times.items():
            avg_time = np.mean(times)
            max_time = np.max(times)
            p95_time = np.percentile(times, 95)

            bottleneck_stats[component] = {
                "avg_time": float(avg_time),
                "max_time": float(max_time),
                "p95_time": float(p95_time),
                "samples": len(times)
            }

        # Sort by average time (descending)
        sorted_bottlenecks = dict(
            sorted(bottleneck_stats.items(), key=lambda x: x[1]["avg_time"], reverse=True)
        )

        return sorted_bottlenecks

    def get_report(self) -> str:
        """Generate human-readable latency report."""
        percentiles = self.get_percentiles()
        regression = self.detect_regression()
        bottlenecks = self.identify_bottlenecks()

        report = []
        report.append("=" * 80)
        report.append("LATENCY TRACKING REPORT")
        report.append("=" * 80)
        report.append("")

        report.append("Percentiles (Time to 99% Confidence):")
        report.append(f"  p50 (median): {percentiles['p50']:.2f} seconds")
        report.append(f"  p95:          {percentiles['p95']:.2f} seconds")
        report.append(f"  p99:          {percentiles['p99']:.2f} seconds")
        report.append(f"  Samples:      {percentiles['count']}")
        report.append("")

        if regression:
            report.append("⚠️  PERFORMANCE REGRESSION DETECTED:")
            report.append(f"  Baseline p99:  {regression['baseline_p99']:.2f}s")
            report.append(f"  Current p99:   {regression['current_p99']:.2f}s")
            report.append(f"  Degradation:   {regression['degradation_percent']:.1f}% slower")
            report.append(f"  Recommendation: {regression['recommendation']}")
            report.append("")
        else:
            report.append("✅ No performance regression detected")
            report.append("")

        if bottlenecks:
            report.append("Bottleneck Analysis (Top 5):")
            for i, (component, stats) in enumerate(list(bottlenecks.items())[:5], 1):
                report.append(f"  {i}. {component}")
                report.append(f"     Average: {stats['avg_time']:.3f}s")
                report.append(f"     p95:     {stats['p95_time']:.3f}s")
                report.append(f"     Max:     {stats['max_time']:.3f}s")
            report.append("")

        report.append("=" * 80)
        return "\n".join(report)

    def _classify_prompt(self, prompt: str) -> str:
        """Classify prompt type for analysis."""
        prompt_lower = prompt.lower()
        if "code" in prompt_lower or "function" in prompt_lower:
            return "code_generation"
        elif "bug" in prompt_lower or "fix" in prompt_lower:
            return "bug_fixing"
        elif "algorithm" in prompt_lower:
            return "algorithm_design"
        elif "explain" in prompt_lower or "what" in prompt_lower:
            return "explanation"
        else:
            return "general"

    def _save_metric(self, metric: LatencyMetric):
        """Save metric to JSON log file."""
        log_file = self.log_dir / f"latency_{datetime.utcnow().strftime('%Y%m%d')}.jsonl"
        with open(log_file, "a") as f:
            f.write(json.dumps(asdict(metric)) + "\n")


class BottleneckProfiler:
    """Profile execution to identify bottlenecks."""

    def __init__(self):
        self.timings = {}
        self.current_component = None
        self.start_time = None

    def start_component(self, component_name: str):
        """Start timing a component."""
        self.current_component = component_name
        self.start_time = time.time()

    def end_component(self):
        """End timing current component."""
        if self.current_component and self.start_time:
            elapsed = time.time() - self.start_time
            self.timings[self.current_component] = elapsed
            self.current_component = None
            self.start_time = None

    def get_timings(self) -> Dict[str, float]:
        """Get all component timings."""
        return self.timings.copy()

    def get_report(self, total_time: float) -> str:
        """Generate bottleneck report."""
        if not self.timings:
            return "No timing data available"

        report = []
        report.append("Bottleneck Profiling:")

        # Sort by time (descending)
        sorted_timings = sorted(self.timings.items(), key=lambda x: x[1], reverse=True)

        for component, time_spent in sorted_timings:
            percentage = (time_spent / total_time) * 100 if total_time > 0 else 0
            report.append(f"  {component}: {time_spent:.3f}s ({percentage:.1f}%)")

            # Flag bottlenecks (>30% of total time)
            if percentage > 30:
                report.append(f"    ⚠️  BOTTLENECK DETECTED (>{percentage:.0f}% of total time)")

        return "\n".join(report)


# Example usage:
if __name__ == "__main__":
    # Example 1: Track latency over time
    tracker = LatencyTracker(baseline_p99=10.0)

    # Simulate executions
    tracker.record_execution(
        prompt="Write a Python function",
        time_to_99_percent=8.5,
        iterations=5,
        bottlenecks={"database_query": 3.2, "guardrails": 2.1, "iteration_loop": 3.2}
    )

    tracker.record_execution(
        prompt="Fix this bug",
        time_to_99_percent=12.3,
        iterations=8,
        bottlenecks={"database_query": 5.1, "guardrails": 2.3, "iteration_loop": 4.9}
    )

    # Generate report
    print(tracker.get_report())

    # Example 2: Profile execution
    profiler = BottleneckProfiler()

    start = time.time()

    profiler.start_component("guardrail_layer_1")
    time.sleep(0.1)
    profiler.end_component()

    profiler.start_component("database_query")
    time.sleep(0.5)  # Simulating slow query
    profiler.end_component()

    profiler.start_component("iteration_loop")
    time.sleep(0.2)
    profiler.end_component()

    total = time.time() - start

    print("\n")
    print(profiler.get_report(total))
