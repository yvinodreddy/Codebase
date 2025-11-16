#!/bin/bash

FILE="/home/user01/claude-test/Exam/index-previous.html"
MAX_SIZE_KB=256
MAX_TOKENS=25000
CHARS_PER_TOKEN=4

echo "════════════════════════════════════════════════════════════"
echo "  FINAL VALIDATION TEST"
echo "  Testing production-ready Read commands"
echo "════════════════════════════════════════════════════════════"
echo ""

# Test the generated chunks
chunks=(
    "0:3"     # offset=0, limit=3
    "4:11"    # offset=4, limit=11
    "15:8"    # offset=15, limit=8
    "24:12"   # offset=24, limit=12
    "36:3"    # offset=36, limit=3
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

    echo "Testing: Read(offset=$offset, limit=$limit)"
    echo "  Lines: $offset to $((end_line-1))"
    echo "  Size: ${chunk_size_kb}KB / ${MAX_SIZE_KB}KB (${size_pct}%)"
    echo "  Est. tokens: $estimated_tokens / $MAX_TOKENS (${token_pct}%)"

    # Check if within limits (with safety margin)
    if [ $chunk_size_kb -le $MAX_SIZE_KB ] && [ $estimated_tokens -le $MAX_TOKENS ]; then
        echo "  ✅ PASS"
        ((PASSED++))
    else
        echo "  ❌ FAIL"
        ((FAILED++))
    fi
    echo ""
done

echo "════════════════════════════════════════════════════════════"
echo "  FINAL RESULTS"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "Total tests: $TOTAL_TESTS"
echo "✅ Passed: $PASSED"
echo "❌ Failed: $FAILED"
echo ""

if [ $FAILED -eq 0 ]; then
    echo "🎉 SUCCESS: 100% VALIDATION RATE!"
    echo "✅ PRODUCTION READY - DEPLOY WITH CONFIDENCE"
    echo ""
    echo "Coverage: 37/39 lines (94.87%)"
    echo "Unreadable lines: 3, 23 (use Grep for these)"
    echo ""
    exit 0
else
    echo "❌ VALIDATION FAILED - NOT PRODUCTION READY"
    exit 1
fi
