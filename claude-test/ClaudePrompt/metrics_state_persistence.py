#!/usr/bin/env python3
"""
metrics_state_persistence.py - State Persistence Layer for Statusline Metrics

PRODUCTION-READY IMPLEMENTATION (2025-11-16)
============================================

PURPOSE:
- Persist last known good metrics so they remain visible after request completion
- Provide state lifecycle management (active, completing, idle)
- Enable smooth transitions between request phases
- Solve the "disappearing values" problem

FEATURES:
- ✅ Atomic file writes for crash safety
- ✅ Timestamp tracking for state freshness
- ✅ Lifecycle state machine (ACTIVE → COMPLETING → IDLE)
- ✅ Graceful degradation if state file corrupted
- ✅ Thread-safe operations
- ✅ Zero breaking changes to existing code

STATE LIFECYCLE:
1. ACTIVE: Request in progress, metrics updating every 300ms
2. COMPLETING: Request finishing, freeze current values
3. IDLE: Request complete, display last frozen values until next request

This ensures user can see final metrics even after request completes.
"""

import json
import os
import time
from datetime import datetime
from typing import Dict, Optional
from pathlib import Path
from enum import Enum
import fcntl


class RequestState(Enum):
    """Request lifecycle states."""
    ACTIVE = "active"          # Request in progress
    COMPLETING = "completing"  # Request finishing
    IDLE = "idle"             # No active request


