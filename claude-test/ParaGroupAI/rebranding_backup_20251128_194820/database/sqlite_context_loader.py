#!/usr/bin/env python3
"""
SQLite Context Loader for Database-First Architecture

This module provides context loading using SQLite as the backend database.
Perfect for development, testing, and single-machine deployments.
Zero configuration - just works!

Author: ULTRATHINK System
Date: 2025-11-19
Version: 1.0.0
"""

import sqlite3
import json
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
from pathlib import Path
import threading

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SQLiteContextLoader:
    """
    SQLite-based context loader with priority-based organization.

    Features:
    - Zero configuration (no database server needed)
    - File-based storage (single .db file)
    - ACID compliant (crash-safe)
    - Thread-safe operations
    - Identical API to PostgreSQL version

    Example:
        >>> loader = SQLiteContextLoader(
        ...     db_path="ultrathink_context.db"
        ... )
        >>> result = loader.load_context_for_instance(
        ...     instance_id="inst_001",
        ...     project_id="proj_001",
        ...     phase_id=1
        ... )
        >>> print(f"Loaded {len(result['critical_context'])} critical items")
    """

    def __init__(self, db_path: str = "ultrathink_context.db"):
        """
        Initialize SQLiteContextLoader.

        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = Path(db_path)
        self._local = threading.local()

        # Ensure database directory exists
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        # Initialize database
        self._initialize_database()

        logger.info(f"✅ SQLite database initialized: {self.db_path}")

    def _get_connection(self) -> sqlite3.Connection:
        """Get thread-local database connection."""
        if not hasattr(self._local, 'conn') or self._local.conn is None:
            self._local.conn = sqlite3.connect(
                str(self.db_path),
                check_same_thread=False,
                timeout=30.0
            )
            self._local.conn.row_factory = sqlite3.Row
            # Enable foreign keys
            self._local.conn.execute("PRAGMA foreign_keys = ON")
            # Enable WAL mode for better concurrency
            self._local.conn.execute("PRAGMA journal_mode = WAL")
        return self._local.conn

    def _initialize_database(self):
        """Initialize database schema if not exists."""
        schema_file = Path(__file__).parent / "schema_sqlite.sql"

        if not schema_file.exists():
            logger.warning(f"⚠️  Schema file not found: {schema_file}")
            return

        # Check if database is already initialized
        conn = self._get_connection()
        cursor = conn.cursor()

        # Check if projects table exists
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='projects'"
        )
        if cursor.fetchone():
            logger.info("✅ Database already initialized")
            return

        # Read and execute schema
        logger.info("🔄 Initializing database schema...")
        with open(schema_file, 'r') as f:
            schema_sql = f.read()

        # Execute schema (split by semicolons)
        for statement in schema_sql.split(';'):
            if statement.strip():
                try:
                    cursor.execute(statement)
                except sqlite3.Error as e:
                    logger.debug(f"Schema statement error (may be safe to ignore): {e}")

        conn.commit()
        logger.info("✅ Database schema initialized")

    def load_context_for_instance(
        self,
        instance_id: str,
        project_id: str,
        phase_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Load full context for an instance.

        Args:
            instance_id: Unique instance identifier
            project_id: Project identifier
            phase_id: Optional phase identifier

        Returns:
            Dict with instance info and CRITICAL context
        """
        logger.info(f"🔄 Loading context for instance {instance_id} (project: {project_id})")

        # Load CRITICAL context
        start_time = datetime.now()
        critical_context = self._load_priority('CRITICAL', project_id, phase_id)
        elapsed_ms = (datetime.now() - start_time).total_seconds() * 1000

        logger.info(f"✅ CRITICAL context loaded: {len(critical_context)} items in {elapsed_ms:.1f}ms")

        # Register instance in DB
        self._register_instance(instance_id, project_id, phase_id)

        # Return immediately with CRITICAL context
        return {
            'instance_id': instance_id,
            'project_id': project_id,
            'phase_id': phase_id,
            'critical_context': critical_context,
            'status': 'ready',
            'load_time_ms': elapsed_ms
        }

    def _load_priority(
        self,
        priority: str,
        project_id: str,
        phase_id: Optional[int]
    ) -> List[Dict[str, Any]]:
        """
        Load context for specific priority level.

        Args:
            priority: Priority level (CRITICAL, HIGH, MEDIUM, LOW)
            project_id: Project identifier
            phase_id: Optional phase identifier

        Returns:
            List of context snapshots
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        query = """
            SELECT snapshot_id, content_type, priority, token_count, content, metadata, created_at
            FROM context_snapshots
            WHERE project_id = ?
              AND priority = ?
              AND (phase_id = ? OR phase_id IS NULL)
            ORDER BY sequence_number ASC
        """
        cursor.execute(query, (project_id, priority, phase_id))

        results = []
        for row in cursor.fetchall():
            results.append({
                'snapshot_id': row['snapshot_id'],
                'content_type': row['content_type'],
                'priority': row['priority'],
                'token_count': row['token_count'],
                'content': row['content'],
                'metadata': row['metadata'],
                'created_at': row['created_at']
            })

        return results

    def _register_instance(
        self,
        instance_id: str,
        project_id: str,
        phase_id: Optional[int]
    ):
        """
        Register instance in active_instances table.

        Args:
            instance_id: Instance identifier
            project_id: Project identifier
            phase_id: Optional phase identifier
        """
        import socket
        import os

        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            query = """
                INSERT OR REPLACE INTO active_instances
                (instance_id, project_id, phase_id, hostname, process_id, status, last_heartbeat)
                VALUES (?, ?, ?, ?, ?, 'active', datetime('now'))
            """
            cursor.execute(query, (
                instance_id,
                project_id,
                phase_id,
                socket.gethostname(),
                os.getpid()
            ))
            conn.commit()
            logger.info(f"✅ Instance {instance_id} registered")
        except sqlite3.Error as e:
            logger.error(f"❌ Failed to register instance: {e}")
            conn.rollback()

    def get_full_context(
        self,
        project_id: str,
        phase_id: Optional[int] = None
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Get full context for a project (all priorities).

        Args:
            project_id: Project identifier
            phase_id: Optional phase identifier

        Returns:
            Dict with context organized by priority
        """
        logger.info(f"🔄 Loading full context for project {project_id}")

        all_context = {}
        total_items = 0

        for priority in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']:
            context = self._load_priority(priority, project_id, phase_id)
            all_context[priority] = context
            total_items += len(context)

        logger.info(f"✅ Full context loaded: {total_items} total items")
        return all_context

    def clear_instance_tokens(self, instance_id: str):
        """
        Clear tokens for an instance.

        Args:
            instance_id: Instance identifier
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "UPDATE active_instances SET current_token_usage = 0 WHERE instance_id = ?",
                (instance_id,)
            )
            conn.commit()
            logger.info(f"✅ Tokens cleared for instance {instance_id}")
        except sqlite3.Error as e:
            logger.error(f"❌ Failed to clear tokens: {e}")
            conn.rollback()

    def update_heartbeat(self, instance_id: str):
        """
        Update heartbeat timestamp for an instance.

        Args:
            instance_id: Instance identifier
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "UPDATE active_instances SET last_heartbeat = datetime('now') WHERE instance_id = ?",
                (instance_id,)
            )
            conn.commit()
        except sqlite3.Error as e:
            logger.warning(f"⚠️  Failed to update heartbeat: {e}")
            conn.rollback()

    def store_context(
        self,
        project_id: str,
        content: Dict[str, Any],
        priority: str = 'HIGH',
        content_type: str = 'code',
        phase_id: Optional[int] = None
    ) -> int:
        """
        Store context snapshot.

        Args:
            project_id: Project identifier
            content: Context data (will be JSON encoded)
            priority: Priority level (CRITICAL, HIGH, MEDIUM, LOW)
            content_type: Type of content
            phase_id: Optional phase identifier

        Returns:
            snapshot_id of created snapshot
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            # Get next sequence number
            cursor.execute(
                "SELECT COALESCE(MAX(sequence_number), 0) + 1 FROM context_snapshots WHERE project_id = ?",
                (project_id,)
            )
            sequence_number = cursor.fetchone()[0]

            # Calculate token count
            token_count = len(json.dumps(content)) // 4

            # Insert snapshot
            query = """
                INSERT INTO context_snapshots
                (project_id, phase_id, sequence_number, content_type, priority, token_count, content)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            cursor.execute(query, (
                project_id,
                phase_id,
                sequence_number,
                content_type,
                priority,
                token_count,
                json.dumps(content)
            ))
            conn.commit()

            snapshot_id = cursor.lastrowid
            logger.info(f"✅ Context snapshot stored: ID {snapshot_id}")
            return snapshot_id

        except sqlite3.Error as e:
            logger.error(f"❌ Failed to store context: {e}")
            conn.rollback()
            raise

    def close(self):
        """Close database connection."""
        if hasattr(self._local, 'conn') and self._local.conn:
            self._local.conn.close()
            self._local.conn = None
            logger.info("✅ Database connection closed")

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()


