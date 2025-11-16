#!/usr/bin/env python3
"""
Create phase-specific standalone_testing_docs/ for all 29 phases
Each phase gets its own documentation under standalone_testing/standalone_testing_docs/
"""

import os
import shutil
from pathlib import Path
from datetime import datetime

# Phase metadata
PHASES = [
    {"num": "00", "name": "Foundation", "port": 8000, "desc": "Core infrastructure setup"},
    {"num": "01", "name": "Data Ingestion", "port": 8001, "desc": "Medical data ingestion pipeline"},
    {"num": "02", "name": "NLP Processing", "port": 8002, "desc": "Natural language processing"},
    {"num": "03", "name": "Entity Recognition", "port": 8003, "desc": "Medical entity extraction"},
    {"num": "04", "name": "Relationship Mapping", "port": 8004, "desc": "Entity relationship mapping"},
    {"num": "05", "name": "Knowledge Graph", "port": 8005, "desc": "Knowledge graph construction"},
    {"num": "06", "name": "Ontology Integration", "port": 8006, "desc": "Medical ontology integration"},
    {"num": "07", "name": "FHIR Integration", "port": 8007, "desc": "FHIR resource handling"},
    {"num": "08", "name": "EHR Connectivity", "port": 8008, "desc": "EHR system integration"},
    {"num": "09", "name": "Clinical Workflows", "port": 8009, "desc": "Clinical workflow automation"},
    {"num": "10", "name": "Decision Support", "port": 8010, "desc": "Clinical decision support"},
    {"num": "11", "name": "Quality Metrics", "port": 8011, "desc": "Healthcare quality metrics"},
    {"num": "12", "name": "Risk Stratification", "port": 8012, "desc": "Patient risk assessment"},
    {"num": "13", "name": "Care Coordination", "port": 8013, "desc": "Care team coordination"},
    {"num": "14", "name": "Patient Engagement", "port": 8014, "desc": "Patient portal and engagement"},
    {"num": "15", "name": "Analytics", "port": 8015, "desc": "Healthcare analytics"},
    {"num": "16", "name": "Reporting", "port": 8016, "desc": "Clinical reporting"},
    {"num": "17", "name": "Compliance", "port": 8017, "desc": "HIPAA and regulatory compliance"},
    {"num": "18", "name": "Security", "port": 8018, "desc": "Security and PHI protection"},
    {"num": "19", "name": "Audit Trail", "port": 8019, "desc": "Audit logging and tracking"},
    {"num": "20", "name": "Monitoring", "port": 8020, "desc": "System health monitoring"},
    {"num": "21", "name": "Performance", "port": 8021, "desc": "Performance optimization"},
    {"num": "22", "name": "Scalability", "port": 8022, "desc": "System scalability"},
    {"num": "23", "name": "API Gateway", "port": 8023, "desc": "API management"},
    {"num": "24", "name": "Integration Hub", "port": 8024, "desc": "Integration orchestration"},
    {"num": "25", "name": "Data Migration", "port": 8025, "desc": "Data migration tools"},
    {"num": "26", "name": "Testing", "port": 8026, "desc": "Automated testing"},
    {"num": "27", "name": "Deployment", "port": 8027, "desc": "CI/CD deployment"},
    {"num": "28", "name": "Documentation", "port": 8028, "desc": "Documentation generation"},
]

