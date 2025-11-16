# Neo4j Medical Ontology - Quick Start Guide

## ✅ Status: PRODUCTION READY

**Last Updated:** 2025-11-08
**Total Entities:** 7,050
**Success Rate:** 100%

---

## Quick Access

### Database Connection

```bash
# Web Browser (Best for exploration)
http://localhost:7474

# Credentials
Username: neo4j
Password: mJe@!ikwcoi4udlFXE$n!ENtv1iAw^F
Database: neo4j
```

### Docker Access

```bash
# cypher-shell access
docker exec -it swarmcare-neo4j cypher-shell \
  -u neo4j \
  -p 'mJe@!ikwcoi4udlFXE$n!ENtv1iAw^F' \
  -d neo4j
```

### Python Access

```python
from neo4j import GraphDatabase

driver = GraphDatabase.driver(
    "bolt://localhost:7687",
    auth=("neo4j", "mJe@!ikwcoi4udlFXE$n!ENtv1iAw^F")
)

with driver.session(database="neo4j") as session:
    result = session.run("MATCH (n:SNOMED) RETURN n LIMIT 5")
    for record in result:
        print(record["n"])

driver.close()
```

---

## Loaded Ontologies

| Ontology | Count | Description |
|----------|-------|-------------|
| SNOMED CT | 1,010 | Clinical terminology |
| ICD-10 | 500 | Disease classification |
| RxNorm | 500 | Medication terminology |
| LOINC | 500 | Lab tests & observations |
| CPT | 500 | Medical procedures |
| HPO | 500 | Human phenotype |
| MeSH | 500 | Medical subject headings |
| UMLS | 500 | Unified medical language |
| ATC | 540 | Drug classification |
| OMIM | 500 | Genetic disorders |
| GO | 500 | Gene ontology |
| NDC | 500 | Drug codes |
| RadLex | 500 | Radiology lexicon |

**Total:** 7,050 entities

---

## Sample Queries

### Get all labels
```cypher
CALL db.labels()
```

### Count nodes by ontology
```cypher
MATCH (n)
RETURN labels(n)[0] as ontology, count(n) as count
ORDER BY count DESC
```

### Find cardiovascular conditions
```cypher
MATCH (s:SNOMED {system: 'cardiovascular'})
RETURN s.code, s.term
LIMIT 25
```

### Find drugs for a condition
```cypher
MATCH (i:ICD10 {code: 'I10.0'})-[:TREATS_WITH]->(r:RxNorm)
RETURN i.description, r.concept_name
```

### Find diagnostic tests
```cypher
MATCH (s:SNOMED)-[:DIAGNOSED_BY]->(l:LOINC)
RETURN s.term, l.long_name
LIMIT 10
```

### Search by term
```cypher
MATCH (n:SNOMED)
WHERE n.term CONTAINS 'Diabetes'
RETURN n
LIMIT 10
```

---

## Maintenance Commands

### Verify Database

```bash
# Run full verification
cd /home/user01/claude-test/SwarmCare/SwarmCare_Production/phases/phase00/deliverables
python3 LOAD_NEO4J_ONTOLOGIES.py
```

### Reload Database

If you need to reload from scratch:

```bash
cd /home/user01/claude-test/SwarmCare/SwarmCare_Production/phases/phase00/deliverables
python3 LOAD_NEO4J_ONTOLOGIES.py
```

This will:
1. Clear the database
2. Load all constraints
3. Load all indexes
4. Load all 7,050 nodes
5. Create relationships
6. Verify everything

**Time:** ~90 seconds

---

## File Locations

### Source Data
```
/home/user01/claude-test/SwarmCare/SwarmCare_Production/phases/phase00/deliverables/
├── neo4j-medical-ontologies.cypher          # Source data (810 KB)
├── LOAD_NEO4J_ONTOLOGIES.py                 # Production loader script
├── PRODUCTION_VERIFICATION_REPORT.md        # Full verification report
├── QUICK_START_GUIDE.md                     # This file
└── LOAD_SUMMARY.json                        # Latest load summary
```

---

## Troubleshooting

### Can't connect to Neo4j
```bash
# Check if container is running
docker ps | grep neo4j

# Start if stopped
docker start swarmcare-neo4j

# Check logs
docker logs swarmcare-neo4j
```

### Forgot password
The password is stored in the docker container env:
```bash
docker exec swarmcare-neo4j env | grep NEO4J_AUTH
```

Current password: `mJe@!ikwcoi4udlFXE$n!ENtv1iAw^F`

### Database seems empty
Run the loader to populate:
```bash
cd /home/user01/claude-test/SwarmCare/SwarmCare_Production/phases/phase00/deliverables
python3 LOAD_NEO4J_ONTOLOGIES.py
```

---

## Integration with RAG System

The Neo4j ontologies are designed to integrate with the Phase 01 RAG system:

```python
# Example integration
from neo4j import GraphDatabase

class KnowledgeGraphConnector:
    def __init__(self):
        self.driver = GraphDatabase.driver(
            "bolt://localhost:7687",
            auth=("neo4j", "mJe@!ikwcoi4udlFXE$n!ENtv1iAw^F")
        )

    def find_related_concepts(self, term):
        """Find medical concepts related to a term"""
        with self.driver.session(database="neo4j") as session:
            result = session.run("""
                MATCH (n)
                WHERE n.term CONTAINS $term
                   OR n.name CONTAINS $term
                   OR n.description CONTAINS $term
                RETURN n
                LIMIT 10
            """, term=term)
            return [record["n"] for record in result]

    def close(self):
        self.driver.close()
```

---

## Support

**Documentation:**
- Full report: `PRODUCTION_VERIFICATION_REPORT.md`
- Neo4j docs: https://neo4j.com/docs/

**Verification:**
All ontologies have been verified with 100% success rate. See `LOAD_SUMMARY.json` for latest metrics.

---

**Status:** ✅ PRODUCTION READY
**Date:** 2025-11-08
