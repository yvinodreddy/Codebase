"""
Phase 09: Documentation - Comprehensive Test Suite
Production-ready tests with 100% coverage target

Tests documentation generation system including:
- Technical documentation
- User guides
- Tutorials
- API documentation
- Deployment documentation
"""

import unittest
import sys
import os
import json
from datetime import datetime

# Add code directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'code'))

from implementation import Phase09Implementation


class TestPhase09Initialization(unittest.TestCase):
    """Test Phase 09 initialization and setup"""

    def setUp(self):
        """Set up test fixtures"""
        self.implementation = Phase09Implementation()

    def test_phase_metadata(self):
        """Test phase metadata is correct"""
        self.assertEqual(self.implementation.phase_id, 9)
        self.assertEqual(self.implementation.phase_name, "Documentation")
        self.assertEqual(self.implementation.story_points, 21)
        self.assertEqual(self.implementation.priority, "P1")
        self.assertIn("Technical docs", self.implementation.description)

    def test_framework_initialization(self):
        """Test agent framework components are initialized"""
        self.assertIsNotNone(self.implementation)
        self.assertEqual(self.implementation.framework_version, "100%")

    def test_initial_status(self):
        """Test initial status is NOT_STARTED"""
        self.assertEqual(self.implementation.status, "NOT_STARTED")


class TestDocumentationTypes(unittest.TestCase):
    """Test all documentation types"""

    def setUp(self):
        """Set up test fixtures"""
        self.implementation = Phase09Implementation()

    def test_technical_documentation(self):
        """Test technical documentation initialization"""
        tech_docs = self.implementation._init_technical_docs()

        self.assertEqual(tech_docs["name"], "Technical Documentation")
        self.assertEqual(tech_docs["status"], "initialized")
        self.assertGreaterEqual(len(tech_docs["components"]), 8)
        self.assertIn("Architecture diagrams", tech_docs["components"])
        self.assertIn("Markdown", tech_docs["formats"])
        self.assertTrue(tech_docs["auto_generated"])

    def test_user_guides(self):
        """Test user guides initialization"""
        user_guides = self.implementation._init_user_guides()

        self.assertEqual(user_guides["name"], "User Guides")
        self.assertEqual(user_guides["status"], "initialized")
        self.assertGreaterEqual(len(user_guides["components"]), 8)
        self.assertIn("Clinicians", user_guides["target_audiences"])
        self.assertIn("Getting started guide", user_guides["components"])

    def test_tutorials(self):
        """Test tutorials initialization"""
        tutorials = self.implementation._init_tutorials()

        self.assertEqual(tutorials["name"], "Tutorials")
        self.assertEqual(tutorials["status"], "initialized")
        self.assertGreaterEqual(len(tutorials["tutorial_categories"]), 8)
        self.assertIn("Beginner", tutorials["difficulty_levels"])
        self.assertIn("Video tutorials", tutorials["delivery_methods"])

    def test_api_documentation(self):
        """Test API documentation initialization"""
        api_docs = self.implementation._init_api_docs()

        self.assertEqual(api_docs["name"], "API Documentation")
        self.assertEqual(api_docs["status"], "initialized")
        self.assertGreaterEqual(len(api_docs["components"]), 8)
        self.assertEqual(api_docs["api_specifications"]["openapi_version"], "3.1.0")
        self.assertIn("python", api_docs["languages"])

    def test_deployment_documentation(self):
        """Test deployment documentation initialization"""
        deployment_docs = self.implementation._init_deployment_docs()

        self.assertEqual(deployment_docs["name"], "Deployment Documentation")
        self.assertEqual(deployment_docs["status"], "initialized")
        self.assertGreaterEqual(len(deployment_docs["components"]), 10)
        self.assertIn("Kubernetes", deployment_docs["deployment_targets"])
        self.assertIn("terraform", deployment_docs["automation"])


