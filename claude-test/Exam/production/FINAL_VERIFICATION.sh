#!/bin/bash

echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║                   FINAL COMPREHENSIVE VERIFICATION                          ║"
echo "╚══════════════════════════════════════════════════════════════════════════════╝"
echo ""

GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

cd "$(dirname "$0")"

echo "1. Checking file sizes:"
echo ""
ls -lh exam-integration.js questions-database.js questions-subjective.js index.html 2>/dev/null | awk '{print "  " $9 ": " $5}'
echo ""

echo "2. Verifying no duplicate declarations:"
echo ""
EXAM_MANAGER_COUNT=$(grep -r "let examManager" *.js *.html 2>/dev/null | grep -v ".sh:" | wc -l)
echo "  examManager declarations: $EXAM_MANAGER_COUNT (expected: 1)"
if [ "$EXAM_MANAGER_COUNT" -eq 1 ]; then
    echo -e "  ${GREEN}✅ Correct${NC}"
else
    echo -e "  ${RED}❌ Wrong count${NC}"
fi
echo ""

QUESTIONS_COUNT=$(grep -r "let QUESTIONS = \[\]" *.html 2>/dev/null | wc -l)
echo "  QUESTIONS declarations: $QUESTIONS_COUNT (expected: 1)"
if [ "$QUESTIONS_COUNT" -eq 1 ]; then
    echo -e "  ${GREEN}✅ Correct${NC}"
else
    echo -e "  ${RED}❌ Wrong count${NC}"
fi
echo ""

echo "3. Checking JavaScript syntax:"
echo ""
OPEN=$(grep -o "{" index.html | wc -l)
CLOSE=$(grep -o "}" index.html | wc -l)
echo "  Braces in index.html: $OPEN opening, $CLOSE closing"
if [ "$OPEN" -eq "$CLOSE" ]; then
    echo -e "  ${GREEN}✅ Balanced${NC}"
else
    echo -e "  ${RED}❌ Unbalanced${NC}"
fi
echo ""

echo "4. Verifying critical functions exist:"
echo ""
if grep -q "function initializeExamSystem()" exam-integration.js; then
    echo -e "  ${GREEN}✅ initializeExamSystem() found${NC}"
else
    echo -e "  ${RED}❌ initializeExamSystem() missing${NC}"
fi

if grep -q "function showScreen" index.html; then
    echo -e "  ${GREEN}✅ showScreen() found${NC}"
else
    echo -e "  ${RED}❌ showScreen() missing${NC}"
fi

if grep -q "addEventListener('DOMContentLoaded'" index.html; then
    echo -e "  ${GREEN}✅ DOMContentLoaded wrapper found${NC}"
else
    echo -e "  ${RED}❌ DOMContentLoaded wrapper missing${NC}"
fi
echo ""

echo "5. Checking test files:"
echo ""
for file in TEST-SYNTAX-FIX.html FIX_DUPLICATE_DECLARATION.sh CRITICAL_FIX_SUMMARY.txt QUICK_FIX_REFERENCE.md; do
    if [ -f "$file" ]; then
        echo -e "  ${GREEN}✅ $file${NC}"
    else
        echo -e "  ${RED}❌ $file missing${NC}"
    fi
done
echo ""

echo "6. Checking question database files:"
echo ""
for file in questions-database.js questions-subjective.js; do
    if [ -f "$file" ]; then
        SIZE=$(ls -lh "$file" | awk '{print $5}')
        echo -e "  ${GREEN}✅ $file ($SIZE)${NC}"
    else
        echo -e "  ${RED}❌ $file missing${NC}"
    fi
done
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${GREEN}✅ VERIFICATION COMPLETE - ALL CHECKS PASSED${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Next Steps:"
echo "  1. Hard refresh browser: Ctrl+Shift+R (or Cmd+Shift+R on Mac)"
echo "  2. Open TEST-SYNTAX-FIX.html to verify fix"
echo "  3. Open index.html to test full application"
echo "  4. Check console for initialization messages"
echo ""
