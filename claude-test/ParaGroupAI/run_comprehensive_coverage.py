#!/usr/bin/env python3
"""
Comprehensive Coverage Test Runner
Runs tests for all specified files and reports coverage
"""

import subprocess
import sys
from pathlib import Path
from typing import List, Dict, Tuple

# Target files as specified by user
TARGET_FILES = [
    "third_party_validation/run_validation.py",
    "transform_mocks_to_real_tests.py",
    "ultrathink.py",
    "update_realtime_metrics.py",
    "validate_my_response.py",
    "validation_loop.py",
    "verbose_logger.py",
    "api/__init__.py",
    "api/health_endpoints.py",
    "api/main.py",
    "api/orchestrator_integration.py",
    "claude_integration.py",
    "agent_framework/agentic_search.py",
    "agent_framework/code_generator.py",
    "agent_framework/context_manager.py",
    "agent_framework/context_manager_enhanced.py"
]

def check_file_coverage(file_path: str, test_dir: str = "tests/unit_instance5") -> Tuple[bool, float, str]:
    """Check coverage for a single file"""
    module_name = Path(file_path).stem
    test_file = Path(test_dir) / f"test_{module_name}.py"

    if not test_file.exists():
        return False, 0.0, f"Test file not found: {test_file}"

    # Run pytest with coverage for this specific file
    cmd = [
        "pytest",
        str(test_file),
        f"--cov={file_path.replace('.py', '').replace('/', '.')}",
        "--cov-report=term",
        "--tb=no",
        "-q"
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )

        # Parse coverage from output
        output = result.stdout + result.stderr
        coverage = 0.0

        # Look for coverage percentage in output
        lines = output.split('\n')
        for line in lines:
            if 'TOTAL' in line or file_path.replace('/', '.').replace('.py', '') in line:
                parts = line.split()
                for part in parts:
                    if '%' in part:
                        try:
                            coverage = float(part.strip('%'))
                            break
                        except:
                            pass

        success = coverage >= 90.0
        return success, coverage, output if not success else "PASSED"

    except subprocess.TimeoutExpired:
        return False, 0.0, "Test timed out"
    except Exception as e:
        return False, 0.0, f"Error: {e}"

def main():
    """Main test runner"""
    print("="*80)
    print("🔬 COMPREHENSIVE COVERAGE TEST RUNNER")
    print("="*80)
    print(f"Testing {len(TARGET_FILES)} files for 90%+ coverage requirement\n")

    results = []
    passed = 0
    failed = 0

    for file_path in TARGET_FILES:
        print(f"📝 Testing: {file_path}")

        success, coverage, message = check_file_coverage(file_path)

        if success:
            print(f"  ✅ PASSED: {coverage:.1f}% coverage")
            passed += 1
        else:
            print(f"  ❌ FAILED: {coverage:.1f}% coverage")
            if coverage < 90:
                print(f"     Reason: Coverage below 90% threshold")
            failed += 1

        results.append({
            "file": file_path,
            "coverage": coverage,
            "passed": success,
            "message": message
        })

    # Summary
    print("\n" + "="*80)
    print("📊 SUMMARY REPORT")
    print("="*80)

    print(f"\nTotal Files: {len(TARGET_FILES)}")
    print(f"✅ Passed: {passed} files")
    print(f"❌ Failed: {failed} files")
    print(f"Success Rate: {(passed/len(TARGET_FILES)*100):.1f}%")

    # Detailed failure report
    if failed > 0:
        print("\n🔴 FILES REQUIRING ATTENTION:")
        for result in results:
            if not result["passed"]:
                print(f"\n  {result['file']}:")
                print(f"    Current coverage: {result['coverage']:.1f}%")
                print(f"    Required: 90.0%")
                print(f"    Gap: {90.0 - result['coverage']:.1f}%")

    # Action items
    print("\n" + "="*80)
    print("📝 NEXT STEPS")
    print("="*80)

    if failed > 0:
        print("\n1. For each failed file, improve test coverage by:")
        print("   - Adding more test cases for untested functions")
        print("   - Testing edge cases and error conditions")
        print("   - Covering all code branches and conditionals")
        print("\n2. Run coverage report for specific file:")
        print("   pytest tests/unit_instance5/test_FILE.py --cov=MODULE --cov-report=html")
        print("\n3. Check htmlcov/index.html to see uncovered lines")
    else:
        print("\n✅ All files meet the 90% coverage requirement!")
        print("🎉 Production-ready test suite achieved!")

    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())