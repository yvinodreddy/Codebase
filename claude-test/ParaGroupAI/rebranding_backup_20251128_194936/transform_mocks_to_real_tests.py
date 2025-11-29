#!/usr/bin/env python3
"""
Transform Mock-Based Tests to Real Code Tests
==============================================

Converts tests that mock the function under test into tests that actually
execute real code with only dependencies mocked.

**Target:** Fix 9.83% → 90%+ coverage by making tests execute real code.

**Transformation:**
BEFORE (Mock-based - doesn't test real code):
    def test_configure_cors():
        with patch('module.func') as mock:
            mock.return_value = "result"
            assert mock() == "result"  # Tests mock, not real code!

AFTER (Real code test):
    def test_configure_cors():
        from module import func
        # Mock only dependencies
        with patch('module.external_api') as mock_api:
            result = func(real_args)  # Tests REAL function!
            assert result == expected
"""

import re
import ast
from pathlib import Path
from typing import List, Tuple, Dict
import sys

class MockToRealTransformer:
    """Transforms mock-based tests to real code tests"""

    def __init__(self):
        self.tests_dir = Path(__file__).parent / "tests" / "unit_generated"
        self.transformations_made = 0
        self.files_processed = 0

    def identify_mocked_function(self, test_content: str) -> List[Tuple[str, str]]:
        """
        Identify functions that are being mocked when they should be tested.

        Returns: List of (module_path, function_name) tuples
        """
        # Pattern: with patch('module.path.function_name') as mock_func:
        pattern = r"with patch\(['\"]([^'\"]+)\['\"]\) as (\w+):"
        matches = re.findall(pattern, test_content)

        mocked_functions = []
        for full_path, mock_var in matches:
            # Split module.function_name
            parts = full_path.rsplit('.', 1)
            if len(parts) == 2:
                module_path, func_name = parts
                mocked_functions.append((module_path, func_name, mock_var))

        return mocked_functions

    def analyze_test_file(self, test_file: Path) -> Dict:
        """
        Analyze a test file to understand what needs transformation.

        Returns dict with transformation recommendations.
        """
        with open(test_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Identify what module is being tested
        # From: tests/unit_generated/test_module_comprehensive.py
        # Extract: module name
        test_filename = test_file.stem  # e.g., test_security_headers_comprehensive
        module_name = test_filename.replace('test_', '').replace('_comprehensive', '')

        # Find all mocked functions
        mocked_functions = self.identify_mocked_function(content)

        # Check if module functions are being mocked (BAD)
        module_funcs_mocked = [
            (mod, func, var) for mod, func, var in mocked_functions
            if module_name in mod.replace('/', '.').replace('_', '')
        ]

        return {
            'file': test_file,
            'module_name': module_name,
            'total_mocks': len(mocked_functions),
            'module_funcs_mocked': module_funcs_mocked,
            'needs_transformation': len(module_funcs_mocked) > 0
        }

    def transform_test_function(self, test_func_code: str, module_path: str,
                                func_name: str) -> str:
        """
        Transform a single test function from mock-based to real code test.

        Args:
            test_func_code: The full test function code
            module_path: e.g., 'security.security_headers'
            func_name: e.g., 'configure_cors'

        Returns:
            Transformed test function code
        """
        lines = test_func_code.split('\n')
        transformed_lines = []

        in_mock_context = False
        indent = ""

        for line in lines:
            # Detect: with patch('module.func') as mock_func:
            if f"with patch('{module_path}.{func_name}')" in line:
                # Replace with real import
                indent = line[:len(line) - len(line.lstrip())]
                transformed_lines.append(f"{indent}# TRANSFORMED: Using real code instead of mock")
                transformed_lines.append(f"{indent}from {module_path} import {func_name}")
                transformed_lines.append(f"{indent}")
                in_mock_context = True
                continue

            # Skip mock setup lines (mock.return_value = ...)
            if in_mock_context and 'return_value' in line and '=' in line:
                continue

            # Transform mock_func() calls to real function calls
            if in_mock_context and f"mock_func(" in line:
                # Extract arguments
                match = re.search(r'mock_func\((.*?)\)', line)
                if match:
                    args = match.group(1)
                    line = line.replace(f"mock_func({args})", f"{func_name}({args})")

            transformed_lines.append(line)

        return '\n'.join(transformed_lines)

    def transform_file(self, test_file: Path) -> Tuple[bool, int]:
        """
        Transform an entire test file.

        Returns: (success, num_transformations)
        """
        analysis = self.analyze_test_file(test_file)

        if not analysis['needs_transformation']:
            return (True, 0)

        with open(test_file, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content
        transformations = 0

        for module_path, func_name, mock_var in analysis['module_funcs_mocked']:
            # Find and transform each test function that mocks this function
            # Pattern: def test_xxx(...): followed by patch block
            pattern = rf"(def test_\w+\([^)]*\):.*?)(with patch\(['\"]{ module_path}.{func_name}['\"].*?assert.*?)(?=\n\n|\ndef test|\nclass |$)"

            def replace_func(match):
                nonlocal transformations
                test_signature = match.group(1)
                test_body = match.group(2)

                # Transform the test body
                transformed_body = self.transform_test_function(
                    test_signature + test_body,
                    module_path,
                    func_name
                )

                transformations += 1
                return transformed_body

            content = re.sub(pattern, replace_func, content, flags=re.DOTALL)

        # Write back if changed
        if content != original_content:
            with open(test_file, 'w', encoding='utf-8') as f:
                f.write(content)
            return (True, transformations)
        else:
            return (True, 0)

    def transform_all(self) -> Dict:
        """
        Transform all test files from mock-based to real code tests.

        Returns: Summary statistics
        """
        test_files = sorted(self.tests_dir.glob("test_*_comprehensive.py"))

        print("="*80)
        print("🔄 TRANSFORMING MOCK-BASED TESTS TO REAL CODE TESTS")
        print("="*80)
        print()
        print(f"Found {len(test_files)} test files to analyze")
        print()

        results = []
        total_transformations = 0

        for i, test_file in enumerate(test_files, 1):
            print(f"[{i}/{len(test_files)}] Processing {test_file.name}...", end=" ")

            analysis = self.analyze_test_file(test_file)

            if not analysis['needs_transformation']:
                print("✓ Already using real code")
                results.append({'file': test_file.name, 'status': 'ok', 'transformations': 0})
                continue

            success, num_transforms = self.transform_file(test_file)

            if success:
                print(f"✓ Transformed {num_transforms} tests")
                total_transformations += num_transforms
                results.append({
                    'file': test_file.name,
                    'status': 'transformed',
                    'transformations': num_transforms
                })
            else:
                print("✗ Failed")
                results.append({'file': test_file.name, 'status': 'failed', 'transformations': 0})

        print()
        print("="*80)
        print("✅ TRANSFORMATION COMPLETE")
        print("="*80)
        print(f"Total transformations: {total_transformations}")
        print(f"Files processed: {len(test_files)}")
        print()

        return {
            'total_transformations': total_transformations,
            'files_processed': len(test_files),
            'results': results
        }


def main():
    """Main execution function"""

    print(__doc__)

    transformer = MockToRealTransformer()
    summary = transformer.transform_all()

    print("\n📊 SUMMARY:")
    print(f"   Transformations made: {summary['total_transformations']}")
    print(f"   Files processed: {summary['files_processed']}")
    print()
    print("Next steps:")
    print("   1. Run pytest to verify tests still pass")
    print("   2. Run coverage to check improvement")
    print("   3. Review transformed tests manually")
    print()

    return 0 if summary['total_transformations'] >= 0 else 1


if __name__ == "__main__":
    sys.exit(main())
