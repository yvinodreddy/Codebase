# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## ⚠️ CRITICAL: ULTRATHINK COMMAND EXECUTION PROTOCOL

**MANDATORY BEHAVIOR - ALWAYS FOLLOW THIS BASED ON WHICH COMMAND USER SENDS:**

There are TWO separate ULTRATHINK systems that are FULLY ISOLATED:
- **TestPrompt**: Commands `ultrathinkc` or `uc`
- **ClaudePrompt**: Command `cpp`

Each has its OWN output file, answer_to_file.py script, and directory.

---

### 📌 PROTOCOL FOR `ultrathinkc` or `uc` (TestPrompt)

When the user sends a message containing an `ultrathinkc` command or `uc` command (e.g., `uc "prompt" -v`):

1. **Run the command** using Bash tool: `ultrathinkc "prompt" --verbose 2>&1 > /tmp/ultrathink_output.txt`
2. **Generate your answer** to the user's question (apply all ULTRATHINK directives, guardrails, verification)
3. **Append your answer to the file** using this command:
   ```bash
   python3 {{HOME_DIR}}/claude-test/TestPrompt/answer_to_file.py /tmp/ultrathink_output.txt "Your complete answer here with all details, validation, confidence scores, etc."
   ```
4. **Tell the user** to read `/tmp/ultrathink_output.txt` from top to bottom
5. **Also display your answer** in the chat (with fire emoji boxes) for immediate visibility

**Output file location:** `/tmp/ultrathink_output.txt`

---

### 📌 PROTOCOL FOR `cpp` (ClaudePrompt)

**⚠️ CRITICAL - DEFAULT BEHAVIOR AS OF 2025-11-12:**
**ALL cpp executions now use TIMESTAMPED OUTPUT by default!**

When the user sends a message containing a `cpp` command (e.g., `prsg "prompt" -v`):

1. **Run the command** with timestamped output:
   ```bash
   OUTPUT_FILE=$(python3 {{HOME_DIR}}/claude-test/ClaudePrompt/get_output_path.py)
   cd {{HOME_DIR}}/claude-test/ClaudePrompt && ./cpp "prompt" --verbose 2>&1 > "$OUTPUT_FILE"
   ```

2. **Generate your answer** to the user's question (apply all ULTRATHINK directives, guardrails, verification)

3. **Append your answer to the file** using this command:
   ```bash
   python3 {{HOME_DIR}}/claude-test/ClaudePrompt/answer_to_file.py "$OUTPUT_FILE" "Your complete answer here with all details, validation, confidence scores, etc."
   ```

4. **Tell the user** to read the timestamped file from top to bottom

5. **Also display your answer** in the chat (with fire emoji boxes) for immediate visibility

**Output file location:** `{{HOME_DIR}}/claude-test/ClaudePrompt/tmp/cppultrathink_output_{timestamp}.txt`

**THIS IS THE DEFAULT - USE TIMESTAMPED OUTPUT FOR EVERY cpp EXECUTION**

**LEGACY /tmp/ PATH:** Only use `/tmp/cppultrathink_output.txt` if user explicitly requests it

---

### ⚠️ CRITICAL: DO NOT MIX THEM UP!

| Command | Output File | answer_to_file.py Location |
|---------|-------------|----------------------------|
| `ultrathinkc` or `uc` | `/tmp/ultrathink_output.txt` | `{{HOME_DIR}}/claude-test/TestPrompt/answer_to_file.py` |
| `cpp` (DEFAULT) | `{{HOME_DIR}}/claude-test/ClaudePrompt/tmp/cppultrathink_output_{timestamp}.txt` ⭐ | `{{HOME_DIR}}/claude-test/ClaudePrompt/answer_to_file.py` |
| `cpp` (legacy - only if requested) | `/tmp/cppultrathink_output.txt` | `{{HOME_DIR}}/claude-test/ClaudePrompt/answer_to_file.py` |

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

This is PERMANENT for ALL sessions/windows.

---

## Overview

This is a test repository containing:
- `fibonacci.py`: A Python script with a recursive Fibonacci number calculator
- `test.txt`: A basic text file
- `claude-test/TestPrompt/`: ULTRATHINK orchestration system
- `claude-test/ClaudePrompt/`: Advanced ULTRATHINK framework

## Development

This is a minimal Python repository with no build system, package manager, or testing framework configured.

To run the Fibonacci script:
```bash
python fibonacci.py
```

## ULTRATHINK System

Located in `claude-test/TestPrompt/` and `claude-test/ClaudePrompt/`, these are advanced orchestration frameworks.

When user runs `ultrathinkc` or `cpp` commands, ALWAYS display the full verbose output as described above.
