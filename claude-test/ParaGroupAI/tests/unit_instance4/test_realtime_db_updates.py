#!/usr/bin/env python3
"""Comprehensive test suite for realtime_db_updates.py - Target: 90%+ coverage"""
import pytest
import sqlite3
import tempfile
import os
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from realtime_db_updates import update_track_progress, create_track, insert_log_entry

class TestRealtimeDbUpdates:
    def setup_method(self):
        self.temp_db = tempfile.mktemp(suffix='.db')
        self._create_test_db()
    
    def teardown_method(self):
        if os.path.exists(self.temp_db):
            os.unlink(self.temp_db)
    
    def _create_test_db(self):
        conn = sqlite3.connect(self.temp_db)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE tracks (
                id INTEGER PRIMARY KEY,
                name TEXT,
                status TEXT,
                progress INTEGER,
                current_task TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("""
            CREATE TABLE log_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                track_id INTEGER,
                level TEXT,
                message TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("INSERT INTO tracks (id, name, status, progress) VALUES (1, 'Test', 'RUNNING', 0)")
        conn.commit()
        conn.close()
    
    def test_update_track_progress_status(self):
        result = update_track_progress(1, status="COMPLETED", db_path=self.temp_db)
        assert result == True
        conn = sqlite3.connect(self.temp_db)
        cursor = conn.cursor()
        cursor.execute("SELECT status FROM tracks WHERE id=1")
        status = cursor.fetchone()[0]
        conn.close()
        assert status == "COMPLETED"
    
    def test_update_track_progress_all_fields(self):
        result = update_track_progress(
            1, status="RUNNING", progress=50, 
            current_task="Processing", db_path=self.temp_db
        )
        assert result == True
    
    def test_update_track_progress_no_updates(self):
        result = update_track_progress(1, db_path=self.temp_db)
        assert result == True
    
    def test_update_track_progress_error(self):
        result = update_track_progress(1, status="INVALID", db_path="/invalid/path.db")
        assert result == False
    
    def test_create_track(self):
        track_id = create_track(
            name="New Track", status="PENDING", 
            progress=0, current_task="Starting", db_path=self.temp_db
        )
        assert track_id is not None
        assert track_id > 0
    
    def test_create_track_error(self):
        track_id = create_track(db_path="/invalid/path.db")
        assert track_id is None
    
    def test_insert_log_entry(self):
        result = insert_log_entry(1, "INFO", "Test message", db_path=self.temp_db)
        assert result == True
    
    def test_insert_log_entry_error(self):
        result = insert_log_entry(1, "INFO", "Test", db_path="/invalid/path.db")
        assert result == False

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
