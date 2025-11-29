#!/bin/bash
# phase7_database_tables.sh
# CHANGE 7.1: Rename database tables

set -e

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_DIR="/home/user01/claude-test/ClaudePrompt/rebranding_scripts/logs"
mkdir -p "$LOG_DIR"
LOG_FILE="${LOG_DIR}/phase7_db_tables_${TIMESTAMP}.log"

echo "==================================================================" | tee -a "$LOG_FILE"
echo "PHASE 7.1: Database Table Rename" | tee -a "$LOG_FILE"
echo "==================================================================" | tee -a "$LOG_FILE"

# Generate SQL migration script
cat > /home/user01/claude-test/ParaGroupAI/migrations/rename_tables.sql << 'EOF'
-- Para Group AI Orchestrator® - Table Rename Migration
-- Created: 2025-11-28

-- Rename tables (PostgreSQL syntax)
ALTER TABLE claudeprompt_contexts RENAME TO paragroup_contexts;
ALTER TABLE claudeprompt_messages RENAME TO paragroup_messages;
ALTER TABLE claudeprompt_sessions RENAME TO paragroup_sessions;
ALTER TABLE claudeprompt_users RENAME TO paragroup_users;

-- Update foreign key constraints (if needed)
-- ALTER TABLE paragroup_messages
--   DROP CONSTRAINT fk_claudeprompt_context,
--   ADD CONSTRAINT fk_paragroup_context
--   FOREIGN KEY (context_id) REFERENCES paragroup_contexts(id);

-- Create views for backward compatibility (optional)
CREATE OR REPLACE VIEW claudeprompt_contexts AS SELECT * FROM paragroup_contexts;
CREATE OR REPLACE VIEW claudeprompt_messages AS SELECT * FROM paragroup_messages;
CREATE OR REPLACE VIEW claudeprompt_sessions AS SELECT * FROM paragroup_sessions;
CREATE OR REPLACE VIEW claudeprompt_users AS SELECT * FROM paragroup_users;
EOF

echo "✅ Created SQL migration script: migrations/rename_tables.sql" | tee -a "$LOG_FILE"
echo "⚠️  NOTE: Review and execute manually with appropriate database credentials" | tee -a "$LOG_FILE"
echo "✅ PHASE 7.1 COMPLETE" | tee -a "$LOG_FILE"