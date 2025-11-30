# CRITICAL REQUIREMENT: ALL ANSWERS FROM CLAUDE CODE

**Date**: 2025-11-29
**Status**: MANDATORY, CRITICAL, NON-NEGOTIABLE, NO WAY TO GO
**Effective**: PERMANENT - 2025-11-29 and FOREVER

---

## 🎯 THE CORE PRINCIPLE

**WHEN YOU ASK A QUESTION → ANSWER ALWAYS COMES FROM CLAUDE CODE**

**NOT from database. NOT from stored prompts. NOT from past context.**

**FROM CLAUDE CODE.**

This is **MANDATORY, CRITICAL, NON-NEGOTIABLE, AND NO WAY TO GO**.

---

## 📊 System Architecture (CORRECT)

```
User asks question
  ↓
prsg wrapper
  ↓
Query type detection
  ↓
┌─────────────────────────────────────────┐
│ Is this a conversation history query?  │
│ ("what did we discuss?")                │
└─────────────────────────────────────────┘
         │
         ├─ NO (file-based query) ──────────┐
         │                                   │
         │                                   ↓
         │                          Skip dual retrieval
         │                                   │
         │                                   ↓
         │                          Pass to Claude Code
         │                                   │
         │                                   ↓
         │                   Claude Code uses file tools:
         │                   - Glob("**/*.py")
         │                   - Grep("pattern")
         │                   - Read(files)
         │                                   │
         │                                   ↓
         │                   ANSWER FROM CLAUDE CODE ✅
         │
         └─ YES (history query) ────────────┐
                                             │
                                             ↓
                                    Run dual retrieval
                                             │
                                             ↓
                              Search database for past context
                                             │
                                             ↓
                              Retrieve relevant conversations
                                             │
                                             ↓
                              Pass context TO Claude Code
                                             │
                                             ↓
                  Claude Code GENERATES NEW ANSWER using context ✅
                                             │
                                             ↓
                                    ANSWER FROM CLAUDE CODE ✅
```

**IN BOTH CASES: ANSWER COMES FROM CLAUDE CODE!**

---

## ✅ DATABASE PURPOSE (CORRECT)

### What Database IS For

**1. Context Storage During Compaction**
- When token limit reaches 85% capacity
- System compacts conversation history
- Stores compressed context in database
- Tagged with project ID and instance ID

**2. Context Retrieval**
- When you return to same folder (project ID)
- System retrieves past context from database
- Passes context TO Claude Code
- Claude Code generates answer using that context

**3. Multi-Instance Support**
- Same project, different windows (different instance IDs)
- Database stores context for each instance
- Allows context sharing across instances
- All linked to same project ID

**4. Project Tracking**
- Store project IDs based on folder path
- Store instance IDs for each session
- Link all context to correct project/instance
- Maintain history across sessions

### What Database IS NOT For

**❌ NEVER answer questions FROM database**
- Database doesn't generate answers
- Database doesn't analyze code
- Database doesn't review security
- Database doesn't check performance

**❌ NEVER search database for codebase analysis**
- "Analyze code for security" → NOT from database
- "Find performance bottlenecks" → NOT from database
- "Review code quality" → NOT from database
- "Check test coverage" → NOT from database

---

## 🔥 THE FLOW (CORRECT)

### Example 1: Codebase Analysis Query

**Query**: "Analyze this codebase for security issues"

```
prsg wrapper
  ↓
Query type: FILE-BASED (detected by keywords)
  ↓
Skip dual retrieval (no database search)
  ↓
Pass directly to Claude Code
  ↓
Claude Code uses file tools:
  - Glob("**/*.py", "**/*.js", "**/*.ts")
  - Grep("password|secret|API_KEY|hardcoded")
  - Read(suspicious_files)
  ↓
Claude Code ANALYZES actual files
  ↓
Claude Code GENERATES answer:
  "Found 3 security issues:
   1. Hardcoded password in config.py:42
   2. SQL injection risk in database.py:156
   3. XSS vulnerability in templates/user.html:78"
  ↓
ANSWER FROM CLAUDE CODE ✅
```

