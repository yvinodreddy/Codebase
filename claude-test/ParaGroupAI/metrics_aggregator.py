#!/usr/bin/env python3
"""
metrics_aggregator.py - Cross-Instance Metrics Aggregation

PRODUCTION-READY IMPLEMENTATION (2025-11-16)
============================================

PURPOSE:
- Aggregate metrics across all active Claude Code instances
- Provide cross-instance totals for display
- Calculate combined resource usage
- Support per-instance and global view

FEATURES:
- ✅ Scan all instance files automatically
- ✅ Calculate total agents across instances
- ✅ Calculate weighted average confidence
- ✅ Count active instances
- ✅ Cleanup stale instance files
- ✅ Thread-safe operations
- ✅ Graceful degradation if files missing

USAGE:
    from metrics_aggregator import MetricsAggregator

    aggregator = MetricsAggregator()

    # Get aggregated metrics
    totals = aggregator.aggregate_all()

    print(f"Total agents: {totals['total_agents']}")
    print(f"Active instances: {totals['instance_count']}")
    print(f"Average confidence: {totals['avg_confidence']}")
"""

import json
import os
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import fcntl


class MetricsAggregator:
    """
    Aggregates metrics across all active Claude Code instances.

    Scans instance-specific files and calculates:
    - Total agent count (sum across all instances)
    - Total active instances
    - Weighted average confidence
    - Combined resource usage
    - Per-instance breakdown
    """

    def __init__(self, tmp_dir: Optional[str] = None, max_age_seconds: int = 300):
        """
        Initialize metrics aggregator.

        Args:
            tmp_dir: Directory containing instance metrics files
                    (default: /home/user01/claude-test/ClaudePrompt/tmp/)
            max_age_seconds: Maximum age for file to be considered active
                            (default: 300 = 5 minutes)
        """
        if tmp_dir is None:
            tmp_dir = "/home/user01/claude-test/ClaudePrompt/tmp"

        self.tmp_dir = Path(tmp_dir)
        self.max_age_seconds = max_age_seconds

    def scan_instance_files(self, pattern: str) -> List[Tuple[Path, float]]:
        """
        Scan for instance files matching pattern.

        Args:
            pattern: Glob pattern (e.g., "agent_usage_counter_*.txt")

        Returns:
            List of (file_path, age_seconds) tuples for active files
        """
        active_files = []
        cutoff_time = time.time() - self.max_age_seconds

        for file_path in self.tmp_dir.glob(pattern):
            try:
                mtime = os.path.getmtime(file_path)
                if mtime >= cutoff_time:
                    age = time.time() - mtime
                    active_files.append((file_path, age))
            except Exception:
                # Skip inaccessible files
                continue

        return active_files

    def aggregate_agent_counts(self) -> Dict:
        """
        Aggregate agent counts across all instances.

        Returns:
            Dictionary with:
            - total_agents: Sum of agents across all instances
            - instance_counts: List of per-instance counts
            - instance_count: Number of active instances
            - max_agents: Highest agent count from any instance
            - min_agents: Lowest agent count from any instance
        """
        # Scan for agent counter files
        pattern = "agent_usage_counter_*.txt"
        instance_files = self.scan_instance_files(pattern)

        total_agents = 0
        instance_counts = []

        for file_path, age in instance_files:
            try:
                with open(file_path, 'r') as f:
                    count = int(f.read().strip())
                    total_agents += count
                    instance_counts.append({
                        'instance_id': self._extract_instance_id(file_path.name),
                        'agents': count,
                        'age_seconds': age
                    })
            except Exception:
                # Skip corrupted files
                continue

        return {
            'total_agents': total_agents,
            'instance_counts': instance_counts,
            'instance_count': len(instance_counts),
            'max_agents': max(instance_counts, key=lambda x: x['agents'])['agents'] if instance_counts else 0,
            'min_agents': min(instance_counts, key=lambda x: x['agents'])['agents'] if instance_counts else 0
        }

    def aggregate_confidence_scores(self) -> Dict:
        """
        Aggregate confidence scores across all instances.

        Returns:
            Dictionary with:
            - avg_confidence: Weighted average confidence
            - instance_confidences: List of per-instance confidences
            - max_confidence: Highest confidence from any instance
            - min_confidence: Lowest confidence from any instance
        """
        # Scan for realtime metrics files
        pattern = "realtime_metrics_*.json"
        instance_files = self.scan_instance_files(pattern)

        confidences = []

        for file_path, age in instance_files:
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    conf = data.get('confidence')

                    # Parse confidence (could be string or number)
                    if conf and conf != '--':
                        if isinstance(conf, str):
                            conf = float(conf.rstrip('%'))
                        else:
                            conf = float(conf)

                        confidences.append({
                            'instance_id': self._extract_instance_id(file_path.name),
                            'confidence': conf,
                            'age_seconds': age
                        })
            except Exception:
                # Skip corrupted files or unparseable confidence
                continue

        # Calculate weighted average (weight by recency)
        if confidences:
            # Weight: newer files get higher weight
            total_weight = 0
            weighted_sum = 0

            for item in confidences:
                weight = 1.0 / (1.0 + item['age_seconds'] / 60.0)  # Decay over minutes
                weighted_sum += item['confidence'] * weight
                total_weight += weight

            avg_confidence = weighted_sum / total_weight if total_weight > 0 else 0
        else:
            avg_confidence = 0

        return {
            'avg_confidence': avg_confidence,
            'instance_confidences': confidences,
            'max_confidence': max(confidences, key=lambda x: x['confidence'])['confidence'] if confidences else 0,
            'min_confidence': min(confidences, key=lambda x: x['confidence'])['confidence'] if confidences else 0
        }

    def aggregate_state_persistence(self) -> Dict:
        """
        Aggregate state persistence metrics across all instances.

        Returns:
            Dictionary with:
            - active_instances: Number of instances in ACTIVE state
            - completing_instances: Number of instances in COMPLETING state
            - idle_instances: Number of instances in IDLE state
            - total_requests: Sum of request_count across all instances
        """
        # Scan for state files
        pattern = "statusline_state_*.json"
        instance_files = self.scan_instance_files(pattern)

        active_count = 0
        completing_count = 0
        idle_count = 0
        total_requests = 0

        states = []

        for file_path, age in instance_files:
            try:
                with open(file_path, 'r') as f:
                    fcntl.flock(f.fileno(), fcntl.LOCK_SH)
                    try:
                        state = json.load(f)
                    finally:
                        fcntl.flock(f.fileno(), fcntl.LOCK_UN)

                    lifecycle_state = state.get('lifecycle_state', 'unknown')

                    if lifecycle_state == 'active':
                        active_count += 1
                    elif lifecycle_state == 'completing':
                        completing_count += 1
                    elif lifecycle_state == 'idle':
                        idle_count += 1

                    total_requests += state.get('request_count', 0)

                    states.append({
                        'instance_id': self._extract_instance_id(file_path.name),
                        'lifecycle_state': lifecycle_state,
                        'executing': state.get('executing', False),
                        'agents': state.get('agents', 'N/A'),
                        'tokens_display': state.get('tokens_display', '0k/200k'),
                        'confidence': state.get('confidence', '--'),
                        'age_seconds': age
                    })
            except Exception:
                # Skip corrupted files
                continue

        return {
            'active_instances': active_count,
            'completing_instances': completing_count,
            'idle_instances': idle_count,
            'total_instances': len(states),
            'total_requests': total_requests,
            'instance_states': states
        }

    def aggregate_all(self) -> Dict:
        """
        Aggregate all metrics across all instances.

        Returns:
            Comprehensive dictionary with all aggregated metrics:
            - Agents (total, per-instance, min, max)
            - Confidence (avg, per-instance, min, max)
            - State (active/completing/idle counts)
            - Instance count
            - Timestamp
        """
        agents_data = self.aggregate_agent_counts()
        confidence_data = self.aggregate_confidence_scores()
        state_data = self.aggregate_state_persistence()

        return {
            # Agent metrics
            'total_agents': agents_data['total_agents'],
            'instance_count': agents_data['instance_count'],
            'max_agents': agents_data['max_agents'],
            'min_agents': agents_data['min_agents'],
            'agent_breakdown': agents_data['instance_counts'],

            # Confidence metrics
            'avg_confidence': confidence_data['avg_confidence'],
            'max_confidence': confidence_data['max_confidence'],
            'min_confidence': confidence_data['min_confidence'],
            'confidence_breakdown': confidence_data['instance_confidences'],

            # State metrics
            'active_instances': state_data['active_instances'],
            'completing_instances': state_data['completing_instances'],
            'idle_instances': state_data['idle_instances'],
            'total_instances': state_data['total_instances'],
            'total_requests': state_data['total_requests'],
            'state_breakdown': state_data['instance_states'],

            # Metadata
            'timestamp': datetime.now().isoformat(),
            'aggregation_method': 'file_scan'
        }

    def get_instance_metrics(self, instance_id: str) -> Optional[Dict]:
        """
        Get metrics for a specific instance.

        Args:
            instance_id: Instance ID to query

        Returns:
            Dictionary with instance metrics, or None if not found
        """
        all_metrics = self.aggregate_all()

        # Find instance in breakdowns
        instance_data = {
            'instance_id': instance_id,
            'agents': None,
            'confidence': None,
            'state': None
        }

        # Search agent breakdown
        for item in all_metrics['agent_breakdown']:
            if item['instance_id'] == instance_id:
                instance_data['agents'] = item['agents']
                break

        # Search confidence breakdown
        for item in all_metrics['confidence_breakdown']:
            if item['instance_id'] == instance_id:
                instance_data['confidence'] = item['confidence']
                break

        # Search state breakdown
        for item in all_metrics['state_breakdown']:
            if item['instance_id'] == instance_id:
                instance_data['state'] = item
                break

        # Return None if instance not found
        if instance_data['agents'] is None and instance_data['confidence'] is None:
            return None

        return instance_data

    def cleanup_stale_files(self, max_age_hours: int = 24) -> Dict:
        """
        Cleanup stale instance metric files.

        Args:
            max_age_hours: Maximum age in hours (default: 24)

        Returns:
            Dictionary with cleanup statistics
        """
        cutoff_time = time.time() - (max_age_hours * 3600)
        cleaned_count = 0
        cleaned_files = []

        patterns = [
            "agent_usage_counter_*.txt",
            "realtime_metrics_*.json",
            "statusline_state_*.json"
        ]

        for pattern in patterns:
            for file_path in self.tmp_dir.glob(pattern):
                try:
                    mtime = os.path.getmtime(file_path)
                    if mtime < cutoff_time:
                        file_path.unlink()
                        cleaned_count += 1
                        cleaned_files.append(str(file_path))
                except Exception:
                    # Skip files we can't delete
                    continue

        return {
            'cleaned_count': cleaned_count,
            'cleaned_files': cleaned_files,
            'max_age_hours': max_age_hours
        }

    def _extract_instance_id(self, filename: str) -> str:
        """
        Extract instance ID from filename.

        Args:
            filename: Filename (e.g., "agent_usage_counter_20251116_031234_a1b2c3d4.txt")

        Returns:
            Instance ID (e.g., "20251116_031234_a1b2c3d4")
        """
        # Remove file extension
        name_without_ext = Path(filename).stem

        # Split by last underscore groups (timestamp_pid_hash)
        parts = name_without_ext.split('_')

        # Instance ID is last 3 parts: YYYYMMDD_HHMMSS_hash
        if len(parts) >= 3:
            # Find where the timestamp starts (8 digits)
            for i in range(len(parts) - 2):
                if len(parts[i]) == 8 and parts[i].isdigit():
                    # Found timestamp, combine with next 2 parts
                    return '_'.join(parts[i:i+3])

        # Fallback: return everything after first underscore
        if '_' in name_without_ext:
            return name_without_ext.split('_', 1)[1]

        return "unknown"


