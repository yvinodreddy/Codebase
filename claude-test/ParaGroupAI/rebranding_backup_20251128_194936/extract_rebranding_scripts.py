#!/usr/bin/env python3
"""
Script Extractor for Para Group Rebranding Execution Plan
Extracts all embedded bash scripts from the markdown execution plan
and creates individual executable script files.
"""

import os
import re
from pathlib import Path

def extract_scripts():
    """Extract all bash scripts from the execution plan markdown file."""

    # Paths
    plan_file = '/home/user01/claude-test/ClaudePrompt/PARA_GROUP_REBRANDING_EXECUTION_PLAN.md'
    scripts_dir = '/home/user01/claude-test/ClaudePrompt/rebranding_scripts'

    # Create scripts directory if it doesn't exist
    os.makedirs(scripts_dir, exist_ok=True)

    # Read the execution plan
    with open(plan_file, 'r') as f:
        content = f.read()

    # Pattern to match bash code blocks with optional filename comments
    # Looks for: ```bash followed by script content followed by ```
    pattern = r'```bash\n(.*?)\n```'

    scripts_found = []

    # Find all bash code blocks
    matches = re.finditer(pattern, content, re.DOTALL)

    for idx, match in enumerate(matches, 1):
        script_content = match.group(1)

        # Skip empty scripts
        if not script_content.strip():
            continue

        # Try to extract filename from first line if it's a comment
        lines = script_content.split('\n')
        script_name = None
        script_body = script_content

        # Check first few lines for filename patterns
        for line in lines[:5]:
            line = line.strip()
            # Look for patterns like: # filename.sh or # EXECUTE_REBRANDING.sh
            if line.startswith('#') and '.sh' in line:
                # Extract filename
                filename_match = re.search(r'(\w+\.sh)', line)
                if filename_match:
                    script_name = filename_match.group(1)
                    break

        # If no filename found, generate one
        if not script_name:
            # Try to identify script purpose from first comment
            first_comment = None
            for line in lines:
                if line.strip().startswith('#') and not line.strip().startswith('#!'):
                    first_comment = line.strip('# ')
                    break

            if first_comment and 'CHANGE' in first_comment:
                # Extract CHANGE number
                change_match = re.search(r'CHANGE\s+(\d+\.\d+)', first_comment)
                if change_match:
                    script_name = f"change_{change_match.group(1).replace('.', '_')}.sh"
                else:
                    script_name = f"script_{idx:03d}.sh"
            elif first_comment:
                # Use first few words of comment
                name_part = '_'.join(first_comment.lower().split()[:4])
                name_part = re.sub(r'[^a-z0-9_]', '', name_part)
                script_name = f"{name_part}.sh"
            else:
                script_name = f"script_{idx:03d}.sh"

        # Save script
        script_path = os.path.join(scripts_dir, script_name)

        # Add shebang if not present
        if not script_body.startswith('#!'):
            script_body = '#!/bin/bash\n\n' + script_body

        with open(script_path, 'w') as f:
            f.write(script_body)

        # Make executable
        os.chmod(script_path, 0o755)

        scripts_found.append(script_name)
        print(f"✓ Extracted: {script_name}")

    print(f"\n{'='*80}")
    print(f"Extraction Complete!")
    print(f"{'='*80}")
    print(f"Total scripts extracted: {len(scripts_found)}")
    print(f"Scripts location: {scripts_dir}")
    print(f"\nAll scripts are executable (chmod 755)")

    # Create master execution script
    create_master_script(scripts_dir, scripts_found)

    return scripts_found

