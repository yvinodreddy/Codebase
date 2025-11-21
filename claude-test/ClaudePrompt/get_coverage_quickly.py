#!/usr/bin/env python3
"""
Quick coverage measurement script
Runs pytest with coverage and reports results
"""
import subprocess
import json
import sys

print("🔧 Running pytest with coverage measurement...")
print("   This may take 1-2 minutes...")
print()

# Run pytest with coverage
result = subprocess.run(
    ['pytest', 'tests/unit_real_coverage/', '--cov=.', '--cov-report=json', '-q', '--tb=no'],
    capture_output=True,
    text=True,
    timeout=120
)

# Check if coverage.json was created
try:
    with open('coverage.json') as f:
        data = json.load(f)

    coverage_pct = data['totals']['percent_covered']
    covered = data['totals']['covered_lines']
    total = data['totals']['num_statements']

    print(f"✅ COVERAGE MEASUREMENT COMPLETE")
    print(f"")
    print(f"   Coverage: {coverage_pct:.2f}%")
    print(f"   Lines covered: {covered:,}")
    print(f"   Total lines: {total:,}")
    print(f"   Gap to 99%: {99 - coverage_pct:.2f}%")
    print(f"")

    # Count test results from output
    output_lines = result.stdout.split('\n')
    for line in output_lines[-15:]:
        if 'passed' in line or 'failed' in line:
            print(f"   {line.strip()}")

    sys.exit(0)

except Exception as e:
    print(f"❌ Error reading coverage.json: {e}")
    print(f"")
    print(f"Pytest output:")
    print(result.stdout[-500:])
    sys.exit(1)
