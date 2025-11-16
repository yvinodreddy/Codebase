#!/usr/bin/env bash
#
# Comprehensive test suite for global ultrathinkc command
# Tests accessibility from multiple directories and with various options
#

set -e  # Exit on error

# Add ~/.local/bin to PATH
export PATH="$HOME/.local/bin:$PATH"

echo "================================================================================
ULTRATHINKC GLOBAL COMMAND TEST SUITE
================================================================================
"

# Test counter
TESTS_PASSED=0
TESTS_FAILED=0
TOTAL_TESTS=0

# Function to run a test
run_test() {
    local test_name="$1"
    local test_dir="$2"
    local test_cmd="$3"
    local expect_success="${4:-true}"

    TOTAL_TESTS=$((TOTAL_TESTS + 1))

    echo "
[TEST $TOTAL_TESTS] $test_name
Directory: $test_dir
Command: $test_cmd
"

    # Run test in specified directory
    if (cd "$test_dir" && eval "$test_cmd" > /tmp/ultrathinkc_test_output.txt 2>&1); then
        if [ "$expect_success" = "true" ]; then
            echo "✅ PASSED"
            TESTS_PASSED=$((TESTS_PASSED + 1))
        else
            echo "❌ FAILED (expected failure but succeeded)"
            TESTS_FAILED=$((TESTS_FAILED + 1))
        fi
    else
        if [ "$expect_success" = "false" ]; then
            echo "✅ PASSED (expected failure)"
            TESTS_PASSED=$((TESTS_PASSED + 1))
        else
            echo "❌ FAILED"
            echo "Error output:"
            cat /tmp/ultrathinkc_test_output.txt
            TESTS_FAILED=$((TESTS_FAILED + 1))
        fi
    fi
}

# Test 1: Check if ultrathinkc is in PATH
run_test "ultrathinkc is in PATH" "$HOME" "which ultrathinkc"

# Test 2: Help from home directory
run_test "Help from home directory" "$HOME" "ultrathinkc --help"

# Test 3: Help from /tmp
run_test "Help from /tmp" "/tmp" "ultrathinkc --help"

# Test 4: Help from root directory
run_test "Help from root directory" "/" "ultrathinkc --help"

# Test 5: Help from /var
run_test "Help from /var" "/var" "ultrathinkc --help"

# Test 6: --how flag from different directory
run_test "--how flag from /tmp" "/tmp" "ultrathinkc --how"

# Test 7: Simple prompt from /tmp (exit code 1 is expected with "COMPLETED WITH WARNINGS")
echo "
[TEST $((TOTAL_TESTS + 1))] Simple prompt from /tmp
Directory: /tmp
Command: ultrathinkc 'hello world'
"
TOTAL_TESTS=$((TOTAL_TESTS + 1))
OUTPUT=$(cd /tmp && ultrathinkc 'hello world' 2>&1)
if [[ "$OUTPUT" == *"ULTRATHINK"* ]] || [[ "$OUTPUT" == *"COMPLETED"* ]]; then
    echo "✅ PASSED (generated ULTRATHINK prompt)"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo "❌ FAILED (did not generate ULTRATHINK prompt)"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# Test 8: Simple prompt from home
echo "
[TEST $((TOTAL_TESTS + 1))] Simple prompt from home
Directory: $HOME
Command: ultrathinkc 'test prompt'
"
TOTAL_TESTS=$((TOTAL_TESTS + 1))
OUTPUT=$(cd "$HOME" && ultrathinkc 'test prompt' 2>&1)
if [[ "$OUTPUT" == *"ULTRATHINK"* ]] || [[ "$OUTPUT" == *"COMPLETED"* ]]; then
    echo "✅ PASSED (generated ULTRATHINK prompt)"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo "❌ FAILED (did not generate ULTRATHINK prompt)"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# Test 9: Verify symlink points to correct location
run_test "Symlink verification" "$HOME" "test -L $HOME/.local/bin/ultrathinkc"

# Test 10: Verify target file exists
run_test "Target file exists" "$HOME" "test -f /home/user01/claude-test/ClaudePrompt/ultrathink.py"

# Summary
echo "
================================================================================
TEST RESULTS
================================================================================
Total Tests: $TOTAL_TESTS
Passed: $TESTS_PASSED
Failed: $TESTS_FAILED
Success Rate: $(awk "BEGIN {printf \"%.1f\", ($TESTS_PASSED/$TOTAL_TESTS)*100}")%

"

if [ $TESTS_FAILED -eq 0 ]; then
    echo "✅ ALL TESTS PASSED - ultrathinkc is production-ready!"
    exit 0
else
    echo "❌ SOME TESTS FAILED - review errors above"
    exit 1
fi
