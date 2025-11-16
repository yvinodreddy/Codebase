# RMMS Phase 2: Manual Functional Testing Checklist

**Generated**: $(date)
**Application URL**: http://localhost:5090
**Default Credentials**: admin / admin@123

---

## TESTING INSTRUCTIONS

Complete each test case below and mark as ✅ PASS or ❌ FAIL.

---

## 1. AUTHENTICATION TESTING (SEC-AUTH Series)

### SEC-AUTH-001: Login with valid credentials
- [ ] Navigate to http://localhost:5090
- [ ] Enter username: `admin`
- [ ] Enter password: `admin@123`
- [ ] Click Login
- [ ] **Expected**: Redirected to Dashboard
- [ ] **Result**: _____

### SEC-AUTH-002: Login with invalid username
- [ ] Navigate to /Account/Login
- [ ] Enter username: `nonexistent`
- [ ] Enter password: `anything`
- [ ] Click Login
- [ ] **Expected**: Error message "Invalid credentials"
- [ ] **Result**: _____

### SEC-AUTH-003: Login with invalid password
- [ ] Navigate to /Account/Login
- [ ] Enter username: `admin`
- [ ] Enter password: `wrongpassword`
- [ ] Click Login
- [ ] **Expected**: Error message "Invalid credentials"
- [ ] **Result**: _____

### SEC-AUTH-007: Session timeout
- [ ] Login successfully
- [ ] Wait 30+ minutes idle
- [ ] Try to navigate to any page
- [ ] **Expected**: Redirected to login
- [ ] **Result**: _____

### SEC-AUTHZ-001: Access protected page without login
- [ ] Logout if logged in
- [ ] Navigate directly to /PaddyProcurement
- [ ] **Expected**: Redirected to /Account/Login
- [ ] **Result**: _____

---

## 2. PADDY PROCUREMENT MODULE (FUNC-PP Series)

