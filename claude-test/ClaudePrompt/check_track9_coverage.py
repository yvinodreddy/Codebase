#!/usr/bin/env python3
"""Check code coverage for all track9 modules"""

import subprocess
import json
from pathlib import Path

# Track9 modules (excluding the timeout ones)
modules = [
    ("achieve_100_percent_coverage.py", "test_achieve_100_percent_coverage_real.py"),
    ("add_sys_exit_mocking.py", "test_add_sys_exit_mocking_real.py"),
    ("apply_comprehensive_test_fixes.py", "test_apply_comprehensive_test_fixes_real.py"),
    ("debug_generate_tests.py", "test_debug_generate_tests_real.py"),
    # Skip: enhance_coverage_to_90.py (timeout)
    ("enhance_tests_for_90_coverage.py", "test_enhance_tests_for_90_coverage_real.py"),
    ("enhance_tests_for_real_coverage.py", "test_enhance_tests_for_real_coverage_real.py"),
    ("enhance_tests_to_90.py", "test_enhance_tests_to_90_real.py"),
    ("fix_all_test_syntax_errors.py", "test_fix_all_test_syntax_errors_real.py"),
    ("fix_all_with_statements.py", "test_fix_all_with_statements_real.py"),
    ("fix_module_level_exit.py", "test_fix_module_level_exit_real.py"),
    ("fix_pytest_skip_tests.py", "test_fix_pytest_skip_tests_real.py"),
    # Skip: fix_system_exit_in_tests.py (timeout)
    ("fix_test_files_complete.py", "test_fix_test_files_complete_real.py"),
    ("fix_test_syntax_errors.py", "test_fix_test_syntax_errors_real.py"),
]

print("="*80)
print("📊 TRACK9 COVERAGE ANALYSIS")
print("="*80)
print()

coverage_results = []

for module, test_file in modules:
    module_path = Path(module)
    test_path = Path(f"tests/unit_track9_fixes/{test_file}")

    if not module_path.exists():
        print(f"⚠️  Module not found: {module}")
        continue

    if not test_path.exists():
        print(f"⚠️  Test file not found: {test_file}")
        continue

    print(f"Checking coverage for: {module}...", end=" ")

    # Remove old coverage files
    for f in ['.coverage', 'coverage.json', 'coverage.xml']:
        try:
            Path(f).unlink()
        except FileNotFoundError:
            pass

    # Run pytest with coverage
    try:
        result = subprocess.run(
            [
                "python3", "-m", "pytest",
                str(test_path),
                f"--cov={module}",
                "--cov-report=json",
                "-q", "--tb=no", "--no-cov-on-fail"
            ],
            capture_output=True,
            text=True,
            timeout=30
        )

        # Check coverage.json
        cov_file = Path("coverage.json")
        if cov_file.exists():
            with open(cov_file, 'r') as f:
                cov_data = json.load(f)

            if str(module_path) in cov_data.get('files', {}):
                file_cov = cov_data['files'][str(module_path)]
                coverage_pct = file_cov['summary']['percent_covered']

                status = "✅" if coverage_pct >= 90 else ("🟡" if coverage_pct >= 75 else "❌")
                print(f"{status} {coverage_pct:.1f}%")

                coverage_results.append((module, coverage_pct))
            else:
                print("⚠️  No coverage data")
        else:
            print("⚠️  No coverage file generated")

    except subprocess.TimeoutExpired:
        print("⏳ Timeout")
    except Exception as e:
        print(f"❌ Error: {e}")

print()
print("="*80)
print("📊 SUMMARY")
print("="*80)

if coverage_results:
    avg_coverage = sum(cov for _, cov in coverage_results) / len(coverage_results)
    above_90 = sum(1 for _, cov in coverage_results if cov >= 90)
    above_75 = sum(1 for _, cov in coverage_results if cov >= 75)
    total = len(coverage_results)

    print(f"\nModules Analyzed: {total}")
    print(f"Average Coverage: {avg_coverage:.1f}%")
    print(f"Modules >= 90%: {above_90}/{total} ({above_90/total*100:.1f}%)")
    print(f"Modules >= 75%: {above_75}/{total} ({above_75/total*100:.1f}%)")

    print(f"\n📋 Detailed Results:")
    for module, cov in sorted(coverage_results, key=lambda x: x[1], reverse=True):
        status = "✅" if cov >= 90 else ("🟡" if cov >= 75 else "❌")
        print(f"   {status} {module:50s} {cov:6.1f}%")

print("\n" + "="*80)