**Database involvement**: ZERO
**Answer source**: Claude Code analyzing actual files

### Example 2: Conversation History Query

**Query**: "What did we discuss about authentication implementation?"

```
prsg wrapper
  ↓
Query type: HISTORY (detected by "what did we discuss")
  ↓
Run dual retrieval
  ↓
Search database for:
  - project_id = "proj_my-project_abc12345"
  - Keywords: "authentication", "implementation"
  ↓
Database returns stored conversations:
  - Discussion from 2025-11-20: "Should use JWT tokens"
  - Discussion from 2025-11-22: "Added refresh token support"
  - Discussion from 2025-11-25: "Implemented OAuth 2.0"
  ↓
Pass retrieved context TO Claude Code
  ↓
Claude Code READS the context
  ↓
Claude Code GENERATES NEW answer:
  "Based on our previous discussions:

   Nov 20: We decided to use JWT tokens for authentication
   Nov 22: Added refresh token support for better UX
   Nov 25: Implemented OAuth 2.0 for social login

   The current implementation uses JWT with refresh tokens
   and supports OAuth 2.0 for Google/Facebook login."
  ↓
ANSWER FROM CLAUDE CODE ✅
```

**Database involvement**: Provides context (stored conversations)
**Answer source**: Claude Code generating NEW answer from context

### Example 3: Context Compaction

**Scenario**: Token usage reaches 170K/200K (85% capacity)

```
System triggers compaction
  ↓
Retrieve relevant context from database:
  - Last 50 important messages
  - Project decisions
  - Key implementation details
  ↓
Compress and inject into active memory
  ↓
User asks NEW question: "How should we handle errors?"
  ↓
Claude Code has context from database
  ↓
Claude Code GENERATES answer using:
  - Retrieved context (what we decided before)
  - Current question
  - Available file tools
  ↓
ANSWER FROM CLAUDE CODE ✅
```

**Database involvement**: Provides context to avoid losing history
**Answer source**: Claude Code generating answer with full context

---

## 🚫 WHAT NEVER HAPPENS (IMPORTANT)

### ❌ Database Does NOT Answer Questions

**NEVER**:
```
User: "Analyze code for security"
  ↓
Database searches for "security"
  ↓
Database returns: "Here are stored messages about security"
  ↓
System shows database results as answer ❌ WRONG!
```

**CORRECT**:
```
User: "Analyze code for security"
  ↓
Skip database entirely
  ↓
Claude Code analyzes FILES
  ↓
Claude Code generates answer ✅ CORRECT!
```

### ❌ Database Does NOT Generate Responses

**Database role**: **STORAGE ONLY**
- Stores conversations
- Stores context
- Stores project/instance metadata
- Stores nothing else

**Database does NOT**:
- Generate answers
- Analyze code
- Review security
- Check performance
- Create responses

### ❌ Database Search Does NOT Replace Claude Code

**NEVER replace Claude Code with database search!**

Claude Code:
- ✅ Has file access (Glob, Grep, Read)
- ✅ Can analyze actual code
- ✅ Can generate new insights
- ✅ Can iterate to 99.9% confidence
- ✅ Can use all 8 guardrail layers

Database:
- ❌ Has NO file access
- ❌ Cannot analyze code
- ❌ Cannot generate insights
- ❌ Cannot improve confidence (static data)
- ❌ Has NO guardrails

**ALWAYS use Claude Code for answers!**

---

## 💡 WHY THIS MATTERS

### The Problem We Fixed (2025-11-29)

**BEFORE (BROKEN)**:
```
User: "Analyze codebase for security"
  ↓
Dual retrieval runs (WRONG!)
  ↓
Searches database (28 stored conversations)
  ↓
Stuck at 94% confidence (database has no codebase content!)
  ↓
Continues 1000 iterations (can't improve - wrong data source)
  ↓
NEVER analyzes actual files ❌
```

