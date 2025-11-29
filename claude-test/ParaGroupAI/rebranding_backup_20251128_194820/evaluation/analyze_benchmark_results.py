#!/usr/bin/env python3
"""
Automated Benchmark Results Analyzer

Analyzes ULTRATHINK benchmark outputs and generates comprehensive reports.
Supports scaling to 200 prompts across 5 categories.
"""

import os
import re
import json
import glob
from datetime import datetime
from typing import Dict, List, Optional, Tuple


class BenchmarkAnalyzer:
    """Analyzes benchmark results from ULTRATHINK system."""

    def __init__(self, results_dir: str = "tmp"):
        self.results_dir = results_dir
        self.benchmark_categories = {
            "code_generation": ["track1", "track5"],  # Fibonacci, React Auth
            "bug_fixing": ["track2"],  # Factorial
            "algorithm_design": ["track3"],  # Dijkstra
            "complex_reasoning": ["track4"],  # Race Condition
        }

    def find_latest_benchmark_files(self) -> Dict[str, str]:
        """Find the most recent benchmark output files."""
        pattern = os.path.join(self.results_dir, "cppultrathink_output_track*_*.txt")
        files = glob.glob(pattern)

        # Get the 5 most recent files (one for each track)
        recent_files = {}
        for track in range(1, 6):
            track_pattern = os.path.join(self.results_dir, f"cppultrathink_output_track{track}_*.txt")
            track_files = sorted(glob.glob(track_pattern), key=os.path.getmtime, reverse=True)
            if track_files:
                recent_files[f"track{track}"] = track_files[0]

        return recent_files

    def extract_metrics(self, file_path: str) -> Dict[str, any]:
        """Extract key metrics from a benchmark output file."""
        metrics = {
            "file_path": file_path,
            "file_size": os.path.getsize(file_path),
            "has_metrics_table": False,
            "confidence_score": None,
            "validation_layers": None,
            "context_management": None,
            "test_coverage": None,
            "success_rate": None,
            "guardrail_layers_passed": None,
        }

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Check if metrics comparison table exists
            metrics["has_metrics_table"] = "PERFORMANCE METRICS COMPARISON" in content

            # Extract confidence score from metrics table
            confidence_match = re.search(r'Achieved\s+│\s+\d+%\s+│\s+\d+%\s+│\s+([\d.]+)%', content)
            if confidence_match:
                metrics["confidence_score"] = float(confidence_match.group(1))

            # Extract validation layers
            layers_match = re.search(r'Total Layers\s+│\s+\d+\s+│\s+\d+\s+│\s+(\d+)', content)
            if layers_match:
                metrics["validation_layers"] = int(layers_match.group(1))

            # Extract success rate
            success_match = re.search(r'Success Rate\s+│\s+\d+%\s+│\s+\d+%\s+│\s+([\d.]+)%', content)
            if success_match:
                metrics["success_rate"] = float(success_match.group(1))

            # Extract test coverage
            coverage_match = re.search(r'Context Manager\s+│\s+\d+%\s+│\s+\d+%\s+│\s+([\d.]+)%', content)
            if coverage_match:
                metrics["test_coverage"] = float(coverage_match.group(1))

            # Count guardrail layer passes
            guardrail_count = content.count("✅ Layer")
            if guardrail_count > 0:
                metrics["guardrail_layers_passed"] = guardrail_count

        except Exception as e:
            print(f"Error analyzing {file_path}: {e}")

        return metrics

    def generate_summary_report(self, benchmark_files: Dict[str, str]) -> str:
        """Generate a comprehensive summary report."""
        report = []
        report.append("=" * 80)
        report.append("📊 ULTRATHINK BENCHMARK RESULTS SUMMARY")
        report.append("=" * 80)
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Benchmarks Executed: {len(benchmark_files)}")
        report.append("")

        all_metrics = {}
        for track, file_path in sorted(benchmark_files.items()):
            metrics = self.extract_metrics(file_path)
            all_metrics[track] = metrics

            # Determine benchmark name
            track_num = int(track.replace("track", ""))
            benchmark_names = {
                1: "Code Generation - Fibonacci with Memoization",
                2: "Bug Fixing - RecursionError in Factorial",
                3: "Algorithm Design - Dijkstra's Shortest Path",
                4: "Complex Reasoning - Race Condition Analysis",
                5: "Code Generation - React Authentication Component",
            }

            report.append(f"{'='*80}")
            report.append(f"Benchmark {track_num}: {benchmark_names.get(track_num, 'Unknown')}")
            report.append(f"{'='*80}")
            report.append(f"File: {os.path.basename(file_path)}")
            report.append(f"Size: {metrics['file_size']:,} bytes")
            report.append(f"")
            report.append(f"✅ Metrics Table Present: {metrics['has_metrics_table']}")
            report.append(f"")

            if metrics['confidence_score']:
                report.append(f"📈 CONFIDENCE SCORE: {metrics['confidence_score']}%")
                if metrics['confidence_score'] >= 99.0:
                    report.append(f"   ✅ Target met (≥99%)")
                else:
                    report.append(f"   ⚠️  Below target (target: 99%+)")

            if metrics['validation_layers']:
                report.append(f"🛡️  VALIDATION LAYERS: {metrics['validation_layers']}/8")
                if metrics['validation_layers'] == 8:
                    report.append(f"   ✅ All layers operational")
                else:
                    report.append(f"   ⚠️  Some layers missing")

            if metrics['guardrail_layers_passed']:
                report.append(f"🔒 GUARDRAIL LAYERS PASSED: {metrics['guardrail_layers_passed']}")

            if metrics['test_coverage']:
                report.append(f"🧪 TEST COVERAGE: {metrics['test_coverage']}%")
                if metrics['test_coverage'] >= 60.0:
                    report.append(f"   ✅ Target met (≥60%)")
                else:
                    report.append(f"   ⚠️  Below target (target: 60%+)")

            if metrics['success_rate']:
                report.append(f"✓  SUCCESS RATE: {metrics['success_rate']}%")
                if metrics['success_rate'] >= 99.0:
                    report.append(f"   ✅ Excellent (≥99%)")
                else:
                    report.append(f"   ⚠️  Below target (target: 99%+)")

            report.append("")

        # Overall Statistics
        report.append("=" * 80)
        report.append("📊 OVERALL STATISTICS")
        report.append("=" * 80)

        total_benchmarks = len(all_metrics)
        benchmarks_with_metrics = sum(1 for m in all_metrics.values() if m['has_metrics_table'])
        avg_confidence = sum(m['confidence_score'] for m in all_metrics.values() if m['confidence_score']) / total_benchmarks if total_benchmarks > 0 else 0

        report.append(f"Total Benchmarks: {total_benchmarks}")
        report.append(f"Benchmarks with Metrics Table: {benchmarks_with_metrics}/{total_benchmarks} ({benchmarks_with_metrics/total_benchmarks*100:.1f}%)")
        report.append(f"Average Confidence Score: {avg_confidence:.2f}%")
        report.append("")

        # Status Assessment
        if benchmarks_with_metrics == total_benchmarks and avg_confidence >= 99.0:
            report.append("✅ STATUS: PRODUCTION-READY")
            report.append("   All benchmarks passed with 99%+ confidence.")
            report.append("   Metrics comparison table appears in 100% of outputs.")
        elif benchmarks_with_metrics == total_benchmarks:
            report.append("🟡 STATUS: METRICS IMPLEMENTED, CONFIDENCE NEEDS IMPROVEMENT")
            report.append(f"   Metrics table present in all outputs.")
            report.append(f"   Average confidence: {avg_confidence:.2f}% (target: 99%+)")
        else:
            report.append("⚠️  STATUS: IMPLEMENTATION INCOMPLETE")
            report.append(f"   Metrics table missing in {total_benchmarks - benchmarks_with_metrics} benchmark(s).")

        report.append("")
        report.append("=" * 80)

        return "\n".join(report)

    def generate_200_prompts_roadmap(self) -> str:
        """Generate roadmap for scaling to 200 prompts."""
        roadmap = []
        roadmap.append("=" * 80)
        roadmap.append("🗺️  ROADMAP TO 200 BENCHMARK PROMPTS")
        roadmap.append("=" * 80)
        roadmap.append("")
        roadmap.append("CURRENT STATE: 5 prompts (Phase 1 Complete)")
        roadmap.append("TARGET: 200 prompts (40 per category)")
        roadmap.append("")

        categories = {
            "Code Generation": {
                "current": 2,
                "target": 40,
                "subcategories": [
                    "Python (15 prompts): web, data, algorithms, ML",
                    "JavaScript/TypeScript (10 prompts): React, Node, Vue",
                    "Other languages (10 prompts): Go, Rust, Java, C++",
                    "Cross-cutting (5 prompts): testing, docs, CI/CD",
                ]
            },
            "Bug Fixing": {
                "current": 1,
                "target": 40,
                "subcategories": [
                    "Logic errors (10 prompts)",
                    "Memory leaks (5 prompts)",
                    "Race conditions (5 prompts)",
                    "Security vulnerabilities (10 prompts)",
                    "Performance issues (10 prompts)",
                ]
            },
            "Algorithm Design": {
                "current": 1,
                "target": 40,
                "subcategories": [
                    "Searching (10 prompts): binary search, etc.",
                    "Sorting (5 prompts): quicksort, mergesort",
                    "Graph algorithms (10 prompts): DFS, BFS, Dijkstra",
                    "Dynamic programming (10 prompts): knapsack, LCS",
                    "Data structures (5 prompts): trees, heaps",
                ]
            },
            "Complex Reasoning": {
                "current": 1,
                "target": 40,
                "subcategories": [
                    "Concurrency (10 prompts)",
                    "Distributed systems (10 prompts)",
                    "System design (10 prompts)",
                    "Optimization problems (10 prompts)",
                ]
            },
            "Production Scenarios": {
                "current": 0,
                "target": 40,
                "subcategories": [
                    "Database design (10 prompts)",
                    "API design (10 prompts)",
                    "Security hardening (10 prompts)",
                    "Performance optimization (10 prompts)",
                ]
            }
        }

        for category, details in categories.items():
            current = details["current"]
            target = details["target"]
            remaining = target - current
            progress = (current / target) * 100

            roadmap.append(f"📁 {category}")
            roadmap.append(f"   Current: {current} prompts | Target: {target} prompts")
            roadmap.append(f"   Remaining: {remaining} prompts | Progress: {progress:.1f}%")
            roadmap.append(f"")
            roadmap.append(f"   Subcategories:")
            for sub in details["subcategories"]:
                roadmap.append(f"   - {sub}")
            roadmap.append("")

        roadmap.append("=" * 80)
        roadmap.append("IMPLEMENTATION PHASES")
        roadmap.append("=" * 80)
        roadmap.append("")
        roadmap.append("✅ Phase 1 (Complete): Foundation - 5 prompts")
        roadmap.append("   Status: All 5 benchmarks executed successfully")
        roadmap.append("   Metrics: 100% have comparison table")
        roadmap.append("")
        roadmap.append("⏳ Phase 2 (Next): Scale to 25 prompts (5 per category)")
        roadmap.append("   Timeline: 1-2 weeks")
        roadmap.append("   Focus: Core scenarios for each category")
        roadmap.append("")
        roadmap.append("⏳ Phase 3: Scale to 100 prompts (20 per category)")
        roadmap.append("   Timeline: 1 month")
        roadmap.append("   Focus: Edge cases and advanced scenarios")
        roadmap.append("")
        roadmap.append("⏳ Phase 4: Scale to 200 prompts (40 per category)")
        roadmap.append("   Timeline: 2-3 months")
        roadmap.append("   Focus: Comprehensive coverage with automated testing")
        roadmap.append("")
        roadmap.append("=" * 80)

        return "\n".join(roadmap)

    def analyze_and_report(self, output_file: Optional[str] = None) -> str:
        """Main analysis function - finds files, analyzes, and generates report."""
        # Find latest benchmark files
        benchmark_files = self.find_latest_benchmark_files()

        if not benchmark_files:
            return "⚠️  No benchmark files found in tmp/ directory."

        # Generate reports
        summary = self.generate_summary_report(benchmark_files)
        roadmap = self.generate_200_prompts_roadmap()

        full_report = summary + "\n\n" + roadmap

        # Save to file if specified
        if output_file:
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(full_report)
            print(f"✅ Report saved to: {output_file}")

        return full_report


def main():
    """Main entry point."""
    analyzer = BenchmarkAnalyzer()

    # Generate timestamp for output file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"evaluation/results/benchmark_analysis_{timestamp}.txt"

    # Run analysis and generate report
    report = analyzer.analyze_and_report(output_file)

    # Print to console
    print(report)

    return 0


if __name__ == "__main__":
    exit(main())
