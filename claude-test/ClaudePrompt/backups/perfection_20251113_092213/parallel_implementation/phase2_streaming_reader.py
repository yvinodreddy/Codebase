#!/usr/bin/env python3
"""Phase 2: Streaming Log Reader - INDEPENDENT"""
import time
import os
from datetime import datetime

PHASE_LOG = "parallel_implementation/logs/phase2.log"

def log(msg):
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_msg = f"[PHASE2] [{ts}] {msg}"
    print(log_msg)
    with open(PHASE_LOG, 'a') as f:
        f.write(log_msg + '\n')

log("="*80)
log("PHASE 2: STREAMING LOG READER")
log("="*80)
log("Creating real-time log monitoring system...")

# Create realtime_log_monitor.py
monitor_code = '''#!/usr/bin/env python3
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
'''

with open('realtime_log_monitor.py', 'w') as f:
    f.write(monitor_code)

log("✅ Created realtime_log_monitor.py")
log("PHASE 2 COMPLETED - SUCCESS ✅")
exit(0)
