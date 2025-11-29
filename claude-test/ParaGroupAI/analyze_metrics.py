#!/usr/bin/env python3
"""
analyze_metrics.py - Correlation Analysis Tool

Analyzes the relationship between context usage and confidence scores.
Identifies bottlenecks and provides optimization recommendations.

Usage:
    python3 analyze_metrics.py [--last N] [--export]
"""

import csv
import sys
import os
from datetime import datetime
from collections import defaultdict
from typing import List, Dict, Tuple

class MetricsAnalyzer:
    """Analyzes ULTRATHINK execution metrics."""

    def __init__(self, csv_file: str):
        self.csv_file = csv_file
        self.metrics = []
        self.load_metrics()

    def load_metrics(self):
        """Load metrics from CSV file."""
        if not os.path.exists(self.csv_file):
            print(f"⚠️  Metrics file not found: {self.csv_file}")
            print("Run cpp_with_metrics first to generate data.")
            sys.exit(1)

        with open(self.csv_file, 'r') as f:
            reader = csv.DictReader(f)
            self.metrics = list(reader)

        if not self.metrics:
            print("⚠️  No metrics data available yet.")
            print("Run cpp_with_metrics to start collecting data.")
            sys.exit(1)

    def get_last_n(self, n: int) -> List[Dict]:
        """Get last N executions."""
        return self.metrics[-n:] if len(self.metrics) >= n else self.metrics

    def analyze_context_vs_confidence(self, data: List[Dict]) -> Dict:
        """Analyze correlation between context usage and confidence."""

        # Define context usage brackets
        brackets = {
            '0-50%': {'min': 0, 'max': 50, 'confidences': [], 'count': 0},
            '50-85%': {'min': 50, 'max': 85, 'confidences': [], 'count': 0},
            '85-95%': {'min': 85, 'max': 95, 'confidences': [], 'count': 0},
            '95-100%': {'min': 95, 'max': 100, 'confidences': [], 'count': 0},
        }

        # Categorize data
        for entry in data:
            try:
                context_pct = float(entry['Context_Pct'])
                confidence = float(entry['Confidence'])

                for bracket_name, bracket_data in brackets.items():
                    if bracket_data['min'] <= context_pct < bracket_data['max']:
                        bracket_data['confidences'].append(confidence)
                        bracket_data['count'] += 1
                        break
            except (ValueError, KeyError):
                continue

        # Calculate averages
        results = {}
        for bracket_name, bracket_data in brackets.items():
            if bracket_data['count'] > 0:
                avg_confidence = sum(bracket_data['confidences']) / bracket_data['count']
                results[bracket_name] = {
                    'avg_confidence': avg_confidence,
                    'count': bracket_data['count'],
                    'status': self._get_status(avg_confidence, bracket_name)
                }
            else:
                results[bracket_name] = {
                    'avg_confidence': 0,
                    'count': 0,
                    'status': 'N/A'
                }

        return results

    def _get_status(self, confidence: float, bracket: str) -> str:
        """Get status indicator based on confidence and bracket."""
        if confidence >= 99:
            return '✅ OPTIMAL'
        elif confidence >= 95:
            return '✅ EFFICIENT'
        elif confidence >= 90:
            return '🟡 WARNING'
        else:
            return '🔴 CRITICAL'

    def find_bottlenecks(self, data: List[Dict]) -> List[Dict]:
        """Identify slow executions and high context usage."""
        bottlenecks = []

        for entry in data:
            try:
                time_sec = float(entry['Time_Sec'])
                context_pct = float(entry['Context_Pct'])
                confidence = float(entry['Confidence'])

                # Flag as bottleneck if:
                # - Time > 60 seconds
                # - Context > 85%
                # - Confidence < 95%
                if time_sec > 60 or context_pct > 85 or confidence < 95:
                    bottlenecks.append({
                        'timestamp': entry['Timestamp'],
                        'prompt': entry['Prompt'],
                        'time': time_sec,
                        'context': context_pct,
                        'confidence': confidence,
                        'reasons': []
                    })

                    if time_sec > 60:
                        bottlenecks[-1]['reasons'].append(f'Slow execution ({time_sec:.1f}s)')
                    if context_pct > 85:
                        bottlenecks[-1]['reasons'].append(f'High context ({context_pct:.1f}%)')
                    if confidence < 95:
                        bottlenecks[-1]['reasons'].append(f'Low confidence ({confidence:.1f}%)')
            except (ValueError, KeyError):
                continue

        return bottlenecks

    def calculate_efficiency_score(self, data: List[Dict]) -> Dict:
        """Calculate overall system efficiency."""
        if not data:
            return {'score': 0, 'grade': 'N/A'}

        total_confidence = 0
        total_time = 0
        high_context_count = 0

        for entry in data:
            try:
                total_confidence += float(entry['Confidence'])
                total_time += float(entry['Time_Sec'])
                if float(entry['Context_Pct']) > 85:
                    high_context_count += 1
            except (ValueError, KeyError):
                continue

        avg_confidence = total_confidence / len(data)
        avg_time = total_time / len(data)
        high_context_rate = (high_context_count / len(data)) * 100

        # Scoring formula:
        # - Confidence: 50% weight
        # - Speed (inverse of avg time): 30% weight
        # - Low context rate: 20% weight
        confidence_score = (avg_confidence / 100) * 50
        speed_score = max(0, (60 - avg_time) / 60) * 30 if avg_time > 0 else 30
        context_score = max(0, (100 - high_context_rate) / 100) * 20

        efficiency_score = confidence_score + speed_score + context_score

        # Determine grade
        if efficiency_score >= 90:
            grade = 'A (Excellent)'
        elif efficiency_score >= 80:
            grade = 'B (Good)'
        elif efficiency_score >= 70:
            grade = 'C (Fair)'
        elif efficiency_score >= 60:
            grade = 'D (Poor)'
        else:
            grade = 'F (Critical)'

        return {
            'score': efficiency_score,
            'grade': grade,
            'avg_confidence': avg_confidence,
            'avg_time': avg_time,
            'high_context_rate': high_context_rate
        }

    def display_analysis(self, last_n: int = 100):
        """Display comprehensive metrics analysis."""
        data = self.get_last_n(last_n)

        print("=" * 80)
        print("📊 ULTRATHINK METRICS ANALYSIS")
        print("=" * 80)
        print(f"Analyzing last {len(data)} executions")
        print(f"Data file: {self.csv_file}")
        print("")

        # Context vs Confidence Correlation
        print("─" * 80)
        print("🔍 CONTEXT VS CONFIDENCE CORRELATION")
        print("─" * 80)
        print("")

        correlation = self.analyze_context_vs_confidence(data)

        print("┌─────────────┬─────────────────┬────────┬──────────────────┐")
        print("│ Context     │ Avg Confidence  │ Count  │ Status           │")
        print("├─────────────┼─────────────────┼────────┼──────────────────┤")

        for bracket, stats in correlation.items():
            if stats['count'] > 0:
                print(f"│ {bracket:11s} │ {stats['avg_confidence']:14.1f}% │ {stats['count']:6d} │ {stats['status']:16s} │")
            else:
                print(f"│ {bracket:11s} │ {'N/A':>14s} │ {stats['count']:6d} │ {'N/A':16s} │")

        print("└─────────────┴─────────────────┴────────┴──────────────────┘")
        print("")

        # Find correlation insight
        if correlation['0-50%']['count'] > 0 and correlation['85-95%']['count'] > 0:
            optimal_conf = correlation['0-50%']['avg_confidence']
            warning_conf = correlation['85-95%']['avg_confidence']
            delta = optimal_conf - warning_conf

            if delta > 2:
                print(f"⚠️  FINDING: Context usage above 85% correlates with {delta:.1f}% drop in confidence")
                print(f"   Optimal zone (0-50%): {optimal_conf:.1f}% avg confidence")
                print(f"   Warning zone (85-95%): {warning_conf:.1f}% avg confidence")
                print("")

        # Efficiency Score
        print("─" * 80)
        print("🎯 SYSTEM EFFICIENCY SCORE")
        print("─" * 80)
        print("")

        efficiency = self.calculate_efficiency_score(data)

        print(f"Overall Score: {efficiency['score']:.1f}/100  ({efficiency['grade']})")
        print("")
        print(f"  • Average Confidence: {efficiency['avg_confidence']:.1f}%")
        print(f"  • Average Time: {efficiency['avg_time']:.1f}s")
        print(f"  • High Context Rate: {efficiency['high_context_rate']:.1f}%")
        print("")

        # Bottlenecks
        print("─" * 80)
        print("🚨 BOTTLENECKS IDENTIFIED")
        print("─" * 80)
        print("")

        bottlenecks = self.find_bottlenecks(data)

        if bottlenecks:
            print(f"Found {len(bottlenecks)} executions with issues:")
            print("")

            for i, issue in enumerate(bottlenecks[:5], 1):  # Show top 5
                print(f"{i}. {issue['timestamp']}")
                print(f"   Prompt: \"{issue['prompt']}\"")
                print(f"   Issues: {', '.join(issue['reasons'])}")
                print("")

            if len(bottlenecks) > 5:
                print(f"   ... and {len(bottlenecks) - 5} more")
                print("")
        else:
            print("✅ No bottlenecks detected. System performing optimally.")
            print("")

        # Recommendations
        print("─" * 80)
        print("💡 RECOMMENDATIONS")
        print("─" * 80)
        print("")

        recommendations = []

        if efficiency['high_context_rate'] > 30:
            recommendations.append("• Reduce prompt complexity to keep context below 85%")
            recommendations.append("• Use task chunking for complex multi-step prompts")

        if efficiency['avg_time'] > 45:
            recommendations.append(f"• Average execution time ({efficiency['avg_time']:.1f}s) is high")
            recommendations.append("• Consider breaking large tasks into smaller chunks")

        if efficiency['avg_confidence'] < 98:
            recommendations.append(f"• Average confidence ({efficiency['avg_confidence']:.1f}%) below target (99%)")
            recommendations.append("• Review prompts in the 85-95% context range")

        if not recommendations:
            recommendations.append("✅ System is operating optimally. No immediate actions needed.")

        for rec in recommendations:
            print(rec)

        print("")
        print("=" * 80)

def main():
    """Main execution."""
    import argparse

    parser = argparse.ArgumentParser(description='Analyze ULTRATHINK metrics')
    parser.add_argument('--last', type=int, default=100,
                       help='Analyze last N executions (default: 100)')
    parser.add_argument('--csv', type=str,
                       default='/home/user01/claude-test/ClaudePrompt/logs/metrics.csv',
                       help='Path to metrics CSV file')

    args = parser.parse_args()

    analyzer = MetricsAnalyzer(args.csv)
    analyzer.display_analysis(last_n=args.last)

if __name__ == '__main__':
    main()
