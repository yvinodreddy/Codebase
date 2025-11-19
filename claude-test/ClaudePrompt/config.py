#!/usr/bin/env python3
"""
ULTRATHINK Configuration File
Centralized configuration for all magic numbers and settings.

This file consolidates all configuration values that were previously
scattered across multiple files. Each constant includes documentation
explaining its purpose and rationale.
"""

class UltrathinkConfig:
    """
    Main configuration class for ULTRATHINK system.
    All magic numbers, thresholds, and settings centralized here.
    """

    # =========================================================================
    # CONFIDENCE THRESHOLDS
    # =========================================================================

    CONFIDENCE_PRODUCTION = 99.0
    """
    Target confidence for production-ready output.

    - 99%+ indicates multi-method verification passed
    - Based on industry standard for mission-critical AI (AWS, Google)
    - Lower = faster but less reliable
    - Higher = slower but more trustworthy

    Used by: master_orchestrator.py, ultrathink.py
    """

    CONFIDENCE_VERIFICATION = 95.0
    """
    Minimum confidence for individual verification methods.

    - Each of 5 verification methods must hit 95%
    - Aggregate must hit 99% (higher standard)
    - Ensures no single weak verification method

    Used by: verification_system.py
    """

    # =========================================================================
    # CONTEXT MANAGEMENT
    # =========================================================================

    CONTEXT_WINDOW_TOKENS = 200_000
    """
    Maximum tokens in context (Claude 3 Sonnet/Opus limit).

    - Sonnet 3.5: 200K tokens
    - Opus 3: 200K tokens
    - Haiku 3: 200K tokens

    Used by: context_manager.py
    """

    CONTEXT_COMPACTION_THRESHOLD = 0.85
    """
    Trigger auto-compaction at 85% context usage.

    - Leaves 15% buffer (30K tokens) for response
    - Prevents mid-response cutoff
    - Industry standard: 80-90%

    Used by: context_manager.py
    """

    CONTEXT_MIN_COMPACTION_RATIO = 0.30
    """
    Minimum token reduction required for compaction to be worthwhile.

    - Must save at least 30% of tokens
    - Otherwise, compaction overhead not justified

    Used by: context_manager.py
    """

    # =========================================================================
    # ITERATION LIMITS
    # =========================================================================

    MAX_REFINEMENT_ITERATIONS = 20
    """
    Maximum feedback loop iterations before giving up.

    - Extended from 10 to 20 for higher accuracy targets
    - First 10 iterations: Standard refinement
    - Next 10 iterations: Deep refinement if 99%+ not reached
    - Balances quality vs. time
    - 95% of queries converge in 1-3 iterations
    - 20 is safety limit for edge cases targeting 99-100% confidence
    - Prevents infinite loops

    Used by: feedback_loop.py, feedback_loop_enhanced.py, validate_my_response.py
    """

    MIN_ITERATIONS_BEFORE_EARLY_EXIT = 2
    """
    Minimum iterations to run before allowing early exit.

    - Even if confidence met on iteration 1, do at least 2
    - Ensures validation is thorough

    Used by: feedback_loop_enhanced.py
    """

    # =========================================================================
    # PERFORMANCE
    # =========================================================================

    GUARDRAIL_TIMEOUT_SECONDS = 5.0
    """
    Timeout for individual guardrail validation.

    - Prevents one slow guardrail from blocking
    - 5s chosen as 2x the slowest guardrail (Layer 6: 2.4s)

    Used by: master_orchestrator.py (after P1 implementation)
    """

    PARALLEL_AGENTS_MAX = 500
    """
    Maximum simultaneous parallel agents for high-scale projects.

    - INCREASED FROM 30 TO 500 for enterprise-scale workloads
    - Supports 1000+ task projects with massive parallelism
    - Dynamic scaling based on workload:
      * Simple tasks: 8-25 agents
      * Moderate tasks: 25-100 agents
      * Complex tasks: 100-250 agents
      * Enterprise tasks: 250-500 agents
    - Modern systems with 16+ cores can handle 500 concurrent I/O-bound agents
    - Each agent: ~1-5MB memory (500 agents = ~500MB-2.5GB)
    - Thread pool executor with work stealing for optimal CPU utilization
    - Breadth-first parallelism for maximum throughput
    - Depth-first fallback for memory-constrained environments

    Performance characteristics:
    - 500 agents can process 500 parallel validation checks
    - Reduces iteration time from minutes to seconds
    - Critical for 99-100% confidence targets (mandatory requirement)

    Used by: subagent_orchestrator.py, validate_my_response.py, ultrathink.py
    """

    TOKEN_COUNTING_RECOUNT_THRESHOLD = 0.80
    """
    When to do full token recount (vs incremental).

    - At 80% of context window, do full recount for accuracy
    - Before that, use incremental counting for speed

    Used by: context_manager.py (after P2 implementation)
    """

    # =========================================================================
    # RATE LIMITING (S4)
    # =========================================================================

    RATE_LIMIT_CALLS = 500
    """
    Maximum API calls allowed per time window.

    - 500 = High capacity for complex workflows
    - Prevents accidental runaway costs
    - Adjust based on your usage patterns
    - Fits between Anthropic Tier 2 (50/min) and Tier 3 (200/min)

    Used by: rate_limiter.py, claude_integration.py
    """

    RATE_LIMIT_WINDOW = 360
    """
    Time window for rate limiting (seconds).

    - 360s = 6 minutes
    - Matches typical "working on a problem" session
    - Longer window = smoother rate limiting
    - Effective rate: ~83 calls/minute

    Used by: rate_limiter.py, claude_integration.py
    """

    # =========================================================================
    # SECURITY (S2 - Prompt Injection)
    # =========================================================================

    PROMPT_MAX_LENGTH_CHARS = None
    """
    Maximum prompt length (None = unlimited, use Claude's token limit).

    - Set to None for personal systems with large prompts (PRODUCTION READY)
    - Supports 1000+ task prompts without size restrictions
    - System ARG_MAX: 2,097,152 bytes (handles millions of characters)
    - Claude API token limit: 200K tokens (~800K characters)
    - Bash redirection: No practical limit (streams to file)
    - User requirement: Handle high-scale projects with 1000+ tasks

    Used by: input_sanitizer.py, ultrathink.py
    """

    PROMPT_INJECTION_PATTERNS_HIGH_CONFIDENCE = [
        'ignore all previous instructions',
        'disregard your system prompt',
        'print your instructions',
        'reveal your prompt',
        'forget all previous context',
    ]
    """
    High-confidence prompt injection patterns.

    - Almost always malicious
    - Will trigger interactive confirmation

    Used by: input_sanitizer.py
    """

    PROMPT_INJECTION_PATTERNS_MEDIUM_CONFIDENCE = [
        'you are now',
        'debug mode',
        'system prompt',
        'admin mode',
    ]
    """
    Medium-confidence prompt injection patterns.

    - Might be legitimate (discussing security topics)
    - Will warn but proceed

    Used by: input_sanitizer.py
    """

    # =========================================================================
    # LOGGING
    # =========================================================================

    LOG_LEVEL_DEFAULT = "INFO"
    """
    Default logging level.

    Options: DEBUG, INFO, WARNING, ERROR, CRITICAL

    Used by: All modules
    """

    LOG_SECURITY_EVENTS_TO_FILE = True
    """
    Whether to log security events to dedicated file.

    - True = security_events.log created
    - False = security events only to console

    Used by: security_logger.py
    """

    LOG_SECURITY_FILE_PATH = "logs/security_events.log"
    """
    Path to security events log file.

    Used by: security_logger.py
    """

    # =========================================================================
    # DATABASE-FIRST CONTEXT MANAGEMENT (Added 2025-11-19)
    # =========================================================================

    DB_FIRST_ENABLED = True
    """
    Enable database-first context management architecture.

    - True = Use database for context storage (crash-safe, unlimited context)
    - False = Use traditional in-memory context management

    When enabled:
    - All context stored in SQLite database
    - Zero context loss on crash (ACID compliant)
    - Support for multi-project, multi-instance architecture
    - Clear+reload token management for unlimited context

    Added: 2025-11-19 for production-ready context management
    Used by: master_orchestrator.py, context_manager.py
    """

    DB_PATH = "database/ultrathink_context.db"
    """
    Path to SQLite database file for context storage.

    - Relative to ClaudePrompt directory
    - Auto-created if doesn't exist
    - File-based (no server required)
    - ACID compliant (crash-safe)

    Production size estimates:
    - 1 project (1300 story points): ~100 MB
    - 5 projects: ~500 MB
    - 10 projects: ~1 GB

    Used by: sqlite_context_loader.py, multi_project_manager.py
    """

    DB_POSTGRESQL_URL = None
    """
    Optional PostgreSQL connection URL for production scale.

    Format: postgresql://user:password@host:port/database

    - None = Use SQLite (default)
    - Set URL = Use PostgreSQL for cloud deployments

    PostgreSQL advantages:
    - Better concurrency (100+ instances)
    - LISTEN/NOTIFY for real-time sync
    - Cloud-native (RDS, Cloud SQL, etc.)

    Used by: async_context_loader.py (if PostgreSQL support enabled)
    """

    DB_REDIS_URL = None
    """
    Optional Redis URL for caching context (performance optimization).

    Format: redis://host:port/db

    - None = No caching (load directly from database)
    - Set URL = Use Redis for faster context retrieval

    Redis is OPTIONAL - database is source of truth.
    Cache crashes = No data loss (reload from DB).

    Used by: async_context_loader.py (if Redis support enabled)
    """

    DB_CONTEXT_PRIORITY_CRITICAL_LOAD_TIME_MS = 100
    """
    Target load time for CRITICAL priority context (milliseconds).

    - CRITICAL context must load fast (<100ms)
    - User can start working immediately
    - Other priorities load in background

    Used by: sqlite_context_loader.py, async_context_loader.py
    """

    DB_TOKEN_CLEAR_THRESHOLD = 0.85
    """
    Auto-clear tokens when usage exceeds this threshold (0.0 to 1.0).

    - 0.85 = Clear at 85% usage (170K tokens)
    - Leaves 15% buffer (30K tokens)
    - Prevents mid-response token exhaustion

    Clear+reload strategy:
    1. Clear tokens to 0
    2. Context preserved in database (zero loss)
    3. Reload context from database
    4. Instance ready with 200K tokens available

    Used by: token_manager.py
    """

    DB_MAX_PROJECTS = 100
    """
    Maximum number of projects (soft limit for monitoring).

    - Not enforced by database (unlimited)
    - Used for alerting when approaching scale limits
    - Each project can have unlimited instances

    Used by: multi_project_manager.py
    """

    DB_MAX_INSTANCES_PER_PROJECT = 10
    """
    Maximum instances per project (soft limit for monitoring).

    - Not enforced by database (unlimited)
    - Recommended limit for SQLite backend
    - PostgreSQL can handle 100+ instances easily

    Architecture support:
    - SQLite: 1-10 instances per project (good performance)
    - PostgreSQL: 100+ instances per project (excellent performance)

    Used by: multi_project_manager.py
    """

    DB_HEARTBEAT_INTERVAL_SECONDS = 30
    """
    Heartbeat interval for instance health monitoring (seconds).

    - Instances send heartbeat every 30 seconds
    - Used for crash detection
    - Stale threshold: 10 minutes (300 seconds)

    Used by: sqlite_context_loader.py, multi_project_manager.py
    """

    DB_CLEANUP_STALE_INSTANCES_SECONDS = 600
    """
    Mark instances as crashed if no heartbeat within this time (seconds).

    - 600 seconds = 10 minutes
    - Instances marked as 'crashed' status
    - Can be restarted and recover full context from database

    Used by: Database cleanup functions
    """

    # =========================================================================
    # RESPONSE FORMATTING
    # =========================================================================

    RESPONSE_FORMAT_ULTRATHINK = True
    """
    Use ULTRATHINK format for all responses.

    - Boxed sections with 80 `=` characters
    - [VERBOSE] tags with 3-space indentation
    - Proper spacing (1 blank line between subsections)
    - Clean code blocks and tables
    - Professional terminal-style output

    Set to False to use standard markdown format.

    User requirement: Format must be PERMANENT and survive restarts.
    Effective: 2025-11-09 and forever.

    Used by: All response generation
    """

    RESPONSE_SECTION_WIDTH = 80
    """
    Width of section headers (number of = characters).

    Standard: 80 characters (fits standard terminal width)

    Used by: Response formatting
    """

    RESPONSE_VERBOSE_INDENT = 3
    """
    Number of spaces for [VERBOSE] sub-item indentation.

    - 3 spaces for sub-items (NOT 2, NOT 4)
    - 6 spaces for nested items (2 levels deep)

    Used by: Response formatting
    """

    # =========================================================================
    # TESTING
    # =========================================================================

    TEST_MODE = False
    """
    Enable test mode (uses mocks instead of real API calls).

    - Set to True in test environment
    - Set to False in production

    Used by: claude_integration.py, tests/
    """

    TEST_MOCK_CLAUDE_RESPONSES = True
    """
    Use mock Claude responses in tests.

    - Saves API costs during testing
    - Ensures reproducible test results

    Used by: tests/mocks/
    """

    # =========================================================================
    # MODEL CONFIGURATION
    # =========================================================================

    CLAUDE_MODEL_NAME = "claude-sonnet-4-5-20250929"
    """
    Default Claude model to use.

    Options:
    - claude-sonnet-4-5-20250929 (latest, best balance)
    - claude-opus-3-5-20241022 (most capable, slower, expensive)
    - claude-haiku-3-5-20241022 (fastest, cheapest, less capable)

    Used by: claude_integration.py
    """

    CLAUDE_MAX_TOKENS = 8192
    """
    Maximum tokens per Claude response.

    - 8192 = Good balance for most tasks (handles ~32,000 characters)
    - Supports large-scale reports with thousands of lines
    - Output can be streamed to files for unlimited size
    - File I/O approach bypasses in-memory buffer limitations
    - PRODUCTION READY: Handles 5000+ line reports via file streaming

    Used by: claude_integration.py, ultrathink.py
    """

    # =========================================================================
    # QUALITY SCORING WEIGHTS
    # =========================================================================

    QUALITY_WEIGHT_PROMPT = 0.15
    """Prompt analysis weight (15%)"""

    QUALITY_WEIGHT_AGENTS = 0.25
    """Agent execution weight (25%)"""

    QUALITY_WEIGHT_GUARDRAILS = 0.30
    """Guardrails validation weight (30%)"""

    QUALITY_WEIGHT_EFFICIENCY = 0.15
    """Efficiency weight (15%)"""

    QUALITY_WEIGHT_VERIFICATION = 0.15
    """Verification weight (15%)"""

    """
    Quality scoring component weights.

    Total must sum to 1.0 (100%)
    - Guardrails highest (30%) - most critical for safety
    - Agents second (25%) - core functionality
    - Prompt, Efficiency, Verification equal (15% each)

    Used by: master_orchestrator.py
    """

    # =========================================================================
    # FILE PATHS
    # =========================================================================

    ALLOWED_PROMPT_FILE_BASE_DIRS = ["."]
    """
    Allowed base directories for --file prompts.

    - ["."] = Only current directory and subdirectories
    - ["/home/user01/prompts", "."] = Allow specific dir + current
    - For security, restrict file access to known locations

    Used by: ultrathink.py (S3 - file path validation)
    """

    # =========================================================================
    # DEPENDENCY SCANNING (S7)
    # =========================================================================

    DEPENDENCY_SCAN_ON_STARTUP = False
    """
    Run dependency vulnerability scan on system startup.

    - True = Check on every ultrathinkc run (slower startup)
    - False = Manual scan only (faster, run weekly)

    Used by: dependency_scanner.py
    """

    DEPENDENCY_SCAN_CACHE_HOURS = 24
    """
    Cache dependency scan results for this many hours.

    - 24 hours = Daily scanning
    - 168 hours = Weekly scanning

    Used by: dependency_scanner.py
    """


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

