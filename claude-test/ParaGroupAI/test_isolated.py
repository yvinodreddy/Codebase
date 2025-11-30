#!/usr/bin/env python3
"""Isolated test - runs in subprocess to avoid any caching"""

import subprocess
import sys

# Test script to run in subprocess
test_script = """
import sys
sys.path.insert(0, '/home/user01/claude-test/ParaGroupAI')

# Clean import
from master_orchestrator import MasterOrchestrator

# Try to create
orchestrator = MasterOrchestrator()
print(f"✅ SUCCESS: Created orchestrator with context manager type: {type(orchestrator.context_manager).__name__}")
"""

# Run in subprocess
result = subprocess.run(
    [sys.executable, "-c", test_script],
    capture_output=True,
    text=True,
    cwd='/home/user01/claude-test/ParaGroupAI'
)

print("STDOUT:")
print(result.stdout)
print("\nSTDERR:")
print(result.stderr)
print(f"\nExit code: {result.returncode}")
