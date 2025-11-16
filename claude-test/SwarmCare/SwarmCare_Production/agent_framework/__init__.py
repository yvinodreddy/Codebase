"""
SwarmCare Agent Framework
Implements Anthropic's Claude Agent SDK patterns for production-ready medical AI agents

Components:
- AgentFeedbackLoop: gather context → take action → verify work → repeat
- ContextManager: Automatic context compaction for long-running agents
- SubagentOrchestrator: Parallel subagent execution and context isolation
- AgenticSearch: File system navigation for context gathering
- CodeGenerator: Generate and verify executable code
- MultiMethodVerifier: Multi-method output verification
- MCPIntegration: Model Context Protocol for standardized integrations

Based on: https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk
"""

from .feedback_loop import AgentFeedbackLoop, FeedbackLoopResult
from .context_manager import ContextManager, ContextCompactionLog
from .subagent_orchestrator import SubagentOrchestrator, SubagentResult
from .agentic_search import AgenticSearch, SearchResult
from .code_generator import CodeGenerator, CodeVerificationResult
from .verification_system import MultiMethodVerifier, VerificationResult
from .mcp_integration import MCPIntegration, MCPConnection

__version__ = "1.0.0"
__author__ = "SwarmCare Team"
__license__ = "MIT"

__all__ = [
    "AgentFeedbackLoop",
    "FeedbackLoopResult",
    "ContextManager",
    "ContextCompactionLog",
    "SubagentOrchestrator",
    "SubagentResult",
    "AgenticSearch",
    "SearchResult",
    "CodeGenerator",
    "CodeVerificationResult",
    "MultiMethodVerifier",
    "VerificationResult",
    "MCPIntegration",
    "MCPConnection",
]
