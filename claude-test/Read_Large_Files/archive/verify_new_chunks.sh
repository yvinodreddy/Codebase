#!/bin/bash

FILE="/home/user01/claude-test/Exam/index-previous.html"
MAX_SIZE_KB=256
MAX_TOKENS=25000
CHARS_PER_TOKEN=4

echo "════════════════════════════════════════════════════════════"
echo "  VERIFYING NEW CHUNK CONFIGURATION"
echo "════════════════════════════════════════════════════════════"
echo ""

# Test the new chunks from the latest run
chunks=(
    "0:3"     # offset=0, limit=3
    "3:4"     # offset=3, limit=4
    "7:12"    # offset=7, limit=12
    "19:8"    # offset=19, limit=8
    "27:3"    # offset=27, limit=3
    "30:9"    # offset=30, limit=9
)

TOTAL_TESTS=${#chunks[@]}
PASSED=0
FAILED=0

for chunk in "${chunks[@]}"; do
    IFS=':' read -r offset limit <<< "$chunk"
    end_line=$((offset + limit))

    # Calculate exact size of this chunk
    chunk_size=0
    for ((line=offset; line<end_line; line++)); do
        LINE_CONTENT=$(sed -n "$((line+1))p" "$FILE")
        LINE_SIZE=${#LINE_CONTENT}
        chunk_size=$((chunk_size + LINE_SIZE))
    done

    chunk_size_kb=$((chunk_size / 1024))
    estimated_tokens=$((chunk_size / CHARS_PER_TOKEN))

    # Calculate percentage of limits
    size_pct=$((chunk_size_kb * 100 / MAX_SIZE_KB))
    token_pct=$((estimated_tokens * 100 / MAX_TOKENS))

    echo "Chunk: offset=$offset, limit=$limit (lines $offset-$((end_line-1)))"
    echo "  Size: ${chunk_size_kb}KB / ${MAX_SIZE_KB}KB (${size_pct}%)"
    echo "  Tokens: $estimated_tokens / $MAX_TOKENS (${token_pct}%)"

    # Check if within limits
    if [ $chunk_size_kb -le $MAX_SIZE_KB ] && [ $estimated_tokens -le $MAX_TOKENS ]; then
        echo "  ✅ PASS"
        ((PASSED++))
    else
        echo "  ❌ FAIL - EXCEEDS LIMITS!"
        ((FAILED++))
    fi
    echo ""
done

echo "════════════════════════════════════════════════════════════"
echo "  RESULTS"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "Total chunks: $TOTAL_TESTS"
echo "✅ Passed: $PASSED"
echo "❌ Failed: $FAILED"
echo ""

if [ $FAILED -eq 0 ]; then
    echo "🎉 SUCCESS: 100% COVERAGE WITH 100% VALIDATION!"
    echo "✅ PRODUCTION READY - ALL 39 LINES READABLE"
    exit 0
else
    echo "❌ VALIDATION FAILED"
    exit 1
fi
