# RMMS Runtime Testing Plan

## Prerequisites

### 1. Database Setup
- [ ] SQL Server instance running
- [ ] Update connection string in `appsettings.json` (line 5)
- [ ] Execute database schema creation scripts
- [ ] Execute stored procedures creation scripts
- [ ] Verify all required tables exist
- [ ] Seed initial test data (optional)

### 2. Configuration
- [ ] Update `DefaultState` in appsettings.json (currently "YourState")
- [ ] Verify `AppSettings` section values
- [ ] Ensure log file directory has write permissions

### 3. Application Start
- [ ] Run: `dotnet run` from RMMS.Web directory
- [ ] Verify application starts without errors
- [ ] Access https://localhost:5001 (or configured port)
- [ ] Check console for any startup errors

---

## Test Categories

### Category 1: Authentication & Authorization

#### Test 1.1: User Login
- **URL**: `/Account/Login`
- **Steps**:
  1. Navigate to login page
  2. Enter valid credentials
  3. Click login button
- **Expected**: Redirect to dashboard, no errors
- **Verify**: User session established, name displayed in header

#### Test 1.2: Invalid Login
- **Steps**: Enter invalid credentials
- **Expected**: Error message displayed, remains on login page

#### Test 1.3: Logout
- **Steps**: Click logout
- **Expected**: Redirect to login, session cleared

#### Test 1.4: Protected Page Access
- **Steps**: Access /Dashboard/Index without login
- **Expected**: Redirect to login page

---

### Category 2: Dashboard

#### Test 2.1: Dashboard Load
- **URL**: `/Dashboard/Index`
- **Steps**: Navigate to dashboard after login
- **Expected**:
  - Page loads without blank screen
  - Stock summary displays
  - Charts render (monthly sales, procurement)
  - Quick stats show numbers
- **Verify**: No console errors, all widgets populated

#### Test 2.2: Dashboard with No Data
- **Steps**: Load dashboard with empty database
- **Expected**:
  - Page still loads
  - Shows zero values (not errors)
  - No crash

#### Test 2.3: Dashboard SQL Error Handling
- **Steps**: Temporarily break database connection
- **Expected**:
  - Page loads with error alert
  - Shows safe default values (0s)
  - Application doesn't crash

---

### Category 3: Paddy Procurement

#### Test 3.1: View All Procurements
- **URL**: `/PaddyProcurement/Index`
- **Steps**: Navigate to procurement list
- **Expected**: List displays (empty or with records), no blank page
- **Verify**: Table renders, search box works

#### Test 3.2: Create New Procurement
- **URL**: `/PaddyProcurement/Create`
- **Steps**:
  1. Click "Add New Procurement"
  2. Fill all required fields
  3. Submit form
- **Expected**:
  - Record saved to database
  - Redirect to Index
  - Success message displayed
  - New record appears in list

#### Test 3.3: Create with Invalid Data
- **Steps**: Submit form with missing required fields
- **Expected**: Validation errors displayed, form not submitted

#### Test 3.4: Edit Existing Procurement
- **URL**: `/PaddyProcurement/Edit/{id}`
- **Steps**:
  1. Click edit on existing record
  2. Modify fields
  3. Submit
- **Expected**: Changes saved, record updated in database

#### Test 3.5: Delete Procurement
- **Steps**: Click delete, confirm
- **Expected**:
  - Record marked as inactive (IsActive = false)
  - Removed from list
  - Database record retained

#### Test 3.6: View Details
- **URL**: `/PaddyProcurement/Details/{id}`
- **Steps**: Click details/view on record
- **Expected**: All procurement details displayed correctly

---

### Category 4: Rice Sales

#### Test 4.1: View All Sales
- **URL**: `/RiceSales/Index`
- **Expected**: Sales list loads, no null reference exceptions

#### Test 4.2: Create Sale with GST Calculation
- **URL**: `/RiceSales/Create`
- **Steps**:
  1. Fill sale details
  2. Enter buyer address with state
  3. Submit
- **Expected**:
  - GST calculated correctly (CGST+SGST or IGST)
  - Uses DefaultState from configuration
  - Record saved

#### Test 4.3: Create Sale - Intrastate
- **Steps**: Create sale with buyer in same state as DefaultState
- **Expected**: CGST and SGST calculated (split GST)

