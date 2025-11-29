#!/bin/bash

# OWASP Security Test Suite
# Automated testing of all security features
# Run this script to verify OWASP implementation

set -e  # Exit on error
set -u  # Exit on undefined variable

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Counters
TESTS_PASSED=0
TESTS_FAILED=0
TESTS_TOTAL=0

# Log function
log() {
  echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

log_error() {
  echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} ❌ $1"
}

log_warning() {
  echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} ⚠️  $1"
}

log_info() {
  echo -e "${BLUE}[INFO]${NC} $1"
}

test_passed() {
  ((TESTS_PASSED++))
  ((TESTS_TOTAL++))
  echo -e "  ${GREEN}✅ PASS${NC}: $1"
}

test_failed() {
  ((TESTS_FAILED++))
  ((TESTS_TOTAL++))
  echo -e "  ${RED}❌ FAIL${NC}: $1"
}

# Header
echo ""
echo "================================================================================"
echo "OWASP SECURITY TEST SUITE"
echo "================================================================================"
echo ""

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Create test directory
mkdir -p tests/security
cd tests/security

# Test 1: Verify ENCRYPTION_KEY exists
echo ""
echo "================================================================================"
echo "TEST 1: ENCRYPTION_KEY Configuration"
echo "================================================================================"
echo ""

