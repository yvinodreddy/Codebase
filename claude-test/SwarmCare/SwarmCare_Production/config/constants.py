"""
SwarmCare Application Constants
Centralized configuration values to replace magic numbers

All configuration values should be defined here as named constants
to improve code maintainability and readability.
"""

# ==============================================================================
# RAG SYSTEM CONSTANTS (Phase 1)
# ==============================================================================

# Document chunking
CHUNK_SIZE = 512
CHUNK_OVERLAP = 128
MAX_CHUNKS_PER_DOCUMENT = 1000

# Vector search
DEFAULT_TOP_K = 5
MAX_TOP_K = 100
MIN_SIMILARITY_SCORE = 0.7

# Embeddings
EMBEDDING_DIMENSION = 1536  # OpenAI ada-002
EMBEDDING_MODEL = "text-embedding-ada-002"

# ==============================================================================
# CONTEXT MANAGEMENT (Agent Framework)
# ==============================================================================

# Token limits
MAX_CONTEXT_TOKENS = 100_000
COMPACTION_THRESHOLD = 0.8  # Compact at 80% of max tokens
MIN_CONTEXT_TOKENS = 1000

# Summary lengths
SHORT_SUMMARY_LENGTH = 200
MEDIUM_SUMMARY_LENGTH = 500
LONG_SUMMARY_LENGTH = 1000

# ==============================================================================
# AGENT SYSTEM CONSTANTS (Phase 2)
# ==============================================================================

# Agent execution
MAX_AGENT_RETRIES = 3
AGENT_TIMEOUT_SECONDS = 300  # 5 minutes
MAX_PARALLEL_AGENTS = 5

# Task execution
TASK_RETRY_DELAY_SECONDS = 2
TASK_MAX_EXECUTION_TIME = 600  # 10 minutes

# ==============================================================================
# GUARDRAILS CONSTANTS
# ==============================================================================

# Layer configuration
TOTAL_GUARDRAIL_LAYERS = 7
MAX_VALIDATION_RETRIES = 3

# Content filtering thresholds
CONTENT_SAFETY_THRESHOLD_LOW = 0.3
CONTENT_SAFETY_THRESHOLD_MEDIUM = 0.5
CONTENT_SAFETY_THRESHOLD_HIGH = 0.7

# PHI detection
PHI_PATTERN_COUNT = 18  # Number of HIPAA identifiers
PHI_DETECTION_CONFIDENCE_THRESHOLD = 0.85

# Medical terminology
MEDICAL_ONTOLOGY_COUNT = 13
MIN_MEDICAL_TERM_LENGTH = 3
MAX_MEDICAL_TERM_LENGTH = 100

# Groundedness detection
GROUNDEDNESS_THRESHOLD = 0.8
MAX_HALLUCINATION_RATE = 0.1

# ==============================================================================
# API CONSTANTS (Phase 4)
# ==============================================================================

# Rate limiting
DEFAULT_RATE_LIMIT_PER_MINUTE = 60
DEFAULT_RATE_LIMIT_PER_HOUR = 1000
RATE_LIMIT_BURST_SIZE = 10

# Request limits
MAX_REQUEST_SIZE_MB = 10
MAX_QUERY_LENGTH = 5000
MIN_QUERY_LENGTH = 1

# Response limits
MAX_RESPONSE_SIZE_MB = 50
MAX_STREAMING_CHUNK_SIZE = 4096

# Timeouts
API_REQUEST_TIMEOUT = 30  # seconds
WEBSOCKET_PING_INTERVAL = 30  # seconds
WEBSOCKET_TIMEOUT = 300  # 5 minutes

# ==============================================================================
# DATABASE CONSTANTS
# ==============================================================================

# Neo4j
NEO4J_DEFAULT_PORT = 7687
NEO4J_BROWSER_PORT = 7474
NEO4J_MAX_CONNECTION_POOL_SIZE = 50
NEO4J_CONNECTION_TIMEOUT = 30
NEO4J_MAX_TRANSACTION_RETRY = 3

# Redis
REDIS_DEFAULT_PORT = 6379
REDIS_DEFAULT_DB = 0
REDIS_DEFAULT_TTL = 3600  # 1 hour
REDIS_MAX_CONNECTIONS = 50

# ==============================================================================
# AUTHENTICATION & SECURITY
# ==============================================================================

