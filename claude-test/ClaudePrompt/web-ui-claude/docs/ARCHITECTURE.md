# ULTRATHINK Web UI - Architecture Documentation

## 🎯 Executive Summary

A production-ready web-based interface for Claude Code that enables:
- Folder-based project management
- Natural language query interface
- Automated code changes via Claude API
- OAuth2 Google authentication
- Real-time progress tracking
- Deployable to Netlify (frontend) + cloud backend

## 📋 System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    USER BROWSER                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  React Frontend (Netlify)                            │   │
│  │  - Authentication UI                                 │   │
│  │  - Folder Browser                                    │   │
│  │  - Query Interface                                   │   │
│  │  - Code Editor/Viewer                                │   │
│  │  - Real-time Progress                                │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                          │ HTTPS + WebSocket
                          ▼
┌─────────────────────────────────────────────────────────────┐
│            FastAPI Backend (Railway/Render/Fly.io)          │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Authentication Layer                                │   │
│  │  - OAuth2 Google                                     │   │
│  │  - JWT Token Management                              │   │
│  │  - Session Store (Redis)                             │   │
│  └─────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  File System Manager                                 │   │
│  │  - Sandboxed Access                                  │   │
│  │  - Path Validation                                   │   │
│  │  - File Operations                                   │   │
│  └─────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Claude Integration Layer                            │   │
│  │  - ULTRATHINK Bridge                                 │   │
│  │  - Context Management                                │   │
│  │  - Response Streaming                                │   │
│  └─────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  WebSocket Manager                                   │   │
│  │  - Real-time Updates                                 │   │
│  │  - Progress Tracking                                 │   │
│  │  - Error Handling                                    │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│              External Services                               │
│  - Google OAuth2 (Authentication)                           │
│  - Claude API (Anthropic)                                   │
│  - Redis (Session/Cache)                                    │
└─────────────────────────────────────────────────────────────┘
```

## 🏗️ Component Architecture

### 1. Frontend (React + TypeScript)

**Tech Stack:**
- React 18+ with TypeScript
- Vite (build tool)
- Tailwind CSS (styling)
- Monaco Editor (code editor)
- React Query (data fetching)
- Zustand (state management)
- Socket.io-client (WebSocket)

**Key Components:**
```
frontend/
├── src/
│   ├── components/
│   │   ├── Auth/
│   │   │   ├── LoginPage.tsx
│   │   │   ├── GoogleOAuthButton.tsx
│   │   │   └── AuthGuard.tsx
│   │   ├── FileBrowser/
│   │   │   ├── FolderSelector.tsx
│   │   │   ├── FileTree.tsx
│   │   │   └── FilePreview.tsx
│   │   ├── QueryInterface/
│   │   │   ├── QueryInput.tsx
│   │   │   ├── QueryHistory.tsx
│   │   │   └── SuggestedQueries.tsx
│   │   ├── CodeEditor/
│   │   │   ├── MonacoEditor.tsx
│   │   │   ├── DiffViewer.tsx
│   │   │   └── FileExplorer.tsx
│   │   └── Progress/
│   │       ├── RealTimeProgress.tsx
│   │       ├── TaskList.tsx
│   │       └── ProgressBar.tsx
│   ├── hooks/
│   │   ├── useAuth.ts
│   │   ├── useFileSystem.ts
│   │   ├── useClaudeQuery.ts
│   │   └── useWebSocket.ts
│   ├── services/
│   │   ├── api.ts
│   │   ├── websocket.ts
│   │   └── auth.ts
│   ├── store/
│   │   ├── authStore.ts
│   │   ├── projectStore.ts
│   │   └── queryStore.ts
│   ├── types/
│   │   └── index.ts
│   └── App.tsx
├── public/
├── index.html
├── package.json
├── tsconfig.json
├── vite.config.ts
└── tailwind.config.js
```

### 2. Backend (FastAPI + Python)

**Tech Stack:**
- FastAPI 0.104+
- Python 3.12+
- Anthropic Claude API
- OAuth2 with Google
- Redis (sessions)
- WebSocket (Socket.io)
- JWT tokens

**Key Modules:**
```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── oauth.py
│   │   ├── jwt_handler.py
│   │   └── dependencies.py
│   ├── filesystem/
│   │   ├── __init__.py
│   │   ├── manager.py
│   │   ├── validator.py
│   │   └── operations.py
│   ├── claude/
│   │   ├── __init__.py
│   │   ├── integration.py
│   │   ├── ultrathink_bridge.py
│   │   └── streaming.py
│   ├── websocket/
│   │   ├── __init__.py
│   │   ├── manager.py
│   │   └── handlers.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── project.py
│   │   └── query.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── files.py
│   │   ├── query.py
│   │   └── websocket.py
│   └── middleware/
│       ├── __init__.py
│       ├── cors.py
│       └── security.py
├── tests/
├── requirements.txt
├── Dockerfile
└── .env.example
```

## 🔐 Authentication Flow

```
1. User clicks "Login with Google"
   ↓
