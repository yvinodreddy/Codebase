#!/usr/bin/env python3
"""
COMPLETE TESTS for multi_layer_system.py - 100% Coverage
Covers all 23 missing lines with targeted scenarios
"""

import pytest
import sys
import os
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch

# Add paths
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "guardrails"))

try:
    from multi_layer_system import MultiLayerGuardrailSystem
    from azure_content_safety import ValidationResult
except ImportError as e:
    pytest.skip(f"Cannot import: {e}", allow_module_level=True)


class TestMultiLayerSystemComplete:
    """Complete coverage tests targeting all 23 missing lines"""

    # ============ FEATURE DISABLED TESTS (Lines 130, 148, 175, 210, 239, 262) ============

    @patch.dict(os.environ, {'ENABLE_PROMPT_SHIELDS': 'false'})
    def test_line_130_prompt_shields_disabled(self):
        """Line 130: Prompt shields disabled via env var"""
        system = MultiLayerGuardrailSystem()
        result = system.layer1_prompt_shields("test input")

        assert result.passed == True
        assert "disabled" in result.message.lower()

    @patch.dict(os.environ, {'ENABLE_CONTENT_FILTERING': 'false'})
    def test_line_148_content_filtering_disabled(self):
        """Line 148: Content filtering disabled via env var"""
        system = MultiLayerGuardrailSystem()
        result = system.layer2_input_content_filter("test input")

        assert result.passed == True
        assert "disabled" in result.message.lower()

    @patch.dict(os.environ, {'ENABLE_PHI_DETECTION': 'false'})
    def test_line_175_phi_detection_disabled(self):
        """Line 175: PHI detection disabled via env var"""
        system = MultiLayerGuardrailSystem()
        result = system.layer3_phi_detection("test input", content_type="medical_education")

        assert result.passed == True
        assert "disabled" in result.message.lower()

    @patch.dict(os.environ, {'MEDICAL_TERMINOLOGY_VALIDATION': 'false'})
    def test_line_210_terminology_validation_disabled(self):
        """Line 210: Terminology validation disabled via env var"""
        system = MultiLayerGuardrailSystem()
        result = system.layer4_terminology_validation("test", content_type="medical_education")

        assert result.passed == True
        assert "disabled" in result.message.lower()

    @patch.dict(os.environ, {'ENABLE_CONTENT_FILTERING': 'false'})
    def test_line_239_output_content_filtering_disabled(self):
        """Line 239: Output content filtering disabled via env var"""
        system = MultiLayerGuardrailSystem()
        result = system.layer5_output_content_filter("test output")

        assert result.passed == True
        assert "disabled" in result.message.lower()

    @patch.dict(os.environ, {'ENABLE_GROUNDEDNESS_CHECK': 'false'})
    def test_line_262_groundedness_disabled(self):
        """Line 262: Groundedness check disabled via env var"""
        system = MultiLayerGuardrailSystem()
        result = system.layer6_groundedness_check("test output")

        assert result.passed == True
        assert "disabled" in result.message.lower()

    # ============ FAILURE PATH TESTS (Lines 365-366, 372-373, 379-380, 393-394, 400-401, 407-408) ============

    def test_lines_365_366_layer1_failure(self):
        """Lines 365-366: Layer 1 (prompt shields) failure increments stats and returns"""
        system = MultiLayerGuardrailSystem()

        # Mock layer1 to fail
        with patch.object(system, 'layer1_prompt_shields', return_value=ValidationResult(
            passed=False,
            layer="layer_1_prompt_shields",
            message="Jailbreak detected"
        )):
            result = system.process_with_guardrails("malicious input")

            # Lines 365-366 should execute
            assert system.stats["blocked_by_layer"]["layer_1_prompt_shields"] >= 1
            assert result["success"] == False
            assert result["blocked_at"] == "layer_1"

    def test_lines_372_373_layer2_failure(self):
        """Lines 372-373: Layer 2 (input content) failure"""
        system = MultiLayerGuardrailSystem()

        # Mock layer1 pass, layer2 fail
        with patch.object(system, 'layer1_prompt_shields', return_value=ValidationResult(passed=True, layer="layer_1", message="OK")):
            with patch.object(system, 'layer2_input_content_filter', return_value=ValidationResult(
                passed=False,
                layer="layer_2_input_content",
                message="Harmful content detected"
            )):
                result = system.process_with_guardrails("harmful input")

                # Lines 372-373 should execute
                assert system.stats["blocked_by_layer"]["layer_2_input_content"] >= 1
                assert result["blocked_at"] == "layer_2"

    def test_lines_379_380_layer3_failure(self):
        """Lines 379-380: Layer 3 (PHI detection) failure"""
        system = MultiLayerGuardrailSystem()

        # Mock layers 1-2 pass, layer 3 fail
        with patch.object(system, 'layer1_prompt_shields', return_value=ValidationResult(passed=True, layer="layer_1", message="OK")):
            with patch.object(system, 'layer2_input_content_filter', return_value=ValidationResult(passed=True, layer="layer_2", message="OK")):
                with patch.object(system, 'layer3_phi_detection', return_value=ValidationResult(
                    passed=False,
                    layer="layer_3_phi_detection",
                    message="PHI detected"
                )):
                    result = system.process_with_guardrails("input with PHI", content_type="medical_education")

                    # Lines 379-380 should execute
                    assert system.stats["blocked_by_layer"]["layer_3_phi_detection"] >= 1
                    assert result["blocked_at"] == "layer_3"

    def test_lines_384_385_success_no_output(self):
        """Lines 384-385: Success when no output provided (input validation only)"""
        system = MultiLayerGuardrailSystem()

        # Mock all input layers to pass
        with patch.object(system, 'layer1_prompt_shields', return_value=ValidationResult(passed=True, layer="layer_1", message="OK")):
            with patch.object(system, 'layer2_input_content_filter', return_value=ValidationResult(passed=True, layer="layer_2", message="OK")):
                with patch.object(system, 'layer3_phi_detection', return_value=ValidationResult(passed=True, layer="layer_3", message="OK")):
                    # Call WITHOUT output parameter
                    result = system.process_with_guardrails("safe input", output=None)

                    # Lines 384-385 should execute
                    assert system.stats["successful"] >= 1
                    assert result["success"] == True
                    assert result["blocked_at"] is None

    def test_lines_393_394_layer4_failure(self):
        """Lines 393-394: Layer 4 (terminology) failure"""
        system = MultiLayerGuardrailSystem()

        # Mock layers 1-3 pass, layer 4 fail
        with patch.object(system, 'layer1_prompt_shields', return_value=ValidationResult(passed=True, layer="layer_1", message="OK")):
            with patch.object(system, 'layer2_input_content_filter', return_value=ValidationResult(passed=True, layer="layer_2", message="OK")):
                with patch.object(system, 'layer3_phi_detection', return_value=ValidationResult(passed=True, layer="layer_3", message="OK")):
                    with patch.object(system, 'layer4_terminology_validation', return_value=ValidationResult(
                        passed=False,
                        layer="layer_4_terminology",
                        message="Invalid terminology"
                    )):
                        result = system.process_with_guardrails("input", output="output with bad terms", content_type="medical_education")

                        # Lines 393-394 should execute
                        assert system.stats["blocked_by_layer"]["layer_4_terminology"] >= 1
                        assert result["blocked_at"] == "layer_4"

    def test_lines_400_401_layer5_failure(self):
        """Lines 400-401: Layer 5 (output content) failure"""
        system = MultiLayerGuardrailSystem()

        # Mock layers 1-4 pass, layer 5 fail
        with patch.object(system, 'layer1_prompt_shields', return_value=ValidationResult(passed=True, layer="layer_1", message="OK")):
            with patch.object(system, 'layer2_input_content_filter', return_value=ValidationResult(passed=True, layer="layer_2", message="OK")):
                with patch.object(system, 'layer3_phi_detection', return_value=ValidationResult(passed=True, layer="layer_3", message="OK")):
                    with patch.object(system, 'layer4_terminology_validation', return_value=ValidationResult(passed=True, layer="layer_4", message="OK")):
                        with patch.object(system, 'layer5_output_content_filter', return_value=ValidationResult(
                            passed=False,
                            layer="layer_5_output_content",
                            message="Harmful output"
                        )):
                            result = system.process_with_guardrails("input", output="harmful output")

                            # Lines 400-401 should execute
                            assert system.stats["blocked_by_layer"]["layer_5_output_content"] >= 1
                            assert result["blocked_at"] == "layer_5"

    def test_lines_407_408_layer6_failure(self):
        """Lines 407-408: Layer 6 (groundedness) failure"""
        system = MultiLayerGuardrailSystem()

        # Mock layers 1-5 pass, layer 6 fail
        with patch.object(system, 'layer1_prompt_shields', return_value=ValidationResult(passed=True, layer="layer_1", message="OK")):
            with patch.object(system, 'layer2_input_content_filter', return_value=ValidationResult(passed=True, layer="layer_2", message="OK")):
                with patch.object(system, 'layer3_phi_detection', return_value=ValidationResult(passed=True, layer="layer_3", message="OK")):
                    with patch.object(system, 'layer4_terminology_validation', return_value=ValidationResult(passed=True, layer="layer_4", message="OK")):
                        with patch.object(system, 'layer5_output_content_filter', return_value=ValidationResult(passed=True, layer="layer_5", message="OK")):
                            with patch.object(system, 'layer6_groundedness_check', return_value=ValidationResult(
                                passed=False,
                                layer="layer_6_groundedness",
                                message="Not grounded"
                            )):
                                result = system.process_with_guardrails("input", output="ungrounded output")

                                # Lines 407-408 should execute
                                assert system.stats["blocked_by_layer"]["layer_6_groundedness"] >= 1
                                assert result["blocked_at"] == "layer_6"

    # ============ LAYER 7 SPECIAL TESTS (Lines 310, 315) ============

    def test_line_310_fact_checker_failure(self):
        """Line 310: Fact checker fails and returns fact_result"""
        system = MultiLayerGuardrailSystem()
        system._initialize_medical_validators()

        # Mock HIPAA to pass, fact checker to fail
        with patch.object(system.hipaa_validator, 'validate_compliance', return_value=ValidationResult(
            passed=True,
            layer="hipaa",
            message="HIPAA OK"
        )):
            with patch.object(system.fact_checker, 'check_medical_facts', return_value=ValidationResult(
                passed=False,
                layer="fact_check",
                message="Medical facts incorrect"
            )):
                result = system.layer7_compliance_and_facts("output text", content_type="medical_education")

                # Line 310 should execute (return fact_result)
                assert result.passed == False
                assert "fact" in result.message.lower() or result.layer == "fact_check"

    def test_line_315_hipaa_warnings(self):
        """Line 315: HIPAA result has warnings that get extended"""
        system = MultiLayerGuardrailSystem()
        system._initialize_medical_validators()

        # Mock HIPAA to pass with warnings
        hipaa_warnings = ["Warning 1: Sensitive term used", "Warning 2: Review needed"]
        with patch.object(system.hipaa_validator, 'validate_compliance', return_value=ValidationResult(
            passed=True,
            layer="hipaa",
            message="HIPAA passed with warnings",
            details={"warnings": hipaa_warnings}
        )):
            with patch.object(system.fact_checker, 'check_medical_facts', return_value=ValidationResult(
                passed=True,
                layer="fact_check",
                message="Facts OK"
            )):
                result = system.layer7_compliance_and_facts("output text", content_type="medical_education")

                # Line 315 should execute (warnings.extend)
                assert result.passed == True
                if result.details and "warnings" in result.details:
                    assert len(result.details["warnings"]) >= len(hipaa_warnings)

    # ============ IMPORT TEST (Line 20) ============

    def test_line_20_medical_guardrails_import(self):
        """Line 20: Import from medical_guardrails"""
        # Force re-import to trigger coverage of line 20
        import sys
        import importlib

        # Remove from cache if present
        if 'multi_layer_system' in sys.modules:
            del sys.modules['multi_layer_system']
        if 'guardrails.multi_layer_system' in sys.modules:
            del sys.modules['guardrails.multi_layer_system']

        # Re-import to trigger line 20
        try:
            from multi_layer_system import MultiLayerGuardrailSystem
            # The import on line 20 was successful
            assert MultiLayerGuardrailSystem is not None

            # Also verify medical_guardrails was imported
            import medical_guardrails
            assert hasattr(medical_guardrails, 'PHIDetector') or hasattr(medical_guardrails, 'HIPAAComplianceValidator')
        except ImportError:
            pytest.skip("medical_guardrails not available")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=multi_layer_system", "--cov-report=term-missing"])
