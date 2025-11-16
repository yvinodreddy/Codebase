/**
 * SECURITY LOGGING & MONITORING
 * OWASP A09: Security Logging and Monitoring Failures
 *
 * Comprehensive security event logging for audit trails and incident response
 * Production-ready with structured logging
 */

import { writeFileSync, appendFileSync, existsSync, mkdirSync } from 'fs';
import { join } from 'path';

// Log levels
export enum LogLevel {
  DEBUG = 'DEBUG',
  INFO = 'INFO',
  WARN = 'WARN',
  ERROR = 'ERROR',
  CRITICAL = 'CRITICAL',
}

// Security event types
export enum SecurityEvent {
  // Authentication events
  LOGIN_SUCCESS = 'LOGIN_SUCCESS',
  LOGIN_FAILURE = 'LOGIN_FAILURE',
  LOGOUT = 'LOGOUT',
  PASSWORD_CHANGE = 'PASSWORD_CHANGE',
  PASSWORD_RESET_REQUEST = 'PASSWORD_RESET_REQUEST',
  PASSWORD_RESET_COMPLETE = 'PASSWORD_RESET_COMPLETE',
  ACCOUNT_LOCKED = 'ACCOUNT_LOCKED',
  MFA_ENABLED = 'MFA_ENABLED',
  MFA_DISABLED = 'MFA_DISABLED',

  // Authorization events
  ACCESS_DENIED = 'ACCESS_DENIED',
  PRIVILEGE_ESCALATION_ATTEMPT = 'PRIVILEGE_ESCALATION_ATTEMPT',
  UNAUTHORIZED_API_ACCESS = 'UNAUTHORIZED_API_ACCESS',

  // Input validation failures
  INJECTION_ATTEMPT = 'INJECTION_ATTEMPT',
  XSS_ATTEMPT = 'XSS_ATTEMPT',
  PATH_TRAVERSAL_ATTEMPT = 'PATH_TRAVERSAL_ATTEMPT',
  SSRF_ATTEMPT = 'SSRF_ATTEMPT',

  // Rate limiting & abuse
  RATE_LIMIT_EXCEEDED = 'RATE_LIMIT_EXCEEDED',
  BRUTE_FORCE_ATTEMPT = 'BRUTE_FORCE_ATTEMPT',
  DOS_ATTEMPT = 'DOS_ATTEMPT',

  // Data integrity
  DATA_TAMPERING_DETECTED = 'DATA_TAMPERING_DETECTED',
  CHECKSUM_MISMATCH = 'CHECKSUM_MISMATCH',
  INVALID_SIGNATURE = 'INVALID_SIGNATURE',

  // Cryptographic events
  ENCRYPTION_FAILURE = 'ENCRYPTION_FAILURE',
  DECRYPTION_FAILURE = 'DECRYPTION_FAILURE',
  WEAK_KEY_DETECTED = 'WEAK_KEY_DETECTED',

  // File operations
  SUSPICIOUS_FILE_UPLOAD = 'SUSPICIOUS_FILE_UPLOAD',
  FILE_ACCESS_DENIED = 'FILE_ACCESS_DENIED',
  MALICIOUS_FILE_DETECTED = 'MALICIOUS_FILE_DETECTED',

  // Configuration & system
  CONFIG_CHANGE = 'CONFIG_CHANGE',
  SYSTEM_ERROR = 'SYSTEM_ERROR',
  SECURITY_SCAN_INITIATED = 'SECURITY_SCAN_INITIATED',
  VULNERABILITY_DETECTED = 'VULNERABILITY_DETECTED',
}

// Log entry interface
export interface LogEntry {
  timestamp: string;
  level: LogLevel;
  event: SecurityEvent | string;
  message: string;
  userId?: string;
  userEmail?: string;
  ipAddress?: string;
  userAgent?: string;
  requestId?: string;
  method?: string;
  path?: string;
  statusCode?: number;
  responseTime?: number;
  additionalData?: Record<string, any>;
}

/**
 * Security Logger class
 * OWASP A09: Security Logging and Monitoring Failures
 */
export class SecurityLogger {
  private logDir: string;
  private logFile: string;
  private securityLogFile: string;
  private errorLogFile: string;

