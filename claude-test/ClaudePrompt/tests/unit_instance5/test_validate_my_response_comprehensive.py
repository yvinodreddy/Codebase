#!/usr/bin/env python3
"""
Comprehensive REAL tests for validate_my_response.py
Tests actual code execution with 90%+ coverage target
"""

import pytest
import sys
import os
import json
from pathlib import Path
from unittest.mock import patch, Mock, MagicMock
import argparse

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Import the ACTUAL module being tested
from validate_my_response import ResponseValidator

class TestResponseValidator:
    """Comprehensive tests for ResponseValidator class"""

    def setup_method(self):
        """Setup test fixtures"""
        self.validator = ResponseValidator()

    def test_initialization(self):
        """Test ResponseValidator initialization with real objects"""
        # Verify the validator is properly initialized
        assert self.validator is not None
        assert hasattr(self.validator, 'guardrails')
        assert hasattr(self.validator, 'verifier')
        assert hasattr(self.validator, 'target_confidence')

        # Check target confidence is set correctly
        assert self.validator.target_confidence == 99.0

    def test_validate_with_good_response(self):
        """Test validation with a high-quality response"""
        response = """
        The mathematical sum of 2+2 equals 4.
        This is based on fundamental arithmetic principles where addition
        combines quantities. In base-10 number system, 2+2=4 is axiomatic.
        """
        prompt = "What is 2+2?"

        result = self.validator.validate(response, prompt, iteration=1)

        # Check result structure
        assert isinstance(result, dict)
        assert 'confidence' in result
        assert 'is_acceptable' in result
        assert 'suggestions' in result
        assert 'iteration' in result

        # Confidence should be a float between 0 and 100
        assert isinstance(result['confidence'], (int, float))
        assert 0 <= result['confidence'] <= 100

    def test_validate_with_poor_response(self):
        """Test validation with a low-quality response"""
        response = "idk"  # Very poor response
        prompt = "Explain quantum computing in detail"

        result = self.validator.validate(response, prompt, iteration=1)

        # Should have low confidence
        assert result['confidence'] < 50
        assert result['is_acceptable'] == False
        assert len(result['suggestions']) > 0  # Should have improvement suggestions

    def test_validate_empty_response(self):
        """Test validation with empty response"""
        response = ""
        prompt = "What is the capital of France?"

        result = self.validator.validate(response, prompt, iteration=1)

        # Empty response should have very low confidence
        assert result['confidence'] < 10
        assert result['is_acceptable'] == False
        assert any('empty' in s.lower() or 'no content' in s.lower()
                  for s in result['suggestions'])

    def test_validate_with_iterations(self):
        """Test validation across multiple iterations"""
        response = "The answer is 42"
        prompt = "What is the meaning of life?"

        # Test different iteration numbers
        for i in range(1, 5):
            result = self.validator.validate(response, prompt, iteration=i)
            assert result['iteration'] == i
            assert isinstance(result['confidence'], (int, float))

    def test_validate_without_prompt(self):
        """Test validation when no original prompt provided"""
        response = "This is a test response without context"

        result = self.validator.validate(response, prompt=None, iteration=1)

        # Should still return valid result structure
        assert isinstance(result, dict)
        assert 'confidence' in result
        assert 'is_acceptable' in result

    def test_validate_with_code_response(self):
        """Test validation with code in response"""
        response = """
        Here's a Python function to calculate factorial:

        ```python
        def factorial(n):
            if n <= 1:
                return 1
            return n * factorial(n-1)
        ```

        This uses recursion to calculate n!
        """
        prompt = "Write a factorial function"

        result = self.validator.validate(response, prompt, iteration=1)

        # Code responses should be validated
        assert isinstance(result['confidence'], (int, float))
        assert 'guardrails' in result
        assert 'verification' in result

    def test_validate_confidence_calculation(self):
        """Test that confidence is calculated correctly"""
        response = "Paris is the capital of France."
        prompt = "What is the capital of France?"

        result = self.validator.validate(response, prompt, iteration=1)

        # Check confidence calculation components
        assert 'guardrails' in result
        assert 'verification' in result

        if 'confidence' in result['guardrails']:
            assert isinstance(result['guardrails']['confidence'], (int, float))

        if 'confidence' in result['verification']:
            assert isinstance(result['verification']['confidence'], (int, float))

        # Combined confidence should be weighted average
        assert result['confidence'] >= 0 and result['confidence'] <= 100

    def test_validate_with_special_characters(self):
        """Test validation with special characters and unicode"""
        response = "Special chars: @#$%^&* émojis: 🎉🔥 unicode: αβγδ"
        prompt = "Test special characters"

        # Should not crash on special characters
        result = self.validator.validate(response, prompt, iteration=1)
        assert isinstance(result, dict)
        assert 'confidence' in result

    def test_validate_very_long_response(self):
        """Test validation with very long response"""
        response = "This is a test. " * 1000  # Very long response
        prompt = "Write a long essay"

        result = self.validator.validate(response, prompt, iteration=1)

        # Should handle long responses
        assert isinstance(result, dict)
        assert 'confidence' in result

        # Might have suggestions about length or repetition
        if result['suggestions']:
            assert isinstance(result['suggestions'], list)

    def test_validate_response_with_errors(self):
        """Test validation detects potential errors in response"""
        response = "The capital of France is London"  # Factually incorrect
        prompt = "What is the capital of France?"

        result = self.validator.validate(response, prompt, iteration=1)

        # Should have lower confidence for incorrect information
        assert result['confidence'] < 90  # Shouldn't be highly confident

    def test_is_acceptable_threshold(self):
        """Test is_acceptable flag respects confidence threshold"""
        # Test with high confidence response
        good_response = """
        Python is a high-level programming language known for its
        readability and versatility. It supports multiple programming
        paradigms including object-oriented, functional, and procedural
        programming. Python is widely used in web development, data science,
        machine learning, and automation.
        """

        result = self.validator.validate(good_response, "What is Python?", 1)

        # Check is_acceptable is set based on target_confidence
        if result['confidence'] >= self.validator.target_confidence:
            assert result['is_acceptable'] == True
        else:
            assert result['is_acceptable'] == False

    def test_suggestions_generation(self):
        """Test that suggestions are generated for low-confidence responses"""
        poor_response = "yes"  # Too brief
        prompt = "Explain the theory of relativity"

        result = self.validator.validate(poor_response, prompt, iteration=1)

        # Should have suggestions for improvement
        assert isinstance(result['suggestions'], list)
        assert len(result['suggestions']) > 0

        # Suggestions should be strings
        for suggestion in result['suggestions']:
            assert isinstance(suggestion, str)
            assert len(suggestion) > 0

    @patch('validate_my_response.MultiLayerGuardrailSystem')
    def test_guardrails_integration(self, mock_guardrails_class):
        """Test integration with guardrails system"""
        # Setup mock
        mock_guardrails = Mock()
        mock_guardrails.validate_all.return_value = {
            'passed': True,
            'confidence': 95.0,
            'failures': []
        }
        mock_guardrails_class.return_value = mock_guardrails

        # Create new validator with mocked guardrails
        validator = ResponseValidator()
        result = validator.validate("Test response", "Test prompt", 1)

        # Verify guardrails were called
        mock_guardrails.validate_all.assert_called()

    @patch('validate_my_response.MultiMethodVerifier')
    def test_verifier_integration(self, mock_verifier_class):
        """Test integration with verification system"""
        # Setup mock
        mock_verifier = Mock()
        mock_verifier.verify_all.return_value = {
            'passed': True,
            'confidence': 92.0,
            'methods_passed': 3
        }
        mock_verifier_class.return_value = mock_verifier

        # Create new validator with mocked verifier
        validator = ResponseValidator()
        result = validator.validate("Test response", "Test prompt", 1)

        # Verify verifier was called
        mock_verifier.verify_all.assert_called()

    def test_json_serializable_output(self):
        """Test that output is JSON serializable"""
        response = "This is a test response"
        prompt = "Test prompt"

        result = self.validator.validate(response, prompt, iteration=1)

        # Should be JSON serializable
        json_str = json.dumps(result)
        assert json_str is not None

        # Should be able to parse it back
        parsed = json.loads(json_str)
        assert parsed == result

    def test_edge_case_none_inputs(self):
        """Test handling of None inputs"""
        # Test with None response
        result = self.validator.validate(None, "prompt", 1)
        assert result['confidence'] < 10
        assert result['is_acceptable'] == False

        # Test with None prompt (should still work)
        result = self.validator.validate("response", None, 1)
        assert isinstance(result, dict)

    def test_iteration_limit(self):
        """Test behavior at maximum iteration limit"""
        response = "Test response"
        prompt = "Test prompt"

        # Test at maximum iterations (from config)
        max_iter = 20  # MAX_REFINEMENT_ITERATIONS from config
        result = self.validator.validate(response, prompt, iteration=max_iter)

        assert result['iteration'] == max_iter
        assert isinstance(result['confidence'], (int, float))


