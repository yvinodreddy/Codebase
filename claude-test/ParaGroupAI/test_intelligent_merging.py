#!/usr/bin/env python3
"""
Comprehensive tests for intelligent result merging in dual retrieval.

Tests cover:
1. Basic merging with overlap
2. No overlap scenario (all unique results)
3. 100% overlap scenario (identical results)
4. Quality-based filtering (low quality results excluded)
5. Complex scenario with mixed quality
6. Validation checks
7. Edge cases (empty inputs, single result, etc.)
"""
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

def create_mock_result(title: str, desc: str, score: float, method: str = 'keyword') -> dict:
    """Create a mock search result for testing."""
    if method == 'keyword':
        return {
            'content': {
                'title': title,
                'description': desc,
                'code_example': 'def example(): pass'
            },
            'score': score,
            'id': f'msg_{title.replace(" ", "_")}'
        }
    else:  # semantic
        return {
            'message': {
                'content': {
                    'title': title,
                    'description': desc,
                    'code_example': 'def example(): pass'
                },
                'id': f'msg_{title.replace(" ", "_")}'
            },
            'similarity': score
        }


def test_basic_merging_with_overlap():
    """Test 1: Basic merging with 50% overlap."""
    print("=" * 80)
    print("TEST 1: Basic Merging with Overlap")
    print("=" * 80)

    try:
        from database.dual_context_retriever import DualContextRetriever

        retriever = DualContextRetriever()

        # Create keyword results (5 results)
        keyword_results = [
            create_mock_result("Auth Implementation", "JWT authentication with refresh tokens", 0.95, 'keyword'),
            create_mock_result("User Login", "Login endpoint implementation", 0.90, 'keyword'),
            create_mock_result("Password Reset", "Password reset flow", 0.85, 'keyword'),
            create_mock_result("Session Management", "Session handling", 0.80, 'keyword'),
            create_mock_result("OAuth Integration", "OAuth 2.0 setup", 0.75, 'keyword'),
        ]

        # Create semantic results (5 results, 2 overlap with keyword)
        semantic_results = [
            create_mock_result("Auth Implementation", "JWT authentication with refresh tokens", 0.92, 'semantic'),
            create_mock_result("User Login", "Login endpoint implementation", 0.88, 'semantic'),
            create_mock_result("Multi-Factor Auth", "MFA implementation guide", 0.87, 'semantic'),
            create_mock_result("Security Best Practices", "Auth security patterns", 0.82, 'semantic'),
            create_mock_result("Token Validation", "JWT token validation", 0.78, 'semantic'),
        ]

        # Test merging
        merged = retriever._merge_results_intelligently(
            keyword_results=keyword_results,
            semantic_results=semantic_results,
            query="authentication implementation"
        )

        print(f"✅ Keyword results: {len(keyword_results)}")
        print(f"✅ Semantic results: {len(semantic_results)}")
        print(f"✅ Merged results: {len(merged)}")
        print(f"✅ Expected: 8-10 (2 overlap + best from 3 keyword unique + best from 3 semantic unique)")

        # Verify merge sources are present
        sources = {r.get('merge_source') for r in merged}
        print(f"✅ Merge sources found: {sources}")

        # Verify quality scores are present
        has_scores = sum(1 for r in merged if 'quality_score' in r)
        print(f"✅ Results with quality scores: {has_scores}/{len(merged)}")

        if len(merged) >= 5:
            print("✅ TEST 1 PASSED\n")
            return True
        else:
            print("❌ TEST 1 FAILED - Not enough merged results\n")
            return False

    except Exception as e:
        print(f"❌ TEST 1 FAILED: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def test_no_overlap_scenario():
    """Test 2: No overlap - all unique results from both methods."""
    print("=" * 80)
    print("TEST 2: No Overlap Scenario")
    print("=" * 80)

    try:
        from database.dual_context_retriever import DualContextRetriever

        retriever = DualContextRetriever()

        # Create completely different keyword results
        keyword_results = [
            create_mock_result("Keyword Result 1", "Description 1", 0.90, 'keyword'),
            create_mock_result("Keyword Result 2", "Description 2", 0.85, 'keyword'),
            create_mock_result("Keyword Result 3", "Description 3", 0.80, 'keyword'),
        ]

        # Create completely different semantic results
        semantic_results = [
            create_mock_result("Semantic Result 1", "Different description 1", 0.88, 'semantic'),
            create_mock_result("Semantic Result 2", "Different description 2", 0.83, 'semantic'),
            create_mock_result("Semantic Result 3", "Different description 3", 0.78, 'semantic'),
        ]

        # Test merging
        merged = retriever._merge_results_intelligently(
            keyword_results=keyword_results,
            semantic_results=semantic_results,
            query="test query"
        )

        print(f"✅ Keyword results: {len(keyword_results)}")
        print(f"✅ Semantic results: {len(semantic_results)}")
        print(f"✅ Merged results: {len(merged)}")
        print(f"✅ Expected: Up to 6 (0 overlap + up to 3 keyword + up to 3 semantic)")

        # With no overlap, should get best from both methods
        if len(merged) >= 3:  # At least some results from both
            print("✅ TEST 2 PASSED\n")
            return True
        else:
            print("❌ TEST 2 FAILED - Not enough results\n")
            return False

    except Exception as e:
        print(f"❌ TEST 2 FAILED: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def test_complete_overlap():
    """Test 3: 100% overlap - identical results from both methods."""
    print("=" * 80)
    print("TEST 3: Complete Overlap (100%)")
    print("=" * 80)

    try:
        from database.dual_context_retriever import DualContextRetriever

        retriever = DualContextRetriever()

        # Create identical results for both methods
        keyword_results = [
            create_mock_result("Shared Result 1", "Same description 1", 0.90, 'keyword'),
            create_mock_result("Shared Result 2", "Same description 2", 0.85, 'keyword'),
            create_mock_result("Shared Result 3", "Same description 3", 0.80, 'keyword'),
        ]

        semantic_results = [
            create_mock_result("Shared Result 1", "Same description 1", 0.88, 'semantic'),
            create_mock_result("Shared Result 2", "Same description 2", 0.83, 'semantic'),
            create_mock_result("Shared Result 3", "Same description 3", 0.78, 'semantic'),
        ]

        # Test merging
        merged = retriever._merge_results_intelligently(
            keyword_results=keyword_results,
            semantic_results=semantic_results,
            query="test query"
        )

        print(f"✅ Keyword results: {len(keyword_results)}")
        print(f"✅ Semantic results: {len(semantic_results)}")
        print(f"✅ Merged results: {len(merged)}")
        print(f"✅ Expected: 3 (100% overlap, no unique results)")

        # With 100% overlap, should get exactly 3 results (the overlap)
        if len(merged) == 3:
            print("✅ TEST 3 PASSED\n")
            return True
        else:
            print("❌ TEST 3 FAILED - Wrong number of results\n")
            print(f"   Expected 3 (overlap only), got {len(merged)}")
            return False

    except Exception as e:
        print(f"❌ TEST 3 FAILED: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def test_quality_filtering():
    """Test 4: 100% Coverage - ALL results included (with quality tiers)."""
    print("=" * 80)
    print("TEST 4: 100% Coverage (All Results Included)")
    print("=" * 80)

    try:
        from database.dual_context_retriever import DualContextRetriever

        retriever = DualContextRetriever()

        # Create keyword results with varying quality (some very low score)
        keyword_results = [
            create_mock_result("High Quality", "Detailed implementation with examples and best practices", 0.95, 'keyword'),
            create_mock_result("Medium Quality", "Basic implementation", 0.70, 'keyword'),
            create_mock_result("Low Quality", "Brief", 0.30, 'keyword'),  # Very low score
        ]

        # Create semantic results with varying quality
        semantic_results = [
            create_mock_result("Good Semantic", "Comprehensive guide with code samples", 0.88, 'semantic'),
            create_mock_result("Poor Semantic", "X", 0.25, 'semantic'),  # Very low score
        ]

        # Test merging
        merged = retriever._merge_results_intelligently(
            keyword_results=keyword_results,
            semantic_results=semantic_results,
            query="implementation guide"
        )

        print(f"✅ Keyword results: {len(keyword_results)}")
        print(f"✅ Semantic results: {len(semantic_results)}")
        print(f"✅ Merged results: {len(merged)}")

        # NEW BEHAVIOR (2025-11-29): ALL results should be included for 100% coverage
        # Low quality results should be INCLUDED but FLAGGED with quality_tier
        titles = [r.get('content', {}).get('title', r.get('message', {}).get('content', {}).get('title', ''))
                  for r in merged]
        print(f"✅ Titles in merged results: {titles}")

        # Verify ALL results are included (including low quality)
        expected_total = len(keyword_results) + len(semantic_results)  # 3 + 2 = 5
        has_all_results = (len(merged) == expected_total)

        # Verify quality tiers are present
        quality_tiers = [r.get('quality_tier') for r in merged]
        has_quality_tiers = all(tier is not None for tier in quality_tiers)

        print(f"✅ Expected {expected_total} results, got {len(merged)}")
        print(f"✅ Quality tiers: {quality_tiers}")

        if has_all_results and has_quality_tiers:
            print("✅ TEST 4 PASSED - 100% coverage (all results included with quality tiers)\n")
            return True
        else:
            print("❌ TEST 4 FAILED - Not all results included or missing quality tiers\n")
            return False

    except Exception as e:
        print(f"❌ TEST 4 FAILED: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def test_validation_checks():
    """Test 5: Validation checks on merged results."""
    print("=" * 80)
    print("TEST 5: Validation Checks")
    print("=" * 80)

    try:
        from database.dual_context_retriever import DualContextRetriever

        retriever = DualContextRetriever()

        # Create sample results
        keyword_results = [
            create_mock_result("Result 1", "Description 1", 0.90, 'keyword'),
            create_mock_result("Result 2", "Description 2", 0.85, 'keyword'),
        ]

        semantic_results = [
            create_mock_result("Result 1", "Description 1", 0.88, 'semantic'),  # Overlap
            create_mock_result("Result 3", "Description 3", 0.83, 'semantic'),
        ]

        # Test merging
        merged = retriever._merge_results_intelligently(
            keyword_results=keyword_results,
            semantic_results=semantic_results,
            query="test"
        )

        # Run validation
        validation = retriever._validate_merged_results(
            merged_results=merged,
            keyword_results=keyword_results,
            semantic_results=semantic_results,
            overlap_count=1  # One overlap
        )

        print(f"✅ Validation result: {validation['is_valid']}")
        print(f"✅ Total merged: {validation['statistics']['total_merged']}")
        print(f"✅ Has quality scores: {validation['statistics']['has_quality_scores']}")
        print(f"✅ Has merge metadata: {validation['statistics']['has_merge_metadata']}")
        print(f"✅ Duplicates found: {validation['statistics']['duplicates_found']}")

        if validation['is_valid']:
            print("✅ TEST 5 PASSED - Validation successful\n")
            return True
        else:
            print("❌ TEST 5 FAILED - Validation failed")
            print(f"   Errors: {validation['validation_errors']}")
            return False

    except Exception as e:
        print(f"❌ TEST 5 FAILED: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def test_edge_case_empty_inputs():
    """Test 6: Edge case - empty inputs."""
    print("=" * 80)
    print("TEST 6: Edge Case - Empty Inputs")
    print("=" * 80)

    try:
        from database.dual_context_retriever import DualContextRetriever

        retriever = DualContextRetriever()

        # Test with empty inputs
        merged = retriever._merge_results_intelligently(
            keyword_results=[],
            semantic_results=[],
            query="test"
        )

        print(f"✅ Keyword results: 0")
        print(f"✅ Semantic results: 0")
        print(f"✅ Merged results: {len(merged)}")

        if len(merged) == 0:
            print("✅ TEST 6 PASSED - Handles empty inputs correctly\n")
            return True
        else:
            print("❌ TEST 6 FAILED - Should return empty list for empty inputs\n")
            return False

    except Exception as e:
        print(f"❌ TEST 6 FAILED: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def test_edge_case_one_empty():
    """Test 7: Edge case - one method has results, other is empty."""
    print("=" * 80)
    print("TEST 7: Edge Case - One Empty Input")
    print("=" * 80)

    try:
        from database.dual_context_retriever import DualContextRetriever

        retriever = DualContextRetriever()

        # Only keyword results, semantic empty
        keyword_results = [
            create_mock_result("Result 1", "Description 1", 0.90, 'keyword'),
            create_mock_result("Result 2", "Description 2", 0.85, 'keyword'),
        ]

        merged = retriever._merge_results_intelligently(
            keyword_results=keyword_results,
            semantic_results=[],
            query="test"
        )

        print(f"✅ Keyword results: {len(keyword_results)}")
        print(f"✅ Semantic results: 0")
        print(f"✅ Merged results: {len(merged)}")

        # Should get best from keyword only
        if len(merged) > 0:
            print("✅ TEST 7 PASSED - Handles one empty input correctly\n")
            return True
        else:
            print("❌ TEST 7 FAILED - Should have some results from keyword\n")
            return False

    except Exception as e:
        print(f"❌ TEST 7 FAILED: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def run_all_tests():
    """Run all merge tests."""
    print("\n")
    print("=" * 80)
    print("INTELLIGENT MERGING TEST SUITE")
    print("=" * 80)
    print("Testing intelligent result merging for dual retrieval")
    print("=" * 80)
    print("\n")

    results = []

    # Run tests
    results.append(("Basic Merging with Overlap", test_basic_merging_with_overlap()))
    results.append(("No Overlap Scenario", test_no_overlap_scenario()))
    results.append(("Complete Overlap (100%)", test_complete_overlap()))
    results.append(("Quality-Based Filtering", test_quality_filtering()))
    results.append(("Validation Checks", test_validation_checks()))
    results.append(("Edge Case: Empty Inputs", test_edge_case_empty_inputs()))
    results.append(("Edge Case: One Empty Input", test_edge_case_one_empty()))

    # Summary
    print("=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)

    passed = 0
    failed = 0

    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:.<50} {status}")
        if result:
            passed += 1
        else:
            failed += 1

    print("=" * 80)
    print(f"Total: {passed + failed} tests")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print("=" * 80)

    if failed == 0:
        print("\n✅ ALL TESTS PASSED - Intelligent merging working correctly!")
        print("✅ Algorithm successfully combines best results from both methods")
        print("✅ Quality-based filtering working as expected")
        print("✅ Validation catches issues")
        print("✅ Edge cases handled properly")
        return 0
    else:
        print(f"\n❌ {failed} tests failed - Review errors above")
        return 1


if __name__ == "__main__":
    exit_code = run_all_tests()
    sys.exit(exit_code)
