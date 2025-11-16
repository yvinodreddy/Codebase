# Claude Code - Quick Reference Card
## Keep This Open While You Work

---

## 🚀 Keyboard Shortcuts (Memorize These First!)

| Shortcut | Action | Use Case |
|----------|--------|----------|
| **Tab** | Toggle thinking ON/OFF | Complex problems need thinking |
| **Ctrl+O** | View transcript | See conversation history |
| **Ctrl+R** | Search history | Find past commands |
| **Ctrl+B** | Start background command | Dev servers, long-running tasks |
| **Ctrl+G** | Edit in external editor | Complex multi-line prompts |
| **Esc** | Interrupt Claude | Stop current operation |
| **Shift+Tab** | Toggle auto-accept edits | Speed up or slow down |

---

## 📝 Essential Slash Commands (Use Daily)

```bash
/help                    # Get help on any topic
/permissions             # View/manage tool permissions
/model                   # Switch AI models (Haiku/Sonnet/Opus)
/context                 # Check how much context you're using
/memory                  # View or edit conversation memory
/resume                  # Switch between conversations
/rewind                  # Undo recent code changes
/usage                   # Check your plan limits
/cost                    # View session costs
/export                  # Export conversation
```

---

## 💡 Magic Phrases (Say These Exactly)

| Say This | Claude Does This |
|----------|------------------|
| `think` | Enters thinking mode (deeper reasoning) |
| `think harder` | More intensive thinking |
| `ultrathink` | Maximum reasoning power |
| `plan this` | Creates step-by-step execution plan |
| `in parallel: 1. ... 2. ... 3. ...` | Executes tasks simultaneously |

---

## 📁 @-Mention Patterns (Context Injection)

```bash
@file.py                 # Add specific file
@folder/                 # Add entire folder
@*.json                  # Add all matching files
@src/**/*.py            # Recursive pattern matching

# Multiple mentions
@config.py @tests/ @README.md

# With questions
@auth.py how does login work?
@api/ find the bug in user endpoint
```

**Tip**: Press Tab while typing @ for autocomplete!

---

## 🔒 Permission Quick Setup

```bash
# Allow all npm commands
/permissions allow Bash(npm:*)

# Allow all git commands
/permissions allow Bash(git:*)

# Allow Python execution
/permissions allow Bash(python:*)

# Allow Docker commands
/permissions allow Bash(docker:*)

# Allow reading project files
/permissions allow Read(//home/user01/projects/**)

# Allow writing to src folder
/permissions allow Write(//home/user01/projects/src/**)

# Deny dangerous commands
/permissions deny Bash(rm -rf:*)
```

---

## 🎯 Common Task Templates

### 1. Fix a Bug
```
The [feature] is broken when [condition].
Error: [error message]
Expected: [expected behavior]
Fix it and add tests.
```

### 2. Add a Feature
```
Add [feature description] to @file.py
Requirements:
- [requirement 1]
- [requirement 2]
Include tests and documentation.
```

### 3. Review Code
```
Review @file.py for:
- Security issues
- Performance problems
- Best practices violations
- Missing error handling
```

### 4. Write Tests
```
Write comprehensive tests for @file.py covering:
- Happy paths
- Edge cases
- Error conditions
```

### 5. Create Git Commit
```
Commit these changes with a descriptive message
```

### 6. Create Pull Request
```
Create a PR for this feature
```

### 7. Debug Production Issue
```
ultrathink - [description of production issue]
Logs: [relevant logs]
Find root cause and fix ASAP
```

---

## 🔧 Background Command Pattern

```bash
# Press Ctrl+B, then type command
npm run dev              # Dev server
npm run watch            # File watcher
tail -f logs/app.log     # Log monitoring
python manage.py runserver  # Django dev server

# Then continue working while it runs
```

---

## 🎨 Custom Slash Commands

**Location**: `.claude/commands/your-command.md`

**Template**:
```markdown
---
description: Brief description of what this does
---

Your prompt template here.
Use @-mentions for files.
Use variables if needed.
```

**Usage**: `/your-command`

---

## 🤖 Custom Agents

**Location**: `.claude/agents/your-agent.md`

**Template**:
```markdown
---
name: your-agent
description: What this agent specializes in
tools:
  - Read
  - Write
  - Grep
---

You are a [specialist type]. When invoked, you:
1. [task 1]
2. [task 2]
3. [task 3]
```

**Usage**: `@your-agent do something`

---

## 📊 Model Selection Guide

