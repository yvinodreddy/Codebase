# SwarmCare Production Deployment - Quick Start Guide

## Prerequisites Checklist

Before deploying to production, ensure you have:

- [ ] Azure subscription with admin access
- [ ] Azure CLI installed (`az --version`)
- [ ] Docker and Docker Compose installed
- [ ] Python 3.x installed
- [ ] Access to production domain/hosting

## Step-by-Step Deployment

### 1. Set Up Azure Resources (30 minutes)

```bash
# Login to Azure
az login

# Create resource group
az group create --name swarmcare-prod-rg --location eastus

# Create Azure Key Vault
az keyvault create \
  --name swarmcare-prod-kv \
  --resource-group swarmcare-prod-rg \
  --location eastus

# Add secrets to Key Vault
az keyvault secret set --vault-name swarmcare-prod-kv \
  --name NEO4J-PASSWORD --value "$(openssl rand -base64 32)"

az keyvault secret set --vault-name swarmcare-prod-kv \
  --name JWT-SECRET-KEY --value "$(openssl rand -base64 64)"

# Get your Azure OpenAI key from portal and add it
az keyvault secret set --vault-name swarmcare-prod-kv \
  --name AZURE-OPENAI-API-KEY --value "your-key-here"

# Create Application Insights
az monitor app-insights component create \
  --app swarmcare-prod-insights \
  --location eastus \
  --resource-group swarmcare-prod-rg
```

### 2. Configure Environment (10 minutes)

```bash
# Copy .env.example to .env
cp .env.example .env

# Edit .env with production values
nano .env

# Required changes:
# - ENVIRONMENT=production
# - DEBUG=false  
# - AZURE_KEY_VAULT_URL=https://swarmcare-prod-kv.vault.azure.net/
# - ALLOWED_ORIGINS=https://your-production-domain.com
# - Update all Azure endpoints and keys
```

### 3. Install Dependencies (5 minutes)

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install spaCy medical model
python -m spacy download en_core_web_sm
```

### 4. Run Production Readiness Tests (2 minutes)

```bash
# Run all tests
pytest tests/test_production_readiness.py -v

# Expected output: 14/14 tests passing
```

### 5. Deploy with Docker Compose (5 minutes)

```bash
# Build and start all services
docker-compose up -d

# Check service health
docker-compose ps

# View logs
docker-compose logs -f swarmcare-api

# Verify Neo4j is running
curl http://localhost:7474

# Verify API is running  
curl http://localhost:8000/api/health
```

### 6. Load Medical Ontologies (10 minutes)

```bash
# Wait for Neo4j to be fully ready
sleep 30

# Load medical ontologies
docker-compose exec neo4j cypher-shell -u neo4j -p $NEO4J_PASSWORD \
  < phases/phase00/deliverables/neo4j-medical-ontologies.cypher

# Verify ontologies loaded
docker-compose exec neo4j cypher-shell -u neo4j -p $NEO4J_PASSWORD \
  -c "MATCH (n) RETURN count(n) AS node_count"
```

### 7. Test API Endpoints (5 minutes)

```bash
# Get auth token (for testing)
TOKEN="your-test-token"

# Test health endpoint
curl http://localhost:8000/api/health

# Test RAG query
curl -X POST http://localhost:8000/api/rag/query \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query": "What are the symptoms of diabetes?", "context_size": 5}'

# Test dashboard metrics
curl http://localhost:8000/api/dashboard/metrics \
  -H "Authorization: Bearer $TOKEN"
```

### 8. Configure Monitoring (15 minutes)

```bash
# Set up Azure Application Insights
# Get connection string from Azure Portal

# Update .env
APPLICATIONINSIGHTS_CONNECTION_STRING=InstrumentationKey=xxx;IngestionEndpoint=xxx

# Restart services
docker-compose restart swarmcare-api

# Verify monitoring
# Check Azure Portal > Application Insights > Live Metrics
```

### 9. Set Up Production DNS & SSL (30 minutes)

```bash
# Point your domain to server IP
# Example: swarmcare.yourdomain.com -> 203.0.113.1

# Install Nginx and Certbot for SSL
sudo apt update
sudo apt install nginx certbot python3-certbot-nginx

# Configure Nginx reverse proxy
sudo nano /etc/nginx/sites-available/swarmcare