def create_readme(phase):
    """Create phase-specific README.md"""
    return f"""# Phase {phase['num']}: {phase['name']} - Standalone Testing Documentation

**Port:** {phase['port']}
**Description:** {phase['desc']}
**Last Updated:** {datetime.now().strftime('%Y-%m-%d')}

---

## Quick Start

```bash
# Navigate to deployment folder
cd deployment

# Run the testing application
./run.sh

# Access the UI
# Browser: http://localhost:{phase['port']}
```

---

## What's in This Phase?

### Purpose
{phase['desc']}

### Testing Scope
- **Requirements:** Modify BRD.md and user_stories.json
- **Test Data:** Pre-seeded medical ontologies and EHR samples
- **Testing UI:** Browser-based interactive testing at port {phase['port']}
- **API Endpoints:** FastAPI application with Swagger docs

---

## Directory Structure

```
standalone_testing/
├── requirements/
│   ├── BRD.md                    # Business Requirements Document
│   ├── user_stories.json         # User stories for this phase
│   └── ai_agent_prompts.json     # CrewAI agent configurations
├── deployment/
│   ├── app.py                    # FastAPI testing application
│   ├── run.sh                    # One-click startup script
│   ├── frontend/                 # UI templates and static files
│   └── generated_files/          # Generated code from testing
├── test_data/
│   ├── seeding_scripts/          # Data seeding automation
│   ├── medical_ontologies/       # SNOMED CT, ICD-10, etc.
│   └── ehr_samples/              # Epic, Cerner, etc.
└── standalone_testing_docs/      # ← YOU ARE HERE
    ├── README.md                 # This file
    ├── QUICK_REFERENCE.md        # Quick command reference
    ├── ARCHITECTURE.md           # Technical architecture
    └── TESTING_GUIDE.md          # How to test this phase
```

---

## Documentation Files

| File | Purpose |
|------|---------|
| **README.md** | Overview and quick start (this file) |
| **QUICK_REFERENCE.md** | One-page command reference |
| **ARCHITECTURE.md** | Technical architecture details |
| **TESTING_GUIDE.md** | Step-by-step testing instructions |

---

## How to Use This Phase

### 1. Review Requirements
```bash
cd requirements
cat BRD.md
cat user_stories.json
```

### 2. Modify Requirements (Optional)
```bash
nano BRD.md
nano user_stories.json
```

### 3. Start Testing Application
```bash
cd deployment
./run.sh
```

### 4. Access Testing UI
- **URL:** http://localhost:{phase['port']}
- **API Docs:** http://localhost:{phase['port']}/docs
- **Health Check:** http://localhost:{phase['port']}/api/health

### 5. Test Features
- Use the browser UI to test all functionality
- Check API endpoints via Swagger docs
- Review generated code in `deployment/generated_files/`

### 6. Review Results
```bash
cd deployment/generated_files
ls -la
```

---

## Dependencies

### Required
```bash
# Core packages
pip3 install --break-system-packages \\
    fastapi>=0.109.0 \\
    uvicorn>=0.27.0 \\
    python-multipart \\
    pydantic>=2.0.0 \\
    python-dotenv>=1.0.0
```

### Optional (for full functionality)
```bash
# Docker services
docker-compose up -d neo4j redis

# Additional packages
pip3 install --break-system-packages \\
    crewai>=0.70.0 \\
    neo4j>=5.13.0 \\
    redis>=5.0.0
```

---

## Testing Commands

### Health Check
```bash
curl http://localhost:{phase['port']}/api/health | python3 -m json.tool
```

### Start Application
```bash
cd deployment
./run.sh
```

### Stop Application
```bash
# Kill process on port {phase['port']}
lsof -ti:{phase['port']} | xargs kill -9
```

### Restart Application
```bash
lsof -ti:{phase['port']} | xargs kill -9
cd deployment && ./run.sh
```

---

## Troubleshooting

### Port Already in Use
```bash
# Kill existing process
lsof -ti:{phase['port']} | xargs kill -9

# Verify port is free
lsof -i:{phase['port']}
```

### FastAPI Not Found
```bash
# Install dependencies
pip3 install --break-system-packages fastapi uvicorn
```

### Docker Services Not Running
```bash
# Start services
cd ../../..  # Navigate to project root
docker-compose up -d neo4j redis

# Check status
docker ps
```

### Cannot Access UI
```bash
# Verify application is running
curl http://localhost:{phase['port']}/api/health

# Check logs
cd deployment
tail -f ../../../logs/phase{phase['num']}.log
```

---

## Phase Independence

This phase is **100% independent** and can be tested without any other phases running.

### Self-Contained Features
- ✅ Own requirements (BRD, user stories)
- ✅ Own test data (seeded automatically)
- ✅ Own testing UI (port {phase['port']})
- ✅ Own API endpoints
- ✅ Own documentation

### Integration Ready
When testing is complete, generated files can be copied to the main application:
```bash
cp deployment/generated_files/* ../../../integration/phase{phase['num']}/
```

---

## Next Steps

1. **Review this documentation** - Understand the phase scope
2. **Check requirements** - Read BRD.md and user_stories.json
3. **Start testing** - Run `./deployment/run.sh`
4. **Access UI** - Open http://localhost:{phase['port']}
5. **Test features** - Use the browser interface
6. **Review results** - Check generated files

---

## Support

For issues or questions:
1. Check **TROUBLESHOOTING** section above
2. Review **TESTING_GUIDE.md** for detailed instructions
3. Check **ARCHITECTURE.md** for technical details
4. Verify **QUICK_REFERENCE.md** for quick commands

---

**Phase {phase['num']} - {phase['name']} Testing**
**Status:** Ready for Testing
**Port:** {phase['port']}
**Updated:** {datetime.now().strftime('%Y-%m-%d')}
"""

