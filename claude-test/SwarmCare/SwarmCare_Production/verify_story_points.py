#!/usr/bin/env python3
"""
Verify actual story points for all 29 phases
Find discrepancy between expected (1362) and calculated (1139)
"""

from pathlib import Path
import re

def extract_story_points(file_path: Path):
    """Extract story points from implementation file"""
    try:
        with open(file_path, 'r') as f:
            content = f.read()

        # Look for story_points assignment
        patterns = [
            r'self\.story_points\s*=\s*(\d+)',
            r'Story Points:\s*(\d+)',
            r'story_points\s*=\s*(\d+)'
        ]

        for pattern in patterns:
            match = re.search(pattern, content)
            if match:
                return int(match.group(1))

        return None
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

if __name__ == "__main__":
    root_path = Path("/home/user01/claude-test/SwarmCare/SwarmCare_Production")
    phases_dir = root_path / "phases"

    print("📊 VERIFYING STORY POINTS FOR ALL 29 PHASES")
    print("=" * 80)

    total_points = 0
    phase_data = []

    for phase_num in range(29):
        phase_dir = phases_dir / f"phase{phase_num:02d}"
        impl_file = phase_dir / "code" / "implementation.py"

        if impl_file.exists():
            points = extract_story_points(impl_file)
            if points:
                phase_data.append((phase_num, points))
                total_points += points
                print(f"Phase {phase_num:02d}: {points:3d} points")
            else:
                print(f"Phase {phase_num:02d}: ⚠️  Could not extract story points")
        else:
            print(f"Phase {phase_num:02d}: ❌ implementation.py not found")

    print("=" * 80)
    print(f"Total Story Points: {total_points}")
    print(f"Expected: 1362")
    print(f"Discrepancy: {1362 - total_points}")

    if total_points != 1362:
        print(f"\n❌ DISCREPANCY FOUND: {abs(1362 - total_points)} points difference!")
        print("\nPhases that may have incorrect story points:")

        # Known correct values (need to verify these)
        expected_points = {
            0: 37, 1: 60, 2: 48, 3: 35, 4: 30, 5: 47, 6: 25, 7: 12,
            8: 40, 9: 53, 10: 42, 11: 37, 12: 45, 13: 30, 14: 28,
            15: 50, 16: 55, 17: 48, 18: 60, 19: 22, 20: 35, 21: 28,
            22: 33, 23: 25, 24: 40, 25: 38, 26: 45, 27: 42, 28: 50
        }

        expected_total = sum(expected_points.values())
        print(f"\nSum of expected values: {expected_total}")

        if expected_total != 1362:
            print("\n⚠️  Expected values in code don't sum to 1362!")
            print("Need to find the actual correct values...")
    else:
        print("\n✅ Story points verified correctly!")
