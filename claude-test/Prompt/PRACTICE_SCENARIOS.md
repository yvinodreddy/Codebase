# Claude Code: Interactive Practice Scenarios
## Hands-On Challenges to Master Every Feature

---

## 🎮 How to Use This Guide

1. **Choose your level**: Beginner → Advanced
2. **Read the scenario**: Understand the challenge
3. **Attempt solution**: Try on your own first
4. **Check solution**: Compare with provided approach
5. **Reflect**: What did you learn?
6. **Repeat**: Practice until confident

**Pro Tip**: Do these in a test project, not production!

---

## 🥉 BEGINNER SCENARIOS

### Scenario 1: The First Conversation
**Skill**: Basic interaction with Claude Code
**Duration**: 15 minutes

#### The Challenge
You've just joined a new project and need to understand what it does.

**Files**:
- `README.md` - Project overview
- `src/main.py` - Main application
- `requirements.txt` - Dependencies

**Task**:
1. Ask Claude about the project structure
2. Have Claude explain the main.py file
3. Understand what dependencies are used
4. Get a summary of what the application does

#### Try It Yourself
(Take 10 minutes to attempt)

#### Solution Approach
```bash
# Start Claude
claude

# Conversation flow:
You: "What files are in this directory?"

You: "@README.md summarize this project"

You: "@src/main.py explain what this code does"

You: "@requirements.txt what are the main dependencies and what do they do?"

You: "Based on everything you've read, give me a comprehensive overview of this application"
```

#### What You Learned
- ✅ Basic conversation patterns
- ✅ @-mention syntax
- ✅ How to request summaries
- ✅ Building context progressively

---

### Scenario 2: The Bug Hunter
**Skill**: Using Claude to find and fix bugs
**Duration**: 30 minutes

#### The Challenge
Users report that the calculator sometimes returns wrong results for division.

**File**: `calculator.py`
```python
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    return a / b

def calculate(operation, a, b):
    if operation == "add":
        return add(a, b)
    elif operation == "subtract":
        return subtract(a, b)
    elif operation == "multiply":
        return multiply(a, b)
    elif operation == "divide":
        return divide(a, b)
```

**Task**:
1. Find the bug
2. Fix it
3. Add error handling
4. Add tests

#### Try It Yourself
(Take 15 minutes to attempt)

#### Solution Approach
```bash
You: "@calculator.py there's a bug with division returning wrong results sometimes. Find and fix it."

Claude will:
1. Identify: No check for division by zero
2. Fix: Add zero check
3. Suggest: Better error handling
4. Implement: Safe version

You: "Add comprehensive error handling"

You: "Write tests for all operations including edge cases"
```

#### Expected Fix
```python
def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
```

#### What You Learned
- ✅ How to describe bugs to Claude
- ✅ Claude identifies edge cases
- ✅ Error handling patterns
- ✅ Test generation

---

### Scenario 3: The Documentation Writer
**Skill**: Generating documentation
**Duration**: 20 minutes

#### The Challenge
You have a working API but no documentation.

**File**: `api.py`
```python
from flask import Flask, request, jsonify

app = Flask(__name__)

users = []

@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users)

@app.route('/users', methods=['POST'])
def create_user():
    user = request.json
    users.append(user)
    return jsonify(user), 201

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    if user_id < len(users):
        return jsonify(users[user_id])
    return jsonify({"error": "Not found"}), 404
```

**Task**:
1. Add docstrings to all functions
2. Create API documentation
3. Add usage examples
4. Create README

#### Try It Yourself
(Take 10 minutes to attempt)

#### Solution Approach
```bash
You: "@api.py add comprehensive docstrings to all functions"

You: "Create API documentation in Markdown format with:
- Endpoint descriptions
- Request/response examples
- Status codes
- Error cases"

You: "Create a README with:
- Setup instructions
- Usage examples
- API overview"
```

