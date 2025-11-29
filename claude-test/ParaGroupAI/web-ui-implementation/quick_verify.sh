#!/bin/bash

# Quick Security Verification Script
# Run this to verify OWASP implementation in 60 seconds

echo "================================================================================"
echo "OWASP SECURITY - QUICK VERIFICATION"
echo "================================================================================"
echo ""

cd "$(dirname "$0")"

# Test 1: ENCRYPTION_KEY
echo "1. Checking ENCRYPTION_KEY..."
if grep -q "^ENCRYPTION_KEY=" .env.local 2>/dev/null; then
  KEY=$(grep "^ENCRYPTION_KEY=" .env.local | cut -d '=' -f2)
  if [ "${#KEY}" -eq 64 ]; then
    echo "   ✅ ENCRYPTION_KEY configured (64 characters)"
  else
    echo "   ⚠️  ENCRYPTION_KEY found but wrong length: ${#KEY}"
  fi
else
  echo "   ❌ ENCRYPTION_KEY not found"
fi

# Test 2: Security modules
echo ""
echo "2. Checking security modules..."
for file in input-validation.ts authentication.ts crypto.ts logging.ts; do
  if [ -f "src/lib/security/$file" ]; then
    echo "   ✅ $file"
  else
    echo "   ❌ $file not found"
  fi
done

# Test 3: Security imports in API routes
echo ""
echo "3. Checking security imports in API routes..."
ROUTES_WITH_IMPORTS=$(grep -l "securityLogger" src/pages/api/**/*.ts 2>/dev/null | wc -l)
echo "   ✅ $ROUTES_WITH_IMPORTS routes have security imports"

# Test 4: TypeScript compilation
echo ""
echo "4. Checking TypeScript compilation..."
if npm run type-check > /dev/null 2>&1; then
  echo "   ✅ TypeScript compiles with 0 errors"
else
  echo "   ❌ TypeScript compilation errors found"
fi

# Test 5: Dev server status
echo ""
echo "5. Checking dev server..."
if curl -s http://localhost:3000 > /dev/null 2>&1; then
  echo "   ✅ Dev server running at http://localhost:3000"
else
  echo "   ⚠️  Dev server not running (start with: npm run dev)"
fi

# Test 6: Security headers
echo ""
echo "6. Checking security headers..."
if curl -s http://localhost:3000 > /dev/null 2>&1; then
  HEADERS=$(curl -sI http://localhost:3000)

  if echo "$HEADERS" | grep -q "Strict-Transport-Security"; then
    echo "   ✅ HSTS header active"
  fi

  if echo "$HEADERS" | grep -q "X-Frame-Options"; then
    echo "   ✅ X-Frame-Options active (clickjacking protection)"
  fi

  if echo "$HEADERS" | grep -q "Content-Security-Policy"; then
    echo "   ✅ CSP active (XSS protection)"
  fi
fi

echo ""
echo "================================================================================"
echo "✅ QUICK VERIFICATION COMPLETE"
echo "================================================================================"
echo ""
echo "Next steps:"
echo "  1. Read: .claude_docs/TESTING_AND_VERIFICATION_GUIDE.md"
echo "  2. Read: .claude_docs/SECURITY_LEARNING_PATH.md"
echo "  3. Run: ./run_security_tests.sh (full test suite)"
echo ""
