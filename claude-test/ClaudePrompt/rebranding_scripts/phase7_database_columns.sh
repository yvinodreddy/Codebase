#!/bin/bash
# phase7_database_columns.sh
# CHANGE 7.2: Rename database columns

set -e

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_FILE="/home/user01/claude-test/ParaGroupAI/rebranding_logs/phase7_db_columns_${TIMESTAMP}.log"

echo "==================================================================" | tee -a "$LOG_FILE"
echo "PHASE 7.2: Database Column Rename" | tee -a "$LOG_FILE"
echo "==================================================================" | tee -a "$LOG_FILE"

# Generate SQL migration script
cat > /home/user01/claude-test/ParaGroupAI/migrations/rename_columns.sql << 'EOF'
-- Para Group AI Orchestrator® - Column Rename Migration
-- Created: 2025-11-28

-- Rename columns containing "claudeprompt" references
ALTER TABLE paragroup_contexts
  RENAME COLUMN claudeprompt_version TO paragroup_version;

ALTER TABLE paragroup_sessions
  RENAME COLUMN claudeprompt_config TO paragroup_config;

-- Add comments
COMMENT ON TABLE paragroup_contexts IS 'Para Group AI Orchestrator® context storage';
COMMENT ON TABLE paragroup_messages IS 'Para Group AI Orchestrator® message history';
EOF

echo "✅ Created SQL migration script: migrations/rename_columns.sql" | tee -a "$LOG_FILE"
echo "✅ PHASE 7.2 COMPLETE" | tee -a "$LOG_FILE"