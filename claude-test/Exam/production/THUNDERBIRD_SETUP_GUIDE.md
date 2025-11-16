# 📧 COMPLETE THUNDERBIRD EMAIL AUTOMATION GUIDE

**Email**: careers@semanticdataservices.com
**Recipients**: 55 internship candidates
**Method**: Python automation + Thunderbird SMTP settings
**Time**: 20 minutes total

---

## 🎯 OVERVIEW

You have `careers@semanticdataservices.com` configured in Thunderbird. This guide will:

1. Extract SMTP settings from Thunderbird
2. Configure Python script to use these settings
3. Test with your own email first
4. Send to all 55 candidates automatically

---

## 📋 STEP 1: GET SMTP SETTINGS FROM THUNDERBIRD (5 minutes)

### Method A: From Thunderbird Settings (Recommended)

1. **Open Thunderbird**

2. **Go to Account Settings**:
   - Click ☰ (menu) → **Account Settings**
   - Or: Tools → Account Settings

3. **Find your email account**:
   - In left sidebar, click: **careers@semanticdataservices.com**

4. **Click "Outgoing Server (SMTP)"** in left sidebar

5. **Note down these settings**:
   ```
   Server Name:     __________________ (e.g., smtp.semanticdataservices.com)
   Port:            __________________ (usually 587, 465, or 25)
   Connection security: ______________ (STARTTLS, SSL/TLS, or None)
   Authentication:  __________________ (usually "Normal password")
   Username:        __________________ (usually careers@semanticdataservices.com)
   ```

6. **Write down your password**:
   - This is the password you use to login to careers@semanticdataservices.com

### Method B: From prefs.js File (Advanced)

If you can't find settings in Thunderbird UI:

1. Open Thunderbird profile folder:
   - Linux: `~/.thunderbird/xxxxxxxx.default/prefs.js`
   - Windows: `%APPDATA%\Thunderbird\Profiles\xxxxxxxx.default\prefs.js`
   - Mac: `~/Library/Thunderbird/Profiles/xxxxxxxx.default/prefs.js`

2. Search for these lines:
   ```javascript
   user_pref("mail.smtpserver.smtp1.hostname", "smtp.example.com");
   user_pref("mail.smtpserver.smtp1.port", 587);
   user_pref("mail.smtpserver.smtp1.username", "careers@semanticdataservices.com");
   ```

---

## ⚙️ STEP 2: CONFIGURE THE PYTHON SCRIPT (5 minutes)

Open `send_with_company_email.py` in a text editor.

### Find these lines (around line 18-25):

```python
SENDER_EMAIL = 'careers@semanticdataservices.com'
SENDER_PASSWORD = ''  # SET THIS - Your company email password
SENDER_NAME = 'Semantic Data Services - Recruitment Team'

# SMTP Server Settings
SMTP_SERVER = ''  # e.g., 'smtp.semanticdataservices.com'
SMTP_PORT = 587  # Common: 587 (TLS) or 465 (SSL)
USE_TLS = True  # Set to False if using SSL (port 465)
```

### Update with YOUR settings from Step 1:

```python
SENDER_EMAIL = 'careers@semanticdataservices.com'
SENDER_PASSWORD = 'YourPasswordHere123'  # ⚠️ Your actual email password
SENDER_NAME = 'Semantic Data Services - Recruitment Team'

# Example for common hosting providers:
SMTP_SERVER = 'smtp.semanticdataservices.com'  # From Thunderbird settings
SMTP_PORT = 587  # From Thunderbird (587 = TLS, 465 = SSL, 25 = plain)
USE_TLS = True  # True for port 587, False for port 465
```

### Common SMTP Settings by Provider:

#### If your domain uses **cPanel/Hostgator/Bluehost/GoDaddy**:
```python
SMTP_SERVER = 'mail.semanticdataservices.com'  # or smtp.semanticdataservices.com
SMTP_PORT = 587
USE_TLS = True
```

#### If your domain uses **Google Workspace (G Suite)**:
```python
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
USE_TLS = True
```

#### If your domain uses **Microsoft 365**:
```python
SMTP_SERVER = 'smtp.office365.com'
SMTP_PORT = 587
USE_TLS = True
```

#### If your domain uses **Zoho Mail**:
```python
SMTP_SERVER = 'smtp.zoho.com'
SMTP_PORT = 587
USE_TLS = True
```

**Save the file** after making changes.

---

## ✅ STEP 3: TEST SMTP CONNECTION (2 minutes)

Before sending any emails, test that the script can connect to your SMTP server:

```bash
cd /home/user01/claude-test/Exam/production
python3 send_with_company_email.py --smtp-test
```

