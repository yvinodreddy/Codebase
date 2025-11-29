#!/usr/bin/env python3
"""
Convert HTML Career Success Roadmap to PDF
"""

import subprocess
import sys
import os

def convert_html_to_pdf_chromium():
    """Convert HTML to PDF using Chromium headless"""
    html_file = "/home/user01/claude-test/ClaudePrompt/CAREER_SUCCESS_ROADMAP.html"
    pdf_file = "/home/user01/claude-test/ClaudePrompt/CAREER_SUCCESS_ROADMAP.pdf"

    # Try chromium-browser first
    chromium_commands = [
        "chromium-browser",
        "chromium",
        "google-chrome",
        "google-chrome-stable"
    ]

    for cmd in chromium_commands:
        try:
            result = subprocess.run(
                [cmd, "--headless", "--disable-gpu", "--print-to-pdf=" + pdf_file, html_file],
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0 or os.path.exists(pdf_file):
                print(f"✅ PDF created successfully: {pdf_file}")
                print(f"   Used: {cmd}")
                return True
        except (FileNotFoundError, subprocess.TimeoutExpired):
            continue

    return False

def print_manual_instructions():
    """Print instructions for manual PDF conversion"""
    print("\n" + "="*80)
    print("📄 HTML REPORT CREATED SUCCESSFULLY!")
    print("="*80)
    print("\nLocation: /home/user01/claude-test/ClaudePrompt/CAREER_SUCCESS_ROADMAP.html")
    print("\n🔥 TO CONVERT TO PDF (Choose ONE method):")
    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("METHOD 1: Using Browser (EASIEST)")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("1. Open the HTML file in Chrome/Firefox/Edge:")
    print("   file:///home/user01/claude-test/ClaudePrompt/CAREER_SUCCESS_ROADMAP.html")
    print("\n2. Press Ctrl+P (or Cmd+P on Mac)")
    print("\n3. Select 'Save as PDF' as destination")
    print("\n4. Settings:")
    print("   • Layout: Portrait")
    print("   • Paper size: Letter or A4")
    print("   • Margins: Default")
    print("   • Options: ✓ Background graphics")
    print("\n5. Click 'Save' → Choose location → Save as PDF")

    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("METHOD 2: Using Command Line (If available)")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("\nIf wkhtmltopdf is installed:")
    print("   wkhtmltopdf CAREER_SUCCESS_ROADMAP.html CAREER_SUCCESS_ROADMAP.pdf")

    print("\nIf chromium is installed:")
    print("   chromium --headless --disable-gpu --print-to-pdf=CAREER_SUCCESS_ROADMAP.pdf CAREER_SUCCESS_ROADMAP.html")

    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("METHOD 3: Online Converter")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("\n1. Upload HTML file to: https://www.html2pdf.com")
    print("2. Click 'Convert to PDF'")
    print("3. Download the generated PDF")

    print("\n" + "="*80)
    print("📋 REPORT FEATURES:")
    print("="*80)
    print("✓ Visual timeline (6-12 month roadmap)")
    print("✓ Color-coded sections for easy navigation")
    print("✓ SMARTER mnemonic for success formula")
    print("✓ Interactive decision flowchart")
    print("✓ Financial calculation worksheet")
    print("✓ Sample interview responses")
    print("✓ H4 EAD visa advantages highlighted")
    print("✓ Action items with checkboxes")
    print("✓ 60-75% success probability analysis")
    print("✓ Professional design - memorable & actionable")
    print("\n" + "="*80)
    print("💡 TIP: Print to PDF and review weekly to stay on track!")
    print("="*80 + "\n")

if __name__ == "__main__":
    print("Attempting to convert HTML to PDF...")

    if not convert_html_to_pdf_chromium():
        print("\n⚠️  Automatic PDF conversion not available (no chromium/chrome found)")
        print_manual_instructions()
    else:
        print("\n✅ PDF conversion successful!")
        print("\n📄 Files created:")
        print("   • HTML: /home/user01/claude-test/ClaudePrompt/CAREER_SUCCESS_ROADMAP.html")
        print("   • PDF:  /home/user01/claude-test/ClaudePrompt/CAREER_SUCCESS_ROADMAP.pdf")
        print("\n💡 You can now send the PDF file to your friend!")
