#!/usr/bin/env python3
"""
Diagnostic Script for Semantic Search Empty Content Issue

Investigates:
1. Database records - What content exists in snapshots?
2. Message extraction - Are messages being extracted correctly?
3. Semantic similarity - Why might we get 0.0000 scores?
4. Empty content - What causes empty results?
"""

import sys
import json
import sqlite3
from pathlib import Path

# Add paths
SCRIPT_DIR = Path(__file__).parent.absolute()
sys.path.insert(0, str(SCRIPT_DIR))

from database.dual_context_retriever import DualContextRetriever
import logging

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

def check_database_content(project_id: str):
    """Check what's actually in the database."""
    print("\n" + "="*80)
    print("DIAGNOSTIC 1: Database Content Analysis")
    print("="*80)

    # Find database file
    db_path = SCRIPT_DIR / "multi_project.db"

    if not db_path.exists():
        print(f"❌ Database not found at: {db_path}")
        return

    print(f"✅ Database found: {db_path}")

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Count total snapshots
    cursor.execute("SELECT COUNT(*) as count FROM context_snapshots WHERE project_id = ?", (project_id,))
    total_count = cursor.fetchone()['count']
    print(f"\nTotal snapshots for project '{project_id}': {total_count}")

    if total_count == 0:
        print("❌ No snapshots found - database is empty for this project!")
        conn.close()
        return

    # Sample first 5 records
    cursor.execute("""
        SELECT snapshot_id, content, created_at
        FROM context_snapshots
        WHERE project_id = ?
        ORDER BY created_at DESC
        LIMIT 5
    """, (project_id,))

    print("\n" + "-"*80)
    print("Sample Records (first 5):")
    print("-"*80)

    empty_content_count = 0
    partial_content_count = 0
    full_content_count = 0

    for i, row in enumerate(cursor.fetchall(), 1):
        content_json = json.loads(row['content'])

        print(f"\nRecord {i} (ID: {row['snapshot_id']}):")
        print(f"  Timestamp: {row['created_at']}")
        print(f"  Fields present: {list(content_json.keys())}")

        # Check each field
        has_title = 'title' in content_json and content_json['title']
        has_description = 'description' in content_json and content_json['description']
        has_code = 'code_example' in content_json and content_json['code_example']
        has_tags = 'tags' in content_json and content_json['tags']

        print(f"  Has title: {'✅' if has_title else '❌'}")
        print(f"  Has description: {'✅' if has_description else '❌'}")
        print(f"  Has code_example: {'✅' if has_code else '❌'}")
        print(f"  Has tags: {'✅' if has_tags else '❌'}")

        # Combine content (same logic as dual_context_retriever.py)
        combined_content = ""
        if has_title:
            combined_content += f"Title: {content_json['title']}\n\n"
        if has_description:
            combined_content += f"Description: {content_json['description']}\n\n"
        if has_code:
            combined_content += f"Code:\n{content_json['code_example']}\n\n"
        if has_tags:
            combined_content += f"Tags: {', '.join(content_json['tags'])}"

        combined_length = len(combined_content.strip())
        print(f"  Combined content length: {combined_length} chars")

        if combined_length == 0:
            empty_content_count += 1
            print("  ⚠️ EMPTY - This record has no searchable content!")
        elif combined_length < 50:
            partial_content_count += 1
            print("  ⚠️ MINIMAL - Very little content (< 50 chars)")
        else:
            full_content_count += 1
            print("  ✅ GOOD - Has sufficient content")

        # Show preview
        if combined_length > 0:
            preview = combined_content.strip()[:100]
            print(f"  Preview: {preview}...")

    conn.close()

    # Summary
    print("\n" + "-"*80)
    print("Content Quality Summary:")
    print("-"*80)
    print(f"  Empty content: {empty_content_count}/5")
    print(f"  Minimal content (< 50 chars): {partial_content_count}/5")
    print(f"  Full content: {full_content_count}/5")

    if empty_content_count > 0:
        print("\n❌ ISSUE FOUND: Some records have empty content!")
        print("   This explains why semantic search shows empty results.")

    if partial_content_count > 0:
        print("\n⚠️ WARNING: Some records have minimal content!")
        print("   These may produce low similarity scores (close to 0.0000).")

