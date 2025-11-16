# 🤖 SwarmCare Agent Framework Guide

**Based on:** Anthropic's Claude Agent SDK Best Practices
**Version:** 1.0.0
**Date:** 2025-10-27

---

## 📋 TABLE OF CONTENTS

1. [Overview](#overview)
2. [Core Concepts](#core-concepts)
3. [Components](#components)
4. [Quick Start](#quick-start)
5. [Usage Examples](#usage-examples)
6. [Best Practices](#best-practices)
7. [API Reference](#api-reference)
8. [Troubleshooting](#troubleshooting)

---

## 🎯 OVERVIEW

The SwarmCare Agent Framework implements Anthropic's best practices for building production-ready AI agents. It provides a complete toolkit for creating agents that can:

- ✅ **Self-correct** through iterative feedback loops
- ✅ **Scale** with parallel subagent execution
- ✅ **Handle complexity** with automatic context management
- ✅ **Verify rigorously** with multi-method validation
- ✅ **Integrate easily** with external services via MCP

### The Agent Feedback Loop

The core pattern that powers all SwarmCare agents:

```
┌─────────────────────────────────────────────────────────┐
│                   AGENT FEEDBACK LOOP                    │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  1. GATHER CONTEXT                                      │
│     └─ Agentic search, subagents, context management   │
│                                                          │
│  2. TAKE ACTION                                         │
│     └─ Execute task with guardrails                    │
│                                                          │
│  3. VERIFY WORK                                         │
│     └─ Multi-method verification                       │
│                                                          │
│  4. REPEAT (if verification fails)                      │
│     └─ Learn from failures, adjust approach            │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## 🔑 CORE CONCEPTS

### 1. Agent Feedback Loop

**What it is:** The fundamental pattern for reliable agents

**Why it matters:** Agents that can check and improve their own output are fundamentally more reliable

**When to use:** Every agent that needs to produce reliable output

**Example:**
```python
from feedback_loop import AgentFeedbackLoop

loop = AgentFeedbackLoop(max_iterations=10)
result = loop.execute(
    task={"goal": "implement feature X"},
    context_gatherer=gather_context_func,
    action_executor=execute_action_func,
    verifier=verify_output_func
)
```

### 2. Context Management

**What it is:** Automatic context compaction for long-running agents

**Why it matters:** Prevents context overflow on long tasks

**When to use:** Any agent that might run for multiple iterations or process large amounts of information

**Example:**
```python
from context_manager import ContextManager

context = ContextManager(max_tokens=100000, compact_threshold=0.8)
context.add_message("user", "Large message...")
# Automatic compaction occurs at 80% usage
```

### 3. Subagent Orchestration

**What it is:** Parallel execution of multiple agents

**Why it matters:**
- **2-5x speedup** on complex tasks
- **Better context management** (isolated contexts)
- **Scalability** for large workloads

**When to use:** When you need to gather information from multiple sources or perform independent tasks simultaneously

**Example:**
```python
from subagent_orchestrator import SubagentOrchestrator

orchestrator = SubagentOrchestrator(max_parallel=5)

# Spawn multiple subagents
tasks = [
    {"goal": "search emails"},
    {"goal": "search calendar"},
    {"goal": "search docs"}
]

subagent_ids = orchestrator.spawn_parallel(
    tasks=tasks,
    context_gatherer=gather_func,
    action_executor=execute_func,
    verifier=verify_func
)

# Wait for results
results = orchestrator.wait_for_subagents(subagent_ids)

# Merge results (only relevant info, not full context!)
merged = orchestrator.merge_subagent_results(results)
```

### 4. Agentic Search

**What it is:** File system navigation using bash commands (grep, find, etc.)

**Why it matters:**
- More accurate than semantic search
- More transparent (see exact commands)
- Easier to maintain

**When to use:** Context gathering, exploring codebases, finding dependencies

**Anthropic's Recommendation:** Start with agentic search, only add semantic search if needed

**Example:**
```python
from agentic_search import AgenticSearch

search = AgenticSearch()

# Search phases
results = search.search_phases("guardrails")

# Find dependencies
deps = search.find_dependencies(phase_id=5)

# Gather comprehensive context
context = search.gather_context_for_phase(5)
```

### 5. Multi-Method Verification

**What it is:** Combine multiple verification approaches

**Why it matters:** Each method catches different types of issues

**Methods:**
1. **Rules-based** (best) - Clear rules, explain failures
2. **Code verification** - Linting, type checking, security
3. **Guardrails** - Medical safety, HIPAA compliance
4. **Visual feedback** - Screenshots for UI tasks
5. **LLM as judge** - Fuzzy criteria evaluation

**Example:**
```python
from verification_system import MultiMethodVerifier

verifier = MultiMethodVerifier()

result = verifier.verify_output(
    output=generated_code,
    context={"input": user_request},
    output_type="code"
)

if result["overall_passed"]:
    print("All verifications passed!")
```

### 6. Model Context Protocol (MCP)

**What it is:** Standardized integrations to external services

**Why it matters:**
- No custom integration code needed
- Automatic OAuth handling
- Pre-built, maintained connectors

**Services:** Slack, GitHub, Google Drive, Asana, and more

**Example:**
```python
from mcp_integration import MCPIntegration

mcp = MCPIntegration()

# Call tool on Slack
results = mcp.call_tool("slack", "search_messages", {
    "query": "project X",
    "limit": 10
})
```

---

## 🚀 QUICK START

### Installation

The agent framework is already included in SwarmCare. Just import the components you need:

```python
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'agent_framework'))

from feedback_loop import AgentFeedbackLoop
from context_manager import ContextManager
from subagent_orchestrator import SubagentOrchestrator
from agentic_search import AgenticSearch
from verification_system import MultiMethodVerifier
from mcp_integration import MCPIntegration
```

### Basic Agent Template

```python
class MyAgent:
    def __init__(self):
        # Initialize components
        self.feedback_loop = AgentFeedbackLoop(max_iterations=10)
        self.context = ContextManager(max_tokens=100000)
        self.verifier = MultiMethodVerifier()

    def gather_context(self, task, iteration_log):
        """Step 1: Gather context"""
        # Your context gathering logic
        return {"task": task}

    def take_action(self, task, context):
        """Step 2: Take action"""
        # Your implementation logic
        return {"result": "success"}

    def verify_work(self, output, context, task):
        """Step 3: Verify work"""
        verification = self.verifier.verify_output(
            output=output,
            context=context,
            output_type="data"
        )
        return {
            "passed": verification["overall_passed"],
            "message": "Verification result"
        }

    def execute(self, task):
        """Main execution with feedback loop"""
        result = self.feedback_loop.execute(
            task=task,
            context_gatherer=self.gather_context,
            action_executor=self.take_action,
            verifier=self.verify_work
        )
        return result
```

### Run Your Agent

```python
agent = MyAgent()
result = agent.execute({"goal": "accomplish task X"})

if result.success:
    print(f"Success after {result.iterations} iterations!")
else:
    print(f"Failed: {result.error}")
```

---

## 💡 USAGE EXAMPLES

### Example 1: Simple Agent with Feedback Loop

```python
from feedback_loop import AgentFeedbackLoop

def gather_context(task, iteration_log):
    # Learn from previous failures
    if iteration_log:
        previous_errors = [log.verification.get("error") for log in iteration_log]
        return {"task": task, "previous_errors": previous_errors}
    return {"task": task}

def take_action(task, context):
    # Implement your logic
    return {"result": "implementation"}

def verify_output(output, context, task):
    # Verify the output
    if output.get("result") == "implementation":
        return {"passed": True, "message": "Output is correct"}
    return {"passed": False, "message": "Output incomplete"}

# Execute with feedback loop
loop = AgentFeedbackLoop(max_iterations=5)
result = loop.execute(
    task={"goal": "implement feature"},
    context_gatherer=gather_context,
    action_executor=take_action,
    verifier=verify_output
)
```

### Example 2: Agent with Subagents for Parallel Search

```python
from subagent_orchestrator import SubagentOrchestrator
from agentic_search import AgenticSearch

search = AgenticSearch()
orchestrator = SubagentOrchestrator(max_parallel=3)

# Define search tasks
search_tasks = [
    {"goal": "search previous implementations"},
    {"goal": "find dependencies"},
    {"goal": "analyze documentation"}
]

# Spawn subagents in parallel
subagent_ids = orchestrator.spawn_parallel(
    tasks=search_tasks,
    context_gatherer=lambda t, log: {"task": t},
    action_executor=lambda t, ctx: search.gather_context_for_phase(0),
    verifier=lambda out, ctx, t: {"passed": True, "message": "Done"}
)

# Wait for results
results = orchestrator.wait_for_subagents(subagent_ids, timeout=60)

# Merge results (only relevant info!)
merged = orchestrator.merge_subagent_results(results)

print(f"Found {len(merged['key_findings'])} key findings")
```

### Example 3: Agent with Context Compaction

```python
from context_manager import ContextManager
from feedback_loop import AgentFeedbackLoop

# Small context to demonstrate compaction
context = ContextManager(max_tokens=5000, compact_threshold=0.7)

def gather_context(task, iteration_log):
    # Add large messages
    context.add_message("user", "Large context..." * 100)
    return {"task": task}

def take_action(task, ctx):
    # Add more messages
    context.add_message("assistant", "Processing..." * 100)
    return {"result": "success"}

def verify_output(output, ctx, task):
    return {"passed": True, "message": "Done"}

loop = AgentFeedbackLoop(max_iterations=10)
result = loop.execute(
    task={"goal": "test"},
    context_gatherer=gather_context,
    action_executor=take_action,
    verifier=verify_output
)

# Context was automatically compacted
print(f"Compactions: {len(context.compaction_log)}")
```

### Example 4: Complete Phase Implementation

See `phases/phase00/code/implementation_enhanced.py` for a complete example of a phase implementation using all agent framework components.

---

## 🎓 BEST PRACTICES

### 1. Always Use the Feedback Loop

❌ **Don't do this:**
```python
def execute(self, task):
    output = self.implement(task)
    return output  # No verification!
```

✅ **Do this:**
```python
def execute(self, task):
    result = self.feedback_loop.execute(
        task=task,
        context_gatherer=self.gather_context,
        action_executor=self.take_action,
        verifier=self.verify_work
    )
    return result
```

### 2. Implement Learning from Failures

❌ **Don't do this:**
```python
def gather_context(task, iteration_log):
    return {"task": task}  # Ignores previous failures
```

✅ **Do this:**
```python
def gather_context(task, iteration_log):
    context = {"task": task}

    if iteration_log:
        # Learn from previous attempts
        previous_errors = [
            log.verification.get("message")
            for log in iteration_log
            if not log.success
        ]
        context["previous_errors"] = previous_errors
        context["attempt_number"] = len(iteration_log) + 1

    return context
```

### 3. Use Subagents for Independent Tasks

❌ **Don't do this:**
```python
# Sequential execution (slow)
result1 = search_emails()
result2 = search_calendar()
result3 = search_docs()
```

✅ **Do this:**
```python
# Parallel execution (2-5x faster)
tasks = [
    {"goal": "search emails"},
    {"goal": "search calendar"},
    {"goal": "search docs"}
]
subagent_ids = orchestrator.spawn_parallel(tasks, ...)
results = orchestrator.wait_for_subagents(subagent_ids)
```

### 4. Return Only Relevant Information from Subagents

❌ **Don't do this:**
```python
# Subagent returns EVERYTHING (bloats context)
return {"full_context": massive_data_structure}
```

✅ **Do this:**
```python
# Subagent returns only key findings
return {
    "summary": "Found 3 relevant matches",
    "key_data": [match1, match2, match3]
}
```

### 5. Use Rules-Based Verification as Primary Method

❌ **Don't do this:**
```python
# Rely only on LLM-as-judge (expensive, less robust)
def verify(output):
    return llm_judge(output)
```

✅ **Do this:**
```python
# Use rules-based verification (best practice)
def verify(output):
    rules = {
        "not_empty": lambda o: o is not None,
        "has_required_fields": lambda o: all(f in o for f in required_fields),
        "no_sensitive_data": lambda o: not has_sensitive_data(o)
    }

    for rule_name, rule_check in rules.items():
        if not rule_check(output):
            return {
                "passed": False,
                "rule_failed": rule_name,
                "how_to_fix": get_fix_instructions(rule_name)
            }

    return {"passed": True}
```

### 6. Enable Context Compaction for Long Tasks

❌ **Don't do this:**
```python
# No compaction = context overflow on long tasks
context = ContextManager(max_tokens=100000, compact_threshold=1.0)
```

✅ **Do this:**
```python
# Auto-compact at 80% to prevent overflow
context = ContextManager(max_tokens=100000, compact_threshold=0.8)
```

---

## 📚 API REFERENCE

### AgentFeedbackLoop

**Purpose:** Orchestrate the gather → act → verify → repeat cycle

**Constructor:**
```python
AgentFeedbackLoop(
    max_iterations: int = 10,
    enable_learning: bool = True,
    log_file: Optional[str] = None
)
```

**Methods:**

#### `execute(task, context_gatherer, action_executor, verifier) -> FeedbackLoopResult`

Execute task with feedback loop.

**Parameters:**
- `task`: Dict with task configuration
- `context_gatherer`: Function(task, iteration_log) -> context
- `action_executor`: Function(task, context) -> output
- `verifier`: Function(output, context, task) -> verification_result

**Returns:** `FeedbackLoopResult` with:
- `success`: bool
- `output`: Any
- `iterations`: int
- `total_duration_seconds`: float
- `iteration_log`: List[IterationLog]
- `error`: Optional[str]

#### `get_statistics() -> Dict[str, Any]`

Get execution statistics.

**Returns:** Dict with success rate, iteration counts, timing

---

### ContextManager

**Purpose:** Manage agent context with automatic compaction

**Constructor:**
```python
ContextManager(
    max_tokens: int = 100000,
    compact_threshold: float = 0.8,
    keep_recent: int = 10
)
```

**Methods:**

#### `add_message(role: str, content: str, metadata: Optional[Dict] = None)`

Add message to context. Triggers auto-compaction if needed.

#### `compact()`

Manually trigger compaction. Usually called automatically.

#### `mark_important(message_index: int)`

Mark message as important (preserved during compaction).

#### `get_statistics() -> Dict[str, Any]`

Get context usage statistics.

---

### SubagentOrchestrator

**Purpose:** Manage parallel subagent execution

**Constructor:**
```python
SubagentOrchestrator(
    max_parallel: int = 5,
    default_context_size: int = 50000
)
```

**Methods:**

#### `spawn_parallel(tasks, context_gatherer, action_executor, verifier) -> List[str]`

Spawn multiple subagents in parallel.

**Returns:** List of subagent IDs

#### `wait_for_subagents(subagent_ids: List[str], timeout: float = 300) -> Dict[str, SubagentResult]`

Wait for subagents to complete.

**Returns:** Dict of subagent_id -> SubagentResult

#### `merge_subagent_results(results: Dict[str, SubagentResult]) -> Dict[str, Any]`

Merge results from multiple subagents.

**Returns:** Merged result with key findings and errors

---

### AgenticSearch

**Purpose:** File system navigation and context gathering

**Constructor:**
```python
AgenticSearch(base_path: Optional[str] = None)
```

**Methods:**

#### `search_phases(query: str) -> SearchResult`

Search across all phases for query.

#### `find_files(pattern: str) -> SearchResult`

Find files matching pattern.

#### `find_dependencies(phase_id: int) -> List[Dict]`

Find phases that depend on given phase.

#### `gather_context_for_phase(phase_id: int) -> Dict[str, Any]`

Comprehensive context gathering for a phase.

---

### MultiMethodVerifier

**Purpose:** Multi-method output verification

**Constructor:**
```python
MultiMethodVerifier()
```

**Methods:**

#### `verify_output(output, context, output_type: str, task: Optional[Dict] = None) -> Dict[str, Any]`

Verify output using multiple methods.

**Parameters:**
- `output`: Output to verify
- `context`: Context including input, requirements
- `output_type`: "text", "code", "data", or "ui"
- `task`: Optional task configuration

**Returns:** Dict with:
- `overall_passed`: bool
- `methods_used`: List[str]
- `method_results`: Dict[str, VerificationResult]
- `all_recommendations`: List[str]

---

### MCPIntegration

**Purpose:** Model Context Protocol integrations

**Constructor:**
```python
MCPIntegration()
```

**Methods:**

#### `call_tool(server_name: str, tool_name: str, params: Dict) -> Any`

Call tool on MCP server.

**Example:**
```python
mcp.call_tool("slack", "search_messages", {"query": "project X"})
```

#### `list_available_servers() -> List[str]`

List registered MCP servers.

#### `list_server_tools(server_name: str) -> List[str]`

List tools available on a server.

---

## 🔧 TROUBLESHOOTING

### Issue: Agent hits max iterations without success

**Symptoms:** FeedbackLoopResult with `success=False`, `error="Max iterations reached"`

**Causes:**
1. Verification criteria too strict
2. Agent not learning from failures
3. Max iterations too low
4. Fundamental issue with task

**Solutions:**
1. Review verification rules in `verify_work()`
2. Implement learning in `gather_context()` using `iteration_log`
3. Increase `max_iterations`
4. Check if task is actually achievable

**Example:**
```python
def gather_context(task, iteration_log):
    context = {"task": task}

    # Learn from failures
    if iteration_log:
        failed_attempts = [log for log in iteration_log if not log.success]

        # Adjust approach based on failures
        if len(failed_attempts) > 2:
            context["use_alternative_approach"] = True

        # Extract error patterns
        errors = [log.verification.get("message") for log in failed_attempts]
        context["avoid_errors"] = errors

    return context
```

---

### Issue: Context overflow errors

**Symptoms:** Errors about context limits, "too many tokens"

**Causes:**
1. No context compaction enabled
2. Compact threshold too high (e.g., 1.0)
3. Keep_recent set too high

**Solutions:**
1. Enable compaction: `compact_threshold=0.8`
2. Lower threshold: `compact_threshold=0.7`
3. Reduce keep_recent: `keep_recent=10`

**Example:**
```python
# Before (wrong)
context = ContextManager(max_tokens=100000, compact_threshold=1.0)

# After (correct)
context = ContextManager(
    max_tokens=100000,
    compact_threshold=0.8,  # Compact at 80%
    keep_recent=10  # Keep last 10 messages
)
```

---

### Issue: Subagents timing out

**Symptoms:** `TimeoutError` when waiting for subagents

**Causes:**
1. Subagent tasks too complex
2. Timeout too short
3. Deadlock or infinite loop in subagent

**Solutions:**
1. Break down tasks into smaller pieces
2. Increase timeout
3. Add logging to identify stuck subagent

**Example:**
```python
# Increase timeout
results = orchestrator.wait_for_subagents(
    subagent_ids,
    timeout=600  # 10 minutes instead of default 5
)

# Or break down tasks
# Before (complex task)
tasks = [{"goal": "analyze entire codebase"}]

# After (smaller tasks)
tasks = [
    {"goal": "analyze phase 0-9"},
    {"goal": "analyze phase 10-19"},
    {"goal": "analyze phase 20-28"}
]
```

---

### Issue: Verification always fails

**Symptoms:** All iterations fail verification

**Causes:**
1. Verification rules impossible to satisfy
2. Output format mismatch
3. Bug in verification logic

**Solutions:**
1. Review verification rules
2. Log output to see actual format
3. Add debug logging to verifier

**Example:**
```python
def verify_work(self, output, context, task):
    # Add logging
    logger.debug(f"Verifying output: {output}")
    logger.debug(f"Expected format: {task.get('expected_format')}")

    # Check output format
    if not isinstance(output, dict):
        return {
            "passed": False,
            "message": f"Expected dict, got {type(output).__name__}",
            "how_to_fix": "Return a dictionary instead"
        }

    # Rest of verification...
```

---

## 📊 PERFORMANCE TIPS

### 1. Use Subagents for I/O-Bound Tasks

**Speedup:** 2-5x for independent I/O tasks

```python
# Parallel I/O operations
tasks = [
    {"goal": "fetch API data"},
    {"goal": "read large files"},
    {"goal": "query database"}
]
subagent_ids = orchestrator.spawn_parallel(tasks, ...)
```

### 2. Keep Subagent Results Small

**Speedup:** Better context efficiency

```python
# Return only what's needed
return {
    "summary": "Found 10 matches",
    "top_3": [match1, match2, match3]
    # NOT: "all_data": massive_list
}
```

### 3. Use Agentic Search Over Semantic Search

**Speedup:** Faster for most cases, more accurate

```python
# Agentic search (bash commands)
search.search_phases("guardrails")  # Fast, accurate

# Only add semantic search if:
# - Need fuzzy matching
# - Very large datasets
# - Speed critical for queries
```

### 4. Compact Context Proactively

**Speedup:** Prevents expensive overflows

```python
context = ContextManager(
    max_tokens=100000,
    compact_threshold=0.7  # Compact early to avoid emergency compaction
)
```

---

## 🎉 CONCLUSION

You now have a complete understanding of the SwarmCare Agent Framework!

**Key Takeaways:**
1. **Always use the feedback loop** - it's the foundation of reliable agents
2. **Learn from failures** - pass iteration_log to context gatherer
3. **Use subagents** for parallelization and context isolation
4. **Verify rigorously** - rules-based is best, combine methods
5. **Manage context** - enable auto-compaction for long tasks

**Next Steps:**
1. Study `phases/phase00/code/implementation_enhanced.py` for complete example
2. Read `ANTHROPIC_AGENT_SDK_ANALYSIS_REPORT.md` for detailed comparison
3. Run tests: `python3 tests/agent_framework/test_*.py`
4. Start implementing your own agents!

**Need Help?**
- Check `TROUBLESHOOTING` section above
- Review API Reference
- Read Anthropic's article: https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk

---

**Last Updated:** 2025-10-27
**Version:** 1.0.0
**Status:** Production Ready ✅
