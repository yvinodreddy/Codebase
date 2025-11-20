# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with the ULTRATHINK orchestration system.

## ⛔ CRITICAL - PERMANENT RULE - NEVER VIOLATE ⛔

**NEVER USE CLAUDE API - NO EXCEPTIONS**

This is a MANDATORY, PERMANENT, NON-NEGOTIABLE rule:

1. ❌ **NEVER enable Claude API** (no `--api` flag)
2. ❌ **NEVER add ANTHROPIC_API_KEY** to .bashrc
3. ❌ **NEVER make API calls** that incur charges
4. ❌ **NEVER suggest using API mode**
5. ❌ **NEVER change code to use API by default**

**WHY:**
- API charges money ($0.003-0.015 per request)
- User pays $200/month for Claude Code (already included)
- Using API = paying twice for the same service
- User explicitly removed API key to prevent charges

**WHAT TO USE INSTEAD:**
- ✅ Claude Code mode (default) - NO CHARGES
- ✅ Display enhanced prompts to Claude Code
- ✅ Claude Code executes with full file access
- ✅ All included in $200/month subscription

**IF ANYONE SUGGESTS USING API:**
Respond: "NO. We use Claude Code mode only. No API charges allowed. This is permanent."

This rule is RECORDED and PERMANENT. Do not violate it.

## ⏱️ TIME LIMITS AND EXECUTION CONSTRAINTS

**CRITICAL UNDERSTANDING - NO TIME LIMITS FOR CLAUDE CODE:**

Claude Code operates under a $200/month subscription model with the following constraints:

### ✅ What Claude Code HAS:
- **NO time limits** for completing requests
- **NO artificial deadlines** for implementation
- **UNLIMITED iterations** for refinement and perfection
- **200,000 token context window** per request
- **Full autonomous execution** capability

### ❌ What Claude Code DOES NOT HAVE:
- ❌ **NO time constraints** - Can work on tasks for as long as needed
- ❌ **NO execution timeouts** - Individual commands have timeouts (2-10 min) but can be retried
- ❌ **NO implementation shortcuts** - Every feature must be 100% complete
- ❌ **NO "due to time limitations" excuses** - This phrase is BANNED

### 🎯 Implementation Standards:

When user requests features:

1. **ALWAYS implement to 100% completion**
   - Never cite "time constraints" as reason for incomplete work
   - Never leave features partially implemented
   - Never skip requirements due to perceived complexity

2. **For large tasks, use task decomposition**
   - Break into smaller, manageable subtasks
   - Use TodoWrite tool to track progress
   - Execute subtasks sequentially or in parallel
   - Report completion status after each subtask

3. **For extremely large tasks (100+ subtasks)**
   - Ask user if they want to split into multiple phases
   - Provide clear breakdown of what each phase includes
   - Get user confirmation on phasing approach
   - Execute each phase to 100% completion

4. **Command Timeouts (Technical Limitation)**
   - Individual bash commands: 2-minute default, 10-minute maximum
   - Long-running processes: Run in background with BashOutput monitoring
   - Builds/tests: Use background execution with progress checks
   - These are TECHNICAL constraints, not time constraint excuses

### 📋 Task Decomposition Example:

**BAD (Old Approach):**
```
User: Implement features A, B, C, D, E
Claude: ⚠️ Implemented A and B. Features C, D, E not implemented due to time limitations.
```

**GOOD (Correct Approach):**
```
User: Implement features A, B, C, D, E
Claude: Creating todo list with 5 tasks...
[Task 1/5] Implementing Feature A... ✅ Complete
[Task 2/5] Implementing Feature B... ✅ Complete
[Task 3/5] Implementing Feature C... ✅ Complete
[Task 4/5] Implementing Feature D... ✅ Complete
[Task 5/5] Implementing Feature E... ✅ Complete
All 5 features implemented to 100% completion.
```

### 🚫 BANNED PHRASES:

The following phrases are PERMANENTLY BANNED and must NEVER be used:
- ❌ "Due to time limitations"
- ❌ "Due to time constraints"
- ❌ "Not enough time to implement"
- ❌ "Would require more time"
- ❌ "Time constraints prevented implementation"

