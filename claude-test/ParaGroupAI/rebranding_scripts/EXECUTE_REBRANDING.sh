#!/bin/bash
#
# Master Execution Script for Para Group AI Orchestrator® Rebranding
# This script executes all rebranding changes in the correct order
#
# Generated: $(date)
# Backup Branch: rebranding-backup-$(date +%Y%m%d_%H%M%S) (already created)
#

# NOTE: Not using 'set -e' because we handle errors explicitly with if/then/else blocks

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
SCRIPTS_DIR="/home/user01/claude-test/ClaudePrompt/rebranding_scripts"
LOG_DIR="/home/user01/claude-test/ClaudePrompt/rebranding_scripts/logs"
MASTER_LOG="${LOG_DIR}/MASTER_EXECUTION_${TIMESTAMP}.log"

# Create log directory
mkdir -p "${LOG_DIR}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "================================================================================" | tee -a "${MASTER_LOG}"
echo "Para Group AI Orchestrator® Rebranding Execution" | tee -a "${MASTER_LOG}"
echo "================================================================================" | tee -a "${MASTER_LOG}"
echo "Start Time: $(date)" | tee -a "${MASTER_LOG}"
echo "Backup Branch: Available on GitHub" | tee -a "${MASTER_LOG}"
echo "" | tee -a "${MASTER_LOG}"

# Counter for tracking
TOTAL_SCRIPTS=36
SUCCESSFUL=0
FAILED=0

# Execute each script

echo "[1/36] Executing: 1_backup_current_state.sh" | tee -a "${MASTER_LOG}"
if bash "${SCRIPTS_DIR}/1_backup_current_state.sh" >> "${MASTER_LOG}" 2>&1; then
    echo -e "${GREEN}✓ 1_backup_current_state.sh completed successfully${NC}" | tee -a "${MASTER_LOG}"
    ((SUCCESSFUL++))
else
    echo -e "${RED}✗ 1_backup_current_state.sh failed${NC}" | tee -a "${MASTER_LOG}"
    ((FAILED++))
fi
echo "" | tee -a "${MASTER_LOG}"

echo "[2/36] Executing: phase1_product_name_rebrand.sh" | tee -a "${MASTER_LOG}"
if bash "${SCRIPTS_DIR}/phase1_product_name_rebrand.sh" >> "${MASTER_LOG}" 2>&1; then
    echo -e "${GREEN}✓ phase1_product_name_rebrand.sh completed successfully${NC}" | tee -a "${MASTER_LOG}"
    ((SUCCESSFUL++))
else
    echo -e "${RED}✗ phase1_product_name_rebrand.sh failed${NC}" | tee -a "${MASTER_LOG}"
    ((FAILED++))
fi
echo "" | tee -a "${MASTER_LOG}"

echo "[3/36] Executing: validate_phase1_product_name.sh" | tee -a "${MASTER_LOG}"
if bash "${SCRIPTS_DIR}/validate_phase1_product_name.sh" >> "${MASTER_LOG}" 2>&1; then
    echo -e "${GREEN}✓ validate_phase1_product_name.sh completed successfully${NC}" | tee -a "${MASTER_LOG}"
    ((SUCCESSFUL++))
else
    echo -e "${RED}✗ validate_phase1_product_name.sh failed${NC}" | tee -a "${MASTER_LOG}"
    ((FAILED++))
fi
echo "" | tee -a "${MASTER_LOG}"

echo "[4/36] Executing: phase1_cli_command_rename.sh" | tee -a "${MASTER_LOG}"
if bash "${SCRIPTS_DIR}/phase1_cli_command_rename.sh" >> "${MASTER_LOG}" 2>&1; then
    echo -e "${GREEN}✓ phase1_cli_command_rename.sh completed successfully${NC}" | tee -a "${MASTER_LOG}"
    ((SUCCESSFUL++))
else
    echo -e "${RED}✗ phase1_cli_command_rename.sh failed${NC}" | tee -a "${MASTER_LOG}"
    ((FAILED++))
fi
echo "" | tee -a "${MASTER_LOG}"

