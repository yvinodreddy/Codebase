#!/usr/bin/env python3
"""Comprehensive test suite for smart_test_generator.py - Target: 90%+ coverage"""
import pytest
import json
import ast
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock, mock_open
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from smart_test_generator import SmartTestGenerator

class TestSmartTestGenerator:
    def setup_method(self):
        self.temp_coverage = tempfile.mktemp(suffix='.json')
        self.coverage_data = {
            'files': {
                'test_module.py': {
                    'missing_lines': [5, 10, 15, 20]
                }
            }
        }
        with open(self.temp_coverage, 'w') as f:
            json.dump(self.coverage_data, f)

        self.generator = SmartTestGenerator(self.temp_coverage)

    def teardown_method(self):
        if Path(self.temp_coverage).exists():
            Path(self.temp_coverage).unlink()

    def test_initialization(self):
        assert self.generator.coverage == self.coverage_data

    def test_get_uncovered_lines(self):
        lines = self.generator.get_uncovered_lines('test_module.py')
        assert lines == {5, 10, 15, 20}

    def test_get_uncovered_lines_no_file(self):
        lines = self.generator.get_uncovered_lines('nonexistent.py')
        assert lines == set()

    def test_analyze_source_file(self):
        test_content = '''
def test_func():
    pass

class TestClass:
    def test_method(self):
        pass
'''
        with patch('builtins.open', mock_open(read_data=test_content)):
            analysis = self.generator.analyze_source_file('test.py')

            assert len(analysis['functions']) == 1
            assert analysis['functions'][0]['name'] == 'test_func'
            assert len(analysis['classes']) == 1
            assert analysis['classes'][0]['name'] == 'TestClass'

    def test_generate_test_for_function_no_args(self):
        func_info = {'name': 'test_func', 'args': []}
        test_code = self.generator.generate_test_for_function(func_info, 'test_module')

        assert 'def test_test_func_executes():' in test_code
        assert 'from test_module import test_func' in test_code
        assert 'result = test_func()' in test_code

    def test_generate_test_for_function_with_args(self):
        func_info = {'name': 'calc', 'args': ['a', 'b']}
        test_code = self.generator.generate_test_for_function(func_info, 'calculator')

        assert 'result = calc(None, None)' in test_code

    def test_generate_test_for_class(self):
        class_info = {
            'name': 'TestClass',
            'methods': [
                {'name': 'method1', 'args': ['self']},
                {'name': '_private', 'args': ['self']}
            ]
        }
        test_code = self.generator.generate_test_for_class(class_info, 'test_module')

        assert 'def test_TestClass_instantiation():' in test_code
        assert 'def test_TestClass_method1_method():' in test_code
        assert '_private' not in test_code  # Private methods skipped

    def test_generate_test_file(self):
        with patch.object(self.generator, 'analyze_source_file') as mock_analyze:
            mock_analyze.return_value = {
                'functions': [{'name': 'func1', 'args': []}],
                'classes': []
            }

            test_content = self.generator.generate_test_file('module.py')

            assert '#!/usr/bin/env python3' in test_content
            assert 'def test_module_loads():' in test_content
            assert 'import module' in test_content

    def test_validate_syntax_valid(self):
        valid_code = "def test(): pass"
        assert self.generator.validate_syntax(valid_code) == True

    def test_validate_syntax_invalid(self):
        invalid_code = "def test() pass"  # Missing colon
        assert self.generator.validate_syntax(invalid_code) == False

    @patch.object(SmartTestGenerator, 'generate_test_file')
    @patch.object(SmartTestGenerator, 'validate_syntax')
    def test_generate_tests_for_file_success(self, mock_validate, mock_generate):
        mock_generate.return_value = "test code"
        mock_validate.return_value = True

        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / 'tests'
            output_dir.mkdir()

            result = self.generator.generate_tests_for_file(
                'module.py', str(output_dir)
            )

            assert result == True
            assert (output_dir / 'test_module_real.py').exists()

    @patch.object(SmartTestGenerator, 'generate_test_file')
    @patch.object(SmartTestGenerator, 'validate_syntax')
    def test_generate_tests_for_file_syntax_error(self, mock_validate, mock_generate):
        mock_generate.return_value = "invalid code"
        mock_validate.return_value = False

        result = self.generator.generate_tests_for_file('module.py', 'tests')
        assert result == False

    @patch.object(SmartTestGenerator, 'generate_test_file')
    def test_generate_tests_for_file_exception(self, mock_generate):
        mock_generate.side_effect = Exception("Error")

        result = self.generator.generate_tests_for_file('module.py', 'tests')
        assert result == False

if __name__ == "__main__":
    pytest.main([__file__, "-v"])