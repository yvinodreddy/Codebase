#!/usr/bin/env python3
"""
Task Archiver - Extract and store comprehensive task metadata

Extracts from completed cpp tasks:
- Original prompt
- Agent orchestration details
- ULTRATHINK stages
- Guardrail results
- Execution metrics
- Complete timeline
"""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


class TaskMetadataExtractor:
    """Extract comprehensive metadata from cpp task output files"""

    def __init__(self, output_file: Path):
        self.output_file = output_file
        self.metadata = {}

    def extract_all(self) -> Dict:
        """Extract all metadata from task file"""
        try:
            with open(self.output_file, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()

            self.metadata = {
                "task_id": self.output_file.stem,
                "output_file": str(self.output_file),
                "file_size_kb": round(self.output_file.stat().st_size / 1024, 1),
                "line_count": len(lines),
                "created_at": datetime.fromtimestamp(
                    self.output_file.stat().st_ctime
                ).isoformat(),
                "completed_at": datetime.fromtimestamp(
                    self.output_file.stat().st_mtime
                ).isoformat(),
                "prompt": self._extract_prompt(lines),
                "agents": self._extract_agents(lines),
                "stages": self._extract_stages(lines),
                "guardrails": self._extract_guardrails(lines),
                "context_usage": self._extract_context(lines),
                "execution_time": self._extract_execution_time(lines),
                "status": self._determine_status(lines),
                "errors": self._extract_errors(lines),
                "warnings": self._extract_warnings(lines),
                "summary": self._extract_summary(lines),
            }

            return self.metadata

        except Exception as e:
            return {
                "task_id": self.output_file.stem,
                "error": str(e),
                "status": "ERROR"
            }

    def _extract_prompt(self, lines: List[str]) -> str:
        """Extract the original prompt"""
        prompt_lines = []
        in_prompt = False

        for line in lines[:200]:  # Check first 200 lines
            if "Prompt:" in line or "📝 Prompt:" in line:
                in_prompt = True
                # Extract from same line
                if ":" in line:
                    prompt_text = line.split(":", 1)[1].strip()
                    if prompt_text:
                        prompt_lines.append(prompt_text)
                continue

            if in_prompt:
                if line.strip().startswith("===") or "⏱️" in line:
                    break
                if line.strip():
                    prompt_lines.append(line.strip())

        if prompt_lines:
            return " ".join(prompt_lines)[:500]  # First 500 chars
        return "Unknown"

    def _extract_agents(self, lines: List[str]) -> Dict:
        """Extract agent allocation and details"""
        agents = {
            "total_allocated": 0,
            "max_available": 500,
            "details": []
        }

        for i, line in enumerate(lines):
            # Find total agents allocated
            if "Agents to allocate:" in line or "Total Agents Allocated:" in line:
                match = re.search(r'(\d+)/(\d+)', line)
                if match:
                    agents["total_allocated"] = int(match.group(1))
                    agents["max_available"] = int(match.group(2))

            # Extract individual agent details
            if "Agent ID:" in line:
                agent_id_match = re.search(r'Agent ID:\s*(\S+)', line)
                if agent_id_match:
                    agent_id = agent_id_match.group(1)

                    # Look ahead for details
                    agent_info = {"id": agent_id}
                    for j in range(i+1, min(i+10, len(lines))):
                        next_line = lines[j]
                        if "Name:" in next_line:
                            agent_info["name"] = next_line.split("Name:")[-1].strip()[:50]
                        elif "Role:" in next_line:
                            agent_info["role"] = next_line.split("Role:")[-1].strip()[:80]
                        elif "Priority:" in next_line:
                            agent_info["priority"] = next_line.split("Priority:")[-1].strip()

                    agents["details"].append(agent_info)

        return agents

    def _extract_stages(self, lines: List[str]) -> List[Dict]:
        """Extract ULTRATHINK stages completed"""
        stages = []

        for line in lines:
            if "[VERBOSE] STAGE" in line:
                match = re.search(r'STAGE\s*(\d+):\s*(.+)', line)
                if match:
                    stage_num = int(match.group(1))
                    stage_name = match.group(2).strip()

                    # Avoid duplicates
                    if not any(s["number"] == stage_num for s in stages):
                        stages.append({
                            "number": stage_num,
                            "name": stage_name[:100]
                        })

        return sorted(stages, key=lambda x: x["number"])

    def _extract_guardrails(self, lines: List[str]) -> Dict:
        """Extract guardrail validation results"""
        guardrails = {
            "total_layers": 0,
            "layers": []
        }

        for i, line in enumerate(lines):
            if "Layer" in line and ("PASS" in line or "FAIL" in line):
                match = re.search(r'Layer\s*(\d+)', line)
                if match:
                    layer_num = int(match.group(1))
                    status = "PASS" if "PASS" in line else "FAIL"

                    # Extract layer name
                    name_match = re.search(r'Layer\s*\d+:\s*(.+?)(?:─|PASS|FAIL)', line)
                    layer_name = name_match.group(1).strip() if name_match else "Unknown"

                    # Avoid duplicates
                    if not any(l["number"] == layer_num for l in guardrails["layers"]):
                        guardrails["layers"].append({
                            "number": layer_num,
                            "name": layer_name[:50],
                            "status": status
                        })

        guardrails["total_layers"] = len(guardrails["layers"])
        guardrails["layers"] = sorted(guardrails["layers"], key=lambda x: x["number"])

        return guardrails

    def _extract_context(self, lines: List[str]) -> Dict:
        """Extract context window usage"""
        context = {
            "used_tokens": 0,
            "max_tokens": 200000,
            "percentage": 0.0
        }

        for line in lines[:500]:
            if "Estimated usage" in line or "tokens" in line.lower():
                match = re.search(r'(\d+)[,\s]*tokens', line)
                if match:
                    context["used_tokens"] = int(match.group(1))
                    context["percentage"] = round(
                        (context["used_tokens"] / context["max_tokens"]) * 100, 2
                    )
                    break

        return context

    def _extract_execution_time(self, lines: List[str]) -> Dict:
        """Extract execution timing information"""
        timing = {
            "started_at": None,
            "completed_at": None,
            "duration_seconds": 0
        }

        for line in lines[:100]:
            if "⏱️  Started:" in line or "Started:" in line:
                # Extract timestamp
                match = re.search(r'(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})', line)
                if match:
                    timing["started_at"] = match.group(1)

        for line in reversed(lines[-100:]):
            if "completed" in line.lower() and any(x in line for x in ["Stage", "STAGE", "✓"]):
                # Found completion indicator
                match = re.search(r'(\d+\.\d+)s', line)
                if match:
                    timing["duration_seconds"] = float(match.group(1))
                    break

        return timing

    def _determine_status(self, lines: List[str]) -> str:
        """Determine task completion status"""
        recent = lines[-100:] if len(lines) > 100 else lines

        # Check for completion markers
        for line in reversed(recent):
            if "THE ANSWER ENDS HERE" in line or "ANSWER ENDS HERE" in line:
                return "COMPLETED"
            if "COMPLETE" in line.upper() and "TRACK" in line.upper():
                return "COMPLETED"

        # Check for errors
        error_count = sum(1 for line in recent if "ERROR" in line.upper() or "FAILED" in line.upper())
        if error_count > 5:
            return "FAILED"

        return "UNKNOWN"

    def _extract_errors(self, lines: List[str]) -> List[str]:
        """Extract error messages"""
        errors = []
        for line in lines[-200:]:  # Last 200 lines
            if "ERROR" in line.upper() or "FAIL" in line.upper():
                error_text = line.strip()[:150]
                if error_text and error_text not in errors:
                    errors.append(error_text)

        return errors[-10:]  # Last 10 errors

    def _extract_warnings(self, lines: List[str]) -> List[str]:
        """Extract warning messages"""
        warnings = []
        for line in lines[-200:]:
            if "WARNING" in line.upper() or "WARN" in line.upper():
                warning_text = line.strip()[:150]
                if warning_text and warning_text not in warnings:
                    warnings.append(warning_text)

        return warnings[-10:]  # Last 10 warnings

    def _extract_summary(self, lines: List[str]) -> str:
        """Extract task summary from answer section"""
        summary_lines = []
        in_summary = False

        for line in reversed(lines[-200:]):
            if "SUMMARY" in line.upper() or "Executive Summary" in line:
                in_summary = True
                continue

            if in_summary:
                if line.strip().startswith("===") or line.strip().startswith("##"):
                    break
                if line.strip() and not line.strip().startswith("🔥"):
                    summary_lines.insert(0, line.strip())

        if summary_lines:
            return " ".join(summary_lines[:3])[:300]  # First 300 chars
        return ""


class TaskArchiveManager:
    """Manage task archive storage and retrieval"""

    def __init__(self, archive_dir: Path):
        self.archive_dir = archive_dir
        self.archive_dir.mkdir(exist_ok=True)
        self.archive_file = archive_dir / "tasks.json"
        self.tasks = self._load_archive()

    def _load_archive(self) -> Dict:
        """Load existing archive"""
        if self.archive_file.exists():
            try:
                with open(self.archive_file, 'r') as f:
                    return json.load(f)
            except Exception:
                return {"tasks": [], "last_updated": None}
        return {"tasks": [], "last_updated": None}

    def _save_archive(self):
        """Save archive to disk"""
        self.tasks["last_updated"] = datetime.now().isoformat()
        with open(self.archive_file, 'w') as f:
            json.dump(self.tasks, f, indent=2)

    def archive_task(self, task_metadata: Dict) -> bool:
        """Add task to archive"""
        try:
            # Check if already archived
            task_id = task_metadata.get("task_id")
            if any(t.get("task_id") == task_id for t in self.tasks["tasks"]):
                # Update existing
                for i, t in enumerate(self.tasks["tasks"]):
                    if t.get("task_id") == task_id:
                        self.tasks["tasks"][i] = task_metadata
                        break
            else:
                # Add new
                self.tasks["tasks"].append(task_metadata)

            # Sort by completion time (newest first)
            self.tasks["tasks"].sort(
                key=lambda x: x.get("completed_at", ""),
                reverse=True
            )

            self._save_archive()
            return True

        except Exception as e:
            print(f"Error archiving task: {e}")
            return False

    def get_archived_tasks(self) -> List[Dict]:
        """Get all archived tasks"""
        return self.tasks["tasks"]

    def get_task_by_id(self, task_id: str) -> Optional[Dict]:
        """Get specific task by ID"""
        for task in self.tasks["tasks"]:
            if task.get("task_id") == task_id:
                return task
        return None

    def get_tasks_by_status(self, status: str) -> List[Dict]:
        """Get tasks filtered by status"""
        return [
            task for task in self.tasks["tasks"]
            if task.get("status") == status
        ]


# CLI for testing
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python3 task_archiver.py <output_file.txt>")
        sys.exit(1)

    output_file = Path(sys.argv[1])
    if not output_file.exists():
        print(f"Error: File not found: {output_file}")
        sys.exit(1)

    # Extract metadata
    extractor = TaskMetadataExtractor(output_file)
    metadata = extractor.extract_all()

    # Pretty print
    print(json.dumps(metadata, indent=2))

    # Archive it
    archive_dir = Path(__file__).parent / "archive"
    archiver = TaskArchiveManager(archive_dir)
    archiver.archive_task(metadata)
    print(f"\n✅ Task archived successfully!")
