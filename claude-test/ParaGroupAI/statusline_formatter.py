#!/usr/bin/env python3
"""
statusline_formatter.py - Enhanced Statusline Display Formatter

PRODUCTION-READY IMPLEMENTATION (2025-11-16)
============================================

PURPOSE:
- Format metrics for statusline display with instance isolation
- Show current instance metrics vs. total across all instances
- Provide clear, concise, informative display format
- Support both per-instance and shared modes

FEATURES:
- ✅ Enhanced format: "Agents: X/Y (N instances)"
- ✅ Backward compatible with shared mode
- ✅ Color-coded status indicators
- ✅ Token usage with percentage
- ✅ Confidence score with precision
- ✅ Automatic mode detection

DISPLAY FORMATS:

Per-Instance Mode (NEW):
    Agents: 25/145 (5)  ← 25 current, 145 total, 5 instances
    Tokens: 15k/200k (7.5%)
    Conf: 99.2%
    Status: 🟢 OPTIMAL

Shared Mode (LEGACY):
    Agents: 145
    Tokens: 15k/200k (7.5%)
    Conf: 99.2%
    Status: 🟢 OPTIMAL

USAGE:
    from statusline_formatter import StatuslineFormatter

    formatter = StatuslineFormatter(instance_mode=True)

    # Format with aggregated data
    display = formatter.format_all(
        current_agents=25,
        total_agents=145,
        instance_count=5,
        tokens_used=15000,
        tokens_total=200000,
        confidence=99.2,
        status='🟢 OPTIMAL'
    )

    print(display)  # Agents: 25/145 (5) | Tokens: 15k/200k (7.5%) | ...
"""

import json
from typing import Dict, Optional


class StatuslineFormatter:
    """
    Formats metrics for statusline display with instance isolation support.

    Provides two display modes:
    1. Per-instance mode: Shows current/total with instance count
    2. Shared mode: Shows simple totals (backward compatible)
    """

    def __init__(self, instance_mode: bool = False):
        """
        Initialize formatter.

        Args:
            instance_mode: Enable per-instance display format
        """
        self.instance_mode = instance_mode

    def format_agents(self, current: int, total: Optional[int] = None,
                      instance_count: Optional[int] = None) -> str:
        """
        Format agent count display.

        Args:
            current: Current instance agent count
            total: Total agents across all instances (optional)
            instance_count: Number of active instances (optional)

        Returns:
            Formatted string

        Examples:
            Per-instance: "Agents: 25/145 (5)"
            Shared: "Agents: 145"
            Single: "Agents: 25"
        """
        if self.instance_mode and total is not None and instance_count is not None:
            # Per-instance mode with aggregation
            return f"Agents: {current}/{total} ({instance_count})"
        elif total is not None and total != current:
            # Show ratio even if not in instance mode
            return f"Agents: {current}/{total}"
        else:
            # Simple mode
            return f"Agents: {current}"

    def format_tokens(self, used: int, total: int = 200000,
                      show_percentage: bool = True) -> str:
        """
        Format token usage display.

        Args:
            used: Tokens used
            total: Total tokens available (default: 200000)
            show_percentage: Show percentage in parentheses

        Returns:
            Formatted string

        Examples:
            "Tokens: 15k/200k (7.5%)"
            "Tokens: 150k/200k (75.0%)"
        """
        used_k = int(used / 1000)
        total_k = int(total / 1000)

        if show_percentage:
            pct = (used / total * 100) if total > 0 else 0
            return f"Tokens: {used_k}k/{total_k}k ({pct:.1f}%)"
        else:
            return f"Tokens: {used_k}k/{total_k}k"

    def format_confidence(self, confidence: float) -> str:
        """
        Format confidence score display.

        Args:
            confidence: Confidence score (0-100)

        Returns:
            Formatted string

        Examples:
            "Conf: 99.2%"
            "Conf: 100.0%"
            "Conf: --" (if confidence is 0 or invalid)
        """
        if confidence <= 0:
            return "Conf: --"
        else:
            return f"Conf: {confidence:.1f}%"

    def format_status(self, status: str) -> str:
        """
        Format status display.

        Args:
            status: Status string (e.g., "🟢 OPTIMAL")

        Returns:
            Formatted string

        Examples:
            "Status: 🟢 OPTIMAL"
            "Status: 🟡 WARNING"
        """
        return f"Status: {status}"

    def format_all(self, current_agents: int,
                   total_agents: Optional[int] = None,
                   instance_count: Optional[int] = None,
                   tokens_used: int = 0,
                   tokens_total: int = 200000,
                   confidence: float = 0.0,
                   status: str = "🟢 OPTIMAL",
                   separator: str = " | ") -> str:
        """
        Format all metrics into a single statusline display.

        Args:
            current_agents: Current instance agent count
            total_agents: Total agents across instances (optional)
            instance_count: Number of active instances (optional)
            tokens_used: Tokens used
            tokens_total: Total tokens available
            confidence: Confidence score (0-100)
            status: Status string
            separator: Separator between metrics

        Returns:
            Complete formatted statusline

        Examples:
            Per-instance: "Agents: 25/145 (5) | Tokens: 15k/200k (7.5%) | Conf: 99.2% | Status: 🟢 OPTIMAL"
            Shared: "Agents: 145 | Tokens: 15k/200k (7.5%) | Conf: 99.2% | Status: 🟢 OPTIMAL"
        """
        parts = [
            self.format_agents(current_agents, total_agents, instance_count),
            self.format_tokens(tokens_used, tokens_total),
            self.format_confidence(confidence),
            self.format_status(status)
        ]

        return separator.join(parts)

    def format_compact(self, current_agents: int,
                       total_agents: Optional[int] = None,
                       instance_count: Optional[int] = None,
                       tokens_pct: float = 0.0,
                       confidence: float = 0.0) -> str:
        """
        Format compact display (no status, shorter format).

        Args:
            current_agents: Current instance agent count
            total_agents: Total agents across instances (optional)
            instance_count: Number of active instances (optional)
            tokens_pct: Token usage percentage
            confidence: Confidence score (0-100)

        Returns:
            Compact formatted statusline

        Examples:
            "A:25/145(5) T:7.5% C:99.2%"
        """
        if self.instance_mode and total_agents is not None and instance_count is not None:
            agents_str = f"A:{current_agents}/{total_agents}({instance_count})"
        else:
            agents_str = f"A:{current_agents}"

        tokens_str = f"T:{tokens_pct:.1f}%"

        if confidence > 0:
            conf_str = f"C:{confidence:.1f}%"
        else:
            conf_str = "C:--"

        return f"{agents_str} {tokens_str} {conf_str}"

    def format_json(self, current_agents: int,
                    total_agents: Optional[int] = None,
                    instance_count: Optional[int] = None,
                    tokens_used: int = 0,
                    tokens_total: int = 200000,
                    confidence: float = 0.0,
                    status: str = "🟢 OPTIMAL") -> str:
        """
        Format metrics as JSON.

        Args:
            current_agents: Current instance agent count
            total_agents: Total agents across instances (optional)
            instance_count: Number of active instances (optional)
            tokens_used: Tokens used
            tokens_total: Total tokens available
            confidence: Confidence score (0-100)
            status: Status string

        Returns:
            JSON string

        Example:
            {
              "agents": {
                "current": 25,
                "total": 145,
                "instance_count": 5
              },
              "tokens": {
                "used": 15000,
                "total": 200000,
                "percentage": 7.5
              },
              "confidence": 99.2,
              "status": "🟢 OPTIMAL"
            }
        """
        data = {
            "agents": {
                "current": current_agents
            },
            "tokens": {
                "used": tokens_used,
                "total": tokens_total,
                "percentage": (tokens_used / tokens_total * 100) if tokens_total > 0 else 0
            },
            "confidence": confidence,
            "status": status
        }

        if total_agents is not None:
            data["agents"]["total"] = total_agents

        if instance_count is not None:
            data["agents"]["instance_count"] = instance_count

        return json.dumps(data, indent=2)

    def parse_metrics_dict(self, metrics: Dict) -> Dict:
        """
        Parse metrics dictionary into formatter arguments.

        Args:
            metrics: Dictionary with metrics from verifier/aggregator

        Returns:
            Dictionary with formatter arguments

        Example Input:
            {
              'agents': 25,
              'total_agents': 145,
              'instance_count': 5,
              'tokens_used': 15000,
              'tokens_total': 200000,
              'tokens_pct': 7.5,
              'confidence': 99.2,
              'status': '🟢 OPTIMAL'
            }
        """
        return {
            'current_agents': metrics.get('agents', 0),
            'total_agents': metrics.get('total_agents'),
            'instance_count': metrics.get('instance_count'),
            'tokens_used': metrics.get('tokens_used', 0),
            'tokens_total': metrics.get('tokens_total', 200000),
            'confidence': metrics.get('confidence', 0.0),
            'status': metrics.get('status', '🟢 OPTIMAL')
        }