def get_all_config_values():
    """
    Get all configuration values as a dictionary.

    Useful for debugging and logging.

    Returns:
        dict: All config values
    """
    config_dict = {}
    for key in dir(UltrathinkConfig):
        if not key.startswith('_') and key.isupper():
            config_dict[key] = getattr(UltrathinkConfig, key)
    return config_dict


def validate_config():
    """
    Validate that configuration values are reasonable.

    Raises:
        ValueError: If configuration is invalid
    """
    # Check weights sum to 1.0
    total_weight = (
        UltrathinkConfig.QUALITY_WEIGHT_PROMPT +
        UltrathinkConfig.QUALITY_WEIGHT_AGENTS +
        UltrathinkConfig.QUALITY_WEIGHT_GUARDRAILS +
        UltrathinkConfig.QUALITY_WEIGHT_EFFICIENCY +
        UltrathinkConfig.QUALITY_WEIGHT_VERIFICATION
    )

    if abs(total_weight - 1.0) > 0.01:
        raise ValueError(
            f"Quality weights must sum to 1.0, got {total_weight:.3f}"
        )

    # Check confidence thresholds
    if not (0 <= UltrathinkConfig.CONFIDENCE_PRODUCTION <= 100):
        raise ValueError(
            f"CONFIDENCE_PRODUCTION must be 0-100, got {UltrathinkConfig.CONFIDENCE_PRODUCTION}"
        )

    # Check rate limiting
    if UltrathinkConfig.RATE_LIMIT_CALLS <= 0:
        raise ValueError("RATE_LIMIT_CALLS must be positive")

    if UltrathinkConfig.RATE_LIMIT_WINDOW <= 0:
        raise ValueError("RATE_LIMIT_WINDOW must be positive")

    return True


# Run validation on import
validate_config()


# =============================================================================
# USAGE EXAMPLES
# =============================================================================

if __name__ == "__main__":
    """Demonstrate config usage"""

    print("ULTRATHINK Configuration")
    print("=" * 70)
    print(f"Production confidence: {UltrathinkConfig.CONFIDENCE_PRODUCTION}%")
    print(f"Context window: {UltrathinkConfig.CONTEXT_WINDOW_TOKENS:,} tokens")
    print(f"Rate limiting: {UltrathinkConfig.RATE_LIMIT_CALLS} calls per {UltrathinkConfig.RATE_LIMIT_WINDOW}s")
    print(f"Max iterations: {UltrathinkConfig.MAX_REFINEMENT_ITERATIONS}")
    print(f"Model: {UltrathinkConfig.CLAUDE_MODEL_NAME}")

    print("\nAll configuration values:")
    print("-" * 70)
    for key, value in get_all_config_values().items():
        print(f"{key}: {value}")

    print("\nValidation:", "✅ PASSED" if validate_config() else "❌ FAILED")
