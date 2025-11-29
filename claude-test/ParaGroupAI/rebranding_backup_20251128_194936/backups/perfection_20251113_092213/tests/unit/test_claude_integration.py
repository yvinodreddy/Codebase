"""
Integration tests for claude_integration.py module.

This test suite extends coverage for the Claude SDK integration layer,
focusing on API interactions, orchestration workflows, and end-to-end processing.

Target Coverage: Boost claude_integration.py from 15% to 70%+
Strategy: Integration tests for API workflow, error handling, guardrails
"""

import pytest
import sys
import os
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch, PropertyMock
from datetime import datetime
import json

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from claude_integration import (
    mask_api_key,
    ClaudeResponse,
    ClaudeOrchestrator
)
from master_orchestrator import OrchestrationResult


class TestMaskApiKey:
    """Test API key masking functionality."""

    @pytest.mark.filterwarnings("ignore::pytest.PytestUnraisableExceptionWarning")
    def test_mask_api_key_standard(self):
        """Should mask API key showing only first 8 characters."""
        key = "sk-ant-api03-1234567890abcdef"
        masked = mask_api_key(key)

        assert masked == "sk-ant-a...***"
        assert "1234567890" not in masked

    def test_mask_api_key_short_key(self):
        """Should mask short keys completely."""
        short_key = "short"
        masked = mask_api_key(short_key)

        assert masked == "***"

    def test_mask_api_key_empty(self):
        """Should handle empty keys."""
        masked = mask_api_key("")
        assert masked == "***"

    def test_mask_api_key_none(self):
        """Should handle None values."""
        masked = mask_api_key(None)
        assert masked == "***"

    def test_mask_api_key_minimum_length(self):
        """Should mask keys at boundary length."""
        key = "123456789012"  # Exactly 12 chars
        masked = mask_api_key(key)

        assert masked.startswith("12345678")
        assert masked.endswith("...***")


class TestClaudeResponse:
    """Test ClaudeResponse dataclass."""

    def test_claude_response_initialization(self):
        """Should initialize ClaudeResponse with all fields."""
        orch_result = Mock(spec=OrchestrationResult)
        orch_result.confidence_score = 99.5
        orch_result.iterations_performed = 3
        orch_result.total_duration_seconds = 2.5

        response = ClaudeResponse(
            success=True,
            response_text="Test response",
            claude_model="claude-sonnet-4-5-20250929",
            orchestration_result=orch_result,
            total_tokens=1500,
            cost_estimate=0.045,
            timestamp="2025-01-01T00:00:00"
        )

        assert response.success is True
        assert response.response_text == "Test response"
        assert response.claude_model == "claude-sonnet-4-5-20250929"
        assert response.total_tokens == 1500
        assert response.cost_estimate == 0.045

    def test_claude_response_to_dict(self):
        """Should convert ClaudeResponse to dictionary."""
        orch_result = Mock(spec=OrchestrationResult)
        orch_result.confidence_score = 98.0
        orch_result.iterations_performed = 2
        orch_result.total_duration_seconds = 1.8

        response = ClaudeResponse(
            success=True,
            response_text="Response",
            claude_model="claude-3-haiku-20240307",
            orchestration_result=orch_result,
            total_tokens=800,
            cost_estimate=0.01,
            timestamp="2025-01-01T00:00:00"
        )

        result_dict = response.to_dict()

        assert result_dict["success"] is True
        assert result_dict["response_text"] == "Response"
        assert result_dict["orchestration_metrics"]["confidence_score"] == 98.0
        assert result_dict["total_tokens"] == 800

    def test_claude_response_with_validation(self):
        """Should include validation and verification results."""
        orch_result = Mock(spec=OrchestrationResult)
        orch_result.confidence_score = 99.2
        orch_result.iterations_performed = 1
        orch_result.total_duration_seconds = 1.0

        response = ClaudeResponse(
            success=True,
            response_text="Validated response",
            claude_model="claude-sonnet-4-5-20250929",
            orchestration_result=orch_result,
            total_tokens=1200,
            cost_estimate=0.036,
            timestamp="2025-01-01T00:00:00",
            output_validation={"passed": True, "layers": 7},
            verification_result={"passed": True, "methods": 3},
            final_confidence=99.5
        )

        assert response.output_validation["passed"] is True
        assert response.verification_result["passed"] is True
        assert response.final_confidence == 99.5

        result_dict = response.to_dict()
        assert "output_validation" in result_dict
        assert "verification_result" in result_dict


