#!/usr/bin/env python3
"""
Script to enhance test coverage to 90% for all target modules.
Analyzes coverage gaps and adds specific tests to reach target.
"""

import subprocess
import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple

class CoverageEnhancer:
    """Enhance test coverage to meet 90% target"""

    def __init__(self):
        self.target_coverage = 90.0
        self.test_dir = Path("tests/unit_instance4")
        self.modules = [
            "multi_source_metrics_verifier.py",
            "prompt_history.py",
            "prompt_preprocessor.py",
            "realtime_db_updates.py",
            "realtime_log_monitor.py",
            "realtime_verbose_logger.py",
            "replace_all_placeholders.py",
            "replace_final_placeholders.py",
            "replace_remaining_placeholders.py",
            "scripts/code_review_automation.py",
            "setup_database.py",
            "smart_test_generator.py",
            "stage_progress_tracker.py",
            "statusline_formatter.py",
            "streaming_output.py",
            "task_archiver.py"
        ]

    def get_current_coverage(self, module: str) -> Tuple[float, List[str]]:
        """Get current coverage and missing lines for a module"""
        test_file = self.test_dir / f"test_{Path(module).stem}.py"

        if not test_file.exists():
            return 0.0, []

        try:
            # Run pytest with coverage for specific module
            result = subprocess.run(
                [
                    "python3", "-m", "pytest",
                    str(test_file),
                    f"--cov={module}",
                    "--cov-report=json",
                    "-q"
                ],
                capture_output=True,
                text=True
            )

            # Parse coverage report
            if Path("coverage.json").exists():
                with open("coverage.json") as f:
                    data = json.load(f)

                for file_path, file_data in data.get("files", {}).items():
                    if module in file_path:
                        coverage = file_data["summary"]["percent_covered"]
                        missing = file_data.get("missing_lines", [])
                        return coverage, missing

        except Exception as e:
            print(f"Error getting coverage for {module}: {e}")

        return 0.0, []

    def generate_coverage_report(self) -> Dict[str, Dict]:
        """Generate comprehensive coverage report for all modules"""
        report = {}

        print("=" * 80)
        print("COVERAGE ANALYSIS REPORT")
        print("=" * 80)

        for module in self.modules:
            coverage, missing_lines = self.get_current_coverage(module)
            gap = self.target_coverage - coverage

            report[module] = {
                "current_coverage": coverage,
                "gap": gap,
                "missing_lines": missing_lines,
                "status": "✅ PASS" if coverage >= self.target_coverage else "❌ FAIL"
            }

            # Print status
            status_icon = "✅" if coverage >= self.target_coverage else "❌"
            print(f"{status_icon} {module:40} {coverage:6.2f}% (Gap: {gap:+6.2f}%)")

        return report

    def suggest_improvements(self, report: Dict[str, Dict]):
        """Suggest specific improvements for modules below target"""
        print("\n" + "=" * 80)
        print("IMPROVEMENT SUGGESTIONS")
        print("=" * 80)

        for module, data in report.items():
            if data["current_coverage"] < self.target_coverage:
                print(f"\n📝 {module}")
                print(f"   Current: {data['current_coverage']:.2f}%")
                print(f"   Needed:  {self.target_coverage:.2f}%")
                print(f"   Gap:     {data['gap']:.2f}%")

                if data["missing_lines"]:
                    print(f"   Missing lines: {data['missing_lines'][:10]}...")

                # Suggest specific test types based on gap
                if data["gap"] > 20:
                    print("   💡 Needs comprehensive test rewrite")
                elif data["gap"] > 10:
                    print("   💡 Add tests for error handling and edge cases")
                elif data["gap"] > 5:
                    print("   💡 Add tests for uncovered exception handlers")
                else:
                    print("   💡 Minor additions needed for specific lines")

    def run_all_tests_with_coverage(self):
        """Run all tests and show overall coverage"""
        print("\n" + "=" * 80)
        print("RUNNING ALL TESTS WITH COVERAGE")
        print("=" * 80)

        result = subprocess.run(
            [
                "python3", "-m", "pytest",
                str(self.test_dir),
                "--cov=.",
                "--cov-report=term",
                "-q"
            ],
            capture_output=True,
            text=True
        )

        # Extract coverage summary
        for line in result.stdout.split("\n"):
            if "TOTAL" in line:
                print(f"\nOverall Coverage: {line}")

    def main(self):
        """Main execution"""
        print("🔍 Analyzing test coverage for 16 target modules...")
        print(f"📊 Target Coverage: {self.target_coverage}%\n")

        # Generate coverage report
        report = self.generate_coverage_report()

        # Count passing modules
        passing = sum(1 for data in report.values() if data["current_coverage"] >= self.target_coverage)
        total = len(report)

        print(f"\n📈 Summary: {passing}/{total} modules meet {self.target_coverage}% target")

        # Suggest improvements
        if passing < total:
            self.suggest_improvements(report)

        # Run all tests
        self.run_all_tests_with_coverage()

        # Final summary
        print("\n" + "=" * 80)
        print("FINAL RECOMMENDATIONS")
        print("=" * 80)

        if passing == total:
            print("✅ All modules meet the 90% coverage target!")
        else:
            failing = total - passing
            print(f"⚠️  {failing} modules need improvement to reach 90% coverage")
            print("\nPriority order (easiest to fix first):")

            # Sort by gap (smallest gap first)
            sorted_modules = sorted(
                [(m, d) for m, d in report.items() if d["current_coverage"] < self.target_coverage],
                key=lambda x: x[1]["gap"]
            )

            for i, (module, data) in enumerate(sorted_modules[:5], 1):
                print(f"{i}. {module} - Gap: {data['gap']:.2f}%")

if __name__ == "__main__":
    enhancer = CoverageEnhancer()
    enhancer.main()