#!/usr/bin/env bash
#
# debug_hook_input.sh - Debug what INPUT_JSON actually contains
#
# This script logs the raw INPUT_JSON to a file so we can see
# what data is actually available in the PostToolUse hook.

# Read JSON from stdin
INPUT_JSON=$(cat)

# Log to debug file
DEBUG_FILE="/home/user01/claude-test/ClaudePrompt/tmp/hook_input_debug.json"
echo "$INPUT_JSON" | python3 -m json.tool > "$DEBUG_FILE" 2>&1

# Also log timestamp
echo "=== Hook executed at $(date) ===" >> "/home/user01/claude-test/ClaudePrompt/tmp/hook_debug.log"
echo "$INPUT_JSON" | python3 -c "import sys, json; data = json.load(sys.stdin); print('Keys available:', list(data.keys()))" >> "/home/user01/claude-test/ClaudePrompt/tmp/hook_debug.log" 2>&1

# Pass through to not break the hook
echo '{"status": "debug_logged"}'
