#!/usr/bin/env python3
from pathlib import Path

# Test the exact logic from ultrathink.py lines 1493-1518
test_file = Path('/home/user01/claude-test/ClaudePrompt/tmp/ultrathink-prompt-123.txt')
file_path = test_file.resolve()

cwd = Path.cwd()
home = Path.home()

print(f"File path: {file_path}")
print(f"CWD: {cwd}")
print(f"Home: {home}")
print()

# Check if file is in current directory or user's home directory
is_in_cwd = False
is_in_home = False

try:
    result = file_path.relative_to(cwd)
    is_in_cwd = True
    print(f"✅ relative_to(cwd) WORKS: {result}")
except ValueError as e:
    print(f"❌ relative_to(cwd) FAILED: {e}")

try:
    result = file_path.relative_to(home)
    is_in_home = True
    print(f"✅ relative_to(home) WORKS: {result}")
except ValueError as e:
    print(f"❌ relative_to(home) FAILED: {e}")

print()
print(f"is_in_cwd: {is_in_cwd}")
print(f"is_in_home: {is_in_home}")
print(f"Security check passes: {is_in_cwd or is_in_home}")
