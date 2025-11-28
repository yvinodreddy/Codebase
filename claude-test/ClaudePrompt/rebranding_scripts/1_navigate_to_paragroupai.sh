#!/bin/bash

# 1. Navigate to ParaGroupAI directory
cd /home/user01/claude-test/ParaGroupAI

# 2. Make all scripts executable
chmod +x *.sh

# 3. Run master execution script
bash EXECUTE_REBRANDING.sh

# 4. Review output log
cat rebranding_logs/MASTER_EXECUTION_*.log

# 5. Activate new bash alias
source ~/.bashrc

# 6. Test new CLI command
prsg "test prompt" -v