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
    """
    Update the real-time metrics file.

    ENHANCED (2025-11-16): Now preserves comprehensive metrics from PostToolUse hook.
    Only updates specified fields, preserves all other comprehensive fields.
    """

    # Ensure tmp directory exists
    METRICS_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Load existing metrics if file exists (PRESERVE ALL EXISTING FIELDS)
    metrics = {}
    if METRICS_FILE.exists():
        try:
            with open(METRICS_FILE, 'r') as f:
                metrics = json.load(f)
        except (json.JSONDecodeError, IOError):
            metrics = {}

    # Update ONLY the specified fields (preserve everything else)
    # NOTE: agents from cppm is in format "8/30" (used/total)
    # We should NOT overwrite agents_total from comprehensive_metrics_updater
    if agents is not None:
        # If agents is in format "X/Y", extract just X for agents field
        if isinstance(agents, str) and '/' in agents:
            agent_parts = agents.split('/')
            metrics['agents'] = agent_parts[0].strip()  # Current/active agents
            # DO NOT overwrite agents_total if it exists
            if 'agents_total' not in metrics:
                metrics['agents_total'] = agent_parts[0].strip()  # Fallback
        else:
            metrics['agents'] = agents

    if context_pct is not None:
        metrics['context_pct'] = float(context_pct)
        # Also update tokens_pct if not present
        if 'tokens_pct' not in metrics:
            metrics['tokens_pct'] = float(context_pct)

    if confidence is not None:
        metrics['confidence'] = float(confidence)

    metrics['executing'] = executing
    metrics['last_update'] = datetime.now().isoformat()

    # Preserve comprehensive fields if they exist:
    # - agents_total, agents_active, agents_completed, agents_background
    # - tokens_used, tokens_total, tokens_display
    # - background_tasks_count, background_tasks
    # - agent_counts, status
    # These are already in metrics dict and won't be overwritten

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
    """
    Reset metrics to default state.

    ENHANCED (2025-11-16): Preserves comprehensive metrics from PostToolUse hook.
    Only resets legacy cppm fields, keeps all comprehensive tracking intact.
    """
    METRICS_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Load existing metrics to preserve comprehensive fields
    existing_metrics = {}
    if METRICS_FILE.exists():
        try:
            with open(METRICS_FILE, 'r') as f:
                existing_metrics = json.load(f)
        except (json.JSONDecodeError, IOError):
            existing_metrics = {}

    # Start with existing metrics (preserves comprehensive fields)
    metrics = existing_metrics.copy()

    # Only reset the legacy cppm fields
    metrics.update({
        'context_pct': 0.0,  # Legacy field
        'executing': False,
        'last_update': datetime.now().isoformat()
    })

    # Preserve these comprehensive fields if they exist:
    # - agents, agents_total, agents_active, agents_completed, agents_background
    # - tokens_used, tokens_total, tokens_pct, tokens_display
    # - confidence, status
    # - background_tasks_count, background_tasks
    # - agent_counts
    # All already preserved by using existing_metrics.copy()

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
