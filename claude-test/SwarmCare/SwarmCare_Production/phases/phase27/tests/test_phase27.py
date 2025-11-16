"""
Phase 27: Full Trial Lifecycle (EDC, eConsent, AE)
Unit tests
"""

import unittest
import sys
import os

# Add code directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'code'))

from implementation import Phase27Implementation


class TestPhase27(unittest.TestCase):
    """Test cases for Phase 27"""

    def setUp(self):
        """Set up test fixtures"""
        self.implementation = Phase27Implementation()

    def test_initialization(self):
        """Test proper initialization"""
        self.assertEqual(self.implementation.phase_id, 27)
        self.assertEqual(self.implementation.phase_name, "Full Trial Lifecycle (EDC, eConsent, AE)")
        self.assertEqual(self.implementation.story_points, 45)
        self.assertEqual(self.implementation.priority, "P1")

    def test_framework_available_attribute(self):
        """Test framework_available is an instance attribute"""
        self.assertTrue(hasattr(self.implementation, 'framework_available'))
        self.assertIsInstance(self.implementation.framework_available, bool)

    def test_guardrails_integration(self):
        """Test guardrails are properly integrated"""
        if self.implementation.framework_available:
            self.assertTrue(hasattr(self.implementation, 'guardrails'))
            self.assertTrue(hasattr(self.implementation, 'feedback_loop'))
            self.assertTrue(hasattr(self.implementation, 'context'))
            self.assertTrue(hasattr(self.implementation, 'orchestrator'))
            self.assertTrue(hasattr(self.implementation, 'search'))
            self.assertTrue(hasattr(self.implementation, 'verifier'))

    def test_take_action(self):
        """Test take_action returns proper output"""
        task = {"goal": "Implement Phase 27", "phase_id": 27}
        context = {"task": task, "phase_id": 27}

        output = self.implementation.take_action(task, context)

        self.assertIn("phase_id", output)
        self.assertIn("components", output)
        self.assertIn("status", output)
        self.assertEqual(output["phase_id"], 27)
        self.assertEqual(output["status"], "implemented")

    def test_trial_management_capabilities(self):
        """Test trial management capabilities are exposed"""
        task = {"goal": "Implement Phase 27", "phase_id": 27}
        context = {"task": task, "phase_id": 27}
        output = self.implementation.take_action(task, context)

        trial_mgmt = output["components"]["capabilities"]["trial_management"]
        self.assertIn("features", trial_mgmt)
        self.assertIn("trial_phases", trial_mgmt)
        self.assertIn("Trial creation and protocol management", trial_mgmt["features"])

    def test_electronic_consent_capabilities(self):
        """Test eConsent capabilities are exposed"""
        task = {"goal": "Implement Phase 27", "phase_id": 27}
        context = {"task": task, "phase_id": 27}
        output = self.implementation.take_action(task, context)

        econsent = output["components"]["capabilities"]["electronic_consent"]
        self.assertIn("features", econsent)
        self.assertIn("comprehension_questions", econsent)
        self.assertEqual(econsent["pass_threshold"], "80% (4 out of 5 questions)")

    def test_adverse_event_capabilities(self):
        """Test AE reporting capabilities are exposed"""
        task = {"goal": "Implement Phase 27", "phase_id": 27}
        context = {"task": task, "phase_id": 27}
        output = self.implementation.take_action(task, context)

        ae = output["components"]["capabilities"]["adverse_event_reporting"]
        self.assertIn("severity_grades", ae)
        self.assertIn("causality_levels", ae)
        self.assertIn("sae_criteria", ae)
        self.assertEqual(ae["severity_grades"]["Grade 5"], "Death")

    def test_edc_capabilities(self):
        """Test EDC capabilities are exposed"""
        task = {"goal": "Implement Phase 27", "phase_id": 27}
        context = {"task": task, "phase_id": 27}
        output = self.implementation.take_action(task, context)

        edc = output["components"]["capabilities"]["electronic_data_capture"]
        self.assertIn("features", edc)
        self.assertIn("validation_rules", edc)
        self.assertIn("cdisc_compliance", edc)
        self.assertEqual(edc["cdisc_compliance"], "SDTM (Study Data Tabulation Model)")

    def test_regulatory_compliance(self):
        """Test regulatory compliance standards"""
        task = {"goal": "Implement Phase 27", "phase_id": 27}
        context = {"task": task, "phase_id": 27}
        output = self.implementation.take_action(task, context)

        compliance = output["components"]["capabilities"]["regulatory_compliance"]
        self.assertIn("standards", compliance)
        self.assertIn("21_CFR_Part_11", compliance["standards"])
        self.assertIn("GCP", compliance["standards"])
        self.assertIn("HIPAA", compliance["standards"])
        self.assertIn("GDPR", compliance["standards"])
        self.assertIn("CDISC", compliance["standards"])

    def test_audit_trail_features(self):
        """Test audit trail features"""
        task = {"goal": "Implement Phase 27", "phase_id": 27}
        context = {"task": task, "phase_id": 27}
        output = self.implementation.take_action(task, context)

        audit = output["components"]["capabilities"]["audit_trails"]
        self.assertIn("features", audit)
        self.assertIn("logged_actions", audit)
        self.assertIn("Complete audit logging (21 CFR Part 11 compliant)", audit["features"])

    def test_reporting_dashboards(self):
        """Test reporting dashboards"""
        task = {"goal": "Implement Phase 27", "phase_id": 27}
        context = {"task": task, "phase_id": 27}
        output = self.implementation.take_action(task, context)

        dashboards = output["components"]["capabilities"]["reporting_dashboards"]
        self.assertIn("trial_dashboard", dashboards)
        trial_dashboard = dashboards["trial_dashboard"]
        self.assertIn("enrollment_metrics", trial_dashboard)
        self.assertIn("safety_metrics", trial_dashboard)
        self.assertIn("data_quality_metrics", trial_dashboard)

    def test_system_integration(self):
        """Test system integration"""
        task = {"goal": "Implement Phase 27", "phase_id": 27}
        context = {"task": task, "phase_id": 27}
        output = self.implementation.take_action(task, context)

        integration = output["components"]["capabilities"]["system_integration"]
        self.assertTrue(integration["integrated"])
        self.assertTrue(integration["zero_dependencies"])
        self.assertTrue(integration["python_stdlib_only"])
        self.assertEqual(len(integration["components"]), 4)

    def test_production_ready(self):
        """Test production ready flag"""
        task = {"goal": "Implement Phase 27", "phase_id": 27}
        context = {"task": task, "phase_id": 27}
        output = self.implementation.take_action(task, context)

        self.assertTrue(output["components"]["production_ready"])
        self.assertEqual(output["components"]["agent_framework_integration"], "100%")

    def test_verify_work(self):
        """Test verification works properly"""
        task = {"goal": "Implement Phase 27", "phase_id": 27}
        context = {"task": task, "phase_id": 27}
        output = self.implementation.take_action(task, context)

        verification = self.implementation.verify_work(output, context, task)

        self.assertIn("passed", verification)
        self.assertIn("message", verification)
        self.assertTrue(verification["passed"])

    def test_get_stats(self):
        """Test statistics retrieval"""
        stats = self.implementation.get_stats()

        self.assertEqual(stats["phase_id"], 27)
        self.assertEqual(stats["phase_name"], "Full Trial Lifecycle (EDC, eConsent, AE)")
        self.assertEqual(stats["story_points"], 45)
        self.assertEqual(stats["framework_version"], "100%")


if __name__ == "__main__":
    unittest.main()
