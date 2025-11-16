# Testing Guide - Phase 14: Patient Engagement

**Port:** 8014
**Description:** Patient portal and engagement
**Updated:** 2025-11-08

---

## Quick Test (30 seconds)

```bash
# 1. Navigate to deployment
cd standalone_testing/deployment

# 2. Start application
./run.sh

# 3. Wait for startup (5 seconds)
# 4. Open browser to http://localhost:8014
# 5. Verify UI loads
# 6. Check health endpoint
curl http://localhost:8014/api/health
```

**Expected Result:** Healthy status with phase information

---

## Comprehensive Testing

### Step 1: Environment Setup

#### Check Python Version
```bash
python3 --version
# Expected: Python 3.12 or higher
```

#### Install Dependencies
```bash
pip3 install --break-system-packages \
    fastapi>=0.109.0 \
    uvicorn>=0.27.0 \
    python-multipart \
    pydantic>=2.0.0 \
    python-dotenv>=1.0.0
```

#### Verify Installation
```bash
python3 -c "from fastapi import FastAPI; import uvicorn; print('✅ Dependencies OK')"
```

---

### Step 2: Start Docker Services (Optional)

```bash
# Navigate to project root
cd ../../..

# Start Neo4j and Redis
docker-compose up -d neo4j redis

# Verify services
docker ps | grep -E '(neo4j|redis)'
```

**Expected Output:**
```
swarmcare-neo4j    Up    7687/tcp, 7474/tcp
swarmcare-redis    Up    6379/tcp
```

---

### Step 3: Review Requirements

#### Business Requirements
```bash
cd standalone_testing/requirements
cat BRD.md
```

**What to Check:**
- Objectives clearly defined
- Success criteria listed
- Dependencies identified

#### User Stories
```bash
cat user_stories.json | python3 -m json.tool
```

**What to Check:**
- User roles defined
- Acceptance criteria clear
- Priority levels set

---

### Step 4: Seed Test Data

```bash
cd ../test_data/seeding_scripts

# Run master seeding script
python3 seed_all.py
```

**Expected Output:**
```
✅ Seeded SNOMED CT concepts
✅ Seeded ICD-10 codes
✅ Seeded Epic FHIR samples
✅ Seeded Cerner samples
✅ All test data loaded successfully
```

**Verification:**
```bash
# Check Neo4j data (if using)
cypher-shell -u neo4j -p <password> \
    "MATCH (n:TestData) RETURN count(n)"
```

---

### Step 5: Start Testing Application

```bash
cd ../../deployment

# Start application
./run.sh
```

**Expected Output:**
```
🚀 Starting Phase 14: Patient Engagement Testing
✅ Python 3.12+ detected
✅ FastAPI installed
✅ Docker services running
✅ Test data seeded
🌐 Starting server on port 8014...
✅ Server started successfully
🌐 Access UI at: http://localhost:8014
```

**Troubleshooting:**
```bash
# If port in use
lsof -ti:8014 | xargs kill -9

# If Docker not running
docker-compose up -d neo4j redis

# If dependencies missing
pip3 install --break-system-packages fastapi uvicorn
```

---

### Step 6: Test Health Endpoint

```bash
# Basic health check
curl http://localhost:8014/api/health

# Formatted output
curl http://localhost:8014/api/health | python3 -m json.tool
```

**Expected Response:**
```json
{
    "status": "healthy",
    "phase": "14",
    "phase_name": "Patient Engagement",
    "timestamp": "2025-11-08T...",
    "services": {
        "neo4j": {"status": "running"},
        "redis": {"status": "running"}
    }
}
```

---

### Step 7: Test UI in Browser

#### Access Points
1. **Main UI:** http://localhost:8014
2. **API Docs:** http://localhost:8014/docs
3. **OpenAPI:** http://localhost:8014/openapi.json

#### UI Testing Checklist
- [ ] Page loads without errors
- [ ] Phase name and description displayed
- [ ] Navigation menu functional
- [ ] Test controls responsive
- [ ] Results display properly

#### API Documentation Testing
- [ ] Swagger UI accessible
- [ ] All endpoints listed
- [ ] Try It Out feature works
- [ ] Schemas documented

---

### Step 8: Test API Endpoints

#### Requirements Endpoint
```bash
# Get requirements
curl http://localhost:8014/api/requirements | python3 -m json.tool

# Update requirements (example)
curl -X POST http://localhost:8014/api/requirements \
    -H "Content-Type: application/json" \
    -d '{"objective": "Updated objective"}'
```

#### Testing Endpoint
```bash
# Run tests
curl -X POST http://localhost:8014/api/test/run \
    -H "Content-Type: application/json" \
    -d '{"test_suite": "all"}'

# Get results
curl http://localhost:8014/api/test/results | python3 -m json.tool
```

#### Data Management
```bash
# Check data status
curl http://localhost:8014/api/data/status | python3 -m json.tool

# Reseed data
curl -X POST http://localhost:8014/api/data/seed
```

---

### Step 9: Feature Testing