**Expected Output (Success)**:
```
[2025-11-05 10:00:00] [INFO] 🔌 Testing connection to smtp.semanticdataservices.com:587...
[2025-11-05 10:00:01] [INFO] ✅ SMTP connection test successful!
```

**If you see errors**:

### Error: "Connection refused"
**Fix**: Wrong SMTP_SERVER or SMTP_PORT
- Double-check Thunderbird settings
- Try alternative: `mail.semanticdataservices.com` instead of `smtp.semanticdataservices.com`

### Error: "Authentication failed"
**Fix**: Wrong password
- Verify you're using the correct email password
- Some providers require App Passwords (like Gmail)

### Error: "SSL/TLS error"
**Fix**: Wrong USE_TLS setting
- If port 587: Set `USE_TLS = True`
- If port 465: Set `USE_TLS = False` (uses SSL instead)

---

## 🔍 STEP 4: CHECK CONFIGURATION (1 minute)

Verify all settings are correct:

```bash
python3 send_with_company_email.py --config-check
```

**Expected Output**:
```
================================================================================
📋 CONFIGURATION CHECK
================================================================================
Sender Email:     careers@semanticdataservices.com
Sender Name:      Semantic Data Services - Recruitment Team
Password Set:     ✅ Yes
SMTP Server:      smtp.semanticdataservices.com
SMTP Port:        587
Use TLS:          ✅ Yes
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

**All checkmarks ✅?** Proceed to Step 5.

---

## 🧪 STEP 5: SEND TEST EMAIL TO YOURSELF (3 minutes)

**CRITICAL**: Always test with your own email first!

### Replace with YOUR personal email:

```bash
python3 send_with_company_email.py --test vinodyellagonda@paragroup.com
```

**Expected Output**:
```
================================================================================
🧪 SENDING TEST EMAIL
================================================================================
[2025-11-05 10:05:00] [INFO] 🔌 Testing connection to smtp.semanticdataservices.com:587...
[2025-11-05 10:05:01] [INFO] 🔐 Starting TLS encryption...
[2025-11-05 10:05:02] [INFO] 🔑 Logging in as careers@semanticdataservices.com...
[2025-11-05 10:05:03] [INFO] ✅ Sent to: Test Candidate <vinodyellagonda@paragroup.com>

✅ Test email sent successfully!
📬 Check your inbox at: vinodyellagonda@paragroup.com

If the email looks good, run: python3 send_with_company_email.py --send-all
```

### Check Your Email Inbox:

1. Open your email (vinodyellagonda@paragroup.com)
2. Look for subject: **"Action Required: Complete Your Technical Assessment - Semantic Data Services"**
3. **Verify the email**:
   - ✅ **From**: Shows "Semantic Data Services - Recruitment Team <careers@semanticdataservices.com>"
   - ✅ **HTML formatting**: Gradient purple header, color-coded sections
   - ✅ **CTA Button**: "🚀 Start Assessment Now" button works
   - ✅ **Exam URL**: Button links to https://semanticservices.netlify.app
   - ✅ **Dates**: Nov 05 - Nov 07, 2025 are correct
   - ✅ **Personalization**: Says "Dear Test," (first name extracted)
   - ✅ **Contact**: careers@semanticdataservices.com shown
   - ✅ **Mobile responsive**: Open on phone to test

**If email looks perfect**, proceed to Step 6.

**If email not received**:
- Check spam/junk folder
- Check sent folder in Thunderbird
- Re-run with `--test` again

---

## 🚀 STEP 6: SEND TO ALL 55 CANDIDATES (10 minutes)

**This is the FINAL step** - emails will be sent to all candidates.

```bash
python3 send_with_company_email.py --send-all
```

**You'll be asked to confirm**:
```
⚠️  You are about to send emails to 55 candidates from careers@semanticdataservices.com.
   Continue? (yes/no):
```

Type `yes` and press Enter.

### Expected Output (full campaign):

```
================================================================================
📧 STARTING AUTOMATED EMAIL CAMPAIGN
================================================================================
[2025-11-05 10:10:00] [INFO] ✅ Loaded 55 candidates from candidates.csv
[2025-11-05 10:10:00] [INFO] 📊 Total candidates: 55
[2025-11-05 10:10:00] [INFO] ✅ Already sent: 0
[2025-11-05 10:10:00] [INFO] 📤 Pending to send: 55

[2025-11-05 10:10:01] [INFO] 🔌 Connecting to smtp.semanticdataservices.com:587...
[2025-11-05 10:10:02] [INFO] 🔐 Starting TLS encryption...
[2025-11-05 10:10:03] [INFO] 🔑 Logging in as careers@semanticdataservices.com...
[2025-11-05 10:10:04] [INFO] ✅ SMTP connection established