| Model | Speed | Quality | Cost | Use For |
|-------|-------|---------|------|---------|
| **Haiku** | ⚡⚡⚡ | ⭐⭐ | $ | Simple edits, searches |
| **Sonnet** | ⚡⚡ | ⭐⭐⭐ | $$ | Most tasks (default) |
| **Opus** | ⚡ | ⭐⭐⭐⭐⭐ | $$$ | Critical decisions |
| **OpusPlan** | ⚡⚡ | ⭐⭐⭐⭐ | $$ | Planning + execution |
| **HaikuPlan** | ⚡⚡⚡ | ⭐⭐⭐ | $ | Fast planning + execution |

**Switch**: Type `/model` and select

---

## 🚦 When to Use Thinking Mode

### Use Thinking ✅
- Complex architectural decisions
- Debugging subtle/intermittent bugs
- Performance optimization strategies
- Security vulnerability analysis
- Refactoring large codebases
- Algorithm design

### Skip Thinking ❌
- Simple file edits
- Running tests
- Creating commits
- Formatting code
- Adding comments
- Renaming variables

---

## 💾 Memory Management

```bash
# Add to memory (start message with #)
#Remember: We use Redis for caching

# View all memory
/memory

# Edit memory
/memory edit
```

---

## 🔍 Finding Things Fast

```bash
# Find files
@explore find all API endpoints

# Search code content
@explore search for TODO comments

# Ask about codebase
@explore how does authentication work?
```

---

## ⚡ Productivity Hacks

### 1. Parallel Execution
```
In parallel:
1. Run tests
2. Build documentation
3. Lint code
```

### 2. Chained Workflows
```
1. Pull latest from main
2. Run migrations
3. Run tests
4. If tests pass: deploy to staging
```

### 3. Context Preservation
```
# First ask
@src/ explain the architecture

# Later (same session)
Now add caching to the user service
# Claude remembers without re-reading!
```

---

## 🐛 Quick Troubleshooting

### Claude can't find files?
```bash
pwd                      # Check current directory
/add-dir /path/to/project
/permissions allow Read(//path/to/project/**)
```

### Commands slow?
```bash
/model                   # Switch to Haiku
Tab                      # Toggle thinking OFF
@explore instead of manual searching
```

### Context full?
```bash
/context                 # Check usage
/clear                   # Start fresh
/resume                  # Switch conversation
```

### Permission denied?
```bash
/permissions             # View current permissions
/permissions allow Bash([command]:*)
```

---

## 📈 Daily Checklist

### Morning Setup
- [ ] `claude` - Start session
- [ ] `/permissions` - Verify permissions
- [ ] `/resume` - Continue yesterday's work
- [ ] Check background processes (if any)

### During Work
- [ ] Use `@explore` for codebase searches
- [ ] Press Tab to toggle thinking as needed
- [ ] Use Ctrl+B for dev servers
- [ ] Let Claude commit and PR your work

### End of Day
- [ ] `/cost` - Check session costs
- [ ] `/export` - Export important conversations
- [ ] Review what you learned
- [ ] Update custom commands/agents

---

## 🎓 Learning Path

### Week 1: Basics
- [ ] Master keyboard shortcuts
- [ ] Learn @-mention patterns
- [ ] Practice permission management
- [ ] Use thinking mode

### Week 2: Intermediate
- [ ] Create first custom slash command
- [ ] Use background commands
- [ ] Try parallel execution
- [ ] Set up memory management

### Week 3: Advanced
- [ ] Create custom agent
- [ ] Set up hooks
- [ ] Use MCP servers
- [ ] Optimize workflows

### Week 4: Expert
- [ ] Multi-repository workflows
- [ ] Advanced automation
- [ ] Team collaboration patterns
- [ ] Performance tuning

---

## 📞 Get Help

```bash
/help                    # General help
/help [topic]           # Specific topic help
/doctor                 # Diagnose issues

# Community
GitHub: github.com/anthropics/claude-code/issues
Docs: docs.claude.com/claude-code
```

---

## 💯 Success Metrics

Track weekly:
- ⏱️ Hours saved: ___
- 🐛 Bugs prevented: ___
- 🚀 Features shipped: ___
- 📚 New skills learned: ___
- 😊 Energy level improvement: ___

---

## 🎯 Remember

1. **Start small**: Master basics before advanced features
2. **Build habits**: Use same patterns daily
3. **Experiment**: Try new features in safe environments
4. **Document**: Save your best workflows
5. **Share**: Help teammates level up

---

**Print This Card** | **Keep It Visible** | **Reference Daily**

*Your productivity multiplier is just one command away!*
