#!/usr/bin/env python3
"""
Answer-to-File System for ULTRATHINK

This script captures Claude Code's answer and appends it to the output file.
User can then read the complete file (prompt + answer) from top to bottom.
"""

import sys
import os

def append_answer_section(output_file: str, answer: str):
    """
    Append the answer section to the output file with clear visual markers.

    Args:
        output_file: Path to the output file (e.g., /tmp/cppultrathink_output.txt)
        answer: The actual answer text from Claude Code
    """
    with open(output_file, 'a') as f:
        f.write("\n\n")
        f.write("=" * 80 + "\n")
        f.write("🎯 CLAUDE CODE'S ANSWER (SCROLL DOWN TO SEE THIS)\n")
        f.write("=" * 80 + "\n")
        f.write("\n")
        f.write("⬇️" * 40 + "\n")
        f.write("⬇️" + " " * 78 + "⬇️\n")
        f.write("⬇️" + " " * 20 + "THE ANSWER STARTS HERE" + " " * 36 + "⬇️\n")
        f.write("⬇️" + " " * 78 + "⬇️\n")
        f.write("⬇️" * 40 + "\n")
        f.write("\n")
        f.write(answer)
        f.write("\n\n")
        f.write("⬆️" * 40 + "\n")
        f.write("⬆️" + " " * 78 + "⬆️\n")
        f.write("⬆️" + " " * 23 + "THE ANSWER ENDS HERE" + " " * 35 + "⬆️\n")
        f.write("⬆️" + " " * 78 + "⬆️\n")
        f.write("⬆️" * 40 + "\n")
        f.write("\n")
        f.write("=" * 80 + "\n")
        f.write("✅ You can now read this file from top to bottom!\n")
        f.write("=" * 80 + "\n")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: answer_to_file.py <output_file> <answer_text>")
        sys.exit(1)

    output_file = sys.argv[1]
    answer = sys.argv[2]

    append_answer_section(output_file, answer)
    print(f"✅ Answer appended to {output_file}")
