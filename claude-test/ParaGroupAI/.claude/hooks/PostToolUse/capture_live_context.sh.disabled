#!/bin/bash
#
# capture_live_context.sh - Enhanced PostToolUse Hook for LIVE Context Capture
#
# PRODUCTION-READY IMPLEMENTATION (2025-11-16)
# ==========================================
#
# This hook captures LIVE conversation_stats from Claude Code's JSON input
# and writes it to the context cache for use by the statusline.
#
# ZERO BREAKING CHANGES:
# - All existing functionality preserved
# - Graceful degradation if conversation_stats unavailable
# - Backward compatible with manual /context capture
#
# MULTI-SOURCE CAPTURE:
# 1. conversation_stats from JSON input (highest priority - LIVE)
# 2. Tool execution metrics
# 3. Agent usage counter
#

# Read JSON input from stdin
INPUT_JSON=$(cat)

# Paths
CONTEXT_CACHE="/tmp/claude_context_cache.txt"
METRICS_FILE="/home/user01/claude-test/ClaudePrompt/tmp/realtime_metrics.json"
AGENT_COUNTER="/home/user01/claude-test/ClaudePrompt/tmp/agent_usage_counter.txt"

# Ensure tmp directory exists
mkdir -p "/home/user01/claude-test/ClaudePrompt/tmp"

# ============================================================================
# STEP 1: Extract conversation_stats from JSON input (LIVE)
# ============================================================================

# Try to extract LIVE token/context metrics from conversation_stats
CONV_STATS=$(echo "$INPUT_JSON" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    stats = data.get('conversation_stats', {})
    if stats:
        # Extract available fields
        result = {
            'context_tokens': stats.get('context_tokens', stats.get('tokens_used', stats.get('total_tokens', 0))),
            'max_tokens': stats.get('max_tokens', stats.get('context_limit', 200000)),
            'model': data.get('model', {}).get('displayName', 'Unknown')
        }
        print(json.dumps(result))
    else:
        print('{}')
except:
    print('{}')
" 2>/dev/null)

# Check if we got valid conversation_stats
if [[ -n "$CONV_STATS" ]] && [[ "$CONV_STATS" != "{}" ]]; then
    # We have LIVE conversation_stats!
    CONTEXT_TOKENS=$(echo "$CONV_STATS" | python3 -c "import sys, json; d=json.load(sys.stdin); print(d.get('context_tokens', 0))" 2>/dev/null || echo "0")
    MAX_TOKENS=$(echo "$CONV_STATS" | python3 -c "import sys, json; d=json.load(sys.stdin); print(d.get('max_tokens', 200000))" 2>/dev/null || echo "200000")
    MODEL=$(echo "$CONV_STATS" | python3 -c "import sys, json; d=json.load(sys.stdin); print(d.get('model', 'Unknown'))" 2>/dev/null || echo "Unknown")

    if [[ "$CONTEXT_TOKENS" -gt 0 ]]; then
        # Calculate percentage
        TOKENS_PCT=$(echo "scale=1; ($CONTEXT_TOKENS / $MAX_TOKENS) * 100" | bc -l 2>/dev/null || echo "0.0")

        # Format as k
        TOKENS_USED_K=$(echo "scale=0; $CONTEXT_TOKENS / 1000" | bc 2>/dev/null || echo "0")
        TOKENS_TOTAL_K=$(echo "scale=0; $MAX_TOKENS / 1000" | bc 2>/dev/null || echo "200")

        # Write to context cache in /context format
        # This allows the multi-source verifier to use it as a LIVE source
        cat > "$CONTEXT_CACHE" << EOF
Context Usage
$MODEL · ${TOKENS_USED_K}k/${TOKENS_TOTAL_K}k tokens (${TOKENS_PCT}%)
EOF

        # Touch the file to update timestamp (marks it as LIVE/fresh)
        touch "$CONTEXT_CACHE"
    fi
fi

# ============================================================================
# STEP 2: Track agent usage
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
# Exclude SlashCommand and other non-agent tools
if [[ "$TOOL_NAME" != "unknown" ]] && [[ "$TOOL_NAME" != "SlashCommand" ]]; then
    CURRENT_COUNT=$(cat "$AGENT_COUNTER" 2>/dev/null || echo "0")
    NEW_COUNT=$((CURRENT_COUNT + 1))
    echo "$NEW_COUNT" > "$AGENT_COUNTER"
    AGENTS_USED="$NEW_COUNT"
else
    AGENTS_USED=$(cat "$AGENT_COUNTER" 2>/dev/null || echo "0")
fi

# ============================================================================
# STEP 3: Update realtime_metrics.json with LIVE data
# ============================================================================

# Calculate context percentage from cached or live data
if [[ -n "$TOKENS_PCT" ]]; then
    CONTEXT_PCT="$TOKENS_PCT"
else
    # Try to read from existing metrics
    CONTEXT_PCT=$(python3 -c "import json; d=json.load(open('$METRICS_FILE')); print(d.get('context_pct', 0.0))" 2>/dev/null || echo "0.0")
fi

# Update metrics file
python3 << EOF
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
except:
    pass

with open('$METRICS_FILE', 'w') as f:
    json.dump(metrics, f, indent=2)
EOF

# ============================================================================
# STEP 4: Output for hook system (optional)
# ============================================================================

echo "{\"status\": \"live_context_captured\", \"agents_used\": $AGENTS_USED, \"context_pct\": $CONTEXT_PCT, \"tool\": \"$TOOL_NAME\"}"

exit 0
