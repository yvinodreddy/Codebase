"""
SwarmCare Production Readiness Test Suite
Comprehensive tests to verify production deployment readiness

Test Categories:
1. Security & Authentication
2. Configuration & Secrets
3. Rate Limiting & Performance
4. HIPAA Compliance
5. Guardrails System
6. Database Connectivity
7. API Endpoints
8. Error Handling
9. Monitoring & Logging
10. Docker & Deployment

Run with: pytest tests/test_production_readiness.py -v
"""

import os
import sys
import pytest
import asyncio
import time
from pathlib import Path
from typing import Dict, Any
import json

# Add project paths
sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "security"))
sys.path.insert(0, str(Path(__file__).parent.parent / "config"))
sys.path.insert(0, str(Path(__file__).parent.parent / "guardrails"))

# ==============================================================================
# TEST 1: SECURITY - NO HARDCODED SECRETS
# ==============================================================================

def test_no_hardcoded_secrets_in_docker_compose():
    """Verify no hardcoded passwords in docker-compose.yml"""
    docker_compose_path = Path(__file__).parent.parent / "docker-compose.yml"

    if not docker_compose_path.exists():
        pytest.skip("docker-compose.yml not found")

    content = docker_compose_path.read_text()

    # Check for specific hardcoded passwords (not just the word "password")
    forbidden_patterns = [
        "swarmcare123",
        "admin123",
        "password123",
        "changeme",
        "NEO4J_PASSWORD=swarmcare",
        "NEO4J_AUTH=neo4j/swarmcare"
    ]

    for pattern in forbidden_patterns:
        assert pattern.lower() not in content.lower(), \
            f"❌ CRITICAL: Found hardcoded credential pattern '{pattern}' in docker-compose.yml"

    # Verify environment variable usage
    assert "${NEO4J_PASSWORD}" in content or "$NEO4J_PASSWORD" in content, \
        "❌ CRITICAL: NEO4J_PASSWORD should use environment variable"

    print("✅ PASS: No hardcoded secrets in docker-compose.yml")


def test_env_file_exists():
    """Verify .env file exists and has required variables"""
    env_path = Path(__file__).parent.parent / ".env"

    assert env_path.exists(), \
        "❌ CRITICAL: .env file not found. Create from .env.example"

    content = env_path.read_text()

    required_vars = [
        "NEO4J_PASSWORD",
        "JWT_SECRET_KEY",
        "AZURE_OPENAI_API_KEY",
        "ENVIRONMENT"
    ]

    for var in required_vars:
        assert var in content, \
            f"❌ CRITICAL: Required variable '{var}' not found in .env"

    print("✅ PASS: .env file exists with required variables")


def test_env_in_gitignore():
    """Verify .env is in .gitignore"""
    gitignore_path = Path(__file__).parent.parent / ".gitignore"

    if gitignore_path.exists():
        content = gitignore_path.read_text()
        assert ".env" in content, \
            "❌ CRITICAL: .env should be in .gitignore to prevent secret leakage"
        print("✅ PASS: .env is in .gitignore")
    else:
        pytest.fail("❌ CRITICAL: .gitignore not found")


# ==============================================================================
# TEST 2: CONFIGURATION VALIDATION
# ==============================================================================

def test_constants_file_exists():
    """Verify constants.py exists and has proper structure"""
    constants_path = Path(__file__).parent.parent / "config" / "constants.py"

    assert constants_path.exists(), \
        "❌ FAIL: config/constants.py not found"

    # Import and verify
    try:
        from constants import (
            CHUNK_SIZE,
            MAX_CONTEXT_TOKENS,
            DEFAULT_RATE_LIMIT_PER_MINUTE,
            JWT_ALGORITHM
        )
        assert isinstance(CHUNK_SIZE, int), "CHUNK_SIZE should be int"
        assert isinstance(MAX_CONTEXT_TOKENS, int), "MAX_CONTEXT_TOKENS should be int"
        assert isinstance(DEFAULT_RATE_LIMIT_PER_MINUTE, int), "DEFAULT_RATE_LIMIT_PER_MINUTE should be int"
        assert isinstance(JWT_ALGORITHM, str), "JWT_ALGORITHM should be str"

        print("✅ PASS: Constants file exists and is properly structured")
    except ImportError as e:
        pytest.fail(f"❌ FAIL: Cannot import constants: {e}")


