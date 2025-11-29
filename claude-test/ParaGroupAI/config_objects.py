#!/usr/bin/env python3
"""
Configuration Objects for ULTRATHINK System
Provides dataclass-based config objects for type-safe configuration management.

This module wraps UltrathinkConfig from config.py with typed dataclasses
for use in tests and production code requiring structured config objects.
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from config import UltrathinkConfig


@dataclass
class OrchestratorConfig:
    """Configuration for Master Orchestrator"""

    # Confidence thresholds
    confidence_production: float = UltrathinkConfig.CONFIDENCE_PRODUCTION
    confidence_verification: float = UltrathinkConfig.CONFIDENCE_VERIFICATION

    # Iteration limits
    max_refinement_iterations: int = UltrathinkConfig.MAX_REFINEMENT_ITERATIONS
    min_iterations_before_early_exit: int = UltrathinkConfig.MIN_ITERATIONS_BEFORE_EARLY_EXIT

    # Performance
    guardrail_timeout_seconds: float = UltrathinkConfig.GUARDRAIL_TIMEOUT_SECONDS
    parallel_agents_max: int = UltrathinkConfig.PARALLEL_AGENTS_MAX

    # Context management
    context_window_tokens: int = UltrathinkConfig.CONTEXT_WINDOW_TOKENS
    context_compaction_threshold: float = UltrathinkConfig.CONTEXT_COMPACTION_THRESHOLD
    context_min_compaction_ratio: float = UltrathinkConfig.CONTEXT_MIN_COMPACTION_RATIO

    # Database-first architecture
    db_first_enabled: bool = UltrathinkConfig.DB_FIRST_ENABLED
    db_path: str = UltrathinkConfig.DB_PATH
    db_postgresql_url: Optional[str] = UltrathinkConfig.DB_POSTGRESQL_URL
    db_redis_url: Optional[str] = UltrathinkConfig.DB_REDIS_URL

    # Model configuration
    claude_model_name: str = UltrathinkConfig.CLAUDE_MODEL_NAME
    claude_max_tokens: int = UltrathinkConfig.CLAUDE_MAX_TOKENS

    # Quality scoring weights
    quality_weight_prompt: float = UltrathinkConfig.QUALITY_WEIGHT_PROMPT
    quality_weight_agents: float = UltrathinkConfig.QUALITY_WEIGHT_AGENTS
    quality_weight_guardrails: float = UltrathinkConfig.QUALITY_WEIGHT_GUARDRAILS
    quality_weight_efficiency: float = UltrathinkConfig.QUALITY_WEIGHT_EFFICIENCY
    quality_weight_verification: float = UltrathinkConfig.QUALITY_WEIGHT_VERIFICATION

    # Response formatting
    response_format_ultrathink: bool = UltrathinkConfig.RESPONSE_FORMAT_ULTRATHINK
    response_section_width: int = UltrathinkConfig.RESPONSE_SECTION_WIDTH
    response_verbose_indent: int = UltrathinkConfig.RESPONSE_VERBOSE_INDENT

    # Testing
    test_mode: bool = UltrathinkConfig.TEST_MODE
    test_mock_claude_responses: bool = UltrathinkConfig.TEST_MOCK_CLAUDE_RESPONSES


@dataclass
class SecurityConfig:
    """Configuration for Security and Sanitization"""

    # Prompt injection patterns
    prompt_injection_patterns_high_confidence: List[str] = field(
        default_factory=lambda: UltrathinkConfig.PROMPT_INJECTION_PATTERNS_HIGH_CONFIDENCE.copy()
    )
    prompt_injection_patterns_medium_confidence: List[str] = field(
        default_factory=lambda: UltrathinkConfig.PROMPT_INJECTION_PATTERNS_MEDIUM_CONFIDENCE.copy()
    )

    # Prompt limits
    prompt_max_length_chars: Optional[int] = UltrathinkConfig.PROMPT_MAX_LENGTH_CHARS

    # File access
    allowed_prompt_file_base_dirs: List[str] = field(
        default_factory=lambda: UltrathinkConfig.ALLOWED_PROMPT_FILE_BASE_DIRS.copy()
    )

    # Logging
    log_security_events_to_file: bool = UltrathinkConfig.LOG_SECURITY_EVENTS_TO_FILE
    log_security_file_path: str = UltrathinkConfig.LOG_SECURITY_FILE_PATH

    # Dependency scanning
    dependency_scan_on_startup: bool = UltrathinkConfig.DEPENDENCY_SCAN_ON_STARTUP
    dependency_scan_cache_hours: int = UltrathinkConfig.DEPENDENCY_SCAN_CACHE_HOURS


@dataclass
class PerformanceConfig:
    """Configuration for Performance and Rate Limiting"""

    # Rate limiting
    rate_limit_calls: int = UltrathinkConfig.RATE_LIMIT_CALLS
    rate_limit_window: int = UltrathinkConfig.RATE_LIMIT_WINDOW

    # Token counting
    token_counting_recount_threshold: float = UltrathinkConfig.TOKEN_COUNTING_RECOUNT_THRESHOLD

    # Parallel execution
    parallel_agents_max: int = UltrathinkConfig.PARALLEL_AGENTS_MAX

    # Guardrail timeout
    guardrail_timeout_seconds: float = UltrathinkConfig.GUARDRAIL_TIMEOUT_SECONDS

    # Database performance
    db_context_priority_critical_load_time_ms: int = UltrathinkConfig.DB_CONTEXT_PRIORITY_CRITICAL_LOAD_TIME_MS
    db_token_clear_threshold: float = UltrathinkConfig.DB_TOKEN_CLEAR_THRESHOLD
    db_heartbeat_interval_seconds: int = UltrathinkConfig.DB_HEARTBEAT_INTERVAL_SECONDS
    db_cleanup_stale_instances_seconds: int = UltrathinkConfig.DB_CLEANUP_STALE_INSTANCES_SECONDS


@dataclass
class DatabaseConfig:
    """Configuration for Database Management"""

    # Database paths
    db_path: str = UltrathinkConfig.DB_PATH
    db_postgresql_url: Optional[str] = UltrathinkConfig.DB_POSTGRESQL_URL
    db_redis_url: Optional[str] = UltrathinkConfig.DB_REDIS_URL

    # Database-first architecture
    db_first_enabled: bool = UltrathinkConfig.DB_FIRST_ENABLED

    # Performance
    db_context_priority_critical_load_time_ms: int = UltrathinkConfig.DB_CONTEXT_PRIORITY_CRITICAL_LOAD_TIME_MS
    db_token_clear_threshold: float = UltrathinkConfig.DB_TOKEN_CLEAR_THRESHOLD

    # Multi-project support
    db_max_projects: int = UltrathinkConfig.DB_MAX_PROJECTS
    db_max_instances_per_project: int = UltrathinkConfig.DB_MAX_INSTANCES_PER_PROJECT

    # Health monitoring
    db_heartbeat_interval_seconds: int = UltrathinkConfig.DB_HEARTBEAT_INTERVAL_SECONDS
    db_cleanup_stale_instances_seconds: int = UltrathinkConfig.DB_CLEANUP_STALE_INSTANCES_SECONDS


@dataclass
class LoggingConfig:
    """Configuration for Logging"""

    # Log level
    log_level_default: str = UltrathinkConfig.LOG_LEVEL_DEFAULT

    # Security logging
    log_security_events_to_file: bool = UltrathinkConfig.LOG_SECURITY_EVENTS_TO_FILE
    log_security_file_path: str = UltrathinkConfig.LOG_SECURITY_FILE_PATH


@dataclass
class ConfidenceConfig:
    """Configuration for Confidence Thresholds"""

    # Production confidence target
    confidence_production: float = UltrathinkConfig.CONFIDENCE_PRODUCTION
    confidence_verification: float = UltrathinkConfig.CONFIDENCE_VERIFICATION

    # Minimum iterations
    min_iterations_before_early_exit: int = UltrathinkConfig.MIN_ITERATIONS_BEFORE_EARLY_EXIT


@dataclass
class GuardrailsConfig:
    """Configuration for Guardrails System"""

    # Performance
    guardrail_timeout_seconds: float = UltrathinkConfig.GUARDRAIL_TIMEOUT_SECONDS

    # Quality weights
    quality_weight_guardrails: float = UltrathinkConfig.QUALITY_WEIGHT_GUARDRAILS

    # Logging
    log_security_events_to_file: bool = UltrathinkConfig.LOG_SECURITY_EVENTS_TO_FILE


# =============================================================================
# FACTORY FUNCTIONS
# =============================================================================

def get_default_orchestrator_config() -> OrchestratorConfig:
    """Get default orchestrator configuration"""
    return OrchestratorConfig()


def get_default_security_config() -> SecurityConfig:
    """Get default security configuration"""
    return SecurityConfig()


def get_default_performance_config() -> PerformanceConfig:
    """Get default performance configuration"""
    return PerformanceConfig()


def get_default_database_config() -> DatabaseConfig:
    """Get default database configuration"""
    return DatabaseConfig()


def get_default_logging_config() -> LoggingConfig:
    """Get default logging configuration"""
    return LoggingConfig()


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

def get_all_configs() -> Dict[str, Any]:
    """Get all configuration objects as a dictionary"""
    return {
        "orchestrator": get_default_orchestrator_config(),
        "security": get_default_security_config(),
        "performance": get_default_performance_config(),
        "database": get_default_database_config(),
        "logging": get_default_logging_config(),
    }


if __name__ == "__main__":
    """Demonstrate config objects usage"""

    print("ULTRATHINK Configuration Objects")
    print("=" * 70)

    orch_config = get_default_orchestrator_config()
    print(f"Orchestrator - Max iterations: {orch_config.max_refinement_iterations}")
    print(f"Orchestrator - Parallel agents: {orch_config.parallel_agents_max}")

    sec_config = get_default_security_config()
    print(f"Security - Max prompt length: {sec_config.prompt_max_length_chars}")

    perf_config = get_default_performance_config()
    print(f"Performance - Rate limit: {perf_config.rate_limit_calls} calls/{perf_config.rate_limit_window}s")

    print("\n✅ All config objects initialized successfully")
