# ULTRATHINK Response Format Template

**STATUS**: PERMANENT - This format is MANDATORY for all Claude Code responses to ULTRATHINK prompts.

**COMMITMENT DATE**: 2025-11-09
**USER TIME INVESTED**: Multiple hours
**REQUIREMENT**: Format must survive window close and computer restart

---

## Quick Reference

### Section Header
```
================================================================================
SECTION NAME
================================================================================
```

### Content with [VERBOSE] Tags
```
[VERBOSE] Main point
[VERBOSE]   ✓ Sub-item (3-space indent)
[VERBOSE]   ✓ Another sub-item
```

### Spacing
- 1 blank line between subsections
- 1 blank line before/after headers
- 1 blank line before/after code blocks
- 1 blank line before/after tables
- 1 blank line before/after `---` separators

### Code Block
````
```python
def example():
    return "code here"
```
````

### Table
```
| Column 1 | Column 2 |
|----------|----------|
| Data     | Data     |
```

### Visual Elements
- ✅ Success
- ❌ Error
- 🟡 Warning
- ✓ Checkmark
- `---` Separator

---

## Detailed Specification

### 1. Section Headers

**Format**:
```
================================================================================
SECTION NAME
================================================================================
```

**Rules**:
- EXACTLY 80 equals signs (=)
- Optional emoji prefix (🎯, 📊, ✅, 🔍, 💡, 🔥)
- Title in ALL CAPS or Title Case
- One blank line before header
- One blank line after header

**Examples**:
```
================================================================================
🎯 IMPLEMENTATION PLAN
================================================================================

================================================================================
SECTION 1: ANALYSIS
================================================================================

================================================================================
✅ SUMMARY
================================================================================
```

---

### 2. [VERBOSE] Tags

**Format**:
```
[VERBOSE] Main point
[VERBOSE]   ✓ Sub-item (exactly 3 spaces)
[VERBOSE]   ✓ Another sub-item
[VERBOSE]     • Nested item (6 spaces = 2 levels)
```

**Rules**:
- Use for enumerated items and stage descriptions
- Main items start at column 0
- Sub-items indented with EXACTLY 3 spaces
- Nested items: 6 spaces (3 per level)
- Use ✓ checkmarks for completed/valid items
- Use • bullets for nested details

**Example**:
```
[VERBOSE] Analyzing prompt structure...
[VERBOSE]   ✓ Intent detected: code_generation
[VERBOSE]   ✓ Complexity: moderate
[VERBOSE]   ✓ Required components: [guardrails, verification]
[VERBOSE]     • Guardrail layers: 7
[VERBOSE]     • Verification methods: 5
[VERBOSE]   ✓ Duration: 0.14s
```

---

### 3. Spacing (CRITICAL)

**Rules**:

| Element                    | Before | After |
|----------------------------|--------|-------|
| Section header             | 1 line | 1 line |
| Subsection                 | 1 line | 1 line |
| Paragraph                  | 1 line | 1 line |
| `---` separator            | 1 line | 1 line |
| Code block                 | 1 line | 1 line |
| Table                      | 1 line | 1 line |
| [VERBOSE] group            | 0      | 1 line |

**Example (showing spacing)**:
```
[VERBOSE] Group of items:
[VERBOSE]   ✓ Item 1
[VERBOSE]   ✓ Item 2
[VERBOSE]   ✓ Item 3
                              ← 1 blank line here

Next paragraph or section starts here.
                              ← 1 blank line here

---
                              ← 1 blank line here

Major section separator.
```

---

### 4. Code Blocks

**Format**:
````
Brief description of what code does:

```language
code here
```
````

**Rules**:
- ALWAYS specify language (python, bash, javascript, json, etc.)
- Add brief description BEFORE code block
- One blank line before description
- One blank line after code block
- Indent consistently within code

**Example**:
````
Implementation of rate limiter:

```python
class RateLimiter:
    def __init__(self, max_calls=500, time_window=360):
        self.max_calls = max_calls
        self.time_window = time_window
```

This allows 500 calls per 6 minutes.
````

---

### 5. Tables

**Format**:
```
| Column 1      | Column 2      | Column 3      |
|---------------|---------------|---------------|
| Data          | Data          | Data          |
| More data     | More data     | More data     |
```

**Rules**:
- Use markdown table format
- Align columns with `|` separators
- Header row followed by separator row
- One blank line before table
- One blank line after table
- Use for comparisons, metrics, structured data