def main():
    """CLI interface for testing."""
    import argparse

    parser = argparse.ArgumentParser(description='Statusline Formatter')
    parser.add_argument('--instance-mode', action='store_true', help='Enable instance mode')
    parser.add_argument('--current-agents', type=int, default=25, help='Current agents')
    parser.add_argument('--total-agents', type=int, help='Total agents across instances')
    parser.add_argument('--instance-count', type=int, help='Number of instances')
    parser.add_argument('--tokens-used', type=int, default=15000, help='Tokens used')
    parser.add_argument('--tokens-total', type=int, default=200000, help='Total tokens')
    parser.add_argument('--confidence', type=float, default=99.2, help='Confidence score')
    parser.add_argument('--status', type=str, default='🟢 OPTIMAL', help='Status')
    parser.add_argument('--compact', action='store_true', help='Use compact format')
    parser.add_argument('--json', action='store_true', help='Output as JSON')

    args = parser.parse_args()

    formatter = StatuslineFormatter(instance_mode=args.instance_mode)

    if args.json:
        output = formatter.format_json(
            current_agents=args.current_agents,
            total_agents=args.total_agents,
            instance_count=args.instance_count,
            tokens_used=args.tokens_used,
            tokens_total=args.tokens_total,
            confidence=args.confidence,
            status=args.status
        )
    elif args.compact:
        tokens_pct = (args.tokens_used / args.tokens_total * 100) if args.tokens_total > 0 else 0
        output = formatter.format_compact(
            current_agents=args.current_agents,
            total_agents=args.total_agents,
            instance_count=args.instance_count,
            tokens_pct=tokens_pct,
            confidence=args.confidence
        )
    else:
        output = formatter.format_all(
            current_agents=args.current_agents,
            total_agents=args.total_agents,
            instance_count=args.instance_count,
            tokens_used=args.tokens_used,
            tokens_total=args.tokens_total,
            confidence=args.confidence,
            status=args.status
        )

    print(output)


if __name__ == '__main__':
    main()
