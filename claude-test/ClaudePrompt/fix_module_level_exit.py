#!/usr/bin/env python3
"""Fix module-level exit() calls that break pytest"""
import re
from pathlib import Path

FILES_TO_FIX = [
    "parallel_implementation/phase2_streaming_reader.py",
    "parallel_implementation/phase3_guardrails_fixes.py",
    "parallel_implementation/phase5_websocket_enhancement.py",
    "parallel_implementation/phase6_testing.py",
]

def fix_file(filepath):
    """Wrap module-level code in if __name__ == '__main__' guard"""
    path = Path(filepath)
    if not path.exists():
        print(f"❌ {filepath} not found")
        return False

    content = path.read_text()
    lines = content.splitlines(keepends=True)

    # Find where module-level execution starts (after imports and function defs)
    # Look for the first line that's not: import, from, def, class, comment, blank
    exec_start = None
    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith('#'):
            continue
        if stripped.startswith(('import ', 'from ')):
            continue
        if stripped.startswith(('def ', 'class ')):
            continue
        if '=' in stripped and stripped.split('=')[0].strip().isupper():
            # Constant definition
            continue
        # Found first executable line
        exec_start = i
        break

    if exec_start is None:
        print(f"✅ {filepath}: No module-level execution found")
        return True

    # Wrap everything from exec_start onwards in if __name__ == '__main__'
    before = lines[:exec_start]
    after = lines[exec_start:]

    # Check if already has if __name__ guard
    content_str = ''.join(after)
    if 'if __name__' in content_str:
        print(f"✅ {filepath}: Already has __name__ guard")
        return True

    # Add the guard
    new_content = ''.join(before) + '\nif __name__ == "__main__":\n' + ''.join(f'    {line}' for line in after)

    # Fix exit(0) to be just exit() or return
    new_content = new_content.replace('    exit(0)', '    exit(0)  # OK in __main__')

    path.write_text(new_content)
    print(f"✅ {filepath}: Wrapped in __name__ guard")
    return True

def main():
    print("="*80)
    print("FIX MODULE-LEVEL exit() CALLS")
    print("="*80)
    print()

    for filepath in FILES_TO_FIX:
        fix_file(filepath)

    print()
    print("="*80)
    print("DONE")
    print("="*80)

if __name__ == "__main__":
    main()