2. Redirect to Google OAuth consent screen
   ↓
3. User grants permission
   ↓
4. Google redirects back with authorization code
   ↓
5. Backend exchanges code for access token
   ↓
6. Backend creates JWT token with user info
   ↓
7. Frontend stores JWT in localStorage
   ↓
8. User prompted to enter Claude API key (encrypted storage)
   ↓
9. API key validated with Anthropic
   ↓
10. User authenticated and ready to use
```

## 🔒 Security Architecture

### Authentication
- OAuth2 Google authentication
- JWT tokens with 24h expiration
- Refresh token rotation
- Secure HTTP-only cookies option

### API Key Management
- Claude API keys encrypted at rest (AES-256)
- Keys stored per-user in secure backend
- Never exposed to frontend
- Key validation on first use

### File System Security
- Sandboxed file access
- Path traversal prevention
- Whitelist-based directory access
- Size limits on file operations
- Read-only mode option

### Network Security
- HTTPS only (enforced)
- CORS with whitelist
- Rate limiting (100 req/min per user)
- DDoS protection
- CSP headers

## 📡 Real-time Communication

### WebSocket Protocol
```javascript
// Connection
Client → Server: { type: "connect", token: "jwt_token" }
Server → Client: { type: "connected", sessionId: "xxx" }

// Query Execution
Client → Server: {
  type: "execute_query",
  folder: "/path/to/project",
  query: "Add authentication to the API"
}

Server → Client: {
  type: "progress",
  stage: "analyzing_codebase",
  progress: 25,
  message: "Analyzing 50 files..."
}

Server → Client: {
  type: "file_change",
  file: "/path/to/file.py",
  diff: "...",
  reason: "Added authentication middleware"
}

Server → Client: {
  type: "complete",
  filesChanged: 5,
  summary: "Authentication implemented successfully"
}
```

## 💾 Data Models

### User
```python
class User(BaseModel):
    id: str
    email: str
    name: str
    picture: str
    claude_api_key_encrypted: Optional[str]
    created_at: datetime
    last_login: datetime
```

### Project
```python
class Project(BaseModel):
    id: str
    user_id: str
    name: str
    path: str
    last_query: Optional[str]
    created_at: datetime
    updated_at: datetime
```

### Query
```python
class QueryRequest(BaseModel):
    folder_path: str
    query: str
    context_files: List[str] = []
    max_iterations: int = 20
    confidence_threshold: float = 99.0

class QueryResponse(BaseModel):
    query_id: str
    status: str  # "pending", "running", "complete", "error"
    files_changed: List[FileChange]
    summary: str
    execution_time_ms: float
```

## 🚀 Deployment Architecture

### Frontend (Netlify)
```
Deployment: Automatic from Git main branch
Build Command: npm run build
Publish Directory: dist/
Environment Variables:
  - VITE_API_URL=https://api.paragroupcli.com
  - VITE_WS_URL=wss://api.paragroupcli.com
