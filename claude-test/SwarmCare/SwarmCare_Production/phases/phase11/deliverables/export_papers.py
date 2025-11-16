#!/usr/bin/env python3
"""
Export research papers to multiple formats
Supports: PDF, DOCX, LaTeX, HTML
"""

import sys
import argparse
from pathlib import Path


def export_to_html(paper_file, output_dir):
    """Export Markdown to HTML"""
    import markdown

    content = paper_file.read_text()
    html = markdown.markdown(content, extensions=['extra', 'codehilite', 'toc'])

    html_template = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>SwarmCare Research Paper</title>
    <style>
        body {{ font-family: 'Georgia', serif; max-width: 800px; margin: 40px auto; line-height: 1.6; }}
        h1 {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
        h2 {{ color: #34495e; margin-top: 30px; }}
        code {{ background: #f4f4f4; padding: 2px 6px; border-radius: 3px; }}
        table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
        th {{ background-color: #3498db; color: white; }}
    </style>
</head>
<body>
{html}
</body>
</html>"""

    output_file = output_dir / paper_file.with_suffix('.html').name
    output_file.write_text(html_template)
    return output_file


def export_to_latex(paper_file, output_dir):
    """Export Markdown to LaTeX"""

    content = paper_file.read_text()

    # Basic Markdown to LaTeX conversion
    latex = content.replace('#', '\\section')
    latex = latex.replace('**', '\\textbf{')
    latex = latex.replace('*', '\\textit{')

    latex_template = f"""\\documentclass[11pt,a4paper]{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage{{geometry}}
\\usepackage{{hyperref}}
\\geometry{{margin=1in}}

\\title{{SwarmCare Research Paper}}
\\author{{SwarmCare Research Team}}
\\date{{2025}}

\\begin{{document}}

\\maketitle

{latex}

\\end{{document}}"""

    output_file = output_dir / paper_file.with_suffix('.tex').name
    output_file.write_text(latex_template)
    return output_file


def main():
    """Main export function"""

    parser = argparse.ArgumentParser(description='Export research papers to multiple formats')
    parser.add_argument('--format', choices=['html', 'latex', 'all'], default='all',
                        help='Export format (default: all)')
    parser.add_argument('--paper', type=int, help='Export specific paper number (1-5)')
    parser.add_argument('--output', default='./exports', help='Output directory')

    args = parser.parse_args()

    deliverables_dir = Path(__file__).parent
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 80)
    print("EXPORTING RESEARCH PAPERS")
    print("=" * 80)
    print()
    print(f"Format: {args.format}")
    print(f"Output: {output_dir}")
    print()

    # Get paper files
    if args.paper:
        paper_files = list(deliverables_dir.glob(f"paper_{args.paper:02d}_*.md"))
    else:
        paper_files = list(deliverables_dir.glob("paper_*.md"))

    exported_count = 0

    for paper_file in sorted(paper_files):
        print(f"Exporting: {paper_file.name}")

        if args.format in ['html', 'all']:
            try:
                output_file = export_to_html(paper_file, output_dir)
                print(f"  ✅ HTML: {output_file.name}")
                exported_count += 1
            except ImportError:
                print(f"  ⚠️  HTML: markdown module not available (pip install markdown)")
            except Exception as e:
                print(f"  ❌ HTML: {e}")

        if args.format in ['latex', 'all']:
            try:
                output_file = export_to_latex(paper_file, output_dir)
                print(f"  ✅ LaTeX: {output_file.name}")
                exported_count += 1
            except Exception as e:
                print(f"  ❌ LaTeX: {e}")

        print()

    print("=" * 80)
    print(f"EXPORT COMPLETE: {exported_count} files generated")
    print("=" * 80)
    print()
    print(f"Output directory: {output_dir.absolute()}")
    print()

    # Note about PDF/DOCX
    if args.format == 'all' or args.format in ['pdf', 'docx']:
        print("Note: For PDF/DOCX export, use:")
        print("  - pandoc (recommended): pandoc input.md -o output.pdf")
        print("  - LaTeX: pdflatex file.tex")
        print()


if __name__ == "__main__":
    main()
