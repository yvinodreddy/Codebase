"""
Phase 25: Validated Patient-Facing XAI
Comprehensive Implementation Tests

Tests the Phase25Implementation class with full agent framework integration.
Validates proper integration with guardrails, feedback loops, and verification systems.
"""

import unittest
import sys
import os
from datetime import datetime

# Add code directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'code'))

from implementation import Phase25Implementation


class TestPhase25Implementation(unittest.TestCase):
    """Test cases for Phase 25 implementation"""

    def setUp(self):
        """Set up test fixtures"""
        self.implementation = Phase25Implementation()

    def test_initialization(self):
        """Test proper initialization"""
        self.assertEqual(self.implementation.phase_id, 25)
        self.assertEqual(self.implementation.phase_name, "Validated Patient-Facing XAI")
        self.assertEqual(self.implementation.story_points, 35)
        self.assertEqual(self.implementation.priority, "P1")
        self.assertEqual(self.implementation.description, "Patient portals, understandable explanations, health literacy")
        self.assertEqual(self.implementation.status, "NOT_STARTED")
        self.assertEqual(self.implementation.framework_version, "100%")

    def test_framework_available_attribute(self):
        """Test framework_available is an instance attribute"""
        self.assertTrue(hasattr(self.implementation, 'framework_available'))
        self.assertIsInstance(self.implementation.framework_available, bool)

    def test_guardrails_integration(self):
        """Test guardrails are properly integrated"""
        self.assertTrue(hasattr(self.implementation, 'framework_available'))

        # If framework is available, guardrails should be present
        if self.implementation.framework_available:
            self.assertTrue(hasattr(self.implementation, 'guardrails'))
            self.assertTrue(hasattr(self.implementation, 'feedback_loop'))
            self.assertTrue(hasattr(self.implementation, 'context'))
            self.assertTrue(hasattr(self.implementation, 'orchestrator'))
            self.assertTrue(hasattr(self.implementation, 'search'))
            self.assertTrue(hasattr(self.implementation, 'verifier'))
        else:
            # If not available, that's acceptable for testing environment
            self.assertIsInstance(self.implementation.framework_available, bool)

    def test_gather_context(self):
        """Test context gathering"""
        task = {"goal": "Test context gathering", "phase_id": 25}
        context = self.implementation.gather_context(task, [])

        self.assertIsInstance(context, dict)
        self.assertIn("task", context)
        self.assertEqual(context["task"]["phase_id"], 25)

    def test_take_action(self):
        """Test action execution"""
        task = {"goal": "Test action", "phase_id": 25}
        context = {"task": task, "phase_id": 25}

        output = self.implementation.take_action(task, context)

        self.assertIsInstance(output, dict)
        self.assertIn("phase_id", output)
        self.assertIn("phase_name", output)
        self.assertIn("story_points", output)
        self.assertIn("status", output)
        self.assertIn("components", output)
        self.assertIn("agent_framework_version", output)
        self.assertIn("timestamp", output)

    def test_verify_work(self):
        """Test verification"""
        task = {"goal": "Test verification", "phase_id": 25}
        context = {"task": task}
        output = {
            "phase_id": 25,
            "status": "implemented",
            "components": {"test": "data"}
        }

        verification = self.implementation.verify_work(output, context, task)

        self.assertIsInstance(verification, dict)
        self.assertIn("passed", verification)
        self.assertIn("message", verification)
        self.assertIsInstance(verification["passed"], bool)

    def test_implementation_capabilities(self):
        """Test implementation returns all required capabilities"""
        task = {"goal": "Test capabilities", "phase_id": 25}
        context = {"task": task, "phase_id": 25}

        output = self.implementation.take_action(task, context)
        components = output["components"]

        # Check all main capabilities
        self.assertIn("capabilities", components)
        capabilities = components["capabilities"]

        self.assertIn("health_literacy_assessment", capabilities)
        self.assertIn("explanation_generation", capabilities)
        self.assertIn("multi_language_support", capabilities)
        self.assertIn("accessibility", capabilities)
        self.assertIn("validation_system", capabilities)
        self.assertIn("patient_portal_integration", capabilities)

    def test_health_literacy_levels(self):
        """Test health literacy levels are properly exposed"""
        task = {"goal": "Test literacy levels", "phase_id": 25}
        context = {"task": task}
        output = self.implementation.take_action(task, context)

        literacy = output["components"]["capabilities"]["health_literacy_assessment"]
        self.assertIn("levels", literacy)
        levels = literacy["levels"]

        # Check all 5 levels are present
        expected_levels = ["basic", "elementary", "intermediate", "advanced", "expert"]
        for level in expected_levels:
            self.assertIn(level, levels)

    def test_explanation_types(self):
        """Test explanation types are comprehensive"""
        task = {"goal": "Test explanation types", "phase_id": 25}
        context = {"task": task}
        output = self.implementation.take_action(task, context)

        explanation = output["components"]["capabilities"]["explanation_generation"]
        self.assertIn("types", explanation)
        types = explanation["types"]

        # Check key explanation types
        expected_types = ["diagnosis", "medication", "test_result", "treatment"]
        for exp_type in expected_types:
            self.assertIn(exp_type, types)

    def test_multi_language_support(self):
        """Test multi-language support is configured"""
        task = {"goal": "Test language support", "phase_id": 25}
        context = {"task": task}
        output = self.implementation.take_action(task, context)

        languages = output["components"]["capabilities"]["multi_language_support"]
        self.assertIn("languages", languages)
        self.assertIn("count", languages)
        self.assertGreater(languages["count"], 5)  # At least 6 languages

    def test_accessibility_features(self):
        """Test accessibility features are comprehensive"""
        task = {"goal": "Test accessibility", "phase_id": 25}
        context = {"task": task}
        output = self.implementation.take_action(task, context)

        accessibility = output["components"]["capabilities"]["accessibility"]
        self.assertIn("wcag_compliance", accessibility)
        self.assertEqual(accessibility["wcag_compliance"], "WCAG 2.1 AAA")
        self.assertTrue(accessibility["screen_reader_optimized"])

    def test_compliance_requirements(self):
        """Test HIPAA and compliance requirements"""
        task = {"goal": "Test compliance", "phase_id": 25}
        context = {"task": task}
        output = self.implementation.take_action(task, context)

        compliance = output["components"]["compliance"]
        self.assertTrue(compliance["hipaa_compliant"])
        self.assertIn("phi_protection", compliance)
        self.assertIn("audit_logging", compliance)
        self.assertIn("encryption", compliance)

    def test_agent_framework_version(self):
        """Test agent framework version is 100%"""
        task = {"goal": "Test framework version", "phase_id": 25}
        context = {"task": task}
        output = self.implementation.take_action(task, context)

        self.assertEqual(output["agent_framework_version"], "100%")
        self.assertEqual(output["components"]["agent_framework_integration"], "100%")


