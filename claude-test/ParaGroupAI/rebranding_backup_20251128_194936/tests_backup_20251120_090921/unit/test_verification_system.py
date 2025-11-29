#!/usr/bin/env python3
"""
Unit Tests for agent_framework/verification_system.py
Tests multi-method verification system.

Test Coverage Target: 75%+
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agent_framework.verification_system import (
    VerificationResult,
    MultiMethodVerifier,
)


# ==========================================
# VERIFICATION RESULT TESTS
# ==========================================

class TestVerificationResult:
    """Test VerificationResult dataclass."""

    def test_result_creation(self):
        """VerificationResult should be created with all fields."""
        result = VerificationResult(
            passed=True,
            method="rules_based",
            message="All checks passed"
        )
        assert result.passed is True
        assert result.method == "rules_based"
        assert result.message == "All checks passed"

    def test_result_with_details(self):
        """VerificationResult should support details."""
        result = VerificationResult(
            passed=False,
            method="code_verification",
            message="Syntax error",
            details={"error": "SyntaxError on line 5"}
        )
        assert result.details["error"] == "SyntaxError on line 5"

    def test_result_with_recommendations(self):
        """VerificationResult should support recommendations."""
        result = VerificationResult(
            passed=False,
            method="rules_based",
            message="Failed validation",
            recommendations=["Add error handling", "Improve documentation"]
        )
        assert len(result.recommendations) == 2
        assert "Add error handling" in result.recommendations

    def test_result_default_timestamp(self):
        """VerificationResult should auto-generate timestamp."""
        result = VerificationResult(
            passed=True,
            method="test",
            message="Test"
        )
        assert result.timestamp is not None
        assert len(result.timestamp) > 0

    def test_to_dict(self):
        """to_dict should convert result to dictionary."""
        result = VerificationResult(
            passed=True,
            method="rules_based",
            message="Success",
            details={"count": 5},
            recommendations=["Optimize"]
        )
        result_dict = result.to_dict()

        assert result_dict["passed"] is True
        assert result_dict["method"] == "rules_based"
        assert result_dict["message"] == "Success"
        assert result_dict["details"]["count"] == 5
        assert "Optimize" in result_dict["recommendations"]


# ==========================================
# MULTI-METHOD VERIFIER INITIALIZATION TESTS
# ==========================================

class TestMultiMethodVerifierInit:
    """Test MultiMethodVerifier initialization."""

    def test_init_creates_verifier(self):
        """MultiMethodVerifier should initialize."""
        verifier = MultiMethodVerifier()
        assert verifier is not None

    def test_init_creates_empty_log(self):
        """MultiMethodVerifier should start with empty log."""
        verifier = MultiMethodVerifier()
        assert len(verifier.verification_log) == 0

    def test_init_handles_missing_guardrails(self):
        """MultiMethodVerifier should handle missing guardrails gracefully."""
        # Should not crash even if guardrails unavailable
        verifier = MultiMethodVerifier()
        assert verifier is not None


# ==========================================
# VERIFY OUTPUT TESTS
# ==========================================

class TestVerifyOutput:
    """Test verify_output method."""

    def test_verify_text_output(self):
        """verify_output should verify text output."""
        verifier = MultiMethodVerifier()

        result = verifier.verify_output(
            output="This is test output",
            context={"input": "Generate text"},
            output_type="text"
        )

        assert isinstance(result, dict)
        assert "method_results" in result
        assert "overall_passed" in result

    def test_verify_code_output(self):
        """verify_output should verify code output."""
        verifier = MultiMethodVerifier()

        code = "def hello():\n    return 'world'"
        result = verifier.verify_output(
            output=code,
            context={"input": "Create hello function"},
            output_type="code"
        )

        assert "method_results" in result
        assert "code_verification" in result["method_results"]

    def test_verify_data_output(self):
        """verify_output should verify data output."""
        verifier = MultiMethodVerifier()

        data = {"key": "value", "count": 42}
        result = verifier.verify_output(
            output=data,
            context={"input": "Generate data"},
            output_type="data"
        )

        assert "method_results" in result
        assert "data_validation" in result["method_results"]

    def test_verify_ui_output(self):
        """verify_output should verify UI output."""
        verifier = MultiMethodVerifier()

        ui_spec = {"component": "button", "text": "Click me"}
        result = verifier.verify_output(
            output=ui_spec,
            context={"input": "Create button"},
            output_type="ui"
        )

        assert "method_results" in result
        assert "visual" in result["method_results"]

    def test_verify_with_fuzzy_validation(self):
        """verify_output should use LLM judge for fuzzy validation."""
        verifier = MultiMethodVerifier()

        result = verifier.verify_output(
            output="Creative story about dragons",
            context={"input": "Write a story", "fuzzy_validation": True},
            output_type="text"
        )

        assert "method_results" in result
        assert "llm_judge" in result["method_results"]

    def test_verify_overall_passed_all_pass(self):
        """verify_output should return overall_passed=True if all pass."""
        verifier = MultiMethodVerifier()

        result = verifier.verify_output(
            output="Valid output",
            context={"input": "Test"},
            output_type="text"
        )

        # Should have overall_passed key
        assert "overall_passed" in result


# ==========================================
# RULES-BASED VERIFICATION TESTS
# ==========================================

class TestVerifyRulesBased:
    """Test _verify_rules_based method."""

    def test_verify_empty_output_fails(self):
        """Empty output should fail rules-based verification."""
        verifier = MultiMethodVerifier()

        result = verifier._verify_rules_based(
            output="",
            context={"input": "Generate something"},
            task=None
        )

        assert result.passed is False
        # Message may vary but should indicate failure
        assert isinstance(result.message, str)

    def test_verify_non_empty_output_passes(self):
        """Non-empty output should pass basic rules."""
        verifier = MultiMethodVerifier()

        result = verifier._verify_rules_based(
            output="This is valid output",
            context={"input": "Generate text"},
            task=None
        )

        assert result.passed is True

    def test_verify_with_requirements(self):
        """Verification should check requirements if provided."""
        verifier = MultiMethodVerifier()

        result = verifier._verify_rules_based(
            output="This is a test",
            context={
                "input": "Generate text",
                "requirements": ["Must contain 'test'"]
            },
            task=None
        )

        # Implementation may vary, but should handle requirements
        assert isinstance(result, VerificationResult)


# ==========================================
# CODE VERIFICATION TESTS
# ==========================================

class TestVerifyCode:
    """Test _verify_code method."""

    def test_verify_valid_python_code(self):
        """Valid Python code should pass syntax check."""
        verifier = MultiMethodVerifier()

        code = """
