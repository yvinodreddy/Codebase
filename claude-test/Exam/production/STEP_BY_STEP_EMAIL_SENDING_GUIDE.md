# 📧 COMPLETE STEP-BY-STEP EMAIL AUTOMATION GUIDE

**Status**: Production-Ready System
**Candidates**: 55 internship applicants
**Method**: Automated Python script with Gmail SMTP
**Estimated Time**: 15 minutes setup + 10 minutes sending

---

## 🎯 WHAT YOU HAVE NOW

✅ **candidates.csv** - Clean list of 55 candidates with names and emails
✅ **send_assessment_emails.py** - Production-ready automated email sender
✅ **Customized HTML email template** - Personalized for each candidate
✅ **Error handling & logging** - Complete audit trail
✅ **Rate limiting** - Respects Gmail sending limits

---

## 📋 PREREQUISITES

Before you start, you need:

1. ✅ **Gmail account** (vinodyellagonda@paragroup.com)
2. ✅ **Gmail App Password** (NOT your regular password)
3. ✅ **Python 3** installed on your computer
4. ✅ **Internet connection**

---

## 🔐 STEP 1: CREATE GMAIL APP PASSWORD (5 minutes)

Gmail requires an "App Password" for automated scripts (for security).

### Instructions:

1. **Go to Google Account Settings**:
   - Visit: https://myaccount.google.com/
   - Sign in with vinodyellagonda@paragroup.com

2. **Enable 2-Step Verification** (if not already enabled):
   - Click "Security" in left sidebar
   - Scroll to "How you sign in to Google"
   - Click "2-Step Verification"
   - Follow prompts to enable it

3. **Create App Password**:
   - Go to: https://myaccount.google.com/apppasswords
   - Or: Security → 2-Step Verification → App passwords (at bottom)
   - Select app: "Mail"
   - Select device: "Other (Custom name)" → Type: "Assessment Email Sender"
   - Click "Generate"
   - **COPY THE 16-CHARACTER PASSWORD** (looks like: `abcd efgh ijkl mnop`)

4. **Save this password** - You'll need it in Step 3

---

## 💻 STEP 2: PREPARE THE SCRIPT (2 minutes)

### Option A: Using the Terminal (Linux/Mac/WSL)

```bash
# Navigate to the production folder
cd /home/user01/claude-test/Exam/production

# Make script executable
chmod +x send_assessment_emails.py

# Verify files are present
ls -lh candidates.csv send_assessment_emails.py
```

### Option B: Using Windows

1. Open File Explorer
2. Navigate to: `C:\Users\YourName\claude-test\Exam\production`
3. Verify these files exist:
   - `candidates.csv`
   - `send_assessment_emails.py`

---

## ⚙️ STEP 3: CONFIGURE THE SCRIPT (3 minutes)

Open `send_assessment_emails.py` in a text editor and set your Gmail App Password:

### Find this line (around line 23):

```python
SENDER_PASSWORD = ''  # SET THIS - Use App Password
```

### Change it to:

```python
SENDER_PASSWORD = 'abcd efgh ijkl mnop'  # Your 16-character App Password from Step 1
```

**IMPORTANT**: Keep the quotes, paste your actual 16-character password from Step 1.

### Verify other settings (should already be correct):

```python
SENDER_EMAIL = 'vinodyellagonda@paragroup.com'
EXAM_URL = 'https://semanticservices.netlify.app'
START_DATE = 'November 05, 2025 at 9:00 AM EST'
END_DATE = 'November 07, 2025 at 11:59 PM EST'
ORGANIZATION = 'Semantic Data Services'
CONTACT_EMAIL = 'careers@semanticdataservices.com'
```

**Save the file** after making changes.

---

## ✅ STEP 4: CHECK CONFIGURATION (1 minute)

Run a configuration check to verify everything is set up correctly:

```bash
python3 send_assessment_emails.py --config-check
```

**Expected Output**:

