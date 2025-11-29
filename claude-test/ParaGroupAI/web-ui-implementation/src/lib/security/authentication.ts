/**
 * AUTHENTICATION & AUTHORIZATION LIBRARY
 * OWASP A01: Broken Access Control
 * OWASP A07: Identification and Authentication Failures
 *
 * Production-ready authentication with JWT, session management, RBAC
 */

import { SignJWT, jwtVerify } from 'jose';
import { randomBytes, scrypt, timingSafeEqual } from 'crypto';
import { promisify } from 'util';

const scryptAsync = promisify(scrypt);

// Environment configuration
const JWT_SECRET = process.env.JWT_SECRET || 'CHANGE-THIS-IN-PRODUCTION-OR-SECURITY-WILL-FAIL';
const JWT_ALGORITHM = 'HS256';
const JWT_EXPIRATION = '24h';  // 24 hours
const SESSION_DURATION = 24 * 60 * 60 * 1000;  // 24 hours in ms

// User roles for RBAC (Role-Based Access Control)
export enum UserRole {
  ADMIN = 'admin',
  USER = 'user',
  VIEWER = 'viewer',
}

// Permissions for fine-grained access control
export enum Permission {
  READ_FILES = 'read:files',
  WRITE_FILES = 'write:files',
  DELETE_FILES = 'delete:files',
  READ_QUERIES = 'read:queries',
  WRITE_QUERIES = 'write:queries',
  MANAGE_USERS = 'manage:users',
  VIEW_ANALYTICS = 'view:analytics',
}

// Role-to-permissions mapping
const ROLE_PERMISSIONS: Record<UserRole, Permission[]> = {
  [UserRole.ADMIN]: [
    Permission.READ_FILES,
    Permission.WRITE_FILES,
    Permission.DELETE_FILES,
    Permission.READ_QUERIES,
    Permission.WRITE_QUERIES,
    Permission.MANAGE_USERS,
    Permission.VIEW_ANALYTICS,
  ],
  [UserRole.USER]: [
    Permission.READ_FILES,
    Permission.WRITE_FILES,
    Permission.READ_QUERIES,
    Permission.WRITE_QUERIES,
    Permission.VIEW_ANALYTICS,
  ],
  [UserRole.VIEWER]: [
    Permission.READ_FILES,
    Permission.READ_QUERIES,
    Permission.VIEW_ANALYTICS,
  ],
};

export interface User {
  id: string;
  email: string;
  name: string;
  role: UserRole;
  verified: boolean;
  createdAt: Date;
  lastLoginAt?: Date;
}

export interface JWTPayload {
  userId: string;
  email: string;
  role: UserRole;
  sessionId: string;
  iat: number;
  exp: number;
}

/**
 * Hash password securely using scrypt
 * OWASP A02: Cryptographic Failures (proper password hashing)
 */
export async function hashPassword(password: string): Promise<string> {
  const salt = randomBytes(16).toString('hex');
  const derivedKey = (await scryptAsync(password, salt, 64)) as Buffer;
  return `${salt}:${derivedKey.toString('hex')}`;
}

/**
 * Verify password using timing-safe comparison
 * OWASP A07: Authentication Failures (prevent timing attacks)
 */
export async function verifyPassword(password: string, hash: string): Promise<boolean> {
  const [salt, key] = hash.split(':');
  const keyBuffer = Buffer.from(key, 'hex');
  const derivedKey = (await scryptAsync(password, salt, 64)) as Buffer;

  // Timing-safe comparison to prevent timing attacks
  return timingSafeEqual(keyBuffer, derivedKey);
}

/**
 * Generate JWT token
 * OWASP A07: Authentication Failures (secure token generation)
 */
export async function generateJWT(user: User, sessionId: string): Promise<string> {
  const secret = new TextEncoder().encode(JWT_SECRET);

  const jwt = await new SignJWT({
    userId: user.id,
    email: user.email,
    role: user.role,
    sessionId,
  })
    .setProtectedHeader({ alg: JWT_ALGORITHM })
    .setIssuedAt()
    .setExpirationTime(JWT_EXPIRATION)
    .setIssuer('para-group-web-ui')
    .setAudience('para-group-api')
    .sign(secret);

  return jwt;
}

/**
 * Verify JWT token
 * OWASP A07: Authentication Failures (secure token verification)
 */
export async function verifyJWT(token: string): Promise<JWTPayload | null> {
  try {
    const secret = new TextEncoder().encode(JWT_SECRET);

    const { payload } = await jwtVerify(token, secret, {
      issuer: 'para-group-web-ui',
      audience: 'para-group-api',
    });

    return payload as unknown as JWTPayload;
  } catch (error) {
    // Token invalid, expired, or tampered
    return null;
  }
}

/**
 * Generate secure session ID
 * OWASP A07: Authentication Failures (secure session management)
 */
export function generateSessionId(): string {
  return randomBytes(32).toString('hex');
}

/**
 * Session store (in-memory - replace with Redis in production)
 * OWASP A07: Authentication Failures (session management)
 */
class SessionStore {
  private sessions: Map<string, { userId: string; expiresAt: Date }> = new Map();

  public create(userId: string): string {
    const sessionId = generateSessionId();
    const expiresAt = new Date(Date.now() + SESSION_DURATION);

    this.sessions.set(sessionId, { userId, expiresAt });
    return sessionId;
  }

  public get(sessionId: string): string | null {
    const session = this.sessions.get(sessionId);

    if (!session) return null;

    // Check expiration
    if (session.expiresAt < new Date()) {
      this.sessions.delete(sessionId);
      return null;
    }

    return session.userId;
  }

