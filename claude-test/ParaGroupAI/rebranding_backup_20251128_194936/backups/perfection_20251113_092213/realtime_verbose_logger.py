#!/usr/bin/env python3
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
        self.file_handle.write(message + '\n')
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

        self._write(f"\n{'=' * 80}")
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
        self._write(f"\n[VERBOSE] ┌─ Layer {layer_num}: {layer_name} {'─' * (55 - len(layer_name))}┐")
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