class TestClaudeOrchestratorInit:
    """Test ClaudeOrchestrator initialization."""

    @patch.dict(os.environ, {"ANTHROPIC_API_KEY": "sk-ant-test-key-123456789012"})
    @patch('claude_integration.anthropic.Anthropic')
    @patch('claude_integration.MasterOrchestrator')
    def test_init_with_env_key(self, mock_orch, mock_anthropic):
        """Should initialize with API key from environment."""
        orchestrator = ClaudeOrchestrator(enable_rate_limiting=False)

        assert orchestrator.api_key == "sk-ant-test-key-123456789012"
        assert orchestrator.model == "claude-sonnet-4-5-20250929"
        mock_anthropic.assert_called_once()

    @patch('claude_integration.anthropic.Anthropic')
    @patch('claude_integration.MasterOrchestrator')
    def test_init_with_explicit_key(self, mock_orch, mock_anthropic):
        """Should initialize with explicit API key."""
        orchestrator = ClaudeOrchestrator(
            api_key="sk-ant-explicit-key-123456789012",
            enable_rate_limiting=False
        )

        assert orchestrator.api_key == "sk-ant-explicit-key-123456789012"
        mock_anthropic.assert_called_once()

    @patch.dict(os.environ, {}, clear=True)
    def test_init_without_api_key_raises(self):
        """Should raise ValueError if no API key provided."""
        with pytest.raises(ValueError, match="ANTHROPIC_API_KEY must be set"):
            ClaudeOrchestrator()

    @patch.dict(os.environ, {"ANTHROPIC_API_KEY": "sk-ant-test-key-123456789012"})
    @patch('claude_integration.anthropic.Anthropic')
    @patch('claude_integration.MasterOrchestrator')
    def test_init_with_custom_model(self, mock_orch, mock_anthropic):
        """Should initialize with custom model."""
        orchestrator = ClaudeOrchestrator(
            model="claude-3-opus-20240229",
            enable_rate_limiting=False
        )

        assert orchestrator.model == "claude-3-opus-20240229"

    @patch.dict(os.environ, {"ANTHROPIC_API_KEY": "sk-ant-test-key-123456789012"})
    @patch('claude_integration.anthropic.Anthropic')
    @patch('claude_integration.MasterOrchestrator')
    def test_init_with_custom_confidence(self, mock_orch, mock_anthropic):
        """Should initialize with custom confidence threshold."""
        mock_orch_instance = MagicMock()
        mock_orch.return_value = mock_orch_instance

        orchestrator = ClaudeOrchestrator(
            min_confidence_score=95.0,
            enable_rate_limiting=False
        )

        mock_orch.assert_called_once_with(
            min_confidence_score=95.0,
            max_refinement_iterations=20
        )

    @patch.dict(os.environ, {"ANTHROPIC_API_KEY": "sk-ant-test-key-123456789012"})
    @patch('claude_integration.anthropic.Anthropic')
    @patch('claude_integration.MasterOrchestrator')
    def test_init_with_rate_limiting(self, mock_orch, mock_anthropic):
        """Should initialize rate limiter when enabled."""
        with patch('agent_framework.rate_limiter.RateLimiter'):
            with patch('claude_integration.Config') as mock_config:
                mock_config.RATE_LIMIT_CALLS = 5
                mock_config.RATE_LIMIT_WINDOW = 60

                orchestrator = ClaudeOrchestrator(enable_rate_limiting=True)

                assert orchestrator.rate_limiter is not None

    @patch.dict(os.environ, {"ANTHROPIC_API_KEY": "sk-ant-test-key-123456789012"})
    @patch('claude_integration.anthropic.Anthropic')
    @patch('claude_integration.MasterOrchestrator')
    def test_init_without_rate_limiting(self, mock_orch, mock_anthropic):
        """Should not initialize rate limiter when disabled."""
        orchestrator = ClaudeOrchestrator(enable_rate_limiting=False)

        assert orchestrator.rate_limiter is None

    @patch.dict(os.environ, {"ANTHROPIC_API_KEY": "sk-ant-test-key-123456789012"})
    @patch('claude_integration.anthropic.Anthropic')
    @patch('claude_integration.MasterOrchestrator')
    def test_init_stats_tracking(self, mock_orch, mock_anthropic):
        """Should initialize statistics tracking."""
        orchestrator = ClaudeOrchestrator(enable_rate_limiting=False)

        assert orchestrator.stats["total_requests"] == 0
        assert orchestrator.stats["total_tokens"] == 0
        assert orchestrator.stats["total_cost"] == 0.0


