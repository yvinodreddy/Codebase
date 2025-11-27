# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## ⚠️ CRITICAL: ULTRATHINK COMMAND EXECUTION PROTOCOL

**MANDATORY BEHAVIOR - ALWAYS FOLLOW THIS BASED ON WHICH COMMAND USER SENDS:**

There are TWO separate ULTRATHINK systems that are FULLY ISOLATED:
- **TestPrompt**: Commands `ultrathinkc` or `uc`
- **ClaudePrompt**: Command `cpp`

Each has its OWN output file, answer_to_file.py script, and directory.

### 🎯 WORKING DIRECTORY CONTEXT (PERMANENT - AS OF 2025-11-27)

**CRITICAL: cpp NOW PRESERVES ORIGINAL WORKING DIRECTORY**

When running `cpp` from ANY directory:

1. **You CAN run cpp from any directory** - No need to cd to ClaudePrompt first
   ```bash
   cd /home/user01/my-project
   cpp "your question" -v
   # System stays in /home/user01/my-project
   ```

2. **Each directory gets unique project ID** - Based on directory path
   - `/home/user01/my-project` → `proj_my-project_abc12345`
   - `/tmp/test` → `proj_test_def67890`
   - Same directory always gets same project ID (deterministic)

3. **Context stored in database** - Linked to original working directory
   - Project ID derived from directory path
   - Instance ID generated per session
   - All context stored with correct directory reference

4. **Output files always go to ClaudePrompt/tmp** - Timestamped
   - Format: `/home/user01/claude-test/ClaudePrompt/tmp/cppultrathink_output_YYYYMMDD_HHMMSS_mmm.txt`
   - Preserves complete history
   - No file conflicts in parallel execution

5. **Use --project-id to override** - Point to different project
   ```bash
   cd /anywhere
   cpp "question" --project-id proj_my-project_abc12345
   # Uses my-project context, regardless of current directory
   ```

**HOW IT WORKS (Technical):**
- cpp wrapper captures `$(pwd)` IMMEDIATELY at start
- Exports as `ULTRATHINK_ORIGINAL_CWD` environment variable
- All Python scripts read this variable for context
- Database stores project with original directory path
- User's shell never changes directory (bash script behavior)

This is PERMANENT for ALL sessions/windows.

---

### 📌 PROTOCOL FOR `ultrathinkc` or `uc` (TestPrompt)

**⚠️ CRITICAL - DEFAULT BEHAVIOR AS OF 2025-11-19:**
**ALL ultrathinkc/uc executions now use TIMESTAMPED OUTPUT by default!**

When the user sends a message containing an `ultrathinkc` command or `uc` command (e.g., `uc "prompt" -v`):

1. **Run the command** with timestamped output:
   ```bash
   OUTPUT_FILE=$(python3 /home/user01/claude-test/TestPrompt/get_output_path.py)
   ultrathinkc "prompt" --verbose 2>&1 > "$OUTPUT_FILE"
   ```

2. **Generate your answer** to the user's question (apply all ULTRATHINK directives, guardrails, verification)

3. **Append your answer to the file** using this command:
   ```bash
   python3 /home/user01/claude-test/TestPrompt/answer_to_file.py "$OUTPUT_FILE" "Your complete answer here with all details, validation, confidence scores, etc."
   ```

4. **Tell the user** to read the timestamped file from top to bottom

5. **Also display your answer** in the chat (with fire emoji boxes) for immediate visibility

**Output file location:** `/home/user01/claude-test/TestPrompt/tmp/ultrathink_output_{timestamp}.txt`

**THIS IS THE DEFAULT - USE TIMESTAMPED OUTPUT FOR EVERY ultrathinkc/uc EXECUTION**

**LEGACY /tmp/ PATH:** Only use `/tmp/ultrathink_output.txt` if user explicitly requests it

---

### 📌 PROTOCOL FOR `cpp` (ClaudePrompt)

**⚠️ CRITICAL - DEFAULT BEHAVIOR AS OF 2025-11-12:**
**ALL cpp executions now use TIMESTAMPED OUTPUT by default!**

**⚠️ UPDATED 2025-11-27: NO NEED TO CD TO CLAUDEPROMPT DIRECTORY!**
**cpp can now be run from ANY directory and preserves original context!**

When the user sends a message containing a `cpp` command (e.g., `cpp "prompt" -v`):

1. **Run the command** with timestamped output (from ANY directory):
   ```bash
   OUTPUT_FILE=$(python3 /home/user01/claude-test/ClaudePrompt/get_output_path.py)
   cpp "prompt" --verbose 2>&1 > "$OUTPUT_FILE"
   ```

   Note: cpp is aliased to `/home/user01/claude-test/ClaudePrompt/cpp` in ~/.bashrc

2. **Generate your answer** to the user's question (apply all ULTRATHINK directives, guardrails, verification)

3. **Append your answer to the file** using this command:
   ```bash
   python3 /home/user01/claude-test/ClaudePrompt/answer_to_file.py "$OUTPUT_FILE" "Your complete answer here with all details, validation, confidence scores, etc."
   ```

4. **Tell the user** to read the timestamped file from top to bottom

5. **Also display your answer** in the chat (with fire emoji boxes) for immediate visibility

