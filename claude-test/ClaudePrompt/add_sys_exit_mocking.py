#!/usr/bin/env python3
"""
add_sys_exit_mocking.py - Add sys.exit mocking to tests that need it
SIMPLE AND DIRECT (2025-11-21)

Adds `with patch("sys.exit"):` to test functions that call main()
"""
import re
from pathlib import Path

def fix_file(file_path):
    """Add sys.exit mocking to a single test file"""
    with open(file_path, 'r') as f:
        content = f.read()

    original_content = content

    # Pattern: test function that imports and calls main()
    # OLD:
    #     from module import main
    #     try:
    #         result = main()
    # NEW:
    #     from module import main
    #     with patch("sys.exit"):
    #         try:
    #             result = main()

    pattern = r'(def test_main[^\n]+\n[^\n]*"""[^"]*""")\n(\s+)(from \w+ import main)\n(\s+)(try:)'

    def add_mock(match):
        indent = match.group(4)  # Get indentation from 'try:'
        return (
            f'{match.group(1)}\n'
            f'{match.group(2)}{match.group(3)}\n'
            f'{indent}with patch("sys.exit"):\n'
            f'{indent}    {match.group(5)}'
        )

    content = re.sub(pattern, add_mock, content)

    # Ensure import exists
    if 'with patch("sys.exit")' in content and 'from unittest.mock import patch' not in content:
        # Add import after pytest import
        content = re.sub(
            r'(import pytest\n)',
            r'\1from unittest.mock import patch\n',
            content
        )

    if content != original_content:
        with open(file_path, 'w') as f:
            f.write(content)
        return True
    return False

def main():
    test_dir = Path("tests/unit_real_coverage")
    test_files = list(test_dir.glob("test_*_real.py"))

    print(f"🔧 Adding sys.exit mocking to {len(test_files)} test files")
    print()

    fixed = 0
    for test_file in test_files:
        if fix_file(test_file):
            fixed += 1
            print(f"✓ {test_file.name}")

    print()
    print(f"📊 Fixed {fixed} files")
    return 0

if __name__ == "__main__":
    exit(main())
