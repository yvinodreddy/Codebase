#!/usr/bin/env python3
"""
Comprehensive Codebase Analysis
Analyzes security, performance, code quality, and test coverage
"""

import os
import re
import ast
import sqlite3
from pathlib import Path
from typing import Dict, List, Tuple
import subprocess

class CodebaseAnalyzer:
    def __init__(self, root_dir: str = "."):
        self.root_dir = root_dir
        self.issues = {
            "security": [],
            "performance": [],
            "code_quality": [],
            "test_coverage": []
        }
    
    def analyze_security(self):
        """Scan for security issues"""
        print("[SECURITY] Starting security analysis...")
        
        # Check for SQL injection vulnerabilities
        python_files = list(Path(self.root_dir).rglob("*.py"))
        
        for file in python_files:
            try:
                with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    lines = content.split('\n')
                
                # Check for string formatting in SQL
                for i, line in enumerate(lines, 1):
                    if 'execute' in line and ('f"' in line or '%" ' in line or '.format(' in line):
                        self.issues["security"].append({
                            "type": "SQL Injection Risk",
                            "file": str(file),
                            "line": i,
                            "severity": "HIGH",
                            "description": "SQL query uses string formatting instead of parameterized queries",
                            "code": line.strip()
                        })
                    
                    # Check for os.system or subprocess with shell=True
                    if ('os.system(' in line or 'shell=True' in line) and not line.strip().startswith('#'):
                        self.issues["security"].append({
                            "type": "Command Injection Risk",
                            "file": str(file),
                            "line": i,
                            "severity": "HIGH",
                            "description": "Using shell=True or os.system can lead to command injection",
                            "code": line.strip()
                        })
                    
                    # Check for hardcoded secrets
                    if re.search(r'(password|secret|api_key|token)\s*=\s*["\'][^"\']+["\']', line, re.I):
                        if 'example' not in line.lower() and 'placeholder' not in line.lower():
                            self.issues["security"].append({
                                "type": "Hardcoded Secret",
                                "file": str(file),
                                "line": i,
                                "severity": "CRITICAL",
                                "description": "Potential hardcoded secret detected",
                                "code": "*** REDACTED ***"
                            })
            
            except Exception as e:
                print(f"Error analyzing {file}: {e}")
        
        print(f"[SECURITY] Found {len(self.issues['security'])} security issues")
    
    def analyze_performance(self):
        """Check for performance bottlenecks"""
        print("[PERFORMANCE] Starting performance analysis...")
        
        python_files = list(Path(self.root_dir).rglob("*.py"))
        
        for file in python_files:
            try:
                with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    lines = content.split('\n')
                
                for i, line in enumerate(lines, 1):
                    # Check for N+1 query patterns
                    if 'for ' in line and i < len(lines) - 5:
                        next_lines = '\n'.join(lines[i:i+5])
                        if 'execute(' in next_lines or 'query(' in next_lines:
                            self.issues["performance"].append({
                                "type": "N+1 Query Pattern",
                                "file": str(file),
                                "line": i,
                                "severity": "MEDIUM",
                                "description": "Potential N+1 query pattern (query inside loop)",
                                "code": line.strip()
                            })
                    
                    # Check for missing DB connection pooling
                    if 'sqlite3.connect(' in line and 'close()' not in content:
                        self.issues["performance"].append({
                            "type": "Resource Leak",
                            "file": str(file),
                            "line": i,
                            "severity": "MEDIUM",
                            "description": "DB connection may not be properly closed",
                            "code": line.strip()
                        })
                    
                    # Check for file operations without context manager
                    if 'open(' in line and 'with ' not in lines[max(0, i-2):i+1][0] if i > 0 else '':
                        self.issues["performance"].append({
                            "type": "Resource Leak",
                            "file": str(file),
                            "line": i,
                            "severity": "LOW",
                            "description": "File opened without context manager (may leak file descriptor)",
                            "code": line.strip()
                        })
            
            except Exception as e:
                print(f"Error analyzing {file}: {e}")
        
        print(f"[PERFORMANCE] Found {len(self.issues['performance'])} performance issues")
    
    def analyze_code_quality(self):
        """Check code quality issues"""
        print("[CODE QUALITY] Starting code quality analysis...")
        
        python_files = list(Path(self.root_dir).rglob("*.py"))
        
        for file in python_files:
            try:
                with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    lines = content.split('\n')
                
                # Check for missing docstrings
                try:
                    tree = ast.parse(content)
                    for node in ast.walk(tree):
                        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                            if not ast.get_docstring(node):
                                self.issues["code_quality"].append({
                                    "type": "Missing Docstring",
                                    "file": str(file),
                                    "line": node.lineno,
                                    "severity": "LOW",
                                    "description": f"{node.__class__.__name__} '{node.name}' missing docstring",
                                    "code": f"def {node.name}..." if isinstance(node, ast.FunctionDef) else f"class {node.name}..."
                                })
                except SyntaxError:
                    pass
                
                for i, line in enumerate(lines, 1):
                    # Check for bare except
                    if re.match(r'^\s*except\s*:', line):
                        self.issues["code_quality"].append({
                            "type": "Bare Except Clause",
                            "file": str(file),
                            "line": i,
                            "severity": "MEDIUM",
                            "description": "Bare except clause catches all exceptions (use specific exceptions)",
                            "code": line.strip()
                        })
                    
                    # Check for print statements (should use logging)
                    if 'print(' in line and 'test' not in str(file).lower():
                        self.issues["code_quality"].append({
                            "type": "Print Statement",
                            "file": str(file),
                            "line": i,
                            "severity": "LOW",
                            "description": "Using print() instead of logging",
                            "code": line.strip()
                        })
            
            except Exception as e:
                print(f"Error analyzing {file}: {e}")
        
        print(f"[CODE QUALITY] Found {len(self.issues['code_quality'])} code quality issues")
    
    def analyze_test_coverage(self):
        """Check test coverage"""
        print("[TEST COVERAGE] Starting test coverage analysis...")
        
        # Find all test files
        test_files = list(Path(self.root_dir).rglob("test_*.py"))
        test_files.extend(Path(self.root_dir).rglob("*_test.py"))
        
        # Find all Python files
        python_files = list(Path(self.root_dir).rglob("*.py"))
        python_files = [f for f in python_files if 'test' not in str(f) and '__pycache__' not in str(f)]
        
        # Check if tests exist
        if len(test_files) == 0:
            self.issues["test_coverage"].append({
                "type": "No Tests",
                "file": "N/A",
                "line": 0,
                "severity": "HIGH",
                "description": "No test files found in codebase",
                "code": ""
            })
        else:
            # Calculate coverage ratio
            tested_files = set()
            for test_file in test_files:
                try:
                    with open(test_file, 'r') as f:
                        content = f.read()
                        for py_file in python_files:
                            module_name = py_file.stem
                            if module_name in content:
                                tested_files.add(str(py_file))
                except:
                    pass
            
            untested_files = set(str(f) for f in python_files) - tested_files
            coverage_pct = (len(tested_files) / len(python_files) * 100) if python_files else 0
            
            self.issues["test_coverage"].append({
                "type": "Test Coverage",
                "file": "Overall",
                "line": 0,
                "severity": "INFO",
                "description": f"Test coverage: {coverage_pct:.1f}% ({len(tested_files)}/{len(python_files)} files)",
                "code": f"{len(untested_files)} files untested"
            })
            
            # Report untested critical files
            for file in untested_files:
                if any(x in file for x in ['orchestrator', 'security', 'guardrails']):
                    self.issues["test_coverage"].append({
                        "type": "Missing Tests",
                        "file": file,
                        "line": 0,
                        "severity": "MEDIUM",
                        "description": "Critical file missing test coverage",
                        "code": ""
                    })
        
        print(f"[TEST COVERAGE] Found {len(self.issues['test_coverage'])} test coverage issues")
    
    def generate_report(self) -> str:
        """Generate analysis report"""
        report = []
        report.append("="*80)
        report.append("CODEBASE ANALYSIS REPORT")
        report.append("="*80)
        report.append("")
        
        for category, issues in self.issues.items():
            if issues:
                report.append(f"\n{'='*80}")
                report.append(f"{category.upper().replace('_', ' ')}: {len(issues)} issues")
                report.append("="*80)
                
                # Group by severity
                by_severity = {}
                for issue in issues:
                    severity = issue.get('severity', 'UNKNOWN')
                    if severity not in by_severity:
                        by_severity[severity] = []
                    by_severity[severity].append(issue)
                
                for severity in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'INFO']:
                    if severity in by_severity:
                        report.append(f"\n{severity} ({len(by_severity[severity])} issues):")
                        report.append("-"*80)
                        for issue in by_severity[severity][:10]:  # Limit to 10 per severity
                            report.append(f"\nType: {issue['type']}")
                            report.append(f"File: {issue['file']}")
                            if issue['line']:
                                report.append(f"Line: {issue['line']}")
                            report.append(f"Description: {issue['description']}")
                            if issue.get('code'):
                                report.append(f"Code: {issue['code'][:100]}")
                        
                        if len(by_severity[severity]) > 10:
                            report.append(f"\n... and {len(by_severity[severity]) - 10} more")
        
        report.append("\n" + "="*80)
        report.append("SUMMARY")
        report.append("="*80)
        total = sum(len(issues) for issues in self.issues.values())
        report.append(f"Total Issues: {total}")
        for category, issues in self.issues.items():
            report.append(f"  {category.replace('_', ' ').title()}: {len(issues)}")
        
        return "\n".join(report)
    
    def run_analysis(self):
        """Run all analysis checks"""
        self.analyze_security()
        self.analyze_performance()
        self.analyze_code_quality()
        self.analyze_test_coverage()
        
        report = self.generate_report()
        
        # Save report
        with open('CODEBASE_ANALYSIS_REPORT.md', 'w') as f:
            f.write(report)
        
        print(f"\n{'='*80}")
        print("Analysis complete! Report saved to: CODEBASE_ANALYSIS_REPORT.md")
        print("="*80)
        
        return report

if __name__ == '__main__':
    analyzer = CodebaseAnalyzer()
    report = analyzer.run_analysis()
    print(report)
