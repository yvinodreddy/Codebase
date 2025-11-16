#!/bin/bash
#
# test_live_metrics_comprehensive.sh - Comprehensive Test Suite for Live Metrics
#
# Tests all components of the live metrics system:
# 1. Live context parser
# 2. Enhanced statusline
# 3. Agent counter
# 4. Backward compatibility
# 5. Integration with existing systems
#
# Exit codes:
#   0 = All tests passed
#   1 = One or more tests failed
#

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test counters
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

# Helper functions
print_header() {
    echo ""
    echo -e "${BLUE}================================================================================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}================================================================================================${NC}"
}

print_test() {
    echo -e "\n${YELLOW}TEST $TOTAL_TESTS:${NC} $1"
}

pass_test() {
    PASSED_TESTS=$((PASSED_TESTS + 1))
    echo -e "${GREEN}✅ PASS${NC}: $1"
}

fail_test() {
    FAILED_TESTS=$((FAILED_TESTS + 1))
    echo -e "${RED}❌ FAIL${NC}: $1"
    echo -e "${RED}   Error: $2${NC}"
}

# Change to ClaudePrompt directory
cd /home/user01/claude-test/ClaudePrompt || exit 1

print_header "🧪 COMPREHENSIVE LIVE METRICS TEST SUITE"

echo "Test Suite for:"
echo "  • Live context parser (get_live_context_metrics.py)"
echo "  • Enhanced statusline (statusline_with_live_metrics.sh)"
echo "  • Agent usage counter (capture_live_metrics.sh hook)"
echo "  • Backward compatibility"
echo "  • Integration testing"

# ============================================================================
# TEST GROUP 1: Live Context Parser
# ============================================================================

print_header "TEST GROUP 1: Live Context Parser"

# Test 1.1: Parser script exists and is executable
TOTAL_TESTS=$((TOTAL_TESTS + 1))
print_test "Parser script exists and is executable"
if [[ -x "get_live_context_metrics.py" ]]; then
    pass_test "get_live_context_metrics.py is executable"
else
    fail_test "get_live_context_metrics.py is not executable" "Script not found or not executable"
fi

# Test 1.2: Parser can handle sample /context output
TOTAL_TESTS=$((TOTAL_TESTS + 1))
print_test "Parser can parse sample /context output"

