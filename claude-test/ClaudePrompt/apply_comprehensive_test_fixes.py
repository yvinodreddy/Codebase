#!/usr/bin/env python3
"""
Apply comprehensive fixes to make generated tests runnable.
Replaces placeholders with actual function/class names from modules.
"""

import os
import re
import ast
from pathlib import Path
from typing import Dict, Set, List, Tuple

def extract_module_elements(module_path: Path) -> Tuple[str, Set[str], Set[str]]:
    """Extract module name, function names, and class names from a module"""
    module_name = module_path.stem
    functions = set()
    classes = set()

    try:
        with open(module_path, 'r') as f:
            source = f.read()
            tree = ast.parse(source)

        for node in tree.body:
            if isinstance(node, ast.FunctionDef):
                if not node.name.startswith('_'):
                    functions.add(node.name)
            elif isinstance(node, ast.ClassDef):
                classes.add(node.name)

    except Exception as e:
        print(f"⚠️  Error parsing {module_path}: {e}")

    return module_name, functions, classes

def fix_test_file_comprehensively(test_file: Path, module_path: Path) -> int:
    """Apply comprehensive fixes to a test file"""
    fixes = 0

    # Extract actual names from module
    module_name, functions, classes = extract_module_elements(module_path)

    with open(test_file, 'r') as f:
        content = f.read()

    original = content

    # Fix imports
    content = re.sub(r'import module_name', f'import {module_name}', content)
    content = re.sub(r'from module_name import', f'from {module_name} import', content)

    # Fix patch decorators and calls
    content = re.sub(r"patch\('module\.", f"patch('{module_name}.", content)
    content = re.sub(r"patch\('module_name\.", f"patch('{module_name}.", content)

    # Replace func_name with actual function names
    if functions:
        # Use the first function for generic replacements
        first_func = list(functions)[0]
        content = re.sub(r'\bfunc_name\b', first_func, content)

        # Fix function-specific tests
        for func in functions:
            # Fix test class names
            old_pattern = f"class TestFunc:"
            new_pattern = f"class Test{func.title().replace('_', '')}:"
            content = re.sub(old_pattern, new_pattern, content)

            # Fix test method names
            content = re.sub(f'def test_func_', f'def test_{func}_', content)

            # Fix imports
            content = re.sub(f'from {module_name} import func_name', f'from {module_name} import {func}', content)

    # Replace class_name with actual class names
    if classes:
        # Use the first class for generic replacements
        first_class = list(classes)[0]
        content = re.sub(r'\bclass_name\b', first_class, content)
        content = re.sub(r'\bClassName\b', first_class, content)

        # Fix class-specific tests
        for cls in classes:
            # Fix test class names
            old_pattern = f"class TestClass:"
            new_pattern = f"class Test{cls}:"
            content = re.sub(old_pattern, new_pattern, content)

            # Fix test method names
            content = re.sub(f'def test_class_', f'def test_{cls.lower()}_', content)

            # Fix imports
            content = re.sub(f'from {module_name} import class_name', f'from {module_name} import {cls}', content)

    # Fix remaining generic placeholders
    content = re.sub(r'function', first_func if functions else 'main', content)
    content = re.sub(r'ClassName', first_class if classes else 'TestClass', content)

    # Fix mock fixtures
    content = re.sub(r'mock_classname', f'mock_{first_class.lower()}' if classes else 'mock_obj', content)

    # Remove any remaining curly braces from non-f-strings
    lines = content.split('\n')
    fixed_lines = []
    for line in lines:
        # Skip f-strings
        if 'f"' not in line and "f'" not in line:
            # Remove standalone curly braces around identifiers
            line = re.sub(r'\{(\w+)\}(?!\s*["\'])', r'\1', line)
        fixed_lines.append(line)
    content = '\n'.join(fixed_lines)

    # Count fixes
    if content != original:
        # Rough count of changes
        fixes = len([1 for a, b in zip(original.split(), content.split()) if a != b])

    # Write back
    with open(test_file, 'w') as f:
        f.write(content)

    return fixes

def main():
    """Apply comprehensive fixes to all test files"""
    test_dir = Path("tests/unit_instance2")
    project_root = Path(".")

    print("=" * 80)
    print("🔧 APPLYING COMPREHENSIVE FIXES TO TEST FILES")
    print("=" * 80)

    # Map test files to source files
    test_to_source = {
        "test_dashboard_cli.py": "dashboard_cli.py",
        "test_dashboard_enhanced.py": "dashboard_enhanced.py",
        "test_dashboard_realtime.py": "dashboard_realtime.py",
        "test_dashboard_redirect.py": "dashboard_redirect.py",
        "test_dashboard_redirect_8889.py": "dashboard_redirect_8889.py",
        "test_dashboard_server.py": "dashboard_server.py",
        "test_enhanced_websocket_broadcast.py": "enhanced_websocket_broadcast.py",
        "test_extract_confidence_from_output.py": "extract_confidence_from_output.py",
        "test_find_broken_tests.py": "find_broken_tests.py",
        "test_find_untested_files.py": "find_untested_files.py",
        "test_fix_all_test_syntax_errors.py": "fix_all_test_syntax_errors.py",
        "test_fix_all_with_statements.py": "fix_all_with_statements.py",
        "test_fix_module_level_exit.py": "fix_module_level_exit.py",
        "test_fix_pytest_skip_tests.py": "fix_pytest_skip_tests.py",
        "test_fix_stuck_agents.py": "fix_stuck_agents.py",
        "test_fix_system_exit_in_tests.py": "fix_system_exit_in_tests.py",
    }

    total_fixes = 0
    for test_file_name, source_file in test_to_source.items():
        test_file = test_dir / test_file_name
        source_path = project_root / source_file

        if test_file.exists() and source_path.exists():
            print(f"\n[Processing] {test_file_name} -> {source_file}")
            fixes = fix_test_file_comprehensively(test_file, source_path)
            total_fixes += fixes
            print(f"  ✅ Applied {fixes} fixes")
        else:
            if not test_file.exists():
                print(f"  ⚠️  Test file not found: {test_file}")
            if not source_path.exists():
                print(f"  ⚠️  Source file not found: {source_path}")

    print("\n" + "=" * 80)
    print(f"✅ APPLIED {total_fixes} FIXES TO TEST FILES")
    print("=" * 80)
    print("\n🚀 Tests should now be runnable. Try:")
    print(f"   pytest tests/unit_instance2 -v")

    return 0

if __name__ == "__main__":
    exit(main())