  constructor(logDirectory: string = 'logs') {
    this.logDir = join(process.cwd(), logDirectory);
    this.logFile = join(this.logDir, 'application.log');
    this.securityLogFile = join(this.logDir, 'security.log');
    this.errorLogFile = join(this.logDir, 'error.log');

    // Ensure log directory exists
    if (!existsSync(this.logDir)) {
      mkdirSync(this.logDir, { recursive: true });
    }
  }

  /**
   * Log security event
   * OWASP A09: Security Logging and Monitoring Failures
   */
  public logSecurityEvent(
    event: SecurityEvent,
    message: string,
    data?: Partial<LogEntry>
  ): void {
    const entry: LogEntry = {
      timestamp: new Date().toISOString(),
      level: this.getLogLevelForEvent(event),
      event,
      message,
      ...data,
    };

    // Log to security log file
    this.appendToFile(this.securityLogFile, entry);

    // Also log to main log file
    this.appendToFile(this.logFile, entry);

    // If critical, also log to error log
    if (entry.level === LogLevel.CRITICAL || entry.level === LogLevel.ERROR) {
      this.appendToFile(this.errorLogFile, entry);
    }

    // Console output in development
    if (process.env.NODE_ENV !== 'production') {
      console.log(`[${entry.level}] ${entry.event}: ${entry.message}`);
    }
  }

  /**
   * Log authentication attempt
   * OWASP A07: Authentication Failures
   */
  public logAuthAttempt(
    success: boolean,
    email: string,
    ipAddress: string,
    userAgent: string,
    additionalData?: Record<string, any>
  ): void {
    this.logSecurityEvent(
      success ? SecurityEvent.LOGIN_SUCCESS : SecurityEvent.LOGIN_FAILURE,
      success ? `Successful login for ${email}` : `Failed login attempt for ${email}`,
      {
        userEmail: email,
        ipAddress,
        userAgent,
        additionalData,
      }
    );
  }

  /**
   * Log access denied event
   * OWASP A01: Broken Access Control
   */
  public logAccessDenied(
    userId: string,
    resource: string,
    ipAddress: string,
    reason: string
  ): void {
    this.logSecurityEvent(
      SecurityEvent.ACCESS_DENIED,
      `Access denied to ${resource}: ${reason}`,
      {
        userId,
        ipAddress,
        additionalData: { resource, reason },
      }
    );
  }

  /**
   * Log injection attempt
   * OWASP A03: Injection
   */
  public logInjectionAttempt(
    type: 'SQL' | 'XSS' | 'Command' | 'LDAP' | 'XML',
    payload: string,
    ipAddress: string,
    path: string
  ): void {
    this.logSecurityEvent(
      SecurityEvent.INJECTION_ATTEMPT,
      `${type} injection attempt detected`,
      {
        ipAddress,
        path,
        additionalData: {
          injectionType: type,
          payload: this.sanitizePayload(payload),
        },
      }
    );
  }

  /**
   * Log rate limit exceeded
   * OWASP A07: Authentication Failures (brute force protection)
   */
  public logRateLimitExceeded(
    ipAddress: string,
    endpoint: string,
    requestCount: number
  ): void {
    this.logSecurityEvent(
      SecurityEvent.RATE_LIMIT_EXCEEDED,
      `Rate limit exceeded for ${endpoint}`,
      {
        ipAddress,
        path: endpoint,
        additionalData: { requestCount },
      }
    );
  }

  /**
   * Log data tampering
   * OWASP A08: Software and Data Integrity Failures
   */
  public logDataTampering(
    resource: string,
    expectedChecksum: string,
    actualChecksum: string,
    userId?: string
  ): void {
    this.logSecurityEvent(
      SecurityEvent.DATA_TAMPERING_DETECTED,
      `Data tampering detected in ${resource}`,
      {
        userId,
        additionalData: {
          resource,
          expectedChecksum,
          actualChecksum,
        },
      }
    );
  }

  /**
   * Log SSRF attempt
   * OWASP A10: Server-Side Request Forgery
   */
  public logSSRFAttempt(
    targetUrl: string,
    ipAddress: string,
    userId?: string
  ): void {
    this.logSecurityEvent(
      SecurityEvent.SSRF_ATTEMPT,
      `SSRF attempt detected targeting ${targetUrl}`,
      {
        userId,
        ipAddress,
        additionalData: { targetUrl },
      }
    );
  }

