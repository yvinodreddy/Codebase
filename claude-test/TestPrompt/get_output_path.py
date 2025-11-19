#!/usr/bin/env python3
"""
Output Path Manager for TestPrompt ULTRATHINK System

Generates timestamped output file paths to prevent:
1. File overwriting in parallel execution
2. Loss of command history
3. System cleanup vulnerabilities

Returns: /home/user01/claude-test/TestPrompt/tmp/ultrathink_output_YYYYMMDD_HHMMSS_mmm.txt

Usage:
    # Default (single execution)
    OUTPUT_FILE=$(python3 get_output_path.py)

    # With track number (parallel execution)
    OUTPUT_FILE=$(python3 get_output_path.py --track 1)

Author: ULTRATHINK System
Date: 2025-11-19
Version: 1.0.0
"""

import os
import sys
import argparse
from datetime import datetime


def get_output_path(track_number=None):
    """
    Generate a timestamped output file path.

    Args:
        track_number (int, optional): Track number for parallel execution

    Returns:
        str: Full path to the output file

    Example:
        >>> get_output_path()
        '/home/user01/claude-test/TestPrompt/tmp/ultrathink_output_20251119_121705_816.txt'

        >>> get_output_path(track_number=1)
        '/home/user01/claude-test/TestPrompt/tmp/ultrathink_output_track1_20251119_121705_816.txt'
    """
    base_dir = "/home/user01/claude-test/TestPrompt/tmp"

    # Ensure directory exists
    os.makedirs(base_dir, exist_ok=True)

    # Generate timestamp: YYYYMMDD_HHMMSS_mmm (mmm = milliseconds)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]

    # Generate filename based on track number
    if track_number is not None:
        filename = f"ultrathink_output_track{track_number}_{timestamp}.txt"
    else:
        filename = f"ultrathink_output_{timestamp}.txt"

    # Return full path
    return os.path.join(base_dir, filename)


def main():
    """
    Main entry point for command-line usage.
    """
    parser = argparse.ArgumentParser(
        description='Generate timestamped output file path for TestPrompt ULTRATHINK system'
    )
    parser.add_argument(
        '--track',
        type=int,
        metavar='N',
        help='Track number for parallel execution (e.g., --track 1)'
    )

    args = parser.parse_args()

    # Generate and print the output path
    output_path = get_output_path(track_number=args.track)
    print(output_path)

    return 0


if __name__ == "__main__":
    sys.exit(main())
