# Email Campaign System

Production-ready, configuration-based email campaign manager with automatic retry and rate limit handling.

## Features

✅ **Configuration-Based** - All settings in `config.json`, no code changes needed
✅ **Template System** - Separate HTML templates with variable substitution
✅ **Resume Capability** - Automatically skips already-sent emails
✅ **Rate Limit Handling** - Automatic reconnection and batch processing
✅ **Auto-Retry** - Optional script for hands-free campaign completion
✅ **Portable** - Uses relative paths, copy folder anywhere
✅ **Production-Ready** - Comprehensive logging and error handling

## Quick Start

### 1. Setup Your Campaign

```bash
cd campaign/
```

### 2. Configure SMTP Settings

Edit `config.json` and update:

```json
{
  "smtp": {
    "server": "smtp.your-provider.com",
    "port": 587,
    "sender_email": "your-email@company.com",
    "sender_password": "your-password"
  }
}
```

### 3. Prepare Candidates List

Edit `data/candidates.csv`:

```csv
Name,Email
John Doe,john.doe@example.com
Jane Smith,jane.smith@example.com
```

### 4. Customize Email Template

Edit `templates/assessment_invitation.html` to match your needs.

Update template variables in `config.json`:

```json
{
  "template_variables": {
    "ORGANIZATION": "Your Company Name",
    "EXAM_URL": "https://your-exam-url.com",
    "END_DATE": "December 31, 2025",
    "CONTACT_EMAIL": "contact@company.com"
  }
}
```

### 5. Test Your Setup

Send a test email:

```bash
python3 send_campaign.py --test-email your-email@example.com
```

### 6. Run Campaign

Send to all candidates:

```bash
python3 send_campaign.py --send-all
```

Or use auto-retry for hands-free operation:

```bash
./auto_retry.sh &
```

## File Structure

```
campaign/
├── send_campaign.py              # Main campaign script
├── auto_retry.sh                 # Auto-retry wrapper script
├── config.json                   # Configuration file
├── README.md                     # This file
├── templates/
│   └── assessment_invitation.html  # Email template
├── data/
│   ├── candidates.csv            # List of candidates
│   └── sent_emails.txt           # Tracking file (auto-generated)
└── logs/
    ├── campaign.log              # Campaign execution log
    └── auto_retry.log            # Auto-retry log
```

## Usage Guide

### Command Line Options

```bash
# Send test email
python3 send_campaign.py --test-email EMAIL

# Run campaign (sends to all pending candidates)
python3 send_campaign.py --send-all

# Dry run (validate configuration without sending)
python3 send_campaign.py --dry-run
```

### Template Variables

Available variables in HTML templates:

| Variable | Description | Example |
|----------|-------------|---------|
| `{{FIRST_NAME}}` | Candidate's first name | John |
| `{{FULL_NAME}}` | Candidate's full name | John Doe |
| `{{EMAIL}}` | Candidate's email | john@example.com |
| `{{ORGANIZATION}}` | Company name (from config) | Acme Corp |
| `{{EXAM_URL}}` | Assessment URL (from config) | https://exam.com |
| `{{END_DATE}}` | Deadline (from config) | Dec 31, 2025 |
| `{{CONTACT_EMAIL}}` | Contact email (from config) | hr@acme.com |
| `{{YOUR_TITLE}}` | Your title (from config) | HR Manager |

### Configuration Reference

#### SMTP Settings

```json
{
  "smtp": {
    "server": "smtp.hostinger.com",    // SMTP server address
    "port": 587,                        // Port (587 for TLS, 465 for SSL)
    "use_tls": true,                    // Use TLS encryption
    "sender_email": "email@domain.com", // From address
    "sender_password": "password",      // SMTP password
    "sender_name": "Company Name"       // From name
  }
}
```

#### Campaign Settings

```json
{
  "campaign": {
    "subject": "Email Subject",                        // Email subject line
    "template_file": "templates/your_template.html",   // Path to template
    "candidates_file": "data/candidates.csv",          // Path to candidates
    "sent_emails_file": "data/sent_emails.txt",        // Tracking file
    "log_file": "logs/campaign.log"                    // Log file
  }
}
```

#### Rate Limiting

```json
{
  "sending": {
    "emails_per_batch": 10,           // Emails before pause
    "delay_between_emails": 3,        // Seconds between emails
    "delay_between_batches": 60,      // Seconds between batches
    "max_consecutive_failures": 2     // Failures before reconnect
  }
}
```