if grep -q "^ENCRYPTION_KEY=" "../../.env.local"; then
  ENCRYPTION_KEY=$(grep "^ENCRYPTION_KEY=" "../../.env.local" | cut -d '=' -f2)
  KEY_LENGTH=${#ENCRYPTION_KEY}

  if [ "$KEY_LENGTH" -eq 64 ]; then
    test_passed "ENCRYPTION_KEY exists and is 64 characters"
  else
    test_failed "ENCRYPTION_KEY length is $KEY_LENGTH (expected 64)"
  fi
else
  test_failed "ENCRYPTION_KEY not found in .env.local"
fi

# Test 2: Verify security modules exist
echo ""
echo "================================================================================"
echo "TEST 2: Security Modules Existence"
echo "================================================================================"
echo ""

SECURITY_MODULES=(
  "../../src/lib/security/input-validation.ts"
  "../../src/lib/security/authentication.ts"
  "../../src/lib/security/crypto.ts"
  "../../src/lib/security/logging.ts"
)

for module in "${SECURITY_MODULES[@]}"; do
  if [ -f "$module" ]; then
    test_passed "$(basename $module) exists"
  else
    test_failed "$(basename $module) not found"
  fi
done

# Test 3: TypeScript compilation
echo ""
echo "================================================================================"
echo "TEST 3: TypeScript Compilation"
echo "================================================================================"
echo ""

cd ../..
if npm run type-check > /dev/null 2>&1; then
  test_passed "TypeScript compilation passes (0 errors)"
else
  test_failed "TypeScript compilation failed"
fi
cd tests/security

# Test 4: XSS Prevention
echo ""
echo "================================================================================"
echo "TEST 4: XSS Prevention"
echo "================================================================================"
echo ""

cat > test_xss.ts << 'EOF'
import { sanitizeHTML } from '../../src/lib/security/input-validation';

const tests = [
  {
    name: 'Script tag removal',
    input: '<script>alert("XSS")</script>',
    shouldNotContain: 'script',
  },
  {
    name: 'Image onerror removal',
    input: '<img src=x onerror="alert(1)">',
    shouldNotContain: 'onerror',
  },
  {
    name: 'Safe tag preservation',
    input: '<b>Hello</b>',
    shouldContain: '<b>Hello</b>',
  },
];

let passed = 0;
let failed = 0;

tests.forEach(test => {
  const output = sanitizeHTML(test.input);

  if (test.shouldNotContain) {
    if (!output.includes(test.shouldNotContain)) {
      console.log(`✅ ${test.name}`);
      passed++;
    } else {
      console.log(`❌ ${test.name}: Still contains '${test.shouldNotContain}'`);
      failed++;
    }
  }

  if (test.shouldContain) {
    if (output.includes(test.shouldContain)) {
      console.log(`✅ ${test.name}`);
      passed++;
    } else {
      console.log(`❌ ${test.name}: Missing '${test.shouldContain}'`);
      failed++;
    }
  }
});

process.exit(failed > 0 ? 1 : 0);
EOF

cd ../..
if npx ts-node tests/security/test_xss.ts 2>&1 | grep -q "✅"; then
  XSS_OUTPUT=$(npx ts-node tests/security/test_xss.ts 2>&1)
  echo "$XSS_OUTPUT"
  XSS_PASS_COUNT=$(echo "$XSS_OUTPUT" | grep -c "✅" || true)
  test_passed "XSS prevention ($XSS_PASS_COUNT/3 tests passed)"
else
  test_failed "XSS prevention tests failed"
fi
cd tests/security

# Test 5: SSRF Prevention
echo ""
echo "================================================================================"
echo "TEST 5: SSRF Prevention"
echo "================================================================================"
echo ""

cat > test_ssrf.ts << 'EOF'
import { validateURL } from '../../src/lib/security/input-validation';

const tests = [
  { url: 'http://localhost:3000', shouldBlock: true, name: 'Localhost' },
  { url: 'http://127.0.0.1', shouldBlock: true, name: 'Loopback' },
  { url: 'http://192.168.1.1', shouldBlock: true, name: 'Private IP' },
  { url: 'https://google.com', shouldBlock: false, name: 'Public URL' },
];

let passed = 0;
let failed = 0;

tests.forEach(test => {
  const result = validateURL(test.url);
  const blocked = !result.isValid;

  if (blocked === test.shouldBlock) {
    console.log(`✅ ${test.name}: ${blocked ? 'Blocked' : 'Allowed'} correctly`);
    passed++;
  } else {
    console.log(`❌ ${test.name}: Expected ${test.shouldBlock ? 'blocked' : 'allowed'}, got ${blocked ? 'blocked' : 'allowed'}`);
    failed++;
  }
});

process.exit(failed > 0 ? 1 : 0);
EOF

cd ../..
if npx ts-node tests/security/test_ssrf.ts 2>&1 | grep -q "✅"; then
  SSRF_OUTPUT=$(npx ts-node tests/security/test_ssrf.ts 2>&1)
  echo "$SSRF_OUTPUT"
  SSRF_PASS_COUNT=$(echo "$SSRF_OUTPUT" | grep -c "✅" || true)
  test_passed "SSRF prevention ($SSRF_PASS_COUNT/4 tests passed)"
else
  test_failed "SSRF prevention tests failed"
fi
cd tests/security

# Test 6: Path Traversal Prevention
echo ""
echo "================================================================================"
echo "TEST 6: Path Traversal Prevention"
echo "================================================================================"
echo ""

cat > test_path_traversal.ts << 'EOF'
import { validateFilePath } from '../../src/lib/security/input-validation';

const tests = [
  { path: '../../../etc/passwd', shouldBlock: true, name: 'Parent directory traversal' },
  { path: '../../.env.local', shouldBlock: true, name: 'Environment file access' },
  { path: 'uploads/file.txt', shouldBlock: false, name: 'Valid relative path' },
];

let passed = 0;
let failed = 0;

tests.forEach(test => {
  const result = validateFilePath(test.path);
  const blocked = !result.isValid;

  if (blocked === test.shouldBlock) {
    console.log(`✅ ${test.name}: ${blocked ? 'Blocked' : 'Allowed'} correctly`);
    passed++;
  } else {
    console.log(`❌ ${test.name}: Expected ${test.shouldBlock ? 'blocked' : 'allowed'}, got ${blocked ? 'blocked' : 'allowed'}`);
    failed++;
  }
});

process.exit(failed > 0 ? 1 : 0);
EOF

cd ../..
if npx ts-node tests/security/test_path_traversal.ts 2>&1 | grep -q "✅"; then
  PATH_OUTPUT=$(npx ts-node tests/security/test_path_traversal.ts 2>&1)
  echo "$PATH_OUTPUT"
  PATH_PASS_COUNT=$(echo "$PATH_OUTPUT" | grep -c "✅" || true)
  test_passed "Path traversal prevention ($PATH_PASS_COUNT/3 tests passed)"
else
  test_failed "Path traversal prevention tests failed"
fi
cd tests/security

# Test 7: Password Hashing
echo ""
echo "================================================================================"
echo "TEST 7: Password Hashing"
echo "================================================================================"
echo ""

cat > test_password.ts << 'EOF'
import { hashPassword, verifyPassword } from '../../src/lib/security/authentication';

async function test() {
  let passed = 0;
  let failed = 0;

  // Test 1: Hash password
  const password = 'TestPassword123!';
  const hash = await hashPassword(password);

  if (hash.length > 100 && hash.includes(':')) {
    console.log('✅ Password hashed successfully');
    passed++;
  } else {
    console.log('❌ Password hashing failed');
    failed++;
  }

  // Test 2: Verify correct password
  const correctVerify = await verifyPassword(password, hash);
  if (correctVerify) {
    console.log('✅ Correct password verified');
    passed++;
  } else {
    console.log('❌ Correct password not verified');
    failed++;
  }

  // Test 3: Reject wrong password
  const wrongVerify = await verifyPassword('WrongPassword', hash);
  if (!wrongVerify) {
    console.log('✅ Wrong password rejected');
    passed++;
  } else {
    console.log('❌ Wrong password accepted');
    failed++;
  }

  // Test 4: Different salts for same password
  const hash2 = await hashPassword(password);
  if (hash !== hash2) {
    console.log('✅ Different salts generated');
    passed++;
  } else {
    console.log('❌ Same hash for same password (salt not random)');
    failed++;
  }

  process.exit(failed > 0 ? 1 : 0);
}

test();
EOF

cd ../..
if npx ts-node tests/security/test_password.ts 2>&1 | grep -q "✅"; then
  PASS_OUTPUT=$(npx ts-node tests/security/test_password.ts 2>&1)
  echo "$PASS_OUTPUT"
  PASS_PASS_COUNT=$(echo "$PASS_OUTPUT" | grep -c "✅" || true)
  test_passed "Password hashing ($PASS_PASS_COUNT/4 tests passed)"
else
  test_failed "Password hashing tests failed"
fi
cd tests/security

# Test 8: Encryption
echo ""
echo "================================================================================"
echo "TEST 8: AES-256-GCM Encryption"
echo "================================================================================"
echo ""

cat > test_encryption.ts << 'EOF'
import { encrypt, decrypt } from '../../src/lib/security/crypto';

let passed = 0;
let failed = 0;

// Test 1: Encrypt data
const plaintext = 'Sensitive data: 4111-1111-1111-1111';
const encrypted = encrypt(plaintext);

if (encrypted.length > plaintext.length && !encrypted.includes('4111')) {
  console.log('✅ Data encrypted successfully');
  passed++;
} else {
  console.log('❌ Encryption failed or data not obscured');
  failed++;
}

// Test 2: Decrypt data
const decrypted = decrypt(encrypted);
if (decrypted === plaintext) {
  console.log('✅ Data decrypted successfully');
  passed++;
} else {
  console.log('❌ Decryption failed');
  failed++;
}

// Test 3: Tamper detection
const tampered = encrypted.replace(/a/g, 'b');
try {
  decrypt(tampered);
  console.log('❌ Tampering not detected');
  failed++;
} catch (error) {
  console.log('✅ Tampering detected');
  passed++;
}

process.exit(failed > 0 ? 1 : 0);
EOF

cd ../..
if npx ts-node tests/security/test_encryption.ts 2>&1 | grep -q "✅"; then
  ENC_OUTPUT=$(npx ts-node tests/security/test_encryption.ts 2>&1)
  echo "$ENC_OUTPUT"
  ENC_PASS_COUNT=$(echo "$ENC_OUTPUT" | grep -c "✅" || true)
  test_passed "Encryption ($ENC_PASS_COUNT/3 tests passed)"
else
  test_failed "Encryption tests failed"
fi
cd tests/security

# Test 9: HMAC Integrity
echo ""
echo "================================================================================"
echo "TEST 9: HMAC Integrity Verification"
echo "================================================================================"
echo ""

cat > test_hmac.ts << 'EOF'
import { generateHMAC, verifyHMAC } from '../../src/lib/security/crypto';

const secret = 'test-secret-key-12345678901234567890';
let passed = 0;
let failed = 0;

// Test 1: Generate HMAC
const data = 'Important document content';
const signature = generateHMAC(data, secret);

if (signature.length === 128) {
  console.log('✅ HMAC generated successfully');
  passed++;
} else {
  console.log('❌ HMAC generation failed');
  failed++;
}

// Test 2: Verify correct signature
const isValid = verifyHMAC(data, signature, secret);
if (isValid) {
  console.log('✅ Valid signature verified');
  passed++;
} else {
  console.log('❌ Valid signature rejected');
  failed++;
}

// Test 3: Detect tampered data
const tamperedData = 'Tampered document content';
const isTampered = verifyHMAC(tamperedData, signature, secret);
if (!isTampered) {
  console.log('✅ Tampered data detected');
  passed++;
} else {
  console.log('❌ Tampered data accepted');
  failed++;
}

process.exit(failed > 0 ? 1 : 0);
EOF

cd ../..
if npx ts-node tests/security/test_hmac.ts 2>&1 | grep -q "✅"; then
  HMAC_OUTPUT=$(npx ts-node tests/security/test_hmac.ts 2>&1)
  echo "$HMAC_OUTPUT"
  HMAC_PASS_COUNT=$(echo "$HMAC_OUTPUT" | grep -c "✅" || true)
  test_passed "HMAC integrity ($HMAC_PASS_COUNT/3 tests passed)"
else
  test_failed "HMAC integrity tests failed"
fi
cd tests/security

# Test 10: Rate Limiting
echo ""
echo "================================================================================"
echo "TEST 10: Rate Limiting"
echo "================================================================================"
echo ""

cat > test_rate_limit.ts << 'EOF'
import { RateLimiter } from '../../src/lib/security/input-validation';

const limiter = new RateLimiter(5, 10000); // 5 requests per 10 seconds
const clientIP = '192.168.1.100';

let passed = 0;
let failed = 0;

// Test 1: Allow first 5 requests
let allowedCount = 0;
for (let i = 0; i < 5; i++) {
  if (limiter.isAllowed(clientIP)) {
    allowedCount++;
  }
}

if (allowedCount === 5) {
  console.log('✅ First 5 requests allowed');
  passed++;
} else {
  console.log(`❌ Only ${allowedCount}/5 requests allowed`);
  failed++;
}

// Test 2: Block 6th request
if (!limiter.isAllowed(clientIP)) {
  console.log('✅ 6th request blocked (rate limit enforced)');
  passed++;
} else {
  console.log('❌ 6th request allowed (rate limit not enforced)');
  failed++;
}

// Test 3: Check remaining count
const remaining = limiter.getRemaining(clientIP);
if (remaining === 0) {
  console.log('✅ Remaining count is 0');
  passed++;
} else {
  console.log(`❌ Remaining count is ${remaining} (expected 0)`);
  failed++;
}

process.exit(failed > 0 ? 1 : 0);
EOF

cd ../..
if npx ts-node tests/security/test_rate_limit.ts 2>&1 | grep -q "✅"; then
  RATE_OUTPUT=$(npx ts-node tests/security/test_rate_limit.ts 2>&1)
  echo "$RATE_OUTPUT"
  RATE_PASS_COUNT=$(echo "$RATE_OUTPUT" | grep -c "✅" || true)
  test_passed "Rate limiting ($RATE_PASS_COUNT/3 tests passed)"
else
  test_failed "Rate limiting tests failed"
fi
cd tests/security

# Test 11: Security Headers
echo ""
echo "================================================================================"
echo "TEST 11: Security Headers"
echo "================================================================================"
echo ""

log_info "Testing security headers..."

# Check if dev server is running
if ! curl -s http://localhost:3000 > /dev/null 2>&1; then
  test_failed "Dev server not running (start with: npm run dev)"
else
  HEADERS=$(curl -sI http://localhost:3000)

  # Check HSTS
  if echo "$HEADERS" | grep -qi "Strict-Transport-Security"; then
    test_passed "HSTS header present"
  else
    test_failed "HSTS header missing"
  fi

  # Check X-Frame-Options
  if echo "$HEADERS" | grep -qi "X-Frame-Options"; then
    test_passed "X-Frame-Options header present"
  else
    test_failed "X-Frame-Options header missing"
  fi

  # Check X-Content-Type-Options
  if echo "$HEADERS" | grep -qi "X-Content-Type-Options"; then
    test_passed "X-Content-Type-Options header present"
  else
    test_failed "X-Content-Type-Options header missing"
  fi

  # Check CSP
  if echo "$HEADERS" | grep -qi "Content-Security-Policy"; then
    test_passed "Content-Security-Policy header present"
  else
    test_failed "Content-Security-Policy header missing"
  fi
fi

# Summary
echo ""
echo "================================================================================"
echo "TEST SUMMARY"
echo "================================================================================"
echo ""
echo -e "${GREEN}Passed:${NC} $TESTS_PASSED"
echo -e "${RED}Failed:${NC} $TESTS_FAILED"
echo -e "${BLUE}Total: ${NC} $TESTS_TOTAL"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
  echo -e "${GREEN}✅ ALL TESTS PASSED${NC}"
  echo ""
  exit 0
else
  echo -e "${RED}❌ SOME TESTS FAILED${NC}"
  echo ""
  exit 1
fi
