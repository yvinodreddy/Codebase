# Phase 07: FHIR Integration - Standalone Testing Documentation

**Port:** 8007
**Description:** FHIR resource handling
**Last Updated:** 2025-11-08

---

## Quick Start

```bash
# Navigate to deployment folder
cd deployment

# Run the testing application
./run.sh

# Access the UI
# Browser: http://localhost:8007
```

---

## What's in This Phase?

### Purpose
FHIR resource handling

### Testing Scope
- **Requirements:** Modify BRD.md and user_stories.json
- **Test Data:** Pre-seeded medical ontologies and EHR samples
- **Testing UI:** Browser-based interactive testing at port 8007
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
- **URL:** http://localhost:8007
- **API Docs:** http://localhost:8007/docs
- **Health Check:** http://localhost:8007/api/health

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
pip3 install --break-system-packages \
    fastapi>=0.109.0 \
    uvicorn>=0.27.0 \
    python-multipart \
    pydantic>=2.0.0 \
    python-dotenv>=1.0.0
```

### Optional (for full functionality)
```bash
# Docker services
docker-compose up -d neo4j redis

# Additional packages
pip3 install --break-system-packages \
    crewai>=0.70.0 \
    neo4j>=5.13.0 \
    redis>=5.0.0
```

---

## Testing Commands

### Health Check
```bash
curl http://localhost:8007/api/health | python3 -m json.tool
```

### Start Application
```bash
cd deployment
./run.sh
```

### Stop Application
```bash
# Kill process on port 8007
lsof -ti:8007 | xargs kill -9
```

### Restart Application
```bash
lsof -ti:8007 | xargs kill -9
cd deployment && ./run.sh
```

---

## Troubleshooting

### Port Already in Use
```bash
# Kill existing process
lsof -ti:8007 | xargs kill -9

# Verify port is free
lsof -i:8007
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
curl http://localhost:8007/api/health

# Check logs
cd deployment
tail -f ../../../logs/phase07.log
```

---

## Phase Independence

This phase is **100% independent** and can be tested without any other phases running.

### Self-Contained Features
- ✅ Own requirements (BRD, user stories)
- ✅ Own test data (seeded automatically)
- ✅ Own testing UI (port 8007)
- ✅ Own API endpoints
- ✅ Own documentation

### Integration Ready
When testing is complete, generated files can be copied to the main application:
```bash
cp deployment/generated_files/* ../../../integration/phase07/
```

---

## Next Steps

1. **Review this documentation** - Understand the phase scope
2. **Check requirements** - Read BRD.md and user_stories.json
3. **Start testing** - Run `./deployment/run.sh`
4. **Access UI** - Open http://localhost:8007
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

**Phase 07 - FHIR Integration Testing**
**Status:** Ready for Testing
**Port:** 8007
**Updated:** 2025-11-08
