#!/usr/bin/env python3
"""
test_instance_isolation.py - Comprehensive Instance Isolation Test Suite

PRODUCTION-READY IMPLEMENTATION (2025-11-16)
============================================

PURPOSE:
- Test all instance isolation functionality
- Verify per-instance file creation
- Test cross-instance aggregation
- Validate display formatting
- Ensure backward compatibility

TEST COVERAGE:
- ✅ Instance ID generation and uniqueness
- ✅ Instance registration and cleanup
- ✅ Per-instance state files
- ✅ Per-instance metrics tracking
- ✅ Cross-instance aggregation
- ✅ Display formatting (both modes)
- ✅ Backward compatibility (shared mode)
- ✅ Stale instance cleanup

RUN ALL TESTS:
    python3 test_instance_isolation.py

RUN SPECIFIC TEST:
    python3 test_instance_isolation.py TestInstanceIDManager.test_unique_id_generation
"""

import unittest
import os
import sys
import json
import time
import tempfile
import shutil
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from instance_id_manager import InstanceIDManager
from metrics_state_persistence import MetricsStatePersistence, RequestState
from multi_source_metrics_verifier import MultiSourceMetricsVerifier
from metrics_aggregator import MetricsAggregator
from statusline_formatter import StatuslineFormatter


class TestInstanceIDManager(unittest.TestCase):
    """Test instance ID generation and management."""

    def setUp(self):
        """Create temporary directory for tests."""
        self.test_dir = tempfile.mkdtemp()
        self.manager = InstanceIDManager(lock_dir=f"{self.test_dir}/instances")

    def tearDown(self):
        """Cleanup test directory."""
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_unique_id_generation(self):
        """Test that generated IDs are unique."""
        id1 = self.manager.generate_instance_id()
        time.sleep(0.001)  # Small delay to ensure different timestamp
        id2 = self.manager.generate_instance_id()

        self.assertNotEqual(id1, id2, "Instance IDs should be unique")
        self.assertTrue(len(id1) > 10, "Instance ID should be reasonably long")

    def test_id_format(self):
        """Test that instance ID has correct format."""
        instance_id = self.manager.generate_instance_id()

        # Should have format: YYYYMMDD_HHMMSS_pid_hash
        parts = instance_id.split('_')
        self.assertGreaterEqual(len(parts), 3, "ID should have at least 3 parts")

        # First part should be 8-digit date
        self.assertEqual(len(parts[0]), 8, "First part should be 8-digit date")
        self.assertTrue(parts[0].isdigit(), "Date should be numeric")

    def test_instance_registration(self):
        """Test instance registration creates lock file."""
        success = self.manager.register_instance(metadata={'test': 'data'})

        self.assertTrue(success, "Registration should succeed")
        self.assertTrue(self.manager._registered, "Should be marked as registered")
        self.assertTrue(self.manager._lock_file.exists(), "Lock file should exist")

        # Verify lock file content
        with open(self.manager._lock_file, 'r') as f:
            data = json.load(f)
            self.assertEqual(data['instance_id'], self.manager.get_instance_id())
            self.assertEqual(data['metadata']['test'], 'data')

    def test_list_active_instances(self):
        """Test listing active instances."""
        # Create 3 instances
        instances = []
        for i in range(3):
            mgr = InstanceIDManager(lock_dir=f"{self.test_dir}/instances")
            mgr.register_instance(metadata={'index': i})
            instances.append(mgr)

        # List active instances
        active = self.manager.list_active_instances()

        self.assertEqual(len(active), 3, "Should find 3 active instances")

    def test_cleanup_stale_instances(self):
        """Test cleanup of stale instances."""
        # Create a stale lock file
        stale_id = "20200101_000000_12345_abcd"
        stale_lock = self.manager._lock_dir / f"instance_{stale_id}.lock"

        lock_data = {
            'instance_id': stale_id,
            'pid': 99999,
            'start_time': '2020-01-01T00:00:00',
            'last_heartbeat': '2020-01-01T00:00:00'
        }

        with open(stale_lock, 'w') as f:
            json.dump(lock_data, f)

        # Run cleanup
        cleaned = self.manager.cleanup_stale_instances(max_age_seconds=60)

        self.assertEqual(cleaned, 1, "Should clean up 1 stale instance")
        self.assertFalse(stale_lock.exists(), "Stale lock file should be removed")