[2025-11-05 10:10:05] [INFO] ✅ Sent to: Anoushka Malik <anoushka22m@gmail.com>
[2025-11-05 10:10:07] [INFO] ✅ Sent to: Abhishek Kumar Shukla <abhishekkumarshukla.official@gmail.com>
[2025-11-05 10:10:09] [INFO] ✅ Sent to: Aayush Saini <ayushsaini2308@gmail.com>
[2025-11-05 10:10:11] [INFO] ✅ Sent to: Aditya Anand <adidiwakar1316@gmail.com>
[2025-11-05 10:10:13] [INFO] ✅ Sent to: Arshdeep Singh <as9.arshdeepsingh9@gmail.com>
[2025-11-05 10:10:15] [INFO] ✅ Sent to: Aryan Sharma <aryan.sharma6428@gmail.com>
[2025-11-05 10:10:17] [INFO] ✅ Sent to: Bhawna Parashar <parasharbhawna51@gmail.com>
[2025-11-05 10:10:19] [INFO] ✅ Sent to: Harshita Khanijo <khanijoharshita@gmail.com>
[2025-11-05 10:10:21] [INFO] ✅ Sent to: Jayaprakash Dirisala <jayprakashdirisala@gmail.com>
[2025-11-05 10:10:23] [INFO] ✅ Sent to: Juturu Yaswanth Reddy <juturuyaswanthreddyreddy@gmail.com>

[2025-11-05 10:10:25] [INFO] ⏸️  Batch complete (10/55). Waiting 60s...

[2025-11-05 10:11:27] [INFO] ✅ Sent to: Ketan Mittal <ketanmittal3000@gmail.com>
...
[2025-11-05 10:19:45] [INFO] ✅ Sent to: Yash Thakur <yashth19@gmail.com>

================================================================================
📧 EMAIL CAMPAIGN COMPLETE
================================================================================
✅ Successfully sent: 55
❌ Failed: 0
📊 Total processed: 55

📝 Full log saved to: email_sending_log.txt
✅ Sent emails log: sent_emails.txt
```

**Duration**: ~10 minutes (rate limiting: 2 seconds between emails, 60 seconds after every 10 emails)

---

## 📊 STEP 7: VERIFY COMPLETION (2 minutes)

### Check Log Files:

```bash
# View detailed log
cat email_sending_log.txt

# View list of sent emails
cat sent_emails.txt

# Count total sent
wc -l sent_emails.txt
# Should output: 55

# Check for any failures
grep "FAILED" email_sending_log.txt
# Should be empty
```

### Check Thunderbird Sent Folder:

1. Open Thunderbird
2. Select **careers@semanticdataservices.com** account
3. Click **Sent** folder
4. You should see 55 sent emails
5. All with subject: "Action Required: Complete Your Technical Assessment..."

---

## 🔄 IF SOMETHING GOES WRONG

### Problem: Script Stops Midway

**Solution**: Just re-run the script
```bash
python3 send_with_company_email.py --send-all
```

The script automatically tracks which emails were sent in `sent_emails.txt` and skips them.

### Problem: "Sending quota exceeded"

**Cause**: Email provider has daily sending limits

**Solution**:
- Wait 24 hours
- Re-run script (it will continue from where it stopped)
- Contact your email hosting provider to increase limits

### Problem: Some emails marked as spam

**Solution**:
- Ensure SPF/DKIM records are configured for your domain
- Contact email provider to whitelist bulk sending
- Warm up the email account by sending fewer emails first

### Problem: Emails go to spam for recipients

**Prevention**:
- Ask candidates to check spam folder
- Send reminder email: "Check spam if you didn't receive it"
- Ensure your domain has proper SPF/DKIM/DMARC records

---

## 📧 ALTERNATIVE: MANUAL METHOD VIA THUNDERBIRD

If Python script doesn't work, use Thunderbird's Mail Merge add-on:

### Step 1: Install Mail Merge Add-on

1. Open Thunderbird
2. Tools → Add-ons and Themes
3. Search: "Mail Merge"
4. Install: **"Mail Merge"** by Alexander Bergmann
5. Restart Thunderbird

### Step 2: Prepare CSV File

The `candidates.csv` is already ready! Format:
```
Name,Email
Anoushka Malik,anoushka22m@gmail.com
Abhishek Kumar Shukla,abhishekkumarshukla.official@gmail.com
...
```

### Step 3: Compose Email Template

1. In Thunderbird: **Write** (new email)
2. **To**: `{{Email}}`
3. **Subject**: `Action Required: Complete Your Technical Assessment - Semantic Data Services`
4. **Body**: Copy the HTML template from the Python script
   - Replace `{first_name}` with `{{Name}}`

### Step 4: Start Mail Merge

1. With email draft open: **File → Mail Merge**
2. **Select source**: Browse to `candidates.csv`
3. **Field delimiter**: Comma
4. **Preview**: Check first few emails look correct
5. **Send mode**:
   - Test: Send to yourself first
   - Production: Send Now (or Save as Drafts)
6. Click **OK**

**Pros**: Visual interface, no coding
**Cons**: Manual process, less automation

---

## 📊 EXPECTED RESULTS

### Email Delivery Rates (Industry Standard):

- **Sent**: 55/55 (100%)
- **Delivered**: 53-55 (96-100%) - Some may bounce
- **Opened**: 35-42 (63-76%)
- **Clicked (exam URL)**: 27-38 (49-69%)
- **Completed Exam**: 22-33 (40-60%)

### Timeline:

- **Nov 5 (Day 1)**: Send emails → 25-35% open within 24 hours
- **Nov 6 (Day 2)**: Send reminder? → Another 20-30% open
- **Nov 7 (Day 3)**: Final deadline → Last-minute completions

---

## 🔐 SECURITY BEST PRACTICES

### Password in Script

⚠️ The script contains your email password in plain text!

**Secure it**:
```bash
# Set file permissions (only you can read)
chmod 600 send_with_company_email.py

