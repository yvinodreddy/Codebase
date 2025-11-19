# BEST PRACTICES - DIRECTORY STRUCTURE & PROJECT MANAGEMENT

**Version:** 1.0.0
**Date:** 2025-11-19

================================================================================

## 🎯 UNDERSTANDING PROJECT AUTO-DETECTION

The database-first integration automatically creates projects based on your **working directory**. Each unique directory path gets its own project.

================================================================================

## 📁 DIRECTORY STRUCTURE PATTERNS

### ✅ RECOMMENDED: One Root Directory Per Logical Project

**Pattern:**
```
/home/user01/my-app/
  ├── frontend/
  ├── backend/
  ├── tests/
  └── docs/
```

**Usage:**
```bash
# Always work from the root
cd /home/user01/my-app

# All commands use same project
cpp "implement frontend feature" -v
cpp "add backend API endpoint" -v
cpp "write integration tests" -v
cpp "update documentation" -v
```

**Result:**
- ✅ ONE project: `proj_my-app_xxxxx`
- ✅ ONE instance per session
- ✅ All context stored together
- ✅ Easy to track and manage

================================================================================

## ⚠️ WHAT HAPPENS WITH SUBDIRECTORIES

### Scenario: Working from Different Subdirectories

```bash
# From root
cd /home/user01/my-app
cpp "plan architecture" -v
# → Project: proj_my-app_xxxxx

# From frontend subdirectory
cd /home/user01/my-app/frontend
cpp "create navbar component" -v
# → Project: proj_frontend_yyyyy  (DIFFERENT PROJECT!)

# From backend subdirectory
cd /home/user01/my-app/backend
cpp "implement auth" -v
# → Project: proj_backend_zzzzz  (DIFFERENT PROJECT!)
```

**Result:**
- ⚠️ THREE separate projects created
- ⚠️ THREE separate instances
- ⚠️ Context split across projects
- ⚠️ Harder to track holistically

================================================================================

## 💡 BEST PRACTICE: STAY AT ROOT LEVEL

### Why Root Level is Better

**1. Unified Context**
   - All work on the project stays together
   - Easy to review project history
   - Token usage tracked holistically

**2. Simpler Management**
   - One project ID to remember
   - One instance to monitor
   - Clear project boundaries

**3. Better Visibility**
   - `./db-cli inspect proj_my-app_xxxxx` shows everything
   - All snapshots in one place
   - Complete project timeline

### Example: Full Stack Development

```bash
# ✅ RECOMMENDED: Work from root
cd /home/user01/full-stack-app

cpp "design database schema" -v
cpp "implement user model in backend" -v
cpp "create login UI in frontend" -v
cpp "write API integration tests" -v

# All stored in: proj_full-stack-app_xxxxx
./db-cli inspect proj_full-stack-app_xxxxx
# Shows all 4 snapshots together
```

```bash
# ❌ NOT RECOMMENDED: Work from subdirectories
cd /home/user01/full-stack-app/backend
cpp "implement user model" -v          # proj_backend_xxx

cd /home/user01/full-stack-app/frontend
cpp "create login UI" -v                # proj_frontend_yyy

cd /home/user01/full-stack-app/tests
cpp "write integration tests" -v        # proj_tests_zzz

# Context split across 3 projects - harder to manage!
```

================================================================================

## 🔧 MANUAL PROJECT ID OVERRIDE

### When You Have Multiple Logical Projects in One Directory

**Scenario:**
```
/home/user01/ClaudePrompt/
  ├── web-ui-implementation/     (Separate project)
  ├── database/                  (Part of core)
  ├── guardrails/                (Part of core)
  └── agent_framework/           (Part of core)
```

You might want:
- One project for core ULTRATHINK
- One project for web-ui-implementation

### Solution: Use --project-id Flag

**Step 1: Create initial projects from respective directories**

```bash
# Create core ULTRATHINK project
cd /home/user01/ClaudePrompt
cpp "core ULTRATHINK work" -v
# → Creates: proj_ClaudePrompt_xxxxx
# Note the project ID shown at start and end

# Create web-ui project
cd /home/user01/ClaudePrompt/web-ui-implementation
cpp "web UI work" -v
# → Creates: proj_web-ui-implementation_yyy
# Note the project ID shown at start and end
```

**Step 2: Reuse project IDs explicitly**

