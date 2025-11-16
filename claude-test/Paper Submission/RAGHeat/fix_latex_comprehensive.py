#!/usr/bin/env python3
"""
Comprehensive LaTeX Fixer for World-Class IEEE Paper
Fixes all formatting issues systematically
"""

import re

# Read the original file (first 1446 lines only, no duplicates)
with open('stock_heat_diffusion_model_FINAL_ULTIMATE.tex', 'r', encoding='utf-8') as f:
    lines = f.readlines()[:1446]

# Remove any tcolorbox-related lines
cleaned_lines = []
skip = False
for i, line in enumerate(lines):
    if 'tcolorbox' in line or 'tcbuselibrary' in line or 'newtcbtheorem' in line:
        skip = True
    elif skip and line.strip() and not line.strip().startswith('%') and '\\' in line and 'theorem' not in line.lower():
        skip = False
        
    if not skip:
        cleaned_lines.append(line)

# Find where to insert new packages (after tikz library)
insert_idx = None
for i, line in enumerate(cleaned_lines):
    if 'usetikzlibrary' in line:
        insert_idx = i + 1
        break

if insert_idx:
    # Insert new packages and theorem environments
    new_content = [
        '\n',
        '% Additional packages for world-class formatting\n',
        '\\usepackage{mdframed}   % For boxed theorems\n',
        '\\usepackage{breakurl}   % For URL breaking\n',
        '\\usepackage{microtype}  % Better typography\n',
        '\\usepackage{balance}    % Balanced columns\n',
        '\\usepackage{dblfloatfix} % Fix for two-column floats\n',
        '\n',
        '% Theorem environments (standard numbering)\n',
        '\\newtheorem{theorem}{Theorem}[section]\n',
        '\\newtheorem{lemma}[theorem]{Lemma}\n',
        '\\newtheorem{definition}[theorem]{Definition}\n',
        '\\newtheorem{problem}[theorem]{Problem}\n',
        '\\newtheorem{corollary}[theorem]{Corollary}\n',
        '\n',
    ]
    cleaned_lines = cleaned_lines[:insert_idx] + new_content + cleaned_lines[insert_idx:]

# Add closing \end{document} command
cleaned_lines.append('\n')
cleaned_lines.append('\\end{document}\n')

# Write the fixed file
with open('stock_heat_diffusion_model_WORLD_CLASS_FINAL.tex', 'w', encoding='utf-8') as f:
    f.writelines(cleaned_lines)

print("✓ Fixed LaTeX file created: stock_heat_diffusion_model_WORLD_CLASS_FINAL.tex")
print(f"✓ Total lines: {len(cleaned_lines)}")
print("✓ Removed tcolorbox (caused counter errors)")
print("✓ Added mdframed, breakurl, microtype, balance, dblfloatfix")
print("✓ Added standard theorem environments")
print("✓ Added \\end{document} command")
