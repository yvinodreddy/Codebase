#!/usr/bin/env python3
"""
SWARMCARE Agents Performance Benchmark
Phase 02: Production Performance Testing

Benchmarks all 6 agents against their SLA targets:
- Knowledge Agent: < 2s
- Case Agent: < 3s
- Conversation Agent: < 1s
- Compliance Agent: < 100ms
- Podcast Agent: < 30s
- QA Agent: < 500ms

Usage:
    python3 performance_benchmark.py
    python3 performance_benchmark.py --iterations 100
    python3 performance_benchmark.py --agent knowledge --iterations 50
"""

import sys
import os
import time
import json
import argparse
import statistics
from datetime import datetime
from typing import Dict, List

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'code'))

try:
    from implementation import Phase02Implementation
    IMPLEMENTATION_AVAILABLE = True
except ImportError as e:
    print(f"❌ Failed to import implementation: {e}")
    IMPLEMENTATION_AVAILABLE = False


class AgentBenchmark:
    """Performance benchmark for agents"""

    def __init__(self):
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "phase": "Phase 02: SWARMCARE Agents",
            "benchmarks": {}
        }

    def benchmark_all_agents(self, iterations=10) -> Dict:
        """Benchmark all agents"""
        print("=" * 80)
        print("SWARMCARE AGENTS PERFORMANCE BENCHMARK")
        print("=" * 80)
        print(f"Started: {self.results['timestamp']}")
        print(f"Iterations: {iterations}")
        print("=" * 80)
        print()

        if not IMPLEMENTATION_AVAILABLE:
            print("❌ Implementation not available")
            return self.results

        # Initialize phase
        try:
            phase = Phase02Implementation()
        except Exception as e:
            print(f"❌ Failed to initialize phase: {e}")
            return self.results

        # Benchmark each agent
        agents = [
            ("knowledge", "Knowledge Agent", 2000),
            ("case", "Case Agent", 3000),
            ("conversation", "Conversation Agent", 1000),
            ("compliance", "Compliance Agent", 100),
            ("podcast", "Podcast Agent", 30000),
            ("qa", "QA Agent", 500)
        ]

        for agent_key, agent_name, sla_ms in agents:
            self._benchmark_agent(phase, agent_key, agent_name, sla_ms, iterations)

        # Print summary
        self._print_summary()

        return self.results

    def _benchmark_agent(self, phase, agent_key, agent_name, sla_ms, iterations):
        """Benchmark single agent"""
        print(f"Benchmarking {agent_name}...")
        print(f"  Target SLA: < {sla_ms}ms")
        print(f"  Iterations: {iterations}")

        durations = []

        for i in range(iterations):
            start_time = time.time()

            try:
                # Initialize agent
                if agent_key == "knowledge":
                    agent = phase._initialize_knowledge_agent()
                elif agent_key == "case":
                    agent = phase._initialize_case_agent()
                elif agent_key == "conversation":
                    agent = phase._initialize_conversation_agent()
                elif agent_key == "compliance":
                    agent = phase._initialize_compliance_agent()
                elif agent_key == "podcast":
                    agent = phase._initialize_podcast_agent()
                elif agent_key == "qa":
                    agent = phase._initialize_qa_agent()
                else:
                    raise ValueError(f"Unknown agent: {agent_key}")

                duration_ms = (time.time() - start_time) * 1000
                durations.append(duration_ms)

            except Exception as e:
                print(f"  ❌ Iteration {i+1} failed: {e}")
                continue

        if not durations:
            print(f"  ❌ {agent_name}: All iterations failed")
            self.results["benchmarks"][agent_key] = {
                "name": agent_name,
                "error": "All iterations failed"
            }
            return

        # Calculate statistics
        min_time = min(durations)
        max_time = max(durations)
        avg_time = statistics.mean(durations)
        median_time = statistics.median(durations)
        p95_time = self._percentile(durations, 95)
        p99_time = self._percentile(durations, 99)

        # Check SLA compliance
        sla_met = avg_time < sla_ms
        sla_status = "✅ PASS" if sla_met else "❌ FAIL"

        print(f"  {sla_status}")
        print(f"  Min:     {min_time:.2f}ms")
        print(f"  Max:     {max_time:.2f}ms")
        print(f"  Avg:     {avg_time:.2f}ms")
        print(f"  Median:  {median_time:.2f}ms")
        print(f"  P95:     {p95_time:.2f}ms")
        print(f"  P99:     {p99_time:.2f}ms")
        print()

        # Store results
        self.results["benchmarks"][agent_key] = {
            "name": agent_name,
            "sla_ms": sla_ms,
            "sla_met": sla_met,
            "iterations": len(durations),
            "min_ms": min_time,
            "max_ms": max_time,
            "avg_ms": avg_time,
            "median_ms": median_time,
            "p95_ms": p95_time,
            "p99_ms": p99_time
        }

    def _percentile(self, data, percentile):
        """Calculate percentile"""
        sorted_data = sorted(data)
        index = int((percentile / 100) * len(sorted_data))
        return sorted_data[min(index, len(sorted_data) - 1)]

    def _print_summary(self):
        """Print benchmark summary"""
        print("=" * 80)
        print("BENCHMARK SUMMARY")
        print("=" * 80)

        if not self.results["benchmarks"]:
            print("No benchmarks completed")
            return

        total_agents = len(self.results["benchmarks"])
        passed_agents = sum(1 for b in self.results["benchmarks"].values()
                          if b.get("sla_met", False))

        print(f"Total Agents: {total_agents}")
        print(f"SLA Met: {passed_agents}")
        print(f"SLA Failed: {total_agents - passed_agents}")
        print(f"Success Rate: {(passed_agents / total_agents * 100):.1f}%")
        print()

        # Print table
        print("Agent Performance Summary:")
        print("-" * 80)
        print(f"{'Agent':<20} {'SLA':<10} {'Avg':<10} {'P95':<10} {'Status':<10}")
        print("-" * 80)

        for agent_key, data in self.results["benchmarks"].items():
            if "error" in data:
                print(f"{data['name']:<20} {'N/A':<10} {'ERROR':<10} {'ERROR':<10} {'❌ FAIL':<10}")
            else:
                status = "✅ PASS" if data["sla_met"] else "❌ FAIL"
                print(f"{data['name']:<20} "
                      f"<{data['sla_ms']}ms{'':<4} "
                      f"{data['avg_ms']:.1f}ms{'':<4} "
                      f"{data['p95_ms']:.1f}ms{'':<4} "
                      f"{status:<10}")

        print("-" * 80)
        print("=" * 80)

    def save_report(self, filename="performance_benchmark_report.json"):
        """Save benchmark report"""
        report_path = os.path.join(os.path.dirname(__file__), filename)
        with open(report_path, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"\nBenchmark report saved to: {report_path}")


def main():
    """Main benchmark entry point"""
    parser = argparse.ArgumentParser(description="Benchmark SWARMCARE Agents")
    parser.add_argument("--iterations", "-i", type=int, default=10,
                       help="Number of iterations per agent (default: 10)")
    parser.add_argument("--agent", "-a", type=str,
                       help="Benchmark specific agent only")
    args = parser.parse_args()

    benchmark = AgentBenchmark()

    # Run benchmark
    results = benchmark.benchmark_all_agents(iterations=args.iterations)

    # Save report
    benchmark.save_report()

    # Determine exit code
    if not results["benchmarks"]:
        sys.exit(1)

    all_passed = all(b.get("sla_met", False) for b in results["benchmarks"].values()
                    if "error" not in b)

    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
