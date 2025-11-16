#!/usr/bin/env python3
"""
Load and Verify Medical Ontologies in Neo4j
Loads 6,500+ medical entities from Phase 00 into Neo4j and verifies them
"""

from neo4j import GraphDatabase
import os
from pathlib import Path
import time

# Connection details
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "mJe@!ikwcoi4udlFXE$n!ENtv1iAw^F")

# Ontology file path
ONTOLOGY_FILE = Path("neo4j-medical-ontologies.cypher")

def check_current_state():
    """Check current state of Neo4j database"""
    print("=" * 80)
    print("🔍 STEP 1: CHECKING CURRENT NEO4J STATE")
    print("=" * 80)

    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    with driver.session(database="neo4j") as session:
        # Count nodes
        result = session.run("MATCH (n) RETURN count(n) as count")
        node_count = result.single()["count"]

        # Get labels
        result = session.run("CALL db.labels()")
        labels = [r["label"] for r in result]

        print(f"📊 Current Database State:")
        print(f"  - Total Nodes: {node_count:,}")
        print(f"  - Labels: {len(labels)}")
        if labels:
            print(f"  - Label names: {', '.join(labels[:10])}")

    driver.close()
    print()
    return node_count

def load_ontologies():
    """Load ontologies from cypher file into Neo4j"""
    print("=" * 80)
    print("📥 STEP 2: LOADING ONTOLOGIES INTO NEO4J")
    print("=" * 80)

    # Check if file exists
    if not ONTOLOGY_FILE.exists():
        print(f"❌ ERROR: Ontology file not found at: {ONTOLOGY_FILE}")
        return False

    print(f"✅ Found ontology file: {ONTOLOGY_FILE}")
    print(f"   File size: {ONTOLOGY_FILE.stat().st_size:,} bytes")

    # Read the cypher file
    with open(ONTOLOGY_FILE, 'r') as f:
        cypher_content = f.read()

    # Split into individual statements
    statements = [s.strip() for s in cypher_content.split(';') if s.strip()]
    print(f"   Total statements: {len(statements):,}")
    print()

    # Connect to Neo4j
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    # Execute statements in batches
    print("⏳ Loading ontologies (this may take a few minutes)...")
    start_time = time.time()

    successful = 0
    failed = 0

    with driver.session(database="neo4j") as session:
        for i, statement in enumerate(statements, 1):
            if not statement or statement.startswith('//'):
                continue

            try:
                session.run(statement)
                successful += 1

                # Progress indicator
                if i % 500 == 0:
                    elapsed = time.time() - start_time
                    print(f"  ⏳ Progress: {i:,}/{len(statements):,} statements ({i/len(statements)*100:.1f}%) - {elapsed:.1f}s")
            except Exception as e:
                failed += 1
                if failed <= 5:  # Only show first 5 errors
                    print(f"  ⚠️  Error in statement {i}: {str(e)[:100]}")

    driver.close()

    elapsed = time.time() - start_time
    print()
    print(f"✅ Loading complete in {elapsed:.1f} seconds")
    print(f"  - Successful: {successful:,}")
    print(f"  - Failed: {failed:,}")
    print()

    return True

def verify_loaded_ontologies():
    """Verify the loaded ontologies in Neo4j"""
    print("=" * 80)
    print("✅ STEP 3: VERIFYING LOADED ONTOLOGIES")
    print("=" * 80)

    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    # Expected ontologies
    expected_ontologies = [
        'SNOMED', 'ICD10', 'RxNorm', 'LOINC', 'CPT',
        'HPO', 'MeSH', 'UMLS', 'ATC', 'OMIM',
        'GO', 'NDC', 'RadLex'
    ]

    with driver.session(database="neo4j") as session:
        # Overall counts
        result = session.run("MATCH (n) RETURN count(n) as count")
        total_nodes = result.single()["count"]

        result = session.run("MATCH ()-[r]->() RETURN count(r) as count")
        total_rels = result.single()["count"]

        print(f"📊 Overall Database Statistics:")
        print(f"  - Total Nodes: {total_nodes:,}")
        print(f"  - Total Relationships: {total_rels:,}")
        print()

        # Check each ontology
        print("🏷️  Ontology Breakdown:")
        print("-" * 80)
        print(f"{'Ontology':<20} {'Expected':<15} {'Actual':<15} {'Status'}")
        print("-" * 80)

        total_found = 0
        all_good = True

        for ontology in expected_ontologies:
            try:
                result = session.run(f"MATCH (n:`{ontology}`) RETURN count(n) as count")
                count = result.single()["count"]
                total_found += count

                expected = 500
                status = "✅" if count >= expected * 0.95 else "⚠️"
                if count < expected * 0.95:
                    all_good = False

                print(f"{ontology:<20} {expected:<15} {count:<15} {status}")
            except Exception as e:
                print(f"{ontology:<20} {'500':<15} {'0':<15} ❌")
                all_good = False

        print("-" * 80)
        print(f"{'TOTAL':<20} {'6,500':<15} {total_found:<15}")
        print()

        # Get relationship types
        result = session.run("CALL db.relationshipTypes()")
        rel_types = [r["relationshipType"] for r in result]

        if rel_types:
            print(f"🔗 Relationship Types ({len(rel_types)}):")
            for rel_type in rel_types[:10]:
                result = session.run(f"MATCH ()-[r:`{rel_type}`]->() RETURN count(r) as count")
                count = result.single()["count"]
                print(f"  - {rel_type}: {count:,}")
            if len(rel_types) > 10:
                print(f"  ... and {len(rel_types) - 10} more")
        print()

    driver.close()

    print("=" * 80)
    if all_good and total_found >= 6500 * 0.95:
        print("✅ VERIFICATION SUCCESSFUL - ALL ONTOLOGIES LOADED!")
        print(f"🎯 {total_found:,} medical entities verified across {len(expected_ontologies)} ontologies")
    else:
        print("⚠️  VERIFICATION COMPLETED WITH WARNINGS")
        print(f"Found {total_found:,} entities (expected ~6,500)")
    print("=" * 80)
    print()

    return all_good

def main():
    """Main execution flow"""
    print()
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 78 + "║")
    print("║" + "  SwarmCare Medical Ontology Loader & Verifier".center(78) + "║")
    print("║" + "  Load 6,500+ medical entities into Neo4j".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("╚" + "═" * 78 + "╝")
    print()

    # Step 1: Check current state
    current_nodes = check_current_state()

    # Step 2: Load if needed
    if current_nodes > 0:
        response = input(f"⚠️  Database already has {current_nodes:,} nodes. Clear and reload? (yes/no): ")
        if response.lower() == 'yes':
            print("\n🗑️  Clearing database...")
            driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
            with driver.session(database="neo4j") as session:
                session.run("MATCH (n) DETACH DELETE n")
            driver.close()
            print("✅ Database cleared\n")
            load_ontologies()
        else:
            print("\n⏭️  Skipping load, proceeding to verification...\n")
    else:
        load_ontologies()

    # Step 3: Verify
    verify_loaded_ontologies()

    # Final summary
    print("💡 HOW TO ACCESS:")
    print("-" * 80)
    print(f"  Browser UI:   http://localhost:7474")
    print(f"  Bolt URI:     {NEO4J_URI}")
    print(f"  Username:     {NEO4J_USER}")
    print(f"  Password:     {NEO4J_PASSWORD}")
    print()
    print("  Example queries:")
    print("    MATCH (n:SNOMED) RETURN n LIMIT 25")
    print("    MATCH (n) RETURN labels(n), count(n)")
    print("-" * 80)
    print()

if __name__ == "__main__":
    main()
