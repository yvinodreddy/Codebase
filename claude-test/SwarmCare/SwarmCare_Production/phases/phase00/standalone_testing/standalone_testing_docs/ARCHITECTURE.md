# Technical Architecture - Phase 00: Foundation

**Port:** 8000
**Description:** Core infrastructure setup
**Updated:** 2025-11-08

---

## Phase Overview

### Purpose
Core infrastructure setup

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
FastAPI Application (Port 8000)
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
PHASE_NUMBER=00
PHASE_NAME="Foundation"
PORT=8000

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
# Access http://localhost:8000
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
cd phases/phase00/standalone_testing/deployment
./run.sh
```

### Production Deployment
```bash
# Use production-grade ASGI server
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app:app --bind 0.0.0.0:8000
```

---

## Monitoring

### Health Checks
```bash
# Basic health
curl http://localhost:8000/api/health

# Detailed status
curl http://localhost:8000/api/status
```

### Logs
```bash
# Application logs
tail -f ../../../logs/phase00.log

# Docker logs (if using)
docker logs swarmcare-phase00
```

---

## Integration

### With Main Application
```bash
# Copy generated files
cp deployment/generated_files/* ../../../integration/phase00/

# Import phase module
from phases.phase00.integration import Phase00Module
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
# Check what's using port 8000
lsof -i:8000

# Kill conflicting process
lsof -ti:8000 | xargs kill -9
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

**Phase 00 - Foundation**
**Architecture Version:** 1.0
**Updated:** 2025-11-08
