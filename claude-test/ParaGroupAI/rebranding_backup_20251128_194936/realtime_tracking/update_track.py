#!/usr/bin/env python3
"""
Database update utility for track scripts
Replaces sqlite3 command-line tool with Python sqlite3 module
"""

import sqlite3
import sys
from pathlib import Path

DB_PATH = "realtime-tracking/track_state.db"


def update_progress(track_id, progress, current_task, timestamp):
    """Update track progress in database"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE tracks
            SET progress = ?,
                current_task = ?,
                last_update = ?
            WHERE id = ?
        """, (progress, current_task, timestamp, track_id))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error updating progress: {e}", file=sys.stderr)
        return False


def update_status(track_id, status, timestamp):
    """Update track status in database"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE tracks
            SET status = ?,
                last_update = ?
            WHERE id = ?
        """, (status, timestamp, track_id))

        if status == "RUNNING":
            cursor.execute("""
                UPDATE tracks
                SET started_at = ?
                WHERE id = ?
            """, (timestamp, track_id))
        elif status == "COMPLETED":
            cursor.execute("""
                UPDATE tracks
                SET completed_at = ?
                WHERE id = ?
            """, (timestamp, track_id))

        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error updating status: {e}", file=sys.stderr)
        return False


def log_entry(track_id, timestamp, level, message):
    """Insert log entry into database"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO log_entries (track_id, timestamp, level, message)
            VALUES (?, ?, ?, ?)
        """, (track_id, timestamp, level, message))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error logging entry: {e}", file=sys.stderr)
        return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: update_track.py <command> <args...>", file=sys.stderr)
        sys.exit(1)

    command = sys.argv[1]

    if command == "progress":
        # update_track.py progress <track_id> <progress> <current_task> <timestamp>
        if len(sys.argv) != 6:
            print("Usage: update_track.py progress <track_id> <progress> <task> <timestamp>", file=sys.stderr)
            sys.exit(1)
        track_id = int(sys.argv[2])
        progress = int(sys.argv[3])
        current_task = sys.argv[4]
        timestamp = sys.argv[5]
        success = update_progress(track_id, progress, current_task, timestamp)
        sys.exit(0 if success else 1)

    elif command == "status":
        # update_track.py status <track_id> <status> <timestamp>
        if len(sys.argv) != 5:
            print("Usage: update_track.py status <track_id> <status> <timestamp>", file=sys.stderr)
            sys.exit(1)
        track_id = int(sys.argv[2])
        status = sys.argv[3]
        timestamp = sys.argv[4]
        success = update_status(track_id, status, timestamp)
        sys.exit(0 if success else 1)

    elif command == "log":
        # update_track.py log <track_id> <timestamp> <level> <message>
        if len(sys.argv) != 6:
            print("Usage: update_track.py log <track_id> <timestamp> <level> <message>", file=sys.stderr)
            sys.exit(1)
        track_id = int(sys.argv[2])
        timestamp = sys.argv[3]
        level = sys.argv[4]
        message = sys.argv[5]
        success = log_entry(track_id, timestamp, level, message)
        sys.exit(0 if success else 1)

    else:
        print(f"Unknown command: {command}", file=sys.stderr)
        sys.exit(1)