**User frustration**:
- ⏱️ Wastes time (endless validation loop)
- 🔴 No results (database lacks code)
- 😡 System broken

**AFTER (FIXED)**:
```
User: "Analyze codebase for security"
  ↓
Query type: FILE-BASED
  ↓
Skip database (correct!)
  ↓
Claude Code uses file tools
  ↓
Analyzes ACTUAL files ✅
  ↓
Returns answer in seconds ✅
```

**User satisfaction**:
- ⚡ Fast (no validation loop)
- ✅ Accurate (from real files)
- 😊 System works

---

## 📝 IMPLEMENTATION

### Files Modified

**1. `/home/user01/claude-test/ParaGroupAI/prsg`** (lines 113-156)
- Added query type detection
- Conditional dual retrieval based on query type
- File-based queries → Skip database, use Claude Code file tools
- History queries → Retrieve context, pass to Claude Code

**2. `/home/user01/claude-test/ParaGroupAI/query_type_detector.py`**
- Smart keyword-based detection
- FILE keywords: analyze, codebase, security, performance, fix, implement
- HISTORY keywords: "what did we", previous, discussed, remember

### How It Works

**Query Classification**:
```python
def should_run_dual_retrieval(query: str) -> bool:
    """
    Returns:
        True: History query → Retrieve context from database → Pass to Claude Code
        False: File query → Skip database → Claude Code uses file tools directly
    """
    query_lower = query.lower()

    # History query?
    if any(kw in query_lower for kw in HISTORY_KEYWORDS):
        return True  # Retrieve context, Claude Code generates answer

    # File-based query?
    if any(kw in query_lower for kw in FILE_KEYWORDS):
        return False  # Skip database, Claude Code analyzes files

    # Default: Skip database (safer for code queries)
    return False
```

---

## 🎯 THE GUARANTEE

**NO MATTER WHAT QUERY YOU ASK:**

✅ **Answer ALWAYS comes from Claude Code**
✅ **Database ONLY provides context (when needed)**
✅ **Claude Code ALWAYS generates the response**
✅ **99.9% confidence requirement applies**
✅ **All 8 guardrail layers apply**

**This is GUARANTEED, MANDATORY, CRITICAL, NON-NEGOTIABLE.**

---

## 📚 SUMMARY

### Database Role (CORRECT)

**Database IS**:
- Storage system for conversations
- Context provider during compaction
- Project/instance tracker
- Multi-instance support

**Database IS NOT**:
- Answer generator
- Code analyzer
- Security reviewer
- Performance checker

### Claude Code Role (CORRECT)

**Claude Code IS**:
- Answer generator (ALWAYS!)
- Code analyzer (using file tools)
- Security reviewer (using Grep, Read)
- Performance checker (using file analysis)
- Context processor (using retrieved context)

### The Flow (CORRECT)

```
Question → Query Type Detection
              │
              ├─ File-based → Claude Code (file tools)
              │                    ↓
              │              ANSWER FROM CLAUDE CODE ✅
              │
              └─ History → Retrieve context → Claude Code (with context)
                                                   ↓
                                        ANSWER FROM CLAUDE CODE ✅
```

**IN ALL CASES: ANSWER FROM CLAUDE CODE!**

---

## 🔒 COMMITMENT

This requirement is **PERMANENT**:

- **Effective**: 2025-11-29 and FOREVER
- **Documented**: Both CLAUDE.md files (ParaGroupAI and root)
- **Implemented**: query_type_detector.py + prsg wrapper
- **Tested**: Verified working correctly
- **Mandatory**: NO EXCEPTIONS, NO COMPROMISES

**User explicitly required**:
> "the answer should come from always claude code this is MANDATORY, CRITICAL, NON-NEGOTIABLE AND NO WAY TO GO"

**This is now PERMANENTLY IMPLEMENTED and DOCUMENTED.**

---

**Prepared by**: Claude Code
**Date**: 2025-11-29
**Status**: IMPLEMENTED AND PERMANENT
**Priority**: CRITICAL - FOUNDATIONAL REQUIREMENT
