# RMMS Issue Reporting Template

**Please fill out this template for each issue you encounter:**

---

## Issue #1

### Page/Module:
*(e.g., Production Batches, Machines, etc.)*

### URL:
*(e.g., http://localhost:5090/ProductionBatches)*

### Issue Type:
- [ ] Cannot access page (404 error)
- [ ] Page loads but crashes
- [ ] Form doesn't submit
- [ ] Data doesn't display
- [ ] Button doesn't work
- [ ] Layout/UI issue
- [ ] Other (describe below)

### What you tried to do:
*(Step-by-step what you clicked/did)*
1.
2.
3.

### What happened (actual result):
*(Describe the error or unexpected behavior)*


### What you expected to happen:
*(What should have happened instead)*


### Error message (if any):
*(Copy any error messages you see on screen or in browser console)*


### Screenshots (if possible):
*(Take a screenshot and note the filename)*


---

## Issue #2

*(Repeat the above format for each issue)*

---

## Quick Issue Checklist

Before reporting, please verify:
- [ ] I am logged in to the application
- [ ] The application is running (http://localhost:5090 is accessible)
- [ ] I have refreshed the page (Ctrl+F5)
- [ ] I checked browser console for errors (F12 → Console tab)

---

## How to Check Browser Console Errors:

1. Open the page with the issue
2. Press F12 to open Developer Tools
3. Click on the "Console" tab
4. Look for red error messages
5. Copy the error text and paste it in the issue report above

---

## Application Log Errors

To get recent application errors, run this command:
```bash
tail -100 /tmp/rmms_app.log | grep -i "error\|exception\|fail"
```

Paste the output here:
```

```

---

## Database Connection Test

Run this to verify database is accessible:
```bash
/opt/mssql-tools18/bin/sqlcmd -S 172.17.208.1 -U sa -P 'YourStrong@Passw0rd' -d RMMS_Production -Q "SELECT COUNT(*) FROM ProductionBatches" -C
```

Result:
```

```

---

**After filling out this template, share it with me and I'll fix all issues systematically.**
