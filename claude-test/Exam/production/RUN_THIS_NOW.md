# ⚡ RUN THIS NOW - HOSTINGER EMAIL AUTOMATION

**Email**: careers@semanticdataservices.com (Already in Thunderbird ✅)
**Time**: 15 minutes
**Commands**: 5 simple commands

---

## 🎯 YOU ONLY NEED TO DO THIS:

### STEP 1: Set Your Password (2 minutes)

```bash
cd /home/user01/claude-test/Exam/production
nano send_with_company_email.py
```

**Find line 21:**
```python
SENDER_PASSWORD = ''
```

**Change to** (use your actual password):
```python
SENDER_PASSWORD = 'YourPasswordHere'
```

Press: `Ctrl+O` (save), `Enter`, `Ctrl+X` (exit)

---

### STEP 2: Test SMTP Connection (1 minute)

```bash
python3 send_with_company_email.py --smtp-test
```

**Expected:**
```
✅ SMTP connection test successful!
```

If you see ✅ → Continue
If you see ❌ → See troubleshooting below

---

### STEP 3: Send Test to Yourself (2 minutes)

```bash
python3 send_with_company_email.py --test vinodyellagonda@paragroup.com
```

**Check your email** - should look professional with purple gradient header!

---

### STEP 4: Send to All 55 Candidates (10 minutes)

```bash
python3 send_with_company_email.py --send-all
```

Type `yes` when asked. Wait 10 minutes.

**Done!** ✅

---

### STEP 5: Verify (1 minute)

```bash
wc -l sent_emails.txt
```

Should show: `55`

---

## ⚡ SUPER QUICK (Copy & Paste)

```bash
cd /home/user01/claude-test/Exam/production
nano send_with_company_email.py  # Set password on line 21, save
python3 send_with_company_email.py --smtp-test
python3 send_with_company_email.py --test vinodyellagonda@paragroup.com
python3 send_with_company_email.py --send-all
```

---

## ❌ TROUBLESHOOTING

### "Authentication failed"
→ Wrong password. Use the same password as your Thunderbird login.

### "Connection refused"
→ Try alternative port:
```bash
nano send_with_company_email.py
```
Change line 27 to: `SMTP_PORT = 587`
Change line 28 to: `USE_TLS = True`

---

## 📧 WHAT'S ALREADY CONFIGURED

```python
SMTP_SERVER = 'smtp.hostinger.com'  ✅ Already set
SMTP_PORT = 465                      ✅ Already set
SENDER_EMAIL = 'careers@semanticdataservices.com'  ✅ Already set
```

**You only need to set:** `SENDER_PASSWORD` (line 21)

---

## ✅ THAT'S IT!

**Total**: 5 commands
**Time**: 15 minutes
**Result**: 55 professional emails sent from careers@semanticdataservices.com

---

**Start now:** Set password → Test → Send ✅