class MetricsStatePersistence:
    """
    Manages persistent state for statusline metrics across request lifecycle.

    Solves the problem where metrics disappear after request completion by:
    1. Storing last known good values during ACTIVE requests
    2. Freezing values when request enters COMPLETING state
    3. Persisting frozen values through IDLE state
    4. Only updating when new request starts (ACTIVE)
    """

    def __init__(self, state_file: Optional[str] = None):
        """
        Initialize state persistence manager.

        Args:
            state_file: Path to state file (default: tmp/statusline_state.json)
        """
        if state_file is None:
            state_file = "/home/user01/claude-test/ClaudePrompt/tmp/statusline_state.json"

        self.state_file = Path(state_file)
        self.state_file.parent.mkdir(parents=True, exist_ok=True)

        # Default state
        self.default_state = {
            'lifecycle_state': RequestState.IDLE.value,
            'agents': 'N/A',
            'tokens_used': 0,
            'tokens_total': 200000,
            'tokens_pct': 0.0,
            'tokens_display': '0k/200k',
            'confidence': '--',
            'status': '🟢 OPTIMAL',
            'executing': False,
            'last_update': None,
            'last_active_update': None,  # Timestamp of last ACTIVE update
            'frozen_at': None,            # Timestamp when values were frozen
            'request_count': 0            # Total requests processed
        }

    def load_state(self) -> Dict:
        """
        Load current state from file with failsafe fallback.

        Returns:
            State dictionary (defaults if file missing/corrupt)
        """
        if not self.state_file.exists():
            return self.default_state.copy()

        try:
            with open(self.state_file, 'r') as f:
                # Acquire shared lock for reading
                fcntl.flock(f.fileno(), fcntl.LOCK_SH)
                try:
                    state = json.load(f)

                    # Validate state has required fields
                    for key in self.default_state:
                        if key not in state:
                            state[key] = self.default_state[key]

                    return state
                finally:
                    fcntl.flock(f.fileno(), fcntl.LOCK_UN)
        except Exception as e:
            # Corrupted file - return defaults
            return self.default_state.copy()

    def save_state(self, state: Dict) -> bool:
        """
        Save state to file atomically (crash-safe).

        Args:
            state: State dictionary to save

        Returns:
            True if successful, False otherwise
        """
        try:
            # Add timestamp
            state['last_update'] = datetime.now().isoformat()

            # Write to temporary file first (atomic)
            temp_file = self.state_file.with_suffix('.tmp')

            with open(temp_file, 'w') as f:
                # Acquire exclusive lock for writing
                fcntl.flock(f.fileno(), fcntl.LOCK_EX)
                try:
                    json.dump(state, f, indent=2)
                    f.flush()
                    os.fsync(f.fileno())
                finally:
                    fcntl.flock(f.fileno(), fcntl.LOCK_UN)

            # Atomic rename
            temp_file.replace(self.state_file)
            return True
        except Exception as e:
            return False

    def update_active_metrics(self, metrics: Dict) -> bool:
        """
        Update metrics during ACTIVE request.

        This is called repeatedly (every 300ms) while request is in progress.
        It updates the current values and marks state as ACTIVE.

        Args:
            metrics: New metrics to store

        Returns:
            True if successful
        """
        state = self.load_state()

        # Update lifecycle state
        state['lifecycle_state'] = RequestState.ACTIVE.value
        state['executing'] = True
        state['last_active_update'] = datetime.now().isoformat()

        # Update metrics
        state['agents'] = metrics.get('agents', state['agents'])
        state['tokens_used'] = metrics.get('tokens_used', state['tokens_used'])
        state['tokens_total'] = metrics.get('tokens_total', state['tokens_total'])
        state['tokens_pct'] = metrics.get('tokens_pct', state['tokens_pct'])
        state['tokens_display'] = metrics.get('tokens_display', state['tokens_display'])
        state['confidence'] = metrics.get('confidence', state['confidence'])
        state['status'] = metrics.get('status', state['status'])

        return self.save_state(state)

    def freeze_metrics(self) -> bool:
        """
        Freeze current metrics when request is COMPLETING.

        This is called when request finishes. It transitions state from
        ACTIVE → COMPLETING and freezes current values.

        Returns:
            True if successful
        """
        state = self.load_state()

        # Only freeze if currently ACTIVE
        if state['lifecycle_state'] == RequestState.ACTIVE.value:
            state['lifecycle_state'] = RequestState.COMPLETING.value
            state['executing'] = False
            state['frozen_at'] = datetime.now().isoformat()
            state['request_count'] = state.get('request_count', 0) + 1

            return self.save_state(state)

        return False

    def mark_idle(self) -> bool:
        """
        Mark state as IDLE after request completion.

        This transitions state from COMPLETING → IDLE.
        Frozen values remain visible until next ACTIVE request.

        Returns:
            True if successful
        """
        state = self.load_state()

        # Only mark idle if currently COMPLETING
        if state['lifecycle_state'] == RequestState.COMPLETING.value:
            state['lifecycle_state'] = RequestState.IDLE.value
            state['executing'] = False

            return self.save_state(state)

        return False

    def get_display_metrics(self, current_metrics: Optional[Dict] = None) -> Dict:
        """
        Get metrics to display in statusline based on lifecycle state.

        DECISION LOGIC:
        - ACTIVE: Use current_metrics if provided, else persisted state
        - COMPLETING: Use persisted frozen values
        - IDLE: Use persisted frozen values

        This ensures:
        - Real-time updates during active requests
        - Frozen values persist after completion
        - User always sees meaningful data (never blank)

        Args:
            current_metrics: Optional current metrics from live sources

        Returns:
            Metrics dictionary to display
        """
        state = self.load_state()
        lifecycle = RequestState(state['lifecycle_state'])

        if lifecycle == RequestState.ACTIVE:
            # During ACTIVE request, use current metrics if available
            if current_metrics:
                # Update persistent state with current values
                self.update_active_metrics(current_metrics)
                return current_metrics
            else:
                # Fallback to persisted state
                return {
                    'agents': state['agents'],
                    'tokens_used': state['tokens_used'],
                    'tokens_total': state['tokens_total'],
                    'tokens_pct': state['tokens_pct'],
                    'tokens_display': state['tokens_display'],
                    'confidence': state['confidence'],
                    'status': state['status'],
                    'executing': state['executing']
                }

        elif lifecycle in [RequestState.COMPLETING, RequestState.IDLE]:
            # After request completes, show frozen values
            return {
                'agents': state['agents'],
                'tokens_used': state['tokens_used'],
                'tokens_total': state['tokens_total'],
                'tokens_pct': state['tokens_pct'],
                'tokens_display': state['tokens_display'],
                'confidence': state['confidence'],
                'status': state['status'],
                'executing': False  # Always false when not active
            }

        else:
            # Unknown state - return defaults
            return self.default_state.copy()

    def detect_new_request(self, current_executing: bool) -> bool:
        """
        Detect if a new request has started.

        This automatically transitions from IDLE → ACTIVE when new request begins.

        Args:
            current_executing: Is a request currently executing?

        Returns:
            True if new request detected
        """
        state = self.load_state()
        lifecycle = RequestState(state['lifecycle_state'])

        # If currently IDLE but execution detected, new request started
        if lifecycle == RequestState.IDLE and current_executing:
            state['lifecycle_state'] = RequestState.ACTIVE.value
            state['executing'] = True
            self.save_state(state)
            return True

        return False

    def get_state_summary(self) -> Dict:
        """
        Get summary of current state for debugging.

        Returns:
            State summary dictionary
        """
        state = self.load_state()

        return {
            'lifecycle_state': state['lifecycle_state'],
            'executing': state['executing'],
            'request_count': state['request_count'],
            'last_update': state['last_update'],
            'last_active_update': state['last_active_update'],
            'frozen_at': state['frozen_at'],
            'current_metrics': {
                'agents': state['agents'],
                'tokens': state['tokens_display'],
                'confidence': state['confidence'],
                'status': state['status']
            }
        }


