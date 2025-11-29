#!/bin/bash
#
# capture_metrics.sh - PostToolUse Hook for Real-Time Metrics Capture
#
# This hook runs after each tool execution and updates the real-time
# metrics display in the status line.
#
# Receives JSON input via stdin containing:
# - tool_name: The tool that was executed
# - tool_input: The input parameters
# - tool_result: The result from the tool
# - conversation_stats: Context and token information
#

# Read JSON input from stdin
INPUT_JSON=$(cat)

# Extract relevant metrics from the conversation stats using Python (no jq dependency)
CONTEXT_TOKENS=$(echo "$INPUT_JSON" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('conversation_stats', {}).get('context_tokens', 0))" 2>/dev/null || echo "0")
TOTAL_TOKENS=$(echo "$INPUT_JSON" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('conversation_stats', {}).get('total_tokens', 200000))" 2>/dev/null || echo "200000")
TOOL_NAME=$(echo "$INPUT_JSON" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('tool_name', 'unknown'))" 2>/dev/null || echo "unknown")

# Calculate context percentage
if [[ "$TOTAL_TOKENS" -gt 0 ]]; then
    CONTEXT_PCT=$(echo "scale=2; ($CONTEXT_TOKENS / $TOTAL_TOKENS) * 100" | bc -l 2>/dev/null || echo "0.0")
else
    CONTEXT_PCT="0.0"
fi

# Update real-time metrics file
UPDATE_SCRIPT="/home/user01/claude-test/ClaudePrompt/update_realtime_metrics.py"

if [[ -f "$UPDATE_SCRIPT" ]]; then
    # Update with current context information
    # Note: Agents and confidence will be updated by the main cpp wrapper
    python3 "$UPDATE_SCRIPT" \
        --context-pct "$CONTEXT_PCT" \
        --executing \
        2>/dev/null

    # Output for hook system (optional)
    echo "{\"status\": \"metrics_updated\", \"context_pct\": $CONTEXT_PCT, \"tool\": \"$TOOL_NAME\"}"
fi

exit 0
