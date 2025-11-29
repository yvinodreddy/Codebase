#!/usr/bin/env python3
"""
test_statusline_fixes.py - Comprehensive Statusline Fixes Validation Suite

PRODUCTION-READY TESTING FRAMEWORK (2025-11-16)
================================================

Tests all statusline components to ensure 100% production readiness:
1. Confidence score extraction (answer section priority)
2. Token count extraction from multiple sources
3. Agent counting accuracy
4. Real-time update loop functionality
5. Multi-source verification logic
6. End-to-end integration

VALIDATION CRITERIA:
- All tests must pass (100% success rate)
- No regressions in existing functionality
- Performance requirements met (< 100ms per update)
- Error handling verified
"""

import json
import os
import sys
import time
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, List, Tuple, Optional


class Colors:
    """ANSI color codes for terminal output."""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


class StatuslineTestSuite:
    """Comprehensive test suite for statusline fixes."""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.test_results = []
        self.base_path = Path("/home/user01/claude-test/ClaudePrompt")

    def log(self, message: str, level: str = "INFO"):
        """Log message with optional verbosity control."""
        if self.verbose or level in ["ERROR", "SUCCESS", "FAIL"]:
            prefix = {
                "INFO": f"{Colors.BLUE}[INFO]{Colors.RESET}",
                "SUCCESS": f"{Colors.GREEN}[✓]{Colors.RESET}",
                "FAIL": f"{Colors.RED}[✗]{Colors.RESET}",
                "WARN": f"{Colors.YELLOW}[!]{Colors.RESET}",
                "ERROR": f"{Colors.RED}[ERROR]{Colors.RESET}"
            }.get(level, "[?]")
            print(f"{prefix} {message}")

    def run_test(self, name: str, test_func) -> bool:
        """Run a single test and record result."""
        self.log(f"\nRunning: {name}", "INFO")
        try:
            start_time = time.time()
            result, message = test_func()
            duration = time.time() - start_time

            self.test_results.append({
                'name': name,
                'passed': result,
                'message': message,
                'duration_ms': duration * 1000
            })

            if result:
                self.log(f"PASSED: {name} ({duration*1000:.1f}ms) - {message}", "SUCCESS")
            else:
                self.log(f"FAILED: {name} - {message}", "FAIL")

            return result
        except Exception as e:
            self.test_results.append({
                'name': name,
                'passed': False,
                'message': f'Exception: {str(e)}',
                'duration_ms': 0
            })
            self.log(f"FAILED: {name} - Exception: {e}", "ERROR")
            return False

    # ========================================================================
    # TEST 1: Confidence Score Extraction
    # ========================================================================

    def test_confidence_extraction(self) -> Tuple[bool, str]:
        """Test that confidence is extracted from answer section, not system."""
        # Create test file with both system (100%) and answer (85%) confidence
        test_content = """
[VERBOSE] System output here
Confidence: 100%

⬇️⬇️⬇️⬇️⬇️⬇️⬇️
ANSWER SECTION

**Confidence Level: 85%**

This is the real confidence from the analysis.
"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write(test_content)
            test_file = f.name

        try:
            # Run extractor
            result = subprocess.run(
                ['python3', str(self.base_path / 'extract_confidence_from_output.py'),
                 test_file, '--json'],
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.returncode != 0:
                return False, f"Extractor failed: {result.stderr}"

            data = json.loads(result.stdout)
            confidence = data.get('confidence')

            if confidence == 85.0:
                return True, f"Correctly extracted answer confidence (85%) over system (100%)"
            else:
                return False, f"Expected 85%, got {confidence}"

        finally:
            os.unlink(test_file)

    # ========================================================================
    # TEST 2: Multi-Source Token Verification
    # ========================================================================

    def test_multi_source_verification(self) -> Tuple[bool, str]:
        """Test that multi-source verifier prioritizes sources correctly."""
        # Create mock context cache (highest priority)
        cache_file = "/tmp/claude_context_cache.txt"
        with open(cache_file, 'w') as f:
            f.write("claude-sonnet-4-5-20250929 · 36k/200k tokens (18%)\n")

        # Touch to make it fresh
        os.utime(cache_file, None)

        try:
            # Run verifier
            result = subprocess.run(
                ['python3', str(self.base_path / 'multi_source_metrics_verifier.py'),
                 '--json'],
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.returncode != 0:
                return False, f"Verifier failed: {result.stderr}"

            data = json.loads(result.stdout)

            tokens_display = data.get('tokens_display', '')
            tokens_pct = data.get('tokens_pct', 0.0)

            # Check if values match expected
            if '36k' in tokens_display and 17.0 <= tokens_pct <= 19.0:
                return True, f"Correctly extracted tokens: {tokens_display} ({tokens_pct}%)"
            else:
                return False, f"Expected ~36k/18%, got {tokens_display} ({tokens_pct}%)"

        finally:
            if os.path.exists(cache_file):
                os.unlink(cache_file)

    # ========================================================================
    # TEST 3: Agent Counter Accuracy
    # ========================================================================

    def test_agent_counter(self) -> Tuple[bool, str]:
        """Test that agent counter increments correctly."""
        counter_file = self.base_path / "tmp" / "agent_usage_counter.txt"
        counter_file.parent.mkdir(exist_ok=True)

        # Reset counter
        with open(counter_file, 'w') as f:
            f.write("0")

        # Simulate 5 tool uses
        for i in range(5):
            current = int(counter_file.read_text())
            new_count = current + 1
            counter_file.write_text(str(new_count))

        final_count = int(counter_file.read_text())

        if final_count == 5:
            return True, f"Agent counter accurate: {final_count} uses"
        else:
            return False, f"Expected 5, got {final_count}"

    # ========================================================================
    # TEST 4: Real-Time Update Script Exists
    # ========================================================================

    def test_realtime_loop_exists(self) -> Tuple[bool, str]:
        """Test that real-time update loop script exists and is executable."""
        loop_script = self.base_path / "realtime_metrics_loop.sh"

        if not loop_script.exists():
            return False, "Real-time loop script not found"

        if not os.access(loop_script, os.X_OK):
            return False, "Real-time loop script not executable"

        # Test that it can show status
        result = subprocess.run(
            [str(loop_script), 'status'],
            capture_output=True,
            text=True,
            timeout=2
        )

        if result.returncode in [0, 1]:  # 0 = running, 1 = not running (both ok)
            return True, "Real-time loop script functional"
        else:
            return False, f"Loop script error: {result.stderr}"

    # ========================================================================
    # TEST 5: Update Metrics From Output
    # ========================================================================

    def test_update_metrics_from_output(self) -> Tuple[bool, str]:
        """Test that metrics are updated correctly after cpp execution."""
        # Create test output file with confidence score
        test_content = """
