#!/usr/bin/env python3
"""
Debug version of generate_real_test_implementations.py to understand why replacements aren't working
"""

import os
import ast
import re
from pathlib import Path

# Set project root
project_root = Path(__file__).parent
tests_dir = project_root / "tests" / "unit_generated"

# Test with one file
test_file = tests_dir / "test_ultrathink_comprehensive.py"
source_file = project_root / "ultrathink.py"

print(f"Test file exists: {test_file.exists()}")
print(f"Source file exists: {source_file.exists()}")

# Parse source file
with open(source_file, 'r') as f:
    source_code = f.read()
    tree = ast.parse(source_code)

# Extract function names
functions = {}
for node in ast.walk(tree):
    if isinstance(node, ast.FunctionDef):
        print(f"Found function: {node.name} (starts with _: {node.name.startswith('_')})")
        if not node.name.startswith('_'):
            functions[node.name] = {"name": node.name}

print(f"\nFunctions available for testing: {list(functions.keys())}")

# Read test file
with open(test_file, 'r') as f:
    test_content = f.read()

# Find test functions with placeholders
lines = test_content.split('\n')
for i, line in enumerate(lines):
    if 'def test_' in line:
        test_match = re.search(r'def (test_\w+)\(self', line)
        if test_match:
            test_name = test_match.group(1)
            # Check if next lines contain placeholder
            if i + 3 < len(lines):
                next_lines = '\n'.join(lines[i:i+5])
                if 'assert True  # Placeholder' in next_lines:
                    # Extract function name
                    func_name = test_name.replace('test_', '').replace('_basic', '').replace('_edge_cases', '').replace('_error_handling', '')
                    print(f"\nTest: {test_name}")
                    print(f"  Extracted function name: {func_name}")
                    print(f"  Function exists in source: {func_name in functions}")
                    print(f"  Would be replaced: {func_name in functions}")