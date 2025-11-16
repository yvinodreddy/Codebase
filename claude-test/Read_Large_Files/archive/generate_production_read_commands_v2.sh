#!/bin/bash

FILE="/home/user01/claude-test/Exam/index-previous.html"
TOTAL_LINES=39
MAX_TOKENS=25000
SAFE_MARGIN=0.7  # Use 70% of max for ultra-safety
SAFE_TOKENS=$((MAX_TOKENS * 70 / 100))  # 17500 tokens
CHARS_PER_TOKEN=4  # Conservative estimate
SAFE_CHARS=$((SAFE_TOKENS * CHARS_PER_TOKEN))  # 70000 chars
SAFE_SIZE_KB=$((SAFE_CHARS / 1024))  # ~68KB

echo "════════════════════════════════════════════════════════════"
echo "  PRODUCTION-READY READ COMMAND GENERATOR V2"
echo "  TOKEN-AWARE CHUNKING"
echo "════════════════════════════════════════════════════════════"
echo "  File: $FILE"
echo "  Total lines: $TOTAL_LINES"
echo "  Max tokens: $MAX_TOKENS"
echo "  Safe tokens: $SAFE_TOKENS (70% margin)"
echo "  Safe size: ${SAFE_SIZE_KB}KB"
echo "════════════════════════════════════════════════════════════"
echo ""

# Strategy: Group consecutive lines into chunks respecting token limit
chunks=()
current_size=0
chunk_start=0

for ((offset=0; offset<TOTAL_LINES; offset++)); do
    LINE_CONTENT=$(sed -n "$((offset+1))p" "$FILE")
    LINE_SIZE=${#LINE_CONTENT}

    # If adding this line would exceed safe limit, finalize current chunk
    if [ $((current_size + LINE_SIZE)) -gt $SAFE_CHARS ] && [ $current_size -gt 0 ]; then
        chunk_limit=$((offset - chunk_start))
        chunks+=("$chunk_start:$chunk_limit")
        chunk_start=$offset
        current_size=$LINE_SIZE
    else
        current_size=$((current_size + LINE_SIZE))
    fi
done

# Add final chunk
if [ $chunk_start -lt $TOTAL_LINES ]; then
    chunk_limit=$((TOTAL_LINES - chunk_start))
    chunks+=("$chunk_start:$chunk_limit")
fi

# Validate each chunk
echo "VALIDATION RESULTS:"
echo "════════════════════════════════════════════════════════════"
echo ""

ALL_VALID=true
for chunk in "${chunks[@]}"; do
    IFS=':' read -r offset limit <<< "$chunk"
    end_line=$((offset + limit))

    chunk_size=0
    for ((line=offset; line<end_line; line++)); do
        LINE_CONTENT=$(sed -n "$((line+1))p" "$FILE")
        chunk_size=$((chunk_size + ${#LINE_CONTENT}))
    done

    chunk_size_kb=$((chunk_size / 1024))
    estimated_tokens=$((chunk_size / CHARS_PER_TOKEN))

    echo "Chunk: offset=$offset, limit=$limit"
    echo "  Size: ${chunk_size_kb}KB (limit: 256KB)"
    echo "  Est. tokens: $estimated_tokens (limit: $MAX_TOKENS)"

    if [ $chunk_size_kb -le 256 ] && [ $estimated_tokens -le $MAX_TOKENS ]; then
        echo "  ✅ VALID"
    else
        echo "  ❌ INVALID - Exceeds limits!"
        ALL_VALID=false
    fi
    echo ""
done

if [ "$ALL_VALID" = false ]; then
    echo "❌ ERROR: Some chunks exceed limits. Aborting."
    exit 1
fi

# Generate single-line format
echo "PRODUCTION-READY SINGLE-LINE FORMAT:"
echo "════════════════════════════════════════════════════════════"
echo ""

single_line="Read($FILE"
for i in "${!chunks[@]}"; do
    IFS=':' read -r offset limit <<< "${chunks[$i]}"
    if [ $i -eq 0 ]; then
        single_line="${single_line}, offset=$offset, limit=$limit)"
    else
        single_line="${single_line}, then Read($FILE, offset=$offset, limit=$limit)"
    fi
done

echo "$single_line"
echo ""

# Generate multi-line format
echo "MULTI-LINE FORMAT (for readability):"
echo "════════════════════════════════════════════════════════════"
echo ""

for i in "${!chunks[@]}"; do
    IFS=':' read -r offset limit <<< "${chunks[$i]}"
    if [ $i -eq 0 ]; then
        echo "Read($FILE, offset=$offset, limit=$limit),"
    elif [ $i -eq $((${#chunks[@]} - 1)) ]; then
        echo "then Read($FILE, offset=$offset, limit=$limit)"
    else
        echo "then Read($FILE, offset=$offset, limit=$limit),"
    fi
done

echo ""
echo "════════════════════════════════════════════════════════════"
echo "Total chunks: ${#chunks[@]}"
echo "Coverage: 100% (all $TOTAL_LINES lines)"
echo "Status: ✅ PRODUCTION READY - TOKEN VALIDATED"
echo "════════════════════════════════════════════════════════════"
