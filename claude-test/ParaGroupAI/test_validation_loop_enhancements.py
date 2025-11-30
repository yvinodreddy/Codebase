#!/usr/bin/env python3
"""
Test Suite: Validation Loop Enhancements
Date: 2025-11-29
Purpose: Validate exception handling and _refine_results() improvements

Tests:
1. Exception handling - allows up to 5 consecutive failures
2. _refine_results() - intelligent refinement with scoring
3. Zero breaking changes - existing functionality preserved
"""

import sys
import os
import unittest
from unittest.mock import Mock, patch, MagicMock
from typing import List, Dict

# Add database directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'database'))

from dual_context_retriever import DualContextRetriever


class TestExceptionHandling(unittest.TestCase):
    """Test improved exception handling in validation loop"""

    def setUp(self):
        """Set up test fixtures"""
        self.retriever = DualContextRetriever()

    @patch('dual_context_retriever.DualContextRetriever._run_validation_script')
    def test_continues_after_single_exception(self, mock_validation):
        """Test that validation continues after single exception"""
        # Simulate: Exception on iteration 1, success on iteration 2
        mock_validation.side_effect = [
            Exception("Validation timeout"),  # Iteration 1 - fails
            {'confidence': 99.5, 'is_acceptable': True, 'suggestions': []}  # Iteration 2 - succeeds
        ]

        results = [{'message': {'content': 'test'}, 'score': 0.95}]

        # Should NOT break after first exception
        # Should continue to iteration 2 and succeed
        output = self.retriever._validate_results_with_feedback_loop(
            results=results,
            query="test query",
            method_name="keyword"
        )

        # Validation should have been called 2 times
        self.assertEqual(mock_validation.call_count, 2)
        # Should reach 99.5% confidence
        self.assertEqual(output['confidence'], 99.5)
        # Should NOT exit early
        self.assertFalse(output['early_exit'])

    @patch('dual_context_retriever.DualContextRetriever._run_validation_script')
    def test_aborts_after_5_consecutive_failures(self, mock_validation):
        """Test that validation aborts after 5 consecutive exceptions"""
        # Simulate: 5 consecutive exceptions
        mock_validation.side_effect = [
            Exception("Timeout 1"),
            Exception("Timeout 2"),
            Exception("Timeout 3"),
            Exception("Timeout 4"),
            Exception("Timeout 5"),
            # Should not reach here
            {'confidence': 99.5, 'is_acceptable': True, 'suggestions': []}
        ]

        results = [{'message': {'content': 'test'}, 'score': 0.95}]

        # Should break after 5 consecutive exceptions
        output = self.retriever._validate_results_with_feedback_loop(
            results=results,
            query="test query",
            method_name="keyword"
        )

        # Validation should have been called exactly 5 times (then aborted)
        self.assertEqual(mock_validation.call_count, 5)
        # Should return 0 confidence (no successful validation)
        self.assertEqual(output['confidence'], 0)

    @patch('dual_context_retriever.DualContextRetriever._run_validation_script')
    def test_resets_counter_after_successful_validation(self, mock_validation):
        """Test that consecutive failures counter resets after success"""
        # Simulate: Fail, Fail, Success, Fail, Success (reaches 99%)
        mock_validation.side_effect = [
            Exception("Timeout 1"),  # Failure 1
            Exception("Timeout 2"),  # Failure 2
            {'confidence': 85.0, 'is_acceptable': False, 'suggestions': ['More detail']},  # Success - counter resets
            Exception("Timeout 3"),  # Failure 1 (reset)
            {'confidence': 99.5, 'is_acceptable': True, 'suggestions': []}  # Success - target reached
        ]

        results = [{'message': {'content': 'test'}, 'score': 0.95}]

        # Should NOT abort (counter resets after each success)
        output = self.retriever._validate_results_with_feedback_loop(
            results=results,
            query="test query",
            method_name="keyword"
        )

        # Should reach target confidence
        self.assertEqual(output['confidence'], 99.5)
        # Should have 5 iterations (2 exceptions, 1 low confidence, 1 exception, 1 success)
        self.assertEqual(output['iterations'], 5)