### ✅ CORRECT ALTERNATIVES:

Instead, use:
- ✅ "Implementation complete for all requested features"
- ✅ "Breaking down into N subtasks for systematic execution"
- ✅ "This is a large task - would you like me to implement in phases?"
- ✅ "Executing all N features sequentially with progress updates"

### 📝 Documentation Requirement:

This time limit policy must be present in:
- ✅ /home/user01/claude-test/CLAUDE.md - Global rules
- ✅ /home/user01/claude-test/ClaudePrompt/CLAUDE.md (this file) - ULTRATHINK project rules
- ✅ /home/user01/claude-test/ClaudePrompt/web-ui-implementation/.claude_docs/DEVELOPMENT_STANDARDS.md

All three files MUST contain consistent messaging about:
1. NO time limits for Claude Code
2. 100% completion requirement for all features
3. Task decomposition for large requests
4. Banned phrases list
5. Correct alternatives

This is a PERMANENT, NON-NEGOTIABLE standard effective 2025-11-14 and forever.

---

## 📊 PERMANENT METRICS COMPARISON TABLE

**MANDATORY REQUIREMENT - EFFECTIVE 2025-11-20**

### Critical Rule: Display 3-Way Comparison on EVERY Execution

Every `cpp` command execution MUST display the permanent metrics comparison table showing:

1. **Claude Code (Baseline)** - Standard Claude Code without enhancements
2. **cpps (Before Metrics)** - ULTRATHINK v1.0 before industry metrics implementation
3. **cpps (After Metrics)** - ULTRATHINK v2.0 with all enhancements (current)

### Why This Matters

This comparison demonstrates:
- ✅ **Value delivered**: Shows +12.3% confidence improvement (87% → 99.3%)
- ✅ **ROI visibility**: Quantifies \$500K-\$2M annual savings
- ✅ **Feature tracking**: Documents all 8 guardrail layers, database backing, metrics
- ✅ **Progress evidence**: User sees improvements every execution
- ✅ **Decision validation**: Proves enhancements are working as intended

### Implementation

The comparison table is:
- **Automatically displayed** on every cpp execution
- **Stored in output files** for permanent record
- **Non-optional** - MANDATORY for all executions
- **Production-ready** - Fully implemented in ultrathink.py

### Metrics Tracked

The 3-way comparison shows 8 categories:
1. Confidence Score (Target, Achieved, Delta)
2. Validation Layers (Input, Output, Total, Coverage)
3. Context Management (Capacity, Database, Retrieval)
4. Verification Methods (Available, Multi-method, Score)
5. Latency & Performance (Time, Regression, Bottlenecks)
6. Failure Resilience (Chaos, Database, Agents, Recovery)
7. Test Coverage (Context Manager, Critical Paths, Edge Cases)
8. Quality Metrics (Bug Detection, Multi-Compaction, Success Rate)

### Example Output

Every cpp execution will show:
```
================================================================================
📊 PERFORMANCE METRICS COMPARISON - YOUR IMPROVEMENT TRACKING
================================================================================

┌──────────────────────────────────────────────────────────────────────────┐
│                    3-WAY FRAMEWORK COMPARISON                            │
├──────────────────────────────────────────────────────────────────────────┤
│ Metric                │ Claude Code │ cpps (Before) │ cpps (After)    │
│                       │ (Baseline)  │ (v1.0)        │ (Current v2.0)  │
├───────────────────────┼─────────────┼───────────────┼─────────────────┤
│ 1. CONFIDENCE SCORE   │    87%      │    96%        │    99.3%       ✓│
│ 2. VALIDATION LAYERS  │    0        │    7          │    8           ✓│
│ 3. CONTEXT MANAGEMENT │    200K     │    200K       │    Unlimited   ✓│
│ ... [8 categories total showing comprehensive improvements]             │
└──────────────────────────────────────────────────────────────────────────┘

ROI: \$500K-\$2M annual savings (99% reduction in production incidents)
```

### Documentation Requirements

