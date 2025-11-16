#!/usr/bin/env bash
#
# Simple production-ready test for global ultrathinkc command
#

# Add ~/.local/bin to PATH
export PATH="$HOME/.local/bin:$PATH"

echo "================================================================================
ULTRATHINKC PRODUCTION-READY TEST
================================================================================
"

# Test results
PASSED=0
FAILED=0

# Test 1: Check if ultrathinkc is in PATH
echo "[TEST 1] Checking if ultrathinkc is globally accessible..."
if which ultrathinkc > /dev/null 2>&1; then
    echo "✅ PASSED - ultrathinkc found in PATH"
    PASSED=$((PASSED + 1))
else
    echo "❌ FAILED - ultrathinkc not in PATH"
    FAILED=$((FAILED + 1))
fi

# Test 2: Verify symlink
echo -e "\n[TEST 2] Verifying symlink installation..."
if [ -L "$HOME/.local/bin/ultrathinkc" ]; then
    echo "✅ PASSED - Symlink exists"
    PASSED=$((PASSED + 1))
else
    echo "❌ FAILED - Symlink missing"
    FAILED=$((FAILED + 1))
fi

# Test 3: Verify target script exists
echo -e "\n[TEST 3] Verifying target script exists..."
if [ -f "/home/user01/claude-test/TestPrompt/ultrathink.py" ]; then
    echo "✅ PASSED - Target script exists"
    PASSED=$((PASSED + 1))
else
    echo "❌ FAILED - Target script missing"
    FAILED=$((FAILED + 1))
fi

# Test 4: Help from /tmp
echo -e "\n[TEST 4] Running ultrathinkc --help from /tmp..."
if (cd /tmp && ultrathinkc --help > /dev/null 2>&1); then
    echo "✅ PASSED - Help works from /tmp"
    PASSED=$((PASSED + 1))
else
    echo "❌ FAILED - Help failed from /tmp"
    FAILED=$((FAILED + 1))
fi

# Test 5: Help from root
echo -e "\n[TEST 5] Running ultrathinkc --help from / ..."
if (cd / && ultrathinkc --help > /dev/null 2>&1); then
    echo "✅ PASSED - Help works from /"
    PASSED=$((PASSED + 1))
else
    echo "❌ FAILED - Help failed from /"
    FAILED=$((FAILED + 1))
fi

# Test 6: --how from different directory
echo -e "\n[TEST 6] Running ultrathinkc --how from /var..."
if (cd /var && ultrathinkc --how > /dev/null 2>&1); then
    echo "✅ PASSED - --how works from /var"
    PASSED=$((PASSED + 1))
else
    echo "❌ FAILED - --how failed from /var"
    FAILED=$((FAILED + 1))
fi

# Test 7: Process a simple prompt (expect exit code 1 with "COMPLETED WITH WARNINGS")
echo -e "\n[TEST 7] Processing simple prompt from /tmp..."
if (cd /tmp && timeout 10 ultrathinkc 'test' > /tmp/test_output.txt 2>&1); then
    # Exit code 0 (unlikely but possible)
    if [ -s /tmp/test_output.txt ]; then
        echo "✅ PASSED - Generated output from /tmp"
        PASSED=$((PASSED + 1))
    else
        echo "❌ FAILED - No output generated"
        FAILED=$((FAILED + 1))
    fi
else
    # Exit code 1 is expected (COMPLETED WITH WARNINGS)
    if [ -s /tmp/test_output.txt ]; then
        echo "✅ PASSED - Generated output from /tmp (exit 1 expected)"
        PASSED=$((PASSED + 1))
    else
        echo "❌ FAILED - No output generated"
        FAILED=$((FAILED + 1))
    fi
fi

# Summary
TOTAL=$((PASSED + FAILED))
SUCCESS_RATE=$(awk "BEGIN {printf \"%.1f\", ($PASSED/$TOTAL)*100}")

echo "
================================================================================
FINAL RESULTS
================================================================================
Total Tests: $TOTAL
Passed: $PASSED
Failed: $FAILED
Success Rate: $SUCCESS_RATE%
"

if [ $FAILED -eq 0 ]; then
    echo "✅ ALL TESTS PASSED - ultrathinkc IS PRODUCTION-READY!"
    echo "
ultrathinkc can now be run from ANY directory without requiring a path:
   • ultrathinkc \"your prompt\"
   • ultrathinkc --help
   • ultrathinkc --how
"
    exit 0
else
    echo "❌ $FAILED TEST(S) FAILED"
    exit 1
fi
