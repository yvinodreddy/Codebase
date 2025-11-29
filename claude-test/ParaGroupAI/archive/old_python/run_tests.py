#!/usr/bin/env python3
"""
Comprehensive Test Runner for ULTRATHINK
Runs all test suites with coverage reporting
"""

import sys
import subprocess
from pathlib import Path


def run_command(cmd, description):
    """Run command and print status"""
    print(f"\n{'='*70}")
    print(f"{description}")
    print(f"{'='*70}")

    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

    print(result.stdout)
    if result.stderr:
        print(result.stderr)

    return result.returncode == 0


def main():
    """Run all tests"""
    print("="*70)
    print("ULTRATHINK COMPREHENSIVE TEST SUITE")
    print("="*70)

    results = {}

    # Check if pytest is installed
    try:
        import pytest
        print("✅ pytest found")
    except ImportError:
        print("❌ pytest not installed. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pytest", "pytest-cov"])

    # 1. Run critical path tests
    success = run_command(
        f"{sys.executable} -m pytest tests/test_critical_path.py -v",
        "T1: CRITICAL PATH TESTS"
    )
    results["Critical Path (T1)"] = success

    # 2. Run integration tests
    success = run_command(
        f"{sys.executable} -m pytest tests/test_integration.py -v",
        "T2: INTEGRATION TESTS"
    )
    results["Integration (T2)"] = success

    # 3. Run security tests
    success = run_command(
        f"{sys.executable} -m pytest tests/test_security.py -v",
        "T3: SECURITY TESTS"
    )
    results["Security (T3)"] = success

    # 4. Run performance tests
    success = run_command(
        f"{sys.executable} -m pytest tests/test_performance.py -v -s",
        "T4: PERFORMANCE TESTS"
    )
    results["Performance (T4)"] = success

    # 5. Run end-to-end tests
    success = run_command(
        f"{sys.executable} -m pytest tests/test_end_to_end.py -v",
        "T6: END-TO-END TESTS"
    )
    results["End-to-End (T6)"] = success

    # 6. Run all tests with coverage
    success = run_command(
        f"{sys.executable} -m pytest tests/ -v --cov=. --cov-report=term-missing --cov-report=html --cov-report=json",
        "ALL TESTS WITH COVERAGE"
    )
    results["Coverage Report"] = success

    # Print summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)

    passed = sum(1 for v in results.values() if v)
    total = len(results)

    for name, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {name}")

    print(f"\nTotal: {passed}/{total} test suites passed")

    if passed == total:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test suite(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