def create_quick_reference(phase):
    """Create phase-specific QUICK_REFERENCE.md"""
    return f"""# Quick Reference - Phase {phase['num']}: {phase['name']}

**Port:** {phase['port']} | **Updated:** {datetime.now().strftime('%Y-%m-%d')}

---

## Instant Start

```bash
cd deployment
./run.sh
# Access: http://localhost:{phase['port']}
```

---

## Essential Commands

### Start Application
```bash
cd deployment && ./run.sh
```

### Stop Application
```bash
lsof -ti:{phase['port']} | xargs kill -9
```

### Health Check
```bash
curl http://localhost:{phase['port']}/api/health | python3 -m json.tool
```

### View Logs
```bash
tail -f ../../../logs/phase{phase['num']}.log
```

---

## URLs

| Endpoint | URL |
|----------|-----|
| **UI** | http://localhost:{phase['port']} |
| **API Docs** | http://localhost:{phase['port']}/docs |
| **Health** | http://localhost:{phase['port']}/api/health |
| **OpenAPI** | http://localhost:{phase['port']}/openapi.json |

---

## File Locations

```
Requirements:   standalone_testing/requirements/
Deployment:     standalone_testing/deployment/
Test Data:      standalone_testing/test_data/
Documentation:  standalone_testing/standalone_testing_docs/
Generated:      standalone_testing/deployment/generated_files/
```

---

## Quick Troubleshooting

| Issue | Solution |
|-------|----------|
| Port in use | `lsof -ti:{phase['port']} \\| xargs kill -9` |
| FastAPI missing | `pip3 install --break-system-packages fastapi uvicorn` |
| Docker down | `docker-compose up -d neo4j redis` |
| Cannot access UI | Check `curl localhost:{phase['port']}/api/health` |

---

## Dependencies Install

```bash
pip3 install --break-system-packages \\
    fastapi>=0.109.0 \\
    uvicorn>=0.27.0 \\
    python-multipart \\
    pydantic>=2.0.0 \\
    python-dotenv>=1.0.0
```

---

## Testing Workflow

1. **Review Requirements** → `cd requirements && cat BRD.md`
2. **Start App** → `cd deployment && ./run.sh`
3. **Open Browser** → http://localhost:{phase['port']}
4. **Test Features** → Use UI to test functionality
5. **Check Results** → `cd generated_files && ls -la`

---

**Phase {phase['num']} - {phase['name']}**
**Ready for Testing**
"""

