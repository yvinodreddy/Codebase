# Simple Testing Checklist
**Print this and check off as you test**

---

## DATABASE SETUP
- [ ] Test data inserted (TEST_DATA_SCRIPTS.sql)
- [ ] 53 records confirmed in database

---

## APPLICATION STARTUP
- [ ] Application runs without errors
- [ ] Can access homepage
- [ ] Can login (if required)

---

## CRITICAL FIXES TO VERIFY

### 1. DECIMAL VALIDATION (Priority 1)
- [ ] Enter 100.555 in Paddy Procurement → Saves as 100.56
- [ ] Enter 50.999 in Rice Sales → Saves as 51.00
- [ ] Enter 75.123 in any price field → Saves as 75.12

### 2. DATATABLE ERRORS (Priority 1)
- [ ] Cash Book - No console errors
- [ ] Vouchers - No console errors
- [ ] Payables - No console errors
- [ ] Receivables - No console errors

### 3. FADING ISSUES (Priority 1)
- [ ] External Rice - Wait 2 min → Still visible
- [ ] Loans Receivables - Wait 2 min → Still visible

### 4. NAVIGATION (Priority 2)
- [ ] Stock Summary → Print → Back → Goes to Paddy Procurement

### 5. SEND REMINDERS (Priority 2)
- [ ] Payables → "Send Reminders" → Success message
- [ ] Receivables → "Send Reminders" → Success message

### 6. OUTSTANDING PAYMENTS (Priority 2)
- [ ] "Pay Now" button → Goes to payment page
- [ ] "Send Reminder" button → Confirmation → Success
- [ ] Pagination works (page 1, 2, 3)
- [ ] Sorting works (click column headers)
- [ ] Search works

---

## CRUD OPERATIONS (Test on ALL 11 modules)

### Paddy Procurement
- [ ] Create new record
- [ ] Edit existing record
- [ ] Delete record
- [ ] Search works

### Rice Sales
- [ ] Create | Edit | Delete | Search
- [ ] Print Preview works

### Byproduct Sales
- [ ] Create | Edit | Delete | Search

### External Rice Sales
- [ ] Create | Edit | Delete | Search

### Bank Transactions
- [ ] Create | Edit | Delete | Search

### Cash Book
- [ ] Create | Edit | Delete | Search

### Vouchers
- [ ] Create | Edit | Delete | Search
- [ ] No UI button overlap

### Payables
- [ ] Create | Edit | Delete | Search

### Receivables
- [ ] Create | Edit | Delete | Search

### Loan Advances
- [ ] Create | Edit | Delete
- [ ] Shows database data (not hard-coded)

### Fixed Assets
- [ ] Create | Edit | Delete | Search

---

## REPORTS (Test all 10)

### Dashboard
- [ ] Shows data (not empty)
- [ ] Graphs render
- [ ] NOT hard-coded values

### Daily Sales Report
- [ ] Select date
- [ ] Data displays

### Monthly Sales Report
- [ ] Select month/year
- [ ] Chart displays
- [ ] Data calculates correctly

### Product-Wise Sales
- [ ] Data shows
- [ ] Charts render
- [ ] Pagination works

### Customer-Wise Sales
- [ ] Data shows
- [ ] Charts visible
- [ ] Search works

### Rice Stock Report
- [ ] Data displays
- [ ] Grouped by grade

### Paddy Stock Report
- [ ] NOT showing 0
- [ ] Shows real data from procurement
- [ ] Grouped by variety

### Outstanding Payments Report
- [ ] Shows payables and receivables
- [ ] Buttons work
- [ ] Pagination works

### Profit & Loss Statement
- [ ] Generates without error
- [ ] Shows income/expenses

### Cash Flow Report
- [ ] Data displays

---

## SCORE

**Total Tests:** 80
**Passed:** _____ / 80
**Failed:** _____ / 80
**Completion:** _____ %

---

## ISSUES FOUND

| # | Module | Issue Description | Screenshot |
|---|--------|-------------------|------------|
| 1 |        |                   |            |
| 2 |        |                   |            |
| 3 |        |                   |            |
| 4 |        |                   |            |
| 5 |        |                   |            |

---

**If you find issues, report them and I will fix immediately!**
