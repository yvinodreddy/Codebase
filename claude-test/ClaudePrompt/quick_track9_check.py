#!/usr/bin/env python3
"""Quick check of all track9 _real.py test files"""

import subprocess
from pathlib import Path

test_files = sorted(Path("tests/unit_track9_fixes").glob("test_*_real.py"))

print(f"Testing {len(test_files)} files...\n")

total_passed = 0
total_failed = 0
results = []

for test_file in test_files:
    print(f"Testing: {test_file.name}...", end=" ")

    try:
        result = subprocess.run(
            ["python3", "-m", "pytest", str(test_file), "-q", "--no-cov", "--tb=no"],
            capture_output=True,
            text=True,
            timeout=30
        )

        output = result.stdout + result.stderr

        # Parse output for passed/failed count
        import re
        match = re.search(r'(\d+) passed', output)
        passed = int(match.group(1)) if match else 0

        match = re.search(r'(\d+) failed', output)
        failed = int(match.group(1)) if match else 0

        total_passed += passed
        total_failed += failed

        status = "✅" if failed == 0 else "❌"
        print(f"{status} {passed} passed, {failed} failed")

        results.append((test_file.name, passed, failed))

    except subprocess.TimeoutExpired:
        print("⏳ TIMEOUT")
        results.append((test_file.name, 0, 0))
    except Exception as e:
        print(f"❌ ERROR: {e}")
        results.append((test_file.name, 0, 0))

print("\n" + "="*60)
print(f"TOTAL: {total_passed} passed, {total_failed} failed")
success_rate = (total_passed / (total_passed + total_failed) * 100) if (total_passed + total_failed) > 0 else 0
print(f"Success Rate: {success_rate:.1f}%")
print("="*60)