```
================================================================================
📋 CONFIGURATION CHECK
================================================================================
SMTP Server:      smtp.gmail.com:587
Sender Email:     vinodyellagonda@paragroup.com
Password Set:     ✅ Yes
Exam URL:         https://semanticservices.netlify.app
Start Date:       November 05, 2025 at 9:00 AM EST
End Date:         November 07, 2025 at 11:59 PM EST
Organization:     Semantic Data Services
Contact Email:    careers@semanticdataservices.com
Candidates File:  candidates.csv ✅ Found
================================================================================

✅ Loaded 55 candidates from candidates.csv
Total candidates to email: 55
```

**If you see all ✅ checkmarks**, proceed to Step 5.

**If you see ❌ marks**:
- Password Not Set → Go back to Step 3
- Candidates File Not Found → Ensure you're in the correct directory

---

## 🧪 STEP 5: SEND TEST EMAIL TO YOURSELF (2 minutes)

**CRITICAL**: Always test first before sending to candidates!

```bash
python3 send_assessment_emails.py --test
```

**Expected Output**:

```
================================================================================
🧪 SENDING TEST EMAIL TO YOURSELF
================================================================================
[2025-11-05 10:30:45] [INFO] 🔌 Connecting to smtp.gmail.com...
[2025-11-05 10:30:46] [INFO] ✅ SMTP connection established
[2025-11-05 10:30:47] [INFO] ✅ Sent to: Test Candidate <vinodyellagonda@paragroup.com>

✅ Test email sent successfully!
Check your inbox at: vinodyellagonda@paragroup.com

If the email looks good, run: python3 send_assessment_emails.py --send-all
```

### Check Your Gmail Inbox:

1. Open Gmail (vinodyellagonda@paragroup.com)
2. Look for email with subject: **"Action Required: Complete Your Technical Assessment - Semantic Data Services"**
3. **Verify the email**:
   - ✅ HTML formatting looks professional (gradient header, colored sections)
   - ✅ Exam URL button works: https://semanticservices.netlify.app
   - ✅ Dates are correct (Nov 05 - Nov 07, 2025)
   - ✅ Contact email is careers@semanticdataservices.com
   - ✅ All information is accurate

**If test email looks good**, proceed to Step 6.

**If test email has issues**:
- Didn't receive? Check spam folder
- Wrong information? Edit the configuration in Step 3
- Formatting broken? Email client may not support HTML (try opening in Gmail web)

---

## 🚀 STEP 6: SEND TO ALL 55 CANDIDATES (10 minutes)

**This is the FINAL step** - emails will be sent to all candidates.

```bash
python3 send_assessment_emails.py --send-all
```

**You'll be asked to confirm**:

```
⚠️  You are about to send emails to 55 candidates. Continue? (yes/no):
```

Type `yes` and press Enter.

**Expected Output** (will take ~10 minutes with rate limiting):

```
================================================================================
📧 STARTING AUTOMATED EMAIL CAMPAIGN
================================================================================
[2025-11-05 10:35:00] [INFO] ✅ Loaded 55 candidates from candidates.csv
[2025-11-05 10:35:00] [INFO] 📊 Total candidates: 55
[2025-11-05 10:35:00] [INFO] ✅ Already sent: 0
[2025-11-05 10:35:00] [INFO] 📤 Pending to send: 55

[2025-11-05 10:35:01] [INFO] 🔌 Connecting to smtp.gmail.com...
[2025-11-05 10:35:02] [INFO] ✅ SMTP connection established

[2025-11-05 10:35:03] [INFO] ✅ Sent to: Anoushka Malik <anoushka22m@gmail.com>
[2025-11-05 10:35:05] [INFO] ✅ Sent to: Abhishek Kumar Shukla <abhishekkumarshukla.official@gmail.com>
[2025-11-05 10:35:07] [INFO] ✅ Sent to: Aayush Saini <ayushsaini2308@gmail.com>
[2025-11-05 10:35:09] [INFO] ✅ Sent to: Aditya Anand <adidiwakar1316@gmail.com>
...
[2025-11-05 10:35:23] [INFO] ⏸️  Batch complete (10/55). Waiting 60s before next batch...
...
[2025-11-05 10:44:15] [INFO] ✅ Sent to: Yash Thakur <yashth19@gmail.com>

================================================================================
📧 EMAIL CAMPAIGN COMPLETE
================================================================================
✅ Successfully sent: 55
❌ Failed: 0
📊 Total processed: 55

📝 Full log saved to: email_sending_log.txt
✅ Sent emails log: sent_emails.txt
```

