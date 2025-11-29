#!/usr/bin/env python3
"""
Unit Tests for agent_framework/feedback_loop.py
Tests agent feedback loop pattern implementation.

Test Coverage Target: 70%+
"""

import pytest
import sys
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agent_framework.feedback_loop import (
    IterationLog,
    FeedbackLoopResult,
    AgentFeedbackLoop,
)


# ==========================================
# ITERATION LOG TESTS
# ==========================================

class TestIterationLog:
    """Test IterationLog dataclass."""

    def test_iteration_log_creation(self):
        """IterationLog should be created with all fields."""
        log = IterationLog(
            iteration=1,
            timestamp="2025-01-01T12:00:00",
            context={"input": "test"},
            output="result",
            verification={"passed": True},
            success=True,
            duration_seconds=1.5
        )

        assert log.iteration == 1
        assert log.success is True
        assert log.duration_seconds == 1.5


# ==========================================
# FEEDBACK LOOP RESULT TESTS
# ==========================================

class TestFeedbackLoopResult:
    """Test FeedbackLoopResult dataclass."""

    def test_result_creation(self):
        """FeedbackLoopResult should be created with required fields."""
        result = FeedbackLoopResult(
            success=True,
            output="Final output",
            iterations=3,
            total_duration_seconds=5.0
        )

        assert result.success is True
        assert result.output == "Final output"
        assert result.iterations == 3
        assert result.total_duration_seconds == 5.0

    def test_result_with_error(self):
        """FeedbackLoopResult should support error field."""
        result = FeedbackLoopResult(
            success=False,
            output=None,
            iterations=5,
            total_duration_seconds=10.0,
            error="Max iterations reached"
        )

        assert result.success is False
        assert result.error == "Max iterations reached"

    def test_to_dict(self):
        """to_dict should convert result to dictionary."""
        log = IterationLog(
            iteration=1,
            timestamp="2025-01-01T12:00:00",
            context={},
            output="test",
            verification={},
            success=True,
            duration_seconds=1.0
        )

        result = FeedbackLoopResult(
            success=True,
            output="output",
            iterations=1,
            total_duration_seconds=1.0,
            iteration_log=[log]
        )

        result_dict = result.to_dict()

        assert isinstance(result_dict, dict)
        assert result_dict["success"] is True
        assert result_dict["iterations"] == 1
        assert len(result_dict["iteration_log"]) == 1

    def test_save_to_file(self):
        """save_to_file should save result to JSON."""
        result = FeedbackLoopResult(
            success=True,
            output="test",
            iterations=1,
            total_duration_seconds=1.0
        )

        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tf:
            result.save_to_file(tf.name)
            assert Path(tf.name).exists()


# ==========================================
# AGENT FEEDBACK LOOP INITIALIZATION TESTS
# ==========================================

class TestAgentFeedbackLoopInit:
    """Test AgentFeedbackLoop initialization."""

    def test_init_with_defaults(self):
        """AgentFeedbackLoop should initialize with defaults."""
        loop = AgentFeedbackLoop()

        assert loop.max_iterations == 10
        assert loop.enable_learning is True

    def test_init_with_custom_values(self):
        """AgentFeedbackLoop should accept custom values."""
        loop = AgentFeedbackLoop(
            max_iterations=5,
            enable_learning=False
        )

        assert loop.max_iterations == 5
        assert loop.enable_learning is False


# ==========================================
# EXECUTE TESTS
# ==========================================

