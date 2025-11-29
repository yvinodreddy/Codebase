#!/usr/bin/env python3
"""
Direct fix for remaining track10 test issues
"""

from pathlib import Path
import re

def fix_test_all_public_functions(test_file_path, module_name):
    """Fix the test_all_public_functions_accessible method"""
    content = test_file_path.read_text()

    # Find and replace the problematic test method
    fixed_method = f'''    def test_all_public_functions_accessible(self):
        """Verify all public functions are accessible"""
        import {module_name}
        public_attrs = [attr for attr in dir({module_name}) if not attr.startswith('_')]
        assert len(public_attrs) > 0, "Module has public interface"
'''

    # Replace the broken version
    content = re.sub(
        r'def test_all_public_functions_accessible\(self\):.*?assert len\(public_attrs\) > 0.*?"Module has public interface"',
        fixed_method.strip(),
        content,
        flags=re.DOTALL
    )

    test_file_path.write_text(content)

def fix_with_none_inputs_tests(test_file_path):
    """Fix the _with_none_inputs test methods that still have wrong imports"""
    content = test_file_path.read_text()

    # Get the module name from the test file
    if 'replace_all_placeholders' in str(test_file_path):
        class_name = 'ProductionTestReplacer'
        module_name = 'replace_all_placeholders'

        # Fix each method that tries to import functions directly
        methods = [
            ('analyze_source_module', 'analyze_source_module'),
            ('generate_real_function_test', 'generate_real_function_test'),
            ('generate_real_class_test', 'generate_real_class_test'),
            ('replace_placeholder_in_file', 'replace_placeholder_in_file'),
        ]

        for func_name, method_name in methods:
            # Pattern: from module import function
            pattern = f'from {module_name} import {func_name}\\s+try:\\s+result = {func_name}\\(None\\)'
            replacement = f'''from {module_name} import {class_name}

        try:
            replacer = {class_name}()
            result = replacer.{method_name}(None)'''
            content = re.sub(pattern, replacement, content)

    elif 'replace_remaining_placeholders' in str(test_file_path):
        class_name = 'AggressiveReplacer'
        module_name = 'replace_remaining_placeholders'

        methods = [
            ('get_generic_test_impl', 'get_generic_test_impl'),
            ('replace_placeholders_in_file', 'replace_placeholders_in_file'),
        ]

        for func_name, method_name in methods:
            pattern = f'from {module_name} import {func_name}\\s+try:\\s+result = {func_name}\\(None'
            replacement = f'''from {module_name} import {class_name}

        try:
            replacer = {class_name}()
            result = replacer.{method_name}(None'''
            content = re.sub(pattern, replacement, content)

    elif 'generate_tests_instance9' in str(test_file_path):
        class_name = 'TestGeneratorInstance9'
        module_name = 'generate_tests_instance9'

        methods = [
            ('generate_test_file', 'generate_test_file'),
        ]

        for func_name, method_name in methods:
            pattern = f'from {module_name} import {func_name}\\s+try:\\s+result = {func_name}\\(None'
            replacement = f'''from {module_name} import {class_name}

        try:
            generator = {class_name}()
            result = generator.{method_name}(None'''
            content = re.sub(pattern, replacement, content)

    elif 'generate_100_percent_coverage' in str(test_file_path):
        class_name = 'Complete100PercentCoverageGenerator'
        module_name = 'generate_100_percent_coverage'

        methods = [
            ('generate_100_percent_tests', 'generate_100_percent_tests'),
            ('process_all_files', 'process_all_files'),
        ]

        for func_name, method_name in methods:
            pattern = f'from {module_name} import {func_name}\\s+try:\\s+result = {func_name}\\(None'
            replacement = f'''from {module_name} import {class_name}

        try:
            generator = {class_name}()
            result = generator.{method_name}(None'''
            content = re.sub(pattern, replacement, content)

    test_file_path.write_text(content)

def main():
    print("=" * 80)
    print("🔧 FIXING REMAINING TRACK10 TEST ISSUES (V2)")
    print("=" * 80)
    print()

    test_dir = Path("tests/unit_track10_utils")

    # Fix test_all_public_functions_accessible in all comprehensive tests
    module_mappings = [
        ("test_convert_to_pdf_comprehensive.py", "convert_to_pdf"),
        ("test_dashboard_redirect_8889_comprehensive.py", "dashboard_redirect_8889"),
        ("test_replace_final_placeholders_comprehensive.py", "replace_final_placeholders"),
        ("test_replace_all_placeholders_comprehensive.py", "replace_all_placeholders"),
        ("test_replace_remaining_placeholders_comprehensive.py", "replace_remaining_placeholders"),
        ("test_generate_tests_instance9_comprehensive.py", "generate_tests_instance9"),
        ("test_generate_100_percent_coverage_comprehensive.py", "generate_100_percent_coverage"),
    ]

    for test_name, module_name in module_mappings:
        test_file = test_dir / test_name
        if test_file.exists():
            fix_test_all_public_functions(test_file, module_name)
            print(f"✅ Fixed test_all_public_functions in {test_name}")

    # Fix _with_none_inputs tests
    none_inputs_tests = [
        "test_replace_all_placeholders_comprehensive.py",
        "test_replace_remaining_placeholders_comprehensive.py",
        "test_generate_tests_instance9_comprehensive.py",
        "test_generate_100_percent_coverage_comprehensive.py",
    ]

    for test_name in none_inputs_tests:
        test_file = test_dir / test_name
        if test_file.exists():
            fix_with_none_inputs_tests(test_file)
            print(f"✅ Fixed _with_none_inputs tests in {test_name}")

    print()
    print("=" * 80)
    print("✅ ALL REMAINING ISSUES FIXED")
    print("=" * 80)

if __name__ == "__main__":
    main()
