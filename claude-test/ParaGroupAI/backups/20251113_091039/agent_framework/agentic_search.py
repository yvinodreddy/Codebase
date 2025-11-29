"""
Agentic Search Implementation
File system navigation and context gathering using bash commands

Based on Anthropic's recommendation: use agentic search (bash) over semantic search
"""

import logging
import subprocess
import os
import json
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass
class SearchResult:
    """Result from a search operation"""
    query: str
    method: str  # "grep", "find", "analysis"
    matches: List[Dict[str, Any]]
    total_matches: int
    execution_time_seconds: float
    command_used: str


class AgenticSearch:
    """
    File system navigation and context gathering using bash commands.

    Anthropic recommends:
    - Start with agentic search (more accurate, transparent)
    - Add semantic search only if needed (faster but less accurate)

    This class uses bash commands like grep, find, tail to explore
    the file system and gather context.

    Example:
        >>> search = AgenticSearch()
        >>> results = search.search_phases("guardrails")
        >>> context = search.gather_context_for_phase(5)
    """

    def __init__(self, base_path: Optional[str] = None):
        """
        Initialize agentic search.

        Args:
            base_path: Base path for searches (default: current SwarmCare_Production)
        """
        if base_path is None:
            base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        self.base_path = Path(base_path)
        self.search_log: List[SearchResult] = []

        logger.info(f"AgenticSearch initialized (base_path={self.base_path})")

    def search_phases(self, query: str, case_sensitive: bool = False) -> SearchResult:
        """
        Search across all phases for relevant information.

        Args:
            query: Search term
            case_sensitive: If True, case-sensitive search

        Returns:
            SearchResult with matches
        """
        import time
        start_time = time.time()

        # Build grep command
        flags = "-r" if not case_sensitive else "-r"
        if not case_sensitive:
            flags += " -i"

        command = f"cd {self.base_path} && grep {flags} '{query}' phases/*/ 2>/dev/null || true"

        logger.debug(f"Executing: {command}")

        # Execute
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True
        )

        # Parse results
        matches = self._parse_grep_output(result.stdout)

        execution_time = time.time() - start_time

        search_result = SearchResult(
            query=query,
            method="grep",
            matches=matches,
            total_matches=len(matches),
            execution_time_seconds=execution_time,
            command_used=command
        )

        self.search_log.append(search_result)

        logger.info(f"Found {len(matches)} matches for '{query}' in {execution_time:.3f}s")

        return search_result

    def find_files(self, pattern: str, directory: str = "phases") -> SearchResult:
        """
        Find files matching pattern.

        Args:
            pattern: File pattern (e.g., "*.py", "*test*.py")
            directory: Directory to search in

        Returns:
            SearchResult with matching files
        """
        import time
        start_time = time.time()

        search_dir = self.base_path / directory

        command = f"find {search_dir} -name '{pattern}' 2>/dev/null || true"

        logger.debug(f"Executing: {command}")

        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True
        )

        # Parse results
        files = [
            {"file": line.strip(), "relative_path": str(Path(line.strip()).relative_to(self.base_path))}
            for line in result.stdout.strip().split("\n")
            if line.strip()
        ]

        execution_time = time.time() - start_time

        search_result = SearchResult(
            query=pattern,
            method="find",
            matches=files,
            total_matches=len(files),
            execution_time_seconds=execution_time,
            command_used=command
        )

        self.search_log.append(search_result)

        logger.info(f"Found {len(files)} files matching '{pattern}' in {execution_time:.3f}s")

        return search_result

    def find_dependencies(self, phase_id: int) -> List[Dict[str, Any]]:
        """
        Find all phases that depend on this phase.

        Uses grep to search for dependency references.
        """
        # Search for references to this phase
        result = self.search_phases(f"phase.*{phase_id}")

        dependencies = []

        for match in result.matches:
            # Check if this is a dependency declaration
            if "depend" in match.get("line", "").lower():
                dependencies.append(match)

        logger.info(f"Found {len(dependencies)} dependencies for phase {phase_id}")

        return dependencies

    def analyze_previous_implementation(self, phase_id: int) -> Optional[Dict[str, Any]]:
        """
        Analyze how previous phase was implemented.

        Returns code structure, imports, patterns used.
        """
        if phase_id == 0:
            return None

        prev_phase = phase_id - 1
        impl_path = self.base_path / f"phases/phase{prev_phase:02d}/code/implementation.py"

        if not impl_path.exists():
            logger.warning(f"Previous phase implementation not found: {impl_path}")
            return None

        # Read implementation
        with open(impl_path, 'r') as f:
            code = f.read()

        analysis = {
            "phase_id": prev_phase,
            "file_path": str(impl_path),
            "code_structure": self._analyze_code_structure(code),
            "imports": self._extract_imports(code),
            "classes": self._extract_classes(code),
            "functions": self._extract_functions(code),
            "patterns": self._identify_patterns(code),
            "lines_of_code": len(code.split("\n"))
        }

        logger.info(f"Analyzed previous implementation (phase {prev_phase})")

        return analysis

    def gather_context_for_phase(self, phase_id: int) -> Dict[str, Any]:
        """
        Comprehensive context gathering for a phase.

        Uses multiple search strategies:
        1. Load phase manifest
        2. Search for related phases
        3. Find dependencies
        4. Analyze previous implementation
        5. Search documentation
        6. Find guardrails usage

        Returns:
            Dictionary with comprehensive phase context
        """
        logger.info(f"Gathering comprehensive context for phase {phase_id}")

        context = {
            "phase_id": phase_id,
            "phase_info": self._load_phase_manifest(phase_id),
            "related_phases": self.search_phases(f"phase {phase_id}").matches[:10],
            "dependencies": self.find_dependencies(phase_id),
            "previous_implementation": self.analyze_previous_implementation(phase_id),
            "related_docs": self.search_documentation(f"phase {phase_id}").matches[:5],
            "guardrails_usage": self.search_phases("MultiLayerGuardrailSystem").matches[:5],
            "similar_implementations": self._find_similar_implementations(phase_id),
            "test_files": self.find_files(f"*test*phase{phase_id:02d}*.py").matches
        }

        logger.info(f"Context gathered for phase {phase_id} with {len(context)} components")

        return context

    def search_documentation(self, query: str) -> SearchResult:
        """Search documentation files"""
        import time
        start_time = time.time()

        command = f"cd {self.base_path} && grep -ri '{query}' *.md 2>/dev/null || true"

        logger.debug(f"Executing: {command}")

        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True
        )

        matches = self._parse_grep_output(result.stdout)

        execution_time = time.time() - start_time

        search_result = SearchResult(
            query=query,
            method="grep_docs",
            matches=matches,
            total_matches=len(matches),
            execution_time_seconds=execution_time,
            command_used=command
        )

        return search_result

    def _load_phase_manifest(self, phase_id: int) -> Optional[Dict[str, Any]]:
        """Load phase information from manifest"""
        manifest_path = self.base_path / ".tracker/phase_manifest.json"

        if not manifest_path.exists():
            logger.warning("Phase manifest not found")
            return None

        with open(manifest_path, 'r') as f:
            manifest = json.load(f)

        # Find this phase
        for phase in manifest.get("phases", []):
            if phase.get("phase_id") == phase_id:
                return phase

        return None

    def _find_similar_implementations(self, phase_id: int) -> List[Dict[str, Any]]:
        """Find implementations similar to this phase"""
        # Get phase info
        phase_info = self._load_phase_manifest(phase_id)

        if not phase_info:
            return []

        # Search for similar phases by description
        description = phase_info.get("description", "")
        keywords = description.split()[:3]  # First 3 words

        similar = []
        for keyword in keywords:
            result = self.search_phases(keyword)
            similar.extend(result.matches[:2])

        return similar[:5]  # Top 5

    def _parse_grep_output(self, output: str) -> List[Dict[str, Any]]:
        """Parse grep output into structured matches"""
        matches = []

        for line in output.strip().split("\n"):
            if not line:
                continue

            parts = line.split(":", 2)
            if len(parts) >= 2:
                matches.append({
                    "file": parts[0],
                    "line_number": parts[1] if len(parts) > 2 else "unknown",
                    "line": parts[2] if len(parts) > 2 else parts[1],
                    "preview": parts[2][:200] if len(parts) > 2 else parts[1][:200]
                })

        return matches

    def _analyze_code_structure(self, code: str) -> Dict[str, Any]:
        """Analyze code structure"""
        lines = code.split("\n")

        return {
            "total_lines": len(lines),
            "code_lines": sum(1 for line in lines if line.strip() and not line.strip().startswith("#")),
            "comment_lines": sum(1 for line in lines if line.strip().startswith("#")),
            "docstring_lines": code.count('"""') // 2 * 3,  # Rough estimate
            "blank_lines": sum(1 for line in lines if not line.strip())
        }

    def _extract_imports(self, code: str) -> List[str]:
        """Extract import statements"""
        imports = []

        for line in code.split("\n"):
            stripped = line.strip()
            if stripped.startswith("import ") or stripped.startswith("from "):
                imports.append(stripped)

        return imports

    def _extract_classes(self, code: str) -> List[str]:
        """Extract class definitions"""
        classes = []

        for line in code.split("\n"):
            stripped = line.strip()
            if stripped.startswith("class "):
                # Extract class name
                class_name = stripped.split("class ")[1].split("(")[0].split(":")[0].strip()
                classes.append(class_name)

        return classes

    def _extract_functions(self, code: str) -> List[str]:
        """Extract function definitions"""
        functions = []

        for line in code.split("\n"):
            stripped = line.strip()
            if stripped.startswith("def "):
                # Extract function name
                func_name = stripped.split("def ")[1].split("(")[0].strip()
                functions.append(func_name)

        return functions

    def _identify_patterns(self, code: str) -> List[str]:
        """Identify common patterns in code"""
        patterns = []

        if "MultiLayerGuardrailSystem" in code:
            patterns.append("uses_guardrails")

        if "AgentFeedbackLoop" in code:
            patterns.append("uses_feedback_loop")

        if "ContextManager" in code:
            patterns.append("uses_context_manager")

        if "SubagentOrchestrator" in code:
            patterns.append("uses_subagents")

        if "class" in code:
            patterns.append("object_oriented")

        if "async def" in code:
            patterns.append("async_programming")

        if "try:" in code and "except" in code:
            patterns.append("error_handling")

        return patterns

    def get_statistics(self) -> Dict[str, Any]:
        """Get search statistics"""
        if not self.search_log:
            return {"error": "No searches performed"}

        return {
            "total_searches": len(self.search_log),
            "total_matches": sum(r.total_matches for r in self.search_log),
            "average_matches_per_search": sum(r.total_matches for r in self.search_log) / len(self.search_log),
            "total_execution_time": sum(r.execution_time_seconds for r in self.search_log),
            "average_execution_time": sum(r.execution_time_seconds for r in self.search_log) / len(self.search_log),
            "search_methods": list(set(r.method for r in self.search_log))
        }