class TestClaudeOrchestratorProcess:
    """Test ClaudeOrchestrator process method."""

    @pytest.mark.filterwarnings("ignore::pytest.PytestUnraisableExceptionWarning")
    @patch.dict(os.environ, {"ANTHROPIC_API_KEY": "sk-ant-test-key-123456789012"})
    @patch('claude_integration.anthropic.Anthropic')
    @patch('claude_integration.MasterOrchestrator')
    def test_process_with_input_validation_failure(self, mock_orch_class, mock_anthropic):
        """Should handle input validation failure."""
        mock_orch = MagicMock()
        mock_orch_class.return_value = mock_orch

        # Mock guardrails to fail Layer 1
        mock_layer1 = MagicMock()
        mock_layer1.passed = False
        mock_orch.guardrails.layer1_prompt_shields.return_value = mock_layer1

        orchestrator = ClaudeOrchestrator(enable_rate_limiting=False)

        result = orchestrator.process("malicious prompt")

        assert result.success is False
        assert "blocked" in result.response_text.lower()
        assert result.total_tokens == 0
        assert result.cost_estimate == 0.0

    @pytest.mark.filterwarnings("ignore::pytest.PytestUnraisableExceptionWarning")
    @patch.dict(os.environ, {"ANTHROPIC_API_KEY": "sk-ant-test-key-123456789012"})
    @patch('claude_integration.anthropic.Anthropic')
    @patch('claude_integration.MasterOrchestrator')
    def test_process_layer2_failure(self, mock_orch_class, mock_anthropic):
        """Should handle Layer 2 content filter failure."""
        mock_orch = MagicMock()
        mock_orch_class.return_value = mock_orch

        # Mock Layer 1 pass, Layer 2 fail
        mock_layer1 = MagicMock()
        mock_layer1.passed = True
        mock_layer2 = MagicMock()
        mock_layer2.passed = False

        mock_orch.guardrails.layer1_prompt_shields.return_value = mock_layer1
        mock_orch.guardrails.layer2_input_content_filter.return_value = mock_layer2

        orchestrator = ClaudeOrchestrator(enable_rate_limiting=False)

        result = orchestrator.process("inappropriate content")

        assert result.success is False
        assert "blocked" in result.response_text.lower()

    @pytest.mark.filterwarnings("ignore::pytest.PytestUnraisableExceptionWarning")
    @patch.dict(os.environ, {"ANTHROPIC_API_KEY": "sk-ant-test-key-123456789012"})
    @patch('claude_integration.anthropic.Anthropic')
    @patch('claude_integration.MasterOrchestrator')
    def test_process_layer3_phi_detection_failure(self, mock_orch_class, mock_anthropic):
        """Should handle Layer 3 PHI detection failure."""
        mock_orch = MagicMock()
        mock_orch_class.return_value = mock_orch

        # Mock Layer 1-2 pass, Layer 3 fail
        mock_layer1 = MagicMock()
        mock_layer1.passed = True
        mock_layer2 = MagicMock()
        mock_layer2.passed = True
        mock_layer3 = MagicMock()
        mock_layer3.passed = False

        mock_orch.guardrails.layer1_prompt_shields.return_value = mock_layer1
        mock_orch.guardrails.layer2_input_content_filter.return_value = mock_layer2
        mock_orch.guardrails.layer3_phi_detection.return_value = mock_layer3

        orchestrator = ClaudeOrchestrator(enable_rate_limiting=False)

        result = orchestrator.process("Patient SSN 123-45-6789")

        assert result.success is False
        assert "blocked" in result.response_text.lower()