class TestGenerationTools(unittest.TestCase):
    """Test documentation generation tools"""

    def setUp(self):
        """Set up test fixtures"""
        self.implementation = Phase09Implementation()

    def test_static_site_generators(self):
        """Test static site generators configuration"""
        tools = self.implementation._init_generation_tools()

        self.assertIn("static_site_generators", tools)
        self.assertIn("mkdocs", tools["static_site_generators"])
        self.assertTrue(tools["static_site_generators"]["mkdocs"]["enabled"])
        self.assertIn("sphinx", tools["static_site_generators"])
        self.assertIn("docusaurus", tools["static_site_generators"])

    def test_api_doc_generators(self):
        """Test API documentation generators"""
        tools = self.implementation._init_generation_tools()

        self.assertIn("api_doc_generators", tools)
        self.assertEqual(tools["api_doc_generators"]["swagger_ui"], "Enabled")
        self.assertEqual(tools["api_doc_generators"]["redoc"], "Enabled")

    def test_diagram_tools(self):
        """Test diagram tools configuration"""
        tools = self.implementation._init_generation_tools()

        self.assertIn("diagram_tools", tools)
        self.assertEqual(tools["diagram_tools"]["mermaid"], "Enabled")
        self.assertEqual(tools["diagram_tools"]["plantuml"], "Enabled")
        self.assertEqual(tools["diagram_tools"]["graphviz"], "Enabled")

    def test_linters(self):
        """Test linter configuration"""
        tools = self.implementation._init_generation_tools()

        self.assertIn("linters", tools)
        self.assertEqual(tools["linters"]["markdownlint"], "Enabled")
        self.assertIn("vale", tools["linters"])

    def test_automation(self):
        """Test automation features"""
        tools = self.implementation._init_generation_tools()

        self.assertIn("automation", tools)
        self.assertTrue(tools["automation"]["auto_build_on_commit"])
        self.assertTrue(tools["automation"]["auto_deploy_to_docs_site"])


class TestPhaseExecution(unittest.TestCase):
    """Test phase execution logic"""

    def setUp(self):
        """Set up test fixtures"""
        self.implementation = Phase09Implementation()

    def test_gather_context(self):
        """Test context gathering"""
        task = {"goal": "Implement Documentation", "phase_id": 9}
        context = self.implementation.gather_context(task, [])

        self.assertIsNotNone(context)
        self.assertIsInstance(context, dict)

    def test_take_action(self):
        """Test action execution"""
        task = {"goal": "Implement Documentation", "phase_id": 9}
        context = {"task": task, "phase_id": 9}

        output = self.implementation.take_action(task, context)

        self.assertIsNotNone(output)
        self.assertEqual(output["phase_id"], 9)
        self.assertEqual(output["status"], "implemented")
        self.assertIn("components", output)

    def test_verify_work(self):
        """Test work verification"""
        task = {"goal": "Implement Documentation", "phase_id": 9}
        context = {"task": task, "phase_id": 9}
        output = self.implementation.take_action(task, context)

        verification = self.implementation.verify_work(output, context, task)

        self.assertIsNotNone(verification)
        self.assertIn("passed", verification)
        self.assertIn("message", verification)

    def test_full_execution(self):
        """Test full phase execution"""
        task = {"goal": "Implement Documentation", "phase_id": 9}

        result = self.implementation.execute(task)

        self.assertIsNotNone(result)
        self.assertTrue(result.success)
        self.assertIsNotNone(result.output)
        self.assertEqual(result.output["phase_id"], 9)

    def test_get_stats(self):
        """Test statistics retrieval"""
        stats = self.implementation.get_stats()

        self.assertEqual(stats["phase_id"], 9)
        self.assertEqual(stats["phase_name"], "Documentation")
        self.assertEqual(stats["story_points"], 21)
        self.assertEqual(stats["framework_version"], "100%")


class TestDocumentationStatistics(unittest.TestCase):
    """Test documentation statistics calculation"""

    def setUp(self):
        """Set up test fixtures"""
        self.implementation = Phase09Implementation()

    def test_statistics_calculation(self):
        """Test statistics are calculated correctly"""
        task = {"goal": "Implement Documentation", "phase_id": 9}
        context = {"task": task, "phase_id": 9}
        output = self.implementation.take_action(task, context)

        stats = output["components"]["statistics"]

        self.assertEqual(stats["total_documentation_types"], 5)
        self.assertGreater(stats["total_components"], 0)
        self.assertGreater(stats["generation_tools_count"], 0)
        self.assertTrue(stats["all_initialized"])
        self.assertEqual(stats["framework_integration"], "100%")

    def test_component_counts(self):
        """Test component counts are accurate"""
        tech_docs = self.implementation._init_technical_docs()
        user_guides = self.implementation._init_user_guides()
        tutorials = self.implementation._init_tutorials()
        api_docs = self.implementation._init_api_docs()
        deployment = self.implementation._init_deployment_docs()

        total = (len(tech_docs["components"]) +
                len(user_guides["components"]) +
                len(tutorials["tutorial_categories"]) +
                len(api_docs["components"]) +
                len(deployment["components"]))

        self.assertGreater(total, 40)  # Should have 40+ components total