---

## 📊 STEP 7: VERIFY COMPLETION (2 minutes)

### Check Log Files:

1. **email_sending_log.txt** - Complete detailed log
   ```bash
   cat email_sending_log.txt
   ```

2. **sent_emails.txt** - List of emails that were sent
   ```bash
   cat sent_emails.txt
   ```

### Check Your Gmail Sent Folder:

- Open Gmail → Sent
- You should see 55 sent emails (one per candidate)
- All with subject: "Action Required: Complete Your Technical Assessment..."

---

## 🔄 IF SOMETHING GOES WRONG

### Problem: Script Stops Midway

**Solution**: Just re-run the script
```bash
python3 send_assessment_emails.py --send-all
```

The script automatically skips emails that were already sent (tracked in `sent_emails.txt`).

### Problem: Gmail Blocks Sending

**Error**: "Daily sending quota exceeded"

**Cause**: Gmail free accounts have a daily limit of ~500 emails

**Solution**:
- Wait 24 hours and continue (script will resume from where it stopped)
- Or use a Google Workspace account (higher limits)

### Problem: "Authentication failed"

**Cause**: Wrong App Password

**Solution**:
1. Verify you used the App Password (not regular password)
2. App Password should be 16 characters with spaces
3. Re-generate App Password in Google Account Settings

### Problem: Some Emails Fail

**Check the log** for specific errors:
```bash
grep "FAILED" email_sending_log.txt
```

**Common causes**:
- Invalid email address (typo in candidates.csv)
- Email bounced (non-existent email)
- Temporary network issue

**Solution**: Fix the email in candidates.csv and re-run (script will only send to failed emails)

---

## 📧 ADVANCED: GMAIL YAMM METHOD (Alternative)

If you prefer a GUI approach instead of Python script:

### Step 1: Install YAMM

1. Open Google Sheets: https://sheets.google.com
2. Extensions → Add-ons → Get add-ons
3. Search for "Yet Another Mail Merge" (YAMM)
4. Install and authorize

### Step 2: Prepare Spreadsheet

1. Create new Google Sheet
2. Copy candidates.csv data:

```
Name                        | Email
----------------------------|-----------------------------
Anoushka Malik              | anoushka22m@gmail.com
Abhishek Kumar Shukla       | abhishekkumarshukla.official@gmail.com
...
```

### Step 3: Create Email Template

1. In Gmail, create a draft email
2. Subject: `Action Required: Complete Your Technical Assessment - Semantic Data Services`
3. Body: Copy the HTML email template
4. Use merge tags: `{{Name}}`, `{{Email}}`
5. Save as draft

### Step 4: Send via YAMM

1. In Google Sheet: Extensions → YAMM → Start Mail Merge
2. Select your draft email
3. Map columns: Name → {{Name}}, Email → {{Email}}
4. Click "Send emails"

**Pros**:
- GUI interface
- Easier for non-programmers
- Tracking built-in

**Cons**:
- YAMM free tier: 50 emails/day
- Need to upgrade for 55 candidates (or send in 2 days)

---

## 📊 EXPECTED RESULTS

### Email Delivery Rates:

**Typical metrics** for bulk emails:

- **Sent**: 55/55 (100%)
- **Delivered**: 53-55 (96-100%) - Some may bounce
- **Opened**: 35-40 (63-73%) - Industry standard
- **Clicked (exam URL)**: 25-35 (45-63%)
- **Completed Exam**: 20-30 (36-55%)

### Timeline:

- **Day 1 (Nov 5)**: Send emails → 20-30% open within 24 hours
- **Day 2 (Nov 6)**: Reminder needed? → Another 20-30% open
- **Day 3 (Nov 7)**: Final deadline → Last-minute completions

---

## 📱 OPTIONAL: SMS REMINDERS

For candidates who don't open emails, send SMS reminders on Day 6 (Nov 6):

