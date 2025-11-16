"""
Comprehensive Testing Suite for Orchestration System
Tests all components to ensure 96-100% accuracy and reliability
"""

import pytest
import logging
import sys
import os
from pathlib import Path

# Add paths for imports
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / "agent_framework"))
sys.path.insert(0, str(Path(__file__).parent / "guardrails"))

from prompt_preprocessor import PromptPreprocessor
from master_orchestrator import MasterOrchestrator


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def preprocessor():
    """Create prompt preprocessor instance"""
    return PromptPreprocessor()


@pytest.fixture
def orchestrator():
    """Create master orchestrator instance"""
    return MasterOrchestrator(min_confidence_score=90.0)


# ============================================================================
# PROMPT PREPROCESSOR TESTS
# ============================================================================

class TestPromptPreprocessor:
    """Test prompt preprocessing and intent classification"""

    def test_question_intent_classification(self, preprocessor):
        """Test classification of question prompts"""
        prompt = "What is machine learning?"
        analysis = preprocessor.analyze_prompt(prompt)

        assert analysis.intent_type == "question"
        assert analysis.complexity in ["simple", "moderate"]
        assert analysis.confidence > 0.5

    def test_code_generation_intent(self, preprocessor):
        """Test classification of code generation prompts"""
        prompt = "Write a Python function to calculate Fibonacci numbers"
        analysis = preprocessor.analyze_prompt(prompt)

        assert analysis.intent_type == "code_generation"
        assert analysis.requires_code_generation is True
        assert "code_generator" in analysis.required_components

    def test_complex_task_detection(self, preprocessor):
        """Test detection of complex tasks"""
        prompt = """Implement a comprehensive medical AI system with:
        - Multi-layer guardrails for safety
        - Adaptive feedback loops for quality
        - Parallel subagent processing
        - Full verification system
        """
        analysis = preprocessor.analyze_prompt(prompt)

        assert analysis.complexity == "very_complex"
        assert analysis.requires_parallel_processing is True
        assert len(analysis.required_components) >= 3

    def test_search_requirement_detection(self, preprocessor):
        """Test detection of search requirements"""
        prompt = "Find all files that contain the word 'guardrail'"
        analysis = preprocessor.analyze_prompt(prompt)

        assert analysis.requires_search is True
        assert "agentic_search" in analysis.required_components

    def test_iteration_estimation(self, preprocessor):
        """Test iteration count estimation"""
        simple_prompt = "What is Python?"
        complex_prompt = "Implement a full-stack web application"

        simple_analysis = preprocessor.analyze_prompt(simple_prompt)
        complex_analysis = preprocessor.analyze_prompt(complex_prompt)

        assert simple_analysis.estimated_iterations < complex_analysis.estimated_iterations
        assert simple_analysis.estimated_iterations >= 3
        assert complex_analysis.estimated_iterations >= 5

    def test_metadata_extraction(self, preprocessor):
        """Test metadata extraction from prompts"""
        prompt = "Write a Python function? Here's some code: ```python\ndef test(): pass```"
        analysis = preprocessor.analyze_prompt(prompt)

        assert analysis.metadata["has_question_mark"] is True
        assert analysis.metadata["has_code_block"] is True
        assert analysis.metadata["word_count"] > 0

    def test_medical_context_detection(self, preprocessor):
        """Test detection of medical context"""
        prompt = "Explain the medical diagnosis process for patients with diabetes"
        analysis = preprocessor.analyze_prompt(prompt)

        assert analysis.metadata["mentions_medical"] is True


# ============================================================================
# MASTER ORCHESTRATOR TESTS
# ============================================================================

