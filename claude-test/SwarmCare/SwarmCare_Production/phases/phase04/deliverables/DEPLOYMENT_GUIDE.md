# Phase 04: Frontend Application - Deployment Guide

## Quick Navigation

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Local Development Setup](#local-development-setup)
- [Docker Deployment](#docker-deployment)
- [Kubernetes Deployment](#kubernetes-deployment)
- [Testing & Validation](#testing--validation)
- [Monitoring](#monitoring)
- [Troubleshooting](#troubleshooting)

---

## Overview

Phase 04 delivers three production-ready frontend applications:

1. **RAG UI** - Interactive knowledge base interface
2. **SWARMCARE Dashboard** - Real-time agent monitoring
3. **Podcast UI** - Medical podcast generation and playback

**Technology Stack:**
- Frontend: React 18 + TypeScript + Tailwind CSS
- Backend: FastAPI + Python 3.11
- Cache: Redis 7
- Database: PostgreSQL 15
- Deployment: Docker + Kubernetes

**Story Points:** 47 | **Priority:** P1

---

## Prerequisites

### Required Software

```bash
# Check versions
node --version          # v18.0.0 or higher
npm --version           # v9.0.0 or higher
python3 --version       # 3.11 or higher
docker --version        # 20.10.0 or higher
kubectl version         # 1.25.0 or higher (for K8s deployment)
```

### Required Packages

```bash
# Python packages
pip3 install fastapi uvicorn[standard] pydantic redis psycopg2-binary

# Node packages (in frontend directory)
npm install react react-dom axios typescript @types/react @types/react-dom
```

---

## Local Development Setup

### Option 1: Quick Start (Recommended)

```bash
# 1. Navigate to deliverables
cd /home/user01/claude-test/SwarmCare/SwarmCare_Production/phases/phase04/deliverables

# 2. Start all services with Docker Compose
docker-compose up -d

# 3. Wait for services to be healthy
docker-compose ps

# 4. Access applications
# Frontend:  http://localhost:3000
# Backend:   http://localhost:8000
# API Docs:  http://localhost:8000/api/docs
```

### Option 2: Manual Setup

#### Backend Setup

```bash
# 1. Install dependencies
cd /home/user01/claude-test/SwarmCare/SwarmCare_Production/phases/phase04/deliverables
pip3 install -r requirements.txt

# 2. Start Redis (in separate terminal)
docker run -d -p 6379:6379 redis:7-alpine

# 3. Start PostgreSQL (in separate terminal)
docker run -d -p 5432:5432 \
  -e POSTGRES_DB=swarmcare_frontend \
  -e POSTGRES_USER=swarmcare \
  -e POSTGRES_PASSWORD=dev_password \
  postgres:15-alpine

# 4. Start backend
python3 backend_api.py
```

#### Frontend Setup

```bash
# 1. Create React app (if not exists)
npx create-react-app frontend --template typescript
cd frontend

# 2. Install dependencies
npm install axios react-query tailwindcss

# 3. Copy frontend components
cp ../frontend_*.tsx src/

# 4. Start development server
npm start
```

---

## Docker Deployment

### Build Images

```bash
# Navigate to deliverables directory
cd /home/user01/claude-test/SwarmCare/SwarmCare_Production/phases/phase04/deliverables

# Build frontend image
docker build -f Dockerfile.frontend -t swarmcare/frontend:latest .

# Build backend image
docker build -f Dockerfile.backend -t swarmcare/backend-api:latest .
```

### Run with Docker Compose

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Check service health
docker-compose ps

# Stop all services
docker-compose down
```

### Individual Container Management

```bash
# Frontend
docker run -d -p 3000:80 \
  -e REACT_APP_API_URL=http://localhost:8000 \
  swarmcare/frontend:latest

# Backend
docker run -d -p 8000:8000 \
  -e REDIS_HOST=redis \
  -e POSTGRES_HOST=postgres \
  swarmcare/backend-api:latest

# Redis
docker run -d -p 6379:6379 redis:7-alpine

# PostgreSQL
docker run -d -p 5432:5432 \
  -e POSTGRES_DB=swarmcare_frontend \
  -e POSTGRES_USER=swarmcare \
  -e POSTGRES_PASSWORD=secure_password \
  postgres:15-alpine
```

---

## Kubernetes Deployment

### Prerequisites

```bash
# Verify K8s cluster is running
kubectl cluster-info

# Verify kubectl access
kubectl get nodes
```

### Deploy to Kubernetes

```bash
# 1. Navigate to deliverables
cd /home/user01/claude-test/SwarmCare/SwarmCare_Production/phases/phase04/deliverables

# 2. Apply manifests
kubectl apply -f kubernetes-deployment.yaml

# 3. Wait for pods to be ready
kubectl wait --for=condition=ready pod -l app=frontend -n swarmcare-frontend --timeout=300s
kubectl wait --for=condition=ready pod -l app=backend -n swarmcare-frontend --timeout=300s

# 4. Check deployment status
kubectl get all -n swarmcare-frontend
```

### Access Services

```bash
# Get frontend service external IP/port
kubectl get service frontend-service -n swarmcare-frontend

# Port forward for local access
kubectl port-forward -n swarmcare-frontend service/frontend-service 8080:80

# Access application
# http://localhost:8080
```

### Update Deployment

```bash
# Update images
kubectl set image deployment/frontend-deployment frontend=swarmcare/frontend:v2 -n swarmcare-frontend
kubectl set image deployment/backend-deployment backend=swarmcare/backend-api:v2 -n swarmcare-frontend

# Rollout status
kubectl rollout status deployment/frontend-deployment -n swarmcare-frontend

# Rollback if needed
kubectl rollout undo deployment/frontend-deployment -n swarmcare-frontend
```

### Scale Deployments

```bash
# Scale frontend
kubectl scale deployment frontend-deployment --replicas=5 -n swarmcare-frontend

# Scale backend
kubectl scale deployment backend-deployment --replicas=10 -n swarmcare-frontend

# Verify scaling
kubectl get pods -n swarmcare-frontend
```

---

## Testing & Validation

### Run Verification Script

```bash
cd /home/user01/claude-test/SwarmCare/SwarmCare_Production/phases/phase04/deliverables
python3 verify_phase04.py
```

**Expected Output:**
```
✅ PHASE 04 VERIFICATION: PASSED
Success Rate: 100.0%
```

### Run Test Suite

```bash
# Run comprehensive tests
python3 test_comprehensive.py

# Expected output
# ✅ ALL TESTS PASSED - PHASE 04 VALIDATED
```

### Manual Testing

#### Test RAG UI

```bash
# Test RAG query endpoint
curl -X POST http://localhost:8000/api/rag/query \
  -H "Authorization: Bearer test-token" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is diabetes?", "context_size": 5, "stream": false}'
```

#### Test Dashboard API

```bash
# Get agent status
curl http://localhost:8000/api/dashboard/agents \
  -H "Authorization: Bearer test-token"

# Get metrics
curl http://localhost:8000/api/dashboard/metrics \
  -H "Authorization: Bearer test-token"
```

#### Test Podcast API

```bash
# Generate podcast
curl -X POST http://localhost:8000/api/podcast/generate \
  -H "Authorization: Bearer test-token" \
  -H "Content-Type: application/json" \
  -d '{"ehr_data": "Patient data...", "voice": "neural", "duration_minutes": 10}'
```

---

## Monitoring

### Health Checks

```bash
# Backend health
curl http://localhost:8000/api/health

# Frontend health (Docker)
docker exec swarmcare-frontend wget -q -O- http://localhost:80/

# Kubernetes health
kubectl get pods -n swarmcare-frontend
```

### View Logs

**Docker:**
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend

# Last 100 lines
docker-compose logs --tail=100 backend
```

**Kubernetes:**
```bash
# All pods
kubectl logs -f -l app=backend -n swarmcare-frontend

# Specific pod
kubectl logs -f <pod-name> -n swarmcare-frontend

# Previous pod logs
kubectl logs --previous <pod-name> -n swarmcare-frontend
```

### Metrics

**Prometheus Metrics (if enabled):**
```bash
# Scrape backend metrics
curl http://localhost:8000/metrics
```

**Resource Usage:**
```bash
# Docker
docker stats

# Kubernetes
kubectl top pods -n swarmcare-frontend
kubectl top nodes
```

---

## Troubleshooting

### Common Issues

#### Issue: Backend fails to start

**Symptoms:**
```
Error: Cannot connect to Redis
Error: Cannot connect to PostgreSQL
```

**Solution:**
```bash
# Check Redis connection
docker exec swarmcare-redis redis-cli ping
# Expected: PONG

# Check PostgreSQL connection
docker exec swarmcare-postgres pg_isready -U swarmcare
# Expected: accepting connections

# Restart services
docker-compose restart backend
```

#### Issue: Frontend shows "API connection failed"

**Symptoms:**
- Frontend loads but shows connection errors
- Network errors in browser console

**Solution:**
```bash
# Check backend is running
curl http://localhost:8000/api/health

# Check CORS configuration
# Ensure frontend URL is in backend CORS allowed_origins

# Check environment variables
docker exec swarmcare-frontend env | grep REACT_APP
```

#### Issue: Kubernetes pods in CrashLoopBackOff

**Symptoms:**
```bash
kubectl get pods -n swarmcare-frontend
# Shows: CrashLoopBackOff
```

**Solution:**
```bash
# Check pod logs
kubectl logs <pod-name> -n swarmcare-frontend

# Describe pod for events
kubectl describe pod <pod-name> -n swarmcare-frontend

# Check secrets and configmaps
kubectl get secrets -n swarmcare-frontend
kubectl get configmaps -n swarmcare-frontend

# Delete and recreate pod
kubectl delete pod <pod-name> -n swarmcare-frontend
```

#### Issue: High memory usage

**Solution:**
```bash
# Check resource usage
docker stats
kubectl top pods -n swarmcare-frontend

# Increase resource limits in deployment
# Edit kubernetes-deployment.yaml:
# resources:
#   limits:
#     memory: "2Gi"  # Increase from 1Gi

# Apply changes
kubectl apply -f kubernetes-deployment.yaml
```

### Debug Mode

**Backend Debug Mode:**
```bash
# Enable debug logging
docker-compose up -d backend
docker-compose exec backend bash
export LOG_LEVEL=debug
python3 backend_api.py
```

**Frontend Debug Mode:**
```bash
# Check React DevTools in browser
# Open browser console
# Set localStorage debug flag
localStorage.setItem('debug', 'true')
```

### Get Support

**Check logs:**
```bash
# Save logs for support
docker-compose logs > phase04-logs.txt
kubectl logs -n swarmcare-frontend -l app=backend > phase04-k8s-logs.txt
```

**Verify deliverables:**
```bash
python3 verify_phase04.py
```

**Run tests:**
```bash
python3 test_comprehensive.py
```

---

## Security Considerations

### Production Secrets

**DO NOT use default secrets in production!**

```bash
# Generate secure secrets
openssl rand -base64 32  # For JWT_SECRET
openssl rand -base64 32  # For POSTGRES_PASSWORD
openssl rand -base64 32  # For API_KEY
```

### Update Kubernetes Secrets

```bash
# Create production secrets
kubectl create secret generic api-secrets \
  --from-literal=JWT_SECRET=$(openssl rand -base64 32) \
  --from-literal=POSTGRES_PASSWORD=$(openssl rand -base64 32) \
  --from-literal=API_KEY=$(openssl rand -base64 32) \
  -n swarmcare-frontend
```

### HTTPS/TLS

**Enable TLS in production:**
1. Obtain SSL certificate (Let's Encrypt recommended)
2. Configure Ingress with TLS
3. Update `kubernetes-deployment.yaml` Ingress section
4. Force HTTPS redirect

---

## Performance Tuning

### Backend Performance

```bash
# Increase workers (Dockerfile.backend)
CMD ["uvicorn", "backend_api:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "8"]

# Enable caching
# Configure Redis with larger memory
docker run -d -p 6379:6379 redis:7-alpine redis-server --maxmemory 2gb
```

### Frontend Performance

```bash
# Enable Gzip compression (nginx.conf)
gzip on;
gzip_types text/plain text/css application/json application/javascript;

# Enable caching
location ~* \.(js|css|png|jpg|jpeg|gif|ico)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

### Database Performance

```bash
# Increase PostgreSQL connections
docker run -d postgres:15-alpine \
  -c max_connections=200 \
  -c shared_buffers=256MB
```

---

## Backup & Recovery

### Backup Data

```bash
# Backup PostgreSQL
docker exec swarmcare-postgres pg_dump -U swarmcare swarmcare_frontend > backup.sql

# Backup Redis
docker exec swarmcare-redis redis-cli SAVE
docker cp swarmcare-redis:/data/dump.rdb ./redis-backup.rdb
```

### Restore Data

```bash
# Restore PostgreSQL
docker exec -i swarmcare-postgres psql -U swarmcare swarmcare_frontend < backup.sql

# Restore Redis
docker cp ./redis-backup.rdb swarmcare-redis:/data/dump.rdb
docker-compose restart redis
```

---

## Success Checklist

- [ ] All services running (frontend, backend, redis, postgres)
- [ ] Health checks passing
- [ ] RAG UI accessible and functional
- [ ] Dashboard showing agent status
- [ ] Podcast UI generating episodes
- [ ] Tests passing (verify_phase04.py)
- [ ] No errors in logs
- [ ] Performance metrics acceptable
- [ ] Monitoring configured
- [ ] Backups configured

---

**Status**: ✅ Production Ready
**Last Updated**: 2025-10-28
**Version**: 1.0.0
**Contact**: SwarmCare Engineering