def create_architecture(phase):
    """Create phase-specific ARCHITECTURE.md"""
    return f"""# Technical Architecture - Phase {phase['num']}: {phase['name']}

**Port:** {phase['port']}
**Description:** {phase['desc']}
**Updated:** {datetime.now().strftime('%Y-%m-%d')}

---

## Phase Overview

### Purpose
{phase['desc']}

### Technical Stack
- **Framework:** FastAPI 0.109+
- **Server:** Uvicorn (ASGI)
- **Database:** Neo4j 5.13 (optional)
- **Cache:** Redis 7 (optional)
- **AI:** CrewAI with Azure OpenAI GPT-4o
- **Language:** Python 3.12+

---

## Architecture Components

### 1. Testing Application (app.py)
FastAPI application providing:
- Browser-based testing UI
- REST API endpoints
- Swagger/OpenAPI documentation
- Health monitoring
- Test data management

### 2. Requirements Management
- **BRD.md:** Business requirements document
- **user_stories.json:** User stories in JSON format
- **ai_agent_prompts.json:** CrewAI agent configurations

### 3. Test Data Seeding
Automated seeding of:
- **Medical Ontologies:** SNOMED CT, ICD-10, CPT, LOINC, RxNorm, etc.
- **EHR Samples:** Epic FHIR, Cerner, Allscripts, etc.
- **Test Scenarios:** Realistic clinical data

### 4. Deployment Automation
- **run.sh:** One-click startup script
- Environment validation
- Docker service orchestration
- Automatic browser launch

---

## Directory Structure

```
standalone_testing/
├── requirements/
│   ├── BRD.md                         # Business Requirements
│   ├── user_stories.json              # User Stories
│   └── ai_agent_prompts.json          # AI Agent Configs
│
├── deployment/
│   ├── app.py                         # FastAPI Application
│   ├── run.sh                         # Startup Script
│   ├── frontend/
│   │   ├── index.html                 # Main UI
│   │   ├── static/
│   │   │   ├── css/                   # Stylesheets
│   │   │   └── js/                    # JavaScript
│   │   └── templates/                 # Jinja2 templates
│   └── generated_files/               # Output from testing
│
├── test_data/
│   ├── seeding_scripts/
│   │   ├── seed_all.py                # Master seeding script
│   │   ├── seed_ontologies.py         # Ontology data
│   │   └── seed_ehr_samples.py        # EHR samples
│   ├── medical_ontologies/
│   │   ├── snomed_ct.json
│   │   ├── icd10.json
│   │   └── ...
│   └── ehr_samples/
│       ├── epic_fhir.json
│       ├── cerner.json
│       └── ...
│
└── standalone_testing_docs/           # Phase Documentation
    ├── README.md
    ├── QUICK_REFERENCE.md
    ├── ARCHITECTURE.md                # ← YOU ARE HERE
    └── TESTING_GUIDE.md
```

---

## API Endpoints

### Health & Status
```
GET  /api/health              # Health check
GET  /api/status              # Detailed status
```

### Requirements Management
```
GET  /api/requirements        # Get current requirements
POST /api/requirements        # Update requirements
```

### Testing
```
POST /api/test/run            # Run phase tests
GET  /api/test/results        # Get test results
```

### Data Management
```
POST /api/data/seed           # Seed test data
GET  /api/data/status         # Check data status
```

---

## Data Flow

```
User Browser
    ↓
FastAPI Application (Port {phase['port']})
    ↓
┌─────────────┬─────────────┬─────────────┐
│  Neo4j DB   │  Redis Cache │  Test Data  │
│  (optional) │  (optional)  │  (seeded)   │
└─────────────┴─────────────┴─────────────┘
    ↓
Generated Files & Results
```

---

## Configuration

### Environment Variables
```bash
# Application
PHASE_NUMBER={phase['num']}
PHASE_NAME="{phase['name']}"
PORT={phase['port']}

# Azure OpenAI (optional)
AZURE_OPENAI_API_KEY=<from-keyvault>
AZURE_OPENAI_ENDPOINT=<from-keyvault>

# Neo4j (optional)
NEO4J_URI=bolt://localhost:7687
NEO4J_PASSWORD=<from-env>

# Redis (optional)
REDIS_HOST=localhost
REDIS_PORT=6379
```

### Dependencies
```python
# requirements.txt
fastapi>=0.109.0
uvicorn>=0.27.0
python-multipart
pydantic>=2.0.0
python-dotenv>=1.0.0
crewai>=0.70.0          # Optional
neo4j>=5.13.0           # Optional
redis>=5.0.0            # Optional
```

---

## Security

### HIPAA Compliance
- PHI detection and masking
- Audit logging
- Encrypted data at rest
- Secure data transmission

### Authentication
- JWT-based authentication (optional)
- Azure AD integration (optional)
- API key validation

### Rate Limiting
- Per-minute limits
- Per-hour limits
- IP-based throttling

---

## Testing Strategy

### Unit Testing
```bash
pytest standalone_testing/tests/unit/
```

### Integration Testing
```bash
pytest standalone_testing/tests/integration/
```

### Browser Testing
```bash
# Start app and test via UI
cd deployment && ./run.sh
# Access http://localhost:{phase['port']}
```

---

## Performance

### Expected Metrics
- **Startup Time:** < 5 seconds
- **API Response:** < 100ms (p95)
- **UI Load Time:** < 2 seconds
- **Data Seeding:** < 30 seconds

### Optimization
- Redis caching for frequent queries
- Lazy loading of test data
- Connection pooling for Neo4j
- Static file caching

---

## Deployment

### Local Development
```bash
cd deployment
./run.sh
```

### Docker Deployment
```bash
# From project root
docker-compose up -d neo4j redis
cd phases/phase{phase['num']}/standalone_testing/deployment
./run.sh
```

### Production Deployment
```bash
# Use production-grade ASGI server
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app:app --bind 0.0.0.0:{phase['port']}
```

---

## Monitoring

### Health Checks
```bash
# Basic health
curl http://localhost:{phase['port']}/api/health

# Detailed status
curl http://localhost:{phase['port']}/api/status
```

### Logs
```bash
# Application logs
tail -f ../../../logs/phase{phase['num']}.log

# Docker logs (if using)
docker logs swarmcare-phase{phase['num']}
```

---

## Integration

### With Main Application
```bash
# Copy generated files
cp deployment/generated_files/* ../../../integration/phase{phase['num']}/

# Import phase module
from phases.phase{phase['num']}.integration import Phase{phase['num']}Module
```

### With Other Phases
Each phase is independent, but can share:
- Common database (Neo4j)
- Common cache (Redis)
- Common configurations (.env)

---

## Troubleshooting

### Port Conflicts
```bash
# Check what's using port {phase['port']}
lsof -i:{phase['port']}

# Kill conflicting process
lsof -ti:{phase['port']} | xargs kill -9
```

### Database Connection
```bash
# Test Neo4j connection
cypher-shell -u neo4j -p <password>

# Test Redis connection
redis-cli ping
```

### Import Errors
```python
# Verify Python path
import sys
print(sys.path)

# Add project root to path
sys.path.insert(0, '/path/to/SwarmCare_Production')
```

---

## Best Practices

### Development
1. Always use virtual environments (optional for system Python)
2. Install dependencies with `--break-system-packages` if needed
3. Test locally before integration
4. Keep documentation updated

### Testing
1. Start with health check
2. Verify all dependencies installed
3. Check Docker services if needed
4. Review logs for errors

### Integration
1. Test phase independently first
2. Review generated files
3. Validate requirements met
4. Copy to integration folder

---

**Phase {phase['num']} - {phase['name']}**
**Architecture Version:** 1.0
**Updated:** {datetime.now().strftime('%Y-%m-%d')}
"""

