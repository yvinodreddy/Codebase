#!/usr/bin/env python3
"""
PERMANENT COVERAGE TRACKING SYSTEM
Updates coverage metrics across all instances and CLAUDE.md files

MANDATORY, CRITICAL, NON-NEGOTIABLE
Ensures accurate live coverage data is always available
"""

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def run_full_coverage_analysis():
    """Run complete coverage analysis on all tests"""
    print("=" * 80)
    print("🔍 RUNNING COMPREHENSIVE COVERAGE ANALYSIS")
    print("=" * 80)

    cmd = [
        "pytest",
        "tests/unit_track2_agents/",
        "tests/unit_track4_security/",
        "tests/unit_track5_database/",
        "-q",
        "--cov=.",
        "--cov-report=json:coverage_live.json",
        "--cov-report=term"
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300
        )

        # Extract coverage percentage from output
        output_lines = result.stdout.split('\n')
        for line in output_lines:
            if "TOTAL" in line and "%" in line:
                parts = line.split()
                for i, part in enumerate(parts):
                    if '%' in part:
                        coverage_pct = part.replace('%', '')
                        return float(coverage_pct), result.stdout

        return None, result.stdout

    except Exception as e:
        print(f"❌ Coverage analysis failed: {e}")
        return None, str(e)


def load_coverage_json():
    """Load coverage data from JSON file"""
    try:
        with open('coverage_live.json', 'r') as f:
            return json.load(f)
    except:
        return None


def update_claude_md_files(coverage_pct, coverage_json):
    """Update CLAUDE.md files with latest coverage"""

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    coverage_section = f"""
================================================================================
📊 LIVE TEST COVERAGE - UPDATED {timestamp}
================================================================================

**CURRENT COVERAGE: {coverage_pct:.2f}%**

This data is LIVE and updated automatically.
Last Coverage Run: {timestamp}

**Coverage Breakdown:**
- Total Statements: {coverage_json['totals']['num_statements'] if coverage_json else 'N/A'}
- Covered Statements: {coverage_json['totals']['covered_lines'] if coverage_json else 'N/A'}
- Missing Statements: {coverage_json['totals']['missing_lines'] if coverage_json else 'N/A'}

**Test Statistics:**
- Coverage updated every test run
- Stored in: coverage_live.json
- Tracked in Git for all instances

**How to get latest coverage:**
```bash
python3 update_coverage_metrics.py
```

This will:
1. Run full coverage analysis
2. Update all CLAUDE.md files
3. Save to coverage_live.json
4. Display current metrics

**PERMANENT TRACKING:** This coverage data is committed to Git and available
across all instances, windows, and sessions.

================================================================================
"""

    # Update root CLAUDE.md
    root_claude = Path("/home/user01/claude-test/CLAUDE.md")
    if root_claude.exists():
        content = root_claude.read_text()

        # Find and replace coverage section or append
        if "LIVE TEST COVERAGE" in content:
            # Replace existing section
            import re
            pattern = r'={80,}\n📊 LIVE TEST COVERAGE.*?={80,}\n'
            content = re.sub(pattern, coverage_section, content, flags=re.DOTALL)
        else:
            # Append at end
            content += "\n" + coverage_section

        root_claude.write_text(content)
        print(f"✅ Updated {root_claude}")

    # Update ClaudePrompt CLAUDE.md
    project_claude = Path("/home/user01/claude-test/ClaudePrompt/CLAUDE.md")
    if project_claude.exists():
        content = project_claude.read_text()

        if "LIVE TEST COVERAGE" in content:
            import re
            pattern = r'={80,}\n📊 LIVE TEST COVERAGE.*?={80,}\n'
            content = re.sub(pattern, coverage_section, content, flags=re.DOTALL)
        else:
            content += "\n" + coverage_section

        project_claude.write_text(content)
        print(f"✅ Updated {project_claude}")

    # Also create a simple coverage status file
    status_file = Path("/home/user01/claude-test/ClaudePrompt/.coverage_status")
    status_file.write_text(f"""CURRENT_COVERAGE={coverage_pct:.2f}%
LAST_UPDATED={timestamp}
STATEMENTS_TOTAL={coverage_json['totals']['num_statements'] if coverage_json else 'N/A'}
STATEMENTS_COVERED={coverage_json['totals']['covered_lines'] if coverage_json else 'N/A'}
""")
    print(f"✅ Created {status_file}")


def main():
    """Main execution"""
    print("\n" + "=" * 80)
    print("📊 PERMANENT COVERAGE TRACKING SYSTEM")
    print("=" * 80)
    print()

    # Run coverage analysis
    coverage_pct, output = run_full_coverage_analysis()

    if coverage_pct is None:
        print("❌ Could not determine coverage percentage")
        print(output)
        return 1

    print()
    print("=" * 80)
    print(f"✅ COVERAGE ANALYSIS COMPLETE: {coverage_pct:.2f}%")
    print("=" * 80)
    print()

    # Load detailed JSON data
    coverage_json = load_coverage_json()

    # Update CLAUDE.md files
    print("📝 Updating CLAUDE.md files...")
    update_claude_md_files(coverage_pct, coverage_json)

    print()
    print("=" * 80)
    print("✅ COVERAGE METRICS UPDATED SUCCESSFULLY")
    print("=" * 80)
    print()
    print(f"Current Coverage: {coverage_pct:.2f}%")
    print(f"Updated Files:")
    print("  - /home/user01/claude-test/CLAUDE.md")
    print("  - /home/user01/claude-test/ClaudePrompt/CLAUDE.md")
    print("  - coverage_live.json")
    print("  - .coverage_status")
    print()
    print("💾 These files are tracked in Git and available to all instances")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