echo "[5/36] Executing: validate_phase1_cli_rename.sh" | tee -a "${MASTER_LOG}"
if bash "${SCRIPTS_DIR}/validate_phase1_cli_rename.sh" >> "${MASTER_LOG}" 2>&1; then
    echo -e "${GREEN}✓ validate_phase1_cli_rename.sh completed successfully${NC}" | tee -a "${MASTER_LOG}"
    ((SUCCESSFUL++))
else
    echo -e "${RED}✗ validate_phase1_cli_rename.sh failed${NC}" | tee -a "${MASTER_LOG}"
    ((FAILED++))
fi
echo "" | tee -a "${MASTER_LOG}"

echo "[6/36] Executing: phase2_directory_rename.sh" | tee -a "${MASTER_LOG}"
if bash "${SCRIPTS_DIR}/phase2_directory_rename.sh" >> "${MASTER_LOG}" 2>&1; then
    echo -e "${GREEN}✓ phase2_directory_rename.sh completed successfully${NC}" | tee -a "${MASTER_LOG}"
    ((SUCCESSFUL++))
else
    echo -e "${RED}✗ phase2_directory_rename.sh failed${NC}" | tee -a "${MASTER_LOG}"
    ((FAILED++))
fi
echo "" | tee -a "${MASTER_LOG}"

echo "[7/36] Executing: phase2_subdirectory_rename.sh" | tee -a "${MASTER_LOG}"
if bash "${SCRIPTS_DIR}/phase2_subdirectory_rename.sh" >> "${MASTER_LOG}" 2>&1; then
    echo -e "${GREEN}✓ phase2_subdirectory_rename.sh completed successfully${NC}" | tee -a "${MASTER_LOG}"
    ((SUCCESSFUL++))
else
    echo -e "${RED}✗ phase2_subdirectory_rename.sh failed${NC}" | tee -a "${MASTER_LOG}"
    ((FAILED++))
fi
echo "" | tee -a "${MASTER_LOG}"

echo "[8/36] Executing: phase3_python_imports.sh" | tee -a "${MASTER_LOG}"
if bash "${SCRIPTS_DIR}/phase3_python_imports.sh" >> "${MASTER_LOG}" 2>&1; then
    echo -e "${GREEN}✓ phase3_python_imports.sh completed successfully${NC}" | tee -a "${MASTER_LOG}"
    ((SUCCESSFUL++))
else
    echo -e "${RED}✗ phase3_python_imports.sh failed${NC}" | tee -a "${MASTER_LOG}"
    ((FAILED++))
fi
echo "" | tee -a "${MASTER_LOG}"

echo "[9/36] Executing: phase3_code_strings.sh" | tee -a "${MASTER_LOG}"
if bash "${SCRIPTS_DIR}/phase3_code_strings.sh" >> "${MASTER_LOG}" 2>&1; then
    echo -e "${GREEN}✓ phase3_code_strings.sh completed successfully${NC}" | tee -a "${MASTER_LOG}"
    ((SUCCESSFUL++))
else
    echo -e "${RED}✗ phase3_code_strings.sh failed${NC}" | tee -a "${MASTER_LOG}"
    ((FAILED++))
fi
echo "" | tee -a "${MASTER_LOG}"

echo "[10/36] Executing: phase3_class_names.sh" | tee -a "${MASTER_LOG}"
if bash "${SCRIPTS_DIR}/phase3_class_names.sh" >> "${MASTER_LOG}" 2>&1; then
    echo -e "${GREEN}✓ phase3_class_names.sh completed successfully${NC}" | tee -a "${MASTER_LOG}"
    ((SUCCESSFUL++))
else
    echo -e "${RED}✗ phase3_class_names.sh failed${NC}" | tee -a "${MASTER_LOG}"
    ((FAILED++))
fi
echo "" | tee -a "${MASTER_LOG}"

echo "[11/36] Executing: phase4_readme.sh" | tee -a "${MASTER_LOG}"
if bash "${SCRIPTS_DIR}/phase4_readme.sh" >> "${MASTER_LOG}" 2>&1; then
    echo -e "${GREEN}✓ phase4_readme.sh completed successfully${NC}" | tee -a "${MASTER_LOG}"
    ((SUCCESSFUL++))
else
    echo -e "${RED}✗ phase4_readme.sh failed${NC}" | tee -a "${MASTER_LOG}"
    ((FAILED++))
