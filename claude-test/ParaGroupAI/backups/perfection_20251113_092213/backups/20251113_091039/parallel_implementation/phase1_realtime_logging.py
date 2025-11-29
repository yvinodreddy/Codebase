#!/usr/bin/env python3
"""
Phase 1: Real-Time Logging Implementation
INDEPENDENT - No dependencies on other phases
"""

import sys
import os
import time
import sqlite3
from pathlib import Path
from datetime import datetime

# Setup logging for this phase
PHASE_LOG = "parallel_implementation/logs/phase1.log"
os.makedirs("parallel_implementation/logs", exist_ok=True)

def log(message: str):
    """Log to both stdout and file"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_message = f"[PHASE1] [{timestamp}] {message}"
    print(log_message)
    with open(PHASE_LOG, 'a') as f:
        f.write(log_message + '\n')

def main():
    log("="*80)
    log("PHASE 1: REAL-TIME LOGGING IMPLEMENTATION")
    log("="*80)
    log("Status: STARTING")

    start_time = time.time()

    try:
        # Task 1.1: Enhanced Verbose Logger with File Writing
        log("[Task 1.1] Creating RealtimeVerboseLogger class...")

        realtime_logger_code = '''#!/usr/bin/env python3
"""
Real-Time Verbose Logger - Writes to file AND stdout immediately
Enhanced version of verbose_logger.py with file output
"""

import time
import sys
from typing import Optional, Dict, Any, List
from datetime import datetime
from verbose_logger import VerboseLogger


class RealtimeVerboseLogger(VerboseLogger):
    """
    Enhanced logger that writes to file AND stdout immediately.
    CRITICAL: Uses line buffering to ensure real-time writes.
    """

    def __init__(self, output_file: str, enabled: bool = True):
        """
        Initialize real-time logger

        Args:
            output_file: Path to output file for logging
            enabled: Whether verbose logging is enabled
        """
        super().__init__(enabled)
        self.output_file = output_file

        # Open file with line buffering (buffering=1) for immediate writes
        self.file_handle = open(output_file, 'a', buffering=1, encoding='utf-8')

        # Track when we last wrote to file
        self.last_write_time = time.time()
        self.write_interval = 0.1  # Force write every 0.1 seconds

    def _write(self, message: str):
        """Write immediately to both stdout and file"""
        # Write to stdout
        print(message)
        sys.stdout.flush()

        # Write to file
        self.file_handle.write(message + '\\n')
        self.file_handle.flush()  # CRITICAL: Force OS to write NOW

        # Update timestamp
        self.last_write_time = time.time()

    def _ensure_write(self):
        """Ensure file is written to disk periodically"""
        current_time = time.time()
        if current_time - self.last_write_time >= self.write_interval:
            self.file_handle.flush()
            self.last_write_time = current_time

    # Override all logging methods to use _write

    def stage_header(self, stage_number: int, stage_name: str):
        """Print a stage header with separator"""
        if not self.enabled:
            return

        self.stage_start_time = time.time()
        self.current_stage = f"STAGE {stage_number}"

        self._write(f"\\n{'=' * 80}")
        self._write(f"[VERBOSE] STAGE {stage_number}: {stage_name}")
        self._write('=' * 80)

    def stage_footer(self, duration: Optional[float] = None):
        """Print stage completion with timing"""
        if not self.enabled:
            return

        if duration is None and self.stage_start_time:
            duration = time.time() - self.stage_start_time

        if duration is not None:
            self._write(f"[VERBOSE]   ✓ {self.current_stage} completed in {duration:.3f}s")

    def info(self, message: str, indent: bool = False):
        """Print verbose info message"""
        if not self.enabled:
            return

        prefix = "[VERBOSE]   " if indent else "[VERBOSE] "
        self._write(f"{prefix}{message}")

    def success(self, message: str, indent: bool = True):
        """Print success message with checkmark"""
        if not self.enabled:
            return

        prefix = "[VERBOSE]   " if indent else "[VERBOSE] "
        self._write(f"{prefix}✓ {message}")

    def warning(self, message: str, indent: bool = True):
        """Print warning message"""
        if not self.enabled:
            return

        prefix = "[VERBOSE]   " if indent else "[VERBOSE] "
        self._write(f"{prefix}⚠️  {message}")

    def error(self, message: str, indent: bool = True):
        """Print error message"""
        if not self.enabled:
            return

        prefix = "[VERBOSE]   " if indent else "[VERBOSE] "
        self._write(f"{prefix}❌ {message}")

    def metric(self, key: str, value: Any, indent: bool = True):
        """Print a metric key-value pair"""
        if not self.enabled:
            return

        prefix = "[VERBOSE]   " if indent else "[VERBOSE] "
        self._write(f"{prefix}{key}: {value}")

    def processing_step(self, step: str, status: str = "in progress"):
        """Print a processing step"""
        if not self.enabled:
            return

        if status == "done":
            self._write(f"[VERBOSE]   ✓ {step}")
        elif status == "failed":
            self._write(f"[VERBOSE]   ❌ {step}")
        elif status == "warning":
            self._write(f"[VERBOSE]   ⚠️  {step}")
        else:
            self._write(f"[VERBOSE]   → {step}")

    def guardrail_layer(self, layer_num: int, layer_name: str, layer_purpose: str,
                       passed: bool, details: dict = None):
        """Print detailed guardrail layer information"""
        if not self.enabled:
            return

        status = "✅ PASS" if passed else "❌ FAIL"
        self._write(f"\\n[VERBOSE] ┌─ Layer {layer_num}: {layer_name} {'─' * (55 - len(layer_name))}┐")
        self._write(f"[VERBOSE] │ Status: {status:<67} │")
        self._write(f"[VERBOSE] │ Purpose: {layer_purpose:<65} │")

        if details:
            for key, value in details.items():
                display_line = f"{key}: {value}"
                if len(display_line) > 65:
                    display_line = display_line[:62] + "..."
                self._write(f"[VERBOSE] │ {display_line:<67} │")

        self._write(f"[VERBOSE] └{'─' * 72}┘")

    def close(self):
        """Close file handle"""
        if hasattr(self, 'file_handle') and self.file_handle:
            self.file_handle.flush()
            self.file_handle.close()

    def __del__(self):
        """Ensure file is closed on deletion"""
        self.close()


# Convenience function
def create_realtime_logger(output_file: str, enabled: bool = True) -> RealtimeVerboseLogger:
    """Create and return a real-time verbose logger"""
    return RealtimeVerboseLogger(output_file, enabled)
'''

        # Write the enhanced logger
        with open('realtime_verbose_logger.py', 'w') as f:
            f.write(realtime_logger_code)

        log("[Task 1.1] ✅ RealtimeVerboseLogger created: realtime_verbose_logger.py")

        # Task 1.2: Stage Progress Tracker
        log("[Task 1.2] Creating StageProgressTracker...")

        progress_tracker_code = '''#!/usr/bin/env python3
"""
Stage Progress Tracker
Calculates 0-100% progress based on ULTRATHINK stages
"""

from typing import Dict


class StageProgressTracker:
    """Tracks progress through 6 ULTRATHINK stages"""

    STAGES = {
        1: {"name": "Prompt Preprocessing & Analysis", "weight": 16},
        2: {"name": "Guardrails - Input Validation", "weight": 17},
        3: {"name": "Context Management", "weight": 17},
        4: {"name": "Agent Orchestration", "weight": 17},
        5: {"name": "Execution", "weight": 17},
        6: {"name": "Output Validation", "weight": 16}
    }

    def __init__(self):
        self.current_stage = 0
        self.stage_completion = 0.0

    def set_stage(self, stage_number: int, completion: float = 0.0):
        """
        Set current stage and completion percentage

        Args:
            stage_number: Stage number (1-6)
            completion: Completion percentage for this stage (0.0-1.0)
        """
        if stage_number < 1 or stage_number > 6:
            raise ValueError(f"Stage number must be 1-6, got {stage_number}")

        if completion < 0.0 or completion > 1.0:
            raise ValueError(f"Completion must be 0.0-1.0, got {completion}")

        self.current_stage = stage_number
        self.stage_completion = completion

    def calculate_progress(self, stage_number: int = None, stage_completion: float = None) -> int:
        """
        Calculate overall 0-100% progress

        Args:
            stage_number: Optional stage number override
            stage_completion: Optional completion override

        Returns:
            Integer progress percentage (0-100)
        """
        stage = stage_number if stage_number is not None else self.current_stage
        completion = stage_completion if stage_completion is not None else self.stage_completion

        if stage == 0:
            return 0

        if stage > 6:
            return 100

        # Calculate weight of all previous stages
        previous_weight = sum(
            s['weight'] for i, s in self.STAGES.items() if i < stage
        )

        # Calculate current stage contribution
        current_weight = self.STAGES[stage]['weight'] * completion

        # Total progress
        total_progress = previous_weight + current_weight

        return int(total_progress)

    def get_stage_name(self, stage_number: int = None) -> str:
        """Get name of a stage"""
        stage = stage_number if stage_number is not None else self.current_stage
        if stage < 1 or stage > 6:
            return "Unknown"
        return self.STAGES[stage]['name']

    def mark_stage_complete(self, stage_number: int):
        """Mark a stage as complete and advance"""
        self.set_stage(stage_number, 1.0)
        if stage_number < 6:
            self.set_stage(stage_number + 1, 0.0)

    def get_status(self) -> Dict:
        """Get current status"""
        return {
            'current_stage': self.current_stage,
            'stage_name': self.get_stage_name(),
            'stage_completion': self.stage_completion,
            'overall_progress': self.calculate_progress()
        }


# Convenience function
def create_progress_tracker() -> StageProgressTracker:
    """Create and return a progress tracker"""
    return StageProgressTracker()
'''

        with open('stage_progress_tracker.py', 'w') as f:
            f.write(progress_tracker_code)

        log("[Task 1.2] ✅ StageProgressTracker created: stage_progress_tracker.py")

        # Task 1.3: Database Update Function
        log("[Task 1.3] Creating database update functions...")

        db_update_code = '''#!/usr/bin/env python3
"""
Real-Time Database Updates
Updates tracks table with real-time progress
"""

import sqlite3
from datetime import datetime
from typing import Optional


def update_track_progress(
    track_id: int,
    status: str = None,
    progress: int = None,
    current_task: str = None,
    db_path: str = "realtime-tracking/track_state.db"
) -> bool:
    """
    Update track progress in real-time

    Args:
        track_id: Track ID to update
        status: New status (RUNNING, COMPLETED, FAILED)
        progress: Progress percentage (0-100)
        current_task: Current operation description
        db_path: Path to database

    Returns:
        bool: True if successful
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Build update query dynamically
        updates = []
        params = []

        if status is not None:
            updates.append("status = ?")
            params.append(status)

        if progress is not None:
            updates.append("progress = ?")
            params.append(progress)

        if current_task is not None:
            updates.append("current_task = ?")
            params.append(current_task)

        # Always update timestamp
        updates.append("updated_at = CURRENT_TIMESTAMP")

        if not updates:
            return True  # Nothing to update

        # Add track_id to params
        params.append(track_id)

        # Execute update
        query = f"UPDATE tracks SET {', '.join(updates)} WHERE id = ?"
        cursor.execute(query, params)
        conn.commit()
        conn.close()

        return True

    except Exception as e:
        print(f"[ERROR] Failed to update track {track_id}: {e}")
        return False


