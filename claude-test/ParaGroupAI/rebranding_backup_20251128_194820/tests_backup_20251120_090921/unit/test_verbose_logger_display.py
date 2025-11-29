"""
Comprehensive display tests for verbose_logger.py module.

This test suite targets uncovered display methods in verbose_logger.py,
focusing on specialized output functions that weren't covered by basic tests.

Target Coverage: Boost verbose_logger.py from 26% to 65%+
Strategy: Test all display methods with actual output
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from verbose_logger import VerboseLogger


class TestLayer8HallucinationDetection:
    """Test Layer 8 hallucination detection display."""

    def test_layer8_pass_all_methods(self, capsys):
        """Should display Layer 8 with all methods passing."""
        logger = VerboseLogger(enabled=True)

        methods_passed = {
            "cross_reference": True,
            "source_verification": True,
            "consistency_check": True,
            "claim_validation": True,
            "temporal_accuracy": True,
            "logical_coherence": True,
            "citation_check": True,
            "expert_knowledge": True
        }

        logger.hallucination_detection_layer(
            passed=True,
            confidence=98.5,
            detections=0,
            methods_passed=methods_passed
        )

        captured = capsys.readouterr()
        assert "Layer 8: Hallucination Detection" in captured.out
        assert "✅ PASS" in captured.out
        assert "98.5%" in captured.out
        assert "Cross Reference" in captured.out
        assert "8 Detection Methods" in captured.out

    def test_layer8_fail_some_methods(self, capsys):
        """Should display Layer 8 with some methods failing."""
        logger = VerboseLogger(enabled=True)

        methods_passed = {
            "cross_reference": True,
            "source_verification": False,
            "consistency_check": True,
            "claim_validation": False,
            "temporal_accuracy": True,
            "logical_coherence": True,
            "citation_check": False,
            "expert_knowledge": True
        }

        logger.hallucination_detection_layer(
            passed=False,
            confidence=75.0,
            detections=3,
            methods_passed=methods_passed
        )

        captured = capsys.readouterr()
        assert "❌ FAIL" in captured.out
        assert "75.0%" in captured.out
        assert "Detections Found: 3" in captured.out

    def test_layer8_disabled_mode(self, capsys):
        """Should produce no output when disabled."""
        logger = VerboseLogger(enabled=False)

        logger.hallucination_detection_layer(
            passed=True,
            confidence=99.0,
            detections=0,
            methods_passed={}
        )

        captured = capsys.readouterr()
        assert captured.out == ""


class TestEnhancedVerificationSystem:
    """Test enhanced verification system display."""

    def test_enhanced_verification_above_target(self, capsys):
        """Should display verification with confidence above target."""
        logger = VerboseLogger(enabled=True)

        methods = {
            "Logical Consistency": {"passed": True, "confidence": 99.2, "agents": 50},
            "Factual Accuracy": {"passed": True, "confidence": 98.8, "agents": 75},
            "Completeness": {"passed": True, "confidence": 99.5, "agents": 40},
            "Quality Assurance": {"passed": True, "confidence": 99.0, "agents": 35}
        }

        logger.enhanced_verification_system(
            confidence=99.1,
            agents_used=200,
            methods=methods
        )

        captured = capsys.readouterr()
        assert "ENHANCED VERIFICATION SYSTEM" in captured.out
        assert "500-Agent Validation" in captured.out
        assert "99.1%" in captured.out
        assert "200/500" in captured.out
        assert "✅ CONFIDENCE TARGET ACHIEVED" in captured.out
        assert "99.1% ≥ 99.0%" in captured.out

    def test_enhanced_verification_below_target(self, capsys):
        """Should display verification with confidence below target."""
        logger = VerboseLogger(enabled=True)

        methods = {
            "Logical Consistency": {"passed": True, "confidence": 95.0, "agents": 30},
            "Factual Accuracy": {"passed": False, "confidence": 87.5, "agents": 40}
        }

        logger.enhanced_verification_system(
            confidence=91.2,
            agents_used=70,
            methods=methods
        )

        captured = capsys.readouterr()
        assert "⚠️  BELOW TARGET" in captured.out
        assert "91.2% < 99.0%" in captured.out
        assert "refinement needed" in captured.out

    def test_enhanced_verification_method_display(self, capsys):
        """Should display all verification methods correctly."""
        logger = VerboseLogger(enabled=True)

        methods = {
            "Method A": {"passed": True, "confidence": 99.0, "agents": 50},
            "Method B": {"passed": False, "confidence": 85.0, "agents": 30}
        }

        logger.enhanced_verification_system(
            confidence=92.0,
            agents_used=80,
            methods=methods
        )

        captured = capsys.readouterr()
        assert "Method A" in captured.out
        assert "Method B" in captured.out
        assert "99.0%" in captured.out
        assert "85.0%" in captured.out
        assert "50 agents" in captured.out
        assert "30 agents" in captured.out

    def test_enhanced_verification_disabled(self, capsys):
        """Should produce no output when disabled."""
        logger = VerboseLogger(enabled=False)

        logger.enhanced_verification_system(
            confidence=99.5,
            agents_used=100,
            methods={}
        )

        captured = capsys.readouterr()
        assert captured.out == ""


class TestAgentCapacityEnhanced:
    """Test enhanced agent capacity display."""

    def test_agent_capacity_low_utilization(self, capsys):
        """Should display low utilization status."""
        logger = VerboseLogger(enabled=True)

        logger.agent_capacity_enhanced(
            current=50,
            maximum=500,
            utilization=10.0
        )

        captured = capsys.readouterr()
        assert "AGENT ORCHESTRATION" in captured.out
        assert "500 Agents" in captured.out
        assert "Current Allocation: 50 agents" in captured.out
        assert "Maximum Capacity: 500 agents" in captured.out
        assert "Utilization: 10.0%" in captured.out
        assert "Available: 450 agents" in captured.out
        assert "🟢 LOW" in captured.out
        assert "suitable for simple tasks" in captured.out

    def test_agent_capacity_moderate_utilization(self, capsys):
        """Should display moderate utilization status."""
        logger = VerboseLogger(enabled=True)

        logger.agent_capacity_enhanced(
            current=150,
            maximum=500,
            utilization=30.0
        )

        captured = capsys.readouterr()
        assert "🟢 MODERATE" in captured.out
        assert "suitable for complex tasks" in captured.out

    def test_agent_capacity_high_utilization(self, capsys):
        """Should display high utilization status."""
        logger = VerboseLogger(enabled=True)

        logger.agent_capacity_enhanced(
            current=350,
            maximum=500,
            utilization=70.0
        )

        captured = capsys.readouterr()
        assert "🟡 HIGH" in captured.out
        assert "enterprise-scale processing" in captured.out

    def test_agent_capacity_full_utilization(self, capsys):
        """Should display full utilization status."""
        logger = VerboseLogger(enabled=True)

        logger.agent_capacity_enhanced(
            current=450,
            maximum=500,
            utilization=90.0
        )

        captured = capsys.readouterr()
        assert "🔴 FULL" in captured.out
        assert "maximum capacity utilized" in captured.out

    def test_agent_capacity_progress_bar(self, capsys):
        """Should display progress bar."""
        logger = VerboseLogger(enabled=True)

        logger.agent_capacity_enhanced(
            current=250,
            maximum=500,
            utilization=50.0
        )

        captured = capsys.readouterr()
        assert "[" in captured.out
        assert "]" in captured.out
        assert "250/500" in captured.out
        # Should have some filled and some empty blocks
        assert "█" in captured.out
        assert "░" in captured.out

    def test_agent_capacity_scaling_standards(self, capsys):
        """Should display scaling standards."""
        logger = VerboseLogger(enabled=True)

        logger.agent_capacity_enhanced(
            current=100,
            maximum=500,
            utilization=20.0
        )

        captured = capsys.readouterr()
        assert "Scaling Standards:" in captured.out
        assert "Simple tasks: 8-25 agents" in captured.out
        assert "Moderate tasks: 25-100 agents" in captured.out
        assert "Complex tasks: 100-250 agents" in captured.out
        assert "Enterprise: 250-500 agents" in captured.out

    def test_agent_capacity_disabled(self, capsys):
        """Should produce no output when disabled."""
        logger = VerboseLogger(enabled=False)

        logger.agent_capacity_enhanced(
            current=100,
            maximum=500,
            utilization=20.0
        )

        captured = capsys.readouterr()
        assert captured.out == ""


class TestConfidenceGuaranteeStatus:
    """Test confidence guarantee status display."""

    def test_confidence_above_target(self, capsys):
        """Should display confidence above target."""
        logger = VerboseLogger(enabled=True)

        logger.confidence_guarantee_status(
            current=99.5,
            target=99.0,
            iteration=2,
            max_iterations=20
        )

        captured = capsys.readouterr()
        assert "99-100% CONFIDENCE GUARANTEE" in captured.out
        assert "Mandatory Requirement" in captured.out
        assert "Current Confidence: 99.5%" in captured.out
        assert "Target Confidence: 99.0%" in captured.out
        assert "NON-NEGOTIABLE" in captured.out
        assert "Iteration: 2/20" in captured.out

    def test_confidence_below_target(self, capsys):
        """Should display confidence below target."""
        logger = VerboseLogger(enabled=True)

        logger.confidence_guarantee_status(
            current=95.0,
            target=99.0,
            iteration=5,
            max_iterations=20
        )

        captured = capsys.readouterr()
        assert "95.0%" in captured.out
        assert "99.0%" in captured.out
        assert "5/20" in captured.out

    def test_confidence_at_max_iterations(self, capsys):
        """Should display at maximum iterations."""
        logger = VerboseLogger(enabled=True)

        logger.confidence_guarantee_status(
            current=98.0,
            target=99.0,
            iteration=20,
            max_iterations=20
        )

        captured = capsys.readouterr()
        assert "20/20" in captured.out

    def test_confidence_disabled(self, capsys):
        """Should produce no output when disabled."""
        logger = VerboseLogger(enabled=False)

        logger.confidence_guarantee_status(
            current=99.5,
            target=99.0,
            iteration=1,
            max_iterations=20
        )

        captured = capsys.readouterr()
        assert captured.out == ""


class TestAdditionalDisplayMethods:
    """Test additional display methods."""

    def test_prompt_info_display(self, capsys):
        """Should display prompt information."""
        logger = VerboseLogger(enabled=True)

        logger.prompt_info(prompt_length=150, target_confidence=99.0)

        captured = capsys.readouterr()
        assert "150" in captured.out
        assert "99.0" in captured.out

    def test_framework_benefits_display(self, capsys):
        """Should display framework benefits."""
        logger = VerboseLogger(enabled=True)

        logger.framework_benefits()

        captured = capsys.readouterr()
        assert "ULTRATHINK" in captured.out or "Framework" in captured.out

    def test_processing_step_display(self, capsys):
        """Should display processing step."""
        logger = VerboseLogger(enabled=True)

        logger.processing_step("Analyzing prompt")

        captured = capsys.readouterr()
        assert "Analyzing prompt" in captured.out
        assert "[VERBOSE]" in captured.out

    def test_guardrail_layer_display(self, capsys):
        """Should display guardrail layer."""
        logger = VerboseLogger(enabled=True)

        logger.guardrail_layer(
            layer_num=1,
            layer_name="Test Layer",
            layer_purpose="Testing",
            passed=True,
            details={"Check1": "Passed", "Check2": "Passed"}
        )

        captured = capsys.readouterr()
        assert "Layer 1" in captured.out
        assert "Test Layer" in captured.out
        assert "Testing" in captured.out
        assert "✅ PASS" in captured.out


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
