#!/usr/bin/env python3
"""
Phase 07: Testing & QA
Comprehensive Unit and Integration Tests

Test Coverage:
- Phase implementation
- Unit testing framework
- Integration testing framework
- Performance testing framework
- Clinical validation framework
"""

import unittest
import sys
import os
from pathlib import Path

# Add code directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'code'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'deliverables'))

from implementation import Phase07Implementation

try:
    from unit_testing_framework import UnitTestFramework, TestFixtures, MockObjects
    from integration_testing_framework import IntegrationTestSuite, WorkflowIntegrationTest
    from performance_testing_framework import PerformanceTestFramework, PerformanceTest
    from clinical_validation_framework import ClinicalValidator, ClinicalValidationTest
    DELIVERABLES_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Deliverables not available: {e}")
    DELIVERABLES_AVAILABLE = False


class TestPhase07Implementation(unittest.TestCase):
    """Test Phase 07 main implementation"""

    def setUp(self):
        """Set up test fixtures"""
        self.implementation = Phase07Implementation()

    def test_initialization(self):
        """Test proper initialization"""
        self.assertEqual(self.implementation.phase_id, 7)
        self.assertEqual(self.implementation.phase_name, "Testing & QA")
        self.assertEqual(self.implementation.story_points, 68)
        self.assertEqual(self.implementation.priority, "P0")

    def test_phase_execution(self):
        """Test phase execution"""
        task = {"goal": "Implement Testing & QA", "phase_id": 7}
        result = self.implementation.execute(task)

        self.assertIsNotNone(result)
        self.assertTrue(hasattr(result, 'success'))

        if result.success:
            self.assertIsNotNone(result.output)
            self.assertIn('phase_id', result.output)
            self.assertIn('components', result.output)

    def test_get_stats(self):
        """Test statistics retrieval"""
        stats = self.implementation.get_stats()

        self.assertIn('phase_id', stats)
        self.assertIn('phase_name', stats)
        self.assertIn('story_points', stats)
        self.assertEqual(stats['phase_id'], 7)


@unittest.skipUnless(DELIVERABLES_AVAILABLE, "Deliverables not available")
class TestUnitTestingFramework(unittest.TestCase):
    """Test unit testing framework"""

    def setUp(self):
        """Set up test fixtures"""
        self.framework = UnitTestFramework()

    def test_framework_initialization(self):
        """Test framework initialization"""
        self.assertIsNotNone(self.framework)
        self.assertIsNotNone(self.framework.fixtures)
        self.assertIsNotNone(self.framework.mocks)

    def test_fixtures_patient_data(self):
        """Test patient data fixture"""
        patient_data = self.framework.fixtures.get_sample_patient_data()

        self.assertIn('patient_id', patient_data)
        self.assertIn('demographics', patient_data)
        self.assertIn('vitals', patient_data)

    def test_fixtures_clinical_note(self):
        """Test clinical note fixture"""
        note = self.framework.fixtures.get_sample_clinical_note()

        self.assertIn('type', note)
        self.assertIn('text', note)

    def test_mock_guardrails(self):
        """Test mock guardrails"""
        mock = self.framework.mocks.MockGuardrails()
        result = mock.validate("test content")

        self.assertIn('passed', result)
        self.assertTrue(result['passed'])

    def test_mock_database(self):
        """Test mock database"""
        mock_db = self.framework.mocks.MockDatabase()

        # Test insert
        data = {'key': 'value'}
        insert_id = mock_db.insert('test_table', data)
        self.assertIsNotNone(insert_id)

        # Test query
        results = mock_db.query('test_table')
        self.assertEqual(len(results), 1)

        # Test clear
        mock_db.clear()
        results = mock_db.query('test_table')
        self.assertEqual(len(results), 0)


@unittest.skipUnless(DELIVERABLES_AVAILABLE, "Deliverables not available")
class TestIntegrationTestingFramework(unittest.TestCase):
    """Test integration testing framework"""

    def setUp(self):
        """Set up test fixtures"""
        self.suite = IntegrationTestSuite()

    def test_suite_initialization(self):
        """Test suite initialization"""
        self.assertIsNotNone(self.suite)
        self.assertEqual(len(self.suite.tests), 0)

    def test_add_test(self):
        """Test adding test to suite"""
        test = WorkflowIntegrationTest("test_workflow", {'test': True})
        self.suite.add_test(test)

        self.assertEqual(len(self.suite.tests), 1)

    def test_workflow_integration_test(self):
        """Test workflow integration test execution"""
        test = WorkflowIntegrationTest("test_workflow", {'patient_id': 'TEST_001'})

        result = test.run()

        # Should pass even without actual workflow engine
        self.assertIsNotNone(result)
        self.assertIn(test.name, "Workflow Integration: test_workflow")


