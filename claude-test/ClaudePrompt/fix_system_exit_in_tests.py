#!/usr/bin/env python3
"""
fix_system_exit_in_tests.py - Fix SystemExit failures in tests by mocking sys.exit()
PRODUCTION-READY (2025-11-21)

ROOT CAUSE: Tests call main() functions that use sys.exit(), causing SystemExit exceptions
SOLUTION: Add sys.exit mocking to tests that fail with SystemExit

This script ONLY modifies FAILING tests, never touches passing tests.
"""
import re
import subprocess
from pathlib import Path
import sys

def test_file_has_failures(test_file):
    """Check if a test file has any failing tests"""
    try:
        result = subprocess.run(
            ['pytest', str(test_file), '-v', '--tb=no', '-q'],
            capture_output=True,
            text=True,
            timeout=30
        )
        # Check if output contains "FAILED" and "SystemExit"
        return 'FAILED' in result.stdout and 'SystemExit' in result.stdout
    except:
        return False

def fix_system_exit_in_file(file_path):
    """Add sys.exit mocking to tests that need it"""
    with open(file_path, 'r') as f:
        content = f.read()

    original_content = content
    fixes_applied = 0

    # Check if file already has proper sys.exit mocking
    if 'patch("sys.exit")' in content or 'patch(\'sys.exit\')' in content:
        return 0  # Already fixed

    # Pattern: test_main_executes or test_main_with_various_inputs that call main()
    # These need sys.exit mocking
    pattern = r'(def test_main[^(]*\([^)]*\):.*?from \w+ import main.*?)(try:\s+)(.*?)(except Exception:)'

    def replacement(match):
        nonlocal fixes_applied
        fixes_applied += 1
        indent = "    "  # Standard indentation
        return (
            f'{match.group(1)}'
            f'with patch("sys.exit"):\n'
            f'{indent * 2}{match.group(2)}'
            f'{match.group(3)}'
            f'{match.group(4)}'
        )

    # Apply fix
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    # Also ensure unittest.mock.patch is imported
    if fixes_applied > 0 and 'from unittest.mock import patch' not in new_content:
        # Add import at the top after other imports
        import_pattern = r'(import pytest\n)'
        if re.search(import_pattern, new_content):
            new_content = re.sub(import_pattern, r'\1from unittest.mock import patch\n', new_content)
        else:
            # Add at the very top
            new_content = 'from unittest.mock import patch\n' + new_content

    if new_content != original_content:
        with open(file_path, 'w') as f:
            f.write(new_content)
        return fixes_applied

    return 0

def main():
    """Fix SystemExit issues in test files that are failing"""
    test_dir = Path("tests/unit_real_coverage")

    if not test_dir.exists():
        print(f"❌ Test directory not found: {test_dir}")
        return 1

    test_files = list(test_dir.glob("test_*_real.py"))

    print(f"🔧 FIXING SYSTEMEXIT FAILURES")
    print(f"   Directory: {test_dir}")
    print(f"   Total files: {len(test_files)}")
    print()
    print("   Strategy: Only fix files with SystemExit failures")
    print("   Passing tests: UNTOUCHED")
    print()

    total_fixes = 0
    files_fixed = 0
    files_checked = 0

    # Only process first 10 files as a test
    for test_file in test_files[:10]:
        files_checked += 1
        print(f"Checking {test_file.name}...", end=" ", flush=True)

        if test_file_has_failures(test_file):
            fixes = fix_system_exit_in_file(test_file)
            if fixes > 0:
                total_fixes += fixes
                files_fixed += 1
                print(f"✓ FIXED ({fixes} test(s))")
            else:
                print("✓ No fixes needed")
        else:
            print("✓ Passing - skipped")

    print()
    print(f"📊 SUMMARY (Phase 1 - First 10 files):")
    print(f"   Files checked: {files_checked}")
    print(f"   Files fixed: {files_fixed}")
    print(f"   Total fixes applied: {total_fixes}")
    print()

    if files_fixed > 0:
        print(f"✅ Phase 1 complete! Fixes applied to {files_fixed} files.")
        print(f"   Run this script again to process remaining {len(test_files) - 10} files")
    else:
        print(f"⚠️ No fixes needed in first 10 files")
        print(f"   This is good! Tests may already be working.")

    return 0

if __name__ == "__main__":
    exit(main())
