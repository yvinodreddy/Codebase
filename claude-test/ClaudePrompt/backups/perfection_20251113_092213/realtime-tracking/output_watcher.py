#!/usr/bin/env python3
"""
Output File Watcher
Monitors tmp/ directory for new ULTRATHINK output files and parses them in real-time
"""

import os
import time
import sqlite3
import json
from pathlib import Path
from typing import Dict, Set
from datetime import datetime
from ultrathink_parser import parse_ultrathink_output


class OutputWatcher:
    """Watch for new output files and parse them"""

    def __init__(self, watch_dir: str = "tmp", db_path: str = "realtime-tracking/track_state.db"):
        self.watch_dir = watch_dir
        self.db_path = db_path
        self.known_files: Set[str] = set()
        self.file_track_map: Dict[str, int] = {}

    def start(self):
        """Start watching for new files"""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Output watcher started")
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Watching directory: {self.watch_dir}")

        # Initial scan
        self._scan_existing_files()

        # Continuous monitoring
        while True:
            try:
                self._check_for_new_files()
                self._update_existing_files()
                time.sleep(2)  # Check every 2 seconds
            except KeyboardInterrupt:
                print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Output watcher stopped")
                break
            except Exception as e:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Error: {e}")
                time.sleep(2)

    def _scan_existing_files(self):
        """Scan for existing output files"""
        if not os.path.exists(self.watch_dir):
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Watch directory not found: {self.watch_dir}")
            return

        for file in Path(self.watch_dir).glob("cppultrathink_output_*.txt"):
            if file.name not in self.known_files:
                self.known_files.add(file.name)
                self._process_file(str(file))

    def _check_for_new_files(self):
        """Check for new output files"""
        if not os.path.exists(self.watch_dir):
            return

        for file in Path(self.watch_dir).glob("cppultrathink_output_*.txt"):
            if file.name not in self.known_files:
                self.known_files.add(file.name)
                print(f"[{datetime.now().strftime('%H:%M:%S')}] New file detected: {file.name}")
                self._process_file(str(file))

    def _update_existing_files(self):
        """Update data for files that are still being written"""
        for file_name in list(self.known_files):
            file_path = os.path.join(self.watch_dir, file_name)
            if os.path.exists(file_path):
                # Check if file is still being written (modified recently)
                mtime = os.path.getmtime(file_path)
                if time.time() - mtime < 10:  # Modified in last 10 seconds
                    self._process_file(file_path, update=True)

    def _process_file(self, file_path: str, update: bool = False):
        """Process an output file and update database"""
        try:
            # Parse the file
            parsed_data = parse_ultrathink_output(file_path)

            if not parsed_data:
                return

            # Get or create track ID for this file
            track_id = self._get_track_id_for_file(file_path)

            if not track_id:
                return

            # Update database with parsed data
            self._update_database(track_id, file_path, parsed_data)

            if not update:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Processed: Track {track_id}")

        except Exception as e:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Error processing {file_path}: {e}")

    def _get_track_id_for_file(self, file_path: str) -> int:
        """Get track ID for a file (create new track if needed)"""
        # Check if we already have a mapping
        if file_path in self.file_track_map:
            return self.file_track_map[file_path]

        # Query database to find track with this output file
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Get the most recent track (assuming newest output = newest track)
        cursor.execute("""
            SELECT id FROM tracks
            ORDER BY id DESC
            LIMIT 1
        """)
        result = cursor.fetchone()

        if result:
            track_id = result[0]
            self.file_track_map[file_path] = track_id
            conn.close()
            return track_id

        conn.close()
        return None

    def _update_database(self, track_id: int, file_path: str, parsed_data: Dict):
        """Update ultrathink_details table with parsed data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Prepare JSON strings
        agents_json = json.dumps(parsed_data.get('agents', []))
        guardrails_json = json.dumps(parsed_data.get('guardrails', []))
        metrics_json = json.dumps(parsed_data.get('metrics', {}))
        enhanced_prompt = parsed_data.get('enhanced_prompt', '')[:5000]  # Limit size

        # Insert or update ultrathink_details
        cursor.execute('''
            INSERT OR REPLACE INTO ultrathink_details (
                track_id, current_stage, current_stage_number, total_stages,
                agents_allocated, agents_data, guardrails_status,
                verbose_output_path, enhanced_prompt, metrics_data, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        ''', (
            track_id,
            parsed_data.get('current_stage', 'Processing'),
            parsed_data.get('current_stage_number', 0),
            6,  # Total stages
            parsed_data.get('metrics', {}).get('agents_allocated', 0),
            agents_json,
            guardrails_json,
            file_path,
            enhanced_prompt,
            metrics_json
        ))

        conn.commit()
        conn.close()


def main():
    """Main entry point"""
    watcher = OutputWatcher()
    watcher.start()


if __name__ == '__main__':
    main()
