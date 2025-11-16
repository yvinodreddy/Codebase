#!/usr/bin/env python3
"""
Real-Time Log Monitor - tail -f style streaming
"""
import time
import os
from typing import Callable, Optional

class RealtimeLogMonitor:
    """Monitors log file and streams new content"""

    def __init__(self, log_file: str, callback: Callable[[str], None]):
        self.log_file = log_file
        self.callback = callback
        self.last_position = 0
        self.running = False

    def start_monitoring(self):
        """Start monitoring file for new content"""
        self.running = True

        # Wait for file to exist
        while not os.path.exists(self.log_file) and self.running:
            time.sleep(1)

        if not self.running:
            return

        while self.running:
            try:
                with open(self.log_file, 'r') as f:
                    f.seek(self.last_position)
                    new_lines = f.readlines()
                    self.last_position = f.tell()

                    for line in new_lines:
                        self.callback(line.rstrip())

                time.sleep(2)  # Check every 2 seconds

            except Exception as e:
                print(f"Monitor error: {e}")
                time.sleep(2)

    def stop_monitoring(self):
        """Stop monitoring"""
        self.running = False
