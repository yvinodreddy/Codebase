#!/usr/bin/env bash
#
# Verify ULTRATHINK Verbose Mode - Check All Sections Are Present
#
# This script runs ultrathinkc with --verbose and verifies all expected sections
# are present in the output.
#

echo "=================================================================================="
echo "🔍 ULTRATHINK VERBOSE MODE VERIFICATION"
echo "=================================================================================="
echo ""

# Test prompt
PROMPT="what is 2+2"

echo "Running: ultrathinkc \"$PROMPT\" --verbose"
echo ""
echo "Analyzing output for all expected sections..."
echo ""

# Capture output
OUTPUT=$(ultrathinkc "$PROMPT" --verbose 2>&1)

# Section counters
framework_benefits=0
stages=0
layers=0
agents=0
iterations=0
context_mgmt=0
quality_scoring=0
comparison=0

# Check for each section
if echo "$OUTPUT" | grep -q "FRAMEWORK - WHAT YOU'RE GETTING"; then
    framework_benefits=1
fi

stages=$(echo "$OUTPUT" | grep -c "^\[VERBOSE\] STAGE [0-9]:")
layers=$(echo "$OUTPUT" | grep -c "^\[VERBOSE\] ┌─ Layer [0-9]:")
agents=$(echo "$OUTPUT" | grep -c "^\[VERBOSE\] 🤖 Agent Component:")
iterations=$(echo "$OUTPUT" | grep -c "^\[VERBOSE\] 🔄 Iteration [0-9]")

if echo "$OUTPUT" | grep -q "Context Management - Detailed Breakdown"; then
    context_mgmt=1
fi

if echo "$OUTPUT" | grep -q "Quality Score Breakdown"; then
    quality_scoring=1
fi

if echo "$OUTPUT" | grep -q "FRAMEWORK COMPARISON"; then
    comparison=1
fi

# Display results
echo "=================================================================================="
echo "📊 VERIFICATION RESULTS"
echo "=================================================================================="
echo ""

# Framework Benefits
if [ $framework_benefits -eq 1 ]; then
    echo "✅ Framework Benefits Section: FOUND"
else
    echo "❌ Framework Benefits Section: NOT FOUND"
fi

# Stages
if [ $stages -eq 6 ]; then
    echo "✅ All 6 Stages: FOUND ($stages/6)"
else
    echo "⚠️  Stages: PARTIAL ($stages/6)"
fi

# Guardrail Layers
if [ $layers -eq 7 ]; then
    echo "✅ All 7 Guardrail Layers: FOUND ($layers/7)"
else
    echo "⚠️  Guardrail Layers: PARTIAL ($layers/7)"
fi

# Agent Components
if [ $agents -ge 3 ]; then
    echo "✅ Agent Framework Components: FOUND ($agents components)"
else
    echo "⚠️  Agent Components: PARTIAL ($agents/3)"
fi

# Iteration Details
if [ $iterations -ge 1 ]; then
    echo "✅ Iteration Loop Details: FOUND ($iterations iterations)"
else
    echo "❌ Iteration Loop Details: NOT FOUND"
fi

# Context Management
if [ $context_mgmt -eq 1 ]; then
    echo "✅ Context Management Details: FOUND"
else
    echo "❌ Context Management Details: NOT FOUND"
fi

# Quality Scoring
if [ $quality_scoring -eq 1 ]; then
    echo "✅ Quality Scoring Breakdown: FOUND"
else
    echo "❌ Quality Scoring Breakdown: NOT FOUND"
fi

# Framework Comparison
if [ $comparison -eq 1 ]; then
    echo "✅ Framework Comparison (Direct vs ULTRATHINK): FOUND"
else
    echo "❌ Framework Comparison: NOT FOUND"
fi

echo ""
echo "=================================================================================="
echo "📝 SUMMARY"
echo "=================================================================================="
echo ""

total_sections=8
found_sections=0

[ $framework_benefits -eq 1 ] && found_sections=$((found_sections + 1))
[ $stages -eq 6 ] && found_sections=$((found_sections + 1))
[ $layers -eq 7 ] && found_sections=$((found_sections + 1))
[ $agents -ge 3 ] && found_sections=$((found_sections + 1))
[ $iterations -ge 1 ] && found_sections=$((found_sections + 1))
[ $context_mgmt -eq 1 ] && found_sections=$((found_sections + 1))
[ $quality_scoring -eq 1 ] && found_sections=$((found_sections + 1))
[ $comparison -eq 1 ] && found_sections=$((found_sections + 1))

percentage=$((found_sections * 100 / total_sections))

echo "Sections Found: $found_sections/$total_sections ($percentage%)"
echo ""

if [ $found_sections -eq $total_sections ]; then
    echo "✅ VERIFICATION: ALL SECTIONS PRESENT AND WORKING"
    echo ""
    echo "The verbose mode is displaying correctly with:"
    echo "  • Framework benefits (what you get vs without)"
    echo "  • All 6 processing stages"
    echo "  • All 7 guardrail layers individually"
    echo "  • Agent framework components"
    echo "  • Iteration loop with confidence tracking"
    echo "  • Context management details"
    echo "  • Quality scoring breakdown"
    echo "  • Framework comparison (Direct vs ULTRATHINK)"
    echo ""
    echo "🎉 VERBOSE MODE: 100% COMPLETE"
    exit 0
else
    echo "⚠️  VERIFICATION: SOME SECTIONS MISSING"
    echo ""
    echo "Found $found_sections out of $total_sections expected sections."
    echo "This may indicate a partial implementation or output filtering."
    echo ""
    echo "Try viewing the full output:"
    echo "  ultrathinkc \"$PROMPT\" --verbose 2>&1 | less"
    exit 1
fi
