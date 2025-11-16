#!/bin/bash
echo "=============================================="
echo "ISOLATION VERIFICATION SCRIPT"
echo "=============================================="
echo ""

echo "TEST 1: Check ClaudePrompt for TestPrompt references"
echo "----------------------------------------------"
cd /home/user01/claude-test/ClaudePrompt
FOUND=$(grep -r "TestPrompt" --include="*.py" --include="*.md" --exclude="*.backup" . 2>/dev/null | wc -l)
if [ $FOUND -eq 0 ]; then
    echo "✅ PASS: No TestPrompt references in ClaudePrompt"
else
    echo "❌ FAIL: Found $FOUND references to TestPrompt"
    grep -r "TestPrompt" --include="*.py" --include="*.md" --exclude="*.backup" . | head -10
fi
echo ""

echo "TEST 2: Verify cpp command exists and is executable"
echo "----------------------------------------------"
if [ -x /home/user01/claude-test/ClaudePrompt/cpp ]; then
    echo "✅ PASS: cpp command is executable"
else
    echo "❌ FAIL: cpp command not found or not executable"
fi
echo ""

echo "TEST 3: Verify TestPrompt still has ultrathinkc"
echo "----------------------------------------------"
if [ -x /home/user01/claude-test/TestPrompt/ultrathinkc ]; then
    echo "✅ PASS: ultrathinkc still exists in TestPrompt"
else
    echo "❌ FAIL: ultrathinkc missing from TestPrompt"
fi
echo ""

echo "TEST 4: Verify separate log directories"
echo "----------------------------------------------"
if [ -d /home/user01/claude-test/TestPrompt/logs ] && [ -d /home/user01/claude-test/ClaudePrompt/logs ]; then
    echo "✅ PASS: Both log directories exist separately"
else
    echo "❌ FAIL: Log directory missing"
fi
echo ""

echo "TEST 5: Check config.py differences"
echo "----------------------------------------------"
DIFF=$(diff /home/user01/claude-test/TestPrompt/config.py /home/user01/claude-test/ClaudePrompt/config.py 2>/dev/null | grep -c "ClaudePrompt")
if [ $DIFF -gt 0 ]; then
    echo "✅ PASS: config.py files are different (ClaudePrompt references found)"
    echo "   Found $DIFF differences related to ClaudePrompt"
else
    echo "⚠️  WARNING: config.py files appear identical"
fi
echo ""

echo "TEST 6: Run functional test on both"
echo "----------------------------------------------"
cd /home/user01/claude-test/TestPrompt
timeout 30 ./ultrathinkc "test" > /tmp/isolation_test_tp.txt 2>&1
TP_RESULT=$?

cd /home/user01/claude-test/ClaudePrompt
timeout 30 ./cpp "test" > /tmp/isolation_test_cp.txt 2>&1
CP_RESULT=$?

if [ $TP_RESULT -eq 0 ]; then
    echo "✅ PASS: TestPrompt (uc) command works"
elif [ $TP_RESULT -eq 124 ]; then
    echo "⚠️  TIMEOUT: TestPrompt took >30s (may still work)"
else
    echo "❌ FAIL: TestPrompt (uc) command failed with code $TP_RESULT"
fi

if [ $CP_RESULT -eq 0 ]; then
    echo "✅ PASS: ClaudePrompt (cpp) command works"
elif [ $CP_RESULT -eq 124 ]; then
    echo "⚠️  TIMEOUT: ClaudePrompt took >30s (may still work)"
else
    echo "❌ FAIL: ClaudePrompt (cpp) command failed with code $CP_RESULT"
fi
echo ""

echo "TEST 7: Check for cross-contamination in output"
echo "----------------------------------------------"
TP_CONTAM=$(grep -i "claudeprompt" /tmp/isolation_test_tp.txt 2>/dev/null | wc -l)
CP_CONTAM=$(grep -i "testprompt" /tmp/isolation_test_cp.txt 2>/dev/null | wc -l)

if [ $TP_CONTAM -eq 0 ]; then
    echo "✅ PASS: No ClaudePrompt references in TestPrompt output"
else
    echo "❌ FAIL: Found $TP_CONTAM ClaudePrompt references in TestPrompt output"
fi

if [ $CP_CONTAM -eq 0 ]; then
    echo "✅ PASS: No TestPrompt references in ClaudePrompt output"
else
    echo "❌ FAIL: Found $CP_CONTAM TestPrompt references in ClaudePrompt output"
fi
echo ""

echo "TEST 8: Verify separate output file paths"
echo "----------------------------------------------"
# Check that ClaudePrompt documentation uses cppultrathink_output.txt
CPP_OUTPUT_REFS=$(grep -r "cppultrathink_output\.txt" /home/user01/claude-test/ClaudePrompt --include="*.md" --include="*.py" 2>/dev/null | wc -l)
# Check that TestPrompt still uses ultrathink_output.txt (not cpp version)
TP_OUTPUT_REFS=$(grep -r "ultrathink_output\.txt" /home/user01/claude-test/TestPrompt --include="*.md" --include="*.py" 2>/dev/null | grep -v "cppultrathink" | wc -l)

if [ $CPP_OUTPUT_REFS -gt 0 ]; then
    echo "✅ PASS: ClaudePrompt uses cppultrathink_output.txt ($CPP_OUTPUT_REFS references)"
else
    echo "⚠️  WARNING: ClaudePrompt may not have output file path configured"
fi

if [ $TP_OUTPUT_REFS -gt 0 ]; then
    echo "✅ PASS: TestPrompt uses ultrathink_output.txt ($TP_OUTPUT_REFS references)"
else
    echo "⚠️  WARNING: TestPrompt may not have output file path configured"
fi

# Verify the actual output files are separate
if [ -f /tmp/cppultrathink_output.txt ] && [ -f /tmp/ultrathink_output.txt ]; then
    echo "✅ PASS: Both output files exist and are separate"
    echo "   - /tmp/ultrathink_output.txt ($(wc -l < /tmp/ultrathink_output.txt) lines)"
    echo "   - /tmp/cppultrathink_output.txt ($(wc -l < /tmp/cppultrathink_output.txt) lines)"
else
    echo "ℹ️  INFO: Output files not yet created (run cpp and uc commands first)"
fi
echo ""

echo "=============================================="
echo "ISOLATION VERIFICATION COMPLETE"
echo "=============================================="