class TestRefinementLogic(unittest.TestCase):
    """Test intelligent refinement in _refine_results()"""

    def setUp(self):
        """Set up test fixtures"""
        self.retriever = DualContextRetriever()

    def test_refine_with_no_suggestions(self):
        """Test refinement with empty suggestions returns original results"""
        results = [
            {'message': {'content': 'Result 1'}, 'score': 0.95},
            {'message': {'content': 'Result 2'}, 'score': 0.85}
        ]
        suggestions = []

        refined = self.retriever._refine_results(results, suggestions)

        # Should return original results unchanged
        self.assertEqual(len(refined), 2)
        self.assertEqual(refined, results)

    def test_refine_boosts_detailed_content(self):
        """Test that detailed content gets boosted in scoring"""
        results = [
            {
                'message': {'content': 'Short result'},
                'score': 0.80
            },
            {
                'message': {'content': 'This is a very detailed explanation with comprehensive coverage of the topic including specific examples and concrete implementation details that demonstrate the concept thoroughly.' * 3},
                'score': 0.75  # Lower original score
            }
        ]
        suggestions = ['Add more detail', 'Include comprehensive examples']

        refined = self.retriever._refine_results(results, suggestions)

        # Detailed content should be ranked higher despite lower original score
        self.assertEqual(len(refined), 2)
        # First result should be the detailed one (boosted)
        self.assertIn('comprehensive', refined[0]['message']['content'])
        # Should have refinement metadata
        self.assertIn('refinement_score', refined[0])
        self.assertIn('boost_applied', refined[0])
        self.assertIn('original_score', refined[0])

    def test_refine_filters_low_quality_results(self):
        """Test that low-quality results get filtered out"""
        results = [
            {'message': {'content': 'High quality detailed content with examples and implementation'}, 'score': 0.95},
            {'message': {'content': 'Medium quality content'}, 'score': 0.70},
            {'message': {'content': 'Low'}, 'score': 0.20}  # Should be filtered (below 30% of max)
        ]
        suggestions = ['Add more detail']

        refined = self.retriever._refine_results(results, suggestions)

        # Low quality result should be filtered out
        self.assertLessEqual(len(refined), 2)
        # All remaining results should have reasonable scores
        for result in refined:
            self.assertGreaterEqual(result['refinement_score'], 0.30)

    def test_refine_preserves_original_scores(self):
        """Test that original scores are preserved for transparency"""
        results = [
            {'message': {'content': 'Test content'}, 'score': 0.85}
        ]
        suggestions = ['Add detail']

        refined = self.retriever._refine_results(results, suggestions)

        # Should preserve original score
        self.assertEqual(refined[0]['original_score'], 0.85)
        # Should have refinement score
        self.assertIn('refinement_score', refined[0])
        # Refinement score should be different (boosted)
        self.assertNotEqual(refined[0]['refinement_score'], refined[0]['original_score'])


class TestZeroBreakingChanges(unittest.TestCase):
    """Test that enhancements don't break existing functionality"""

    def setUp(self):
        """Set up test fixtures"""
        self.retriever = DualContextRetriever()

    @patch('dual_context_retriever.DualContextRetriever._run_validation_script')
    def test_validation_loop_still_reaches_target(self, mock_validation):
        """Test that validation loop still reaches 99.9% target"""
        # Simulate normal successful validation
        mock_validation.return_value = {
            'confidence': 99.9,
            'is_acceptable': True,
            'suggestions': []
        }

        results = [{'message': {'content': 'test'}, 'score': 0.95}]

        output = self.retriever._validate_results_with_feedback_loop(
            results=results,
            query="test query",
            method_name="keyword"
        )

        # Should reach target on first iteration
        self.assertEqual(output['confidence'], 99.9)
        self.assertTrue(output['early_exit'])
        self.assertIn("Target", output['exit_reason'])

    @patch('dual_context_retriever.DualContextRetriever._run_validation_script')
    def test_validation_loop_still_iterates_1000_times(self, mock_validation):
        """Test that validation loop still tries 1000 iterations if needed"""
        # Simulate never reaching target
        mock_validation.return_value = {
            'confidence': 94.0,
            'is_acceptable': False,
            'suggestions': ['Improve quality']
        }

        results = [{'message': {'content': 'test'}, 'score': 0.95}]

        output = self.retriever._validate_results_with_feedback_loop(
            results=results,
            query="test query",
            method_name="keyword"
        )

        # Should try all 1000 iterations
        self.assertEqual(output['iterations'], 1000)
        # Should return actual confidence achieved
        self.assertEqual(output['confidence'], 94.0)
        # Should NOT exit early
        self.assertFalse(output['early_exit'])

    def test_refine_backward_compatible(self):
        """Test that _refine_results() is backward compatible"""
        # Old behavior: If no suggestions, return original
        results = [
            {'message': {'content': 'Test'}, 'score': 0.85}
        ]

        # Should work with empty suggestions (backward compatible)
        refined = self.retriever._refine_results(results, [])
        self.assertEqual(refined, results)

        # Should work with None suggestions (defensive)
        refined = self.retriever._refine_results(results, None)
        self.assertEqual(refined, results)

        # Should work with empty results (defensive)
        refined = self.retriever._refine_results([], ['suggestion'])
        self.assertEqual(refined, [])


def run_tests():
    """Run all test suites"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestExceptionHandling))
    suite.addTests(loader.loadTestsFromTestCase(TestRefinementLogic))
    suite.addTests(loader.loadTestsFromTestCase(TestZeroBreakingChanges))

    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Print summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("="*80)

    if result.wasSuccessful():
        print("✅ ALL TESTS PASSED - Enhancements verified, zero breaking changes!")
        return 0
    else:
        print("❌ TESTS FAILED - Review failures above")
        return 1


if __name__ == '__main__':
    sys.exit(run_tests())
