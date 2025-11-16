# SwarmCare Production Deployment Runbook

**Version:** 1.0.0
**Last Updated:** 2025-10-28
**Maintained By:** SwarmCare DevOps Team

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Pre-Deployment Checklist](#pre-deployment-checklist)
3. [Deployment Procedures](#deployment-procedures)
4. [Rollback Procedures](#rollback-procedures)
5. [Monitoring & Alerts](#monitoring--alerts)
6. [Troubleshooting](#troubleshooting)
7. [Emergency Contacts](#emergency-contacts)

---

## Quick Start

### Minimal Deployment (5 Minutes)

```bash
# 1. Configure kubectl context
export KUBECONFIG=~/.kube/production-config

# 2. Verify cluster connectivity
kubectl cluster-info

# 3. Deploy with Helm
cd deliverables/helm
helm upgrade --install swarmcare . \
  --namespace swarmcare \
  --create-namespace \
  --wait --timeout 10m

# 4. Verify deployment
kubectl get pods -n swarmcare
kubectl get svc -n swarmcare
```

### Automated Deployment

```bash
cd deliverables/scripts
./deploy.sh
```

---

## Pre-Deployment Checklist

### Prerequisites

- [ ] Kubernetes cluster v1.24+ running
- [ ] kubectl configured and authenticated
- [ ] Helm 3.12+ installed
- [ ] Sufficient cluster resources (3+ nodes, 12+ CPU, 24GB+ RAM)
- [ ] Container images pushed to ACR
- [ ] Secrets configured in Key Vault
- [ ] Database backup completed
- [ ] Change request approved
- [ ] Maintenance window scheduled
- [ ] Team notified

### Environment Verification

```bash
# Check cluster version
kubectl version --short

# Check node resources
kubectl top nodes

# Check storage classes
kubectl get storageclass

# Verify namespace exists
kubectl get namespace swarmcare
```

---

## Deployment Procedures

### Standard Deployment (Production)

**Duration:** ~15 minutes
**Risk Level:** Medium
**Rollback Time:** ~5 minutes

#### Step 1: Prepare

```bash
# Set environment variables
export NAMESPACE=swarmcare
export HELM_RELEASE=swarmcare
export IMAGE_TAG=v1.0.0

# Navigate to deployment directory
cd /path/to/SwarmCare/phases/phase08
```

#### Step 2: Backup Current State

```bash
./deliverables/scripts/backup-restore.sh backup
```

Expected output: Backup created with timestamp

#### Step 3: Update Configuration

```bash
# Review current values
helm get values $HELM_RELEASE -n $NAMESPACE

# Update image tag in values.yaml
sed -i "s/tag: .*/tag: $IMAGE_TAG/" deliverables/helm/values.yaml
```

#### Step 4: Dry Run

```bash
helm upgrade --install $HELM_RELEASE ./deliverables/helm \
  --namespace $NAMESPACE \
  --dry-run --debug
```

Expected: No errors, valid YAML output

#### Step 5: Deploy

```bash
helm upgrade --install $HELM_RELEASE ./deliverables/helm \
  --namespace $NAMESPACE \
  --create-namespace \
  --wait --timeout 10m \
  --atomic
```

Expected: Release upgraded, all pods running

#### Step 6: Verify

```bash
# Check deployment status
kubectl rollout status deployment/$HELM_RELEASE -n $NAMESPACE

# Check pod health
kubectl get pods -n $NAMESPACE

# Check services
kubectl get svc -n $NAMESPACE

# Run smoke tests
kubectl run smoke-test --rm -i --restart=Never \
  --image=curlimages/curl:latest \
  --namespace=$NAMESPACE \
  -- curl -f http://swarmcare:8000/health
```

Expected: All pods Running, health check returns 200

#### Step 7: Monitor

```bash
# Watch pod logs
kubectl logs -f deployment/$HELM_RELEASE -n $NAMESPACE

# Check metrics
kubectl top pods -n $NAMESPACE

# View Grafana dashboards
open https://grafana.swarmcare.example.com
```

Expected: No errors in logs, normal resource usage

---

## Rollback Procedures

### Immediate Rollback

**Duration:** ~5 minutes
**Use When:** Critical issues detected

```bash
# List revisions
helm history $HELM_RELEASE -n $NAMESPACE

# Rollback to previous revision
helm rollback $HELM_RELEASE -n $NAMESPACE --wait

# Verify rollback
kubectl rollout status deployment/$HELM_RELEASE -n $NAMESPACE
```

### Rollback to Specific Revision

```bash
# Rollback to specific revision
helm rollback $HELM_RELEASE 5 -n $NAMESPACE --wait

# Verify
kubectl get pods -n $NAMESPACE
```

### Database Rollback

```bash
# Restore from backup
./deliverables/scripts/backup-restore.sh restore <timestamp>

# Verify database
kubectl exec -it postgresql-0 -n $NAMESPACE -- psql -U postgres -c "\l"
```

---

## Monitoring & Alerts

### Key Metrics to Monitor

1. **Pod Health**
   - Metric: `kube_pod_status_phase{namespace="swarmcare"}`
   - Threshold: < 95% running = WARNING
   - Action: Check pod logs, describe pod

2. **CPU Usage**
   - Metric: `container_cpu_usage_seconds_total{namespace="swarmcare"}`
   - Threshold: > 80% = WARNING, > 90% = CRITICAL
   - Action: Scale up, optimize code

3. **Memory Usage**
   - Metric: `container_memory_usage_bytes{namespace="swarmcare"}`
   - Threshold: > 85% = WARNING, > 95% = CRITICAL
   - Action: Scale up, check for memory leaks

4. **Response Time**
   - Metric: `http_request_duration_seconds_bucket{namespace="swarmcare"}`
   - Threshold: p95 > 2s = WARNING, p95 > 5s = CRITICAL
   - Action: Investigate slow queries, check dependencies

5. **Error Rate**
   - Metric: `http_requests_total{status=~"5.."}[5m]`
   - Threshold: > 1% = WARNING, > 5% = CRITICAL
   - Action: Check logs, review recent changes

### Alert Response

#### Critical Alert: Service Down

```bash
# 1. Check pod status
kubectl get pods -n swarmcare

# 2. Check events
kubectl get events -n swarmcare --sort-by='.lastTimestamp'

# 3. Check logs
kubectl logs -l app.kubernetes.io/name=swarmcare -n swarmcare --tail=100

# 4. Describe failing pods
kubectl describe pod <pod-name> -n swarmcare

# 5. If persistent, rollback
helm rollback swarmcare -n swarmcare
```

#### High Memory Usage

```bash
# 1. Identify high-memory pods
kubectl top pods -n swarmcare --sort-by=memory

# 2. Check for memory leaks
kubectl exec -it <pod-name> -n swarmcare -- /bin/sh
# Inside pod: check process memory with top or ps

# 3. Scale up if needed
kubectl scale deployment/swarmcare --replicas=5 -n swarmcare

# 4. Restart pods to clear memory
kubectl rollout restart deployment/swarmcare -n swarmcare
```

---

## Troubleshooting

### Pods Not Starting

**Symptoms:** Pods stuck in Pending, CrashLoopBackOff, or ImagePullBackOff

**Diagnosis:**
```bash
kubectl describe pod <pod-name> -n swarmcare
kubectl logs <pod-name> -n swarmcare --previous
```

**Common Causes & Solutions:**

1. **Insufficient Resources**
   ```bash
   kubectl describe nodes  # Check available resources
   kubectl scale deployment/swarmcare --replicas=2 -n swarmcare  # Reduce replicas
   ```

2. **Image Pull Failure**
   ```bash
   kubectl get secret acr-secret -n swarmcare  # Verify secret exists
   az acr login --name swarmcareacr  # Test ACR access
   ```

3. **Configuration Error**
   ```bash
   kubectl logs <pod-name> -n swarmcare  # Check startup logs
   kubectl get configmap -n swarmcare  # Verify ConfigMap
   ```

### Database Connection Issues

**Symptoms:** Application logs show database connection errors

**Diagnosis:**
```bash
# Test database connectivity
kubectl run db-test --rm -i --restart=Never \
  --image=postgres:14 \
  --namespace=swarmcare \
  -- psql -h postgresql -U postgres -c "SELECT 1"

# Check database pod
kubectl get pods -l app.kubernetes.io/name=postgresql -n swarmcare
kubectl logs postgresql-0 -n swarmcare
```

**Solutions:**

1. **Database Pod Down**
   ```bash
   kubectl delete pod postgresql-0 -n swarmcare  # Restart pod
   ```

2. **Network Policy Blocking**
   ```bash
   kubectl get networkpolicies -n swarmcare
   kubectl describe networkpolicy allow-to-postgresql -n swarmcare
   ```

3. **Credentials Invalid**
   ```bash
   kubectl get secret database-secret -n swarmcare
   kubectl delete secret database-secret -n swarmcare
   # Recreate secret with correct credentials
   ```

### High Latency

**Symptoms:** Slow API responses, timeouts

**Diagnosis:**
```bash
# Check Prometheus metrics
curl http://prometheus.swarmcare.example.com/api/v1/query?query=http_request_duration_seconds_bucket

# Check pod resources
kubectl top pods -n swarmcare

# Check database performance
kubectl exec -it postgresql-0 -n swarmcare -- psql -U postgres -c "
SELECT pid, usename, application_name, state, query
FROM pg_stat_activity
WHERE state != 'idle'
ORDER BY query_start DESC LIMIT 10;"
```

**Solutions:**

1. **Resource Constraints**
   ```bash
   kubectl scale deployment/swarmcare --replicas=5 -n swarmcare
   ```

2. **Slow Database Queries**
   - Review slow query log
   - Add indexes
   - Optimize queries

3. **External API Delays**
   - Check TTS provider status
   - Implement circuit breakers
   - Add caching

---

## Emergency Contacts

### On-Call Schedule

- **Primary:** DevOps Team (+1-555-0100)
- **Secondary:** Platform Team (+1-555-0200)
- **Database:** DBA Team (+1-555-0300)
- **Security:** Security Team (+1-555-0400)

### Escalation Path

1. **Level 1:** On-call Engineer (15 min response)
2. **Level 2:** Team Lead (30 min response)
3. **Level 3:** Engineering Manager (1 hour response)
4. **Level 4:** VP Engineering (2 hour response)

### Communication Channels

- **Slack:** #swarmcare-alerts
- **Pager:** PagerDuty
- **Email:** devops@swarmcare.example.com
- **Status Page:** https://status.swarmcare.example.com

---

## Maintenance Windows

### Scheduled Maintenance

- **Day:** Sunday
- **Time:** 02:00-04:00 UTC
- **Frequency:** Weekly (as needed)

### Pre-Maintenance Steps

1. Notify users 48 hours in advance
2. Create database backup
3. Test deployment in staging
4. Prepare rollback plan
5. Update status page

### Post-Maintenance Steps

1. Verify all services running
2. Check metrics and alerts
3. Update status page
4. Notify completion
5. Post-mortem if issues occurred

---

**Document Version:** 1.0.0
**Last Review:** 2025-10-28
**Next Review:** 2025-11-28
