# 🚀 ONE-PAGE QUICK START: Send Emails to 55 Candidates

**Email**: careers@semanticdataservices.com (configured in Thunderbird)
**Time**: 20 minutes total

---

## 📝 STEP 1: Get SMTP Settings from Thunderbird (5 min)

1. Open **Thunderbird**
2. Click **☰** → **Account Settings**
3. Click **"Outgoing Server (SMTP)"** in left sidebar
4. Write down these 3 things:
   ```
   Server Name: __________________ (e.g., smtp.semanticdataservices.com)
   Port:        __________________ (usually 587)
   Security:    __________________ (usually STARTTLS)
   ```
5. Remember your email password: **__________________**

---

## ⚙️ STEP 2: Configure the Script (5 min)

1. Open `send_with_company_email.py` in text editor
2. Find lines 18-25, change to YOUR settings:

```python
SENDER_EMAIL = 'careers@semanticdataservices.com'
SENDER_PASSWORD = 'YOUR_PASSWORD_HERE'  # ⚠️ From Step 1

SMTP_SERVER = 'smtp.semanticdataservices.com'  # ⚠️ From Thunderbird
SMTP_PORT = 587  # ⚠️ From Thunderbird (587 or 465)
USE_TLS = True  # True if port 587, False if port 465
```

3. **Save** the file

---

## ✅ STEP 3: Test Everything (5 min)

```bash
cd /home/user01/claude-test/Exam/production

# Test SMTP connection
python3 send_with_company_email.py --smtp-test

# Should see: ✅ SMTP connection test successful!
```

If you see ✅, proceed. If ❌, double-check SMTP settings.

---

## 🧪 STEP 4: Send Test to Yourself (3 min)

```bash
python3 send_with_company_email.py --test vinodyellagonda@paragroup.com
```

**Check your email** (vinodyellagonda@paragroup.com):
- ✅ Email received?
- ✅ Looks professional?
- ✅ Button works? (https://semanticservices.netlify.app)

If YES to all, proceed to Step 5.

---

## 🚀 STEP 5: Send to All 55 Candidates (10 min)

```bash
python3 send_with_company_email.py --send-all
```

Type `yes` when asked.

**Wait 10 minutes**. You'll see:
```
✅ Successfully sent: 55
❌ Failed: 0
```

Done! ✅

---

## 🔍 STEP 6: Verify (2 min)

```bash
# Check how many were sent
wc -l sent_emails.txt
# Should show: 55

# Check Thunderbird Sent folder
# Should see 55 emails
```

---

## ❌ IF SOMETHING FAILS

### "SMTP connection failed"
- Wrong password? Re-check Step 1
- Wrong server? Try `mail.semanticdataservices.com` instead

### "Authentication failed"
- Wrong password
- Try: `mail.semanticdataservices.com` or ask IT for SMTP server

### Script stopped midway?
- Just re-run: `python3 send_with_company_email.py --send-all`
- It skips already-sent emails automatically

---

## 📞 COMMON SMTP SERVERS BY PROVIDER

**cPanel/Hostgator/Bluehost**:
```python
SMTP_SERVER = 'mail.semanticdataservices.com'
SMTP_PORT = 587
USE_TLS = True
```

**Google Workspace**:
```python
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
USE_TLS = True
```

**Microsoft 365**:
```python
SMTP_SERVER = 'smtp.office365.com'
SMTP_PORT = 587
USE_TLS = True
```

---

## ✅ SUCCESS CHECKLIST

- [ ] Got SMTP settings from Thunderbird
- [ ] Configured script with password & SMTP server
- [ ] SMTP test passed (`--smtp-test`)
- [ ] Test email to yourself passed
- [ ] Test email looks perfect
- [ ] Sent to all 55 candidates
- [ ] Verified 55 emails in sent_emails.txt
- [ ] Verified 55 emails in Thunderbird Sent folder

---

**Total Time**: 20-30 minutes
**Result**: 55 professional emails sent from careers@semanticdataservices.com ✅