class TestMetricsStatePersistence(unittest.TestCase):
    """Test per-instance state persistence."""

    def setUp(self):
        """Create temporary directory for tests."""
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Cleanup test directory."""
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_shared_mode(self):
        """Test backward compatible shared mode."""
        manager = MetricsStatePersistence(
            state_file=f"{self.test_dir}/statusline_state.json"
        )

        self.assertIsNone(manager.instance_id, "Should not have instance ID in shared mode")
        self.assertTrue("statusline_state.json" in str(manager.state_file))

    def test_instance_mode(self):
        """Test per-instance mode with instance ID."""
        instance_id = "20251116_031234_12345_abcd"
        manager = MetricsStatePersistence(instance_id=instance_id)

        self.assertEqual(manager.instance_id, instance_id)
        self.assertTrue(instance_id in str(manager.state_file), "State file should include instance ID")

    def test_per_instance_state_files(self):
        """Test that different instances create separate state files."""
        id1 = "inst1"
        id2 = "inst2"

        mgr1 = MetricsStatePersistence(
            state_file=f"{self.test_dir}/state.json",
            instance_id=id1
        )
        mgr2 = MetricsStatePersistence(
            state_file=f"{self.test_dir}/state.json",
            instance_id=id2
        )

        # Update different metrics for each instance
        mgr1.update_active_metrics({'agents': '10', 'confidence': '95.0'})
        mgr2.update_active_metrics({'agents': '20', 'confidence': '99.0'})

        # Verify files are separate
        state1 = mgr1.load_state()
        state2 = mgr2.load_state()

        self.assertEqual(state1['agents'], '10', "Instance 1 should have 10 agents")
        self.assertEqual(state2['agents'], '20', "Instance 2 should have 20 agents")


class TestMultiSourceMetricsVerifier(unittest.TestCase):
    """Test per-instance metrics verification."""

    def setUp(self):
        """Create temporary directory for tests."""
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Cleanup test directory."""
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_shared_mode_verifier(self):
        """Test verifier in shared mode (backward compatible)."""
        verifier = MultiSourceMetricsVerifier()

        self.assertIsNone(verifier.instance_id, "Should not have instance ID in shared mode")

    def test_instance_mode_verifier(self):
        """Test verifier in per-instance mode."""
        instance_id = "test_instance_123"
        verifier = MultiSourceMetricsVerifier(instance_id=instance_id)

        self.assertEqual(verifier.instance_id, instance_id)


class TestMetricsAggregator(unittest.TestCase):
    """Test cross-instance metrics aggregation."""

    def setUp(self):
        """Create temporary directory for tests."""
        self.test_dir = tempfile.mkdtemp()
        self.aggregator = MetricsAggregator(tmp_dir=self.test_dir)

    def tearDown(self):
        """Cleanup test directory."""
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_aggregate_agent_counts(self):
        """Test aggregating agent counts across instances."""
        # Create instance counter files
        instances = [
            ("inst1", 25),
            ("inst2", 35),
            ("inst3", 25),
            ("inst4", 35),
            ("inst5", 25)
        ]

        for inst_id, count in instances:
            counter_file = Path(self.test_dir) / f"agent_usage_counter_{inst_id}.txt"
            counter_file.write_text(str(count))

        # Aggregate
        data = self.aggregator.aggregate_agent_counts()

        self.assertEqual(data['total_agents'], 145, "Total agents should be 145")
        self.assertEqual(data['instance_count'], 5, "Should have 5 instances")
        self.assertEqual(data['max_agents'], 35, "Max should be 35")
        self.assertEqual(data['min_agents'], 25, "Min should be 25")

    def test_aggregate_confidence_scores(self):
        """Test aggregating confidence scores."""
        # Create realtime metrics files
        instances = [
            ("inst1", 95.0),
            ("inst2", 99.0),
            ("inst3", 98.5)
        ]

        for inst_id, conf in instances:
            metrics_file = Path(self.test_dir) / f"realtime_metrics_{inst_id}.json"
            metrics_file.write_text(json.dumps({'confidence': conf}))

        # Aggregate
        data = self.aggregator.aggregate_confidence_scores()

        self.assertGreater(data['avg_confidence'], 0, "Average confidence should be > 0")
        self.assertEqual(data['max_confidence'], 99.0, "Max confidence should be 99.0")
        self.assertEqual(data['min_confidence'], 95.0, "Min confidence should be 95.0")

    def test_aggregate_all(self):
        """Test full aggregation of all metrics."""
        # Create test files
        counter_file = Path(self.test_dir) / "agent_usage_counter_test1.txt"
        counter_file.write_text("30")

        metrics_file = Path(self.test_dir) / "realtime_metrics_test1.json"
        metrics_file.write_text(json.dumps({'confidence': 99.5, 'executing': True}))

        # Aggregate all
        data = self.aggregator.aggregate_all()

        self.assertEqual(data['total_agents'], 30)
        self.assertEqual(data['instance_count'], 1)
        self.assertGreater(data['avg_confidence'], 0)
        self.assertIn('timestamp', data)


