"""
Tests for AgentFeedbackLoop
"""

import unittest
import sys
import os

# Add agent_framework to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..', 'agent_framework'))

from feedback_loop import AgentFeedbackLoop, FeedbackLoopResult


class TestAgentFeedbackLoop(unittest.TestCase):
    """Test AgentFeedbackLoop functionality"""

    def test_initialization(self):
        """Test loop initialization"""
        loop = AgentFeedbackLoop(max_iterations=5)
        self.assertEqual(loop.max_iterations, 5)
        self.assertEqual(len(loop.iteration_log), 0)

    def test_successful_execution(self):
        """Test successful execution with feedback loop"""
        def context_gatherer(task, log):
            return {"task": task, "attempt": len(log) + 1}

        def action_executor(task, context):
            # Succeed on second attempt
            if context["attempt"] >= 2:
                return {"result": "success"}
            return {"result": "incomplete"}

        def verifier(output, context, task):
            if output.get("result") == "success":
                return {"passed": True, "message": "Success"}
            return {"passed": False, "message": "Incomplete"}

        loop = AgentFeedbackLoop(max_iterations=5)
        result = loop.execute(
            task={"goal": "test"},
            context_gatherer=context_gatherer,
            action_executor=action_executor,
            verifier=verifier
        )

        self.assertTrue(result.success)
        self.assertEqual(result.iterations, 2)
        self.assertEqual(len(result.iteration_log), 2)

    def test_max_iterations_reached(self):
        """Test failure when max iterations reached"""
        def context_gatherer(task, log):
            return {"task": task}

        def action_executor(task, context):
            return {"result": "incomplete"}

        def verifier(output, context, task):
            # Always fail
            return {"passed": False, "message": "Always fails"}

        loop = AgentFeedbackLoop(max_iterations=3)
        result = loop.execute(
            task={"goal": "test"},
            context_gatherer=context_gatherer,
            action_executor=action_executor,
            verifier=verifier
        )

        self.assertFalse(result.success)
        self.assertEqual(result.iterations, 3)
        self.assertIsNotNone(result.error)

    def test_learning_from_failures(self):
        """Test that loop learns from previous failures"""
        attempts = []

        def context_gatherer(task, log):
            # Should receive previous attempts in log
            attempts.append(len(log))
            return {"task": task, "previous_attempts": len(log)}

        def action_executor(task, context):
            return {"attempt_number": context["previous_attempts"]}

        def verifier(output, context, task):
            # Succeed on third attempt
            if output["attempt_number"] >= 2:
                return {"passed": True, "message": "Success"}
            return {"passed": False, "message": f"Attempt {output['attempt_number']} failed"}

        loop = AgentFeedbackLoop(max_iterations=5, enable_learning=True)
        result = loop.execute(
            task={"goal": "test"},
            context_gatherer=context_gatherer,
            action_executor=action_executor,
            verifier=verifier
        )

        self.assertTrue(result.success)
        self.assertEqual(attempts, [0, 1, 2])  # Context gatherer called 3 times with increasing log size

    def test_statistics(self):
        """Test statistics generation"""
        def context_gatherer(task, log):
            return {"task": task}

        def action_executor(task, context):
            return {"result": "success"}

        def verifier(output, context, task):
            return {"passed": True, "message": "Success"}

        loop = AgentFeedbackLoop(max_iterations=5)
        loop.execute(
            task={"goal": "test"},
            context_gatherer=context_gatherer,
            action_executor=action_executor,
            verifier=verifier
        )

        stats = loop.get_statistics()

        self.assertIn("total_iterations", stats)
        self.assertIn("successful_iterations", stats)
        self.assertIn("success_rate", stats)
        self.assertEqual(stats["total_iterations"], 1)


if __name__ == "__main__":
    unittest.main()