def create_testing_guide(phase):
    """Create phase-specific TESTING_GUIDE.md"""
    return f"""# Testing Guide - Phase {phase['num']}: {phase['name']}

**Port:** {phase['port']}
**Description:** {phase['desc']}
**Updated:** {datetime.now().strftime('%Y-%m-%d')}

---

## Quick Test (30 seconds)

```bash
# 1. Navigate to deployment
cd standalone_testing/deployment

# 2. Start application
./run.sh

# 3. Wait for startup (5 seconds)
# 4. Open browser to http://localhost:{phase['port']}
# 5. Verify UI loads
# 6. Check health endpoint
curl http://localhost:{phase['port']}/api/health
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
pip3 install --break-system-packages \\
    fastapi>=0.109.0 \\
    uvicorn>=0.27.0 \\
    python-multipart \\
    pydantic>=2.0.0 \\
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
cypher-shell -u neo4j -p <password> \\
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
🚀 Starting Phase {phase['num']}: {phase['name']} Testing
✅ Python 3.12+ detected
✅ FastAPI installed
✅ Docker services running
✅ Test data seeded
🌐 Starting server on port {phase['port']}...
✅ Server started successfully
🌐 Access UI at: http://localhost:{phase['port']}
```

**Troubleshooting:**
```bash
# If port in use
lsof -ti:{phase['port']} | xargs kill -9

# If Docker not running
docker-compose up -d neo4j redis

# If dependencies missing
pip3 install --break-system-packages fastapi uvicorn
```

---

### Step 6: Test Health Endpoint

```bash
# Basic health check
curl http://localhost:{phase['port']}/api/health

# Formatted output
curl http://localhost:{phase['port']}/api/health | python3 -m json.tool
```

**Expected Response:**
```json
{{
    "status": "healthy",
    "phase": "{phase['num']}",
    "phase_name": "{phase['name']}",
    "timestamp": "2025-11-08T...",
    "services": {{
        "neo4j": {{"status": "running"}},
        "redis": {{"status": "running"}}
    }}
}}
```

---

### Step 7: Test UI in Browser

#### Access Points
1. **Main UI:** http://localhost:{phase['port']}
2. **API Docs:** http://localhost:{phase['port']}/docs
3. **OpenAPI:** http://localhost:{phase['port']}/openapi.json

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
curl http://localhost:{phase['port']}/api/requirements | python3 -m json.tool

# Update requirements (example)
curl -X POST http://localhost:{phase['port']}/api/requirements \\
    -H "Content-Type: application/json" \\
    -d '{{"objective": "Updated objective"}}'
```

#### Testing Endpoint
```bash
# Run tests
curl -X POST http://localhost:{phase['port']}/api/test/run \\
    -H "Content-Type: application/json" \\
    -d '{{"test_suite": "all"}}'

# Get results
curl http://localhost:{phase['port']}/api/test/results | python3 -m json.tool
```

#### Data Management
```bash
# Check data status
curl http://localhost:{phase['port']}/api/data/status | python3 -m json.tool

# Reseed data
curl -X POST http://localhost:{phase['port']}/api/data/seed
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
time curl http://localhost:{phase['port']}/api/health

# Expected: < 100ms
```

#### Load Testing (Optional)
```bash
# Install hey (HTTP load generator)
# Test with 100 requests
hey -n 100 -c 10 http://localhost:{phase['port']}/api/health
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
curl http://localhost:{phase['port']}/api/database/status

# Test query
curl -X POST http://localhost:{phase['port']}/api/database/query \\
    -H "Content-Type: application/json" \\
    -d '{{"cypher": "MATCH (n:TestData) RETURN count(n)"}}'
```

#### Test Cache Integration
```bash
# Verify Redis connection
curl http://localhost:{phase['port']}/api/cache/status

# Test cache operations
curl -X POST http://localhost:{phase['port']}/api/cache/set \\
    -H "Content-Type: application/json" \\
    -d '{{"key": "test", "value": "data"}}'

curl http://localhost:{phase['port']}/api/cache/get/test
```

---

### Step 12: Review Results

#### Check Logs
```bash
# Application logs
tail -f ../../../logs/phase{phase['num']}.log

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
curl http://localhost:{phase['port']}/api/test/report > test_report.json

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
lsof -ti:{phase['port']} | xargs kill -9
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
curl http://localhost:{phase['port']}/api/health

# Check logs
tail -f ../../../logs/phase{phase['num']}.log

# Restart application
lsof -ti:{phase['port']} | xargs kill -9
./run.sh
```

---

## Test Checklist

### Pre-Testing
- [ ] Python 3.12+ installed
- [ ] Dependencies installed
- [ ] Docker services running (optional)
- [ ] Port {phase['port']} available

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

**Phase {phase['num']} - {phase['name']}**
**Testing Status:** Ready
**Port:** {phase['port']}
**Updated:** {datetime.now().strftime('%Y-%m-%d')}
"""

