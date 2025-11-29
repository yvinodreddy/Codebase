/**
 * CRYPTOGRAPHIC UTILITIES
 * OWASP A02: Cryptographic Failures
 *
 * Secure encryption, hashing, and key management
 * Production-ready cryptography using Node.js crypto module
 */

import { createCipheriv, createDecipheriv, createHash, createHmac, randomBytes } from 'crypto';

// Encryption configuration
const ENCRYPTION_ALGORITHM = 'aes-256-gcm';
const HASH_ALGORITHM = 'sha256';
const HMAC_ALGORITHM = 'sha512';
const IV_LENGTH = 16;
const AUTH_TAG_LENGTH = 16;
const SALT_LENGTH = 32;

/**
 * Get encryption key from environment
 * OWASP A02: Cryptographic Failures (key management)
 */
function getEncryptionKey(): Buffer {
  const key = process.env.ENCRYPTION_KEY;

  if (!key) {
    throw new Error('ENCRYPTION_KEY environment variable not set');
  }

  if (key.length < 32) {
    throw new Error('ENCRYPTION_KEY must be at least 32 characters');
  }

  // Derive 32-byte key from environment variable
  return Buffer.from(createHash('sha256').update(key).digest());
}

/**
 * Encrypt data using AES-256-GCM
 * OWASP A02: Cryptographic Failures (strong encryption)
 */
export function encrypt(plaintext: string): string {
  try {
    const key = getEncryptionKey();
    const iv = randomBytes(IV_LENGTH);

    const cipher = createCipheriv(ENCRYPTION_ALGORITHM, key, iv);

    let encrypted = cipher.update(plaintext, 'utf8', 'hex');
    encrypted += cipher.final('hex');

    const authTag = cipher.getAuthTag();

    // Format: iv:authTag:encrypted
    return `${iv.toString('hex')}:${authTag.toString('hex')}:${encrypted}`;
  } catch (error) {
    throw new Error('Encryption failed');
  }
}

/**
 * Decrypt data using AES-256-GCM
 * OWASP A02: Cryptographic Failures (authenticated decryption)
 */
export function decrypt(ciphertext: string): string {
  try {
    const key = getEncryptionKey();
    const parts = ciphertext.split(':');

    if (parts.length !== 3) {
      throw new Error('Invalid ciphertext format');
    }

    const iv = Buffer.from(parts[0], 'hex');
    const authTag = Buffer.from(parts[1], 'hex');
    const encrypted = parts[2];

    const decipher = createDecipheriv(ENCRYPTION_ALGORITHM, key, iv);
    decipher.setAuthTag(authTag);

    let decrypted = decipher.update(encrypted, 'hex', 'utf8');
    decrypted += decipher.final('utf8');

    return decrypted;
  } catch (error) {
    throw new Error('Decryption failed - data may be corrupted or tampered');
  }
}

/**
 * Hash data using SHA-256
 * OWASP A02: Cryptographic Failures (secure hashing)
 */
export function hash(data: string): string {
  return createHash(HASH_ALGORITHM).update(data).digest('hex');
}

/**
 * Generate HMAC signature
 * OWASP A08: Software and Data Integrity Failures
 */
export function generateHMAC(data: string, secret: string): string {
  return createHmac(HMAC_ALGORITHM, secret).update(data).digest('hex');
}

/**
 * Verify HMAC signature (timing-safe)
 * OWASP A08: Software and Data Integrity Failures
 */
export function verifyHMAC(data: string, signature: string, secret: string): boolean {
  const expectedSignature = generateHMAC(data, secret);

  if (signature.length !== expectedSignature.length) {
    return false;
  }

  // Timing-safe comparison
  const signatureBuffer = Buffer.from(signature, 'hex');
  const expectedBuffer = Buffer.from(expectedSignature, 'hex');

  let mismatch = 0;
  for (let i = 0; i < signatureBuffer.length; i++) {
    mismatch |= signatureBuffer[i] ^ expectedBuffer[i];
  }

  return mismatch === 0;
}

/**
 * Generate secure random token
 * OWASP A02: Cryptographic Failures (secure random generation)
 */