def test_semantic_retrieval(project_id: str):
    """Test semantic retrieval with a sample query."""
    print("\n" + "="*80)
    print("DIAGNOSTIC 2: Semantic Retrieval Test")
    print("="*80)

    try:
        retriever = DualContextRetriever(project_id=project_id)

        # Get all messages
        messages = retriever._get_all_messages()

        print(f"\n✅ Extracted {len(messages)} messages from database")

        if len(messages) == 0:
            print("❌ No messages available - cannot test semantic search!")
            return

        # Check message content
        print("\nMessage Content Analysis:")
        print("-"*80)

        empty_msg_count = 0
        for i, msg in enumerate(messages[:5], 1):
            content = msg.get('content', '')
            content_len = len(content)

            print(f"\nMessage {i}:")
            print(f"  ID: {msg.get('id')}")
            print(f"  Content length: {content_len} chars")

            if content_len == 0:
                empty_msg_count += 1
                print("  ⚠️ EMPTY MESSAGE!")
            else:
                preview = content[:100]
                print(f"  Preview: {preview}...")

        if empty_msg_count > 0:
            print(f"\n❌ FOUND {empty_msg_count} EMPTY MESSAGES!")
            print("   This will cause 0.0000 similarity scores.")

        # Test semantic search
        if retriever.semantic_retriever:
            print("\n" + "-"*80)
            print("Testing Semantic Search:")
            print("-"*80)

            test_query = "How does authentication work?"
            print(f"\nQuery: '{test_query}'")

            results = retriever.semantic_retriever.retrieve(test_query, messages, k=5)

            print(f"\nRetrieved {len(results)} results")

            for i, result in enumerate(results, 1):
                score = result.get('score', 0.0)
                msg = result.get('message', {})
                content = msg.get('content', '')

                print(f"\n  Result {i}:")
                print(f"    Similarity: {score:.4f}")
                print(f"    Content length: {len(content)} chars")

                if score < 0.0001:
                    print(f"    ⚠️ NEAR-ZERO SIMILARITY!")
                    if len(content) == 0:
                        print(f"    Cause: Empty message content")
                    else:
                        print(f"    Cause: Query has no semantic overlap with content")
                        print(f"    Content preview: {content[:50]}...")
        else:
            print("\n❌ Semantic retriever not available!")
            print("   Check if sentence-transformers is installed.")

    except Exception as e:
        logger.error(f"Semantic retrieval test failed: {e}")
        import traceback
        traceback.print_exc()

def diagnose_zero_similarity():
    """Explain possible causes of 0.0000 similarity."""
    print("\n" + "="*80)
    print("DIAGNOSTIC 3: Understanding 0.0000 Similarity Scores")
    print("="*80)

    print("\nPossible causes of 0.0000 (or near-zero) similarity:")

    print("\n1. Empty Message Content")
    print("   - Database record has no title, description, code, or tags")
    print("   - Combined content is empty string")
    print("   - Embedding is all zeros or undefined")
    print("   - Result: Cosine similarity = 0.0000")

    print("\n2. No Semantic Overlap")
    print("   - Query: 'How does authentication work?'")
    print("   - Content: 'UI rendering performance optimization'")
    print("   - No shared concepts or keywords")
    print("   - Result: Very low similarity (< 0.1)")

    print("\n3. Query Too Broad or Vague")
    print("   - Query: 'test'")
    print("   - Content: Specific technical implementation")
    print("   - Generic query doesn't match specific content")
    print("   - Result: Low similarity")

    print("\n4. Embedding Model Limitations")
    print("   - Model: all-MiniLM-L6-v2 (384-dim embeddings)")
    print("   - Limited semantic understanding for very technical content")
    print("   - May not capture domain-specific terminology")
    print("   - Result: Lower similarity than expected")

    print("\n✅ Solutions:")
    print("   - Ensure all database records have meaningful content")
    print("   - Use more specific queries")
    print("   - Consider using larger embedding models for better accuracy")
    print("   - Validate data quality before semantic search")

def main():
    """Run all diagnostics."""
    print("="*80)
    print("SEMANTIC SEARCH DIAGNOSTIC TOOL")
    print("="*80)
    print("\nInvestigating why semantic search shows 0.0000 similarity and empty content...")

    # Use default project ID (you can change this)
    project_id = "default_project"

    # Check if we can determine project ID from environment or database
    try:
        import os
        if os.path.exists("multi_project.db"):
            conn = sqlite3.connect("multi_project.db")
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT project_id FROM context_snapshots LIMIT 1")
            row = cursor.fetchone()
            if row:
                project_id = row[0]
                print(f"\nUsing project_id: {project_id}")
            conn.close()
    except Exception as e:
        logger.warning(f"Could not determine project_id: {e}")

    # Run diagnostics
    check_database_content(project_id)
    test_semantic_retrieval(project_id)
    diagnose_zero_similarity()

    # Final summary
    print("\n" + "="*80)
    print("DIAGNOSTIC SUMMARY")
    print("="*80)
    print("\n✅ Diagnostic complete!")
    print("\nTo fix empty content issues:")
    print("  1. Check database records have title, description, or code_example")
    print("  2. Validate data quality during insertion")
    print("  3. Filter out empty messages before semantic search")
    print("  4. Use more specific queries for better similarity scores")

    print("\nTo verify fixes:")
    print("  python3 test_simplified_validation.py")
    print("  ./prsg 'test query' -v")

if __name__ == "__main__":
    main()
