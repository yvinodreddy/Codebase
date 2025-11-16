"""
Integration tests for agent framework
Tests that all components work together
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..', 'agent_framework'))

from feedback_loop import AgentFeedbackLoop
from context_manager import ContextManager
from agentic_search import AgenticSearch
from verification_system import MultiMethodVerifier


class TestAgentFrameworkIntegration(unittest.TestCase):
    """Integration tests for complete agent framework"""

    def test_complete_agent_workflow(self):
        """Test complete agent workflow with all components"""
        # Initialize components
        feedback_loop = AgentFeedbackLoop(max_iterations=3)
        context_manager = ContextManager(max_tokens=10000)
        search = AgenticSearch()
        verifier = MultiMethodVerifier()

        # Define workflow functions
        def context_gatherer(task, iteration_log):
            # Use search to gather context
            phase_id = task.get("phase_id", 0)
            context = search.gather_context_for_phase(phase_id)

            # Add to context manager
            context_manager.add_message("system", f"Gathered context for phase {phase_id}")

            return context

        def action_executor(task, context):
            # Simulate action
            output = {
                "phase_id": task.get("phase_id"),
                "status": "completed",
                "result": "Implementation complete"
            }

            # Add to context
            context_manager.add_message("assistant", f"Executed task: {task.get('goal')}")

            return output

        def verify_output(output, context, task):
            # Use multi-method verifier
            verification = verifier.verify_output(
                output=output,
                context={"input": task.get("goal", "")},
                output_type="data",
                task={"expected_type": "dict"}
            )

            return {
                "passed": verification["overall_passed"],
                "message": "Verification " + ("passed" if verification["overall_passed"] else "failed")
            }

        # Execute complete workflow
        task = {
            "goal": "Implement phase 0",
            "phase_id": 0
        }

        result = feedback_loop.execute(
            task=task,
            context_gatherer=context_gatherer,
            action_executor=action_executor,
            verifier=verify_output
        )

        # Verify complete workflow succeeded
        self.assertTrue(result.success)
        self.assertGreater(len(context_manager.messages), 0)
        self.assertGreater(len(search.search_log), 0)
        self.assertGreater(len(verifier.verification_log), 0)

    def test_feedback_loop_with_context_compaction(self):
        """Test feedback loop with context compaction"""
        # Small context to force compaction
        context_manager = ContextManager(max_tokens=500, compact_threshold=0.7)
        feedback_loop = AgentFeedbackLoop(max_iterations=10)

        iteration_count = 0

        def context_gatherer(task, iteration_log):
            nonlocal iteration_count
            iteration_count += 1

            # Add large messages to force compaction
            context_manager.add_message("user", "Large context message " * 50)

            return {"iteration": iteration_count}

        def action_executor(task, context):
            # Add more context
            context_manager.add_message("assistant", "Processing " * 50)
            return {"iteration": context["iteration"]}

        def verifier(output, context, task):
            # Succeed on iteration 3
            if output["iteration"] >= 3:
                return {"passed": True, "message": "Success"}
            return {"passed": False, "message": "Not yet"}

        result = feedback_loop.execute(
            task={"goal": "test"},
            context_gatherer=context_gatherer,
            action_executor=action_executor,
            verifier=verifier
        )

        # Should succeed
        self.assertTrue(result.success)

        # Compaction should have occurred
        self.assertGreater(len(context_manager.compaction_log), 0)

    def test_agentic_search_with_verification(self):
        """Test agentic search combined with verification"""
        search = AgenticSearch()
        verifier = MultiMethodVerifier()

        # Search for phase information
        context = search.gather_context_for_phase(0)

        # Verify the gathered context
        verification = verifier.verify_output(
            output=context,
            context={"input": "gather phase 0 context"},
            output_type="data",
            task={
                "expected_type": "dict",
                "required_fields": ["phase_id", "phase_info"]
            }
        )

        # Context should have required fields
        self.assertIn("phase_id", context)
        self.assertIn("phase_info", context)


if __name__ == "__main__":
    unittest.main()
