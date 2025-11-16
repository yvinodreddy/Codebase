# SwarmCare Phase 00 - Production Deployment Guide

**Version:** 2.1 Ultra-Comprehensive
**Status:** ✅ PRODUCTION READY
**Generated:** 2025-10-27

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Quick Start](#quick-start)
4. [Detailed Deployment](#detailed-deployment)
5. [Verification](#verification)
6. [Troubleshooting](#troubleshooting)
7. [Performance Tuning](#performance-tuning)
8. [Maintenance](#maintenance)

---

## Overview

This guide provides step-by-step instructions for deploying the SwarmCare Phase 00 medical ontology database to Neo4j in a production environment.

### What You're Deploying

- **7,050 medical entities** across 13 ontologies
- **13 unique constraints** for data integrity
- **13 indexes** for query performance
- **Cross-ontology relationships** for medical knowledge graph
- **Production-ready** Neo4j Cypher script

---

## Prerequisites

### System Requirements

#### Minimum Requirements
- **CPU:** 2 cores
- **RAM:** 4 GB
- **Disk:** 2 GB free space
- **OS:** Linux, macOS, or Windows

#### Recommended for Production
- **CPU:** 4+ cores
- **RAM:** 8+ GB
- **Disk:** 10+ GB SSD
- **OS:** Linux (Ubuntu 20.04+ or RHEL 8+)

### Software Requirements

1. **Neo4j Database**
   - Version: 4.0 or higher
   - Recommended: Neo4j 5.x (latest)
   - Edition: Community or Enterprise

2. **Neo4j Cypher Shell**
   - Included with Neo4j installation
   - Alternative: Neo4j Browser

3. **Python 3.7+** (for verification scripts)

### Installation Instructions

#### Installing Neo4j on Linux

```bash
# Add Neo4j repository
wget -O - https://debian.neo4j.com/neotechnology.gpg.key | sudo apt-key add -
echo 'deb https://debian.neo4j.com stable latest' | sudo tee /etc/apt/sources.list.d/neo4j.list

# Install Neo4j
sudo apt-get update
sudo apt-get install neo4j

# Start Neo4j
sudo systemctl start neo4j
sudo systemctl enable neo4j
```

#### Installing Neo4j on macOS

```bash
# Using Homebrew
brew install neo4j

# Start Neo4j
neo4j start
```

#### Installing Neo4j on Windows

1. Download from: https://neo4j.com/download/
2. Run installer
3. Start Neo4j Desktop or Service

---

## Quick Start

### 5-Minute Deployment

```bash
# 1. Navigate to deliverables directory
cd /home/user01/claude-test/SwarmCare/SwarmCare_Production/phases/phase00/deliverables

# 2. Start Neo4j (if not running)
neo4j start

# 3. Deploy ontologies
cat neo4j-medical-ontologies.cypher | cypher-shell -u neo4j -p <your-password>

# 4. Verify deployment
python3 verify_ontologies.py

# Done! ✅
```

### Expected Output

```
✅ VERIFICATION PASSED - PRODUCTION READY!
🎯 Generated 7050 medical entities across 13 ontologies
🚀 Ready for Neo4j deployment
```

---

## Detailed Deployment

### Step 1: Prepare Neo4j Database

#### 1.1 Configure Neo4j

Edit Neo4j configuration file (`neo4j.conf`):

```conf
# Memory settings (adjust based on your system)
dbms.memory.heap.initial_size=1G
dbms.memory.heap.max_size=2G
dbms.memory.pagecache.size=1G

# Connection settings
dbms.connector.bolt.enabled=true
dbms.connector.bolt.listen_address=0.0.0.0:7687
dbms.connector.http.enabled=true
dbms.connector.http.listen_address=0.0.0.0:7474

# Security (change default password!)
dbms.security.auth_enabled=true
```

#### 1.2 Start Neo4j

```bash
# Linux/macOS
neo4j start

# Windows
# Use Neo4j Desktop or run as service
```

#### 1.3 Verify Neo4j is Running

```bash
# Check status
neo4j status

# Expected output:
# Neo4j is running at pid XXXXX

# Test connection
cypher-shell -u neo4j -p <password> "RETURN 'Connected!' AS status;"
```

### Step 2: Backup Existing Data (if applicable)

```bash
# Stop Neo4j
neo4j stop

# Backup existing database
cp -r /var/lib/neo4j/data /var/lib/neo4j/data.backup

# Restart Neo4j
neo4j start
```

### Step 3: Clear Existing Ontology Data (Optional)

⚠️ **WARNING:** This will delete ALL data in the database!

```cypher
# Connect to database
cypher-shell -u neo4j -p <password>

# Delete all nodes and relationships
MATCH (n) DETACH DELETE n;

# Verify database is empty
MATCH (n) RETURN count(n);
// Expected: 0
```

### Step 4: Deploy Ontology Data

#### Option A: Using Cypher Shell (Recommended)

```bash
# Navigate to deliverables directory
cd /home/user01/claude-test/SwarmCare/SwarmCare_Production/phases/phase00/deliverables

# Deploy ontologies
cat neo4j-medical-ontologies.cypher | cypher-shell -u neo4j -p <password>

# Monitor progress (deployment takes 1-2 minutes)
```

#### Option B: Using Neo4j Browser

1. Open Neo4j Browser: http://localhost:7474
2. Login with credentials
3. Open file: `neo4j-medical-ontologies.cypher`
4. Copy entire contents
5. Paste into query window
6. Click "Run" (play button)

#### Option C: Using Neo4j Admin Import (For Large Datasets)

```bash
# Stop Neo4j
neo4j stop

# Import (faster for large datasets)
neo4j-admin import \
  --database=neo4j \
  --input=neo4j-medical-ontologies.cypher

# Start Neo4j
neo4j start
```

### Step 5: Verify Deployment

#### 5.1 Run Automated Verification

```bash
python3 verify_ontologies.py
```

#### 5.2 Manual Verification Queries

```cypher
// Count all nodes
MATCH (n) RETURN count(n) AS total_nodes;
// Expected: 7050

// Count by ontology
MATCH (n)
WITH labels(n)[0] AS ontology, count(*) AS count
WHERE ontology IN ['SNOMED', 'ICD10', 'RxNorm', 'LOINC', 'CPT', 'HPO',
                   'MeSH', 'UMLS', 'ATC', 'OMIM', 'GO', 'NDC', 'RadLex']
RETURN ontology, count
ORDER BY ontology;

// Check constraints
CALL db.constraints();
// Expected: 13 constraints

// Check indexes
CALL db.indexes();
// Expected: 13+ indexes

// Check relationships
MATCH ()-[r]->() RETURN type(r), count(*) AS count;
// Expected: 4 relationship types

// Sample query: Find diabetes treatments
MATCH (i:ICD10)-[:TREATS_WITH]->(r:RxNorm)
WHERE i.description CONTAINS 'diabetes'
RETURN i.description, r.name, r.drug_class
LIMIT 10;
```

### Step 6: Test Performance

```cypher
// Test 1: Simple lookup (should be < 1ms)
PROFILE MATCH (s:SNOMED {code: '1000000'}) RETURN s;

// Test 2: Index scan (should be < 5ms)
PROFILE MATCH (i:ICD10) WHERE i.description CONTAINS 'diabetes' RETURN i LIMIT 10;

// Test 3: Relationship traversal (should be < 10ms)
PROFILE MATCH (s:SNOMED)-[r:MAPS_TO]->(i:ICD10) RETURN s, r, i LIMIT 10;

// Test 4: Complex query (should be < 50ms)
PROFILE MATCH (s:SNOMED)-[:MAPS_TO]->(i:ICD10)-[:TREATS_WITH]->(r:RxNorm)
WHERE s.system = 'cardiovascular'
RETURN s.term, i.description, r.name
LIMIT 20;
```

---

## Verification

### Automated Verification

```bash
# Run comprehensive verification
python3 verify_ontologies.py

# Expected output:
# ✅ VERIFICATION PASSED - PRODUCTION READY!
# 🎯 Generated 7050 medical entities across 13 ontologies
```

### Manual Verification Checklist

- [ ] Neo4j is running
- [ ] Database contains 7,050+ nodes
- [ ] All 13 ontologies present
- [ ] 13 constraints created
- [ ] 13+ indexes created
- [ ] Cross-ontology relationships present
- [ ] Sample queries return expected results
- [ ] Performance benchmarks met

---

## Troubleshooting

### Issue: "Connection refused" error

**Solution:**
```bash
# Check if Neo4j is running
neo4j status

# If not running, start it
neo4j start

# Check ports
netstat -an | grep 7474  # HTTP
netstat -an | grep 7687  # Bolt
```

### Issue: "Out of memory" error

**Solution:**
```bash
# Increase heap size in neo4j.conf
dbms.memory.heap.initial_size=2G
dbms.memory.heap.max_size=4G

# Restart Neo4j
neo4j restart
```

### Issue: "Constraint already exists" error

**Solution:**
```cypher
// Drop existing constraints
DROP CONSTRAINT snomed_code IF EXISTS;
// Repeat for all constraints

// Re-run deployment script
```

### Issue: Slow query performance

**Solution:**
```cypher
// Rebuild indexes
CALL db.indexes() YIELD name
CALL db.index.fulltext.drop(name);

// Re-run deployment script to recreate indexes
```

### Issue: "Transaction too large" error

**Solution:**
```bash
# Increase transaction size limit in neo4j.conf
dbms.memory.transaction.max_size=10G

# Restart Neo4j
neo4j restart
```

---

## Performance Tuning

### Memory Configuration

```conf
# For 8GB System
dbms.memory.heap.initial_size=2G
dbms.memory.heap.max_size=4G
dbms.memory.pagecache.size=2G

# For 16GB System
dbms.memory.heap.initial_size=4G
dbms.memory.heap.max_size=8G
dbms.memory.pagecache.size=4G
```

### Query Optimization

```cypher
// Use PROFILE to analyze queries
PROFILE MATCH (s:SNOMED) WHERE s.term CONTAINS 'diabetes' RETURN s;

// Use EXPLAIN to see execution plan
EXPLAIN MATCH (s:SNOMED)-[r]->(i:ICD10) RETURN s, r, i LIMIT 10;

// Create additional indexes as needed
CREATE INDEX snomed_system IF NOT EXISTS FOR (s:SNOMED) ON (s.system);
```

### Connection Pool Tuning

```conf
# Increase connection pool size
dbms.connector.bolt.thread_pool_min_size=5
dbms.connector.bolt.thread_pool_max_size=400
```

---

## Maintenance

### Regular Backups

```bash
# Online backup (Enterprise only)
neo4j-admin backup --database=neo4j --backup-dir=/backups

# Offline backup (All editions)
neo4j stop
cp -r /var/lib/neo4j/data /backups/data-$(date +%Y%m%d)
neo4j start
```

### Database Statistics

```cypher
// Check database size
CALL apoc.meta.stats();

// Check node distribution
CALL apoc.meta.nodeTypeProperties();

// Check relationship distribution
CALL apoc.meta.relTypeProperties();
```

### Monitoring

```bash
# Check logs
tail -f /var/log/neo4j/neo4j.log

# Check metrics (if enabled)
curl http://localhost:7474/db/neo4j/metrics
```

### Updates and Upgrades

```bash
# To update ontology data:
# 1. Regenerate data
python3 generate_production_ontologies.py

# 2. Verify
python3 verify_ontologies.py

# 3. Backup current database
# 4. Deploy new version
cat neo4j-medical-ontologies.cypher | cypher-shell -u neo4j -p <password>

# 5. Verify deployment
python3 verify_ontologies.py
```

---

## Security Best Practices

### 1. Change Default Password

```cypher
// Connect as neo4j
:server connect

// Change password
ALTER CURRENT USER SET PASSWORD FROM 'neo4j' TO '<strong-password>';
```

### 2. Enable Authentication

```conf
# In neo4j.conf
dbms.security.auth_enabled=true
```

### 3. Configure SSL/TLS

```conf
# Enable HTTPS
dbms.connector.https.enabled=true
dbms.ssl.policy.https.enabled=true
```

### 4. Restrict Network Access

```conf
# Bind to specific interface
dbms.connector.bolt.listen_address=127.0.0.1:7687
dbms.connector.http.listen_address=127.0.0.1:7474
```

---

## Production Deployment Checklist

- [ ] System requirements met
- [ ] Neo4j installed and configured
- [ ] Memory settings optimized
- [ ] Default password changed
- [ ] Authentication enabled
- [ ] Backup strategy implemented
- [ ] Monitoring configured
- [ ] Firewall rules configured
- [ ] SSL/TLS enabled (for production)
- [ ] Ontology data deployed
- [ ] Verification passed
- [ ] Performance benchmarks met
- [ ] Documentation reviewed

---

## Support and Resources

### Documentation
- Neo4j Documentation: https://neo4j.com/docs/
- Cypher Query Language: https://neo4j.com/docs/cypher-manual/
- Neo4j Operations: https://neo4j.com/docs/operations-manual/

### Community
- Neo4j Community Forum: https://community.neo4j.com/
- Stack Overflow: https://stackoverflow.com/questions/tagged/neo4j

### SwarmCare Project
- Project Repository: (internal)
- Phase Documentation: `../docs/`
- Issue Tracker: (internal)

---

## Next Steps

After successful deployment:

1. ✅ **Phase 00 Complete** - Medical ontology foundation deployed
2. ⏭️ **Phase 01** - Integrate RAG Heat System
3. ⏭️ **Phase 02** - Implement advanced search
4. ⏭️ **Phase 03+** - Build medical reasoning engine

---

## Appendix: Sample Queries

### Query 1: Find All Diabetes-Related Entities

```cypher
MATCH (n)
WHERE (n.term IS NOT NULL AND n.term =~ '(?i).*diabetes.*')
   OR (n.description IS NOT NULL AND n.description =~ '(?i).*diabetes.*')
   OR (n.concept_name IS NOT NULL AND n.concept_name =~ '(?i).*diabetes.*')
RETURN labels(n)[0] AS ontology, n
LIMIT 50;
```

### Query 2: Find Treatment Pathways

```cypher
MATCH path = (s:SNOMED)-[:MAPS_TO]->(i:ICD10)-[:TREATS_WITH]->(r:RxNorm)
RETURN s.term AS condition, i.description AS diagnosis, r.name AS treatment, r.drug_class
LIMIT 25;
```

### Query 3: Find Diagnostic Tests for Conditions

```cypher
MATCH (s:SNOMED)-[:DIAGNOSED_BY]->(l:LOINC)
RETURN s.term AS condition, l.long_name AS test, l.system
LIMIT 25;
```

### Query 4: Ontology Statistics

```cypher
MATCH (n)
WITH labels(n)[0] AS ontology, count(*) AS count
WHERE ontology IN ['SNOMED', 'ICD10', 'RxNorm', 'LOINC', 'CPT', 'HPO',
                   'MeSH', 'UMLS', 'ATC', 'OMIM', 'GO', 'NDC', 'RadLex']
RETURN ontology, count
ORDER BY count DESC;
```

---

**Document Version:** 1.0
**Last Updated:** 2025-10-27
**Status:** Production Ready ✅
**Maintained By:** SwarmCare Development Team
