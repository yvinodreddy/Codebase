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
- ✅ /home/semanticraj/claude-test/CLAUDE.md - Global rules
- ✅ /home/semanticraj/claude-test/ClaudePrompt/CLAUDE.md (this file) - ULTRATHINK project rules
- ✅ /home/semanticraj/claude-test/ClaudePrompt/web-ui-implementation/.claude_docs/DEVELOPMENT_STANDARDS.md

All three files MUST contain consistent messaging about:
1. NO time limits for Claude Code
2. 100% completion requirement for all features
3. Task decomposition for large requests
4. Banned phrases list
5. Correct alternatives

This is a PERMANENT, NON-NEGOTIABLE standard effective 2025-11-14 and forever.

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
   - Format: `/home/semanticraj/claude-test/ClaudePrompt/tmp/cppultrathink_output_YYYYMMDD_HHMMSS_mmm.txt`
   - With track: `/home/semanticraj/claude-test/ClaudePrompt/tmp/cppultrathink_output_track1_YYYYMMDD_HHMMSS_mmm.txt`

3. **Generate your answer** to the user's question (apply all ULTRATHINK directives, guardrails, verification)

4. **Append your answer to the file** using this command:
   ```bash
   python3 /home/semanticraj/claude-test/ClaudePrompt/answer_to_file.py "$OUTPUT_FILE" "Your complete answer here with all details, validation, confidence scores, etc."
   ```

5. **Tell the user** to read the timestamped file from top to bottom

6. **Also display your answer** in the chat (with fire emoji boxes) for immediate visibility

**Output file location:** `/home/semanticraj/claude-test/ClaudePrompt/tmp/cppultrathink_output_{timestamp}.txt`

**THIS IS THE DEFAULT - USE THIS FOR EVERY cpp EXECUTION**

---

#### **LEGACY METHOD: /tmp/ Output (ONLY if user explicitly requests it)**

⚠️ DO NOT USE THIS UNLESS USER EXPLICITLY ASKS FOR /tmp/ PATH

For backward compatibility only:

1. **Run the command** using Bash tool: `cpp "prompt" --verbose 2>&1 > /tmp/cppultrathink_output.txt`
2. **Generate your answer** to the user's question (apply all ULTRATHINK directives, guardrails, verification)
3. **Append your answer to the file** using this command:
   ```bash
   python3 /home/semanticraj/claude-test/ClaudePrompt/answer_to_file.py /tmp/cppultrathink_output.txt "Your complete answer here with all details, validation, confidence scores, etc."
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
   python3 /home/semanticraj/claude-test/TestPrompt/answer_to_file.py /tmp/ultrathink_output.txt "Your complete answer here with all details, validation, confidence scores, etc."
   ```
4. **Tell the user** to read `/tmp/ultrathink_output.txt` from top to bottom
5. **Also display your answer** in the chat (with fire emoji boxes) for immediate visibility

**Output file location:** `/tmp/ultrathink_output.txt`

---

### ⚠️ CRITICAL: DO NOT MIX THEM UP!

| Command | Output File | answer_to_file.py Location |
|---------|-------------|----------------------------|
| `cpp` (DEFAULT) | `ClaudePrompt/tmp/cppultrathink_output_{timestamp}.txt` ⭐ | `/home/semanticraj/claude-test/ClaudePrompt/answer_to_file.py` |
| `cpp` (legacy - only if requested) | `/tmp/cppultrathink_output.txt` | `/home/semanticraj/claude-test/ClaudePrompt/answer_to_file.py` |
| `ultrathinkc` or `uc` | `/tmp/ultrathink_output.txt` | `/home/semanticraj/claude-test/TestPrompt/answer_to_file.py` |

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
   python3 /home/semanticraj/claude-test/ClaudePrompt/validate_my_response.py \
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
/home/semanticraj/claude-test/ClaudePrompt/validate_my_response.py
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