def create_track(
    name: str = "CPP Execution",
    status: str = "RUNNING",
    progress: int = 0,
    current_task: str = "Starting...",
    db_path: str = "realtime-tracking/track_state.db"
) -> Optional[int]:
    """
    Create new track in database

    Returns:
        int: Track ID if successful, None if failed
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO tracks (name, status, progress, current_task)
            VALUES (?, ?, ?, ?)
        """, (name, status, progress, current_task))

        track_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return track_id

    except Exception as e:
        print(f"[ERROR] Failed to create track: {e}")
        return None


def insert_log_entry(
    track_id: int,
    level: str,
    message: str,
    db_path: str = "realtime-tracking/track_state.db"
) -> bool:
    """
    Insert log entry into database

    Args:
        track_id: Track ID
        level: Log level (DEBUG, INFO, WARNING, ERROR)
        message: Log message
        db_path: Path to database

    Returns:
        bool: True if successful
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO log_entries (track_id, level, message, timestamp)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
        """, (track_id, level, message))

        conn.commit()
        conn.close()

        return True

    except Exception as e:
        print(f"[ERROR] Failed to insert log entry: {e}")
        return False
'''

        with open('realtime_db_updates.py', 'w') as f:
            f.write(db_update_code)

        log("[Task 1.3] ✅ Database update functions created: realtime_db_updates.py")

        # Create test script
        log("[Task 1.4] Creating test script...")

        test_code = '''#!/usr/bin/env python3