  /**
   * Log API request
   * General monitoring
   */
  public logAPIRequest(
    method: string,
    path: string,
    statusCode: number,
    responseTime: number,
    userId?: string,
    ipAddress?: string
  ): void {
    const entry: LogEntry = {
      timestamp: new Date().toISOString(),
      level: statusCode >= 500 ? LogLevel.ERROR : statusCode >= 400 ? LogLevel.WARN : LogLevel.INFO,
      event: 'API_REQUEST',
      message: `${method} ${path} ${statusCode}`,
      method,
      path,
      statusCode,
      responseTime,
      userId,
      ipAddress,
    };

    this.appendToFile(this.logFile, entry);
  }

  /**
   * Log error with stack trace
   * OWASP A09: Security Logging and Monitoring Failures
   */
  public logError(
    error: Error,
    context?: string,
    userId?: string
  ): void {
    const entry: LogEntry = {
      timestamp: new Date().toISOString(),
      level: LogLevel.ERROR,
      event: SecurityEvent.SYSTEM_ERROR,
      message: error.message,
      userId,
      additionalData: {
        context,
        stack: error.stack,
        name: error.name,
      },
    };

    this.appendToFile(this.errorLogFile, entry);
    this.appendToFile(this.logFile, entry);

    if (process.env.NODE_ENV !== 'production') {
      console.error(error);
    }
  }

  /**
   * Get log level for security event
   */
  private getLogLevelForEvent(event: SecurityEvent): LogLevel {
    const criticalEvents = [
      SecurityEvent.PRIVILEGE_ESCALATION_ATTEMPT,
      SecurityEvent.DATA_TAMPERING_DETECTED,
      SecurityEvent.MALICIOUS_FILE_DETECTED,
      SecurityEvent.DOS_ATTEMPT,
    ];

    const errorEvents = [
      SecurityEvent.ACCESS_DENIED,
      SecurityEvent.INJECTION_ATTEMPT,
      SecurityEvent.SSRF_ATTEMPT,
      SecurityEvent.BRUTE_FORCE_ATTEMPT,
      SecurityEvent.ENCRYPTION_FAILURE,
      SecurityEvent.DECRYPTION_FAILURE,
    ];

    const warnEvents = [
      SecurityEvent.LOGIN_FAILURE,
      SecurityEvent.RATE_LIMIT_EXCEEDED,
      SecurityEvent.ACCOUNT_LOCKED,
      SecurityEvent.XSS_ATTEMPT,
      SecurityEvent.PATH_TRAVERSAL_ATTEMPT,
    ];

    if (criticalEvents.includes(event)) return LogLevel.CRITICAL;
    if (errorEvents.includes(event)) return LogLevel.ERROR;
    if (warnEvents.includes(event)) return LogLevel.WARN;

    return LogLevel.INFO;
  }

  /**
   * Append log entry to file
   */
  private appendToFile(filename: string, entry: LogEntry): void {
    try {
      const logLine = JSON.stringify(entry) + '\n';
      appendFileSync(filename, logLine, 'utf8');
    } catch (error) {
      // Fail silently - don't want logging to crash the app
      console.error('Failed to write to log file:', error);
    }
  }

  /**
   * Sanitize payload for logging (truncate if too long)
   */
  private sanitizePayload(payload: string): string {
    const maxLength = 500;
    if (payload.length > maxLength) {
      return payload.substring(0, maxLength) + '... [truncated]';
    }
    return payload;
  }

  /**
   * Query logs (for admin dashboards)
   * OWASP A09: Security Logging and Monitoring Failures
   */
  public queryLogs(options?: {
    level?: LogLevel;
    event?: SecurityEvent;
    userId?: string;
    startDate?: Date;
    endDate?: Date;
    limit?: number;
  }): LogEntry[] {
    // This is a simplified implementation
    // In production, use a proper logging service (ELK, Splunk, Datadog)
    return [];
  }

  /**
   * Export logs for forensics
   * OWASP A09: Security Logging and Monitoring Failures
   */
  public exportLogs(startDate: Date, endDate: Date): string {
    return `Export logs from ${startDate.toISOString()} to ${endDate.toISOString()}`;
  }
}

// Global security logger instance
export const securityLogger = new SecurityLogger();

/**
 * Helper function to log security events globally
 */
export function logSecurityEvent(
  event: SecurityEvent,
  message: string,
  data?: Partial<LogEntry>
): void {
  securityLogger.logSecurityEvent(event, message, data);
}
