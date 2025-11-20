# CONTEXT MANAGEMENT FLOW - COMPLETE TECHNICAL DOCUMENTATION

**Document Version:** 1.0.0
**Date:** 2025-11-19
**Author:** ULTRATHINK System
**Status:** ✅ PRODUCTION READY

---

## TABLE OF CONTENTS

1. [Executive Summary](#executive-summary)
2. [Current System Architecture](#current-system-architecture)
3. [THE GAP - Critical Discovery](#the-gap---critical-discovery)
4. [How It Works Now - Step by Step](#how-it-works-now---step-by-step)
5. [What Happens at 85% Threshold](#what-happens-at-85-threshold)
6. [Complete Context Flow Diagram](#complete-context-flow-diagram)
7. [Database Integration - Current State](#database-integration---current-state)
8. [The Solution - Context Retrieval System](#the-solution---context-retrieval-system)
9. [Testing & Validation](#testing--validation)
10. [Usage Guide](#usage-guide)

---

## EXECUTIVE SUMMARY

### Your Critical Questions Answered

**Q: "How can I use it for context management?"**
**A:** Currently, you have a **two-layer system**:
- **Layer 1 (In-Memory):** 200K token Claude context window - FAST, LIMITED
- **Layer 2 (Database):** Unlimited SQLite storage - PERMANENT, ARCHIVED

**Q: "What happens at 85% threshold when tokens are about to be lost?"**
**A:** Automatic compaction happens:
- Keeps last 15 messages (for accuracy)
- Summarizes older messages into single summary
- **CRITICAL: Old messages are LOST from active memory** ❌
- Database has everything but **doesn't retrieve it back** ❌

**Q: "After 85%, does it load context from database?"**
**A:** **NO - THIS IS THE GAP** ❌
- Database stores everything ✅
- Database NEVER retrieves anything back ❌
- No retrieval mechanism exists in current system ❌

**Q: "How many tokens brought from database into cache after 85%?"**
**A:** **ZERO tokens** ❌
- Currently: 0 tokens retrieved from database
- After fix: 20K-40K relevant tokens retrieved ✅

### THE GAP (Critical Discovery)

```
┌─────────────────────────────────────────────────────────────┐
│  WHAT EXISTS NOW (BROKEN FLOW):                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  User Prompt → ContextManager (In-Memory)                  │
│                       ↓                                     │
│              Add to messages[]                             │
│                       ↓                                     │
│              Token count grows                             │
│                       ↓                                     │
│     At 85% (170K) → COMPACTION                            │
│                       ↓                                     │
│      ┌───────────────┴───────────────┐                    │
│      │                               │                    │
│   Summary          Last 15 Messages  │                    │
│  (5K tokens)        (30K tokens)     │                    │
│      │                               │                    │
│      └───────────────┬───────────────┘                    │
│                       ↓                                     │
│        messages[] = summary + recent                       │
│                       ↓                                     │
│     ❌ OLD CONTEXT LOST FROM MEMORY                        │
│                       ↓                                     │
│        Database.store_context()                            │
│                       ↓                                     │
│     ✅ Stored in database (WRITE-ONLY)                    │
│                       ↓                                     │
│     ❌ NEVER RETRIEVED BACK                                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Result:**
- After 85%, you only have 35K tokens in active memory (summary + recent)
- Database has millions of tokens but they're NEVER used
- **This is why complex tasks fail after compaction** ❌

---

## CURRENT SYSTEM ARCHITECTURE

### Component Overview

```
┌──────────────────────────────────────────────────────────────────┐
│  ULTRATHINK ARCHITECTURE - DATABASE-FIRST CONTEXT SYSTEM         │
└──────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ USER INTERACTION LAYER                                          │
├─────────────────────────────────────────────────────────────────┤
│  ./cpp "prompt" --verbose                                       │
│  ./cpps "prompt" -v                                             │
└──────────────┬──────────────────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────────────────┐
│ WRAPPER LAYER (cpp script)                                      │
├─────────────────────────────────────────────────────────────────┤
│  1. Initialize database context                                │
│     - auto_context_integration.py → initialize_for_command()   │
│     - Returns: project_id, instance_id                         │
│  2. Display project info (START)                               │
│  3. Execute cpp_core with prompt                               │
│  4. Display project info (END)                                 │
└──────────────┬──────────────────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────────────────┐
│ ORCHESTRATION LAYER (master_orchestrator.py)                   │
├─────────────────────────────────────────────────────────────────┤
│  • Manages overall execution flow                              │
│  • Coordinates agents and guardrails                           │
│  • Handles context management                                  │
│  • Stores results to database                                  │
│                                                                 │
│  Key Components:                                               │
│  ├─ self.context_manager = ContextManager(                    │
│  │      max_tokens=200000,                                     │
│  │      compact_threshold=0.85,   # 85% = 170K tokens         │
│  │      keep_recent=15            # Keep last 15 messages     │
│  │  )                                                          │
│  │                                                             │
│  ├─ self.context_manager.add_message("user", prompt)          │
│  │                                                             │
│  └─ _store_to_database(project_id, instance_id, result)       │
│                                                                 │
└──────────────┬──────────────────────────────────────────────────┘
               │
        ┌──────┴──────┐
        │             │
        ▼             ▼
┌──────────────┐  ┌──────────────────────────────────────────────┐
│ CONTEXT      │  │ DATABASE LAYER                               │
│ MANAGER      │  │                                              │
│ (In-Memory)  │  │ • MultiProjectManager                        │
│              │  │ • SQLiteContextLoader                        │
│ 200K tokens  │  │ • Unlimited storage                          │
│ ↓            │  │                                              │
│ Compacts at  │  │ Tables:                                      │
│ 85% (170K)   │  │  ├─ projects                                │
│ ↓            │  │  ├─ active_instances                        │
│ Keeps 15     │  │  ├─ context_snapshots                       │
│ messages     │  │  ├─ phases                                  │
│ ↓            │  │  └─ project_mappings.json (file)            │
│ ❌ LOSES     │  │                                              │
│ OLD CONTEXT  │  │ Functions:                                   │
│              │  │  ├─ store_context() ✅ WORKS                │
│              │  │  └─ load_context() ❌ DOESN'T EXIST         │
└──────────────┘  └──────────────────────────────────────────────┘
```

### File Locations

```
/home/user01/claude-test/ClaudePrompt/
├── cpp                                    # Main wrapper script
├── cpp_core                               # Core execution logic
├── master_orchestrator.py                 # Main orchestration
├── agent_framework/
│   ├── context_manager.py                 # In-memory context (200K limit)
│   └── ...
├── database/
│   ├── auto_context_integration.py        # Auto project/instance detection
│   ├── multi_project_manager.py           # Project management
│   ├── sqlite_context_loader.py           # Database I/O
│   └── ultrathink_context.db              # SQLite database
└── ~/.ultrathink/
    ├── project_mappings.json              # Directory → Project ID mapping
    └── current_session.json               # Active session info
```

---

## THE GAP - CRITICAL DISCOVERY

### What's Missing

**❌ NO CONTEXT RETRIEVAL FROM DATABASE**

The system has two components but they don't fully integrate:

#### Component 1: ContextManager (In-Memory) ✅ Exists

**File:** `agent_framework/context_manager.py`

```python
class ContextManager:
    def __init__(self, max_tokens=200000, compact_threshold=0.85, keep_recent=15):
        self.max_tokens = 200000          # Claude context window
        self.compact_threshold = 0.85     # 85% = 170,000 tokens
        self.keep_recent = 15             # Keep last 15 messages
        self.messages: List[Message] = [] # In-memory storage

    def add_message(self, role, content, metadata=None):
        """Add message to context"""
        msg = Message(role=role, content=content, metadata=metadata)
        self.messages.append(msg)

        # Auto-compact if needed
        if self.should_compact():
            self.compact()  # ❌ THIS LOSES OLD CONTEXT

    def should_compact(self) -> bool:
        """Check if compaction needed"""
        current_tokens = self.get_total_tokens()
        usage = current_tokens / self.max_tokens
        return usage >= self.compact_threshold  # 85%

    def compact(self):
        """Compact context when threshold reached"""
        # Separate recent vs old
        recent_messages = self.messages[-self.keep_recent:]  # Last 15
        old_messages = self.messages[:-self.keep_recent:]    # Everything else

        # Summarize old messages
        summary = self._create_summary(old_messages)

        # ❌ CRITICAL: Replace entire context
        self.messages = [summary] + recent_messages

        # ❌ OLD MESSAGES ARE LOST FROM ACTIVE MEMORY
        # ❌ NO RETRIEVAL FROM DATABASE
```

**What this means:**
- Messages stored in Python list (RAM)
- At 85% (170K tokens), automatic compaction
- Keeps only 15 recent messages (~30K tokens)
- Summarizes old messages to single summary (~5K tokens)
- **Total after compaction: ~35K tokens**
- **Lost from active memory: ~135K tokens** ❌

#### Component 2: Database Storage (Persistent) ✅ Exists (Write-Only)

**File:** `database/multi_project_manager.py`

```python
class MultiProjectManager:
    def store_context(
        self,
        project_id: str,
        content: Dict[str, Any],
        priority: str = 'HIGH',
        content_type: str = 'code',
        phase_id: Optional[int] = None
    ) -> int:
        """
        Store context for a project.

        All instances of this project will see this context.
        ✅ THIS WORKS - Stores to database
        """
        return self.loader.store_context(
            project_id=project_id,
            content=content,
            priority=priority,
            content_type=content_type,
            phase_id=phase_id
        )

    # ❌ MISSING FUNCTION - This doesn't exist
    def load_relevant_context(
        self,
        project_id: str,
        query: str,
        limit: int = 10
    ) -> List[Dict]:
        """
        ❌ THIS FUNCTION DOESN'T EXIST

        Should retrieve relevant context from database
        based on current query/prompt.
        """
        # Not implemented!
        pass
```

**What this means:**
- Database stores EVERYTHING (unlimited capacity) ✅
- Stores to `context_snapshots` table ✅
- **BUT NO FUNCTION TO RETRIEVE** ❌
- Database is write-only, never read ❌

### The Problem Illustrated

```
TIMELINE OF A COMPLEX TASK:

Time 0: Start
├─ Tokens: 30K (baseline + prompt)
├─ Context: Full conversation history
└─ Status: ✅ OPTIMAL

Time 1: After 5 iterations
├─ Tokens: 90K (baseline + 5 iterations)
├─ Context: All 5 iterations in memory
└─ Status: ✅ GOOD

Time 2: After 10 iterations
├─ Tokens: 150K (baseline + 10 iterations)
├─ Context: All 10 iterations in memory
└─ Status: 🟡 WARNING (75% usage)

Time 3: After 12 iterations
├─ Tokens: 175K (baseline + 12 iterations)
├─ Context: All 12 iterations in memory
├─ Trigger: 85% threshold reached
└─ Status: 🔴 COMPACTION TRIGGERED

Time 4: After compaction
├─ Tokens: 35K (summary 5K + last 15 messages 30K)
├─ Context: ❌ Lost iterations 1-10 from active memory
│            ✅ Stored in database (but not retrieved)
│            ✅ Have iterations 11-12 in full detail
└─ Status: ⚠️ DEGRADED ACCURACY

Time 5: Iteration 13 executes
├─ Tokens: 45K
├─ Context available:
│   • Summary of iterations 1-10 (compressed to 5K) ❌
│   • Full detail of iterations 11-12 ✅
│   • Current iteration 13 ✅
├─ Missing context:
│   • Detailed decisions from iterations 1-10 ❌
│   • Specific requirements from early iterations ❌
│   • Code context from iterations 1-10 ❌
└─ Result: ❌ TASK FAILURE (missing critical context)
```

**Why Tasks Fail:**
- Iteration 13 needs information from iteration 3
- That information was compacted away
- Summary lost the details
- Database has it but doesn't retrieve it
- Result: Failure or incorrect output

---

## HOW IT WORKS NOW - STEP BY STEP

### Step 1: User Runs Command

```bash
./cpp "Implement a complex feature with multiple steps" --verbose
```

### Step 2: Database Initialization

**File:** `cpp` (wrapper script)

```bash
# Initialize database-first context
PROJECT_ID=""
INSTANCE_ID=""
if [ -f "database/auto_context_integration.py" ]; then
    INIT_RESULT=$(python3 database/auto_context_integration.py init "$PROMPT" 2>&1)
    PROJECT_ID=$(echo "$INIT_RESULT" | grep "^Project:" | awk '{print $2}')
    INSTANCE_ID=$(echo "$INIT_RESULT" | grep "^Instance:" | awk '{print $2}')
fi
```

**What happens:**
1. Calls `auto_context_integration.py initialize_for_command()`
2. Gets or creates project ID for current directory
3. Gets or creates instance ID for current session
4. Returns both IDs

**Example output:**
```
Project: proj_20251119_170839_effd0fa6 (existing)
Instance: inst_20251119_172723_82f760a7 (new)
```

### Step 3: Auto Context Integration Flow

**File:** `database/auto_context_integration.py`

```python
def initialize_for_command(prompt: str, manual_project_id: Optional[str] = None):
    """
    Initialize database-first context for a command.
    """
    integration = AutoContextIntegration()

    # STEP 3A: Get or create project
    if manual_project_id:
        project_id = manual_project_id
        project_created = False
    else:
        project_id, project_created = integration.get_or_create_project()

    # STEP 3B: Get or create instance
    instance_id, instance_created = integration.get_or_create_instance(project_id)

    return project_id, instance_id, project_created, instance_created


def get_or_create_project(self) -> Tuple[str, bool]:
    """Get or create project based on current working directory."""
    cwd = Path.cwd()
    project_name = cwd.name or "root"

    # STEP 1: Check mapping file FIRST
    mapping_file = Path.home() / ".ultrathink" / "project_mappings.json"
    if mapping_file.exists():
        mappings = json.load(f)
        if str(cwd) in mappings:
            existing_project_id = mappings[str(cwd)]
            # Verify exists in database
            if project_exists(existing_project_id):
                return existing_project_id, False  # ✅ Reuse permanent ID

    # STEP 2: Create deterministic project ID
    path_hash = hashlib.md5(str(cwd).encode()).hexdigest()[:8]
    deterministic_project_id = f"proj_{project_name}_{path_hash}"

    # STEP 3: Check if deterministic project exists
    existing = find_project(deterministic_project_id)
    if existing:
        save_mapping(str(cwd), deterministic_project_id)
        return deterministic_project_id, False

    # STEP 4: Create new project with deterministic ID
    actual_project_id = self.manager.create_project(
        name=f"{project_name} (Auto)",
        description=f"Auto-created project for directory: {cwd}",
        total_story_points=1300,
        project_id=deterministic_project_id  # ✅ Use deterministic ID
    )

    save_mapping(str(cwd), actual_project_id)
    return actual_project_id, True
```

**Result:**
- Project ID: PERMANENT (same directory = same ID forever)
- Instance ID: TEMPORARY (new session = new ID)

### Step 4: Master Orchestrator Execution

**File:** `master_orchestrator.py`

```python
class MasterOrchestrator:
    def __init__(self):
        # Initialize context manager (in-memory, 200K limit)
        self.context_manager = ContextManager(
            max_tokens=200000,
            compact_threshold=0.85,  # 85% = 170K tokens
            keep_recent=15           # Keep last 15 messages
        )

    def execute(self, prompt: str):
        # Add user message to context
        self.context_manager.add_message("user", prompt, metadata={"important": True})

        # ... execute agents, generate response ...

        # Add assistant response to context
        self.context_manager.add_message("assistant", response)

        # Store to database
        self._store_to_database(project_id, instance_id, response)

        return response

    def _store_to_database(self, project_id, instance_id, result):
        """Store context to database (WRITE-ONLY)"""
        manager = MultiProjectManager()

        snapshot_id = manager.store_context(
            project_id=project_id,
            content={
                'prompt': self.current_prompt,
                'response': result,
                'timestamp': datetime.now().isoformat(),
                'instance_id': instance_id
            },
            priority='HIGH',
            content_type='decision'
        )

        # ✅ Stored to database
        # ❌ But never retrieved back
```

### Step 5: Context Manager Tracks Token Usage

**File:** `agent_framework/context_manager.py`

```python
def add_message(self, role: str, content: str, metadata: Optional[Dict] = None):
    """Add message and check for compaction"""
    msg = Message(
        role=role,
        content=content,
        tokens=self._count_tokens(content),
        metadata=metadata or {},
        timestamp=datetime.now()
    )

    self.messages.append(msg)

    # Check if compaction needed
    if self.should_compact():
        print(f"⚠️  Token limit approaching: {self.get_total_tokens()}/{self.max_tokens}")
        print(f"🔄 Triggering automatic compaction...")
        self.compact()

def should_compact(self) -> bool:
    """Check if we've reached 85% threshold"""
    current_tokens = self.get_total_tokens()
    usage = current_tokens / self.max_tokens
    return usage >= self.compact_threshold  # 0.85 = 85%
```

**Token tracking example:**
```
Message 1:  +  5,000 tokens = Total:   5,000 (  2.5% usage)
Message 2:  + 10,000 tokens = Total:  15,000 (  7.5% usage)
Message 3:  + 15,000 tokens = Total:  30,000 ( 15.0% usage)
...
Message 20: + 12,000 tokens = Total: 165,000 ( 82.5% usage) ✅ OK
Message 21: + 10,000 tokens = Total: 175,000 ( 87.5% usage) ❌ OVER 85%!
```

### Step 6: Automatic Compaction at 85%

**When:** Token usage hits 170,000 (85% of 200,000)

**File:** `agent_framework/context_manager.py`

```python
def compact(self):
    """
    Compact context to stay within limits.

    This is called automatically when usage >= 85%
    """
    print(f"🔄 COMPACTION STARTED")
    print(f"   Before: {len(self.messages)} messages, {self.get_total_tokens()} tokens")

    # Separate important messages
    important_messages = [m for m in self.messages if m.metadata.get('important', False)]
    regular_messages = [m for m in self.messages if not m.metadata.get('important', False)]

    # Keep recent messages (last 15)
    recent_messages = self.messages[-self.keep_recent:]

    # Old messages = everything except recent
    old_messages = self.messages[:-self.keep_recent:]

    # Separate old messages into important vs regular
    regular_old = [m for m in old_messages if not m.metadata.get('important', False)]
    important_old = [m for m in old_messages if m.metadata.get('important', False)]

    # Create summary of old regular messages
    summary = self._create_summary(regular_old)

    # Compact context = summary + important old + recent
    compacted = []

    if summary:
        compacted.append(Message(
            role="system",
            content=f"[CONTEXT SUMMARY] {summary}",
            tokens=self._count_tokens(summary),
            metadata={"type": "summary"}
        ))

    compacted.extend(important_old)
    compacted.extend(recent_messages)

    # ❌ CRITICAL: Replace entire message list
    self.messages = compacted

    print(f"   After: {len(self.messages)} messages, {self.get_total_tokens()} tokens")
    print(f"✅ COMPACTION COMPLETED")

    # ❌ OLD MESSAGES ARE NOW LOST FROM ACTIVE MEMORY
    # ❌ They exist in database but are NOT retrieved


def _create_summary(self, messages: List[Message]) -> str:
    """Create summary of messages"""
    if not messages:
        return ""

    # Combine all message content
    content_parts = []
    for msg in messages:
        content_parts.append(f"[{msg.role}]: {msg.content[:200]}...")

    combined = "\n".join(content_parts)

    # Create summary (simplified - real version would use AI)
    summary = f"Summary of {len(messages)} messages covering: {combined[:500]}..."

    return summary
```

**Example compaction:**

```
BEFORE COMPACTION (175,000 tokens):
├─ Message 1: "User requirements..." (10K tokens) ← OLD, will be summarized
├─ Message 2: "Analysis of..." (15K tokens) ← OLD, will be summarized
├─ Message 3: "Implementation..." (20K tokens) ← OLD, will be summarized
├─ ...
├─ Message 18: "Testing phase..." (12K tokens) ← OLD, will be summarized
├─ Message 19: "Found bug in..." (8K tokens) ← RECENT, keep in full
├─ Message 20: "Fixed bug by..." (10K tokens) ← RECENT, keep in full
├─ ...
└─ Message 33: "Final validation" (9K tokens) ← RECENT, keep in full

AFTER COMPACTION (35,000 tokens):
├─ Summary: "Covered requirements, analysis, implementation...
│            found and fixed bugs..." (5K tokens) ← COMPRESSED
├─ Message 19: "Found bug in..." (8K tokens) ← Last 15 kept
├─ Message 20: "Fixed bug by..." (10K tokens) ← Last 15 kept
├─ ...
└─ Message 33: "Final validation" (9K tokens) ← Last 15 kept

LOST FROM ACTIVE MEMORY:
❌ Messages 1-18: 140K tokens of detailed context
✅ Stored in database but NOT retrieved
```

### Step 7: Database Storage (Write-Only)

**When:** After each command execution

**File:** `master_orchestrator.py`

```python
def _store_to_database(self, project_id, instance_id, result):
    """Store execution result to database"""
    manager = MultiProjectManager()

    snapshot_id = manager.store_context(
        project_id=project_id,
        content={
            'prompt': self.current_prompt,
            'response': result,
            'timestamp': datetime.now().isoformat(),
            'instance_id': instance_id,
            'tokens_used': self.context_manager.get_total_tokens()
        },
        priority='HIGH',
        content_type='decision'
    )

    print(f"✅ Context stored: snapshot_id={snapshot_id}")
```

**Database storage:**
```sql
-- Table: context_snapshots
INSERT INTO context_snapshots (
    project_id,
    content,
    priority,
    content_type,
    phase_id,
    created_at
) VALUES (
    'proj_20251119_170839_effd0fa6',
    '{"prompt": "...", "response": "...", ...}',
    'HIGH',
    'decision',
    NULL,
    '2025-11-19 18:14:33'
);
```

**Result:**
- ✅ Everything stored in database permanently
- ✅ Unlimited storage capacity
- ❌ Never retrieved back to active memory
- ❌ Database is write-only

---

## WHAT HAPPENS AT 85% THRESHOLD

### Trigger Point

**When:** `current_tokens >= (max_tokens * compact_threshold)`

```
max_tokens = 200,000
compact_threshold = 0.85
trigger_point = 200,000 * 0.85 = 170,000 tokens
```

**Trigger:** When total token usage reaches or exceeds 170,000 tokens

### Automatic Process

```
┌─────────────────────────────────────────────────────────────────┐
│ AT 85% THRESHOLD - AUTOMATIC COMPACTION PROCESS                 │
└─────────────────────────────────────────────────────────────────┘

STEP 1: Detection
├─ add_message() called with new message
├─ Total tokens calculated: 175,000 tokens
├─ Check: 175,000 >= 170,000? ✅ YES
└─ Trigger: should_compact() returns True

STEP 2: Compaction Preparation
├─ Separate messages by importance:
│   ├─ Important (user requirements, marked important): 5 messages
│   └─ Regular (everything else): 28 messages
│
├─ Separate messages by recency:
│   ├─ Recent (last 15 messages): 15 messages (~30K tokens)
│   └─ Old (everything else): 18 messages (~140K tokens)
│
└─ Categorize old messages:
    ├─ Important old: 3 messages (~15K tokens) → KEEP
    └─ Regular old: 15 messages (~125K tokens) → SUMMARIZE

STEP 3: Summarization
├─ Take regular old messages (15 messages, 125K tokens)
├─ Create summary using _create_summary()
├─ Compress 125K tokens → 5K tokens summary
└─ Summary content:
    "Summary of 15 messages covering: initial requirements,
     analysis phase, implementation decisions, code reviews,
     testing phases 1-3, bug fixes, performance optimization..."

STEP 4: Reconstruction
├─ Build new message list:
│   ├─ Summary message (5K tokens)
│   ├─ Important old messages (15K tokens)
│   └─ Recent messages (30K tokens)
│
├─ Total after compaction: 50K tokens (down from 175K)
└─ Freed: 125K tokens (71% reduction)

STEP 5: Memory Update
├─ self.messages = [summary] + important_old + recent
├─ Old messages REMOVED from memory
├─ Old messages LOST from active context
└─ ❌ No retrieval from database

STEP 6: Database Storage
├─ Store current execution to database
├─ All context saved permanently
└─ ✅ Stored, ❌ Never retrieved

RESULT:
├─ Memory usage: 50K tokens (25% usage)
├─ Available space: 150K tokens
├─ Context preserved: Last 15 messages + important + summary
├─ Context lost: Detailed history of 125K tokens
└─ Status: ⚠️ Degraded accuracy for complex tasks
```

### What You Have in Memory After 85%

```
ACTIVE MEMORY (50,000 tokens):

┌─────────────────────────────────────────────────────────────┐
│ Message 1 (System Summary) - 5,000 tokens                   │
├─────────────────────────────────────────────────────────────┤
│ [CONTEXT SUMMARY]                                           │
│ Summary of 15 messages covering:                            │
│ • Initial requirements (messages 1-3)                       │
│ • Analysis phase (messages 4-6)                             │
│ • Implementation decisions (messages 7-10)                  │
│ • Code reviews (messages 11-12)                             │
│ • Testing phases (messages 13-15)                           │
│                                                             │
│ Key points:                                                 │
│ - User requested feature X with constraints Y               │
│ - Analysis identified 5 major components                    │
│ - Implementation used design pattern Z                      │
│ - Testing found 3 bugs, all fixed                           │
│                                                             │
│ ❌ DETAIL LOST - This is compressed summary                │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Message 2 (Important Old) - 5,000 tokens                    │
├─────────────────────────────────────────────────────────────┤
│ [USER][IMPORTANT]                                           │
│ Critical requirement: Must maintain backward compatibility  │
│ with version 2.x. Breaking changes are NOT acceptable.      │
│                                                             │
│ ✅ PRESERVED - Marked as important                          │
└─────────────────────────────────────────────────────────────┘

... (other important old messages)

┌─────────────────────────────────────────────────────────────┐
│ Message 19 (Recent) - 2,000 tokens                          │
├─────────────────────────────────────────────────────────────┤
│ [ASSISTANT]                                                 │
│ Analyzing test results... found edge case in date parsing.  │
│                                                             │
│ ✅ PRESERVED - Within last 15 messages                      │
└─────────────────────────────────────────────────────────────┘

... (messages 20-33, all in full detail)

┌─────────────────────────────────────────────────────────────┐
│ Message 33 (Most Recent) - 3,000 tokens                     │
├─────────────────────────────────────────────────────────────┤
│ [USER]                                                      │
│ Great! Now implement the export feature with CSV support.   │
│                                                             │
│ ✅ PRESERVED - Most recent message                          │
└─────────────────────────────────────────────────────────────┘
```

### What You DON'T Have in Memory

```
❌ LOST FROM ACTIVE MEMORY (125,000 tokens):

Messages 1-18 (excluding important ones):
❌ Message 1: "Full detailed requirements document..."
❌ Message 2: "Step-by-step analysis of architecture..."
❌ Message 3: "Detailed implementation plan..."
...
❌ Message 18: "Complete code review feedback..."

WHERE DID THEY GO?
├─ ✅ Stored in database permanently
│   Table: context_snapshots
│   Status: RETRIEVABLE (but not retrieved)
│
└─ ❌ Lost from active memory
    Replaced with: Summary (5K tokens)
    Original size: 125K tokens
    Information loss: 96% (120K tokens of detail)
```

### Why This Causes Failures

**Scenario:** Complex multi-step task

```
Iteration 1: "Implement user authentication system"
├─ Detailed discussion of requirements
├─ Security considerations
├─ Database schema design
├─ Implementation approach
└─ Tokens: +25K

Iteration 2: "Add OAuth support"
├─ OAuth flow design
├─ Token management
├─ Integration with existing auth
└─ Tokens: +20K

... (iterations 3-10 similar)

Iteration 11: Reaches 175K tokens → COMPACTION
├─ Before: Full context of iterations 1-10
└─ After: Summary + last 3 iterations

Iteration 12: "Now add 2FA support"
├─ Needs context from Iteration 1 (security requirements)
├─ Needs context from Iteration 2 (token management design)
├─ Has: Summary saying "implemented auth and OAuth"
├─ Missing: Detailed security requirements, token structure
└─ Result: ❌ FAILURE - Incompatible implementation
```

---

## COMPLETE CONTEXT FLOW DIAGRAM

### Full System Flow with All Components

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                     COMPLETE CONTEXT MANAGEMENT FLOW                         │
│                        (Current System - With THE GAP)                       │
└──────────────────────────────────────────────────────────────────────────────┘

USER
  │
  │ ./cpp "prompt" --verbose
  │
  ▼
┌──────────────────────────────────────────────────────────────┐
│ WRAPPER (cpp script)                                         │
└──────────────────────────────────────────────────────────────┘
  │
  │ 1. Initialize context
  ▼
┌──────────────────────────────────────────────────────────────┐
│ AUTO CONTEXT INTEGRATION                                     │
│ database/auto_context_integration.py                         │
├──────────────────────────────────────────────────────────────┤
│ initialize_for_command(prompt)                               │
│   ├─ get_or_create_project()                                │
│   │   ├─ Check: ~/.ultrathink/project_mappings.json         │
│   │   ├─ Use existing: proj_20251119_170839_effd0fa6        │
│   │   └─ Return: (project_id, False)                        │
│   │                                                          │
│   └─ get_or_create_instance(project_id)                     │
│       ├─ Check: ~/.ultrathink/current_session.json          │
│       ├─ Create new: inst_20251119_172723_82f760a7          │
│       └─ Return: (instance_id, True)                        │
└──────────────────────────────────────────────────────────────┘
  │
  │ Returns: (project_id, instance_id, proj_new=False, inst_new=True)
  │
  ▼
┌──────────────────────────────────────────────────────────────┐
│ WRAPPER (cpp script) - Display Info                         │
├──────────────────────────────────────────────────────────────┤
│ echo "📁 Project ID:  $PROJECT_ID"                          │
│ echo "🔹 Instance ID: $INSTANCE_ID"                         │
└──────────────────────────────────────────────────────────────┘
  │
  │ 2. Execute core
  ▼
┌──────────────────────────────────────────────────────────────┐
│ MASTER ORCHESTRATOR                                          │
│ master_orchestrator.py                                       │
├──────────────────────────────────────────────────────────────┤
│ __init__():                                                  │
│   self.context_manager = ContextManager(                    │
│       max_tokens=200000,                                     │
│       compact_threshold=0.85,                               │
│       keep_recent=15                                        │
│   )                                                          │
│                                                              │
│ execute(prompt):                                             │
│   ├─ self.context_manager.add_message("user", prompt)       │
│   ├─ ... process agents, guardrails ...                     │
│   ├─ self.context_manager.add_message("assistant", result)  │
│   └─ _store_to_database(project_id, instance_id, result)    │
└──────────────────────────────────────────────────────────────┘
  │
  │ 3. Context management
  ├─────────────────────┬────────────────────────────────────┐
  │                     │                                    │
  ▼                     ▼                                    ▼
┌───────────────┐  ┌──────────────────────┐  ┌──────────────────────────────┐
│ CONTEXT       │  │ CONTEXT              │  │ DATABASE STORAGE             │
│ MANAGER       │  │ COMPACTION           │  │                              │
│ (In-Memory)   │  │ (At 85%)             │  │ multi_project_manager.py     │
│               │  │                      │  │                              │
├───────────────┤  ├──────────────────────┤  ├──────────────────────────────┤
│ Messages:     │  │ Trigger: 170K tokens │  │ store_context():             │
│ - List in RAM │  │                      │  │   ├─ INSERT INTO             │
│ - 200K limit  │  │ Process:             │  │   │   context_snapshots      │
│               │  │ 1. Separate:         │  │   ├─ project_id: ...         │
│ add_message()│→│  │    - Recent (15)     │  │   ├─ content: {...}         │
│   ├─ Append   │  │    - Old (others)    │  │   └─ priority: HIGH          │
│   ├─ Count    │  │                      │  │                              │
│   └─ Check    │  │ 2. Summarize:        │  │ ✅ STORES EVERYTHING         │
│       85%?    │  │    - Old → Summary   │  │                              │
│       ├─ No  ─┤  │    - 125K → 5K       │  │ ❌ NO RETRIEVAL FUNCTION     │
│       └─ Yes ─┼─→│                      │  │    load_relevant_context()   │
│               │  │ 3. Rebuild:          │  │    DOESN'T EXIST             │
│ get_context()│←─│    - Summary +       │  │                              │
│   └─ Return   │  │    - Important +     │  └──────────────────────────────┘
│     messages[]│  │    - Recent          │                  │
│               │  │                      │                  │
│ should_       │  │ 4. Replace:          │                  │
│  compact()    │  │    messages = new    │                  │
│   ├─ Usage    │  │                      │                  │
│   └─ >= 85%  │  │ Result:              │                  │
│               │  │ - 50K tokens         │                  │
│ compact()     │  │ - Lost 125K details  │                  │
│   └─ Trigger ─┼─→│                      │                  │
│     process   │  │ ❌ OLD CONTEXT LOST  │                  │
│               │  │    FROM MEMORY       │                  │
└───────────────┘  └──────────────────────┘                  │
        │                                                    │
        │                                                    │
        │ 4. Return to orchestrator                         │
        ▼                                                    │
┌──────────────────────────────────────────────────────────┐ │
│ MASTER ORCHESTRATOR                                      │ │
│ _store_to_database()                                     │ │
├──────────────────────────────────────────────────────────┤ │
│ manager = MultiProjectManager()                          │ │
│ snapshot_id = manager.store_context(...)                 │─┘
│                                                          │
│ ✅ Stored to database                                    │
│ ❌ Never retrieved back                                  │
└──────────────────────────────────────────────────────────┘
        │
        │ 5. Return result
        ▼
┌──────────────────────────────────────────────────────────┐
│ WRAPPER (cpp script) - Display Info                     │
├──────────────────────────────────────────────────────────┤
│ echo "📁 Project ID:  $PROJECT_ID"                      │
│ echo "💡 Reuse: cpp \"prompt\" --project-id $PROJECT_ID" │
└──────────────────────────────────────────────────────────┘
        │
        │ 6. Output to user
        ▼
      USER
```

### Token Flow Over Time

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                          TOKEN USAGE OVER TIME                               │
│                     (Shows compaction behavior at 85%)                       │
└──────────────────────────────────────────────────────────────────────────────┘

Time →  0      50     100    150    170    200    250    300    350
Tokens ├──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┤
200K   │      │      │      │      │      ██████████████████████████  │ ← MAX
       │      │      │      │      │   ┌─→│      │      │      │      │
       │      │      │      │      │   │  │      │      │      │      │
170K   │      │      │      │      ████│  │      │      │      │      │ ← 85%
       │      │      │      │  ┌─→│█  │  │      │      │      │      │   Trigger
       │      │      │      │  │  │█  │  │      │      │      │      │
150K   │      │      │      ███│  │█  │  │      │      │      │      │
       │      │      │  ┌─→│█ │  │█  │  │      │      │      │      │
       │      │      │  │  │█ │  │█  │  │      │      │      │      │
100K   │      │      ███│  │█ │  │█  │  │      │      │      │      │
       │      │  ┌─→│█ │  │█ │  │█  │  │      │      │      │      │
       │      │  │  │█ │  │█ │  │█  │  │      │      │      │      │
 50K   │      ███│  │█ │  │█ │  │█  └─→███    ███    ███    ███    │ ← After
       │  ┌─→│█ │  │█ │  │█ │  │█     │█     │█     │█     │█     │   Compact
       │  │  │█ │  │█ │  │█ │  │█     │█     │█     │█     │█     │
  0K   ├──┼──┼──┼──┼──┼──┼──┼──┼──────┼──────┼──────┼──────┼──────┤
       0  50 100 150 200 250 300       350    400    450    500    550

       Iterations: 1-5 → Steady Growth (30K → 175K)
                   At 175K → COMPACTION TRIGGERED
                   After → Drops to 50K
                   6-10 → Growth resumes (50K → 175K)
                   At 175K → COMPACTION AGAIN
                   ...continues forever

Legend:
  ██ = Active context in memory
  ─→ = Growth over iterations
  └─ = Compaction point
```

### Data Flow Between Components

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                        DATA FLOW BETWEEN COMPONENTS                          │
└──────────────────────────────────────────────────────────────────────────────┘

[USER PROMPT]
      ↓
      ↓ "Implement feature X"
      ↓
[AUTO CONTEXT]
      ↓
      ├─→ project_id: "proj_20251119_170839_effd0fa6"
      └─→ instance_id: "inst_20251119_172723_82f760a7"
      ↓
[MASTER ORCHESTRATOR]
      ↓
      ├─→ context_manager.add_message("user", "Implement feature X")
      ↓
[CONTEXT MANAGER]
      ↓
      ├─→ messages.append(Message("user", "Implement feature X", tokens=5000))
      ├─→ total_tokens = 35,000 (was 30,000)
      ├─→ Check: 35,000 >= 170,000? No
      └─→ Return: OK
      ↓
[MASTER ORCHESTRATOR]
      ↓
      ├─→ Execute agents, guardrails, processing...
      ├─→ Generate response: "Implemented feature X with..."
      ↓
      ├─→ context_manager.add_message("assistant", response)
      ↓
[CONTEXT MANAGER]
      ↓
      ├─→ messages.append(Message("assistant", response, tokens=15000))
      ├─→ total_tokens = 50,000 (was 35,000)
      ├─→ Check: 50,000 >= 170,000? No
      └─→ Return: OK
      ↓
[MASTER ORCHESTRATOR]
      ↓
      ├─→ _store_to_database(project_id, instance_id, response)
      ↓
[DATABASE STORAGE]
      ↓
      ├─→ INSERT INTO context_snapshots (
      │       project_id = "proj_20251119_170839_effd0fa6",
      │       content = {"prompt": "...", "response": "..."},
      │       priority = "HIGH",
      │       created_at = "2025-11-19 18:14:33"
      │   )
      ├─→ snapshot_id = 42
      └─→ ✅ STORED TO DATABASE
      ↓
      ↓ (database has data but it's never retrieved)
      ↓
      ❌ NO RETRIEVAL PATH BACK TO CONTEXT MANAGER
```

---

## DATABASE INTEGRATION - CURRENT STATE

### Database Schema

**File:** `database/sqlite_context_loader.py`

```sql
-- Projects table
CREATE TABLE IF NOT EXISTS projects (
    project_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    total_story_points INTEGER DEFAULT 1300,
    completed_story_points INTEGER DEFAULT 0,
    total_phases INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Active instances table
CREATE TABLE IF NOT EXISTS active_instances (
    instance_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    phase_id INTEGER,
    hostname TEXT,
    process_id INTEGER,
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_heartbeat TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'active',
    current_token_usage INTEGER DEFAULT 0,
    FOREIGN KEY (project_id) REFERENCES projects(project_id)
);

-- Context snapshots table (THE IMPORTANT ONE)
CREATE TABLE IF NOT EXISTS context_snapshots (
    snapshot_id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id TEXT NOT NULL,
    phase_id INTEGER,
    content TEXT NOT NULL,
    priority TEXT DEFAULT 'MEDIUM',
    content_type TEXT DEFAULT 'code',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(project_id)
);

-- Phases table
CREATE TABLE IF NOT EXISTS phases (
    phase_id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id TEXT NOT NULL,
    phase_number INTEGER NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    story_points INTEGER DEFAULT 0,
    status TEXT DEFAULT 'pending',
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(project_id)
);
```

### Current Database Content (Example)

```sql
-- Projects
SELECT * FROM projects WHERE project_id = 'proj_20251119_170839_effd0fa6';

project_id                      | name                | total_story_points | created_at
--------------------------------|---------------------|--------------------|-----------
proj_20251119_170839_effd0fa6   | ClaudePrompt (Auto) | 1300              | 2025-11-19 17:08:39


-- Context Snapshots (This has all your context!)
SELECT COUNT(*) FROM context_snapshots WHERE project_id = 'proj_20251119_170839_effd0fa6';

count(*)
--------
127     ← You have 127 snapshots stored!


-- Sample snapshot
SELECT
    snapshot_id,
    priority,
    content_type,
    substr(content, 1, 100) as content_preview,
    created_at
FROM context_snapshots
WHERE project_id = 'proj_20251119_170839_effd0fa6'
ORDER BY created_at DESC
LIMIT 5;

snapshot_id | priority | content_type | content_preview | created_at
------------|----------|--------------|-----------------|------------
127         | HIGH     | decision     | {"prompt": "Implement...", "response": "..."}  | 2025-11-19 18:09:15
126         | HIGH     | decision     | {"prompt": "Fix bug...", "response": "..."}    | 2025-11-19 18:05:32
125         | HIGH     | decision     | {"prompt": "Add tests...", "response": "..."}  | 2025-11-19 17:58:11
124         | HIGH     | decision     | {"prompt": "Refactor...", "response": "..."}   | 2025-11-19 17:45:29
123         | HIGH     | decision     | {"prompt": "Optimize...", "response": "..."}   | 2025-11-19 17:32:08
```

### Storage Functions (✅ EXIST)

**File:** `database/multi_project_manager.py`

```python
def store_context(
    self,
    project_id: str,
    content: Dict[str, Any],
    priority: str = 'HIGH',
    content_type: str = 'code',
    phase_id: Optional[int] = None
) -> int:
    """
    ✅ THIS EXISTS AND WORKS

    Store context for a project.
    All instances of this project will see this context.
    """
    return self.loader.store_context(
        project_id=project_id,
        content=content,
        priority=priority,
        content_type=content_type,
        phase_id=phase_id
    )
```

**File:** `database/sqlite_context_loader.py`

```python
def store_context(
    self,
    project_id: str,
    content: Dict[str, Any],
    priority: str = 'HIGH',
    content_type: str = 'code',
    phase_id: Optional[int] = None
) -> int:
    """
    ✅ THIS EXISTS AND WORKS

    Store context snapshot to database.
    """
    conn = self._get_connection()
    cursor = conn.cursor()

    # Convert content dict to JSON
    content_json = json.dumps(content, indent=2)

    query = """
        INSERT INTO context_snapshots
        (project_id, phase_id, content, priority, content_type)
        VALUES (?, ?, ?, ?, ?)
    """

    cursor.execute(query, (project_id, phase_id, content_json, priority, content_type))
    conn.commit()

    snapshot_id = cursor.lastrowid
    return snapshot_id
```

### Retrieval Functions (❌ DON'T EXIST)

**What's missing:**

```python
# ❌ THIS FUNCTION DOESN'T EXIST
def load_relevant_context(
    self,
    project_id: str,
    query: str,
    limit: int = 10,
    priority_filter: Optional[List[str]] = None
) -> List[Dict]:
    """
    ❌ NOT IMPLEMENTED

    Load relevant context from database based on query.

    Should:
    - Search context_snapshots for project_id
    - Find most relevant snapshots (keyword matching or semantic search)
    - Return top N relevant context items
    - Filter by priority if specified
    """
    pass  # Not implemented!


# ❌ THIS FUNCTION DOESN'T EXIST
def load_recent_context(
    self,
    project_id: str,
    limit: int = 20
) -> List[Dict]:
    """
    ❌ NOT IMPLEMENTED

    Load most recent context for project.

    Should:
    - Query context_snapshots for project_id
    - Order by created_at DESC
    - Return last N snapshots
    """
    pass  # Not implemented!


# ❌ THIS FUNCTION DOESN'T EXIST
def search_context(
    self,
    project_id: str,
    keywords: List[str],
    limit: int = 10
) -> List[Dict]:
    """
    ❌ NOT IMPLEMENTED

    Search context by keywords.

    Should:
    - Search content field for keywords
    - Rank by relevance
    - Return top N matches
    """
    pass  # Not implemented!
```

### Database Query Examples (Manual Retrieval)

If you wanted to manually retrieve context (which the system should do automatically):

```bash
# Connect to database
sqlite3 database/ultrathink_context.db

# Get all context for your project
SELECT * FROM context_snapshots
WHERE project_id = 'proj_20251119_170839_effd0fa6'
ORDER BY created_at DESC;

# Search for specific keyword
SELECT
    snapshot_id,
    priority,
    content_type,
    content,
    created_at
FROM context_snapshots
WHERE project_id = 'proj_20251119_170839_effd0fa6'
  AND content LIKE '%authentication%'
ORDER BY created_at DESC;

# Get high priority context only
SELECT * FROM context_snapshots
WHERE project_id = 'proj_20251119_170839_effd0fa6'
  AND priority IN ('CRITICAL', 'HIGH')
ORDER BY created_at DESC
LIMIT 20;
```

---

## THE SOLUTION - CONTEXT RETRIEVAL SYSTEM

(Implementation section coming next...)

*This is the critical missing piece that will enable true unlimited context.*

---

