#!/usr/bin/env python3
"""
Enhanced comprehensive tests for validate_my_response.py
Target: 90% coverage with real code execution
"""

import pytest
import sys
import os
import json
import tempfile
from pathlib import Path
from unittest.mock import patch, Mock, MagicMock, call
from io import StringIO
import contextlib

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import validate_my_response
from validate_my_response import ResponseValidator

class TestValidateMyResponseComprehensive:
    """Achieve 90% coverage for validate_my_response"""

    def setup_method(self):
        """Setup test fixtures"""
        self.validator = ResponseValidator()

    def test_initialization(self):
        """Test ResponseValidator initialization"""
        assert self.validator.target_confidence == 99.0
        assert hasattr(self.validator, 'guardrails')
        assert hasattr(self.validator, 'verifier')

    def test_validate_good_response(self):
        """Test validation with high-quality response"""
        response = "Python is a high-level programming language."
        result = self.validator.validate(response, "What is Python?", 1)

        assert isinstance(result, dict)
        assert 'confidence' in result
        assert 'is_acceptable' in result
        assert isinstance(result['confidence'], (int, float))

    def test_validate_poor_response(self):
        """Test validation with poor response"""
        response = "idk"
        result = self.validator.validate(response, "Explain quantum physics", 1)

        assert result['confidence'] < 50
        assert result['is_acceptable'] == False
        assert len(result['suggestions']) > 0

    def test_validate_empty_response(self):
        """Test validation with empty response"""
        result = self.validator.validate("", "Test prompt", 1)

        assert result['confidence'] < 10
        assert result['is_acceptable'] == False

    def test_validate_with_code(self):
        """Test validation with code in response"""
        response = """
        ```python
        def factorial(n):
            return 1 if n <= 1 else n * factorial(n-1)
        ```
        """
        result = self.validator.validate(response, "Write factorial", 1)
        assert 'confidence' in result

    def test_validate_iterations(self):
        """Test multiple iterations"""
        response = "Test"
        for i in range(1, 5):
            result = self.validator.validate(response, "prompt", i)
            assert result['iteration'] == i

    def test_validate_none_inputs(self):
        """Test with None inputs"""
        result = self.validator.validate(None, "prompt", 1)
        assert result['confidence'] < 10

        result = self.validator.validate("response", None, 1)
        assert isinstance(result, dict)

    def test_json_serializable(self):
        """Test JSON serialization of output"""
        result = self.validator.validate("test", "prompt", 1)
        json_str = json.dumps(result)
        assert json_str is not None

    @patch('sys.argv', ['validate_my_response.py', 'test', '--prompt', 'test'])
    @patch('builtins.print')
    def test_main_function(self, mock_print):
        """Test main function"""
        validate_my_response.main()
        mock_print.assert_called()

    def test_confidence_calculation(self):
        """Test confidence score calculation"""
        # Test various response qualities
        responses = [
            ("The answer is 42", 50, 80),  # Medium quality
            ("I don't know", 0, 30),  # Poor quality
            ("Detailed explanation here...", 70, 100)  # Good quality
        ]

        for response, min_conf, max_conf in responses:
            result = self.validator.validate(response, "Test", 1)
            assert min_conf <= result['confidence'] <= max_conf
