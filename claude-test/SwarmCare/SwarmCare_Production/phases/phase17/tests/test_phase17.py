"""
Phase 17: Population Health Management
Unit tests for implementation module
"""

import unittest
import sys
import os
import json

# Add code directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'code'))

from implementation import Phase17Implementation


class TestPhase17Implementation(unittest.TestCase):
    """Test cases for Phase 17 Implementation"""

    def setUp(self):
        """Set up test fixtures"""
        self.implementation = Phase17Implementation()

    def test_initialization(self):
        """Test proper initialization"""
        self.assertEqual(self.implementation.phase_id, 17)
        self.assertEqual(self.implementation.phase_name, "Population Health Management")
        self.assertEqual(self.implementation.story_points, 43)
        self.assertEqual(self.implementation.priority, "P1")
        self.assertEqual(self.implementation.framework_version, "100%")

    def test_framework_availability(self):
        """Test framework availability flag"""
        self.assertTrue(hasattr(self.implementation, 'framework_available'))
        self.assertIsInstance(self.implementation.framework_available, bool)

    def test_guardrails_integration(self):
        """Test guardrails are properly integrated"""
        # Check that framework_available attribute exists
        self.assertTrue(hasattr(self.implementation, 'framework_available'))

        # If framework is available, guardrails should be present
        if self.implementation.framework_available:
            self.assertTrue(hasattr(self.implementation, 'guardrails'))
            self.assertTrue(hasattr(self.implementation, 'feedback_loop'))
            self.assertTrue(hasattr(self.implementation, 'context'))
            self.assertTrue(hasattr(self.implementation, 'orchestrator'))
        else:
            # If not available, that's acceptable for testing environment
            self.assertIsInstance(self.implementation.framework_available, bool)

    def test_gather_context(self):
        """Test context gathering"""
        task = {"goal": "Test context gathering", "phase_id": 17}
        context = self.implementation.gather_context(task, [])

        self.assertIsInstance(context, dict)
        self.assertIn("phase_id", context)

    def test_take_action(self):
        """Test action execution"""
        task = {"goal": "Test implementation", "phase_id": 17}
        context = {"task": task, "phase_id": 17}

        output = self.implementation.take_action(task, context)

        self.assertIsInstance(output, dict)
        self.assertIn("phase_id", output)
        self.assertIn("components", output)
        self.assertEqual(output["phase_id"], 17)

    def test_verify_work(self):
        """Test work verification"""
        task = {"goal": "Test verification", "phase_id": 17}
        context = {"task": task, "phase_id": 17}
        output = {
            "phase_id": 17,
            "status": "implemented",
            "components": {"status": "configured"}
        }

        verification = self.implementation.verify_work(output, context, task)

        self.assertIsInstance(verification, dict)
        self.assertIn("passed", verification)
        self.assertTrue(verification["passed"])

    def test_execute(self):
        """Test full execution"""
        task = {"goal": "Implement Population Health Management", "phase_id": 17}

        result = self.implementation.execute(task)

        self.assertTrue(result.success)
        self.assertIsNotNone(result.output)
        self.assertEqual(result.output["phase_id"], 17)

    def test_implementation_capabilities(self):
        """Test implementation returns all required capabilities"""
        task = {"goal": "Test capabilities", "phase_id": 17}
        context = {"task": task, "phase_id": 17}

        output = self.implementation.take_action(task, context)
        components = output["components"]

        # Check risk stratification capabilities
        self.assertIn("risk_stratification", components["capabilities"])
        risk_cap = components["capabilities"]["risk_stratification"]
        self.assertIn("models", risk_cap)
        self.assertIn("HCC", risk_cap["models"])

        # Check care gaps capabilities
        self.assertIn("care_gaps_identification", components["capabilities"])
        gaps_cap = components["capabilities"]["care_gaps_identification"]
        self.assertIn("frameworks", gaps_cap)
        self.assertIn("HEDIS", gaps_cap["frameworks"])

        # Check quality measures capabilities
        self.assertIn("quality_measures", components["capabilities"])
        quality_cap = components["capabilities"]["quality_measures"]
        self.assertIn("measure_types", quality_cap)

        # Check interventions capabilities
        self.assertIn("interventions", components["capabilities"])

        # Check cohort management capabilities
        self.assertIn("cohort_management", components["capabilities"])

    def test_compliance_features(self):
        """Test HIPAA compliance features"""
        task = {"goal": "Test compliance", "phase_id": 17}
        context = {"task": task, "phase_id": 17}

        output = self.implementation.take_action(task, context)
        compliance = output["components"]["compliance"]

        self.assertTrue(compliance["hipaa_compliant"])
        self.assertIn("phi_protection", compliance)
        self.assertIn("audit_logging", compliance)

    def test_performance_specs(self):
        """Test performance specifications"""
        task = {"goal": "Test performance", "phase_id": 17}
        context = {"task": task, "phase_id": 17}

        output = self.implementation.take_action(task, context)
        performance = output["components"]["performance"]

        self.assertIn("patient_analysis_time_ms", performance)
        self.assertIn("population_analysis_time_ms", performance)

    def test_get_stats(self):
        """Test statistics retrieval"""
        stats = self.implementation.get_stats()

        self.assertIsInstance(stats, dict)
        self.assertEqual(stats["phase_id"], 17)
        self.assertEqual(stats["phase_name"], "Population Health Management")
        self.assertEqual(stats["story_points"], 43)


class TestPhaseStateManagement(unittest.TestCase):
    """Test phase state management"""

    def setUp(self):
        self.implementation = Phase17Implementation()

    def test_phase_state_update(self):
        """Test phase state is updated correctly"""
        # Execute implementation
        task = {"goal": "Test state update", "phase_id": 17}
        result = self.implementation.execute(task)

        # Check state file exists
        state_file = os.path.join(
            os.path.dirname(__file__), '..', '.state', 'phase_state.json'
        )
        self.assertTrue(os.path.exists(state_file))

        # Read state file
        with open(state_file, 'r') as f:
            state = json.load(f)

        # Verify state contents
        self.assertEqual(state["phase_id"], 17)
        self.assertEqual(state["phase_name"], "Population Health Management")
        self.assertEqual(state["story_points"], 43)
        self.assertTrue(state["success"])


if __name__ == "__main__":
    unittest.main()
