# Phase 02: SWARMCARE Agents - Deployment Guide

**Version:** 2.1
**Last Updated:** 2025-10-28
**Status:** Production-Ready ✅

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Deployment Options](#deployment-options)
4. [Kubernetes Deployment](#kubernetes-deployment)
5. [Docker Compose Deployment](#docker-compose-deployment)
6. [Configuration](#configuration)
7. [Monitoring & Observability](#monitoring--observability)
8. [Security Considerations](#security-considerations)
9. [Troubleshooting](#troubleshooting)
10. [Post-Deployment Verification](#post-deployment-verification)

---

## Overview

This guide provides comprehensive instructions for deploying all 6 SWARMCARE agents to production:

- **Knowledge Agent** - Medical knowledge retrieval
- **Case Agent** - Patient case analysis
- **Conversation Agent** - Natural language interactions
- **Compliance Agent** - HIPAA compliance monitoring
- **Podcast Agent** - Medical podcast generation
- **QA Agent** - Quality assurance

---

## Prerequisites

### System Requirements

**Minimum Requirements:**
- Kubernetes 1.24+ OR Docker 20.10+
- 16 CPU cores
- 32GB RAM
- 100GB SSD storage

**Recommended for Production:**
- Kubernetes 1.27+
- 32 CPU cores
- 64GB RAM
- 500GB SSD storage
- Load balancer (Azure LB, AWS ELB, or NGINX)

### Software Dependencies

```bash
# Required tools
- kubectl 1.24+
- helm 3.10+
- docker 20.10+
- docker-compose 2.0+

# Optional but recommended
- prometheus
- grafana
- istio (service mesh)
```

### Access Requirements

- Cloud provider access (Azure/AWS/GCP)
- Container registry credentials
- TLS certificates for HTTPS
- Environment-specific secrets

---

## Deployment Options

### Option 1: Kubernetes (Production Recommended)

**Best for:**
- Production environments
- High availability
- Auto-scaling
- Multi-region deployments

**Deployment time:** 15-30 minutes

### Option 2: Docker Compose (Development/Testing)

**Best for:**
- Local development
- Testing environments
- Quick demonstrations
- Single-server deployments

**Deployment time:** 5-10 minutes

---

## Kubernetes Deployment

### Step 1: Prepare Configuration

```bash
# Navigate to phase02 deliverables
cd /home/user01/claude-test/SwarmCare/SwarmCare_Production/phases/phase02/deliverables

# Review configuration
cat agents-config.yaml
cat kubernetes-deployment.yaml
```

### Step 2: Create Namespace

```bash
# Create production namespace
kubectl apply -f - <<EOF
apiVersion: v1
kind: Namespace
metadata:
  name: swarmcare-production
  labels:
    name: swarmcare-production
    phase: "02"
EOF
```

### Step 3: Configure Secrets

```bash
# Create secrets for sensitive data
kubectl create secret generic swarmcare-secrets \
  --from-literal=neo4j-uri="bolt://neo4j:7687" \
  --from-literal=neo4j-username="neo4j" \
  --from-literal=neo4j-password="your-secure-password" \
  --from-literal=epic-fhir-endpoint="https://fhir.epic.com" \
  --from-literal=cerner-fhir-endpoint="https://fhir.cerner.com" \
  -n swarmcare-production
```

### Step 4: Apply ConfigMaps

```bash
# Apply agent configuration
kubectl apply -f agents-config.yaml -n swarmcare-production

# Verify configmap
kubectl get configmap swarmcare-agents-config -n swarmcare-production
```

### Step 5: Deploy Agents

```bash
# Deploy all 6 agents
kubectl apply -f kubernetes-deployment.yaml -n swarmcare-production

# Watch deployment progress
kubectl get pods -n swarmcare-production -w
```

### Step 6: Verify Deployment

```bash
# Check all pods are running
kubectl get pods -n swarmcare-production

# Expected output:
# knowledge-agent-xxx      1/1     Running   0          2m
# case-agent-xxx           1/1     Running   0          2m
# conversation-agent-xxx   1/1     Running   0          2m
# compliance-agent-xxx     1/1     Running   0          2m
# podcast-agent-xxx        1/1     Running   0          2m
# qa-agent-xxx             1/1     Running   0          2m

# Check services
kubectl get svc -n swarmcare-production

# Check logs
kubectl logs -f deployment/knowledge-agent -n swarmcare-production
```

### Step 7: Configure Ingress

```bash
# Create ingress for external access
kubectl apply -f - <<EOF
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: swarmcare-agents-ingress
  namespace: swarmcare-production
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  tls:
    - hosts:
        - agents.swarmcare.io
      secretName: swarmcare-agents-tls
  rules:
    - host: agents.swarmcare.io
      http:
        paths:
          - path: /knowledge
            pathType: Prefix
            backend:
              service:
                name: knowledge-agent
                port:
                  number: 80
          - path: /case
            pathType: Prefix
            backend:
              service:
                name: case-agent
                port:
                  number: 80
EOF
```

---

## Docker Compose Deployment

### Step 1: Prepare Environment

```bash
# Navigate to phase02 deliverables
cd /home/user01/claude-test/SwarmCare/SwarmCare_Production/phases/phase02/deliverables

# Create .env file
cat > .env <<EOF
# EHR Integrations
EPIC_FHIR_ENDPOINT=https://fhir.epic.com
CERNER_FHIR_ENDPOINT=https://fhir.cerner.com

# Monitoring
PROMETHEUS_ENDPOINT=http://prometheus:9090
GRAFANA_ENDPOINT=http://grafana:3000

# Logging
LOG_LEVEL=INFO
EOF
```

### Step 2: Pull Images

```bash
# Pull all agent images
docker-compose pull
```

### Step 3: Start Services

```bash
# Start all services in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# Check service status
docker-compose ps
```

### Step 4: Verify Services

```bash
# Test each agent endpoint
curl http://localhost:8081/health  # Knowledge Agent
curl http://localhost:8082/health  # Case Agent
curl http://localhost:8083/health  # Conversation Agent
curl http://localhost:8084/health  # Compliance Agent
curl http://localhost:8085/health  # Podcast Agent
curl http://localhost:8086/health  # QA Agent

# Access Grafana dashboard
open http://localhost:3000
```

---

## Configuration

### Agent Configuration

Each agent can be configured via:
1. **Environment Variables**
2. **ConfigMaps** (Kubernetes)
3. **Config Files**

**Example: Knowledge Agent Configuration**

```yaml
knowledge_agent:
  performance_sla: "2000ms"
  retry_attempts: 3
  timeout: 5000
  integrations:
    neo4j:
      uri: "${NEO4J_URI}"
      database: "medical_ontologies"
```

### Resource Limits

Configure resource limits based on load:

```yaml
resources:
  requests:
    cpu: "1"
    memory: "2Gi"
  limits:
    cpu: "2"
    memory: "4Gi"
```

---

## Monitoring & Observability

### Prometheus Metrics

All agents expose metrics on port `9090`:

```bash
# Query agent metrics
curl http://knowledge-agent:9090/metrics
```

**Key Metrics:**
- `agent_requests_total` - Total requests
- `agent_duration_seconds` - Request duration
- `agent_errors_total` - Total errors
- `agent_sla_violations` - SLA violations

### Grafana Dashboards

Access Grafana at `http://localhost:3000` (admin/admin)

**Pre-built Dashboards:**
1. Agent Performance Overview
2. SLA Compliance
3. Error Rates
4. Resource Utilization

### Logging

Agents log to stdout in JSON format:

```bash
# View logs (Kubernetes)
kubectl logs -f deployment/knowledge-agent -n swarmcare-production

# View logs (Docker)
docker-compose logs -f knowledge-agent
```

---

## Security Considerations

### Network Security

1. **TLS/HTTPS:** Enable TLS for all external endpoints
2. **Network Policies:** Restrict pod-to-pod communication
3. **Service Mesh:** Use Istio for mTLS

### Data Security

1. **Encryption at Rest:** Enable for all persistent volumes
2. **Encryption in Transit:** TLS 1.3 for all connections
3. **Secrets Management:** Use Kubernetes secrets or Azure Key Vault

### HIPAA Compliance

1. **PHI Protection:** Compliance Agent monitors all data
2. **Audit Logging:** All access logged to SIEM
3. **Access Control:** RBAC enforced at all levels

---

## Troubleshooting

### Common Issues

**Issue 1: Pods not starting**

```bash
# Check pod status
kubectl describe pod <pod-name> -n swarmcare-production

# Check events
kubectl get events -n swarmcare-production --sort-by='.lastTimestamp'
```

**Issue 2: High memory usage**

```bash
# Scale down replicas
kubectl scale deployment knowledge-agent --replicas=1 -n swarmcare-production

# Increase resource limits
kubectl set resources deployment knowledge-agent --limits=memory=8Gi -n swarmcare-production
```

**Issue 3: SLA violations**

```bash
# Check metrics
curl http://qa-agent:9090/metrics | grep sla_violation

# Check logs for errors
kubectl logs deployment/qa-agent -n swarmcare-production | grep ERROR
```

---

## Post-Deployment Verification

### Step 1: Run Verification Script

```bash
cd /home/user01/claude-test/SwarmCare/SwarmCare_Production/phases/phase02/deliverables

python3 verify_agents.py --verbose
```

**Expected Output:**
```
================================================================================
SWARMCARE AGENTS VERIFICATION
================================================================================
Verifying Knowledge Agent...
  ✅ Knowledge Agent: VERIFIED
Verifying Case Agent...
  ✅ Case Agent: VERIFIED
...
✅ ALL AGENTS VERIFIED SUCCESSFULLY
================================================================================
```

### Step 2: Run Performance Benchmark

```bash
python3 performance_benchmark.py --iterations 100
```

**Expected Output:**
```
================================================================================
SWARMCARE AGENTS PERFORMANCE BENCHMARK
================================================================================
Agent Performance Summary:
--------------------------------------------------------------------------------
Agent                SLA        Avg        P95        Status
--------------------------------------------------------------------------------
Knowledge Agent      <2000ms    1.2ms      1.8ms      ✅ PASS
Case Agent           <3000ms    2.1ms      2.7ms      ✅ PASS
...
================================================================================
```

### Step 3: Check Health Endpoints

```bash
# Test all health endpoints
for port in 8081 8082 8083 8084 8085 8086; do
  echo "Testing port $port..."
  curl -f http://localhost:$port/health || echo "FAILED"
done
```

### Step 4: Verify Integration

```bash
# Run integration tests
cd ../tests
python3 test_phase02.py
```

---

## Maintenance

### Scaling

```bash
# Scale conversation agent (high traffic)
kubectl scale deployment conversation-agent --replicas=10 -n swarmcare-production

# Enable autoscaling
kubectl autoscale deployment conversation-agent \
  --min=3 --max=20 --cpu-percent=70 \
  -n swarmcare-production
```

### Updates

```bash
# Rolling update
kubectl set image deployment/knowledge-agent \
  knowledge-agent=swarmcare/knowledge-agent:2.2 \
  -n swarmcare-production

# Rollback if needed
kubectl rollout undo deployment/knowledge-agent -n swarmcare-production
```

### Backup

```bash
# Backup configuration
kubectl get all -n swarmcare-production -o yaml > backup.yaml

# Backup secrets
kubectl get secrets -n swarmcare-production -o yaml > secrets-backup.yaml
```

---

## Support

For deployment issues:
1. Check logs: `kubectl logs <pod-name>`
2. Check events: `kubectl get events`
3. Review documentation: `docs/IMPLEMENTATION_GUIDE.md`
4. Run diagnostics: `python3 verify_agents.py --verbose`

---

**Deployment Guide Version:** 2.1
**Last Updated:** 2025-10-28
**Status:** ✅ Production-Ready
