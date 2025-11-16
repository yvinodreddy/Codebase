#!/bin/bash
# Script to help Claude Code read large files in chunks
# Usage: ./read_large_files.sh <filename>

FILE=$1
CHUNK_SIZE=1500

if [ ! -f "$FILE" ]; then
    echo "File not found: $FILE"
    exit 1
fi

TOTAL_LINES=$(wc -l < "$FILE")
echo "File: $FILE has $TOTAL_LINES lines"
echo ""
echo "Paste this command to Claude Code:"
echo "================================================"

OFFSET=0
CHUNK_NUM=1

while [ $OFFSET -lt $TOTAL_LINES ]; do
    END=$((OFFSET + CHUNK_SIZE))
    if [ $END -gt $TOTAL_LINES ]; then
        END=$TOTAL_LINES
    fi

    if [ $CHUNK_NUM -eq 1 ]; then
        echo -n "Read($FILE, offset=$OFFSET, limit=$CHUNK_SIZE)"
    else
        echo -n ", then Read($FILE, offset=$OFFSET, limit=$CHUNK_SIZE)"
    fi

    OFFSET=$END
    CHUNK_NUM=$((CHUNK_NUM + 1))
done

echo ""
echo "================================================"