# Example usage
def main():
    """Example usage of SQLiteContextLoader."""
    with SQLiteContextLoader("ultrathink_context.db") as loader:
        # Create a test project
        conn = loader._get_connection()
        cursor = conn.cursor()

        # Check if test project exists
        cursor.execute("SELECT project_id FROM projects WHERE project_id = ?", ("proj_test_001",))
        if not cursor.fetchone():
            cursor.execute(
                "INSERT INTO projects (project_id, name, description, total_story_points) VALUES (?, ?, ?, ?)",
                ("proj_test_001", "Test Project", "Database-first test", 100)
            )
            conn.commit()
            print("✅ Test project created")

        # Load context for instance
        result = loader.load_context_for_instance(
            instance_id="inst_test_001",
            project_id="proj_test_001",
            phase_id=None
        )

        print(f"✅ Instance ready in ~{result['load_time_ms']:.1f}ms")
        print(f"✅ CRITICAL context loaded: {len(result['critical_context'])} items")

        # Store some context
        loader.store_context(
            project_id="proj_test_001",
            content={"message": "Test context snapshot", "timestamp": datetime.now().isoformat()},
            priority="HIGH",
            content_type="test"
        )
        print("✅ Context snapshot stored")

        # Get full context
        full_context = loader.get_full_context("proj_test_001")
        total_items = sum(len(items) for items in full_context.values())
        print(f"✅ Full context: {total_items} total items")


if __name__ == "__main__":
    main()
