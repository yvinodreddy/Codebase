#!/usr/bin/env python3
"""
Validate all research papers meet production standards
Comprehensive validation script
"""

import json
import sys
from pathlib import Path


def validate_paper_file(paper_file):
    """Validate a paper markdown file"""

    if not paper_file.exists():
        return {"valid": False, "error": "File not found"}

    content = paper_file.read_text()

    checks = {
        "has_title": "# " in content,
        "has_authors": "**Authors**:" in content,
        "has_abstract": "## Abstract" in content,
        "has_introduction": "# 1. Introduction" in content,
        "has_methodology": "# 2. Methodology" in content,
        "has_results": "# 3. Results" in content,
        "has_discussion": "# 4. Discussion" in content,
        "has_conclusion": "# 5. Conclusion" in content,
        "has_references": "## References" in content,
        "sufficient_length": len(content) > 5000,  # At least 5KB
    }

    all_passed = all(checks.values())

    return {
        "valid": all_passed,
        "checks": checks,
        "size": len(content),
        "file": paper_file.name
    }


def validate_bibtex_file(bibtex_file):
    """Validate a BibTeX file"""

    if not bibtex_file.exists():
        return {"valid": False, "error": "File not found"}

    content = bibtex_file.read_text()

    checks = {
        "has_entries": "@article{" in content or "@inproceedings{" in content,
        "has_author": "author = {" in content,
        "has_title": "title = {" in content,
        "has_journal": "journal = {" in content,
        "has_year": "year = {" in content,
        "sufficient_entries": content.count("@article{") >= 1,
    }

    all_passed = all(checks.values())

    return {
        "valid": all_passed,
        "checks": checks,
        "entries": content.count("@article{") + content.count("@inproceedings{"),
        "file": bibtex_file.name
    }


def main():
    """Main validation function"""

    print("=" * 80)
    print("VALIDATING RESEARCH PAPERS - PRODUCTION STANDARDS")
    print("=" * 80)
    print()

    deliverables_dir = Path(__file__).parent

    papers_valid = 0
    papers_total = 0
    bibtex_valid = 0
    bibtex_total = 0

    # Validate papers
    print("Validating Papers:")
    print("-" * 80)

    for paper_num in range(1, 6):
        # Find paper file (domain-specific naming)
        paper_files = list(deliverables_dir.glob(f"paper_{paper_num:02d}_*.md"))

        if not paper_files:
            print(f"❌ Paper {paper_num}: Not found")
            papers_total += 1
            continue

        paper_file = paper_files[0]
        papers_total += 1

        result = validate_paper_file(paper_file)

        if result["valid"]:
            papers_valid += 1
            print(f"✅ Paper {paper_num}: {paper_file.name}")
            print(f"   Size: {result['size']:,} bytes")
        else:
            print(f"❌ Paper {paper_num}: {paper_file.name}")
            print(f"   Failed checks: {[k for k, v in result['checks'].items() if not v]}")

    print()

    # Validate BibTeX files
    print("Validating Citations:")
    print("-" * 80)

    for paper_num in range(1, 6):
        bibtex_file = deliverables_dir / f"paper_{paper_num:02d}_citations.bib"
        bibtex_total += 1

        result = validate_bibtex_file(bibtex_file)

        if result["valid"]:
            bibtex_valid += 1
            print(f"✅ BibTeX {paper_num}: {bibtex_file.name} ({result['entries']} entries)")
        else:
            print(f"❌ BibTeX {paper_num}: {bibtex_file.name}")

    # Validate combined BibTeX
    all_bibtex = deliverables_dir / "all_citations.bib"
    if all_bibtex.exists():
        result = validate_bibtex_file(all_bibtex)
        if result["valid"]:
            print(f"✅ Combined BibTeX: all_citations.bib ({result['entries']} entries)")
        else:
            print(f"❌ Combined BibTeX: all_citations.bib")

    print()
    print("=" * 80)
    print("VALIDATION SUMMARY")
    print("=" * 80)
    print()
    print(f"Papers Validated: {papers_valid}/{papers_total} ({papers_valid/papers_total*100:.0f}%)")
    print(f"BibTeX Validated: {bibtex_valid}/{bibtex_total} ({bibtex_valid/bibtex_total*100:.0f}%)")
    print()

    all_valid = papers_valid == papers_total and bibtex_valid == bibtex_total

    if all_valid:
        print("✅ ALL VALIDATIONS PASSED - PRODUCTION READY")
        return 0
    else:
        print("❌ SOME VALIDATIONS FAILED")
        return 1


if __name__ == "__main__":
    sys.exit(main())
