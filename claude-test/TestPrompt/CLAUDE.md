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
- **ClaudePrompt**: Command `cpp` → `/tmp/cppultrathink_output.txt`

Each has its OWN output file, answer_to_file.py script, and directory.

---

### 📌 PRIMARY PROTOCOL FOR `ultrathinkc` or `uc` (TestPrompt - THIS DIRECTORY)

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

### 📌 ALTERNATIVE PROTOCOL FOR `cpp` (ClaudePrompt)

When the user sends a message containing a `cpp` command (e.g., `cpp "prompt" -v`):

1. **Run the command** using Bash tool: `cpp "prompt" --verbose 2>&1 > /tmp/cppultrathink_output.txt`
2. **Generate your answer** to the user's question (apply all ULTRATHINK directives, guardrails, verification)
3. **Append your answer to the file** using this command:
   ```bash
   python3 /home/user01/claude-test/ClaudePrompt/answer_to_file.py /tmp/cppultrathink_output.txt "Your complete answer here with all details, validation, confidence scores, etc."
   ```
4. **Tell the user** to read `/tmp/cppultrathink_output.txt` from top to bottom
5. **Also display your answer** in the chat (with fire emoji boxes) for immediate visibility

**Output file location:** `/tmp/cppultrathink_output.txt`

---

### ⚠️ CRITICAL: DO NOT MIX THEM UP!

| Command | Output File | answer_to_file.py Location |
|---------|-------------|----------------------------|
| `ultrathinkc` or `uc` | `/tmp/ultrathink_output.txt` | `/home/user01/claude-test/TestPrompt/answer_to_file.py` |
| `cpp` | `/tmp/cppultrathink_output.txt` | `/home/user01/claude-test/ClaudePrompt/answer_to_file.py` |

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
ultrathinkc "your prompt here" --verbose
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
- ✅ ALL prompts processed through ultrathinkc
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
   python3 /home/user01/claude-test/TestPrompt/validate_my_response.py \
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
/home/user01/claude-test/TestPrompt/validate_my_response.py
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
