#!/usr/bin/env python3
"""
instance_id_manager.py - Instance Isolation and ID Management

PRODUCTION-READY IMPLEMENTATION (2025-11-16)
============================================

PURPOSE:
- Generate unique instance IDs for each Claude Code window/session
- Register and track active instances across the system
- Provide cleanup mechanisms for stale instances
- Enable per-instance resource tracking and isolation

FEATURES:
- ✅ Unique ID generation (timestamp + PID + random hash)
- ✅ Instance lock file management
- ✅ Automatic stale instance cleanup
- ✅ Thread-safe operations with file locking
- ✅ Singleton pattern for consistent ID within process
- ✅ Environment variable override for testing
- ✅ Zero breaking changes - backward compatible

USAGE:
    from instance_id_manager import InstanceIDManager

    # Get singleton instance
    manager = InstanceIDManager.get_instance()

    # Get current instance ID (auto-generates if needed)
    instance_id = manager.get_instance_id()

    # List all active instances
    active = manager.list_active_instances()

    # Cleanup on exit
    manager.cleanup()

INSTANCE ID FORMAT:
    Format: {timestamp}_{pid}_{random_hash}
    Example: 20251116_031234_a1b2c3d4

    Components:
    - timestamp: YYYYMMDD_HHMMSS for chronological sorting
    - pid: Process ID for uniqueness
    - random_hash: 8-char hex for collision prevention
"""

import os
import sys
import time
import fcntl
import hashlib
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional, Dict
import atexit


