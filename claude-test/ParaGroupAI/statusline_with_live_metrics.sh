#!/bin/bash
#
# statusline_with_live_metrics.sh - Enhanced Claude Code Status Line with LIVE Metrics
#
# ENHANCEMENTS (2025-11-16):
# - Integrates with /context command for LIVE token usage
# - Displays actual agent count from current execution (not allocated)
# - Shows live context percentage calculated from /context
# - New format: Model | Context | Agents Live | Tokens from /context | % Live | Status
#
# This script displays current execution metrics in the Claude Code status line,
# providing instant visibility into LIVE metrics from the running Claude Code session.
#
# The status line updates automatically every 300ms when conversation messages update.
#
# BACKWARD COMPATIBILITY:
# - Falls back to existing metrics if /context data not available
# - All existing functionality preserved
# - Zero breaking changes
#

# Read JSON input from stdin (provided by Claude Code)
INPUT_JSON=$(cat)

# ============================================================================
# STEP 1: Extract basic session info from Claude Code's JSON input
# ============================================================================

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
        if 'sonnet-4-5' in model_id or 'sonnet-4.5' in model_id:
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

# Determine context source (ClaudePrompt for cpp commands, System for claude code)
if [[ "$DIR_NAME" == "ClaudePrompt" ]]; then
    CONTEXT_SOURCE="ClaudePrompt"
else
    CONTEXT_SOURCE="System"
fi

# ============================================================================
# STEP 2: Try to get LIVE metrics from /context command output cache
# ============================================================================

CONTEXT_CACHE="/tmp/claude_context_cache.txt"
LIVE_METRICS_AVAILABLE=false
TOKENS_USED_K="0"
TOKENS_TOTAL_K="200"
TOKENS_PCT="0.0"
AGENTS_LIVE="N/A"

# Check if cached /context output exists and is recent (< 5 seconds old)
if [[ -f "$CONTEXT_CACHE" ]]; then
    FILE_AGE=$(($(date +%s) - $(stat -c %Y "$CONTEXT_CACHE" 2>/dev/null || echo 0)))

    if [[ $FILE_AGE -lt 5 ]]; then
        # Parse /context output using Python
        LIVE_METRICS=$(python3 /home/user01/claude-test/ClaudePrompt/get_live_context_metrics.py --json --input "$CONTEXT_CACHE" 2>/dev/null)

        if [[ $? -eq 0 ]]; then
            # Successfully parsed
            LIVE_METRICS_AVAILABLE=true

            # Extract values using Python
            TOKENS_USED=$(echo "$LIVE_METRICS" | python3 -c "import sys, json; d=json.load(sys.stdin); print(d.get('tokens_used', 0))" 2>/dev/null || echo 0)
            TOKENS_TOTAL=$(echo "$LIVE_METRICS" | python3 -c "import sys, json; d=json.load(sys.stdin); print(d.get('tokens_total', 200000))" 2>/dev/null || echo 200000)
            TOKENS_PCT=$(echo "$LIVE_METRICS" | python3 -c "import sys, json; d=json.load(sys.stdin); print(d.get('tokens_pct', 0.0))" 2>/dev/null || echo 0.0)
            TOKENS_DISPLAY=$(echo "$LIVE_METRICS" | python3 -c "import sys, json; d=json.load(sys.stdin); print(d.get('tokens_display', '0k/200k'))" 2>/dev/null || echo "0k/200k")

            # Convert tokens to k format
            TOKENS_USED_K=$(echo "scale=0; $TOKENS_USED / 1000" | bc 2>/dev/null || echo 0)
            TOKENS_TOTAL_K=$(echo "scale=0; $TOKENS_TOTAL / 1000" | bc 2>/dev/null || echo 200)

            # Model from /context overrides config.py
            MODEL_FROM_CONTEXT=$(echo "$LIVE_METRICS" | python3 -c "import sys, json; d=json.load(sys.stdin); print(d.get('model_short', 'Unknown'))" 2>/dev/null)
            if [[ "$MODEL_FROM_CONTEXT" != "Unknown" ]]; then
                MODEL="$MODEL_FROM_CONTEXT"
            fi
        fi
    fi
fi

# ============================================================================
# STEP 3: Get agent count from realtime metrics (actual usage, not allocated)
# ============================================================================

METRICS_FILE="/home/user01/claude-test/ClaudePrompt/tmp/realtime_metrics.json"
CONFIDENCE="--"
STATUS="🟢 READY"
EXECUTING=false

