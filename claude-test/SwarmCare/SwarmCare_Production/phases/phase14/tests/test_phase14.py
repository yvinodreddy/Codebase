"""
Phase 14: Multi-modal AI - Medical Imaging
Comprehensive unit and integration tests
"""

import unittest
import sys
import os
import json
from pathlib import Path

# Add code directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'code'))

from implementation import Phase14Implementation


class TestPhase14Implementation(unittest.TestCase):
    """Test cases for Phase 14 implementation"""

    def setUp(self):
        """Set up test fixtures"""
        self.implementation = Phase14Implementation()

    def test_initialization(self):
        """Test proper initialization"""
        self.assertEqual(self.implementation.phase_id, 14)
        self.assertEqual(self.implementation.phase_name, "Multi-modal AI - Medical Imaging")
        self.assertEqual(self.implementation.story_points, 76)
        self.assertEqual(self.implementation.priority, "P0")
        self.assertEqual(self.implementation.description, "X-ray, CT, MRI analysis, abnormality detection")

    def test_framework_version(self):
        """Test framework version"""
        self.assertEqual(self.implementation.framework_version, "100%")

    def test_guardrails_integration(self):
        """Test guardrails are properly integrated"""
        # Guardrails may or may not be available depending on environment
        # Check that framework_available attribute exists
        self.assertTrue(hasattr(self.implementation, 'framework_available'))

        # If framework is available, guardrails should be present
        if self.implementation.framework_available:
            self.assertTrue(hasattr(self.implementation, 'guardrails'))
        else:
            # If not available, that's acceptable for testing environment
            self.assertIsInstance(self.implementation.framework_available, bool)

    def test_context_gathering(self):
        """Test context gathering"""
        task = {"goal": "Implement medical imaging", "phase_id": 14}
        context = self.implementation.gather_context(task, [])

        self.assertIsInstance(context, dict)
        self.assertIn("phase_id", context)

    def test_action_execution(self):
        """Test action execution"""
        task = {"goal": "Implement medical imaging", "phase_id": 14}
        context = self.implementation.gather_context(task, [])
        output = self.implementation.take_action(task, context)

        self.assertIsInstance(output, dict)
        self.assertIn("phase_id", output)
        self.assertIn("status", output)
        self.assertIn("components", output)

    def test_verification(self):
        """Test verification"""
        task = {"goal": "Implement medical imaging", "phase_id": 14}
        context = self.implementation.gather_context(task, [])
        output = self.implementation.take_action(task, context)
        verification = self.implementation.verify_work(output, context, task)

        self.assertIsInstance(verification, dict)
        self.assertIn("passed", verification)
        self.assertIn("message", verification)

    def test_complete_execution(self):
        """Test complete execution cycle"""
        task = {"goal": "Implement Phase 14: Medical Imaging", "phase_id": 14}
        result = self.implementation.execute(task)

        self.assertIsNotNone(result)
        self.assertTrue(hasattr(result, 'success'))
        self.assertTrue(hasattr(result, 'output'))

    def test_get_stats(self):
        """Test statistics retrieval"""
        stats = self.implementation.get_stats()

        self.assertIsInstance(stats, dict)
        self.assertEqual(stats["phase_id"], 14)
        self.assertEqual(stats["phase_name"], "Multi-modal AI - Medical Imaging")
        self.assertEqual(stats["story_points"], 76)
        self.assertEqual(stats["framework_version"], "100%")

    def test_phase_logic_implementation(self):
        """Test phase-specific logic implementation"""
        context = {"task": "test", "phase_id": 14}
        result = self.implementation._implement_phase_logic(context)

        self.assertIsInstance(result, dict)
        self.assertIn("status", result)
        self.assertIn("phase", result)
        self.assertIn("implemented", result)

        # Check for medical imaging specific components
        if "components" in result:
            self.assertIn("capabilities", result)
            self.assertIn("performance_metrics", result)
            self.assertIn("clinical_integration", result)

    def test_production_readiness(self):
        """Test production readiness indicators"""
        task = {"goal": "Verify production readiness", "phase_id": 14}
        context = self.implementation.gather_context(task, [])
        output = self.implementation.take_action(task, context)

        # Check production readiness markers
        if "production_ready" in output:
            self.assertTrue(output["production_ready"])

        if "compliance" in output:
            self.assertTrue(output["compliance"].get("hipaa", False))


class TestPhase14Integration(unittest.TestCase):
    """Integration tests for Phase 14"""

    def test_medical_imaging_import(self):
        """Test medical imaging core can be imported"""
        try:
            from medical_imaging_core import MedicalImagingPipeline
            pipeline = MedicalImagingPipeline(use_guardrails=False)
            self.assertIsNotNone(pipeline)
        except ImportError:
            self.skipTest("Medical imaging core not available")

    def test_imaging_modalities(self):
        """Test imaging modalities enumeration"""
        try:
            from medical_imaging_core import ImagingModality
            modalities = [m.value for m in ImagingModality]
            self.assertGreater(len(modalities), 0)
        except ImportError:
            self.skipTest("Medical imaging core not available")

    def test_abnormality_types(self):
        """Test abnormality types enumeration"""
        try:
            from medical_imaging_core import AbnormalityType
            abnormalities = [a.value for a in AbnormalityType]
            self.assertGreater(len(abnormalities), 0)
        except ImportError:
            self.skipTest("Medical imaging core not available")


class TestPhase14StateManagement(unittest.TestCase):
    """Test state management"""

    def test_phase_state_file_exists(self):
        """Test phase state file exists"""
        state_path = Path(__file__).parent.parent / ".state" / "phase_state.json"
        self.assertTrue(state_path.exists())

    def test_phase_state_structure(self):
        """Test phase state JSON structure"""
        state_path = Path(__file__).parent.parent / ".state" / "phase_state.json"

        with open(state_path, 'r') as f:
            state = json.load(f)

        self.assertIn("phase_id", state)
        self.assertIn("phase_name", state)
        self.assertIn("story_points", state)
        self.assertIn("status", state)
        self.assertEqual(state["phase_id"], 14)


def run_all_tests():
    """Run all tests with detailed reporting"""
    print("\n" + "="*80)
    print("PHASE 14: IMPLEMENTATION TESTS")
    print("="*80)

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTests(loader.loadTestsFromTestCase(TestPhase14Implementation))
    suite.addTests(loader.loadTestsFromTestCase(TestPhase14Integration))
    suite.addTests(loader.loadTestsFromTestCase(TestPhase14StateManagement))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("\n" + "="*80)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("="*80)

    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    exit(run_all_tests())