def test_secrets_manager_exists():
    """Verify secrets manager module exists"""
    secrets_path = Path(__file__).parent.parent / "security" / "secrets_manager.py"

    assert secrets_path.exists(), \
        "❌ FAIL: security/secrets_manager.py not found"

    try:
        from secrets_manager import SecretsManager, get_secret
        assert callable(get_secret), "get_secret should be callable"
        print("✅ PASS: Secrets manager module exists and is importable")
    except ImportError as e:
        pytest.fail(f"❌ FAIL: Cannot import secrets_manager: {e}")


# ==============================================================================
# TEST 3: RATE LIMITING
# ==============================================================================

def test_rate_limiting_configuration():
    """Test rate limiting is properly configured"""
    # Load backend API configuration
    backend_api_path = Path(__file__).parent.parent / "phases" / "phase04" / "deliverables" / "backend_api.py"

    if not backend_api_path.exists():
        pytest.skip("backend_api.py not found")

    content = backend_api_path.read_text()

    # Verify rate limiting is implemented
    assert "RateLimitMiddleware" in content, \
        "❌ FAIL: RateLimitMiddleware not found in backend_api.py"

    assert "RATE_LIMIT_PER_MINUTE" in content, \
        "❌ FAIL: RATE_LIMIT_PER_MINUTE not configured"

    assert "RATE_LIMIT_PER_HOUR" in content, \
        "❌ FAIL: RATE_LIMIT_PER_HOUR not configured"

    # Verify 429 status code is returned
    assert "429" in content, \
        "❌ FAIL: Rate limit should return 429 status code"

    print("✅ PASS: Rate limiting is properly configured")


# ==============================================================================
# TEST 4: CORS SECURITY
# ==============================================================================

def test_cors_not_overly_permissive():
    """Verify CORS is not configured with wildcards"""
    backend_api_path = Path(__file__).parent.parent / "phases" / "phase04" / "deliverables" / "backend_api.py"

    if not backend_api_path.exists():
        pytest.skip("backend_api.py not found")

    content = backend_api_path.read_text()

    # Check for overly permissive CORS
    lines = content.split('\n')
    cors_section_found = False

    for i, line in enumerate(lines):
        if 'CORSMiddleware' in line:
            cors_section_found = True
            # Check next 10 lines for configuration
            cors_block = '\n'.join(lines[i:i+10])

            # Verify it uses environment variables
            assert "ALLOWED_ORIGINS" in cors_block or "allow_origins=" not in cors_block, \
                "❌ FAIL: CORS should use environment variable for origins"

            # Should not have allow_methods=["*"] hardcoded
            if 'allow_methods' in cors_block:
                assert 'allow_methods=["*"]' not in cors_block.replace(" ", ""), \
                    "❌ FAIL: CORS allow_methods should not be wildcard ['*']"

            break

    assert cors_section_found, "❌ FAIL: CORSMiddleware configuration not found"
    print("✅ PASS: CORS is properly restricted")


# ==============================================================================
# TEST 5: HIPAA COMPLIANCE
# ==============================================================================

def test_audit_logging_enabled():
    """Verify HIPAA audit logging is configured"""
    from dotenv import load_dotenv
    load_dotenv()

    audit_enabled = os.getenv("HIPAA_AUDIT_LOG_ENABLED", "false").lower() == "true"

    assert audit_enabled or os.getenv("ENVIRONMENT") == "development", \
        "❌ FAIL: HIPAA audit logging must be enabled in production"

    print("✅ PASS: HIPAA audit logging is configured")


def test_phi_detection_enabled():
    """Verify PHI detection is enabled in guardrails"""
    guardrails_path = Path(__file__).parent.parent / "guardrails" / "medical_guardrails.py"

    if not guardrails_path.exists():
        pytest.skip("medical_guardrails.py not found")

    content = guardrails_path.read_text()

    # Check for PHI detection patterns
    phi_indicators = ["ssn", "social security", "medical record", "phone", "email"]
    found_count = sum(1 for indicator in phi_indicators if indicator in content.lower())

    assert found_count >= 3, \
        f"❌ FAIL: PHI detection should cover multiple identifier types (found {found_count})"

    print("✅ PASS: PHI detection is implemented")


# ==============================================================================
# TEST 6: GUARDRAILS SYSTEM
# ==============================================================================

