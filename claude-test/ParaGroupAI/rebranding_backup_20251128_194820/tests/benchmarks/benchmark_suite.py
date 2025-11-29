"""
Automated Performance Benchmarking Suite
Detects performance regressions automatically
"""

import time
import json
import statistics
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Callable
import functools


class PerformanceBenchmark:
    """Manages performance benchmarking and regression detection."""

    def __init__(self, baseline_file: str = "benchmarks/baseline.json"):
        self.baseline_file = Path(baseline_file)
        self.baseline_file.parent.mkdir(exist_ok=True)
        self.results: Dict[str, List[float]] = {}
        self.baseline = self._load_baseline()

    def _load_baseline(self) -> Dict:
        """Load baseline performance metrics."""
        if self.baseline_file.exists():
            with open(self.baseline_file) as f:
                return json.load(f)
        return {}

    def _save_baseline(self):
        """Save current results as new baseline."""
        with open(self.baseline_file, 'w') as f:
            json.dump(self.baseline, f, indent=2)

    def benchmark(self, name: str, iterations: int = 100):
        """Decorator to benchmark a function."""
        def decorator(func: Callable):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                durations = []

                # Warmup
                for _ in range(10):
                    func(*args, **kwargs)

                # Actual benchmark
                for _ in range(iterations):
                    start = time.perf_counter()
                    result = func(*args, **kwargs)
                    duration = time.perf_counter() - start
                    durations.append(duration * 1000)  # Convert to ms

                self.results[name] = durations

                # Calculate statistics
                mean = statistics.mean(durations)
                median = statistics.median(durations)
                stdev = statistics.stdev(durations) if len(durations) > 1 else 0
                p95 = statistics.quantiles(durations, n=20)[18] if len(durations) >= 20 else max(durations)
                p99 = statistics.quantiles(durations, n=100)[98] if len(durations) >= 100 else max(durations)

                # Check for regression
                regression = self._check_regression(name, mean)

                print(f"Benchmark: {name}")
                print(f"  Iterations: {iterations}")
                print(f"  Mean: {mean:.3f}ms")
                print(f"  Median: {median:.3f}ms")
                print(f"  Stdev: {stdev:.3f}ms")
                print(f"  P95: {p95:.3f}ms")
                print(f"  P99: {p99:.3f}ms")

                if regression:
                    print(f"  ⚠️  REGRESSION DETECTED: {regression['change']:.1f}% slower than baseline")
                else:
                    print(f"  ✅ Performance within acceptable range")

                print()

                return result

            return wrapper
        return decorator

    def _check_regression(self, name: str, current_mean: float) -> Dict:
        """Check if performance regressed compared to baseline."""
        if name not in self.baseline:
            # First run - set baseline
            self.baseline[name] = {
                'mean': current_mean,
                'timestamp': datetime.now().isoformat(),
            }
            self._save_baseline()
            return None

        baseline_mean = self.baseline[name]['mean']
        threshold = 1.10  # 10% regression threshold

        if current_mean > baseline_mean * threshold:
            change_percent = ((current_mean - baseline_mean) / baseline_mean) * 100
            return {
                'baseline': baseline_mean,
                'current': current_mean,
                'change': change_percent,
            }

        # Update baseline if performance improved significantly (>5%)
        if current_mean < baseline_mean * 0.95:
            self.baseline[name] = {
                'mean': current_mean,
                'timestamp': datetime.now().isoformat(),
            }
            self._save_baseline()

        return None

    def generate_report(self, output_file: str = "benchmark_report.html"):
        """Generate HTML report of benchmark results."""
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Performance Benchmark Report</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                table { border-collapse: collapse; width: 100%; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                th { background-color: #4CAF50; color: white; }
                .regression { background-color: #ffcccc; }
                .improvement { background-color: #ccffcc; }
            </style>
        </head>
        <body>
            <h1>Performance Benchmark Report</h1>
            <p>Generated: {timestamp}</p>
            <table>
                <tr>
                    <th>Benchmark</th>
                    <th>Mean (ms)</th>
                    <th>Median (ms)</th>
                    <th>P95 (ms)</th>
                    <th>P99 (ms)</th>
                    <th>Baseline (ms)</th>
                    <th>Change</th>
                </tr>
        """.format(timestamp=datetime.now().isoformat())

        for name, durations in self.results.items():
            mean = statistics.mean(durations)
            median = statistics.median(durations)
            p95 = statistics.quantiles(durations, n=20)[18] if len(durations) >= 20 else max(durations)
            p99 = statistics.quantiles(durations, n=100)[98] if len(durations) >= 100 else max(durations)

            baseline_mean = self.baseline.get(name, {}).get('mean', mean)
            change = ((mean - baseline_mean) / baseline_mean) * 100 if baseline_mean else 0

            row_class = ''
            if change > 10:
                row_class = 'regression'
            elif change < -5:
                row_class = 'improvement'

            html += f"""
                <tr class="{row_class}">
                    <td>{name}</td>
                    <td>{mean:.3f}</td>
                    <td>{median:.3f}</td>
                    <td>{p95:.3f}</td>
                    <td>{p99:.3f}</td>
                    <td>{baseline_mean:.3f}</td>
                    <td>{change:+.1f}%</td>
                </tr>
            """

        html += """
            </table>
        </body>
        </html>
        """

        with open(output_file, 'w') as f:
            f.write(html)

        print(f"✅ Benchmark report generated: {output_file}")


# Example usage
if __name__ == "__main__":
    bench = PerformanceBenchmark()

    @bench.benchmark("simple_addition", iterations=1000)
    def test_addition():
        return 2 + 2

    @bench.benchmark("list_comprehension", iterations=500)
    def test_list_comp():
        return [i**2 for i in range(1000)]

    test_addition()
    test_list_comp()

    bench.generate_report()