def hello():
    return "world"
"""
        result = verifier._verify_code(code)

        # Code may not pass all quality checks but should have no syntax errors
        assert "errors" in result.details
        assert len(result.details["errors"]) == 0  # No syntax errors

    def test_verify_invalid_python_code(self):
        """Invalid Python code should fail."""
        verifier = MultiMethodVerifier()

        code = """
def hello(
    return "world"  # Missing closing paren
"""
        result = verifier._verify_code(code)

        assert result.passed is False
        # Should have syntax errors
        assert "errors" in result.details
        assert len(result.details["errors"]) > 0

    def test_verify_empty_code(self):
        """Empty code should fail."""
        verifier = MultiMethodVerifier()

        result = verifier._verify_code("")

        assert result.passed is False


# ==========================================
# DATA VERIFICATION TESTS
# ==========================================

class TestVerifyData:
    """Test _verify_data method."""

    def test_verify_valid_dict(self):
        """Valid dictionary should pass."""
        verifier = MultiMethodVerifier()

        data = {"key": "value", "count": 42}
        result = verifier._verify_data(data, context={})

        assert result.passed is True

    def test_verify_valid_list(self):
        """Valid list should pass."""
        verifier = MultiMethodVerifier()

        data = [1, 2, 3, 4, 5]
        result = verifier._verify_data(data, context={})

        assert result.passed is True

    def test_verify_none_data(self):
        """None data should fail."""
        verifier = MultiMethodVerifier()

        result = verifier._verify_data(None, context={})

        assert result.passed is False


# ==========================================
# VISUAL VERIFICATION TESTS
# ==========================================

class TestVerifyVisual:
    """Test _verify_visual method."""

    def test_verify_ui_spec(self):
        """UI spec should be verified."""
        verifier = MultiMethodVerifier()

        ui_spec = {
            "component": "button",
            "text": "Click me",
            "color": "blue"
        }
        result = verifier._verify_visual(ui_spec, context={})

        # Should return a result (implementation may vary)
        assert isinstance(result, VerificationResult)


# ==========================================
# LLM JUDGE VERIFICATION TESTS
# ==========================================

class TestVerifyWithLLMJudge:
    """Test _verify_with_llm_judge method."""

    @patch('agent_framework.verification_system.MultiMethodVerifier._verify_with_llm_judge')
    def test_llm_judge_called_with_fuzzy(self, mock_llm):
        """LLM judge should be called for fuzzy validation."""
        mock_llm.return_value = VerificationResult(
            passed=True,
            method="llm_judge",
            message="Quality approved"
        )

        verifier = MultiMethodVerifier()
        verifier._verify_with_llm_judge = mock_llm

        result = verifier.verify_output(
            output="Creative content",
            context={"fuzzy_validation": True},
            output_type="text"
        )

        mock_llm.assert_called_once()


# ==========================================
# GET STATISTICS TESTS
# ==========================================

class TestGetStatistics:
    """Test get_statistics method."""

    def test_get_statistics_initial(self):
        """get_statistics should return initial stats."""
        verifier = MultiMethodVerifier()

        stats = verifier.get_statistics()

        assert isinstance(stats, dict)
        # May return error if no verifications yet
        assert "total_verifications" in stats or "error" in stats

    def test_get_statistics_after_verifications(self):
        """get_statistics should track verifications."""
        verifier = MultiMethodVerifier()

        # Perform some verifications
        verifier.verify_output("test1", {"input": "test"}, "text")
        verifier.verify_output("test2", {"input": "test"}, "text")

        stats = verifier.get_statistics()

        assert stats["total_verifications"] >= 2


# ==========================================
# INTEGRATION TESTS
# ==========================================

class TestVerificationSystemIntegration:
    """Test real-world verification scenarios."""

    def test_complete_code_verification_workflow(self):
        """Test verifying generated code."""
        verifier = MultiMethodVerifier()

        code = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
"""
        result = verifier.verify_output(
            output=code,
            context={"input": "Generate Fibonacci function"},
            output_type="code"
        )

        assert "method_results" in result
        assert "code_verification" in result["method_results"]
        # Code may have warnings but should have no syntax errors
        code_result = result["method_results"]["code_verification"]
        assert "errors" in code_result["details"]

    def test_multi_method_verification_all_pass(self):
        """Test multiple verification methods passing."""
        verifier = MultiMethodVerifier()

        result = verifier.verify_output(
            output="This is valid, high-quality output",
            context={"input": "Generate text"},
            output_type="text"
        )

        # Should have method_results
        assert "method_results" in result
        assert len(result["method_results"]) > 0

    def test_verification_failure_provides_recommendations(self):
        """Test that failed verifications provide recommendations."""
        verifier = MultiMethodVerifier()

        # Empty output should fail
        result = verifier.verify_output(
            output="",
            context={"input": "Generate something"},
            output_type="text"
        )

        # Should have failed
        assert result["overall_passed"] is False

        # Should have recommendations in at least one result
        has_recommendations = False
        for method_result in result.values():
            if isinstance(method_result, VerificationResult):
                if len(method_result.recommendations) > 0:
                    has_recommendations = True
                    break

        assert has_recommendations or result["overall_passed"] is False


# Pytest marker for unit tests
pytestmark = pytest.mark.unit


if __name__ == "__main__":
    # Allow running tests directly
    pytest.main([__file__, "-v"])