#### Test 4.4: Create Sale - Interstate
- **Steps**: Create sale with buyer in different state
- **Expected**: IGST calculated (full GST rate)

#### Test 4.5: Generate Invoice
- **Steps**: Click "Generate Invoice" on sale record
- **Expected**: Invoice displays with correct calculations

---

### Category 5: By-Product Sales (Thread Safety Testing)

#### Test 5.1: Create Multiple Sales Rapidly
- **URL**: `/ByProductSales/Create`
- **Steps**:
  1. Open page in multiple browser tabs
  2. Submit forms simultaneously from different tabs
- **Expected**:
  - All records saved correctly
  - No duplicate IDs
  - No data corruption
- **Verify**: Lock statements prevent race conditions

#### Test 5.2: Update Same Record Concurrently
- **Steps**:
  1. Open same record for editing in 2 tabs
  2. Submit changes from both tabs
- **Expected**:
  - Last write wins
  - No exception thrown
  - Data remains consistent

---

### Category 6: Cash Book

#### Test 6.1: View Cash Book
- **URL**: `/CashBook/Index`
- **Expected**:
  - List displays
  - Print button works (window.print())
  - Current balance calculated correctly

#### Test 6.2: Create Cash Entry
- **URL**: `/CashBook/Create`
- **Steps**:
  1. Create receipt entry (Receipts > 0, Payments = 0)
  2. Create payment entry (Payments > 0, Receipts = 0)
- **Expected**:
  - Running balance calculated correctly
  - Balance = previous balance + receipts - payments

#### Test 6.3: Balance Recalculation on Update
- **Steps**:
  1. Create 3 entries with running balance
  2. Edit the 2nd entry (change amount)
  3. Save
- **Expected**:
  - All subsequent balances recalculated
  - Final balance correct

#### Test 6.4: Balance Recalculation on Delete
- **Steps**:
  1. Delete middle entry from cash book
  2. Check balances
- **Expected**: All balances recalculated, entries after deletion adjusted

#### Test 6.5: Get Current Balance
- **Steps**: Call GetCurrentBalance() via any page showing balance
- **Expected**: Correct sum of all active entries

---

### Category 7: Bank Transactions

#### Test 7.1: View Bank Transactions
- **URL**: `/BankTransactions/Index`
- **Expected**:
  - List displays
  - Reconcile button works (alert appears)

#### Test 7.2: Bank Reconciliation
- **Steps**: Click "Reconcile Bank" button
- **Expected**: Confirmation dialog appears (currently mock functionality)

---

### Category 8: Payables Overdue (Financial Validation)

#### Test 8.1: View Overdue Payables
- **URL**: `/PayablesOverdue/Index`
- **Expected**: List of overdue payables, sorted by days overdue

#### Test 8.2: Record Payment - Valid Amount
- **Steps**:
  1. Find payable with BalancePayable = $1000
  2. Record payment of $500
- **Expected**:
  - Payment accepted
  - AmountPaid increases by $500
  - BalancePayable = $500

#### Test 8.3: Record Payment - Negative Amount
- **Steps**: Attempt to record payment of -$100
- **Expected**:
  - Exception thrown
  - Error message: "Payment amount must be greater than zero."
  - Record not modified

#### Test 8.4: Record Payment - Zero Amount
- **Steps**: Attempt to record payment of $0
- **Expected**: Exception, amount must be > 0

#### Test 8.5: Record Payment - Exceeds Balance
- **Steps**:
  1. Payable has BalancePayable = $500
  2. Attempt payment of $600
- **Expected**:
  - Exception thrown
  - Error: "Payment amount ($600.00) cannot exceed balance payable ($500.00)"
  - Record not modified

#### Test 8.6: Record Payment - Exact Balance
- **Steps**: Record payment equal to BalancePayable
- **Expected**:
  - Payment accepted
  - BalancePayable = $0
  - Payable fully paid

---

### Category 9: Receivables Overdue (Financial Validation)

#### Test 9.1: Record Receipt - Valid Amount
- **URL**: `/ReceivablesOverdue`
- **Steps**: Record receipt for $300 against BalanceDue of $1000
- **Expected**:
  - Receipt recorded
  - AmountReceived increases
  - BalanceDue decreases

