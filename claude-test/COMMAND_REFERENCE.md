# ULTRATHINK Command Reference

## Two Independent Instances

| Instance | Location | Command | Purpose |
|----------|----------|---------|---------|
| **TestPrompt** | `/home/user01/claude-test/TestPrompt` | `uc` or `ultrathinkc` | Original, stable version |
| **ClaudePrompt** | `/home/user01/claude-test/ClaudePrompt` | `cpp` | Experimental, upgradeable version |

## Commands

### TestPrompt (Original)
```bash
cd /home/user01/claude-test/TestPrompt
./ultrathinkc "prompt" -v
# OR use alias (if configured)
uc "prompt" -v
```

### ClaudePrompt (New)
```bash
cd /home/user01/claude-test/ClaudePrompt
./cpp "prompt" -v
```

## Quick Navigation

```bash
# Navigate to TestPrompt
cd /home/user01/claude-test/TestPrompt

# Navigate to ClaudePrompt
cd /home/user01/claude-test/ClaudePrompt
```

## Verification

Check isolation between both instances:
```bash
/home/user01/claude-test/verify_isolation.sh
```

Expected output: 6-7 tests passing

## Backup Locations

- **Compressed**: `BACKUPS/TestPrompt_backup_TIMESTAMP.tar.gz`
- **Uncompressed**: `TestPrompt_BACKUP_SAFE/`

## Restore TestPrompt (If Needed)

```bash
cd /home/user01/claude-test
rm -rf TestPrompt
cp -r TestPrompt_BACKUP_SAFE TestPrompt
```

## Features

Both instances have:
- 8-layer guardrail system
- Multi-agent orchestration (up to 500 agents)
- 200K token context window
- 99% confidence targeting
- Comprehensive validation
- Verbose mode (`-v` flag)

## Isolation Benefits

✅ Test upgrades in ClaudePrompt without risking TestPrompt
✅ Run both simultaneously for A/B testing
✅ Easy rollback if ClaudePrompt has issues
✅ Gradual migration path for proven enhancements

Created: 2025-11-11
