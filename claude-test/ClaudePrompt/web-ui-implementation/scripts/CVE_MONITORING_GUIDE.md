# CVE Monitoring System - Complete Guide

## Overview

Automated vulnerability scanning and monitoring system that:
- Scans npm dependencies for known vulnerabilities
- Checks National Vulnerability Database (NVD)
- Generates detailed security reports
- Alerts on critical/high severity issues
- Tracks security posture over time

## Quick Start

```bash
# Run manual scan
./scripts/cve-monitor.sh

# Schedule weekly scans (Sunday 2 AM)
crontab -e
# Add: 0 2 * * 0 /full/path/to/scripts/cve-monitor.sh
```

## Components

### 1. cve-monitor.sh
Main scanning script that:
- Runs `npm audit` for dependency vulnerabilities
- Checks for outdated packages with `npm-check-updates`
- Scans source code for security anti-patterns
- Generates JSON reports
- Determines required actions based on severity

### 2. Reports Directory
Location: `security-reports/`

Generated files:
- `cve-report-YYYYMMDD_HHMMSS.json` - Summary report
- `npm-audit-YYYYMMDD_HHMMSS.json` - Full npm audit results
- `outdated-YYYYMMDD_HHMMSS.json` - Outdated package list

### 3. Severity Levels & Response Times

| Severity | Response Time | Action |
|----------|---------------|---------|
| Critical | 24 hours | Immediate fix required |
| High | 7 days | High priority fix |
| Moderate | 30 days | Standard fix schedule |
| Low | Next sprint | Review and fix if time permits |

## Manual Scan

```bash
cd /home/user01/claude-test/ClaudePrompt/web-ui-implementation
./scripts/cve-monitor.sh
```

Exit codes:
- `0` - No critical/high vulnerabilities
- `1` - High vulnerabilities found
- `2` - Critical vulnerabilities found

## Automated Scanning

### Option 1: Cron Job (Linux/Mac)

```bash
# Edit crontab
crontab -e

# Add this line for weekly scans (Sunday 2 AM)
0 2 * * 0 /home/user01/claude-test/ClaudePrompt/web-ui-implementation/scripts/cve-monitor.sh >> /var/log/cve-monitor.log 2>&1
```

### Option 2: GitHub Actions (CI/CD)

Create `.github/workflows/security-scan.yml`:

```yaml
name: Security Scan

on:
  schedule:
    - cron: '0 2 * * 0'  # Weekly Sunday 2 AM
  workflow_dispatch:  # Manual trigger

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: npm ci
      - run: ./scripts/cve-monitor.sh
      - name: Upload reports
        uses: actions/upload-artifact@v3
        with:
          name: security-reports
          path: security-reports/
```

## Interpreting Results

### Sample Output

```
================================
CVE MONITORING SCAN STARTED
================================
Date: Wed Nov 14 08:00:00 2025
Report: /path/to/security-reports/cve-report-20251114_080000.json

[1/4] Running npm audit...
  Critical: 0
  High:     2
  Moderate: 5
  Low:      8
  Total:    15

[2/4] Checking for outdated packages...
  Outdated packages: 12

[3/4] Security best practices check...
  Security issues found: 0

[4/4] Generating summary report...
  Report saved: /path/to/cve-report-20251114_080000.json

================================
SCAN COMPLETE
================================
⚠ HIGH VULNERABILITIES FOUND: 2
  ACTION REQUIRED: Fix within 7 days

Full report: /path/to/cve-report-20251114_080000.json
To fix issues: npm audit fix
To update packages: ncu -u && npm install
```

### JSON Report Format

```json
{
  "timestamp": "2025-11-14T08:00:00-05:00",
  "scan_type": "automated_weekly",
  "npm_audit": {
    "critical": 0,
    "high": 2,
    "moderate": 5,
    "low": 8,
    "total": 15
  },
  "outdated_packages": 12,
  "security_issues": 0,
  "reports": {
    "npm_audit": "security-reports/npm-audit-20251114_080000.json",
    "outdated": "security-reports/outdated-20251114_080000.json",
    "summary": "security-reports/cve-report-20251114_080000.json"
  }
}
```

## Fixing Vulnerabilities

### Automatic Fixes

```bash
# Try automatic fixes (safe updates)
npm audit fix

# Force automatic fixes (may break things)
npm audit fix --force
```

### Manual Fixes

1. Review the npm audit report:
```bash
npm audit
```

2. Update specific package:
```bash
npm update package-name
```

3. Update to specific version:
```bash
npm install package-name@version
```

4. If no fix available, consider:
   - Finding alternative package
   - Accepting the risk (document why)
   - Waiting for upstream fix

## Alerting Configuration

### Email Alerts

Edit `cve-monitor.sh` lines 230-232:

```bash
if [ "$CRITICAL" -gt 0 ] || [ "$HIGH" -gt 0 ]; then
    echo "Critical vulnerabilities found. See $REPORT_FILE" | \
      mail -s "Security Alert: CVE Scan" admin@example.com
fi
```

### Slack Alerts

Get webhook URL from Slack, then edit lines 234-238:

```bash
if [ "$CRITICAL" -gt 0 ] || [ "$HIGH" -gt 0 ]; then
    curl -X POST -H 'Content-type: application/json' \
      --data "{\"text\":\"🚨 Security Alert: $CRITICAL critical, $HIGH high vulnerabilities. Report: $REPORT_FILE\"}" \
      https://hooks.slack.com/services/YOUR/WEBHOOK/URL
fi
```

### Discord Webhooks

```bash
if [ "$CRITICAL" -gt 0 ] || [ "$HIGH" -gt 0 ]; then
    curl -X POST -H 'Content-type: application/json' \
      --data "{\"content\":\"🚨 Security Alert: $CRITICAL critical, $HIGH high vulnerabilities\"}" \
      https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/YOUR_WEBHOOK_TOKEN
fi
```

## Best Practices

1. **Run scans weekly** - Automated via cron/GitHub Actions
2. **Fix critical within 24 hours** - Drop everything if critical found
3. **Review reports monthly** - Track trends over time
4. **Keep dependencies updated** - Run `ncu -u && npm install` monthly
5. **Document exceptions** - If you can't fix, document why
6. **Monitor NVD** - Check https://nvd.nist.gov for new CVEs
7. **Subscribe to security advisories** - GitHub security alerts

## Troubleshooting

### Script fails with "jq: command not found"

Install jq:
```bash
# Ubuntu/Debian
sudo apt-get install jq

# Mac
brew install jq

# CentOS/RHEL
sudo yum install jq
```

### npm-check-updates not found

Install globally:
```bash
npm install -g npm-check-updates
```

### Permission denied

Make script executable:
```bash
chmod +x scripts/cve-monitor.sh
```

### Cron job not running

1. Check cron service: `sudo systemctl status cron`
2. Check logs: `grep CRON /var/log/syslog`
3. Use absolute paths in crontab
4. Redirect output to log file for debugging

## Integration with CI/CD

### Pre-commit Hook

Create `.husky/pre-commit`:
```bash
#!/bin/sh
npm audit --audit-level=critical
```

### Pre-push Hook

Create `.husky/pre-push`:
```bash
#!/bin/sh
./scripts/cve-monitor.sh
```

## Resources

- **NVD Database**: https://nvd.nist.gov
- **npm audit docs**: https://docs.npmjs.com/cli/v8/commands/npm-audit
- **OWASP Top 10**: https://owasp.org/www-project-top-ten/
- **Snyk Vulnerability DB**: https://snyk.io/vuln/
- **GitHub Security Advisories**: https://github.com/advisories

## Contact

For security issues, contact: security@yourcompany.com
