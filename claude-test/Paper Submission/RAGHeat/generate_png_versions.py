#!/usr/bin/env python3
"""
Generate PNG versions of elite visualizations for preview
PDFs remain the primary publication-ready format
"""

import subprocess
import os

print("Converting PDFs to high-resolution PNGs for preview...")
print("="*70)

pdf_files = [
    'paper_elite_baseline_weights.pdf',
    'paper_elite_regime_graph.pdf',
    'paper_elite_heat_propagation.pdf',
    'paper_elite_complete_graph.pdf',
]

for pdf_file in pdf_files:
    png_file = pdf_file.replace('.pdf', '.png')

    # Use pdftoppm for high-quality conversion (600 DPI)
    try:
        subprocess.run([
            'pdftoppm', '-png', '-r', '300', '-singlefile',
            pdf_file, png_file.replace('.png', '')
        ], check=True, capture_output=True)

        file_size = os.path.getsize(png_file) / 1024  # KB
        print(f"✅ {png_file} ({file_size:.0f} KB)")

    except subprocess.CalledProcessError:
        print(f"⚠️  Could not convert {pdf_file} (pdftoppm not available)")
        print("   PDFs are the primary format - PNGs are optional for preview only")
    except FileNotFoundError:
        print(f"⚠️  pdftoppm not installed - skipping PNG conversion")
        print("   PDFs are vector format and ready for publication")
        break

print("="*70)
print("✅ PDFs are publication-ready (vector, editable, scalable)")
print("   PNGs are for preview only - use PDFs for submissions")