def create_master_script(scripts_dir, script_list):
    """Create a master execution script that runs all scripts in order."""

    master_script = f"""#!/bin/bash
#
# Master Execution Script for Para Group AI Orchestrator® Rebranding
# This script executes all rebranding changes in the correct order
#
# Generated: $(date)
# Backup Branch: rebranding-backup-$(date +%Y%m%d_%H%M%S) (already created)
#

set -e  # Exit on any error

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
SCRIPTS_DIR="{scripts_dir}"
LOG_DIR="{scripts_dir}/logs"
MASTER_LOG="${{LOG_DIR}}/MASTER_EXECUTION_${{TIMESTAMP}}.log"

# Create log directory
mkdir -p "${{LOG_DIR}}"

# Colors for output
RED='\\033[0;31m'
GREEN='\\033[0;32m'
YELLOW='\\033[1;33m'
NC='\\033[0m' # No Color

echo "{'='*80}" | tee -a "${{MASTER_LOG}}"
echo "Para Group AI Orchestrator® Rebranding Execution" | tee -a "${{MASTER_LOG}}"
echo "{'='*80}" | tee -a "${{MASTER_LOG}}"
echo "Start Time: $(date)" | tee -a "${{MASTER_LOG}}"
echo "Backup Branch: Available on GitHub" | tee -a "${{MASTER_LOG}}"
echo "" | tee -a "${{MASTER_LOG}}"

# Counter for tracking
TOTAL_SCRIPTS={len(script_list)}
SUCCESSFUL=0
FAILED=0

# Execute each script
{_generate_script_execution_commands(script_list)}

echo "" | tee -a "${{MASTER_LOG}}"
echo "{'='*80}" | tee -a "${{MASTER_LOG}}"
echo "Execution Summary" | tee -a "${{MASTER_LOG}}"
echo "{'='*80}" | tee -a "${{MASTER_LOG}}"
echo "Total Scripts: ${{TOTAL_SCRIPTS}}" | tee -a "${{MASTER_LOG}}"
echo "Successful: ${{SUCCESSFUL}}" | tee -a "${{MASTER_LOG}}"
echo "Failed: ${{FAILED}}" | tee -a "${{MASTER_LOG}}"
echo "End Time: $(date)" | tee -a "${{MASTER_LOG}}"
echo "" | tee -a "${{MASTER_LOG}}"

if [ "${{FAILED}}" -eq 0 ]; then
    echo -e "${{GREEN}}✓ All scripts executed successfully!${{NC}}" | tee -a "${{MASTER_LOG}}"
    echo "" | tee -a "${{MASTER_LOG}}"
    echo "Para Group AI Orchestrator® rebranding complete!" | tee -a "${{MASTER_LOG}}"
    exit 0
else
    echo -e "${{RED}}✗ ${{FAILED}} script(s) failed. Check logs for details.${{NC}}" | tee -a "${{MASTER_LOG}}"
    exit 1
fi
"""

    master_path = f"{scripts_dir}/EXECUTE_REBRANDING.sh"
    with open(master_path, 'w') as f:
        f.write(master_script)

    os.chmod(master_path, 0o755)
    print(f"\n✓ Created master execution script: EXECUTE_REBRANDING.sh")
    print(f"\n{'='*80}")
    print(f"READY TO EXECUTE!")
    print(f"{'='*80}")
    print(f"\nSingle command to execute all changes:")
    print(f"\n    bash {master_path}\n")
    print(f"This will execute all {len(script_list)} rebranding scripts in order.")
    print(f"Logs will be saved to: {scripts_dir}/logs/")
    print(f"{'='*80}\n")

def _generate_script_execution_commands(script_list):
    """Generate the script execution commands for master script."""
    commands = []
    for idx, script in enumerate(script_list, 1):
        commands.append(f"""
echo "[{idx}/{len(script_list)}] Executing: {script}" | tee -a "${{MASTER_LOG}}"
if bash "${{SCRIPTS_DIR}}/{script}" >> "${{MASTER_LOG}}" 2>&1; then
    echo -e "${{GREEN}}✓ {script} completed successfully${{NC}}" | tee -a "${{MASTER_LOG}}"
    ((SUCCESSFUL++))
else
    echo -e "${{RED}}✗ {script} failed${{NC}}" | tee -a "${{MASTER_LOG}}"
    ((FAILED++))
fi
echo "" | tee -a "${{MASTER_LOG}}"
""")
    return ''.join(commands)

if __name__ == '__main__':
    try:
        scripts = extract_scripts()
        print("\nScript extraction completed successfully!")
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