Features:
  - CDN distribution
  - HTTPS automatic
  - Custom domain support
  - Rollback capability
```

### Backend (Railway/Render/Fly.io)
```
Deployment: Docker container
Port: 8000
Health Check: /health
Environment Variables:
  - GOOGLE_CLIENT_ID
  - GOOGLE_CLIENT_SECRET
  - CLAUDE_API_KEY_ENCRYPTION_KEY
  - REDIS_URL
  - JWT_SECRET
  - ALLOWED_ORIGINS
Resources:
  - CPU: 1 vCPU
  - Memory: 1GB RAM
  - Storage: 10GB
Scaling:
  - Auto-scale: 1-5 instances
  - Load balancer: Automatic
```

### Redis (Upstash/Redis Cloud)
```
Purpose:
  - Session storage
  - Rate limiting
  - Query cache
  - WebSocket connection tracking
Configuration:
  - Max Memory: 256MB
  - Eviction: LRU
  - Persistence: AOF
```

## 📊 Performance Requirements

| Metric | Target | Strategy |
|--------|--------|----------|
| Page Load | < 2s | Code splitting, lazy loading |
| API Response | < 500ms | Caching, optimized queries |
| WebSocket Latency | < 100ms | Persistent connections |
| File Upload | < 5s for 10MB | Chunked uploads |
| Concurrent Users | 100+ | Horizontal scaling |
| Uptime | 99.9% | Health checks, auto-restart |

## 🧪 Testing Strategy

### Frontend Testing
- Unit: Jest + React Testing Library (80% coverage)
- Integration: Cypress E2E tests
- Visual: Chromatic snapshots
- Performance: Lighthouse CI

### Backend Testing
- Unit: Pytest (90% coverage)
- Integration: FastAPI TestClient
- Load: Locust (100 concurrent users)
- Security: OWASP ZAP scan

## 📈 Monitoring & Observability

### Metrics (Prometheus)
- Request rate
- Error rate
- Response time (p50, p95, p99)
- Active WebSocket connections
- Claude API usage
- File operations

### Logging (ELK Stack)
- Structured JSON logs
- Request/response logging
- Error tracking
- User activity audit

### Tracing (OpenTelemetry)
- Request tracing
- Claude API calls
- File operations
- WebSocket messages

## 🔄 CI/CD Pipeline

```yaml
GitHub Actions Workflow:

Frontend:
  1. Install dependencies
  2. Run tests (Jest + Cypress)
  3. Build (Vite)
  4. Deploy to Netlify

Backend:
  1. Install dependencies
  2. Run tests (Pytest)
  3. Security scan (Bandit)
  4. Build Docker image
  5. Push to registry
  6. Deploy to Railway/Render

On every:
  - Push to main: Deploy to production
  - Pull request: Deploy to preview
  - Tag: Create release
```

## 🎯 Success Metrics

| KPI | Target | Measurement |
|-----|--------|-------------|
| User Satisfaction | 4.5/5 | User surveys |
| Query Success Rate | > 95% | Backend logs |
| Average Response Time | < 30s | Metrics dashboard |
| Daily Active Users | 50+ | Analytics |
| Zero Breaking Changes | 100% | Automated tests |
| Security Incidents | 0 | Security logs |

## 📚 API Documentation

Full OpenAPI/Swagger documentation available at:
- Development: http://localhost:8000/docs
- Production: https://api.paragroupcli.com/docs

## 🛠️ Development Setup

See separate documents:
- `SETUP.md` - Local development environment
- `DEPLOYMENT.md` - Production deployment guide
- `API.md` - API reference
- `CONTRIBUTING.md` - Contribution guidelines

## ✅ Production Readiness Checklist

- [ ] All tests passing (frontend + backend)
- [ ] Security audit completed
- [ ] Performance benchmarks met
- [ ] Documentation complete
- [ ] Monitoring configured
- [ ] Backup strategy defined
- [ ] Disaster recovery plan
- [ ] GDPR compliance review
- [ ] Load testing passed
- [ ] User acceptance testing
