#!/usr/bin/env python3
"""
Unit Tests for master_orchestrator.py
Tests central orchestration system coordinating all components.

Test Coverage Target: 70%+
Production-Ready Quality Standards
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch, call

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from master_orchestrator import (
    OrchestrationResult,
    MasterOrchestrator
)


# ==========================================
# ORCHESTRATION RESULT TESTS
# ==========================================

class TestOrchestrationResult:
    """Test OrchestrationResult dataclass."""

    def test_result_creation(self):
        """Should create orchestration result with required fields."""
        result = OrchestrationResult(
            success=True,
            output="Test output",
            confidence_score=99.5,
            prompt_analysis={},
            guardrails_validation={},
            agent_execution={},
            verification_results={},
            quality_metrics={},
            iterations_performed=5,
            total_duration_seconds=2.5
        )

        assert result.success is True
        assert result.output == "Test output"
        assert result.confidence_score == 99.5

    def test_to_dict_conversion(self):
        """Should convert result to dictionary."""
        result = OrchestrationResult(
            success=True,
            output="Output",
            confidence_score=95.0,
            prompt_analysis={},
            guardrails_validation={},
            agent_execution={},
            verification_results={},
            quality_metrics={},
            iterations_performed=3,
            total_duration_seconds=1.5
        )

        result_dict = result.to_dict()

        assert isinstance(result_dict, dict)
        assert result_dict["success"] is True
        assert result_dict["confidence_score"] == 95.0


# ==========================================
# MASTER ORCHESTRATOR INITIALIZATION TESTS
# ==========================================

class TestMasterOrchestratorInit:
    """Test MasterOrchestrator initialization."""

    @patch('master_orchestrator.get_monitor')
    @patch('master_orchestrator.MultiLayerGuardrailSystem')
    @patch('master_orchestrator.PromptPreprocessor')
    @patch('master_orchestrator.ContextManager')
    def test_init_with_defaults(self, mock_ctx_mgr, mock_preprocessor, mock_guardrails, mock_monitor):
        """Should initialize with default values."""
        orchestrator = MasterOrchestrator()

        assert orchestrator.min_confidence_score == 99.0
        assert orchestrator.max_refinement_iterations == 20
        assert orchestrator.verbose is False

    @patch('master_orchestrator.get_monitor')
    @patch('master_orchestrator.MultiLayerGuardrailSystem')
    @patch('master_orchestrator.PromptPreprocessor')
    @patch('master_orchestrator.ContextManager')
    def test_init_with_custom_values(self, mock_ctx_mgr, mock_preprocessor, mock_guardrails, mock_monitor):
        """Should initialize with custom values."""
        orchestrator = MasterOrchestrator(
            min_confidence_score=95.0,
            max_refinement_iterations=10,
            verbose=True
        )

        assert orchestrator.min_confidence_score == 95.0
        assert orchestrator.max_refinement_iterations == 10
        assert orchestrator.verbose is True

    @patch('master_orchestrator.get_monitor')
    @patch('master_orchestrator.MultiLayerGuardrailSystem')
    @patch('master_orchestrator.PromptPreprocessor')
    @patch('master_orchestrator.ContextManager')
    def test_initializes_components(self, mock_ctx_mgr, mock_preprocessor, mock_guardrails, mock_monitor):
        """Should initialize all required components."""
        orchestrator = MasterOrchestrator()

        assert orchestrator.preprocessor is not None
        assert orchestrator.guardrails is not None
        assert orchestrator.monitor is not None
        assert orchestrator.context_manager is not None


# ==========================================
# PROCESS METHOD TESTS - SUCCESS FLOW
# ==========================================

class TestProcessSuccess:
    """Test process method - successful orchestration."""

    @patch('master_orchestrator.get_monitor')
    @patch('master_orchestrator.MultiLayerGuardrailSystem')
    @patch('master_orchestrator.PromptPreprocessor')
    @patch('master_orchestrator.ContextManager')
    def test_processes_simple_prompt_successfully(self, mock_ctx_mgr_class, mock_preprocessor_class, mock_guardrails_class, mock_monitor):
        """Should process simple prompt successfully."""
        # Mock context manager with proper get_statistics return value
        mock_ctx_mgr = MagicMock()
        mock_ctx_mgr_class.return_value = mock_ctx_mgr
        mock_ctx_mgr.get_total_tokens.return_value = 100
        mock_ctx_mgr.get_statistics.return_value = {
            "total_messages": 2,
            "total_tokens": 150,
            "usage_percentage": 0.075,
            "compactions_performed": 0,
            "total_tokens_saved": 0
        }

        # Mock preprocessor
        mock_preprocessor = MagicMock()
        mock_preprocessor_class.return_value = mock_preprocessor

        mock_analysis = MagicMock()
        mock_analysis.intent_type = "question"
        mock_analysis.complexity = "SIMPLE"
        mock_analysis.required_components = []
        mock_analysis.estimated_iterations = 3
        mock_analysis.confidence = 0.95
        mock_analysis.requires_code_generation = False
        mock_analysis.requires_search = False
        mock_analysis.requires_external_services = False
        mock_analysis.metadata = {}
        mock_analysis.to_dict.return_value = {"intent": "question"}

        mock_preprocessor.analyze_prompt.return_value = mock_analysis

        # Mock guardrails
        mock_guardrails = MagicMock()
        mock_guardrails_class.return_value = mock_guardrails
        mock_guardrails.process_with_guardrails.return_value = {
            "success": True,
            "passed_layers": ["Layer1", "Layer2"],
            "warnings": 0,
            "validation_log": []
        }

        orchestrator = MasterOrchestrator(min_confidence_score=95.0)

        result = orchestrator.process("What is Python?")

        assert result.success is True
        assert result.confidence_score >= 95.0

    @patch('master_orchestrator.get_monitor')
    @patch('master_orchestrator.MultiLayerGuardrailSystem')
    @patch('master_orchestrator.PromptPreprocessor')
    @patch('master_orchestrator.ContextManager')
    def test_adds_messages_to_context_manager(self, mock_ctx_mgr_class, mock_preprocessor_class, mock_guardrails_class, mock_monitor):
        """Should add messages to context manager."""
        mock_ctx_mgr = MagicMock()
        mock_ctx_mgr_class.return_value = mock_ctx_mgr
        mock_ctx_mgr.get_total_tokens.return_value = 100
        mock_ctx_mgr.get_statistics.return_value = {
            "total_messages": 2,
            "total_tokens": 150,
            "usage_percentage": 0.075,
            "compactions_performed": 0,
            "total_tokens_saved": 0
        }

        # Mock preprocessor
        mock_preprocessor = MagicMock()
        mock_preprocessor_class.return_value = mock_preprocessor

        mock_analysis = MagicMock()
        mock_analysis.intent_type = "question"
        mock_analysis.complexity = "SIMPLE"
        mock_analysis.required_components = []
        mock_analysis.estimated_iterations = 3
        mock_analysis.confidence = 0.95
        mock_analysis.requires_code_generation = False
        mock_analysis.requires_search = False
        mock_analysis.requires_external_services = False
        mock_analysis.metadata = {}
        mock_analysis.to_dict.return_value = {}

        mock_preprocessor.analyze_prompt.return_value = mock_analysis

        # Mock guardrails
        mock_guardrails = MagicMock()
        mock_guardrails_class.return_value = mock_guardrails
        mock_guardrails.process_with_guardrails.return_value = {
            "success": True,
            "passed_layers": [],
            "warnings": 0,
            "validation_log": []
        }

        orchestrator = MasterOrchestrator()
        orchestrator.process("Test prompt")

        # Should have added user message and assistant message
        assert mock_ctx_mgr.add_message.call_count >= 1


# ==========================================
# PROCESS METHOD TESTS - INPUT VALIDATION FAILURE
# ==========================================

class TestProcessInputValidationFailure:
    """Test process method when input validation fails."""

    @patch('master_orchestrator.get_monitor')
    @patch('master_orchestrator.MultiLayerGuardrailSystem')
    @patch('master_orchestrator.PromptPreprocessor')
    @patch('master_orchestrator.ContextManager')
    def test_fails_when_input_validation_fails(self, mock_ctx_mgr, mock_preprocessor_class, mock_guardrails_class, mock_monitor):
        """Should fail when input validation fails."""
        # Mock preprocessor
        mock_preprocessor = MagicMock()
        mock_preprocessor_class.return_value = mock_preprocessor

        mock_analysis = MagicMock()
        mock_analysis.to_dict.return_value = {"intent": "malicious"}

        mock_preprocessor.analyze_prompt.return_value = mock_analysis

        # Mock guardrails to fail
        mock_guardrails = MagicMock()
        mock_guardrails_class.return_value = mock_guardrails
        mock_guardrails.process_with_guardrails.return_value = {
            "success": False,
            "blocked_at": "Layer 1: Prompt Shields",
            "validation_log": []
        }

        orchestrator = MasterOrchestrator()
        result = orchestrator.process("Malicious input")

        assert result.success is False
        assert "blocked" in str(result.errors).lower() or len(result.errors) > 0


# ==========================================
# INITIALIZE COMPONENTS TESTS
# ==========================================

class TestInitializeComponents:
    """Test _initialize_components method."""

    @patch('master_orchestrator.get_monitor')
    @patch('master_orchestrator.MultiLayerGuardrailSystem')
    @patch('master_orchestrator.PromptPreprocessor')
    @patch('master_orchestrator.ContextManager')
    @patch('master_orchestrator.CodeGenerator')
    def test_initializes_code_generator(self, mock_codegen, mock_ctx_mgr, mock_preprocessor, mock_guardrails, mock_monitor):
        """Should initialize code generator when needed."""
        orchestrator = MasterOrchestrator()

        orchestrator._initialize_components(["code_generator"])

        assert orchestrator.code_generator is not None

    @patch('master_orchestrator.get_monitor')
    @patch('master_orchestrator.MultiLayerGuardrailSystem')
    @patch('master_orchestrator.PromptPreprocessor')
    @patch('master_orchestrator.ContextManager')
    @patch('master_orchestrator.AgenticSearch')
    def test_initializes_agentic_search(self, mock_search, mock_ctx_mgr, mock_preprocessor, mock_guardrails, mock_monitor):
        """Should initialize agentic search when needed."""
        orchestrator = MasterOrchestrator()

        orchestrator._initialize_components(["agentic_search"])

        assert orchestrator.agentic_search is not None

    @patch('master_orchestrator.get_monitor')
    @patch('master_orchestrator.MultiLayerGuardrailSystem')
    @patch('master_orchestrator.PromptPreprocessor')
    @patch('master_orchestrator.ContextManager')
    @patch('master_orchestrator.MultiMethodVerifier')
    def test_initializes_verifier(self, mock_verifier, mock_ctx_mgr, mock_preprocessor, mock_guardrails, mock_monitor):
        """Should initialize verifier when needed."""
        orchestrator = MasterOrchestrator()

        orchestrator._initialize_components(["verification_system"])

        assert orchestrator.verifier is not None


# ==========================================
# EXECUTE AGENTS TESTS
# ==========================================

class TestExecuteAgents:
    """Test _execute_agents method."""

    @patch('master_orchestrator.get_monitor')
    @patch('master_orchestrator.MultiLayerGuardrailSystem')
    @patch('master_orchestrator.PromptPreprocessor')
    @patch('master_orchestrator.ContextManager')
    @patch('master_orchestrator.AdaptiveFeedbackLoop')
    def test_executes_agents_with_feedback_loop(self, mock_feedback_loop_class, mock_ctx_mgr, mock_preprocessor, mock_guardrails, mock_monitor):
        """Should execute agents using adaptive feedback loop."""
        # Mock feedback loop
        mock_feedback_loop = MagicMock()
        mock_feedback_loop_class.return_value = mock_feedback_loop

        mock_result = MagicMock()
        mock_result.success = True
        mock_result.output = {"type": "text", "content": "Response"}
        mock_result.iterations = 3
        mock_result.total_duration_seconds = 1.5
        mock_result.to_dict.return_value = {"success": True}

        mock_feedback_loop.execute.return_value = mock_result

        orchestrator = MasterOrchestrator()

        # Mock analysis
        mock_analysis = MagicMock()
        mock_analysis.estimated_iterations = 5
        mock_analysis.requires_code_generation = False
        mock_analysis.requires_search = False
        mock_analysis.requires_external_services = False
        mock_analysis.to_dict.return_value = {}

        result = orchestrator._execute_agents(
            prompt="Test prompt",
            prompt_analysis=mock_analysis,
            context={}
        )

        assert result["success"] is True
        assert mock_feedback_loop.execute.called


# ==========================================
# CALCULATE QUALITY METRICS TESTS
# ==========================================

class TestCalculateQualityMetrics:
    """Test _calculate_quality_metrics method."""

    @patch('master_orchestrator.get_monitor')
    @patch('master_orchestrator.MultiLayerGuardrailSystem')
    @patch('master_orchestrator.PromptPreprocessor')
    @patch('master_orchestrator.ContextManager')
    def test_calculates_quality_metrics(self, mock_ctx_mgr, mock_preprocessor, mock_guardrails, mock_monitor):
        """Should calculate quality metrics correctly."""
        orchestrator = MasterOrchestrator()

        mock_analysis = MagicMock()
        mock_analysis.confidence = 0.95
        mock_analysis.estimated_iterations = 5

        agent_result = {
            "success": True,
            "iterations": 3
        }

        output_validation = {
            "success": True,
            "warnings": 0,
            "validation_log": []
        }

        metrics = orchestrator._calculate_quality_metrics(
            prompt_analysis=mock_analysis,
            agent_result=agent_result,
            output_validation=output_validation
        )

        assert "confidence_score" in metrics
        assert "confidence_breakdown" in metrics
        assert 0 <= metrics["confidence_score"] <= 100


# ==========================================
# DETERMINE CONTENT TYPE TESTS
# ==========================================

class TestDetermineContentType:
    """Test _determine_content_type method."""

    @patch('master_orchestrator.get_monitor')
    @patch('master_orchestrator.MultiLayerGuardrailSystem')
    @patch('master_orchestrator.PromptPreprocessor')
    @patch('master_orchestrator.ContextManager')
    def test_detects_medical_content(self, mock_ctx_mgr, mock_preprocessor, mock_guardrails, mock_monitor):
        """Should detect medical content."""
        orchestrator = MasterOrchestrator()

        mock_analysis = MagicMock()
        mock_analysis.metadata = {"mentions_medical": True}
        mock_analysis.requires_code_generation = False

        content_type = orchestrator._determine_content_type(mock_analysis)

        assert content_type == "medical_education"

    @patch('master_orchestrator.get_monitor')
    @patch('master_orchestrator.MultiLayerGuardrailSystem')
    @patch('master_orchestrator.PromptPreprocessor')
    @patch('master_orchestrator.ContextManager')
    def test_detects_code_content(self, mock_ctx_mgr, mock_preprocessor, mock_guardrails, mock_monitor):
        """Should detect code content."""
        orchestrator = MasterOrchestrator()

        mock_analysis = MagicMock()
        mock_analysis.metadata = {}
        mock_analysis.requires_code_generation = True

        content_type = orchestrator._determine_content_type(mock_analysis)

        assert content_type == "code"

    @patch('master_orchestrator.get_monitor')
    @patch('master_orchestrator.MultiLayerGuardrailSystem')
    @patch('master_orchestrator.PromptPreprocessor')
    @patch('master_orchestrator.ContextManager')
    def test_defaults_to_general(self, mock_ctx_mgr, mock_preprocessor, mock_guardrails, mock_monitor):
        """Should default to general content type."""
        orchestrator = MasterOrchestrator()

        mock_analysis = MagicMock()
        mock_analysis.metadata = {}
        mock_analysis.requires_code_generation = False

        content_type = orchestrator._determine_content_type(mock_analysis)

        assert content_type == "general"


# ==========================================
# COLLECT WARNINGS TESTS
# ==========================================

class TestCollectWarnings:
    """Test _collect_warnings method."""

    @patch('master_orchestrator.get_monitor')
    @patch('master_orchestrator.MultiLayerGuardrailSystem')
    @patch('master_orchestrator.PromptPreprocessor')
    @patch('master_orchestrator.ContextManager')
    def test_collects_warnings_from_validation(self, mock_ctx_mgr, mock_preprocessor, mock_guardrails, mock_monitor):
        """Should collect warnings from validation log."""
        orchestrator = MasterOrchestrator()

        validation = {
            "validation_log": [
                {
                    "details": {
                        "warnings": ["Warning 1", "Warning 2"]
                    }
                },
                {
                    "details": {
                        "warnings": ["Warning 3"]
                    }
                }
            ]
        }

        warnings = orchestrator._collect_warnings(validation)

        assert len(warnings) == 3
        assert "Warning 1" in warnings
        assert "Warning 2" in warnings
        assert "Warning 3" in warnings


# ==========================================
# CREATE FAILED RESULT TESTS
# ==========================================

class TestCreateFailedResult:
    """Test _create_failed_result method."""

    @patch('master_orchestrator.get_monitor')
    @patch('master_orchestrator.MultiLayerGuardrailSystem')
    @patch('master_orchestrator.PromptPreprocessor')
    @patch('master_orchestrator.ContextManager')
    def test_creates_failed_result(self, mock_ctx_mgr, mock_preprocessor, mock_guardrails, mock_monitor):
        """Should create failed orchestration result."""
        orchestrator = MasterOrchestrator()

        result = orchestrator._create_failed_result(
            prompt_analysis={"intent": "test"},
            guardrails_validation={"success": False},
            error="Test error",
            duration=1.5
        )

        assert result.success is False
        assert result.confidence_score == 0.0
        assert "Test error" in result.errors
        assert result.total_duration_seconds == 1.5


# ==========================================
# UPDATE STATISTICS TESTS
# ==========================================

class TestUpdateStatistics:
    """Test _update_statistics method."""

    @patch('master_orchestrator.get_monitor')
    @patch('master_orchestrator.MultiLayerGuardrailSystem')
    @patch('master_orchestrator.PromptPreprocessor')
    @patch('master_orchestrator.ContextManager')
    def test_updates_statistics(self, mock_ctx_mgr, mock_preprocessor, mock_guardrails, mock_monitor):
        """Should update running statistics."""
        orchestrator = MasterOrchestrator()

        orchestrator.stats["successful_requests"] = 2

        result = OrchestrationResult(
            success=True,
            output="Output",
            confidence_score=98.0,
            prompt_analysis={},
            guardrails_validation={},
            agent_execution={},
            verification_results={},
            quality_metrics={},
            iterations_performed=5,
            total_duration_seconds=2.5
        )

        orchestrator._update_statistics(result)

        assert orchestrator.stats["average_confidence"] > 0
        assert orchestrator.stats["average_iterations"] > 0
        assert orchestrator.stats["average_duration"] > 0


# ==========================================
# GET STATISTICS TESTS
# ==========================================

class TestGetStatistics:
    """Test get_statistics method."""

    @patch('master_orchestrator.get_monitor')
    @patch('master_orchestrator.MultiLayerGuardrailSystem')
    @patch('master_orchestrator.PromptPreprocessor')
    @patch('master_orchestrator.ContextManager')
    def test_returns_statistics(self, mock_ctx_mgr, mock_preprocessor, mock_guardrails, mock_monitor):
        """Should return orchestrator statistics."""
        orchestrator = MasterOrchestrator()

        orchestrator.stats["total_requests"] = 10
        orchestrator.stats["successful_requests"] = 9
        orchestrator.stats["failed_requests"] = 1

        stats = orchestrator.get_statistics()

        assert stats["total_requests"] == 10
        assert stats["successful_requests"] == 9
        assert stats["success_rate"] == 90.0


# ==========================================
# INTEGRATION TESTS
# ==========================================

class TestMasterOrchestratorIntegration:
    """Test complete orchestration workflows."""

    @patch('master_orchestrator.get_monitor')
    @patch('master_orchestrator.MultiLayerGuardrailSystem')
    @patch('master_orchestrator.PromptPreprocessor')
    @patch('master_orchestrator.ContextManager')
    def test_complete_successful_workflow(self, mock_ctx_mgr_class, mock_preprocessor_class, mock_guardrails_class, mock_monitor):
        """Test complete workflow from prompt to result."""
        # Setup mocks
        mock_ctx_mgr = MagicMock()
        mock_ctx_mgr_class.return_value = mock_ctx_mgr
        mock_ctx_mgr.get_total_tokens.return_value = 100
        mock_ctx_mgr.get_statistics.return_value = {
            "total_messages": 2,
            "total_tokens": 150,
            "usage_percentage": 0.075,
            "compactions_performed": 0,
            "total_tokens_saved": 0
        }

        mock_preprocessor = MagicMock()
        mock_preprocessor_class.return_value = mock_preprocessor

        mock_analysis = MagicMock()
        mock_analysis.intent_type = "question"
        mock_analysis.complexity = "SIMPLE"
        mock_analysis.required_components = []
        mock_analysis.estimated_iterations = 3
        mock_analysis.confidence = 0.95
        mock_analysis.requires_code_generation = False
        mock_analysis.requires_search = False
        mock_analysis.requires_external_services = False
        mock_analysis.metadata = {}
        mock_analysis.to_dict.return_value = {}

        mock_preprocessor.analyze_prompt.return_value = mock_analysis

        mock_guardrails = MagicMock()
        mock_guardrails_class.return_value = mock_guardrails
        mock_guardrails.process_with_guardrails.return_value = {
            "success": True,
            "passed_layers": [],
            "warnings": 0,
            "validation_log": []
        }

        orchestrator = MasterOrchestrator(min_confidence_score=95.0)

        result = orchestrator.process("Simple test question")

        assert result.success is True
        assert result.confidence_score >= 95.0
        assert result.iterations_performed >= 0


# Pytest marker for unit tests
pytestmark = pytest.mark.unit


if __name__ == "__main__":
    # Allow running tests directly
    pytest.main([__file__, "-v"])