class InstanceIDManager:
    """
    Singleton manager for instance ID generation and tracking.

    Manages instance lifecycle:
    1. Generate unique ID on first access
    2. Create lock file to register instance
    3. Track all active instances
    4. Cleanup stale instances (>1 hour inactive)
    5. Remove lock file on exit
    """

    _instance = None
    _instance_id = None
    _lock_dir = None
    _lock_file = None
    _registered = False

    def __init__(self, lock_dir: Optional[str] = None):
        """
        Initialize instance manager.

        Args:
            lock_dir: Directory for instance lock files
                     (default: /home/user01/claude-test/ClaudePrompt/tmp/instances/)
        """
        if lock_dir is None:
            lock_dir = "/home/user01/claude-test/ClaudePrompt/tmp/instances"

        self._lock_dir = Path(lock_dir)
        self._lock_dir.mkdir(parents=True, exist_ok=True)

        # Register cleanup on exit
        atexit.register(self.cleanup)

    @classmethod
    def get_instance(cls, lock_dir: Optional[str] = None) -> 'InstanceIDManager':
        """
        Get singleton instance of manager.

        Args:
            lock_dir: Optional lock directory override

        Returns:
            Singleton InstanceIDManager instance
        """
        if cls._instance is None:
            cls._instance = cls(lock_dir)
        return cls._instance

    def generate_instance_id(self) -> str:
        """
        Generate unique instance ID.

        Format: {timestamp}_{pid}_{random_hash}

        Components:
        - timestamp: YYYYMMDD_HHMMSS for chronological sorting
        - pid: Process ID for uniqueness
        - random_hash: 8-char hex for collision prevention

        Returns:
            Unique instance ID string
        """
        # Check for environment variable override (for testing)
        if 'ULTRATHINK_INSTANCE_ID' in os.environ:
            return os.environ['ULTRATHINK_INSTANCE_ID']

        # Generate timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Get process ID
        pid = os.getpid()

        # Generate random hash (8 chars)
        random_data = f"{timestamp}_{pid}_{time.time()}_{os.urandom(16).hex()}"
        random_hash = hashlib.sha256(random_data.encode()).hexdigest()[:8]

        # Combine components
        instance_id = f"{timestamp}_{pid}_{random_hash}"

        return instance_id

    def get_instance_id(self, auto_register: bool = True) -> str:
        """
        Get current instance ID (generates if not exists).

        Args:
            auto_register: Automatically register instance with lock file

        Returns:
            Current instance ID
        """
        if self._instance_id is None:
            self._instance_id = self.generate_instance_id()

            if auto_register:
                self.register_instance()

        return self._instance_id

    def register_instance(self, metadata: Optional[Dict] = None) -> bool:
        """
        Register instance by creating lock file.

        Lock file contains:
        - instance_id
        - pid
        - start_time
        - last_heartbeat
        - metadata (optional)

        Args:
            metadata: Optional metadata to store (e.g., task description)

        Returns:
            True if registration successful
        """
        if self._registered:
            # Already registered - update heartbeat
            return self.update_heartbeat()

        instance_id = self.get_instance_id(auto_register=False)
        self._lock_file = self._lock_dir / f"instance_{instance_id}.lock"

        try:
            # Create lock file with metadata
            lock_data = {
                'instance_id': instance_id,
                'pid': os.getpid(),
                'start_time': datetime.now().isoformat(),
                'last_heartbeat': datetime.now().isoformat(),
                'metadata': metadata or {}
            }

            with open(self._lock_file, 'w') as f:
                # Acquire exclusive lock
                fcntl.flock(f.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                try:
                    json.dump(lock_data, f, indent=2)
                    f.flush()
                    os.fsync(f.fileno())
                finally:
                    fcntl.flock(f.fileno(), fcntl.LOCK_UN)

            self._registered = True
            return True

        except IOError:
            # Lock file already exists (shouldn't happen with unique ID)
            return False

    def update_heartbeat(self) -> bool:
        """
        Update heartbeat timestamp in lock file.

        Call this periodically (e.g., every 30 seconds) to keep instance alive.

        Returns:
            True if update successful
        """
        if not self._registered or self._lock_file is None:
            return False

        try:
            # Read current lock data
            with open(self._lock_file, 'r') as f:
                fcntl.flock(f.fileno(), fcntl.LOCK_SH)
                try:
                    lock_data = json.load(f)
                finally:
                    fcntl.flock(f.fileno(), fcntl.LOCK_UN)

            # Update heartbeat
            lock_data['last_heartbeat'] = datetime.now().isoformat()

            # Write back
            with open(self._lock_file, 'w') as f:
                fcntl.flock(f.fileno(), fcntl.LOCK_EX)
                try:
                    json.dump(lock_data, f, indent=2)
                    f.flush()
                    os.fsync(f.fileno())
                finally:
                    fcntl.flock(f.fileno(), fcntl.LOCK_UN)

            return True

        except Exception:
            return False

    def list_active_instances(self, max_age_seconds: int = 3600) -> List[Dict]:
        """
        List all active instances (with recent heartbeats).

        Args:
            max_age_seconds: Maximum age for heartbeat (default: 3600 = 1 hour)

        Returns:
            List of active instance metadata dicts
        """
        active_instances = []
        cutoff_time = datetime.now() - timedelta(seconds=max_age_seconds)

        # Scan all lock files
        for lock_file in self._lock_dir.glob("instance_*.lock"):
            try:
                with open(lock_file, 'r') as f:
                    fcntl.flock(f.fileno(), fcntl.LOCK_SH)
                    try:
                        lock_data = json.load(f)
                    finally:
                        fcntl.flock(f.fileno(), fcntl.LOCK_UN)

                # Parse heartbeat time
                heartbeat_str = lock_data.get('last_heartbeat')
                if heartbeat_str:
                    heartbeat_time = datetime.fromisoformat(heartbeat_str)

                    # Check if recent enough
                    if heartbeat_time >= cutoff_time:
                        active_instances.append(lock_data)

            except Exception:
                # Skip corrupted lock files
                continue

        return active_instances

    def cleanup_stale_instances(self, max_age_seconds: int = 3600) -> int:
        """
        Cleanup stale instance lock files.

        Removes lock files with old heartbeats or non-existent PIDs.

        Args:
            max_age_seconds: Maximum age for heartbeat (default: 3600 = 1 hour)

        Returns:
            Number of stale instances cleaned up
        """
        cleaned_count = 0
        cutoff_time = datetime.now() - timedelta(seconds=max_age_seconds)

        for lock_file in self._lock_dir.glob("instance_*.lock"):
            try:
                with open(lock_file, 'r') as f:
                    fcntl.flock(f.fileno(), fcntl.LOCK_SH)
                    try:
                        lock_data = json.load(f)
                    finally:
                        fcntl.flock(f.fileno(), fcntl.LOCK_UN)

                # Check heartbeat age
                heartbeat_str = lock_data.get('last_heartbeat')
                is_stale = False

                if heartbeat_str:
                    heartbeat_time = datetime.fromisoformat(heartbeat_str)
                    if heartbeat_time < cutoff_time:
                        is_stale = True
                else:
                    is_stale = True

                # Check if process still exists
                pid = lock_data.get('pid')
                if pid:
                    try:
                        # Check if process exists (send signal 0)
                        os.kill(pid, 0)
                    except OSError:
                        # Process doesn't exist
                        is_stale = True

                # Remove if stale
                if is_stale:
                    lock_file.unlink()
                    cleaned_count += 1

            except Exception:
                # Try to remove corrupted files
                try:
                    lock_file.unlink()
                    cleaned_count += 1
                except:
                    pass

        return cleaned_count

    def cleanup(self) -> bool:
        """
        Cleanup current instance (remove lock file).

        Called automatically on exit via atexit.

        Returns:
            True if cleanup successful
        """
        if not self._registered or self._lock_file is None:
            return False

        try:
            if self._lock_file.exists():
                self._lock_file.unlink()
            self._registered = False
            return True
        except Exception:
            return False

    def get_instance_file_path(self, base_name: str, extension: str = ".txt") -> Path:
        """
        Get per-instance file path.

        Converts shared file name to per-instance file name.

        Args:
            base_name: Base file name (e.g., "agent_usage_counter")
            extension: File extension (default: ".txt")

        Returns:
            Path to per-instance file

        Example:
            get_instance_file_path("agent_usage_counter", ".txt")
            → /path/to/agent_usage_counter_20251116_031234_a1b2c3d4.txt
        """
        instance_id = self.get_instance_id()
        instance_file = f"{base_name}_{instance_id}{extension}"
        return self._lock_dir.parent / instance_file

    def get_all_instance_files(self, base_name: str, extension: str = ".txt") -> List[Path]:
        """
        Get all instance files matching pattern.

        Args:
            base_name: Base file name (e.g., "agent_usage_counter")
            extension: File extension (default: ".txt")

        Returns:
            List of paths to instance files

        Example:
            get_all_instance_files("agent_usage_counter", ".txt")
            → [agent_usage_counter_inst1.txt, agent_usage_counter_inst2.txt, ...]
        """
        pattern = f"{base_name}_*{extension}"
        instance_dir = self._lock_dir.parent
        return list(instance_dir.glob(pattern))


def main():
    """CLI interface for testing."""
    import argparse

    parser = argparse.ArgumentParser(description='Instance ID Manager')
    parser.add_argument('--generate', action='store_true', help='Generate new instance ID')
    parser.add_argument('--get', action='store_true', help='Get current instance ID')
    parser.add_argument('--register', action='store_true', help='Register instance')
    parser.add_argument('--list', action='store_true', help='List active instances')
    parser.add_argument('--cleanup', action='store_true', help='Cleanup stale instances')
    parser.add_argument('--file-path', type=str, help='Get per-instance file path')
    parser.add_argument('--json', action='store_true', help='Output as JSON')

    args = parser.parse_args()

    manager = InstanceIDManager.get_instance()

    if args.generate:
        instance_id = manager.generate_instance_id()
        if args.json:
            print(json.dumps({'instance_id': instance_id}))
        else:
            print(f"Generated ID: {instance_id}")

    elif args.get:
        instance_id = manager.get_instance_id()
        if args.json:
            print(json.dumps({'instance_id': instance_id}))
        else:
            print(f"Current ID: {instance_id}")

    elif args.register:
        success = manager.register_instance()
        if args.json:
            print(json.dumps({'registered': success}))
        else:
            print(f"Registration: {'✅ SUCCESS' if success else '❌ FAILED'}")

    elif args.list:
        instances = manager.list_active_instances()
        if args.json:
            print(json.dumps({'count': len(instances), 'instances': instances}, indent=2))
        else:
            print(f"Active Instances: {len(instances)}")
            for inst in instances:
                print(f"  - {inst['instance_id']} (PID: {inst['pid']})")

    elif args.cleanup:
        count = manager.cleanup_stale_instances()
        if args.json:
            print(json.dumps({'cleaned': count}))
        else:
            print(f"Cleaned up {count} stale instances")

    elif args.file_path:
        path = manager.get_instance_file_path(args.file_path)
        if args.json:
            print(json.dumps({'path': str(path)}))
        else:
            print(f"Instance file: {path}")

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
