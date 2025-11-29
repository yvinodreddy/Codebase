/**
 * INPUT VALIDATION & SANITIZATION LIBRARY
 * OWASP A03: Injection Protection
 *
 * Prevents SQL injection, XSS, Command injection, Path traversal, etc.
 * Production-ready, world-class security standards
 */

import DOMPurify from 'isomorphic-dompurify';
import validator from 'validator';

/**
 * Sanitize HTML content to prevent XSS attacks
 * OWASP A03: Injection Protection
 */
export function sanitizeHTML(input: string): string {
  if (!input) return '';

  return DOMPurify.sanitize(input, {
    ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'a', 'p', 'br', 'ul', 'ol', 'li', 'code', 'pre'],
    ALLOWED_ATTR: ['href', 'title', 'target'],
    ALLOW_DATA_ATTR: false,
    ALLOW_UNKNOWN_PROTOCOLS: false,
  });
}

/**
 * Validate and sanitize email addresses
 * OWASP A03: Injection Protection
 */
export function validateEmail(email: string): { isValid: boolean; sanitized: string; error?: string } {
  if (!email || typeof email !== 'string') {
    return { isValid: false, sanitized: '', error: 'Email is required' };
  }

  const trimmed = email.trim().toLowerCase();

  if (!validator.isEmail(trimmed)) {
    return { isValid: false, sanitized: trimmed, error: 'Invalid email format' };
  }

  // Additional security: Check for suspicious patterns
  if (trimmed.includes('..') || trimmed.includes('--')) {
    return { isValid: false, sanitized: trimmed, error: 'Suspicious email format' };
  }

  return { isValid: true, sanitized: trimmed };
}

/**
 * Validate and sanitize file paths to prevent path traversal
 * OWASP A01: Broken Access Control & A03: Injection
 */
