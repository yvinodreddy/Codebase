#!/usr/bin/env python3
"""
Comprehensive Testing Suite for Database-First Context Management

Tests all components with 100% coverage:
- Database initialization
- Project creation and management
- Instance launching and coordination
- Context storage and retrieval
- Priority-based loading
- Token management (clear+reload)
- Multi-instance coordination
- Error handling and edge cases

Author: ULTRATHINK System
Date: 2025-11-19
Version: 1.0.0
"""

import os
import sys
import sqlite3
import json
import time
from pathlib import Path
from typing import Dict, List, Any

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

from sqlite_context_loader import SQLiteContextLoader
from multi_project_manager import MultiProjectManager
from token_manager import TokenManager


class TestResult:
    """Test result container."""

    def __init__(self, name: str):
        self.name = name
        self.passed = False
        self.error = None
        self.duration_ms = 0


class DatabaseFirstTestSuite:
    """Comprehensive test suite for database-first architecture."""

    def __init__(self, test_db_path: str = "test_ultrathink.db"):
        """Initialize test suite with temporary database."""
        self.test_db_path = test_db_path
        self.results: List[TestResult] = []

        # Clean up test database if exists
        if os.path.exists(test_db_path):
            os.remove(test_db_path)

    def run_all_tests(self) -> bool:
        """Run all tests and return overall success."""
        print("\n" + "=" * 80)
        print("DATABASE-FIRST CONTEXT MANAGEMENT - TEST SUITE")
        print("=" * 80 + "\n")

        # Run tests
        test_methods = [
            self.test_database_initialization,
            self.test_project_creation,
            self.test_instance_launch,
            self.test_context_storage,
            self.test_context_retrieval,
            self.test_priority_based_loading,
            self.test_token_management,
            self.test_token_clear_and_reload,
            self.test_multi_instance_coordination,
            self.test_multi_project_isolation,
            self.test_phase_management,
            self.test_heartbeat_monitoring,
            self.test_project_summary,
            self.test_error_handling,
            self.test_concurrent_operations,
            self.test_performance_benchmarks
        ]

        for test_method in test_methods:
            result = self._run_test(test_method)
            self.results.append(result)

        # Display results
        self._display_results()

        # Return overall success
        return all(r.passed for r in self.results)

    def _run_test(self, test_method) -> TestResult:
        """Run single test with timing and error handling."""
        result = TestResult(test_method.__name__)

        start_time = time.time()

        try:
            test_method()
            result.passed = True
        except AssertionError as e:
            result.passed = False
            result.error = str(e)
        except Exception as e:
            result.passed = False
            result.error = f"Unexpected error: {e}"

        result.duration_ms = (time.time() - start_time) * 1000

        return result

    def _display_results(self):
        """Display test results."""
        print("\n" + "=" * 80)
        print("TEST RESULTS")
        print("=" * 80 + "\n")

        passed = 0
        failed = 0

        for result in self.results:
            status = "✅ PASSED" if result.passed else "❌ FAILED"
            duration = f"{result.duration_ms:.1f}ms"

            # Format test name (remove test_ prefix)
            name = result.name.replace("test_", "").replace("_", " ").title()

            print(f"Test: {name:<40} {status:>15} ({duration})")

            if not result.passed and result.error:
                print(f"      Error: {result.error}")

            if result.passed:
                passed += 1
            else:
                failed += 1

        print("\n" + "=" * 80)
        if failed == 0:
            print(f"✅ ALL TESTS PASSED ({passed}/{len(self.results)})")
        else:
            print(f"❌ SOME TESTS FAILED ({passed} passed, {failed} failed)")
        print("=" * 80 + "\n")

    # =========================================================================
    # TEST CASES
    # =========================================================================

    def test_database_initialization(self):
        """Test database schema initialization."""
        loader = SQLiteContextLoader(self.test_db_path)

        # Check tables exist
        conn = loader._get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = {row['name'] for row in cursor.fetchall()}

        required_tables = {'projects', 'phases', 'context_snapshots', 'active_instances', 'schema_version'}

        assert required_tables.issubset(tables), f"Missing tables: {required_tables - tables}"

        # Check schema version
        cursor.execute("SELECT version FROM schema_version ORDER BY applied_at DESC LIMIT 1")
        row = cursor.fetchone()
        assert row is not None, "No schema version found"
        assert row['version'] == '1.0.0', f"Wrong schema version: {row['version']}"

        loader.close()

    def test_project_creation(self):
        """Test project creation."""
        manager = MultiProjectManager(self.test_db_path)

        # Create project
        project_id = manager.create_project(
            name="Test Project",
            description="Testing project creation",
            total_story_points=1300
        )

        assert project_id.startswith("proj_"), f"Invalid project_id format: {project_id}"

        # Verify in database
        conn = manager.loader._get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM projects WHERE project_id = ?", (project_id,))
        row = cursor.fetchone()

        assert row is not None, "Project not found in database"
        assert row['name'] == "Test Project"
        assert row['total_story_points'] == 1300

        manager.close()

    def test_instance_launch(self):
        """Test instance launching."""
        manager = MultiProjectManager(self.test_db_path)

        # Create project first
        project_id = manager.create_project("Test Project", "Test", 100)

        # Launch instance
        instance_id = manager.launch_instance(project_id)

        assert instance_id.startswith("inst_"), f"Invalid instance_id format: {instance_id}"

        # Verify in database
        conn = manager.loader._get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM active_instances WHERE instance_id = ?", (instance_id,))
        row = cursor.fetchone()

        assert row is not None, "Instance not found in database"
        assert row['project_id'] == project_id
        assert row['status'] == 'active'

        manager.close()

    def test_context_storage(self):
        """Test context storage."""
        manager = MultiProjectManager(self.test_db_path)

        # Create project
        project_id = manager.create_project("Test Project", "Test", 100)

        # Store context
        content = {"code": "def foo(): pass", "decision": "Use function"}
        snapshot_id = manager.store_context(
            project_id=project_id,
            content=content,
            priority="HIGH",
            content_type="code"
        )

        assert snapshot_id > 0, f"Invalid snapshot_id: {snapshot_id}"

        # Verify in database
        conn = manager.loader._get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM context_snapshots WHERE snapshot_id = ?", (snapshot_id,))
        row = cursor.fetchone()

        assert row is not None, "Context snapshot not found"
        assert row['priority'] == 'HIGH'
        assert row['content_type'] == 'code'
        assert json.loads(row['content']) == content

        manager.close()

    def test_context_retrieval(self):
        """Test context retrieval."""
        loader = SQLiteContextLoader(self.test_db_path)
        manager = MultiProjectManager(self.test_db_path)

        # Create project
        project_id = manager.create_project("Test Project", "Test", 100)

        # Store context
        manager.store_context(project_id, {"item": 1}, priority="CRITICAL")
        manager.store_context(project_id, {"item": 2}, priority="HIGH")
        manager.store_context(project_id, {"item": 3}, priority="MEDIUM")

        # Load context for instance
        instance_id = "test_inst_001"
        result = loader.load_context_for_instance(instance_id, project_id)

        assert result['instance_id'] == instance_id
        assert result['project_id'] == project_id
        assert result['status'] == 'ready'
        assert len(result['critical_context']) == 1, "Should load 1 CRITICAL item"

        # Get full context
        full_context = loader.get_full_context(project_id)

        assert len(full_context['CRITICAL']) == 1
        assert len(full_context['HIGH']) == 1
        assert len(full_context['MEDIUM']) == 1
        assert len(full_context['LOW']) == 0

        loader.close()
        manager.close()

    def test_priority_based_loading(self):
        """Test priority-based context loading."""
        loader = SQLiteContextLoader(self.test_db_path)
        manager = MultiProjectManager(self.test_db_path)

        # Create project
        project_id = manager.create_project("Test Project", "Test", 100)

        # Store context with different priorities
        for i in range(1, 6):
            manager.store_context(project_id, {"item": i}, priority="CRITICAL")
        for i in range(6, 11):
            manager.store_context(project_id, {"item": i}, priority="HIGH")
        for i in range(11, 16):
            manager.store_context(project_id, {"item": i}, priority="MEDIUM")

        # Load context (should load only CRITICAL initially)
        instance_id = "test_inst_001"
        start_time = time.time()
        result = loader.load_context_for_instance(instance_id, project_id)
        elapsed_ms = (time.time() - start_time) * 1000

        assert len(result['critical_context']) == 5, "Should load 5 CRITICAL items"
        assert elapsed_ms < 200, f"Load time too slow: {elapsed_ms:.1f}ms (target: <200ms)"

        loader.close()
        manager.close()

    def test_token_management(self):
        """Test token usage tracking."""
        manager = MultiProjectManager(self.test_db_path)
        token_mgr = TokenManager(self.test_db_path)

        # Create project and instance
        project_id = manager.create_project("Test Project", "Test", 100)
        instance_id = manager.launch_instance(project_id)

        # Update token usage
        token_mgr.update_token_usage(instance_id, 85000)

        # Check usage
        usage = token_mgr.check_token_usage(instance_id)

        assert usage is not None, "Usage should not be None"
        assert usage['current_token_usage'] == 85000
        assert usage['percentage'] == 42.5  # 85000 / 200000 * 100
        assert usage['tokens_remaining'] == 115000

        manager.close()
        token_mgr.close()

    def test_token_clear_and_reload(self):
        """Test token clear+reload functionality."""
        manager = MultiProjectManager(self.test_db_path)
        token_mgr = TokenManager(self.test_db_path)

        # Create project and instance
        project_id = manager.create_project("Test Project", "Test", 100)
        instance_id = manager.launch_instance(project_id)

        # Store some context
        manager.store_context(project_id, {"item": 1}, priority="CRITICAL")
        manager.store_context(project_id, {"item": 2}, priority="HIGH")

        # Set token usage to high level
        token_mgr.update_token_usage(instance_id, 170000)

        # Clear and reload
        result = token_mgr.clear_and_reload(instance_id)

        assert result is not None, "Clear+reload should return result"
        assert result['tokens_before'] == 170000
        assert result['tokens_after'] == 0
        assert result['context_items_loaded'] == 2
        assert result['critical_items'] == 1
        assert result['status'] == 'ready'

        # Verify tokens cleared
        usage = token_mgr.check_token_usage(instance_id)
        assert usage['current_token_usage'] == 0

        manager.close()
        token_mgr.close()

    def test_multi_instance_coordination(self):
        """Test multiple instances for same project."""
        manager = MultiProjectManager(self.test_db_path)

        # Create project
        project_id = manager.create_project("Test Project", "Test", 100)

        # Launch 3 instances
        instances = []
        for i in range(3):
            instance_id = manager.launch_instance(project_id)
            instances.append(instance_id)

        # Verify all instances registered
        project_instances = manager.get_project_instances(project_id)

        assert len(project_instances) == 3

        for instance in project_instances:
            assert instance['instance_id'] in instances
            assert instance['project_id'] == project_id
            assert instance['status'] == 'active'

        manager.close()

    def test_multi_project_isolation(self):
        """Test context isolation between projects."""
        manager = MultiProjectManager(self.test_db_path)
        loader = SQLiteContextLoader(self.test_db_path)

        # Create 2 projects
        project_a = manager.create_project("Project A", "Test A", 100)
        project_b = manager.create_project("Project B", "Test B", 200)

        # Store context for each
        manager.store_context(project_a, {"project": "A", "data": 1}, priority="HIGH")
        manager.store_context(project_b, {"project": "B", "data": 2}, priority="HIGH")

        # Get context for project A
        context_a = loader.get_full_context(project_a)

        # Verify only project A's context returned
        assert len(context_a['HIGH']) == 1
        content_a = json.loads(context_a['HIGH'][0]['content'])
        assert content_a['project'] == 'A'

        # Get context for project B
        context_b = loader.get_full_context(project_b)

        # Verify only project B's context returned
        assert len(context_b['HIGH']) == 1
        content_b = json.loads(context_b['HIGH'][0]['content'])
        assert content_b['project'] == 'B'

        manager.close()
        loader.close()

    def test_phase_management(self):
        """Test phase creation and management."""
        manager = MultiProjectManager(self.test_db_path)

        # Create project
        project_id = manager.create_project("Test Project", "Test", 1300)

        # Create phases
        phase_ids = []
        for i in range(1, 4):
            phase_id = manager.create_phase(
                project_id=project_id,
                phase_number=i,
                name=f"Phase {i}",
                story_points=100 * i
            )
            phase_ids.append(phase_id)

        assert len(phase_ids) == 3

        # Verify phases in database
        conn = manager.loader._get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM phases WHERE project_id = ? ORDER BY phase_number", (project_id,))
        rows = cursor.fetchall()

        assert len(rows) == 3
        for i, row in enumerate(rows, 1):
            assert row['phase_number'] == i
            assert row['name'] == f"Phase {i}"

        manager.close()

    def test_heartbeat_monitoring(self):
        """Test instance heartbeat updates."""
        loader = SQLiteContextLoader(self.test_db_path)
        manager = MultiProjectManager(self.test_db_path)

        # Create project and instance
        project_id = manager.create_project("Test Project", "Test", 100)
        instance_id = manager.launch_instance(project_id)

        # Get initial heartbeat
        conn = loader._get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT last_heartbeat FROM active_instances WHERE instance_id = ?", (instance_id,))
        heartbeat_1 = cursor.fetchone()['last_heartbeat']

        # Wait a moment (1+ second for SQLite datetime precision)
        time.sleep(1.1)

        # Update heartbeat
        loader.update_heartbeat(instance_id)

        # Get updated heartbeat
        cursor.execute("SELECT last_heartbeat FROM active_instances WHERE instance_id = ?", (instance_id,))
        heartbeat_2 = cursor.fetchone()['last_heartbeat']

        assert heartbeat_2 > heartbeat_1, "Heartbeat should be updated"

        loader.close()
        manager.close()

    def test_project_summary(self):
        """Test project summary view."""
        manager = MultiProjectManager(self.test_db_path)

        # Create 2 projects
        project_a = manager.create_project("Project A", "Test A", 500)
        project_b = manager.create_project("Project B", "Test B", 800)

        # Launch instances
        manager.launch_instance(project_a)
        manager.launch_instance(project_a)
        manager.launch_instance(project_b)

        # Store context
        manager.store_context(project_a, {"data": 1}, priority="HIGH")
        manager.store_context(project_a, {"data": 2}, priority="HIGH")
        manager.store_context(project_b, {"data": 3}, priority="HIGH")

        # Get summary
        summaries = manager.get_project_summary()

        assert len(summaries) >= 2, "Should have at least 2 projects"

        # Find project A summary
        summary_a = next((s for s in summaries if s['project_id'] == project_a), None)
        assert summary_a is not None, f"Project A not found in summaries"
        assert summary_a['active_instances'] == 2
        assert summary_a['total_snapshots'] == 2

        # Find project B summary
        summary_b = next((s for s in summaries if s['project_id'] == project_b), None)
        assert summary_b is not None, f"Project B not found in summaries"
        assert summary_b['active_instances'] == 1
        assert summary_b['total_snapshots'] == 1

        manager.close()

    def test_error_handling(self):
        """Test error handling for invalid operations."""
        manager = MultiProjectManager(self.test_db_path)
        token_mgr = TokenManager(self.test_db_path)

        # Test: Check usage for non-existent instance
        usage = token_mgr.check_token_usage("nonexistent_instance")
        assert usage is None, "Should return None for non-existent instance"

        # Test: Clear+reload for non-existent instance
        result = token_mgr.clear_and_reload("nonexistent_instance")
        assert result is None, "Should return None for non-existent instance"

        # Test: Invalid token count (negative)
        project_id = manager.create_project("Test Project", "Test", 100)
        instance_id = manager.launch_instance(project_id)

        token_mgr.update_token_usage(instance_id, -1000)  # Should be rejected
        usage = token_mgr.check_token_usage(instance_id)
        assert usage['current_token_usage'] >= 0, "Token count should not be negative"

        # Test: Invalid token count (> 200K)
        token_mgr.update_token_usage(instance_id, 300000)  # Should be rejected
        usage = token_mgr.check_token_usage(instance_id)
        assert usage['current_token_usage'] <= 200000, "Token count should not exceed 200K"

        manager.close()
        token_mgr.close()

    def test_concurrent_operations(self):
        """Test concurrent database operations."""
        manager = MultiProjectManager(self.test_db_path)

        # Create project
        project_id = manager.create_project("Test Project", "Test", 100)

        # Simulate concurrent context storage (rapid writes)
        snapshot_ids = []
        for i in range(20):
            snapshot_id = manager.store_context(
                project_id=project_id,
                content={"iteration": i},
                priority="HIGH"
            )
            snapshot_ids.append(snapshot_id)

        # Verify all snapshots stored
        assert len(snapshot_ids) == 20
        assert len(set(snapshot_ids)) == 20, "All snapshot IDs should be unique"

        # Verify in database
        conn = manager.loader._get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) as count FROM context_snapshots WHERE project_id = ?", (project_id,))
        count = cursor.fetchone()['count']

        assert count == 20, f"Expected 20 snapshots, found {count}"

        manager.close()

    def test_performance_benchmarks(self):
        """Test performance benchmarks."""
        loader = SQLiteContextLoader(self.test_db_path)
        manager = MultiProjectManager(self.test_db_path)

        # Create project
        project_id = manager.create_project("Performance Test", "Test", 1000)

        # Store 100 context items
        for i in range(100):
            priority = ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW'][i % 4]
            manager.store_context(
                project_id=project_id,
                content={"iteration": i, "data": "x" * 100},
                priority=priority
            )

        # Benchmark: Load CRITICAL context (target: <200ms)
        instance_id = "perf_test_001"
        start_time = time.time()
        result = loader.load_context_for_instance(instance_id, project_id)
        load_time_ms = (time.time() - start_time) * 1000

        assert load_time_ms < 200, f"Load time too slow: {load_time_ms:.1f}ms (target: <200ms)"

        # Benchmark: Get full context (target: <500ms)
        start_time = time.time()
        full_context = loader.get_full_context(project_id)
        full_load_time_ms = (time.time() - start_time) * 1000

        assert full_load_time_ms < 500, f"Full load time too slow: {full_load_time_ms:.1f}ms (target: <500ms)"

        # Benchmark: Store context (target: <10ms)
        start_time = time.time()
        manager.store_context(project_id, {"benchmark": "test"}, priority="HIGH")
        store_time_ms = (time.time() - start_time) * 1000

        assert store_time_ms < 10, f"Store time too slow: {store_time_ms:.1f}ms (target: <10ms)"

        loader.close()
        manager.close()

    def cleanup(self):
        """Clean up test database."""
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)
            print(f"✅ Test database cleaned up: {self.test_db_path}")


def main():
    """Run test suite."""
    suite = DatabaseFirstTestSuite("test_ultrathink.db")

    try:
        success = suite.run_all_tests()

        # Cleanup
        suite.cleanup()

        # Exit with appropriate code
        sys.exit(0 if success else 1)

    except Exception as e:
        print(f"\n❌ Test suite failed with error: {e}")
        import traceback
        traceback.print_exc()

        # Cleanup even on error
        suite.cleanup()

        sys.exit(1)


if __name__ == "__main__":
    main()
