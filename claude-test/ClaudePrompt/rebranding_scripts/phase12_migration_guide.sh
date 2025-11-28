#!/bin/bash
# phase12_migration_guide.sh
# CHANGE 12.2: Create user migration guide

set -e

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_FILE="/home/user01/claude-test/ParaGroupAI/rebranding_logs/phase12_migration_${TIMESTAMP}.log"

echo "==================================================================" | tee -a "$LOG_FILE"
echo "PHASE 12.2: Migration Guide Creation" | tee -a "$LOG_FILE"
echo "==================================================================" | tee -a "$LOG_FILE"

cd /home/user01/claude-test/ParaGroupAI

cat > MIGRATION_GUIDE.md << 'EOF'
# Para Group AI Orchestrator® - Migration Guide

**Effective Date:** 2025-11-28
**Version:** 1.0

---

## What's Changing?

We've rebranded from "ClaudePrompt" to **Para Group AI Orchestrator®** to better reflect our mission and eliminate potential trademark conflicts.

### Key Changes:

| Old | New |
|-----|-----|
| Product: ClaudePrompt | Product: Para Group AI Orchestrator® |
| CLI Command: `cpp` | CLI Command: `prsg` |
| Directory: ClaudePrompt/ | Directory: ParaGroupAI/ |
| Package: claudeprompt | Package: para-group-ai-orchestrator |

---

## For Users

### Immediate Actions:

1. **Update your bash alias:**
   ```bash
   source ~/.bashrc  # Load new 'prsg' alias
   ```

2. **Start using new CLI command:**
   ```bash
   # Old way (still works during transition):
   cpp "your prompt" -v

   # New way (recommended):
   prsg "your prompt" -v
   ```

3. **Update bookmarks:**
   - Old: (old domain if applicable)
   - New: https://ai.paragroup.com

### Backward Compatibility:

✅ **Good news:** Existing scripts and workflows will continue to work!

- `cpp` command still works (symlinked to `prsg`)
- Old imports still work (backward compatibility shims)
- Database views preserve old table names
- 301 redirects preserve old URLs

### Deprecation Timeline:

- **Phase 1 (Months 1-3):** Both `cpp` and `prsg` work
- **Phase 2 (Months 4-6):** Deprecation warnings for `cpp`
- **Phase 3 (Month 7+):** Remove `cpp` (prsg only)

---

## For Developers

### Update Your Code:

**Python imports:**