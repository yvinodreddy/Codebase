"""
Phase 01: RAG Heat System
Unit tests
"""

import unittest
import sys
import os

# Add code directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'code'))

from implementation import Phase01Implementation


class TestPhase01(unittest.TestCase):
    """Test cases for Phase 01"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.implementation = Phase01Implementation()
    
    def test_initialization(self):
        """Test proper initialization"""
        self.assertEqual(self.implementation.phase_id, 1)
        self.assertEqual(self.implementation.phase_name, "RAG Heat System")
        self.assertIsNotNone(self.implementation.guardrails)
    
    def test_guardrails_integration(self):
        """Test guardrails are properly integrated"""
        self.assertIsNotNone(self.implementation.guardrails)
    
    # TODO: Add more tests here


if __name__ == "__main__":
    unittest.main()
