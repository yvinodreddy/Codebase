# Claude Code: Complete Mastery Guide
## From Zero to Hero - Production-Ready Workflows

> **Last Updated**: 2025-10-31
> **For Version**: 2.0.30 and later
> **Your Path**: Beginner → Intermediate → Advanced → Expert

---

## Table of Contents

1. [Introduction & Philosophy](#introduction--philosophy)
2. [Quick Start (First 5 Minutes)](#quick-start-first-5-minutes)
3. [Core Concepts](#core-concepts)
4. [Essential Commands (Daily Use)](#essential-commands-daily-use)
5. [Intermediate Workflows](#intermediate-workflows)
6. [Advanced Techniques](#advanced-techniques)
7. [Expert-Level Mastery](#expert-level-mastery)
8. [Productivity Multipliers](#productivity-multipliers)
9. [Real-World Scenarios](#real-world-scenarios)
10. [Troubleshooting & Optimization](#troubleshooting--optimization)
11. [Staying Updated](#staying-updated)

---

## Introduction & Philosophy

### What is Claude Code?

Claude Code is an AI-powered coding assistant that works directly in your terminal and VS Code. Think of it as:
- **A pair programmer** who never gets tired
- **A code reviewer** who reads at superhuman speed
- **A documentation expert** who knows thousands of libraries
- **A debugging partner** who sees patterns you miss

### Core Philosophy

**Time = Life Energy**
Every minute saved is energy you can invest in:
- Learning new skills
- Solving harder problems
- Building better products
- Living a balanced life

**Claude Code helps you:**
1. ✅ Automate repetitive tasks (save hours daily)
2. ✅ Catch bugs before they reach production (save days of debugging)
3. ✅ Learn best practices in real-time (accelerate skill growth)
4. ✅ Focus on creative problem-solving (enhance job satisfaction)

---

## Quick Start (First 5 Minutes)

### Basic Interaction Pattern

```bash
# Start Claude Code
claude

# Your first conversation
You: "Show me the files in this directory"
Claude: [uses tools to list files]

You: "Read the main.py file"
Claude: [reads and shows content]

You: "Add error handling to the database connection"
Claude: [analyzes code, suggests improvements, makes changes]
```

### The Three Modes

| Mode | Trigger | Use When |
|------|---------|----------|
| **Normal** | Default | Regular coding tasks |
| **Plan Mode** | Say "think" or "plan this" | Complex multi-step tasks |
| **Bash Mode** | Press `Ctrl+B` | Run background commands |

### Essential Keyboard Shortcuts

| Shortcut | Action | Why You Need It |
|----------|--------|-----------------|
| `Tab` | Toggle thinking | Get deeper reasoning |
| `Ctrl+O` | View transcript | See conversation history |
| `Ctrl+R` | Search history | Find past commands fast |
| `Ctrl+B` | Background command | Keep dev servers running |
| `Ctrl+G` | Edit in external editor | Complex prompt editing |
| `Esc` | Interrupt | Stop current operation |

---

## Core Concepts

### 1. Tools - Claude's Superpowers

Claude has access to specialized tools. Understanding them = using Claude effectively.

#### File Operations
- **Read**: Views file contents (up to 2000 lines)
- **Write**: Creates new files (prefers Edit for existing files)
- **Edit**: Modifies existing files with surgical precision
- **Glob**: Finds files by pattern (`**/*.js`, `src/**/*.py`)
- **Grep**: Searches code content (regex supported)

```bash
# Example conversation
You: "Find all Python files in src/"
Claude: [uses Glob tool with pattern: src/**/*.py]

You: "Search for TODO comments in those files"
Claude: [uses Grep tool with pattern: TODO]
```

#### Code Operations
- **Bash**: Runs terminal commands
- **Task**: Spawns specialized sub-agents for complex work
- **NotebookEdit**: Edits Jupyter notebooks

#### Intelligence Operations
- **WebSearch**: Searches the internet
- **WebFetch**: Reads web pages
- **AskUserQuestion**: Asks clarifying questions

### 2. Permissions - Security & Control

**Philosophy**: You control what Claude can do.

```bash
# View current permissions
/permissions

# Allow specific tools
/permissions allow Bash(npm:*)  # Allow all npm commands
/permissions allow Read(//home/user01/projects/**)  # Allow reading project files

# Deny dangerous operations
/permissions deny Bash(rm -rf:*)  # Block destructive commands
```

**Smart Permission Patterns**:
```bash
# Development workflows
Bash(git:*)           # All git commands
Bash(npm:*)           # All npm commands
Bash(python:*)        # All Python executions
Bash(docker:*)        # All Docker commands

# File access
Read(//home/user01/projects/**)    # Recursive project access
Write(//home/user01/projects/src/**) # Write to src only
```

### 3. @-Mentions - Context Injection

Add files, folders, or resources directly to the conversation.

```bash
# Mention files
You: "@src/app.py how does authentication work?"

# Mention folders
You: "@tests/ are these tests comprehensive?"

# Mention multiple files
You: "@config.yaml @.env what's misconfigured?"

# Mention MCP resources
You: "@database-schema explain the user table"
```

**Pro Tip**: @-mentions support tab completion! Start typing and press Tab.

### 4. Slash Commands - Productivity Boosters

Built-in commands for common tasks.

| Command | Purpose | Example |
|---------|---------|---------|
| `/help` | Get help | `/help permissions` |
| `/permissions` | Manage tool access | `/permissions allow Bash(git:*)` |
| `/model` | Switch AI models | `/model` (opens selector) |
| `/context` | Check context usage | `/context` |
| `/memory` | Manage conversation memory | `/memory edit` |
| `/resume` | Switch conversations | `/resume` |
| `/rewind` | Undo code changes | `/rewind` |
| `/usage` | Check plan limits | `/usage` |
| `/cost` | View session costs | `/cost` |
| `/export` | Export conversation | `/export` |

### 5. Custom Slash Commands - Your Workflows

Create reusable prompt templates.

**Location**: `.claude/commands/`

**Example**: `.claude/commands/review.md`
```markdown
---
description: Code review checklist
---

Review the selected code for:
1. Security vulnerabilities
2. Performance issues
3. Code style violations
4. Missing error handling
5. Test coverage gaps

Provide specific line-by-line feedback.
```

**Usage**:
```bash
You: "/review @src/auth.py"
Claude: [runs comprehensive review]
```

### 6. Subagents - Specialized Workers

Claude can spawn specialized AI agents for specific tasks.

**Built-in Agents**:
- **Explore**: Fast codebase exploration (powered by Haiku)
- **Plan**: Strategic planning for complex tasks

**Custom Agents**: Create in `.claude/agents/`

```bash
# Invoke by @-mentioning
You: "@explore find all API endpoints"
Claude: [Explore agent searches efficiently]
```

### 7. Thinking Mode - Deep Reasoning

```bash
# Activate thinking
You: "think about how to refactor this architecture"

# Levels of thinking
You: "think harder"      # More reasoning
You: "ultrathink"        # Maximum reasoning

# Toggle thinking (sticky)
Press Tab while typing
```

**When to use thinking**:
- ✅ Complex architectural decisions
- ✅ Debugging subtle issues
- ✅ Performance optimization strategies
- ✅ Security analysis

### 8. Plan Mode - Strategic Execution

For multi-step tasks, Claude creates a plan first.

```bash
You: "Implement user authentication with JWT, password reset, and email verification"

Claude: [enters plan mode]
1. Create User model with password hashing
2. Implement JWT token generation
3. Add login/logout endpoints
4. Create password reset flow
5. Add email verification
6. Write comprehensive tests

Ready to proceed? [Y/n]
```

---

## Essential Commands (Daily Use)

### Category 1: Code Understanding

#### "Explain this codebase"
```bash
You: "Explain the architecture of this project"
Claude: [uses Explore agent to map out structure]
```

#### "Find where X is implemented"
```bash
You: "Find where user authentication is implemented"
Claude: [searches with Grep and Glob]
```

#### "Show me how X works"
```bash
You: "@src/payment.py explain the refund logic"
```

### Category 2: Code Modification

#### "Fix this bug"
```bash
You: "The login endpoint returns 500 when password is wrong. Fix it."
Claude:
1. [reads endpoint code]
2. [identifies missing error handling]
3. [suggests fix]
4. [implements fix with Edit tool]
```

#### "Add feature X"
```bash
You: "Add pagination to the users API endpoint"
Claude: [plans implementation, modifies code, adds tests]
```

#### "Refactor this code"
```bash
You: "@src/legacy.py refactor this to use modern Python patterns"
```

### Category 3: Testing & Validation

#### "Write tests"
```bash
You: "Write comprehensive tests for @src/payment.py"
Claude: [analyzes code, creates test file with multiple test cases]
```

#### "Run tests and fix failures"
```bash
You: "Run pytest and fix any failures"
Claude:
1. [runs tests with Bash]
2. [identifies failures]
3. [analyzes root causes]
4. [fixes code]
5. [reruns tests]
6. [repeats until all pass]
```

### Category 4: Git Operations

#### "Create a commit"
```bash
You: "Commit these changes"
Claude:
1. [runs git status]
2. [runs git diff]
3. [analyzes changes]
4. [creates descriptive commit message]
5. [commits with proper attribution]
```

#### "Create a pull request"
```bash
You: "Create a PR for this feature"
Claude:
1. [analyzes all commits in branch]
2. [creates comprehensive PR description]
3. [uses gh cli to create PR]
4. [returns PR URL]
```

### Category 5: Documentation

#### "Document this code"
```bash
You: "@src/api.py add comprehensive docstrings"
```

#### "Create README"
```bash
You: "Create a README for this project"
Claude: [analyzes codebase, creates professional README]
```

---

## Intermediate Workflows

### Workflow 1: Feature Development (End-to-End)

```bash
# Step 1: Planning
You: "think about implementing a rate limiting middleware"

# Step 2: Implementation
You: "Create the rate limiting middleware with Redis backend"

# Step 3: Testing
You: "Write unit and integration tests"

# Step 4: Documentation
You: "Add docstrings and update README"

# Step 5: Commit
You: "Commit these changes"

# Step 6: PR
You: "Create a pull request"
```

**Time Saved**: 2-3 hours → 20-30 minutes

### Workflow 2: Bug Investigation & Fix

```bash
# Step 1: Reproduce
You: "Run the app and reproduce the bug where cart total is wrong"
Claude: [runs app in background with Ctrl+B, tests scenarios]

# Step 2: Investigate
You: "@explore find all code related to cart calculations"

# Step 3: Identify Root Cause
You: "think about what could cause cart total miscalculations"

# Step 4: Fix
You: "Fix the bug and add tests to prevent regression"

# Step 5: Verify
You: "Run all tests and verify the fix"
```

**Time Saved**: 1-2 hours → 15-20 minutes

### Workflow 3: Code Review Response

```bash
# Step 1: Fetch PR comments
You: "Show me the comments on PR #123"
Claude: [uses gh cli to fetch comments]

# Step 2: Address each comment
You: "Address all the review comments"

# Step 3: Update PR
You: "Push the changes and respond to reviewers"
```

**Time Saved**: 30-60 minutes → 5-10 minutes

### Workflow 4: Dependency Update

```bash
# Step 1: Update
You: "Update all npm packages to latest compatible versions"

# Step 2: Test
You: "Run all tests and check for breaking changes"

# Step 3: Fix breaks
You: "Fix any issues caused by updates"

# Step 4: Commit
You: "Commit the dependency updates"
```

**Time Saved**: 1-2 hours → 15-30 minutes

---

## Advanced Techniques

### Technique 1: Parallel Task Execution

Claude can work on multiple independent tasks simultaneously.

```bash
You: "In parallel:
1. Write tests for @src/auth.py
2. Document @src/api.py
3. Fix linting errors in @src/utils.py"

Claude: [spawns multiple sub-tasks, executes concurrently]
```

**Benefit**: 3x faster than sequential execution

### Technique 2: Background Process Management

Keep long-running processes alive while Claude works on other tasks.

```bash
# Start dev server in background
You: [Press Ctrl+B]
You: "npm run dev"

# Now Claude can work while server runs
You: "Write integration tests that hit localhost:3000"

# Check background process
You: "Show me the dev server output"
```

### Technique 3: Custom Agents for Repetitive Tasks

Create specialized agents for your workflows.

**Example**: `.claude/agents/api-reviewer.md`
```markdown
---
name: api-reviewer
description: Reviews API endpoints for best practices
tools:
  - Read
  - Grep
  - Write
---

You are an API review specialist. When invoked, review API endpoints for:
1. RESTful design principles
2. Proper HTTP status codes
3. Input validation
4. Error handling
5. Authentication/authorization
6. Rate limiting
7. Documentation

Provide specific, actionable feedback.
```

**Usage**:
```bash
You: "@api-reviewer review all endpoints in @src/api/"
```

### Technique 4: Hooks for Automation

Hooks execute scripts on specific events.

**Location**: `.claude/settings.json`

```json
{
  "hooks": {
    "PostToolUse": {
      "tools": ["Write", "Edit"],
      "command": "npm run lint -- --fix $FILE_PATH",
      "description": "Auto-format on file changes"
    },
    "PreToolUse": {
      "tools": ["Bash(npm:*)"],
      "command": "echo 'Running npm command...'",
      "description": "Log npm commands"
    },
    "SessionEnd": {
      "command": "git status",
      "description": "Show git status on exit"
    }
  }
}
```

### Technique 5: MCP Servers for External Data

Connect Claude to databases, APIs, and services.

```bash
# List available MCP servers
/mcp

# Enable/disable by @-mentioning
You: "@database-server"

# Use MCP resources
You: "@database-schema explain the schema"
You: "@jira-tickets show open bugs"
```

### Technique 6: Memory Management for Long Projects

Save context across sessions.

```bash
# Add to memory
You: "#Remember: Use Redis for caching, not memcached"

# View memory
/memory

# Edit memory
/memory edit
```

### Technique 7: Sandbox Mode for Safe Execution

Run untrusted code safely (Linux/Mac only).

```bash
# Enable in settings.json
{
  "sandbox": {
    "enabled": true,
    "allowUnsandboxedCommands": ["git", "npm", "python"]
  }
}
```

---

## Expert-Level Mastery

### Strategy 1: Workflow Orchestration

Chain multiple workflows with error handling.

```bash
You: "Execute this workflow with full error handling:
1. Pull latest from main
2. Run database migrations
3. Run all tests
4. If tests pass: deploy to staging
5. If tests fail: create detailed bug report
6. Notify team on Slack"
```

### Strategy 2: Context-Aware Caching

Leverage Claude's context awareness for faster iterations.

```bash
# First conversation
You: "@src/ explain the architecture"

# Later in same session (context preserved)
You: "Now add caching to the user service we discussed"
# Claude remembers the architecture without re-reading
```

### Strategy 3: Multi-Repository Workflows

```bash
# Add multiple directories
/add-dir /home/user01/backend
/add-dir /home/user01/frontend

# Work across repos
You: "Update the API contract in both backend and frontend"
```

### Strategy 4: Automated Code Quality Gates

Create slash command: `.claude/commands/pre-commit.md`
```markdown
---
description: Pre-commit quality checks
---

Run these checks:
1. Linting (fail if errors)
2. Type checking (fail if errors)
3. Unit tests (fail if failures)
4. Security scan (warn on issues)
5. Coverage check (warn if < 80%)

Report results in a structured format.
```

### Strategy 5: Learning Mode

Use Claude to build your skills.

```bash
You: "Explain the design patterns used in @src/ and teach me when to use each"

You: "As I write this feature, explain each decision and suggest best practices"
```

---

## Productivity Multipliers

### Time-Saving Calculations

| Task | Without Claude | With Claude | Time Saved |
|------|---------------|-------------|------------|
| Feature development | 4 hours | 1 hour | 3 hours |
| Bug investigation | 2 hours | 20 mins | 1h 40m |
| Code review response | 1 hour | 10 mins | 50 mins |
| Documentation | 1 hour | 15 mins | 45 mins |
| Test writing | 2 hours | 30 mins | 1h 30m |
| Refactoring | 3 hours | 45 mins | 2h 15m |

**Daily Savings**: 4-6 hours → Focus on high-value work

### Energy Management

**Before Claude**:
- 2 hours: Simple feature implementation (exhausting)
- 3 hours: Bug hunting (frustrating)
- 1 hour: Documentation (boring)
- Mental state: Drained

**With Claude**:
- 30 mins: Feature (energizing - focus on design)
- 20 mins: Bug fixing (satisfying - quick resolution)
- 10 mins: Documentation (effortless)
- Mental state: Energized for creative work

### Career Acceleration

**Skills You Learn Faster**:
1. Best practices (real-time feedback)
2. New languages (assisted learning)
3. Architecture patterns (guided decisions)
4. Debugging techniques (see patterns)
5. Code review skills (high-quality examples)

**Result**: 2-3x faster skill acquisition

---

## Real-World Scenarios

### Scenario 1: Production Incident

**Situation**: Payment API is down, users can't checkout.

```bash
You: "ultrathink - payment API is returning 500 errors. Find and fix ASAP"

Claude:
1. [checks logs with Bash]
2. [identifies database connection timeout]
3. [reads database config]
4. [finds connection pool exhaustion]
5. [increases pool size]
6. [restarts service]
7. [verifies fix]
8. [creates post-mortem]

Time to resolution: 5 minutes vs. 30+ minutes
```

### Scenario 2: Technical Debt Sprint

**Situation**: Need to refactor legacy codebase.

```bash
You: "Plan a technical debt reduction sprint for @src/legacy/"

Claude: [creates comprehensive plan]
1. Identify code smells
2. Prioritize by impact
3. Create refactoring tasks
4. Estimate effort
5. Suggest migration strategy

You: "Execute the plan"
Claude: [works through systematically with tests]
```

### Scenario 3: New Team Member Onboarding

**Situation**: Help new developer understand codebase.

```bash
You: "Create onboarding documentation for new developers"

Claude:
1. [analyzes codebase structure]
2. [identifies key components]
3. [creates architecture diagram]
4. [writes setup guide]
5. [documents common workflows]
6. [adds troubleshooting section]
```

### Scenario 4: Security Audit

```bash
You: "Perform security audit on @src/ focusing on:
- SQL injection
- XSS vulnerabilities
- Authentication flaws
- Secrets in code"

Claude: [comprehensive security analysis with specific line numbers]
```

### Scenario 5: Performance Optimization

```bash
You: "Profile the application and optimize the slowest endpoints"

Claude:
1. [adds profiling]
2. [runs performance tests]
3. [identifies bottlenecks]
4. [optimizes queries]
5. [adds caching]
6. [measures improvement]
```

---

## Troubleshooting & Optimization

### Common Issues & Solutions

#### Issue 1: "Claude can't find my files"

**Symptoms**: "File not found" errors

**Solutions**:
```bash
# Check current directory
pwd

# Add project directory
/add-dir /path/to/project

# Verify permissions
/permissions

# Allow file access
/permissions allow Read(//path/to/project/**)
```

#### Issue 2: "Commands are slow"

**Solutions**:
1. Use Explore agent for searching: `@explore find X`
2. Be specific with file paths: `@src/specific.py` not `@src/`
3. Enable thinking only when needed: Press Tab to toggle off
4. Use Haiku model for simple tasks: `/model` → select Haiku

#### Issue 3: "Claude doesn't remember context"

**Solutions**:
```bash
# Save important info to memory
You: "#Remember: Database uses PostgreSQL 14"

# Check context usage
/context

# Export conversation for later reference
/export
```

#### Issue 4: "Permission errors"

**Solutions**:
```bash
# View denied tools
/permissions

# Allow specific tools
/permissions allow Bash(npm:*)

# Use --dangerously-skip-permissions for trusted environments
claude --dangerously-skip-permissions
```

#### Issue 5: "Git commits lack context"

**Solution**: Let Claude analyze full history
```bash
You: "Review the last 5 commits and create a detailed PR description"
```

### Performance Optimization

#### 1. Context Management

```bash
# Start fresh for unrelated tasks
/clear

# Resume specific conversations
/resume

# Rewind to undo changes
/rewind
```

#### 2. Model Selection

| Task Type | Recommended Model | Why |
|-----------|------------------|-----|
| Simple edits | Haiku | Fast, cost-effective |
| Complex features | Sonnet | Balanced quality/speed |
| Critical decisions | Opus | Highest quality |
| Planning only | OpusPlan | Opus for planning, Sonnet for execution |

#### 3. Parallel Execution

Always run independent tasks in parallel:
```bash
# Good ✅
You: "In parallel: run tests, build docs, and lint code"

# Bad ❌
You: "Run tests"
[wait]
You: "Build docs"
[wait]
You: "Lint code"
```

---

## Staying Updated

### Automatic Update Monitoring

See `monitor_releases.py` script (created separately) for automated notifications.

### Manual Checks

```bash
# View latest release notes
/release-notes

# Check for updates
claude --version
```

### Learning New Features

When new features release:

1. **Read release notes**: `/release-notes`
2. **Experiment**: Try the feature on a small task
3. **Integrate**: Add to your workflows
4. **Document**: Update your custom commands/agents

### Community Resources

- **Official Docs**: https://docs.claude.com/claude-code
- **GitHub Issues**: https://github.com/anthropics/claude-code/issues
- **Blog**: https://www.anthropic.com/news

---

## Quick Reference Card

### Keyboard Shortcuts
- `Tab` - Toggle thinking
- `Ctrl+O` - View transcript
- `Ctrl+R` - Search history
- `Ctrl+B` - Background command
- `Ctrl+G` - Edit in external editor
- `Esc` - Interrupt

### Essential Commands
- `/help` - Get help
- `/permissions` - Manage permissions
- `/model` - Switch models
- `/context` - Check context usage
- `/resume` - Switch conversations
- `/rewind` - Undo changes

### Common Patterns
- `@file.py` - Mention file
- `#Remember: ...` - Add to memory
- `think` - Enable thinking mode
- `Ctrl+B → command` - Background process

### Power User Tips
1. Create custom slash commands in `.claude/commands/`
2. Create custom agents in `.claude/agents/`
3. Set up hooks in `.claude/settings.json`
4. Use @explore for fast codebase searches
5. Press Tab to toggle thinking mode
6. Use parallel execution for independent tasks

---

## Success Metrics

Track your productivity improvements:

### Weekly Metrics
- [ ] Hours saved
- [ ] Bugs prevented
- [ ] Code reviews completed
- [ ] Features shipped
- [ ] Learning milestones

### Monthly Review
- [ ] New skills acquired
- [ ] Workflow optimizations implemented
- [ ] Team productivity impact
- [ ] Work-life balance improvement

---

## Conclusion

**You now have the knowledge to**:
- ✅ Use Claude Code efficiently from day one
- ✅ Build productivity-multiplying workflows
- ✅ Stay updated with new features automatically
- ✅ Solve problems faster and with less stress
- ✅ Focus on creative, high-value work
- ✅ Accelerate your career growth

**Remember**: Every minute saved compounds. Start small, build habits, watch your productivity soar.

**Next Steps**:
1. Try the Quick Start scenarios
2. Set up automated release monitoring
3. Create your first custom slash command
4. Track time saved in first week
5. Share learnings with your team

---

**Document Version**: 1.0
**Maintained By**: Auto-generated with updates from release monitoring
**Last Verified**: 2025-10-31
