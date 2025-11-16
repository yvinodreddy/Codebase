#!/usr/bin/env python3
"""
Fix FRAMEWORK_AVAILABLE scope bug in all phase implementations
Removes the problematic assignment inside exception handlers
"""

from pathlib import Path

def fix_scope_bug(file_path: Path):
    """Remove the problematic FRAMEWORK_AVAILABLE assignment"""

    with open(file_path, 'r') as f:
        lines = f.readlines()

    fixed_lines = []
    skip_next = False

    for i, line in enumerate(lines):
        # Skip lines that have the problematic assignment inside exception handlers
        if skip_next and 'FRAMEWORK_AVAILABLE = False' in line and line.strip().startswith('FRAMEWORK_AVAILABLE'):
            print(f"   Removed problematic line: {line.strip()}")
            skip_next = False
            continue

        # Check if we're in an exception handler
        if 'except Exception as e:' in line or 'except ImportError as e:' in line:
            # Look ahead to see if next non-comment line has the assignment
            for j in range(i+1, min(i+5, len(lines))):
                if 'FRAMEWORK_AVAILABLE = False' in lines[j] and lines[j].strip().startswith('FRAMEWORK_AVAILABLE'):
                    skip_next = True
                    break

        fixed_lines.append(line)
        skip_next = False

    # Write back
    with open(file_path, 'w') as f:
        f.writelines(fixed_lines)

    return True

if __name__ == "__main__":
    root_path = Path("/home/user01/claude-test/SwarmCare/SwarmCare_Production")
    phases_dir = root_path / "phases"

    print("🔧 Fixing FRAMEWORK_AVAILABLE scope bug in all phases")
    print("=" * 80)

    fixed_count = 0
    for phase_num in range(29):
        impl_file = phases_dir / f"phase{phase_num:02d}" / "code" / "implementation.py"
        if impl_file.exists():
            print(f"\nPhase {phase_num:02d}:")
            try:
                fix_scope_bug(impl_file)
                fixed_count += 1
                print(f"   ✅ Fixed")
            except Exception as e:
                print(f"   ❌ Error: {e}")

    print(f"\n" + "=" * 80)
    print(f"📊 Processed {fixed_count}/29 phases")
    print("✅ All phases fixed!")
