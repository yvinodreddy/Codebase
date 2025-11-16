#!/bin/bash

echo "════════════════════════════════════════════════════════════"
echo "  COMPREHENSIVE READ VALIDATION TEST"
echo "════════════════════════════════════════════════════════════"
echo ""

FILE="$1"
if [ -z "$FILE" ]; then
    echo "Usage: $0 <filename>"
    exit 1
fi

TOTAL_LINES=$(wc -l < "$FILE")
echo "Testing file: $FILE"
echo "Total lines: $TOTAL_LINES"
echo ""

# Test different chunk sizes
for CHUNK_SIZE in 1 2 3 5 10; do
    echo "Testing chunk size: $CHUNK_SIZE lines..."
    
    # Generate test with bash script
    bash /home/user01/claude-test/Exam/read_large_file.sh "$FILE" $CHUNK_SIZE > /tmp/test_output_${CHUNK_SIZE}.txt 2>&1
    
    # Count how many Read commands were generated
    NUM_COMMANDS=$(grep -c "^Read(" /tmp/test_output_${CHUNK_SIZE}.txt)
    echo "  Generated $NUM_COMMANDS read commands"
    
    # Verify coverage
    EXPECTED_COMMANDS=$(( (TOTAL_LINES + CHUNK_SIZE - 1) / CHUNK_SIZE ))
    if [ $NUM_COMMANDS -eq $EXPECTED_COMMANDS ]; then
        echo "  ✓ Coverage verified: $NUM_COMMANDS commands cover all $TOTAL_LINES lines"
    else
        echo "  ✗ Coverage mismatch: expected $EXPECTED_COMMANDS, got $NUM_COMMANDS"
    fi
    echo ""
done

echo "════════════════════════════════════════════════════════════"
echo "  RECOMMENDATION FOR index-previous.html:"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "Based on file analysis:"
echo "- File size: 447KB"
echo "- Total lines: $TOTAL_LINES"
echo "- Avg bytes/line: $((457728 / TOTAL_LINES)) bytes"
echo ""
echo "✓ SAFEST: Use chunk size of 1 line (guaranteed to work)"
echo "⚠ RISKY: Larger chunks may exceed 256KB limit due to uneven line sizes"
echo ""