#### Test 9.2: Record Receipt - Negative Amount
- **Expected**: Exception, "Receipt amount must be greater than zero."

#### Test 9.3: Record Receipt - Exceeds Balance Due
- **Steps**: Record receipt > BalanceDue
- **Expected**: Exception with formatted amounts

#### Test 9.4: Get Overdue Receivables
- **Steps**: Call GetOverdueReceivables()
- **Expected**: Only returns records where DaysOverdue > 0 and IsActive = true

#### Test 9.5: Get Total Outstanding
- **Expected**: Correct sum of all active BalanceDue amounts

#### Test 9.6: Search by Customer Name
- **Steps**: Use GetByCustomer("John")
- **Expected**: Case-insensitive partial match, returns all matching customers

---

### Category 10: Loans & Advances (Financial Validation)

#### Test 10.1: Record Repayment - Valid Amount
- **URL**: `/LoansAdvances`
- **Steps**: Record repayment of $200 against Balance of $1000
- **Expected**:
  - Repayment recorded
  - Balance decreases to $800
  - RepaymentDate updated

#### Test 10.2: Record Repayment - Negative Amount
- **Expected**: Exception thrown

#### Test 10.3: Record Repayment - Exceeds Balance
- **Steps**: Attempt repayment > current Balance
- **Expected**:
  - Exception: "Repayment amount ($X) cannot exceed loan balance ($Y)"
  - Record unchanged

#### Test 10.4: Get Outstanding Loans
- **Expected**: Returns only loans where Balance > 0 and IsActive = true

---

### Category 11: Fixed Assets

#### Test 11.1: Create Fixed Asset
- **URL**: `/FixedAssets/Create`
- **Steps**: Create asset with purchase details
- **Expected**: Asset saved, thread-safe ID assignment

#### Test 11.2: Concurrent Asset Creation
- **Steps**: Create multiple assets simultaneously
- **Expected**: No ID collisions, all records saved correctly

---

### Category 12: Vouchers

#### Test 12.1: Create Voucher
- **URL**: `/Vouchers/Create`
- **Expected**: Voucher created with thread-safe operations

#### Test 12.2: View Vouchers by Date
- **Steps**: Filter vouchers by date range
- **Expected**: Correct filtering, no exceptions

---

### Category 13: Settings

#### Test 13.1: View Settings Page
- **URL**: `/Settings/Index`
- **Expected**:
  - Page loads
  - Forms display
  - Alert messages indicate pending implementation

#### Test 13.2: Profile Settings
- **Steps**: Try to update profile
- **Expected**: Alert: "Profile settings are not saved yet. Backend implementation is pending."

#### Test 13.3: Password Change
- **Steps**: Try to change password
- **Expected**: Alert: "Password change is not implemented yet. Backend integration is pending."

#### Test 13.4: Preferences
- **Steps**: Try to save preferences
- **Expected**: Alert about pending implementation

---

### Category 14: SQL Exception Handling

#### Test 14.1: Database Connection Lost
- **Steps**:
  1. Stop SQL Server while app is running
  2. Try to access any database-backed page
- **Expected**:
  - Descriptive error message
  - Application doesn't crash
  - Exception wrapped with context

#### Test 14.2: Invalid SQL Query
- **Steps**: Trigger scenario that causes SQL error (if possible)
- **Expected**: SqlException caught, wrapped, re-thrown with message

#### Test 14.3: Dashboard Graceful Degradation
- **Steps**: Break dashboard data retrieval
- **Expected**:
  - Page loads with error alert
  - Shows safe defaults (zeros)
  - Doesn't crash entire app

---

### Category 15: Navigation & UI

#### Test 15.1: Main Menu Navigation
- **Steps**: Click each main menu item
- **Expected**: All pages load without blank screens

#### Test 15.2: Breadcrumbs
- **Steps**: Navigate through Create → Index flows
- **Expected**: Breadcrumbs accurate, clickable

#### Test 15.3: Search Functionality
- **Steps**: Use search boxes on Index pages
- **Expected**: Results filter correctly

#### Test 15.4: Pagination
- **Steps**: If >10 records, test pagination
- **Expected**: Page navigation works

---

### Category 16: Data Validation

#### Test 16.1: Required Fields
- **Steps**: Submit forms with missing required fields
- **Expected**: Validation errors, form not submitted

