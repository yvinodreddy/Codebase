#!/usr/bin/env python3
"""Comprehensive test suite for setup_database.py - Target: 90%+ coverage"""
import pytest
import sqlite3
import tempfile
import os
from pathlib import Path
from unittest.mock import patch
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

class TestSetupDatabase:
    def test_database_creation(self):
        # Import here to avoid module-level DB creation
        with patch('setup_database.DB_PATH', tempfile.mktemp(suffix='.db')):
            from setup_database import create_database, DB_PATH
            
            # Create database
            create_database()
            
            # Verify database exists
            assert Path(DB_PATH).exists()
            
            # Verify tables exist
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            # Check tracks table
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='tracks'")
            assert cursor.fetchone() is not None
            
            # Check tasks table
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='tasks'")
            assert cursor.fetchone() is not None
            
            # Check log_entries table
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='log_entries'")
            assert cursor.fetchone() is not None
            
            # Check metrics table
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='metrics'")
            assert cursor.fetchone() is not None
            
            # Check that 10 tracks were initialized
            cursor.execute("SELECT COUNT(*) FROM tracks")
            count = cursor.fetchone()[0]
            assert count == 10
            
            conn.close()
            
            # Cleanup
            if Path(DB_PATH).exists():
                Path(DB_PATH).unlink()
    
    def test_database_recreation(self):
        with patch('setup_database.DB_PATH', tempfile.mktemp(suffix='.db')):
            from setup_database import create_database, DB_PATH
            
            # Create initial database
            create_database()
            
            # Add custom data
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tracks (id, name, status) VALUES (100, 'Custom', 'PENDING')")
            conn.commit()
            conn.close()
            
            # Recreate database (should remove existing)
            create_database()
            
            # Check custom data is gone
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tracks WHERE id=100")
            assert cursor.fetchone() is None
            conn.close()
            
            # Cleanup
            if Path(DB_PATH).exists():
                Path(DB_PATH).unlink()

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