### FUNC-PP-001: Create paddy procurement record
- [ ] Login as admin
- [ ] Navigate to Paddy Procurement
- [ ] Click "New Procurement"
- [ ] Fill all required fields:
  - Receipt Date: (today's date)
  - Voucher Number: TEST-001
  - Supplier Name: Test Supplier
  - Paddy Variety: Basmati
  - Quantity Received: 1000
  - Total Net Weight: 950
- [ ] Click Save
- [ ] **Expected**: Record created, redirected to Index
- [ ] **Result**: _____

### FUNC-PP-002: Edit paddy procurement record
- [ ] From Paddy Procurement Index
- [ ] Click Edit on any record
- [ ] Change Supplier Name to "Updated Supplier"
- [ ] Click Save
- [ ] **Expected**: Record updated
- [ ] **Result**: _____

### FUNC-PP-003: Delete paddy procurement record
- [ ] From Paddy Procurement Index
- [ ] Click Delete on test record
- [ ] Confirm deletion
- [ ] **Expected**: Record deleted
- [ ] **Result**: _____

### FUNC-PP-004: View paddy procurement details
- [ ] From Index, click View/Details
- [ ] **Expected**: All fields displayed correctly
- [ ] **Result**: _____

### FUNC-PP-005: Search paddy procurement records
- [ ] On Index page, use DataTables search box
- [ ] Enter supplier name
- [ ] **Expected**: Filtered results shown
- [ ] **Result**: _____

### FUNC-PP-006: Pagination works
- [ ] Ensure 10+ records exist
- [ ] **Expected**: Pagination controls visible
- [ ] Click Next page
- [ ] **Expected**: Next set of records shown
- [ ] **Result**: _____

---

## 3. RICE SALES MODULE (FUNC-RS Series)

### FUNC-RS-001: Create rice sales record
- [ ] Navigate to Rice Sales
- [ ] Click New Sale
- [ ] Fill required fields:
  - Sale Date: (today)
  - Invoice Number: INV-001
  - Buyer Name: Test Buyer
  - Rice Grade: Premium
  - Quantity: 500
  - Unit Price: 50
- [ ] Click Save
- [ ] **Expected**: Record created, Gross Invoice Amount calculated
- [ ] **Result**: _____

### FUNC-RS-005: Verify total amount calculation
- [ ] Create sale with Quantity=100, Unit Price=50
- [ ] **Expected**: Total calculated as 5000
- [ ] **Result**: _____

### FUNC-RS-006: Verify GST calculation
- [ ] Check if GST fields are calculated
- [ ] **Expected**: CGST, SGST, or IGST populated
- [ ] **Result**: _____

---

## 4. CASH BOOK MODULE (FUNC-CB Series)

### FUNC-CB-001: Create cash receipt
- [ ] Navigate to Cash Book
- [ ] Click New Transaction
- [ ] Fill:
  - Date: (today)
  - Voucher No: CB-R-001
  - Particulars: Cash received from sale
  - Receipts: 5000
  - Payments: 0
- [ ] Save
- [ ] **Expected**: Receipt recorded
- [ ] **Result**: _____

### FUNC-CB-002: Create cash payment
- [ ] Click New Transaction
- [ ] Fill:
  - Date: (today)
  - Voucher No: CB-P-001
  - Particulars: Office supplies
  - Receipts: 0
  - Payments: 500
- [ ] Save
- [ ] **Expected**: Payment recorded
- [ ] **Result**: _____

### FUNC-CB-005: View cash book balance
- [ ] On Cash Book Index
- [ ] Check summary cards at top
- [ ] **Expected**: Total Receipts, Payments, Current Balance shown
- [ ] **Expected**: Balance = Receipts - Payments
- [ ] **Result**: _____

---

## 5. BANK TRANSACTIONS MODULE (FUNC-BT Series)

### FUNC-BT-001: Create bank credit
- [ ] Navigate to Bank Transactions
- [ ] Click New Transaction
- [ ] Fill:
  - Date: (today)
  - Bank Name: State Bank
  - Account No: 1234567890
  - Particulars: Customer payment
  - Deposits: 10000
  - Withdrawals: 0
- [ ] Save
- [ ] **Expected**: Deposit recorded
- [ ] **Result**: _____

### FUNC-BT-002: Create bank debit
- [ ] Create transaction with Withdrawals > 0
- [ ] **Expected**: Withdrawal recorded
- [ ] **Result**: _____

---

## 6. FIXED ASSETS MODULE (FUNC-FA Series)

### FUNC-FA-001: Create fixed asset
- [ ] Navigate to Fixed Assets
- [ ] Click Add Asset
- [ ] Fill:
  - Asset ID: FA-001
  - Purchase Date: (date)
  - Asset Name: Rice Mill Machine
  - Supplier: ABC Machinery
  - Purchase Value: 500000
  - Depreciation Rate: 10
- [ ] Save
- [ ] **Expected**: Asset created
- [ ] **Result**: _____

### FUNC-FA-005: Calculate depreciation
- [ ] View asset details
- [ ] Check Accumulated Depreciation
- [ ] **Expected**: Depreciation calculated based on rate
- [ ] **Result**: _____

---

## 7. DATATABLES FUNCTIONALITY

### DT-FUNC-001: Pagination
- [ ] On any Index page with 10+ records
- [ ] Change "Show 10 entries" to "Show 25 entries"
- [ ] **Expected**: Page shows 25 records
- [ ] **Result**: _____

### DT-FUNC-002: Search
- [ ] Use search box on Index page
- [ ] Enter search term
- [ ] **Expected**: Results filtered in real-time
- [ ] **Result**: _____

### DT-FUNC-003: Sorting
- [ ] Click column header to sort
- [ ] **Expected**: Data sorted ascending
- [ ] Click again
- [ ] **Expected**: Data sorted descending
- [ ] **Result**: _____

### DT-FUNC-004: Export to Excel
- [ ] Click "Excel" export button
- [ ] **Expected**: Excel file downloads
- [ ] **Result**: _____

### DT-FUNC-005: Export to PDF
- [ ] Click "PDF" export button
- [ ] **Expected**: PDF file downloads
- [ ] **Result**: _____

### DT-FUNC-006: Print
- [ ] Click "Print" button
- [ ] **Expected**: Print dialog opens
- [ ] **Result**: _____

---

## 8. REPORTS MODULE (FUNC-REP Series)

### FUNC-REP-001: Dashboard loads
- [ ] Navigate to / or /Home
- [ ] **Expected**: Dashboard with summary cards
- [ ] **Expected**: Charts load (if implemented)
- [ ] **Result**: _____

### FUNC-REP-002: Daily sales report
- [ ] Navigate to Reports
- [ ] Select Daily Sales Report
- [ ] Choose date
- [ ] **Expected**: Report generated
- [ ] **Result**: _____

### FUNC-REP-007: Stock report
- [ ] Navigate to Stock Summary
- [ ] **Expected**: Stock levels shown
- [ ] **Result**: _____

---

## 9. FORM VALIDATION (DATA-VAL Series)

### DATA-VAL-001: Required field validation
- [ ] On any Create form
- [ ] Leave required fields empty
- [ ] Try to save
- [ ] **Expected**: Validation errors shown
- [ ] **Expected**: Form not submitted
- [ ] **Result**: _____

### DATA-VAL-002: Data type validation
- [ ] Enter text in numeric field (e.g., Quantity)
- [ ] **Expected**: Client-side validation error
- [ ] **Result**: _____

### DATA-VAL-003: Range validation
- [ ] Enter negative number in Quantity
- [ ] **Expected**: Validation error
- [ ] **Result**: _____

### DATA-VAL-004: Date format validation
- [ ] Enter invalid date format
- [ ] **Expected**: Date picker or validation error
- [ ] **Result**: _____

---

## 10. UI/UX TESTING

### UX-USE-002: Navigation is intuitive
- [ ] Test main menu navigation
- [ ] **Expected**: All menu items work
- [ ] **Expected**: Active page highlighted
- [ ] **Result**: _____

### UX-USE-003: Forms are easy to fill
- [ ] Create a record in any module
- [ ] **Expected**: Labels clear, fields logically ordered
- [ ] **Result**: _____

### UX-USE-004: Error messages are helpful
- [ ] Trigger a validation error
- [ ] **Expected**: Error message explains issue
- [ ] **Expected**: Error message in red/highlighted
- [ ] **Result**: _____

### UX-USE-005: Confirmation messages are clear
- [ ] Save a record
- [ ] **Expected**: Success message shown
- [ ] **Result**: _____

---

## 11. RESPONSIVE DESIGN (UX-BROWSER Series)

### Test on Different Screen Sizes

#### Desktop (1920x1080)
- [ ] All pages render correctly
- [ ] DataTables show all columns
- [ ] No horizontal scrolling
- [ ] **Result**: _____

#### Tablet (768px width)
- [ ] Pages adjust to tablet view
- [ ] Tables responsive/scrollable
- [ ] Buttons accessible
- [ ] **Result**: _____

#### Mobile (375px width)
- [ ] Pages adjust to mobile view
- [ ] Navigation becomes hamburger menu
- [ ] Forms stack vertically
- [ ] Tables scrollable
- [ ] **Result**: _____

---

## 12. BROWSER COMPATIBILITY (UX-BROWSER Series)

Test the application in multiple browsers:

### Chrome (Latest)
- [ ] All features work
- [ ] **Result**: _____

### Firefox (Latest)
- [ ] All features work
- [ ] **Result**: _____

### Edge (Latest)
- [ ] All features work
- [ ] **Result**: _____

### Safari (if available)
- [ ] All features work
- [ ] **Result**: _____

---

## SUMMARY

**Total Test Cases**: 50+
**Passed**: _____
**Failed**: _____
**Pass Rate**: _____%

**Critical Issues Found**:
1. _____
2. _____
3. _____

**Recommendations**:
_____

**Tester Name**: __________
**Date Completed**: __________
**Sign-off**: __________

---

## NOTES

- Mark each test as ✅ PASS or ❌ FAIL
- Document any issues in detail
- Take screenshots of errors
- Report all findings in issue tracker