This requirement must be present in:
- ✅ /home/user01/claude-test/ClaudePrompt/CLAUDE.md (this file)
- ✅ /home/user01/claude-test/CLAUDE.md (root level)
- ✅ ultrathink.py (implemented in generate_3way_metrics_comparison() function)

### Enforcement

This is:
- **MANDATORY** - Cannot be disabled or removed
- **NON-NEGOTIABLE** - User explicitly requested as critical requirement
- **PERMANENT** - Effective 2025-11-20 and forever
- **PRODUCTION-READY** - Fully tested and validated

**DO NOT remove or modify this requirement without explicit user authorization.**

---

## Overview

This directory contains the ULTRATHINK system - an advanced orchestration framework for Claude API integration with:
- Multi-layer guardrails (7 layers)
- Adaptive feedback loops
- Context management (200K tokens)
- Verification systems
- Rate limiting and security enhancements

## ⚠️ CRITICAL: ULTRATHINK COMMAND EXECUTION PROTOCOL

**MANDATORY BEHAVIOR - ALWAYS FOLLOW THIS BASED ON WHICH COMMAND USER SENDS:**

There are TWO separate ULTRATHINK systems that are FULLY ISOLATED:
- **TestPrompt**: Commands `ultrathinkc` or `uc` → `/tmp/ultrathink_output.txt`
- **ClaudePrompt**: Command `cpp` → Timestamped output files

Each has its OWN output file, answer_to_file.py script, and directory.

---

### 📌 PRIMARY PROTOCOL FOR `cpp` (ClaudePrompt - THIS DIRECTORY)

**⚠️ CRITICAL - DEFAULT BEHAVIOR AS OF 2025-11-12:**
**ALL cpp executions now use TIMESTAMPED OUTPUT by default!**

#### **DEFAULT METHOD: Timestamped Output (ALWAYS USE THIS)**

When the user sends a message with `cpp` command:

1. **Run the command** with timestamped output:
   ```bash
   OUTPUT_FILE=$(python3 get_output_path.py)
   ./cpp "prompt" --verbose 2>&1 > "$OUTPUT_FILE"
   ```

   Or with track number for parallel execution:
   ```bash
   OUTPUT_FILE=$(python3 get_output_path.py --track 1)
   ./cpp "prompt" --verbose 2>&1 > "$OUTPUT_FILE"
   ```

2. **Output file will be automatically timestamped**:
   - Format: `/home/user01/claude-test/ClaudePrompt/tmp/cppultrathink_output_YYYYMMDD_HHMMSS_mmm.txt`
   - With track: `/home/user01/claude-test/ClaudePrompt/tmp/cppultrathink_output_track1_YYYYMMDD_HHMMSS_mmm.txt`

3. **Generate your answer** to the user's question (apply all ULTRATHINK directives, guardrails, verification)

4. **Append your answer to the file** using this command:
   ```bash
   python3 /home/user01/claude-test/ClaudePrompt/answer_to_file.py "$OUTPUT_FILE" "Your complete answer here with all details, validation, confidence scores, etc."
   ```

5. **Tell the user** to read the timestamped file from top to bottom

6. **Also display your answer** in the chat (with fire emoji boxes) for immediate visibility

**Output file location:** `/home/user01/claude-test/ClaudePrompt/tmp/cppultrathink_output_{timestamp}.txt`

**THIS IS THE DEFAULT - USE THIS FOR EVERY cpp EXECUTION**

---

#### **LEGACY METHOD: /tmp/ Output (ONLY if user explicitly requests it)**

⚠️ DO NOT USE THIS UNLESS USER EXPLICITLY ASKS FOR /tmp/ PATH

For backward compatibility only:

1. **Run the command** using Bash tool: `cpp "prompt" --verbose 2>&1 > /tmp/cppultrathink_output.txt`
2. **Generate your answer** to the user's question (apply all ULTRATHINK directives, guardrails, verification)
3. **Append your answer to the file** using this command:
   ```bash
   python3 /home/user01/claude-test/ClaudePrompt/answer_to_file.py /tmp/cppultrathink_output.txt "Your complete answer here with all details, validation, confidence scores, etc."
   ```
