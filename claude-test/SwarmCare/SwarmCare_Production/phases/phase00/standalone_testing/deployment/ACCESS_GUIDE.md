# How to Access Phase 00 Application - COMPLETE GUIDE

**Status:** ✅ ALL SERVICES RUNNING
**Date:** 2025-11-08

---

## 🌐 Access URLs - ALL WORKING

### 1. Main Dashboard (Port 8000) ✅
```
http://localhost:8000
```
**What you'll see:**
- Services Status (Neo4j & Redis)
- Testing section (Run tests, view results)
- Requirements (User stories, BRD)
- Metrics (Story points, completion)
- Generated Files (List files)
- Execution Log (Activity log)

### 2. API Documentation (Swagger UI) ✅
```
http://localhost:8000/docs
```
**What you can do:**
- Test all API endpoints interactively
- See request/response schemas
- Execute API calls directly from browser

### 3. Neo4j Browser ✅
```
http://localhost:7474
```
**Credentials:**
- Username: `neo4j`
- Password: `mJe@!ikwcoi4udlFXE$n!ENtv1iAw^F`

**What you can do:**
- Query graph database
- View medical ontologies
- Run Cypher queries
- Visualize data

### 4. Redis (NOT BROWSER ACCESSIBLE) ⚠️
```
Port: 6379
```
**Why you can't access it in browser:**
Redis is NOT a web service - it's a data store that uses a binary protocol (RESP).

**How to verify Redis is working:**
```bash
# Option 1: Check via API
curl http://localhost:8000/api/services/status

# Option 2: Use redis-cli (if installed)
redis-cli ping

# Option 3: Use docker
docker exec swarmcare-redis redis-cli ping
```

---

## 🔍 Testing All Endpoints

### Quick Test (All Endpoints)
```bash
cd /home/user01/claude-test/SwarmCare/SwarmCare_Production/phases/phase00/standalone_testing/deployment

# Test all endpoints
curl http://localhost:8000/api/health | python3 -m json.tool
curl http://localhost:8000/api/services/status | python3 -m json.tool
curl http://localhost:8000/api/metrics | python3 -m json.tool
curl http://localhost:8000/api/stories | python3 -m json.tool | head -50
```

### Available API Endpoints

#### Core Endpoints
```
✅ GET  /                        - Main dashboard (HTML)
✅ GET  /docs                    - API documentation (Swagger)
✅ GET  /api/health              - Health check
```

#### Services
```
✅ GET  /api/services/status     - Neo4j & Redis status
```

#### Testing
```
✅ POST /api/tests/run           - Run all tests
✅ GET  /api/tests/results       - Get test results
```

#### User Stories
```
✅ GET  /api/stories             - Get all user stories
✅ GET  /api/stories/{id}        - Get specific story
✅ POST /api/stories             - Create new story
✅ PUT  /api/stories/{id}        - Update story
✅ DELETE /api/stories/{id}      - Delete story
```

#### Metrics & Tracking
```
✅ GET  /api/metrics             - Phase metrics
✅ GET  /api/trackers/phase      - Phase-level tracker
✅ GET  /api/trackers/unified    - Unified tracker status
```

#### File Generation
```
✅ POST /api/generate            - Generate code files
✅ GET  /api/generated/files     - List generated files
```

#### Documentation
```
✅ POST /api/documentation/sync  - Sync documentation
```

#### Logs
```
✅ GET  /api/logs                - Get execution logs
✅ POST /api/logs/clear          - Clear logs
```

---

## 🐛 Troubleshooting

### "Can't access http://localhost:8000"

**Check if application is running:**
```bash
netstat -tlnp | grep 8000
# Should show: LISTEN on 0.0.0.0:8000
```

**If not running, start it:**
```bash
cd /home/user01/claude-test/SwarmCare/SwarmCare_Production/phases/phase00/standalone_testing/deployment
./START_APPLICATION.sh
```

### "Can't access Redis in browser"

This is NORMAL! Redis is not a web service.

**Verify Redis is working:**
```bash
# Via API
curl http://localhost:8000/api/services/status

# Should return:
# {"redis": {"status": "running", "url": "http://localhost:6379"}}
```

**Access Redis programmatically:**
```python
import redis
client = redis.Redis(host='localhost', port=6379, decode_responses=True)
client.ping()  # Returns True if working
```

### "Neo4j Browser not working"

**Check if Neo4j is running:**
```bash
docker ps | grep neo4j
```

**Restart if needed:**
```bash
docker restart swarmcare-neo4j
# Wait 10 seconds
curl http://localhost:7474
```

---

## 📊 Port Summary

| Service | Port | Browser Access | Purpose |
|---------|------|----------------|---------|
| FastAPI Dashboard | 8000 | ✅ YES | Main application & API |
| Neo4j Browser | 7474 | ✅ YES | Graph database UI |
| Neo4j Bolt | 7687 | ❌ NO | Database protocol (not HTTP) |
| Redis | 6379 | ❌ NO | Data store (not HTTP) |

**IMPORTANT:**
- Only ports 8000 and 7474 are accessible via web browser
- Ports 7687 (Neo4j Bolt) and 6379 (Redis) use binary protocols, not HTTP
- Access Neo4j Bolt and Redis programmatically via Python/APIs

---

## ✅ Verification Checklist

Run these commands to verify everything works:

```bash
# 1. Check all services are running
docker ps | grep swarmcare
# Should show: swarmcare-neo4j and swarmcare-redis

# 2. Check ports are listening
netstat -tlnp | grep -E '(8000|7474|6379)'
# Should show all three ports

# 3. Test FastAPI app
curl http://localhost:8000/api/health
# Should return: {"status":"healthy"...}

# 4. Test Neo4j browser
curl http://localhost:7474
# Should return HTML

# 5. Test Redis via API
curl http://localhost:8000/api/services/status
# Should return: {"redis":{"status":"running"}}

# 6. Run comprehensive tests
cd /home/user01/claude-test/SwarmCare/SwarmCare_Production/phases/phase00/standalone_testing/deployment
python3 comprehensive_test.py
# Should show: 100% pass rate
```

---

## 🎯 What Each Service Does

### Port 8000 - FastAPI Application
**THIS IS YOUR MAIN APPLICATION**
- Interactive dashboard with 6 sections
- RESTful API for all operations
- Real-time metrics and monitoring
- User story management
- Test execution
- File generation

### Port 7474 - Neo4j Browser
- Graph database visualization
- Cypher query interface
- Data exploration
- Medical ontology browsing

### Port 6379 - Redis
- In-memory data store
- Caching layer
- Session storage
- (Access via API, not browser)

---

## 🚀 Quick Start

```bash
# Start everything
cd /home/user01/claude-test/SwarmCare/SwarmCare_Production/phases/phase00/standalone_testing/deployment
./START_APPLICATION.sh

# Open in browser
# 1. Main Dashboard: http://localhost:8000
# 2. API Docs: http://localhost:8000/docs
# 3. Neo4j Browser: http://localhost:7474
```

---

**Last Updated:** 2025-11-08
**Status:** ✅ ALL SERVICES OPERATIONAL
