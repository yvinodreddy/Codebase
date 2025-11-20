#!/usr/bin/env python3
"""
Autonomous fix for all test file IndentationErrors.
Fixes incomplete 'with' statements by adding pass statements.
"""

import re
from pathlib import Path

# List of files and their error lines
FILES_TO_FIX = [
    ("tests/unit_generated/test_medical_guardrails_comprehensive.py", 46),
    ("tests/unit_generated/test_feedback_loop_comprehensive.py", 46),
    ("tests/unit_generated/test_circuit_breaker_comprehensive.py", 46),
    ("tests/unit_generated/test_master_orchestrator_comprehensive.py", 46),
    ("tests/unit_generated/test_ultrathink_comprehensive.py", 287),
    ("tests/unit_generated/test_verification_system_comprehensive.py", 46),
    ("tests/unit_generated/test_agentic_search_comprehensive.py", 46),
    ("tests/unit_generated/test_claude_integration_comprehensive.py", 81),
    ("tests/unit_generated/test_multi_layer_system_comprehensive.py", 46),
    ("tests/unit_generated/test_rate_limiter_comprehensive.py", 80),
]

def fix_file(filepath: str, error_line: int) -> bool:
    """Fix IndentationError in a test file"""
    try:
        path = Path(filepath)
        if not path.exists():
            print(f"❌ File not found: {filepath}")
            return False

        # Read file
        lines = path.read_text().splitlines(keepends=True)

        # Check if the error line has a 'with' statement
        if error_line - 1 >= len(lines):
            print(f"❌ Line {error_line} out of range in {filepath}")
            return False

        with_line_idx = error_line - 2  # -1 for 0-index, -1 for "line before error"
        with_line = lines[with_line_idx]

        if 'with ' not in with_line and 'with(' not in with_line:
            print(f"⚠️  Line {error_line - 1} doesn't contain 'with': {with_line.strip()}")
            # Still try to add pass

        # Get indentation of the with statement
        indent_match = re.match(r'(\s*)', with_line)
        indent = indent_match.group(1) if indent_match else ''

        # Add a pass statement with proper indentation
        # The pass should be more indented than the with statement
        pass_indent = indent + '    '
        pass_line = f'{pass_indent}pass  # Auto-fixed: incomplete with statement\n'

        # Insert the pass statement after the with statement
        lines.insert(with_line_idx + 1, pass_line)

        # Write back
        path.write_text(''.join(lines))

        print(f"✅ Fixed: {filepath} (added pass at line {error_line})")
        return True

    except Exception as e:
        print(f"❌ Error fixing {filepath}: {e}")
        return False

def main():
    print("="*80)
    print("AUTONOMOUS TEST FILE SYNTAX FIX")
    print("="*80)
    print()

    fixed = 0
    failed = 0

    for filepath, error_line in FILES_TO_FIX:
        if fix_file(filepath, error_line):
            fixed += 1
        else:
            failed += 1

    print()
    print("="*80)
    print(f"RESULTS: {fixed} fixed, {failed} failed")
    print("="*80)

    return 0 if failed == 0 else 1

if __name__ == "__main__":
    exit(main())
