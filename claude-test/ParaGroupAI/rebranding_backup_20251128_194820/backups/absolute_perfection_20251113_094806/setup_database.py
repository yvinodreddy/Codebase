#!/usr/bin/env python3
"""
Database setup script for ULTRATHINK 10-Track Execution System
Creates SQLite database with schema for real-time tracking
"""

import sqlite3
import sys
from pathlib import Path

DB_PATH = "track_state.db"

def create_database():
    """Create database with full schema for track state management"""

    print(f"Creating database: {DB_PATH}")

    # Remove existing database
    db_file = Path(DB_PATH)
    if db_file.exists():
        print(f"Removing existing database...")
        db_file.unlink()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Track state table
    print("Creating tracks table...")
    cursor.execute("""
        CREATE TABLE tracks (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            status TEXT CHECK(status IN ('PENDING', 'RUNNING', 'COMPLETED', 'FAILED', 'PAUSED')) DEFAULT 'PENDING',
            progress INTEGER DEFAULT 0 CHECK(progress >= 0 AND progress <= 100),
            started_at TIMESTAMP,
            completed_at TIMESTAMP,
            duration_seconds INTEGER,
            last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            current_task TEXT,
            log_file TEXT,
            error_message TEXT,
            retry_count INTEGER DEFAULT 0
        )
    """)

    # Task state table
    print("Creating tasks table...")
    cursor.execute("""
        CREATE TABLE tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            track_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            status TEXT CHECK(status IN ('PENDING', 'RUNNING', 'COMPLETED', 'FAILED', 'SKIPPED')) DEFAULT 'PENDING',
            progress INTEGER DEFAULT 0 CHECK(progress >= 0 AND progress <= 100),
            started_at TIMESTAMP,
            completed_at TIMESTAMP,
            error_message TEXT,
            FOREIGN KEY (track_id) REFERENCES tracks(id) ON DELETE CASCADE
        )
    """)

    # Log entries table
    print("Creating log_entries table...")
    cursor.execute("""
        CREATE TABLE log_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            track_id INTEGER NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            level TEXT CHECK(level IN ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')) DEFAULT 'INFO',
            message TEXT,
            metadata TEXT,
            FOREIGN KEY (track_id) REFERENCES tracks(id) ON DELETE CASCADE
        )
    """)

    # Metrics table
    print("Creating metrics table...")
    cursor.execute("""
        CREATE TABLE metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            track_id INTEGER,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            metric_name TEXT NOT NULL,
            metric_value REAL NOT NULL,
            FOREIGN KEY (track_id) REFERENCES tracks(id) ON DELETE CASCADE
        )
    """)

    # Create indexes for performance
    print("Creating indexes...")
    cursor.execute("CREATE INDEX idx_tracks_status ON tracks(status)")
    cursor.execute("CREATE INDEX idx_tasks_track_id ON tasks(track_id)")
    cursor.execute("CREATE INDEX idx_tasks_status ON tasks(status)")
    cursor.execute("CREATE INDEX idx_logs_track_id ON log_entries(track_id)")
    cursor.execute("CREATE INDEX idx_logs_timestamp ON log_entries(timestamp)")
    cursor.execute("CREATE INDEX idx_metrics_track_id ON metrics(track_id)")

    # Initialize 10 tracks
    print("Initializing 10 tracks...")
    tracks = [
        (1, "Core Infrastructure & Database", "SQLite schema, FastAPI boilerplate", "logs/track1.log"),
        (2, "WebSocket Real-Time Layer", "Socket.IO integration, broadcast system", "logs/track2.log"),
        (3, "Log File Watching System", "Inotify-based file watcher", "logs/track3.log"),
        (4, "React Dashboard Layout", "Main UI structure with routing", "logs/track4.log"),
        (5, "React Real-Time Components", "Progress bars, live log feeds", "logs/track5.log"),
        (6, "State Management & Data Layer", "Database CRUD operations", "logs/track6.log"),
        (7, "Track Execution Scripts 1-5", "Bash scripts for tracks 1-5", "logs/track7.log"),
        (8, "Track Execution Scripts 6-10", "Bash scripts for tracks 6-10", "logs/track8.log"),
        (9, "Testing & Validation Suite", "Unit, integration, E2E tests", "logs/track9.log"),
        (10, "Master Orchestration System", "One-command launch script", "logs/track10.log"),
    ]

    for track_id, name, description, log_file in tracks:
        cursor.execute("""
            INSERT INTO tracks (id, name, description, status, progress, log_file)
            VALUES (?, ?, ?, 'PENDING', 0, ?)
        """, (track_id, name, description, log_file))

    conn.commit()
    conn.close()

    print(f"\n✅ Database created successfully: {DB_PATH}")
    print(f"   - 10 tracks initialized")
    print(f"   - All tables and indexes created")
    print(f"   - Ready for real-time tracking\n")

if __name__ == "__main__":
    try:
        create_database()
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error creating database: {e}", file=sys.stderr)
        sys.exit(1)
