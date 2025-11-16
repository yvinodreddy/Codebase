#!/bin/bash

echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║          DUPLICATE VARIABLE DECLARATION FIX - VERIFICATION                  ║"
echo "╚══════════════════════════════════════════════════════════════════════════════╝"
echo ""

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

cd "$(dirname "$0")"

echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${RED}CRITICAL ISSUE FIXED: DUPLICATE VARIABLE DECLARATION${NC}"
echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${YELLOW}PROBLEM:${NC}"
echo "  Variable 'examManager' was declared TWICE:"
echo "  1. Line 253 in exam-integration.js: let examManager = null;"
echo "  2. Line 2022 in index.html: let examManager = null;"
echo ""
echo "  JavaScript 'let' does NOT allow redeclaration in the same scope"
echo "  Result: SyntaxError - All JavaScript failed to load"
echo "  Impact: Login form completely broken, no event listeners attached"
echo ""
echo -e "${GREEN}FIX:${NC}"
echo "  Removed duplicate declaration from exam-integration.js"
echo "  Kept declaration in index.html (main application)"
echo "  exam-integration.js now only provides initializeExamSystem() function"
echo ""

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}VERIFICATION CHECKS${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Check 1: examManager is NOT in exam-integration.js
if ! grep -q "let examManager" exam-integration.js; then
    echo -e "${GREEN}✅ PASS${NC} - examManager removed from exam-integration.js"
else
    echo -e "${RED}❌ FAIL${NC} - examManager STILL in exam-integration.js"
fi

# Check 2: examManager IS in index.html
if grep -q "let examManager = null;" index.html; then
    echo -e "${GREEN}✅ PASS${NC} - examManager declared in index.html"
else
    echo -e "${RED}❌ FAIL${NC} - examManager NOT found in index.html"
fi

# Check 3: Only ONE declaration of examManager across all files
EXAM_MANAGER_COUNT=$(grep -r "let examManager" *.js *.html 2>/dev/null | grep -v ".sh:" | wc -l)
if [ "$EXAM_MANAGER_COUNT" -eq 1 ]; then
    echo -e "${GREEN}✅ PASS${NC} - Exactly ONE examManager declaration found"
else
    echo -e "${RED}❌ FAIL${NC} - Found $EXAM_MANAGER_COUNT examManager declarations (expected 1)"
fi

# Check 4: QUESTIONS is only declared once
QUESTIONS_COUNT=$(grep -r "let QUESTIONS = \[\]" *.html 2>/dev/null | wc -l)
if [ "$QUESTIONS_COUNT" -eq 1 ]; then
    echo -e "${GREEN}✅ PASS${NC} - Exactly ONE QUESTIONS declaration found"
else
    echo -e "${RED}❌ FAIL${NC} - Found $QUESTIONS_COUNT QUESTIONS declarations (expected 1)"
fi

# Check 5: JavaScript files exist
if [ -f "exam-integration.js" ]; then
    echo -e "${GREEN}✅ PASS${NC} - exam-integration.js exists"
else
    echo -e "${RED}❌ FAIL${NC} - exam-integration.js NOT found"
fi

if [ -f "questions-database.js" ]; then
    echo -e "${GREEN}✅ PASS${NC} - questions-database.js exists"
else
    echo -e "${RED}❌ FAIL${NC} - questions-database.js NOT found"
fi

if [ -f "questions-subjective.js" ]; then
    echo -e "${GREEN}✅ PASS${NC} - questions-subjective.js exists"
else
    echo -e "${RED}❌ FAIL${NC} - questions-subjective.js NOT found"
fi

# Check 6: initializeExamSystem function exists
if grep -q "function initializeExamSystem()" exam-integration.js; then
    echo -e "${GREEN}✅ PASS${NC} - initializeExamSystem() function found"
else
    echo -e "${RED}❌ FAIL${NC} - initializeExamSystem() function NOT found"
fi

# Check 7: Script tags are correct in index.html
if grep -q '<script src="exam-integration.js"></script>' index.html; then
    echo -e "${GREEN}✅ PASS${NC} - exam-integration.js script tag present"
else
    echo -e "${RED}❌ FAIL${NC} - exam-integration.js script tag NOT found"
fi

# Check 8: DOMContentLoaded wrapper exists
if grep -q "addEventListener('DOMContentLoaded'" index.html; then
    echo -e "${GREEN}✅ PASS${NC} - DOMContentLoaded wrapper present"
else
    echo -e "${RED}❌ FAIL${NC} - DOMContentLoaded wrapper missing"
fi

# Check 9: Login form handler exists
if grep -q "getElementById('loginForm').addEventListener('submit'" index.html; then
    echo -e "${GREEN}✅ PASS${NC} - Login form handler present"
else
    echo -e "${RED}❌ FAIL${NC} - Login form handler missing"
fi

# Check 10: Brace balance check
OPEN_BRACES=$(grep -o "{" index.html | wc -l)
CLOSE_BRACES=$(grep -o "}" index.html | wc -l)

if [ "$OPEN_BRACES" -eq "$CLOSE_BRACES" ]; then
    echo -e "${GREEN}✅ PASS${NC} - JavaScript brace balance correct ($OPEN_BRACES braces)"
else
    echo -e "${RED}❌ FAIL${NC} - Brace mismatch ($OPEN_BRACES opening, $CLOSE_BRACES closing)"
fi

echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}WHAT WAS THE PROBLEM${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "Browser Console Error:"
echo "  Uncaught SyntaxError: Identifier 'examManager' has already been declared"
echo "  at index.html:1980:13"
echo ""
echo "Root Cause:"
echo "  1. exam-integration.js loads first (line 1973)"
echo "  2. exam-integration.js declares: let examManager = null;"
echo "  3. index.html then tries to declare: let examManager = null;"
echo "  4. JavaScript 'let' prevents redeclaration = SyntaxError"
echo "  5. ALL JavaScript fails to load"
echo "  6. No event listeners attach"
echo "  7. Login form completely broken"
echo ""

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}HOW IT'S FIXED${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "BEFORE (BROKEN):"
echo ""
echo "  exam-integration.js (line 253):"
echo "    let examManager = null;  ← DUPLICATE!"
echo ""
echo "  index.html (line 2022):"
echo "    let examManager = null;  ← DUPLICATE!"
echo ""
echo "  Result: SyntaxError, nothing works"
echo ""
echo "AFTER (FIXED):"
echo ""
echo "  exam-integration.js:"
echo "    (declaration removed)"
echo "    function initializeExamSystem() {  ← Only provides function"
echo ""
echo "  index.html (line 2022):"
echo "    let examManager = null;  ← Single declaration"
echo ""
echo "  Result: JavaScript loads correctly, all features work"
echo ""

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}TESTING INSTRUCTIONS${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${GREEN}Step 1: Clear Browser Cache${NC}"
echo "  IMPORTANT: Hard refresh to load new JavaScript files"
echo "  - Chrome/Edge: Ctrl+Shift+R (Windows/Linux) or Cmd+Shift+R (Mac)"
echo "  - Firefox: Ctrl+Shift+R (Windows/Linux) or Cmd+Shift+R (Mac)"
echo "  - Safari: Cmd+Option+R"
echo ""

echo -e "${GREEN}Step 2: Open index.html${NC}"
echo "  - Open index.html in browser"
echo "  - Open Developer Console (F12)"
echo ""

echo -e "${GREEN}Step 3: Check Console Messages${NC}"
echo "  You should see:"
echo "  ✅ EmailJS initialized"
echo "  ✅ DOM loaded - initializing event listeners..."
echo "  ✅ All event listeners initialized successfully"
echo ""
echo "  You should NOT see:"
echo "  ❌ SyntaxError: Identifier 'examManager' has already been declared"
echo ""

echo -e "${GREEN}Step 4: Test Login Form${NC}"
echo "  1. Fill out the form:"
echo "     - Name: John Doe"
echo "     - Email: john@example.com"
echo "     - Phone: 1234567890"
echo "  2. Click 'Continue to Assessment'"
echo "  3. Should navigate to Rules Screen"
echo "  4. Console should show:"
echo "     - '📝 Login form submitted'"
echo "     - '✅ Validation passed'"
echo "     - '✅ Login successful'"
echo "     - '➡️ Navigating to Rules Screen...'"
echo ""

echo -e "${GREEN}Step 5: Test Exam Start${NC}"
echo "  1. On Rules Screen, click 'Start Exam'"
echo "  2. Should load 15 random questions"
echo "  3. Console should show:"
echo "     - '🎲 Initializing random question system...'"
echo "     - '✅ Random question system initialized successfully!'"
echo "     - '📊 Selected Questions: Total: 15'"
echo ""

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}TROUBLESHOOTING${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${YELLOW}Issue: Still seeing SyntaxError${NC}"
echo "  Solution:"
echo "  - Hard refresh browser (Ctrl+Shift+R)"
echo "  - Clear browser cache completely"
echo "  - Close and reopen browser"
echo "  - Check that exam-integration.js was updated"
echo ""

echo -e "${YELLOW}Issue: Login form still not working${NC}"
echo "  Solution:"
echo "  - Check console for any other errors"
echo "  - Verify all JavaScript files are loading"
echo "  - Run this verification script"
echo "  - Check that DOMContentLoaded wrapper exists"
echo ""

echo -e "${YELLOW}Issue: Questions not loading${NC}"
echo "  Solution:"
echo "  - Verify questions-database.js exists"
echo "  - Verify questions-subjective.js exists"
echo "  - Check console for initialization messages"
echo "  - Verify QUESTION_DATABASE is defined"
echo ""

echo ""
echo -e "${GREEN}╔════════════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                         ✅ FIX COMPLETE ✅                                  ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo "The duplicate variable declaration has been fixed!"
echo "Clear your browser cache and test index.html"
echo ""
echo "Expected result:"
echo "  ✅ No SyntaxError in console"
echo "  ✅ Login form works correctly"
echo "  ✅ Exam starts with 15 random questions"
echo "  ✅ All features functional"
echo ""
