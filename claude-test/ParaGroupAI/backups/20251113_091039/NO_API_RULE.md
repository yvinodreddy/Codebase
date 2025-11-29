# PERMANENT RULE - NO API CHARGES ALLOWED

**Date:** November 10, 2025
**Status:** ⛔ MANDATORY - NEVER VIOLATE ⛔

---

## THE RULE

**NEVER USE CLAUDE API THAT INCURS CHARGES**

This is a PERMANENT, NON-NEGOTIABLE, MANDATORY rule that MUST be followed by:
- All future Claude Code sessions
- All code modifications
- All enhancements
- All bug fixes
- All features

---

## WHY THIS RULE EXISTS

### Financial Reason
1. User pays **$200/month** for Claude Code subscription
2. Claude API charges **$0.003-0.015 per request**
3. Using API = **Paying twice** for the same service
4. User explicitly **removed API key** from .bashrc to prevent charges

### Example Cost Impact
```
100 requests/day × 30 days = 3,000 requests/month
3,000 × $0.01 average = $30/month EXTRA
Annual cost: $360/year WASTED

With Claude Code: $0 extra (included)
```

---

## WHAT IS FORBIDDEN

❌ **NEVER** add `ANTHROPIC_API_KEY` to .bashrc
❌ **NEVER** enable `--api` flag by default
❌ **NEVER** make code use API automatically
❌ **NEVER** suggest using API mode
❌ **NEVER** modify code to call Claude API
❌ **NEVER** change default behavior to use API
❌ **NEVER** enable API for "better output"
❌ **NEVER** use API for "formatted reports"

---

## WHAT TO DO INSTEAD

✅ **USE Claude Code mode** (default)
✅ **Display enhanced prompts** to Claude Code
✅ **Let Claude Code respond** with formatting
✅ **Generate formatted output** in Claude Code responses
✅ **Keep API key removed** from .bashrc

---

## THE REAL ISSUE

### What User Wanted
- Beautiful formatted output (like the old system)
- With all stages, layers, metrics
- **WITHOUT using API**
- **WITHOUT any charges**

### What Was Wrong
- Old system used API → Generated beautiful output
- New system removed API → Lost formatted output
- **Solution is NOT to add API back**
- **Solution is to generate formatted output in Claude Code mode**

---

## THE CORRECT SOLUTION

When user runs:
```bash
cpp "what is 2+2" --verbose
```

**What should happen:**
1. ✅ Display enhanced prompt to Claude Code (NO API)
2. ✅ Claude Code responds
3. ✅ Claude Code generates formatted output with:
   - All 6 stages
   - All 7 guardrail layers
   - All [VERBOSE] tags
   - Context management metrics
   - Framework comparison
   - **WITHOUT calling API**
   - **WITHOUT any charges**

---

## ENFORCEMENT

### In Code
- Default: `use_claude_api=False`
- Only enable if user explicitly uses `--api` flag
- **NEVER enable automatically**
- **NEVER change this logic**

### In Documentation
- CLAUDE.md: Permanent warning
- NO_API_RULE.md: This file
- All documentation: Clear statements

### In Future Sessions
- This rule persists across:
  - Window closes
  - Computer restarts
  - New sessions
  - Context compaction
  - Code modifications

---

## IF SOMEONE SUGGESTS API

**Response:**
```
NO. We use Claude Code mode only.
No API charges allowed.
This is a permanent rule.
See: /home/user01/claude-test/ClaudePrompt/NO_API_RULE.md
```

---

## WHAT USER ACTUALLY WANTS

**OLD OUTPUT (what user wants back):**
```
================================================================================
🔥 ULTRATHINK - Unified Orchestration System
================================================================================

[VERBOSE] STAGE 1: Prompt Preprocessing
[VERBOSE] STAGE 2: Guardrails - Input Validation (Layers 1-3)
[VERBOSE] ┌─ Layer 1: Prompt Shields ─────────────┐
[VERBOSE] │ Status: ✅ PASS                        │
[VERBOSE] └───────────────────────────────────────┘
... (100+ lines of beautiful formatted output)
```

**HOW TO ACHIEVE IT:**
- Generate this formatted output in Claude Code's response
- **NOT by calling API**
- By having Claude Code produce the formatted text
- All included in $200/month subscription
- **Zero additional charges**

---

## SUMMARY

**What is FORBIDDEN:** Using Claude API (costs money)
**What is REQUIRED:** Using Claude Code (included in subscription)
**What user wants:** Formatted output (can be done in Claude Code)
**What is NOT acceptable:** Paying twice for the same service

**This rule is PERMANENT and MANDATORY.**

---

**Recorded:** November 10, 2025
**Effective:** Immediately and forever
**Authority:** User directive (highest priority)
**Violations:** Not acceptable under any circumstances

**END OF RULE**
