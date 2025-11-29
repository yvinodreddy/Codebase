#!/bin/bash
#
# capture_live_context_enhanced.sh - ENHANCED PostToolUse Hook with Debugging
#
# PRODUCTION-READY IMPLEMENTATION (2025-11-16)
# ==========================================
#
# ENHANCEMENTS FROM PREVIOUS VERSION:
# - Comprehensive logging for debugging
# - Better error handling
# - Multi-source data extraction
# - Writes to multiple cache locations for redundancy
# - Validates extracted data before writing
#
# ZERO BREAKING CHANGES - All existing functionality preserved
#

# Read JSON input from stdin
INPUT_JSON=$(cat)

# Paths
CONTEXT_CACHE="/tmp/claude_context_cache.txt"
METRICS_FILE="/home/user01/claude-test/ClaudePrompt/tmp/realtime_metrics.json"
AGENT_COUNTER="/home/user01/claude-test/ClaudePrompt/tmp/agent_usage_counter.txt"
DEBUG_LOG="/home/user01/claude-test/ClaudePrompt/tmp/hook_debug.log"

# Ensure tmp directory exists
mkdir -p "/home/user01/claude-test/ClaudePrompt/tmp"

# Enable debugging (set to 0 to disable)
DEBUG=1

log_debug() {
    if [[ $DEBUG -eq 1 ]]; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S.%3N')] $1" >> "$DEBUG_LOG"
    fi
}

log_debug "=== PostToolUse Hook Started ==="

# ============================================================================
# STEP 1: Extract conversation_stats from JSON input (LIVE DATA)
# ============================================================================

log_debug "Extracting conversation_stats from JSON input..."

