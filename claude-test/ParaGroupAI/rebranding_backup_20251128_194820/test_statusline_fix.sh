#!/bin/bash
#
# Comprehensive Statusline Validation Test
# Tests all fixes applied to statusline_with_metrics.sh
#

echo "========================================="
echo "Statusline Fix Validation Test"
echo "========================================="
echo ""

# Test 1: Empty JSON (tests all fallbacks)
echo "Test 1: Empty JSON (should use fallbacks)"
echo "Input: {}"
OUTPUT=$(echo '{}' | ./statusline_with_metrics.sh 2>&1)
echo "Output: $OUTPUT"

# Check for ANSI escape codes (should have ESC character)
if echo "$OUTPUT" | cat -A | grep -q "\^\["; then
    echo "✅ PASS: ANSI escape codes present"
else
    echo "❌ FAIL: ANSI escape codes missing"
fi

# Check for model name (should NOT be "Unknown")
if echo "$OUTPUT" | grep -q "Unknown"; then
    echo "❌ FAIL: Model shows as 'Unknown'"
else
    echo "✅ PASS: Model name is set (not 'Unknown')"
fi

# Check for full directory path (should NOT be just ~)
if echo "$OUTPUT" | grep -q "/home/user01/claude-test/ClaudePrompt"; then
    echo "✅ PASS: Full directory path displayed"
else
    echo "❌ FAIL: Full directory path missing"
fi

# Check for directory name
if echo "$OUTPUT" | grep -q "ClaudePrompt"; then
    echo "✅ PASS: Directory name 'ClaudePrompt' found"
else
    echo "❌ FAIL: Directory name not found"
fi

echo ""
echo "Test 2: JSON with model info"
echo "Input: JSON with model displayName"
TESTJSON='{"model": {"displayName": "Test Model"}, "currentDirectory": "/test/dir"}'
OUTPUT2=$(echo "$TESTJSON" | ./statusline_with_metrics.sh 2>&1)
echo "Output: $OUTPUT2"

if echo "$OUTPUT2" | grep -q "Test Model"; then
    echo "✅ PASS: Model name from JSON used"
else
    echo "❌ FAIL: Model name from JSON not used"
fi

if echo "$OUTPUT2" | grep -q "/test/dir"; then
    echo "✅ PASS: Directory from JSON used"
else
    echo "❌ FAIL: Directory from JSON not used"
fi

echo ""
echo "Test 3: Visual output test (with actual escape codes)"
echo "Running statusline with empty JSON..."
echo '{}' | ./statusline_with_metrics.sh
echo ""

echo "========================================="
echo "Test Complete"
echo "========================================="
