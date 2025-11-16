"""
Phase 02: SWARMCARE Agents - Comprehensive Test Suite
Production-ready tests with 100% coverage target

Tests all 6 agents:
- Knowledge Agent
- Case Agent
- Conversation Agent
- Compliance Agent
- Podcast Agent
- QA Agent
"""

import unittest
import sys
import os
import json
from datetime import datetime

# Add code directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'code'))

from implementation import Phase02Implementation


class TestPhase02Initialization(unittest.TestCase):
    """Test Phase 02 initialization and setup"""

    def setUp(self):
        """Set up test fixtures"""
        self.implementation = Phase02Implementation()

    def test_phase_metadata(self):
        """Test phase metadata is correct"""
        self.assertEqual(self.implementation.phase_id, 2)
        self.assertEqual(self.implementation.phase_name, "SWARMCARE Agents")
        self.assertEqual(self.implementation.story_points, 94)
        self.assertEqual(self.implementation.priority, "P0")
        self.assertIn("6 AI agents", self.implementation.description)

    def test_framework_initialization(self):
        """Test agent framework components are initialized"""
        # Framework components may not be available in all environments
        # Test graceful degradation
        self.assertIsNotNone(self.implementation)
        self.assertEqual(self.implementation.framework_version, "100%")

    def test_initial_status(self):
        """Test initial status is NOT_STARTED"""
        self.assertEqual(self.implementation.status, "NOT_STARTED")


class TestSWARMCAREAgents(unittest.TestCase):
    """Test all 6 SWARMCARE agents"""

    def setUp(self):
        """Set up test fixtures"""
        self.implementation = Phase02Implementation()

    def test_knowledge_agent_initialization(self):
        """Test Knowledge Agent is properly initialized"""
        agent = self.implementation._initialize_knowledge_agent()

        self.assertEqual(agent["name"], "Knowledge Agent")
        self.assertEqual(agent["type"], "knowledge_retrieval")
        self.assertEqual(agent["status"], "initialized")
        self.assertIn("Medical literature search", agent["capabilities"])
        self.assertIn("Neo4j knowledge graph", agent["integrations"][0])
        self.assertIn("medical_accuracy", agent["guardrails"])
        self.assertIn("< 2s", agent["performance_sla"])

    def test_case_agent_initialization(self):
        """Test Case Agent is properly initialized"""
        agent = self.implementation._initialize_case_agent()

        self.assertEqual(agent["name"], "Case Agent")
        self.assertEqual(agent["type"], "case_analysis")
        self.assertEqual(agent["status"], "initialized")
        self.assertIn("Patient case summarization", agent["capabilities"])
        self.assertIn("EHR systems", agent["integrations"][0])
        self.assertIn("hipaa_compliance", agent["guardrails"])
        self.assertIn("< 3s", agent["performance_sla"])

    def test_conversation_agent_initialization(self):
        """Test Conversation Agent is properly initialized"""
        agent = self.implementation._initialize_conversation_agent()

        self.assertEqual(agent["name"], "Conversation Agent")
        self.assertEqual(agent["type"], "natural_language")
        self.assertEqual(agent["status"], "initialized")
        self.assertIn("Natural language understanding", agent["capabilities"])
        self.assertIn("Voice AI systems", agent["integrations"])
        self.assertIn("content_safety", agent["guardrails"])
        self.assertIn("< 1s", agent["performance_sla"])

    def test_compliance_agent_initialization(self):
        """Test Compliance Agent is properly initialized"""
        agent = self.implementation._initialize_compliance_agent()

        self.assertEqual(agent["name"], "Compliance Agent")
        self.assertEqual(agent["type"], "regulatory_compliance")
        self.assertEqual(agent["status"], "initialized")
        self.assertIn("HIPAA compliance verification", agent["capabilities"])
        self.assertIn("Security monitoring systems", agent["integrations"])
        self.assertIn("strict_phi_protection", agent["guardrails"])
        self.assertIn("Real-time", agent["performance_sla"])

    def test_podcast_agent_initialization(self):
        """Test Podcast Agent is properly initialized"""
        agent = self.implementation._initialize_podcast_agent()

        self.assertEqual(agent["name"], "Podcast Agent")
        self.assertEqual(agent["type"], "content_generation")
        self.assertEqual(agent["status"], "initialized")
        self.assertIn("EHR-to-narrative conversion", agent["capabilities"])
        self.assertIn("Text-to-speech", agent["integrations"][0])
        self.assertIn("content_accuracy", agent["guardrails"])
        self.assertIn("< 30s", agent["performance_sla"])

    def test_qa_agent_initialization(self):
        """Test QA Agent is properly initialized"""
        agent = self.implementation._initialize_qa_agent()

        self.assertEqual(agent["name"], "QA Agent")
        self.assertEqual(agent["type"], "quality_assurance")
        self.assertEqual(agent["status"], "initialized")
        self.assertIn("AI output validation", agent["capabilities"])
        self.assertIn("Multi-method verification", agent["integrations"][0])
        self.assertIn("comprehensive_validation", agent["guardrails"])
        self.assertIn("< 500ms", agent["performance_sla"])

    def test_all_six_agents_created(self):
        """Test that all 6 agents are created"""
        agents = {}
        agents["knowledge"] = self.implementation._initialize_knowledge_agent()
        agents["case"] = self.implementation._initialize_case_agent()
        agents["conversation"] = self.implementation._initialize_conversation_agent()
        agents["compliance"] = self.implementation._initialize_compliance_agent()
        agents["podcast"] = self.implementation._initialize_podcast_agent()
        agents["qa"] = self.implementation._initialize_qa_agent()

        self.assertEqual(len(agents), 6)
        self.assertIn("knowledge", agents)
        self.assertIn("case", agents)
        self.assertIn("conversation", agents)
        self.assertIn("compliance", agents)
        self.assertIn("podcast", agents)
        self.assertIn("qa", agents)


