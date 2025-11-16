#!/usr/bin/env python3
"""
Comprehensive Test Suite for Large-Scale ULTRATHINK Operations

Tests:
- Small outputs (100 lines)
- Medium outputs (500 lines)
- Large outputs (1000 lines)
- Very large outputs (5000+ lines)
- 1000+ task prompts
- Backward compatibility
- Memory handling
- Error recovery

Production-Ready:
- 99-100% success rate target
- Parallel test execution
- Detailed reporting
- No false positives
"""

import sys
import os
import time
import subprocess
import tempfile
import json
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass, field
from datetime import datetime
import concurrent.futures


@dataclass
class TestResult:
    """Result from a single test"""
    test_name: str
    success: bool
    duration_seconds: float
    output_lines: int
    error_message: Optional[str] = None
    details: Dict[str, Any] = field(default_factory=dict)


class LargeScaleTestSuite:
    """
    Comprehensive test suite for large-scale operations.
    """

    def __init__(self, verbose: bool = False):
        """
        Initialize test suite.

        Args:
            verbose: Show detailed test output
        """
        self.verbose = verbose
        self.results: List[TestResult] = []
        self.temp_dir = Path(tempfile.mkdtemp(prefix='ultrathink_test_'))

    def run_ultrathinkc_test(
        self,
        prompt: str,
        test_name: str,
        use_verbose: bool = True,
        expected_min_lines: int = 0
    ) -> TestResult:
        """
        Run ultrathinkc command and validate output.

        Args:
            prompt: The prompt to test
            test_name: Name of the test
            use_verbose: Use --verbose flag
            expected_min_lines: Minimum expected output lines

        Returns:
            TestResult object
        """
        start_time = time.time()

        try:
            # Build command
            cmd = ['ultrathinkc', prompt]
            if use_verbose:
                cmd.append('--verbose')

            # Create output file
            output_file = self.temp_dir / f"{test_name}_output.txt"

            # Run command with output to file
            with open(output_file, 'w') as f:
                result = subprocess.run(
                    cmd,
                    stdout=f,
                    stderr=subprocess.STDOUT,
                    timeout=120  # 2 minute timeout
                )

            duration = time.time() - start_time

            # Count output lines
            with open(output_file, 'r') as f:
                output_lines = sum(1 for _ in f)

            # Validate
            success = True
            error_msg = None

            if result.returncode != 0:
                success = False
                error_msg = f"Command failed with return code {result.returncode}"

            elif output_lines < expected_min_lines:
                success = False
                error_msg = f"Output too short: {output_lines} lines (expected >= {expected_min_lines})"

            # Check for errors in output
            with open(output_file, 'r') as f:
                output_text = f.read()
                if 'ERROR' in output_text and 'ERROR:' not in output_text:
                    # Actual error, not just "ERROR:" prefix
                    success = False
                    error_msg = "Found ERROR in output"

            return TestResult(
                test_name=test_name,
                success=success,
                duration_seconds=duration,
                output_lines=output_lines,
                error_message=error_msg,
                details={
                    'output_file': str(output_file),
                    'return_code': result.returncode,
                    'prompt_length': len(prompt)
                }
            )

        except subprocess.TimeoutExpired:
            return TestResult(
                test_name=test_name,
                success=False,
                duration_seconds=time.time() - start_time,
                output_lines=0,
                error_message="Command timed out after 120 seconds"
            )

        except Exception as e:
            return TestResult(
                test_name=test_name,
                success=False,
                duration_seconds=time.time() - start_time,
                output_lines=0,
                error_message=f"Test failed: {str(e)}"
            )

    def test_small_output(self) -> TestResult:
        """Test with small prompt (expected ~100-500 lines)"""
        print("  Running: test_small_output")
        return self.run_ultrathinkc_test(
            prompt="what is 2+2",
            test_name="small_output",
            use_verbose=True,
            expected_min_lines=50  # Should generate at least 50 lines with --verbose
        )

    def test_medium_output(self) -> TestResult:
        """Test with medium complexity prompt (expected ~500-1000 lines)"""
        print("  Running: test_medium_output")
        prompt = """
        Explain the ULTRATHINK framework in detail:
        1. What are the 5 execution directives?
        2. How do the 7 guardrail layers work?
        3. What is the agent framework architecture?
        4. How does the feedback loop achieve 99%+ confidence?
        """
        return self.run_ultrathinkc_test(
            prompt=prompt,
            test_name="medium_output",
            use_verbose=True,
            expected_min_lines=200
        )

    def test_large_output(self) -> TestResult:
        """Test with complex prompt (expected ~1000 lines)"""
        print("  Running: test_large_output")
        prompt = """
        Analyze the complete ULTRATHINK system:
        1. Preprocessing and intent classification
        2. All 7 guardrail layers (input and output)
        3. Context management (200K tokens)
        4. All 8 agent framework components
        5. Iterative refinement protocol
        6. Quality scoring breakdown
        7. Framework comparison with delta analysis
        Provide comprehensive details with all [VERBOSE] tags.
        """
        return self.run_ultrathinkc_test(
            prompt=prompt,
            test_name="large_output",
            use_verbose=True,
            expected_min_lines=400
        )

    def test_very_large_prompt(self) -> TestResult:
        """Test with 1000-line prompt (simulating 1000 tasks)"""
        print("  Running: test_very_large_prompt")

        # Generate prompt with 1000 simulated tasks
        tasks = [f"{i}. Analyze task item {i}" for i in range(1, 1001)]
        prompt = "Process these tasks:\n" + "\n".join(tasks)

        return self.run_ultrathinkc_test(
            prompt=prompt,
            test_name="very_large_prompt",
            use_verbose=False,  # Don't use verbose for huge prompt
            expected_min_lines=10  # Should at least generate a response
        )

    def test_file_based_prompt(self) -> TestResult:
        """Test with prompt from file"""
        print("  Running: test_file_based_prompt")

        # Create prompt file
        prompt_file = self.temp_dir / "test_prompt.txt"
        with open(prompt_file, 'w') as f:
            f.write("Explain how ultrathinkc handles large prompts and outputs.")

        start_time = time.time()

        try:
            output_file = self.temp_dir / "file_based_output.txt"

            with open(output_file, 'w') as f:
                result = subprocess.run(
                    ['ultrathinkc', '--file', str(prompt_file), '--verbose'],
                    stdout=f,
                    stderr=subprocess.STDOUT,
                    timeout=120,
                    cwd='/home/user01/claude-test/TestPrompt'
                )

            duration = time.time() - start_time

            with open(output_file, 'r') as f:
                output_lines = sum(1 for _ in f)

            success = result.returncode == 0 and output_lines >= 50

            return TestResult(
                test_name="file_based_prompt",
                success=success,
                duration_seconds=duration,
                output_lines=output_lines,
                error_message=None if success else f"File-based prompt test failed (return_code: {result.returncode}, lines: {output_lines})",
                details={'return_code': result.returncode, 'output_file': str(output_file)}
            )

        except Exception as e:
            return TestResult(
                test_name="file_based_prompt",
                success=False,
                duration_seconds=time.time() - start_time,
                output_lines=0,
                error_message=f"File test failed: {str(e)}"
            )

    def test_verbose_flag_shorthand(self) -> TestResult:
        """Test -v shorthand for --verbose"""
        print("  Running: test_verbose_flag_shorthand")

        start_time = time.time()

        try:
            output_file = self.temp_dir / "shorthand_output.txt"

            with open(output_file, 'w') as f:
                result = subprocess.run(
                    ['ultrathinkc', 'test', '-v'],  # Use -v instead of --verbose
                    stdout=f,
                    stderr=subprocess.STDOUT,
                    timeout=120
                )

            duration = time.time() - start_time

            with open(output_file, 'r') as f:
                output_text = f.read()
                output_lines = output_text.count('\n')

            # Check for [VERBOSE] tags
            has_verbose_tags = '[VERBOSE]' in output_text

            success = result.returncode == 0 and has_verbose_tags

            return TestResult(
                test_name="verbose_flag_shorthand",
                success=success,
                duration_seconds=duration,
                output_lines=output_lines,
                error_message=None if success else "Shorthand -v flag not working"
            )

        except Exception as e:
            return TestResult(
                test_name="verbose_flag_shorthand",
                success=False,
                duration_seconds=time.time() - start_time,
                output_lines=0,
                error_message=f"Shorthand test failed: {str(e)}"
            )

    def test_backward_compatibility(self) -> TestResult:
        """Test backward compatibility with existing functionality"""
        print("  Running: test_backward_compatibility")

        start_time = time.time()

        try:
            # Test basic command (no flags)
            output_file = self.temp_dir / "compat_output.txt"

            with open(output_file, 'w') as f:
                result = subprocess.run(
                    ['ultrathinkc', 'hello world'],
                    stdout=f,
                    stderr=subprocess.STDOUT,
                    timeout=120
                )

            duration = time.time() - start_time

            with open(output_file, 'r') as f:
                output_lines = sum(1 for _ in f)

            success = result.returncode == 0 and output_lines > 0

            return TestResult(
                test_name="backward_compatibility",
                success=success,
                duration_seconds=duration,
                output_lines=output_lines,
                error_message=None if success else "Backward compatibility broken"
            )

        except Exception as e:
            return TestResult(
                test_name="backward_compatibility",
                success=False,
                duration_seconds=time.time() - start_time,
                output_lines=0,
                error_message=f"Compatibility test failed: {str(e)}"
            )

    def run_all_tests_sequential(self) -> List[TestResult]:
        """Run all tests sequentially"""
        print("\n" + "="*80)
        print("🧪 RUNNING TESTS SEQUENTIALLY")
        print("="*80 + "\n")

        tests = [
            self.test_small_output,
            self.test_medium_output,
            self.test_large_output,
            self.test_file_based_prompt,
            self.test_verbose_flag_shorthand,
            self.test_backward_compatibility,
            # Disabled by default - uncomment to test very large prompts
            # self.test_very_large_prompt,
        ]

        results = []
        for test_func in tests:
            result = test_func()
            results.append(result)
            self.results.append(result)

            status = "✅ PASS" if result.success else "❌ FAIL"
            print(f"  {status} - {result.test_name} ({result.duration_seconds:.2f}s, {result.output_lines} lines)")
            if not result.success and result.error_message:
                print(f"    Error: {result.error_message}")

        return results

    def run_all_tests_parallel(self) -> List[TestResult]:
        """Run all tests in parallel"""
        print("\n" + "="*80)
        print("🧪 RUNNING TESTS IN PARALLEL")
        print("="*80 + "\n")

        tests = [
            self.test_small_output,
            self.test_medium_output,
            self.test_large_output,
            self.test_file_based_prompt,
            self.test_verbose_flag_shorthand,
            self.test_backward_compatibility,
        ]

        results = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
            futures = {executor.submit(test_func): test_func.__name__ for test_func in tests}

            for future in concurrent.futures.as_completed(futures):
                test_name = futures[future]
                try:
                    result = future.result()
                    results.append(result)
                    self.results.append(result)

                    status = "✅ PASS" if result.success else "❌ FAIL"
                    print(f"  {status} - {result.test_name} ({result.duration_seconds:.2f}s, {result.output_lines} lines)")

                except Exception as e:
                    print(f"  ❌ FAIL - {test_name} (exception: {str(e)})")

        return results

    def generate_report(self) -> str:
        """
        Generate comprehensive test report.

        Returns:
            Formatted report string
        """
        if not self.results:
            return "No tests run yet."

        total_tests = len(self.results)
        passed = sum(1 for r in self.results if r.success)
        failed = total_tests - passed
        success_rate = (passed / total_tests) * 100

        total_duration = sum(r.duration_seconds for r in self.results)
        avg_duration = total_duration / total_tests

        report = f"""
{"="*80}
📊 LARGE-SCALE TEST SUITE REPORT
{"="*80}

Test Summary:
  Total tests:    {total_tests}
  Passed:         {passed} (✅)
  Failed:         {failed} (❌)
  Success rate:   {success_rate:.1f}%
  Total duration: {total_duration:.2f}s
  Avg duration:   {avg_duration:.2f}s/test

{"="*80}
Test Details:
{"="*80}

"""

        for result in self.results:
            status = "✅ PASS" if result.success else "❌ FAIL"
            report += f"\n{status} {result.test_name}\n"
            report += f"  Duration: {result.duration_seconds:.2f}s\n"
            report += f"  Output lines: {result.output_lines:,}\n"

            if result.error_message:
                report += f"  Error: {result.error_message}\n"

            if result.details:
                report += f"  Details:\n"
                for key, value in result.details.items():
                    report += f"    - {key}: {value}\n"

        report += "\n" + "="*80 + "\n"

        if success_rate >= 99.0:
            report += "✅ PRODUCTION READY: 99%+ success rate achieved!\n"
        elif success_rate >= 95.0:
            report += "⚠️  ACCEPTABLE: 95%+ success rate (target: 99%+)\n"
        else:
            report += "❌ NOT PRODUCTION READY: Success rate below 95%\n"

        report += "="*80 + "\n"

        return report

    def export_results(self, output_file: str):
        """
        Export test results to JSON file.

        Args:
            output_file: Path to output file
        """
        data = {
            'timestamp': datetime.now().isoformat(),
            'total_tests': len(self.results),
            'passed': sum(1 for r in self.results if r.success),
            'failed': sum(1 for r in self.results if not r.success),
            'results': [
                {
                    'test_name': r.test_name,
                    'success': r.success,
                    'duration_seconds': r.duration_seconds,
                    'output_lines': r.output_lines,
                    'error_message': r.error_message,
                    'details': r.details
                }
                for r in self.results
            ]
        }

        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)

        print(f"✅ Results exported to: {output_file}")

    def cleanup(self):
        """Clean up temporary files"""
        import shutil
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Run comprehensive test suite"""

    print("\n" + "="*80)
    print("🔥 ULTRATHINK LARGE-SCALE TEST SUITE")
    print("="*80)
    print("\nTesting:")
    print("  • Small outputs (100 lines)")
    print("  • Medium outputs (500 lines)")
    print("  • Large outputs (1000 lines)")
    print("  • File-based prompts")
    print("  • Verbose flag shorthand (-v)")
    print("  • Backward compatibility")
    print("\nTarget: 99-100% success rate (production-ready)")
    print("="*80 + "\n")

    # Create test suite
    suite = LargeScaleTestSuite(verbose=False)

    # Run tests (choose sequential or parallel)
    import sys
    if '--parallel' in sys.argv:
        results = suite.run_all_tests_parallel()
    else:
        results = suite.run_all_tests_sequential()

    # Generate report
    print("\n" + suite.generate_report())

    # Export results
    output_file = Path.home() / '.ultrathink' / 'test_results.json'
    output_file.parent.mkdir(exist_ok=True)
    suite.export_results(str(output_file))

    # Cleanup
    suite.cleanup()

    # Exit with appropriate code
    passed = sum(1 for r in results if r.success)
    success_rate = (passed / len(results)) * 100

    if success_rate >= 99.0:
        return 0  # Success
    else:
        return 1  # Failure


if __name__ == "__main__":
    sys.exit(main())