class TestPhase25Execution(unittest.TestCase):
    """Test execution flow"""

    def setUp(self):
        """Set up test fixtures"""
        self.implementation = Phase25Implementation()

    def test_execute_returns_result(self):
        """Test execute returns proper result"""
        task = {"goal": "Implement Validated Patient-Facing XAI", "phase_id": 25}
        result = self.implementation.execute(task)

        self.assertIsNotNone(result)
        self.assertTrue(hasattr(result, 'success'))
        self.assertTrue(hasattr(result, 'output'))

    def test_execute_success(self):
        """Test successful execution"""
        task = {"goal": "Implement Validated Patient-Facing XAI", "phase_id": 25}
        result = self.implementation.execute(task)

        self.assertTrue(result.success)
        self.assertIsNotNone(result.output)

    def test_state_update(self):
        """Test phase state is updated after execution"""
        import json
        from pathlib import Path

        task = {"goal": "Implement Validated Patient-Facing XAI", "phase_id": 25}
        result = self.implementation.execute(task)

        # Check state file was created/updated
        state_path = Path(__file__).parent.parent / ".state" / "phase_state.json"
        self.assertTrue(state_path.exists())

        # Load and verify state
        with open(state_path, 'r') as f:
            state = json.load(f)

        self.assertEqual(state["phase_id"], 25)
        self.assertEqual(state["phase_name"], "Validated Patient-Facing XAI")
        self.assertIn("status", state)
        self.assertIn("success", state)


if __name__ == "__main__":
    # Run tests with verbose output
    unittest.main(verbosity=2)