# JWT
JWT_ALGORITHM = "RS256"
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 30
JWT_REFRESH_TOKEN_EXPIRE_DAYS = 7
JWT_ISSUER = "swarmcare"

# Password requirements
MIN_PASSWORD_LENGTH = 12
PASSWORD_REQUIRE_UPPERCASE = True
PASSWORD_REQUIRE_LOWERCASE = True
PASSWORD_REQUIRE_DIGITS = True
PASSWORD_REQUIRE_SPECIAL = True

# Session
SESSION_TIMEOUT_MINUTES = 30
MAX_CONCURRENT_SESSIONS = 5

# Encryption
ENCRYPTION_ALGORITHM = "AES-256-GCM"
ENCRYPTION_KEY_LENGTH = 32  # bytes

# ==============================================================================
# HIPAA COMPLIANCE (Phase 6)
# ==============================================================================

# Audit logging
AUDIT_LOG_RETENTION_DAYS = 2555  # 7 years
AUDIT_LOG_MAX_SIZE_MB = 100

# PHI encryption
PHI_FIELD_ENCRYPTION_ENABLED = True
PHI_AT_REST_ENCRYPTION_ENABLED = True
PHI_IN_TRANSIT_ENCRYPTION_ENABLED = True

# ==============================================================================
# PERFORMANCE & SCALING
# ==============================================================================

# Concurrency
MAX_CONCURRENT_REQUESTS = 100
MAX_WORKER_THREADS = 4
MAX_ASYNC_TASKS = 50

# Caching
CACHE_DEFAULT_TTL = 300  # 5 minutes
CACHE_MAX_SIZE_MB = 500

# Batch processing
BATCH_SIZE = 100
MAX_BATCH_SIZE = 1000

# ==============================================================================
# MONITORING & METRICS
# ==============================================================================

# Metrics collection
METRICS_COLLECTION_INTERVAL = 60  # seconds
METRICS_RETENTION_DAYS = 90

# Health checks
HEALTH_CHECK_INTERVAL = 30  # seconds
HEALTH_CHECK_TIMEOUT = 5  # seconds

# Alerting
ALERT_THRESHOLD_ERROR_RATE = 0.05  # 5%
ALERT_THRESHOLD_LATENCY_MS = 1000  # 1 second
ALERT_THRESHOLD_CPU_PERCENT = 80
ALERT_THRESHOLD_MEMORY_PERCENT = 85

# ==============================================================================
# PHASE-SPECIFIC CONSTANTS
# ==============================================================================

# Phase 14: Medical Imaging
MEDICAL_IMAGING_MAX_SIZE_MB = 500
MEDICAL_IMAGING_TARGET_LATENCY_MS = 500
DICOM_MAX_SERIES_SIZE = 1000

# Phase 19 & 28: Voice AI
VOICE_AI_TARGET_LATENCY_MS = 500
VOICE_AI_SAMPLE_RATE = 16000
VOICE_AI_CHANNELS = 1
VOICE_AI_CHUNK_DURATION_MS = 100

# Phase 24: EHR Integration
EHR_SYNC_INTERVAL_MINUTES = 15
EHR_BATCH_SIZE = 50
FHIR_API_VERSION = "R4"

# Phase 15: Medical NLP
ICD10_CODE_LENGTH = 7
CPT_CODE_LENGTH = 5
LOINC_CODE_LENGTH = 7
AUTO_CODING_TARGET_LATENCY_MS = 40

# ==============================================================================
# ERROR CODES
# ==============================================================================

# Custom error codes for SwarmCare
ERROR_CODE_GUARDRAIL_FAILURE = 1000
ERROR_CODE_PHI_DETECTED = 1001
ERROR_CODE_MEDICAL_VALIDATION_FAILED = 1002
ERROR_CODE_HIPAA_VIOLATION = 1003
ERROR_CODE_RATE_LIMIT_EXCEEDED = 1004
ERROR_CODE_AUTHENTICATION_FAILED = 1005
ERROR_CODE_AUTHORIZATION_FAILED = 1006
ERROR_CODE_INVALID_REQUEST = 1007
ERROR_CODE_RESOURCE_NOT_FOUND = 1008
ERROR_CODE_INTERNAL_ERROR = 1009

# ==============================================================================
# VERSION INFORMATION
# ==============================================================================

SWARMCARE_VERSION = "2.1.0"
API_VERSION = "1.0.0"
GUARDRAILS_VERSION = "1.0.0"
