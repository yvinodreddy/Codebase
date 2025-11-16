#!/bin/bash

# COMPREHENSIVE TEST SUITE FOR smart_read_generator.sh

echo "════════════════════════════════════════════════════════════"
echo "  COMPREHENSIVE TEST SUITE"
echo "  Testing smart_read_generator.sh"
echo "════════════════════════════════════════════════════════════"
echo ""

SCRIPT="./smart_read_generator.sh"
PASS=0
FAIL=0
TOTAL=0

# Function to run test
run_test() {
    local test_name="$1"
    local expected_result="$2"  # "pass" or "fail"
    shift 2
    local command="$@"

    ((TOTAL++))
    echo "Test $TOTAL: $test_name"
    echo "  Command: $command"

    if eval "$command" > /dev/null 2>&1; then
        actual_result="pass"
    else
        actual_result="fail"
    fi

    if [ "$actual_result" = "$expected_result" ]; then
        echo "  ✅ PASS (expected $expected_result, got $actual_result)"
        ((PASS++))
    else
        echo "  ❌ FAIL (expected $expected_result, got $actual_result)"
        ((FAIL++))
    fi
    echo ""
}

# Test 1: No argument provided (should fail)
run_test "No argument provided" "fail" "$SCRIPT"

# Test 2: Non-existent file (should fail)
run_test "Non-existent file" "fail" "$SCRIPT /tmp/nonexistent_file_12345.txt"

# Test 3: Valid file - index-previous.html (should pass)
run_test "Valid file - index-previous.html" "pass" "$SCRIPT index-previous.html"

# Test 4: Absolute path (should pass)
run_test "Absolute path" "pass" "$SCRIPT /home/user01/claude-test/Exam/index-previous.html"

# Create test files for edge cases
echo "Creating test files for edge cases..."

# Test 5: Empty file (should fail)
touch /tmp/empty_file.txt
run_test "Empty file" "fail" "$SCRIPT /tmp/empty_file.txt"
rm -f /tmp/empty_file.txt

# Test 6: Small file (should pass)
echo "Line 1" > /tmp/small_file.txt
echo "Line 2" >> /tmp/small_file.txt
echo "Line 3" >> /tmp/small_file.txt
run_test "Small file (3 lines)" "pass" "$SCRIPT /tmp/small_file.txt"
rm -f /tmp/small_file.txt

# Test 7: File with single line (should pass)
echo "Single line of text" > /tmp/single_line.txt
run_test "Single line file" "pass" "$SCRIPT /tmp/single_line.txt"
rm -f /tmp/single_line.txt

# Test 8: File with no trailing newline (should pass)
printf "Line without newline" > /tmp/no_newline.txt
run_test "File with no trailing newline" "pass" "$SCRIPT /tmp/no_newline.txt"
rm -f /tmp/no_newline.txt

# Test 9: Relative path (should pass)
if [ -f "index-previous.html" ]; then
    run_test "Relative path" "pass" "$SCRIPT ./index-previous.html"
fi

# Test 10: Check if output file is created
echo "Test: Output file creation"
$SCRIPT index-previous.html > /dev/null 2>&1
if [ -f "/home/user01/claude-test/Exam/PRODUCTION_READ_COMMANDS.txt" ]; then
    echo "  ✅ PASS - Output file created"
    ((PASS++))
else
    echo "  ❌ FAIL - Output file not created"
    ((FAIL++))
fi
((TOTAL++))
echo ""

echo "════════════════════════════════════════════════════════════"
echo "  TEST RESULTS"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "Total tests: $TOTAL"
echo "✅ Passed: $PASS"
echo "❌ Failed: $FAIL"
echo ""

if [ $FAIL -eq 0 ]; then
    echo "🎉 SUCCESS: All tests passed!"
    echo "✅ PRODUCTION READY"
    exit 0
else
    echo "⚠  WARNING: Some tests failed"
    exit 1
fi