fi
echo "" | tee -a "${MASTER_LOG}"

echo "[12/36] Executing: phase4_api_docs.sh" | tee -a "${MASTER_LOG}"
if bash "${SCRIPTS_DIR}/phase4_api_docs.sh" >> "${MASTER_LOG}" 2>&1; then
    echo -e "${GREEN}✓ phase4_api_docs.sh completed successfully${NC}" | tee -a "${MASTER_LOG}"
    ((SUCCESSFUL++))
else
    echo -e "${RED}✗ phase4_api_docs.sh failed${NC}" | tee -a "${MASTER_LOG}"
    ((FAILED++))
fi
echo "" | tee -a "${MASTER_LOG}"

echo "[13/36] Executing: phase4_code_comments.sh" | tee -a "${MASTER_LOG}"
if bash "${SCRIPTS_DIR}/phase4_code_comments.sh" >> "${MASTER_LOG}" 2>&1; then
    echo -e "${GREEN}✓ phase4_code_comments.sh completed successfully${NC}" | tee -a "${MASTER_LOG}"
    ((SUCCESSFUL++))
else
    echo -e "${RED}✗ phase4_code_comments.sh failed${NC}" | tee -a "${MASTER_LOG}"
    ((FAILED++))
fi
echo "" | tee -a "${MASTER_LOG}"

echo "[14/36] Executing: phase5_homepage.sh" | tee -a "${MASTER_LOG}"
if bash "${SCRIPTS_DIR}/phase5_homepage.sh" >> "${MASTER_LOG}" 2>&1; then
    echo -e "${GREEN}✓ phase5_homepage.sh completed successfully${NC}" | tee -a "${MASTER_LOG}"
    ((SUCCESSFUL++))
else
    echo -e "${RED}✗ phase5_homepage.sh failed${NC}" | tee -a "${MASTER_LOG}"
    ((FAILED++))
fi
echo "" | tee -a "${MASTER_LOG}"

echo "[15/36] Executing: phase5_seo.sh" | tee -a "${MASTER_LOG}"
if bash "${SCRIPTS_DIR}/phase5_seo.sh" >> "${MASTER_LOG}" 2>&1; then
    echo -e "${GREEN}✓ phase5_seo.sh completed successfully${NC}" | tee -a "${MASTER_LOG}"
    ((SUCCESSFUL++))
else
    echo -e "${RED}✗ phase5_seo.sh failed${NC}" | tee -a "${MASTER_LOG}"
    ((FAILED++))
fi
echo "" | tee -a "${MASTER_LOG}"

echo "[16/36] Executing: phase5_trademark_symbol.sh" | tee -a "${MASTER_LOG}"
if bash "${SCRIPTS_DIR}/phase5_trademark_symbol.sh" >> "${MASTER_LOG}" 2>&1; then
    echo -e "${GREEN}✓ phase5_trademark_symbol.sh completed successfully${NC}" | tee -a "${MASTER_LOG}"
    ((SUCCESSFUL++))
else
    echo -e "${RED}✗ phase5_trademark_symbol.sh failed${NC}" | tee -a "${MASTER_LOG}"
    ((FAILED++))
fi
echo "" | tee -a "${MASTER_LOG}"

echo "[17/36] Executing: using_lets_encrypt.sh" | tee -a "${MASTER_LOG}"
if bash "${SCRIPTS_DIR}/using_lets_encrypt.sh" >> "${MASTER_LOG}" 2>&1; then
    echo -e "${GREEN}✓ using_lets_encrypt.sh completed successfully${NC}" | tee -a "${MASTER_LOG}"
    ((SUCCESSFUL++))
else
    echo -e "${RED}✗ using_lets_encrypt.sh failed${NC}" | tee -a "${MASTER_LOG}"
    ((FAILED++))
fi
echo "" | tee -a "${MASTER_LOG}"

echo "[18/36] Executing: phase6_redirects.sh" | tee -a "${MASTER_LOG}"
if bash "${SCRIPTS_DIR}/phase6_redirects.sh" >> "${MASTER_LOG}" 2>&1; then
    echo -e "${GREEN}✓ phase6_redirects.sh completed successfully${NC}" | tee -a "${MASTER_LOG}"
    ((SUCCESSFUL++))
