# Claude Code: Complete Setup & Installation Guide
## Get Started in 10 Minutes - Production Configuration in 30

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Quick Start (10 Minutes)](#quick-start-10-minutes)
3. [Production Setup (30 Minutes)](#production-setup-30-minutes)
4. [Configuration Guide](#configuration-guide)
5. [Integration Setup](#integration-setup)
6. [Troubleshooting](#troubleshooting)
7. [Team Setup](#team-setup)

---

## Prerequisites

### System Requirements

| Component | Requirement | Why |
|-----------|-------------|-----|
| **OS** | Linux, macOS, or Windows (WSL) | Core functionality |
| **Node.js** | v16 or later | Runtime environment |
| **Git** | Any recent version | Version control integration |
| **Terminal** | Any modern terminal | Interface |
| **Internet** | Stable connection | API communication |

### Check Your System

```bash
# Check Node.js
node --version  # Should be v16+

# Check npm
npm --version

# Check Git
git --version

# Check Python (for monitoring scripts)
python3 --version  # Should be 3.8+
```

### Required Accounts

- **Anthropic Account**: [Sign up](https://claude.ai)
- **Subscription**: Claude Pro or Claude Max
  - Pro: Good for daily use
  - Max: Best for intensive work

---

## Quick Start (10 Minutes)

### Step 1: Installation (2 minutes)

```bash
# Install Claude Code globally
npm install -g @anthropic-ai/claude-code

# Verify installation
claude --version
```

**Expected Output**: `claude-code version X.X.X`

---

### Step 2: Authentication (3 minutes)

```bash
# Start Claude Code
claude

# First-time setup will prompt for authentication
# Choose your method:
# 1. Browser OAuth (Recommended)
# 2. API Key
# 3. Bedrock/Vertex (Enterprise)
```

**Browser OAuth (Easiest)**:
1. Follow the browser prompt
2. Log into claude.ai
3. Authorize the application
4. Return to terminal

**API Key**:
1. Get key from https://console.anthropic.com
2. Enter when prompted
3. Key is stored securely

---

### Step 3: First Conversation (5 minutes)

```bash
# Already in Claude Code session

You: "Hello! Can you explain what you can do?"

# Try basic operations
You: "Show me the files in this directory"

You: "Read the README.md file"

You: "Create a simple Python script that prints 'Hello World'"
```

**Success**: You've successfully installed and used Claude Code!

---

## Production Setup (30 Minutes)

### Phase 1: Project Setup (10 minutes)

#### Create Project Directory Structure

```bash
cd /path/to/your/project

# Create Claude Code configuration directory
mkdir -p .claude/{commands,agents}

# Create settings file
touch .claude/settings.json
```

#### Configure Project Settings

**`.claude/settings.json`**:
```json
{
  "version": "2.0",
  "projectName": "My Project",
  "description": "Project description",

  "permissions": {
    "allowedTools": [
      "Read(//absolute/path/to/project/**)",
      "Write(//absolute/path/to/project/src/**)",
      "Bash(git:*)",
      "Bash(npm:*)",
      "Bash(python:*)",
      "Bash(pytest:*)"
    ],
    "deniedTools": [
      "Bash(rm -rf:*)",
      "Bash(sudo:*)"
    ]
  },

  "hooks": {
    "PostToolUse": {
      "tools": ["Write", "Edit"],
      "command": "npx prettier --write $FILE_PATH",
      "description": "Auto-format on file changes"
    }
  },

  "ignorePatterns": [
    "**/node_modules/**",
    "**/.git/**",
    "**/dist/**",
    "**/build/**",
    "**/.venv/**",
    "**/__pycache__/**"
  ]
}
```

---

### Phase 2: Essential Commands (10 minutes)

#### Create Core Commands

**1. Code Review** (`.claude/commands/review.md`)
```markdown
---
description: Comprehensive code review
---

Review the code for:
1. **Security**: SQL injection, XSS, auth issues
2. **Performance**: N+1 queries, inefficient algorithms
3. **Best Practices**: Code style, patterns, maintainability
4. **Testing**: Coverage, edge cases
5. **Documentation**: Comments, docstrings, README

Provide specific, actionable feedback with line numbers.
```

**2. Test Generation** (`.claude/commands/test.md`)
```markdown
---
description: Generate comprehensive tests
---

Generate tests for the selected code covering:
1. **Happy Paths**: Normal operation
2. **Edge Cases**: Boundary conditions
3. **Error Cases**: Invalid inputs, exceptions
4. **Integration**: Component interactions

Use appropriate testing framework (pytest, jest, etc.).
Include test fixtures and mocks where needed.
```

**3. Bug Investigation** (`.claude/commands/bug.md`)
```markdown
---
description: Systematic bug investigation
---

Bug Investigation Workflow:

1. **Gather Information**:
   - Expected behavior?
   - Actual behavior?
   - Reproduction steps?
   - Error messages/logs?

2. **Investigation**:
   - Read relevant code
   - Check recent changes (git log)
   - Search for similar issues

3. **Root Cause Analysis** (use thinking mode):
   - What's causing this?
   - Why did it happen?
   - What else could be affected?

4. **Solution**:
   - Propose fix
   - Add tests to prevent regression
   - Update documentation if needed

5. **Verification**:
   - Test the fix
   - Check for side effects
```

**4. Documentation** (`.claude/commands/docs.md`)
```markdown
---
description: Generate comprehensive documentation
---

Generate documentation including:
1. **Docstrings**: All functions and classes
2. **README**: Project overview, setup, usage
3. **API Docs**: Endpoints, parameters, responses
4. **Examples**: Common use cases
5. **Contributing**: How to contribute

Use clear, professional language.
Include code examples.
```

**5. Deploy Checklist** (`.claude/commands/deploy.md`)
```markdown
---
description: Pre-deployment checklist
---

Pre-Deployment Checklist:

1. **Code Quality**:
   - [ ] All tests passing?
   - [ ] Linting clean?
   - [ ] No console.logs/debugger?
   - [ ] Code reviewed?

2. **Functionality**:
   - [ ] Feature works as expected?
   - [ ] No regressions?
   - [ ] Edge cases handled?

3. **Performance**:
   - [ ] No performance degradation?
   - [ ] Database queries optimized?
   - [ ] Caching configured?

4. **Security**:
   - [ ] Security scan passed?
   - [ ] No secrets in code?
   - [ ] Authentication working?

5. **Documentation**:
   - [ ] README updated?
   - [ ] API docs updated?
   - [ ] Changelog updated?

6. **Deployment**:
   - [ ] Database migrations ready?
   - [ ] Environment variables set?
   - [ ] Rollback plan ready?
   - [ ] Monitoring configured?

Proceed with deployment? (yes/no)
```

---

### Phase 3: Permission Configuration (10 minutes)

#### Set Up Smart Permissions

```bash
# Launch Claude Code
claude

# Configure permissions interactively
/permissions
```

#### Recommended Permission Sets

**For Development**:
```bash
/permissions allow Bash(git:*)          # All git operations
/permissions allow Bash(npm:*)          # npm commands
/permissions allow Bash(yarn:*)         # yarn commands
/permissions allow Bash(python:*)       # Python execution
/permissions allow Bash(pytest:*)       # Test running
/permissions allow Bash(docker:*)       # Docker commands
/permissions allow Bash(curl:*)         # API testing
```

**For File Access**:
```bash
# Allow reading entire project
/permissions allow Read(//absolute/path/to/project/**)

# Allow writing to specific directories
/permissions allow Write(//absolute/path/to/project/src/**)
/permissions allow Write(//absolute/path/to/project/tests/**)
/permissions allow Write(//absolute/path/to/project/docs/**)
```

**Safety Blocks**:
```bash
# Prevent destructive operations
/permissions deny Bash(rm -rf:*)
/permissions deny Bash(sudo:*)
/permissions deny Bash(chmod 777:*)

# Prevent writing to protected files
/permissions deny Write(//absolute/path/to/project/.git/**)
/permissions deny Write(//absolute/path/to/project/node_modules/**)
```

#### Save Permissions to Project

Add to `.claude/settings.json`:
```json
{
  "permissions": {
    "allowedTools": [
      "Read(//absolute/path/to/project/**)",
      "Write(//absolute/path/to/project/src/**)",
      "Bash(git:*)",
      "Bash(npm:*)"
    ]
  }
}
```

---

## Configuration Guide

### User-Level Configuration

Location: `~/.claude/settings.json`

```json
{
  "theme": "dark",
  "model": "sonnet",
  "thinkingMode": "auto",
  "autoAccept": false,
  "verbose": true,

  "defaultPermissions": {
    "allowedTools": [
      "Bash(git:*)",
      "Bash(npm:*)"
    ]
  }
}
```

### Project-Level Configuration

Location: `.claude/settings.json` (in your project)

```json
{
  "projectName": "My App",
  "description": "Description of the project",

  "permissions": {
    "allowedTools": [
      "Read(//project/path/**)",
      "Write(//project/path/src/**)"
    ],
    "deniedTools": [
      "Bash(rm -rf:*)"
    ]
  },

  "hooks": {
    "PostToolUse": {
      "tools": ["Edit"],
      "command": "npm run format -- $FILE_PATH"
    }
  },

  "ignorePatterns": [
    "**/node_modules/**",
    "**/.git/**"
  ]
}
```

### Keyboard Shortcuts Configuration

Default shortcuts work out of the box. To customize, check `/config` command.

---

## Integration Setup

### VS Code Extension

```bash
# Install VS Code extension
# Search for "Claude Code" in extensions

# Or via command line
code --install-extension anthropic.claude-code
```

**Features**:
- Integrated chat panel
- File mentions with autocomplete
- Inline suggestions
- Quick actions

### Git Integration

Claude Code works seamlessly with git:

```bash
# Git hooks (optional)
# Add to .git/hooks/pre-commit

#!/bin/bash
# Run tests before commit
npm test || exit 1

# Run Claude Code quality check
claude -p "/review @staged-files" || exit 1
```

### CI/CD Integration

**GitHub Actions** (`.github/workflows/claude-review.yml`):
```yaml
name: Claude Code Review

on: [pull_request]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install Claude Code
        run: npm install -g @anthropic-ai/claude-code

      - name: Run Review
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          claude -p "Review all changed files for security and quality issues" \
            --dangerously-skip-permissions
```

### Terminal Integration

**Add to `.bashrc` or `.zshrc`**:
```bash
# Quick Claude Code alias
alias cc='claude'

# Auto-start monitoring
python3 /path/to/monitor_releases.py

# Quick commands
alias ccr='claude -p "/review"'
alias cct='claude -p "/test"'
```

---

## Troubleshooting

### Common Issues

#### Issue 1: Authentication Failed

**Symptoms**: Can't log in, token errors

**Solutions**:
```bash
# Clear existing credentials
rm ~/.claude/credentials

# Re-authenticate
claude

# For macOS keychain issues
security unlock-keychain
```

#### Issue 2: Permission Denied

**Symptoms**: "Tool permission denied" messages

**Solutions**:
```bash
# Check current permissions
/permissions

# Allow specific tool
/permissions allow Bash(command:*)

# For testing only (NOT for production)
claude --dangerously-skip-permissions
```

#### Issue 3: Files Not Found

**Symptoms**: Claude can't find files you mention

**Solutions**:
```bash
# Check current directory
pwd

# Add project directory
/add-dir /path/to/project

# Allow file reading
/permissions allow Read(//path/to/project/**)
```

#### Issue 4: Slow Performance

**Solutions**:
```bash
# Switch to faster model
/model
# Select: Haiku

# Turn off thinking mode
Press Tab (toggle off)

# Clear context
/clear

# Use Explore agent for searches
@explore find X
```

#### Issue 5: Context Overflow

**Symptoms**: "Context limit exceeded" errors

**Solutions**:
```bash
# Check context usage
/context

# Start fresh conversation
/clear

# Use more targeted queries
@specific-file.py instead of @entire-directory/
```

### Getting Help

```bash
# Built-in help
/help
/help [topic]

# Diagnose issues
/doctor

# Check status
/status

# View release notes
/release-notes
```

### Community Support

- **GitHub Issues**: https://github.com/anthropics/claude-code/issues
- **Documentation**: https://docs.claude.com/claude-code
- **Blog**: https://anthropic.com/news

---

## Team Setup

### Shared Configuration

**Create `.claude/settings.json` in project root**:

```json
{
  "projectName": "Team Project",
  "version": "2.0",

  "permissions": {
    "allowedTools": [
      "Read(//project/path/**)",
      "Write(//project/path/src/**)",
      "Bash(git:*)",
      "Bash(npm:*)"
    ]
  },

  "ignorePatterns": [
    "**/node_modules/**",
    "**/.git/**"
  ]
}
```

**Commit to repository**:
```bash
git add .claude/
git commit -m "Add Claude Code team configuration"
```

### Team Commands

Create shared commands in `.claude/commands/`:

- `/review` - Standard review checklist
- `/test` - Team test standards
- `/pr` - PR template
- `/deploy` - Deployment checklist

### Team Agents

Create shared agents in `.claude/agents/`:

- `@api-reviewer` - API review standards
- `@security-checker` - Security requirements
- `@test-generator` - Test standards

### Documentation for Team

Create `docs/claude-code-guide.md`:

```markdown
# Team Claude Code Guide

## Getting Started
1. Install: `npm install -g @anthropic-ai/claude-code`
2. Authenticate: Follow prompts
3. Trust project: When prompted, trust the repo

## Team Commands
- `/review` - Code review before PR
- `/test` - Generate tests
- `/pr` - Create PR with template
- `/deploy` - Deployment checklist

## Team Agents
- `@api-reviewer` - Review API changes
- `@security-checker` - Security review

## Best Practices
1. Always run `/review` before PR
2. Use `/test` for new features
3. Check `/deploy` before deployment
4. Keep permissions strict

## Questions?
Ask in #dev-tools Slack channel
```

---

## Advanced Setup

### Custom Models (Enterprise)

For Bedrock/Vertex integration:

```bash
# Set environment variables
export ANTHROPIC_BASE_URL="your-endpoint"
export ANTHROPIC_API_KEY="your-key"

# Or use config
claude --configure
```

### Hooks Setup

Advanced automation with hooks (`.claude/settings.json`):

```json
{
  "hooks": {
    "PreToolUse": {
      "tools": ["Bash(git commit:*)"],
      "command": "npm test",
      "timeout": 60000,
      "description": "Run tests before commit"
    },

    "PostToolUse": {
      "tools": ["Write", "Edit"],
      "command": "npx prettier --write $FILE_PATH && git add $FILE_PATH",
      "description": "Format and stage changes"
    },

    "SessionStart": {
      "command": "git fetch origin",
      "description": "Fetch latest changes"
    },

    "SessionEnd": {
      "command": "git status",
      "description": "Show status on exit"
    }
  }
}
```

### MCP Server Setup

Connect external data sources:

```bash
# List available MCP servers
/mcp

# Configure MCP server
# Edit ~/.claude/mcp.json

# Example: Database MCP
{
  "mcpServers": {
    "database": {
      "command": "node",
      "args": ["path/to/mcp-server.js"],
      "env": {
        "DB_URL": "postgresql://..."
      }
    }
  }
}
```

---

## Verification Checklist

### After Setup, Verify:

- [ ] Claude Code starts successfully
- [ ] Authentication works
- [ ] Can read project files
- [ ] Permissions configured correctly
- [ ] Custom commands work (`/review`, etc.)
- [ ] Git integration works
- [ ] Keyboard shortcuts work
- [ ] Background processes work (Ctrl+B)
- [ ] Can create commits and PRs
- [ ] Documentation accessible

### Test Basic Workflow:

```bash
# 1. Start Claude
claude

# 2. Read a file
You: "@README.md summarize"

# 3. Run a command
You: "Show git status"

# 4. Use custom command
You: "/review @src/main.py"

# 5. Create something
You: "Create a test file for main.py"

# 6. Commit
You: "Review changes and create a commit"
```

**All working?** ✅ You're ready to go!

---

## Next Steps

1. **Complete Quick Start Tutorial**: `CLAUDE_CODE_COMPLETE_GUIDE.md`
2. **Try Practice Scenarios**: `PRACTICE_SCENARIOS.md`
3. **Set Up Monitoring**: Run `monitor_releases.py --configure`
4. **Follow Learning Path**: `LEARNING_PATH.md`
5. **Create First Custom Command**: For your most common task
6. **Join Community**: Share your experience

---

## Update & Maintenance

### Keep Claude Code Updated

```bash
# Check current version
claude --version

# Update to latest
npm update -g @anthropic-ai/claude-code

# View what's new
claude
/release-notes
```

### Backup Your Configuration

```bash
# Backup user config
cp -r ~/.claude ~/claude-backup

# Backup project config
git add .claude/
git commit -m "Update Claude Code configuration"
```

---

## Quick Reference

### Essential Commands After Setup

```bash
# Start Claude
claude

# Get help
/help

# Configure
/config

# Check permissions
/permissions

# View context
/context

# Switch model
/model

# Check status
/status
```

---

**Setup Complete!** 🎉

You're now ready to achieve 5-10x productivity improvements with Claude Code.

---

**Document Version**: 1.0
**Last Updated**: 2025-10-31
**Setup Time**: 10 minutes (quick) / 30 minutes (production)