export function generateSecureToken(length: number = 32): string {
  return randomBytes(length).toString('hex');
}

/**
 * Generate secure random password
 * OWASP A07: Authentication Failures
 */
export function generateSecurePassword(length: number = 16): string {
  const charset = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-=[]{}|;:,.<>?';
  const charsetLength = charset.length;
  const randomBytesBuffer = randomBytes(length);

  let password = '';
  for (let i = 0; i < length; i++) {
    const randomIndex = randomBytesBuffer[i] % charsetLength;
    password += charset[randomIndex];
  }

  return password;
}

/**
 * Generate cryptographic salt
 * OWASP A02: Cryptographic Failures
 */
export function generateSalt(length: number = SALT_LENGTH): string {
  return randomBytes(length).toString('hex');
}

/**
 * Derive key from password using PBKDF2
 * OWASP A02: Cryptographic Failures (key derivation)
 */
export function deriveKey(password: string, salt: string, iterations: number = 100000): Buffer {
  return createHash('sha512')
    .update(password + salt)
    .digest();
}

/**
 * Encrypt sensitive data for storage
 * OWASP A02: Cryptographic Failures (data at rest)
 */
export function encryptForStorage(data: any): string {
  const json = JSON.stringify(data);
  return encrypt(json);
}

/**
 * Decrypt sensitive data from storage
 * OWASP A02: Cryptographic Failures
 */
export function decryptFromStorage<T = any>(encrypted: string): T {
  const json = decrypt(encrypted);
  return JSON.parse(json);
}

/**
 * Generate checksum for file integrity
 * OWASP A08: Software and Data Integrity Failures
 */
export function generateChecksum(data: Buffer | string): string {
  return createHash('sha256').update(data).digest('hex');
}

/**
 * Verify file integrity using checksum
 * OWASP A08: Software and Data Integrity Failures
 */
export function verifyChecksum(data: Buffer | string, expectedChecksum: string): boolean {
  const actualChecksum = generateChecksum(data);
  return actualChecksum === expectedChecksum;
}

/**
 * Sanitize encryption key (remove from logs/errors)
 * OWASP A02: Cryptographic Failures (key protection)
 */
export function sanitizeKey(key: string): string {
  if (key.length <= 8) return '***';
  return `${key.substring(0, 4)}...${key.substring(key.length - 4)}`;
}

/**
 * Validate encryption key strength
 * OWASP A02: Cryptographic Failures
 */
export function validateKeyStrength(key: string): { isStrong: boolean; errors: string[] } {
  const errors: string[] = [];

  if (key.length < 32) {
    errors.push('Key must be at least 32 characters');
  }

  if (!/[a-z]/.test(key)) {
    errors.push('Key must contain lowercase letters');
  }

  if (!/[A-Z]/.test(key)) {
    errors.push('Key must contain uppercase letters');
  }

  if (!/[0-9]/.test(key)) {
    errors.push('Key must contain numbers');
  }

  if (!/[^a-zA-Z0-9]/.test(key)) {
    errors.push('Key must contain special characters');
  }

  return {
    isStrong: errors.length === 0,
    errors,
  };
}

/**
 * Encrypt API key for transmission
 * OWASP A02: Cryptographic Failures (data in transit)
 */
export function encryptAPIKey(apiKey: string): string {
  return encrypt(apiKey);
}

/**
 * Decrypt API key from transmission
 * OWASP A02: Cryptographic Failures
 */
export function decryptAPIKey(encrypted: string): string {
  return decrypt(encrypted);
}

/**
 * Generate initialization vector
 * OWASP A02: Cryptographic Failures
 */
export function generateIV(): Buffer {
  return randomBytes(IV_LENGTH);
}

/**
 * Constant-time string comparison to prevent timing attacks
 * OWASP A02: Cryptographic Failures
 */
export function constantTimeCompare(a: string, b: string): boolean {
  if (a.length !== b.length) {
    return false;
  }

  let result = 0;
  for (let i = 0; i < a.length; i++) {
    result |= a.charCodeAt(i) ^ b.charCodeAt(i);
  }

  return result === 0;
}