else
    echo -e "${RED}✗ phase6_redirects.sh failed${NC}" | tee -a "${MASTER_LOG}"
    ((FAILED++))
fi
echo "" | tee -a "${MASTER_LOG}"

echo "[19/36] Executing: phase7_database_tables.sh" | tee -a "${MASTER_LOG}"
if bash "${SCRIPTS_DIR}/phase7_database_tables.sh" >> "${MASTER_LOG}" 2>&1; then
    echo -e "${GREEN}✓ phase7_database_tables.sh completed successfully${NC}" | tee -a "${MASTER_LOG}"
    ((SUCCESSFUL++))
else
    echo -e "${RED}✗ phase7_database_tables.sh failed${NC}" | tee -a "${MASTER_LOG}"
    ((FAILED++))
fi
echo "" | tee -a "${MASTER_LOG}"

echo "[20/36] Executing: phase7_database_columns.sh" | tee -a "${MASTER_LOG}"
if bash "${SCRIPTS_DIR}/phase7_database_columns.sh" >> "${MASTER_LOG}" 2>&1; then
    echo -e "${GREEN}✓ phase7_database_columns.sh completed successfully${NC}" | tee -a "${MASTER_LOG}"
    ((SUCCESSFUL++))
else
    echo -e "${RED}✗ phase7_database_columns.sh failed${NC}" | tee -a "${MASTER_LOG}"
    ((FAILED++))
fi
echo "" | tee -a "${MASTER_LOG}"

echo "[21/36] Executing: phase8_package_json.sh" | tee -a "${MASTER_LOG}"
if bash "${SCRIPTS_DIR}/phase8_package_json.sh" >> "${MASTER_LOG}" 2>&1; then
    echo -e "${GREEN}✓ phase8_package_json.sh completed successfully${NC}" | tee -a "${MASTER_LOG}"
    ((SUCCESSFUL++))
else
    echo -e "${RED}✗ phase8_package_json.sh failed${NC}" | tee -a "${MASTER_LOG}"
    ((FAILED++))
fi
echo "" | tee -a "${MASTER_LOG}"

echo "[22/36] Executing: phase8_python_package.sh" | tee -a "${MASTER_LOG}"
if bash "${SCRIPTS_DIR}/phase8_python_package.sh" >> "${MASTER_LOG}" 2>&1; then
    echo -e "${GREEN}✓ phase8_python_package.sh completed successfully${NC}" | tee -a "${MASTER_LOG}"
    ((SUCCESSFUL++))
else
    echo -e "${RED}✗ phase8_python_package.sh failed${NC}" | tee -a "${MASTER_LOG}"
    ((FAILED++))
fi
echo "" | tee -a "${MASTER_LOG}"

echo "[23/36] Executing: phase8_npm_config.sh" | tee -a "${MASTER_LOG}"
if bash "${SCRIPTS_DIR}/phase8_npm_config.sh" >> "${MASTER_LOG}" 2>&1; then
    echo -e "${GREEN}✓ phase8_npm_config.sh completed successfully${NC}" | tee -a "${MASTER_LOG}"
    ((SUCCESSFUL++))
else
    echo -e "${RED}✗ phase8_npm_config.sh failed${NC}" | tee -a "${MASTER_LOG}"
    ((FAILED++))
fi
echo "" | tee -a "${MASTER_LOG}"

echo "[24/36] Executing: phase10_trademark_notices.sh" | tee -a "${MASTER_LOG}"
if bash "${SCRIPTS_DIR}/phase10_trademark_notices.sh" >> "${MASTER_LOG}" 2>&1; then
    echo -e "${GREEN}✓ phase10_trademark_notices.sh completed successfully${NC}" | tee -a "${MASTER_LOG}"
    ((SUCCESSFUL++))
else
    echo -e "${RED}✗ phase10_trademark_notices.sh failed${NC}" | tee -a "${MASTER_LOG}"
    ((FAILED++))
fi
echo "" | tee -a "${MASTER_LOG}"

echo "[25/36] Executing: phase10_license.sh" | tee -a "${MASTER_LOG}"
if bash "${SCRIPTS_DIR}/phase10_license.sh" >> "${MASTER_LOG}" 2>&1; then
    echo -e "${GREEN}✓ phase10_license.sh completed successfully${NC}" | tee -a "${MASTER_LOG}"
    ((SUCCESSFUL++))