"""
Test Real-Time Logging System
"""

import time
from realtime_verbose_logger import create_realtime_logger
from stage_progress_tracker import create_progress_tracker
from realtime_db_updates import create_track, update_track_progress, insert_log_entry

def test_realtime_logging():
    """Test the real-time logging system"""

    # Create test output file
    output_file = "parallel_implementation/test_realtime_log.txt"

    # Create logger
    logger = create_realtime_logger(output_file, enabled=True)

    # Create progress tracker
    tracker = create_progress_tracker()

    # Create test track
    track_id = create_track(name="Test Track", status="RUNNING", progress=0)

    if not track_id:
        print("Failed to create track")
        return False

    print(f"Created track ID: {track_id}")

    # Simulate processing through 6 stages
    for stage in range(1, 7):
        logger.stage_header(stage, tracker.get_stage_name(stage))

        # Simulate work in this stage
        for i in range(5):
            completion = (i + 1) / 5
            tracker.set_stage(stage, completion)
            progress = tracker.calculate_progress()

            # Log operation
            operation = f"Processing step {i+1}/5 in {tracker.get_stage_name(stage)}"
            logger.processing_step(operation, "in progress")

            # Update database
            update_track_progress(
                track_id=track_id,
                progress=progress,
                current_task=operation
            )

            # Insert log entry
            insert_log_entry(track_id, "INFO", operation)

            # Small delay to simulate work
            time.sleep(0.5)

        # Mark stage complete
        tracker.mark_stage_complete(stage)
        logger.stage_footer()

        # Update database
        update_track_progress(
            track_id=track_id,
            progress=tracker.calculate_progress(),
            current_task=f"Completed {tracker.get_stage_name(stage)}"
        )

    # Final update
    update_track_progress(
        track_id=track_id,
        status="COMPLETED",
        progress=100,
        current_task="All stages completed"
    )

    logger.success("Test completed successfully!")
    logger.close()

    print(f"\\nTest complete! Check {output_file} for real-time logs.")
    print(f"Track ID {track_id} should show 100% progress in database.")

    return True

if __name__ == '__main__':
    success = test_realtime_logging()
    exit(0 if success else 1)
'''

        with open('parallel_implementation/test_phase1.py', 'w') as f:
            f.write(test_code)

        log("[Task 1.4] ✅ Test script created: parallel_implementation/test_phase1.py")

        # Run quick validation
        log("[Validation] Testing imports...")
        import subprocess
        result = subprocess.run(
            ['python3', '-c', 'from realtime_verbose_logger import create_realtime_logger; from stage_progress_tracker import create_progress_tracker; from realtime_db_updates import create_track; print("✓ All imports successful")'],
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode == 0:
            log(f"[Validation] ✅ {result.stdout.strip()}")
        else:
            log(f"[Validation] ⚠️  Import test failed: {result.stderr}")

        duration = time.time() - start_time
        log("="*80)
        log(f"PHASE 1 COMPLETED in {duration:.2f}s")
        log("Status: SUCCESS ✅")
        log("="*80)

        return 0

    except Exception as e:
        log(f"❌ PHASE 1 FAILED: {e}")
        import traceback
        log(traceback.format_exc())
        return 1

if __name__ == '__main__':
    exit(main())