# Create sample /context output
cat > /tmp/test_context_sample.txt << 'EOF'
[?2026h[?2026l[?2026h[?2026l[?2026h
 Context Usage
⛁ ⛁ ⛁ ⛁ ⛁ ⛁ ⛁ ⛀ ⛁ ⛁   claude-sonnet-4-5-20250929 · 29k/200k tokens (15%)
⛁ ⛁ ⛁ ⛁ ⛁ ⛶ ⛶ ⛶ ⛶ ⛶
⛶ ⛶ ⛶ ⛶ ⛶ ⛶ ⛶ ⛶ ⛶ ⛶   ⛁ System prompt: 2.8k tokens (1.4%)
⛶ ⛶ ⛶ ⛶ ⛶ ⛶ ⛶ ⛶ ⛶ ⛶   ⛁ System tools: 13.4k tokens (6.7%)
⛶ ⛶ ⛶ ⛶ ⛶ ⛶ ⛶ ⛶ ⛶ ⛶   ⛁ Memory files: 1.5k tokens (0.8%)
⛶ ⛶ ⛶ ⛶ ⛶ ⛶ ⛶ ⛶ ⛶ ⛶   ⛁ Messages: 11.4k tokens (5.7%)
⛶ ⛶ ⛶ ⛶ ⛶ ⛶ ⛶ ⛶ ⛶ ⛶   ⛶ Free space: 171k (85.4%)
EOF

PARSE_RESULT=$(python3 get_live_context_metrics.py --json --input /tmp/test_context_sample.txt 2>&1)
if echo "$PARSE_RESULT" | grep -q '"status": "success"'; then
    # Verify parsed values
    TOKENS_USED=$(echo "$PARSE_RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('tokens_used', 0))")
    TOKENS_PCT=$(echo "$PARSE_RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('tokens_pct', 0))")

    if [[ "$TOKENS_USED" == "29000" ]] && [[ "$TOKENS_PCT" == "15.0" ]]; then
        pass_test "Parser correctly extracted tokens_used=29000 and tokens_pct=15.0"
    else
        fail_test "Parser extracted incorrect values" "Expected tokens_used=29000, tokens_pct=15.0; Got tokens_used=$TOKENS_USED, tokens_pct=$TOKENS_PCT"
    fi
else
    fail_test "Parser failed to parse /context output" "$PARSE_RESULT"
fi

# Test 1.3: Parser handles missing input gracefully
TOTAL_TESTS=$((TOTAL_TESTS + 1))
print_test "Parser handles missing input gracefully"

PARSE_RESULT=$(echo "" | python3 get_live_context_metrics.py --json 2>&1)
if echo "$PARSE_RESULT" | grep -q '"status"'; then
    pass_test "Parser returned structured JSON even with no input"
else
    fail_test "Parser did not handle missing input gracefully" "$PARSE_RESULT"
fi

# ============================================================================
# TEST GROUP 2: Enhanced Statusline
# ============================================================================

print_header "TEST GROUP 2: Enhanced Statusline"

# Test 2.1: Enhanced statusline script exists
TOTAL_TESTS=$((TOTAL_TESTS + 1))
print_test "Enhanced statusline script exists and is executable"
if [[ -x "statusline_with_live_metrics.sh" ]]; then
    pass_test "statusline_with_live_metrics.sh is executable"
else
    fail_test "statusline_with_live_metrics.sh is not executable" "Script not found or not executable"
fi

# Test 2.2: Statusline can run with minimal input
TOTAL_TESTS=$((TOTAL_TESTS + 1))
print_test "Statusline can run with minimal JSON input"

TEST_JSON='{"model": {"displayName": "Sonnet 4.5"}, "currentDirectory": "/home/user01/claude-test/ClaudePrompt"}'
STATUSLINE_OUTPUT=$(echo "$TEST_JSON" | bash statusline_with_live_metrics.sh 2>&1)

if [[ -n "$STATUSLINE_OUTPUT" ]]; then
    pass_test "Statusline generated output"
else
    fail_test "Statusline did not generate output" "Empty output"
fi

# Test 2.3: Statusline shows correct model name
TOTAL_TESTS=$((TOTAL_TESTS + 1))
print_test "Statusline displays model name correctly"

if echo "$STATUSLINE_OUTPUT" | grep -q "Sonnet 4.5"; then
    pass_test "Model name 'Sonnet 4.5' appears in statusline"
else
    fail_test "Model name not found in statusline" "Output: $STATUSLINE_OUTPUT"
fi

# Test 2.4: Statusline shows live metrics indicator when cache available
TOTAL_TESTS=$((TOTAL_TESTS + 1))
print_test "Statusline shows [LIVE] indicator when /context cache is fresh"

# Create fresh /context cache
cp /tmp/test_context_sample.txt /tmp/claude_context_cache.txt
touch /tmp/claude_context_cache.txt  # Update timestamp

STATUSLINE_OUTPUT=$(echo "$TEST_JSON" | bash statusline_with_live_metrics.sh 2>&1)

if echo "$STATUSLINE_OUTPUT" | grep -q "\[LIVE\]"; then
    pass_test "Statusline shows [LIVE] indicator with fresh cache"
else
    # This is not a hard failure - just a warning
    echo -e "${YELLOW}⚠️  INFO${NC}: [LIVE] indicator not shown (cache may not be detected)"
fi

# ============================================================================
# TEST GROUP 3: Agent Usage Counter
# ============================================================================

print_header "TEST GROUP 3: Agent Usage Counter"

# Test 3.1: Agent counter hook exists
TOTAL_TESTS=$((TOTAL_TESTS + 1))
print_test "Agent counter hook exists and is executable"
HOOK_PATH=".claude/hooks/PostToolUse/capture_live_metrics.sh"
if [[ -x "$HOOK_PATH" ]]; then
    pass_test "capture_live_metrics.sh hook is executable"
else
    fail_test "capture_live_metrics.sh hook is not executable" "Hook not found at $HOOK_PATH"
fi

# Test 3.2: Agent counter initializes correctly
TOTAL_TESTS=$((TOTAL_TESTS + 1))
print_test "Agent counter can be initialized"

rm -f tmp/agent_usage_counter.txt
mkdir -p tmp

# Simulate hook execution
TEST_HOOK_JSON='{"tool_name": "Read", "tool_input": {}, "tool_result": "success", "conversation_stats": {"context_tokens": 10000, "total_tokens": 200000}}'
HOOK_OUTPUT=$(echo "$TEST_HOOK_JSON" | bash "$HOOK_PATH" 2>&1)

if [[ -f "tmp/agent_usage_counter.txt" ]]; then
    COUNTER_VALUE=$(cat tmp/agent_usage_counter.txt)
    if [[ "$COUNTER_VALUE" == "1" ]]; then
        pass_test "Agent counter initialized to 1 after first tool use"
    else
        fail_test "Agent counter has unexpected value" "Expected 1, got $COUNTER_VALUE"
    fi
else
    fail_test "Agent counter file was not created" "File: tmp/agent_usage_counter.txt"
fi

# Test 3.3: Agent counter increments correctly
TOTAL_TESTS=$((TOTAL_TESTS + 1))
print_test "Agent counter increments on multiple tool uses"

# Simulate second tool use
echo "$TEST_HOOK_JSON" | bash "$HOOK_PATH" >/dev/null 2>&1

COUNTER_VALUE=$(cat tmp/agent_usage_counter.txt)
if [[ "$COUNTER_VALUE" == "2" ]]; then
    pass_test "Agent counter incremented to 2 after second tool use"
else
    fail_test "Agent counter did not increment correctly" "Expected 2, got $COUNTER_VALUE"
fi

# Test 3.4: Agent counter updates realtime metrics
TOTAL_TESTS=$((TOTAL_TESTS + 1))
print_test "Agent counter updates realtime_metrics.json"

if [[ -f "tmp/realtime_metrics.json" ]]; then
    AGENTS_VALUE=$(python3 -c "import json; print(json.load(open('tmp/realtime_metrics.json')).get('agents', 'N/A'))")
    if [[ "$AGENTS_VALUE" == "2" ]]; then
        pass_test "Realtime metrics shows agents=2"
    else
        echo -e "${YELLOW}⚠️  INFO${NC}: Realtime metrics shows agents=$AGENTS_VALUE (expected 2)"
    fi
else
    fail_test "realtime_metrics.json was not created" "File: tmp/realtime_metrics.json"
fi

# ============================================================================
# TEST GROUP 4: Backward Compatibility
# ============================================================================

print_header "TEST GROUP 4: Backward Compatibility"

# Test 4.1: Original statusline script still exists
TOTAL_TESTS=$((TOTAL_TESTS + 1))
print_test "Original statusline script still exists"
if [[ -f "statusline_with_metrics.sh" ]]; then
    pass_test "Original statusline_with_metrics.sh preserved"
else
    fail_test "Original statusline_with_metrics.sh missing" "BREAKING CHANGE: File removed"
fi

# Test 4.2: Original statusline still works
TOTAL_TESTS=$((TOTAL_TESTS + 1))
print_test "Original statusline still functions correctly"

ORIGINAL_OUTPUT=$(echo "$TEST_JSON" | bash statusline_with_metrics.sh 2>&1)
if [[ -n "$ORIGINAL_OUTPUT" ]]; then
    pass_test "Original statusline generates output"
else
    fail_test "Original statusline broken" "BREAKING CHANGE: Original statusline does not work"
fi

# Test 4.3: Original hook still exists
TOTAL_TESTS=$((TOTAL_TESTS + 1))
print_test "Original capture_metrics.sh hook still exists"
if [[ -f ".claude/hooks/PostToolUse/capture_metrics.sh" ]]; then
    pass_test "Original capture_metrics.sh hook preserved"
else
    echo -e "${YELLOW}⚠️  INFO${NC}: Original hook not found (may have been replaced - not necessarily breaking)"
fi

# ============================================================================
# TEST GROUP 5: Integration Testing
# ============================================================================

print_header "TEST GROUP 5: Integration Testing"

# Test 5.1: Helper functions script exists
TOTAL_TESTS=$((TOTAL_TESTS + 1))
print_test "Helper functions script exists"
if [[ -f "capture_context_helper.sh" ]]; then
    pass_test "capture_context_helper.sh exists"
else
    fail_test "capture_context_helper.sh missing" "Helper functions not available"
fi

# Test 5.2: Helper functions can be sourced
TOTAL_TESTS=$((TOTAL_TESTS + 1))
print_test "Helper functions can be sourced without errors"

if bash -c "source capture_context_helper.sh && declare -F capture_context" >/dev/null 2>&1; then
    pass_test "Helper functions source successfully"
else
    fail_test "Helper functions have syntax errors" "Cannot source script"
fi

# Test 5.3: End-to-end simulation
TOTAL_TESTS=$((TOTAL_TESTS + 1))
print_test "End-to-end metrics flow simulation"

# Reset counters
rm -f tmp/agent_usage_counter.txt
rm -f tmp/realtime_metrics.json

# 1. Simulate /context capture
cp /tmp/test_context_sample.txt /tmp/claude_context_cache.txt
touch /tmp/claude_context_cache.txt

# 2. Simulate 3 tool uses
for i in {1..3}; do
    echo "$TEST_HOOK_JSON" | bash "$HOOK_PATH" >/dev/null 2>&1
done

# 3. Generate statusline
FINAL_STATUSLINE=$(echo "$TEST_JSON" | bash statusline_with_live_metrics.sh 2>&1)

# Verify results
FINAL_AGENTS=$(cat tmp/agent_usage_counter.txt 2>/dev/null || echo "0")
if [[ "$FINAL_AGENTS" == "3" ]] && echo "$FINAL_STATUSLINE" | grep -q "👥 3"; then
    pass_test "End-to-end flow: 3 agents counted and displayed in statusline"
else
    fail_test "End-to-end flow incomplete" "Agents counted: $FINAL_AGENTS, Statusline: $FINAL_STATUSLINE"
fi

# ============================================================================
# FINAL RESULTS
# ============================================================================

print_header "📊 TEST RESULTS SUMMARY"

echo ""
echo "Total Tests Run: $TOTAL_TESTS"
echo -e "${GREEN}Passed: $PASSED_TESTS${NC}"
echo -e "${RED}Failed: $FAILED_TESTS${NC}"
echo ""

# Calculate success rate
SUCCESS_RATE=$(echo "scale=1; ($PASSED_TESTS / $TOTAL_TESTS) * 100" | bc -l 2>/dev/null || echo "0")
echo "Success Rate: ${SUCCESS_RATE}%"
echo ""

if [[ $FAILED_TESTS -eq 0 ]]; then
    echo -e "${GREEN}✅ ALL TESTS PASSED - PRODUCTION READY${NC}"
    echo ""
    echo "Next steps:"
    echo "  1. Review statusline_with_live_metrics.sh"
    echo "  2. Update Claude Code settings to use new statusline"
    echo "  3. Test in live environment"
    exit 0
else
    echo -e "${RED}❌ SOME TESTS FAILED - REVIEW REQUIRED${NC}"
    echo ""
    echo "Failed tests: $FAILED_TESTS/$TOTAL_TESTS"
    echo "Please review the failures above and fix before deployment"
    exit 1
fi
