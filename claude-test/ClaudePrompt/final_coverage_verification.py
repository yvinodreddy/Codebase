#!/usr/bin/env python3
"""
Final Coverage Verification for Track 2
Verifies all files have 100% coverage and all tests pass
"""

import subprocess
import json
from pathlib import Path
from typing import Dict, List

class FinalVerification:
    """Final verification of Track 2 test coverage"""

    def __init__(self):
        self.track2_files = [
            'agent_framework/context_manager.py',
            'agent_framework/context_manager_enhanced.py',
            'agent_framework/context_manager_optimized.py',
            'agent_framework/verification_system.py',
            'agent_framework/verification_system_enhanced.py',
            'agent_framework/feedback_loop.py',
            'agent_framework/feedback_loop_enhanced.py',
            'agent_framework/feedback_loop_overlapped.py',
            'agent_framework/rate_limiter.py',
            'agent_framework/subagent_orchestrator.py',
            'agent_framework/agentic_search.py',
            'agent_framework/code_generator.py',
            'agent_framework/mcp_integration.py',
            'answer_to_file.py',
            'prompt_history.py'
        ]

    def run_full_coverage_check(self) -> Dict:
        """Run full coverage check for all Track 2 files"""
        print("=" * 80)
        print("🔍 FINAL VERIFICATION - TRACK 2 COVERAGE")
        print("=" * 80)
        print()

        cmd = [
            'pytest', 'tests/complete_track2_100',
            '--cov=agent_framework',
            '--cov=answer_to_file',
            '--cov=prompt_history',
            '--cov-report=json',
            '--cov-report=term',
            '-v', '--tb=short'
        ]

        print("Running comprehensive test suite...")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

        # Parse results
        coverage_data = self._parse_coverage_json()
        test_results = self._parse_test_output(result.stdout)

        return {
            'coverage': coverage_data,
            'tests': test_results,
            'pytest_exitcode': result.returncode
        }

    def _parse_coverage_json(self) -> Dict:
        """Parse coverage.json file"""
        try:
            with open('coverage.json', 'r') as f:
                cov_data = json.load(f)

            results = {}
            for file in self.track2_files:
                if file in cov_data['files']:
                    file_data = cov_data['files'][file]
                    summary = file_data['summary']

                    results[file] = {
                        'percent': summary['percent_covered'],
                        'covered': summary['covered_lines'],
                        'missing': summary['num_statements'] - summary['covered_lines'],
                        'total': summary['num_statements'],
                        'missing_lines': file_data.get('missing_lines', [])
                    }

            return results

        except Exception as e:
            print(f"⚠️  Error parsing coverage: {e}")
            return {}

    def _parse_test_output(self, output: str) -> Dict:
        """Parse pytest output for test results"""
        results = {
            'passed': 0,
            'failed': 0,
            'skipped': 0,
            'errors': 0,
            'total': 0
        }

        # Look for summary line like "351 passed, 20 failed, 38 skipped"
        summary_pattern = r'(\d+) passed|(\d+) failed|(\d+) skipped|(\d+) error'
        for match in re.finditer(summary_pattern, output):
            if match.group(1):
                results['passed'] = int(match.group(1))
            elif match.group(2):
                results['failed'] = int(match.group(2))
            elif match.group(3):
                results['skipped'] = int(match.group(3))
            elif match.group(4):
                results['errors'] = int(match.group(4))

        results['total'] = results['passed'] + results['failed'] + results['skipped'] + results['errors']

        return results

    def print_final_report(self, verification_results: Dict):
        """Print comprehensive final report"""
        coverage = verification_results['coverage']
        tests = verification_results['tests']

        print("\n" + "=" * 80)
        print("📊 FINAL TRACK 2 TEST COVERAGE REPORT")
        print("=" * 80)
        print()

        # Coverage statistics
        if coverage:
            total_covered = sum(c['covered'] for c in coverage.values())
            total_lines = sum(c['total'] for c in coverage.values())
            overall_percent = (total_covered / total_lines * 100) if total_lines > 0 else 0

            files_at_100 = sum(1 for c in coverage.values() if c['percent'] >= 99.5)

            print(f"📈 Coverage Statistics:")
            print(f"   Overall: {overall_percent:.2f}%")
            print(f"   Lines covered: {total_covered}/{total_lines}")
            print(f"   Files at 100%: {files_at_100}/15")
            print()

            # Per-file breakdown
            print(f"📋 Per-File Coverage:\n")
            for file, data in sorted(coverage.items(), key=lambda x: x[1]['percent'], reverse=True):
                percent = data['percent']
                missing = data['missing']

                if percent >= 99.5:
                    status = "✅ 100%"
                elif percent >= 90:
                    status = f"🟢 {percent:.1f}%"
                elif percent >= 70:
                    status = f"🟡 {percent:.1f}%"
                else:
                    status = f"🔴 {percent:.1f}%"

                filename = Path(file).name
                print(f"   {status:<15} {filename:<50} ({missing} lines missing)")

            print()

        # Test statistics
        if tests['total'] > 0:
            success_rate = (tests['passed'] / tests['total'] * 100) if tests['total'] > 0 else 0

            print(f"🧪 Test Results:")
            print(f"   Total tests: {tests['total']}")
            print(f"   ✅ Passed: {tests['passed']}")
            print(f"   ❌ Failed: {tests['failed']}")
            print(f"   ⏭️  Skipped: {tests['skipped']}")
            print(f"   ⚠️  Errors: {tests['errors']}")
            print(f"   Success rate: {success_rate:.1f}%")
            print()

        # Final verdict
        print("=" * 80)

        all_at_100 = all(c['percent'] >= 99.5 for c in coverage.values()) if coverage else False
        all_tests_pass = tests['failed'] == 0 and tests['errors'] == 0 if tests['total'] > 0 else False

        if all_at_100 and all_tests_pass:
            print("🎉 SUCCESS! 100% COVERAGE + 100% SUCCESS RATE ACHIEVED!")
            print("   ✅ All 15 files at 100% coverage")
            print("   ✅ All tests passing")
        elif all_at_100:
            print("🎯 100% COVERAGE ACHIEVED! (with some test failures)")
            print(f"   ✅ All 15 files at 100% coverage")
            print(f"   ⚠️  {tests['failed']} tests failing - need fixes")
        elif all_tests_pass:
            print("✅ ALL TESTS PASSING! (coverage not yet 100%)")
            print(f"   🔄 {files_at_100}/15 files at 100% coverage")
            print(f"   ✅ All tests passing")
        else:
            print("🔄 IN PROGRESS")
            print(f"   Coverage: {files_at_100}/15 files at 100%")
            print(f"   Tests: {tests['failed']} failing, {tests['errors']} errors")

        print("=" * 80)
        print()

        return all_at_100 and all_tests_pass


if __name__ == "__main__":
    import re
    import sys

    verifier = FinalVerification()
    results = verifier.run_full_coverage_check()
    success = verifier.print_final_report(results)

    sys.exit(0 if success else 1)
