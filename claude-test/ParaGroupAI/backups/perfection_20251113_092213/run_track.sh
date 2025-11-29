#!/usr/bin/env bash
#
# Run a specific track with timestamped output
#
# Usage:
#   ./run_track.sh 1 "Your prompt for track 1"
#   ./run_track.sh 2 "Your prompt for track 2"
#

set -e  # Exit on error

# Check arguments
if [ $# -lt 2 ]; then
    echo "Usage: ./run_track.sh <track_number> <prompt>"
    echo "Example: ./run_track.sh 1 'Implement testing infrastructure'"
    exit 1
fi

TRACK_NUM=$1
PROMPT=$2

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Generate unique output file for this track
OUTPUT_FILE=$(python3 "$SCRIPT_DIR/get_output_path.py" --track "$TRACK_NUM")

echo "=============================================================================="
echo "🚀 TRACK $TRACK_NUM EXECUTION"
echo "=============================================================================="
echo "📁 Output file: $OUTPUT_FILE"
echo "📝 Prompt: $PROMPT"
echo "⏱️  Started: $(date '+%Y-%m-%d %H:%M:%S')"
echo "=============================================================================="
echo ""

# Run cpp command with output redirected to unique file
"$SCRIPT_DIR/cpp" "$PROMPT" --verbose 2>&1 | tee "$OUTPUT_FILE"

# Show completion message
echo ""
echo "=============================================================================="
echo "✅ TRACK $TRACK_NUM COMPLETE"
echo "=============================================================================="
echo "📁 Output saved to: $OUTPUT_FILE"
echo "⏱️  Completed: $(date '+%Y-%m-%d %H:%M:%S')"
echo "📖 Read output: cat $OUTPUT_FILE"
echo "=============================================================================="
