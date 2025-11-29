# Universal Usage Guide - Orchestration System Everywhere

**Use your 96-100% confidence orchestration system in ANY environment:**
- ✅ Claude Code (any directory)
- ✅ Claude Web (chat.claude.com)
- ✅ Terminal/Command Line
- ✅ Any Python project
- ✅ API integration

---

## 🚀 QUICK START (3 Steps)

### Step 1: Activate Bash Configuration

```bash
source ~/.bashrc
```

This activates:
- `CLAUDE_CODE_MAX_OUTPUT_TOKENS=100000` (maximized for your Claude MAX subscription)
- `orchestrate` command (works from ANY directory)
- `ultrathink` command (enhanced autonomous mode)

### Step 2: Test It Works

```bash
# From ANY directory
cd ~
orchestrate "explain this directory"

# Or use ULTRATHINK mode
ultrathink "what can you do?"
```

### Step 3: Use Everywhere

See examples below for your specific use case.

---

## 📍 USE CASE 1: Claude Code (ANY Directory)

### Basic Usage
```bash
# Navigate to ANY project
cd /path/to/your/project

# Run orchestration
orchestrate "analyze this codebase"
orchestrate "fix all bugs"
orchestrate "write comprehensive tests"
```

### With Claude API
```bash
orchestrate "implement new feature" --claude
```

### Save Results
```bash
orchestrate "refactor code" --output results.json
```

### ULTRATHINK Mode (Autonomous)
```bash
ultrathink "build a REST API with full validation"
ultrathink "optimize performance" --claude
```

---

## 🌐 USE CASE 2: Claude Web (chat.claude.com)

### Method 1: Generate Web-Compatible Prompt

```bash
ultrathink "your request here" --mode web-compatible
```

**Copy the output and paste into chat.claude.com**

### Method 2: Export as Template

```bash
ultrathink "build authentication system" --mode web-compatible --export web-prompt.json
```

Open `web-prompt.json`, copy the `ultrathink_prompt` field, paste into Claude Web.

### Example Web-Compatible Prompt

Run this:
```bash
ultrathink "explain machine learning" --mode web-compatible
```

You'll get a prompt like:
```
🔥 ULTRATHINK MODE ACTIVATED 🔥

Process this request using the ULTRATHINK framework:

### 1. AUTONOMOUS EXECUTION MODE
- TAKE FULL CONTROL: Analyze, plan, execute without confirmation
- CONFIDENCE-DRIVEN: Target 96-100% confidence
- PRODUCTION-READY ONLY: Deployment-ready quality

### 2. QUALITY ASSURANCE FRAMEWORK
[... comprehensive validation framework ...]

USER REQUEST: explain machine learning

BEGIN EXECUTION NOW 🚀
```

**Copy and paste this entire block into Claude Web!**

---

## 💻 USE CASE 3: Terminal (Command Line)

### From Your Home Directory
```bash
cd ~
orchestrate "list all Python projects in subdirectories"
```

### From Any Project Directory
```bash
cd /home/user01/my-project
orchestrate "analyze project structure" --context auto
```

### Show Current Directory Context
```bash
orchestrate --show-dir
```

### Verbose Mode
```bash
orchestrate "complex task" --verbose
```

---

## 🐍 USE CASE 4: Python Integration

### Basic Python Script

```python
#!/usr/bin/env python3
import sys
sys.path.insert(0, '/home/user01/claude-test/ClaudePrompt')

from master_orchestrator import MasterOrchestrator

orchestrator = MasterOrchestrator(min_confidence_score=96.0)
result = orchestrator.process("Your prompt here")

if result.success:
    print(f"Confidence: {result.confidence_score:.2f}%")
    print(f"Output: {result.output}")
else:
    print(f"Failed: {result.errors}")
```

### With Claude API

```python
from claude_integration import ClaudeOrchestrator

orchestrator = ClaudeOrchestrator()
response = orchestrator.process("Write a function...")

print(response.response_text)
print(f"Confidence: {response.orchestration_result.confidence_score:.2f}%")
```

---

## 🔧 USE CASE 5: API Integration

### REST API Example

