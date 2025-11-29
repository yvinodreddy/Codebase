#!/usr/bin/env python3
"""
Generate targeted tests for uncovered lines in Track 5 files.
Analyzes coverage reports and creates tests that target specific uncovered lines.
"""

import subprocess
import json
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple


# Track 5 file mappings
TRACK5_FILES = {
    "find_untested_files.py": ("find_untested_files", "tests/unit_track5_database/test_find_untested_files_real.py"),
    "setup_database.py": ("setup_database", "tests/unit_track5_database/test_setup_database_real.py"),
    "analyze_modules_structure.py": ("analyze_modules_structure", "tests/unit_track5_database/test_analyze_modules_structure_real.py"),
    "database/token_manager.py": ("database.token_manager", "tests/unit_track5_database/test_token_manager_real.py"),
    "database/multi_project_manager.py": ("database.multi_project_manager", "tests/unit_track5_database/test_multi_project_manager_real.py"),
    "database/sqlite_context_loader.py": ("database.sqlite_context_loader", "tests/unit_track5_database/test_sqlite_context_loader_real.py"),
    "analyze_codebase.py": ("analyze_codebase", "tests/unit_track5_database/test_analyze_codebase_real.py"),
    "database/db_cli.py": ("database.db_cli", "tests/unit_track5_database/test_db_cli_real.py"),
    "find_broken_tests.py": ("find_broken_tests", "tests/unit_track5_database/test_find_broken_tests_real.py"),
    "database/auto_context_integration.py": ("database.auto_context_integration", "tests/unit_track5_database/test_auto_context_integration_real.py"),
    "database/async_context_loader.py": ("database.async_context_loader", "tests/unit_track5_database/test_async_context_loader_real.py"),
    "database/init_database.py": ("database.init_database", "tests/unit_track5_database/test_init_database_real.py"),
    "database/context_retriever.py": ("database.context_retriever", "tests/unit_track5_database/test_context_retriever_real.py"),
    "realtime_db_updates.py": ("realtime_db_updates", "tests/unit_track5_database/test_realtime_db_updates_real.py"),
}


def get_coverage_for_file(source_file: str, test_file: str) -> Tuple[float, List[int]]:
    """Run pytest with coverage for a specific file and return coverage % and missing lines."""
    try:
        result = subprocess.run(
            ["pytest", test_file, f"--cov={source_file}", "--cov-report=term-missing", "-q"],
            capture_output=True,
            text=True,
            timeout=60
        )
        output = result.stdout + result.stderr

        # Parse coverage percentage and missing lines
        coverage_match = re.search(rf"{re.escape(source_file)}\s+\d+\s+\d+\s+(\d+)%", output)
        missing_match = re.search(rf"{re.escape(source_file)}.*?(\d+(?:-\d+)?(?:,\s*\d+(?:-\d+)?)*)\s*$", output, re.MULTILINE)

        coverage_pct = float(coverage_match.group(1)) if coverage_match else 0.0

        missing_lines = []
        if missing_match:
            missing_str = missing_match.group(1)
            for part in missing_str.split(','):
                part = part.strip()
                if '-' in part:
                    start, end = map(int, part.split('-'))
                    missing_lines.extend(range(start, end + 1))
                elif part.isdigit():
                    missing_lines.append(int(part))

        return coverage_pct, missing_lines

    except Exception as e:
        print(f"Error getting coverage for {source_file}: {e}")
        return 0.0, []


def analyze_uncovered_lines(source_file: Path, missing_lines: List[int]) -> Dict[str, any]:
    """Analyze the source file to understand what the uncovered lines are."""
    try:
        with open(source_file, 'r') as f:
            lines = f.readlines()

        uncovered_info = {
            'function_defs': [],
            'class_defs': [],
            'conditionals': [],
            'error_handling': [],
            'main_blocks': [],
            'other': []
        }

        for line_num in missing_lines:
            if line_num <= len(lines):
                line = lines[line_num - 1].strip()

                if line.startswith('def '):
                    uncovered_info['function_defs'].append((line_num, line))
                elif line.startswith('class '):
                    uncovered_info['class_defs'].append((line_num, line))
                elif 'if ' in line or 'elif ' in line or 'else:' in line:
                    uncovered_info['conditionals'].append((line_num, line))
                elif 'except' in line or 'try:' in line or 'raise ' in line:
                    uncovered_info['error_handling'].append((line_num, line))
                elif '__name__' in line and '__main__' in line:
                    uncovered_info['main_blocks'].append((line_num, line))
                else:
                    uncovered_info['other'].append((line_num, line))

        return uncovered_info

    except Exception as e:
        print(f"Error analyzing {source_file}: {e}")
        return {}


