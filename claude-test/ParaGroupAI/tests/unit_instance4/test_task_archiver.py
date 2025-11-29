#!/usr/bin/env python3
"""Comprehensive test suite for task_archiver.py - Target: 90%+ coverage"""
import pytest
import json
import tempfile
import shutil
from pathlib import Path
from datetime import datetime
from unittest.mock import Mock, patch, MagicMock
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from task_archiver import TaskMetadataExtractor, TaskArchiveManager

class TestTaskMetadataExtractor:
    def setup_method(self):
        self.temp_file = tempfile.mktemp(suffix='_output.txt')
        self.create_test_output_file()
        self.extractor = TaskMetadataExtractor(Path(self.temp_file))

    def teardown_method(self):
        if Path(self.temp_file).exists():
            Path(self.temp_file).unlink()

    def create_test_output_file(self):
        content = """📝 Prompt: What is 2+2?
[VERBOSE] STAGE 1: Input Analysis
[VERBOSE] STAGE 2: Guardrails - Input Validation
[VERBOSE] Layer 1: Content Filter ─────── ✅ PASS
[VERBOSE] Layer 2: Security Check ─────── ✅ PASS
Agents to allocate: 25/500
Agent ID: agent_001
  Name: TestAgent
  Role: Calculator
  Priority: High
Estimated usage: 1500 tokens
⏱️  Started: 2025-11-22 10:00:00
[VERBOSE]   ✓ STAGE 1 completed in 0.5s
[ERROR] Something went wrong
[WARNING] Low memory
THE ANSWER ENDS HERE
"""
        with open(self.temp_file, 'w') as f:
            f.write(content)

    def test_initialization(self):
        assert self.extractor.output_file == Path(self.temp_file)
        assert self.extractor.metadata == {}

    def test_extract_all(self):
        metadata = self.extractor.extract_all()

        assert metadata['task_id'] == Path(self.temp_file).stem
        assert metadata['prompt'] == "What is 2+2?"
        assert metadata['agents']['total_allocated'] == 25
        assert len(metadata['stages']) > 0
        assert len(metadata['guardrails']['layers']) > 0
        assert metadata['status'] == "COMPLETED"

    def test_extract_prompt(self):
        with open(self.temp_file) as f:
            lines = f.readlines()

        prompt = self.extractor._extract_prompt(lines)
        assert prompt == "What is 2+2?"

    def test_extract_agents(self):
        with open(self.temp_file) as f:
            lines = f.readlines()

        agents = self.extractor._extract_agents(lines)
        assert agents['total_allocated'] == 25
        assert agents['max_available'] == 500
        assert len(agents['details']) > 0

    def test_extract_stages(self):
        with open(self.temp_file) as f:
            lines = f.readlines()

        stages = self.extractor._extract_stages(lines)
        assert len(stages) == 2
        assert stages[0]['number'] == 1

    def test_extract_guardrails(self):
        with open(self.temp_file) as f:
            lines = f.readlines()

        guardrails = self.extractor._extract_guardrails(lines)
        assert guardrails['total_layers'] == 2
        assert guardrails['layers'][0]['status'] == 'PASS'

    def test_extract_context(self):
        with open(self.temp_file) as f:
            lines = f.readlines()

        context = self.extractor._extract_context(lines)
        assert context['used_tokens'] == 1500

    def test_determine_status_completed(self):
        with open(self.temp_file) as f:
            lines = f.readlines()

        status = self.extractor._determine_status(lines)
        assert status == "COMPLETED"

    def test_extract_errors(self):
        with open(self.temp_file) as f:
            lines = f.readlines()

        errors = self.extractor._extract_errors(lines)
        assert len(errors) > 0
        assert any("ERROR" in e for e in errors)

    def test_extract_warnings(self):
        with open(self.temp_file) as f:
            lines = f.readlines()

        warnings = self.extractor._extract_warnings(lines)
        assert len(warnings) > 0
        assert any("WARNING" in w for w in warnings)

    @patch('builtins.open', side_effect=Exception("Read error"))
    def test_extract_all_error(self, mock_open):
        extractor = TaskMetadataExtractor(Path("test.txt"))
        metadata = extractor.extract_all()

        assert metadata['status'] == "ERROR"
        assert 'error' in metadata


class TestTaskArchiveManager:
    def setup_method(self):
        self.temp_dir = tempfile.mkdtemp()
        self.archive_dir = Path(self.temp_dir) / "archive"
        self.manager = TaskArchiveManager(self.archive_dir)

    def teardown_method(self):
        if Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)

    def test_initialization(self):
        assert self.manager.archive_dir == self.archive_dir
        assert self.archive_dir.exists()
        assert self.manager.archive_file.name == "tasks.json"

    def test_load_archive_empty(self):
        tasks = self.manager._load_archive()
        assert tasks['tasks'] == []
        assert tasks['last_updated'] is None

    def test_save_archive(self):
        self.manager.tasks['tasks'] = [{"id": 1, "test": "data"}]
        self.manager._save_archive()

        with open(self.manager.archive_file) as f:
            data = json.load(f)

        assert len(data['tasks']) == 1
        assert data['last_updated'] is not None

    def test_archive_task_new(self):
        task = {
            "task_id": "test_123",
            "prompt": "Test prompt",
            "completed_at": "2025-11-22 10:00:00"
        }

        result = self.manager.archive_task(task)
        assert result == True
        assert len(self.manager.tasks['tasks']) == 1

    def test_archive_task_update_existing(self):
        task1 = {"task_id": "test_123", "prompt": "Version 1"}
        task2 = {"task_id": "test_123", "prompt": "Version 2"}

        self.manager.archive_task(task1)
        self.manager.archive_task(task2)

        tasks = self.manager.get_archived_tasks()
        assert len(tasks) == 1
        assert tasks[0]['prompt'] == "Version 2"

    def test_get_task_by_id_exists(self):
        task = {"task_id": "test_123", "prompt": "Test"}
        self.manager.archive_task(task)

        result = self.manager.get_task_by_id("test_123")
        assert result is not None
        assert result['prompt'] == "Test"

    def test_get_task_by_id_not_exists(self):
        result = self.manager.get_task_by_id("nonexistent")
        assert result is None

    def test_get_tasks_by_status(self):
        self.manager.archive_task({"task_id": "1", "status": "COMPLETED"})
        self.manager.archive_task({"task_id": "2", "status": "FAILED"})
        self.manager.archive_task({"task_id": "3", "status": "COMPLETED"})

        completed = self.manager.get_tasks_by_status("COMPLETED")
        assert len(completed) == 2

        failed = self.manager.get_tasks_by_status("FAILED")
        assert len(failed) == 1

if __name__ == "__main__":
    pytest.main([__file__, "-v"])