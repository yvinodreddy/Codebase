#!/bin/bash

# Script to generate Read commands for large files
# Usage: ./read_large_file.sh <filename> [chunk_size]
#
# PRODUCTION-READY VERSION - Automatically determines optimal chunk size

if [ -z "$1" ]; then
    echo "Usage: ./read_large_file.sh <filename> [chunk_size]"
    echo "Example: ./read_large_file.sh pagesource.txt 300"
    echo ""
    echo "If chunk_size is not provided, it will be auto-calculated based on file size"
    exit 1
fi

FILENAME="$1"

# Auto-calculate optimal chunk size if not provided
if [ -z "$2" ]; then
    TOTAL_LINES=$(wc -l < "$FILENAME" 2>/dev/null || echo "0")
    FILE_SIZE=$(stat -f%z "$FILENAME" 2>/dev/null || stat -c%s "$FILENAME" 2>/dev/null || echo "0")

    # Calculate average bytes per line
    if [ $TOTAL_LINES -gt 0 ]; then
        AVG_BYTES_PER_LINE=$((FILE_SIZE / TOTAL_LINES))
    else
        AVG_BYTES_PER_LINE=100
    fi

    # Read tool limits: 256KB = 262144 bytes, 25000 tokens
    # Safe limit: use 50KB to account for token overhead and line size variance
    # Using 20% of max to be ULTRA conservative for files with variable line lengths
    # This is especially important for minified HTML/JS/CSS with extremely long lines
    MAX_SAFE_BYTES=51200

    # Calculate chunk size to stay under limits
    CHUNK_SIZE=$((MAX_SAFE_BYTES / AVG_BYTES_PER_LINE))

    # Ensure minimum of 1, maximum of 500
    if [ $CHUNK_SIZE -lt 1 ]; then
        CHUNK_SIZE=1
    elif [ $CHUNK_SIZE -gt 500 ]; then
        CHUNK_SIZE=500
    fi

    # Extra safety: if file has very long lines (avg > 50KB), force chunk size to 1
    if [ $AVG_BYTES_PER_LINE -gt 51200 ]; then
        CHUNK_SIZE=1
    fi
else
    CHUNK_SIZE="$2"
fi

# Check if file exists
if [ ! -f "$FILENAME" ]; then
    echo "Error: File '$FILENAME' not found!"
    exit 1
fi

# Get total line count
TOTAL_LINES=$(wc -l < "$FILENAME")

NUM_CHUNKS=$(( (TOTAL_LINES + CHUNK_SIZE - 1) / CHUNK_SIZE ))
FILE_SIZE_HUMAN=$(ls -lh "$FILENAME" | awk '{print $5}')
AUTO_CALC_MSG=""
if [ -z "$2" ]; then
    AUTO_CALC_MSG=" (auto-calculated)"
fi

echo "════════════════════════════════════════════════════════════"
echo "  READ COMMAND GENERATOR FOR LARGE FILES"
echo "  PRODUCTION-READY VERSION v2.0"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "File: $FILENAME"
echo "Total Lines: $TOTAL_LINES"
echo "File Size: $FILE_SIZE_HUMAN"
echo "Chunk Size: $CHUNK_SIZE lines$AUTO_CALC_MSG"
echo "Number of Chunks: $NUM_CHUNKS"
echo ""
echo "════════════════════════════════════════════════════════════"
echo "  MULTI-LINE FORMAT (FOR READABILITY):"
echo "════════════════════════════════════════════════════════════"
echo ""

# Generate Read commands with absolute path
ABS_PATH=$(cd "$(dirname "$FILENAME")" && pwd)/$(basename "$FILENAME")
offset=0
chunk_num=1

while [ $offset -lt $TOTAL_LINES ]; do
    # Calculate remaining lines
    remaining=$((TOTAL_LINES - offset))

    # Use chunk size or remaining lines, whichever is smaller
    if [ $remaining -lt $CHUNK_SIZE ]; then
        limit=$remaining
    else
        limit=$CHUNK_SIZE
    fi

    # Generate Read command with absolute path
    echo "Read($ABS_PATH, offset=$offset, limit=$limit)"

    # Increment offset
    offset=$((offset + limit))
    chunk_num=$((chunk_num + 1))
done

echo ""
echo "════════════════════════════════════════════════════════════"
echo "  SINGLE-LINE FORMAT (COPY THIS):"
echo "════════════════════════════════════════════════════════════"
echo ""

# Generate single-line format with absolute path
offset=0
commands=""

while [ $offset -lt $TOTAL_LINES ]; do
    remaining=$((TOTAL_LINES - offset))

    if [ $remaining -lt $CHUNK_SIZE ]; then
        limit=$remaining
    else
        limit=$CHUNK_SIZE
    fi

    if [ -z "$commands" ]; then
        commands="Read($ABS_PATH, offset=$offset, limit=$limit)"
    else
        commands="$commands, then Read($ABS_PATH, offset=$offset, limit=$limit)"
    fi

    offset=$((offset + limit))
done

echo "$commands"

echo ""
echo "════════════════════════════════════════════════════════════"
echo "  USAGE INSTRUCTIONS:"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "1. Copy the SINGLE-LINE FORMAT above"
echo "2. Paste it into your Claude prompt"
echo "3. Claude will execute all reads sequentially"
echo ""
echo "════════════════════════════════════════════════════════════"
echo "  TROUBLESHOOTING:"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "❌ ERROR: 'File content exceeds maximum allowed size (256KB)'"
echo "   FIX: Reduce chunk size. Try: $0 $FILENAME 1"
echo ""
echo "❌ ERROR: 'File content exceeds maximum allowed tokens (25000)'"
echo "   FIX: Reduce chunk size. Try: $0 $FILENAME 1"
echo ""
echo "✓ SAFE: Using chunk size of $CHUNK_SIZE lines per read"
echo "✓ COVERAGE: All $TOTAL_LINES lines will be read"
echo ""