def generate_tests_for_gaps(source_file: str, module_path: str, uncovered_info: Dict) -> List[str]:
    """Generate test code targeting uncovered lines."""
    tests = []

    # Generate tests for uncovered conditionals
    if uncovered_info.get('conditionals'):
        test = f'''
def test_conditional_branches_{len(tests)}():
    """Test conditional branches that were previously uncovered"""
    from {module_path.replace('/', '.')} import *

    # TODO: Add tests for lines: {[line for line, _ in uncovered_info['conditionals']]}
    # These are conditional branches (if/elif/else) that need coverage
    try:
        # Call functions with different parameters to hit different branches
        pass
    except:
        pass  # May need specific setup
'''
        tests.append(test)

    # Generate tests for uncovered error handling
    if uncovered_info.get('error_handling'):
        test = f'''
def test_error_handling_{len(tests)}():
    """Test error handling paths that were previously uncovered"""
    from {module_path.replace('/', '.')} import *

    # TODO: Add tests for lines: {[line for line, _ in uncovered_info['error_handling']]}
    # These are try/except/raise statements that need coverage
    try:
        # Trigger error conditions to test exception handling
        pass
    except:
        pass  # May need specific error scenarios
'''
        tests.append(test)

    # Generate tests for uncovered functions
    if uncovered_info.get('function_defs'):
        for line_num, line in uncovered_info['function_defs']:
            func_name_match = re.search(r'def\s+(\w+)', line)
            if func_name_match:
                func_name = func_name_match.group(1)
                test = f'''
def test_{func_name}_uncovered():
    """Test {func_name} function (line {line_num}) that was previously uncovered"""
    from {module_path.replace('/', '.')} import {func_name}

    # TODO: Add comprehensive test for {func_name}
    try:
        # Call with various parameters
        result = {func_name}()  # Adjust parameters as needed
        assert True  # Verify behavior
    except TypeError:
        # May need specific parameters
        pass
'''
                tests.append(test)

    return tests


def main():
    """Main execution - analyze all Track 5 files and generate targeted tests."""
    print("\n" + "=" * 80)
    print("TRACK 5 - TARGETED TEST GENERATION FOR 100% COVERAGE")
    print("=" * 80 + "\n")

    results = {}

    for source_file, (module_path, test_file) in TRACK5_FILES.items():
        print(f"\nAnalyzing: {source_file}")
        print(f"  Module: {module_path}")
        print(f"  Test file: {test_file}")

        # Get current coverage
        coverage_pct, missing_lines = get_coverage_for_file(source_file, test_file)
        print(f"  Current coverage: {coverage_pct}%")
        print(f"  Missing lines: {len(missing_lines)} lines")

        if coverage_pct >= 100.0:
            print(f"  ✅ Already at 100% coverage - SKIP")
            continue

        # Analyze uncovered lines
        source_path = Path(source_file)
        if source_path.exists():
            uncovered_info = analyze_uncovered_lines(source_path, missing_lines)

            print(f"  Uncovered breakdown:")
            print(f"    - Functions: {len(uncovered_info.get('function_defs', []))}")
            print(f"    - Conditionals: {len(uncovered_info.get('conditionals', []))}")
            print(f"    - Error handling: {len(uncovered_info.get('error_handling', []))}")
            print(f"    - __main__ blocks: {len(uncovered_info.get('main_blocks', []))}")
            print(f"    - Other: {len(uncovered_info.get('other', []))}")

            # Generate targeted tests
            new_tests = generate_tests_for_gaps(source_file, module_path, uncovered_info)

            results[source_file] = {
                'coverage': coverage_pct,
                'missing_lines': missing_lines,
                'uncovered_info': uncovered_info,
                'generated_tests': new_tests
            }

            print(f"  Generated {len(new_tests)} targeted test templates")
        else:
            print(f"  ⚠️  Source file not found: {source_path}")

    # Print summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)

    for source_file, data in results.items():
        print(f"\n{source_file}:")
        print(f"  Coverage: {data['coverage']}%")
        print(f"  Gap to 100%: {100 - data['coverage']:.1f}%")
        print(f"  Generated tests: {len(data['generated_tests'])}")

    # Save results
    output_file = "track5_coverage_analysis.json"
    with open(output_file, 'w') as f:
        # Convert to JSON-serializable format
        json_results = {
            source: {
                'coverage': data['coverage'],
                'missing_line_count': len(data['missing_lines']),
                'test_count': len(data['generated_tests'])
            }
            for source, data in results.items()
        }
        json.dump(json_results, f, indent=2)

    print(f"\n✅ Analysis complete - results saved to {output_file}")
    print(f"\nNext steps:")
    print(f"  1. Review generated test templates")
    print(f"  2. Fill in specific test logic for each uncovered line")
    print(f"  3. Run tests to verify 100% coverage achieved")

    return 0


if __name__ == "__main__":
    exit(main())
