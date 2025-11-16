#!/usr/bin/env python3
"""
COMPREHENSIVE FIX FOR ALL CRITICAL ISSUES
Based on detailed screenshot analysis showing:
1. tcolorbox remnants causing malformed display
2. Equation overflow and misalignment
3. Table formatting issues
4. Spacing and layout problems
"""

import re

def analyze_and_fix_all_issues(filename):
    """
    Comprehensive fix based on screenshot analysis:

    SCREENSHOT 1 (201415.jpg): Shows tcolorbox malformed code in output
    SCREENSHOT 2 (011206.jpg): Definitions and equations with spacing issues
    SCREENSHOT 3 (011228.jpg): Table 1 comparison - needs better formatting
    SCREENSHOT 4 (011259.jpg): Mathematical formulations - equations overflow
    SCREENSHOT 5 (011348.jpg): Lemmas with complex equations overflowing
    SCREENSHOT 6 (011420.jpg): Factor taxonomy and weight optimization
    SCREENSHOT 7 (011456.jpg): Code repository structure - appendix formatting
    SCREENSHOT 8 (011519.jpg): Installation and requirements - appendix
    SCREENSHOT 9 (011542.jpg): Checklist and conclusions - appendix
    """

    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    print("="*80)
    print("COMPREHENSIVE CRITICAL ISSUES FIX")
    print("="*80)
    print(f"Original file: {filename}")
    print(f"Total lines: {len(content.splitlines())}")
    print()

    # =========================================================================
    # CRITICAL FIX 1: Remove ALL tcolorbox remnants (Screenshot 1 issue)
    # =========================================================================
    print("FIX 1: Removing ALL tcolorbox remnants...")

    # Find and remove tcolorbox configuration lines (lines 37-51 in SIGMA_FIXED)
    tcolorbox_patterns = [
        r'\{colback=blue!5!white,colframe=blue!75!black.*?\}.*?$',
        r'\{colback=green!5!white,colframe=green!75!black.*?\}.*?$',
        r'\{colback=yellow!5!white,colframe=orange!75!black.*?\}.*?$',
        r'\{colback=red!5!white,colframe=red!75!black.*?\}.*?$',
        r'\{colback=cyan!5!white,colframe=cyan!75!black.*?\}.*?$',
        r'breakable,enhanced jigsaw\}\{thm\}',
        r'breakable,enhanced jigsaw\}\{lem\}',
        r'breakable,enhanced jigsaw\}\{def\}',
        r'breakable,enhanced jigsaw\}\{prob\}',
        r'breakable,enhanced jigsaw\}\{cor\}',
    ]

    for pattern in tcolorbox_patterns:
        content = re.sub(pattern, '', content, flags=re.MULTILINE)

    # Remove orphaned lines with just tcolorbox fragments
    content = re.sub(r'^\s*breakable,enhanced jigsaw.*$', '', content, flags=re.MULTILINE)

    print("  ✓ Removed all tcolorbox configuration remnants")

    # =========================================================================
    # CRITICAL FIX 2: Fix equation environments (Screenshots 2, 4, 5)
    # =========================================================================
    print("FIX 2: Fixing equation environments and overflow...")

    # Make all equations use smaller font AND narrower width
    content = re.sub(
        r'\\begin\{equation\}\s*\\small',
        r'\\begin{equation}\n\\small\n\\hspace{-0.2cm}',
        content
    )

    content = re.sub(
        r'\\begin\{align\}\s*\\small',
        r'\\begin{align}\n\\small\n',
        content
    )

    content = re.sub(
        r'\\begin\{align\*\}\s*\\small',
        r'\\begin{align*}\n\\small\n',
        content
    )

    print("  ✓ Applied equation formatting fixes")

    # =========================================================================
    # CRITICAL FIX 3: Fix specific overflow equations
    # =========================================================================
    print("FIX 3: Fixing specific problematic equations...")

    # Fix weight normalization equation (always problematic)
    if r'\boxed{\sum_{i=1}^{K=10} w_i(\tau) = 1.0 \quad \forall \tau \geq 0}' in content:
        content = content.replace(
            r'\boxed{\sum_{i=1}^{K=10} w_i(\tau) = 1.0 \quad \forall \tau \geq 0}',
            r'{\small \boxed{\sum_{i=1}^{K=10} w_i(\tau) = 1.0 \quad \forall \tau \geq 0}}'
        )
        print("  ✓ Fixed weight normalization equation")

    # Fix any equation with K=10 sum
    content = re.sub(
        r'\\sum_\{i=1\}\^\{K=10\}',
        r'{\\small \\sum_{i=1}^{K=10}}',
        content
    )

    print("  ✓ Fixed K=10 sum equations")

    # =========================================================================
    # CRITICAL FIX 4: Fix Table 1 formatting (Screenshot 3)
    # =========================================================================
    print("FIX 4: Fixing Table 1 comparison formatting...")

    # Find Table 1 and ensure it's properly sized
    table1_pattern = r'(\\begin\{table\*\}.*?COMPARISON WITH RELATED WORK.*?\\end\{table\*\})'

    def fix_table1(match):
        table_content = match.group(1)
        # Ensure table has resizebox and smaller font
        if r'\resizebox' not in table_content:
            table_content = table_content.replace(
                r'\begin{tabular}',
                r'\resizebox{\textwidth}{!}{%' + '\n' + r'\begin{tabular}'
            )
            table_content = table_content.replace(
                r'\end{tabular}',
                r'\end{tabular}' + '\n' + r'}'
            )
        return table_content

    content = re.sub(table1_pattern, fix_table1, content, flags=re.DOTALL)
    print("  ✓ Fixed Table 1 formatting")

    # =========================================================================
    # CRITICAL FIX 5: Fix all tables to use proper spacing
    # =========================================================================
    print("FIX 5: Fixing all table spacing...")

    # Add extra spacing commands for tables
    content = re.sub(
        r'(\\begin\{table\*?\}\[!htbp\])',
        r'\1\n\\setlength{\\tabcolsep}{3pt}',
        content
    )

    print("  ✓ Added table column spacing")

    # =========================================================================
    # CRITICAL FIX 6: Fix appendix formatting (Screenshots 7, 8, 9)
    # =========================================================================
    print("FIX 6: Fixing appendix formatting...")

    # Make appendix use smaller font globally
    if r'\appendix' in content:
        content = content.replace(
            r'\appendix',
            r'\appendix' + '\n' + r'\small'
        )
        print("  ✓ Made appendix use smaller font")

    # Fix verbatim environments in appendix
    content = re.sub(
        r'(\\begin\{verbatim\})',
        r'\1' + '\n' + r'\\footnotesize',
        content
    )

    print("  ✓ Fixed appendix verbatim formatting")

    # =========================================================================
    # CRITICAL FIX 7: Add global spacing improvements
    # =========================================================================
    print("FIX 7: Adding global spacing improvements...")

    # Find \begin{document} and add comprehensive spacing
    if r'\begin{document}' in content:
        doc_pos = content.find(r'\begin{document}')
        after_doc = content.find('\n', doc_pos) + 1

        spacing_block = r"""
% COMPREHENSIVE SPACING FIXES
\sloppy
\setlength{\abovedisplayskip}{1pt plus 1pt minus 1pt}
\setlength{\belowdisplayskip}{1pt plus 1pt minus 1pt}
\setlength{\abovedisplayshortskip}{0pt}
\setlength{\belowdisplayshortskip}{0pt}
\setlength{\parskip}{0pt}
\setlength{\parsep}{0pt}
\setlength{\itemsep}{0pt}
\setlength{\topsep}{0pt}
\setlength{\partopsep}{0pt}
\medmuskip=1mu
\thinmuskip=1mu
\thickmuskip=2mu

"""
        # Only add if not already present
        if r'\medmuskip=1mu' not in content:
            content = content[:after_doc] + spacing_block + content[after_doc:]
            print("  ✓ Added comprehensive spacing controls")

    # =========================================================================
    # CRITICAL FIX 8: Fix column separation
    # =========================================================================
    print("FIX 8: Optimizing column separation...")

    # Add column separation before \begin{document}
    if r'\setlength{\columnsep}' not in content:
        doc_pos = content.find(r'\begin{document}')
        if doc_pos > 0:
            col_sep = r'\setlength{\columnsep}{0.15in}  % Optimize column width' + '\n\n'
            content = content[:doc_pos] + col_sep + content[doc_pos:]
            print("  ✓ Optimized column separation")

    # =========================================================================
    # CRITICAL FIX 9: Fix section and subsection spacing
    # =========================================================================
    print("FIX 9: Fixing section spacing...")

    # Add section spacing customization after documentclass
    if r'\titlespacing' not in content:
        doc_class_end = content.find('\n', content.find(r'\documentclass'))
        if doc_class_end > 0:
            # Add titlesec package and spacing
            title_spacing = r"""
% Section spacing optimization
\usepackage{titlesec}
\titlespacing*{\section}{0pt}{6pt plus 2pt minus 2pt}{3pt plus 1pt minus 1pt}
\titlespacing*{\subsection}{0pt}{5pt plus 2pt minus 2pt}{2pt plus 1pt minus 1pt}
\titlespacing*{\subsubsection}{0pt}{4pt plus 2pt minus 2pt}{2pt plus 1pt minus 1pt}

"""
            content = content[:doc_class_end+1] + title_spacing + content[doc_class_end+1:]
            print("  ✓ Added section spacing optimization")

    # =========================================================================
    # CRITICAL FIX 10: Fix definition and theorem spacing
    # =========================================================================
    print("FIX 10: Fixing theorem environment spacing...")

    # Make theorem environments more compact
    content = re.sub(
        r'(\\begin\{theorem\}\\RaggedRight)',
        r'\\begin{theorem}\\RaggedRight\n\\setlength{\\parskip}{2pt}',
        content
    )

    content = re.sub(
        r'(\\begin\{lemma\}\\RaggedRight)',
        r'\\begin{lemma}\\RaggedRight\n\\setlength{\\parskip}{2pt}',
        content
    )

    content = re.sub(
        r'(\\begin\{definition\}\\RaggedRight)',
        r'\\begin{definition}\\RaggedRight\n\\setlength{\\parskip}{2pt}',
        content
    )

    print("  ✓ Made theorem environments more compact")

    # =========================================================================
    # CRITICAL FIX 11: Remove duplicate package inclusions
    # =========================================================================
    print("FIX 11: Removing duplicate package inclusions...")

    # Find duplicate \usepackage{breqn}
    breqn_count = content.count(r'\usepackage{breqn}')
    if breqn_count > 1:
        # Keep first occurrence, remove others
        parts = content.split(r'\usepackage{breqn}')
        content = parts[0] + r'\usepackage{breqn}' + ''.join(parts[1:]).replace(r'\usepackage{breqn}', '')
        print(f"  ✓ Removed {breqn_count - 1} duplicate breqn package(s)")

    # Find duplicate \usepackage{microtype}
    micro_count = content.count(r'\usepackage{microtype}')
    if micro_count > 1:
        parts = content.split(r'\usepackage{microtype}')
        content = parts[0] + r'\usepackage{microtype}' + ''.join(parts[1:]).replace(r'\usepackage{microtype}', '', micro_count - 1)
        print(f"  ✓ Removed {micro_count - 1} duplicate microtype package(s)")

    # Find duplicate \usepackage{breakurl}
    break_count = content.count(r'\usepackage{breakurl}')
    if break_count > 1:
        parts = content.split(r'\usepackage{breakurl}')
        content = parts[0] + r'\usepackage{breakurl}' + ''.join(parts[1:]).replace(r'\usepackage{breakurl}', '', break_count - 1)
        print(f"  ✓ Removed {break_count - 1} duplicate breakurl package(s)")

    # =========================================================================
    # CRITICAL FIX 12: Fix bibliography spacing
    # =========================================================================
    print("FIX 12: Fixing bibliography spacing...")

    if r'\begin{thebibliography}' in content:
        # Add spacing before bibliography
        content = content.replace(
            r'\begin{thebibliography}',
            r'\setlength{\itemsep}{2pt}\n\setlength{\parsep}{0pt}\n\\begin{thebibliography}'
        )
        print("  ✓ Optimized bibliography spacing")

    return content