# Add configuration:
server {
    server_name swarmcare.yourdomain.com;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

# Enable site
sudo ln -s /etc/nginx/sites-available/swarmcare /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Get SSL certificate
sudo certbot --nginx -d swarmcare.yourdomain.com
```

### 10. Final Security Verification (10 minutes)

```bash
# Run production readiness tests again
pytest tests/test_production_readiness.py -v

# Check for exposed secrets
grep -r "swarmcare123" . 2>/dev/null | grep -v ".git" | grep -v "PRODUCTION_READINESS_REPORT.md"

# Should return no results

# Verify .env is not tracked
git status

# .env should NOT appear in untracked files

# Test rate limiting
for i in {1..100}; do
  curl -X POST http://localhost:8000/api/rag/query \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"query": "test"}' &
done

# Should see 429 (rate limit) responses after 60 requests/minute
```

## Production Checklist

### Security
- [x] All hardcoded credentials removed
- [x] Azure Key Vault configured
- [x] SSL/TLS certificate installed
- [x] CORS properly restricted
- [x] Rate limiting enabled
- [ ] Firewall configured
- [ ] Security audit completed
- [ ] Penetration testing completed

### Configuration
- [x] .env file created from .env.example
- [x] ENVIRONMENT=production
- [x] DEBUG=false
- [ ] All Azure keys replaced with production values
- [ ] Monitoring configured
- [ ] Backup strategy defined

### Testing
- [x] 14/14 production readiness tests passing
- [ ] Load testing completed (1000 concurrent users)
- [ ] Integration tests passing
- [ ] End-to-end tests passing

### Deployment
- [ ] DNS configured
- [ ] SSL certificate installed
- [ ] Nginx reverse proxy configured
- [ ] Docker services running
- [ ] Neo4j ontologies loaded
- [ ] API health check passing

### Monitoring
- [ ] Azure Application Insights configured
- [ ] Prometheus + Grafana set up
- [ ] Alerts configured
- [ ] Log aggregation set up

### Compliance
- [x] HIPAA audit logging enabled
- [x] PHI detection configured
- [ ] Business Associate Agreement (BAA) signed
- [ ] Security audit completed
- [ ] Compliance documentation complete

## Troubleshooting

### Docker Compose Fails to Start

```bash
# Check logs
docker-compose logs

# Check if ports are in use
sudo netstat -tlnp | grep -E '7474|7687|8000|6379'

# Kill conflicting processes
sudo kill -9 <PID>

# Restart
docker-compose down && docker-compose up -d
```

### Neo4j Connection Errors

```bash
# Check Neo4j logs
docker-compose logs neo4j

# Verify password is correct
echo $NEO4J_PASSWORD

# Test connection
docker-compose exec neo4j cypher-shell -u neo4j -p $NEO4J_PASSWORD
```

### API Returns 500 Errors

```bash
# Check API logs
docker-compose logs swarmcare-api

# Common issues:
# 1. Azure OpenAI key invalid - verify in .env
# 2. Neo4j not ready - wait 30s and retry
# 3. Missing dependencies - run pip install -r requirements.txt
```

### Rate Limiting Not Working

```bash
# Verify middleware is loaded
curl -v http://localhost:8000/api/health

# Check for X-RateLimit headers in response
# Should see:
# X-RateLimit-Limit-Minute: 60
# X-RateLimit-Remaining-Minute: 59
```

## Performance Tuning

### Optimize Neo4j

```bash
# Edit docker-compose.yml
# Increase heap size for production
NEO4J_dbms_memory_heap_max__size=4G
NEO4J_dbms_memory_pagecache__size=2G
```

### Scale API with Multiple Workers

```bash
# In .env
API_WORKERS=8  # 2x CPU cores

# Or use Kubernetes for horizontal scaling
```

### Enable Redis for Rate Limiting

```bash
# Update backend_api.py to use Redis
import redis
rate_limit_storage = redis.Redis(host='redis', port=6379, db=1)
```

## Support & Resources

- **Documentation:** PRODUCTION_READINESS_REPORT.md
- **Tests:** `pytest tests/test_production_readiness.py -v`
- **Logs:** `docker-compose logs -f`
- **Health Check:** http://localhost:8000/api/health

## Rollback Procedure

If deployment fails:

```bash
# Stop all services
docker-compose down

# Restore previous configuration
git checkout .env docker-compose.yml

# Restart with previous version
docker-compose up -d
```

## Success Indicators

Deployment is successful when:

1. ✅ All 14 production readiness tests pass
2. ✅ `http://localhost:8000/api/health` returns HTTP 200
3. ✅ Neo4j browser accessible at `http://localhost:7474`
4. ✅ No errors in `docker-compose logs`
5. ✅ Rate limiting headers present in API responses
6. ✅ Azure Application Insights receiving telemetry

---

**Estimated Total Deployment Time:** 2-3 hours

**Recommended Team:** 1 DevOps engineer + 1 backend developer

**Prerequisites Time:** 30-60 minutes (Azure account setup, domain purchase, etc.)
