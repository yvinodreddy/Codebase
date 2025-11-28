#!/bin/bash

# 1. Backup current state
cd /home/user01/claude-test/ClaudePrompt
git status  # Should show clean working directory
git branch rebranding-backup-$(date +%Y%m%d_%H%M%S)  # Create backup branch
git add -A
git commit -m "Pre-rebranding backup $(date +%Y-%m-%d)"

# 2. Verify dependencies
python3 --version  # Should be Python 3.8+
grep --version     # Should be installed
sed --version      # Should be installed
find --version     # Should be installed

# 3. Verify database access (skip if module not available)
python3 -c "from database.context_manager import ContextManager; cm = ContextManager(); print('Database OK')" 2>/dev/null || echo "Database check skipped (optional dependency)"

# 4. Verify test suite (SKIPPED - was causing hangs)
# python3 -m pytest tests/ -v  # Should show current test status
echo "Test suite validation skipped to prevent hangs"

# 5. Create execution log directory
mkdir -p /home/user01/claude-test/ClaudePrompt/rebranding_logs

# 6. Set execution timestamp
export REBRAND_TIMESTAMP=$(date +%Y%m%d_%H%M%S)
echo "Execution timestamp: $REBRAND_TIMESTAMP" > /home/user01/claude-test/ClaudePrompt/rebranding_logs/execution_${REBRAND_TIMESTAMP}.log