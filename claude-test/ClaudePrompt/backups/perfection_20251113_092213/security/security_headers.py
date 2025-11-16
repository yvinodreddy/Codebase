#!/usr/bin/env python3
"""
Security Headers Middleware
Adds security headers to HTTP responses (CORS, CSP, HSTS, etc.)
"""
from typing import Dict, Optional, List
from fastapi import Request, Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
import logging

logger = logging.getLogger(__name__)


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Middleware to add security headers to all HTTP responses

    Headers added:
    - Content-Security-Policy (CSP): Prevents XSS attacks
    - X-Content-Type-Options: Prevents MIME-sniffing
    - X-Frame-Options: Prevents clickjacking
    - X-XSS-Protection: Enables browser XSS filter
    - Strict-Transport-Security (HSTS): Forces HTTPS
    - Referrer-Policy: Controls referrer information
    - Permissions-Policy: Controls browser features
    """

    def __init__(
        self,
        app,
        enable_hsts: bool = False,  # Set True in production with HTTPS
        hsts_max_age: int = 31536000,  # 1 year
        csp_directives: Optional[Dict[str, List[str]]] = None,
    ):
        super().__init__(app)
        self.enable_hsts = enable_hsts
        self.hsts_max_age = hsts_max_age

        # Default CSP directives (strict but functional)
        self.csp_directives = csp_directives or {
            "default-src": ["'self'"],
            "script-src": ["'self'", "'unsafe-inline'"],  # Allow inline scripts for dashboards
            "style-src": ["'self'", "'unsafe-inline'"],  # Allow inline styles
            "img-src": ["'self'", "data:", "https:"],
            "font-src": ["'self'", "data:"],
            "connect-src": ["'self'", "ws:", "wss:"],  # Allow WebSocket connections
            "frame-ancestors": ["'none'"],  # No framing allowed
            "base-uri": ["'self'"],
            "form-action": ["'self'"],
        }

        logger.info("Security headers middleware initialized")

    async def dispatch(self, request: Request, call_next):
        """Add security headers to response"""
        response = await call_next(request)

        # Content Security Policy
        csp_header = self._build_csp_header()
        response.headers["Content-Security-Policy"] = csp_header

        # Prevent MIME-sniffing
        response.headers["X-Content-Type-Options"] = "nosniff"

        # Prevent clickjacking
        response.headers["X-Frame-Options"] = "DENY"

        # Enable XSS filter in older browsers
        response.headers["X-XSS-Protection"] = "1; mode=block"

        # Control referrer information
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        # Permissions Policy (disable dangerous features)
        response.headers["Permissions-Policy"] = (
            "geolocation=(), microphone=(), camera=(), "
            "payment=(), usb=(), magnetometer=(), gyroscope=()"
        )

        # HSTS (only in production with HTTPS)
        if self.enable_hsts:
            response.headers["Strict-Transport-Security"] = (
                f"max-age={self.hsts_max_age}; includeSubDomains; preload"
            )

        return response

    def _build_csp_header(self) -> str:
        """Build Content-Security-Policy header value"""
        directives = []
        for key, values in self.csp_directives.items():
            directive = f"{key} {' '.join(values)}"
            directives.append(directive)
        return "; ".join(directives)


def configure_cors(
    app,
    allowed_origins: List[str] = None,
    allow_credentials: bool = True,
    allowed_methods: List[str] = None,
    allowed_headers: List[str] = None,
):
    """
    Configure CORS (Cross-Origin Resource Sharing) for FastAPI app

    Args:
        app: FastAPI application instance
        allowed_origins: List of allowed origins (default: localhost only)
        allow_credentials: Allow credentials in requests
        allowed_methods: Allowed HTTP methods
        allowed_headers: Allowed HTTP headers

    Example:
        from fastapi import FastAPI
        app = FastAPI()
        configure_cors(app, allowed_origins=["http://localhost:3000"])
    """
    if allowed_origins is None:
        # Default: Allow localhost on common development ports
        allowed_origins = [
            "http://localhost",
            "http://localhost:8000",
            "http://localhost:8888",
            "http://localhost:8889",
            "http://localhost:3000",
            "http://127.0.0.1",
            "http://127.0.0.1:8000",
            "http://127.0.0.1:8888",
            "http://127.0.0.1:8889",
        ]

    if allowed_methods is None:
        allowed_methods = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]

    if allowed_headers is None:
        allowed_headers = ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=allow_credentials,
        allow_methods=allowed_methods,
        allow_headers=allowed_headers,
    )

    logger.info(f"CORS configured with origins: {allowed_origins}")


def add_security_headers(app, enable_hsts: bool = False):
    """
    Add security headers middleware to FastAPI app

    Args:
        app: FastAPI application instance
        enable_hsts: Enable HSTS (only in production with HTTPS)

    Example:
        from fastapi import FastAPI
        app = FastAPI()
        add_security_headers(app, enable_hsts=True)
    """
    app.add_middleware(
        SecurityHeadersMiddleware,
        enable_hsts=enable_hsts
    )

    logger.info("Security headers middleware added")


# Example usage for FastAPI apps
"""
from fastapi import FastAPI
from security.security_headers import configure_cors, add_security_headers

app = FastAPI()

# Add CORS (must be first)
configure_cors(app, allowed_origins=["http://localhost:3000"])

# Add security headers
add_security_headers(app, enable_hsts=False)  # Set True in production with HTTPS

@app.get("/")
async def root():
    return {"message": "Hello World"}
"""
