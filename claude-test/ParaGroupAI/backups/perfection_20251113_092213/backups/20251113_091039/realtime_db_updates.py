#!/usr/bin/env python3
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
