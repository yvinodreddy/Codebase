# Quick Start Testing Guide
**Get from 0% to 100% Tested in 4 Hours**

---

## STEP 1: Setup (30 minutes)

### 1.1 Verify Database Connection
```bash
# Open appsettings.json
# Check connection string points to your database
```

### 1.2 Run Test Data Scripts
```sql
-- Open TEST_DATA_SCRIPTS.sql in SQL Server Management Studio
-- Execute the script
-- This inserts 53 test records
```

### 1.3 Start Application
```bash
cd /home/user01/claude-test/RMMS.Web/RMMS.Web
dotnet run
```

### 1.4 Open Browser
```
Navigate to: https://localhost:5001 (or http://localhost:5000)
```

---

## STEP 2: Quick Smoke Test (30 minutes)

**Test 1 module completely to verify everything works**

### Test Paddy Procurement Module:

**A. View List (2 min)**
1. Click "Paddy Procurement" in menu
2. ✓ See 5 test records
3. ✓ No errors in browser console (F12)

**B. Create New Record (5 min)**
1. Click "Create" button
2. Fill form:
   - Supplier: "Test Supplier"
   - Variety: "Basmati"
   - Quantity: 100.555 (test 3 decimals)
   - Price: 50.999 (test 3 decimals)
3. Click Save
4. ✓ Success message
5. ✓ Rounds to 100.56 and 51.00

**C. Edit Record (5 min)**
1. Click "Edit" on first record
2. ✓ Form loads with data
3. ✓ Dropdown shows selected variety
4. Change quantity to 200.75
5. Click Save
6. ✓ Success message
7. ✓ List shows 200.75

**D. Delete Record (3 min)**
1. Click "Delete" on last record
2. ✓ Confirmation appears
3. Confirm
4. ✓ Success message
5. ✓ Record removed from list

**E. Search (2 min)**
1. Type "Basmati" in search box
2. ✓ List filters

**F. Stock Summary (3 min)**
1. Click "Stock Summary"
2. ✓ Data displays (not empty)
3. ✓ Totals calculated
4. ✓ Doesn't fade after 1 minute

---

## STEP 3: Critical Features Test (1 hour)

### Test These Key Issues from Mindmap:

**1. Decimal Validation (10 min)**
- [ ] Paddy Procurement: Enter 3 decimals → rounds to 2
- [ ] Rice Sales: Enter 3 decimals → rounds to 2
- [ ] Byproduct Sales: Enter 3 decimals → rounds to 2

**2. DataTable Errors (10 min)**
- [ ] Cash Book: Navigate there 3 times → no console errors
- [ ] Vouchers: Navigate there 3 times → no console errors
- [ ] Payables: Navigate there 3 times → no console errors

**3. Fading Issues (15 min)**
- [ ] External Rice: Load page, wait 2 minutes → still visible
- [ ] Loans Receivables: Load page, wait 2 minutes → still visible

**4. Send Reminders (10 min)**
- [ ] Payables: Click "Send Reminders" → success message
- [ ] Receivables: Click "Send Reminders" → success message

**5. Outstanding Payments (15 min)**
- [ ] Load report
- [ ] Click "Pay Now" → navigates to payment page
- [ ] Click "Send Reminder" → confirmation and success
- [ ] Test pagination (click page 2)
- [ ] Test sorting (click column header)
- [ ] Test search box

---

## STEP 4: Remaining Modules (2 hours)

**Quick test each module (10 min each):**

1. Rice Sales
   - [ ] Create → Edit → Delete
   - [ ] Print Preview works

2. Byproduct Sales
   - [ ] Create → Edit → Delete

3. External Rice Sales
   - [ ] Create → Edit → Delete
   - [ ] No fading

4. Bank Transactions
   - [ ] Create → Edit → Delete
   - [ ] Search works

5. Cash Book
   - [ ] Create → Edit → Delete
   - [ ] No DataTable errors

6. Vouchers
   - [ ] Create → Edit → Delete
   - [ ] No UI overlap

7. Payables
   - [ ] Create → Edit → Delete
   - [ ] Send Reminders works

8. Receivables
   - [ ] Create → Edit → Delete
   - [ ] Send Reminders works

9. Loan Advances
   - [ ] View → Data from DB (not hard-coded)
   - [ ] Create → Edit → Delete

10. Fixed Assets
    - [ ] View → Data displays
    - [ ] Create → Edit → Delete

---

## STEP 5: Reports Test (30 minutes)

**Test each report loads with data:**

1. [ ] Dashboard - Shows data, graphs render
2. [ ] Daily Sales - Select date, data shows
3. [ ] Monthly Sales - Select month, chart shows
4. [ ] Product-Wise Sales - Data shows, can search
5. [ ] Customer-Wise Sales - Data shows, graphs visible
6. [ ] Rice Stock Report - Shows stock by grade
7. [ ] Paddy Stock Report - NOT showing 0, real data
8. [ ] Outstanding Payments - Pagination works
9. [ ] Profit & Loss - Generates without error
10. [ ] Cash Flow - Displays data

---

## STEP 6: Document Issues (30 minutes)

**If you find ANY issues:**

1. Take screenshot
2. Note exact steps to reproduce
3. Copy error message from console (F12)
4. Tell me and I'll fix immediately

---

## CHECKLIST SUMMARY

**Phase 1: Setup**
- [ ] Database connected
- [ ] Test data inserted
- [ ] Application running
- [ ] Can access homepage

**Phase 2: One Module Complete Test**
- [ ] Paddy Procurement fully tested

**Phase 3: Critical Issues**
- [ ] Decimal validation working
- [ ] No DataTable errors
- [ ] No fading issues
- [ ] Send reminders working
- [ ] Outstanding Payments features working

**Phase 4: All Modules**
- [ ] 11 modules all tested (Create/Edit/Delete)

**Phase 5: All Reports**
- [ ] 10 reports all working

**Phase 6: Issues Documented**
- [ ] List of any issues found
- [ ] Screenshots if applicable

---

## EXPECTED RESULTS

**After completing this guide:**
- ✅ 100% of functionality tested
- ✅ All critical issues verified fixed
- ✅ Any remaining issues documented
- ✅ Confidence to deploy to production

**Time Required:** ~4 hours

**Your Role:** Run the tests, document issues
**My Role:** Fix any issues you find immediately

---

**Let's get to 100% together!**
