#!/usr/bin/env python3
"""
Output Path Generator for ULTRATHINK ClaudePrompt

Generates timestamped output file paths for parallel execution.
This ensures each cpp execution gets a unique output file.

Usage:
    python3 get_output_path.py                    # Returns timestamped path
    python3 get_output_path.py --track 1          # Returns path for Track 1
    python3 get_output_path.py --legacy           # Returns legacy /tmp/ path
"""

import sys
import os
from datetime import datetime
from pathlib import Path

# Get the ClaudePrompt directory
SCRIPT_DIR = Path(__file__).parent
TMP_DIR = SCRIPT_DIR / "tmp"

def get_timestamped_path(track=None):
    """
    Generate a timestamped output file path.

    Args:
        track: Optional track number (1-5) for parallel execution

    Returns:
        str: Full path to output file
    """
    # Create timestamp: YYYYMMDD_HHMMSS
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Add microseconds for true uniqueness
    microseconds = datetime.now().strftime("%f")[:3]  # First 3 digits

    # Build filename
    if track:
        filename = f"cppultrathink_output_track{track}_{timestamp}_{microseconds}.txt"
    else:
        filename = f"cppultrathink_output_{timestamp}_{microseconds}.txt"

    # Full path
    output_path = TMP_DIR / filename

    return str(output_path)

def get_legacy_path():
    """
    Get the legacy /tmp/ path for backward compatibility.

    Returns:
        str: /tmp/cppultrathink_output.txt
    """
    return "/tmp/cppultrathink_output.txt"

def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate output file path for cpp command"
    )
    parser.add_argument(
        "--track",
        type=int,
        choices=[1, 2, 3, 4, 5],
        help="Track number for parallel execution (1-5)"
    )
    parser.add_argument(
        "--legacy",
        action="store_true",
        help="Use legacy /tmp/ path for backward compatibility"
    )

    args = parser.parse_args()

    # Ensure tmp directory exists
    TMP_DIR.mkdir(exist_ok=True)

    # Generate path
    if args.legacy:
        path = get_legacy_path()
    else:
        path = get_timestamped_path(track=args.track)

    # Output path (for shell scripts to capture)
    print(path)

    return 0

if __name__ == "__main__":
    sys.exit(main())
