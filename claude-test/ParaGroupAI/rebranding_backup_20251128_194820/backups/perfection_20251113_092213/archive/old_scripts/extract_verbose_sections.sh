#!/usr/bin/env bash
#
# Extract and Display ONLY the [VERBOSE] Sections
#
# This script filters out all logging messages and shows ONLY
# the [VERBOSE] formatted output that you want to see.
#

PROMPT="${1:-what is 2+2}"

echo "Running: ultrathinkc \"$PROMPT\" --verbose"
echo ""
echo "Extracting VERBOSE sections..."
echo ""
echo "=================================================================================="

# Run ultrathinkc and filter to show ONLY [VERBOSE] lines and section headers
ultrathinkc "$PROMPT" --verbose 2>/dev/null | grep -E "^(\[VERBOSE\]|═{20}|🔥|📊|📤|✅ ULTRATHINK)"

echo ""
echo "=================================================================================="
echo ""
echo "✅ VERBOSE sections extracted successfully"
echo ""
echo "To save to file: $0 \"$PROMPT\" > output.txt"