# Read current execution metrics if file exists and is recent (updated within last 5 minutes)
if [[ -f "$METRICS_FILE" ]]; then
    FILE_AGE=$(($(date +%s) - $(stat -c %Y "$METRICS_FILE" 2>/dev/null || echo 0)))

    if [[ $FILE_AGE -lt 300 ]]; then
        # Get actual agents used (not allocated)
        AGENTS_ACTUAL=$(python3 -c "
import json, sys
try:
    data = json.load(open('$METRICS_FILE'))
    # Get actual agents used from metrics
    agents_str = data.get('agents', 'N/A')

    # Parse different formats:
    # - '8/30' (actual/allocated)
    # - '25/30' (allocated)
    # - '8' (just actual)

    if '/' in str(agents_str):
        # Format: X/Y - extract actual (X)
        actual = agents_str.split('/')[0].strip()
        print(actual)
    else:
        print(agents_str)
except:
    print('N/A')
" 2>/dev/null || echo "N/A")

        # If we got actual agents, use it
        if [[ "$AGENTS_ACTUAL" != "N/A" ]]; then
            AGENTS_LIVE="$AGENTS_ACTUAL"
        fi

        # Get confidence and execution status
        CONFIDENCE=$(python3 -c "import json; data=json.load(open('$METRICS_FILE')); print(data.get('confidence', '--'))" 2>/dev/null || echo "--")
        EXECUTING=$(python3 -c "import json; data=json.load(open('$METRICS_FILE')); print(str(data.get('executing', False)).lower())" 2>/dev/null || echo "false")

        # If using live metrics, override context percentage with live value
        if [[ "$LIVE_METRICS_AVAILABLE" == false ]]; then
            # Fall back to stored context percentage
            CONTEXT_PCT_STORED=$(python3 -c "import json; data=json.load(open('$METRICS_FILE')); print(data.get('context_pct', 0.0))" 2>/dev/null || echo "0.0")
            TOKENS_PCT="$CONTEXT_PCT_STORED"
        fi

        # Determine status based on execution state and context
        if [[ "$EXECUTING" == "true" ]]; then
            # During execution, show context-based status
            if (( $(echo "$TOKENS_PCT >= 95" | bc -l 2>/dev/null || echo 0) )); then
                STATUS="🔴 CRITICAL"
            elif (( $(echo "$TOKENS_PCT >= 85" | bc -l 2>/dev/null || echo 0) )); then
                STATUS="🟡 WARNING"
            elif (( $(echo "$TOKENS_PCT >= 50" | bc -l 2>/dev/null || echo 0) )); then
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

# ============================================================================
# STEP 4: Format and display metrics in NEW format
# ============================================================================
# New Format (per user request):
# Model Name | Context Source | Agents Live | Tokens from /context | % Live | Status
#
# Example:
# Sonnet 4.5 | ClaudePrompt | 8 | 29k/200k (15%) | 15.0% | 🟢 ACTIVE

# Color codes - use $'...' syntax for proper escape sequence interpretation
RESET=$'\033[0m'
BOLD=$'\033[1m'
CYAN=$'\033[36m'
GREEN=$'\033[32m'
YELLOW=$'\033[33m'
RED=$'\033[31m'
BLUE=$'\033[34m'

# Get system info
USERNAME=$(whoami 2>/dev/null || echo "user")
HOSTNAME=$(hostname 2>/dev/null || echo "localhost")

# Build metrics portion with NEW format
METRICS=""

# Model Name (colored)
METRICS+="${BOLD}[${CYAN}${MODEL}${RESET}${BOLD}]${RESET} | "

# Context Source (ClaudePrompt or System)
if [[ "$CONTEXT_SOURCE" == "ClaudePrompt" ]]; then
    METRICS+="📁 ${BLUE}${CONTEXT_SOURCE}${RESET}"
else
    METRICS+="📁 ${CONTEXT_SOURCE}"
fi
METRICS+=" | "

# Agents Live (actual usage for this request)
METRICS+="👥 ${AGENTS_LIVE} | "

# Tokens from /context (with live indicator if available)
if [[ "$LIVE_METRICS_AVAILABLE" == true ]]; then
    # Live metrics available - show with indicator
    METRICS+="📊 ${GREEN}${TOKENS_DISPLAY}${RESET} (${TOKENS_PCT}%) [LIVE] | "
else
    # Cached metrics - show without live indicator
    METRICS+="📊 ${TOKENS_USED_K}k/${TOKENS_TOTAL_K}k (${TOKENS_PCT}%) | "
fi

# Percentage (live calculated from /context)
PERCENT_DISPLAY=$(printf "%.1f%%" "$TOKENS_PCT" 2>/dev/null || echo "0.0%")

# Color percentage based on value
if (( $(echo "$TOKENS_PCT >= 95" | bc -l 2>/dev/null || echo 0) )); then
    METRICS+="${RED}${PERCENT_DISPLAY}${RESET} | "
elif (( $(echo "$TOKENS_PCT >= 85" | bc -l 2>/dev/null || echo 0) )); then
    METRICS+="${YELLOW}${PERCENT_DISPLAY}${RESET} | "
elif (( $(echo "$TOKENS_PCT >= 50" | bc -l 2>/dev/null || echo 0) )); then
    METRICS+="${GREEN}${PERCENT_DISPLAY}${RESET} | "
else
    METRICS+="${PERCENT_DISPLAY} | "
fi

# Status (same as before)
METRICS+="${STATUS}"

# ============================================================================
# STEP 5: Output complete status line
# ============================================================================
# Format: username@hostname:/path              ctrl-g hint  [metrics]
# Use printf to output the statusline - METRICS already contains interpreted escape codes
printf "%s@%s:%s                     ctrl-g to edit prompt in code  %s" "${USERNAME}" "${HOSTNAME}" "${CURRENT_DIR}" "${METRICS}"