# Try to extract LIVE token/context metrics from conversation_stats
CONV_STATS=$(echo "$INPUT_JSON" | python3 -c "
import sys, json

try:
    data = json.load(sys.stdin)
    stats = data.get('conversation_stats', {})

    if stats:
        # Print debug info to stderr
        print(f'[DEBUG] Found conversation_stats: {stats}', file=sys.stderr)

        # Extract all possible field names (Claude Code uses different names in different versions)
        context_tokens = (
            stats.get('context_tokens') or
            stats.get('tokens_used') or
            stats.get('total_tokens') or
            stats.get('current_tokens') or
            0
        )

        max_tokens = (
            stats.get('max_tokens') or
            stats.get('context_limit') or
            stats.get('max_context_tokens') or
            200000
        )

        # Get model name from multiple possible locations
        model = (
            data.get('model', {}).get('displayName') or
            data.get('model', {}).get('name') or
            stats.get('model') or
            'Unknown'
        )

        result = {
            'context_tokens': context_tokens,
            'max_tokens': max_tokens,
            'model': model,
            'raw_stats': stats  # Include raw stats for debugging
        }

        print(json.dumps(result))
    else:
        print(f'[DEBUG] No conversation_stats found in JSON input', file=sys.stderr)
        print('{}')
except Exception as e:
    print(f'[DEBUG] Error parsing JSON: {e}', file=sys.stderr)
    import traceback
    traceback.print_exc(file=sys.stderr)
    print('{}')
" 2>>"$DEBUG_LOG")

log_debug "CONV_STATS result: $CONV_STATS"

# Check if we got valid conversation_stats
if [[ -n "$CONV_STATS" ]] && [[ "$CONV_STATS" != "{}" ]]; then
    # Extract individual fields
    CONTEXT_TOKENS=$(echo "$CONV_STATS" | python3 -c "import sys, json; d=json.load(sys.stdin); print(d.get('context_tokens', 0))" 2>/dev/null || echo "0")
    MAX_TOKENS=$(echo "$CONV_STATS" | python3 -c "import sys, json; d=json.load(sys.stdin); print(d.get('max_tokens', 200000))" 2>/dev/null || echo "200000")
    MODEL=$(echo "$CONV_STATS" | python3 -c "import sys, json; d=json.load(sys.stdin); print(d.get('model', 'Unknown'))" 2>/dev/null || echo "Unknown")

    log_debug "Extracted: CONTEXT_TOKENS=$CONTEXT_TOKENS, MAX_TOKENS=$MAX_TOKENS, MODEL=$MODEL"

    # Validate extracted data
    if [[ "$CONTEXT_TOKENS" -gt 0 ]] && [[ "$CONTEXT_TOKENS" -le "$MAX_TOKENS" ]]; then
        # Calculate percentage
        TOKENS_PCT=$(echo "scale=1; ($CONTEXT_TOKENS / $MAX_TOKENS) * 100" | bc -l 2>/dev/null || echo "0.0")

        # Format as k
        TOKENS_USED_K=$(echo "scale=0; $CONTEXT_TOKENS / 1000" | bc 2>/dev/null || echo "0")
        TOKENS_TOTAL_K=$(echo "scale=0; $MAX_TOKENS / 1000" | bc 2>/dev/null || echo "200")

        log_debug "Calculated: TOKENS_PCT=$TOKENS_PCT, TOKENS_USED_K=${TOKENS_USED_K}k, TOKENS_TOTAL_K=${TOKENS_TOTAL_K}k"

        # Write to context cache in /context format
        cat > "$CONTEXT_CACHE" << EOF
Context Usage
$MODEL · ${TOKENS_USED_K}k/${TOKENS_TOTAL_K}k tokens (${TOKENS_PCT}%)
EOF

        # Touch the file to update timestamp (marks it as LIVE/fresh)
        touch "$CONTEXT_CACHE"

        log_debug "✓ Wrote to context cache: $CONTEXT_CACHE"
    else
        log_debug "⚠ Invalid token data: CONTEXT_TOKENS=$CONTEXT_TOKENS (expected > 0 and <= $MAX_TOKENS)"
    fi
else
    log_debug "⚠ No valid conversation_stats available"
    TOKENS_PCT="0.0"
fi

# ============================================================================
# STEP 2: Track agent usage
# ============================================================================

log_debug "Tracking agent usage..."

# Extract tool name
TOOL_NAME=$(echo "$INPUT_JSON" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    tool = data.get('tool_name', 'unknown')
    print(tool)
except:
    print('unknown')
" 2>/dev/null || echo "unknown")

log_debug "Tool name: $TOOL_NAME"

# Initialize counter file if it doesn't exist
if [[ ! -f "$AGENT_COUNTER" ]]; then
    echo "0" > "$AGENT_COUNTER"
    log_debug "Initialized agent counter to 0"
fi

# Increment agent counter (each tool use = 1 agent used)
# Exclude SlashCommand and other non-agent tools
NON_AGENT_TOOLS=("SlashCommand" "unknown" "")

if [[ ! " ${NON_AGENT_TOOLS[@]} " =~ " ${TOOL_NAME} " ]]; then
    CURRENT_COUNT=$(cat "$AGENT_COUNTER" 2>/dev/null || echo "0")
    NEW_COUNT=$((CURRENT_COUNT + 1))
    echo "$NEW_COUNT" > "$AGENT_COUNTER"
    AGENTS_USED="$NEW_COUNT"
    log_debug "Incremented agent counter: $CURRENT_COUNT -> $NEW_COUNT (tool: $TOOL_NAME)"
else
    AGENTS_USED=$(cat "$AGENT_COUNTER" 2>/dev/null || echo "0")
    log_debug "Skipped agent increment for tool: $TOOL_NAME (current count: $AGENTS_USED)"
fi

# ============================================================================
# STEP 3: Update realtime_metrics.json with LIVE data
# ============================================================================

log_debug "Updating realtime_metrics.json..."

# Calculate context percentage from cached or live data
if [[ -n "$TOKENS_PCT" ]]; then
    CONTEXT_PCT="$TOKENS_PCT"
else
    # Try to read from existing metrics
    CONTEXT_PCT=$(python3 -c "
import json
try:
    with open('$METRICS_FILE', 'r') as f:
        d = json.load(f)
    print(d.get('context_pct', 0.0))
except:
    print('0.0')
" 2>/dev/null || echo "0.0")
fi

log_debug "Final CONTEXT_PCT: $CONTEXT_PCT"

# Update metrics file
python3 << EOF >> "$DEBUG_LOG" 2>&1
import json
from datetime import datetime

metrics = {
    'agents': '$AGENTS_USED',
    'context_pct': float('$CONTEXT_PCT'),
    'confidence': '--',  # Will be updated by cpp execution
    'executing': True,
    'last_update': datetime.now().isoformat()
}

try:
    # Try to preserve existing confidence if available
    with open('$METRICS_FILE', 'r') as f:
        existing = json.load(f)
        if 'confidence' in existing and existing['confidence'] != '--':
            metrics['confidence'] = existing['confidence']
            print(f'[DEBUG] Preserved existing confidence: {existing["confidence"]}')
except Exception as e:
    print(f'[DEBUG] Could not load existing metrics: {e}')

try:
    with open('$METRICS_FILE', 'w') as f:
        json.dump(metrics, f, indent=2)
    print(f'[DEBUG] ✓ Updated metrics file: {metrics}')
except Exception as e:
    print(f'[DEBUG] ✗ Failed to write metrics: {e}')
EOF

log_debug "=== PostToolUse Hook Completed ==="

# ============================================================================
# STEP 4: Output for hook system (optional)
# ============================================================================

echo "{\"status\": \"live_context_captured\", \"agents_used\": $AGENTS_USED, \"context_pct\": $CONTEXT_PCT, \"tool\": \"$TOOL_NAME\"}"

exit 0