  public delete(sessionId: string): void {
    this.sessions.delete(sessionId);
  }

  public refresh(sessionId: string): boolean {
    const session = this.sessions.get(sessionId);

    if (!session) return false;

    session.expiresAt = new Date(Date.now() + SESSION_DURATION);
    return true;
  }

  // Cleanup expired sessions (run periodically)
  public cleanup(): number {
    const now = new Date();
    let count = 0;

    for (const [sessionId, session] of this.sessions.entries()) {
      if (session.expiresAt < now) {
        this.sessions.delete(sessionId);
        count++;
      }
    }

    return count;
  }
}

// Global session store instance
export const sessionStore = new SessionStore();

// Run cleanup every hour
if (typeof setInterval !== 'undefined') {
  setInterval(() => sessionStore.cleanup(), 60 * 60 * 1000);
}

/**
 * Check if user has permission
 * OWASP A01: Broken Access Control (RBAC implementation)
 */
export function hasPermission(role: UserRole, permission: Permission): boolean {
  const permissions = ROLE_PERMISSIONS[role];
  return permissions.includes(permission);
}

/**
 * Check if user has any of the specified permissions
 * OWASP A01: Broken Access Control
 */
export function hasAnyPermission(role: UserRole, permissions: Permission[]): boolean {
  return permissions.some(p => hasPermission(role, p));
}

/**
 * Check if user has all specified permissions
 * OWASP A01: Broken Access Control
 */
export function hasAllPermissions(role: UserRole, permissions: Permission[]): boolean {
  return permissions.every(p => hasPermission(role, p));
}

/**
 * Require minimum role
 * OWASP A01: Broken Access Control
 */
export function hasMinimumRole(userRole: UserRole, requiredRole: UserRole): boolean {
  const roleHierarchy = {
    [UserRole.VIEWER]: 1,
    [UserRole.USER]: 2,
    [UserRole.ADMIN]: 3,
  };

  return roleHierarchy[userRole] >= roleHierarchy[requiredRole];
}

/**
 * Login attempt tracking for brute force protection
 * OWASP A07: Authentication Failures
 */
class LoginAttemptTracker {
  private attempts: Map<string, { count: number; lockoutUntil: Date | null }> = new Map();
  private readonly MAX_ATTEMPTS = 5;
  private readonly LOCKOUT_DURATION = 15 * 60 * 1000;  // 15 minutes

  public recordAttempt(identifier: string): void {
    const attempt = this.attempts.get(identifier) || { count: 0, lockoutUntil: null };

    attempt.count++;

    if (attempt.count >= this.MAX_ATTEMPTS) {
      attempt.lockoutUntil = new Date(Date.now() + this.LOCKOUT_DURATION);
    }

    this.attempts.set(identifier, attempt);
  }

  public isLockedOut(identifier: string): boolean {
    const attempt = this.attempts.get(identifier);

    if (!attempt || !attempt.lockoutUntil) return false;

    if (attempt.lockoutUntil < new Date()) {
      // Lockout expired
      this.attempts.delete(identifier);
      return false;
    }

    return true;
  }

  public reset(identifier: string): void {
    this.attempts.delete(identifier);
  }

  public getAttempts(identifier: string): number {
    return this.attempts.get(identifier)?.count || 0;
  }

  public getRemainingAttempts(identifier: string): number {
    return Math.max(0, this.MAX_ATTEMPTS - this.getAttempts(identifier));
  }
}

// Global login attempt tracker
export const loginAttemptTracker = new LoginAttemptTracker();

/**
 * Validate password strength
 * OWASP A07: Authentication Failures
 */
export function validatePasswordStrength(password: string): { isStrong: boolean; errors: string[] } {
  const errors: string[] = [];

  if (password.length < 12) {
    errors.push('Password must be at least 12 characters long');
  }

  if (!/[a-z]/.test(password)) {
    errors.push('Password must contain at least one lowercase letter');
  }

  if (!/[A-Z]/.test(password)) {
    errors.push('Password must contain at least one uppercase letter');
  }

  if (!/[0-9]/.test(password)) {
    errors.push('Password must contain at least one number');
  }

  if (!/[^a-zA-Z0-9]/.test(password)) {
    errors.push('Password must contain at least one special character');
  }

  // Check for common passwords
  const commonPasswords = ['password', '123456', 'qwerty', 'admin', 'letmein'];
  if (commonPasswords.some(common => password.toLowerCase().includes(common))) {
    errors.push('Password is too common');
  }

  return {
    isStrong: errors.length === 0,
    errors,
  };
}

/**
 * Generate CSRF token
 * OWASP A01: Broken Access Control (CSRF protection)
 */
export function generateCSRFToken(): string {
  return randomBytes(32).toString('base64');
}

/**
 * Verify CSRF token (timing-safe)
 * OWASP A01: Broken Access Control
 */
export function verifyCSRFToken(token: string, expected: string): boolean {
  if (!token || !expected) return false;
  if (token.length !== expected.length) return false;

  const tokenBuffer = Buffer.from(token);
  const expectedBuffer = Buffer.from(expected);

  return timingSafeEqual(tokenBuffer, expectedBuffer);
}

/**
 * Extract token from Authorization header
 * OWASP A07: Authentication Failures
 */
export function extractBearerToken(authHeader: string | null): string | null {
  if (!authHeader) return null;

  const parts = authHeader.split(' ');
  if (parts.length !== 2 || parts[0] !== 'Bearer') return null;

  return parts[1];
}