## How It Works

### Resume Capability

The system tracks sent emails in `data/sent_emails.txt`. If the campaign is interrupted:

1. Already-sent emails are automatically skipped
2. Campaign resumes from where it left off
3. No duplicate emails are sent

### Rate Limit Handling

When rate limits are hit:

1. Script automatically reconnects to SMTP server
2. Continues sending remaining emails
3. Uses configurable delays between batches

### Auto-Retry Script

The `auto_retry.sh` script:

1. Runs campaign every 15 minutes
2. Stops when all emails are sent
3. Logs all attempts
4. Creates completion marker file

## Common Workflows

### Starting a New Campaign

```bash
# 1. Clear previous tracking (if reusing folder)
> data/sent_emails.txt

# 2. Update config.json with new settings
# 3. Update data/candidates.csv with new list
# 4. Customize templates/assessment_invitation.html
# 5. Test
python3 send_campaign.py --test-email your@email.com

# 6. Run
python3 send_campaign.py --send-all
```

### Handling Rate Limits

If you hit rate limits mid-campaign:

**Option 1: Wait and Retry Manually**
```bash
# Wait for rate limit to reset (check provider's limits)
# Then run again - already-sent emails will be skipped
python3 send_campaign.py --send-all
```

**Option 2: Use Auto-Retry**
```bash
# Will automatically retry every 15 minutes
./auto_retry.sh &

# Monitor progress
tail -f logs/auto_retry.log
```

### Changing Email Template

1. Edit `templates/assessment_invitation.html`
2. If you need to resend to everyone:
   ```bash
   # Clear tracking file
   > data/sent_emails.txt

   # Run campaign again
   python3 send_campaign.py --send-all
   ```

### Using Different SMTP Providers

#### Hostinger
```json
{
  "smtp": {
    "server": "smtp.hostinger.com",
    "port": 587,
    "use_tls": true
  }
}
```

#### Gmail
```json
{
  "smtp": {
    "server": "smtp.gmail.com",
    "port": 587,
    "use_tls": true
  }
}
```

#### SendGrid
```json
{
  "smtp": {
    "server": "smtp.sendgrid.net",
    "port": 587,
    "use_tls": true,
    "sender_email": "apikey",
    "sender_password": "YOUR_SENDGRID_API_KEY"
  }
}
```

## Troubleshooting

### Connection Timeout

**Issue**: SMTP connection times out

**Solution**:
- Try different port (587 for TLS, 465 for SSL)
- Check firewall settings
- Verify SMTP server address

### Authentication Failed

**Issue**: Login failed

**Solution**:
- Verify email and password
- Check if 2FA is enabled (use app password)
- Ensure SMTP access is enabled for your account

### Rate Limit Exceeded

**Issue**: "Ratelimit exceeded" errors

**Solution**:
- Use `auto_retry.sh` to automatically retry
- Increase delays in config.json
- Check your provider's sending limits

### Template Not Found

**Issue**: "Template file not found" error

**Solution**:
- Verify path in `config.json`
- Ensure template exists in `templates/` folder
- Check file permissions

### No Candidates to Send

**Issue**: "Already sent: X, Pending: 0"

**Solution**:
- Check `data/candidates.csv` has valid entries
- If resending, clear `data/sent_emails.txt`

## Best Practices

1. **Always Test First**
   ```bash
   python3 send_campaign.py --test-email your@email.com
   ```

2. **Use Dry Run for Validation**
   ```bash
   python3 send_campaign.py --dry-run
   ```

3. **Monitor Logs**
   ```bash
   tail -f logs/campaign.log
   ```

4. **Backup Before Major Changes**
   ```bash
   cp -r campaign/ campaign_backup/
   ```

5. **Check Provider Limits**
   - Know your daily/hourly sending limits
   - Adjust batch sizes accordingly
   - Use auto-retry for large campaigns

## Security Notes

- **Never commit `config.json` with real passwords to git**
- Use `.gitignore` to exclude sensitive files
- Consider using environment variables for passwords
- Keep SMTP credentials secure

## Support

For issues or questions:
1. Check logs: `logs/campaign.log`
2. Review configuration: `config.json`
3. Test with single email first
4. Verify SMTP settings with provider

## License

This campaign system is provided as-is for internal use.
