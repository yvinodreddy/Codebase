# Business Requirements Document - Phase 0: Foundation

**Version:** 1.0
**Date:** 2025-11-08
**Story Points:** 40
**Priority:** P0 (Critical)
**Status:** Complete

---

## Executive Summary

Phase 0 establishes the foundational infrastructure for the SwarmCare Ultimate platform. This includes Neo4j graph database setup, medical ontology loading, Docker containerization, and core system configuration.

### Key Deliverables
1. Neo4j 5.13 graph database with 13 medical ontologies
2. Docker Compose infrastructure
3. Redis caching layer
4. System health monitoring
5. Development environment setup

---

## Business Objectives

1. **Establish Data Foundation**: Set up graph database for 13 medical ontologies (SNOMED CT, LOINC, ICD-10, CPT, RxNorm, etc.)
2. **Enable Distributed Deployment**: Containerize all services with Docker
3. **Performance Optimization**: Implement caching layer with Redis
4. **System Reliability**: Add health checks and monitoring
5. **Developer Experience**: Create reproducible development environment

---

## Functional Requirements

### FR-001: Neo4j Graph Database Setup
**Priority:** P0
**Description:** Deploy Neo4j 5.13 with optimized configuration for medical data
**Acceptance Criteria:**
- Neo4j accessible on ports 7474 (HTTP) and 7687 (Bolt)
- 2GB heap memory allocated
- APOC plugin enabled
- Health check endpoint responding

### FR-002: Medical Ontology Loading
**Priority:** P0
**Description:** Load 13 medical ontologies into Neo4j
**Acceptance Criteria:**
- SNOMED CT concepts loaded (100+ sample concepts)
- ICD-10 codes loaded (100+ sample codes)
- CPT codes loaded (50+ sample codes)
- LOINC codes loaded (50+ sample codes)
- RxNorm medications loaded (50+ sample drugs)
- Graph relationships established
- Query performance < 100ms for basic lookups

**Ontologies to Load:**
1. SNOMED CT (clinical terminology)
2. LOINC (lab observations)
3. ICD-10 (diagnosis codes)
4. CPT (procedure codes)
5. RxNorm (medications)
6. HCPCS (healthcare procedures)
7. NDC (national drug codes)
8. UMLS (unified medical language)
9. MeSH (medical subject headings)
10. HPO (human phenotype ontology)
11. OMIM (genetic disorders)
12. RadLex (radiology lexicon)
13. FMA (foundational model of anatomy)

### FR-003: Docker Infrastructure
**Priority:** P0
**Description:** Containerize all services for consistent deployment
**Acceptance Criteria:**
- Docker Compose configuration created
- Neo4j container with persistent volumes
- Redis container for caching
- Network isolation configured
- One-command startup (`docker-compose up`)

### FR-004: Redis Caching Layer
**Priority:** P1
**Description:** Add Redis for caching frequently accessed data
**Acceptance Criteria:**
- Redis 7-alpine deployed
- Accessible on port 6379
- Health check working
- Connection pooling configured

### FR-005: Health Monitoring
**Priority:** P1
**Description:** Implement health checks for all services
**Acceptance Criteria:**
- Neo4j health endpoint responds in <5s
- Redis ping responds in <1s
- Docker Compose health checks configured
- Restart policies defined

---

## Non-Functional Requirements

### NFR-001: Performance
- Neo4j query response time < 100ms (95th percentile)
- Database startup time < 30s
- Docker Compose startup < 60s

### NFR-002: Reliability
- Service uptime > 99.9%
- Automatic restart on failure
- Data persistence across restarts

### NFR-003: Scalability
- Support for 1M+ ontology concepts
- Concurrent connections: 50+
- Horizontal scaling ready

### NFR-004: Security
- No hardcoded passwords (use environment variables)
- Network isolation between services
- TLS support for production

---

## User Stories

### US-001: Database Setup
**As a** developer
**I want** to set up Neo4j with one command
**So that** I can start loading medical ontologies immediately