```bash
# Work on web-ui from ANY directory
cd /home/user01/ClaudePrompt
cpp "add dashboard to web UI" -v --project-id proj_web-ui-implementation_yyy

# Work on core from ANY directory
cd /home/user01/ClaudePrompt/web-ui-implementation
cpp "enhance guardrails" -v --project-id proj_ClaudePrompt_xxxxx
```

**Benefits:**
- ✅ Work from any directory
- ✅ Explicitly control which project stores context
- ✅ Keep logical projects separate
- ✅ Override auto-detection when needed

================================================================================

## 📊 PROJECT ID DISPLAY

### Automatic Display at Start and End

Every cpp/cpps command now displays project ID:

**At Start:**
```
================================================================================
📊 DATABASE-FIRST CONTEXT - SESSION INFO
================================================================================

  📁 Project ID:  proj_my-app_a1b2c3d4
  🔹 Instance ID: inst_20251119_163000_abc123
  📂 Directory:   /home/user01/my-app

  💡 TIP: Use --project-id flag to override auto-detection
     Example: cpp "prompt" --project-id proj_my-app_a1b2c3d4

================================================================================
```

**At End:**
```
================================================================================
📊 DATABASE-FIRST CONTEXT - SESSION SUMMARY
================================================================================

  ✅ Context stored successfully
  📁 Project ID:  proj_my-app_a1b2c3d4
  🔹 Instance ID: inst_20251119_163000_abc123

  📊 View status:   ./db-cli status
  🔍 Inspect:       ./db-cli inspect proj_my-app_a1b2c3d4
  📝 View context:  ./db-cli context --project proj_my-app_a1b2c3d4

  💡 Reuse project: cpp "next prompt" --project-id proj_my-app_a1b2c3d4

================================================================================
```

**Copy the project ID from either location and use it in future commands!**

================================================================================

## 🎓 REAL-WORLD EXAMPLES

### Example 1: Monolithic Application

```
/home/user01/ecommerce-platform/
  ├── src/
  ├── tests/
  ├── docs/
  └── config/
```

**Best Practice:**
```bash
# Always work from root
cd /home/user01/ecommerce-platform

cpp "add payment gateway" -v
cpp "write unit tests" -v
cpp "update API docs" -v

# All use: proj_ecommerce-platform_xxxxx
```

### Example 2: Microservices Architecture

```
/home/user01/microservices/
  ├── user-service/
  ├── order-service/
  ├── payment-service/
  └── shared-lib/
```

**Option A: Separate Projects (Recommended for Microservices)**
```bash
# Each service gets own project
cd /home/user01/microservices/user-service
cpp "implement user auth" -v
# → proj_user-service_xxx

cd /home/user01/microservices/order-service
cpp "process orders" -v
# → proj_order-service_yyy

cd /home/user01/microservices/payment-service
cpp "integrate Stripe" -v
# → proj_payment-service_zzz
```

**Option B: Unified Project with Manual Override**
```bash
# Create service projects once
cd /home/user01/microservices/user-service
cpp "initial setup" -v
# Note: proj_user-service_xxx

cd /home/user01/microservices/order-service
cpp "initial setup" -v
# Note: proj_order-service_yyy

# Work from root with explicit project IDs
cd /home/user01/microservices

cpp "user service: add auth" -v --project-id proj_user-service_xxx
cpp "order service: add validation" -v --project-id proj_order-service_yyy
cpp "shared lib: add utilities" -v  # Auto-creates proj_microservices_www
```

### Example 3: Frontend + Backend Monorepo

```
/home/user01/my-app/
  ├── client/     (React frontend)
  ├── server/     (Node.js backend)
  └── shared/     (Common code)
```

**Recommended: Single Project from Root**
```bash
cd /home/user01/my-app

cpp "add login page to client" -v
cpp "implement auth API in server" -v
cpp "create shared types" -v

# All in: proj_my-app_xxxxx
./db-cli inspect proj_my-app_xxxxx
# Shows complete full-stack development history
```

### Example 4: Complex Project with Sub-Projects

```
/home/user01/platform/
  ├── main-app/       (Core application)
  ├── admin-panel/    (Separate admin UI)
  ├── mobile-app/     (Mobile version)
  └── docs/           (Documentation)
```

**Strategy: Manual Project ID Management**

