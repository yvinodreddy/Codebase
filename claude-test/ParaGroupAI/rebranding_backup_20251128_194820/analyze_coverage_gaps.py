#!/usr/bin/env python3
"""
analyze_coverage_gaps.py - Identify modules needing tests
Parses coverage.json to find files with <70% coverage
"""
import json
from pathlib import Path
from typing import List, Dict, Tuple

def analyze_coverage() -> Tuple[List[Dict], List[Dict], Dict]:
    """
    Analyze coverage.json and categorize files by coverage level

    Returns:
        (phase1_targets, phase2_targets, stats)
        - phase1_targets: Files with 0-50% coverage (highest priority)
        - phase2_targets: Files with 50-70% coverage (secondary priority)
        - stats: Overall statistics
    """
    try:
        with open('coverage.json', 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("❌ coverage.json not found")
        return [], [], {}

    files = data.get('files', {})

    phase1_targets = []  # 0-50% coverage
    phase2_targets = []  # 50-70% coverage
    phase3_targets = []  # 70-90% coverage
    good_coverage = []   # 90%+ coverage

    for file_path, file_data in files.items():
        # Skip test files, __init__.py, and non-Python files
        if 'test' in file_path.lower() or '__init__' in file_path:
            continue
        if not file_path.endswith('.py'):
            continue

        summary = file_data.get('summary', {})
        covered = summary.get('covered_lines', 0)
        total = summary.get('num_statements', 0)

        if total == 0:
            continue  # Skip files with no statements

        coverage_pct = (covered / total) * 100
        missing = summary.get('missing_lines', 0)

        file_info = {
            'path': file_path,
            'coverage': coverage_pct,
            'covered': covered,
            'total': total,
            'missing': missing,
            'gap': 100 - coverage_pct
        }

        if coverage_pct < 50:
            phase1_targets.append(file_info)
        elif coverage_pct < 70:
            phase2_targets.append(file_info)
        elif coverage_pct < 90:
            phase3_targets.append(file_info)
        else:
            good_coverage.append(file_info)

    # Sort by coverage (lowest first)
    phase1_targets.sort(key=lambda x: x['coverage'])
    phase2_targets.sort(key=lambda x: x['coverage'])
    phase3_targets.sort(key=lambda x: x['coverage'])

    stats = {
        'total_coverage': data['totals']['percent_covered'],
        'total_files': len(files),
        'phase1_count': len(phase1_targets),
        'phase2_count': len(phase2_targets),
        'phase3_count': len(phase3_targets),
        'good_count': len(good_coverage)
    }

    return phase1_targets, phase2_targets, phase3_targets, good_coverage, stats

def main():
    print("🔍 ANALYZING COVERAGE GAPS")
    print("=" * 80)
    print()

    phase1, phase2, phase3, good, stats = analyze_coverage()

    print(f"📊 OVERALL STATISTICS")
    print(f"   Current coverage: {stats['total_coverage']:.2f}%")
    print(f"   Target: 99%")
    print(f"   Gap: {99 - stats['total_coverage']:.2f}%")
    print()

    print(f"📁 FILE BREAKDOWN")
    print(f"   Total files analyzed: {stats['total_files']}")
    print(f"   Phase 1 (0-50%):   {stats['phase1_count']} files")
    print(f"   Phase 2 (50-70%):  {stats['phase2_count']} files")
    print(f"   Phase 3 (70-90%):  {stats['phase3_count']} files")
    print(f"   Good (90%+):       {stats['good_count']} files")
    print()

    print("=" * 80)
    print("🎯 PHASE 1 TARGETS: Files with 0-50% coverage")
    print("=" * 80)

    if not phase1:
        print("   ✅ No files with <50% coverage!")
    else:
        for i, file_info in enumerate(phase1[:20], 1):  # Show top 20
            print(f"{i:2}. {file_info['path']}")
            print(f"    Coverage: {file_info['coverage']:5.1f}% | "
                  f"Covered: {file_info['covered']:4}/{file_info['total']:4} lines | "
                  f"Missing: {file_info['missing']:4} lines")

        if len(phase1) > 20:
            print(f"\n    ... and {len(phase1) - 20} more files")

    print()
    print("=" * 80)
    print("🎯 PHASE 2 TARGETS: Files with 50-70% coverage")
    print("=" * 80)

    if not phase2:
        print("   ✅ No files with 50-70% coverage!")
    else:
        for i, file_info in enumerate(phase2[:15], 1):  # Show top 15
            print(f"{i:2}. {file_info['path']}")
            print(f"    Coverage: {file_info['coverage']:5.1f}% | "
                  f"Covered: {file_info['covered']:4}/{file_info['total']:4} lines | "
                  f"Missing: {file_info['missing']:4} lines")

        if len(phase2) > 15:
            print(f"\n    ... and {len(phase2) - 15} more files")

    print()
    print("=" * 80)
    print("📈 NEXT STEPS")
    print("=" * 80)
    print()
    print(f"1. Generate tests for Phase 1 files (targeting 60-70% coverage)")
    print(f"   Expected impact: +{sum(f['gap'] * f['total'] for f in phase1) / sum(stats['total_files'] for _ in [0]) if phase1 else 0:.1f}% overall coverage")
    print()
    print(f"2. Generate tests for Phase 2 files (targeting 80-90% coverage)")
    print(f"   Expected impact: Additional coverage improvement")
    print()
    print(f"3. Polish Phase 3 files to reach 99% overall")
    print()

    # Save detailed results to JSON for programmatic access
    results = {
        'stats': stats,
        'phase1': phase1,
        'phase2': phase2,
        'phase3': phase3,
        'good': good
    }

    with open('coverage_analysis.json', 'w') as f:
        json.dump(results, f, indent=2)

    print("💾 Detailed analysis saved to: coverage_analysis.json")
    print()

    return 0

if __name__ == "__main__":
    exit(main())