def main():
    print("=" * 70)
    print("Creating Phase-Specific Documentation for All 29 Phases")
    print("=" * 70)

    project_root = Path("/home/user01/claude-test/SwarmCare/SwarmCare_Production")
    phases_dir = project_root / "phases"

    created_count = 0
    failed_phases = []

    for phase in PHASES:
        phase_num = phase['num']
        phase_name = phase['name']

        print(f"\n[Phase {phase_num}] Creating documentation for {phase_name}...")

        # Path to phase's standalone_testing_docs/
        docs_dir = phases_dir / f"phase{phase_num}" / "standalone_testing" / "standalone_testing_docs"

        try:
            # Create directory
            docs_dir.mkdir(parents=True, exist_ok=True)

            # Create all documentation files
            (docs_dir / "README.md").write_text(create_readme(phase))
            (docs_dir / "QUICK_REFERENCE.md").write_text(create_quick_reference(phase))
            (docs_dir / "ARCHITECTURE.md").write_text(create_architecture(phase))
            (docs_dir / "TESTING_GUIDE.md").write_text(create_testing_guide(phase))

            print(f"  ✅ Created 4 documentation files")
            created_count += 1

        except Exception as e:
            print(f"  ❌ Failed: {e}")
            failed_phases.append((phase_num, str(e)))

    print("\n" + "=" * 70)
    print("Summary")
    print("=" * 70)
    print(f"✅ Successfully created documentation for {created_count}/29 phases")

    if failed_phases:
        print(f"❌ Failed phases: {len(failed_phases)}")
        for phase_num, error in failed_phases:
            print(f"   Phase {phase_num}: {error}")
    else:
        print("✅ All phases completed successfully!")

    print("\nDocumentation locations:")
    print("phases/phase{00-28}/standalone_testing/standalone_testing_docs/")
    print("  ├── README.md")
    print("  ├── QUICK_REFERENCE.md")
    print("  ├── ARCHITECTURE.md")
    print("  └── TESTING_GUIDE.md")

if __name__ == "__main__":
    main()
