#!/usr/bin/env python3
"""
Complete fix for all test file IndentationErrors.
Removes incomplete 'with' statement lines entirely.
"""

from pathlib import Path

# Files and their problematic line ranges to remove
# Each entry: (file, start_line, end_line) - will remove lines between these (inclusive)
FILES_TO_FIX = [
    ("tests/unit_generated/test_medical_guardrails_comprehensive.py", 46, 47),
    ("tests/unit_generated/test_feedback_loop_comprehensive.py", 46, 47),
    ("tests/unit_generated/test_circuit_breaker_comprehensive.py", 46, 47),
    ("tests/unit_generated/test_master_orchestrator_comprehensive.py", 46, 47),
    ("tests/unit_generated/test_ultrathink_comprehensive.py", 287, 288),
    ("tests/unit_generated/test_verification_system_comprehensive.py", 46, 47),
    ("tests/unit_generated/test_agentic_search_comprehensive.py", 46, 47),
    ("tests/unit_generated/test_claude_integration_comprehensive.py", 81, 82),
    ("tests/unit_generated/test_multi_layer_system_comprehensive.py", 46, 47),
    ("tests/unit_generated/test_rate_limiter_comprehensive.py", 80, 81),
]

def fix_file(filepath: str, start_line: int, end_line: int) -> bool:
    """Remove problematic lines from file"""
    try:
        path = Path(filepath)
        if not path.exists():
            print(f"❌ File not found: {filepath}")
            return False

        # Read file
        lines = path.read_text().splitlines(keepends=True)

        # Convert to 0-indexed
        start_idx = start_line - 1
        end_idx = end_line - 1

        if start_idx >= len(lines) or end_idx >= len(lines):
            print(f"❌ Line range out of bounds in {filepath}")
            return False

        # Show what we're removing
        print(f"Fixing {filepath}:")
        for i in range(start_idx, end_idx + 1):
            print(f"  Removing line {i+1}: {lines[i].rstrip()}")

        # Remove the problematic lines
        del lines[start_idx:end_idx + 1]

        # Write back
        path.write_text(''.join(lines))

        print(f"✅ Fixed: {filepath} (removed lines {start_line}-{end_line})")
        return True

    except Exception as e:
        print(f"❌ Error fixing {filepath}: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("="*80)
    print("COMPLETE TEST FILE SYNTAX FIX (Remove Incomplete With Statements)")
    print("="*80)
    print()

    fixed = 0
    failed = 0

    for filepath, start_line, end_line in FILES_TO_FIX:
        if fix_file(filepath, start_line, end_line):
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
