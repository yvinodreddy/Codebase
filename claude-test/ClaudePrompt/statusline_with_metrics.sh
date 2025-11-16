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
MODEL=$(echo "$INPUT_JSON" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('model', {}).get('displayName', 'Unknown'))" 2>/dev/null || echo "Unknown")
CURRENT_DIR=$(echo "$INPUT_JSON" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('currentDirectory', '~'))" 2>/dev/null || echo "~")
DIR_NAME="${CURRENT_DIR##*/}"

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

# Build status line with color codes
# Format: [$MODEL] 📁 dir | 👥 agents | 📊 context% | ✓ confidence% | status

# Color codes
RESET='\033[0m'
BOLD='\033[1m'
CYAN='\033[36m'
GREEN='\033[32m'
YELLOW='\033[33m'
RED='\033[31m'

# Output formatted status line
echo -ne "${BOLD}[${CYAN}${MODEL}${RESET}${BOLD}]${RESET} 📁 ${DIR_NAME} | "
echo -ne "👥 ${AGENTS} | "

# Context with color based on percentage
if (( $(echo "$CONTEXT_PCT >= 95" | bc -l 2>/dev/null || echo 0) )); then
    echo -ne "${RED}📊 ${CONTEXT_DISPLAY}${RESET} | "
elif (( $(echo "$CONTEXT_PCT >= 85" | bc -l 2>/dev/null || echo 0) )); then
    echo -ne "${YELLOW}📊 ${CONTEXT_DISPLAY}${RESET} | "
elif (( $(echo "$CONTEXT_PCT >= 50" | bc -l 2>/dev/null || echo 0) )); then
    echo -ne "${GREEN}📊 ${CONTEXT_DISPLAY}${RESET} | "
else
    echo -ne "📊 ${CONTEXT_DISPLAY} | "
fi

# Confidence
if [[ "$CONFIDENCE" != "--" ]]; then
    if (( $(echo "$CONFIDENCE >= 99" | bc -l 2>/dev/null || echo 0) )); then
        echo -ne "${GREEN}✓ ${CONFIDENCE_DISPLAY}${RESET} | "
    elif (( $(echo "$CONFIDENCE >= 95" | bc -l 2>/dev/null || echo 0) )); then
        echo -ne "${YELLOW}✓ ${CONFIDENCE_DISPLAY}${RESET} | "
    else
        echo -ne "${RED}✓ ${CONFIDENCE_DISPLAY}${RESET} | "
    fi
else
    echo -ne "✓ ${CONFIDENCE_DISPLAY} | "
fi

# Status
echo -n "${STATUS}"
