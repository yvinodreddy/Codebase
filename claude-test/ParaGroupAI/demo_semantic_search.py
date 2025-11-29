#!/usr/bin/env python3
"""
Demo: Semantic Search vs Keyword Search
Shows BOTH methods side-by-side for comparison.
"""
from database.dual_context_retriever import DualContextRetriever
import sys

def main():
    print("=" * 80)
    print("SEMANTIC SEARCH DEMO - BOTH METHODS COMPARED")
    print("=" * 80)
    print()

    try:
        retriever = DualContextRetriever()
    except Exception as e:
        print(f"ERROR: Failed to initialize retriever: {e}")
        sys.exit(1)

    # Example queries
    queries = [
        "authentication implementation",
        "error handling",
        "database connection"
    ]

    for query in queries:
        print(f"\nQuery: '{query}'")
        print("-" * 80)

        try:
            results = retriever.retrieve_with_both_methods(query, k=5)

            print("\n📊 COMPARISON:")
            comp = results['comparison']
            print(f"  Keyword results: {comp['total_keyword']}")
            print(f"  Semantic results: {comp['total_semantic']}")
            print(f"  Overlap: {comp['overlap_percentage']*100:.1f}%")
            print(f"  Recommendation: Use {results['recommendation']} method")

            if results['keyword_results']:
                print(f"\n🔍 KEYWORD SEARCH (Fast - {comp['keyword_time']:.3f}s):")
                for i, r in enumerate(results['keyword_results'][:3], 1):
                    content = str(r.get('content', ''))[:60]
                    print(f"  {i}. {content}...")

            if results['semantic_results']:
                print(f"\n🧠 SEMANTIC SEARCH (Intelligent - {comp['semantic_time']:.3f}s):")
                for i, r in enumerate(results['semantic_results'][:3], 1):
                    content = str(r['message'].get('content', ''))[:60]
                    score = r['score']
                    print(f"  {i}. {content}... (similarity: {score:.2f})")

        except Exception as e:
            print(f"ERROR processing query: {e}")

        print()

    print("=" * 80)
    print("✅ Demo complete!")
    print("=" * 80)

if __name__ == "__main__":
    main()
