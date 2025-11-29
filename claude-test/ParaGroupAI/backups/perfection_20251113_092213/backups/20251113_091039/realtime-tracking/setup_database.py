#!/usr/bin/env python3
"""
Database setup script for ULTRATHINK 10-Track Real-Time Execution System
Creates SQLite database with schema for real-time tracking

ZERO BREAKING CHANGES:
- New file in new directory (realtime-tracking/)
- Does not modify existing code
- Optional feature - only used when real-time tracking is enabled
"""

import sqlite3
import sys
from pathlib import Path
from datetime import datetime

DB_PATH = "realtime-tracking/track_state.db"

def create_database():
    """Create database with full schema for track state management"""

    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Creating database: {DB_PATH}")

    # Create directory if it doesn't exist
    db_dir = Path(DB_PATH).parent
    db_dir.mkdir(parents=True, exist_ok=True)

    # Remove existing database
    db_file = Path(DB_PATH)
    if db_file.exists():
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Removing existing database...")
        db_file.unlink()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Enable WAL mode for better concurrency
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.execute("PRAGMA synchronous=NORMAL")
    cursor.execute("PRAGMA cache_size=10000")
    cursor.execute("PRAGMA temp_store=MEMORY")

    # Track state table
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Creating tracks table...")
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
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Creating tasks table...")
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
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Creating log_entries table...")
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
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Creating metrics table...")
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
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Creating indexes...")
    cursor.execute("CREATE INDEX idx_tracks_status ON tracks(status)")
    cursor.execute("CREATE INDEX idx_tasks_track_id ON tasks(track_id)")
    cursor.execute("CREATE INDEX idx_tasks_status ON tasks(status)")
    cursor.execute("CREATE INDEX idx_logs_track_id ON log_entries(track_id)")
    cursor.execute("CREATE INDEX idx_logs_timestamp ON log_entries(timestamp)")
    cursor.execute("CREATE INDEX idx_metrics_track_id ON metrics(track_id)")

    # Initialize 10 tracks
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Initializing 10 tracks...")
    tracks = [
        (1, "Core Infrastructure & Database", "SQLite schema, FastAPI boilerplate", "logs/track1.log"),
        (2, "WebSocket Real-Time Layer", "Socket.IO integration, broadcast system", "logs/track2.log"),
        (3, "Log File Watching System", "Inotify-based file watcher", "logs/track3.log"),
        (4, "Web Dashboard UI", "HTML/JS real-time dashboard", "logs/track4.log"),
        (5, "Real-Time Progress Bars", "Live progress tracking components", "logs/track5.log"),
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

    # Verify database
    cursor.execute("SELECT COUNT(*) FROM tracks")
    track_count = cursor.fetchone()[0]

    cursor.execute("PRAGMA integrity_check")
    integrity = cursor.fetchone()[0]

    conn.close()

    print(f"\n{'='*80}")
    print(f"✅ Database created successfully: {DB_PATH}")
    print(f"{'='*80}")
    print(f"   - {track_count} tracks initialized")
    print(f"   - All tables and indexes created")
    print(f"   - Database integrity: {integrity}")
    print(f"   - WAL mode enabled for concurrency")
    print(f"   - Ready for real-time tracking")
    print(f"{'='*80}\n")

    return True

if __name__ == "__main__":
    try:
        success = create_database()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n{'='*80}", file=sys.stderr)
        print(f"❌ Error creating database: {e}", file=sys.stderr)
        print(f"{'='*80}\n", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
