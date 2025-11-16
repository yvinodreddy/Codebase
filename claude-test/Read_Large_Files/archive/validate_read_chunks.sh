#!/bin/bash

FILE="/home/user01/claude-test/Exam/index-previous.html"
MAX_SIZE_KB=256
MAX_TOKENS=25000
SAFE_SIZE_KB=204

echo "════════════════════════════════════════════════════════════"
echo "  COMPREHENSIVE VALIDATION TEST"
echo "  Testing generated Read commands against limits"
echo "════════════════════════════════════════════════════════════"
echo ""

# Test chunks from the generated commands
chunks=(
    "0:15"    # offset=0, limit=15
    "15:14"   # offset=15, limit=14
    "29:10"   # offset=29, limit=10
)

TOTAL_TESTS=${#chunks[@]}
PASSED=0
FAILED=0

for chunk in "${chunks[@]}"; do
    IFS=':' read -r offset limit <<< "$chunk"
    end_line=$((offset + limit))

    # Calculate size of this chunk
    chunk_size=0
    for ((line=offset; line<end_line; line++)); do
        LINE_CONTENT=$(sed -n "$((line+1))p" "$FILE")
        LINE_SIZE=${#LINE_CONTENT}
        chunk_size=$((chunk_size + LINE_SIZE))
    done

    chunk_size_kb=$((chunk_size / 1024))

    # Estimate tokens (rough: 1 token ≈ 4 characters)
    estimated_tokens=$((chunk_size / 4))

    echo "Testing: offset=$offset, limit=$limit"
    echo "  Lines: $offset to $((end_line-1))"
    echo "  Size: ${chunk_size_kb}KB / ${MAX_SIZE_KB}KB limit"
    echo "  Est. tokens: $estimated_tokens / $MAX_TOKENS limit"

    # Check if within limits
    if [ $chunk_size_kb -le $MAX_SIZE_KB ] && [ $estimated_tokens -le $MAX_TOKENS ]; then
        echo "  ✅ PASS - Within all limits"
        ((PASSED++))
    else
        echo "  ❌ FAIL - Exceeds limits!"
        ((FAILED++))
    fi
    echo ""
done

echo "════════════════════════════════════════════════════════════"
echo "  RESULTS:"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "Total tests: $TOTAL_TESTS"
echo "✅ Passed: $PASSED"
echo "❌ Failed: $FAILED"
echo ""

if [ $FAILED -eq 0 ]; then
    echo "🎉 SUCCESS: 100% validation rate!"
    echo "✅ PRODUCTION READY - All chunks are safe"
    exit 0
else
    echo "⚠ WARNING: Some chunks failed validation"
    echo "❌ NOT PRODUCTION READY - Requires adjustment"
    exit 1
fi
