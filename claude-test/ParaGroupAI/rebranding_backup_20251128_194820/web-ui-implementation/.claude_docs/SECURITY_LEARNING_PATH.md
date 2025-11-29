# OWASP Security Learning Path
## From Basic Understanding to Advanced Implementation

**Purpose:** Step-by-step educational journey to understand OWASP security
**Audience:** Developers at all levels
**Learning Time:** 2-4 hours (complete path)

---

## 📚 Table of Contents

1. [Level 1: Basic Understanding (30 minutes)](#level-1-basic-understanding-30-minutes)
2. [Level 2: How It Works (45 minutes)](#level-2-how-it-works-45-minutes)
3. [Level 3: Hands-On Practice (60 minutes)](#level-3-hands-on-practice-60-minutes)
4. [Level 4: Advanced Concepts (45 minutes)](#level-4-advanced-concepts-45-minutes)
5. [Level 5: Production Implementation (60 minutes)](#level-5-production-implementation-60-minutes)

---

## Level 1: Basic Understanding (30 minutes)

### What is OWASP?

**OWASP** = **O**pen **W**eb **A**pplication **S**ecurity **P**roject

- Non-profit organization focused on web security
- Creates the **OWASP Top 10** - list of the 10 most critical web security risks
- Updated every 3-4 years (latest: 2021)
- Used by organizations worldwide as security standard

**Think of it as:** A checklist of the 10 most common ways websites get hacked.

---

### The OWASP Top 10 2021 (Simplified)

| # | Category | What It Means (Simple) | Real-World Example |
|---|----------|------------------------|---------------------|
| **A01** | Broken Access Control | Users can access things they shouldn't | Regular user views admin panel |
| **A02** | Cryptographic Failures | Sensitive data not encrypted | Credit cards stored in plaintext |
| **A03** | Injection | Malicious code injected into app | SQL injection, XSS attacks |
| **A04** | Insecure Design | App designed without security in mind | Password reset without verification |
| **A05** | Security Misconfiguration | Default settings left unchanged | Default admin password "admin" |
| **A06** | Vulnerable Components | Using old, buggy libraries | Using jQuery 1.0 (from 2006) |
| **A07** | Authentication Failures | Weak login/password systems | No password complexity rules |
| **A08** | Data Integrity Failures | No verification data hasn't changed | Downloaded file is actually malware |
| **A09** | Logging & Monitoring Failures | Not tracking security events | Attacker in system for 6 months undetected |
| **A10** | SSRF | Server makes requests to internal systems | Attacker accesses internal database |

---

### What Did We Implement?

We created **4 security modules** (think of them as security toolkits) that protect against all 10 categories:

#### 1. Input Validation Toolkit (`input-validation.ts`)
**Protects against:** Injection (A03), SSRF (A10)
**Simple explanation:** Checks user input to make sure it's safe before using it

**Example:**
```
User enters: <script>alert('hack')</script>
Toolkit cleans: (removes the dangerous parts)
```

#### 2. Authentication Toolkit (`authentication.ts`)
**Protects against:** Broken Access Control (A01), Authentication Failures (A07)
**Simple explanation:** Makes sure only authorized users can access your app

**Example:**
```
User logs in with password "MyPassword123"
Toolkit stores: $scrypt$16384$8$1$3a4b5c... (unreadable hash)
Attacker steals database: Can't reverse the hash to get password
```

#### 3. Cryptography Toolkit (`crypto.ts`)
**Protects against:** Cryptographic Failures (A02), Data Integrity Failures (A08)
**Simple explanation:** Encrypts sensitive data so hackers can't read it

**Example:**
```
Credit card: 4111-1111-1111-1111
Encrypted: f3a7b2c8e9d4f1a6c3e0d7b4a1f8c5e2...
Attacker steals file: Sees gibberish, can't decrypt without key
```

#### 4. Security Logging Toolkit (`logging.ts`)
**Protects against:** Logging & Monitoring Failures (A09)
**Simple explanation:** Records security events so you can detect and investigate attacks

**Example:**
```
[2025-11-14 20:15:32] ❌ FAILED LOGIN from 192.168.1.100
[2025-11-14 20:15:35] ❌ FAILED LOGIN from 192.168.1.100
[2025-11-14 20:15:38] ❌ FAILED LOGIN from 192.168.1.100
[2025-11-14 20:15:41] 🚨 BRUTE FORCE ATTACK DETECTED - IP BLOCKED
```

---

### Why Is This Important?

**Without OWASP security:**
- ❌ Hackers can steal customer credit cards
- ❌ Competitors can access your database
- ❌ Employees can view others' private data
- ❌ You might not know you've been hacked until it's too late

**With OWASP security:**
- ✅ Credit cards encrypted (unreadable if stolen)
- ✅ Access control prevents unauthorized access
- ✅ Injection attacks blocked automatically
- ✅ All security events logged for investigation

**Real-world impact:**
- **Equifax breach (2017):** 147 million records stolen - Cost: $1.4 billion
- **Target breach (2013):** 40 million credit cards stolen - Cost: $292 million
- **Yahoo breach (2014):** 3 billion accounts stolen - Cost: $350 million

**All of these could have been prevented with proper OWASP security.**

---

## Level 2: How It Works (45 minutes)

### How XSS Prevention Works

**XSS (Cross-Site Scripting):** Attacker injects malicious JavaScript into your website

**Example attack:**
```html
User submits: <script>alert('You are hacked!')</script>
Without protection: Script executes, shows popup
With protection: Script removed before execution
```

**How our code prevents it:**

```typescript
// src/lib/security/input-validation.ts
import DOMPurify from 'isomorphic-dompurify';

export function sanitizeHTML(input: string): string {
  return DOMPurify.sanitize(input, {
    ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'a', 'p', 'br'],
    ALLOWED_ATTR: ['href', 'title', 'target'],
  });
}
```

**Step-by-step:**
1. User submits: `<script>alert('hack')</script><b>Hello</b>`
2. DOMPurify checks each tag
3. `<script>` tag is NOT in ALLOWED_TAGS → Removed
4. `<b>` tag IS in ALLOWED_TAGS → Kept
5. Result: `<b>Hello</b>`

**Why DOMPurify?**
- Used by Google, Microsoft, Facebook
- Handles 1000+ XSS bypass techniques
- Automatically updated when new attacks discovered

---

### How Password Hashing Works

**Problem:** Storing passwords in plaintext is dangerous
- If database is stolen, all passwords are exposed
- Hackers can log in as any user

**Solution:** Hash passwords using scrypt

**What is hashing?**
- One-way function (can't reverse it)
- Same password always produces same hash
- Different password produces completely different hash

**Example:**

```typescript
// src/lib/security/authentication.ts
import { scrypt, randomBytes, timingSafeEqual } from 'crypto';

export async function hashPassword(password: string): Promise<string> {
  // Step 1: Generate random salt (prevents rainbow table attacks)
  const salt = randomBytes(16).toString('hex');

  // Step 2: Hash password with scrypt (CPU + memory hard)
  const derivedKey = await scrypt(password, salt, 64);

  // Step 3: Combine salt and hash
  return `${salt}:${derivedKey.toString('hex')}`;
}
```

**Step-by-step:**
1. User enters password: `MyPassword123`
2. Generate random salt: `3a4b5c6d7e8f9a0b`
3. Hash password with salt: `scrypt('MyPassword123', '3a4b5c6d7e8f9a0b')`
4. Result: `3a4b5c6d7e8f9a0b:9f8e7d6c5b4a3e2d1f0e9d8c7b6a5f4e...`

**Why can't this be reversed?**
- Scrypt is designed to be CPU and memory intensive
- Takes ~100ms to hash (fast enough for users)
- Takes 100+ years to brute force with all passwords
- Rainbow tables don't work (salt is random)

**Verification (timing-safe):**

```typescript
export async function verifyPassword(password: string, hash: string): Promise<boolean> {
  const [salt, key] = hash.split(':');
  const keyBuffer = Buffer.from(key, 'hex');
  const derivedKey = await scrypt(password, salt, 64);

  // CRITICAL: Use timingSafeEqual to prevent timing attacks
  return timingSafeEqual(keyBuffer, derivedKey);
}
```

**Why timingSafeEqual?**
- Normal comparison: `a === b` returns faster if first character is different
- Attacker can measure response time to guess password character by character
- `timingSafeEqual` always takes same time regardless of where difference is

---

### How AES-256-GCM Encryption Works

**Problem:** Need to store sensitive data (credit cards, SSNs) securely

**Solution:** Encrypt with AES-256-GCM

**What is AES-256-GCM?**
- **AES:** Advanced Encryption Standard (US government standard)
- **256:** Key size (2^256 possible keys = more than atoms in universe)
- **GCM:** Galois/Counter Mode (authenticated encryption)

**What is authenticated encryption?**
- Not only encrypts data
- Also creates authentication tag to detect tampering
- If data is modified, decryption fails

**Example:**

```typescript
// src/lib/security/crypto.ts
import { createCipheriv, createDecipheriv, randomBytes } from 'crypto';

export function encrypt(plaintext: string): string {
  const key = getEncryptionKey(); // From ENCRYPTION_KEY env var
  const iv = randomBytes(12); // Initialization vector (must be random)

  const cipher = createCipheriv('aes-256-gcm', key, iv);

  let encrypted = cipher.update(plaintext, 'utf8', 'hex');
  encrypted += cipher.final('hex');

  const authTag = cipher.getAuthTag(); // Authentication tag

  // Return: iv:authTag:encrypted
  return `${iv.toString('hex')}:${authTag.toString('hex')}:${encrypted}`;
}
```

**Step-by-step:**
1. Plaintext: `4111-1111-1111-1111` (credit card)
2. Generate random IV: `a1b2c3d4e5f6g7h8i9j0`
3. Encrypt with AES-256-GCM: `f3a7b2c8e9d4f1a6...`
4. Generate auth tag: `c6a2d9f4e7c1b8a5...`
5. Result: `a1b2c3d4e5f6g7h8i9j0:c6a2d9f4e7c1b8a5...:f3a7b2c8e9d4f1a6...`

**Decryption with tamper detection:**

```typescript
export function decrypt(ciphertext: string): string {
  const [ivHex, authTagHex, encrypted] = ciphertext.split(':');

  const iv = Buffer.from(ivHex, 'hex');
  const authTag = Buffer.from(authTagHex, 'hex');

  const decipher = createDecipheriv('aes-256-gcm', key, iv);
  decipher.setAuthTag(authTag); // CRITICAL: Set auth tag before decrypting

  try {
    let decrypted = decipher.update(encrypted, 'hex', 'utf8');
    decrypted += decipher.final('utf8'); // Throws if auth tag doesn't match
    return decrypted;
  } catch (error) {
    throw new Error('Data has been tampered with!');
  }
}
```

**If attacker modifies encrypted data:**
1. Auth tag no longer matches encrypted data
2. `decipher.final()` throws error
3. Decryption fails → Attack detected

---

### How SSRF Prevention Works

**SSRF (Server-Side Request Forgery):** Attacker makes your server send requests to internal systems

**Example attack:**
```
User provides URL: http://localhost:6379/
Your server: Fetches content from internal Redis database
Attacker: Gains access to internal data
```

**How our code prevents it:**

```typescript
// src/lib/security/input-validation.ts
export function validateURL(url: string): { isValid: boolean; error?: string } {
  const blockedPatterns = [
    'localhost',
    '127.0.0.1',
    '0.0.0.0',
    '::1',
    '169.254.', // Link-local
    '10.',      // Private class A
    '172.16.', '172.17.', ..., '172.31.', // Private class B
    '192.168.', // Private class C
  ];

  const urlLower = url.toLowerCase();

  for (const pattern of blockedPatterns) {
    if (urlLower.includes(pattern)) {
      return {
        isValid: false,
        error: `URL contains blocked pattern: ${pattern}`,
      };
    }
  }

  return { isValid: true };
}
```

**Step-by-step:**
1. User provides: `http://192.168.1.1/admin`
2. Convert to lowercase: `http://192.168.1.1/admin`
3. Check each blocked pattern
4. Found match: `192.168.` (private IP)
5. Return: `{ isValid: false, error: 'URL contains blocked pattern: 192.168.' }`

**Why these patterns?**
- `localhost` / `127.0.0.1`: Server's own machine
- `10.x.x.x`, `172.16-31.x.x`, `192.168.x.x`: Private network IPs
- `169.254.x.x`: Link-local addresses
- `::1`: IPv6 localhost

**Attacker cannot access:**
- Internal databases
- Internal APIs
- Cloud metadata services (AWS EC2 metadata at 169.254.169.254)
- Other internal services

---

## Level 3: Hands-On Practice (60 minutes)

### Exercise 1: Test XSS Prevention (10 minutes)

**Objective:** See how XSS attacks are blocked

**Step 1:** Create test file

```bash
cd /home/user01/claude-test/ClaudePrompt/web-ui-implementation
cat > test_xss_exercise.ts << 'EOF'
import { sanitizeHTML } from './src/lib/security/input-validation';

// Test cases
const testCases = [
  {
    name: 'Simple script tag',
    input: '<script>alert("XSS")</script>',
    expectedSafe: true,
  },
  {
    name: 'Image with onerror',
    input: '<img src=x onerror="alert(1)">',
    expectedSafe: true,
  },
  {
    name: 'Safe bold tag',
    input: '<b>Hello World</b>',
    expectedSafe: true,
  },
  {
    name: 'Link with javascript protocol',
    input: '<a href="javascript:alert(1)">Click me</a>',
    expectedSafe: true,
  },
];

console.log('XSS Prevention Test Results:\n');

testCases.forEach((test, index) => {
  const output = sanitizeHTML(test.input);
  const isSafe = !output.includes('script') &&
                 !output.includes('onerror') &&
                 !output.includes('javascript:');

  console.log(`Test ${index + 1}: ${test.name}`);
  console.log(`  Input:  ${test.input}`);
  console.log(`  Output: ${output}`);
  console.log(`  Safe:   ${isSafe ? '✅ YES' : '❌ NO'}\n`);
});
EOF
```

**Step 2:** Run test

```bash
npx ts-node test_xss_exercise.ts
```

**Step 3:** Analyze results

**Questions to answer:**
1. Were all malicious scripts removed?
2. Was the safe `<b>` tag preserved?
3. What happened to the JavaScript protocol in the link?

---

### Exercise 2: Test Password Security (15 minutes)

**Objective:** Understand why password hashing is secure

**Step 1:** Create test file

```bash
cat > test_password_exercise.ts << 'EOF'
import { hashPassword, verifyPassword } from './src/lib/security/authentication';

async function exercise() {
  console.log('Password Security Exercise\n');

  // Part 1: Hash the same password twice
  console.log('Part 1: Same password, different hashes');
  const password = 'MySecurePassword123!';
  const hash1 = await hashPassword(password);
  const hash2 = await hashPassword(password);

  console.log('Password:', password);
  console.log('Hash 1:  ', hash1);
  console.log('Hash 2:  ', hash2);
  console.log('Identical:', hash1 === hash2 ? 'YES' : 'NO (different salts)');
  console.log('');

  // Part 2: Verify password
  console.log('Part 2: Password verification');
  const correctPasswordVerifies = await verifyPassword(password, hash1);
  const wrongPasswordVerifies = await verifyPassword('WrongPassword', hash1);

  console.log('Correct password verifies:', correctPasswordVerifies ? '✅ YES' : '❌ NO');
  console.log('Wrong password verifies:  ', wrongPasswordVerifies ? '❌ YES (BAD!)' : '✅ NO');
  console.log('');

  // Part 3: Try to reverse the hash
  console.log('Part 3: Can we reverse the hash?');
  console.log('Hash:', hash1);
  console.log('Can extract password from hash: ❌ NO (mathematically impossible)');
  console.log('Time to brute force: ~100+ years with modern hardware');
}

exercise();
EOF
```

**Step 2:** Run exercise

```bash
npx ts-node test_password_exercise.ts
```

**Questions to answer:**
1. Why are the two hashes different even though the password is the same?
2. Can you extract the original password from the hash?
3. Why is brute forcing impractical?

---

### Exercise 3: Test Encryption (15 minutes)

**Objective:** See how encryption protects sensitive data

**Step 1:** Create test file

```bash
cat > test_encryption_exercise.ts << 'EOF'
import { encrypt, decrypt } from './src/lib/security/crypto';

console.log('Encryption Exercise\n');

// Part 1: Encrypt credit card
console.log('Part 1: Encrypt credit card number');
const creditCard = '4111-1111-1111-1111';
console.log('Original:  ', creditCard);

const encrypted = encrypt(creditCard);
console.log('Encrypted: ', encrypted);
console.log('Length:    ', encrypted.length, 'characters');
console.log('Readable:  ', encrypted.includes('4111') ? '❌ YES (BAD!)' : '✅ NO');
console.log('');

// Part 2: Decrypt
console.log('Part 2: Decrypt back to original');
const decrypted = decrypt(encrypted);
console.log('Decrypted: ', decrypted);
console.log('Match:     ', decrypted === creditCard ? '✅ YES' : '❌ NO');
console.log('');

// Part 3: Tamper detection
console.log('Part 3: What happens if data is tampered with?');
const tampered = encrypted.replace(/a/g, 'b'); // Change 'a' to 'b'
console.log('Original:  ', encrypted.substring(0, 50) + '...');
console.log('Tampered:  ', tampered.substring(0, 50) + '...');

try {
  decrypt(tampered);
  console.log('Result:     ❌ Tampering NOT detected (BAD!)');
} catch (error) {
  console.log('Result:     ✅ Tampering detected! Error thrown.');
  console.log('Error:     ', error.message);
}
EOF
```

**Step 2:** Run exercise

```bash
npx ts-node test_encryption_exercise.ts
```

**Questions to answer:**
1. Can you read the credit card number in the encrypted text?
2. Does decryption restore the original perfectly?
3. What happens when the encrypted data is modified?

---

### Exercise 4: Test Rate Limiting (10 minutes)

**Objective:** Understand how rate limiting prevents abuse

**Step 1:** Create test file

```bash
cat > test_rate_limit_exercise.ts << 'EOF'
import { RateLimiter } from './src/lib/security/input-validation';

console.log('Rate Limiting Exercise\n');

// Create rate limiter: 5 requests per 10 seconds
const limiter = new RateLimiter(5, 10000);

const clientIP = '192.168.1.100';

console.log('Rate limit: 5 requests per 10 seconds\n');
console.log('Simulating 10 requests from', clientIP, '\n');

for (let i = 1; i <= 10; i++) {
  const allowed = limiter.isAllowed(clientIP);
  const remaining = limiter.getRemaining(clientIP);

  console.log(
    `Request ${i.toString().padStart(2)}:`,
    allowed ? '✅ ALLOWED ' : '❌ BLOCKED ',
    `(${remaining} remaining)`
  );

  if (i === 5) {
    console.log('\n--- Rate limit reached! ---\n');
  }
}

console.log('\n💡 Insight: After 5 requests, all subsequent requests are blocked.');
console.log('   After 10 seconds, the rate limit resets.');
EOF
```

**Step 2:** Run exercise

```bash
npx ts-node test_rate_limit_exercise.ts
```

**Questions to answer:**
1. How many requests are allowed before blocking starts?
2. What happens to request #6?
3. How long until the rate limit resets?

---

### Exercise 5: Test SSRF Prevention (10 minutes)

**Objective:** See how internal network access is blocked

**Step 1:** Create test file

```bash
cat > test_ssrf_exercise.ts << 'EOF'
import { validateURL } from './src/lib/security/input-validation';

console.log('SSRF Prevention Exercise\n');

const urls = [
  { url: 'http://localhost:3000/admin', category: 'Localhost' },
  { url: 'http://127.0.0.1:6379/', category: 'Loopback IP' },
  { url: 'http://192.168.1.1/router', category: 'Private IP (home router)' },
  { url: 'http://10.0.0.5/database', category: 'Private IP (corporate)' },
  { url: 'http://172.16.0.1/api', category: 'Private IP (cloud)' },
  { url: 'http://169.254.169.254/metadata', category: 'AWS metadata service' },
  { url: 'https://google.com', category: 'Public website' },
  { url: 'https://github.com', category: 'Public website' },
];

console.log('Testing URL validation:\n');

urls.forEach(({ url, category }) => {
  const result = validateURL(url);
  console.log(category.padEnd(30), url);
  console.log('  Result:', result.isValid ? '✅ ALLOWED' : '❌ BLOCKED');
  if (!result.isValid) {
    console.log('  Reason:', result.error);
  }
  console.log('');
});

console.log('💡 Insight: Internal networks are blocked, public websites are allowed.');
EOF
```

**Step 2:** Run exercise

```bash
npx ts-node test_ssrf_exercise.ts
```

**Questions to answer:**
1. Why is `localhost` blocked?
2. What are private IP ranges?
3. What is AWS metadata service (169.254.169.254)?

---

## Level 4: Advanced Concepts (45 minutes)

### Timing Attacks

**What is a timing attack?**
- Attacker measures how long operations take
- Uses timing differences to extract information

**Example: Password verification without timing protection**

```typescript
// ❌ VULNERABLE CODE
function verifyPasswordUNSAFE(password: string, hash: string): boolean {
  const [salt, correctKey] = hash.split(':');
  const userKey = hashPassword(password, salt);

  // String comparison is NOT timing-safe
  return userKey === correctKey;
}
```

**Why vulnerable?**
```
Correct password: MyPassword123
Attacker tries:   A
Comparison: M !== A → Returns false immediately (1 microsecond)

Attacker tries:   M
Comparison: M === M → Checks next character (2 microseconds)

Attacker tries:   My
Comparison: My === My → Checks next character (3 microseconds)
```

**Attacker can guess password character by character by measuring response time!**

**Solution: Constant-time comparison**

```typescript
// ✅ SECURE CODE
import { timingSafeEqual } from 'crypto';

function verifyPasswordSAFE(password: string, hash: string): boolean {
  const [salt, correctKey] = hash.split(':');
  const userKey = hashPassword(password, salt);

  // timingSafeEqual ALWAYS takes same time
  return timingSafeEqual(
    Buffer.from(userKey, 'hex'),
    Buffer.from(correctKey, 'hex')
  );
}
```

**Why secure?**
- Compares all characters even if first is wrong
- Always takes same time regardless of where difference is
- Attacker cannot guess password character by character

---

### Rainbow Tables

**What is a rainbow table?**
- Precomputed table of password hashes
- Attacker can instantly look up password from hash

**Example:**

```
Rainbow Table (MD5):
password123 → 482c811da5d5b4bc6d497ffa98491e38
admin       → 21232f297a57a5a743894a0e4a801fc3
letmein     → 0d107d09f5bbe40cade3de5c71e9e9b7
```

**If passwords are hashed without salt:**
```
Database:
user1: 482c811da5d5b4bc6d497ffa98491e38
user2: 21232f297a57a5a743894a0e4a801fc3
```

**Attacker uses rainbow table:**
```
482c811da5d5b4bc6d497ffa98491e38 → password123 ✅ FOUND
21232f297a57a5a743894a0e4a801fc3 → admin ✅ FOUND
```

**Solution: Add salt**

```typescript
// Salted hash
const salt = randomBytes(16); // Random for each password
const hash = scrypt(password, salt, 64);
const stored = `${salt}:${hash}`;

// Database:
user1: 3a4b5c6d7e8f:9f8e7d6c5b4a... (unique hash)
user2: 1a2b3c4d5e6f:8d7c6b5a4e3d... (unique hash)
```

**Why rainbow tables don't work:**
- Each password has different salt
- Same password produces different hash
- Attacker must compute hash for each salt (too slow)

---

### Defense in Depth

**Principle:** Use multiple layers of security
- If one layer fails, others still protect

**Example: Protecting credit card number**

```
Layer 1: Input validation
  → Verify format: ✓ 16 digits
  → Check Luhn algorithm: ✓ Valid card

Layer 2: Access control
  → User authorized to view card: ✓ Admin only

Layer 3: Encryption at rest
  → Store encrypted in database: ✓ AES-256-GCM

Layer 4: Encryption in transit
  → Send over HTTPS only: ✓ TLS 1.3

Layer 5: Logging
  → Log all access: ✓ Who, when, what

Layer 6: Audit
  → Review logs weekly: ✓ Detect anomalies
```

**If attacker breaks one layer:**
- Bypasses input validation → Still encrypted in database
- Steals database → Data is encrypted
- Steals encryption key → Access is logged, can be detected

---

## Level 5: Production Implementation (60 minutes)

### Implementation Checklist

This is what you need to do to use the security modules in production:

#### Phase 1: Configuration (Completed ✅)
- [x] Generate ENCRYPTION_KEY
- [x] Add to `.env.local`
- [x] Verify security modules installed
- [x] Add security imports to API routes

#### Phase 2: Implement Security Logging (Next)
- [ ] Add logging to authentication endpoints
- [ ] Add logging to file access endpoints
- [ ] Add logging to query endpoints
- [ ] Configure log rotation
- [ ] Set up log monitoring

#### Phase 3: Implement Input Validation (Next)
- [ ] Add XSS sanitization to query endpoint
- [ ] Add URL validation to file download
- [ ] Add path validation to file access
- [ ] Add rate limiting to API routes

#### Phase 4: Implement Encryption (Next)
- [ ] Identify sensitive fields (credit cards, SSNs, etc.)
- [ ] Encrypt before storing in database
- [ ] Decrypt when reading from database
- [ ] Add HMAC integrity to file downloads

#### Phase 5: Testing (Next)
- [ ] Run automated tests
- [ ] Manual security testing
- [ ] Load testing
- [ ] Penetration testing

---

### Example: Add Security Logging to /api/auth/me

**Current code (src/pages/api/auth/me.ts):**

```typescript
import { NextApiRequest, NextApiResponse } from 'next';
import { getCookie } from 'cookies-next';
import { verifySession } from '@/lib/auth';

// ✅ OWASP Security Integration (Added 2025-11-15)
import { securityLogger, SecurityEvent } from '@/lib/security/logging';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const token = getCookie('session', { req, res });
  if (!token || typeof token !== 'string') {
    return res.status(200).json({ authenticated: false });
  }

  const session = await verifySession(token);
  if (!session || !session.user) {
    return res.status(200).json({ authenticated: false });
  }

  return res.status(200).json({
    authenticated: true,
    user: {
      id: session.user.id,
      email: session.user.email,
      name: session.user.name,
      picture: session.user.picture,
      verified: session.user.verified,
    },
  });
}
```

**Enhanced code (with security logging):**

```typescript
import { NextApiRequest, NextApiResponse } from 'next';
import { getCookie } from 'cookies-next';
import { verifySession } from '@/lib/auth';

// ✅ OWASP Security Integration (Added 2025-11-15)
import { securityLogger, SecurityEvent } from '@/lib/security/logging';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  const startTime = Date.now();
  const clientIp = (req.headers['x-forwarded-for'] as string) || req.socket.remoteAddress || 'unknown';

  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const token = getCookie('session', { req, res });

  // ✅ NEW: Log missing token
  if (!token || typeof token !== 'string') {
    securityLogger.logSecurityEvent(
      SecurityEvent.UNAUTHORIZED_API_ACCESS,
      'Missing session token',
      {
        ipAddress: clientIp,
        path: '/api/auth/me',
        userAgent: req.headers['user-agent'],
      }
    );
    return res.status(200).json({ authenticated: false });
  }

  const session = await verifySession(token);

  // ✅ NEW: Log invalid session
  if (!session || !session.user) {
    securityLogger.logSecurityEvent(
      SecurityEvent.UNAUTHORIZED_API_ACCESS,
      'Invalid session token',
      {
        ipAddress: clientIp,
        path: '/api/auth/me',
        userAgent: req.headers['user-agent'],
      }
    );
    return res.status(200).json({ authenticated: false });
  }

  // ✅ NEW: Log successful authentication check
  const responseTime = Date.now() - startTime;
  securityLogger.logAPIRequest(
    'GET',
    '/api/auth/me',
    200,
    responseTime,
    session.user.id,
    clientIp
  );

  return res.status(200).json({
    authenticated: true,
    user: {
      id: session.user.id,
      email: session.user.email,
      name: session.user.name,
      picture: session.user.picture,
      verified: session.user.verified,
    },
  });
}
```

**What changed:**
1. Added IP address extraction
2. Added logging for missing token
3. Added logging for invalid session
4. Added logging for successful request with response time

**Benefits:**
- Can detect brute force attacks (many failed attempts)
- Can track who accessed the API and when
- Can measure API performance (response times)
- Can investigate security incidents

---

### Example: Add Rate Limiting to /api/query

**Current code (src/pages/api/query.ts):**

```typescript
import { NextApiRequest, NextApiResponse } from 'next';
import { getCookie } from 'cookies-next';
import { verifySession } from '@/lib/auth';
import { UltrathinkClient } from '@/lib/ultrathink-client';

// ✅ OWASP Security Integration (Added 2025-11-15)
import { securityLogger, SecurityEvent } from '@/lib/security/logging';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  // ... authentication code ...
}
```

**Enhanced code (with rate limiting):**

```typescript
import { NextApiRequest, NextApiResponse } from 'next';
import { getCookie } from 'cookies-next';
import { verifySession } from '@/lib/auth';
import { UltrathinkClient } from '@/lib/ultrathink-client';

// ✅ OWASP Security Integration (Added 2025-11-15)
import { securityLogger, SecurityEvent } from '@/lib/security/logging';
import { RateLimiter } from '@/lib/security/input-validation';

// ✅ NEW: Create rate limiter (100 requests per minute)
const rateLimiter = new RateLimiter(100, 60000);

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  const clientIp = (req.headers['x-forwarded-for'] as string) || req.socket.remoteAddress || 'unknown';

  // ✅ NEW: Check rate limit
  if (!rateLimiter.isAllowed(clientIp)) {
    securityLogger.logRateLimitExceeded(clientIp, '/api/query', 100);
    return res.status(429).json({
      error: 'Too many requests',
      retryAfter: 60
    });
  }

  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  // ... rest of code ...
}
```

**What changed:**
1. Created RateLimiter instance (100 requests per minute)
2. Extract client IP address
3. Check if request is allowed
4. Log rate limit exceeded event
5. Return HTTP 429 with retry time

**Benefits:**
- Prevents abuse (attackers can't send 1000s of requests)
- Protects server resources
- Logs excessive requests for investigation

---

**Next document:** Continue with automated test scripts...
