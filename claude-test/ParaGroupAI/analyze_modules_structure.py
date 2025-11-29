#!/usr/bin/env python3
"""
Analyze actual structure of 16 target modules
Discovers functions, classes, methods for accurate test generation
"""

import ast
import sys
import json
from pathlib import Path
from typing import Dict, List, Any, Set

class ModuleAnalyzer:
    """Analyze Python modules using AST to discover actual structure"""

    def __init__(self):
        self.modules = [
            "fix_test_files_complete.py",
            "generate_100_percent_tests.py",
            "generate_effective_tests.py",
            "generate_real_coverage_tests.py",
            "generate_real_test_fixed.py",
            "generate_real_test_implementations.py",
            "generate_real_tests_for_module.py",
            "get_coverage_quickly.py",
            "get_live_context_metrics.py",
            "high_scale_orchestrator.py",
            "instance_id_manager.py",
            "large_scale_error_handler.py",
            "live_metrics_tracker.py",
            "master_orchestrator.py",
            "metrics_aggregator.py",
            "metrics_state_persistence.py"
        ]

    def analyze_module(self, file_path: str) -> Dict[str, Any]:
        """Analyze a single module and extract its structure"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                source = f.read()

            tree = ast.parse(source, filename=file_path)

            analysis = {
                'file': file_path,
                'functions': [],
                'classes': [],
                'imports': [],
                'has_main': False,
                'has_if_name_main': False,
                'module_docstring': ast.get_docstring(tree),
                'total_lines': len(source.splitlines())
            }

            for node in ast.walk(tree):
                # Functions
                if isinstance(node, ast.FunctionDef):
                    func_info = {
                        'name': node.name,
                        'args': [arg.arg for arg in node.args.args],
                        'lineno': node.lineno,
                        'is_async': isinstance(node, ast.AsyncFunctionDef),
                        'docstring': ast.get_docstring(node),
                        'decorators': [self._get_decorator_name(d) for d in node.decorator_list]
                    }

                    # Check if it's a method (inside a class) or standalone function
                    if self._is_method(tree, node):
                        # Will be captured in class analysis
                        pass
                    else:
                        analysis['functions'].append(func_info)
                        if node.name == 'main':
                            analysis['has_main'] = True

                # Classes
                elif isinstance(node, ast.ClassDef):
                    class_info = {
                        'name': node.name,
                        'lineno': node.lineno,
                        'docstring': ast.get_docstring(node),
                        'methods': [],
                        'bases': [self._get_base_name(b) for b in node.bases]
                    }

                    # Get methods
                    for item in node.body:
                        if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                            method_info = {
                                'name': item.name,
                                'args': [arg.arg for arg in item.args.args],
                                'lineno': item.lineno,
                                'is_async': isinstance(item, ast.AsyncFunctionDef),
                                'is_property': any(self._get_decorator_name(d) == 'property' for d in item.decorator_list),
                                'decorators': [self._get_decorator_name(d) for d in item.decorator_list]
                            }
                            class_info['methods'].append(method_info)

                    analysis['classes'].append(class_info)

                # Check for if __name__ == "__main__"
                elif isinstance(node, ast.If):
                    if self._is_name_main_check(node):
                        analysis['has_if_name_main'] = True

            return analysis

        except Exception as e:
            return {
                'file': file_path,
                'error': str(e),
                'functions': [],
                'classes': []
            }

    def _is_method(self, tree: ast.AST, func_node: ast.FunctionDef) -> bool:
        """Check if a function is a method inside a class"""
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                if func_node in node.body:
                    return True
        return False

    def _get_decorator_name(self, decorator: ast.expr) -> str:
        """Get decorator name"""
        if isinstance(decorator, ast.Name):
            return decorator.id
        elif isinstance(decorator, ast.Attribute):
            return decorator.attr
        elif isinstance(decorator, ast.Call):
            if isinstance(decorator.func, ast.Name):
                return decorator.func.id
            elif isinstance(decorator.func, ast.Attribute):
                return decorator.func.attr
        return 'unknown'

    def _get_base_name(self, base: ast.expr) -> str:
        """Get base class name"""
        if isinstance(base, ast.Name):
            return base.id
        elif isinstance(base, ast.Attribute):
            return base.attr
        return 'unknown'

    def _is_name_main_check(self, node: ast.If) -> bool:
        """Check if this is 'if __name__ == "__main__"' pattern"""
        if isinstance(node.test, ast.Compare):
            if isinstance(node.test.left, ast.Name) and node.test.left.id == '__name__':
                for comp in node.test.comparators:
                    if isinstance(comp, ast.Constant) and comp.value == '__main__':
                        return True
        return False

    def analyze_all_modules(self) -> Dict[str, Dict]:
        """Analyze all 16 target modules"""
        results = {}

        print("=" * 80)
        print("🔍 ANALYZING 16 TARGET MODULES")
        print("=" * 80)

        for module in self.modules:
            print(f"\n📂 Analyzing: {module}")

            file_path = Path(module)
            if not file_path.exists():
                print(f"   ❌ File not found")
                results[module] = {'error': 'File not found'}
                continue

            analysis = self.analyze_module(str(file_path))

            if 'error' in analysis:
                print(f"   ❌ Error: {analysis['error']}")
            else:
                print(f"   ✅ Functions: {len(analysis['functions'])}")
                print(f"   ✅ Classes: {len(analysis['classes'])}")
                if analysis['classes']:
                    total_methods = sum(len(c['methods']) for c in analysis['classes'])
                    print(f"   ✅ Methods: {total_methods}")
                print(f"   ✅ Lines: {analysis['total_lines']}")

            results[module] = analysis

        return results

    def generate_summary_report(self, results: Dict[str, Dict]) -> str:
        """Generate a summary report"""
        report = []
        report.append("\n" + "=" * 80)
        report.append("📊 MODULE STRUCTURE SUMMARY")
        report.append("=" * 80)

        for module, analysis in results.items():
            report.append(f"\n## {module}")
            report.append("─" * 80)

            if 'error' in analysis:
                report.append(f"❌ ERROR: {analysis['error']}")
                continue

            # Functions
            if analysis['functions']:
                report.append(f"\n**Functions ({len(analysis['functions'])}):**")
                for func in analysis['functions']:
                    args_str = ', '.join(func['args'])
                    async_str = "async " if func['is_async'] else ""
                    report.append(f"  • {async_str}{func['name']}({args_str}) [line {func['lineno']}]")

            # Classes
            if analysis['classes']:
                report.append(f"\n**Classes ({len(analysis['classes'])}):**")
                for cls in analysis['classes']:
                    bases_str = f"({', '.join(cls['bases'])})" if cls['bases'] else ""
                    report.append(f"  • {cls['name']}{bases_str} [line {cls['lineno']}]")

                    if cls['methods']:
                        report.append(f"    Methods ({len(cls['methods'])}):")
                        for method in cls['methods']:
                            args_str = ', '.join(method['args'])
                            async_str = "async " if method['is_async'] else ""
                            prop_str = "@property " if method['is_property'] else ""
                            report.append(f"      - {prop_str}{async_str}{method['name']}({args_str}) [line {method['lineno']}]")

            # Metadata
            report.append(f"\n**Metadata:**")
            report.append(f"  • Total lines: {analysis['total_lines']}")
            report.append(f"  • Has main(): {analysis['has_main']}")
            report.append(f"  • Has if __name__ == '__main__': {analysis['has_if_name_main']}")

        return '\n'.join(report)


def main():
    """Main entry point"""
    analyzer = ModuleAnalyzer()

    # Analyze all modules
    results = analyzer.analyze_all_modules()

    # Save JSON results
    output_file = Path("module_structure_analysis.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)

    print(f"\n✅ Saved detailed analysis to: {output_file}")

    # Generate and display summary report
    report = analyzer.generate_summary_report(results)
    print(report)

    # Save report
    report_file = Path("module_structure_report.txt")
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"\n✅ Saved summary report to: {report_file}")
    print("\n" + "=" * 80)
    print("📈 ANALYSIS COMPLETE")
    print("=" * 80)

    # Summary statistics
    total_functions = sum(len(a.get('functions', [])) for a in results.values())
    total_classes = sum(len(a.get('classes', [])) for a in results.values())
    total_methods = sum(
        sum(len(c['methods']) for c in a.get('classes', []))
        for a in results.values()
    )

    print(f"\n📊 Overall Statistics:")
    print(f"   • Total modules analyzed: {len(results)}")
    print(f"   • Total standalone functions: {total_functions}")
    print(f"   • Total classes: {total_classes}")
    print(f"   • Total methods: {total_methods}")
    print(f"   • Total testable items: {total_functions + total_classes + total_methods}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
