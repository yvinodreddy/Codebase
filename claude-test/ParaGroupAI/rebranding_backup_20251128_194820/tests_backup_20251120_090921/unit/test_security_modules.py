"""
Test suite for security modules
Auto-generated to improve test coverage
"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from security.input_sanitizer import sanitize_prompt, SecurityError
from security.error_sanitizer import sanitize_error_message


class TestInputSanitizer(unittest.TestCase):
    """Test input sanitizer security module"""

    def test_sanitize_normal_prompt(self):
        """Test that normal prompts pass through"""
        prompt = "Create a function to add two numbers"
        result = sanitize_prompt(prompt)
        self.assertEqual(result, prompt)

    def test_detect_injection_attempt(self):
        """Test that injection attempts are detected"""
        malicious = "'; DROP TABLE users; --"
        # Should either sanitize or raise SecurityError
        try:
            result = sanitize_prompt(malicious)
            # If it returns, check it's been sanitized
            self.assertNotIn("DROP TABLE", result)
        except SecurityError:
            # This is also acceptable
            pass

    def test_detect_xss_attempt(self):
        """Test XSS detection"""
        xss = "<script>alert('xss')</script>"
        try:
            result = sanitize_prompt(xss)
            self.assertNotIn("<script>", result)
        except SecurityError:
            pass


class TestErrorSanitizer(unittest.TestCase):
    """Test error message sanitizer"""

    def test_sanitize_stack_trace(self):
        """Test that stack traces are sanitized"""
        error = "Error at /home/user/secret/file.py line 42"
        result = sanitize_error_message(error)
        # Should remove file paths
        self.assertNotIn("/home/user/secret", result)

    def test_sanitize_api_keys(self):
        """Test API key removal"""
        error = "Auth failed with key: sk-abc123xyz456"
        result = sanitize_error_message(error)
        self.assertNotIn("sk-abc123xyz456", result)


if __name__ == '__main__':
    unittest.main()
