#!/usr/bin/env python3
"""
Fix syntax errors in generated test files.
Main issue: {func_name} in f-strings being interpreted as set literals.
"""

import os
import re
from pathlib import Path

def fix_test_file(file_path: Path) -> int:
    """Fix syntax errors in a single test file"""
    fixes_made = 0

    with open(file_path, 'r') as f:
        content = f.read()

    original_content = content

    # Fix patterns that cause syntax errors
    patterns = [
        # Fix {func_name}() -> func_name()
        (r'result = {func_name}\(\)', 'result = func_name()'),
        (r'{func_name}\(\)', 'func_name()'),

        # Fix {class_name}() -> class_name()
        (r'instance = {class_name}\(\)', 'instance = class_name()'),
        (r'{class_name}\(\)', 'class_name()'),

        # Fix mock function calls
        (r'mock_{func_name}', 'mock_func'),
        (r'{func_name}_value', 'func_value'),

        # Fix test method names with {
        (r'def test_{func_name}_', 'def test_func_'),
        (r'def test_{class_name}_', 'def test_class_'),

        # Fix f-strings with improper formatting
        (r'\{(\w+)\}', r'\1'),  # Remove unnecessary braces

        # Fix import statements
        (r'from {module_name} import {func_name}', 'from module_name import func_name'),
        (r'from {module_name} import {class_name}', 'from module_name import class_name'),

        # Fix docstrings
        (r'"""Test {func_name}', '"""Test function'),
        (r'"""Test {class_name}', '"""Test class'),

        # Fix patch statements
        (r"patch\('{module_name}.{func_name}'\)", "patch('module.function')"),
        (r"patch\('{module_name}.{class_name}'\)", "patch('module.ClassName')"),
    ]

    for pattern, replacement in patterns:
        new_content = re.sub(pattern, replacement, content)
        if new_content != content:
            fixes_made += len(re.findall(pattern, content))
            content = new_content

    # More complex fixes for actual function imports
    # Extract the actual module name from imports
    module_match = re.search(r'^import (\w+)$', content, re.MULTILINE)
    if module_match:
        module_name = module_match.group(1)

        # Replace placeholders with actual module name
        content = re.sub(r'from module_name import', f'from {module_name} import', content)
        content = re.sub(r"patch\('module\.", f"patch('{module_name}.", content)

        # Fix function names in imports
        func_imports = re.findall(r'from ' + module_name + r' import (\w+)', content)
        for func in func_imports:
            if func not in ['Mock', 'MagicMock', 'patch']:
                # Fix references to this function
                content = re.sub(f'func_name', func, content, count=10)  # Limit replacements
                content = re.sub(f'test_func_', f'test_{func}_', content)
                break

    # Write back if changes were made
    if content != original_content:
        with open(file_path, 'w') as f:
            f.write(content)
        print(f"✅ Fixed {fixes_made} syntax issues in {file_path.name}")
    else:
        print(f"ℹ️  No syntax issues found in {file_path.name}")

    return fixes_made

def main():
    """Fix syntax errors in all test files"""
    test_dir = Path("tests/unit_instance2")

    if not test_dir.exists():
        print("❌ Test directory not found!")
        return 1

    print("=" * 80)
    print("🔧 FIXING SYNTAX ERRORS IN GENERATED TEST FILES")
    print("=" * 80)

    total_fixes = 0
    test_files = list(test_dir.glob("test_*.py"))

    for test_file in test_files:
        fixes = fix_test_file(test_file)
        total_fixes += fixes

    print("\n" + "=" * 80)
    print(f"✅ FIXED {total_fixes} SYNTAX ERRORS IN {len(test_files)} FILES")
    print("=" * 80)

    return 0

if __name__ == "__main__":
    exit(main())