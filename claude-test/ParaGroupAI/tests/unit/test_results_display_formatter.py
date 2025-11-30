#!/usr/bin/env python3
"""
Unit Tests for Results Display Formatter
Tests dual retrieval results formatting and display.

Target: 90%+ code coverage
"""

import pytest
import sys
import os
import tempfile
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from results_display_formatter import ResultsDisplayFormatter


class TestResultsDisplayFormatter:
    """Test suite for ResultsDisplayFormatter class"""

    def setup_method(self):
        """Set up test instance"""
        self.formatter = ResultsDisplayFormatter()

        # Sample data for testing
        self.sample_query = "authentication implementation"

        self.sample_keyword_results = [
            {
                'id': 'msg_001',
                'score': 0.95,
                'title': 'JWT Authentication',
                'content': 'JWT authentication implementation guide',
                'timestamp': '2025-11-30T10:00:00Z'
            },
            {
                'id': 'msg_002',
                'score': 0.88,
                'title': 'OAuth 2.0 Setup',
                'content': 'OAuth 2.0 configuration steps',
                'timestamp': '2025-11-30T09:30:00Z'
            }
        ]

        self.sample_semantic_results = [
            {
                'id': 'msg_001',
                'similarity': 0.9234,
                'title': 'JWT Authentication',
                'content': 'JWT authentication implementation guide',
                'timestamp': '2025-11-30T10:00:00Z'
            },
            {
                'id': 'msg_003',
                'similarity': 0.8567,
                'title': 'Multi-Factor Auth',
                'content': 'MFA implementation with SMS',
                'timestamp': '2025-11-30T08:15:00Z'
            }
        ]

        self.sample_overlap_results = [
            {
                'id': 'msg_001',
                'title': 'JWT Authentication',
                'content': 'JWT authentication implementation guide'
            }
        ]

        self.sample_merged_results = [
            {
                'id': 'msg_001',
                'quality_score': 0.95,
                'merge_source': 'overlap',
                'merge_reason': 'Found by both methods',
                'title': 'JWT Authentication',
                'content': 'JWT authentication implementation guide'
            },
            {
                'id': 'msg_002',
                'quality_score': 0.78,
                'merge_source': 'keyword_unique',
                'merge_reason': 'High-quality keyword result',
                'title': 'OAuth 2.0 Setup',
                'content': 'OAuth 2.0 configuration steps'
            }
        ]

    # ========================================
    # Test __init__()
    # ========================================

    def test_init(self):
        """Test formatter initialization"""
        formatter = ResultsDisplayFormatter()
        assert formatter is not None
        assert isinstance(formatter, ResultsDisplayFormatter)

    # ========================================
    # Test format_all_results()
    # ========================================

    def test_format_all_results_basic(self):
        """Test basic results formatting"""
        output = self.formatter.format_all_results(
            query=self.sample_query,
            keyword_results=self.sample_keyword_results,
            semantic_results=self.sample_semantic_results,
            overlap_results=self.sample_overlap_results,
            merged_results=self.sample_merged_results,
            keyword_confidence=99.3,
            semantic_confidence=99.1,
            recommendation='both'
        )

        assert isinstance(output, str)
        assert len(output) > 0

        # Verify main sections
        assert "DUAL RETRIEVAL RESULTS COMPARISON" in output
        assert "KEYWORD SEARCH RESULTS" in output
        assert "SEMANTIC SEARCH RESULTS" in output
        assert "OVERLAP ANALYSIS" in output
        assert "INTELLIGENT MERGE RESULTS" in output
        assert "RECOMMENDATION" in output

    def test_format_all_results_header(self):
        """Test header section formatting"""
        output = self.formatter.format_all_results(
            query=self.sample_query,
            keyword_results=self.sample_keyword_results,
            semantic_results=self.sample_semantic_results,
            overlap_results=self.sample_overlap_results,
            merged_results=self.sample_merged_results,
            keyword_confidence=99.3,
            semantic_confidence=99.1,
            recommendation='both'
        )

        # Verify query in header
        assert self.sample_query in output

        # Verify confidence scores in header
        assert "99.3%" in output  # Keyword confidence
        assert "99.1%" in output  # Semantic confidence

    def test_format_all_results_keyword_section(self):
        """Test keyword search results section"""
        output = self.formatter.format_all_results(
            query=self.sample_query,
            keyword_results=self.sample_keyword_results,
            semantic_results=self.sample_semantic_results,
            overlap_results=self.sample_overlap_results,
            merged_results=self.sample_merged_results,
            keyword_confidence=99.3,
            semantic_confidence=99.1,
            recommendation='both'
        )

        # Verify keyword results section
        assert "Total results: 2" in output  # 2 keyword results
        assert "msg_001" in output
        assert "msg_002" in output
        assert "JWT Authentication" in output
        assert "OAuth 2.0 Setup" in output
        assert "0.950" in output  # Score for first result

    def test_format_all_results_semantic_section(self):
        """Test semantic search results section"""
        output = self.formatter.format_all_results(
            query=self.sample_query,
            keyword_results=self.sample_keyword_results,
            semantic_results=self.sample_semantic_results,
            overlap_results=self.sample_overlap_results,
            merged_results=self.sample_merged_results,
            keyword_confidence=99.3,
            semantic_confidence=99.1,
            recommendation='both'
        )

        # Verify semantic results section
        assert "msg_003" in output
        assert "Multi-Factor Auth" in output
        assert "0.9234" in output  # Similarity for first result

    def test_format_all_results_overlap_section(self):
        """Test overlap analysis section"""
        output = self.formatter.format_all_results(
            query=self.sample_query,
            keyword_results=self.sample_keyword_results,
            semantic_results=self.sample_semantic_results,
            overlap_results=self.sample_overlap_results,
            merged_results=self.sample_merged_results,
            keyword_confidence=99.3,
            semantic_confidence=99.1,
            recommendation='both'
        )

        # Verify overlap section
        assert "Overlap:" in output
        assert "Overlapping results: 1" in output
        assert "Keyword unique: 1" in output
        assert "Semantic unique: 1" in output

    def test_format_all_results_merge_section(self):
        """Test intelligent merge results section"""
        output = self.formatter.format_all_results(
            query=self.sample_query,
            keyword_results=self.sample_keyword_results,
            semantic_results=self.sample_semantic_results,
            overlap_results=self.sample_overlap_results,
            merged_results=self.sample_merged_results,
            keyword_confidence=99.3,
            semantic_confidence=99.1,
            recommendation='both'
        )

        # Verify merge section
        assert "Total merged results: 2" in output
        assert "merge_source" in output.lower() or "Source:" in output
        assert "Found by both methods" in output

    def test_format_all_results_recommendation_section(self):
        """Test recommendation section formatting"""
        output = self.formatter.format_all_results(
            query=self.sample_query,
            keyword_results=self.sample_keyword_results,
            semantic_results=self.sample_semantic_results,
            overlap_results=self.sample_overlap_results,
            merged_results=self.sample_merged_results,
            keyword_confidence=99.3,
            semantic_confidence=99.1,
            recommendation='both'
        )

        # Verify recommendation section
        assert "Recommended approach:" in output or "RECOMMENDATION" in output

    def test_format_all_results_empty_keyword(self):
        """Test formatting with empty keyword results"""
        output = self.formatter.format_all_results(
            query=self.sample_query,
            keyword_results=[],  # Empty
            semantic_results=self.sample_semantic_results,
            overlap_results=[],
            merged_results=self.sample_semantic_results,
            keyword_confidence=0.0,
            semantic_confidence=99.1,
            recommendation='semantic'
        )

        assert "Total results: 0" in output
        assert "(No keyword results found)" in output

    def test_format_all_results_empty_semantic(self):
        """Test formatting with empty semantic results"""
        output = self.formatter.format_all_results(
            query=self.sample_query,
            keyword_results=self.sample_keyword_results,
            semantic_results=[],  # Empty
            overlap_results=[],
            merged_results=self.sample_keyword_results,
            keyword_confidence=99.3,
            semantic_confidence=0.0,
            recommendation='keyword'
        )

        assert "(No semantic results found)" in output

    def test_format_all_results_all_empty(self):
        """Test formatting with all empty results"""
        output = self.formatter.format_all_results(
            query=self.sample_query,
            keyword_results=[],
            semantic_results=[],
            overlap_results=[],
            merged_results=[],
            keyword_confidence=0.0,
            semantic_confidence=0.0,
            recommendation='error_both_failed'
        )

        assert "DUAL RETRIEVAL RESULTS COMPARISON" in output
        assert "(No keyword results found)" in output
        assert "(No semantic results found)" in output
        assert "(No overlapping results)" in output

    def test_format_all_results_different_recommendations(self):
        """Test different recommendation values"""
        recommendations = ['keyword', 'semantic', 'both', 'error_both_failed']

        for rec in recommendations:
            output = self.formatter.format_all_results(
                query=self.sample_query,
                keyword_results=self.sample_keyword_results,
                semantic_results=self.sample_semantic_results,
                overlap_results=self.sample_overlap_results,
                merged_results=self.sample_merged_results,
                keyword_confidence=99.3,
                semantic_confidence=99.1,
                recommendation=rec
            )

            assert isinstance(output, str)
            assert len(output) > 0

    # ========================================
    # Test format_to_file()
    # ========================================

    def test_format_to_file_creates_file(self):
        """Test that format_to_file creates output file"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            temp_file = f.name

        try:
            self.formatter.format_to_file(
                output_file=temp_file,
                query=self.sample_query,
                keyword_results=self.sample_keyword_results,
                semantic_results=self.sample_semantic_results,
                overlap_results=self.sample_overlap_results,
                merged_results=self.sample_merged_results,
                keyword_confidence=99.3,
                semantic_confidence=99.1,
                recommendation='both'
            )

            # Verify file was created
            assert os.path.exists(temp_file)

            # Verify file has content
            with open(temp_file, 'r') as f:
                content = f.read()
                assert len(content) > 0
                assert "DUAL RETRIEVAL RESULTS COMPARISON" in content

        finally:
            # Cleanup
            if os.path.exists(temp_file):
                os.remove(temp_file)

    def test_format_to_file_content_matches_format_all_results(self):
        """Test that file content matches format_all_results output"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            temp_file = f.name

        try:
            # Get direct output
            direct_output = self.formatter.format_all_results(
                query=self.sample_query,
                keyword_results=self.sample_keyword_results,
                semantic_results=self.sample_semantic_results,
                overlap_results=self.sample_overlap_results,
                merged_results=self.sample_merged_results,
                keyword_confidence=99.3,
                semantic_confidence=99.1,
                recommendation='both'
            )

            # Write to file
            self.formatter.format_to_file(
                output_file=temp_file,
                query=self.sample_query,
                keyword_results=self.sample_keyword_results,
                semantic_results=self.sample_semantic_results,
                overlap_results=self.sample_overlap_results,
                merged_results=self.sample_merged_results,
                keyword_confidence=99.3,
                semantic_confidence=99.1,
                recommendation='both'
            )

            # Read from file
            with open(temp_file, 'r') as f:
                file_content = f.read()

            # Both should be identical
            assert direct_output == file_content

        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)

    # ========================================
    # Edge Cases
    # ========================================

    def test_content_truncation(self):
        """Test that long content is truncated to 150 chars"""
        long_content = "A" * 200  # 200 characters

        keyword_results = [
            {
                'id': 'msg_001',
                'score': 0.95,
                'title': 'Test',
                'content': long_content,
                'timestamp': '2025-11-30T10:00:00Z'
            }
        ]

        output = self.formatter.format_all_results(
            query="test",
            keyword_results=keyword_results,
            semantic_results=[],
            overlap_results=[],
            merged_results=[],
            keyword_confidence=99.0,
            semantic_confidence=0.0,
            recommendation='keyword'
        )

        # Verify content was truncated with "..."
        assert "AAA..." in output
        # Verify full content not present
        assert long_content not in output

    def test_metadata_field_extraction(self):
        """Test extraction from metadata dict"""
        keyword_results = [
            {
                'id': 'msg_001',
                'relevance_score': 0.95,  # Alternative field name
                'metadata': {
                    'title': 'Metadata Title',
                    'timestamp': '2025-11-30T10:00:00Z'
                },
                'text': 'Content from text field'  # Alternative field name
            }
        ]

        output = self.formatter.format_all_results(
            query="test",
            keyword_results=keyword_results,
            semantic_results=[],
            overlap_results=[],
            merged_results=[],
            keyword_confidence=99.0,
            semantic_confidence=0.0,
            recommendation='keyword'
        )

        # Verify metadata extraction worked
        assert "Metadata Title" in output
        assert "Content from text field" in output

    def test_missing_fields(self):
        """Test handling of missing fields in results"""
        incomplete_result = [
            {
                'id': 'msg_001'
                # Missing: score, title, content, timestamp
            }
        ]

        output = self.formatter.format_all_results(
            query="test",
            keyword_results=incomplete_result,
            semantic_results=[],
            overlap_results=[],
            merged_results=[],
            keyword_confidence=99.0,
            semantic_confidence=0.0,
            recommendation='keyword'
        )

        # Verify default values used
        assert "No title" in output
        assert "No content" in output
        assert "N/A" in output  # Timestamp

    def test_zero_overlap(self):
        """Test overlap percentage with zero overlap"""
        output = self.formatter.format_all_results(
            query=self.sample_query,
            keyword_results=self.sample_keyword_results,
            semantic_results=self.sample_semantic_results,
            overlap_results=[],  # Zero overlap
            merged_results=self.sample_merged_results,
            keyword_confidence=99.3,
            semantic_confidence=99.1,
            recommendation='both'
        )

        assert "Overlap: 0.0%" in output or "Overlapping results: 0" in output

    def test_complete_overlap(self):
        """Test overlap percentage with 100% overlap"""
        # Same results in both keyword and semantic
        identical_results = [
            {
                'id': 'msg_001',
                'score': 0.95,
                'similarity': 0.92,
                'title': 'Same Result',
                'content': 'Same content',
                'timestamp': '2025-11-30T10:00:00Z'
            }
        ]

        output = self.formatter.format_all_results(
            query=self.sample_query,
            keyword_results=identical_results,
            semantic_results=identical_results,
            overlap_results=identical_results,
            merged_results=identical_results,
            keyword_confidence=99.3,
            semantic_confidence=99.1,
            recommendation='both'
        )

        assert "Overlap: 100.0%" in output


if __name__ == "__main__":
    # Run tests with verbose output
    pytest.main([__file__, "-v", "--tb=short"])