else
    echo -e "${RED}✗ phase10_license.sh failed${NC}" | tee -a "${MASTER_LOG}"
    ((FAILED++))
fi
echo "" | tee -a "${MASTER_LOG}"

echo "[26/36] Executing: phase10_legal_footer.sh" | tee -a "${MASTER_LOG}"
if bash "${SCRIPTS_DIR}/phase10_legal_footer.sh" >> "${MASTER_LOG}" 2>&1; then
    echo -e "${GREEN}✓ phase10_legal_footer.sh completed successfully${NC}" | tee -a "${MASTER_LOG}"
    ((SUCCESSFUL++))
else
    echo -e "${RED}✗ phase10_legal_footer.sh failed${NC}" | tee -a "${MASTER_LOG}"
    ((FAILED++))
fi
echo "" | tee -a "${MASTER_LOG}"

echo "[27/36] Executing: phase11_marketing.sh" | tee -a "${MASTER_LOG}"
if bash "${SCRIPTS_DIR}/phase11_marketing.sh" >> "${MASTER_LOG}" 2>&1; then
    echo -e "${GREEN}✓ phase11_marketing.sh completed successfully${NC}" | tee -a "${MASTER_LOG}"
    ((SUCCESSFUL++))
else
    echo -e "${RED}✗ phase11_marketing.sh failed${NC}" | tee -a "${MASTER_LOG}"
    ((FAILED++))
fi
echo "" | tee -a "${MASTER_LOG}"

echo "[28/36] Executing: phase11_presentations.sh" | tee -a "${MASTER_LOG}"
if bash "${SCRIPTS_DIR}/phase11_presentations.sh" >> "${MASTER_LOG}" 2>&1; then
    echo -e "${GREEN}✓ phase11_presentations.sh completed successfully${NC}" | tee -a "${MASTER_LOG}"
    ((SUCCESSFUL++))
else
    echo -e "${RED}✗ phase11_presentations.sh failed${NC}" | tee -a "${MASTER_LOG}"
    ((FAILED++))
fi
echo "" | tee -a "${MASTER_LOG}"

echo "[29/36] Executing: phase12_migration_guide.sh" | tee -a "${MASTER_LOG}"
if bash "${SCRIPTS_DIR}/phase12_migration_guide.sh" >> "${MASTER_LOG}" 2>&1; then
    echo -e "${GREEN}✓ phase12_migration_guide.sh completed successfully${NC}" | tee -a "${MASTER_LOG}"
    ((SUCCESSFUL++))
else
    echo -e "${RED}✗ phase12_migration_guide.sh failed${NC}" | tee -a "${MASTER_LOG}"
    ((FAILED++))
fi
echo "" | tee -a "${MASTER_LOG}"

echo "[30/36] Executing: old_still_works.sh" | tee -a "${MASTER_LOG}"
if bash "${SCRIPTS_DIR}/old_still_works.sh" >> "${MASTER_LOG}" 2>&1; then
    echo -e "${GREEN}✓ old_still_works.sh completed successfully${NC}" | tee -a "${MASTER_LOG}"
    ((SUCCESSFUL++))
else
    echo -e "${RED}✗ old_still_works.sh failed${NC}" | tee -a "${MASTER_LOG}"
    ((FAILED++))
fi
echo "" | tee -a "${MASTER_LOG}"

echo "[31/36] Executing: validate_all_phases.sh" | tee -a "${MASTER_LOG}"
if bash "${SCRIPTS_DIR}/validate_all_phases.sh" >> "${MASTER_LOG}" 2>&1; then
    echo -e "${GREEN}✓ validate_all_phases.sh completed successfully${NC}" | tee -a "${MASTER_LOG}"
    ((SUCCESSFUL++))
else
    echo -e "${RED}✗ validate_all_phases.sh failed${NC}" | tee -a "${MASTER_LOG}"
    ((FAILED++))
fi
echo "" | tee -a "${MASTER_LOG}"

echo "[32/36] Executing: rollback_all_changes.sh" | tee -a "${MASTER_LOG}"
if bash "${SCRIPTS_DIR}/rollback_all_changes.sh" >> "${MASTER_LOG}" 2>&1; then
    echo -e "${GREEN}✓ rollback_all_changes.sh completed successfully${NC}" | tee -a "${MASTER_LOG}"
    ((SUCCESSFUL++))
