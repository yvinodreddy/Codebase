#!/usr/bin/env python3
"""
Check coverage for the 16 target modules
"""
import subprocess
import sys
from pathlib import Path

# List of all modules to test
modules = [
    "fix_test_files_complete",
    "generate_100_percent_tests",
    "generate_effective_tests",
    "generate_real_coverage_tests",
    "generate_real_test_fixed",
    "generate_real_test_implementations",
    "generate_real_tests_for_module",
    "get_coverage_quickly",
    "get_live_context_metrics",
    "high_scale_orchestrator",
    "instance_id_manager",
    "large_scale_error_handler",
    "live_metrics_tracker",
    "master_orchestrator",
    "metrics_aggregator",
    "metrics_state_persistence"
]

print("=" * 80)
print("🔍 CHECKING COVERAGE FOR 16 TARGET MODULES")
print("=" * 80)

# Create coverage command with specific module includes
coverage_sources = ",".join(modules)

# Run pytest with coverage for specific modules
cmd = [
    "pytest",
    "tests/unit_instance3/",
    f"--cov={coverage_sources}",
    "--cov-report=term-missing",
    "--cov-report=html",
    "--tb=short",
    "-q"
]

print(f"\n📊 Running: {' '.join(cmd)}\n")

try:
    result = subprocess.run(cmd, capture_output=True, text=True)

    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)

    # Parse coverage from output
    lines = result.stdout.split('\n')
    for line in lines:
        if 'TOTAL' in line or any(mod in line for mod in modules):
            print(line)

    # Check if we met the 90% target
    for line in lines:
        if 'TOTAL' in line:
            parts = line.split()
            if len(parts) >= 4:
                try:
                    coverage_pct = float(parts[-1].rstrip('%'))
                    print(f"\n📈 Total Coverage: {coverage_pct}%")
                    if coverage_pct >= 90:
                        print("✅ SUCCESS: Coverage target of 90% met!")
                    else:
                        print(f"⚠️  WARNING: Coverage {coverage_pct}% is below 90% target")
                except:
                    pass

except Exception as e:
    print(f"❌ Error running coverage: {e}")
    sys.exit(1)

print("\n📁 HTML coverage report generated in: htmlcov/index.html")