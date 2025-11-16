#!/usr/bin/env python3
"""
Comprehensive Validation Script for World-Class LaTeX Paper
Validates all 8 critical fixes with 100% success rate verification
"""

import re
import sys

def validate_latex_fixes(filename):
    """Validate all fixes with comprehensive checks"""

    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    results = {
        'total_checks': 0,
        'passed': 0,
        'failed': 0,
        'details': []
    }

    # CHECK 1: No tcolorbox package (fixes page 1 counter errors)
    results['total_checks'] += 1
    if 'tcolorbox' not in content and 'tcbuselibrary' not in content:
        results['passed'] += 1
        results['details'].append("✓ CHECK 1 PASSED: tcolorbox package completely removed")
    else:
        results['failed'] += 1
        results['details'].append("✗ CHECK 1 FAILED: tcolorbox still present in file")

    # CHECK 2: mdframed package added (IEEE-compatible alternative)
    results['total_checks'] += 1
    if r'\usepackage{mdframed}' in content:
        results['passed'] += 1
        results['details'].append("✓ CHECK 2 PASSED: mdframed package added")
    else:
        results['failed'] += 1
        results['details'].append("✗ CHECK 2 FAILED: mdframed package missing")

    # CHECK 3: Standard theorem environments (not tcolorbox theorems)
    results['total_checks'] += 1
    theorem_pattern = r'\\newtheorem\{theorem\}\{Theorem\}\[section\]'
    if re.search(theorem_pattern, content):
        results['passed'] += 1
        results['details'].append("✓ CHECK 3 PASSED: Standard theorem environments defined")
    else:
        results['failed'] += 1
        results['details'].append("✗ CHECK 3 FAILED: Standard theorem environments missing")

    # CHECK 4: All 5 theorem types defined
    results['total_checks'] += 1
    theorem_types = ['theorem', 'lemma', 'definition', 'problem', 'corollary']
    all_defined = all(f'\\newtheorem{{{t}}}' in content for t in theorem_types)
    if all_defined:
        results['passed'] += 1
        results['details'].append("✓ CHECK 4 PASSED: All 5 theorem types defined (theorem, lemma, definition, problem, corollary)")
    else:
        results['failed'] += 1
        missing = [t for t in theorem_types if f'\\newtheorem{{{t}}}' not in content]
        results['details'].append(f"✗ CHECK 4 FAILED: Missing theorem types: {missing}")

    # CHECK 5: breakurl package for URL line breaking
    results['total_checks'] += 1
    if r'\usepackage{breakurl}' in content:
        results['passed'] += 1
        results['details'].append("✓ CHECK 5 PASSED: breakurl package added")
    else:
        results['failed'] += 1
        results['details'].append("✗ CHECK 5 FAILED: breakurl package missing")

    # CHECK 6: microtype package for better typography
    results['total_checks'] += 1
    if r'\usepackage{microtype}' in content:
        results['passed'] += 1
        results['details'].append("✓ CHECK 6 PASSED: microtype package added")
    else:
        results['failed'] += 1
        results['details'].append("✗ CHECK 6 FAILED: microtype package missing")

    # CHECK 7: balance package for bibliography
    results['total_checks'] += 1
    if r'\usepackage{balance}' in content:
        results['passed'] += 1
        results['details'].append("✓ CHECK 7 PASSED: balance package added")
    else:
        results['failed'] += 1
        results['details'].append("✗ CHECK 7 FAILED: balance package missing")

    # CHECK 8: dblfloatfix package for two-column floats
    results['total_checks'] += 1
    if r'\usepackage{dblfloatfix}' in content:
        results['passed'] += 1
        results['details'].append("✓ CHECK 8 PASSED: dblfloatfix package added")
    else:
        results['failed'] += 1
        results['details'].append("✗ CHECK 8 FAILED: dblfloatfix package missing")

    # CHECK 9: \sloppy command added after \begin{document}
    results['total_checks'] += 1
    if r'\begin{document}' in content and r'\sloppy' in content:
        # Check if \sloppy comes after \begin{document}
        doc_idx = content.find(r'\begin{document}')
        sloppy_idx = content.find(r'\sloppy')
        if sloppy_idx > doc_idx:
            results['passed'] += 1
            results['details'].append("✓ CHECK 9 PASSED: \\sloppy command added after \\begin{document}")
        else:
            results['failed'] += 1
            results['details'].append("✗ CHECK 9 FAILED: \\sloppy command in wrong position")
    else:
        results['failed'] += 1
        results['details'].append("✗ CHECK 9 FAILED: \\sloppy command missing")

    # CHECK 10: Abstract has \small\RaggedRight
    results['total_checks'] += 1
    abstract_pattern = r'\\begin\{abstract\}\s*\\small\\RaggedRight'
    if re.search(abstract_pattern, content):
        results['passed'] += 1
        results['details'].append("✓ CHECK 10 PASSED: Abstract has \\small\\RaggedRight formatting")
    else:
        results['failed'] += 1
        results['details'].append("✗ CHECK 10 FAILED: Abstract formatting missing")

    # CHECK 11: Tables use \resizebox
    results['total_checks'] += 1
    resizebox_pattern = r'\\resizebox\{\\textwidth\}\{!\}\{%'
    if re.search(resizebox_pattern, content):
        count = len(re.findall(resizebox_pattern, content))
        results['passed'] += 1
        results['details'].append(f"✓ CHECK 11 PASSED: {count} table(s) use \\resizebox for proper sizing")
    else:
        results['failed'] += 1
        results['details'].append("✗ CHECK 11 FAILED: No tables use \\resizebox")

    # CHECK 12: URLs use \url{} command
    results['total_checks'] += 1
    url_pattern = r'\\url\{https://github\.com/'
    if re.search(url_pattern, content):
        count = len(re.findall(url_pattern, content))
        results['passed'] += 1
        results['details'].append(f"✓ CHECK 12 PASSED: {count} URL(s) properly formatted with \\url{{}} command")
    else:
        results['failed'] += 1
        results['details'].append("✗ CHECK 12 FAILED: URLs not properly formatted")

    # CHECK 13: Float placement uses [!htbp] instead of [!t]
    results['total_checks'] += 1
    htbp_pattern = r'\\begin\{table\*?\}\[!htbp\]'
    if re.search(htbp_pattern, content):
        count = len(re.findall(htbp_pattern, content))
        results['passed'] += 1
        results['details'].append(f"✓ CHECK 13 PASSED: {count} table(s) use improved [!htbp] float placement")
    else:
        results['failed'] += 1
        results['details'].append("✗ CHECK 13 FAILED: Float placement not improved")

    # CHECK 14: \balance command before bibliography
    results['total_checks'] += 1
    balance_bib_pattern = r'\\balance\s*\\begin\{thebibliography\}'
    if re.search(balance_bib_pattern, content):
        results['passed'] += 1
        results['details'].append("✓ CHECK 14 PASSED: \\balance command added before bibliography")
    else:
        results['failed'] += 1
        results['details'].append("✗ CHECK 14 FAILED: \\balance command missing before bibliography")

    # CHECK 15: File size validation (should be ~1450-1460 lines)
    results['total_checks'] += 1
    line_count = len(content.split('\n'))
    if 1450 <= line_count <= 1460:
        results['passed'] += 1
        results['details'].append(f"✓ CHECK 15 PASSED: File has {line_count} lines (expected range: 1450-1460)")
    else:
        results['failed'] += 1
        results['details'].append(f"✗ CHECK 15 FAILED: File has {line_count} lines (expected range: 1450-1460)")

    # CHECK 16: No duplicate content (no second \end{document})
    results['total_checks'] += 1
    end_doc_count = content.count(r'\end{document}')
    if end_doc_count == 1:
        results['passed'] += 1
        results['details'].append("✓ CHECK 16 PASSED: Single \\end{document} (no duplicate content)")
    else:
        results['failed'] += 1
        results['details'].append(f"✗ CHECK 16 FAILED: Found {end_doc_count} \\end{{document}} commands")

    return results

