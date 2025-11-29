#!/usr/bin/env python3
"""
Automated Code Review Script
Runs multiple code quality tools and generates a comprehensive report
"""
import json
import subprocess
import sys
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any


@dataclass
class CodeQualityMetrics:
    """Code quality metrics from various tools"""
    timestamp: str
    black_compliant: bool
    black_files_need_formatting: int
    isort_compliant: bool
    isort_files_need_sorting: int
    pylint_score: float
    pylint_violations: int
    mypy_errors: int
    mypy_warnings: int
    bandit_issues: Dict[str, int]
    safety_vulnerabilities: int
    test_coverage: float
    tests_passed: int
    tests_failed: int
    tests_total: int


class CodeReviewAutomation:
    """Automated code review orchestrator"""

    def __init__(self, output_dir: str = "code_review_reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.results = {}

    def run_black(self) -> tuple[bool, int]:
        """Check code formatting with black"""
        print("🎨 Running black formatter check...")
        try:
            result = subprocess.run(
                ["black", "--check", "--diff", "."],
                capture_output=True,
                text=True,
                timeout=60
            )
            files_need_formatting = result.stdout.count("would reformat")
            return result.returncode == 0, files_need_formatting
        except Exception as e:
            print(f"❌ Black check failed: {e}")
            return False, 0

    def run_isort(self) -> tuple[bool, int]:
        """Check import sorting with isort"""
        print("📦 Running isort import sorter check...")
        try:
            result = subprocess.run(
                ["isort", "--check-only", "--diff", "."],
                capture_output=True,
                text=True,
                timeout=60
            )
            files_need_sorting = result.stdout.count("would be reformatted")
            return result.returncode == 0, files_need_sorting
        except Exception as e:
            print(f"❌ Isort check failed: {e}")
            return False, 0

    def run_pylint(self) -> tuple[float, int]:
        """Run pylint and extract score"""
        print("🔍 Running pylint analysis...")
        try:
            result = subprocess.run(
                ["pylint", "**/*.py", "--rcfile=.pylintrc"],
                capture_output=True,
                text=True,
                timeout=300
            )
            # Parse pylint output for score
            score = 0.0
            violations = 0
            for line in result.stdout.split("\n"):
                if "Your code has been rated at" in line:
                    score = float(line.split("rated at ")[1].split("/")[0])
                elif line.startswith("***"):
                    violations += 1
            return score, violations
        except Exception as e:
            print(f"❌ Pylint check failed: {e}")
            return 0.0, 0

    def run_mypy(self) -> tuple[int, int]:
        """Run mypy type checking"""
        print("🔬 Running mypy type checker...")
        try:
            result = subprocess.run(
                ["mypy", "."],
                capture_output=True,
                text=True,
                timeout=120
            )
            errors = result.stdout.count("error:")
            warnings = result.stdout.count("note:")
            return errors, warnings
        except Exception as e:
            print(f"❌ Mypy check failed: {e}")
            return 0, 0

    def run_bandit(self) -> Dict[str, int]:
        """Run bandit security scanner"""
        print("🔒 Running bandit security scanner...")
        try:
            result = subprocess.run(
                ["bandit", "-r", ".", "-f", "json"],
                capture_output=True,
                text=True,
                timeout=120
            )
            if result.stdout:
                data = json.loads(result.stdout)
                issues = {
                    "high": 0,
                    "medium": 0,
                    "low": 0
                }
                for item in data.get("results", []):
                    severity = item.get("issue_severity", "").lower()
                    if severity in issues:
                        issues[severity] += 1
                return issues
        except Exception as e:
            print(f"❌ Bandit check failed: {e}")
        return {"high": 0, "medium": 0, "low": 0}

    def run_safety(self) -> int:
        """Run safety dependency checker"""
        print("🛡️ Running safety dependency checker...")
        try:
            result = subprocess.run(
                ["safety", "check", "--json"],
                capture_output=True,
                text=True,
                timeout=60
            )
            if result.stdout:
                data = json.loads(result.stdout)
                return len(data)
        except Exception as e:
            print(f"❌ Safety check failed: {e}")
        return 0

    def run_tests(self) -> tuple[float, int, int, int]:
        """Run tests with coverage"""
        print("🧪 Running test suite with coverage...")
        try:
            result = subprocess.run(
                ["pytest", "tests/unit/", "--cov=.", "--cov-report=json", "-v"],
                capture_output=True,
                text=True,
                timeout=600
            )

            # Parse test results
            passed = result.stdout.count(" PASSED")
            failed = result.stdout.count(" FAILED")
            total = passed + failed

            # Parse coverage
            coverage = 0.0
            cov_file = Path("coverage.json")
            if cov_file.exists():
                with open(cov_file) as f:
                    cov_data = json.load(f)
                    coverage = cov_data.get("totals", {}).get("percent_covered", 0.0)

            return coverage, passed, failed, total
        except Exception as e:
            print(f"❌ Test execution failed: {e}")
            return 0.0, 0, 0, 0

    def generate_report(self, metrics: CodeQualityMetrics) -> None:
        """Generate comprehensive HTML and JSON reports"""
        # Save JSON report
        json_file = self.output_dir / f"report_{metrics.timestamp}.json"
        with open(json_file, "w") as f:
            json.dump(asdict(metrics), f, indent=2)

        # Generate HTML report
        html_file = self.output_dir / "latest_report.html"
        html_content = self._generate_html_report(metrics)
        with open(html_file, "w") as f:
            f.write(html_content)

        print(f"\n✅ Reports generated:")
        print(f"   JSON: {json_file}")
        print(f"   HTML: {html_file}")

    def _generate_html_report(self, metrics: CodeQualityMetrics) -> str:
        """Generate HTML report"""
        return f"""<!DOCTYPE html>
<html>
<head>
    <title>Code Quality Report - {metrics.timestamp}</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 40px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 40px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        h1 {{ color: #333; border-bottom: 3px solid #4CAF50; padding-bottom: 10px; }}
        h2 {{ color: #555; margin-top: 30px; }}
        .metric-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin: 20px 0; }}
        .metric-card {{ padding: 20px; border-radius: 8px; background: #f9f9f9; border-left: 4px solid #4CAF50; }}
        .metric-card.warning {{ border-left-color: #ff9800; }}
        .metric-card.error {{ border-left-color: #f44336; }}
        .metric-label {{ font-size: 14px; color: #666; text-transform: uppercase; }}
        .metric-value {{ font-size: 32px; font-weight: bold; color: #333; margin: 10px 0; }}
        .status {{ display: inline-block; padding: 5px 15px; border-radius: 20px; font-weight: bold; }}
        .status.pass {{ background: #4CAF50; color: white; }}
        .status.fail {{ background: #f44336; color: white; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background: #f0f0f0; font-weight: bold; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 Code Quality Report</h1>
        <p style="color: #666;">Generated: {metrics.timestamp}</p>

        <h2>📊 Overview</h2>
        <div class="metric-grid">
            <div class="metric-card">
                <div class="metric-label">Test Coverage</div>
                <div class="metric-value">{metrics.test_coverage:.1f}%</div>
                <span class="status {'pass' if metrics.test_coverage >= 90 else 'fail'}">
                    {'✅ PASS' if metrics.test_coverage >= 90 else '❌ NEEDS IMPROVEMENT'}
                </span>
            </div>

            <div class="metric-card">
                <div class="metric-label">Pylint Score</div>
                <div class="metric-value">{metrics.pylint_score:.2f}/10</div>
                <span class="status {'pass' if metrics.pylint_score >= 8.0 else 'fail'}">
                    {'✅ PASS' if metrics.pylint_score >= 8.0 else '❌ NEEDS IMPROVEMENT'}
                </span>
            </div>

            <div class="metric-card">
                <div class="metric-label">Tests Passed</div>
                <div class="metric-value">{metrics.tests_passed}/{metrics.tests_total}</div>
                <span class="status {'pass' if metrics.tests_failed == 0 else 'fail'}">
                    {metrics.tests_failed} failed
                </span>
            </div>

            <div class="metric-card {'warning' if metrics.bandit_issues['high'] > 0 else ''}">
                <div class="metric-label">Security Issues</div>
                <div class="metric-value">{metrics.bandit_issues['high']}</div>
                <span class="status {'pass' if metrics.bandit_issues['high'] == 0 else 'fail'}">
                    High Severity
                </span>
            </div>
        </div>

        <h2>🎨 Code Formatting</h2>
        <table>
            <tr>
                <th>Tool</th>
                <th>Status</th>
                <th>Issues</th>
            </tr>
            <tr>
                <td><strong>Black</strong> (Code Formatter)</td>
                <td><span class="status {'pass' if metrics.black_compliant else 'fail'}">
                    {'✅ Compliant' if metrics.black_compliant else '❌ Needs Formatting'}</span></td>
                <td>{metrics.black_files_need_formatting} files</td>
            </tr>
            <tr>
                <td><strong>Isort</strong> (Import Sorter)</td>
                <td><span class="status {'pass' if metrics.isort_compliant else 'fail'}">
                    {'✅ Compliant' if metrics.isort_compliant else '❌ Needs Sorting'}</span></td>
                <td>{metrics.isort_files_need_sorting} files</td>
            </tr>
        </table>

        <h2>🔬 Type Checking</h2>
        <table>
            <tr>
                <th>Tool</th>
                <th>Errors</th>
                <th>Warnings</th>
            </tr>
            <tr>
                <td><strong>Mypy</strong></td>
                <td>{metrics.mypy_errors}</td>
                <td>{metrics.mypy_warnings}</td>
            </tr>
        </table>

        <h2>🔒 Security</h2>
        <table>
            <tr>
                <th>Severity</th>
                <th>Count</th>
            </tr>
            <tr>
                <td><strong>High</strong></td>
                <td style="color: #f44336; font-weight: bold;">{metrics.bandit_issues['high']}</td>
            </tr>
            <tr>
                <td><strong>Medium</strong></td>
                <td style="color: #ff9800; font-weight: bold;">{metrics.bandit_issues['medium']}</td>
            </tr>
            <tr>
                <td><strong>Low</strong></td>
                <td>{metrics.bandit_issues['low']}</td>
            </tr>
            <tr>
                <td><strong>Vulnerable Dependencies</strong></td>
                <td style="color: #f44336; font-weight: bold;">{metrics.safety_vulnerabilities}</td>
            </tr>
        </table>

        <h2>📈 Action Items</h2>
        <ul>
            {('❌ Increase test coverage from ' + str(metrics.test_coverage) + '% to 90%+') if metrics.test_coverage < 90 else '✅ Test coverage meets 90% target'}
            <br>
            {('❌ Fix ' + str(metrics.black_files_need_formatting) + ' files that need black formatting') if not metrics.black_compliant else '✅ All files comply with black formatting'}
            <br>
            {('❌ Fix ' + str(metrics.mypy_errors) + ' mypy type errors') if metrics.mypy_errors > 0 else '✅ No mypy type errors'}
            <br>
            {('❌ Fix ' + str(metrics.bandit_issues['high']) + ' high severity security issues') if metrics.bandit_issues['high'] > 0 else '✅ No high severity security issues'}
        </ul>
    </div>
</body>
</html>"""

    def run_full_review(self) -> CodeQualityMetrics:
        """Run complete code review"""
        print("=" * 80)
        print("🚀 AUTOMATED CODE REVIEW")
        print("=" * 80)
        print()

        # Run all checks
        black_ok, black_files = self.run_black()
        isort_ok, isort_files = self.run_isort()
        pylint_score, pylint_violations = self.run_pylint()
        mypy_errors, mypy_warnings = self.run_mypy()
        bandit_issues = self.run_bandit()
        safety_vulns = self.run_safety()
        coverage, passed, failed, total = self.run_tests()

        # Create metrics object
        metrics = CodeQualityMetrics(
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            black_compliant=black_ok,
            black_files_need_formatting=black_files,
            isort_compliant=isort_ok,
            isort_files_need_sorting=isort_files,
            pylint_score=pylint_score,
            pylint_violations=pylint_violations,
            mypy_errors=mypy_errors,
            mypy_warnings=mypy_warnings,
            bandit_issues=bandit_issues,
            safety_vulnerabilities=safety_vulns,
            test_coverage=coverage,
            tests_passed=passed,
            tests_failed=failed,
            tests_total=total
        )

        # Generate reports
        self.generate_report(metrics)

        # Print summary
        print("\n" + "=" * 80)
        print("📊 SUMMARY")
        print("=" * 80)
        print(f"✅ Test Coverage: {coverage:.1f}%")
        print(f"✅ Pylint Score: {pylint_score:.2f}/10")
        print(f"✅ Tests: {passed}/{total} passed")
        print(f"🔒 Security: {bandit_issues['high']} high, {bandit_issues['medium']} medium issues")
        print("=" * 80)

        return metrics


def main():
    """Main entry point"""
    reviewer = CodeReviewAutomation()
    metrics = reviewer.run_full_review()

    # Exit with error if critical issues found
    if metrics.test_coverage < 90 or metrics.bandit_issues["high"] > 0 or metrics.tests_failed > 0:
        print("\n❌ Code review found critical issues!")
        sys.exit(1)
    else:
        print("\n✅ Code review passed all checks!")
        sys.exit(0)


if __name__ == "__main__":
    main()