if __name__ == "__main__":
    # Example usage
    search = AgenticSearch()

    print("=" * 60)
    print("AGENTIC SEARCH EXAMPLE")
    print("=" * 60)

    # Example 1: Search phases
    print("\n1. Searching for 'guardrails' in phases...")
    result = search.search_phases("guardrails")
    print(f"   Found {result.total_matches} matches in {result.execution_time_seconds:.3f}s")
    if result.matches:
        print(f"   First match: {result.matches[0]['file']}")

    # Example 2: Find Python files
    print("\n2. Finding Python implementation files...")
    result = search.find_files("implementation.py")
    print(f"   Found {result.total_matches} files in {result.execution_time_seconds:.3f}s")

    # Example 3: Gather comprehensive context
    print("\n3. Gathering comprehensive context for phase 0...")
    context = search.gather_context_for_phase(0)
    print(f"   Phase info: {context['phase_info']['name'] if context['phase_info'] else 'Not found'}")
    print(f"   Related phases: {len(context['related_phases'])}")
    print(f"   Dependencies: {len(context['dependencies'])}")

    # Show statistics
    print("\n" + "=" * 60)
    print("STATISTICS")
    print("=" * 60)
    stats = search.get_statistics()
    print(json.dumps(stats, indent=2))

    print("\n✅ Example complete")