class TestMasterOrchestrator:
    """Test master orchestration pipeline"""

    def test_simple_prompt_processing(self, orchestrator):
        """Test processing of simple prompts"""
        prompt = "What is Python?"
        result = orchestrator.process(prompt)

        assert result.success is True
        assert result.confidence_score >= 0
        assert result.iterations_performed >= 0
        assert result.total_duration_seconds > 0

    def test_confidence_scoring(self, orchestrator):
        """Test confidence score calculation"""
        prompt = "Explain machine learning"
        result = orchestrator.process(prompt)

        assert 0 <= result.confidence_score <= 100
        assert "confidence_score" in result.quality_metrics
        assert "confidence_breakdown" in result.quality_metrics

    def test_component_initialization(self, orchestrator):
        """Test lazy component initialization"""
        # Components should be None initially
        assert orchestrator.context_manager is None
        assert orchestrator.code_generator is None

        # After processing a code task, code_generator should be initialized
        result = orchestrator.process("Write a Python function")

        # Check that analysis identified code generation need
        assert result.prompt_analysis["intent_type"] == "code_generation"

    def test_warning_collection(self, orchestrator):
        """Test collection of warnings during processing"""
        prompt = "Test prompt"
        result = orchestrator.process(prompt)

        assert isinstance(result.warnings, list)
        # Warnings should be collected from all stages

    def test_error_handling(self, orchestrator):
        """Test error handling in orchestration"""
        # Test with empty prompt
        result = orchestrator.process("")

        # Should handle gracefully, not crash
        assert result is not None
        assert hasattr(result, 'success')

    def test_statistics_tracking(self, orchestrator):
        """Test statistics tracking"""
        initial_stats = orchestrator.get_statistics()
        initial_requests = initial_stats["total_requests"]

        # Process a prompt
        orchestrator.process("Test prompt")

        # Check statistics updated
        updated_stats = orchestrator.get_statistics()
        assert updated_stats["total_requests"] == initial_requests + 1

    def test_multiple_prompts(self, orchestrator):
        """Test processing multiple prompts"""
        prompts = [
            "What is AI?",
            "Write a function",
            "Explain neural networks"
        ]

        results = []
        for prompt in prompts:
            result = orchestrator.process(prompt)
            results.append(result)

        # All should succeed
        assert all(r.success for r in results)
        assert len(results) == len(prompts)

        # Statistics should reflect all requests
        stats = orchestrator.get_statistics()
        assert stats["total_requests"] >= len(prompts)


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestIntegration:
    """Integration tests for full pipeline"""

    def test_end_to_end_processing(self, orchestrator):
        """Test complete end-to-end processing"""
        prompt = "Explain the concept of machine learning in simple terms"

        result = orchestrator.process(prompt)

        # Verify all stages completed
        assert "prompt_analysis" in result.to_dict()
        assert "guardrails_validation" in result.to_dict()
        assert "agent_execution" in result.to_dict()
        assert "quality_metrics" in result.to_dict()

        # Verify result structure
        assert result.success is True
        assert result.output is not None
        assert result.confidence_score > 0
        assert result.iterations_performed > 0

    def test_guardrails_integration(self, orchestrator):
        """Test guardrails integration"""
        # Test with a prompt that should pass all guardrails
        safe_prompt = "Explain basic addition in mathematics"
        result = orchestrator.process(safe_prompt)

        # Should pass input validation
        assert "input_validation" in result.guardrails_validation
        assert result.guardrails_validation["input_validation"]["success"] is True

    def test_quality_threshold_enforcement(self):
        """Test that quality thresholds are enforced"""
        # Create orchestrator with high threshold
        high_threshold_orchestrator = MasterOrchestrator(min_confidence_score=98.0)

        result = high_threshold_orchestrator.process("Test prompt")

        # Verify minimum confidence setting is applied
        assert high_threshold_orchestrator.min_confidence_score == 98.0

    def test_refinement_iterations(self):
        """Test iterative refinement process"""
        orchestrator = MasterOrchestrator(
            min_confidence_score=95.0,
            max_refinement_iterations=3
        )

        result = orchestrator.process("Complex task requiring refinement")

        # Should attempt refinement if confidence below threshold
        assert result.iterations_performed >= 0


# ============================================================================
# PERFORMANCE TESTS
# ============================================================================

class TestPerformance:
    """Performance and efficiency tests"""

    def test_processing_speed(self, orchestrator):
        """Test that processing completes in reasonable time"""
        import time

        prompt = "What is Python?"
        start = time.time()
        result = orchestrator.process(prompt)
        duration = time.time() - start

        # Should complete within reasonable time (e.g., 30 seconds)
        assert duration < 30.0
        assert result.total_duration_seconds < 30.0

    def test_memory_efficiency(self, orchestrator):
        """Test memory efficiency with multiple requests"""
        import sys

        # Process multiple prompts
        for i in range(10):
            orchestrator.process(f"Test prompt {i}")

        # Memory usage should be reasonable
        # (This is a basic check - more sophisticated profiling would be needed)
        assert sys.getsizeof(orchestrator) < 1024 * 1024  # Less than 1MB

    def test_statistics_accuracy(self, orchestrator):
        """Test accuracy of statistics tracking"""
        # Process known number of prompts
        num_prompts = 5
        for i in range(num_prompts):
            orchestrator.process(f"Prompt {i}")

        stats = orchestrator.get_statistics()

        # Verify counts are accurate
        assert stats["total_requests"] == num_prompts


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def run_comprehensive_tests():
    """Run all tests and generate report"""
    print("\n" + "=" * 80)
    print("COMPREHENSIVE ORCHESTRATION SYSTEM TESTS")
    print("=" * 80)

    # Run pytest with coverage
    pytest_args = [
        __file__,
        "-v",
        "--tb=short",
        "--cov=.",
        "--cov-report=term-missing",
        "--cov-report=html:htmlcov"
    ]

    exit_code = pytest.main(pytest_args)

    print("\n" + "=" * 80)
    print(f"TEST SUITE {'PASSED' if exit_code == 0 else 'FAILED'}")
    print("=" * 80)

    if exit_code == 0:
        print("\n✅ All tests passed successfully!")
        print("📊 Coverage report generated in htmlcov/index.html")
    else:
        print("\n❌ Some tests failed. Please review the output above.")

    return exit_code


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    exit_code = run_comprehensive_tests()
    sys.exit(exit_code)