4. **Tell the user** to read `/tmp/cppultrathink_output.txt` from top to bottom
5. **Also display your answer** in the chat (with fire emoji boxes) for immediate visibility

**Output file location (legacy):** `/tmp/cppultrathink_output.txt`

**ONLY USE IF:** User explicitly requests /tmp/ path

---

#### **Which Method to Use?**

- **✅ ALWAYS USE Timestamped Output (Default)** for:
  - ALL cpp executions (single or parallel)
  - Every use case unless user says otherwise
  - Preserves complete history forever
  - Prevents file conflicts in parallel execution

- **❌ ONLY USE Legacy /tmp/ Output** when:
  - User explicitly requests /tmp/ path
  - User says "use legacy mode"

---

### 📌 ALTERNATIVE PROTOCOL FOR `ultrathinkc` or `uc` (TestPrompt)

When the user sends a message containing an `ultrathinkc` command or `uc` command (e.g., `uc "prompt" -v`):

1. **Run the command** using Bash tool: `ultrathinkc "prompt" --verbose 2>&1 > /tmp/ultrathink_output.txt`
2. **Generate your answer** to the user's question (apply all ULTRATHINK directives, guardrails, verification)
3. **Append your answer to the file** using this command:
   ```bash
   python3 /home/user01/claude-test/TestPrompt/answer_to_file.py /tmp/ultrathink_output.txt "Your complete answer here with all details, validation, confidence scores, etc."
   ```
4. **Tell the user** to read `/tmp/ultrathink_output.txt` from top to bottom
5. **Also display your answer** in the chat (with fire emoji boxes) for immediate visibility

**Output file location:** `/tmp/ultrathink_output.txt`

---

### ⚠️ CRITICAL: DO NOT MIX THEM UP!

| Command | Output File | answer_to_file.py Location |
|---------|-------------|----------------------------|
| `cpp` (DEFAULT) | `ClaudePrompt/tmp/cppultrathink_output_{timestamp}.txt` ⭐ | `/home/user01/claude-test/ClaudePrompt/answer_to_file.py` |
| `cpp` (legacy - only if requested) | `/tmp/cppultrathink_output.txt` | `/home/user01/claude-test/ClaudePrompt/answer_to_file.py` |
| `ultrathinkc` or `uc` | `/tmp/ultrathink_output.txt` | `/home/user01/claude-test/TestPrompt/answer_to_file.py` |

**⭐ DEFAULT:** Always use timestamped output for `cpp` unless user explicitly asks for /tmp/ path

**The file will contain:**
- Part 1: ULTRATHINK system output (all [VERBOSE] stages, guardrails, metrics)
- Part 2: YOUR ANSWER (appended at the end with clear visual markers ⬇️⬇️⬇️)

**This way the user can:**
- ✅ Read the complete file from top to bottom without scrolling in chat
- ✅ See all verbose system processing details
- ✅ Find the answer at the bottom with clear markers
- ✅ No need to scroll through chat messages

**User wants to see in THE FILE:**
- All [VERBOSE] tags
- All 6 STAGE headers
- All 8 Guardrail Layers (Layers 1-8)
- Context Management details
- Agent Components
- Iteration details
- Quality Scoring
- Framework Comparison with Delta Analysis table
- YOUR COMPLETE ANSWER (at the end, after the fire box marker)

This is a PERMANENT requirement for ALL sessions/windows.

## CRITICAL: Response Formatting Standards

**ALL Claude Code responses to ULTRATHINK prompts MUST follow this format:**

### Section Headers
```
================================================================================
SECTION NAME
================================================================================
```
- Use EXACTLY 80 equals signs (=) for headers
- Optional emoji prefix (🎯, 📊, ✅, 🔍, etc.)
- One blank line before and after header
- Title in ALL CAPS or Title Case (be consistent)

### Content Structure
```
[VERBOSE] Main point
[VERBOSE]   ✓ Sub-item (exactly 3-space indent, NOT 2, NOT 4)
[VERBOSE]   ✓ Another sub-item

Explanatory text here with proper spacing.

---

Next major item, clearly separated.
```