class TestDocumentationComponents(unittest.TestCase):
    """Test specific documentation components"""

    def setUp(self):
        """Set up test fixtures"""
        self.implementation = Phase09Implementation()

    def test_technical_docs_components(self):
        """Test technical documentation has all required components"""
        tech_docs = self.implementation._init_technical_docs()
        required = ["Architecture diagrams", "API specifications",
                   "Security documentation"]

        for component in required:
            self.assertIn(component, tech_docs["components"])

    def test_user_guide_audiences(self):
        """Test user guides target all required audiences"""
        user_guides = self.implementation._init_user_guides()
        required_audiences = ["Clinicians", "Administrators"]

        for audience in required_audiences:
            self.assertIn(audience, user_guides["target_audiences"])

    def test_tutorial_difficulty_levels(self):
        """Test tutorials have all difficulty levels"""
        tutorials = self.implementation._init_tutorials()
        required_levels = ["Beginner", "Intermediate", "Advanced"]

        for level in required_levels:
            self.assertIn(level, tutorials["difficulty_levels"])

    def test_api_docs_languages(self):
        """Test API documentation supports multiple languages"""
        api_docs = self.implementation._init_api_docs()
        required_languages = ["python", "javascript", "typescript"]

        for lang in required_languages:
            self.assertIn(lang, api_docs["languages"])

    def test_deployment_targets(self):
        """Test deployment documentation covers all targets"""
        deployment = self.implementation._init_deployment_docs()
        required_targets = ["Kubernetes", "Docker Compose", "Azure"]

        for target in required_targets:
            self.assertIn(target, deployment["deployment_targets"])


class TestDocumentationFormats(unittest.TestCase):
    """Test documentation format support"""

    def setUp(self):
        """Set up test fixtures"""
        self.implementation = Phase09Implementation()

    def test_technical_docs_formats(self):
        """Test technical documentation supports required formats"""
        tech_docs = self.implementation._init_technical_docs()
        required_formats = ["Markdown", "HTML", "PDF"]

        for fmt in required_formats:
            self.assertIn(fmt, tech_docs["formats"])

    def test_user_guides_formats(self):
        """Test user guides support multimedia formats"""
        user_guides = self.implementation._init_user_guides()

        self.assertIn("Video", user_guides["formats"])
        self.assertIn("Interactive", user_guides["formats"])

    def test_tutorial_delivery_methods(self):
        """Test tutorials support multiple delivery methods"""
        tutorials = self.implementation._init_tutorials()
        required_methods = ["Text-based tutorials", "Video tutorials"]

        for method in required_methods:
            self.assertIn(method, tutorials["delivery_methods"])


def run_test_suite():
    """Run the complete test suite and return results"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestPhase09Initialization))
    suite.addTests(loader.loadTestsFromTestCase(TestDocumentationTypes))
    suite.addTests(loader.loadTestsFromTestCase(TestGenerationTools))
    suite.addTests(loader.loadTestsFromTestCase(TestPhaseExecution))
    suite.addTests(loader.loadTestsFromTestCase(TestDocumentationStatistics))
    suite.addTests(loader.loadTestsFromTestCase(TestDocumentationComponents))
    suite.addTests(loader.loadTestsFromTestCase(TestDocumentationFormats))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result


if __name__ == "__main__":
    print("=" * 80)
    print("PHASE 09: DOCUMENTATION - COMPREHENSIVE TEST SUITE")
    print("=" * 80)
    print(f"Test Run: {datetime.now().isoformat()}")
    print("=" * 80)
    print()

    result = run_test_suite()

    print()
    print("=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    print(f"Tests Run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success Rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    print("=" * 80)

    sys.exit(0 if result.wasSuccessful() else 1)
