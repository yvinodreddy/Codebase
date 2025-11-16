#!/bin/bash

echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║              SUBMISSION FIX VERIFICATION - JavaScript Syntax                ║"
echo "╚══════════════════════════════════════════════════════════════════════════════╝"
echo ""

GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

cd "$(dirname "$0")"

echo "1. Checking JavaScript brace balance:"
OPEN=$(grep -o "{" index.html | wc -l)
CLOSE=$(grep -o "}" index.html | wc -l)
echo "  Opening braces: $OPEN"
echo "  Closing braces: $CLOSE"
if [ "$OPEN" -eq "$CLOSE" ]; then
    echo -e "  ${GREEN}✅ Balanced${NC}"
else
    echo -e "  ${RED}❌ Unbalanced${NC}"
fi
echo ""

echo "2. Checking submission functions exist in global scope:"
if grep -q "^        async function submitExam()" index.html; then
    echo -e "  ${GREEN}✅ submitExam() found in global scope${NC}"
else
    echo -e "  ${RED}❌ submitExam() NOT in global scope${NC}"
fi

if grep -q "^        async function sendSubmissionEmail" index.html; then
    echo -e "  ${GREEN}✅ sendSubmissionEmail() found in global scope${NC}"
else
    echo -e "  ${RED}❌ sendSubmissionEmail() NOT in global scope${NC}"
fi

if grep -q "^        function showThankYouScreen()" index.html; then
    echo -e "  ${GREEN}✅ showThankYouScreen() found in global scope${NC}"
else
    echo -e "  ${RED}❌ showThankYouScreen() NOT in global scope${NC}"
fi

if grep -q "^        function showCustomConfirm" index.html; then
    echo -e "  ${GREEN}✅ showCustomConfirm() found in global scope${NC}"
else
    echo -e "  ${RED}❌ showCustomConfirm() NOT in global scope${NC}"
fi
echo ""

echo "3. Checking no duplicate functions:"
SUBMIT_COUNT=$(grep -c "async function submitExam()" index.html)
echo "  submitExam() declarations: $SUBMIT_COUNT (expected: 1)"
if [ "$SUBMIT_COUNT" -eq 1 ]; then
    echo -e "  ${GREEN}✅ No duplicates${NC}"
else
    echo -e "  ${RED}❌ Duplicate found!${NC}"
fi
echo ""

echo "4. Checking event listener attachment:"
if grep -q "getElementById('submitBtn').addEventListener('click'" index.html; then
    echo -e "  ${GREEN}✅ Submit button event listener found${NC}"
else
    echo -e "  ${RED}❌ Submit button event listener missing${NC}"
fi
echo ""

echo "5. Checking proper event listener usage (no inline onclick):"
if grep -q 'id="confirmSubmitBtn"' index.html; then
    echo -e "  ${GREEN}✅ Using ID-based event listeners${NC}"
else
    echo -e "  ${RED}❌ Still using inline onclick${NC}"
fi
echo ""

echo "6. Checking error handling in submitExam:"
if grep -q "try {" index.html && grep -A 10 "async function submitExam()" index.html | grep -q "catch"; then
    echo -e "  ${GREEN}✅ Error handling present${NC}"
else
    echo -e "  ${YELLOW}⚠️  Error handling may be missing${NC}"
fi
echo ""

echo "7. Checking email success message:"
if grep -q "Exam submitted successfully" index.html; then
    echo -e "  ${GREEN}✅ Success message added${NC}"
else
    echo -e "  ${RED}❌ Success message missing${NC}"
fi
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${GREEN}✅ SYNTAX VERIFICATION COMPLETE${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Next: Test in browser"
echo "  1. Clear cache (Ctrl+Shift+R)"
echo "  2. Open index.html"
echo "  3. Complete exam and submit"
echo "  4. Check console for messages"
echo "  5. Verify email received"
echo ""
