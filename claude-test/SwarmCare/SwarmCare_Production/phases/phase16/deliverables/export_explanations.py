#!/usr/bin/env python3
"""
Export Explanations Script
Exports explanations to various formats (JSON, HTML, PDF).
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any


class ExplanationExporter:
    """Exports explanation data to various formats."""

    def __init__(self):
        self.supported_formats = ['json', 'html', 'pdf']

    def export_to_json(self, data: Any, output_file: Path) -> None:
        """Export data to JSON format."""
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"✓ Exported to JSON: {output_file.absolute()}")

    def export_to_html(self, data: Any, output_file: Path) -> None:
        """Export data to HTML format."""
        html_content = self._generate_html(data)
        with open(output_file, 'w') as f:
            f.write(html_content)
        print(f"✓ Exported to HTML: {output_file.absolute()}")

    def export_to_pdf(self, data: Any, output_file: Path) -> None:
        """Export data to PDF format (requires reportlab or similar)."""
        try:
            # Try to use reportlab if available
            from reportlab.lib.pagesizes import letter
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
            from reportlab.lib.styles import getSampleStyleSheet
            from reportlab.lib.units import inch

            doc = SimpleDocTemplate(str(output_file), pagesize=letter)
            styles = getSampleStyleSheet()
            story = []

            # Title
            title = Paragraph("<b>SwarmCare Explanation Report</b>", styles['Title'])
            story.append(title)
            story.append(Spacer(1, 0.3 * inch))

            # Add content
            if isinstance(data, list):
                for i, item in enumerate(data):
                    story.append(Paragraph(f"<b>Explanation {i+1}</b>", styles['Heading2']))
                    story.append(Spacer(1, 0.1 * inch))

                    for key, value in item.items():
                        text = f"<b>{key}:</b> {self._format_value(value)}"
                        story.append(Paragraph(text, styles['Normal']))

                    story.append(Spacer(1, 0.2 * inch))
            else:
                for key, value in data.items():
                    text = f"<b>{key}:</b> {self._format_value(value)}"
                    story.append(Paragraph(text, styles['Normal']))

            # Build PDF
            doc.build(story)
            print(f"✓ Exported to PDF: {output_file.absolute()}")

        except ImportError:
            # Fallback: Create HTML and save as PDF
            print("⚠ Warning: reportlab not available, generating HTML instead of PDF")
            html_file = output_file.with_suffix('.html')
            self.export_to_html(data, html_file)
            print(f"  To convert to PDF, use: wkhtmltopdf {html_file} {output_file}")

    def _format_value(self, value: Any) -> str:
        """Format a value for display."""
        if isinstance(value, (list, dict)):
            return json.dumps(value, indent=2)
        return str(value)

    def _generate_html(self, data: Any) -> str:
        """Generate HTML content from explanation data."""
        html_parts = []

        # HTML header
        html_parts.append("""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>SwarmCare Explanation Report</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        h1 {
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }
        h2 {
            color: #34495e;
            margin-top: 30px;
        }
        .explanation-card {
            background: white;
            border-radius: 8px;
            padding: 20px;
            margin: 20px 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .field {
            margin: 10px 0;
        }
        .field-name {
            font-weight: bold;
            color: #2c3e50;
        }
        .field-value {
            margin-left: 20px;
            color: #555;
        }
        .json-block {
            background: #f8f8f8;
            border: 1px solid #ddd;
            border-radius: 4px;
            padding: 10px;
            margin: 10px 0;
            overflow-x: auto;
        }
        .timestamp {
            color: #7f8c8d;
            font-size: 0.9em;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 10px 0;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #3498db;
            color: white;
        }
        tr:nth-child(even) {
            background-color: #f2f2f2;
        }
    </style>
</head>
<body>
    <h1>SwarmCare Explanation Report</h1>
    <p class="timestamp">Generated: {timestamp}</p>
""".format(timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

        # Process data
        if isinstance(data, list):
            for i, item in enumerate(data):
                html_parts.append(f'<div class="explanation-card">')
                html_parts.append(f'<h2>Explanation {i+1}</h2>')
                html_parts.append(self._format_item_html(item))
                html_parts.append('</div>')
        elif isinstance(data, dict):
            html_parts.append('<div class="explanation-card">')
            html_parts.append(self._format_item_html(data))
            html_parts.append('</div>')

        # HTML footer
        html_parts.append("""
</body>
</html>
""")

        return '\n'.join(html_parts)

    def _format_item_html(self, item: Dict) -> str:
        """Format a single item as HTML."""
        html_parts = []

        for key, value in item.items():
            html_parts.append('<div class="field">')
            html_parts.append(f'<span class="field-name">{key}:</span>')

            if isinstance(value, dict):
                html_parts.append('<div class="json-block">')
                html_parts.append('<table>')
                for k, v in value.items():
                    html_parts.append(f'<tr><td>{k}</td><td>{v}</td></tr>')
                html_parts.append('</table>')
                html_parts.append('</div>')
            elif isinstance(value, list):
                html_parts.append('<div class="field-value">')
                html_parts.append('<ul>')
                for item in value:
                    html_parts.append(f'<li>{item}</li>')
                html_parts.append('</ul>')
                html_parts.append('</div>')
            else:
                html_parts.append(f'<span class="field-value">{value}</span>')

            html_parts.append('</div>')

        return '\n'.join(html_parts)


def main():
    parser = argparse.ArgumentParser(
        description="Export explanations to various formats",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --format json --input explanations.json --output export.json
  %(prog)s --format html --input shap_explanations.json --output report.html
  %(prog)s --format pdf --input all_explanations.json --output report.pdf
        """
    )

    parser.add_argument(
        '--format',
        type=str,
        required=True,
        choices=['json', 'html', 'pdf'],
        help='Output format (json, html, or pdf)'
    )

    parser.add_argument(
        '--input',
        type=str,
        required=True,
        help='Input JSON file containing explanations'
    )

    parser.add_argument(
        '--output',
        type=str,
        required=True,
        help='Output file path'
    )

    args = parser.parse_args()

    # Validate input file
    input_file = Path(args.input)
    if not input_file.exists():
        print(f"Error: Input file not found: {input_file}", file=sys.stderr)
        sys.exit(1)

    # Load input data
    try:
        with open(input_file, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in input file: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading input file: {e}", file=sys.stderr)
        sys.exit(1)

    # Create output directory if needed
    output_file = Path(args.output)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Export data
    exporter = ExplanationExporter()

    try:
        print(f"Exporting to {args.format.upper()} format...")

        if args.format == 'json':
            exporter.export_to_json(data, output_file)
        elif args.format == 'html':
            exporter.export_to_html(data, output_file)
        elif args.format == 'pdf':
            exporter.export_to_pdf(data, output_file)

        print(f"\n✓ Export completed successfully!")

    except Exception as e:
        print(f"\nError during export: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