### Spacing Rules (CRITICAL FOR READABILITY)
- **1 blank line** between subsections
- **1 blank line** between paragraphs
- **1 blank line** before/after section headers
- **1 blank line** before/after `---` separators
- **1 blank line** before/after code blocks
- **1 blank line** before/after tables
- **3-space indentation** for [VERBOSE] sub-items (not 2, not 4)

### Code Blocks
```language
code here
```
- ALWAYS specify language (python, bash, javascript, etc.)
- Indent consistently within block
- Add brief description BEFORE code block
- One blank line before and after

### Tables
| Column 1      | Column 2      |
|---------------|---------------|
| Data          | Data          |

- Use markdown table format
- Align columns with `|` separators
- One blank line before and after
- Use for comparisons, structured data

### Visual Elements
- **Bold** for important terms (sparingly)
- `code style` for file names, variables, commands
- ✅ Success indicators
- ❌ Error indicators
- 🟡 Warning indicators
- ✓ Checkmarks for completed items
- `---` for horizontal separators between major sections

### Why This Matters
This format was developed based on user feedback over multiple sessions:
1. Enhances readability for large text volumes
2. Maintains reader concentration and interest
3. Creates clean visual hierarchy
4. Makes information easy to scan and comprehend
5. Professional terminal-style appearance

**DO NOT use cramped markdown-heavy formatting.** The clean, spaced ULTRATHINK format is MANDATORY.

## File Organization

Key files:
- `ultrathink.py` - Main CLI interface
- `master_orchestrator.py` - Core orchestration logic
- `claude_integration.py` - Claude API integration with rate limiting
- `config.py` - Centralized configuration
- `result_pattern.py` - Result<T, E> error handling pattern
- `agent_framework/` - Agent execution framework
- `guardrails/` - 7-layer validation system
- `security/` - Input sanitization and security tools

## Development Workflow

When running ULTRATHINK commands:
```bash
cpp "your prompt here" --verbose
```

The system will:
1. Show [VERBOSE] preprocessing stages (STAGE 1-6)
2. Display enhanced ULTRATHINK prompt
3. Claude Code responds with properly formatted analysis
4. All responses follow the formatting standards above

## Response Format Commitment

This formatting standard is PERMANENT and applies to:
- ✅ ALL ULTRATHINK responses
- ✅ ALL sessions (even after restart)
- ✅ ALL prompts processed through cpp
- ✅ NOW and FOREVER

User invested significant time developing this format. It must be respected and maintained.

================================================================================
⚠️ MANDATORY VALIDATION PROTOCOL - CRITICAL
================================================================================

**THIS IS THE MOST IMPORTANT SECTION - READ CAREFULLY**

When responding to ANY ULTRATHINK prompt, you MUST follow this validation protocol.
This is NOT optional. This is NOT negotiable. This is MANDATORY.

### Why This Exists

Normal Claude Code responses have ~85% accuracy.
ULTRATHINK requires 99-100% accuracy through systematic validation.
User pays $200/month for Claude Code - we use that, not API calls.

### The Validation Loop

For EVERY response you generate, you MUST:

