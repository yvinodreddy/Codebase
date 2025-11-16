#!/bin/bash
#
# statusline_with_metrics.sh - Claude Code Status Line with Real-Time Metrics
#
# This script displays current execution metrics in the Claude Code status line,
# providing instant visibility into:
# - Current model and directory
# - Agent allocation
# - Context usage with color-coded indicators
# - Confidence scores
# - Execution status
#
# The status line updates automatically every 300ms when conversation messages update.
#

# Read JSON input from stdin (provided by Claude Code)
INPUT_JSON=$(cat)

# Extract basic session info from Claude Code's JSON input using Python (no jq dependency)
# Try to get model from JSON, fallback to config.py if unavailable
MODEL=$(echo "$INPUT_JSON" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    model = data.get('model', {}).get('displayName', '')
    if not model:
        # Fallback to config.py
        import sys
        sys.path.insert(0, '/home/user01/claude-test/ClaudePrompt')
        from config import UltrathinkConfig
        model_id = UltrathinkConfig.CLAUDE_MODEL_NAME
        # Convert 'claude-sonnet-4-5-20250929' to 'Sonnet 4.5'
        if 'sonnet-4-5' in model_id:
            model = 'Sonnet 4.5'
        elif 'sonnet' in model_id:
            model = 'Sonnet'
        elif 'opus' in model_id:
            model = 'Opus'
        elif 'haiku' in model_id:
            model = 'Haiku'
        else:
            model = 'Claude'
    print(model)
except:
    print('Sonnet 4.5')
" 2>/dev/null || echo "Sonnet 4.5")

# Get current directory - try multiple methods for robustness
CURRENT_DIR=$(echo "$INPUT_JSON" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('currentDirectory', ''))" 2>/dev/null)
if [[ -z "$CURRENT_DIR" ]]; then
    CURRENT_DIR=$(pwd 2>/dev/null || echo "$HOME")
fi

# Extract directory name from full path
if [[ "$CURRENT_DIR" == "$HOME" ]]; then
    DIR_NAME="~"
else
    DIR_NAME="${CURRENT_DIR##*/}"
    # If empty (root directory), use full path
    [[ -z "$DIR_NAME" ]] && DIR_NAME="$CURRENT_DIR"
fi

# Path to real-time metrics file
METRICS_FILE="/home/user01/claude-test/ClaudePrompt/tmp/realtime_metrics.json"

# Default values
AGENTS="N/A"
CONTEXT_PCT="0.0"
CONFIDENCE="--"
STATUS="🟢 READY"

# Read current execution metrics if file exists and is recent (updated within last 5 minutes)
if [[ -f "$METRICS_FILE" ]]; then
    FILE_AGE=$(($(date +%s) - $(stat -c %Y "$METRICS_FILE" 2>/dev/null || echo 0)))

    if [[ $FILE_AGE -lt 300 ]]; then
        # File is recent, read metrics using Python
        AGENTS=$(python3 -c "import json; data=json.load(open('$METRICS_FILE')); print(data.get('agents', 'N/A'))" 2>/dev/null || echo "N/A")
        CONTEXT_PCT=$(python3 -c "import json; data=json.load(open('$METRICS_FILE')); print(data.get('context_pct', 0.0))" 2>/dev/null || echo "0.0")
        CONFIDENCE=$(python3 -c "import json; data=json.load(open('$METRICS_FILE')); print(data.get('confidence', '--'))" 2>/dev/null || echo "--")
        EXECUTING=$(python3 -c "import json; data=json.load(open('$METRICS_FILE')); print(str(data.get('executing', False)).lower())" 2>/dev/null || echo "false")

        # Determine status based on execution state and context
        if [[ "$EXECUTING" == "true" ]]; then
            # During execution, show context-based status
            if (( $(echo "$CONTEXT_PCT >= 95" | bc -l 2>/dev/null || echo 0) )); then
                STATUS="🔴 CRITICAL"
            elif (( $(echo "$CONTEXT_PCT >= 85" | bc -l 2>/dev/null || echo 0) )); then
                STATUS="🟡 WARNING"
            elif (( $(echo "$CONTEXT_PCT >= 50" | bc -l 2>/dev/null || echo 0) )); then
                STATUS="✅ ACTIVE"
            else
                STATUS="🟢 ACTIVE"
            fi
        else
            # Not executing, show ready status
            STATUS="🟢 READY"
        fi
    fi
fi

# Format context percentage
CONTEXT_DISPLAY=$(printf "%.1f%%" "$CONTEXT_PCT" 2>/dev/null || echo "0.0%")

# Format confidence
if [[ "$CONFIDENCE" != "--" ]]; then
    CONFIDENCE_DISPLAY=$(printf "%.1f%%" "$CONFIDENCE" 2>/dev/null || echo "--")
else
    CONFIDENCE_DISPLAY="--"
fi

# Build complete status line matching user's desired format
# Format: user@host:/path                  ctrl-g hint  [Model] metrics

# Color codes - use $'...' syntax for proper escape sequence interpretation
RESET=$'\033[0m'
BOLD=$'\033[1m'
CYAN=$'\033[36m'
GREEN=$'\033[32m'
YELLOW=$'\033[33m'
RED=$'\033[31m'

# Get system info
USERNAME=$(whoami 2>/dev/null || echo "user")
HOSTNAME=$(hostname 2>/dev/null || echo "localhost")

# Build metrics portion
METRICS=""
METRICS+="${BOLD}[${CYAN}${MODEL}${RESET}${BOLD}]${RESET} "
METRICS+="📁 ${DIR_NAME} | "
METRICS+="👥 ${AGENTS} | "

# Context with color based on percentage
if (( $(echo "$CONTEXT_PCT >= 95" | bc -l 2>/dev/null || echo 0) )); then
    METRICS+="${RED}📊 ${CONTEXT_DISPLAY}${RESET} | "
elif (( $(echo "$CONTEXT_PCT >= 85" | bc -l 2>/dev/null || echo 0) )); then
    METRICS+="${YELLOW}📊 ${CONTEXT_DISPLAY}${RESET} | "
elif (( $(echo "$CONTEXT_PCT >= 50" | bc -l 2>/dev/null || echo 0) )); then
    METRICS+="${GREEN}📊 ${CONTEXT_DISPLAY}${RESET} | "
else
    METRICS+="📊 ${CONTEXT_DISPLAY} | "
fi

# Confidence
if [[ "$CONFIDENCE" != "--" ]]; then
    if (( $(echo "$CONFIDENCE >= 99" | bc -l 2>/dev/null || echo 0) )); then
        METRICS+="${GREEN}✓ ${CONFIDENCE_DISPLAY}${RESET} | "
    elif (( $(echo "$CONFIDENCE >= 95" | bc -l 2>/dev/null || echo 0) )); then
        METRICS+="${YELLOW}✓ ${CONFIDENCE_DISPLAY}${RESET} | "
    else
        METRICS+="${RED}✓ ${CONFIDENCE_DISPLAY}${RESET} | "
    fi
else
    METRICS+="✓ ${CONFIDENCE_DISPLAY} | "
fi

# Status
METRICS+="${STATUS}"

# Output complete status line
# Format: username@hostname:/path              ctrl-g hint  [metrics]
# Use printf to output the statusline - METRICS already contains interpreted escape codes
printf "%s@%s:%s                     ctrl-g to edit prompt in code  %s" "${USERNAME}" "${HOSTNAME}" "${CURRENT_DIR}" "${METRICS}"
