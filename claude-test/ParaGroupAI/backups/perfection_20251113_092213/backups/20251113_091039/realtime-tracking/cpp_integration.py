#!/usr/bin/env python3
"""
CPP Integration Module for Real-Time Dashboard
Integrates cpp command execution with real-time tracking system

ZERO BREAKING CHANGES:
- New file in realtime-tracking/ directory
- Hooks into cpp execution without modifying cpp script
- Optional feature that can be disabled
"""

import sqlite3
import sys
import json
from datetime import datetime
from pathlib import Path
import re

DB_PATH = "realtime-tracking/track_state.db"

class CPPTracker:
    """Tracks cpp command execution in real-time"""

    def __init__(self, prompt_text, output_file):
        self.prompt_text = prompt_text
        self.output_file = output_file
        self.track_id = None
        self.conn = None

    def initialize_tracking(self):
        """Initialize a new track for this cpp execution"""
        try:
            self.conn = sqlite3.connect(DB_PATH)
            cursor = self.conn.cursor()

            # Create a new track entry
            cursor.execute("""
                INSERT INTO tracks (name, description, status, progress, log_file, current_task)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                f"CPP Execution",
                self.prompt_text[:200],  # First 200 chars of prompt
                'RUNNING',
                0,
                self.output_file,
                'Initializing ULTRATHINK processing...'
            ))

            self.track_id = cursor.lastrowid
            self.conn.commit()

            self.log_entry('INFO', f'Started cpp execution tracking (Track ID: {self.track_id})')

            return self.track_id

        except Exception as e:
            print(f"Warning: Could not initialize tracking: {e}", file=sys.stderr)
            return None

    def log_entry(self, level, message):
        """Log an entry to the database"""
        if not self.conn or not self.track_id:
            return

        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO log_entries (track_id, level, message)
                VALUES (?, ?, ?)
            """, (self.track_id, level, message))
            self.conn.commit()
        except Exception as e:
            print(f"Warning: Could not log entry: {e}", file=sys.stderr)

    def update_progress(self, progress, current_task):
        """Update track progress"""
        if not self.conn or not self.track_id:
            return

        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                UPDATE tracks
                SET progress = ?, current_task = ?, last_update = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (progress, current_task, self.track_id))
            self.conn.commit()
        except Exception as e:
            print(f"Warning: Could not update progress: {e}", file=sys.stderr)

    def update_status(self, status):
        """Update track status"""
        if not self.conn or not self.track_id:
            return

        try:
            cursor = self.conn.cursor()

            if status == 'COMPLETED':
                cursor.execute("""
                    UPDATE tracks
                    SET status = ?, completed_at = CURRENT_TIMESTAMP, progress = 100
                    WHERE id = ?
                """, (status, self.track_id))
            else:
                cursor.execute("""
                    UPDATE tracks
                    SET status = ?
                    WHERE id = ?
                """, (status, self.track_id))

            self.conn.commit()
            self.log_entry('INFO', f'Status changed to: {status}')

        except Exception as e:
            print(f"Warning: Could not update status: {e}", file=sys.stderr)

    def parse_ultrathink_output(self, output_text):
        """Parse ULTRATHINK output to extract stages and progress"""
        stages = []

        # Extract STAGE markers
        stage_pattern = r'\[VERBOSE\] STAGE (\d+):\s*(.+)'
        for match in re.finditer(stage_pattern, output_text):
            stage_num = int(match.group(1))
            stage_name = match.group(2).strip()
            stages.append((stage_num, stage_name))

        return stages

    def monitor_output_file(self):
        """Monitor the output file and update progress based on content"""
        if not Path(self.output_file).exists():
            return

        try:
            with open(self.output_file, 'r') as f:
                content = f.read()

            # Parse stages from output
            stages = self.parse_ultrathink_output(content)

            # Update progress based on stages completed
            if stages:
                last_stage = stages[-1][0]
                progress = min(int((last_stage / 6) * 100), 95)  # 6 stages total, max 95% until complete
                stage_name = stages[-1][1]

                self.update_progress(progress, f'Stage {last_stage}: {stage_name}')

        except Exception as e:
            print(f"Warning: Could not monitor output file: {e}", file=sys.stderr)

    def finalize_tracking(self, success=True):
        """Finalize tracking when cpp execution completes"""
        if not self.conn or not self.track_id:
            return

        try:
            if success:
                self.update_status('COMPLETED')
                self.update_progress(100, 'Processing complete')
                self.log_entry('INFO', 'CPP execution completed successfully')
            else:
                self.update_status('FAILED')
                self.log_entry('ERROR', 'CPP execution failed')

            self.conn.close()

        except Exception as e:
            print(f"Warning: Could not finalize tracking: {e}", file=sys.stderr)


def track_cpp_execution(prompt_text, output_file):
    """
    Track a cpp execution in real-time

    Args:
        prompt_text: The prompt being processed
        output_file: The output file path

    Returns:
        CPPTracker instance
    """
    tracker = CPPTracker(prompt_text, output_file)
    tracker.initialize_tracking()
    return tracker


if __name__ == "__main__":
    # Test the tracker
    if len(sys.argv) < 3:
        print("Usage: python3 cpp_integration.py <prompt> <output_file>")
        sys.exit(1)

    prompt = sys.argv[1]
    output = sys.argv[2]

    tracker = track_cpp_execution(prompt, output)

    # Simulate progress
    import time
    for i in range(1, 7):
        time.sleep(1)
        tracker.update_progress(i * 15, f'Stage {i} processing...')
        tracker.log_entry('INFO', f'Completed stage {i}')

    tracker.finalize_tracking(success=True)
    print(f"Tracking test complete. Track ID: {tracker.track_id}")
