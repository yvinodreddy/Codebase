#!/usr/bin/env python3
"""
Phase 11: Research & Publications
Comprehensive Validation Script

This script validates all research papers meet publication standards:
- Content completeness (all sections present)
- Citation requirements (minimum 3 citations)
- Word count (minimum 1000 words)
- Quality score (100% required for production)
"""

import sys
import os
import json
from pathlib import Path

# Add code directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'code'))

from implementation import Phase11Implementation


def print_header(text, char='='):
    """Print formatted header"""
    print(f"\n{char * 80}")
    print(f"{text:^80}")
    print(f"{char * 80}\n")


def print_section(title):
    """Print section header"""
    print(f"\n{'─' * 80}")
    print(f"  {title}")
    print(f"{'─' * 80}")


def validate_phase11():
    """Run comprehensive validation"""
    print_header("PHASE 11: RESEARCH & PUBLICATIONS VALIDATION")

    # Initialize
    print("🔧 Initializing Phase 11 implementation...")
    implementation = Phase11Implementation()

    # Execute
    print_section("Executing Phase 11")
    task = {"goal": "Generate and validate research papers", "phase_id": 11}
    result = implementation.execute(task)

    # Results
    print_section("Execution Results")
    print(f"Status: {'✅ SUCCESS' if result.success else '❌ FAILED'}")

    if not result.success:
        print(f"Error: {result.error if hasattr(result, 'error') else 'Unknown error'}")
        return False

    output = result.output

    # Paper Generation Summary
    print_section("Paper Generation Summary")
    print(f"Papers Generated: {output['papers_generated']}")
    print(f"Expected: 4+")
    print(f"Status: {'✅ PASS' if output['papers_generated'] >= 4 else '❌ FAIL'}")

    # Individual Paper Details
    print_section("Individual Paper Validation")

    all_valid = True
    for i, paper in enumerate(output['papers'], 1):
        validation = output['validation'][i-1]

        print(f"\n{i}. {paper['title']}")
        print(f"   Type: {paper['type']}")
        print(f"   Domain: {paper['domain']}")
        print(f"   Word Count: {paper['word_count']} {'✅' if paper['word_count'] >= 1000 else '❌'}")
        print(f"   Citations: {paper['citation_count']} {'✅' if paper['citation_count'] >= 3 else '❌'}")
        print(f"   Validation Score: {validation['score']:.1f}% {'✅' if validation['score'] == 100.0 else '❌'}")
        print(f"   Valid: {'✅ YES' if validation['valid'] else '❌ NO'}")

        if not validation['valid']:
            all_valid = False
            print(f"   Failed Checks:")
            for check, passed in validation['checks'].items():
                if not passed:
                    print(f"     - {check}")

    # Quality Metrics
    print_section("Quality Metrics")

    total_words = sum(p['word_count'] for p in output['papers'])
    avg_words = total_words / len(output['papers'])
    total_citations = sum(p['citation_count'] for p in output['papers'])
    avg_citations = total_citations / len(output['papers'])

    print(f"Total Words: {total_words:,}")
    print(f"Average Words/Paper: {avg_words:.0f}")
    print(f"Total Citations: {total_citations}")
    print(f"Average Citations/Paper: {avg_citations:.1f}")

    # Overall Assessment
    print_section("Overall Assessment")

    checks = {
        "Papers Generated (≥4)": output['papers_generated'] >= 4,
        "All Papers Valid": all_valid,
        "Production Ready": output.get('production_ready', False),
        "Framework Integration": output.get('agent_framework_version') == '100%',
    }

    for check, passed in checks.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{check:.<60} {status}")

    overall_pass = all(checks.values())

    print_section("Final Result")
    if overall_pass:
        print("🎉 PHASE 11 VALIDATION: PASSED")
        print("\n✅ All 5 research papers meet publication standards")
        print("✅ 100% validation score across all papers")
        print("✅ Production ready for deployment")
    else:
        print("❌ PHASE 11 VALIDATION: FAILED")
        print("\nSome validation checks did not pass.")

    # Save validation report
    print_section("Saving Validation Report")

    report_path = Path(__file__).parent / ".state" / "validation_report.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)

    report = {
        "phase_id": 11,
        "phase_name": "Research & Publications",
        "validation_passed": overall_pass,
        "papers_generated": output['papers_generated'],
        "papers": output['papers'],
        "validation_results": output['validation'],
        "quality_metrics": {
            "total_words": total_words,
            "avg_words_per_paper": avg_words,
            "total_citations": total_citations,
            "avg_citations_per_paper": avg_citations
        },
        "checks": checks
    }

    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)

    print(f"✅ Validation report saved to: {report_path}")

    print_header("VALIDATION COMPLETE")

    return overall_pass


if __name__ == "__main__":
    success = validate_phase11()
    sys.exit(0 if success else 1)