# Never commit to Git
echo "send_with_company_email.py" >> .gitignore
```

**Better approach** (environment variable):
```python
import os
SENDER_PASSWORD = os.environ.get('EMAIL_PASSWORD', '')
```

Then run:
```bash
export EMAIL_PASSWORD='YourPasswordHere'
python3 send_with_company_email.py --send-all
```

---

## ✅ PRE-FLIGHT CHECKLIST

Before sending to all 55 candidates:

- [ ] SMTP settings extracted from Thunderbird
- [ ] Python script configured (password, server, port)
- [ ] SMTP connection test passed (`--smtp-test`)
- [ ] Configuration check passed (`--config-check`)
- [ ] Test email sent to yourself (`--test`)
- [ ] Test email received and looks perfect
- [ ] Exam URL button works: https://semanticservices.netlify.app
- [ ] Dates are correct: Nov 05 - Nov 07, 2025
- [ ] All 55 candidates in candidates.csv (no duplicates)
- [ ] Script permissions set: `chmod +x send_with_company_email.py`
- [ ] Internet connection stable
- [ ] You have 15 minutes to monitor the process

---

## 🎯 QUICK COMMAND REFERENCE

```bash
# Navigate to folder
cd /home/user01/claude-test/Exam/production

# Test SMTP connection
python3 send_with_company_email.py --smtp-test

# Check configuration
python3 send_with_company_email.py --config-check

# Send test to yourself
python3 send_with_company_email.py --test vinodyellagonda@paragroup.com

# Send to all 55 candidates
python3 send_with_company_email.py --send-all

# Check logs
cat email_sending_log.txt
cat sent_emails.txt
wc -l sent_emails.txt
grep "FAILED" email_sending_log.txt
```

---

## 📞 TROUBLESHOOTING GUIDE

### Common SMTP Server Patterns

If Thunderbird doesn't show clear SMTP settings, try these patterns:

1. `smtp.semanticdataservices.com`
2. `mail.semanticdataservices.com`
3. `smtp.mail.semanticdataservices.com`
4. `server.semanticdataservices.com`

### Test each pattern:

```python
# Edit script, set SMTP_SERVER to each pattern, then:
python3 send_with_company_email.py --smtp-test
```

### Check DNS Records

```bash
# Find MX records (mail server)
dig semanticdataservices.com MX

# Try SMTP server from MX record
```

---

## 🎉 SUCCESS INDICATORS

You'll know it worked when:

✅ All 55 emails visible in Thunderbird Sent folder
✅ `sent_emails.txt` contains 55 email addresses
✅ `email_sending_log.txt` shows "✅ Successfully sent: 55"
✅ No "FAILED" entries in log
✅ Candidates start accessing the exam system
✅ Candidates reply acknowledging receipt

---

## 📋 TIMING BREAKDOWN

| Step | Task | Time |
|------|------|------|
| 1 | Get SMTP settings from Thunderbird | 5 min |
| 2 | Configure Python script | 5 min |
| 3 | Test SMTP connection | 2 min |
| 4 | Check configuration | 1 min |
| 5 | Send test email to yourself | 3 min |
| 6 | Send to all 55 candidates | 10 min |
| 7 | Verify completion | 2 min |
| **Total** | **Complete process** | **28 min** |

---

**Generated**: November 5, 2025
**Status**: ✅ Production-Ready
**Email**: careers@semanticdataservices.com
**Recipients**: 55 internship candidates
**Method**: Thunderbird SMTP + Python automation

---

*This guide provides complete automation using your existing Thunderbird email configuration. No Gmail or Mailchimp needed!*
