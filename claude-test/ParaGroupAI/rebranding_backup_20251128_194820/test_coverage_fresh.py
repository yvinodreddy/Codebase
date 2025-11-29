#!/usr/bin/env python3
"""
Fresh Coverage Test Runner
Creates a clean environment for testing
"""

import subprocess
import sys
import os
from pathlib import Path
import tempfile
import shutil

# Target files as specified
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

def test_single_file(file_path: str):
    """Test a single file in a clean environment"""
    module_name = Path(file_path).stem
    test_file = Path("tests/unit_instance5") / f"test_{module_name}.py"

    if not test_file.exists():
        return 0.0, "Test file not found"

    # Create temporary directory for clean coverage
    with tempfile.TemporaryDirectory() as tmpdir:
        # Set coverage directory to temp location
        env = os.environ.copy()
        env['COVERAGE_FILE'] = f"{tmpdir}/.coverage"

        # Run pytest with clean coverage
        cmd = [
            "python3", "-m", "pytest",
            str(test_file),
            f"--cov={file_path.replace('.py', '').replace('/', '.')}",
            "--cov-report=term",
            "--tb=no",
            "-q",
            "--no-header"
        ]

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                env=env,
                cwd=Path.cwd(),
                timeout=30
            )

            # Parse coverage from output
            output = result.stdout + result.stderr

            # Simple parsing - look for percentage
            for line in output.split('\n'):
                if 'TOTAL' in line or module_name in line:
                    parts = line.split()
                    for i, part in enumerate(parts):
                        if '%' in part:
                            try:
                                return float(part.strip('%')), "OK"
                            except:
                                pass
                        # Also check next item after numbers
                        if i > 2 and parts[i-1].isdigit():
                            try:
                                return float(part.strip('%')), "OK"
                            except:
                                pass

            # If no coverage found, check if tests passed
            if "passed" in output:
                # Tests passed but coverage not measured properly
                return 0.0, "Tests passed but coverage not measured"
            else:
                return 0.0, "Tests failed or error occurred"

        except subprocess.TimeoutExpired:
            return 0.0, "Test timeout"
        except Exception as e:
            return 0.0, f"Error: {e}"

def main():
    """Run fresh coverage tests"""
    print("="*80)
    print("🧪 FRESH COVERAGE TEST RUNNER")
    print("="*80)
    print("Testing with clean coverage environment\n")

    results = []
    total_coverage = 0.0
    files_tested = 0

    for file_path in TARGET_FILES:
        print(f"Testing: {file_path}")
        coverage, status = test_single_file(file_path)

        icon = "✅" if coverage >= 90 else "❌"
        print(f"  {icon} Coverage: {coverage:.1f}% - {status}")

        results.append({
            "file": file_path,
            "coverage": coverage,
            "status": status
        })

        if coverage > 0:
            total_coverage += coverage
            files_tested += 1

    # Summary
    print("\n" + "="*80)
    print("📊 SUMMARY")
    print("="*80)

    avg_coverage = total_coverage / files_tested if files_tested > 0 else 0
    print(f"\nAverage Coverage: {avg_coverage:.1f}%")
    print(f"Files with Coverage: {files_tested}/{len(TARGET_FILES)}")

    # List files needing work
    files_below_90 = [r for r in results if r["coverage"] < 90]
    if files_below_90:
        print(f"\n❌ {len(files_below_90)} files need improvement:")
        for r in files_below_90:
            print(f"  - {r['file']}: {r['coverage']:.1f}%")

    return 0 if avg_coverage >= 90 else 1

if __name__ == "__main__":
    # Clean up any existing coverage files first
    for cov_file in Path.cwd().glob(".coverage*"):
        try:
            cov_file.unlink()
        except:
            pass

    sys.exit(main())