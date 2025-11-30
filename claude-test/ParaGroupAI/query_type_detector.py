#!/usr/bin/env python3
"""
Query Type Detector

Determines whether a query needs:
1. Database search (conversation history / context compaction)
2. File tools (codebase analysis)

CRITICAL PURPOSE (2025-11-29):
Database is ONLY for:
- Storing project context during context compaction (when tokens run out)
- Retrieving stored context and passing to Claude Code LLM
- Conversation history queries ("what did we discuss?")

Database is NOT for:
- Codebase analysis (use file tools: Glob, Grep, Read)
- Security reviews (use file tools)
- Performance analysis (use file tools)
- Code quality checks (use file tools)
"""

import sys

# Keywords that indicate FILE-BASED queries (use Claude Code file tools)
FILE_KEYWORDS = [
    # Analysis keywords
    'analyze', 'codebase', 'code', 'file', 'directory', 'folder',
    'source', 'implementation', 'module', 'package',

    # Security/Quality keywords
    'security', 'vulnerability', 'vulnerabilities', 'exploit',
    'performance', 'bottleneck', 'bottlenecks', 'slow', 'optimize',
    'code quality', 'quality', 'test coverage', 'coverage', 'tests',
    'bug', 'issue', 'error', 'exception', 'crash',

    # Action keywords
    'fix', 'implement', 'refactor', 'optimize', 'improve',
    'add', 'update', 'modify', 'change', 'delete', 'remove',
    'create', 'build', 'develop',

    # File operations
    'read', 'write', 'edit', 'search', 'find', 'locate',
    'review', 'inspect', 'examine',

    # Code-specific
    'function', 'class', 'method', 'variable', 'constant',
    'import', 'export', 'dependency', 'dependencies'
]

# Keywords that indicate HISTORY queries (use database search)
HISTORY_KEYWORDS = [
    # Past references
    'what did we', 'what did you', 'what have we', 'what have you',
    'previous', 'previously', 'earlier', 'before',
    'last time', 'last week', 'last session',

    # Memory/recall
    'you said', 'you mentioned', 'you explained', 'you told',
    'we decided', 'we discussed', 'we talked',
    'remember', 'recall', 'remind',

    # Context requests
    'discuss', 'discussed', 'discussion',
    'talked about', 'mentioned', 'explained',
    'decision', 'approach', 'solution',

    # Retrieval
    'show me the', 'find the conversation', 'search history',
    'what was', 'when did', 'why did'
]

def should_run_dual_retrieval(query: str) -> bool:
    """
    Determine if query needs database search or file tools.

    Args:
        query: User's query string

    Returns:
        True: Run dual retrieval (search database for conversation history)
        False: Skip dual retrieval (let Claude Code use file tools)

    Logic:
        1. Count FILE keywords vs HISTORY keywords
        2. If FILE keywords > HISTORY keywords → File tools (codebase analysis)
        3. If HISTORY keywords > FILE keywords → Database search
        4. Default → File tools (safer for codebase queries)

    CRITICAL FIX (2025-11-29):
    Previous logic checked HISTORY first, causing false positives.
    Example: "Analyze codebase for security issues with step-by-step approach"
             contained "approach" (HISTORY keyword) but is clearly FILE query.
    Solution: Count keywords, prioritize dominant type.
    """
    query_lower = query.lower()

    # Count keyword matches for each type
    file_matches = sum(1 for kw in FILE_KEYWORDS if kw in query_lower)
    history_matches = sum(1 for kw in HISTORY_KEYWORDS if kw in query_lower)

    # If FILE keywords dominate, use file tools (codebase analysis)
    if file_matches > history_matches:
        return False  # File tools

    # If HISTORY keywords dominate, use database search
    if history_matches > file_matches:
        return True  # Database search

    # If equal or both zero, default to file tools (safer)
    return False

def get_query_type_explanation(query: str) -> str:
    """Get human-readable explanation of query type detection."""
    if should_run_dual_retrieval(query):
        return "CONVERSATION HISTORY query - Using database search"
    else:
        return "FILE-BASED query - Using Claude Code file tools"

def main():
    """Command-line interface for query type detection."""
    if len(sys.argv) < 2:
        print("Usage: query_type_detector.py \"your query here\"", file=sys.stderr)
        sys.exit(1)

    query = ' '.join(sys.argv[1:])

    if should_run_dual_retrieval(query):
        print("history")  # Output for shell scripts
        return 0
    else:
        print("file")  # Output for shell scripts
        return 0

if __name__ == "__main__":
    sys.exit(main())
