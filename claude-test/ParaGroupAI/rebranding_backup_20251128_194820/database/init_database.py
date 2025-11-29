#!/usr/bin/env python3
"""
Database Initialization Script

Creates and initializes the SQLite database using Python's sqlite3 module.
This avoids dependency on the sqlite3 command-line tool.

Author: ULTRATHINK System
Date: 2025-11-19
Version: 1.0.0
"""

import sqlite3
import sys
from pathlib import Path


def init_database(db_path: str, schema_path: str) -> dict:
    """
    Initialize database with schema.

    Args:
        db_path: Path to database file
        schema_path: Path to schema SQL file

    Returns:
        Dictionary with status information
    """
    db_path = Path(db_path)
    schema_path = Path(schema_path)

    # Check if schema file exists
    if not schema_path.exists():
        return {
            'success': False,
            'error': f'Schema file not found: {schema_path}'
        }

    # Read schema SQL
    try:
        with open(schema_path, 'r') as f:
            schema_sql = f.read()
    except Exception as e:
        return {
            'success': False,
            'error': f'Failed to read schema file: {e}'
        }

    # Create database and execute schema
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Execute schema (may contain multiple statements)
        cursor.executescript(schema_sql)

        conn.commit()

        # Count tables
        cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table'")
        table_count = cursor.fetchone()[0]

        # Get table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tables = [row[0] for row in cursor.fetchall()]

        conn.close()

        return {
            'success': True,
            'table_count': table_count,
            'tables': tables,
            'db_path': str(db_path)
        }

    except Exception as e:
        return {
            'success': False,
            'error': f'Failed to initialize database: {e}'
        }


def main():
    """Main entry point for script."""
    if len(sys.argv) != 3:
        print("Usage: python3 init_database.py <db_path> <schema_path>")
        sys.exit(1)

    db_path = sys.argv[1]
    schema_path = sys.argv[2]

    result = init_database(db_path, schema_path)

    if result['success']:
        print(f"✓ Database initialized successfully")
        print(f"  Database: {result['db_path']}")
        print(f"  Tables: {result['table_count']}")
        for table in result['tables']:
            print(f"    - {table}")
        sys.exit(0)
    else:
        print(f"✗ Database initialization failed")
        print(f"  Error: {result['error']}")
        sys.exit(1)


if __name__ == "__main__":
    main()
