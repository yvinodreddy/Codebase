#!/bin/bash
# phase10_license.sh
# CHANGE 10.2: Update LICENSE file

set -e

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_DIR="/home/user01/claude-test/ClaudePrompt/rebranding_scripts/logs"
mkdir -p "$LOG_DIR"
LOG_FILE="${LOG_DIR}/phase10_license_${TIMESTAMP}.log"

echo "==================================================================" | tee -a "$LOG_FILE"
echo "PHASE 10.2: LICENSE File Update" | tee -a "$LOG_FILE"
echo "==================================================================" | tee -a "$LOG_FILE"

cd /home/user01/claude-test/ParaGroupAI

if [ -f "LICENSE" ]; then
    # Backup
    cp LICENSE LICENSE.prebrand.bak

    # Update copyright holder
    sed -i 's/Copyright (c) .* ClaudePrompt/Copyright (c) 2025 Para Group LLC/g' LICENSE

    # Add trademark notice at end
    cat >> LICENSE << 'EOF'

---

TRADEMARK NOTICE

Para Group® is a registered trademark of Para Group LLC.
USPTO Registration Numbers: 7113228 (Word Mark), 7113231 (Logo Mark)
Registration Date: July 18, 2023

Use of the Para Group® trademark requires written permission from Para Group LLC.
EOF

    echo "✅ Updated LICENSE file" | tee -a "$LOG_FILE"
else
    echo "⚠️  LICENSE file not found - creating new one" | tee -a "$LOG_FILE"

    cat > LICENSE << 'EOF'
Para Group AI Orchestrator® - LICENSE

Copyright (c) 2025 Para Group LLC. All rights reserved.

[Your license terms here - MIT, Apache 2.0, Proprietary, etc.]

---

TRADEMARK NOTICE

Para Group® is a registered trademark of Para Group LLC.
USPTO Registration Numbers: 7113228 (Word Mark), 7113231 (Logo Mark)
Registration Date: July 18, 2023

Use of the Para Group® trademark requires written permission from Para Group LLC.
EOF

    echo "✅ Created LICENSE file" | tee -a "$LOG_FILE"
fi

echo "✅ PHASE 10.2 COMPLETE" | tee -a "$LOG_FILE"