else
    echo -e "${RED}✗ rollback_all_changes.sh failed${NC}" | tee -a "${MASTER_LOG}"
    ((FAILED++))
fi
echo "" | tee -a "${MASTER_LOG}"

echo "[33/36] Executing: EXECUTE_REBRANDING.sh" | tee -a "${MASTER_LOG}"
if bash "${SCRIPTS_DIR}/EXECUTE_REBRANDING.sh" >> "${MASTER_LOG}" 2>&1; then
    echo -e "${GREEN}✓ EXECUTE_REBRANDING.sh completed successfully${NC}" | tee -a "${MASTER_LOG}"
    ((SUCCESSFUL++))
else
    echo -e "${RED}✗ EXECUTE_REBRANDING.sh failed${NC}" | tee -a "${MASTER_LOG}"
    ((FAILED++))
fi
echo "" | tee -a "${MASTER_LOG}"

echo "[34/36] Executing: 1_navigate_to_paragroupai.sh" | tee -a "${MASTER_LOG}"
if bash "${SCRIPTS_DIR}/1_navigate_to_paragroupai.sh" >> "${MASTER_LOG}" 2>&1; then
    echo -e "${GREEN}✓ 1_navigate_to_paragroupai.sh completed successfully${NC}" | tee -a "${MASTER_LOG}"
    ((SUCCESSFUL++))
else
    echo -e "${RED}✗ 1_navigate_to_paragroupai.sh failed${NC}" | tee -a "${MASTER_LOG}"
    ((FAILED++))
fi
echo "" | tee -a "${MASTER_LOG}"

echo "[35/36] Executing: execute_specific_phase.sh" | tee -a "${MASTER_LOG}"
if bash "${SCRIPTS_DIR}/execute_specific_phase.sh" >> "${MASTER_LOG}" 2>&1; then
    echo -e "${GREEN}✓ execute_specific_phase.sh completed successfully${NC}" | tee -a "${MASTER_LOG}"
    ((SUCCESSFUL++))
else
    echo -e "${RED}✗ execute_specific_phase.sh failed${NC}" | tee -a "${MASTER_LOG}"
    ((FAILED++))
fi
echo "" | tee -a "${MASTER_LOG}"

echo "[36/36] Executing: emergency_rollback.sh" | tee -a "${MASTER_LOG}"
if bash "${SCRIPTS_DIR}/emergency_rollback.sh" >> "${MASTER_LOG}" 2>&1; then
    echo -e "${GREEN}✓ emergency_rollback.sh completed successfully${NC}" | tee -a "${MASTER_LOG}"
    ((SUCCESSFUL++))
else
    echo -e "${RED}✗ emergency_rollback.sh failed${NC}" | tee -a "${MASTER_LOG}"
    ((FAILED++))
fi
echo "" | tee -a "${MASTER_LOG}"


echo "" | tee -a "${MASTER_LOG}"
echo "================================================================================" | tee -a "${MASTER_LOG}"
echo "Execution Summary" | tee -a "${MASTER_LOG}"
echo "================================================================================" | tee -a "${MASTER_LOG}"
echo "Total Scripts: ${TOTAL_SCRIPTS}" | tee -a "${MASTER_LOG}"
echo "Successful: ${SUCCESSFUL}" | tee -a "${MASTER_LOG}"
echo "Failed: ${FAILED}" | tee -a "${MASTER_LOG}"
echo "End Time: $(date)" | tee -a "${MASTER_LOG}"
echo "" | tee -a "${MASTER_LOG}"

if [ "${FAILED}" -eq 0 ]; then
    echo -e "${GREEN}✓ All scripts executed successfully!${NC}" | tee -a "${MASTER_LOG}"
    echo "" | tee -a "${MASTER_LOG}"
    echo "Para Group AI Orchestrator® rebranding complete!" | tee -a "${MASTER_LOG}"
    exit 0
else
    echo -e "${RED}✗ ${FAILED} script(s) failed. Check logs for details.${NC}" | tee -a "${MASTER_LOG}"
    exit 1
fi
