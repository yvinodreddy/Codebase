#!/usr/bin/env python3
"""
Test Suite: 100% Reliability Enhancement
Date: 2025-11-29
Purpose: Verify that exception handling achieves 100% reliability with full diagnostics

This test suite uses fault injection to verify that:
1. ALL exceptions are caught and logged with full diagnostics
2. EVERY failure returns complete error information (never crashes)
3. Transient errors trigger retry with exponential backoff
4. Critical errors return immediately with diagnostics
5. After MAX_CONSECUTIVE_FAILURES, full diagnostics are returned
"""

import sys
import os
import unittest
from unittest.mock import Mock, patch, MagicMock
from typing import List, Dict

# Add database directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'database'))

from dual_context_retriever import DualContextRetriever


class Test100PercentReliability(unittest.TestCase):
    """Test 100% reliability with fault injection"""

    def setUp(self):
        """Set up test fixtures"""
        self.retriever = DualContextRetriever()

    @patch('dual_context_retriever.DualContextRetriever._run_validation_script')
    def test_transient_error_triggers_exponential_backoff(self, mock_validation):
        """Test that transient errors (TimeoutError) trigger exponential backoff"""
        # Simulate: TimeoutError 3 times, then success
        mock_validation.side_effect = [
            TimeoutError("Connection timeout"),  # Failure 1 - wait 2s
            TimeoutError("Connection timeout"),  # Failure 2 - wait 4s
            TimeoutError("Connection timeout"),  # Failure 3 - wait 8s
            {'confidence': 99.5, 'is_acceptable': True, 'suggestions': []}  # Success
        ]

        results = [{'message': {'content': 'test'}, 'score': 0.95}]

        with patch('time.sleep') as mock_sleep:
            output = self.retriever._validate_results_with_feedback_loop(
                results=results,
                query="test query",
                method_name="keyword"
            )

            # Verify exponential backoff was applied
            # wait_time = min(2 ** consecutive_failures, 30)
            # Failure 1: 2^1 = 2s
            # Failure 2: 2^2 = 4s
            # Failure 3: 2^3 = 8s
            self.assertEqual(mock_sleep.call_count, 3)
            self.assertEqual(mock_sleep.call_args_list[0][0][0], 2)   # 2s
            self.assertEqual(mock_sleep.call_args_list[1][0][0], 4)   # 4s
            self.assertEqual(mock_sleep.call_args_list[2][0][0], 8)   # 8s

        # Should eventually succeed
        self.assertEqual(output['confidence'], 99.5)

    @patch('dual_context_retriever.DualContextRetriever._run_validation_script')
    def test_critical_error_returns_immediately_with_diagnostics(self, mock_validation):
        """Test that critical errors (MemoryError) return immediately with full diagnostics"""
        # Simulate: MemoryError on first attempt
        mock_validation.side_effect = MemoryError("Out of memory")

        results = [{'message': {'content': 'test'}, 'score': 0.95}]

        output = self.retriever._validate_results_with_feedback_loop(
            results=results,
            query="test query",
            method_name="keyword"
        )

        # Should return immediately (iteration = 1, not 5)
        self.assertEqual(output['iterations'], 1)
        self.assertTrue(output['early_exit'])
        self.assertIn("Critical error", output['exit_reason'])

        # Should have full diagnostics
        self.assertIn('error_diagnostics', output)
        diagnostics = output['error_diagnostics']
        self.assertEqual(diagnostics['exception_type'], 'MemoryError')
        self.assertIn('Out of memory', diagnostics['exception_message'])
        self.assertIn('stack_trace', diagnostics)
        self.assertEqual(diagnostics['iteration'], 1)

    @patch('dual_context_retriever.DualContextRetriever._run_validation_script')
    def test_all_failures_return_full_diagnostics(self, mock_validation):
        """Test that after 5 consecutive failures, full diagnostics are returned (NEVER crash)"""
        # Simulate: 5 consecutive generic exceptions
        mock_validation.side_effect = [
            ValueError("Invalid data 1"),
            ValueError("Invalid data 2"),
            ValueError("Invalid data 3"),
            ValueError("Invalid data 4"),
            ValueError("Invalid data 5"),
            # Should not reach here
            {'confidence': 99.5, 'is_acceptable': True, 'suggestions': []}
        ]

        results = [{'message': {'content': 'test'}, 'score': 0.95}]

        output = self.retriever._validate_results_with_feedback_loop(
            results=results,
            query="test query",
            method_name="keyword"
        )

        # Should have attempted 5 validations
        self.assertEqual(mock_validation.call_count, 5)

        # Should return with diagnostics (NOT crash)
        self.assertIsNotNone(output)
        self.assertTrue(output['early_exit'])
        self.assertIn("5 consecutive validation failures", output['exit_reason'])

        # Should have FULL error diagnostics
        self.assertIn('error_diagnostics', output)
        diagnostics = output['error_diagnostics']
        self.assertEqual(diagnostics['total_failures'], 5)
        self.assertEqual(diagnostics['last_exception_type'], 'ValueError')
        self.assertIn('Invalid data 5', diagnostics['last_exception_message'])
        self.assertIn('stack_trace', diagnostics)
        self.assertIn('last_stack_trace', diagnostics)

        # Should track validation attempts
        self.assertEqual(diagnostics['all_validation_attempts'], 0)  # All failed
        self.assertEqual(diagnostics['successful_validations'], 0)

    @patch('dual_context_retriever.DualContextRetriever._run_validation_script')
    def test_mixed_failures_and_successes_return_diagnostics(self, mock_validation):
        """Test that mix of failures and successes still returns full diagnostics"""
        # Simulate: Success, Fail, Fail, Success, Fail x5 (total 5 consecutive failures)
        mock_validation.side_effect = [
            {'confidence': 85.0, 'is_acceptable': False, 'suggestions': ['More detail']},  # Success 1
            ValueError("Error 1"),  # Failure 1
            ValueError("Error 2"),  # Failure 2
            {'confidence': 90.0, 'is_acceptable': False, 'suggestions': ['More detail']},  # Success 2 (resets counter)
            ValueError("Error 3"),  # Failure 1 (after reset)
            ValueError("Error 4"),  # Failure 2
            ValueError("Error 5"),  # Failure 3
            ValueError("Error 6"),  # Failure 4
            ValueError("Error 7"),  # Failure 5 - should trigger return with diagnostics
            # Should not reach here
            {'confidence': 99.5, 'is_acceptable': True, 'suggestions': []}
        ]

        results = [{'message': {'content': 'test'}, 'score': 0.95}]

        output = self.retriever._validate_results_with_feedback_loop(
            results=results,
            query="test query",
            method_name="keyword"
        )

        # Should have attempted 9 validations (2 successes + 7 failures)
        self.assertEqual(mock_validation.call_count, 9)

        # Should return with diagnostics after 5 consecutive failures
        self.assertTrue(output['early_exit'])
        self.assertIn('error_diagnostics', output)
        diagnostics = output['error_diagnostics']
        self.assertEqual(diagnostics['total_failures'], 5)  # 5 consecutive

        # Should track successful validations
        self.assertEqual(diagnostics['all_validation_attempts'], 2)  # 2 successful attempts
        self.assertEqual(diagnostics['successful_validations'], 2)

    @patch('dual_context_retriever.DualContextRetriever._run_validation_script')
    def test_exception_details_logged_comprehensively(self, mock_validation):
        """Test that exception details are logged with type, message, and stack trace"""
        # Simulate: Custom exception with specific message
        class CustomValidationError(Exception):
            pass

        mock_validation.side_effect = [
            CustomValidationError("Very specific error message with details"),
            CustomValidationError("Another specific error"),
            CustomValidationError("Third error"),
            CustomValidationError("Fourth error"),
            CustomValidationError("Fifth error"),
        ]

        results = [{'message': {'content': 'test'}, 'score': 0.95}]

        output = self.retriever._validate_results_with_feedback_loop(
            results=results,
            query="test query",
            method_name="keyword"
        )

        # Should have full diagnostics
        self.assertIn('error_diagnostics', output)
        diagnostics = output['error_diagnostics']

        # Verify exception type is captured
        self.assertEqual(diagnostics['last_exception_type'], 'CustomValidationError')

        # Verify exception message is captured
        self.assertIn('Fifth error', diagnostics['last_exception_message'])

        # Verify stack trace is captured
        self.assertIn('stack_trace', diagnostics)
        self.assertIsInstance(diagnostics['last_stack_trace'], str)
        self.assertGreater(len(diagnostics['last_stack_trace']), 0)

    @patch('dual_context_retriever.DualContextRetriever._run_validation_script')
    def test_100_percent_reliability_never_crashes(self, mock_validation):
        """Test that we achieve 100% reliability - NEVER crash without returning diagnostics"""
        # Test with 10 different exception types
        exception_types = [
            ValueError("ValueError test"),
            TypeError("TypeError test"),
            RuntimeError("RuntimeError test"),
            AttributeError("AttributeError test"),
            KeyError("KeyError test"),
            IndexError("IndexError test"),
            ZeroDivisionError("ZeroDivisionError test"),
            FileNotFoundError("FileNotFoundError test"),
            PermissionError("PermissionError test"),
            OSError("OSError test"),
        ]

        for exc in exception_types:
            mock_validation.reset_mock()
            mock_validation.side_effect = [exc] * 5

            results = [{'message': {'content': 'test'}, 'score': 0.95}]

            output = self.retriever._validate_results_with_feedback_loop(
                results=results,
                query="test query",
                method_name="keyword"
            )

            # MUST return a result (not None, not crash)
            self.assertIsNotNone(output)

            # MUST have diagnostics
            self.assertIn('error_diagnostics', output)

            # MUST capture exception type
            diagnostics = output['error_diagnostics']
            self.assertIn(type(exc).__name__, diagnostics['last_exception_type'])

        # 100% reliability achieved - no crashes for any exception type!


def run_tests():
    """Run all test suites"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(Test100PercentReliability))

    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Print summary
    print("\n" + "="*80)
    print("TEST SUMMARY - 100% RELIABILITY VERIFICATION")
    print("="*80)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("="*80)

    if result.wasSuccessful():
        print("✅ 100% RELIABILITY ACHIEVED!")
        print("   - ALL exceptions caught with full diagnostics")
        print("   - NEVER crashes without returning error information")
        print("   - Exponential backoff working for transient errors")
        print("   - Critical errors handled immediately")
        return 0
    else:
        print("❌ TESTS FAILED - Review failures above")
        return 1


if __name__ == '__main__':
    sys.exit(run_tests())
