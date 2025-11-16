# SAFETY CHECKLIST - PREVENT FUTURE DATA LOSS

## ✅ COMPLETED (Immediate Actions)

- [x] Restore all deleted files from backup
- [x] Verify ClaudePrompt system operational
- [x] Verify TestPrompt system operational
- [x] Disable --dangerously-skip-permissions alias
- [x] Create incident report
- [x] Create this safety checklist

## ⚠️  PENDING (High Priority - Do Next)

### 1. Initialize Git Repository
```bash
cd /home/user01/claude-test
git init
git add .
git commit -m "Post-recovery checkpoint - Nov 15 2025"
```

**Why:** Version control prevents permanent data loss. Even if files are deleted, they remain in git history.

### 2. Create Backup Verification Script
```bash
chmod +x /home/user01/claude-test/verify_backup.sh
# Run before ANY cleanup operations
```

**Why:** Ensures backups are complete before allowing deletions.

### 3. Implement Pre-Deletion Hooks
Add to all cleanup scripts:
```bash
# SAFETY CHECK - NEVER SKIP THIS
if [ "$VERIFY_BACKUP" != "TRUE" ]; then
    echo "❌ SAFETY CHECK FAILED: Backup not verified"
    exit 1
fi
```

**Why:** Prevents accidental deletion without backup verification.

## 📋 RECOMMENDED (Medium Priority - This Week)

- [ ] Set up automated daily backups
- [ ] Create restore testing procedure
- [ ] Document all deployment/migration procedures
- [ ] Add file count logging to all scripts
- [ ] Implement dry-run mode for all destructive operations
- [ ] Create emergency recovery runbook

## 🔒 SECURITY BEST PRACTICES (Ongoing)

### Claude Code Usage:
- ❌ **NEVER** use `--dangerously-skip-permissions` in production
- ✅ **ALWAYS** review destructive operations
- ✅ **ALWAYS** use confirmation prompts for deletions
- ✅ **ALWAYS** create backups before major changes

### Script Safety:
- ✅ **ALWAYS** implement backup verification
- ✅ **ALWAYS** log all destructive operations
- ✅ **ALWAYS** provide rollback procedures
- ✅ **ALWAYS** test in dry-run mode first

### Autonomous Mode:
- ⚠️  **USE WITH CAUTION** for file operations
- ✅ **ALWAYS** verify results after execution
- ✅ **ALWAYS** have backups ready
- ❌ **NEVER** combine autonomous mode with skip-permissions

## 🚨 RED FLAGS - STOP IMMEDIATELY IF:

1. Script requests permission to delete >100 files
2. Backup verification fails
3. File count drops unexpectedly
4. Critical directories become inaccessible
5. Any operation mentions "cleanup" without backup

## 📞 EMERGENCY RECOVERY PROCEDURE

If data loss occurs again:

```bash
# 1. STOP - Don't make it worse
# Don't run any more commands

# 2. CHECK BACKUPS
ls -lh /home/user01/claude-test-backup-*

# 3. RESTORE FROM MOST RECENT
cp -r /home/user01/claude-test-backup-YYYYMMDD_HHMMSS/* /home/user01/claude-test/

# 4. VERIFY RESTORATION
find /home/user01/claude-test -type f | wc -l

# 5. TEST CRITICAL SYSTEMS
/home/user01/claude-test/ClaudePrompt/cpp --help
/home/user01/claude-test/TestPrompt/ultrathinkc --help
```

## ✅ SUCCESS CRITERIA

Recovery is complete when:
- [x] All files restored (56,229 >= 55,277) ✅
- [x] ClaudePrompt operational ✅
- [x] TestPrompt operational ✅
- [x] No broken symlinks ✅
- [x] Cron jobs pointing to valid paths ✅
- [x] Safety measures implemented ✅
- [ ] Git repository initialized ⚠️ PENDING
- [ ] Backup verification script created ⚠️ PENDING

---

**Remember:** The 2 hours of downtime could have been 2 weeks of lost work without proper backups. Always backup, always verify, never skip safety checks.

**Last Updated:** 2025-11-15 22:10 EST