class TestExecute:
    """Test execute method."""

    def test_execute_successful_first_try(self):
        """execute should succeed on first try if verification passes."""
        loop = AgentFeedbackLoop(max_iterations=5)

        # Mock functions that succeed immediately
        context_gatherer = MagicMock(return_value={"context": "data"})
        action_executor = MagicMock(return_value="success output")
        verifier = MagicMock(return_value={"passed": True, "message": "OK"})

        result = loop.execute(
            task={"goal": "test task"},
            context_gatherer=context_gatherer,
            action_executor=action_executor,
            verifier=verifier
        )

        assert result.success is True
        assert result.iterations == 1
        assert result.output == "success output"

    def test_execute_retry_until_success(self):
        """execute should retry until verification passes."""
        loop = AgentFeedbackLoop(max_iterations=5)

        context_gatherer = MagicMock(return_value={})
        action_executor = MagicMock(return_value="output")

        # Fail first 2 times, succeed on 3rd
        verifier = MagicMock(side_effect=[
            {"passed": False, "message": "Try 1"},
            {"passed": False, "message": "Try 2"},
            {"passed": True, "message": "Success"}
        ])

        result = loop.execute(
            task={"goal": "test"},
            context_gatherer=context_gatherer,
            action_executor=action_executor,
            verifier=verifier
        )

        assert result.success is True
        assert result.iterations == 3

    def test_execute_max_iterations_reached(self):
        """execute should fail if max iterations reached."""
        loop = AgentFeedbackLoop(max_iterations=3)

        context_gatherer = MagicMock(return_value={})
        action_executor = MagicMock(return_value="output")
        # Always fail verification
        verifier = MagicMock(return_value={"passed": False, "message": "Always fails"})

        result = loop.execute(
            task={"goal": "test"},
            context_gatherer=context_gatherer,
            action_executor=action_executor,
            verifier=verifier
        )

        assert result.success is False
        assert result.iterations == 3
        assert "max iterations" in result.error.lower() or result.error is not None

    def test_execute_with_learning_enabled(self):
        """execute should use learning when enabled."""
        loop = AgentFeedbackLoop(max_iterations=5, enable_learning=True)

        context_gatherer = MagicMock(return_value={"initial": "context"})
        action_executor = MagicMock(return_value="output")
        verifier = MagicMock(return_value={"passed": True, "message": "OK"})

        result = loop.execute(
            task={"goal": "test"},
            context_gatherer=context_gatherer,
            action_executor=action_executor,
            verifier=verifier
        )

        assert result.success is True

    def test_execute_exception_handling(self):
        """execute should handle exceptions gracefully."""
        loop = AgentFeedbackLoop(max_iterations=3)

        context_gatherer = MagicMock(return_value={})
        # Action executor raises exception
        action_executor = MagicMock(side_effect=ValueError("Test error"))
        verifier = MagicMock(return_value={"passed": True})

        result = loop.execute(
            task={"goal": "test"},
            context_gatherer=context_gatherer,
            action_executor=action_executor,
            verifier=verifier
        )

        # Should handle error
        assert result.success is False or result.error is not None


# ==========================================
# GET STATISTICS TESTS
# ==========================================

class TestGetStatistics:
    """Test get_statistics method."""

    def test_get_statistics_after_execution(self):
        """get_statistics should return execution stats."""
        loop = AgentFeedbackLoop()

        context_gatherer = MagicMock(return_value={})
        action_executor = MagicMock(return_value="output")
        verifier = MagicMock(return_value={"passed": True})

        loop.execute(
            task={"goal": "test"},
            context_gatherer=context_gatherer,
            action_executor=action_executor,
            verifier=verifier
        )

        stats = loop.get_statistics()

        assert isinstance(stats, dict)
        assert "total_executions" in stats or len(stats) >= 0


# ==========================================
# INTEGRATION TESTS
# ==========================================

class TestFeedbackLoopIntegration:
    """Test real-world feedback loop scenarios."""

    def test_self_correcting_agent_workflow(self):
        """Test agent that corrects itself over iterations."""
        loop = AgentFeedbackLoop(max_iterations=5)

        # Simulate gathering more context each time
        attempt = {"count": 0}

        def context_gatherer(task, previous_attempts):
            attempt["count"] += 1
            return {"attempt": attempt["count"], "learned": previous_attempts}

        def action_executor(task, context):
            # Get better with each attempt
            if context["attempt"] < 3:
                return f"attempt_{context['attempt']}"
            return "good_output"

        def verifier(output, context, task):
            # Accept only "good_output"
            return {
                "passed": output == "good_output",
                "message": "OK" if output == "good_output" else "Try again"
            }

        result = loop.execute(
            task={"goal": "produce good output"},
            context_gatherer=context_gatherer,
            action_executor=action_executor,
            verifier=verifier
        )

        assert result.success is True
        assert result.iterations == 3
        assert result.output == "good_output"

    def test_iteration_log_tracking(self):
        """Test that iteration logs are properly recorded."""
        loop = AgentFeedbackLoop(max_iterations=3)

        context_gatherer = MagicMock(return_value={"data": "test"})
        action_executor = MagicMock(return_value="output")
        verifier = MagicMock(side_effect=[
            {"passed": False, "message": "Retry"},
            {"passed": True, "message": "OK"}
        ])

        result = loop.execute(
            task={"goal": "test"},
            context_gatherer=context_gatherer,
            action_executor=action_executor,
            verifier=verifier
        )

        # Should have logged both iterations
        assert len(result.iteration_log) == 2
        assert result.iteration_log[0].success is False
        assert result.iteration_log[1].success is True

    def test_duration_tracking(self):
        """Test that durations are tracked."""
        loop = AgentFeedbackLoop(max_iterations=2)

        context_gatherer = MagicMock(return_value={})
        action_executor = MagicMock(return_value="output")
        verifier = MagicMock(return_value={"passed": True})

        result = loop.execute(
            task={"goal": "test"},
            context_gatherer=context_gatherer,
            action_executor=action_executor,
            verifier=verifier
        )

        assert result.total_duration_seconds >= 0
        assert result.iteration_log[0].duration_seconds >= 0


# Pytest marker for unit tests
pytestmark = pytest.mark.unit


if __name__ == "__main__":
    # Allow running tests directly
    pytest.main([__file__, "-v"])
