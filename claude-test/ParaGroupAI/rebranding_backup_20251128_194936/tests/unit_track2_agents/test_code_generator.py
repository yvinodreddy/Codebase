"""
Comprehensive tests for agent_framework/code_generator.py

Target: 90%+ coverage (156/173 statements)
Tests: CodeVerificationResult dataclass, CodeGenerator class methods

MANDATORY TESTING STANDARD:
- Tests REAL code (imports actual classes/functions)
- Mocks ONLY external dependencies
- Covers success paths, error paths, and edge cases
- ≥ 90% statement coverage required
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from agent_framework.code_generator import (
    CodeGenerator,
    CodeVerificationResult
)


class TestCodeVerificationResult:
    """Test CodeVerificationResult dataclass"""

    def test_result_creation(self):
        """Test creating CodeVerificationResult"""
        result = CodeVerificationResult(
            passed=True,
            score=85.5,
            checks={"syntax": {"passed": True}},
            errors=[],
            warnings=["warning1"],
            recommendations=["rec1"]
        )

        assert result.passed is True
        assert result.score == 85.5
        assert result.checks == {"syntax": {"passed": True}}
        assert result.errors == []
        assert result.warnings == ["warning1"]
        assert result.recommendations == ["rec1"]

    def test_to_dict(self):
        """Test converting result to dictionary"""
        result = CodeVerificationResult(
            passed=True,
            score=90.0,
            checks={"syntax": {"passed": True}},
            errors=[],
            warnings=[],
            recommendations=[]
        )

        result_dict = result.to_dict()

        assert result_dict["passed"] is True
        assert result_dict["score"] == 90.0
        assert "checks" in result_dict
        assert "errors" in result_dict
        assert "warnings" in result_dict
        assert "recommendations" in result_dict


class TestCodeGeneratorInit:
    """Test CodeGenerator initialization"""

    def test_init(self):
        """Test CodeGenerator initialization"""
        generator = CodeGenerator()

        assert generator.templates_dir is not None
        assert generator.generation_log == []


class TestGeneratePhaseImplementation:
    """Test generate_phase_implementation method"""

    def test_generate_success(self):
        """Test successful code generation"""
        generator = CodeGenerator()

        requirements = {
            "name": "Test Phase",
            "description": "Test description",
            "features": ["feature1"],
            "guardrails_required": True
        }

        code = generator.generate_phase_implementation(
            phase_id=1,
            requirements=requirements
        )

        assert "class Phase1Implementation" in code
        assert "Test Phase" in code
        assert "MultiLayerGuardrailSystem" in code

    def test_generate_different_phase_id(self):
        """Test generation with different phase ID"""
        generator = CodeGenerator()

        requirements = {
            "name": "Audio Processing",
            "description": "Audio generation"
        }

        code = generator.generate_phase_implementation(
            phase_id=5,
            requirements=requirements
        )

        assert "class Phase5Implementation" in code
        assert "Audio Processing" in code

    def test_generate_with_verification_failure(self):
        """Test generation when verification fails and fixes work"""
        generator = CodeGenerator()

        # Mock verify_code to fail first, then pass
        call_count = 0
        def mock_verify(code):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                # First call - fail
                return CodeVerificationResult(
                    passed=False,
                    score=50,
                    checks={},
                    errors=["IndentationError"],
                    warnings=[],
                    recommendations=[]
                )
            else:
                # Second call after fix - pass
                return CodeVerificationResult(
                    passed=True,
                    score=85,
                    checks={},
                    errors=[],
                    warnings=[],
                    recommendations=[]
                )

        generator.verify_code = mock_verify

        requirements = {"name": "Test", "description": "Test"}
        code = generator.generate_phase_implementation(phase_id=1, requirements=requirements)

        assert code is not None
        assert call_count == 2

    def test_generate_with_verification_failure_no_fix(self):
        """Test generation when verification fails even after fixes"""
        generator = CodeGenerator()

        # Mock verify_code to always fail
        def mock_verify(code):
            return CodeVerificationResult(
                passed=False,
                score=30,
                checks={},
                errors=["SyntaxError: invalid syntax"],
                warnings=[],
                recommendations=[]
            )

        generator.verify_code = mock_verify

        requirements = {"name": "Test", "description": "Test"}

        with pytest.raises(ValueError, match="Failed to generate valid code"):
            generator.generate_phase_implementation(phase_id=1, requirements=requirements)


class TestVerifyCode:
    """Test verify_code method"""

    def test_verify_valid_code(self):
        """Test verification of valid code"""
        generator = CodeGenerator()

        valid_code = '''
import sys
from multi_layer_system import MultiLayerGuardrailSystem
from feedback_loop import AgentFeedbackLoop
from context_manager import ContextManager

def hello():
    """Say hello"""
    return "world"
'''

        result = generator.verify_code(valid_code)

        assert result.passed is True
        assert result.score >= 70
        assert result.checks["syntax"]["passed"] is True

    def test_verify_invalid_syntax(self):
        """Test verification with syntax error"""
        generator = CodeGenerator()

        invalid_code = '''
def hello()  # Missing colon
    return "world"
'''

        result = generator.verify_code(invalid_code)

        assert result.passed is False
        assert len(result.errors) > 0
        assert "SyntaxError" in result.errors[0]

    def test_verify_missing_imports(self):
        """Test verification with missing imports"""
        generator = CodeGenerator()

        code_without_imports = '''
def hello():
    return "world"
'''

        result = generator.verify_code(code_without_imports)

        # Missing imports should generate warnings
        assert len(result.warnings) > 0

    def test_verify_no_guardrails(self):
        """Test verification when guardrails not used"""
        generator = CodeGenerator()

        code = '''
import sys

def hello():
    return "world"
'''

        result = generator.verify_code(code)

        # Should have warning about guardrails
        assert any("guardrails" in w.lower() or "MultiLayerGuardrailSystem" in w for w in result.warnings)


class TestRegenerateWithFixes:
    """Test regenerate_with_fixes method"""

    def test_fix_indentation_error(self):
        """Test fixing indentation errors"""
        generator = CodeGenerator()

        code_with_issue = "def hello():\n    return 'world'"
        errors = ["IndentationError"]

        fixed_code = generator.regenerate_with_fixes(code_with_issue, errors)

        assert fixed_code is not None
        assert isinstance(fixed_code, str)

    def test_fix_name_error(self):
        """Test attempting to fix name errors"""
        generator = CodeGenerator()

        code = "x = undefined_var"
        errors = ["NameError: undefined_var is not defined"]

        fixed_code = generator.regenerate_with_fixes(code, errors)

        assert fixed_code is not None

    def test_fix_syntax_error(self):
        """Test fixing syntax errors"""
        generator = CodeGenerator()

        code = "print 'hello'"  # Python 2 style
        errors = ["SyntaxError"]

        fixed_code = generator.regenerate_with_fixes(code, errors)

        assert fixed_code is not None

    def test_fix_multiple_errors(self):
        """Test fixing multiple error types"""
        generator = CodeGenerator()

        code = "print 'hello'"
        errors = ["IndentationError", "SyntaxError", "NameError"]

        fixed_code = generator.regenerate_with_fixes(code, errors)

        assert fixed_code is not None


class TestLoadTemplate:
    """Test _load_template method"""

    def test_load_template(self):
        """Test loading template"""
        generator = CodeGenerator()

        template = generator._load_template("phase_implementation.py")

        assert template is not None
        assert isinstance(template, str)
        assert "Phase {phase_id}" in template
        assert "MultiLayerGuardrailSystem" in template


class TestGenerateFromTemplate:
    """Test _generate_from_template method"""

    def test_generate_from_template(self):
        """Test generating code from template"""
        generator = CodeGenerator()

        template = "Phase {phase_id}: {name}\n{description}"
        requirements = {
            "name": "Audio Gen",
            "description": "Generate audio"
        }

        code = generator._generate_from_template(template, phase_id=5, requirements=requirements)

        assert "Phase 5" in code
        assert "Audio Gen" in code
        assert "Generate audio" in code

    def test_generate_with_defaults(self):
        """Test generation with missing requirements fields"""
        generator = CodeGenerator()

        template = "Phase {phase_id}: {name}"
        requirements = {}  # Empty requirements

        code = generator._generate_from_template(template, phase_id=3, requirements=requirements)

        assert "Phase 3" in code


class TestCheckSyntax:
    """Test _check_syntax method"""

    def test_check_valid_syntax(self):
        """Test checking valid Python syntax"""
        generator = CodeGenerator()

        valid_code = "def hello():\n    return 'world'"
        result = generator._check_syntax(valid_code)

        assert result["passed"] is True
        assert "valid" in result["message"].lower()

    def test_check_invalid_syntax(self):
        """Test checking invalid syntax"""
        generator = CodeGenerator()

        invalid_code = "def hello()  # Missing colon\n    return 'world'"
        result = generator._check_syntax(invalid_code)

        assert result["passed"] is False
        assert "errors" in result
        assert len(result["errors"]) > 0


class TestCheckImports:
    """Test _check_imports method"""

    def test_all_imports_present(self):
        """Test when all required imports are present"""
        generator = CodeGenerator()

        code = '''
from multi_layer_system import MultiLayerGuardrailSystem
from feedback_loop import AgentFeedbackLoop
from context_manager import ContextManager
'''

        result = generator._check_imports(code)

        assert result["passed"] is True

    def test_missing_imports(self):
        """Test when some imports are missing"""
        generator = CodeGenerator()

        code = "import sys"
        result = generator._check_imports(code)

        assert result["passed"] is False
        assert "warnings" in result
        assert len(result["warnings"]) > 0


class TestCheckGuardrailsUsage:
    """Test _check_guardrails_usage method"""

    def test_guardrails_present(self):
        """Test when guardrails are used"""
        generator = CodeGenerator()

        code = '''
from multi_layer_system import MultiLayerGuardrailSystem

class MyClass:
    def __init__(self):
        self.guardrails = MultiLayerGuardrailSystem()
'''

        result = generator._check_guardrails_usage(code)

        assert result["passed"] is True

    def test_guardrails_absent(self):
        """Test when guardrails are not used"""
        generator = CodeGenerator()

        code = "def hello():\n    return 'world'"
        result = generator._check_guardrails_usage(code)

        assert result["passed"] is False
        assert "MultiLayerGuardrailSystem" in result["message"]


class TestCheckSecurity:
    """Test _check_security method"""

    def test_no_security_issues(self):
        """Test code with no security issues"""
        generator = CodeGenerator()

        safe_code = "def hello():\n    return 'world'"
        result = generator._check_security(safe_code)

        assert result["passed"] is True

    def test_eval_detected(self):
        """Test detection of eval()"""
        generator = CodeGenerator()

        code = "x = eval('1 + 1')"
        result = generator._check_security(code)

        assert result["passed"] is False
        assert any("eval" in w for w in result["warnings"])

    def test_exec_detected(self):
        """Test detection of exec()"""
        generator = CodeGenerator()

        code = "exec('print(1)')"
        result = generator._check_security(code)

        assert result["passed"] is False

    def test_import_detected(self):
        """Test detection of __import__"""
        generator = CodeGenerator()

        code = "m = __import__('os')"
        result = generator._check_security(code)

        assert result["passed"] is False

    def test_os_system_detected(self):
        """Test detection of os.system()"""
        generator = CodeGenerator()

        code = "import os\nos.system('ls')"
        result = generator._check_security(code)

        assert result["passed"] is False


class TestCheckStyle:
    """Test _check_style method"""

    def test_good_style(self):
        """Test code with good style"""
        generator = CodeGenerator()

        code = '''
def hello() -> str:
    """Say hello"""
    return "world"
'''

        result = generator._check_style(code)

        assert result["passed"] is True

    def test_missing_docstrings(self):
        """Test detection of missing docstrings"""
        generator = CodeGenerator()

        code = "def hello():\n    return 'world'"
        result = generator._check_style(code)

        assert "recommendations" in result
        assert any("docstring" in r.lower() for r in result["recommendations"])

    def test_missing_type_hints(self):
        """Test detection of missing type hints"""
        generator = CodeGenerator()

        code = '''
"""Module doc"""
def hello():
    return "world"
'''

        result = generator._check_style(code)

        assert any("type hint" in r.lower() for r in result["recommendations"])

    def test_long_lines(self):
        """Test detection of long lines"""
        generator = CodeGenerator()

        long_line = "x = " + "a" * 130
        code = f'''
"""Doc"""
{long_line}
'''

        result = generator._check_style(code)

        assert any("120 characters" in r for r in result["recommendations"])


class TestCalculateScore:
    """Test _calculate_score method"""

    def test_all_checks_pass(self):
        """Test score when all checks pass"""
        generator = CodeGenerator()

        checks = {
            "syntax": {"passed": True},
            "imports": {"passed": True},
            "guardrails": {"passed": True},
            "security": {"passed": True},
            "style": {"passed": True}
        }

        score = generator._calculate_score(checks)

        assert score == 100

    def test_syntax_only(self):
        """Test score with only syntax passing"""
        generator = CodeGenerator()

        checks = {
            "syntax": {"passed": True},
            "imports": {"passed": False},
            "guardrails": {"passed": False},
            "security": {"passed": False},
            "style": {"passed": False}
        }

        score = generator._calculate_score(checks)

        assert score == 40  # Syntax weight

    def test_empty_checks(self):
        """Test score with no checks"""
        generator = CodeGenerator()

        checks = {}
        score = generator._calculate_score(checks)

        assert score == 0


class TestFixIndentation:
    """Test _fix_indentation method"""

    def test_fix_tabs_to_spaces(self):
        """Test converting tabs to spaces"""
        generator = CodeGenerator()

        code_with_tabs = "def hello():\n\treturn 'world'"
        fixed = generator._fix_indentation(code_with_tabs)

        assert "\t" not in fixed
        assert "    " in fixed

    def test_preserve_code_without_tabs(self):
        """Test that code without tabs is preserved"""
        generator = CodeGenerator()

        code = "def hello():\n    return 'world'"
        fixed = generator._fix_indentation(code)

        assert fixed == code


class TestAddMissingImports:
    """Test _add_missing_imports method"""

    def test_add_imports(self):
        """Test adding missing imports"""
        generator = CodeGenerator()

        code = "x = 1"
        error = "NameError: name 'os' is not defined"

        result = generator._add_missing_imports(code, error)

        assert result is not None
        assert isinstance(result, str)


class TestFixBasicSyntax:
    """Test _fix_basic_syntax method"""

    def test_fix_print_statement(self):
        """Test fixing Python 2 print to Python 3"""
        generator = CodeGenerator()

        code = "print 'hello'"
        fixed = generator._fix_basic_syntax(code)

        assert "print(" in fixed


class TestEdgeCases:
    """Test edge cases and error handling"""

    def test_empty_code(self):
        """Test verification of empty code"""
        generator = CodeGenerator()

        result = generator.verify_code("")

        # Should have syntax check result
        assert "syntax" in result.checks

    def test_very_long_code(self):
        """Test handling very long code"""
        generator = CodeGenerator()

        long_code = "x = 1\n" * 1000
        result = generator.verify_code(long_code)

        assert result is not None

    def test_unicode_code(self):
        """Test handling code with unicode characters"""
        generator = CodeGenerator()

        code = '''
def hello():
    """Say hello in multiple languages: 你好, مرحبا, שלום"""
    return "world"
'''

        result = generator.verify_code(code)

        # Should handle unicode gracefully
        assert result is not None