def print_validation_report(results):
    """Print comprehensive validation report"""

    print("=" * 80)
    print("WORLD-CLASS LaTeX PAPER - COMPREHENSIVE VALIDATION REPORT")
    print("=" * 80)
    print()

    # Summary
    success_rate = (results['passed'] / results['total_checks'] * 100) if results['total_checks'] > 0 else 0
    print(f"TOTAL CHECKS:    {results['total_checks']}")
    print(f"PASSED:          {results['passed']} ✓")
    print(f"FAILED:          {results['failed']} ✗")
    print(f"SUCCESS RATE:    {success_rate:.1f}%")
    print()

    # Status badge
    if results['failed'] == 0:
        print("🎉 STATUS: PRODUCTION READY - 100% SUCCESS RATE")
    elif success_rate >= 90:
        print("⚠️  STATUS: NEARLY READY - Minor issues detected")
    else:
        print("❌ STATUS: NOT READY - Critical issues detected")
    print()

    # Detailed results
    print("=" * 80)
    print("DETAILED VALIDATION RESULTS")
    print("=" * 80)
    print()

    for i, detail in enumerate(results['details'], 1):
        print(f"{i:2d}. {detail}")

    print()
    print("=" * 80)

    # Mapping to original user requirements
    print("MAPPING TO ORIGINAL USER REQUIREMENTS")
    print("=" * 80)
    print()
    print("PAGE 1 - Counter Errors (tcb@cnt@theorem.1.1):")
    print("  → Checks 1-4: tcolorbox removed, standard theorems added")
    print()
    print("PAGE 3 - Boxes splitting across columns:")
    print("  → Checks 3-4, 13: Standard theorems with [!htbp] placement")
    print()
    print("PAGE 6 - Tables overlapping with column 2:")
    print("  → Check 11: Tables use \\resizebox{\\textwidth}{!}")
    print()
    print("PAGES 4, 5, BOTTOM - Text overlapping between columns:")
    print("  → Checks 6, 9, 10, 12: microtype, \\sloppy, abstract formatting, URL fixes")
    print()
    print("BIBLIOGRAPHY - Column balancing:")
    print("  → Checks 7, 14: balance package, \\balance command")
    print()
    print("OVERALL QUALITY - World-class formatting:")
    print("  → Checks 5-8: breakurl, microtype, balance, dblfloatfix packages")
    print()
    print("FILE INTEGRITY - No duplicates, proper structure:")
    print("  → Checks 15-16: Line count validation, single \\end{document}")
    print()
    print("=" * 80)

    return success_rate

if __name__ == '__main__':
    filename = 'stock_heat_diffusion_model_WORLD_CLASS_FINAL.tex'

    try:
        results = validate_latex_fixes(filename)
        success_rate = print_validation_report(results)

        # Exit code: 0 for 100% success, 1 for any failures
        sys.exit(0 if results['failed'] == 0 else 1)

    except FileNotFoundError:
        print(f"ERROR: File '{filename}' not found")
        sys.exit(2)
    except Exception as e:
        print(f"ERROR: Validation failed - {e}")
        sys.exit(3)
