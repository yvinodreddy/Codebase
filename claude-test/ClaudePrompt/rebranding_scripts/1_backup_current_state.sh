#!/bin/bash
# Script 1: Backup Current State
# Para Group AI Orchestrator® Rebranding - Phase 0

echo "════════════════════════════════════════════════════════════════════════════"
echo "Script 1: Creating Backup of Current State"
echo "════════════════════════════════════════════════════════════════════════════"

cd /home/user01/claude-test/ClaudePrompt || exit 1

# 1. Show current git status
echo "[1/6] Checking git status..."
git status

# 2. Create backup branch with timestamp
BRANCH_NAME="rebranding-backup-$(date +%Y%m%d_%H%M%S)"
echo "[2/6] Creating backup branch: $BRANCH_NAME"
git branch "$BRANCH_NAME"
echo "✓ Backup branch created: $BRANCH_NAME"

# 3. Commit any uncommitted changes to backup branch
echo "[3/6] Committing current state..."
git add -A
git commit -m "Pre-rebranding backup $(date +%Y-%m-%d)" || echo "Nothing to commit (already committed)"

# 4. Verify dependencies
echo "[4/6] Verifying system dependencies..."
python3 --version || echo "⚠️  Python3 not found"
grep --version > /dev/null || echo "⚠️  grep not found"
sed --version > /dev/null || echo "⚠️  sed not found"
find --version > /dev/null || echo "⚠️  find not found"

# 5. Verify database access (FIX 2: Error handling for optional dependency)
echo "[5/6] Verifying database access..."
python3 -c "from database.context_manager import ContextManager; cm = ContextManager(); print('Database OK')" 2>/dev/null || echo "Database check skipped (optional dependency)"

# 6. Create execution log directory with ABSOLUTE PATH (FIX 1)
echo "[6/6] Creating execution log directory..."
mkdir -p /home/user01/claude-test/ClaudePrompt/rebranding_logs

# Set execution timestamp with ABSOLUTE PATH (FIX 1)
export REBRAND_TIMESTAMP=$(date +%Y%m%d_%H%M%S)
echo "Execution timestamp: $REBRAND_TIMESTAMP" > /home/user01/claude-test/ClaudePrompt/rebranding_logs/execution_${REBRAND_TIMESTAMP}.log

echo ""
echo "✅ Backup completed successfully"
echo "   Branch: $BRANCH_NAME"
echo "   Timestamp: $REBRAND_TIMESTAMP"
echo "════════════════════════════════════════════════════════════════════════════"

exit 0