**Example**:
```
Configuration comparison:

| Metric        | Original | Your Config | Delta   |
|---------------|----------|-------------|---------|
| Max calls     | 50       | 500         | +1000%  |
| Time window   | 60s      | 360s        | +600%   |
| Effective rate| 50/min   | 83.3/min    | +166%   |

The new configuration provides much higher capacity.
```

---

### 6. Horizontal Separators

**Format**:
```
---
```

**Rules**:
- Use exactly 3 hyphens (---)
- One blank line before
- One blank line after
- Use to separate major items within a section
- Don't overuse (not after every paragraph)

**Example**:
```
First major point with several paragraphs of explanation.
This continues the same major point.

---

Second major point, clearly separated from the first.
```

---

### 7. Visual Elements

**Emojis** (use for visual landmarks):
- 🎯 Goals, targets, objectives
- 📊 Data, statistics, metrics
- ✅ Success, completion, approval
- ❌ Error, failure, rejection
- 🟡 Warning, caution, attention needed
- 🔍 Analysis, investigation, search
- 💡 Ideas, insights, recommendations
- 🔥 Important, urgent, critical
- ⏱️ Time-related, duration, timing
- ✓ Checkmark for valid/completed items

**Text Emphasis**:
- **Bold** for important terms (use sparingly)
- `code style` for file names, variables, commands, technical terms
- ALL CAPS for critical warnings (very sparingly)

**Example**:
```
[VERBOSE] ✅ Verification complete
[VERBOSE]   ✓ All checks passed
[VERBOSE]   ✓ Confidence: 99.3%
[VERBOSE]   ⏱️ Duration: 1.28s

⚠️ **WARNING**: Rate limit approaching!
```

---

## Complete Example Response

````
================================================================================
🎯 ULTRATHINK RESPONSE: EXAMPLE ANALYSIS
================================================================================

Your request: Analyze the configuration
Target: Determine optimal settings


================================================================================
SECTION 1: ANALYSIS
================================================================================

[VERBOSE] Analyzing configuration...
[VERBOSE]   ✓ Parameter 1: Valid (within range 0-100)
[VERBOSE]   ✓ Parameter 2: Valid (within range 0-100)
[VERBOSE]   ✓ Duration: 0.15s

Brief explanatory paragraph here, with proper spacing before and after.

---

**Comparison Table**:

| Metric    | Current | Recommended | Change |
|-----------|---------|-------------|--------|
| Param 1   | 50      | 75          | +50%   |
| Param 2   | 100     | 150         | +50%   |

Analysis shows recommended values provide better performance.


================================================================================
SECTION 2: IMPLEMENTATION
================================================================================

[VERBOSE] Implementation steps:
[VERBOSE]   ✓ Step 1: Update configuration file
[VERBOSE]   ✓ Step 2: Restart service
[VERBOSE]   ✓ Step 3: Verify changes

Code to update configuration:

```python
config = {
    'param1': 75,
    'param2': 150
}
```

This implements the recommended changes.


================================================================================
✅ SUMMARY
================================================================================

[VERBOSE] Results:
[VERBOSE]   ✓ Analysis complete
[VERBOSE]   ✓ Recommendations provided
[VERBOSE]   ✓ Implementation code ready

Next step: Apply changes and test.
````

---

## Why This Format?

Based on extensive user feedback:

1. ✅ **Readability**: Proper spacing prevents text cramming
2. ✅ **Concentration**: Visual hierarchy maintains focus
3. ✅ **Comprehension**: Clear structure aids understanding
4. ✅ **Scannability**: Easy to find specific information
5. ✅ **Professional**: Terminal-style appearance
6. ✅ **Interest**: Visual elements create engagement

**User Quote**:
> "when you are presenting the text it should look like more readable and
> attractive so that you should get an interest and you get concentrated
> when you are reading"

This format achieves that goal.

---

## Commitment

This format is **PERMANENT** and applies to:
- ✅ ALL ULTRATHINK responses
- ✅ ALL sessions (even after restart)
- ✅ ALL prompts processed through `ultrathinkc`

**Effective**: 2025-11-09 and forever
**Reason**: User invested hours developing this standard
**Requirement**: Must survive window close and computer restart

Claude Code will ALWAYS use this format for ULTRATHINK responses.
