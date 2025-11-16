#!/usr/bin/env python3
"""
Performance Telemetry System
Purpose: Collect all execution metrics for analysis
"""

import sqlite3
from datetime import datetime
from pathlib import Path
import json
from contextlib import contextmanager

class TelemetryDatabase:
    """SQLite database for tracking all ClaudePrompt executions"""

    def __init__(self, db_path=None):
        if db_path is None:
            db_path = Path.home() / ".ultrathink" / "telemetry.db"

        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_database()

    def _init_database(self):
        """Create tables if they don't exist"""
        with self._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS executions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME NOT NULL,
                    prompt TEXT NOT NULL,
                    prompt_hash TEXT NOT NULL,
                    complexity TEXT,
                    iterations INTEGER,
                    initial_confidence REAL,
                    final_confidence REAL,
                    confidence_improvement REAL,
                    execution_time_ms INTEGER,
                    guardrail_passes INTEGER,
                    guardrail_failures INTEGER,
                    guardrail_layer_1 BOOLEAN,
                    guardrail_layer_2 BOOLEAN,
                    guardrail_layer_3 BOOLEAN,
                    guardrail_layer_4 BOOLEAN,
                    guardrail_layer_5 BOOLEAN,
                    guardrail_layer_6 BOOLEAN,
                    guardrail_layer_7 BOOLEAN,
                    guardrail_layer_8 BOOLEAN,
                    success BOOLEAN NOT NULL,
                    error_message TEXT,
                    output_length INTEGER,
                    agent_count INTEGER
                )
            """)

            # Create indexes
            conn.execute("CREATE INDEX IF NOT EXISTS idx_timestamp ON executions(timestamp)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_success ON executions(success)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_confidence ON executions(final_confidence)")

    @contextmanager
    def _get_connection(self):
        """Context manager for database connections"""
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    def log_execution(self, **kwargs):
        """Log an execution to the database"""
        with self._get_connection() as conn:
            conn.execute("""
                INSERT INTO executions (
                    timestamp, prompt, prompt_hash, complexity, iterations,
                    initial_confidence, final_confidence, confidence_improvement,
                    execution_time_ms, guardrail_passes, guardrail_failures,
                    guardrail_layer_1, guardrail_layer_2, guardrail_layer_3,
                    guardrail_layer_4, guardrail_layer_5, guardrail_layer_6,
                    guardrail_layer_7, guardrail_layer_8,
                    success, error_message, output_length, agent_count
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                kwargs.get('timestamp', datetime.now()),
                kwargs['prompt'],
                kwargs.get('prompt_hash', ''),
                kwargs.get('complexity', 'UNKNOWN'),
                kwargs.get('iterations', 0),
                kwargs.get('initial_confidence', 0),
                kwargs.get('final_confidence', 0),
                kwargs.get('confidence_improvement', 0),
                kwargs.get('execution_time_ms', 0),
                kwargs.get('guardrail_passes', 0),
                kwargs.get('guardrail_failures', 0),
                kwargs.get('guardrail_layer_1', False),
                kwargs.get('guardrail_layer_2', False),
                kwargs.get('guardrail_layer_3', False),
                kwargs.get('guardrail_layer_4', False),
                kwargs.get('guardrail_layer_5', False),
                kwargs.get('guardrail_layer_6', False),
                kwargs.get('guardrail_layer_7', False),
                kwargs.get('guardrail_layer_8', False),
                kwargs['success'],
                kwargs.get('error_message'),
                kwargs.get('output_length', 0),
                kwargs.get('agent_count', 0)
            ))

    def query_low_confidence(self, threshold=99.0):
        """Query executions with confidence below threshold"""
        with self._get_connection() as conn:
            cursor = conn.execute("""
                SELECT id, timestamp, prompt, final_confidence, iterations
                FROM executions
                WHERE final_confidence < ? AND success = 1
                ORDER BY final_confidence ASC
            """, (threshold,))
            return cursor.fetchall()

    def query_slow_convergence(self, threshold_iterations=10):
        """Query executions that took many iterations"""
        with self _get_connection() as conn:
            cursor = conn.execute("""
                SELECT id, timestamp, prompt, iterations, final_confidence
                FROM executions
                WHERE iterations > ? AND success = 1
                ORDER BY iterations DESC
            """, (threshold_iterations,))
            return cursor.fetchall()

    def get_statistics(self):
        """Get overall statistics"""
        with self._get_connection() as conn:
            cursor = conn.execute("""
                SELECT
                    COUNT(*) as total_executions,
                    SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as successful,
                    AVG(CASE WHEN success = 1 THEN final_confidence ELSE NULL END) as avg_confidence,
                    AVG(CASE WHEN success = 1 THEN iterations ELSE NULL END) as avg_iterations,
                    AVG(CASE WHEN success = 1 THEN execution_time_ms ELSE NULL END) as avg_time_ms
                FROM executions
            """)
            row = cursor.fetchone()
            return {
                "total_executions": row[0],
                "successful": row[1],
                "success_rate": (row[1] / row[0] * 100) if row[0] > 0 else 0,
                "avg_confidence": row[2] or 0,
                "avg_iterations": row[3] or 0,
                "avg_time_ms": row[4] or 0
            }

# Global instance
telemetry = TelemetryDatabase()

if __name__ == "__main__":
    # Test the telemetry system
    print("Testing telemetry system...")

    # Log a test execution
    telemetry.log_execution(
        prompt="Test prompt",
        prompt_hash="abc123",
        complexity="SIMPLE",
        iterations=3,
        initial_confidence=85.0,
        final_confidence=99.2,
        confidence_improvement=14.2,
        execution_time_ms=1500,
        guardrail_passes=8,
        guardrail_failures=0,
        guardrail_layer_1=True,
        guardrail_layer_2=True,
        guardrail_layer_3=True,
        guardrail_layer_4=True,
        guardrail_layer_5=True,
        guardrail_layer_6=True,
        guardrail_layer_7=True,
        guardrail_layer_8=True,
        success=True,
        output_length=500,
        agent_count=10
    )

    # Get statistics
    stats = telemetry.get_statistics()
    print(f"\nStatistics:")
    print(f"  Total executions: {stats['total_executions']}")
    print(f"  Successful: {stats['successful']}")
    print(f"  Success rate: {stats['success_rate']:.1f}%")
    print(f"  Avg confidence: {stats['avg_confidence']:.1f}%")
    print(f"  Avg iterations: {stats['avg_iterations']:.1f}")
    print(f"  Avg time: {stats['avg_time_ms']:.0f}ms")

    print("\n✅ Telemetry system working correctly")
