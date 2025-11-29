# ULTRATHINK API Documentation

## Base URL
```
http://localhost:8000
```

## Authentication
Currently no authentication required. Production deployment should add API keys.

## Endpoints

### Root
```
GET /
```
Returns API information and available endpoints.

**Response:**
```json
{
  "message": "ULTRATHINK API v2.0",
  "status": "operational",
  "endpoints": {...}
}
```

### Health Check
```
GET /health
```
Liveness probe for container orchestration.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-11-13T09:18:29.123Z",
  "version": "2.0.0",
  "uptime_seconds": 3600.5
}
```

### Readiness Check
```
GET /ready
```
Readiness probe indicating service can accept traffic.

**Response:**
```json
{
  "status": "ready",
  "checks": {
    "api": true,
    "orchestrator": true
  },
  "timestamp": "2025-11-13T09:18:29.123Z"
}
```

### Process Prompt
```
POST /v1/prompt
```
Process a prompt through ULTRATHINK orchestration.

**Request Body:**
```json
{
  "prompt": "Your prompt here",
  "verbose": false,
  "max_iterations": 20,
  "confidence_threshold": 99.0
}
```

**Response:**
```json
{
  "response": "AI-generated response",
  "confidence": 99.5,
  "success": true,
  "iterations": 3,
  "guardrails_passed": true,
  "context_tokens_used": 1250,
  "execution_time_ms": 2345.67
}
```

### System Status
```
GET /v1/status
```
Detailed system status and capabilities.

**Response:**
```json
{
  "status": "operational",
  "version": "2.0.0",
  "uptime_seconds": 3600.5,
  "features": {
    "guardrails": "8 layers",
    "context_window": "200K tokens",
    "confidence_target": "99%+",
    "orchestration": "Multi-agent"
  }
}
```

## Interactive Documentation

### Swagger UI
Visit `http://localhost:8000/docs` for interactive API documentation.

### ReDoc
Visit `http://localhost:8000/redoc` for alternative documentation format.

## Rate Limiting
No rate limiting currently implemented. Production deployment should add rate limiting.

## Error Handling

All endpoints return standard HTTP status codes:
- 200: Success
- 400: Bad Request
- 500: Internal Server Error

Error responses include:
```json
{
  "detail": "Error message",
  "error": "Detailed error information"
}
```
