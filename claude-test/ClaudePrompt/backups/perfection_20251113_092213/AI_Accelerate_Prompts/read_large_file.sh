#!/bin/bash

# Script to generate Read commands for large files
# Usage: ./read_large_file.sh <filename> [chunk_size]

if [ -z "$1" ]; then
    echo "Usage: ./read_large_file.sh <filename> [chunk_size]"
    echo "Example: ./read_large_file.sh pagesource.txt 300"
    exit 1
fi

FILENAME="$1"
CHUNK_SIZE="${2:-300}"  # Default 300 lines per chunk

# Check if file exists
if [ ! -f "$FILENAME" ]; then
    echo "Error: File '$FILENAME' not found!"
    exit 1
fi

# Get total line count
TOTAL_LINES=$(wc -l < "$FILENAME")

echo "════════════════════════════════════════════════════════════"
echo "  READ COMMAND GENERATOR FOR LARGE FILES"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "File: $FILENAME"
echo "Total Lines: $TOTAL_LINES"
echo "Chunk Size: $CHUNK_SIZE lines"
echo "Number of Chunks: $(( (TOTAL_LINES + CHUNK_SIZE - 1) / CHUNK_SIZE ))"
echo ""
echo "════════════════════════════════════════════════════════════"
echo "  COPY AND PASTE THE COMMANDS BELOW:"
echo "════════════════════════════════════════════════════════════"
echo ""

# Generate Read commands
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

    # Generate Read command
    echo "Read($FILENAME, offset=$offset, limit=$limit)"

    # Increment offset
    offset=$((offset + limit))
    chunk_num=$((chunk_num + 1))
done

echo ""
echo "════════════════════════════════════════════════════════════"
echo "  SINGLE-LINE FORMAT (for easy copying):"
echo "════════════════════════════════════════════════════════════"
echo ""

# Generate single-line format
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
        commands="Read($FILENAME, offset=$offset, limit=$limit)"
    else
        commands="$commands, then Read($FILENAME, offset=$offset, limit=$limit)"
    fi

    offset=$((offset + limit))
done

echo "$commands"

echo ""
echo "════════════════════════════════════════════════════════════"
echo "  INSTRUCTIONS:"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "1. Copy the single-line format above"
echo "2. Paste it in your prompt to Claude"
echo "3. Claude will read the file in chunks"
echo ""
echo "Example prompt:"
echo "  Please execute: $commands"
echo ""
