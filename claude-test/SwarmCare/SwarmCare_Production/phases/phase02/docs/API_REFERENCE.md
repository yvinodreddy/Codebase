# Phase 02: SWARMCARE Agents - API Reference

**Version:** 2.1
**Last Updated:** 2025-10-28

## Table of Contents

1. [Phase02Implementation Class](#phase02implementation-class)
2. [Agent Initialization Methods](#agent-initialization-methods)
3. [Execution Methods](#execution-methods)
4. [Validation Methods](#validation-methods)
5. [Utility Methods](#utility-methods)
6. [Agent Schemas](#agent-schemas)
7. [Examples](#examples)

---

## Phase02Implementation Class

Main implementation class for Phase 02 SWARMCARE Agents.

### Constructor

```python
Phase02Implementation()
```

**Description:** Initializes Phase 02 with all 6 agents and agent framework components.

**Attributes:**
- `phase_id` (int): Phase identifier (2)
- `phase_name` (str): "SWARMCARE Agents"
- `story_points` (int): 94
- `priority` (str): "P0"
- `description` (str): "6 AI agents: Knowledge, Case, Conversation, Compliance, Podcast, QA"
- `status` (str): Current phase status
- `framework_version` (str): "100%"

**Framework Components:**
- `guardrails`: MultiLayerGuardrailSystem instance
- `feedback_loop`: AdaptiveFeedbackLoop instance
- `context`: ContextManager instance
- `orchestrator`: SubagentOrchestrator instance
- `search`: AgenticSearch instance
- `verifier`: MultiMethodVerifier instance

**Example:**
```python
from implementation import Phase02Implementation

phase = Phase02Implementation()
print(f"Phase {phase.phase_id}: {phase.phase_name}")
print(f"Story Points: {phase.story_points}")
```

---

## Agent Initialization Methods

### _initialize_knowledge_agent()

```python
def _initialize_knowledge_agent(self) -> dict
```

**Description:** Initializes the Knowledge Agent for medical knowledge retrieval.

**Returns:** Dictionary containing agent configuration

**Schema:**
```python
{
    "name": str,
    "type": str,
    "description": str,
    "capabilities": list[str],
    "integrations": list[str],
    "guardrails": list[str],
    "status": str,
    "performance_sla": str
}
```

**Example:**
```python
phase = Phase02Implementation()
knowledge_agent = phase._initialize_knowledge_agent()

print(knowledge_agent["name"])  # "Knowledge Agent"
print(knowledge_agent["capabilities"])  # List of capabilities
```

---

### _initialize_case_agent()

```python
def _initialize_case_agent(self) -> dict
```

**Description:** Initializes the Case Agent for patient case analysis.

**Returns:** Dictionary containing agent configuration

**Key Capabilities:**
- Patient case summarization
- Medical history analysis
- Clinical note generation
- EHR data extraction
- Care plan recommendations

**Example:**
```python
case_agent = phase._initialize_case_agent()
print(case_agent["type"])  # "case_analysis"
print(case_agent["performance_sla"])  # "< 3s for case analysis"
```

---

### _initialize_conversation_agent()

```python
def _initialize_conversation_agent(self) -> dict
```

**Description:** Initializes the Conversation Agent for natural language interactions.

**Returns:** Dictionary containing agent configuration

**Key Features:**
- Natural language understanding
- Multi-turn conversation management
- Context-aware responses
- Medical terminology translation

**Example:**
```python
conversation_agent = phase._initialize_conversation_agent()
print(conversation_agent["performance_sla"])  # "< 1s for conversational responses"
```

---

### _initialize_compliance_agent()

```python
def _initialize_compliance_agent(self) -> dict
```

**Description:** Initializes the Compliance Agent for regulatory compliance.

**Returns:** Dictionary containing agent configuration

**Key Capabilities:**
- HIPAA compliance verification
- PHI detection and protection
- Audit trail generation
- Security policy enforcement

**Example:**
```python
compliance_agent = phase._initialize_compliance_agent()
print(compliance_agent["guardrails"])  # ["strict_phi_protection", "access_control", ...]
```

---

### _initialize_podcast_agent()

```python
def _initialize_podcast_agent(self) -> dict
```

**Description:** Initializes the Podcast Agent for medical podcast generation.

**Returns:** Dictionary containing agent configuration

**Key Capabilities:**
- EHR-to-narrative conversion
- Medical content scripting
- Multi-voice dialogue generation
- Clinical insight summarization

**Example:**
```python
podcast_agent = phase._initialize_podcast_agent()
print(podcast_agent["type"])  # "content_generation"
```

---

### _initialize_qa_agent()

```python
def _initialize_qa_agent(self) -> dict
```

**Description:** Initializes the QA Agent for quality assurance.

**Returns:** Dictionary containing agent configuration

**Key Capabilities:**
- AI output validation
- Medical accuracy verification
- Clinical guideline compliance
- Error detection and correction

**Example:**
```python
qa_agent = phase._initialize_qa_agent()
print(qa_agent["performance_sla"])  # "< 500ms for validation checks"
```

---

## Execution Methods

### execute()

```python
def execute(self, task: dict) -> object
```

**Description:** Main execution method with 100% agent framework integration.

**Parameters:**
- `task` (dict): Task specification
  - `goal` (str): Task goal/description
  - `phase_id` (int): Phase identifier

**Returns:** Result object with attributes:
- `success` (bool): Execution success status
- `output` (dict): Phase output data
- `iterations` (int): Number of iterations
- `total_duration_seconds` (float): Execution time
- `error` (str, optional): Error message if failed

**Example:**
```python
task = {
    "goal": "Implement SWARMCARE Agents",
    "phase_id": 2
}

result = phase.execute(task)

if result.success:
    print("✅ Success!")
    print(f"Agents created: {result.output['components']['total_agents']}")
else:
    print(f"❌ Failed: {result.error}")
```

---

### gather_context()

```python
def gather_context(self, task: dict, iteration_log: list) -> dict
```

**Description:** Gathers context for phase execution with learning from failures.

**Parameters:**
- `task` (dict): Task specification
- `iteration_log` (list): Previous iteration logs

**Returns:** Dictionary containing gathered context

**Example:**
```python
task = {"goal": "Implement agents", "phase_id": 2}
context = phase.gather_context(task, [])
print(context)
```

---

### take_action()

```python
def take_action(self, task: dict, context: dict) -> dict
```

**Description:** Executes phase implementation with given context.

**Parameters:**
- `task` (dict): Task specification
- `context` (dict): Execution context

**Returns:** Dictionary containing implementation output

**Output Schema:**
```python
{
    "phase_id": int,
    "phase_name": str,
    "story_points": int,
    "priority": str,
    "status": str,
    "components": {
        "agents": dict,
        "validation": dict,
        "total_agents": int,
        "framework_integration": str
    },
    "agent_framework_version": str,
    "timestamp": str
}
```

**Example:**
```python
output = phase.take_action(task, context)
print(output["components"]["total_agents"])  # 6
```

---

### verify_work()

```python
def verify_work(self, output: dict, context: dict, task: dict) -> dict
```

**Description:** Multi-method verification of phase output.

**Parameters:**
- `output` (dict): Phase output to verify
- `context` (dict): Execution context
- `task` (dict): Original task

**Returns:** Dictionary containing verification results
```python
{
    "passed": bool,
    "message": str
}
```

**Example:**
```python
verification = phase.verify_work(output, context, task)
if verification["passed"]:
    print("✅ Verification passed")
```

---

## Validation Methods

### _validate_all_agents()

```python
def _validate_all_agents(self, agents: dict) -> dict
```

**Description:** Validates all agents are properly initialized.

**Parameters:**
- `agents` (dict): Dictionary of agent configurations

**Returns:** Validation results dictionary

**Validation Schema:**
```python
{
    "all_agents_initialized": bool,
    "agent_count": int,
    "expected_count": int,
    "agents_validated": [
        {
            "agent": str,
            "valid": bool,
            "status": str
        },
        ...
    ],
    "all_passed": bool
}
```

**Required Fields Per Agent:**
- name
- type
- description
- capabilities
- integrations
- guardrails
- status

**Example:**
```python
agents = {
    "knowledge": phase._initialize_knowledge_agent(),
    "case": phase._initialize_case_agent(),
    # ... other agents
}

validation = phase._validate_all_agents(agents)
print(f"All passed: {validation['all_passed']}")
print(f"Agent count: {validation['agent_count']}/6")
```

---

## Utility Methods

### get_stats()

```python
def get_stats(self) -> dict
```

**Description:** Retrieves execution statistics.

**Returns:** Dictionary containing phase statistics

**Schema:**
```python
{
    "phase_id": int,
    "phase_name": str,
    "story_points": int,
    "status": str,
    "framework_version": str
}
```

**Example:**
```python
stats = phase.get_stats()
print(f"Status: {stats['status']}")
print(f"Framework: {stats['framework_version']}")
```

---

### _update_phase_state()

```python
def _update_phase_state(self, status: str, result: object) -> None
```

**Description:** Updates phase state JSON file.

**Parameters:**
- `status` (str): Phase status
- `result` (object): Execution result

**Side Effects:** Writes to `.state/phase_state.json`

**State Schema:**
```python
{
    "phase_id": int,
    "phase_name": str,
    "story_points": int,
    "priority": str,
    "status": str,
    "success": bool,
    "agent_framework_version": str,
    "updated_at": str
}
```

---

## Agent Schemas

### Generic Agent Schema

All agents follow this structure:

```python
{
    "name": str,                    # Agent name
    "type": str,                    # Agent type
    "description": str,             # Detailed description
    "capabilities": list[str],      # List of capabilities
    "integrations": list[str],      # Integration points
    "guardrails": list[str],        # Applied guardrails
    "status": str,                  # Current status
    "performance_sla": str          # Performance SLA
}
```

### Agent Types

- `knowledge_retrieval` - Knowledge Agent
- `case_analysis` - Case Agent
- `natural_language` - Conversation Agent
- `regulatory_compliance` - Compliance Agent
- `content_generation` - Podcast Agent
- `quality_assurance` - QA Agent

---

## Examples

### Complete Workflow Example

```python
#!/usr/bin/env python3
from implementation import Phase02Implementation
import json

# 1. Initialize phase
print("Initializing Phase 02...")
phase = Phase02Implementation()

# 2. Check initial stats
stats = phase.get_stats()
print(f"Phase: {stats['phase_name']}")
print(f"Story Points: {stats['story_points']}")

# 3. Execute phase
print("\nExecuting phase...")
task = {
    "goal": "Implement SWARMCARE Agents",
    "phase_id": 2
}

result = phase.execute(task)

# 4. Check results
if result.success:
    print("\n✅ Phase 02 completed successfully!")

    output = result.output
    print(f"Phase ID: {output['phase_id']}")
    print(f"Status: {output['status']}")
    print(f"Total Agents: {output['components']['total_agents']}")

    # 5. Examine agents
    agents = output['components']['agents']
    for agent_name, agent_config in agents.items():
        print(f"\n{agent_name.upper()} Agent:")
        print(f"  Type: {agent_config['type']}")
        print(f"  SLA: {agent_config['performance_sla']}")
        print(f"  Status: {agent_config['status']}")

    # 6. Check validation
    validation = output['components']['validation']
    print(f"\nValidation:")
    print(f"  All Passed: {validation['all_passed']}")
    print(f"  Agent Count: {validation['agent_count']}/6")

else:
    print(f"\n❌ Phase 02 failed: {result.error}")

# 7. Final stats
final_stats = phase.get_stats()
print(f"\nFinal Status: {final_stats['status']}")
```

### Individual Agent Testing

```python
# Test individual agents
from implementation import Phase02Implementation

phase = Phase02Implementation()

# Test Knowledge Agent
knowledge = phase._initialize_knowledge_agent()
assert knowledge["name"] == "Knowledge Agent"
assert knowledge["status"] == "initialized"
print("✅ Knowledge Agent OK")

# Test Case Agent
case = phase._initialize_case_agent()
assert "HIPAA" in str(case["guardrails"])
print("✅ Case Agent OK")

# Test all agents
agents = {
    "knowledge": phase._initialize_knowledge_agent(),
    "case": phase._initialize_case_agent(),
    "conversation": phase._initialize_conversation_agent(),
    "compliance": phase._initialize_compliance_agent(),
    "podcast": phase._initialize_podcast_agent(),
    "qa": phase._initialize_qa_agent()
}

validation = phase._validate_all_agents(agents)
assert validation["all_passed"]
print(f"✅ All {validation['agent_count']} agents validated")
```

---

## Error Handling

### Common Errors

**ImportError: Framework not available**
```python
# Framework gracefully degrades
if FRAMEWORK_AVAILABLE:
    # Use full framework
else:
    # Use basic implementation
```

**Validation Failure**
```python
result = phase.execute(task)
if not result.success:
    print(f"Error: {result.error}")
    # Check logs for details
```

### Best Practices

1. Always check `result.success` before accessing output
2. Use try-except for robust error handling
3. Monitor logs for warnings
4. Validate agents after initialization
5. Test in development before production

---

**Version:** 2.1
**Status:** Production-Ready ✅
**Last Updated:** 2025-10-28