#### What You Learned
- ✅ Documentation generation
- ✅ Professional docstring format
- ✅ API documentation structure
- ✅ README best practices

---

## 🥈 INTERMEDIATE SCENARIOS

### Scenario 4: The Feature Factory
**Skill**: End-to-end feature implementation
**Duration**: 60 minutes

#### The Challenge
Implement a user authentication system from scratch.

**Requirements**:
- User registration
- Login/logout
- Password hashing
- JWT tokens
- Input validation
- Error handling
- Tests
- Documentation

**Starting Point**: Empty `auth.py` file

#### Try It Yourself
(Take 45 minutes to attempt)

#### Solution Approach
```bash
You: "think about implementing a secure authentication system with:
- User registration (email, password)
- Login (returns JWT token)
- Password hashing (bcrypt)
- Input validation
- Comprehensive error handling
- Protection against common attacks

Plan the implementation first."

[Claude creates detailed plan]

You: "Implement the plan using Flask and SQLAlchemy"

You: "Write comprehensive tests covering:
- Successful registration
- Duplicate email
- Invalid email format
- Weak password
- Successful login
- Invalid credentials
- Token validation"

You: "Add API documentation"

You: "Review for security vulnerabilities"
```

#### What You Learned
- ✅ Using thinking mode for planning
- ✅ Complex feature implementation
- ✅ Security best practices
- ✅ Comprehensive testing
- ✅ Professional documentation

---

### Scenario 5: The Parallel Processor
**Skill**: Parallel task execution
**Duration**: 45 minutes

#### The Challenge
You need to update 5 different services with similar changes.

**Services**:
- `user_service.py` - Add logging
- `product_service.py` - Add logging
- `order_service.py` - Add logging
- `payment_service.py` - Add logging
- `notification_service.py` - Add logging

**Also need**:
- Tests for each
- Documentation updates

**Task**: Complete everything in under 20 minutes using parallel execution

#### Try It Yourself
(Take 30 minutes to attempt)

#### Solution Approach
```bash
You: "In parallel, add comprehensive logging to all services:

1. @user_service.py - Add structured logging
2. @product_service.py - Add structured logging
3. @order_service.py - Add structured logging
4. @payment_service.py - Add structured logging
5. @notification_service.py - Add structured logging

Use same logging format and include:
- Function entry/exit
- Error logging
- Performance metrics"

[Wait for completion - should be 3-5x faster than sequential]

You: "In parallel, write tests for the logging in each service"

You: "Update documentation for all services"
```

#### What You Learned
- ✅ Massive time savings with parallel execution
- ✅ When tasks are independent
- ✅ Consistent implementation across files
- ✅ Efficient workflows

---

### Scenario 6: The Custom Command Creator
**Skill**: Building reusable workflows
**Duration**: 60 minutes

#### The Challenge
Create a complete set of custom commands for your daily workflow.

**Required Commands**:
1. `/feature` - Start new feature
2. `/bug` - Bug investigation workflow
3. `/review` - Pre-PR checklist
4. `/deploy` - Deployment checklist
5. `/learn` - Document new learnings

#### Try It Yourself
(Take 45 minutes to attempt)

#### Solution Approach

**1. Feature Command** (`.claude/commands/feature.md`)
```markdown
---
description: Start new feature with full setup
---

Starting new feature workflow:

1. Create feature branch: feature/[name]
2. Create feature file with:
   - Implementation stub
   - Test file
   - Documentation section
3. Create task list:
   - [ ] Implementation
   - [ ] Unit tests
   - [ ] Integration tests
   - [ ] Documentation
   - [ ] Code review
4. Set up background dev server

Ask for feature name and details.
```

**2. Bug Command** (`.claude/commands/bug.md`)
```markdown
---
description: Bug investigation workflow
---

Bug investigation process:

1. Gather information:
   - What's the expected behavior?
   - What's the actual behavior?
   - How to reproduce?
   - Relevant logs?

2. Investigation:
   - Read relevant code
   - Check recent changes
   - Look for similar issues

3. Root cause analysis (use thinking mode)

4. Propose fix with:
   - Code changes
   - Tests to prevent regression
   - Documentation if needed

5. Verify fix
```

