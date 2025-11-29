#!/usr/bin/env python3
"""
COMPREHENSIVE REAL TESTS for extract_confidence_from_output.py - 100% Coverage
Tests all 5 extraction methods, file loading, CLI, and edge cases
"""

import pytest
import sys
import os
import tempfile
import json
from pathlib import Path
from unittest.mock import patch, MagicMock
from io import StringIO

# Add paths
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

try:
    from extract_confidence_from_output import ConfidenceExtractor, main
except ImportError as e:
    pytest.skip(f"Cannot import extract_confidence_from_output: {e}", allow_module_level=True)


class TestConfidenceExtractor100Percent:
    """Comprehensive tests for 100% coverage"""

    # ============ INITIALIZATION AND FILE LOADING ============

    def test_init_creates_extractor(self):
        """Test __init__ initializes all attributes"""
        extractor = ConfidenceExtractor("/tmp/test_file.txt")

        assert extractor.file_path == Path("/tmp/test_file.txt")
        assert extractor.content == ""
        assert extractor.answer_section == ""
        assert extractor.confidence_scores == []
        assert extractor.extraction_methods == []

    def test_load_file_not_exists(self):
        """Test load_file returns False when file doesn't exist"""
        extractor = ConfidenceExtractor("/tmp/nonexistent_ultrathink_file_12345.txt")

        result = extractor.load_file()

        assert result == False

    def test_load_file_with_answer_marker(self):
        """Test load_file splits content at answer marker"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("System output here\n⬇️⬇️⬇️\nAnswer content here")
            temp_file = f.name

        try:
            extractor = ConfidenceExtractor(temp_file)
            result = extractor.load_file()

            assert result == True
            assert len(extractor.content) > 0
            assert "Answer content here" in extractor.answer_section
        finally:
            os.unlink(temp_file)

    def test_load_file_without_answer_marker(self):
        """Test load_file uses last 25% as answer when no marker"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            # Write content that's long enough to test 75/25 split
            content = "A" * 100  # First 75 chars are system
            content += "B" * 33  # Last ~25 chars are answer section
            f.write(content)
            temp_file = f.name

        try:
            extractor = ConfidenceExtractor(temp_file)
            result = extractor.load_file()

            assert result == True
            assert len(extractor.answer_section) > 0
        finally:
            os.unlink(temp_file)

    def test_load_file_exception_handling(self):
        """Test load_file handles exceptions gracefully"""
        # Use a directory path instead of file to trigger exception
        extractor = ConfidenceExtractor("/tmp/")

        result = extractor.load_file()

        assert result == False

    # ============ METHOD 1: EXPLICIT CONFIDENCE ============

    def test_method1_confidence_level_in_answer(self):
        """Test method1 extracts **Confidence Level:** from answer section"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("System\n⬇️⬇️⬇️\n**Confidence Level: 95.5%**")
            temp_file = f.name

        try:
            extractor = ConfidenceExtractor(temp_file)
            extractor.load_file()
            score = extractor.method1_explicit_confidence()

            assert score == 95.5
            assert len(extractor.confidence_scores) == 1
            assert extractor.confidence_scores[0]['section'] == 'answer'
        finally:
            os.unlink(temp_file)

    def test_method1_confidence_score_pattern(self):
        """Test method1 extracts Confidence Score: pattern"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("Analysis\nConfidence Score: 87.3%\nEnd")
            temp_file = f.name

        try:
            extractor = ConfidenceExtractor(temp_file)
            extractor.load_file()
            score = extractor.method1_explicit_confidence()

            assert score == 87.3
        finally:
            os.unlink(temp_file)

    def test_method1_final_confidence_pattern(self):
        """Test method1 extracts Final Confidence: pattern"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("Analysis\nFinal Confidence: 92%\nEnd")
            temp_file = f.name

        try:
            extractor = ConfidenceExtractor(temp_file)
            extractor.load_file()
            score = extractor.method1_explicit_confidence()

            assert score == 92.0
        finally:
            os.unlink(temp_file)

    def test_method1_no_confidence_found(self):
        """Test method1 returns None when no confidence patterns found"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("No confidence score in this text")
            temp_file = f.name

        try:
            extractor = ConfidenceExtractor(temp_file)
            extractor.load_file()
            score = extractor.method1_explicit_confidence()

            assert score is None
        finally:
            os.unlink(temp_file)

    # ============ METHOD 2: VALIDATION RESULTS ============

    def test_method2_validation_json_pattern(self):
        """Test method2 extracts from JSON-style validation"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write('{"confidence": 88.5, "is_acceptable": true}')
            temp_file = f.name

        try:
            extractor = ConfidenceExtractor(temp_file)
            extractor.load_file()
            score = extractor.method2_validation_results()

            assert score == 88.5
            assert extractor.confidence_scores[0]['method'] == 'validation_results'
        finally:
            os.unlink(temp_file)

    def test_method2_multiple_confidence_values(self):
        """Test method2 returns max when multiple confidence values"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write('"confidence": 75.0\n"confidence": 90.0\n"confidence": 82.0')
            temp_file = f.name

        try:
            extractor = ConfidenceExtractor(temp_file)
            extractor.load_file()
            score = extractor.method2_validation_results()

            assert score == 90.0  # Should return maximum
        finally:
            os.unlink(temp_file)

    def test_method2_no_validation_found(self):
        """Test method2 returns None when no validation patterns"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("No validation data here")
            temp_file = f.name

        try:
            extractor = ConfidenceExtractor(temp_file)
            extractor.load_file()
            score = extractor.method2_validation_results()

            assert score is None
        finally:
            os.unlink(temp_file)

    # ============ METHOD 3: STRUCTURED SECTIONS ============

    def test_method3_final_verdict_section(self):
        """Test method3 extracts from FINAL VERDICT section"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("Analysis\nFINAL VERDICT\nConfidence: 94%\nEnd")
            temp_file = f.name

        try:
            extractor = ConfidenceExtractor(temp_file)
            extractor.load_file()
            score = extractor.method3_structured_sections()

            assert score == 94.0
        finally:
            os.unlink(temp_file)

    def test_method3_conclusion_section(self):
        """Test method3 extracts from CONCLUSION section"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("Report\nCONCLUSION\nConfidence: 89.5%")
            temp_file = f.name

        try:
            extractor = ConfidenceExtractor(temp_file)
            extractor.load_file()
            score = extractor.method3_structured_sections()

            assert score == 89.5
        finally:
            os.unlink(temp_file)

    def test_method3_no_structured_section(self):
        """Test method3 returns None when no structured sections"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("Random text without sections")
            temp_file = f.name

        try:
            extractor = ConfidenceExtractor(temp_file)
            extractor.load_file()
            score = extractor.method3_structured_sections()

            assert score is None
        finally:
            os.unlink(temp_file)

    # ============ METHOD 4: GUARDRAIL ANALYSIS ============

    def test_method4_guardrail_layers_passed(self):
        """Test method4 calculates confidence from guardrail layers"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("Layer 1: ✅ PASS\nLayer 2: ✅ PASS\nLayer 3: ✅ PASS\nLayer 4: ✅ PASS")
            temp_file = f.name

        try:
            extractor = ConfidenceExtractor(temp_file)
            extractor.load_file()
            score = extractor.method4_guardrail_analysis()

            # 4/8 layers = 50% of layers
            # base_confidence (50) + (4/8) * 45 = 50 + 22.5 = 72.5
            assert score == 72.5
        finally:
            os.unlink(temp_file)

    def test_method4_all_layers_passed(self):
        """Test method4 with all 8 layers passed"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            layers = "\n".join([f"Layer {i}: ✅ passed" for i in range(1, 9)])
            f.write(layers)
            temp_file = f.name

        try:
            extractor = ConfidenceExtractor(temp_file)
            extractor.load_file()
            score = extractor.method4_guardrail_analysis()

            # 8/8 layers = 50 + 45 = 95%
            assert score == 95.0
        finally:
            os.unlink(temp_file)

    def test_method4_no_layers_found(self):
        """Test method4 returns None when no guardrail layers"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("No guardrail information here")
            temp_file = f.name

        try:
            extractor = ConfidenceExtractor(temp_file)
            extractor.load_file()
            score = extractor.method4_guardrail_analysis()

            assert score is None
        finally:
            os.unlink(temp_file)

    # ============ METHOD 5: QUALITY SCORING ============

    def test_method5_quality_score_pattern(self):
        """Test method5 extracts quality scores"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("Quality Score: 85%\nQuality: 90%")
            temp_file = f.name

        try:
            extractor = ConfidenceExtractor(temp_file)
            extractor.load_file()
            score = extractor.method5_quality_scoring()

            # Should average: (85 + 90) / 2 = 87.5
            assert score == 87.5
        finally:
            os.unlink(temp_file)

    def test_method5_single_quality_score(self):
        """Test method5 with single quality score"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("Overall Quality: 92%")
            temp_file = f.name

        try:
            extractor = ConfidenceExtractor(temp_file)
            extractor.load_file()
            score = extractor.method5_quality_scoring()

            assert score == 92.0
        finally:
            os.unlink(temp_file)

    def test_method5_no_quality_found(self):
        """Test method5 returns None when no quality scores"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("No quality metrics in this file")
            temp_file = f.name

        try:
            extractor = ConfidenceExtractor(temp_file)
            extractor.load_file()
            score = extractor.method5_quality_scoring()

            assert score is None
        finally:
            os.unlink(temp_file)

    # ============ EXTRACT ALL METHODS ============

    def test_extract_all_methods_multiple_sources(self):
        """Test extract_all_methods runs all 5 methods"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("""
            Confidence Score: 90%
            "confidence": 85.0
            FINAL VERDICT
            Confidence: 92%
            Layer 1: ✅ PASS
            Quality Score: 88%
            """)
            temp_file = f.name

        try:
            extractor = ConfidenceExtractor(temp_file)
            extractor.load_file()
            scores = extractor.extract_all_methods()

            # Should find scores from multiple methods
            assert len(scores) >= 3  # At least explicit, validation, structured
            assert len(extractor.extraction_methods) >= 3
        finally:
            os.unlink(temp_file)

    def test_extract_all_methods_exception_handling(self):
        """Test extract_all_methods handles exceptions in individual methods"""
        extractor = ConfidenceExtractor("/tmp/test.txt")
        extractor.content = "test"  # Set content without loading file

        # Should not raise exception even if methods fail
        scores = extractor.extract_all_methods()

        assert isinstance(scores, list)

    # ============ GET BEST CONFIDENCE ============

    def test_get_best_confidence_no_scores(self):
        """Test get_best_confidence returns not_found when no scores"""
        extractor = ConfidenceExtractor("/tmp/test.txt")

        result = extractor.get_best_confidence()

        assert result['confidence'] is None
        assert result['status'] == 'not_found'
        assert result['method'] == 'none'

    def test_get_best_confidence_priority_selection(self):
        """Test get_best_confidence selects highest priority score"""
        extractor = ConfidenceExtractor("/tmp/test.txt")

        # Add scores with different priorities
        extractor.confidence_scores = [
            {'method': 'method5', 'score': 95.0, 'priority': 5},
            {'method': 'method1', 'score': 90.0, 'priority': 1},  # Highest priority
            {'method': 'method3', 'score': 92.0, 'priority': 3},
        ]

        result = extractor.get_best_confidence()

        assert result['confidence'] == 90.0  # Should select priority 1
        assert result['method'] == 'method1'
        assert result['status'] == 'success'

    # ============ MAIN EXTRACT METHOD ============

    def test_extract_file_not_found(self):
        """Test extract returns error when file not found"""
        extractor = ConfidenceExtractor("/tmp/nonexistent_file_98765.txt")

        result = extractor.extract()

        assert result['status'] == 'error'
        assert result['method'] == 'file_not_found'
        assert 'File not found' in result['error']

    def test_extract_success_full_workflow(self):
        """Test extract full workflow from file to result"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("Analysis complete\nConfidence Level: 96%\nEnd")
            temp_file = f.name

        try:
            extractor = ConfidenceExtractor(temp_file)
            result = extractor.extract()

            assert result['status'] == 'success'
            assert result['confidence'] == 96.0
            assert 'all_scores' in result
        finally:
            os.unlink(temp_file)

    # ============ MAIN CLI FUNCTION ============

    def test_main_json_output(self):
        """Test main() with --json flag"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("Confidence: 85%")
            temp_file = f.name

        try:
            with patch('sys.argv', ['extract_confidence', temp_file, '--json']):
                output = StringIO()
                with patch('sys.stdout', output):
                    main()

                result = json.loads(output.getvalue())
                assert result['confidence'] == 85.0
                assert result['status'] == 'success'
        finally:
            os.unlink(temp_file)

    def test_main_json_verbose_output(self):
        """Test main() with --json --verbose flags"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("Confidence: 88%")
            temp_file = f.name

        try:
            with patch('sys.argv', ['extract_confidence', temp_file, '--json', '--verbose']):
                output = StringIO()
                with patch('sys.stdout', output):
                    main()

                result = json.loads(output.getvalue())
                assert 'all_scores' in result  # Verbose includes all_scores
        finally:
            os.unlink(temp_file)

    def test_main_text_output_success(self):
        """Test main() text output when confidence found"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("Confidence: 92.5%")
            temp_file = f.name

        try:
            with patch('sys.argv', ['extract_confidence', temp_file]):
                output = StringIO()
                with patch('sys.stdout', output):
                    main()

                assert "92.5" in output.getvalue()
        finally:
            os.unlink(temp_file)

    def test_main_text_verbose_output(self):
        """Test main() text output with --verbose"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("Confidence: 91%")
            temp_file = f.name

        try:
            with patch('sys.argv', ['extract_confidence', temp_file, '--verbose']):
                output = StringIO()
                with patch('sys.stdout', output):
                    main()

                output_text = output.getvalue()
                assert "91" in output_text
                assert "Method:" in output_text
        finally:
            os.unlink(temp_file)

    def test_main_not_found_exit(self):
        """Test main() exits with code 1 when confidence not found"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("No confidence here")
            temp_file = f.name

        try:
            with patch('sys.argv', ['extract_confidence', temp_file]):
                with pytest.raises(SystemExit) as exc_info:
                    main()
                assert exc_info.value.code == 1
        finally:
            os.unlink(temp_file)

    def test_main_error_exit(self):
        """Test main() exits with code 1 on error"""
        with patch('sys.argv', ['extract_confidence', '/tmp/nonexistent_file_99999.txt']):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 1

    # ============ EXCEPTION HANDLING COVERAGE (Lines 257-258) ============

    def test_extract_all_methods_with_exception(self):
        """Test extract_all_methods handles exceptions in methods (lines 257-258)"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("Test content")
            temp_file = f.name

        try:
            extractor = ConfidenceExtractor(temp_file)
            extractor.load_file()

            # Make method1 raise an exception by corrupting the content
            original_content = extractor.content

            # Use patch to make method1 raise an exception
            with patch.object(extractor, 'method1_explicit_confidence', side_effect=Exception("Test exception")):
                # This should trigger lines 257-258 (except Exception: pass)
                scores = extractor.extract_all_methods()

                # Should still work and return scores from other methods
                assert isinstance(scores, list)
                # method1 failed but other methods should still run
        finally:
            os.unlink(temp_file)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
