#!/usr/bin/env python3
"""
Unit Tests for validation_loop.py
Tests iterative validation and refinement loop.

Test Coverage Target: 90%+
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from validation_loop import ValidationLoop, validate_response_to_target


# ==========================================
# VALIDATION LOOP INITIALIZATION TESTS
# ==========================================

class TestValidationLoopInit:
    """Test ValidationLoop initialization."""

    @patch('validation_loop.ResponseValidator')
    def test_init_with_defaults(self, mock_validator):
        """ValidationLoop should initialize with defaults."""
        loop = ValidationLoop()

        assert loop.max_iterations == 20  # Default from config
        assert loop.target_confidence == 99.0  # Production standard

    @patch('validation_loop.ResponseValidator')
    def test_init_with_custom_max_iterations(self, mock_validator):
        """ValidationLoop should accept custom max_iterations."""
        loop = ValidationLoop(max_iterations=5)

        assert loop.max_iterations == 5


# ==========================================
# VALIDATE AND REFINE TESTS - SUCCESS CASES
# ==========================================

class TestValidateAndRefineSuccess:
    """Test validate_and_refine method - success scenarios."""

    @patch('validation_loop.ResponseValidator')
    def test_validates_response_achieving_target_first_try(self, mock_validator_class):
        """Should return response if it achieves target on first try."""
        # Mock validator
        mock_validator = MagicMock()
        mock_validator_class.return_value = mock_validator

        mock_validator.validate.return_value = {
            "confidence": 99.5,
            "is_acceptable": True,
            "target_confidence": 99.0
        }

        loop = ValidationLoop()
        claude_api = MagicMock()

        response, validation = loop.validate_and_refine(
            initial_response="Great response",
            original_prompt="Test question",
            claude_api_call=claude_api,
            verbose=False
        )

        # Should not call Claude API for refinement
        claude_api.assert_not_called()

        # Should return original response
        assert response == "Great response"
        assert validation["confidence"] == 99.5

    @patch('validation_loop.ResponseValidator')
    def test_refines_until_target_achieved(self, mock_validator_class):
        """Should refine response until target achieved."""
        mock_validator = MagicMock()
        mock_validator_class.return_value = mock_validator

        # Sequence: 85% → 92% → 99.5% (success on 3rd)
        mock_validator.validate.side_effect = [
            {"confidence": 85.0, "is_acceptable": False, "suggestions": ["Add detail"]},
            {"confidence": 92.0, "is_acceptable": False, "suggestions": ["Add examples"]},
            {"confidence": 99.5, "is_acceptable": True, "suggestions": []}
        ]

        loop = ValidationLoop(max_iterations=5)

        # Mock Claude API to return improved responses
        claude_api = MagicMock(side_effect=["Better response", "Best response"])

        response, validation = loop.validate_and_refine(
            initial_response="Initial response",
            original_prompt="Test question",
            claude_api_call=claude_api
        )

        # Should have called Claude API twice (for iterations 2 and 3)
        assert claude_api.call_count == 2

        # Should return final refined response
        assert response == "Best response"
        assert validation["confidence"] == 99.5


# ==========================================
# VALIDATE AND REFINE TESTS - MAX ITERATIONS
# ==========================================

class TestValidateAndRefineMaxIterations:
    """Test validate_and_refine when max iterations reached."""

    @patch('validation_loop.ResponseValidator')
    def test_returns_best_response_when_max_iterations_reached(self, mock_validator_class):
        """Should return best response when max iterations reached."""
        mock_validator = MagicMock()
        mock_validator_class.return_value = mock_validator

        # Never quite reaches 99%, best is 95%
        mock_validator.validate.side_effect = [
            {"confidence": 85.0, "is_acceptable": False, "suggestions": ["Improve"]},
            {"confidence": 90.0, "is_acceptable": False, "suggestions": ["Improve"]},
            {"confidence": 95.0, "is_acceptable": False, "suggestions": ["Improve"]}  # Best
        ]

        loop = ValidationLoop(max_iterations=3)

        claude_api = MagicMock(side_effect=["Response 2", "Response 3"])

        response, validation = loop.validate_and_refine(
            initial_response="Response 1",
            original_prompt="Test",
            claude_api_call=claude_api
        )

        # Should have tried 3 times
        assert claude_api.call_count == 2

        # Should return last response (best)
        assert response == "Response 3"

    @patch('validation_loop.ResponseValidator')
    def test_tracks_best_confidence_correctly(self, mock_validator_class):
        """Should track best confidence across iterations."""
        mock_validator = MagicMock()
        mock_validator_class.return_value = mock_validator

        # Confidence: 90% → 95% (best) → 93% (worse) → 94%
        # Need extra validation call for re-validating best response at end
        mock_validator.validate.side_effect = [
            {"confidence": 90.0, "is_acceptable": False, "suggestions": ["A"]},
            {"confidence": 95.0, "is_acceptable": False, "suggestions": ["B"]},
            {"confidence": 93.0, "is_acceptable": False, "suggestions": ["C"]},
            {"confidence": 94.0, "is_acceptable": False, "suggestions": ["D"]},
            {"confidence": 95.0, "is_acceptable": False, "suggestions": []}  # Re-validation of best
        ]

        loop = ValidationLoop(max_iterations=4)

        claude_api = MagicMock(side_effect=["R2", "R3", "R4"])

        response, validation = loop.validate_and_refine(
            initial_response="R1",
            original_prompt="Test",
            claude_api_call=claude_api
        )

        # Should return R2 (95% confidence, the best)
        assert response == "R2"


# ==========================================
# VALIDATE AND REFINE TESTS - ERROR HANDLING
# ==========================================

class TestValidateAndRefineErrorHandling:
    """Test error handling in validate_and_refine."""

    @patch('validation_loop.ResponseValidator')
    def test_handles_claude_api_exception(self, mock_validator_class):
        """Should handle exception from Claude API gracefully."""
        mock_validator = MagicMock()
        mock_validator_class.return_value = mock_validator

        mock_validator.validate.return_value = {
            "confidence": 85.0,
            "is_acceptable": False,
            "suggestions": ["Improve"]
        }

        loop = ValidationLoop()

        # Claude API raises exception
        claude_api = MagicMock(side_effect=Exception("API Error"))

        response, validation = loop.validate_and_refine(
            initial_response="Initial",
            original_prompt="Test",
            claude_api_call=claude_api
        )

        # Should return initial response
        assert response == "Initial"
        assert validation["confidence"] == 85.0

    @patch('validation_loop.ResponseValidator')
    def test_uses_generic_suggestions_if_none_provided(self, mock_validator_class):
        """Should use generic suggestions if validator provides none."""
        mock_validator = MagicMock()
        mock_validator_class.return_value = mock_validator

        # No suggestions in validation result
        mock_validator.validate.side_effect = [
            {"confidence": 85.0, "is_acceptable": False, "suggestions": []},
            {"confidence": 99.5, "is_acceptable": True, "suggestions": []}
        ]

        loop = ValidationLoop()

        claude_api = MagicMock(return_value="Refined response")

        response, validation = loop.validate_and_refine(
            initial_response="Initial",
            original_prompt="Test",
            claude_api_call=claude_api
        )

        # Should have called Claude API
        assert claude_api.call_count == 1

        # Refinement prompt should include generic suggestions
        refinement_prompt = claude_api.call_args[0][0]
        assert "Add more detail" in refinement_prompt or "comprehensive" in refinement_prompt


# ==========================================
# VERBOSE MODE TESTS
# ==========================================

class TestVerboseMode:
    """Test verbose output mode."""

    @patch('validation_loop.ResponseValidator')
    @patch('builtins.print')
    def test_verbose_mode_prints_progress(self, mock_print, mock_validator_class):
        """Verbose mode should print progress."""
        mock_validator = MagicMock()
        mock_validator_class.return_value = mock_validator

        mock_validator.validate.return_value = {
            "confidence": 99.5,
            "is_acceptable": True
        }

        loop = ValidationLoop()
        claude_api = MagicMock()

        loop.validate_and_refine(
            initial_response="Response",
            original_prompt="Test",
            claude_api_call=claude_api,
            verbose=True
        )

        # Should have printed something
        assert mock_print.called

    @patch('validation_loop.ResponseValidator')
    @patch('builtins.print')
    def test_verbose_mode_shows_target_achieved(self, mock_print, mock_validator_class):
        """Verbose mode should show when target achieved."""
        mock_validator = MagicMock()
        mock_validator_class.return_value = mock_validator

        mock_validator.validate.return_value = {
            "confidence": 99.5,
            "is_acceptable": True
        }

        loop = ValidationLoop()
        claude_api = MagicMock()

        loop.validate_and_refine(
            initial_response="Response",
            original_prompt="Test",
            claude_api_call=claude_api,
            verbose=True
        )

        # Check that success message was printed
        print_calls = [str(call) for call in mock_print.call_args_list]
        success_printed = any("TARGET ACHIEVED" in str(call) or "✅" in str(call)
                             for call in print_calls)
        assert success_printed


# ==========================================
# CREATE REFINEMENT PROMPT TESTS
# ==========================================

class TestCreateRefinementPrompt:
    """Test _create_refinement_prompt method."""

    @patch('validation_loop.ResponseValidator')
    def test_creates_refinement_prompt_with_suggestions(self, mock_validator_class):
        """Should create refinement prompt with suggestions."""
        loop = ValidationLoop()

        prompt = loop._create_refinement_prompt(
            original_prompt="What is Python?",
            current_response="Python is a language",
            confidence=85.0,
            target_confidence=99.0,
            suggestions=["Add examples", "Explain features"],
            iteration=1
        )

        # Should include all key elements
        assert "What is Python?" in prompt
        assert "Python is a language" in prompt
        assert "85.0" in prompt or "85" in prompt
        assert "99.0" in prompt or "99" in prompt
        assert "Add examples" in prompt
        assert "Explain features" in prompt

    @patch('validation_loop.ResponseValidator')
    def test_refinement_prompt_includes_iteration_number(self, mock_validator_class):
        """Refinement prompt should include iteration number."""
        loop = ValidationLoop()

        prompt = loop._create_refinement_prompt(
            original_prompt="Test",
            current_response="Response",
            confidence=85.0,
            target_confidence=99.0,
            suggestions=["Improve"],
            iteration=3
        )

        assert "3" in prompt  # Iteration number


# ==========================================
# GET STATISTICS TESTS
# ==========================================

class TestGetStatistics:
    """Test get_statistics method."""

    @patch('validation_loop.ResponseValidator')
    def test_get_statistics_returns_config(self, mock_validator_class):
        """get_statistics should return configuration."""
        loop = ValidationLoop(max_iterations=10)

        stats = loop.get_statistics()

        assert stats["target_confidence"] == 99.0
        assert stats["max_iterations"] == 10


# ==========================================
# CONVENIENCE FUNCTION TESTS
# ==========================================

class TestValidateResponseToTarget:
    """Test validate_response_to_target convenience function."""

    @patch('validation_loop.ResponseValidator')
    def test_convenience_function_creates_loop_and_validates(self, mock_validator_class):
        """Convenience function should create loop and validate."""
        mock_validator = MagicMock()
        mock_validator_class.return_value = mock_validator

        mock_validator.validate.return_value = {
            "confidence": 99.5,
            "is_acceptable": True
        }

        claude_api = MagicMock()

        response, validation = validate_response_to_target(
            response="Test response",
            prompt="Test prompt",
            claude_api_call=claude_api,
            target_confidence=99.0,
            max_iterations=10,
            verbose=False
        )

        # Should return response and validation
        assert response == "Test response"
        assert validation["confidence"] == 99.5


# ==========================================
# INTEGRATION TESTS
# ==========================================

class TestValidationLoopIntegration:
    """Test real-world validation loop scenarios."""

    @patch('validation_loop.ResponseValidator')
    def test_complete_refinement_workflow(self, mock_validator_class):
        """Test complete workflow from poor to excellent response."""
        mock_validator = MagicMock()
        mock_validator_class.return_value = mock_validator

        # Simulate gradual improvement
        mock_validator.validate.side_effect = [
            {"confidence": 70.0, "is_acceptable": False, "suggestions": ["Too brief"]},
            {"confidence": 85.0, "is_acceptable": False, "suggestions": ["Need examples"]},
            {"confidence": 95.0, "is_acceptable": False, "suggestions": ["Add detail"]},
            {"confidence": 99.5, "is_acceptable": True, "suggestions": []}
        ]

        loop = ValidationLoop(max_iterations=10)

        responses = ["Response v2", "Response v3", "Response v4 - Excellent"]
        claude_api = MagicMock(side_effect=responses)

        final_response, validation = loop.validate_and_refine(
            initial_response="Response v1 - Poor",
            original_prompt="Complex question",
            claude_api_call=claude_api
        )

        # Should have refined 3 times
        assert claude_api.call_count == 3

        # Should return best response
        assert final_response == "Response v4 - Excellent"
        assert validation["confidence"] == 99.5


# Pytest marker for unit tests
pytestmark = pytest.mark.unit


if __name__ == "__main__":
    # Allow running tests directly
    pytest.main([__file__, "-v"])