class TestStatuslineFormatter(unittest.TestCase):
    """Test display formatting."""

    def test_shared_mode_formatting(self):
        """Test formatting in shared mode."""
        formatter = StatuslineFormatter(instance_mode=False)

        output = formatter.format_all(
            current_agents=145,
            tokens_used=15000,
            tokens_total=200000,
            confidence=99.2,
            status='🟢 OPTIMAL'
        )

        self.assertIn("Agents: 145", output)
        self.assertIn("Tokens:", output)
        self.assertIn("Conf: 99.2%", output)

    def test_instance_mode_formatting(self):
        """Test formatting in per-instance mode."""
        formatter = StatuslineFormatter(instance_mode=True)

        output = formatter.format_all(
            current_agents=25,
            total_agents=145,
            instance_count=5,
            tokens_used=15000,
            tokens_total=200000,
            confidence=99.2,
            status='🟢 OPTIMAL'
        )

        self.assertIn("Agents: 25/145 (5)", output)
        self.assertIn("Tokens:", output)
        self.assertIn("Conf: 99.2%", output)

    def test_compact_formatting(self):
        """Test compact format."""
        formatter = StatuslineFormatter(instance_mode=True)

        output = formatter.format_compact(
            current_agents=25,
            total_agents=145,
            instance_count=5,
            tokens_pct=7.5,
            confidence=99.2
        )

        self.assertIn("A:25/145(5)", output)
        self.assertIn("T:7.5%", output)
        self.assertIn("C:99.2%", output)

    def test_json_formatting(self):
        """Test JSON format."""
        formatter = StatuslineFormatter(instance_mode=True)

        output = formatter.format_json(
            current_agents=25,
            total_agents=145,
            instance_count=5,
            tokens_used=15000,
            tokens_total=200000,
            confidence=99.2,
            status='🟢 OPTIMAL'
        )

        data = json.loads(output)
        self.assertEqual(data['agents']['current'], 25)
        self.assertEqual(data['agents']['total'], 145)
        self.assertEqual(data['agents']['instance_count'], 5)
        self.assertAlmostEqual(data['tokens']['percentage'], 7.5, places=1)


class TestBackwardCompatibility(unittest.TestCase):
    """Test that all changes are backward compatible."""

    def test_state_persistence_default(self):
        """Test state persistence defaults to shared mode."""
        manager = MetricsStatePersistence()
        self.assertIsNone(manager.instance_id)

    def test_metrics_verifier_default(self):
        """Test metrics verifier defaults to shared mode."""
        verifier = MultiSourceMetricsVerifier()
        self.assertIsNone(verifier.instance_id)

    def test_formatter_default(self):
        """Test formatter defaults to shared mode."""
        formatter = StatuslineFormatter()
        self.assertFalse(formatter.instance_mode)


class TestIntegration(unittest.TestCase):
    """End-to-end integration tests."""

    def setUp(self):
        """Create temporary directory for tests."""
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Cleanup test directory."""
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_full_workflow(self):
        """Test complete workflow: ID generation → metrics → aggregation → formatting."""
        # Step 1: Create instance IDs
        id_mgr = InstanceIDManager(lock_dir=f"{self.test_dir}/instances")
        instance_id = id_mgr.get_instance_id()

        # Step 2: Create per-instance metrics files
        counter_file = Path(self.test_dir) / f"agent_usage_counter_{instance_id}.txt"
        counter_file.write_text("42")

        metrics_file = Path(self.test_dir) / f"realtime_metrics_{instance_id}.json"
        metrics_file.write_text(json.dumps({'confidence': 99.5, 'executing': True}))

        # Step 3: Aggregate metrics
        aggregator = MetricsAggregator(tmp_dir=self.test_dir)
        aggregated = aggregator.aggregate_all()

        self.assertEqual(aggregated['total_agents'], 42)
        self.assertEqual(aggregated['instance_count'], 1)

        # Step 4: Format for display
        formatter = StatuslineFormatter(instance_mode=True)
        display = formatter.format_all(
            current_agents=42,
            total_agents=aggregated['total_agents'],
            instance_count=aggregated['instance_count'],
            tokens_used=10000,
            tokens_total=200000,
            confidence=aggregated['avg_confidence'],
            status='🟢 OPTIMAL'
        )

        self.assertIn("42/42 (1)", display)


def run_tests():
    """Run all tests with detailed output."""
    print("=" * 80)
    print("INSTANCE ISOLATION TEST SUITE")
    print("=" * 80)
    print()

    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestInstanceIDManager))
    suite.addTests(loader.loadTestsFromTestCase(TestMetricsStatePersistence))
    suite.addTests(loader.loadTestsFromTestCase(TestMultiSourceMetricsVerifier))
    suite.addTests(loader.loadTestsFromTestCase(TestMetricsAggregator))
    suite.addTests(loader.loadTestsFromTestCase(TestStatuslineFormatter))
    suite.addTests(loader.loadTestsFromTestCase(TestBackwardCompatibility))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))

    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print()
    print("=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print()

    if result.wasSuccessful():
        print("✅ ALL TESTS PASSED - 100% SUCCESS RATE")
        return 0
    else:
        print("❌ SOME TESTS FAILED")
        return 1


if __name__ == '__main__':
    exit_code = run_tests()
    sys.exit(exit_code)