```python
from flask import Flask, request, jsonify
import sys
sys.path.insert(0, '/home/user01/claude-test/ClaudePrompt')
from master_orchestrator import MasterOrchestrator

app = Flask(__name__)
orchestrator = MasterOrchestrator()

@app.route('/process', methods=['POST'])
def process_prompt():
    data = request.json
    result = orchestrator.process(data['prompt'])

    return jsonify({
        'success': result.success,
        'confidence': result.confidence_score,
        'output': result.output,
        'iterations': result.iterations_performed
    })

if __name__ == '__main__':
    app.run(port=5000)
```

---

## 🎯 CONFIGURATION OPTIONS

### Confidence Levels

```bash
# Stricter (98%+)
orchestrate "critical task" --min-confidence 98.0

# Standard (96%+) - Default
orchestrate "normal task"

# Lenient (90%+)
orchestrate "exploratory task" --min-confidence 90.0
```

### Context Modes

```bash
# Auto (smart context gathering)
orchestrate "analyze" --context auto

# Minimal (no directory context)
orchestrate "simple question" --context minimal

# Full (comprehensive context)
orchestrate "refactor" --context full
```

---

## 📊 TOKEN OPTIMIZATION

### Your Current Configuration

```bash
# In .bashrc
CLAUDE_CODE_MAX_OUTPUT_TOKENS=100000
```

**Why 100,000 is good:**
- Claude Sonnet 4.5 actual limit: ~64K output tokens
- Setting 100K future-proofs for model upgrades
- Ensures you never artificially limit yourself
- Your Claude MAX subscription ($200) is maximized

### Session Token Budget

```
Current Session: 200,000 INPUT tokens
- Remaining: Check status bar in Claude Code
- This is for context/conversation, not output
```

### Cost Estimation

```python
# Check cost before running
orchestrate "large task" --claude --verbose
# Shows estimated cost in output
```

---

## 🎨 ULTRATHINK MODES

### 1. Full Mode (Default)
```bash
ultrathink "your task"
```
- Complete orchestration pipeline
- All guardrails and verification
- 96-100% confidence target
- Local execution

### 2. Web-Compatible Mode
```bash
ultrathink "your task" --mode web-compatible
```
- Formatted for Claude Web
- No code execution needed
- Paste-and-go ready
- Comprehensive validation framework included

### 3. Minimal Mode
```bash
ultrathink "your task" --mode minimal
```
- Core directives only
- Fastest execution
- Still targets 96%+ confidence

### 4. API Mode
```bash
ultrathink "your task" --claude
```
- Uses Claude API
- Full orchestration pipeline
- Cost tracking included

---

## 📁 WORKING FROM ANY DIRECTORY

### Example Workflow

```bash
# Start in home directory
cd ~

# Check what orchestration sees
orchestrate --show-dir

# Move to a project
cd /home/user01/my-dotnet-project

# Run analysis (auto-detects .NET project)
orchestrate "analyze this .NET application"

# Move to another project
cd /var/www/my-website

# Run task (auto-detects web project)
orchestrate "optimize HTML performance"
```

**The orchestrator automatically detects:**
- Git repositories
- Python projects (setup.py, requirements.txt, etc.)
- Node.js projects (package.json)
- .NET projects (*.csproj)
- Project structure and contents

---

## 🔒 SECURITY & PRIVACY

### API Keys

Your `.bashrc` contains:
```bash
ANTHROPIC_API_KEY="sk-ant-api03-..."
```

**Security recommendations:**
1. ✅ Already set in `.bashrc` (private to your user)
2. ✅ Not checked into Git
3. ✅ Protected by file permissions

### Guardrails Protection

Every prompt goes through:
1. **Prompt Shields** - Jailbreak prevention
2. **Content Filtering** - Harmful content detection
3. **PHI Detection** - Privacy protection (HIPAA)
4. **Groundedness** - Factual accuracy
5. **Compliance** - Best practices validation

---

## 🎓 EXAMPLES BY SCENARIO

### Scenario 1: New Project Analysis

```bash
cd /path/to/unknown-project
orchestrate "analyze this project and explain its architecture" --verbose
```

### Scenario 2: Bug Fixing

```bash
cd /path/to/buggy-project
ultrathink "find and fix all bugs with comprehensive testing"
```

### Scenario 3: Code Generation

```bash
orchestrate "write a Python FastAPI app with authentication" --claude --output api-design.json
```

### Scenario 4: Documentation

```bash
ultrathink "generate comprehensive README with setup instructions" --mode web-compatible --export readme-prompt.json
```