1. **Generate Draft Response**
   - Create your initial response to the user's prompt
   - Store it in a variable (don't show to user yet)

2. **Validate Draft**
   ```bash
   python3 /home/user01/claude-test/ClaudePrompt/validate_my_response.py \
     "your draft response here" \
     --prompt "original user prompt" \
     --iteration 1
   ```

3. **Check Confidence Score**
   - Parse the JSON output
   - Check `"is_acceptable": true/false`
   - Check `"confidence": X.X` (target: 99.0+)

4. **If NOT Acceptable (confidence < 99%)**
   - Read `"suggestions"` array from validation output
   - Refine your response based on suggestions
   - Repeat steps 2-4 (increment --iteration)
   - Maximum 20 iterations (config.py: MAX_REFINEMENT_ITERATIONS = 20)

5. **If Acceptable (confidence >= 99%)**
   - Show final validated response to user
   - Include confidence score in output

### Example Workflow

```
User asks: "What is 2+2?"

[ITERATION 1]
Draft: "4"
Validate: confidence 87.5%, suggestions: ["Response too brief - add more context"]

[ITERATION 2]
Draft: "The answer is 4 because 2+2 equals 4 in standard arithmetic."
Validate: confidence 94.2%, suggestions: ["Add mathematical context"]

[ITERATION 3]
Draft: "The mathematical sum of 2+2 equals 4. This follows the commutative
       property of addition where a+b = b+a, and represents combining two
       groups of 2 objects into a single group of 4 objects."
Validate: confidence 99.3%, is_acceptable: true ✅

Show to user: [Final response] (Confidence: 99.3%)
```

### Verbose Mode

If user includes `--verbose` flag:
- Show ALL iterations and confidence scores
- Display validation details
- Use [VERBOSE] tags to show process

Without `--verbose`:
- Only show final validated response
- Include final confidence score

### Critical Rules

1. **NEVER skip validation** - Even for simple questions
2. **ALWAYS iterate until 99%+** - Or maximum 20 iterations
3. **ALWAYS use Bash tool** - To call validate_my_response.py
4. **ALWAYS parse JSON output** - To check is_acceptable flag
5. **ALWAYS show confidence score** - In final response

### Failure Handling

If 20 iterations reached without 99%+:
- Show best attempt (highest confidence achieved)
- Warn user: "⚠️ Could not reach 99% confidence after 20 iterations"
- Show highest confidence: "Best achieved: XX.X%"
- Ask if user wants manual review

### Implementation Details

**Location of validation tool**:
```
/home/user01/claude-test/ClaudePrompt/validate_my_response.py
```

**What it validates**:
- All 7 guardrail layers (Layers 1-7)
- Multi-method verification
- Response quality metrics
- Combined confidence scoring (60% guardrails, 40% verification)

**Output format** (JSON):
```json
{
  "iteration": 1,
  "confidence": 87.5,
  "target_confidence": 99.0,
  "is_acceptable": false,
  "suggestions": ["Add more detail", "Include examples"],
  "guardrails": {"passed": true, "confidence": 85.0},
  "verification": {"passed": true, "confidence": 92.0}
}
```

### Memory Persistence

This protocol is stored in:
- ✅ CLAUDE.md (this file) - Read at session start
- ✅ .clinerules - Additional enforcement layer
- ✅ config.py - Configuration values (iterations, thresholds)
- ✅ FORMAT_TEMPLATE.md - Response format standards

These files ensure validation protocol survives:
- ✅ Window close
- ✅ Computer restart
- ✅ New sessions
- ✅ Context compaction

### Commitment

This validation protocol is PERMANENT and MANDATORY.
Effective: 2025-11-09 and forever.
Reason: User requires 99-100% accuracy, not 85%.
Cost: $200/month Claude Code subscription (already paid).

**YOU MUST VALIDATE EVERY RESPONSE. NO EXCEPTIONS.**

================================================================================
## 🧪 MANDATORY TESTING STANDARDS - 100% COVERAGE REQUIREMENT
================================================================================

**CRITICAL, MANDATORY, NON-NEGOTIABLE, NO EXCEPTIONS**
**Effective:** 2025-11-20 and FOREVER
**Enforcement:** AUTOMATED (pre-commit hooks + CI/CD blocks)

---

### CORE PRINCIPLE

**EVERY Python file MUST have corresponding test file with 90%+ coverage.**

This is NOT optional. This is NOT negotiable. This is PERMANENT.

---

### THE RULE

When creating OR modifying ANY Python file:

1. **Test File MUST be created/updated IMMEDIATELY**
   - Source file: `module/feature.py`
   - Test file: `tests/unit/test_feature.py` OR `tests/integration/test_feature_integration.py`

2. **Test Coverage MUST be ≥ 90%**
   - Run: `pytest tests/unit/test_feature.py --cov=module/feature.py --cov-fail-under=90`
   - MUST pass before commit
   - CI/CD blocks merge if coverage < 90%

3. **Tests MUST use REAL CODE (not just mocks)**
   - Import actual functions/classes
   - Mock ONLY external dependencies (APIs, databases, file I/O)
   - Test actual code execution paths
   - Validate real behavior

---

### WHAT IS ACCEPTABLE vs UNACCEPTABLE

**❌ UNACCEPTABLE (Mock-based test):**
```python
def test_calculate_sum():
    with patch('math_utils.calculate_sum') as mock_func:
        mock_func.return_value = 5
        result = mock_func(2, 3)
        assert result == 5  # ← Tests the MOCK, not real code!
```

**✅ ACCEPTABLE (Real code test):**
```python
def test_calculate_sum():
    from math_utils import calculate_sum
    
    # Test REAL function
    result = calculate_sum(2, 3)
    assert result == 5  # ← Tests REAL implementation!
    
    # Test edge cases
    assert calculate_sum(0, 0) == 0
    assert calculate_sum(-1, 1) == 0
    assert calculate_sum(1000, 2000) == 3000
```

**✅ ACCEPTABLE (Real code with mocked dependencies):**
```python
def test_fetch_user_data():
    from user_service import fetch_user_data
    from unittest.mock import patch, Mock
    
    # Mock ONLY the external dependency (API call)
    with patch('user_service.requests.get') as mock_get:
        mock_response = Mock()
        mock_response.json.return_value = {"id": 1, "name": "Test"}
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        # Test REAL function with mocked dependency
        user = fetch_user_data(user_id=1)
        
        # Validate real code execution
        assert user["id"] == 1
        assert user["name"] == "Test"
        mock_get.assert_called_once_with("https://api.example.com/users/1")
```

---

### MANDATORY TEST STRUCTURE

Every test file MUST include:

1. **Basic Functionality Tests**
   - Test primary use cases
   - Cover main code paths
   - Validate expected outputs

2. **Edge Case Tests**
   - Empty inputs
   - Null/None values
   - Large values
   - Boundary conditions
   - Invalid inputs

3. **Error Handling Tests**
   - Test exception raising
   - Validate error messages
   - Test error recovery
   - Validate cleanup on errors

4. **Integration Tests (if applicable)**
   - Test interactions between components
   - Validate workflows
   - Test state transitions

---

### COVERAGE REQUIREMENTS BY FILE TYPE

| File Type | Minimum Coverage | Priority |
|-----------|------------------|----------|
| Core system files (ultrathink.py, master_orchestrator.py) | 95% | CRITICAL |
| Agent framework files | 90% | CRITICAL |
| Guardrails files | 90% | CRITICAL |
| Security files | 95% | CRITICAL |
| API endpoints | 90% | HIGH |
| Utility functions | 90% | HIGH |
| Configuration files | 85% | MEDIUM |
| Scripts | 80% | MEDIUM |

---

### ENFORCEMENT MECHANISMS

**1. Pre-Commit Hook (Immediate Enforcement)**
```bash
#!/bin/bash
# .git/hooks/pre-commit

# Get list of Python files being committed
PYTHON_FILES=$(git diff --cached --name-only --diff-filter=ACM | grep ".py$")

if [ -n "$PYTHON_FILES" ]; then
    for file in $PYTHON_FILES; do
        # Skip test files and __init__.py
        if [[ $file == tests/* ]] || [[ $file == */__init__.py ]]; then
            continue
        fi
        
        # Check if test file exists
        TEST_FILE="tests/unit/test_$(basename $file)"
        if [ ! -f "$TEST_FILE" ]; then
            echo "❌ ERROR: No test file for $file"
            echo "   Expected: $TEST_FILE"
            echo "   COMMIT BLOCKED - Create test file first"
            exit 1
        fi
        
        # Run coverage check
        pytest "$TEST_FILE" --cov="$file" --cov-fail-under=90 -q
        if [ $? -ne 0 ]; then
            echo "❌ ERROR: Coverage < 90% for $file"
            echo "   COMMIT BLOCKED - Improve test coverage"
            exit 1
        fi
    done
fi

echo "✅ All files have test coverage ≥ 90%"
```

**2. CI/CD Pipeline (Merge Enforcement)**
```yaml
# .github/workflows/test-coverage.yml
name: Test Coverage Enforcement

on: [pull_request]

jobs:
  coverage:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run pytest with coverage
        run: |
          pytest tests/ --cov=. --cov-fail-under=90
      - name: Block merge if coverage < 90%
        run: |
          if [ $? -ne 0 ]; then
            echo "❌ MERGE BLOCKED: Coverage < 90%"
            exit 1
          fi
```

**3. Local Development Check**
```bash
# Run this before committing
./check_test_coverage.sh

# Outputs:
# ✅ all_files: 92.3% coverage (PASS)
# ❌ new_feature.py: 67.2% coverage (FAIL - need 90%+)
```

---

### WORKFLOW FOR NEW FILES

**When creating `module/new_feature.py`:**

1. **Create test file FIRST (TDD approach - recommended)**
   ```bash
   touch tests/unit/test_new_feature.py
   # Write tests first, then implement to make tests pass
   ```

2. **OR create test file IMMEDIATELY after (acceptable)**
   ```bash
   # Created module/new_feature.py
   touch tests/unit/test_new_feature.py
   # Write tests to cover all functions/classes
   ```

3. **Run coverage check**
   ```bash
   pytest tests/unit/test_new_feature.py \
     --cov=module/new_feature.py \
     --cov-report=term-missing \
     --cov-fail-under=90
   ```

4. **If coverage < 90%, add more tests**
   ```bash
   # Check what lines are missing
   pytest tests/unit/test_new_feature.py \
     --cov=module/new_feature.py \
     --cov-report=html
   
   # Open htmlcov/index.html to see uncovered lines
   # Add tests until 90%+ achieved
   ```

5. **Only THEN commit**
   ```bash
   git add module/new_feature.py tests/unit/test_new_feature.py
   git commit -m "Add new_feature with 92% test coverage"
   ```

---

### WHY THIS MATTERS

**Problem we're solving:**
- Previous approach: 892 tests created, all mock-based
- Result: 9.83% code coverage (90% of code UNTESTED)
- Impact: Production bugs, undetected issues, technical debt

**New standard ensures:**
- ✅ Every file has real tests
- ✅ 90%+ coverage = 90%+ of code paths validated
- ✅ Real code testing = catch bugs before production
- ✅ Automated enforcement = no exceptions, no excuses

**ROI:**
- Bugs caught in development: $100-$1K cost
- Bugs in production: $10K-$100K cost
- **Savings: 99% reduction in production incident costs**

---

### EXCEPTIONS (VERY LIMITED)

**ONLY these files are exempt:**

1. `__init__.py` files (usually empty or simple imports)
2. `setup.py` (installation script)
3. Migration scripts (one-time execution)
4. Archived files in `archive/` directory

**ALL other Python files MUST have 90%+ coverage.**

---

### DOCUMENTATION REQUIREMENTS

**This standard MUST be present in:**
- ✅ `/home/user01/claude-test/ClaudePrompt/CLAUDE.md` (this file)
- ✅ `/home/user01/claude-test/CLAUDE.md` (root project)
- ✅ Pre-commit hook: `.git/hooks/pre-commit`
- ✅ CI/CD pipeline: `.github/workflows/test-coverage.yml`
- ✅ README.md - Testing section
- ✅ CONTRIBUTING.md - Developer guidelines

---

### COMMITMENT

This testing standard is PERMANENT and MANDATORY.

**Effective:** 2025-11-20 and forever
**Reason:** User requires production-ready code, not prototypes
**Cost:** Already paid in $200/month subscription - use it fully
**Benefit:** 99% reduction in production bugs = $500K-$2M annual savings

**YOU MUST CREATE TESTS FOR EVERY PYTHON FILE. NO EXCEPTIONS.**

---

### QUICK REFERENCE

```bash
# ✅ ALWAYS DO THIS when creating new_file.py:
1. Write tests/unit/test_new_file.py
2. pytest tests/unit/test_new_file.py --cov=new_file.py --cov-fail-under=90
3. If < 90%, add more tests
4. Only commit when ≥ 90%

# ❌ NEVER DO THIS:
1. Commit Python file without tests
2. Use only mocks (must test real code)
3. Accept < 90% coverage
4. Skip edge cases or error handling tests
```

---

**END OF MANDATORY TESTING STANDARDS**

