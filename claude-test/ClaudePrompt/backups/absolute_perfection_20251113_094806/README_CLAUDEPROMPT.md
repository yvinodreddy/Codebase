# ClaudePrompt - Isolated ULTRATHINK Instance

This is a **completely isolated** copy of the ULTRATHINK framework.

## Key Differences from TestPrompt

- **Command**: `cpp` (instead of `uc` or `ultrathinkc`)
- **Location**: `/home/user01/claude-test/ClaudePrompt`
- **Isolation**: 100% independent from TestPrompt
- **Purpose**: Experimental enhancements and upgrades

## Usage

Basic command:
```bash
cpp "your prompt here" -v
```

With full path:
```bash
/home/user01/claude-test/ClaudePrompt/cpp "prompt" -v
```

## Testing

Run verification:
```bash
cd /home/user01/claude-test
./verify_isolation.sh
```

## Upgrading

This folder can be upgraded independently without affecting TestPrompt.

To upgrade:
1. Make changes in ClaudePrompt
2. Test thoroughly using `cpp "test" -v`
3. Run isolation verification
4. If successful, optionally merge back to TestPrompt

## Backup

Original TestPrompt backed up at:
- `/home/user01/claude-test/BACKUPS/TestPrompt_backup_*.tar.gz`
- `/home/user01/claude-test/TestPrompt_BACKUP_SAFE/`

## Isolation Verified

✅ No TestPrompt references in code
✅ Separate command (`cpp` vs `uc`)
✅ Separate log directories
✅ Can run simultaneously with TestPrompt
✅ No cross-contamination in output

Created: 2025-11-11
Status: Production-Ready
