#!/usr/bin/env python3
"""
Achieve 100% Coverage for Track9 Modules
Analyzes coverage gaps and generates targeted tests
"""

import subprocess
import json
import ast
from pathlib import Path
from typing import Dict, List, Tuple, Set

class Track9CoverageCompleter:
    """Completes coverage to 100% for all Track9 modules"""

    def __init__(self):
        self.modules = [
            "achieve_100_percent_coverage.py",
            "add_sys_exit_mocking.py",
            "apply_comprehensive_test_fixes.py",
            "debug_generate_tests.py",
            "enhance_tests_for_90_coverage.py",
            "enhance_tests_for_real_coverage.py",
            "enhance_tests_to_90.py",
            "fix_all_test_syntax_errors.py",
            "fix_all_with_statements.py",
            "fix_module_level_exit.py",
            "fix_pytest_skip_tests.py",
            "fix_test_files_complete.py",
            "fix_test_syntax_errors.py",
        ]
        self.test_dir = Path("tests/unit_track9_fixes")

    def get_coverage_gaps(self, module: str) -> Tuple[float, List[int], List[str]]:
        """Get coverage percentage, missing lines, and missing line content"""
        test_file = self.test_dir / f"test_{Path(module).stem}_real.py"

        if not Path(module).exists() or not test_file.exists():
            return (0.0, [], [])

        # Clean old coverage files
        for f in ['.coverage', 'coverage.json']:
            try:
                Path(f).unlink()
            except FileNotFoundError:
                pass

        # Run coverage
        try:
            result = subprocess.run(
                [
                    "python3", "-m", "pytest",
                    str(test_file),
                    f"--cov={module}",
                    "--cov-report=json",
                    "--cov-report=term-missing",
                    "-q", "--tb=no"
                ],
                capture_output=True,
                text=True,
                timeout=30
            )

            # Parse coverage data
            cov_file = Path("coverage.json")
            if cov_file.exists():
                with open(cov_file, 'r') as f:
                    cov_data = json.load(f)

                if module in cov_data.get('files', {}):
                    file_data = cov_data['files'][module]
                    percent = file_data['summary']['percent_covered']
                    missing_lines = file_data.get('missing_lines', [])

                    # Get actual line content
                    missing_content = []
                    if missing_lines:
                        with open(module, 'r') as f:
                            lines = f.readlines()
                        missing_content = [
                            f"Line {ln}: {lines[ln-1].strip()}"
                            for ln in missing_lines
                            if ln <= len(lines)
                        ]

                    return (percent, missing_lines, missing_content)

        except (subprocess.TimeoutExpired, FileNotFoundError, Exception) as e:
            print(f"  ⚠️  Error analyzing {module}: {e}")

        return (0.0, [], [])

    def analyze_missing_line_type(self, module: str, line_num: int) -> str:
        """Determine what type of code is on a missing line"""
        try:
            with open(module, 'r') as f:
                lines = f.readlines()

            if line_num > len(lines):
                return "unknown"

            line = lines[line_num - 1].strip()

            # Classify the line
            if not line or line.startswith('#'):
                return "comment"
            elif 'if ' in line and ':' in line:
                return "if_branch"
            elif 'elif ' in line:
                return "elif_branch"
            elif line.startswith('else:'):
                return "else_branch"
            elif 'except' in line or 'raise ' in line:
                return "exception"
            elif 'return ' in line:
                return "return_statement"
            elif line.startswith('def '):
                return "function_def"
            elif line.startswith('class '):
                return "class_def"
            else:
                return "code_line"

        except Exception:
            return "unknown"

    def generate_test_for_missing_line(self, module: str, line_num: int, line_type: str) -> str:
        """Generate a test case to cover a missing line"""
        module_name = Path(module).stem

        if line_type == "if_branch":
            return f"""
    def test_cover_line_{line_num}(self):
        '''Test to cover line {line_num} - {line_type}'''
        # TODO: Add test to execute the if branch at line {line_num}
        # Import the function and call with parameters that trigger this branch
        pass
"""
        elif line_type == "else_branch":
            return f"""
    def test_cover_line_{line_num}(self):
        '''Test to cover line {line_num} - {line_type}'''
        # TODO: Add test to execute the else branch at line {line_num}
        # Import the function and call with parameters that trigger this branch
        pass
"""
        elif line_type == "exception":
            return f"""
    def test_cover_line_{line_num}_exception(self):
        '''Test to cover line {line_num} - exception handling'''
        # TODO: Add test to trigger the exception at line {line_num}
        pass
"""
        else:
            return f"""
    def test_cover_line_{line_num}(self):
        '''Test to cover line {line_num}'''
        # TODO: Add test to execute line {line_num}
        pass
"""

    def run(self):
        """Main execution"""
        print("="*80)
        print("🎯 TRACK9 - ACHIEVING 100% COVERAGE")
        print("="*80)
        print()

        results = []

        for module in self.modules:
            if not Path(module).exists():
                print(f"⚠️  Skipping {module} (not found)")
                continue

            print(f"📊 Analyzing: {module}")

            coverage, missing_lines, missing_content = self.get_coverage_gaps(module)

            if coverage == 0.0:
                print(f"  ⚠️  Could not analyze coverage (timeout or error)")
                continue

            status = "✅" if coverage >= 90 else "🔴"
            print(f"  {status} Current coverage: {coverage:.1f}%")

            if missing_lines:
                print(f"  📝 Missing lines: {len(missing_lines)}")
                for content in missing_content[:5]:  # Show first 5
                    print(f"     - {content}")
                if len(missing_content) > 5:
                    print(f"     ... and {len(missing_content) - 5} more")

            results.append({
                'module': module,
                'coverage': coverage,
                'missing_lines': missing_lines,
                'missing_count': len(missing_lines)
            })
            print()

        # Summary
        print("="*80)
        print("📊 COVERAGE SUMMARY")
        print("="*80)

        if results:
            avg_coverage = sum(r['coverage'] for r in results) / len(results)
            total_missing = sum(r['missing_count'] for r in results)
            above_90 = sum(1 for r in results if r['coverage'] >= 90)

            print(f"\nModules Analyzed: {len(results)}")
            print(f"Average Coverage: {avg_coverage:.1f}%")
            print(f"Modules >= 90%: {above_90}/{len(results)}")
            print(f"Total Missing Lines: {total_missing}")

            print(f"\n📋 Priority List (lowest coverage first):")
            for r in sorted(results, key=lambda x: x['coverage']):
                status = "✅" if r['coverage'] >= 90 else "🔴"
                print(f"  {status} {r['module']:50s} {r['coverage']:6.1f}% ({r['missing_count']} lines missing)")

        print("\n" + "="*80)

        return results


def main():
    completer = Track9CoverageCompleter()
    results = completer.run()

    # Save results
    with open('track9_coverage_gaps.json', 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n📄 Detailed results saved to: track9_coverage_gaps.json")


if __name__ == "__main__":
    main()