export function validateFilePath(filePath: string): { isValid: boolean; sanitized: string; error?: string } {
  if (!filePath || typeof filePath !== 'string') {
    return { isValid: false, sanitized: '', error: 'File path is required' };
  }

  // Remove dangerous characters and patterns
  let sanitized = filePath
    .replace(/\.\./g, '')  // Prevent directory traversal
    .replace(/[<>:"|?*]/g, '')  // Remove invalid filename characters
    .replace(/^\/+/, '')  // Remove leading slashes
    .trim();

  // Prevent absolute paths
  if (sanitized.startsWith('/') || sanitized.includes(':\\')) {
    return { isValid: false, sanitized, error: 'Absolute paths not allowed' };
  }

  // Prevent access to system files
  const dangerousPatterns = ['/etc/', '/proc/', '/sys/', '/dev/', 'C:\\', 'windows\\system32'];
  for (const pattern of dangerousPatterns) {
    if (sanitized.toLowerCase().includes(pattern.toLowerCase())) {
      return { isValid: false, sanitized, error: 'Access to system paths forbidden' };
    }
  }

  return { isValid: true, sanitized };
}

/**
 * Validate URL to prevent SSRF attacks
 * OWASP A10: Server-Side Request Forgery (SSRF)
 */
export function validateURL(url: string, allowedDomains?: string[]): { isValid: boolean; sanitized: string; error?: string } {
  if (!url || typeof url !== 'string') {
    return { isValid: false, sanitized: '', error: 'URL is required' };
  }

  const trimmed = url.trim();

  // Must be valid URL
  if (!validator.isURL(trimmed, {
    protocols: ['http', 'https'],
    require_protocol: true,
    require_valid_protocol: true,
  })) {
    return { isValid: false, sanitized: trimmed, error: 'Invalid URL format' };
  }

  try {
    const urlObj = new URL(trimmed);

    // Prevent access to internal networks (SSRF protection)
    const hostname = urlObj.hostname.toLowerCase();

    // Block localhost and private IPs
    const blockedPatterns = [
      'localhost',
      '127.0.0.1',
      '0.0.0.0',
      '::1',
      '169.254.',  // Link-local
      '10.',       // Private class A
      '172.16.',   // Private class B
      '172.17.',
      '172.18.',
      '172.19.',
      '172.20.',
      '172.21.',
      '172.22.',
      '172.23.',
      '172.24.',
      '172.25.',
      '172.26.',
      '172.27.',
      '172.28.',
      '172.29.',
      '172.30.',
      '172.31.',
      '192.168.',  // Private class C
    ];

    for (const pattern of blockedPatterns) {
      if (hostname.includes(pattern)) {
        return { isValid: false, sanitized: trimmed, error: 'Access to internal networks forbidden' };
      }
    }

    // If allowed domains specified, enforce whitelist
    if (allowedDomains && allowedDomains.length > 0) {
      const isAllowed = allowedDomains.some(domain =>
        hostname === domain || hostname.endsWith(`.${domain}`)
      );

      if (!isAllowed) {
        return { isValid: false, sanitized: trimmed, error: 'Domain not in whitelist' };
      }
    }

    return { isValid: true, sanitized: trimmed };
  } catch (error) {
    return { isValid: false, sanitized: trimmed, error: 'Invalid URL' };
  }
}

/**
 * Sanitize database query input to prevent SQL injection
 * OWASP A03: Injection Protection
 */
export function sanitizeQueryInput(input: string): string {
  if (!input || typeof input !== 'string') return '';

  // Remove SQL keywords and dangerous characters
  return input
    .replace(/['";\\]/g, '')  // Remove quotes and backslashes
    .replace(/--/g, '')        // Remove SQL comments
    .replace(/#/g, '')         // Remove MySQL comments
    .replace(/\/\*/g, '')      // Remove /* comments
    .replace(/\*\//g, '')      // Remove */ comments
    .replace(/xp_/gi, '')      // Remove xp_ procedures
    .replace(/sp_/gi, '')      // Remove sp_ procedures
    .trim();
}

/**
 * Validate integer input with range checking
 * OWASP A03: Injection Protection
 */
export function validateInteger(
  input: any,
  options?: { min?: number; max?: number }
): { isValid: boolean; value: number; error?: string } {
  const parsed = parseInt(input, 10);

  if (isNaN(parsed)) {
    return { isValid: false, value: 0, error: 'Invalid integer' };
  }

  if (options?.min !== undefined && parsed < options.min) {
    return { isValid: false, value: parsed, error: `Value must be >= ${options.min}` };
  }

  if (options?.max !== undefined && parsed > options.max) {
    return { isValid: false, value: parsed, error: `Value must be <= ${options.max}` };
  }

  return { isValid: true, value: parsed };
}

/**
 * Validate API key format
 * OWASP A07: Authentication Failures
 */
export function validateAPIKey(apiKey: string): { isValid: boolean; error?: string } {
  if (!apiKey || typeof apiKey !== 'string') {
    return { isValid: false, error: 'API key is required' };
  }

  const trimmed = apiKey.trim();

  // Check minimum length
  if (trimmed.length < 20) {
    return { isValid: false, error: 'API key too short' };
  }

  // Check format (alphanumeric, hyphens, underscores only)
  if (!/^[a-zA-Z0-9_-]+$/.test(trimmed)) {
    return { isValid: false, error: 'Invalid API key format' };
  }

  return { isValid: true };
}

/**
 * Rate limiting token bucket implementation
 * OWASP A07: Authentication Failures (brute force protection)
 */
export class RateLimiter {
  private tokens: Map<string, { count: number; resetAt: number }> = new Map();

  constructor(
    private maxRequests: number = 100,
    private windowMs: number = 60000  // 1 minute
  ) {}

  /**
   * Check if request is allowed
   * @param identifier - IP address or user ID
   * @returns true if allowed, false if rate limited
   */
  public isAllowed(identifier: string): boolean {
    const now = Date.now();
    const bucket = this.tokens.get(identifier);

    if (!bucket || now > bucket.resetAt) {
      // New bucket or expired
      this.tokens.set(identifier, {
        count: 1,
        resetAt: now + this.windowMs,
      });
      return true;
    }

    if (bucket.count >= this.maxRequests) {
      return false;  // Rate limited
    }

    bucket.count++;
    return true;
  }

  /**
   * Get remaining requests for identifier
   */
  public getRemaining(identifier: string): number {
    const bucket = this.tokens.get(identifier);
    if (!bucket || Date.now() > bucket.resetAt) {
      return this.maxRequests;
    }
    return Math.max(0, this.maxRequests - bucket.count);
  }

  /**
   * Clear rate limit for identifier (for testing)
   */
  public clear(identifier: string): void {
    this.tokens.delete(identifier);
  }
}

/**
 * Validate JSON input to prevent injection
 * OWASP A03: Injection Protection & A08: Data Integrity Failures
 */
export function validateJSON<T = any>(input: string): { isValid: boolean; data?: T; error?: string } {
  if (!input || typeof input !== 'string') {
    return { isValid: false, error: 'JSON input is required' };
  }

  try {
    const data = JSON.parse(input) as T;

    // Additional security: Reject if contains suspicious keys
    const jsonStr = JSON.stringify(data);
    const suspiciousPatterns = ['__proto__', 'constructor', 'prototype'];

    for (const pattern of suspiciousPatterns) {
      if (jsonStr.includes(pattern)) {
        return { isValid: false, error: 'Suspicious JSON keys detected' };
      }
    }

    return { isValid: true, data };
  } catch (error) {
    return { isValid: false, error: 'Invalid JSON format' };
  }
}

/**
 * Sanitize filename to prevent directory traversal and command injection
 * OWASP A01: Broken Access Control & A03: Injection
 */
export function sanitizeFilename(filename: string): string {
  if (!filename || typeof filename !== 'string') return '';

  return filename
    .replace(/[^a-zA-Z0-9._-]/g, '_')  // Only allow safe characters
    .replace(/\.{2,}/g, '.')           // Remove multiple dots
    .replace(/^\.+/, '')               // Remove leading dots
    .replace(/\.+$/, '')               // Remove trailing dots
    .substring(0, 255);                // Limit length
}

/**
 * Validate command input to prevent command injection
 * OWASP A03: Injection Protection
 */
export function validateCommand(input: string): { isValid: boolean; error?: string } {
  if (!input || typeof input !== 'string') {
    return { isValid: false, error: 'Command input is required' };
  }

  // Dangerous characters for command injection
  const dangerousChars = [';', '|', '&', '$', '`', '\n', '\r', '<', '>', '(', ')', '{', '}'];

  for (const char of dangerousChars) {
    if (input.includes(char)) {
      return { isValid: false, error: 'Dangerous characters detected in command' };
    }
  }

  return { isValid: true };
}

/**
 * Global input validation middleware
 * Apply this to all API routes
 */
export function validateRequestInput(body: any): { isValid: boolean; errors: string[] } {
  const errors: string[] = [];

  if (!body || typeof body !== 'object') {
    errors.push('Request body must be an object');
    return { isValid: false, errors };
  }

  // Check for prototype pollution attempts
  if ('__proto__' in body || 'constructor' in body || 'prototype' in body) {
    errors.push('Prototype pollution attempt detected');
    return { isValid: false, errors };
  }

  // Validate all string inputs
  for (const [key, value] of Object.entries(body)) {
    if (typeof value === 'string') {
      // Check for excessively long inputs (DoS prevention)
      if (value.length > 100000) {
        errors.push(`Field '${key}' exceeds maximum length`);
      }

      // Check for null bytes (C-string injection)
      if (value.includes('\0')) {
        errors.push(`Field '${key}' contains null bytes`);
      }
    }
  }

  return {
    isValid: errors.length === 0,
    errors,
  };
}
