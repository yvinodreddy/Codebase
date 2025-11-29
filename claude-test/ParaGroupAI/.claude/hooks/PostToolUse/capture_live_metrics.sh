#!/bin/bash
#
# capture_live_metrics.sh - Enhanced PostToolUse Hook for LIVE Metrics Capture
#
# ENHANCEMENTS (2025-11-16):
# - Tracks ACTUAL tool/agent usage (not allocated)
# - Integrates with /context for live token metrics
# - Counts each tool invocation to provide accurate "agents used" count
#
# This hook runs after each tool execution and updates the real-time
# metrics display in the status line with LIVE, ACTUAL data.
#
# Receives JSON input via stdin containing:
# - tool_name: The tool that was executed
# - tool_input: The input parameters
# - tool_result: The result from the tool
# - conversation_stats: Context and token information
#

# Read JSON input from stdin
INPUT_JSON=$(cat)

# Paths
METRICS_FILE="/home/user01/claude-test/ClaudePrompt/tmp/realtime_metrics.json"
AGENT_COUNTER="/home/user01/claude-test/ClaudePrompt/tmp/agent_usage_counter.txt"
UPDATE_SCRIPT="/home/user01/claude-test/ClaudePrompt/update_realtime_metrics.py"

# Ensure tmp directory exists
mkdir -p "/home/user01/claude-test/ClaudePrompt/tmp"

# ============================================================================
# STEP 1: Track ACTUAL tool/agent usage
# ============================================================================

# Extract tool name
TOOL_NAME=$(echo "$INPUT_JSON" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    print(data.get('tool_name', 'unknown'))
except:
    print('unknown')
" 2>/dev/null || echo "unknown")

# Initialize counter file if it doesn't exist
if [[ ! -f "$AGENT_COUNTER" ]]; then
    echo "0" > "$AGENT_COUNTER"
fi

# Increment agent counter (each tool use = 1 agent used)
if [[ "$TOOL_NAME" != "unknown" ]] && [[ "$TOOL_NAME" != "SlashCommand" ]]; then
    CURRENT_COUNT=$(cat "$AGENT_COUNTER" 2>/dev/null || echo "0")
    NEW_COUNT=$((CURRENT_COUNT + 1))
    echo "$NEW_COUNT" > "$AGENT_COUNTER"
    AGENTS_USED="$NEW_COUNT"
else
    AGENTS_USED=$(cat "$AGENT_COUNTER" 2>/dev/null || echo "0")
fi

# Format agents as "X" (actual used) instead of "X/Y" (allocated)
# The statusline will combine this with max agents (500) if needed
AGENTS_DISPLAY="$AGENTS_USED"

# ============================================================================
# STEP 2: Extract context/token metrics from conversation stats
# ============================================================================

# Try to get token usage from conversation_stats (if provided by Claude Code)
CONTEXT_TOKENS=$(echo "$INPUT_JSON" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    stats = data.get('conversation_stats', {})
    # Try different possible fields
    tokens = stats.get('context_tokens') or stats.get('tokens_used') or stats.get('total_tokens', 0)
    print(int(tokens))
except:
    print(0)
" 2>/dev/null || echo "0")

TOTAL_TOKENS=$(echo "$INPUT_JSON" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    stats = data.get('conversation_stats', {})
    # Default to 200k tokens for Sonnet 4.5
    total = stats.get('max_tokens') or stats.get('context_limit', 200000)
    print(int(total))
except:
    print(200000)
" 2>/dev/null || echo "200000")

# Calculate context percentage
if [[ "$TOTAL_TOKENS" -gt 0 ]] && [[ "$CONTEXT_TOKENS" -gt 0 ]]; then
    CONTEXT_PCT=$(echo "scale=2; ($CONTEXT_TOKENS / $TOTAL_TOKENS) * 100" | bc -l 2>/dev/null || echo "0.0")
else
    CONTEXT_PCT="0.0"
fi

# ============================================================================
# STEP 3: Try to integrate with cached /context output (if available)
# ============================================================================

CONTEXT_CACHE="/tmp/claude_context_cache.txt"

# Check if /context cache exists and is very recent (< 2 seconds)
if [[ -f "$CONTEXT_CACHE" ]]; then
    FILE_AGE=$(($(date +%s) - $(stat -c %Y "$CONTEXT_CACHE" 2>/dev/null || echo 999)))

    if [[ $FILE_AGE -lt 2 ]]; then
        # Cache is fresh - parse it for more accurate metrics
        LIVE_METRICS=$(python3 /home/user01/claude-test/ClaudePrompt/get_live_context_metrics.py \
            --json --input "$CONTEXT_CACHE" 2>/dev/null)

        if [[ $? -eq 0 ]] && [[ -n "$LIVE_METRICS" ]]; then
            # Extract live token metrics
            LIVE_TOKENS=$(echo "$LIVE_METRICS" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    if d.get('status') == 'success':
        print(d.get('tokens_used', 0))
    else:
        print(0)
except:
    print(0)
" 2>/dev/null)

            LIVE_PCT=$(echo "$LIVE_METRICS" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    if d.get('status') == 'success':
        print(d.get('tokens_pct', 0.0))
    else:
        print(0.0)
except:
    print(0.0)
" 2>/dev/null)

            # Use live metrics if available
            if [[ "$LIVE_TOKENS" -gt 0 ]]; then
                CONTEXT_TOKENS="$LIVE_TOKENS"
                CONTEXT_PCT="$LIVE_PCT"
            fi
        fi
    fi
fi

# ============================================================================
# STEP 4: Update real-time metrics using COMPREHENSIVE METRICS UPDATER
# ============================================================================

COMPREHENSIVE_UPDATER="/home/user01/claude-test/ClaudePrompt/comprehensive_metrics_updater.py"

if [[ -f "$COMPREHENSIVE_UPDATER" ]]; then
    # Use NEW comprehensive metrics updater (2025-11-16)
    # This fixes ALL issues:
    # 1. ✅ Agent counter never decreases → Auto-clear logic
    # 2. ✅ No agent visibility → view-agents command
    # 3. ✅ Token tracking shows 0k/200k → Real token usage
    # 4. ✅ Confidence static at 100.0 → Dynamic 0-100
    # 5. ✅ Status not updating → Real-time calculation
    # 6. ✅ Background tasks not tracked → Detection and persistence

    echo "$INPUT_JSON" | python3 "$COMPREHENSIVE_UPDATER" --stdin 2>/dev/null

    # Output for hook system
    echo "{\"status\": \"comprehensive_metrics_updated\", \"tool\": \"$TOOL_NAME\"}"
else
    # Fallback to legacy updater (should never happen)
    python3 "$UPDATE_SCRIPT" \
        --agents "$AGENTS_DISPLAY" \
        --context-pct "$CONTEXT_PCT" \
        --executing \
        2>/dev/null

    echo "{\"status\": \"fallback_legacy_updater\", \"agents_used\": $AGENTS_USED, \"context_pct\": $CONTEXT_PCT, \"tool\": \"$TOOL_NAME\"}"
fi

# ============================================================================
# STEP 5: Log actual usage for debugging
# ============================================================================

# Optional: Log to debug file for troubleshooting
DEBUG_LOG="/home/user01/claude-test/ClaudePrompt/tmp/agent_usage.log"
if [[ "${DEBUG_METRICS}" == "1" ]]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Tool: $TOOL_NAME | Agents Used: $AGENTS_USED | Context: ${CONTEXT_PCT}%" >> "$DEBUG_LOG"
fi

exit 0