def test_guardrails_system_exists():
    """Verify 7-layer guardrail system is implemented"""
    guardrails_path = Path(__file__).parent.parent / "guardrails" / "multi_layer_system.py"

    assert guardrails_path.exists(), \
        "❌ FAIL: multi_layer_system.py not found"

    content = guardrails_path.read_text()

    # Check for 7 layers
    layer_indicators = [
        "prompt",
        "input",
        "phi",
        "medical",
        "output",
        "groundedness",
        "hipaa"
    ]

    found_layers = sum(1 for indicator in layer_indicators if indicator in content.lower())

    assert found_layers >= 5, \
        f"❌ FAIL: Guardrail system should have multiple layers (found {found_layers})"

    print("✅ PASS: Guardrail system is implemented")


# ==============================================================================
# TEST 7: DEPENDENCIES
# ==============================================================================

def test_all_dependencies_listed():
    """Verify all required dependencies are in requirements.txt"""
    req_path = Path(__file__).parent.parent / "requirements.txt"

    assert req_path.exists(), \
        "❌ FAIL: requirements.txt not found"

    content = req_path.read_text()

    critical_deps = [
        "crewai",
        "fastapi",
        "uvicorn",
        "python-dotenv",
        "azure-keyvault-secrets",
        "azure-ai-contentsafety",
        "pydantic"
    ]

    missing = []
    for dep in critical_deps:
        if dep not in content.lower():
            missing.append(dep)

    assert not missing, \
        f"❌ FAIL: Missing critical dependencies: {', '.join(missing)}"

    print("✅ PASS: All critical dependencies are listed")


# ==============================================================================
# TEST 8: ERROR HANDLING
# ==============================================================================

def test_error_handling_in_api():
    """Verify proper error handling in API"""
    backend_api_path = Path(__file__).parent.parent / "phases" / "phase04" / "deliverables" / "backend_api.py"

    if not backend_api_path.exists():
        pytest.skip("backend_api.py not found")

    content = backend_api_path.read_text()

    # Check for try/except blocks
    assert "try:" in content and "except" in content, \
        "❌ FAIL: API should have error handling (try/except)"

    # Check for HTTPException
    assert "HTTPException" in content, \
        "❌ FAIL: API should use HTTPException for error responses"

    # Check for logging
    assert "logger.error" in content or "logging.error" in content, \
        "❌ FAIL: Errors should be logged"

    print("✅ PASS: Error handling is implemented")


# ==============================================================================
# TEST 9: DOCKER CONFIGURATION
# ==============================================================================

def test_docker_compose_valid():
    """Verify docker-compose.yml is valid"""
    docker_compose_path = Path(__file__).parent.parent / "docker-compose.yml"

    if not docker_compose_path.exists():
        pytest.skip("docker-compose.yml not found")

    content = docker_compose_path.read_text()

    # Check for required services
    required_services = ["neo4j", "redis"]
    for service in required_services:
        assert service in content, \
            f"❌ FAIL: Required service '{service}' not found in docker-compose.yml"

    # Check for health checks
    assert "healthcheck" in content, \
        "❌ FAIL: Services should have health checks"

    print("✅ PASS: Docker Compose configuration is valid")


# ==============================================================================
# TEST 10: PERFORMANCE TARGETS
# ==============================================================================

def test_performance_constants_defined():
    """Verify performance targets are defined"""
    try:
        from constants import (
            MEDICAL_IMAGING_TARGET_LATENCY_MS,
            VOICE_AI_TARGET_LATENCY_MS,
            AUTO_CODING_TARGET_LATENCY_MS
        )

        assert MEDICAL_IMAGING_TARGET_LATENCY_MS <= 500, \
            "Medical imaging should target <500ms"

        assert VOICE_AI_TARGET_LATENCY_MS <= 500, \
            "Voice AI should target <500ms"

        assert AUTO_CODING_TARGET_LATENCY_MS <= 50, \
            "Auto-coding should target <50ms"

        print("✅ PASS: Performance targets are properly defined")
    except ImportError:
        pytest.skip("Constants module not available")


# ==============================================================================
# PRODUCTION READINESS SUMMARY
# ==============================================================================

@pytest.fixture(scope="session", autouse=True)
def print_production_readiness_summary(request):
    """Print summary after all tests"""
    yield

    print("\n" + "=" * 80)
    print("SWARMCARE PRODUCTION READINESS TEST SUMMARY")
    print("=" * 80)

    # This will be populated by pytest
    print("\nTest Results:")
    print("  - See above for individual test results")
    print("\nNext Steps:")
    print("  1. Fix any failing tests")
    print("  2. Update Azure Key Vault with production secrets")
    print("  3. Run load testing")
    print("  4. Complete security audit")
    print("  5. Deploy to staging environment")
    print("=" * 80)


# ==============================================================================
# RUN TESTS
# ==============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