**Test your commands**:
```bash
You: "/feature user-profile"
You: "/bug authentication timeout"
```

#### What You Learned
- ✅ Custom command structure
- ✅ Workflow templating
- ✅ Reusable processes
- ✅ Time-saving automation

---

### Scenario 7: The Agent Builder
**Skill**: Creating specialized AI agents
**Duration**: 90 minutes

#### The Challenge
Build a team of specialized agents for different code review aspects.

**Agents to Create**:
1. **Security Reviewer** - Finds security issues
2. **Performance Optimizer** - Identifies performance problems
3. **Test Coverage Checker** - Ensures good test coverage
4. **Documentation Verifier** - Checks documentation quality
5. **Code Style Guardian** - Enforces code style

#### Try It Yourself
(Take 60 minutes to attempt)

#### Solution Approach

**1. Security Reviewer** (`.claude/agents/security-reviewer.md`)
```markdown
---
name: security-reviewer
description: Security vulnerability detection
tools:
  - Read
  - Grep
---

You are a security expert specializing in application security.

When reviewing code, check for:
1. SQL Injection vulnerabilities
2. XSS vulnerabilities
3. Authentication/authorization flaws
4. Secrets in code
5. Insecure dependencies
6. CSRF protection
7. Input validation
8. Secure communication

For each issue found:
- Severity: Critical/High/Medium/Low
- Location: File and line number
- Description: What's the issue?
- Impact: What could happen?
- Fix: How to resolve it?
- Example: Show secure code

Prioritize issues by severity.
```

**2. Performance Optimizer** (`.claude/agents/performance-optimizer.md`)
```markdown
---
name: performance-optimizer
description: Performance bottleneck detection
tools:
  - Read
  - Grep
  - Bash
---

You are a performance optimization expert.

Analyze code for:
1. N+1 query problems
2. Missing database indexes
3. Inefficient algorithms
4. Memory leaks
5. Unnecessary computations
6. Blocking operations
7. Large data transfers
8. Missing caching

For each issue:
- Location: File and line
- Impact: Expected performance gain
- Fix: Specific optimization
- Benchmark: Before/after comparison

Suggest profiling commands when needed.
```

**Test your agent team**:
```bash
You: "@security-reviewer audit @src/auth.py"
You: "@performance-optimizer analyze @src/api.py"
```

#### What You Learned
- ✅ Agent specialization
- ✅ Tool selection for agents
- ✅ Structured output formats
- ✅ Team of agents approach

---

## 🥇 ADVANCED SCENARIOS

### Scenario 8: The Emergency Responder
**Skill**: Production incident response
**Duration**: 30 minutes (timed challenge)

#### The Challenge
**URGENT**: Production is down. You have 30 minutes to find and fix the issue.

**Symptoms**:
- API returning 500 errors
- Database connection timeouts
- Started 2 hours ago after deployment

**Available**:
- Error logs: `logs/production.log`
- Recent commits: Last 5 commits
- Application code: `src/`
- Database config: `config/database.yml`

**Task**:
1. Identify root cause (10 min)
2. Implement fix (10 min)
3. Verify and deploy (5 min)
4. Create incident report (5 min)

#### Try It Yourself
(Set a 30-minute timer!)

#### Solution Approach
```bash
# Minute 0-10: Root cause analysis
You: "ultrathink - PRODUCTION EMERGENCY
Symptoms: API 500 errors, DB timeouts, started 2h ago
1. Analyze @logs/production.log
2. Review recent commits
3. Check @config/database.yml
4. Find root cause ASAP"

[Claude identifies: Connection pool size reduced in recent commit]

# Minute 10-20: Fix implementation
You: "Create hotfix that:
1. Restores proper connection pool size
2. Adds connection pool monitoring
3. Includes rollback plan
4. Has deployment commands ready"

# Minute 20-25: Verification
You: "Generate verification steps:
1. Test script for connection pool
2. Monitoring checks
3. Rollback if needed"

# Minute 25-30: Incident report
You: "Create incident report with:
- Timeline
- Root cause
- Fix applied
- Preventive measures
- Action items"
```

