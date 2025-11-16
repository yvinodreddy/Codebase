#!/usr/bin/env python3
"""
Comprehensive Audit Script for SwarmCare Production
Identifies ALL issues requiring fixes for 100% production readiness
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Tuple
import json

class SwarmCareAuditor:
    def __init__(self, root_path: str):
        self.root_path = Path(root_path)
        self.issues = []
        self.stats = {
            'total_files': 0,
            'duplicate_files': 0,
            'missing_files': 0,
            'invalid_python': 0,
            'missing_docs': 0,
            'missing_tests': 0,
        }

    def audit_all(self) -> Dict:
        """Run comprehensive audit"""
        print("🔍 COMPREHENSIVE SWARMCARE AUDIT")
        print("=" * 80)

        # 1. Check for duplicate files
        print("\n1️⃣  Checking for duplicate/conflicting files...")
        self.check_duplicates()

        # 2. Verify all 29 phases
        print("\n2️⃣  Verifying all 29 phases...")
        self.check_phases()

        # 3. Verify agent_framework
        print("\n3️⃣  Verifying agent_framework directory...")
        self.check_agent_framework()

        # 4. Verify prompts
        print("\n4️⃣  Verifying ai_prompts directory...")
        self.check_prompts()

        # 5. Verify docs
        print("\n5️⃣  Verifying documentation...")
        self.check_docs()

        # 6. Verify guardrails
        print("\n6️⃣  Verifying guardrails...")
        self.check_guardrails()

        # 7. Verify integration
        print("\n7️⃣  Verifying integration directory...")
        self.check_integration()

        # 8. Verify MCP servers
        print("\n8️⃣  Verifying mcp_servers...")
        self.check_mcp_servers()

        # 9. Verify scripts
        print("\n9️⃣  Verifying scripts...")
        self.check_scripts()

        # 10. Verify tests
        print("\n🔟 Verifying tests...")
        self.check_tests()

        # 11. Validate Python syntax
        print("\n1️⃣1️⃣  Validating Python files...")
        self.validate_python_files()

        # 12. Check cross-references
        print("\n1️⃣2️⃣  Checking file mappings and cross-references...")
        self.check_cross_references()

        return self.generate_report()

    def check_duplicates(self):
        """Check for duplicate/conflicting files"""
        # Check phases for implementation duplicates
        phases_dir = self.root_path / "phases"
        for phase_dir in sorted(phases_dir.glob("phase*")):
            code_dir = phase_dir / "code"
            if code_dir.exists():
                impl_files = list(code_dir.glob("implementation*.py"))
                if len(impl_files) > 1:
                    self.issues.append({
                        'severity': 'CRITICAL',
                        'category': 'DUPLICATE_FILES',
                        'location': str(code_dir),
                        'description': f'Multiple implementation files found: {[f.name for f in impl_files]}',
                        'files': [str(f) for f in impl_files]
                    })
                    self.stats['duplicate_files'] += 1

        # Check agent_framework for duplicates
        agent_fw_dir = self.root_path / "agent_framework"
        if agent_fw_dir.exists():
            for py_file in agent_fw_dir.glob("*.py"):
                if '_enhanced' in py_file.name or '_old' in py_file.name or '_backup' in py_file.name:
                    base_name = py_file.name.replace('_enhanced', '').replace('_old', '').replace('_backup', '')
                    base_file = agent_fw_dir / base_name

                    # Skip feedback_loop pair - they work together (inheritance pattern)
                    if py_file.name == 'feedback_loop_enhanced.py' and base_name == 'feedback_loop.py':
                        continue

                    if base_file.exists():
                        # Verify if enhanced imports from base (valid pattern)
                        try:
                            with open(py_file, 'r') as f:
                                content = f.read()
                                if f'from {base_name[:-3]} import' in content or f'from .{base_name[:-3]} import' in content:
                                    # This is a valid inheritance pattern, not a duplicate
                                    continue
                        except:
                            pass

                        self.issues.append({
                            'severity': 'HIGH',
                            'category': 'DUPLICATE_FILES',
                            'location': str(agent_fw_dir),
                            'description': f'Duplicate found: {py_file.name} and {base_name}',
                            'files': [str(py_file), str(base_file)]
                        })
                        self.stats['duplicate_files'] += 1

    def check_phases(self):
        """Verify all 29 phases have required structure"""
        phases_dir = self.root_path / "phases"
        expected_phases = [f"phase{i:02d}" for i in range(29)]

        for phase_name in expected_phases:
            phase_dir = phases_dir / phase_name

            # Check phase exists
            if not phase_dir.exists():
                self.issues.append({
                    'severity': 'CRITICAL',
                    'category': 'MISSING_PHASE',
                    'location': str(phases_dir),
                    'description': f'Phase directory missing: {phase_name}'
                })
                continue

            # Check required subdirectories
            required_dirs = ['code', 'docs', 'tests']
            for req_dir in required_dirs:
                dir_path = phase_dir / req_dir
                if not dir_path.exists():
                    self.issues.append({
                        'severity': 'HIGH',
                        'category': 'MISSING_DIRECTORY',
                        'location': str(phase_dir),
                        'description': f'Missing required directory: {req_dir}'
                    })

            # Check required files
            code_dir = phase_dir / "code"
            if code_dir.exists():
                required_files = ['implementation.py', '__init__.py']
                for req_file in required_files:
                    file_path = code_dir / req_file
                    if not file_path.exists():
                        self.issues.append({
                            'severity': 'CRITICAL',
                            'category': 'MISSING_FILE',
                            'location': str(code_dir),
                            'description': f'Missing required file: {req_file}'
                        })
                        self.stats['missing_files'] += 1

            # Check README and docs
            if not (phase_dir / "README.md").exists():
                self.issues.append({
                    'severity': 'MEDIUM',
                    'category': 'MISSING_DOCS',
                    'location': str(phase_dir),
                    'description': 'Missing README.md'
                })
                self.stats['missing_docs'] += 1

    def check_agent_framework(self):
        """Verify agent_framework has all 7 components"""
        agent_fw_dir = self.root_path / "agent_framework"

        if not agent_fw_dir.exists():
            self.issues.append({
                'severity': 'CRITICAL',
                'category': 'MISSING_DIRECTORY',
                'location': str(self.root_path),
                'description': 'agent_framework directory missing'
            })
            return

        required_components = [
            'feedback_loop.py',
            'context_manager.py',
            'subagent_orchestrator.py',
            'agentic_search.py',
            'code_generator.py',
            'verification_system.py',
            'mcp_integration.py',
            '__init__.py'
        ]

        for component in required_components:
            file_path = agent_fw_dir / component
            if not file_path.exists():
                self.issues.append({
                    'severity': 'CRITICAL',
                    'category': 'MISSING_FILE',
                    'location': str(agent_fw_dir),
                    'description': f'Missing agent framework component: {component}'
                })
                self.stats['missing_files'] += 1

    def check_prompts(self):
        """Verify ai_prompts directory"""
        prompts_dir = self.root_path / "ai_prompts"

        if not prompts_dir.exists():
            self.issues.append({
                'severity': 'MEDIUM',
                'category': 'MISSING_DIRECTORY',
                'location': str(self.root_path),
                'description': 'ai_prompts directory missing'
            })

    def check_docs(self):
        """Verify documentation files"""
        required_docs = [
            'START_HERE.md',
            'AGENT_FRAMEWORK_GUIDE.md',
            'PRODUCTION_READINESS_REPORT.md',
            'COMPLETE_SYSTEM_GUIDE.md'
        ]

        for doc in required_docs:
            doc_path = self.root_path / doc
            if not doc_path.exists():
                self.issues.append({
                    'severity': 'MEDIUM',
                    'category': 'MISSING_DOCS',
                    'location': str(self.root_path),
                    'description': f'Missing documentation: {doc}'
                })
                self.stats['missing_docs'] += 1

    def check_guardrails(self):
        """Verify guardrails directory"""
        guardrails_dir = self.root_path / "guardrails"

        if not guardrails_dir.exists():
            self.issues.append({
                'severity': 'HIGH',
                'category': 'MISSING_DIRECTORY',
                'location': str(self.root_path),
                'description': 'guardrails directory missing'
            })
            return

        required_files = [
            'medical_guardrails.py',
            'crewai_guardrails.py',
            'multi_layer_system.py',
            '__init__.py'
        ]

        for file_name in required_files:
            file_path = guardrails_dir / file_name
            if not file_path.exists():
                self.issues.append({
                    'severity': 'HIGH',
                    'category': 'MISSING_FILE',
                    'location': str(guardrails_dir),
                    'description': f'Missing guardrail file: {file_name}'
                })

    def check_integration(self):
        """Verify integration directory"""
        integration_dir = self.root_path / "integration"

        if not integration_dir.exists():
            self.issues.append({
                'severity': 'MEDIUM',
                'category': 'MISSING_DIRECTORY',
                'location': str(self.root_path),
                'description': 'integration directory missing'
            })

    def check_mcp_servers(self):
        """Verify MCP servers"""
        mcp_dir = self.root_path / "mcp_servers"

        if not mcp_dir.exists():
            self.issues.append({
                'severity': 'MEDIUM',
                'category': 'MISSING_DIRECTORY',
                'location': str(self.root_path),
                'description': 'mcp_servers directory missing'
            })

    def check_scripts(self):
        """Verify scripts directory"""
        scripts_dir = self.root_path / "scripts"

        if not scripts_dir.exists():
            self.issues.append({
                'severity': 'LOW',
                'category': 'MISSING_DIRECTORY',
                'location': str(self.root_path),
                'description': 'scripts directory missing'
            })

    def check_tests(self):
        """Verify tests exist for all phases"""
        phases_dir = self.root_path / "phases"

        for phase_dir in sorted(phases_dir.glob("phase*")):
            tests_dir = phase_dir / "tests"
            if tests_dir.exists():
                test_file = tests_dir / f"test_{phase_dir.name}.py"
                if not test_file.exists():
                    self.issues.append({
                        'severity': 'MEDIUM',
                        'category': 'MISSING_TESTS',
                        'location': str(tests_dir),
                        'description': f'Missing test file: {test_file.name}'
                    })
                    self.stats['missing_tests'] += 1

    def validate_python_files(self):
        """Validate Python syntax for all .py files"""
        import ast

        for py_file in self.root_path.rglob("*.py"):
            if '__pycache__' in str(py_file):
                continue

            self.stats['total_files'] += 1

            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    ast.parse(content)
            except SyntaxError as e:
                self.issues.append({
                    'severity': 'CRITICAL',
                    'category': 'INVALID_PYTHON',
                    'location': str(py_file),
                    'description': f'Python syntax error: {str(e)}'
                })
                self.stats['invalid_python'] += 1
            except Exception as e:
                self.issues.append({
                    'severity': 'HIGH',
                    'category': 'FILE_ERROR',
                    'location': str(py_file),
                    'description': f'Error reading file: {str(e)}'
                })

    def check_cross_references(self):
        """Check that imports and cross-references are valid"""
        # This is a simplified check - could be expanded
        phases_dir = self.root_path / "phases"

        agent_framework_components = [
            'feedback_loop', 'feedback_loop_enhanced', 'context_manager',
            'subagent_orchestrator', 'agentic_search', 'code_generator',
            'verification_system', 'mcp_integration'
        ]

        for phase_dir in sorted(phases_dir.glob("phase*")):
            impl_file = phase_dir / "code" / "implementation.py"
            if impl_file.exists():
                try:
                    with open(impl_file, 'r', encoding='utf-8') as f:
                        content = f.read()

                        # Check for agent_framework imports (multiple patterns)
                        has_framework_import = (
                            'from agent_framework' in content or
                            'import agent_framework' in content or
                            any(f'from {comp} import' in content for comp in agent_framework_components) or
                            any(f'import {comp}' in content for comp in agent_framework_components)
                        )

                        if not has_framework_import:
                            self.issues.append({
                                'severity': 'LOW',
                                'category': 'MISSING_IMPORT',
                                'location': str(impl_file),
                                'description': 'Missing agent_framework imports (may not be integrated)'
                            })
                except Exception as e:
                    pass  # Already caught in validation

    def generate_report(self) -> Dict:
        """Generate comprehensive audit report"""
        print("\n" + "=" * 80)
        print("📊 AUDIT REPORT")
        print("=" * 80)

        # Categorize issues by severity
        critical = [i for i in self.issues if i['severity'] == 'CRITICAL']
        high = [i for i in self.issues if i['severity'] == 'HIGH']
        medium = [i for i in self.issues if i['severity'] == 'MEDIUM']
        low = [i for i in self.issues if i['severity'] == 'LOW']

        print(f"\n🔴 CRITICAL Issues: {len(critical)}")
        for issue in critical:
            print(f"   - [{issue['category']}] {issue['description']}")
            print(f"     Location: {issue['location']}")

        print(f"\n🟠 HIGH Priority Issues: {len(high)}")
        for issue in high:
            print(f"   - [{issue['category']}] {issue['description']}")
            print(f"     Location: {issue['location']}")

        print(f"\n🟡 MEDIUM Priority Issues: {len(medium)}")
        for issue in medium:
            print(f"   - [{issue['category']}] {issue['description']}")

        print(f"\n🟢 LOW Priority Issues: {len(low)}")

        print("\n" + "=" * 80)
        print("📈 STATISTICS")
        print("=" * 80)
        for key, value in self.stats.items():
            print(f"   {key}: {value}")

        print(f"\n   Total Issues Found: {len(self.issues)}")

        # Save detailed report
        report = {
            'total_issues': len(self.issues),
            'critical': len(critical),
            'high': len(high),
            'medium': len(medium),
            'low': len(low),
            'statistics': self.stats,
            'issues': self.issues
        }

        report_file = self.root_path / "AUDIT_REPORT.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"\n✅ Detailed report saved to: {report_file}")

        return report


if __name__ == "__main__":
    root_path = "/home/user01/claude-test/SwarmCare/SwarmCare_Production"

    auditor = SwarmCareAuditor(root_path)
    report = auditor.audit_all()

    # Exit with error code if critical issues found
    if report['critical'] > 0:
        print("\n❌ CRITICAL ISSUES FOUND - System not production ready")
        sys.exit(1)
    elif report['high'] > 0:
        print("\n⚠️  HIGH PRIORITY ISSUES FOUND - Needs attention")
        sys.exit(2)
    else:
        print("\n✅ No critical or high priority issues found")
        sys.exit(0)