**Output file location:** `/home/user01/claude-test/ClaudePrompt/tmp/cppultrathink_output_{timestamp}.txt`

**THIS IS THE DEFAULT - USE TIMESTAMPED OUTPUT FOR EVERY cpp EXECUTION**

**LEGACY /tmp/ PATH:** Only use `/tmp/cppultrathink_output.txt` if user explicitly requests it

---

### ⚠️ CRITICAL: DO NOT MIX THEM UP!

| Command | Output File | answer_to_file.py Location |
|---------|-------------|----------------------------|
| `ultrathinkc` or `uc` (DEFAULT) | `/home/user01/claude-test/TestPrompt/tmp/ultrathink_output_{timestamp}.txt` ⭐ | `/home/user01/claude-test/TestPrompt/answer_to_file.py` |
| `ultrathinkc` or `uc` (legacy - only if requested) | `/tmp/ultrathink_output.txt` | `/home/user01/claude-test/TestPrompt/answer_to_file.py` |
| `cpp` (DEFAULT) | `/home/user01/claude-test/ClaudePrompt/tmp/cppultrathink_output_{timestamp}.txt` ⭐ | `/home/user01/claude-test/ClaudePrompt/answer_to_file.py` |
| `cpp` (legacy - only if requested) | `/tmp/cppultrathink_output.txt` | `/home/user01/claude-test/ClaudePrompt/answer_to_file.py` |

**⭐ DEFAULT:** Always use timestamped output for BOTH `ultrathinkc/uc` AND `cpp` unless user explicitly asks for /tmp/ path

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

This is a simple test repository containing:
- `fibonacci.py`: A Python script with a recursive Fibonacci number calculator
- `test.txt`: A basic text file
- `claude-test/TestPrompt/`: ULTRATHINK orchestration system

## Development

This is a minimal Python repository with no build system, package manager, or testing framework configured.

To run the Fibonacci script:
```bash
python fibonacci.py
```

## ULTRATHINK System

Located in `claude-test/TestPrompt/`, this is an advanced orchestration framework.

When user runs `ultrathinkc` commands, ALWAYS display the full verbose output as described above.

================================================================================
🎯 CRITICAL: 99% CONFIDENCE REQUIREMENT FOR ULTRATHINK SEMANTIC SEARCH
================================================================================

**MANDATORY, NON-NEGOTIABLE, PRODUCTION-GRADE STANDARD**
**Effective: 2025-11-27 and FOREVER**

**Problem Identified and FIXED:**

The initial semantic search implementation in ClaudePrompt had a FATAL FLAW:
- Returned results at 50-90% confidence levels
- NO feedback loop validation
- NO guardrail iteration (only 1 pass)
- NO 99% confidence requirement
- **This was NOT production-grade!**

**Why This Violates Our Standards:**

ULTRATHINK is benchmarked against industry standards from:
- **Leading tech companies**: Google, Amazon, Microsoft, Meta, Netflix
- **Established frameworks**: MLflow, TruLens, DeepEval, RAGAS, LangChain, Semantic Kernel

**ALL of these require 99%+ confidence for production systems.**

**The Fix (PERMANENT):**

ALL retrieval methods (keyword AND semantic) MUST:
1. **Validate to 99% confidence** using feedback loop (up to 20 iterations)
2. **Apply all 8 guardrail layers** on every iteration
3. **NOT return results** until 99% achieved
4. **Return confidence scores** with all results

**Production-Grade Decision Logic:**
```
Step 1: Run keyword search → Validate to 99% (iterate up to 20x)
Step 2: Run semantic search → Validate to 99% (iterate up to 20x)
Step 3: BOTH at 99%? → NOW compare them
Step 4: Return comparison showing which 99%-validated method is better
```

**Implementation:**

**File**: `/home/user01/claude-test/ClaudePrompt/database/dual_context_retriever.py`

**Production Method** (REQUIRED): `retrieve_with_both_methods_validated()`
**Legacy Method** (DEPRECATED): `retrieve_with_both_methods()` - NO validation!

**Why User Is Absolutely Right:**

The user correctly identified that:
- "If you are going below 99%, it is NOT production-grade"
- "User pays $200/month for 99% accuracy, NOT 50-90%"
- "What is the purpose of implementing semantic search if it doesn't reach 99%?"
- "This is CRITICAL, MANDATORY, NON-NEGOTIABLE"

**This is 100% correct and now PERMANENTLY FIXED.**

**Enforcement:**

This is:
- **CRITICAL** - Core system requirement
- **MANDATORY** - Cannot be disabled
- **NON-NEGOTIABLE** - No exceptions allowed
- **PERMANENT** - Effective 2025-11-27 and forever
- **PRODUCTION-GRADE** - Benchmarked against industry leaders

**Any retrieval result below 99% confidence is NOT production-ready.**

See `/home/user01/claude-test/ClaudePrompt/CLAUDE.md` for full implementation details.

================================================================================

---

## Original Content

- Using ImageMagick
   convert Font/RMMS1.jpg -quality 90 Font/RMMS1_fixed.jpg
convert Font/RMMS2.jpg -quality 90 Font/RMMS2_fixed.jpg