def test_main_function():
    """Test the main function with command line arguments"""
    import validate_my_response

    # Test with mock command line arguments
    test_args = ['validate_my_response.py', 'Test response', '--prompt', 'Test prompt', '--iteration', '1']

    with patch('sys.argv', test_args):
        with patch('builtins.print') as mock_print:
            # Should not raise exception
            try:
                validate_my_response.main()
                # Check that something was printed (JSON output)
                mock_print.assert_called()
            except SystemExit as e:
                # OK if it exits with 0
                assert e.code == 0


class TestMainFunctionIntegration:
    """Integration tests for main function"""

    def test_main_with_minimal_args(self):
        """Test main with just response text"""
        import validate_my_response

        with patch('sys.argv', ['validate_my_response.py', 'Test']):
            with patch('builtins.print') as mock_print:
                validate_my_response.main()

                # Should print JSON result
                call_args = mock_print.call_args[0][0]
                result = json.loads(call_args)
                assert 'confidence' in result

    def test_main_with_all_args(self):
        """Test main with all arguments"""
        import validate_my_response

        with patch('sys.argv', ['validate_my_response.py', 'Response text',
                               '--prompt', 'Original prompt',
                               '--iteration', '5']):
            with patch('builtins.print') as mock_print:
                validate_my_response.main()

                call_args = mock_print.call_args[0][0]
                result = json.loads(call_args)
                assert result['iteration'] == 5