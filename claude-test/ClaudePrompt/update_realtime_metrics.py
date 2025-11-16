#!/usr/bin/env python3
"""
update_realtime_metrics.py - Real-Time Metrics Updater

Updates the real-time metrics JSON file that's displayed in the status line.
This runs asynchronously during cpp execution to provide live metrics visibility.

Usage:
    python3 update_realtime_metrics.py --agents "8/30" --context-pct 15.5 --confidence 99.2 --executing
    python3 update_realtime_metrics.py --reset
"""

import json
import os
import sys
import argparse
from pathlib import Path
from datetime import datetime

METRICS_FILE = Path("/home/user01/claude-test/ClaudePrompt/tmp/realtime_metrics.json")

def update_metrics(agents=None, context_pct=None, confidence=None, executing=False):
    """Update the real-time metrics file."""

    # Ensure tmp directory exists
    METRICS_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Load existing metrics if file exists
    metrics = {}
    if METRICS_FILE.exists():
        try:
            with open(METRICS_FILE, 'r') as f:
                metrics = json.load(f)
        except (json.JSONDecodeError, IOError):
            metrics = {}

    # Update metrics with new values
    if agents is not None:
        metrics['agents'] = agents
    if context_pct is not None:
        metrics['context_pct'] = float(context_pct)
    if confidence is not None:
        metrics['confidence'] = float(confidence)

    metrics['executing'] = executing
    metrics['last_update'] = datetime.now().isoformat()

    # Write atomically to prevent race conditions
    temp_file = METRICS_FILE.with_suffix('.tmp')
    try:
        with open(temp_file, 'w') as f:
            json.dump(metrics, f, indent=2)
        temp_file.replace(METRICS_FILE)
        return True
    except IOError as e:
        print(f"Error writing metrics: {e}", file=sys.stderr)
        return False

def reset_metrics():
    """Reset metrics to default state."""
    metrics = {
        'agents': 'N/A',
        'context_pct': 0.0,
        'confidence': 0.0,
        'executing': False,
        'last_update': datetime.now().isoformat()
    }

    METRICS_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(METRICS_FILE, 'w') as f:
        json.dump(metrics, f, indent=2)

    return True

def main():
    parser = argparse.ArgumentParser(
        description='Update real-time metrics for status line display'
    )

    parser.add_argument('--agents', help='Agent allocation (e.g., "8/30")')
    parser.add_argument('--context-pct', type=float, help='Context usage percentage')
    parser.add_argument('--confidence', type=float, help='Confidence score')
    parser.add_argument('--executing', action='store_true', help='Mark as currently executing')
    parser.add_argument('--reset', action='store_true', help='Reset metrics to defaults')

    args = parser.parse_args()

    if args.reset:
        success = reset_metrics()
        if success:
            print("✓ Metrics reset successfully")
        else:
            print("✗ Failed to reset metrics", file=sys.stderr)
            sys.exit(1)
    else:
        success = update_metrics(
            agents=args.agents,
            context_pct=args.context_pct,
            confidence=args.confidence,
            executing=args.executing
        )

        if success:
            print("✓ Metrics updated successfully")
        else:
            print("✗ Failed to update metrics", file=sys.stderr)
            sys.exit(1)

if __name__ == '__main__':
    main()
