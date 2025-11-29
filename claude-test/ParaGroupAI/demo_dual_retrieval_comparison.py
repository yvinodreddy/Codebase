#!/usr/bin/env python3
"""
PERMANENT DUAL RETRIEVAL COMPARISON DEMO

CRITICAL REQUIREMENT (2025-11-29):
This demo shows the MANDATORY display of keyword vs semantic comparison
that must be PERMANENTLY visible in all prsg output files.

This allows you to:
- See exact differences between keyword and semantic search
- Understand quality improvements from dual retrieval
- Validate intelligent merging is combining best from both methods
- Practice with real examples

Usage:
    python3 demo_dual_retrieval_comparison.py

Output:
    - Console display with full comparison
    - Saved to: tmp/dual_retrieval_demo_output.txt
"""

import sys
import os
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from database.dual_context_retriever import DualContextRetriever


def demo_authentication_query():
    """
    Demo 1: Authentication implementation query
    Shows clear difference between keyword exact matching vs semantic understanding
    """
    print("=" * 80)
    print("🔥 DEMO 1: Authentication Implementation Query")
    print("=" * 80)
    print()

    retriever = DualContextRetriever()

    query = "How to implement secure user authentication with JWT tokens"

    print(f"Query: '{query}'")
    print()
    print("This query will show:")
    print("  ✅ Keyword search: Finds results with exact term matches")
    print("  ✅ Semantic search: Finds conceptually similar results")
    print("  ✅ Intelligent merging: Combines best from both methods")
    print()
    print("Running dual retrieval with 99% validation...")
    print()

    # Get comparison output
    output = retriever.print_both_results(
        query=query,
        k=10
    )

    print(output)

    return output


def demo_error_handling_query():
    """
    Demo 2: Error handling query
    Shows semantic search finding conceptually related content
    """
    print("\n\n")
    print("=" * 80)
    print("🔥 DEMO 2: Error Handling Query")
    print("=" * 80)
    print()

    retriever = DualContextRetriever()

    query = "How to handle exceptions and errors gracefully in production"

    print(f"Query: '{query}'")
    print()
    print("This query will show:")
    print("  ✅ Keyword search: Finds 'exception', 'error', 'production' matches")
    print("  ✅ Semantic search: Finds 'error handling', 'try-catch', 'fault tolerance'")
    print("  ✅ Quality difference: Semantic often finds better conceptual matches")
    print()
    print("Running dual retrieval with 99% validation...")
    print()

    # Get comparison output
    output = retriever.print_both_results(
        query=query,
        k=10
    )

    print(output)

    return output


def demo_database_optimization_query():
    """
    Demo 3: Database optimization query
    Shows how both methods complement each other
    """
    print("\n\n")
    print("=" * 80)
    print("🔥 DEMO 3: Database Optimization Query")
    print("=" * 80)
    print()

    retriever = DualContextRetriever()

    query = "Optimize database queries for better performance"

    print(f"Query: '{query}'")
    print()
    print("This query will show:")
    print("  ✅ Keyword search: Finds 'optimize', 'database', 'queries', 'performance'")
    print("  ✅ Semantic search: Finds 'indexing', 'caching', 'query tuning', 'SQL optimization'")
    print("  ✅ Overlap: Results found by BOTH methods (highest confidence)")
    print()
    print("Running dual retrieval with 99% validation...")
    print()

    # Get comparison output
    output = retriever.print_both_results(
        query=query,
        k=10
    )

    print(output)

    return output


def save_all_demos_to_file():
    """
    Save all demo outputs to a permanent file for reference.

    CRITICAL: This file shows what EVERY prsg execution should display.
    """
    output_file = "tmp/dual_retrieval_demo_output.txt"

    # Ensure tmp directory exists
    os.makedirs("tmp", exist_ok=True)

    # Create header
    with open(output_file, 'w') as f:
        f.write("=" * 80 + "\n")
        f.write("PERMANENT DUAL RETRIEVAL COMPARISON DEMO OUTPUT\n")
        f.write("=" * 80 + "\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("\n")
        f.write("CRITICAL REQUIREMENT (2025-11-29):\n")
        f.write("This comparison MUST be PERMANENTLY displayed in ALL prsg output files.\n")
        f.write("\n")
        f.write("This allows you to:\n")
        f.write("  ✅ See exact differences between keyword and semantic search\n")
        f.write("  ✅ Understand quality improvements from dual retrieval\n")
        f.write("  ✅ Validate intelligent merging combines best from both methods\n")
        f.write("  ✅ Make informed decisions about which method works best\n")
        f.write("\n")
        f.write("=" * 80 + "\n")
        f.write("\n\n")

    # Run all demos and append to file
    print("Running all demos and saving to file...")
    print()

    retriever = DualContextRetriever()

    queries = [
        ("Authentication Implementation", "How to implement secure user authentication with JWT tokens"),
        ("Error Handling", "How to handle exceptions and errors gracefully in production"),
        ("Database Optimization", "Optimize database queries for better performance"),
    ]

    for demo_name, query in queries:
        print(f"Running: {demo_name}...")

        # Get and display results
        output = retriever.print_both_results(
            query=query,
            k=10,
            output_file=output_file  # Save to file automatically
        )

        # Also add separator
        with open(output_file, 'a') as f:
            f.write("\n\n")
            f.write("*" * 80 + "\n")
            f.write("*" * 80 + "\n")
            f.write("\n\n")

    print()
    print("=" * 80)
    print(f"✅ All demos saved to: {output_file}")
    print("=" * 80)
    print()
    print("You can review this file to see:")
    print("  1. How keyword search works (exact term matching)")
    print("  2. How semantic search works (conceptual understanding)")
    print("  3. Quality differences between the two methods")
    print("  4. How intelligent merging combines best from both")
    print("  5. 99% confidence validation for production-ready quality")
    print()
    print("This is what EVERY prsg execution should display!")
    print()

    return output_file


def main():
    """
    Main demo runner.

    Shows comprehensive examples of dual retrieval comparison.
    """
    print("\n")
    print("=" * 80)
    print("🔥🔥🔥 DUAL RETRIEVAL COMPARISON DEMO 🔥🔥🔥")
    print("=" * 80)
    print()
    print("CRITICAL REQUIREMENT (2025-11-29):")
    print("This comparison MUST be PERMANENTLY displayed in ALL prsg output files.")
    print()
    print("This demo will show you:")
    print("  1. How keyword search works (exact term matching)")
    print("  2. How semantic search works (conceptual understanding)")
    print("  3. Quality differences between the two methods")
    print("  4. How intelligent merging combines best from both")
    print("  5. 99% confidence validation for production-ready quality")
    print()
    print("Running 3 example queries...")
    print()
    print("=" * 80)
    print()

    # Save all demos to permanent file
    output_file = save_all_demos_to_file()

    print()
    print("=" * 80)
    print("✅✅✅ DEMO COMPLETE ✅✅✅")
    print("=" * 80)
    print()
    print(f"Full output saved to: {output_file}")
    print()
    print("NEXT STEPS:")
    print("  1. Read the output file from top to bottom")
    print("  2. Compare keyword vs semantic results for each query")
    print("  3. Notice the quality differences")
    print("  4. See how intelligent merging combines the best")
    print("  5. Practice with your own queries using:")
    print()
    print("     python3 -c \"")
    print("     from database.dual_context_retriever import DualContextRetriever")
    print("     retriever = DualContextRetriever()")
    print("     output = retriever.print_both_results('your query here', k=10)")
    print("     print(output)")
    print("     \"")
    print()
    print("This comparison is now MANDATORY for ALL prsg executions!")
    print()

    return 0


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
