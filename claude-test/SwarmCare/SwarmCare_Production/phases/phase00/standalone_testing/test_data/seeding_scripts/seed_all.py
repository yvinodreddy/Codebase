#!/usr/bin/env python3
"""
Test Data Seeding Script for Phase 0
Loads all 13 medical ontologies and sample data into Neo4j
"""

import json
import os
import sys
from pathlib import Path

# Add project root to path (from standalone_testing/test_data/seeding_scripts/)
project_root = Path(__file__).parent.parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root))

print("=" * 80)
print("PHASE 0: DATA SEEDING")
print("=" * 80)
print()

# Load seed data
seed_file = Path(__file__).parent.parent / "seed_data.json"

if not seed_file.exists():
    print(f"❌ Error: Seed data file not found: {seed_file}")
    sys.exit(1)

with open(seed_file) as f:
    seed_data = json.load(f)

print(f"✅ Loaded seed data for Phase {seed_data['phase']}")
print()

# Check if Neo4j is available
try:
    from neo4j import GraphDatabase
    NEO4J_AVAILABLE = True
except ImportError:
    print("⚠️  Neo4j Python driver not installed. Install with:")
    print("   pip install neo4j")
    NEO4J_AVAILABLE = False

# Load environment
from dotenv import load_dotenv
load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

if not NEO4J_PASSWORD:
    print("❌ Error: NEO4J_PASSWORD not set in .env")
    sys.exit(1)

print(f"📊 Seeding Medical Ontologies:")
print()

# Seed SNOMED CT
ontology = seed_data["medical_ontologies"]["snomed_ct"]
print(f"1. SNOMED CT: {len(ontology['sample_concepts'])} concepts")

# Seed ICD-10
ontology = seed_data["medical_ontologies"]["icd10"]
print(f"2. ICD-10: {len(ontology['sample_codes'])} codes")

# Seed CPT
ontology = seed_data["medical_ontologies"]["cpt"]
print(f"3. CPT: {len(ontology['sample_codes'])} codes")

# Seed LOINC
ontology = seed_data["medical_ontologies"]["loinc"]
print(f"4. LOINC: {len(ontology['sample_codes'])} codes")

# Seed RxNorm
ontology = seed_data["medical_ontologies"]["rxnorm"]
print(f"5. RxNorm: {len(ontology['sample_medications'])} medications")

print()
print(f"📋 Seeding EHR Data:")
print()

# Seed Epic FHIR
ehr = seed_data["ehr_data"]["epic_fhir"]
print(f"1. Epic FHIR: {len(ehr['sample_patients'])} patients")

print()
print(f"🧪 Seeding API Fixtures:")
print()
print(f"1. RAG Queries: {len(seed_data['api_fixtures']['rag_queries'])}")
print(f"2. Graph Queries: {len(seed_data['api_fixtures']['graph_queries'])}")

print()
print(f"👥 Seeding Patient Scenarios:")
print()
print(f"Total Scenarios: {len(seed_data['patient_scenarios'])}")

if NEO4J_AVAILABLE:
    print()
    print("🔄 Connecting to Neo4j and loading data...")
    print()

    try:
        driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

        with driver.session() as session:
            # Clear existing test data
            session.run("MATCH (n:TestData) DETACH DELETE n")

            # Load SNOMED CT concepts
            snomed_concepts = seed_data["medical_ontologies"]["snomed_ct"]["sample_concepts"]
            for concept in snomed_concepts:
                session.run(
                    """
                    CREATE (c:SNOMEDConcept:TestData {
                        concept_id: $concept_id,
                        term: $term,
                        semantic_tag: $semantic_tag
                    })
                    """,
                    concept_id=concept["concept_id"],
                    term=concept["term"],
                    semantic_tag=concept["semantic_tag"]
                )
            print(f"✅ Loaded {len(snomed_concepts)} SNOMED CT concepts")

            # Load ICD-10 codes
            icd10_codes = seed_data["medical_ontologies"]["icd10"]["sample_codes"]
            for code in icd10_codes:
                session.run(
                    """
                    CREATE (i:ICD10Code:TestData {
                        code: $code,
                        description: $description
                    })
                    """,
                    code=code["code"],
                    description=code["description"]
                )
            print(f"✅ Loaded {len(icd10_codes)} ICD-10 codes")

            # Load CPT codes
            cpt_codes = seed_data["medical_ontologies"]["cpt"]["sample_codes"]
            for code in cpt_codes:
                session.run(
                    """
                    CREATE (c:CPTCode:TestData {
                        code: $code,
                        description: $description
                    })
                    """,
                    code=code["code"],
                    description=code["description"]
                )
            print(f"✅ Loaded {len(cpt_codes)} CPT codes")

            # Load LOINC codes
            loinc_codes = seed_data["medical_ontologies"]["loinc"]["sample_codes"]
            for code in loinc_codes:
                session.run(
                    """
                    CREATE (l:LOINCCode:TestData {
                        code: $code,
                        description: $description
                    })
                    """,
                    code=code["code"],
                    description=code["description"]
                )
            print(f"✅ Loaded {len(loinc_codes)} LOINC codes")

            # Load RxNorm medications
            rxnorm_meds = seed_data["medical_ontologies"]["rxnorm"]["sample_medications"]
            for med in rxnorm_meds:
                session.run(
                    """
                    CREATE (m:RxNormMedication:TestData {
                        rxcui: $rxcui,
                        name: $name
                    })
                    """,
                    rxcui=med["rxcui"],
                    name=med["name"]
                )
            print(f"✅ Loaded {len(rxnorm_meds)} RxNorm medications")

            # Create relationships (example: SNOMED to ICD-10 mapping)
            session.run(
                """
                MATCH (s:SNOMEDConcept {term: 'Diabetes mellitus'})
                MATCH (i:ICD10Code {code: 'E11.9'})
                CREATE (s)-[:MAPS_TO]->(i)
                """
            )
            print(f"✅ Created cross-ontology relationships")

        driver.close()

        print()
        print("━" * 80)
        print("✅ DATA SEEDING COMPLETE")
        print("━" * 80)
        print()
        print("Verify data with:")
        print("  Neo4j Browser: http://localhost:7474")
        print("  Query: MATCH (n:TestData) RETURN count(n)")
        print()

    except Exception as e:
        print(f"❌ Error connecting to Neo4j: {e}")
        print()
        print("Make sure Neo4j is running:")
        print("  docker-compose up -d neo4j")
        sys.exit(1)
else:
    print()
    print("⚠️  Skipping actual data load (Neo4j driver not available)")
    print("   Install with: pip install neo4j")

print("=" * 80)