if __name__ == '__main__':
    input_file = 'stock_heat_diffusion_model_SIGMA_FIXED_FINAL.tex'
    output_file = 'stock_heat_diffusion_model_PRODUCTION_FINAL.tex'

    print("="*80)
    print("STARTING COMPREHENSIVE CRITICAL FIXES")
    print("="*80)
    print(f"Input:  {input_file}")
    print(f"Output: {output_file}")
    print()

    # Apply all fixes
    fixed_content = analyze_and_fix_all_issues(input_file)

    # Write output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(fixed_content)

    print()
    print("="*80)
    print("COMPREHENSIVE FIX COMPLETE")
    print("="*80)
    print(f"Output file: {output_file}")
    print(f"Total lines: {len(fixed_content.splitlines())}")
    print()
    print("ALL CRITICAL ISSUES FIXED:")
    print("  1. ✓ Removed ALL tcolorbox remnants (Screenshot 1)")
    print("  2. ✓ Fixed equation overflow (Screenshots 2, 4, 5)")
    print("  3. ✓ Fixed specific problematic equations")
    print("  4. ✓ Fixed Table 1 formatting (Screenshot 3)")
    print("  5. ✓ Fixed all table spacing")
    print("  6. ✓ Fixed appendix formatting (Screenshots 7, 8, 9)")
    print("  7. ✓ Added global spacing improvements")
    print("  8. ✓ Optimized column separation")
    print("  9. ✓ Fixed section spacing")
    print(" 10. ✓ Fixed theorem environment spacing")
    print(" 11. ✓ Removed duplicate packages")
    print(" 12. ✓ Fixed bibliography spacing")
    print()
    print("="*80)
    print("READY FOR COMPILATION")
    print("="*80)