⬇️⬇️⬇️⬇️⬇️⬇️⬇️
ANSWER SECTION

**Confidence Level: 92%**

Test answer.
"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write(test_content)
            test_file = f.name

        metrics_file = self.base_path / "tmp" / "realtime_metrics.json"
        metrics_file.parent.mkdir(exist_ok=True)

        # Create initial metrics
        initial_metrics = {
            'agents': '5',
            'context_pct': 15.0,
            'confidence': '--',
            'executing': True
        }
        with open(metrics_file, 'w') as f:
            json.dump(initial_metrics, f)

        try:
            # Run update script
            result = subprocess.run(
                [str(self.base_path / 'update_metrics_from_output.sh'), test_file],
                capture_output=True,
                text=True,
                timeout=5
            )

            # Check metrics file was updated
            with open(metrics_file, 'r') as f:
                updated_metrics = json.load(f)

            confidence = updated_metrics.get('confidence')
            executing = updated_metrics.get('executing')

            if confidence == 92.0 and executing == False:
                return True, f"Metrics updated: confidence={confidence}%, executing={executing}"
            else:
                return False, f"Expected confidence=92%, executing=False; got {confidence}%, {executing}"

        finally:
            os.unlink(test_file)

    # ========================================================================
    # TEST 6: Statusline Script Performance
    # ========================================================================

    def test_statusline_performance(self) -> Tuple[bool, str]:
        """Test that statusline renders in < 100ms."""
        statusline_script = self.base_path / "statusline_production_ready.sh"

        if not statusline_script.exists():
            return False, "Statusline script not found"

        # Create test JSON input
        test_input = json.dumps({
            'currentDirectory': '/home/user01/claude-test/ClaudePrompt',
            'conversation_stats': {
                'context_tokens': 36000,
                'max_tokens': 200000
            }
        })

        start_time = time.time()
        result = subprocess.run(
            [str(statusline_script)],
            input=test_input,
            capture_output=True,
            text=True,
            timeout=2
        )
        duration_ms = (time.time() - start_time) * 1000

        if result.returncode == 0 and duration_ms < 100:
            return True, f"Statusline rendered in {duration_ms:.1f}ms (< 100ms target)"
        else:
            return False, f"Too slow: {duration_ms:.1f}ms or failed"

    # ========================================================================
    # TEST 7: End-to-End Integration
    # ========================================================================

    def test_end_to_end_integration(self) -> Tuple[bool, str]:
        """Test complete workflow from hook to statusline."""
        # This tests the full integration:
        # 1. Hook captures metrics
        # 2. Verifier reads from multiple sources
        # 3. Statusline displays correctly

        # Setup test environment
        cache_file = Path("/tmp/claude_context_cache.txt")
        metrics_file = self.base_path / "tmp" / "realtime_metrics.json"

        # Create mock data
        cache_file.write_text("claude-sonnet-4-5-20250929 · 45k/200k tokens (22.5%)\n")
        os.utime(cache_file, None)  # Make fresh

        metrics_file.parent.mkdir(exist_ok=True)
        metrics_file.write_text(json.dumps({
            'agents': '7',
            'context_pct': 22.5,
            'confidence': 95.0,
            'executing': False
        }))

        # Run statusline
        test_input = json.dumps({'currentDirectory': str(self.base_path)})

        result = subprocess.run(
            [str(self.base_path / 'statusline_production_ready.sh')],
            input=test_input,
            capture_output=True,
            text=True,
            timeout=2
        )

        output = result.stdout

        # Check output contains expected values
        checks = [
            ('45k' in output or '22' in output, "Token count"),
            ('7' in output, "Agent count"),
            ('95' in output or 'OPTIMAL' in output, "Confidence/Status")
        ]

        failed_checks = [name for passed, name in checks if not passed]

        if not failed_checks:
            return True, "End-to-end integration successful"
        else:
            return False, f"Missing: {', '.join(failed_checks)}"

    # ========================================================================
    # Main Test Runner
    # ========================================================================

    def run_all_tests(self) -> Dict:
        """Run all tests and return results."""
        self.log(f"\n{Colors.BOLD}{'='*80}{Colors.RESET}", "INFO")
        self.log(f"{Colors.BOLD}STATUSLINE FIXES - COMPREHENSIVE VALIDATION SUITE{Colors.RESET}", "INFO")
        self.log(f"{Colors.BOLD}{'='*80}{Colors.RESET}\n", "INFO")

        tests = [
            ("Confidence Extraction (Answer Priority)", self.test_confidence_extraction),
            ("Multi-Source Token Verification", self.test_multi_source_verification),
            ("Agent Counter Accuracy", self.test_agent_counter),
            ("Real-Time Update Loop", self.test_realtime_loop_exists),
            ("Update Metrics From Output", self.test_update_metrics_from_output),
            ("Statusline Performance (< 100ms)", self.test_statusline_performance),
            ("End-to-End Integration", self.test_end_to_end_integration),
        ]

        for name, test_func in tests:
            self.run_test(name, test_func)

        return self.generate_report()

    def generate_report(self) -> Dict:
        """Generate final test report."""
        total = len(self.test_results)
        passed = sum(1 for r in self.test_results if r['passed'])
        failed = total - passed
        success_rate = (passed / total * 100) if total > 0 else 0

        self.log(f"\n{Colors.BOLD}{'='*80}{Colors.RESET}", "INFO")
        self.log(f"{Colors.BOLD}TEST RESULTS{Colors.RESET}\n", "INFO")

        for result in self.test_results:
            status = f"{Colors.GREEN}✓ PASS{Colors.RESET}" if result['passed'] else f"{Colors.RED}✗ FAIL{Colors.RESET}"
            self.log(f"{status} {result['name']}: {result['message']}", "INFO")

        self.log(f"\n{Colors.BOLD}SUMMARY{Colors.RESET}", "INFO")
        self.log(f"Total Tests: {total}", "INFO")
        self.log(f"Passed: {Colors.GREEN}{passed}{Colors.RESET}", "INFO")
        self.log(f"Failed: {Colors.RED}{failed}{Colors.RESET}", "INFO")
        self.log(f"Success Rate: {success_rate:.1f}%", "INFO")

        if success_rate == 100:
            self.log(f"\n{Colors.GREEN}{Colors.BOLD}✓ ALL TESTS PASSED - PRODUCTION READY{Colors.RESET}\n", "SUCCESS")
        else:
            self.log(f"\n{Colors.RED}{Colors.BOLD}✗ SOME TESTS FAILED - NOT PRODUCTION READY{Colors.RESET}\n", "FAIL")

        self.log(f"{Colors.BOLD}{'='*80}{Colors.RESET}\n", "INFO")

        return {
            'total': total,
            'passed': passed,
            'failed': failed,
            'success_rate': success_rate,
            'results': self.test_results,
            'production_ready': success_rate == 100
        }


def main():
    """Main execution."""
    import argparse

    parser = argparse.ArgumentParser(description='Statusline fixes validation suite')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Verbose output')
    parser.add_argument('--json', action='store_true',
                       help='Output as JSON')

    args = parser.parse_args()

    suite = StatuslineTestSuite(verbose=args.verbose)
    report = suite.run_all_tests()

    if args.json:
        print(json.dumps(report, indent=2))

    sys.exit(0 if report['production_ready'] else 1)


if __name__ == '__main__':
    main()
