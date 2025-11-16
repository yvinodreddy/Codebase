#!/usr/bin/env python3
"""
Fix FRAMEWORK_AVAILABLE scope bug in all phase implementations
"""

import re
from pathlib import Path

def fix_framework_available_bug(file_path: Path):
    """Fix the FRAMEWORK_AVAILABLE scoping issue"""

    with open(file_path, 'r') as f:
        content = f.read()

    # Check if file has the bug (assignment to FRAMEWORK_AVAILABLE without global)
    if 'FRAMEWORK_AVAILABLE = False' in content and 'global FRAMEWORK_AVAILABLE' not in content:
        # Find the __init__ method and add global declaration
        pattern = r'(    def __init__\(self\):)'
        replacement = r'\1\n        global FRAMEWORK_AVAILABLE'

        content_fixed = re.sub(pattern, replacement, content)

        # Also fix any other methods that might reference it
        pattern2 = r'(    def \w+\(self[^)]*\):)(\n\s+"""[^"]*""")?\n(\s+logger\.)'
        def add_global(match):
            method_def = match.group(1)
            docstring = match.group(2) or ''
            next_line = match.group(3)

            # Check if the method uses FRAMEWORK_AVAILABLE
            method_start = match.end()
            method_content = content_fixed[method_start:method_start + 500]

            if 'FRAMEWORK_AVAILABLE' in method_content:
                return f'{method_def}{docstring}\n        global FRAMEWORK_AVAILABLE\n        {next_line}'
            else:
                return match.group(0)

        # Apply fix
        with open(file_path, 'w') as f:
            f.write(content_fixed)

        return True
    return False

if __name__ == "__main__":
    root_path = Path("/home/user01/claude-test/SwarmCare/SwarmCare_Production")
    phases_dir = root_path / "phases"

    fixed_count = 0
    for phase_num in range(29):
        impl_file = phases_dir / f"phase{phase_num:02d}" / "code" / "implementation.py"
        if impl_file.exists():
            if fix_framework_available_bug(impl_file):
                print(f"✅ Fixed phase {phase_num:02d}")
                fixed_count += 1

    print(f"\n📊 Fixed {fixed_count} phases")
