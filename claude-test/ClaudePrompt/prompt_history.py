#!/usr/bin/env python3
"""
Prompt History Manager
Tracks all ultrathinkc prompts with unlimited storage capacity
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional


class PromptHistoryManager:
    """
    Manages prompt history with unlimited storage.
    All prompts are saved with metadata for easy retrieval and reuse.
    """

    def __init__(self, history_file: Optional[str] = None):
        """
        Initialize the prompt history manager

        Args:
            history_file: Path to history JSON file. Defaults to logs/prompt_history.json
        """
        if history_file is None:
            script_dir = Path(__file__).parent
            logs_dir = script_dir / "logs"
            logs_dir.mkdir(exist_ok=True)
            history_file = logs_dir / "prompt_history.json"

        self.history_file = Path(history_file)
        self._ensure_history_file()

    def _ensure_history_file(self):
        """Ensure history file exists with valid JSON"""
        if not self.history_file.exists():
            self._save_history([])
        else:
            # Validate JSON format
            try:
                self._load_history()
            except (json.JSONDecodeError, ValueError):
                # If corrupted, backup and create new
                if self.history_file.stat().st_size > 0:
                    backup_file = self.history_file.with_suffix('.json.backup')
                    self.history_file.rename(backup_file)
                self._save_history([])

    def _load_history(self) -> List[Dict[str, Any]]:
        """Load history from JSON file"""
        try:
            with open(self.history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _save_history(self, history: List[Dict[str, Any]]):
        """Save history to JSON file"""
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2, ensure_ascii=False)

    def add_prompt(
        self,
        prompt: str,
        complexity: str,
        agents_allocated: int,
        mode: str,
        duration_seconds: float = 0.0,
        success: bool = True,
        verbose: bool = False,
        quiet: bool = False,
        additional_metadata: Optional[Dict[str, Any]] = None
    ) -> int:
        """
        Add a prompt to history

        Args:
            prompt: The prompt text
            complexity: SIMPLE, MODERATE, or COMPLEX
            agents_allocated: Number of agents used
            mode: claude_code or api
            duration_seconds: How long it took to process
            success: Whether it completed successfully
            verbose: Whether --verbose was used
            quiet: Whether --quiet was used
            additional_metadata: Any other metadata to store

        Returns:
            The ID of the saved prompt entry
        """
        history = self._load_history()

        # Calculate next ID (1-based)
        next_id = 1 if not history else max(entry['id'] for entry in history) + 1

        entry = {
            'id': next_id,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'prompt': prompt,
            'complexity': complexity,
            'agents_allocated': agents_allocated,
            'mode': mode,
            'duration_seconds': round(duration_seconds, 3),
            'success': success,
            'flags': {
                'verbose': verbose,
                'quiet': quiet
            }
        }

        # Add any additional metadata
        if additional_metadata:
            entry['metadata'] = additional_metadata

        history.append(entry)
        self._save_history(history)

        return next_id

    def get_all(self, limit: Optional[int] = None, offset: int = 0) -> List[Dict[str, Any]]:
        """
        Get all prompts from history

        Args:
            limit: Maximum number of entries to return (None = unlimited)
            offset: Number of entries to skip from the beginning

        Returns:
            List of prompt history entries (newest first)
        """
        history = self._load_history()
        # Reverse to show newest first
        history = list(reversed(history))

        if offset > 0:
            history = history[offset:]

        if limit is not None:
            history = history[:limit]

        return history

    def get_by_id(self, prompt_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a specific prompt by ID

        Args:
            prompt_id: The prompt ID to retrieve

        Returns:
            The prompt entry or None if not found
        """
        history = self._load_history()
        for entry in history:
            if entry['id'] == prompt_id:
                return entry
        return None

    def search(
        self,
        query: str,
        search_in: str = 'prompt',
        case_sensitive: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Search prompts by keyword

        Args:
            query: Search query string
            search_in: Field to search in ('prompt', 'complexity', 'mode', or 'all')
            case_sensitive: Whether search should be case-sensitive

        Returns:
            List of matching prompt entries (newest first)
        """
        history = self._load_history()

        if not case_sensitive:
            query = query.lower()

        matches = []
        for entry in history:
            found = False

            if search_in in ('prompt', 'all'):
                text = entry['prompt'] if case_sensitive else entry['prompt'].lower()
                if query in text:
                    found = True

            if search_in in ('complexity', 'all'):
                text = entry['complexity'] if case_sensitive else entry['complexity'].lower()
                if query in text:
                    found = True

            if search_in in ('mode', 'all'):
                text = entry['mode'] if case_sensitive else entry['mode'].lower()
                if query in text:
                    found = True

            if found:
                matches.append(entry)

        # Return newest first
        return list(reversed(matches))

    def get_by_date(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get prompts within a date range

        Args:
            start_date: Start date in YYYY-MM-DD format (inclusive)
            end_date: End date in YYYY-MM-DD format (inclusive)

        Returns:
            List of matching prompt entries (newest first)
        """
        history = self._load_history()

        matches = []
        for entry in history:
            entry_date = entry['timestamp'].split(' ')[0]  # Extract YYYY-MM-DD

            if start_date and entry_date < start_date:
                continue
            if end_date and entry_date > end_date:
                continue

            matches.append(entry)

        return list(reversed(matches))

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about prompt history

        Returns:
            Dictionary with various statistics
        """
        history = self._load_history()

        if not history:
            return {
                'total_prompts': 0,
                'total_successful': 0,
                'total_failed': 0,
                'avg_duration_seconds': 0,
                'complexity_breakdown': {},
                'mode_breakdown': {},
                'agents_stats': {}
            }

        total = len(history)
        successful = sum(1 for entry in history if entry.get('success', True))
        failed = total - successful

        durations = [entry.get('duration_seconds', 0) for entry in history]
        avg_duration = sum(durations) / len(durations) if durations else 0

        # Complexity breakdown
        complexity_counts = {}
        for entry in history:
            complexity = entry.get('complexity', 'UNKNOWN')
            complexity_counts[complexity] = complexity_counts.get(complexity, 0) + 1

        # Mode breakdown
        mode_counts = {}
        for entry in history:
            mode = entry.get('mode', 'unknown')
            mode_counts[mode] = mode_counts.get(mode, 0) + 1

        # Agent statistics
        agent_counts = [entry.get('agents_allocated', 0) for entry in history]
        agents_stats = {
            'min': min(agent_counts) if agent_counts else 0,
            'max': max(agent_counts) if agent_counts else 0,
            'avg': sum(agent_counts) / len(agent_counts) if agent_counts else 0
        }

        return {
            'total_prompts': total,
            'total_successful': successful,
            'total_failed': failed,
            'success_rate': (successful / total * 100) if total > 0 else 0,
            'avg_duration_seconds': round(avg_duration, 3),
            'complexity_breakdown': complexity_counts,
            'mode_breakdown': mode_counts,
            'agents_stats': agents_stats
        }

    def clear_history(self, confirm: bool = False) -> bool:
        """
        Clear all history (requires confirmation)

        Args:
            confirm: Must be True to actually clear history

        Returns:
            True if history was cleared, False otherwise
        """
        if not confirm:
            return False

        # Backup before clearing
        if self.history_file.exists() and self.history_file.stat().st_size > 0:
            backup_file = self.history_file.with_suffix(
                f'.json.backup.{datetime.now().strftime("%Y%m%d_%H%M%S")}'
            )
            import shutil
            shutil.copy2(self.history_file, backup_file)

        self._save_history([])
        return True

    def export_to_file(self, output_file: str, format: str = 'json') -> bool:
        """
        Export history to a file

        Args:
            output_file: Path to output file
            format: Export format ('json', 'csv', or 'txt')

        Returns:
            True if export succeeded
        """
        history = self._load_history()
        output_path = Path(output_file)

        try:
            if format == 'json':
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(history, f, indent=2, ensure_ascii=False)

            elif format == 'csv':
                import csv
                with open(output_path, 'w', encoding='utf-8', newline='') as f:
                    if not history:
                        return True

                    writer = csv.DictWriter(
                        f,
                        fieldnames=['id', 'timestamp', 'prompt', 'complexity',
                                   'agents_allocated', 'mode', 'duration_seconds', 'success']
                    )
                    writer.writeheader()
                    for entry in history:
                        writer.writerow({
                            'id': entry['id'],
                            'timestamp': entry['timestamp'],
                            'prompt': entry['prompt'][:100] + '...' if len(entry['prompt']) > 100 else entry['prompt'],
                            'complexity': entry['complexity'],
                            'agents_allocated': entry['agents_allocated'],
                            'mode': entry['mode'],
                            'duration_seconds': entry['duration_seconds'],
                            'success': entry['success']
                        })

            elif format == 'txt':
                with open(output_path, 'w', encoding='utf-8') as f:
                    for entry in history:
                        f.write(f"ID: {entry['id']}\n")
                        f.write(f"Date: {entry['timestamp']}\n")
                        f.write(f"Prompt: {entry['prompt']}\n")
                        f.write(f"Complexity: {entry['complexity']}\n")
                        f.write(f"Agents: {entry['agents_allocated']}\n")
                        f.write(f"Mode: {entry['mode']}\n")
                        f.write(f"Duration: {entry['duration_seconds']}s\n")
                        f.write(f"Success: {entry['success']}\n")
                        f.write('-' * 80 + '\n\n')

            return True

        except Exception as e:
            print(f"Error exporting history: {e}")
            return False


def format_history_entry(entry: Dict[str, Any], show_full_prompt: bool = False) -> str:
    """
    Format a single history entry for display

    Args:
        entry: The history entry
        show_full_prompt: Whether to show the full prompt text

    Returns:
        Formatted string
    """
    prompt = entry['prompt']
    if not show_full_prompt and len(prompt) > 80:
        prompt = prompt[:77] + '...'

    # Format flags
    flags = []
    if entry.get('flags', {}).get('verbose'):
        flags.append('--verbose')
    if entry.get('flags', {}).get('quiet'):
        flags.append('--quiet')

    flags_str = ' ' + ' '.join(flags) if flags else ''

    return f"""
┌─────────────────────────────────────────────────────────────────┐
│ ID: {entry['id']:<10} Date: {entry['timestamp']:<30} │
├─────────────────────────────────────────────────────────────────┤
│ Prompt: {prompt:<56} │
├─────────────────────────────────────────────────────────────────┤
│ Complexity: {entry['complexity']:<15} Agents: {entry['agents_allocated']:<3} Mode: {entry['mode']:<12} │
│ Duration: {entry['duration_seconds']:.3f}s       Success: {'✅ Yes' if entry['success'] else '❌ No':<14} │
│ Flags: {flags_str:<57} │
└─────────────────────────────────────────────────────────────────┘
"""


if __name__ == "__main__":
    # Test the prompt history manager
    manager = PromptHistoryManager()

    # Add some test prompts
    print("Testing Prompt History Manager...")

    id1 = manager.add_prompt(
        prompt="What is 2+2?",
        complexity="SIMPLE",
        agents_allocated=8,
        mode="claude_code",
        duration_seconds=1.2,
        verbose=True
    )
    print(f"Added prompt with ID: {id1}")

    id2 = manager.add_prompt(
        prompt="Analyze the entire codebase for security vulnerabilities",
        complexity="COMPLEX",
        agents_allocated=25,
        mode="claude_code",
        duration_seconds=5.8,
        verbose=True
    )
    print(f"Added prompt with ID: {id2}")

    # Get all prompts
    print("\nAll prompts:")
    for entry in manager.get_all():
        print(format_history_entry(entry))

    # Get statistics
    print("\nStatistics:")
    stats = manager.get_statistics()
    print(f"Total prompts: {stats['total_prompts']}")
    print(f"Success rate: {stats['success_rate']:.1f}%")
    print(f"Average duration: {stats['avg_duration_seconds']}s")
    print(f"Complexity breakdown: {stats['complexity_breakdown']}")