#### Success Criteria
- ✅ Root cause identified < 10 min
- ✅ Fix implemented < 20 min
- ✅ Verified and deployed < 25 min
- ✅ Incident report < 30 min

#### What You Learned
- ✅ Emergency response workflow
- ✅ Rapid root cause analysis
- ✅ Quick fix implementation
- ✅ Incident documentation

---

### Scenario 9: The Workflow Orchestrator
**Skill**: Complex multi-step automation
**Duration**: 120 minutes

#### The Challenge
Create a complete CI/CD pipeline with quality gates.

**Requirements**:
1. **Pre-commit hooks**: Format, lint, test
2. **PR workflow**:
   - Auto-review code
   - Run full test suite
   - Check coverage (>80%)
   - Security scan
   - Performance test
3. **Deployment workflow**:
   - Build Docker image
   - Run integration tests
   - Deploy to staging
   - Smoke tests
   - Deploy to production (manual approval)
4. **Monitoring**: Error tracking, performance

#### Try It Yourself
(Take 90 minutes to attempt)

#### Solution Approach

**Phase 1: Hooks Setup** (`.claude/settings.json`)
```json
{
  "hooks": {
    "PostToolUse": {
      "tools": ["Write", "Edit"],
      "command": "npx prettier --write $FILE_PATH && npm run lint -- --fix $FILE_PATH",
      "description": "Auto-format and lint"
    },
    "PreToolUse": {
      "tools": ["Bash(git commit:*)"],
      "command": "npm test && npm run coverage",
      "description": "Tests and coverage before commit"
    }
  }
}
```

**Phase 2: GitHub Actions Workflow**
```bash
You: "Create GitHub Actions workflow with:
1. PR checks (lint, test, coverage, security)
2. Build workflow (Docker image)
3. Deploy workflow (staging → production)
4. Include quality gates
5. Add manual approval for production"
```

**Phase 3: Custom Commands**
```bash
# Create /pre-commit command
# Create /pre-pr command
# Create /deploy command
```

**Phase 4: Monitoring**
```bash
You: "Add monitoring with:
1. Error tracking (Sentry)
2. Performance monitoring (DataDog)
3. Health checks
4. Alerting rules"
```

#### What You Learned
- ✅ Complete CI/CD design
- ✅ Quality gate implementation
- ✅ Automation at scale
- ✅ Production-ready systems

---

### Scenario 10: The Knowledge Transfer
**Skill**: Documentation and teaching
**Duration**: 90 minutes

#### The Challenge
You're leaving the project. Create comprehensive knowledge transfer.

**What to Document**:
1. System architecture
2. Key decisions and why
3. Common issues and solutions
4. Deployment process
5. Monitoring and alerts
6. Emergency procedures
7. Team contacts
8. Future roadmap

#### Try It Yourself
(Take 60 minutes to attempt)

#### Solution Approach
```bash
You: "Analyze my commit history and create knowledge transfer documentation:

1. What systems do I primarily work on?
2. What are the key architectural decisions I made?
3. What are recurring issues I've fixed?
4. What processes do I own?

Analyze: @src/ and git history"

You: "Create comprehensive handoff documentation with:
- System ownership map
- Critical knowledge for each system
- Known issues and solutions
- Deployment runbooks
- Emergency response procedures
- Access and credentials checklist
- Key contacts
- TODO list for successor"

You: "Create onboarding checklist for my replacement"
```