**Story Points:** 5
**Acceptance Criteria:**
- Docker Compose starts Neo4j
- Database accessible via browser (http://localhost:7474)
- Initial schema loaded
- Health check passes

### US-002: Ontology Loading
**As a** data engineer
**I want** to load 13 medical ontologies into Neo4j
**So that** the system has comprehensive medical knowledge

**Story Points:** 13
**Acceptance Criteria:**
- All 13 ontologies loaded successfully
- Relationships between ontologies established
- Query interface available
- Sample queries work (<100ms)

### US-003: Cache Implementation
**As a** backend developer
**I want** Redis caching available
**So that** I can optimize API performance

**Story Points:** 3
**Acceptance Criteria:**
- Redis accessible from Python
- Connection pooling configured
- Health check working

### US-004: Development Environment
**As a** new developer
**I want** a one-command setup
**So that** I can start contributing immediately

**Story Points:** 5
**Acceptance Criteria:**
- `./run.sh` starts entire environment
- All services healthy
- Sample data loaded
- Documentation clear

### US-005: Health Monitoring
**As a** DevOps engineer
**I want** health checks for all services
**So that** I can monitor system status

**Story Points:** 3
**Acceptance Criteria:**
- Health endpoints for all services
- Docker Compose health checks
- Restart policies defined

### US-006: Data Seeding
**As a** QA engineer
**I want** sample test data pre-loaded
**So that** I can test the system without manual setup

**Story Points:** 8
**Acceptance Criteria:**
- 100+ SNOMED concepts
- 100+ ICD-10 codes
- 50+ CPT codes
- 50+ medications
- Realistic patient scenarios

---

## Technical Architecture

### Components
```
┌─────────────────────────────────────┐
│         Docker Compose              │
│                                     │
│  ┌──────────┐      ┌──────────┐   │
│  │  Neo4j   │◄────►│  Redis   │   │
│  │  5.13    │      │  7-alpine│   │
│  └──────────┘      └──────────┘   │
│       ▲                            │
│       │                            │
│  ┌────┴──────────┐                │
│  │ Ontology Data │                │
│  │ 13 Sources    │                │
│  └───────────────┘                │
└─────────────────────────────────────┘
```

### Data Flow
1. Docker Compose starts Neo4j and Redis
2. Health checks verify services are ready
3. Cypher script loads ontologies
4. Relationships are established
5. System is ready for Phase 1 (RAG)

---

## Dependencies

### External Dependencies
- Docker 20.10+
- Docker Compose 2.0+
- 4GB RAM available
- 10GB disk space

### Phase Dependencies
- None (this is Phase 0 - foundation for all others)

### Dependent Phases
- Phase 1 (RAG Heat System) - requires Neo4j
- Phase 2 (SwarmCare Agents) - requires Neo4j
- All subsequent phases depend on this foundation

---

## Success Metrics

| Metric | Target | Actual |
|--------|--------|--------|
| Neo4j Startup Time | <30s | TBD |
| Ontology Load Time | <5min | TBD |
| Query Response Time | <100ms | TBD |
| Service Uptime | >99.9% | TBD |
| Health Check Response | <5s | TBD |
| Test Coverage | >80% | TBD |

---

## Risk Assessment

### High Risk
- **Ontology data size**: May exceed memory limits
  - *Mitigation*: Increase heap size, load incrementally

### Medium Risk
- **Docker resource constraints**: May fail on low-spec machines
  - *Mitigation*: Document minimum requirements, optimize container configs

### Low Risk
- **Network port conflicts**: Ports 7474, 7687, 6379 may be in use
  - *Mitigation*: Configurable ports, conflict detection script

---

## Testing Strategy

### Unit Tests
- Neo4j connection test
- Redis connection test
- Health check endpoint test

### Integration Tests
- Docker Compose startup test
- Ontology loading test
- Cross-ontology relationship queries

### Performance Tests
- Query latency benchmarks
- Concurrent connection test
- Data volume stress test

---

## Implementation Log

### What Was Implemented
1. ✅ Docker Compose configuration
2. ✅ Neo4j 5.13 deployment
3. ✅ Redis 7-alpine deployment
4. ✅ Cypher script for 13 ontologies
5. ✅ Health check configuration
6. ✅ Network isolation
7. ✅ Volume persistence
8. ✅ Environment variable configuration

### What Prompts Were Used
1. "Create Docker Compose with Neo4j and Redis"
2. "Generate Cypher script for medical ontologies"
3. "Implement health checks for all services"
4. "Create one-click deployment script"

### Enhancements Available
1. Add Prometheus metrics
2. Add Grafana dashboards
3. Implement backup automation
4. Add schema versioning
5. Create data import CLI tool

---

## How to Modify Requirements

### Adding New Stories
```bash
python requirements/requirements_editor.py add-story \
  --title "New feature" \
  --description "Feature description" \
  --story-points 5 \
  --priority P1
```

### Modifying Existing Stories
```bash
python requirements/requirements_editor.py modify-story \
  --id US-001 \
  --update "acceptance_criteria" \
  --value "New criteria"
```

### Regenerating Phase
```bash
python requirements/requirements_editor.py regenerate \
  --with-new-requirements
```

---

## References

- Neo4j Documentation: https://neo4j.com/docs/
- Docker Documentation: https://docs.docker.com/
- SNOMED CT: https://www.snomed.org/
- ICD-10: https://www.who.int/classifications/icd/
- LOINC: https://loinc.org/

---

**Phase Owner:** SwarmCare Development Team
**Last Updated:** 2025-11-08
**Review Cycle:** Quarterly