```bash
# Step 1: Initialize each sub-project
cd /home/user01/platform/main-app
cpp "initialize main app" -v
# Copy project ID: proj_main-app_aaa

cd /home/user01/platform/admin-panel
cpp "initialize admin" -v
# Copy project ID: proj_admin-panel_bbb

cd /home/user01/platform/mobile-app
cpp "initialize mobile" -v
# Copy project ID: proj_mobile-app_ccc

# Step 2: Work from anywhere with explicit IDs
cd /home/user01/platform

cpp "main: add feature X" -v --project-id proj_main-app_aaa
cpp "admin: add user management" -v --project-id proj_admin-panel_bbb
cpp "mobile: implement offline mode" -v --project-id proj_mobile-app_ccc

# Step 3: Monitor each project separately
./db-cli inspect proj_main-app_aaa
./db-cli inspect proj_admin-panel_bbb
./db-cli inspect proj_mobile-app_ccc
```

================================================================================

## 🛠️ TROUBLESHOOTING

### Problem: Too Many Projects Created

**Symptoms:**
```bash
./db-cli projects
# Shows many auto-created projects:
# - proj_my-app_xxx
# - proj_frontend_yyy
# - proj_backend_zzz
# - proj_tests_www
```

**Cause:** Working from different subdirectories

**Solution 1: Consolidate Future Work**
```bash
# Always work from root going forward
cd /home/user01/my-app
cpp "all future work" -v --project-id proj_my-app_xxx
```

**Solution 2: Clean Up Database** (Advanced)
```bash
# Manually merge projects in database
# Or delete unwanted projects
# (Requires direct database manipulation)
```

### Problem: Forgot Project ID

**Solution:**
```bash
# View all projects
./db-cli projects

# Or check current session
python3 database/auto_context_integration.py session
```

### Problem: Wrong Project Auto-Detected

**Symptoms:**
You're in `/home/user01/my-app/frontend` but want to use the root project.

**Solution:**
```bash
# Use --project-id flag
cpp "work" -v --project-id proj_my-app_xxxxx

# Or change to root directory
cd /home/user01/my-app
cpp "work" -v
```

================================================================================

## 📋 DECISION TREE

```
Are you working on a single logical project?
├─ YES → Work from ONE root directory
│         Always cd to same place before cpp/cpps
│         Result: Clean, unified project
│
└─ NO → Multiple logical projects in one directory?
   ├─ YES → Use --project-id to explicitly choose
   │         Create each project once from its directory
   │         Copy project IDs for future use
   │         Result: Separate projects, full control
   │
   └─ STILL UNCLEAR → Use auto-detection initially
                      Monitor with ./db-cli projects
                      Refine strategy based on what you see
                      Result: Evolve approach as needed
```

================================================================================

## ✅ RECOMMENDATIONS SUMMARY

### DO:
✅ Work from ONE consistent root directory per logical project
✅ Copy and save project IDs when they're displayed
✅ Use --project-id for explicit control when needed
✅ Monitor with `./db-cli projects` regularly
✅ Keep logical projects separate (microservices, sub-apps)

### DON'T:
❌ Randomly change directories during development
❌ Ignore project IDs displayed at start/end
❌ Mix unrelated work in same project
❌ Create projects unnecessarily

### WHEN IN DOUBT:
💡 Run `./db-cli projects` to see current state
💡 Use `./db-cli inspect proj_xxx` to review project contents
💡 Check `python3 database/auto_context_integration.py session`

================================================================================

## 🎉 CONCLUSION

**SIMPLEST APPROACH (95% of use cases):**
1. One directory per project
2. Always cd to root before cpp/cpps
3. Let auto-detection handle everything

**ADVANCED APPROACH (Complex monorepos):**
1. Create sub-projects from their directories
2. Copy project IDs (displayed at start/end)
3. Use --project-id flag for explicit control
4. Monitor with ./db-cli tools

**BOTH APPROACHES ARE SUPPORTED AND PRODUCTION-READY!**

================================================================================

**Next Steps:**
1. Decide on your directory structure strategy
2. Create initial projects from appropriate directories
3. Copy project IDs for future use
4. Use ./db-cli to monitor and verify

**Questions? Check:**
- `AUTOMATIC_INTEGRATION_GUIDE.md` - Complete automatic integration guide
- `DATABASE_FIRST_USER_GUIDE.md` - Manual database operations
- `./db-cli --help` - CLI tool reference
