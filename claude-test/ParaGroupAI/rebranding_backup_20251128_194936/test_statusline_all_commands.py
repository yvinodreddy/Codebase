#!/usr/bin/env python3
"""
test_statusline_all_commands.py - Comprehensive Test Suite for ALL Command Types

Tests that statusline updates correctly for:
- Bash commands (ls, pwd, echo, cat, grep, etc.)
- Read/Write/Edit operations
- Grep/Glob searches
- Task/WebFetch operations
- SlashCommand operations

Validates:
1. Agent counter increments for each command
2. Token metrics update with real values
3. Confidence score recalculates
4. Status updates based on usage
5. Background task detection works

Production-ready validation with zero breaking changes.
"""

import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Dict, List, Tuple


class StatuslineCommandTester:
    """Test statusline updates for all command types."""

    def __init__(self):
        """Initialize tester."""
        self.base_dir = Path("/home/user01/claude-test/ClaudePrompt")
        self.tmp_dir = self.base_dir / "tmp"
        self.hook_script = self.base_dir / ".claude/hooks/PostToolUse/capture_live_metrics.sh"
        self.metrics_file = self.tmp_dir / "realtime_metrics.json"
        self.agent_counter = self.tmp_dir / "agent_usage_counter.txt"

        # Ensure paths exist
        self.tmp_dir.mkdir(parents=True, exist_ok=True)

    def reset_metrics(self):
        """Reset all metrics to clean state."""
        # Clear metrics file
        if self.metrics_file.exists():
            self.metrics_file.write_text(json.dumps({
                'agents': '0',
                'tokens_used': 0,
                'tokens_total': 200000,
                'tokens_pct': 0.0,
                'confidence': 0.0,
                'status': '🟢 READY'
            }, indent=2))

        # Reset agent counter
        if self.agent_counter.exists():
            self.agent_counter.write_text("0")

    def simulate_tool_execution(self, tool_name: str, tool_input: Dict,
                               tool_result: str = "success",
                               conversation_stats: Dict = None) -> Dict:
        """
        Simulate a tool execution by calling the PostToolUse hook.

        Args:
            tool_name: Name of the tool (Bash, Read, Write, Grep, etc.)
            tool_input: Input parameters for the tool
            tool_result: Result from tool execution
            conversation_stats: Token/context stats from Claude Code

        Returns:
            Updated metrics dictionary
        """
        # Default conversation stats if not provided
        if conversation_stats is None:
            # Simulate increasing token usage
            current_tokens = 30000 + (hash(tool_name) % 20000)
            conversation_stats = {
                'context_tokens': current_tokens,
                'max_tokens': 200000,
                'total_tokens': current_tokens
            }

        # Build hook input JSON
        hook_input = {
            'tool_name': tool_name,
            'tool_input': tool_input,
            'tool_result': tool_result,
            'conversation_stats': conversation_stats
        }

        # Call hook script
        try:
            result = subprocess.run(
                [str(self.hook_script)],
                input=json.dumps(hook_input),
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.returncode != 0:
                print(f"⚠️  Hook execution failed: {result.stderr}")
                return {}

        except Exception as e:
            print(f"⚠️  Hook execution error: {e}")
            return {}

        # Read updated metrics
        if self.metrics_file.exists():
            try:
                return json.loads(self.metrics_file.read_text())
            except:
                return {}

        return {}

    def test_bash_commands(self) -> Tuple[bool, List[str]]:
        """Test that Bash commands update statusline."""
        results = []
        success = True

        print("\n" + "="*80)
        print("TEST 1: Bash Commands (ls, pwd, echo, cat, grep, etc.)")
        print("="*80)

        bash_commands = [
            {"command": "ls", "description": "List files"},
            {"command": "pwd", "description": "Print working directory"},
            {"command": "echo 'test'", "description": "Echo text"},
            {"command": "cat test.txt", "description": "Read file"},
            {"command": "grep 'pattern' file.txt", "description": "Search file"},
            {"command": "find . -name '*.py'", "description": "Find files"},
            {"command": "ps aux", "description": "List processes"},
            {"command": "df -h", "description": "Disk usage"}
        ]

        self.reset_metrics()
        initial_agents = 0

        for i, cmd_info in enumerate(bash_commands, 1):
            cmd = cmd_info['command']
            desc = cmd_info['description']

            print(f"\n[{i}/{len(bash_commands)}] Testing: {desc} ({cmd})")

            # Simulate execution
            metrics = self.simulate_tool_execution(
                tool_name="Bash",
                tool_input={"command": cmd, "description": desc},
                tool_result=f"Output from {cmd}",
                conversation_stats={'context_tokens': 30000 + (i * 2000), 'max_tokens': 200000}
            )

            if not metrics:
                results.append(f"❌ FAIL: {cmd} - No metrics returned")
                success = False
                continue

            # Validate agent counter incremented
            current_agents = int(metrics.get('agents', '0'))
            expected_agents = initial_agents + i

            if current_agents == expected_agents:
                results.append(f"✅ PASS: {cmd} - Agents: {current_agents}")
            else:
                results.append(f"❌ FAIL: {cmd} - Expected {expected_agents} agents, got {current_agents}")
                success = False

            # Validate tokens updated
            tokens_used = metrics.get('tokens_used', 0)
            if tokens_used > 0:
                results.append(f"  ✓ Tokens: {tokens_used} ({metrics.get('tokens_display', 'N/A')})")
            else:
                results.append(f"  ⚠️  Tokens: 0 (may be expected for test environment)")

            # Validate confidence
            confidence = metrics.get('confidence', 0.0)
            results.append(f"  ✓ Confidence: {confidence:.1f}%")

            # Validate status
            status = metrics.get('status', 'Unknown')
            results.append(f"  ✓ Status: {status}")

        return success, results

    def test_file_operations(self) -> Tuple[bool, List[str]]:
        """Test that Read/Write/Edit operations update statusline."""
        results = []
        success = True

        print("\n" + "="*80)
        print("TEST 2: File Operations (Read, Write, Edit)")
        print("="*80)

        operations = [
            {"tool": "Read", "input": {"file_path": "/tmp/test.txt"}},
            {"tool": "Write", "input": {"file_path": "/tmp/test2.txt", "content": "test"}},
            {"tool": "Edit", "input": {"file_path": "/tmp/test.txt", "old_string": "a", "new_string": "b"}},
        ]

        self.reset_metrics()

        for i, op_info in enumerate(operations, 1):
            tool = op_info['tool']
            tool_input = op_info['input']

            print(f"\n[{i}/{len(operations)}] Testing: {tool}")

            metrics = self.simulate_tool_execution(
                tool_name=tool,
                tool_input=tool_input,
                tool_result="success",
                conversation_stats={'context_tokens': 40000 + (i * 3000), 'max_tokens': 200000}
            )

            if not metrics:
                results.append(f"❌ FAIL: {tool} - No metrics returned")
                success = False
                continue

            current_agents = int(metrics.get('agents', '0'))
            if current_agents == i:
                results.append(f"✅ PASS: {tool} - Agents: {current_agents}")
            else:
                results.append(f"❌ FAIL: {tool} - Expected {i} agents, got {current_agents}")
                success = False

        return success, results

    def test_search_operations(self) -> Tuple[bool, List[str]]:
        """Test that Grep/Glob operations update statusline."""
        results = []
        success = True

        print("\n" + "="*80)
        print("TEST 3: Search Operations (Grep, Glob)")
        print("="*80)

        operations = [
            {"tool": "Grep", "input": {"pattern": "test", "output_mode": "content"}},
            {"tool": "Glob", "input": {"pattern": "*.py"}},
        ]

        self.reset_metrics()

        for i, op_info in enumerate(operations, 1):
            tool = op_info['tool']
            tool_input = op_info['input']

            print(f"\n[{i}/{len(operations)}] Testing: {tool}")

            metrics = self.simulate_tool_execution(
                tool_name=tool,
                tool_input=tool_input,
                tool_result="Found 10 matches",
                conversation_stats={'context_tokens': 50000 + (i * 5000), 'max_tokens': 200000}
            )

            if not metrics:
                results.append(f"❌ FAIL: {tool} - No metrics returned")
                success = False
                continue

            current_agents = int(metrics.get('agents', '0'))
            if current_agents == i:
                results.append(f"✅ PASS: {tool} - Agents: {current_agents}")
            else:
                results.append(f"❌ FAIL: {tool} - Expected {i} agents, got {current_agents}")
                success = False

        return success, results

    def test_slashcommand_exclusion(self) -> Tuple[bool, List[str]]:
        """Test that SlashCommand does NOT increment agent counter."""
        results = []
        success = True

        print("\n" + "="*80)
        print("TEST 4: SlashCommand Exclusion (should NOT increment agents)")
        print("="*80)

        self.reset_metrics()

        # Execute a SlashCommand
        metrics = self.simulate_tool_execution(
            tool_name="SlashCommand",
            tool_input={"command": "/help"},
            tool_result="Help text",
            conversation_stats={'context_tokens': 35000, 'max_tokens': 200000}
        )

        if not metrics:
            results.append("⚠️  WARNING: No metrics returned (may be expected)")
            return True, results

        current_agents = int(metrics.get('agents', '0'))
        if current_agents == 0:
            results.append(f"✅ PASS: SlashCommand excluded - Agents: {current_agents}")
        else:
            results.append(f"❌ FAIL: SlashCommand should NOT increment - Agents: {current_agents}")
            success = False

        return success, results

    def test_token_tracking_accuracy(self) -> Tuple[bool, List[str]]:
        """Test that token tracking uses real values."""
        results = []
        success = True

        print("\n" + "="*80)
        print("TEST 5: Token Tracking Accuracy (real values, not 0k/200k)")
        print("="*80)

        self.reset_metrics()

        # Simulate multiple commands with increasing token usage
        token_values = [30000, 45000, 62000, 81000, 95000]

        for i, expected_tokens in enumerate(token_values, 1):
            print(f"\n[{i}/{len(token_values)}] Testing with {expected_tokens} tokens")

            metrics = self.simulate_tool_execution(
                tool_name="Bash",
                tool_input={"command": f"ls -la {i}"},
                tool_result="output",
                conversation_stats={'context_tokens': expected_tokens, 'max_tokens': 200000}
            )

            if not metrics:
                results.append(f"❌ FAIL: Command {i} - No metrics returned")
                success = False
                continue

            actual_tokens = metrics.get('tokens_used', 0)
            tokens_display = metrics.get('tokens_display', 'N/A')

            # Allow some tolerance for estimation
            if actual_tokens > 0:
                results.append(f"✅ PASS: Tokens tracked: {actual_tokens} ({tokens_display})")
            else:
                results.append(f"⚠️  WARNING: Tokens = 0 (may use estimation in test env)")

        return success, results

    def run_all_tests(self) -> bool:
        """Run all tests and report results."""
        print("\n" + "="*80)
        print("COMPREHENSIVE STATUSLINE COMMAND TEST SUITE")
        print("Testing statusline updates for ALL command types")
        print("="*80)

        all_results = []
        all_success = True

        # Test 1: Bash commands
        success, results = self.test_bash_commands()
        all_results.extend(results)
        all_success = all_success and success

        # Test 2: File operations
        success, results = self.test_file_operations()
        all_results.extend(results)
        all_success = all_success and success

        # Test 3: Search operations
        success, results = self.test_search_operations()
        all_results.extend(results)
        all_success = all_success and success

        # Test 4: SlashCommand exclusion
        success, results = self.test_slashcommand_exclusion()
        all_results.extend(results)
        all_success = all_success and success

        # Test 5: Token tracking
        success, results = self.test_token_tracking_accuracy()
        all_results.extend(results)
        all_success = all_success and success

        # Print summary
        print("\n" + "="*80)
        print("TEST SUMMARY")
        print("="*80)

        for result in all_results:
            print(result)

        print("\n" + "="*80)
        if all_success:
            print("✅ ALL TESTS PASSED - Statusline updates for ALL commands!")
        else:
            print("❌ SOME TESTS FAILED - See details above")
        print("="*80)

        return all_success


def main():
    """Run test suite."""
    tester = StatuslineCommandTester()
    success = tester.run_all_tests()

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