**SMS Text**:
```
Hi [Name], your Python & SQL Assessment for Semantic Data Services is due TOMORROW (Nov 7 at 11:59 PM EST). Login: https://semanticservices.netlify.app. Check email for details. Good luck!
```

**Services to use**:
- Twilio (https://www.twilio.com) - $0.0079 per SMS
- AWS SNS (https://aws.amazon.com/sns/) - $0.00645 per SMS
- MessageBird (https://www.messagebird.com) - International support

---

## 📧 REMINDER EMAIL (Day 6 - November 6)

If you want to send a reminder email 1 day before deadline:

### Create: `send_reminder_email.py`

```python
#!/usr/bin/env python3
# Same structure as send_assessment_emails.py
# Change subject to: "REMINDER: Technical Assessment Due Tomorrow - Semantic Data Services"
# Change template to shorter reminder version
```

Or simply modify the existing script's subject line and run again (candidates will receive 2nd email).

---

## ✅ PRODUCTION CHECKLIST

Before sending to all 55 candidates, verify:

- [ ] Gmail App Password is set correctly
- [ ] Test email received and looks professional
- [ ] Exam URL works: https://semanticservices.netlify.app
- [ ] Dates are correct: Nov 05 - Nov 07, 2025
- [ ] Contact email is monitored: careers@semanticdataservices.com
- [ ] All 55 candidates are in candidates.csv
- [ ] No duplicate emails in the list
- [ ] Script has executable permissions (`chmod +x`)
- [ ] Internet connection is stable
- [ ] You have 15 minutes to monitor the sending process

---

## 🎯 QUICK COMMAND REFERENCE

```bash
# Navigate to folder
cd /home/user01/claude-test/Exam/production

# Check configuration
python3 send_assessment_emails.py --config-check

# Send test email
python3 send_assessment_emails.py --test

# Send to all candidates
python3 send_assessment_emails.py --send-all

# Check log
cat email_sending_log.txt

# Check sent emails
cat sent_emails.txt

# Count sent emails
wc -l sent_emails.txt

# Check for failures
grep "FAILED" email_sending_log.txt
```

---

## 📞 TROUBLESHOOTING CONTACTS

**If you encounter issues**:

1. **Gmail Help**: https://support.google.com/mail/answer/185833 (App Passwords)
2. **Python Issues**: Check Python version: `python3 --version` (need 3.6+)
3. **Network Issues**: Test connection: `ping smtp.gmail.com`

---

## 🎉 SUCCESS METRICS

You'll know it's successful when:

✅ All 55 emails show in Gmail Sent folder
✅ `email_sending_log.txt` shows "✅ Successfully sent: 55"
✅ `sent_emails.txt` contains 55 email addresses
✅ No "FAILED" entries in the log
✅ Candidates start logging into the exam system
✅ You receive confirmation emails from EmailJS (when they submit exams)

---

## 📋 TIMELINE SUMMARY

| Time | Task | Duration |
|------|------|----------|
| 0:00 | Create Gmail App Password | 5 min |
| 0:05 | Prepare script files | 2 min |
| 0:07 | Configure script (set password) | 3 min |
| 0:10 | Check configuration | 1 min |
| 0:11 | Send test email to yourself | 2 min |
| 0:13 | Review test email in inbox | 2 min |
| 0:15 | Send to all 55 candidates | 10 min |
| 0:25 | Verify completion & logs | 2 min |
| **0:27** | **DONE!** | **Total: 27 min** |

---

## 🚀 READY TO START?

**Execute these commands in order**:

```bash
# 1. Navigate to folder
cd /home/user01/claude-test/Exam/production

# 2. Check everything is ready
python3 send_assessment_emails.py --config-check

# 3. Send test to yourself
python3 send_assessment_emails.py --test

# 4. If test looks good, send to all
python3 send_assessment_emails.py --send-all
```

---

**Generated**: November 4, 2025
**Status**: ✅ Production-Ready
**Files**: candidates.csv (55 candidates), send_assessment_emails.py (automated sender)
**Support**: careers@semanticdataservices.com

---

*This guide provides a complete automated email solution with zero manual work. Just follow steps 1-6 and all 55 candidates will receive professional, personalized assessment invitations.*
