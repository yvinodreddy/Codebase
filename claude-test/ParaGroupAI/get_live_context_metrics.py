#!/usr/bin/env python3
"""
get_live_context_metrics.py - Live Context Metrics Extractor

Parses the output of `/context` command to extract real-time metrics:
- Model name
- Token usage (used/total)
- Token percentage
- Context breakdown (system, tools, memory, messages)

This ensures statusline displays LIVE metrics, not cached/hardcoded values.

Usage:
    python3 get_live_context_metrics.py [--json]

Returns:
    JSON object with live metrics or formatted text
"""

import subprocess
import re
import json
import sys
from typing import Dict, Optional


class LiveContextMetrics:
    """Extract live metrics from /context command."""

    def __init__(self):
        self.metrics = {
            'model': 'Unknown',
            'model_short': 'Unknown',
            'tokens_used': 0,
            'tokens_total': 200000,
            'tokens_pct': 0.0,
            'tokens_display': '0k/200k',
            'system_tokens': 0,
            'tools_tokens': 0,
            'memory_tokens': 0,
            'messages_tokens': 0,
            'free_tokens': 200000,
            'status': 'success',
            'error': None
        }

    def get_context_output(self) -> Optional[str]:
        """
        Run /context command and capture output.

        Returns:
            Raw output from /context command, or None if failed
        """
        try:
            # Run claude-code with /context command
            # Note: This requires special handling since /context is a CLI command
            # We'll try multiple methods to get the output

            # Method 1: Try to read from environment if available
            context_file = '/tmp/claude_context_latest.txt'

            # Method 2: Parse from a cached location if the system provides it
            # For now, we'll return a placeholder that the shell script will handle
            return None

        except Exception as e:
            self.metrics['status'] = 'error'
            self.metrics['error'] = str(e)
            return None

    def parse_context_output(self, output: str) -> bool:
        """
        Parse /context command output to extract metrics.

        Expected format:
            claude-sonnet-4-5-20250929 · 29k/200k tokens (15%)

        Args:
            output: Raw output from /context command

        Returns:
            True if parsing succeeded, False otherwise
        """
        try:
            # Remove ANSI color codes
            ansi_escape = re.compile(r'\x1b\[[0-9;]*m|\x1b\[\??[0-9;]*[a-zA-Z]')
            clean_output = ansi_escape.sub('', output)

            # Pattern: model-name · XXk/YYYk tokens (ZZ%)
            # Example: claude-sonnet-4-5-20250929 · 29k/200k tokens (15%)
            pattern = r'(claude-[a-z0-9-]+)\s*·\s*(\d+\.?\d*)k?/(\d+\.?\d*)k?\s*tokens\s*\((\d+\.?\d*)%\)'

            match = re.search(pattern, clean_output)

            if match:
                model_full = match.group(1)
                tokens_used_k = float(match.group(2))
                tokens_total_k = float(match.group(3))
                tokens_pct = float(match.group(4))

                # Convert k to actual numbers
                self.metrics['tokens_used'] = int(tokens_used_k * 1000)
                self.metrics['tokens_total'] = int(tokens_total_k * 1000)
                self.metrics['tokens_pct'] = tokens_pct
                self.metrics['tokens_display'] = f"{tokens_used_k:.0f}k/{tokens_total_k:.0f}k"

                # Parse model name
                self.metrics['model'] = model_full
                self.metrics['model_short'] = self._convert_model_name(model_full)

                # Extract component breakdown if available
                # Pattern: System prompt: X.Xk tokens (X.X%)
                system_match = re.search(r'System prompt:\s*[\[\x1b[0-9;]*m]*([0-9.]+)k?\s*tokens\s*\(([0-9.]+)%\)', clean_output)
                if system_match:
                    self.metrics['system_tokens'] = int(float(system_match.group(1)) * 1000)

                # Pattern: System tools: X.Xk tokens (X.X%)
                tools_match = re.search(r'System tools:\s*[\[\x1b[0-9;]*m]*([0-9.]+)k?\s*tokens\s*\(([0-9.]+)%\)', clean_output)
                if tools_match:
                    self.metrics['tools_tokens'] = int(float(tools_match.group(1)) * 1000)

                # Pattern: Memory files: X.Xk tokens (X.X%)
                memory_match = re.search(r'Memory files:\s*[\[\x1b[0-9;]*m]*([0-9.]+)k?\s*tokens\s*\(([0-9.]+)%\)', clean_output)
                if memory_match:
                    self.metrics['memory_tokens'] = int(float(memory_match.group(1)) * 1000)

                # Pattern: Messages: X.Xk tokens (X.X%)
                messages_match = re.search(r'Messages:\s*[\[\x1b[0-9;]*m]*([0-9.]+)k?\s*tokens\s*\(([0-9.]+)%\)', clean_output)
                if messages_match:
                    self.metrics['messages_tokens'] = int(float(messages_match.group(1)) * 1000)

                # Calculate free tokens
                self.metrics['free_tokens'] = self.metrics['tokens_total'] - self.metrics['tokens_used']

                self.metrics['status'] = 'success'
                return True
            else:
                self.metrics['status'] = 'parse_failed'
                self.metrics['error'] = 'Could not parse context output format'
                return False

        except Exception as e:
            self.metrics['status'] = 'error'
            self.metrics['error'] = str(e)
            return False

    def _convert_model_name(self, model_full: str) -> str:
        """
        Convert full model name to short display name.

        Args:
            model_full: Full model name (e.g., claude-sonnet-4-5-20250929)

        Returns:
            Short display name (e.g., Sonnet 4.5)
        """
        if 'sonnet-4-5' in model_full or 'sonnet-4.5' in model_full:
            return 'Sonnet 4.5'
        elif 'sonnet' in model_full:
            return 'Sonnet'
        elif 'opus' in model_full:
            return 'Opus'
        elif 'haiku' in model_full:
            return 'Haiku'
        else:
            return 'Claude'

    def parse_from_stdin(self) -> bool:
        """
        Parse context output from stdin.

        Returns:
            True if parsing succeeded, False otherwise
        """
        try:
            context_output = sys.stdin.read()
            if context_output:
                return self.parse_context_output(context_output)
            else:
                self.metrics['status'] = 'no_input'
                self.metrics['error'] = 'No input provided on stdin'
                return False
        except Exception as e:
            self.metrics['status'] = 'error'
            self.metrics['error'] = str(e)
            return False

    def get_metrics(self) -> Dict:
        """
        Get extracted metrics.

        Returns:
            Dictionary with all extracted metrics
        """
        return self.metrics

    def to_json(self) -> str:
        """
        Convert metrics to JSON string.

        Returns:
            JSON string representation of metrics
        """
        return json.dumps(self.metrics, indent=2)

    def to_text(self) -> str:
        """
        Convert metrics to human-readable text.

        Returns:
            Formatted text representation of metrics
        """
        lines = []
        lines.append(f"Model: {self.metrics['model_short']} ({self.metrics['model']})")
        lines.append(f"Tokens: {self.metrics['tokens_display']} ({self.metrics['tokens_pct']:.1f}%)")
        lines.append(f"  - System: {self.metrics['system_tokens']:,} tokens")
        lines.append(f"  - Tools: {self.metrics['tools_tokens']:,} tokens")
        lines.append(f"  - Memory: {self.metrics['memory_tokens']:,} tokens")
        lines.append(f"  - Messages: {self.metrics['messages_tokens']:,} tokens")
        lines.append(f"Free: {self.metrics['free_tokens']:,} tokens")
        lines.append(f"Status: {self.metrics['status']}")
        if self.metrics['error']:
            lines.append(f"Error: {self.metrics['error']}")
        return '\n'.join(lines)


def main():
    """Main execution."""
    import argparse

    parser = argparse.ArgumentParser(description='Extract live context metrics')
    parser.add_argument('--json', action='store_true',
                       help='Output as JSON')
    parser.add_argument('--input', type=str,
                       help='Input file containing /context output (default: stdin)')

    args = parser.parse_args()

    extractor = LiveContextMetrics()

    if args.input:
        # Read from file
        try:
            with open(args.input, 'r') as f:
                context_output = f.read()
            extractor.parse_context_output(context_output)
        except Exception as e:
            print(json.dumps({'status': 'error', 'error': str(e)}))
            sys.exit(1)
    else:
        # Read from stdin
        extractor.parse_from_stdin()

    if args.json:
        print(extractor.to_json())
    else:
        print(extractor.to_text())


if __name__ == '__main__':
    main()
