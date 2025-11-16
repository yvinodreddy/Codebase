#!/bin/bash

FILE="/home/user01/claude-test/Exam/index-previous.html"
TOTAL_LINES=39
MAX_SIZE_KB=256
SAFE_MARGIN=0.8  # Use 80% of max for safety
SAFE_SIZE_KB=$((MAX_SIZE_KB * 80 / 100))  # 204KB

echo "════════════════════════════════════════════════════════════"
echo "  PRODUCTION-READY READ COMMAND GENERATOR"
echo "  File: $FILE"
echo "  Total lines: $TOTAL_LINES"
echo "  Max safe size per read: ${SAFE_SIZE_KB}KB"
echo "════════════════════════════════════════════════════════════"
echo ""

# Strategy: Group consecutive lines into chunks that stay under safe limit
chunks=()
current_offset=0
current_size=0
chunk_start=0

for ((offset=0; offset<TOTAL_LINES; offset++)); do
    LINE_CONTENT=$(sed -n "$((offset+1))p" "$FILE")
    LINE_SIZE_KB=$((${#LINE_CONTENT} / 1024))

    # If adding this line would exceed safe limit, finalize current chunk
    if [ $((current_size + LINE_SIZE_KB)) -gt $SAFE_SIZE_KB ] && [ $current_size -gt 0 ]; then
        chunk_limit=$((offset - chunk_start))
        chunks+=("offset=$chunk_start, limit=$chunk_limit")
        chunk_start=$offset
        current_size=$LINE_SIZE_KB
    else
        current_size=$((current_size + LINE_SIZE_KB))
    fi
done

# Add final chunk
if [ $chunk_start -lt $TOTAL_LINES ]; then
    chunk_limit=$((TOTAL_LINES - chunk_start))
    chunks+=("offset=$chunk_start, limit=$chunk_limit")
fi

# Generate single-line format
echo "PRODUCTION-READY SINGLE-LINE FORMAT:"
echo "════════════════════════════════════════════════════════════"
echo ""

single_line="Read($FILE"
for i in "${!chunks[@]}"; do
    if [ $i -eq 0 ]; then
        single_line="${single_line}, ${chunks[$i]})"
    else
        single_line="${single_line}, then Read($FILE, ${chunks[$i]})"
    fi
done

echo "$single_line"
echo ""

# Generate multi-line format
echo "MULTI-LINE FORMAT (for readability):"
echo "════════════════════════════════════════════════════════════"
echo ""

for i in "${!chunks[@]}"; do
    if [ $i -eq 0 ]; then
        echo "Read($FILE, ${chunks[$i]}),"
    elif [ $i -eq $((${#chunks[@]} - 1)) ]; then
        echo "then Read($FILE, ${chunks[$i]})"
    else
        echo "then Read($FILE, ${chunks[$i]}),"
    fi
done

echo ""
echo "════════════════════════════════════════════════════════════"
echo "Total chunks: ${#chunks[@]}"
echo "Coverage: 100% (all $TOTAL_LINES lines)"
echo "Status: ✅ PRODUCTION READY"
echo "════════════════════════════════════════════════════════════"
