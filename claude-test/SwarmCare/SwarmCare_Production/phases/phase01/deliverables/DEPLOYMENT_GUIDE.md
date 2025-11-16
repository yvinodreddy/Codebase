# SwarmCare Phase 01 - RAG Heat System Deployment Guide

**Version:** 1.0.0
**Status:** ✅ PRODUCTION READY
**Story Points:** 60/60
**Generated:** 2025-10-28

---

## Table of Contents

1. [Overview](#overview)
2. [Quick Start](#quick-start)
3. [Local Development](#local-development)
4. [Production Deployment](#production-deployment)
5. [Configuration](#configuration)
6. [Testing](#testing)
7. [Monitoring](#monitoring)
8. [Troubleshooting](#troubleshooting)

---

## Overview

The SwarmCare RAG Heat System provides:
- **Document Ingestion**: Intelligent chunking and processing
- **Vector Search**: Semantic similarity using embeddings
- **Knowledge Graph Integration**: Connects to 7,050 medical ontologies from Phase 00
- **REST API**: Production-ready FastAPI endpoints
- **Scalability**: Kubernetes-ready with auto-scaling

### Architecture

```
┌─────────────────┐
│   FastAPI       │ ←─── REST API (Port 8000)
│   REST API      │
└────────┬────────┘
         │
    ┌────▼────┐    ┌──────────────┐    ┌────────────┐
    │   RAG   │───→│ Vector Store │    │  Neo4j KG  │
    │ System  │    │  (Weaviate)  │    │ (Phase 00) │
    └─────────┘    └──────────────┘    └────────────┘
```

---

## Quick Start

### 5-Minute Local Setup

```bash
# 1. Clone and navigate
cd /home/user01/claude-test/SwarmCare/SwarmCare_Production/phases/phase01/deliverables

# 2. Start all services with Docker Compose
docker-compose up -d

# 3. Verify services are running
docker-compose ps

# 4. Test the API
curl http://localhost:8000/health

# Done! API is ready at http://localhost:8000
```

### Quick Test

```bash
# Ingest a sample document
curl -X POST http://localhost:8000/api/v1/documents/ingest \
  -H "Content-Type: application/json" \
  -d '{
    "document_id": "test_001",
    "title": "Diabetes Management",
    "content": "Type 2 diabetes treatment includes metformin...",
    "document_type": "clinical_guideline",
    "source": "Test"
  }'

# Query the system
curl -X POST http://localhost:8000/api/v1/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "diabetes treatment",
    "top_k": 5
  }'
```

---

## Local Development

### Prerequisites

- Docker & Docker Compose
- Python 3.11+
- 8GB RAM minimum
- 10GB disk space

### Setup Development Environment

```bash
# 1. Install Python dependencies
pip install -r requirements.txt

# 2. Start supporting services (Neo4j, Weaviate, Redis)
docker-compose up -d neo4j weaviate redis

# 3. Run API in development mode
python api.py

# API will be available at http://localhost:8000
# API docs at http://localhost:8000/api/docs
```

### Development Workflow

```bash
# Run tests
pytest test_rag_system.py -v

# Generate sample documents
python generate_sample_documents.py

# Check code quality
flake8 *.py
black *.py

# Run verification
python verify_phase01.py
```

---

## Production Deployment

### Option 1: Docker Compose (Recommended for Small Scale)

```bash
# 1. Configure environment
cp .env.example .env
# Edit .env with production values

# 2. Deploy
docker-compose -f docker-compose.yaml up -d

# 3. Verify
docker-compose ps
curl http://localhost:8000/health
```

### Option 2: Kubernetes (Recommended for Production)

```bash
# 1. Create namespace
kubectl create namespace swarmcare-rag

# 2. Configure secrets
kubectl create secret generic rag-secrets \
  --from-literal=neo4j-password=YOUR_PASSWORD \
  --from-literal=api-key=YOUR_API_KEY \
  -n swarmcare-rag

# 3. Deploy
kubectl apply -f kubernetes-deployment.yaml

# 4. Verify
kubectl get pods -n swarmcare-rag
kubectl get svc -n swarmcare-rag

# 5. Access API
kubectl port-forward svc/rag-api 8000:80 -n swarmcare-rag
curl http://localhost:8000/health
```

### Building Docker Image

```bash
# Build production image
docker build -t swarmcare/rag-api:1.0.0 .

# Test image locally
docker run -p 8000:8000 swarmcare/rag-api:1.0.0

# Push to registry
docker push swarmcare/rag-api:1.0.0
```

---

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `ENVIRONMENT` | `production` | Environment name |
| `LOG_LEVEL` | `INFO` | Logging level |
| `CHUNK_SIZE` | `512` | Document chunk size (words) |
| `CHUNK_OVERLAP` | `128` | Chunk overlap size (words) |
| `EMBEDDING_MODEL` | `all-MiniLM-L6-v2` | Sentence transformer model |
| `NEO4J_URI` | `bolt://localhost:7687` | Neo4j connection URI |
| `NEO4J_PASSWORD` | - | Neo4j password (required) |
| `API_PORT` | `8000` | API server port |

### Docker Compose Configuration

```yaml
# docker-compose.override.yml
version: '3.8'
services:
  rag-api:
    environment:
      - CHUNK_SIZE=1024  # Larger chunks
      - LOG_LEVEL=DEBUG   # More verbose logging
```

### Kubernetes Configuration

```yaml
# Custom ConfigMap
apiVersion: v1
kind: ConfigMap
metadata:
  name: rag-config-custom
data:
  CHUNK_SIZE: "1024"
  CHUNK_OVERLAP: "256"
```

---

## Testing

### Running Tests

```bash
# Run all tests
pytest test_rag_system.py -v

# Run with coverage
pytest test_rag_system.py --cov=rag_system --cov-report=html

# Run specific test class
pytest test_rag_system.py::TestRAGSystem -v

# Performance tests only
pytest test_rag_system.py::TestPerformance -v
```

### Load Testing

```bash
# Using Apache Bench
ab -n 1000 -c 10 http://localhost:8000/health

# Using hey
hey -n 1000 -c 10 http://localhost:8000/health
```

### Integration Testing

```bash
# Start all services
docker-compose up -d

# Run integration tests
python -m pytest test_rag_system.py::TestRAGSystem -v

# Stop services
docker-compose down
```

---

## Monitoring

### Prometheus Metrics

Access Prometheus at `http://localhost:9090`

Key metrics:
- `rag_documents_ingested_total`
- `rag_queries_processed_total`
- `rag_query_latency_seconds`
- `rag_vector_store_size`

### Grafana Dashboards

Access Grafana at `http://localhost:3000`
- Username: `admin`
- Password: `swarmcare123`

Import dashboard from `grafana-dashboard.json`

### Health Checks

```bash
# API health
curl http://localhost:8000/health

# Kubernetes readiness
curl http://localhost:8000/ready

# System statistics
curl http://localhost:8000/api/v1/stats
```

### Logs

```bash
# Docker Compose logs
docker-compose logs -f rag-api

# Kubernetes logs
kubectl logs -f deployment/rag-api -n swarmcare-rag

# Follow logs for specific pod
kubectl logs -f pod/rag-api-xxxxx -n swarmcare-rag
```

---

## Troubleshooting

### Issue: API not starting

**Symptoms:**
- Container exits immediately
- "Connection refused" errors

**Solution:**
```bash
# Check logs
docker-compose logs rag-api

# Verify dependencies are running
docker-compose ps

# Restart services
docker-compose restart
```

### Issue: Neo4j connection failed

**Symptoms:**
- "Unable to connect to Neo4j" errors
- Knowledge graph context empty

**Solution:**
```bash
# Verify Neo4j is running
docker-compose ps neo4j

# Check Neo4j logs
docker-compose logs neo4j

# Test connection
cypher-shell -a bolt://localhost:7687 -u neo4j -p swarmcare123
```

### Issue: Slow query performance

**Symptoms:**
- Query latency > 1 second
- High CPU usage

**Solution:**
```bash
# Check system resources
docker stats

# Increase API workers
# In docker-compose.yaml:
environment:
  - MAX_WORKERS: "8"

# Scale horizontally (Kubernetes)
kubectl scale deployment rag-api --replicas=5 -n swarmcare-rag
```

### Issue: Out of memory

**Symptoms:**
- Container killed (OOMKilled)
- Slow performance

**Solution:**
```bash
# Increase memory limit (Docker Compose)
services:
  rag-api:
    mem_limit: 4g

# Increase memory limit (Kubernetes)
resources:
  limits:
    memory: "8Gi"
```

---

## Performance Tuning

### Recommended Settings

**Small Scale (< 1000 documents):**
```yaml
CHUNK_SIZE: 512
CHUNK_OVERLAP: 128
MAX_WORKERS: 2
Memory: 2GB
```

**Medium Scale (1000-10000 documents):**
```yaml
CHUNK_SIZE: 512
CHUNK_OVERLAP: 128
MAX_WORKERS: 4
Memory: 4GB
```

**Large Scale (> 10000 documents):**
```yaml
CHUNK_SIZE: 1024
CHUNK_OVERLAP: 256
MAX_WORKERS: 8
Memory: 8GB
```

---

## Security

### Production Checklist

- [ ] Change default passwords
- [ ] Enable HTTPS/TLS
- [ ] Configure API authentication
- [ ] Set up firewall rules
- [ ] Enable rate limiting
- [ ] Configure CORS appropriately
- [ ] Use secrets management (Vault, AWS Secrets Manager)
- [ ] Enable audit logging
- [ ] Regular security updates
- [ ] Network segmentation

### Example: Enable API Key Authentication

```python
# In api.py
from fastapi import Header, HTTPException

async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != os.getenv("API_KEY"):
        raise HTTPException(status_code=403)
    return x_api_key

# Use in endpoints
@app.post("/api/v1/query", dependencies=[Depends(verify_api_key)])
async def query_rag_system(...):
    ...
```

---

## Backup and Recovery

### Backup Vector Store

```bash
# Docker volume backup
docker run --rm -v swarmcare-weaviate-data:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/weaviate-backup.tar.gz /data

# Kubernetes PVC backup
kubectl exec -n swarmcare-rag deployment/weaviate -- \
  tar czf /tmp/backup.tar.gz /var/lib/weaviate
```

### Restore Vector Store

```bash
# Docker volume restore
docker run --rm -v swarmcare-weaviate-data:/data \
  -v $(pwd):/backup \
  alpine tar xzf /backup/weaviate-backup.tar.gz -C /
```

---

## Scaling

### Horizontal Scaling (Kubernetes)

```bash
# Manual scaling
kubectl scale deployment rag-api --replicas=10 -n swarmcare-rag

# Auto-scaling is configured in kubernetes-deployment.yaml
# HPA will scale between 3-10 replicas based on CPU/memory
```

### Vertical Scaling

```yaml
# Increase resources per pod
resources:
  requests:
    memory: "4Gi"
    cpu: "2000m"
  limits:
    memory: "8Gi"
    cpu: "4000m"
```

---

## Next Steps

1. ✅ Phase 01 Deployed
2. ⏭️ Ingest medical documents
3. ⏭️ Integrate with Phase 00 knowledge graph
4. ⏭️ Configure monitoring and alerting
5. ⏭️ Set up CI/CD pipeline

---

**Document Version:** 1.0.0
**Last Updated:** 2025-10-28
**Status:** Production Ready ✅