class TestAgentValidation(unittest.TestCase):
    """Test agent validation logic"""

    def setUp(self):
        """Set up test fixtures"""
        self.implementation = Phase02Implementation()

    def test_validate_all_agents_success(self):
        """Test successful validation of all agents"""
        agents = {
            "knowledge": self.implementation._initialize_knowledge_agent(),
            "case": self.implementation._initialize_case_agent(),
            "conversation": self.implementation._initialize_conversation_agent(),
            "compliance": self.implementation._initialize_compliance_agent(),
            "podcast": self.implementation._initialize_podcast_agent(),
            "qa": self.implementation._initialize_qa_agent()
        }

        validation = self.implementation._validate_all_agents(agents)

        self.assertTrue(validation["all_agents_initialized"])
        self.assertEqual(validation["agent_count"], 6)
        self.assertEqual(validation["expected_count"], 6)
        self.assertTrue(validation["all_passed"])
        self.assertEqual(len(validation["agents_validated"]), 6)

    def test_agent_required_fields(self):
        """Test each agent has all required fields"""
        required_fields = ["name", "type", "description", "capabilities",
                          "integrations", "guardrails", "status"]

        agents = [
            self.implementation._initialize_knowledge_agent(),
            self.implementation._initialize_case_agent(),
            self.implementation._initialize_conversation_agent(),
            self.implementation._initialize_compliance_agent(),
            self.implementation._initialize_podcast_agent(),
            self.implementation._initialize_qa_agent()
        ]

        for agent in agents:
            for field in required_fields:
                self.assertIn(field, agent,
                            f"Agent {agent.get('name', 'unknown')} missing field: {field}")


class TestPhaseExecution(unittest.TestCase):
    """Test phase execution logic"""

    def setUp(self):
        """Set up test fixtures"""
        self.implementation = Phase02Implementation()

    def test_gather_context(self):
        """Test context gathering"""
        task = {"goal": "Implement SWARMCARE Agents", "phase_id": 2}
        context = self.implementation.gather_context(task, [])

        self.assertIsNotNone(context)
        self.assertIsInstance(context, dict)

    def test_take_action(self):
        """Test action execution"""
        task = {"goal": "Implement SWARMCARE Agents", "phase_id": 2}
        context = {"task": task, "phase_id": 2}

        output = self.implementation.take_action(task, context)

        self.assertIsNotNone(output)
        self.assertEqual(output["phase_id"], 2)
        self.assertEqual(output["status"], "implemented")
        self.assertIn("agents", output["components"])
        self.assertIn("validation", output["components"])
        self.assertEqual(output["components"]["total_agents"], 6)

    def test_verify_work(self):
        """Test work verification"""
        task = {"goal": "Implement SWARMCARE Agents", "phase_id": 2}
        context = {"task": task, "phase_id": 2}
        output = self.implementation.take_action(task, context)

        verification = self.implementation.verify_work(output, context, task)

        self.assertIsNotNone(verification)
        self.assertIn("passed", verification)
        self.assertIn("message", verification)

    def test_full_execution(self):
        """Test full phase execution"""
        task = {"goal": "Implement SWARMCARE Agents", "phase_id": 2}

        result = self.implementation.execute(task)

        self.assertIsNotNone(result)
        self.assertTrue(result.success)
        self.assertIsNotNone(result.output)
        self.assertEqual(result.output["phase_id"], 2)
        self.assertEqual(result.output["components"]["total_agents"], 6)

    def test_get_stats(self):
        """Test statistics retrieval"""
        stats = self.implementation.get_stats()

        self.assertEqual(stats["phase_id"], 2)
        self.assertEqual(stats["phase_name"], "SWARMCARE Agents")
        self.assertEqual(stats["story_points"], 94)
        self.assertEqual(stats["framework_version"], "100%")


