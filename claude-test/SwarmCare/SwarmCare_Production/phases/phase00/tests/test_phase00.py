"""
Phase 00: Foundation & Infrastructure
Unit tests
"""

import unittest
import sys
import os

# Add code directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'code'))

from implementation import Phase00Implementation


class TestPhase00(unittest.TestCase):
    """Test cases for Phase 00"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.implementation = Phase00Implementation()
    
    def test_initialization(self):
        """Test proper initialization"""
        self.assertEqual(self.implementation.phase_id, 0)
        self.assertEqual(self.implementation.phase_name, "Foundation & Infrastructure")
        self.assertEqual(self.implementation.story_points, 37)
        self.assertEqual(self.implementation.priority, "P0")

    def test_framework_integration(self):
        """Test agent framework components are initialized"""
        # Guardrails may be None if env vars missing (acceptable in dev)
        # Other framework components should be present
        self.assertIsNotNone(self.implementation.feedback_loop)
        self.assertIsNotNone(self.implementation.context)
        self.assertIsNotNone(self.implementation.orchestrator)

    def test_phase_execution(self):
        """Test phase can execute without errors"""
        task = {"goal": "Test execution", "phase_id": 0}
        result = self.implementation.execute(task)
        self.assertIsNotNone(result)
        self.assertTrue(hasattr(result, 'success'))

    def test_get_stats(self):
        """Test statistics retrieval"""
        stats = self.implementation.get_stats()
        self.assertEqual(stats['phase_id'], 0)
        self.assertEqual(stats['story_points'], 37)
        self.assertIn('status', stats)
    
    # TODO: Add more tests here


if __name__ == "__main__":
    unittest.main()
