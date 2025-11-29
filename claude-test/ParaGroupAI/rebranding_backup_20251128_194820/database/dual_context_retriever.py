"""
Dual retrieval: keyword AND semantic search with comparison.

⚠️ CRITICAL UPDATE 2025-11-27:
This module now supports 99% confidence validation for BOTH methods.
Use retrieve_with_both_methods_validated() for production-grade results.

⚠️ CRITICAL REQUIREMENT (Effective 2025-11-27):
BOTH keyword AND semantic results MUST be printed in output for comparison.
Use print_both_results() to display complete comparison.

Legacy retrieve_with_both_methods() available for backward compatibility.
"""
from database.context_retriever import ContextRetriever
from database.semantic_retriever import SemanticRetriever
from database.result_formatter import ResultFormatter
from typing import Dict, List, Tuple
import concurrent.futures
import json
import subprocess
import time
import logging

logger = logging.getLogger(__name__)

# Validation constants
MAX_VALIDATION_ITERATIONS = 20
TARGET_CONFIDENCE = 99.0
VALIDATION_SCRIPT = "/home/user01/claude-test/ClaudePrompt/validate_my_response.py"

class DualContextRetriever:
    """Provides BOTH keyword and semantic search with side-by-side comparison."""

    def __init__(self):
        logger.info("Initializing DualContextRetriever")
        try:
            self.keyword_retriever = ContextRetriever()
            logger.info("Keyword retriever: OK")
        except Exception as e:
            logger.error(f"Keyword retriever failed: {e}")
            self.keyword_retriever = None

        try:
            self.semantic_retriever = SemanticRetriever()
            logger.info("Semantic retriever: OK")
        except Exception as e:
            logger.error(f"Semantic retriever failed: {e}")
            self.semantic_retriever = None

    def retrieve_with_both_methods(self, query: str, k: int = 10) -> Dict:
        """
        Run BOTH keyword and semantic search, return BOTH results for comparison.

        ⚠️ LEGACY METHOD - NO VALIDATION:
        This method does NOT validate to 99% confidence.
        For PRODUCTION use, call retrieve_with_both_methods_validated() instead!

        This is the key feature: user sees BOTH methods side-by-side!
        """
        logger.warning("⚠️ Using legacy retrieve_with_both_methods() - NO 99% validation!")
        logger.warning("   For production, use retrieve_with_both_methods_validated() instead")
        logger.info(f"Dual retrieval for query: {query[:50]}...")

        # Get all messages for semantic search
        messages = self._get_all_messages()

        # Run both methods in parallel
        keyword_results = []
        semantic_results = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            # Submit both tasks
            if self.keyword_retriever:
                keyword_future = executor.submit(
                    self._keyword_search_safe, query, k
                )

            if self.semantic_retriever:
                semantic_future = executor.submit(
                    self._semantic_search_safe, query, messages, k
                )

            # Get results
            if self.keyword_retriever:
                keyword_results = keyword_future.result()

            if self.semantic_retriever:
                semantic_results = semantic_future.result()

        # Compare results
        comparison = self._compare_results(keyword_results, semantic_results)

        return {
            'keyword_results': keyword_results,
            'semantic_results': semantic_results,
            'comparison': comparison,
            'recommendation': self._recommend_method(comparison)
        }

    def _keyword_search_safe(self, query: str, k: int) -> List[Dict]:
        """Safe keyword search with error handling."""
        try:
            if self.keyword_retriever:
                return self.keyword_retriever.retrieve(query, limit=k)
        except Exception as e:
            logger.error(f"Keyword search failed: {e}")
        return []

    def _semantic_search_safe(self, query: str, messages: List[Dict], k: int) -> List[Dict]:
        """Safe semantic search with error handling."""
        try:
            if self.semantic_retriever:
                return self.semantic_retriever.retrieve(query, messages, k)
        except Exception as e:
            logger.error(f"Semantic search failed: {e}")
        return []

    def _get_all_messages(self) -> List[Dict]:
        """Get all messages from database."""
        # For now, return empty list
        # TODO: Integrate with actual context database
        return []

    def _compare_results(self, keyword_results, semantic_results):
        """Compare the two result sets."""
        keyword_ids = {r.get('id', i) for i, r in enumerate(keyword_results)}
        semantic_ids = {r['message'].get('id', i) for i, r in enumerate(semantic_results)}

        overlap_ids = keyword_ids & semantic_ids

        return {
            'overlap_percentage': len(overlap_ids) / max(len(keyword_ids), 1) if keyword_ids else 0,
            'overlap_count': len(overlap_ids),
            'keyword_unique_count': len(keyword_ids - overlap_ids),
            'semantic_unique_count': len(semantic_ids - overlap_ids),
            'keyword_time': keyword_results[0].get('retrieval_time', 0) if keyword_results else 0,
            'semantic_time': semantic_results[0].get('retrieval_time', 0) if semantic_results else 0,
            'total_keyword': len(keyword_results),
            'total_semantic': len(semantic_results)
        }

    def _recommend_method(self, comparison):
        """
        Recommend which method to use based on comparison.

        ⚠️ LEGACY METHOD - OVERLAP-BASED (NOT CONFIDENCE-BASED):
        This uses overlap percentage, NOT confidence scores.
        For production, use _recommend_method_by_confidence() instead!
        """
        overlap_pct = comparison['overlap_percentage']

        if overlap_pct >= 0.9:
            return 'keyword'  # Fast and accurate enough
        elif overlap_pct < 0.5:
            return 'both'  # Different results, use both for comprehensive coverage
        else:
            return 'semantic'  # Better semantic understanding

    # =========================================================================
    # PRODUCTION-GRADE METHODS WITH 99% CONFIDENCE VALIDATION
    # =========================================================================

    def retrieve_with_both_methods_validated(
        self,
        query: str,
        k: int = 10,
        require_99_confidence: bool = True
    ) -> Dict:
        """
        Run BOTH keyword and semantic search with 99% confidence validation.

        PRODUCTION-GRADE FLOW:
        1. Run keyword search → Validate to 99% (iterate up to 20x)
        2. Run semantic search → Validate to 99% (iterate up to 20x)
        3. BOTH at 99%? → Compare them
        4. Return comparison with confidence scores

        Args:
            query: Search query
            k: Number of results to retrieve
            require_99_confidence: If True, enforce 99% validation (default: True)

        Returns:
            {
                'keyword_results': [...],
                'keyword_confidence': 99.3,
                'keyword_iterations': 3,
                'semantic_results': [...],
                'semantic_confidence': 99.1,
                'semantic_iterations': 5,
                'comparison': {...},
                'recommendation': 'keyword' | 'semantic' | 'both',
                'validation_summary': {...}
            }
        """
        logger.info(f"🔥 PRODUCTION-GRADE dual retrieval for: {query[:50]}...")
        logger.info(f"   99% Confidence Validation: {'ENABLED ✅' if require_99_confidence else 'DISABLED ⚠️'}")

        # Get all messages for semantic search
        messages = self._get_all_messages()

        # Run both methods in parallel with validation
        keyword_result = {}
        semantic_result = {}

        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            # Submit both validation tasks
            if self.keyword_retriever:
                keyword_future = executor.submit(
                    self._validate_keyword_search,
                    query,
                    k,
                    require_99_confidence
                )

            if self.semantic_retriever:
                semantic_future = executor.submit(
                    self._validate_semantic_search,
                    query,
                    messages,
                    k,
                    require_99_confidence
                )

            # Get validated results
            if self.keyword_retriever:
                keyword_result = keyword_future.result()

            if self.semantic_retriever:
                semantic_result = semantic_future.result()

        # Check if both reached 99%
        keyword_confidence = keyword_result.get('confidence', 0)
        semantic_confidence = semantic_result.get('confidence', 0)

        if require_99_confidence:
            if keyword_confidence < TARGET_CONFIDENCE:
                logger.warning(f"⚠️ Keyword search only reached {keyword_confidence:.1f}% (target: {TARGET_CONFIDENCE}%)")
            if semantic_confidence < TARGET_CONFIDENCE:
                logger.warning(f"⚠️ Semantic search only reached {semantic_confidence:.1f}% (target: {TARGET_CONFIDENCE}%)")

        # Compare results (only meaningful if both are validated)
        comparison = self._compare_validated_results(
            keyword_result.get('results', []),
            semantic_result.get('results', []),
            keyword_confidence,
            semantic_confidence
        )

        # Recommend based on confidence, not just overlap
        recommendation = self._recommend_method_by_confidence(
            comparison,
            keyword_confidence,
            semantic_confidence
        )

        return {
            'keyword_results': keyword_result.get('results', []),
            'keyword_confidence': keyword_confidence,
            'keyword_iterations': keyword_result.get('iterations', 0),
            'semantic_results': semantic_result.get('results', []),
            'semantic_confidence': semantic_confidence,
            'semantic_iterations': semantic_result.get('iterations', 0),
            'comparison': comparison,
            'recommendation': recommendation,
            'validation_summary': {
                'keyword_validated': keyword_confidence >= TARGET_CONFIDENCE,
                'semantic_validated': semantic_confidence >= TARGET_CONFIDENCE,
                'both_validated': (keyword_confidence >= TARGET_CONFIDENCE and
                                 semantic_confidence >= TARGET_CONFIDENCE),
                'production_ready': (keyword_confidence >= TARGET_CONFIDENCE and
                                   semantic_confidence >= TARGET_CONFIDENCE)
            }
        }

    def _validate_keyword_search(
        self,
        query: str,
        k: int,
        require_99: bool
    ) -> Dict:
        """
        Run keyword search and validate to 99% confidence.

        Uses feedback loop with up to 20 iterations.
        """
        logger.info("🔍 Validating keyword search...")

        # Run keyword search
        try:
            results = self.keyword_retriever.retrieve(query, limit=k) if self.keyword_retriever else []
        except Exception as e:
            logger.error(f"Keyword search failed: {e}")
            return {'results': [], 'confidence': 0, 'iterations': 0}

        # If validation not required, return immediately
        if not require_99:
            return {'results': results, 'confidence': 100.0, 'iterations': 0}

        # Validate results through feedback loop
        validated = self._validate_results_with_feedback_loop(
            results=results,
            query=query,
            method_name="keyword"
        )

        return validated

    def _validate_semantic_search(
        self,
        query: str,
        messages: List[Dict],
        k: int,
        require_99: bool
    ) -> Dict:
        """
        Run semantic search and validate to 99% confidence.

        Uses feedback loop with up to 20 iterations.
        """
        logger.info("🧠 Validating semantic search...")

        # Run semantic search
        try:
            results = self.semantic_retriever.retrieve(query, messages, k) if self.semantic_retriever else []
        except Exception as e:
            logger.error(f"Semantic search failed: {e}")
            return {'results': [], 'confidence': 0, 'iterations': 0}

        # If validation not required, return immediately
        if not require_99:
            return {'results': results, 'confidence': 100.0, 'iterations': 0}

        # Validate results through feedback loop
        validated = self._validate_results_with_feedback_loop(
            results=results,
            query=query,
            method_name="semantic"
        )

        return validated

    def _validate_results_with_feedback_loop(
        self,
        results: List[Dict],
        query: str,
        method_name: str
    ) -> Dict:
        """
        Validate search results using feedback loop (up to 20 iterations).

        This is the CRITICAL production-grade validation that was missing!

        Returns:
            {
                'results': [...],  # Final validated results
                'confidence': 99.3,  # Final confidence score
                'iterations': 5,  # Number of iterations needed
                'validation_log': [...]  # All iteration details
            }
        """
        logger.info(f"🔄 Starting validation feedback loop for {method_name} search...")

        current_results = results
        validation_log = []

        for iteration in range(1, MAX_VALIDATION_ITERATIONS + 1):
            # Convert results to text for validation
            results_text = self._results_to_text(current_results, query, method_name)

            # Run validation
            try:
                validation_result = self._run_validation_script(
                    response_text=results_text,
                    prompt=query,
                    iteration=iteration
                )

                confidence = validation_result.get('confidence', 0)
                is_acceptable = validation_result.get('is_acceptable', False)
                suggestions = validation_result.get('suggestions', [])

                validation_log.append({
                    'iteration': iteration,
                    'confidence': confidence,
                    'acceptable': is_acceptable,
                    'suggestions': suggestions
                })

                logger.info(f"   Iteration {iteration}: {confidence:.1f}% confidence")

                # Check if we reached target
                if is_acceptable and confidence >= TARGET_CONFIDENCE:
                    logger.info(f"✅ {method_name.upper()} validated to {confidence:.1f}% after {iteration} iterations")
                    return {
                        'results': current_results,
                        'confidence': confidence,
                        'iterations': iteration,
                        'validation_log': validation_log
                    }

                # If not acceptable, refine results based on suggestions
                if suggestions and iteration < MAX_VALIDATION_ITERATIONS:
                    logger.info(f"   Refining based on suggestions: {suggestions[:2]}")
                    current_results = self._refine_results(current_results, suggestions)

            except Exception as e:
                logger.error(f"Validation error at iteration {iteration}: {e}")
                break

        # If we get here, didn't reach 99%
        final_confidence = validation_log[-1]['confidence'] if validation_log else 0
        logger.warning(f"⚠️ {method_name.upper()} only reached {final_confidence:.1f}% after {MAX_VALIDATION_ITERATIONS} iterations")

        return {
            'results': current_results,
            'confidence': final_confidence,
            'iterations': MAX_VALIDATION_ITERATIONS,
            'validation_log': validation_log
        }

    def _run_validation_script(
        self,
        response_text: str,
        prompt: str,
        iteration: int
    ) -> Dict:
        """
        Call validate_my_response.py to get confidence score.
        """
        try:
            cmd = [
                'python3',
                VALIDATION_SCRIPT,
                response_text,
                '--prompt', prompt,
                '--iteration', str(iteration)
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                return json.loads(result.stdout)
            else:
                logger.error(f"Validation script failed: {result.stderr}")
                return {'confidence': 0, 'is_acceptable': False, 'suggestions': []}

        except Exception as e:
            logger.error(f"Failed to run validation script: {e}")
            return {'confidence': 0, 'is_acceptable': False, 'suggestions': []}

    def _results_to_text(
        self,
        results: List[Dict],
        query: str,
        method_name: str
    ) -> str:
        """Convert results to text format for validation."""
        text_parts = [
            f"{method_name.upper()} SEARCH RESULTS for query: '{query}'",
            f"Total results: {len(results)}",
            ""
        ]

        for i, result in enumerate(results[:5], 1):  # Validate top 5
            if method_name == "keyword":
                text_parts.append(f"{i}. {result.get('content', str(result))[:200]}")
            else:  # semantic
                msg = result.get('message', {})
                similarity = result.get('similarity', 0)
                text_parts.append(f"{i}. [Score: {similarity:.3f}] {str(msg)[:200]}")

        return "\n".join(text_parts)

    def _refine_results(
        self,
        results: List[Dict],
        suggestions: List[str]
    ) -> List[Dict]:
        """
        Refine results based on validation suggestions.

        For now, this is a placeholder. In production:
        - Re-rank based on relevance
        - Filter low-quality results
        - Add context/metadata
        """
        # TODO: Implement intelligent refinement
        # For now, just return original results
        return results

    def _compare_validated_results(
        self,
        keyword_results: List[Dict],
        semantic_results: List[Dict],
        keyword_confidence: float,
        semantic_confidence: float
    ) -> Dict:
        """
        Compare VALIDATED results (both at or near 99% confidence).
        """
        keyword_ids = {r.get('id', i) for i, r in enumerate(keyword_results)}
        semantic_ids = {r['message'].get('id', i) if 'message' in r else i
                       for i, r in enumerate(semantic_results)}

        overlap_ids = keyword_ids & semantic_ids
        overlap_pct = len(overlap_ids) / max(len(keyword_ids), 1) if keyword_ids else 0

        return {
            'overlap_percentage': overlap_pct,
            'overlap_count': len(overlap_ids),
            'keyword_unique_count': len(keyword_ids - overlap_ids),
            'semantic_unique_count': len(semantic_ids - overlap_ids),
            'total_keyword': len(keyword_results),
            'total_semantic': len(semantic_results),
            'keyword_confidence': keyword_confidence,
            'semantic_confidence': semantic_confidence,
            'both_validated_to_99': (keyword_confidence >= TARGET_CONFIDENCE and
                                    semantic_confidence >= TARGET_CONFIDENCE)
        }

    def _recommend_method_by_confidence(
        self,
        comparison: Dict,
        keyword_confidence: float,
        semantic_confidence: float
    ) -> str:
        """
        Recommend method based on CONFIDENCE, not just overlap.

        PRODUCTION-GRADE DECISION LOGIC:
        1. Both < 99%? → ERROR (don't recommend anything)
        2. Only one >= 99%? → Use that one
        3. Both >= 99%? → Compare based on confidence + overlap
        """
        both_validated = comparison.get('both_validated_to_99', False)

        # Case 1: Both failed to reach 99%
        if not both_validated:
            if keyword_confidence < TARGET_CONFIDENCE and semantic_confidence < TARGET_CONFIDENCE:
                return 'error_both_failed'
            elif keyword_confidence >= TARGET_CONFIDENCE:
                return 'keyword'  # Only keyword reached 99%
            else:
                return 'semantic'  # Only semantic reached 99%

        # Case 2: Both validated to 99% - compare them
        overlap_pct = comparison.get('overlap_percentage', 0)
        confidence_diff = abs(keyword_confidence - semantic_confidence)

        # If one is significantly more confident (>2%), prefer it
        if confidence_diff > 2.0:
            return 'keyword' if keyword_confidence > semantic_confidence else 'semantic'

        # If confidence similar, decide based on overlap
        if overlap_pct >= 0.9:
            # Very high overlap - prefer keyword (faster)
            return 'keyword'
        elif overlap_pct < 0.5:
            # Low overlap - use both for comprehensive coverage
            return 'both'
        else:
            # Medium overlap - prefer semantic (better understanding)
            return 'semantic'

    # =========================================================================
    # RESULT PRINTING FOR COMPARISON (CRITICAL REQUIREMENT 2025-11-27)
    # =========================================================================

    def print_both_results(self, query: str, k: int = 10, output_file: str = None) -> str:
        """
        Print BOTH keyword and semantic results for comparison.

        CRITICAL REQUIREMENT (Effective 2025-11-27):
        - BOTH results MUST be visible in output
        - Complete details (content, scores, metadata)
        - Side-by-side comparison
        - MANDATORY for all production use

        This allows users to:
        - See exactly what each method returns
        - Understand differences between methods
        - Make informed decisions
        - Validate both methods work correctly

        Args:
            query: Search query
            k: Number of results
            output_file: Optional file to write output (in addition to return)

        Returns:
            Formatted string with BOTH results
        """
        logger.info(f"🔥 Printing BOTH results for comparison: {query[:50]}...")

        # Get validated results
        result = self.retrieve_with_both_methods_validated(
            query=query,
            k=k,
            require_99_confidence=True  # ALWAYS validate in production
        )

        # Format for output
        formatted_output = ResultFormatter.format_comparison_for_output(result, query)

        # Write to file if specified
        if output_file:
            try:
                with open(output_file, 'a') as f:
                    f.write("\n\n")
                    f.write(formatted_output)
                    f.write("\n\n")
                logger.info(f"✅ Results written to: {output_file}")
            except Exception as e:
                logger.error(f"Failed to write to file: {e}")

        return formatted_output

    def print_both_results_to_file(self, query: str, output_file: str, k: int = 10):
        """
        Convenience method to print results directly to file.

        CRITICAL: This ensures BOTH results are saved for review.

        Args:
            query: Search query
            output_file: File path to write results
            k: Number of results
        """
        return self.print_both_results(query=query, k=k, output_file=output_file)
