"""
Test suite for guardrails modules
Auto-generated to improve test coverage
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))


class TestGuardrailsSystem(unittest.TestCase):
    """Test guardrails system"""

    def test_import_guardrails(self):
        """Test that guardrail modules can be imported"""
        try:
            from guardrails.multi_layer_system import MultiLayerGuardrailSystem
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Failed to import guardrails: {e}")

    def test_guardrail_initialization(self):
        """Test guardrail system initializes"""
        from guardrails.multi_layer_system import MultiLayerGuardrailSystem

        system = MultiLayerGuardrailSystem()
        self.assertIsNotNone(system)

    def test_input_validation(self):
        """Test basic input validation"""
        from guardrails.multi_layer_system import MultiLayerGuardrailSystem

        system = MultiLayerGuardrailSystem()

        # Test normal input
        result = system.validate_input("Write a hello world program")
        self.assertTrue(result.is_valid)


if __name__ == '__main__':
    unittest.main()