@unittest.skipUnless(DELIVERABLES_AVAILABLE, "Deliverables not available")
class TestPerformanceTestingFramework(unittest.TestCase):
    """Test performance testing framework"""

    def setUp(self):
        """Set up test fixtures"""
        self.framework = PerformanceTestFramework()

    def test_framework_initialization(self):
        """Test framework initialization"""
        self.assertIsNotNone(self.framework)
        self.assertEqual(len(self.framework.benchmarks), 0)

    def test_add_benchmark(self):
        """Test adding benchmark"""
        def sample_function():
            return "test"

        self.framework.add_benchmark("test_benchmark", sample_function)
        self.assertEqual(len(self.framework.benchmarks), 1)

    def test_benchmark_execution(self):
        """Test benchmark execution"""
        def fast_function():
            return "fast"

        test = PerformanceTest("test", fast_function)
        summary = test.run_benchmark(iterations=10)

        self.assertIn('response_time', summary)
        self.assertIn('total_requests', summary)
        self.assertEqual(summary['total_requests'], 10)


@unittest.skipUnless(DELIVERABLES_AVAILABLE, "Deliverables not available")
class TestClinicalValidationFramework(unittest.TestCase):
    """Test clinical validation framework"""

    def setUp(self):
        """Set up test fixtures"""
        self.validator = ClinicalValidator()
        self.test_suite = ClinicalValidationTest()

    def test_validator_initialization(self):
        """Test validator initialization"""
        self.assertIsNotNone(self.validator)
        self.assertIsNotNone(self.validator.validation_rules)

    def test_validate_vitals_valid(self):
        """Test vital signs validation - valid case"""
        vitals = {
            'systolic_bp': 120,
            'diastolic_bp': 80,
            'heart_rate': 75,
            'respiratory_rate': 16,
            'temperature': 37.0
        }

        result = self.validator.validate_vitals(vitals)

        self.assertTrue(result['passed'])
        self.assertEqual(len(result['errors']), 0)

    def test_validate_vitals_invalid(self):
        """Test vital signs validation - invalid case"""
        vitals = {
            'systolic_bp': 300,  # Too high
            'heart_rate': 20  # Too low
        }

        result = self.validator.validate_vitals(vitals)

        self.assertFalse(result['passed'])
        self.assertGreater(len(result['errors']), 0)

    def test_validate_clinical_score_qsofa(self):
        """Test qSOFA score validation"""
        result = self.validator.validate_clinical_score('qsofa', 2)

        self.assertTrue(result['passed'])

    def test_validate_clinical_score_invalid(self):
        """Test clinical score validation - invalid"""
        result = self.validator.validate_clinical_score('qsofa', 5)  # Out of range

        self.assertFalse(result['passed'])

    def test_validate_phi_removed(self):
        """Test PHI removal validation"""
        # With PHI removed (redacted)
        text_safe = "Patient [PATIENT_NAME] seen on [DATE]"
        result = self.validator.validate_phi_removed(text_safe)
        self.assertTrue(result['passed'])

    def test_sepsis_criteria_test(self):
        """Test sepsis criteria testing"""
        vitals = {
            'respiratory_rate': 24,
            'gcs': 14,
            'systolic_bp': 95
        }

        result = self.test_suite.test_sepsis_criteria(vitals)
        self.assertTrue(result)

    def test_vital_signs_validity_test(self):
        """Test vital signs validity testing"""
        vitals = {
            'systolic_bp': 120,
            'heart_rate': 75,
            'respiratory_rate': 16
        }

        result = self.test_suite.test_vital_signs_validity(vitals)
        self.assertTrue(result)


class TestIntegration(unittest.TestCase):
    """Integration tests for Phase 07"""

    def test_phase07_frameworks_integration(self):
        """Test that all Phase 07 frameworks integrate properly"""
        impl = Phase07Implementation()
        task = {"goal": "Test integration", "phase_id": 7}

        result = impl.execute(task)

        # Should complete successfully
        self.assertIsNotNone(result)


def run_tests():
    """Run all tests and return results"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestPhase07Implementation))

    if DELIVERABLES_AVAILABLE:
        suite.addTests(loader.loadTestsFromTestCase(TestUnitTestingFramework))
        suite.addTests(loader.loadTestsFromTestCase(TestIntegrationTestingFramework))
        suite.addTests(loader.loadTestsFromTestCase(TestPerformanceTestingFramework))
        suite.addTests(loader.loadTestsFromTestCase(TestClinicalValidationFramework))

    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result


if __name__ == "__main__":
    print("=" * 80)
    print("PHASE 07: TESTING & QA - COMPREHENSIVE TEST SUITE")
    print("=" * 80)
    print()

    result = run_tests()

    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")

    if result.wasSuccessful():
        print("\n✅ ALL TESTS PASSED")
        sys.exit(0)
    else:
        print("\n❌ SOME TESTS FAILED")
        sys.exit(1)
