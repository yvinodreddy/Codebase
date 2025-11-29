#!/usr/bin/env bash
#
# Show ULTRATHINK Verbose Output - Multiple Display Options
#
# This script provides different ways to view the verbose output
# without terminal collapse/truncation issues.
#

PROMPT="${1:-what is 2+2}"
OUTPUT_FILE="/tmp/ultrathink_verbose_output.txt"

echo "=================================================================================="
echo "📺 ULTRATHINK VERBOSE OUTPUT VIEWER"
echo "=================================================================================="
echo ""
echo "Running: ultrathinkc \"$PROMPT\" --verbose"
echo "Saving to: $OUTPUT_FILE"
echo ""

# Run ultrathinkc and save output
ultrathinkc "$PROMPT" --verbose > "$OUTPUT_FILE" 2>&1

# Count lines
TOTAL_LINES=$(wc -l < "$OUTPUT_FILE")
echo "✅ Generated $TOTAL_LINES lines of output"
echo ""

# Show menu
echo "=================================================================================="
echo "📋 VIEWING OPTIONS"
echo "=================================================================================="
echo ""
echo "1. View VERBOSE sections only (no logs)"
echo "2. View all sections with clean formatting"
echo "3. View section-by-section summary"
echo "4. View complete output in pager (less)"
echo "5. View first 100 lines"
echo "6. Extract all [VERBOSE] lines to new file"
echo ""
echo "Choose option (1-6) or press Enter for option 1:"
read -r OPTION

case "${OPTION:-1}" in
    1)
        echo ""
        echo "=================================================================================="
        echo "📺 VERBOSE SECTIONS ONLY"
        echo "=================================================================================="
        echo ""
        grep "^\[VERBOSE\]" "$OUTPUT_FILE" | head -200
        ;;
    2)
        echo ""
        echo "=================================================================================="
        echo "📺 CLEAN FORMATTED OUTPUT"
        echo "=================================================================================="
        echo ""
        grep -E "^(\[VERBOSE\]|═{10}|📊|🔥|✅)" "$OUTPUT_FILE" | head -300
        ;;
    3)
        echo ""
        echo "=================================================================================="
        echo "📺 SECTION-BY-SECTION SUMMARY"
        echo "=================================================================================="
        echo ""

        echo "✅ Framework Benefits:"
        grep -c "FRAMEWORK - WHAT YOU'RE GETTING" "$OUTPUT_FILE" && echo "   FOUND" || echo "   NOT FOUND"

        echo ""
        echo "✅ Stages:"
        for i in {1..6}; do
            if grep -q "STAGE $i:" "$OUTPUT_FILE"; then
                echo "   Stage $i: FOUND"
            else
                echo "   Stage $i: NOT FOUND"
            fi
        done

        echo ""
        echo "✅ Guardrail Layers:"
        for i in {1..7}; do
            if grep -q "Layer $i:" "$OUTPUT_FILE"; then
                echo "   Layer $i: FOUND"
            else
                echo "   Layer $i: NOT FOUND"
            fi
        done

        echo ""
        echo "✅ Agent Components:"
        grep -c "Agent Component:" "$OUTPUT_FILE" | xargs -I {} echo "   Found {} components"

        echo ""
        echo "✅ Other Sections:"
        grep -q "Iteration" "$OUTPUT_FILE" && echo "   Iteration Loop: FOUND" || echo "   Iteration Loop: NOT FOUND"
        grep -q "Context Management" "$OUTPUT_FILE" && echo "   Context Management: FOUND" || echo "   Context Management: NOT FOUND"
        grep -q "Quality Score" "$OUTPUT_FILE" && echo "   Quality Scoring: FOUND" || echo "   Quality Scoring: NOT FOUND"
        grep -q "FRAMEWORK COMPARISON" "$OUTPUT_FILE" && echo "   Framework Comparison: FOUND" || echo "   Framework Comparison: NOT FOUND"
        ;;
    4)
        less "$OUTPUT_FILE"
        ;;
    5)
        head -100 "$OUTPUT_FILE"
        ;;
    6)
        VERBOSE_FILE="/tmp/ultrathink_verbose_only.txt"
        grep "^\[VERBOSE\]" "$OUTPUT_FILE" > "$VERBOSE_FILE"
        echo "✅ Extracted $(wc -l < "$VERBOSE_FILE") VERBOSE lines to: $VERBOSE_FILE"
        echo ""
        echo "View with: cat $VERBOSE_FILE"
        ;;
    *)
        echo "Invalid option"
        ;;
esac

echo ""
echo "=================================================================================="
echo "💾 OUTPUT FILES"
echo "=================================================================================="
echo "Complete output: $OUTPUT_FILE"
echo "View anytime: cat $OUTPUT_FILE"
echo "Search: grep 'pattern' $OUTPUT_FILE"
echo "=================================================================================="
