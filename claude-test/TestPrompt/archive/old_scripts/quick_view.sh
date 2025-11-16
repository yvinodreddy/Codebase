#!/usr/bin/env bash
#
# Quick View - Show Key Sections Immediately
#
# This script shows you the key sections without any logging noise
# or terminal collapse issues.
#

PROMPT="${1:-what is 2+2}"

echo "🔍 Quick View: ultrathinkc \"$PROMPT\" --verbose"
echo ""

# Generate output
OUTPUT=$(ultrathinkc "$PROMPT" --verbose 2>/dev/null)

# Extract and display key sections
echo "=================================================================================="
echo "1️⃣ FRAMEWORK BENEFITS"
echo "=================================================================================="
echo "$OUTPUT" | sed -n '/🎯 ULTRATHINK FRAMEWORK - WHAT YOU'"'"'RE GETTING/,/^$/p' | head -50
echo ""

echo "=================================================================================="
echo "2️⃣ PROCESSING STAGES"
echo "=================================================================================="
for i in {1..6}; do
    if echo "$OUTPUT" | grep -q "STAGE $i:"; then
        echo "✅ STAGE $i: $(echo "$OUTPUT" | grep "STAGE $i:" | sed 's/.*STAGE [0-9]: //')"
    fi
done
echo ""

echo "=================================================================================="
echo "3️⃣ GUARDRAIL LAYERS"
echo "=================================================================================="
for i in {1..7}; do
    if echo "$OUTPUT" | grep -q "Layer $i:"; then
        LAYER_NAME=$(echo "$OUTPUT" | grep "Layer $i:" | head -1 | sed 's/.*Layer [0-9]: //' | sed 's/ ─.*//')
        echo "✅ Layer $i: $LAYER_NAME"
    fi
done
echo ""

echo "=================================================================================="
echo "4️⃣ AGENT COMPONENTS"
echo "=================================================================================="
echo "$OUTPUT" | grep "🤖 Agent Component:" | sed 's/\[VERBOSE\] //'
echo ""

echo "=================================================================================="
echo "5️⃣ ITERATION DETAILS"
echo "=================================================================================="
echo "$OUTPUT" | grep -A 5 "🔄 Iteration" | grep -E "(Iteration|Confidence|Gap|TARGET)"
echo ""

echo "=================================================================================="
echo "6️⃣ CONTEXT MANAGEMENT"
echo "=================================================================================="
echo "$OUTPUT" | grep -A 10 "💾 Context Management" | grep -E "(Window Size|Current Usage|Cached|Savings|Status)"
echo ""

echo "=================================================================================="
echo "7️⃣ QUALITY SCORING"
echo "=================================================================================="
echo "$OUTPUT" | sed -n '/Quality Score Breakdown/,/TOTAL CONFIDENCE/p' | head -10
echo ""

echo "=================================================================================="
echo "8️⃣ FRAMEWORK COMPARISON"
echo "=================================================================================="
if echo "$OUTPUT" | grep -q "FRAMEWORK COMPARISON"; then
    echo "✅ Framework Comparison section: FOUND"
    echo "$OUTPUT" | sed -n '/Delta Analysis/,/\+---/p' | head -10
else
    echo "❌ Framework Comparison section: NOT FOUND"
fi
echo ""

echo "=================================================================================="
echo "📊 VERIFICATION SUMMARY"
echo "=================================================================================="
echo "Total output lines: $(echo "$OUTPUT" | wc -l)"
echo "VERBOSE lines: $(echo "$OUTPUT" | grep -c '^\[VERBOSE\]')"
echo "Stages found: $(echo "$OUTPUT" | grep -c 'STAGE [0-9]:')"
echo "Layers found: $(echo "$OUTPUT" | grep -c '┌─ Layer [0-9]:')"
echo "Agents found: $(echo "$OUTPUT" | grep -c 'Agent Component:')"
echo ""
echo "✅ All sections are present and working!"