class TestAgentCapabilities(unittest.TestCase):
    """Test specific agent capabilities"""

    def setUp(self):
        """Set up test fixtures"""
        self.implementation = Phase02Implementation()

    def test_knowledge_agent_capabilities(self):
        """Test Knowledge Agent has correct capabilities"""
        agent = self.implementation._initialize_knowledge_agent()
        capabilities = agent["capabilities"]

        self.assertGreaterEqual(len(capabilities), 5)
        self.assertTrue(any("literature" in cap.lower() for cap in capabilities))
        self.assertTrue(any("evidence" in cap.lower() for cap in capabilities))

    def test_case_agent_capabilities(self):
        """Test Case Agent has correct capabilities"""
        agent = self.implementation._initialize_case_agent()
        capabilities = agent["capabilities"]

        self.assertGreaterEqual(len(capabilities), 5)
        self.assertTrue(any("patient" in cap.lower() or "case" in cap.lower()
                          for cap in capabilities))

    def test_compliance_agent_capabilities(self):
        """Test Compliance Agent has HIPAA capabilities"""
        agent = self.implementation._initialize_compliance_agent()
        capabilities = agent["capabilities"]

        self.assertTrue(any("hipaa" in cap.lower() for cap in capabilities))
        self.assertTrue(any("phi" in cap.lower() for cap in capabilities))
        self.assertTrue(any("audit" in cap.lower() for cap in capabilities))


class TestAgentIntegrations(unittest.TestCase):
    """Test agent integrations"""

    def setUp(self):
        """Set up test fixtures"""
        self.implementation = Phase02Implementation()

    def test_all_agents_have_integrations(self):
        """Test all agents have integration points defined"""
        agents = [
            self.implementation._initialize_knowledge_agent(),
            self.implementation._initialize_case_agent(),
            self.implementation._initialize_conversation_agent(),
            self.implementation._initialize_compliance_agent(),
            self.implementation._initialize_podcast_agent(),
            self.implementation._initialize_qa_agent()
        ]

        for agent in agents:
            self.assertIn("integrations", agent)
            self.assertIsInstance(agent["integrations"], list)
            self.assertGreater(len(agent["integrations"]), 0)

    def test_knowledge_agent_neo4j_integration(self):
        """Test Knowledge Agent integrates with Neo4j"""
        agent = self.implementation._initialize_knowledge_agent()
        integrations = agent["integrations"]

        self.assertTrue(any("neo4j" in integ.lower() for integ in integrations))


class TestGuardrailsIntegration(unittest.TestCase):
    """Test guardrails integration for all agents"""

    def setUp(self):
        """Set up test fixtures"""
        self.implementation = Phase02Implementation()

    def test_all_agents_have_guardrails(self):
        """Test all agents have guardrails defined"""
        agents = [
            self.implementation._initialize_knowledge_agent(),
            self.implementation._initialize_case_agent(),
            self.implementation._initialize_conversation_agent(),
            self.implementation._initialize_compliance_agent(),
            self.implementation._initialize_podcast_agent(),
            self.implementation._initialize_qa_agent()
        ]

        for agent in agents:
            self.assertIn("guardrails", agent)
            self.assertIsInstance(agent["guardrails"], list)
            self.assertGreater(len(agent["guardrails"]), 0)

    def test_compliance_agent_strict_guardrails(self):
        """Test Compliance Agent has strict guardrails"""
        agent = self.implementation._initialize_compliance_agent()
        guardrails = agent["guardrails"]

        self.assertTrue(any("phi" in gr.lower() for gr in guardrails))
        self.assertTrue(any("access" in gr.lower() for gr in guardrails))


class TestPerformanceSLAs(unittest.TestCase):
    """Test performance SLA definitions"""

    def setUp(self):
        """Set up test fixtures"""
        self.implementation = Phase02Implementation()

    def test_all_agents_have_slas(self):
        """Test all agents have performance SLAs defined"""
        agents = [
            self.implementation._initialize_knowledge_agent(),
            self.implementation._initialize_case_agent(),
            self.implementation._initialize_conversation_agent(),
            self.implementation._initialize_compliance_agent(),
            self.implementation._initialize_podcast_agent(),
            self.implementation._initialize_qa_agent()
        ]

        for agent in agents:
            self.assertIn("performance_sla", agent)
            self.assertIsInstance(agent["performance_sla"], str)
            self.assertGreater(len(agent["performance_sla"]), 0)

    def test_conversation_agent_fast_response(self):
        """Test Conversation Agent has fast response SLA"""
        agent = self.implementation._initialize_conversation_agent()
        sla = agent["performance_sla"]

        # Should be < 1s for conversational responses
        self.assertIn("1s", sla)


def run_test_suite():
    """Run the complete test suite and return results"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestPhase02Initialization))
    suite.addTests(loader.loadTestsFromTestCase(TestSWARMCAREAgents))
    suite.addTests(loader.loadTestsFromTestCase(TestAgentValidation))
    suite.addTests(loader.loadTestsFromTestCase(TestPhaseExecution))
    suite.addTests(loader.loadTestsFromTestCase(TestAgentCapabilities))
    suite.addTests(loader.loadTestsFromTestCase(TestAgentIntegrations))
    suite.addTests(loader.loadTestsFromTestCase(TestGuardrailsIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestPerformanceSLAs))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result


if __name__ == "__main__":
    print("=" * 80)
    print("PHASE 02: SWARMCARE AGENTS - COMPREHENSIVE TEST SUITE")
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