def main():
    """CLI interface for testing."""
    import argparse

    parser = argparse.ArgumentParser(description='Metrics State Persistence Manager')
    parser.add_argument('--update', action='store_true', help='Update with current metrics (ACTIVE)')
    parser.add_argument('--freeze', action='store_true', help='Freeze current metrics (COMPLETING)')
    parser.add_argument('--idle', action='store_true', help='Mark as IDLE')
    parser.add_argument('--get', action='store_true', help='Get display metrics')
    parser.add_argument('--summary', action='store_true', help='Get state summary')
    parser.add_argument('--json', action='store_true', help='Output as JSON')

    # Metric values for --update
    parser.add_argument('--agents', type=str, help='Agent count')
    parser.add_argument('--tokens-used', type=int, help='Tokens used')
    parser.add_argument('--tokens-total', type=int, default=200000, help='Total tokens')
    parser.add_argument('--confidence', type=str, help='Confidence score')

    args = parser.parse_args()

    manager = MetricsStatePersistence()

    if args.update:
        # Calculate percentage
        tokens_pct = (args.tokens_used / args.tokens_total * 100) if args.tokens_used else 0.0
        tokens_used_k = int(args.tokens_used / 1000) if args.tokens_used else 0
        tokens_total_k = int(args.tokens_total / 1000)
        tokens_display = f"{tokens_used_k}k/{tokens_total_k}k"

        metrics = {
            'agents': args.agents or 'N/A',
            'tokens_used': args.tokens_used or 0,
            'tokens_total': args.tokens_total,
            'tokens_pct': tokens_pct,
            'tokens_display': tokens_display,
            'confidence': args.confidence or '--',
            'status': '🟢 ACTIVE'
        }

        success = manager.update_active_metrics(metrics)
        print(json.dumps({'status': 'updated' if success else 'failed'}))

    elif args.freeze:
        success = manager.freeze_metrics()
        print(json.dumps({'status': 'frozen' if success else 'failed'}))

    elif args.idle:
        success = manager.mark_idle()
        print(json.dumps({'status': 'idle' if success else 'failed'}))

    elif args.get:
        metrics = manager.get_display_metrics()
        print(json.dumps(metrics, indent=2))

    elif args.summary:
        summary = manager.get_state_summary()
        print(json.dumps(summary, indent=2))

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