#### What You Learned
- ✅ Knowledge capture
- ✅ Documentation structure
- ✅ Handoff best practices
- ✅ Continuity planning

---

## 🎯 Challenge Modes

### Speed Run Mode
Complete any scenario in half the suggested time.

**Tips**:
- Use parallel execution
- Leverage custom commands
- Use specialized agents
- Pre-configure permissions

### Quality Mode
Complete scenario with perfect code quality.

**Requirements**:
- 100% test coverage
- Zero linting errors
- Security scan passed
- Performance optimized
- Professional documentation

### Teaching Mode
Complete scenario while explaining to someone else.

**Benefits**:
- Deepens understanding
- Reveals knowledge gaps
- Helps others learn
- Builds communication skills

---

## 📊 Progress Tracker

### Beginner Scenarios
- [ ] Scenario 1: First Conversation
- [ ] Scenario 2: Bug Hunter
- [ ] Scenario 3: Documentation Writer

### Intermediate Scenarios
- [ ] Scenario 4: Feature Factory
- [ ] Scenario 5: Parallel Processor
- [ ] Scenario 6: Custom Command Creator
- [ ] Scenario 7: Agent Builder

### Advanced Scenarios
- [ ] Scenario 8: Emergency Responder
- [ ] Scenario 9: Workflow Orchestrator
- [ ] Scenario 10: Knowledge Transfer

### Mastery Achievements
- [ ] Completed all scenarios
- [ ] Beat all time challenges
- [ ] Achieved quality mode on 5+ scenarios
- [ ] Created 10+ custom commands
- [ ] Built 5+ custom agents
- [ ] Saved 20+ hours in one week
- [ ] Taught 3+ people

---

## 🏆 Create Your Own Scenarios

### Template for Custom Scenarios

```markdown
### Scenario X: [Name]
**Skill**: [What skill this teaches]
**Duration**: [Expected time]

#### The Challenge
[Describe the scenario and context]

**Starting Point**: [What you have]
**Goal**: [What you need to achieve]
**Constraints**: [Time, resources, requirements]

#### Try It Yourself
(Attempt before looking at solution)

#### Solution Approach
[Step-by-step solution]

#### What You Learned
- ✅ [Learning 1]
- ✅ [Learning 2]
- ✅ [Learning 3]
```

### Your Custom Scenarios
Document real challenges from your work:

1. **Scenario**: _____________
2. **Scenario**: _____________
3. **Scenario**: _____________

---

## 📈 Measuring Progress

### After Each Scenario

**Reflect**:
1. What went well?
2. What was challenging?
3. What would you do differently?
4. What new technique did you learn?
5. How will you use this at work?

**Measure**:
- Time taken vs. target
- Quality of output
- Skills practiced
- Confidence level (1-10)

**Plan**:
- What to practice next?
- What needs more work?
- What to apply immediately?

---

## 🎓 Graduation Challenge

### The Ultimate Scenario
Combine everything you've learned in one final project.

**Duration**: 4 hours
**Requirements**: Use 20+ different skills

**Project**: "Complete Development Environment"

Build a fully automated development environment with:
1. Custom commands for all common tasks
2. Specialized agents for code review
3. Automated quality gates (hooks)
4. CI/CD pipeline
5. Monitoring and alerting
6. Documentation automation
7. Emergency response playbooks
8. Team collaboration tools

**Success Criteria**:
- Production-ready quality
- 5x productivity improvement
- Comprehensive documentation
- Shareable with team

---

## 🚀 Next Steps

1. **Start**: Pick a scenario at your level
2. **Practice**: Complete all scenarios in your level
3. **Challenge**: Try speed/quality modes
4. **Create**: Build custom scenarios from real work
5. **Share**: Teach others using these scenarios
6. **Master**: Complete graduation challenge

**Remember**: Every scenario completed makes you more productive forever!

---

**Document Version**: 1.0
**Last Updated**: 2025-10-31
**Practice Scenarios**: 10 core + unlimited custom