#### Test Workflow
1. **Select Feature** in UI
2. **Configure Parameters** (if needed)
3. **Click "Test"** button
4. **Review Results** displayed
5. **Check Generated Files** in `generated_files/`

#### Generated Files
```bash
cd generated_files
ls -la

# Expected files:
# - controller.py
# - service.py
# - repository.py
# - tests.py
# - requirements.txt
```

#### Validate Generated Code
```python
# Test generated code
cd generated_files
python3 -m py_compile controller.py
python3 -m py_compile service.py

# Run tests
pytest tests.py -v
```

---

### Step 10: Performance Testing

#### Response Times
```bash
# Measure API response time
time curl http://localhost:8014/api/health

# Expected: < 100ms
```

#### Load Testing (Optional)
```bash
# Install hey (HTTP load generator)
# Test with 100 requests
hey -n 100 -c 10 http://localhost:8014/api/health
```

**Expected Metrics:**
- **Total time:** < 10 seconds
- **Average:** < 100ms per request
- **Success rate:** 100%

---

### Step 11: Integration Testing

#### Test Database Integration
```bash
# Verify Neo4j connection
curl http://localhost:8014/api/database/status

# Test query
curl -X POST http://localhost:8014/api/database/query \
    -H "Content-Type: application/json" \
    -d '{"cypher": "MATCH (n:TestData) RETURN count(n)"}'
```

#### Test Cache Integration
```bash
# Verify Redis connection
curl http://localhost:8014/api/cache/status

# Test cache operations
curl -X POST http://localhost:8014/api/cache/set \
    -H "Content-Type: application/json" \
    -d '{"key": "test", "value": "data"}'

curl http://localhost:8014/api/cache/get/test
```

---

### Step 12: Review Results

#### Check Logs
```bash
# Application logs
tail -f ../../../logs/phase14.log

# Look for:
# - No ERROR messages
# - Successful API calls
# - Proper data seeding
```

#### Validate Outputs
```bash
cd generated_files

# Check file contents
cat controller.py | head -20
cat service.py | head -20

# Verify no syntax errors
python3 -m py_compile *.py
```

#### Test Report
```bash
# Generate test report (if endpoint exists)
curl http://localhost:8014/api/test/report > test_report.json

# View report
cat test_report.json | python3 -m json.tool
```

---

## Testing Scenarios

### Scenario 1: Requirements Modification
1. Edit `requirements/BRD.md`
2. Update `requirements/user_stories.json`
3. Restart application
4. Verify changes reflected in UI
5. Test updated functionality

### Scenario 2: Custom Test Data
1. Create custom test data JSON
2. Add to `test_data/`
3. Update seeding script
4. Reseed database
5. Test with custom data

### Scenario 3: Generated Code Integration
1. Test phase independently
2. Review generated files
3. Copy to main application
4. Run integration tests
5. Deploy if successful

---

## Common Issues

### Port Already in Use
```bash
# Symptom
Error: Address already in use

# Fix
lsof -ti:8014 | xargs kill -9
./run.sh
```

### FastAPI Not Found
```bash
# Symptom
ModuleNotFoundError: No module named 'fastapi'

# Fix
pip3 install --break-system-packages fastapi uvicorn
```

### Database Connection Failed
```bash
# Symptom
Neo4j connection failed

# Fix
docker-compose up -d neo4j
# Wait 10 seconds for startup
curl http://localhost:7474
```

### UI Not Loading
```bash
# Symptom
Browser shows connection refused

# Fix
# Check if app is running
curl http://localhost:8014/api/health

# Check logs
tail -f ../../../logs/phase14.log

# Restart application
lsof -ti:8014 | xargs kill -9
./run.sh
```

---

## Test Checklist

### Pre-Testing
- [ ] Python 3.12+ installed
- [ ] Dependencies installed
- [ ] Docker services running (optional)
- [ ] Port 8014 available

### Basic Testing
- [ ] Application starts successfully
- [ ] Health endpoint returns healthy
- [ ] UI loads in browser
- [ ] API docs accessible

### Feature Testing
- [ ] All features testable via UI
- [ ] API endpoints responding
- [ ] Test data properly seeded
- [ ] Results displayed correctly

### Integration Testing
- [ ] Database connection working
- [ ] Cache connection working
- [ ] File generation successful
- [ ] Code validation passing

### Performance Testing
- [ ] Response times < 100ms
- [ ] Load test passing
- [ ] No memory leaks
- [ ] No error spikes

### Post-Testing
- [ ] Logs reviewed
- [ ] Generated files validated
- [ ] Test report generated
- [ ] Issues documented

---

## Success Criteria

✅ **Phase testing successful when:**
1. Application starts without errors
2. Health endpoint returns healthy status
3. UI loads and displays correctly
4. All API endpoints responding
5. Test data properly seeded
6. Features testable via browser
7. Generated files validated
8. Performance metrics met
9. No critical errors in logs
10. Integration tests passing

---

**Phase 14 - Patient Engagement**
**Testing Status:** Ready
**Port:** 8014
**Updated:** 2025-11-08
