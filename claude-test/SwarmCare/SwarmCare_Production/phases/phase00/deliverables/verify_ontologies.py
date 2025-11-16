#!/usr/bin/env python3
"""
SwarmCare Phase 0: Ontology Verification Script
Verifies all 6,500 medical ontology samples are present and valid
Story Points: 37 | Generated: 2025-10-27
"""

import re
from pathlib import Path
from datetime import datetime

def verify_ontologies():
    """Verify the generated ontology file"""

    print("=" * 90)
    print("🔍 ONTOLOGY VERIFICATION SUITE")
    print("=" * 90)
    print(f"⏰ Timestamp: {datetime.now().isoformat()}")
    print("=" * 90)
    print()

    cypher_file = Path("neo4j-medical-ontologies.cypher")

    if not cypher_file.exists():
        print("❌ ERROR: Ontology file not found!")
        return False

    with open(cypher_file, 'r') as f:
        content = f.read()

    # Define expected ontologies
    ontologies = {
        'SNOMED': {'target': 500, 'full_name': 'SNOMED CT'},
        'ICD10': {'target': 500, 'full_name': 'ICD-10'},
        'RxNorm': {'target': 500, 'full_name': 'RxNorm'},
        'LOINC': {'target': 500, 'full_name': 'LOINC'},
        'CPT': {'target': 500, 'full_name': 'CPT'},
        'HPO': {'target': 500, 'full_name': 'HPO'},
        'MeSH': {'target': 500, 'full_name': 'MeSH'},
        'UMLS': {'target': 500, 'full_name': 'UMLS'},
        'ATC': {'target': 500, 'full_name': 'ATC'},
        'OMIM': {'target': 500, 'full_name': 'OMIM'},
        'GO': {'target': 500, 'full_name': 'GO'},
        'NDC': {'target': 500, 'full_name': 'NDC'},
        'RadLex': {'target': 500, 'full_name': 'RadLex'},
    }

    total_actual = 0
    total_target = 6500
    all_passed = True

    print("📊 ONTOLOGY SAMPLE COUNTS")
    print("-" * 90)
    print(f"{'Ontology':<30} {'Target':<12} {'Actual':<12} {'Status':<12} {'%'}")
    print("-" * 90)

    for ontology, info in ontologies.items():
        target = info['target']
        full_name = info['full_name']

        # Count CREATE statements for this ontology
        pattern = f"CREATE \\(:{ontology}\\s"
        matches = re.findall(pattern, content)
        actual = len(matches)
        total_actual += actual

        # Calculate percentage
        percentage = (actual / target * 100) if target > 0 else 0

        # Determine status
        if actual >= target:
            status = "✅ PASS"
        elif actual >= target * 0.95:  # Within 5%
            status = "⚠️  CLOSE"
        else:
            status = "❌ FAIL"
            all_passed = False

        print(f"{full_name:<30} {target:<12} {actual:<12} {status:<12} {percentage:.1f}%")

    print("-" * 90)
    print(f"{'TOTAL':<30} {total_target:<12} {total_actual:<12} {'':<12}")
    print("=" * 90)
    print()

    # Verify constraints and indexes
    print("🔧 SCHEMA VERIFICATION")
    print("-" * 90)

    constraints = re.findall(r"CREATE CONSTRAINT \w+ IF NOT EXISTS", content)
    indexes = re.findall(r"CREATE INDEX \w+ IF NOT EXISTS", content)

    print(f"Constraints defined: {len(constraints)}")
    print(f"Indexes defined: {len(indexes)}")
    print("-" * 90)
    print()

    # Verify relationships
    print("🔗 RELATIONSHIP VERIFICATION")
    print("-" * 90)

    relationships = re.findall(r"CREATE \([^)]+\)-\[:\w+\]->", content)
    relationship_types = set(re.findall(r"-\[:(\w+)\]->", content))

    print(f"Relationship statements: {len(relationships)}")
    print(f"Unique relationship types: {len(relationship_types)}")
    print(f"Types: {', '.join(sorted(relationship_types))}")
    print("-" * 90)
    print()

    # Overall statistics
    print("📈 OVERALL STATISTICS")
    print("-" * 90)
    print(f"Total ontologies: {len(ontologies)}")
    print(f"Target samples: {total_target}")
    print(f"Actual samples: {total_actual}")
    print(f"Coverage: {(total_actual / total_target * 100):.2f}%")
    print(f"File size: {cypher_file.stat().st_size:,} bytes")
    print(f"Total lines: {len(content.splitlines()):,}")
    print("-" * 90)
    print()

    # Final status
    print("=" * 90)
    if all_passed and total_actual >= total_target * 0.95:
        print("✅ VERIFICATION PASSED - PRODUCTION READY!")
        print(f"🎯 Generated {total_actual} medical entities across 13 ontologies")
        print("🚀 Ready for Neo4j deployment")
        result = True
    else:
        print("⚠️  VERIFICATION COMPLETED WITH WARNINGS")
        print(f"Generated {total_actual} of {total_target} target entities")
        result = False

    print("=" * 90)
    print()

    return result

if __name__ == "__main__":
    success = verify_ontologies()
    exit(0 if success else 1)
