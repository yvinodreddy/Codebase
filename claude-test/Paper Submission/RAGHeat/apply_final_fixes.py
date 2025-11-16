#!/usr/bin/env python3
"""
Apply final fixes for text/table overlapping
"""

import re

with open('stock_heat_diffusion_model_WORLD_CLASS_FINAL.tex', 'r', encoding='utf-8') as f:
    content = f.read()

# FIX 1: Add abstract in smaller font with raggedright
content = re.sub(
    r'(\\begin\{abstract\})',
    r'\1\n\\small\\RaggedRight',
    content
)

# FIX 2: Fix all wide tables with resizebox
content = re.sub(
    r'(\\begin\{table\*\}\[!t\]\s*\\centering\s*\\caption\{[^\}]+\}\s*\\label\{[^\}]+\}\s*\\scriptsize\s*)(\\begin\{tabular\})',
    r'\1\\resizebox{\\textwidth}{!}{%\n\2',
    content
)

content = re.sub(
    r'(\\end\{tabular\})\s*(\\end\{table\*\})',
    r'\1%\n}\n\2',
    content
)

# FIX 3: Add \sloppy to prevent text overflow
content = re.sub(
    r'(\\begin\{document\})',
    r'\1\n\\sloppy  % Prevent text overflow',
    content
)

# FIX 4: Fix URLs
content = content.replace('\\texttt{https://github.com/ragheat/stock-diffusion}', '\\url{https://github.com/ragheat/stock-diffusion}')
content = content.replace('\\texttt{https://github.com/ragheat/stock-heat-diffusion}', '\\url{https://github.com/ragheat/stock-heat-diffusion}')
content = content.replace('\\texttt{github.com/ragheat/stock-diffusion}', '\\url{https://github.com/ragheat/stock-diffusion}')

# FIX 5: Add proper float placement
content = re.sub(
    r'(\\begin\{table\}\[!t\])',
    r'\\begin{table}[!htbp]',
    content
)

content = re.sub(
    r'(\\begin\{table\*\}\[!t\])',
    r'\\begin{table*}[!htbp]',
    content
)

# FIX 6: Add balance command before bibliography
content = re.sub(
    r'(\\begin\{thebibliography\})',
    r'\\balance\n\1',
    content
)

with open('stock_heat_diffusion_model_WORLD_CLASS_FINAL.tex', 'w', encoding='utf-8') as f:
    f.write(content)

print("✓ Applied all final fixes:")
print("  - Added \\small\\RaggedRight to abstract")
print("  - Fixed all wide tables with resizebox")
print("  - Added \\sloppy to prevent overflow")
print("  - Fixed all GitHub URLs")
print("  - Improved float placement [!htbp]")
print("  - Added \\balance before bibliography")