def main():
    """CLI interface for testing."""
    import argparse

    parser = argparse.ArgumentParser(description='Metrics Aggregator')
    parser.add_argument('--all', action='store_true', help='Aggregate all metrics')
    parser.add_argument('--agents', action='store_true', help='Aggregate agent counts')
    parser.add_argument('--confidence', action='store_true', help='Aggregate confidence scores')
    parser.add_argument('--state', action='store_true', help='Aggregate state persistence')
    parser.add_argument('--instance', type=str, help='Get metrics for specific instance')
    parser.add_argument('--cleanup', action='store_true', help='Cleanup stale files')
    parser.add_argument('--max-age', type=int, default=24, help='Max age in hours for cleanup')
    parser.add_argument('--json', action='store_true', help='Output as JSON')

    args = parser.parse_args()

    aggregator = MetricsAggregator()

    if args.all:
        metrics = aggregator.aggregate_all()
        if args.json:
            print(json.dumps(metrics, indent=2))
        else:
            print(f"Total Agents: {metrics['total_agents']} across {metrics['instance_count']} instances")
            print(f"Average Confidence: {metrics['avg_confidence']:.1f}%")
            print(f"Active Instances: {metrics['active_instances']}")
            print(f"Total Requests Processed: {metrics['total_requests']}")

    elif args.agents:
        data = aggregator.aggregate_agent_counts()
        if args.json:
            print(json.dumps(data, indent=2))
        else:
            print(f"Total Agents: {data['total_agents']}")
            print(f"Instances: {data['instance_count']}")
            for item in data['instance_counts']:
                print(f"  - {item['instance_id']}: {item['agents']} agents")

    elif args.confidence:
        data = aggregator.aggregate_confidence_scores()
        if args.json:
            print(json.dumps(data, indent=2))
        else:
            print(f"Average Confidence: {data['avg_confidence']:.1f}%")
            for item in data['instance_confidences']:
                print(f"  - {item['instance_id']}: {item['confidence']:.1f}%")

    elif args.state:
        data = aggregator.aggregate_state_persistence()
        if args.json:
            print(json.dumps(data, indent=2))
        else:
            print(f"Active: {data['active_instances']}")
            print(f"Completing: {data['completing_instances']}")
            print(f"Idle: {data['idle_instances']}")
            print(f"Total Requests: {data['total_requests']}")

    elif args.instance:
        data = aggregator.get_instance_metrics(args.instance)
        if data:
            print(json.dumps(data, indent=2))
        else:
            print(f"Instance {args.instance} not found")

    elif args.cleanup:
        result = aggregator.cleanup_stale_files(max_age_hours=args.max_age)
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"Cleaned up {result['cleaned_count']} stale files")

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
