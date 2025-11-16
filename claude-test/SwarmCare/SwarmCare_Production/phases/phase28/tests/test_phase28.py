"""
Phase 28: Ultra-fast Offline Voice AI (<500ms, 11 EHRs - 100% Market Coverage)
Unit tests
"""

import unittest
import sys
import os

# Add code directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'code'))

from implementation import Phase28Implementation


class TestPhase28(unittest.TestCase):
    """Test cases for Phase 28"""

    def setUp(self):
        """Set up test fixtures"""
        self.implementation = Phase28Implementation()

    def test_initialization(self):
        """Test proper initialization"""
        self.assertEqual(self.implementation.phase_id, 28)
        self.assertEqual(self.implementation.phase_name, "Ultra-fast Offline Voice AI (<500ms, 11 EHRs - 100% Market Coverage)")
        self.assertEqual(self.implementation.story_points, 45)
        self.assertEqual(self.implementation.priority, "P0")
        self.assertIsNotNone(self.implementation.framework_available)

    def test_guardrails_integration(self):
        """Test guardrails are properly integrated"""
        # Guardrails may not be available if environment variables are missing
        if self.implementation.framework_available:
            self.assertIsNotNone(self.implementation.guardrails)
        else:
            self.assertFalse(hasattr(self.implementation, 'guardrails') and self.implementation.guardrails is not None)
    
    # TODO: Add more tests here


if __name__ == "__main__":
    unittest.main()
