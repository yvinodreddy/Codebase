#!/usr/bin/env python3
"""
find_untested_files.py - Find source files that don't have corresponding tests
Simple file-based approach to identify gaps
"""
from pathlib import Path

def find_untested_files():
    """Find Python files that don't have tests"""

    # Get all Python source files (exclude tests, __init__, and certain directories)
    source_files = []
    exclude_dirs = {'tests', '__pycache__', '.git', 'htmlcov', 'venv', 'web-ui-implementation', 'parallel_tasks', 'parallel_iteration2', 'parallel_99_logs'}
    exclude_files = {'__init__.py', 'setup.py'}

    for py_file in Path('.').rglob('*.py'):
        # Skip if in excluded directory
        if any(excl in py_file.parts for excl in exclude_dirs):
            continue

        # Skip if excluded file
        if py_file.name in exclude_files:
            continue

        # Skip if it's a test file itself
        if 'test_' in py_file.name:
            continue

        source_files.append(py_file)

    # Get all existing test files
    test_dir = Path('tests/unit_real_coverage')
    existing_tests = set()

    if test_dir.exists():
        for test_file in test_dir.glob('test_*_real.py'):
            # Extract module name from test file
            # test_module_name_real.py -> module_name
            test_name = test_file.stem  # Remove .py
            test_name = test_name.replace('test_', '').replace('_real', '')
            existing_tests.add(test_name)

    # Find files without tests
    untested = []
    for source_file in source_files:
        module_name = source_file.stem

        if module_name not in existing_tests:
            untested.append(source_file)

    return sorted(untested), sorted(source_files), existing_tests

def main():
    print("🔍 FINDING UNTESTED FILES")
    print("=" * 80)
    print()

    untested, all_sources, existing_tests = find_untested_files()

    print(f"📊 STATISTICS")
    print(f"   Total source files: {len(all_sources)}")
    print(f"   Existing test modules: {len(existing_tests)}")
    print(f"   Untested files: {len(untested)}")
    print(f"   Coverage by count: {((len(all_sources) - len(untested)) / len(all_sources) * 100):.1f}%")
    print()

    print("=" * 80)
    print("📁 UNTESTED FILES (Priority targets for test generation)")
    print("=" * 80)
    print()

    if not untested:
        print("   ✅ All files have tests!")
    else:
        for i, file_path in enumerate(untested[:30], 1):  # Show top 30
            print(f"{i:2}. {file_path}")

        if len(untested) > 30:
            print(f"\n    ... and {len(untested) - 30} more files")

    print()
    print("=" * 80)
    print("💾 Saving untested files list to untested_files.txt")
    print("=" * 80)

    with open('untested_files.txt', 'w') as f:
        for file_path in untested:
            f.write(f"{file_path}\n")

    print(f"✅ Saved {len(untested)} untested file paths")
    print()

    return 0

if __name__ == "__main__":
    exit(main())