### Scenario 5: Refactoring

```bash
orchestrate "refactor code following SOLID principles" --min-confidence 98.0
```

---

## 🛠️ TROUBLESHOOTING

### Issue: Command not found
```bash
# Solution: Reload bashrc
source ~/.bashrc
```

### Issue: Import errors
```bash
# Solution: Check ORCHESTRATION_HOME
echo $ORCHESTRATION_HOME
# Should show: /home/user01/claude-test/ClaudePrompt

# If not set:
export ORCHESTRATION_HOME="/home/user01/claude-test/ClaudePrompt"
```

### Issue: API key not found
```bash
# Solution: Check if set
echo $ANTHROPIC_API_KEY

# If empty, reload bashrc:
source ~/.bashrc
```

### Issue: Low confidence scores
```bash
# Solution: Use more specific prompts or ULTRATHINK mode
ultrathink "very specific detailed request" --verbose
```

---

## 📈 MAXIMIZING YOUR CLAUDE MAX SUBSCRIPTION

### 1. Use Token Budget Wisely

```bash
# For simple questions: local mode
orchestrate "what is this?"

# For complex tasks: API mode with full orchestration
ultrathink "build complete system" --claude
```

### 2. Batch Processing

```bash
# Process multiple tasks in one session
ultrathink "task 1: ... task 2: ... task 3: ..." --output batch-results.json
```

### 3. Export for Reuse

```bash
# Generate templates for common tasks
ultrathink "code review checklist" --mode web-compatible --export code-review-template.json
```

### 4. Cost Tracking

```bash
# Always use --verbose with --claude to see costs
orchestrate "expensive task" --claude --verbose
# Output shows: Cost: $0.123456
```

---

## 🎯 BEST PRACTICES

### 1. Choose the Right Tool

| Task | Use This | Why |
|------|----------|-----|
| Simple question | `orchestrate "question"` | Fast, local |
| Complex autonomous task | `ultrathink "task"` | Full ULTRATHINK directives |
| Claude Web | `ultrathink --mode web-compatible` | No local setup needed |
| Production critical | `ultrathink --claude --min-confidence 98` | API + strict quality |
| Exploration | `orchestrate --context auto` | Smart context gathering |

### 2. Confidence Thresholds

- **Critical/Production**: 98%+
- **Standard**: 96% (default)
- **Exploratory**: 90%

### 3. Save Important Results

```bash
orchestrate "important task" --output $(date +%Y%m%d)-results.json
```

### 4. Use ULTRATHINK for Autonomy

When you DON'T want to be asked for confirmation:
```bash
ultrathink "build entire system from scratch"
```

The ULTRATHINK mode activates:
- AUTONOMOUS EXECUTION (no confirmations)
- PRODUCTION-READY standards
- 100% SUCCESS RATE targeting
- FAIL FAST, FIX FASTER iteration
- PARALLEL processing

---

## 📚 SUMMARY: Quick Command Reference

```bash
# Basic orchestration (local)
orchestrate "your prompt"

# With Claude API
orchestrate "your prompt" --claude

# ULTRATHINK mode (autonomous)
ultrathink "your task"

# For Claude Web
ultrathink "your task" --mode web-compatible

# Show directory context
orchestrate --show-dir

# Verbose output
orchestrate "task" --verbose

# Save results
orchestrate "task" --output file.json

# Set confidence threshold
orchestrate "task" --min-confidence 98.0

# Show ULTRATHINK directives
ultrathink --show-directives

# Export template for Claude Web
ultrathink "task" --mode web-compatible --export template.json
```

---

## 🎉 YOU'RE READY!

**Your orchestration system now works:**
- ✅ In ANY directory
- ✅ With Claude Code
- ✅ With Claude Web
- ✅ Via Terminal
- ✅ In Python scripts
- ✅ Through APIs

**With your Claude MAX subscription ($200), you get:**
- ✅ 100,000 output token limit (maximized)
- ✅ 200,000 input token budget per session
- ✅ Full access to Claude Sonnet 4.5
- ✅ Comprehensive orchestration pipeline
- ✅ 96-100% confidence targeting
- ✅ Autonomous ULTRATHINK execution

Start using it NOW:
```bash
source ~/.bashrc
ultrathink "show me what you can do"
```

🚀 **HAPPY ORCHESTRATING!** 🚀
