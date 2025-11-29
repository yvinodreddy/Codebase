import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

/**
 * SECURITY: Global security headers middleware
 * Applies security headers to ALL requests
 * Complies with OWASP security standards
 */
export function middleware(request: NextRequest) {
  const response = NextResponse.next();

  // SECURITY HEADERS - Applied to ALL responses

  // Prevent clickjacking attacks
  response.headers.set('X-Frame-Options', 'SAMEORIGIN');

  // Prevent MIME sniffing (XSS protection)
  response.headers.set('X-Content-Type-Options', 'nosniff');

  // Enable browser XSS protection
  response.headers.set('X-XSS-Protection', '1; mode=block');

  // Control referrer information
  response.headers.set('Referrer-Policy', 'strict-origin-when-cross-origin');

  // Restrict dangerous browser features
  response.headers.set(
    'Permissions-Policy',
    'geolocation=(), microphone=(), camera=(), payment=(), usb=(), magnetometer=(), gyroscope=()'
  );

  // Content Security Policy (CSP) - Prevent XSS and injection attacks
  response.headers.set(
    'Content-Security-Policy',
    [
      "default-src 'self'",
      "script-src 'self' 'unsafe-inline' 'unsafe-eval'",  // Next.js requires unsafe-inline/eval for dev
      "style-src 'self' 'unsafe-inline'",  // Tailwind requires unsafe-inline
      "img-src 'self' data: https:",
      "font-src 'self' data:",
      "connect-src 'self'",
      "frame-ancestors 'self'",
      "base-uri 'self'",
      "form-action 'self'"
    ].join('; ')
  );

  // HTTPS enforcement (production only)
  if (process.env.NODE_ENV === 'production') {
    response.headers.set(
      'Strict-Transport-Security',
      'max-age=31536000; includeSubDomains; preload'
    );
  }

  // Prevent DNS prefetching
  response.headers.set('X-DNS-Prefetch-Control', 'off');

  // Additional security for downloads
  if (request.nextUrl.pathname.includes('/api/file/download')) {
    response.headers.set('X-Download-Options', 'noopen');
  }

  return response;
}

// Apply middleware to all routes
export const config = {
  matcher: [
    /*
     * Match all request paths except:
     * - _next/static (static files)
     * - _next/image (image optimization)
     * - favicon.ico (favicon)
     */
    '/((?!_next/static|_next/image|favicon.ico).*)',
  ],
};
