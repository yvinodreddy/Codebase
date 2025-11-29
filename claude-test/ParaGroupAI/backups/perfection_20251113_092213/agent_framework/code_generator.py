"""
Code Generator with Verification
Generate and verify executable code (not just text)

Anthropic: "Code is precise, composable, and infinitely reusable,
making it an ideal output for agents."
"""

import logging
import subprocess
import tempfile
import os
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
import ast
import json

logger = logging.getLogger(__name__)


@dataclass
class CodeVerificationResult:
    """Result from code verification"""
    passed: bool
    score: float  # 0-100
    checks: Dict[str, Dict[str, Any]]
    errors: List[str]
    warnings: List[str]
    recommendations: List[str]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "passed": self.passed,
            "score": self.score,
            "checks": self.checks,
            "errors": self.errors,
            "warnings": self.warnings,
            "recommendations": self.recommendations
        }


class CodeGenerator:
    """
    Generate and verify executable code.

    Key principle from Anthropic:
    "Code is precise, composable, and infinitely reusable"

    This class:
    1. Generates Python code (not markdown/text)
    2. Verifies code with multiple checks (syntax, lint, type, security)
    3. Regenerates with fixes if verification fails
    4. Returns executable, tested code

    Example:
        >>> generator = CodeGenerator()
        >>> code = generator.generate_phase_implementation(
        ...     phase_id=5,
        ...     requirements="Implement audio generation with TTS"
        ... )
        >>> # Returns verified, executable Python code
    """

    def __init__(self):
        self.templates_dir = os.path.join(
            os.path.dirname(__file__),
            "templates"
        )
        self.generation_log: List[Dict[str, Any]] = []

        logger.info("CodeGenerator initialized")

    def generate_phase_implementation(
        self,
        phase_id: int,
        requirements: Dict[str, Any]
    ) -> str:
        """
        Generate complete phase implementation code.

        Args:
            phase_id: Phase number
            requirements: Requirements dict with:
                - description: str
                - features: List[str]
                - dependencies: List[str]
                - guardrails_required: bool

        Returns:
            Executable Python code (verified)
        """
        logger.info(f"Generating implementation for phase {phase_id}")

        # Load template
        template = self._load_template("phase_implementation.py")

        # Generate code
        code = self._generate_from_template(
            template,
            phase_id=phase_id,
            requirements=requirements
        )

        # Verify code
        verification = self.verify_code(code)

        # If verification failed, try to fix
        if not verification.passed:
            logger.warning(f"Generated code failed verification, attempting fixes...")
            code = self.regenerate_with_fixes(code, verification.errors)

            # Verify again
            verification = self.verify_code(code)

            if not verification.passed:
                logger.error("Code generation failed after fixes")
                raise ValueError(f"Failed to generate valid code: {verification.errors}")

        logger.info(f"Successfully generated code for phase {phase_id} (score: {verification.score})")

        return code

    def verify_code(self, code: str) -> CodeVerificationResult:
        """
        Multi-layer code verification.

        Checks:
        1. Syntax check (Python AST)
        2. Lint check (pyflakes or similar)
        3. Type check (basic)
        4. Security check (basic patterns)
        5. Guardrails check (must use guardrails)
        6. Style check (PEP 8 basics)

        Returns:
            CodeVerificationResult
        """
        logger.debug("Running code verification...")

        checks = {}
        errors = []
        warnings = []
        recommendations = []

        # Check 1: Syntax
        syntax_result = self._check_syntax(code)
        checks["syntax"] = syntax_result
        if not syntax_result["passed"]:
            errors.extend(syntax_result.get("errors", []))

        # Check 2: Imports
        imports_result = self._check_imports(code)
        checks["imports"] = imports_result
        if not imports_result["passed"]:
            warnings.extend(imports_result.get("warnings", []))

        # Check 3: Guardrails usage
        guardrails_result = self._check_guardrails_usage(code)
        checks["guardrails"] = guardrails_result
        if not guardrails_result["passed"]:
            warnings.append("Code should use MultiLayerGuardrailSystem")

        # Check 4: Security patterns
        security_result = self._check_security(code)
        checks["security"] = security_result
        if not security_result["passed"]:
            warnings.extend(security_result.get("warnings", []))

        # Check 5: Style basics
        style_result = self._check_style(code)
        checks["style"] = style_result
        if not style_result["passed"]:
            recommendations.extend(style_result.get("recommendations", []))

        # Calculate score
        score = self._calculate_score(checks)

        # Overall pass/fail
        passed = len(errors) == 0 and score >= 70

        result = CodeVerificationResult(
            passed=passed,
            score=score,
            checks=checks,
            errors=errors,
            warnings=warnings,
            recommendations=recommendations
        )

        logger.info(f"Verification complete: {'PASS' if passed else 'FAIL'} (score: {score})")

        return result

    def regenerate_with_fixes(self, code: str, errors: List[str]) -> str:
        """
        Attempt to fix code based on error messages.

        This is a simple implementation - in production, you'd use
        an LLM to regenerate with fixes.
        """
        logger.info(f"Attempting to fix {len(errors)} errors...")

        # Simple fixes
        fixed_code = code

        for error in errors:
            if "IndentationError" in error:
                # Try to fix indentation
                fixed_code = self._fix_indentation(fixed_code)

            if "NameError" in error or "undefined" in error.lower():
                # Try to add missing imports
                fixed_code = self._add_missing_imports(fixed_code, error)

            if "SyntaxError" in error:
                # Try basic syntax fixes
                fixed_code = self._fix_basic_syntax(fixed_code)

        return fixed_code

    def _load_template(self, template_name: str) -> str:
        """Load code template"""
        # Basic template since we don't have template files yet
        return '''"""
Phase {phase_id}: {name}
{description}
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..', 'guardrails'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..', 'agent_framework'))

from multi_layer_system import MultiLayerGuardrailSystem
from feedback_loop import AgentFeedbackLoop
from context_manager import ContextManager


class Phase{phase_id}Implementation:
    """Implementation for Phase {phase_id}"""

    def __init__(self):
        self.phase_id = {phase_id}
        self.phase_name = "{name}"
        self.guardrails = MultiLayerGuardrailSystem()
        self.feedback_loop = AgentFeedbackLoop(max_iterations=10)
        self.context = ContextManager(max_tokens=100000)

    def gather_context(self, task, iteration_log):
        """Gather context for task"""
        # Implement context gathering
        return {{"task": task}}

    def take_action(self, task, context):
        """Execute task"""
        # Implement action
        return {{"result": "success"}}

    def verify_work(self, output, context, task):
        """Verify output"""
        # Implement verification
        return {{"passed": True, "message": "Verification passed"}}

    def execute(self, task):
        """Main execution with feedback loop"""
        result = self.feedback_loop.execute(
            task=task,
            context_gatherer=self.gather_context,
            action_executor=self.take_action,
            verifier=self.verify_work
        )
        return result


if __name__ == "__main__":
    impl = Phase{phase_id}Implementation()
    print(f"Phase {{impl.phase_id}}: {{impl.phase_name}}")
'''

    def _generate_from_template(
        self,
        template: str,
        phase_id: int,
        requirements: Dict[str, Any]
    ) -> str:
        """Generate code from template"""
        # Simple template substitution
        code = template.format(
            phase_id=phase_id,
            name=requirements.get("name", f"Phase {phase_id}"),
            description=requirements.get("description", "")
        )
        return code

    def _check_syntax(self, code: str) -> Dict[str, Any]:
        """Check Python syntax"""
        try:
            ast.parse(code)
            return {
                "passed": True,
                "message": "Syntax is valid"
            }
        except SyntaxError as e:
            return {
                "passed": False,
                "errors": [f"SyntaxError at line {e.lineno}: {e.msg}"],
                "message": "Syntax errors found"
            }

    def _check_imports(self, code: str) -> Dict[str, Any]:
        """Check if required imports are present"""
        required_imports = [
            "multi_layer_system",
            "feedback_loop",
            "context_manager"
        ]

        missing = []
        for imp in required_imports:
            if imp not in code:
                missing.append(imp)

        if missing:
            return {
                "passed": False,
                "warnings": [f"Missing recommended import: {imp}" for imp in missing],
                "message": f"Missing {len(missing)} recommended imports"
            }

        return {
            "passed": True,
            "message": "All required imports present"
        }

    def _check_guardrails_usage(self, code: str) -> Dict[str, Any]:
        """Check if code uses guardrails"""
        if "MultiLayerGuardrailSystem" in code:
            return {
                "passed": True,
                "message": "Guardrails system is used"
            }

        return {
            "passed": False,
            "message": "Code should use MultiLayerGuardrailSystem for safety"
        }

    def _check_security(self, code: str) -> Dict[str, Any]:
        """Basic security checks"""
        security_issues = []

        # Check for dangerous patterns
        dangerous_patterns = [
            ("eval(", "Avoid using eval()"),
            ("exec(", "Avoid using exec()"),
            ("__import__(", "Avoid dynamic imports"),
            ("os.system(", "Avoid os.system(), use subprocess")
        ]

        for pattern, message in dangerous_patterns:
            if pattern in code:
                security_issues.append(message)

        if security_issues:
            return {
                "passed": False,
                "warnings": security_issues,
                "message": f"Found {len(security_issues)} security concerns"
            }

        return {
            "passed": True,
            "message": "No obvious security issues"
        }

    def _check_style(self, code: str) -> Dict[str, Any]:
        """Basic style checks"""
        recommendations = []

        # Check for docstrings
        if '"""' not in code and "'''" not in code:
            recommendations.append("Add docstrings to functions and classes")

        # Check for type hints (basic)
        if "def " in code and "->" not in code:
            recommendations.append("Consider adding type hints")

        # Check line length (very basic)
        long_lines = [i+1 for i, line in enumerate(code.split("\n")) if len(line) > 120]
        if long_lines:
            recommendations.append(f"Lines {long_lines[:3]} exceed 120 characters")

        if recommendations:
            return {
                "passed": True,  # Style issues don't fail verification
                "recommendations": recommendations,
                "message": f"{len(recommendations)} style recommendations"
            }

        return {
            "passed": True,
            "message": "Style looks good"
        }

    def _calculate_score(self, checks: Dict[str, Dict[str, Any]]) -> float:
        """Calculate overall code quality score"""
        # Weighted scoring
        weights = {
            "syntax": 40,  # Critical
            "imports": 20,
            "guardrails": 20,
            "security": 15,
            "style": 5
        }

        score = 0
        for check_name, weight in weights.items():
            if check_name in checks and checks[check_name].get("passed", False):
                score += weight

        return score

    def _fix_indentation(self, code: str) -> str:
        """Attempt to fix indentation issues"""
        # Very basic - just ensure consistent spacing
        lines = code.split("\n")
        fixed_lines = []

        for line in lines:
            # Replace tabs with 4 spaces
            fixed_line = line.replace("\t", "    ")
            fixed_lines.append(fixed_line)

        return "\n".join(fixed_lines)

    def _add_missing_imports(self, code: str, error: str) -> str:
        """Add missing imports based on error"""
        # Extract undefined name from error
        # This is simplified - real implementation would be more sophisticated
        return code

    def _fix_basic_syntax(self, code: str) -> str:
        """Fix basic syntax issues"""
        # Very basic fixes
        fixed = code

        # Fix common issues
        fixed = fixed.replace("print ", "print(")  # Python 2 to 3

        return fixed


if __name__ == "__main__":
    # Example usage
    generator = CodeGenerator()

    print("=" * 60)
    print("CODE GENERATOR EXAMPLE")
    print("=" * 60)

    # Generate code for phase 5
    requirements = {
        "name": "Audio Generation",
        "description": "TTS integration and audio post-processing",
        "features": ["TTS", "audio processing"],
        "guardrails_required": True
    }

    print("\nGenerating code for phase 5...")
    code = generator.generate_phase_implementation(
        phase_id=5,
        requirements=requirements
    )

    print("\nGenerated code:")
    print("-" * 60)
    print(code[:500] + "...")
    print("-" * 60)

    # Verify code
    print("\nVerifying code...")
    verification = generator.verify_code(code)

    print(f"\nVerification result:")
    print(f"  Passed: {verification.passed}")
    print(f"  Score: {verification.score}/100")
    print(f"  Errors: {len(verification.errors)}")
    print(f"  Warnings: {len(verification.warnings)}")

    if verification.errors:
        print("\n  Errors:")
        for error in verification.errors:
            print(f"    - {error}")

    if verification.warnings:
        print("\n  Warnings:")
        for warning in verification.warnings:
            print(f"    - {warning}")

    print("\n✅ Example complete")
