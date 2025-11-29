#!/bin/bash
#
# update_metrics_from_output.sh - Update Metrics After cpp Execution
#
# PRODUCTION-READY IMPLEMENTATION (2025-11-16)
# ============================================
#
# This script runs AFTER cpp execution completes to extract the REAL
# confidence score from the actual answer and update metrics.
#
# FEATURES:
# - Extracts confidence from answer section (not system output)
# - Updates realtime_metrics.json with actual confidence
# - Preserves other metrics (agents, tokens, etc.)
# - Zero breaking changes
#
# USAGE:
#   ./update_metrics_from_output.sh <output_file>
#

OUTPUT_FILE="$1"

if [[ -z "$OUTPUT_FILE" ]]; then
    echo "Error: No output file provided" >&2
    exit 1
fi

if [[ ! -f "$OUTPUT_FILE" ]]; then
    echo "Error: Output file not found: $OUTPUT_FILE" >&2
    exit 1
fi

# Paths
EXTRACTOR="/home/user01/claude-test/ClaudePrompt/extract_confidence_from_output.py"
METRICS_FILE="/home/user01/claude-test/ClaudePrompt/tmp/realtime_metrics.json"
UPDATER="/home/user01/claude-test/ClaudePrompt/update_realtime_metrics.py"

# ============================================================================
# STEP 1: Extract confidence score from output file
# ============================================================================

CONFIDENCE_JSON=$(python3 "$EXTRACTOR" "$OUTPUT_FILE" --json 2>/dev/null)

if [[ -z "$CONFIDENCE_JSON" ]]; then
    echo "Warning: Could not extract confidence from output file" >&2
    exit 1
fi

# Parse confidence value
CONFIDENCE=$(echo "$CONFIDENCE_JSON" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    conf = data.get('confidence')
    if conf is not None:
        print(conf)
    else:
        print('--')
except:
    print('--')
" 2>/dev/null)

# ============================================================================
# STEP 2: Update realtime_metrics.json with extracted confidence
# ============================================================================

if [[ "$CONFIDENCE" != "--" ]]; then
    # Update metrics with real confidence score
    python3 "$UPDATER" --confidence "$CONFIDENCE" 2>/dev/null

    if [[ $? -eq 0 ]]; then
        echo "✓ Updated confidence to ${CONFIDENCE}%" >&2
    else
        echo "Warning: Failed to update confidence" >&2
    fi
else
    echo "Warning: No confidence score found in output" >&2
fi

# ============================================================================
# STEP 3: Mark execution as complete (no longer executing)
# ============================================================================

# Update executing flag to false now that cpp is done
python3 << EOF 2>/dev/null
import json
from datetime import datetime

try:
    # Load existing metrics
    with open('$METRICS_FILE', 'r') as f:
        metrics = json.load(f)

    # Mark as not executing
    metrics['executing'] = False
    metrics['last_update'] = datetime.now().isoformat()

    # Write back
    with open('$METRICS_FILE', 'w') as f:
        json.dump(metrics, f, indent=2)

    print('✓ Marked execution as complete', file=sys.stderr)
except Exception as e:
    print(f'Warning: Failed to update executing flag: {e}', file=sys.stderr)
EOF

exit 0
