#!/usr/bin/env python3
"""
Comprehensive fix for ALL incomplete 'with' statements in test files.
Scans each file and removes ALL occurrences.
"""

import re
from pathlib import Path
import ast

def find_and_fix_incomplete_with_statements(filepath: Path) -> int:
    """
    Find and remove all incomplete 'with' statements from a file.
    Returns number of fixes made.
    """
    try:
        content = filepath.read_text()
        lines = content.splitlines(keepends=True)

        fixes_made = 0
        i = 0
        while i < len(lines):
            line = lines[i]

            # Check if this line is a 'with' statement
            stripped = line.strip()
            if stripped.startswith('with ') and stripped.endswith(':'):
                # Check if next line is indented properly (has body)
                if i + 1 < len(lines):
                    next_line = lines[i + 1]
                    current_indent = len(line) - len(line.lstrip())
                    next_indent = len(next_line) - len(next_line.lstrip())

                    # If next line is NOT more indented, this with statement has no body
                    if next_indent <= current_indent and next_line.strip():
                        # Remove this incomplete with statement
                        print(f"  Line {i+1}: Removing incomplete 'with': {line.rstrip()}")
                        del lines[i]
                        fixes_made += 1
                        continue  # Don't increment i, check same index again

            i += 1

        if fixes_made > 0:
            filepath.write_text(''.join(lines))

        return fixes_made

    except Exception as e:
        print(f"  ❌ Error: {e}")
        return 0

def main():
    print("="*80)
    print("COMPREHENSIVE FIX: Remove ALL Incomplete 'with' Statements")
    print("="*80)
    print()

    test_dir = Path("tests/unit_generated")
    test_files = list(test_dir.glob("test_*_comprehensive.py"))

    total_fixes = 0
    files_fixed = 0

    for filepath in sorted(test_files):
        fixes = find_and_fix_incomplete_with_statements(filepath)
        if fixes > 0:
            print(f"✅ {filepath.name}: {fixes} incomplete 'with' statements removed")
            files_fixed += 1
            total_fixes += fixes
        else:
            print(f"   {filepath.name}: No issues found")

    print()
    print("="*80)
    print(f"RESULTS: {files_fixed} files fixed, {total_fixes} total fixes")
    print("="*80)

    # Verify all files are now syntactically valid
    print()
    print("Verifying syntax...")
    errors = []
    for filepath in sorted(test_files):
        try:
            compile(filepath.read_text(), str(filepath), 'exec')
        except SyntaxError as e:
            errors.append(f"{filepath.name}: Line {e.lineno}: {e.msg}")

    if errors:
        print("❌ SYNTAX ERRORS STILL PRESENT:")
        for e in errors:
            print(f"  {e}")
        return 1
    else:
        print(f"✅ ALL {len(test_files)} FILES: SYNTAX VALID")
        return 0

if __name__ == "__main__":
    exit(main())