#### Test 16.2: Data Type Validation
- **Steps**: Enter text in numeric fields
- **Expected**: Validation error

#### Test 16.3: Date Validation
- **Steps**: Enter invalid dates
- **Expected**: Validation error or date picker prevents invalid input

---

### Category 17: Performance & Concurrency

#### Test 17.1: Load Testing - Multiple Users
- **Tool**: Use browser dev tools or simple load testing tool
- **Steps**: Simulate 10+ concurrent users
- **Expected**: No deadlocks, all requests handled

#### Test 17.2: Large Dataset Performance
- **Steps**: Load pages with 1000+ records
- **Expected**: Reasonable load time, no timeout

#### Test 17.3: Thread Safety Stress Test
- **Steps**:
  1. Write script to hammer in-memory services
  2. Create/Update/Delete operations concurrently
- **Expected**: No race conditions, no data corruption

---

## Test Execution Checklist

### Phase 1: Basic Functionality (Priority: High)
- [ ] Application starts successfully
- [ ] Login/Logout works
- [ ] Dashboard loads without blank page
- [ ] All main pages load (no blank screens)
- [ ] Navigation menu functional

### Phase 2: CRUD Operations (Priority: High)
- [ ] Paddy Procurement: Create, Read, Update, Delete
- [ ] Rice Sales: Create, Read, Update, Delete
- [ ] By-Product Sales: Create, Read, Update, Delete
- [ ] Cash Book: Create, Read, Update, Delete
- [ ] Bank Transactions: Create, Read, Update, Delete

### Phase 3: Financial Validations (Priority: Critical)
- [ ] Payables: Payment validation (negative, zero, exceeds balance)
- [ ] Receivables: Receipt validation (negative, zero, exceeds balance)
- [ ] Loans: Repayment validation (negative, zero, exceeds balance)
- [ ] Balance calculations correct

### Phase 4: Error Handling (Priority: Critical)
- [ ] SQL exceptions handled gracefully
- [ ] Null reference exceptions eliminated
- [ ] DBNull handling in dashboard
- [ ] Dashboard graceful degradation

### Phase 5: Thread Safety (Priority: High)
- [ ] Concurrent operations on in-memory services
- [ ] No data corruption under concurrent load
- [ ] No duplicate IDs generated

### Phase 6: Advanced Features (Priority: Medium)
- [ ] GST calculations (intrastate vs interstate)
- [ ] Cash book balance recalculation
- [ ] Search and filter functionality
- [ ] Report generation

---

## Known Issues to Monitor

1. **Unused Exception Variables**: 12 compiler warnings in DashboardService - acceptable for graceful degradation
2. **JavaScript Functionality**: reconcileBank() and printCashBook() are mock implementations
3. **Settings Page**: All forms show alerts about pending implementation
4. **Configuration**: DefaultState must be updated from "YourState" to actual value

---

## Success Criteria

✅ **Application is production-ready when:**
1. All Phase 1-4 tests pass
2. No blank pages occur
3. No unhandled exceptions crash the app
4. Financial validations prevent invalid transactions
5. Thread safety confirmed under concurrent load
6. Data integrity maintained across all operations
7. Database operations handle errors gracefully

---

## Test Reporting

### For Each Failed Test:
1. Test ID and name
2. Steps to reproduce
3. Expected result
4. Actual result
5. Error messages / stack trace
6. Screenshot (if applicable)
7. Severity: Critical / High / Medium / Low

### Summary Metrics:
- Total tests planned: 80+
- Tests passed: ___
- Tests failed: ___
- Tests blocked: ___
- Pass rate: ___%
- Critical issues found: ___

---

## Testing Tools Recommended

1. **Manual Testing**: Primary method for this plan
2. **Browser DevTools**: Console errors, network requests
3. **SQL Server Profiler**: Monitor database queries
4. **Postman**: API endpoint testing (if applicable)
5. **xUnit / NUnit**: Unit tests (future enhancement)
6. **Selenium**: Automated UI testing (future enhancement)

---

## Next Steps After Testing

1. Document all issues found
2. Prioritize fixes (Critical → High → Medium → Low)
3. Fix issues in order of priority
4. Re-test after fixes
5. Perform regression testing
6. Deploy to staging environment
7. User acceptance testing (UAT)
8. Deploy to production