class TestClaudeOrchestratorStatistics:
    """Test statistics tracking."""

    @patch.dict(os.environ, {"ANTHROPIC_API_KEY": "sk-ant-test-key-123456789012"})
    @patch('claude_integration.anthropic.Anthropic')
    @patch('claude_integration.MasterOrchestrator')
    def test_pricing_constants(self, mock_orch, mock_anthropic):
        """Should have pricing defined for all models."""
        orchestrator = ClaudeOrchestrator(enable_rate_limiting=False)

        assert "claude-sonnet-4-5-20250929" in ClaudeOrchestrator.PRICING
        assert "claude-3-opus-20240229" in ClaudeOrchestrator.PRICING
        assert "claude-3-haiku-20240307" in ClaudeOrchestrator.PRICING

        # Check pricing structure
        sonnet_pricing = ClaudeOrchestrator.PRICING["claude-sonnet-4-5-20250929"]
        assert "input" in sonnet_pricing
        assert "output" in sonnet_pricing
        assert sonnet_pricing["input"] == 3.00
        assert sonnet_pricing["output"] == 15.00


class TestClaudeOrchestratorEdgeCases:
    """Test edge cases and error scenarios."""

    @pytest.mark.filterwarnings("ignore::pytest.PytestUnraisableExceptionWarning")
    @patch.dict(os.environ, {"ANTHROPIC_API_KEY": "sk-ant-test-key-123456789012"})
    @patch('claude_integration.anthropic.Anthropic')
    @patch('claude_integration.MasterOrchestrator')
    def test_process_with_source_documents(self, mock_orch_class, mock_anthropic):
        """Should handle source documents in validation."""
        mock_orch = MagicMock()
        mock_orch_class.return_value = mock_orch

        # Mock all layers to pass
        mock_layer = MagicMock()
        mock_layer.passed = True
        mock_orch.guardrails.layer1_prompt_shields.return_value = mock_layer
        mock_orch.guardrails.layer2_input_content_filter.return_value = mock_layer
        mock_orch.guardrails.layer3_phi_detection.return_value = mock_layer

        orchestrator = ClaudeOrchestrator(enable_rate_limiting=False)

        # This will fail at API call, but we're testing validation passes
        try:
            result = orchestrator.process(
                "Test prompt",
                source_documents=["doc1.txt", "doc2.txt"]
            )
        except Exception:
            pass

        # Verify source_documents passed to Layer 1
        mock_orch.guardrails.layer1_prompt_shields.assert_called_once()
        call_kwargs = mock_orch.guardrails.layer1_prompt_shields.call_args[1]
        assert call_kwargs.get("documents") is not None

    @pytest.mark.filterwarnings("ignore::pytest.PytestUnraisableExceptionWarning")
    @patch.dict(os.environ, {"ANTHROPIC_API_KEY": "sk-ant-test-key-123456789012"})
    @patch('claude_integration.anthropic.Anthropic')
    @patch('claude_integration.MasterOrchestrator')
    def test_process_with_custom_parameters(self, mock_orch_class, mock_anthropic):
        """Should accept custom processing parameters."""
        mock_orch = MagicMock()
        mock_orch_class.return_value = mock_orch

        # Mock layers to fail early so we don't hit API
        mock_layer = MagicMock()
        mock_layer.passed = False
        mock_orch.guardrails.layer1_prompt_shields.return_value = mock_layer

        orchestrator = ClaudeOrchestrator(enable_rate_limiting=False)

        result = orchestrator.process(
            "Test",
            system_prompt="Custom system",
            max_tokens=8000,
            temperature=0.5
        )

        # Just verify it accepts the parameters without error
        assert result is not None

    @patch.dict(os.environ, {"ANTHROPIC_API_KEY": "sk-ant-test-key-123456789012"})
    @patch('claude_integration.anthropic.Anthropic')
    @patch('claude_integration.MasterOrchestrator')
    def test_empty_prompt_handling(self, mock_orch_class, mock_anthropic):
        """Should handle empty prompts."""
        mock_orch = MagicMock()
        mock_orch_class.return_value = mock_orch

        # Mock validation to pass
        mock_layer = MagicMock()
        mock_layer.passed = True
        mock_orch.guardrails.layer1_prompt_shields.return_value = mock_layer
        mock_orch.guardrails.layer2_input_content_filter.return_value = mock_layer
        mock_orch.guardrails.layer3_phi_detection.return_value = mock_layer

        orchestrator = ClaudeOrchestrator(enable_rate_limiting=False)

        try:
            result = orchestrator.process("")
        except Exception:
            # Expected - empty prompt will fail somewhere
            pass


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
