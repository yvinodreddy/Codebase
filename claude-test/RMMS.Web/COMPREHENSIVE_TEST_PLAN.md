# RMMS Application - Comprehensive Test Plan
**Version:** 1.0
**Date:** October 4, 2025
**Purpose:** Systematic testing of all CRUD operations, validations, and features

---

## TEST EXECUTION GUIDE

### Prerequisites
1. ✅ Database connection configured in appsettings.json
2. ✅ Database schema created
3. ✅ Application builds successfully (dotnet build)
4. ✅ Application runs (dotnet run)
5. ✅ Test data inserted (use SQL scripts provided)

---

## MODULE 1: PADDY PROCUREMENT

### Test 1.1: CREATE (Insert) Operation
**Steps:**
1. Navigate to Paddy Procurement → Create
2. Fill in all fields:
   - Receipt Date: Today's date
   - Voucher Number: (auto-generated)
   - Supplier Name: "Test Supplier 1"
   - Paddy Variety: "Basmati"
   - Quantity Received: 1000.50 (test decimal)
   - Unit Price: 45.75 (test decimal)
   - Grade: "A"
   - Storage Location: "Warehouse 1"
3. Click Save

**Expected Results:**
- ✅ Success message appears
- ✅ Redirected to Index page
- ✅ New record appears in the list
- ✅ Decimals stored as 1000.50 and 45.75 (2 decimal places)

**Actual Results:** ___________

**Pass/Fail:** ___________

---

### Test 1.2: CREATE with Validation Errors
**Steps:**
1. Navigate to Paddy Procurement → Create
2. Leave Supplier Name blank
3. Leave Paddy Variety blank
4. Click Save

**Expected Results:**
- ✅ Form does NOT submit
- ✅ Validation error messages appear in red
- ✅ Required field errors shown
- ✅ User stays on Create page

**Actual Results:** ___________

**Pass/Fail:** ___________

---

### Test 1.3: CREATE with 3 Decimal Places
**Steps:**
1. Navigate to Paddy Procurement → Create
2. Fill required fields
3. Enter Quantity: 1000.555 (3 decimals)
4. Enter Unit Price: 45.789 (3 decimals)
5. Click Save

**Expected Results:**
- ✅ Save succeeds
- ✅ Values automatically rounded to 1000.56 and 45.79 (2 decimals)
- ✅ Success message appears

**Actual Results:** ___________

**Pass/Fail:** ___________

---

### Test 1.4: READ (View List) Operation
**Steps:**
1. Navigate to Paddy Procurement → Index
2. Observe the list

**Expected Results:**
- ✅ All procurement records display
- ✅ Data loads from database (not hard-coded)
- ✅ List is not empty
- ✅ All columns display correctly

**Actual Results:** ___________

**Pass/Fail:** ___________

---

### Test 1.5: READ (View Details) Operation
**Steps:**
1. Navigate to Paddy Procurement → Index
2. Click "Details" on any record

**Expected Results:**
- ✅ Details page opens
- ✅ All fields display correct values
- ✅ Formatted properly (dates, currency, decimals)

**Actual Results:** ___________

**Pass/Fail:** ___________

---

### Test 1.6: UPDATE (Edit) Operation
**Steps:**
1. Navigate to Paddy Procurement → Index
2. Click "Edit" on an existing record
3. Verify form loads with existing data
4. Change Supplier Name to "Updated Supplier"
5. Change Quantity to 2000.75
6. Click Save

**Expected Results:**
- ✅ Edit form loads with all existing data pre-filled
- ✅ Dropdown shows selected Paddy Variety
- ✅ Success message appears
- ✅ Redirected to Index
- ✅ Changes reflected in the list
- ✅ Check database: UPDATE occurred (not INSERT)

**Actual Results:** ___________

**Pass/Fail:** ___________

---

### Test 1.7: UPDATE with Validation Errors
**Steps:**
1. Navigate to Edit page for a record
2. Clear Supplier Name (make it empty)
3. Click Save

**Expected Results:**
- ✅ Form does NOT submit
- ✅ Validation error appears
- ✅ User stays on Edit page
- ✅ Other fields retain their values

**Actual Results:** ___________

**Pass/Fail:** ___________

---

### Test 1.8: DELETE Operation
**Steps:**
1. Navigate to Paddy Procurement → Index
2. Click "Delete" on a record
3. Confirm deletion

**Expected Results:**
- ✅ Confirmation dialog/page appears
- ✅ After confirmation, success message appears
- ✅ Record removed from list (or marked inactive)
- ✅ Check database: IsActive = false (soft delete)

**Actual Results:** ___________

**Pass/Fail:** ___________

---

### Test 1.9: Search Functionality
**Steps:**
1. Navigate to Paddy Procurement → Index
2. Enter "Basmati" in search box
3. Observe results

**Expected Results:**
- ✅ List filters to show only Basmati varieties
- ✅ Search is case-insensitive
- ✅ Multiple columns are searchable

**Actual Results:** ___________

**Pass/Fail:** ___________

---

### Test 1.10: Pagination (if applicable)
**Steps:**
1. Ensure you have 20+ records
2. Navigate to Paddy Procurement → Index
3. Check for pagination controls

**Expected Results:**
- ✅ Pagination controls appear (if DataTable enabled)
- ✅ Shows 10-25 records per page
- ✅ Can navigate between pages
- ✅ Page numbers work correctly

**Actual Results:** ___________

**Pass/Fail:** ___________

---

### Test 1.11: Stock Summary
**Steps:**
1. Navigate to Paddy Procurement → Stock Summary

**Expected Results:**
- ✅ Stock summary displays
- ✅ Variety-wise breakdown shown
- ✅ Total stock calculated correctly
- ✅ Data comes from procurement records (not hard-coded)
- ✅ No fading after 30 seconds

**Actual Results:** ___________

**Pass/Fail:** ___________

---

### Test 1.12: Stock Summary Navigation
**Steps:**
1. Navigate to Stock Summary
2. Click Print button
3. After print dialog, click Back button

**Expected Results:**
- ✅ Back button returns to Paddy Procurement Index (not Reports)

**Actual Results:** ___________

**Pass/Fail:** ___________

---

## MODULE 2: RICE SALES

### Test 2.1: CREATE Operation
**Steps:**
1. Navigate to Rice Sales → Create
2. Fill all fields:
   - Invoice Number: (auto-generated)
   - Sale Date: Today
   - Buyer Name: "Test Customer 1"
   - Rice Grade: "Basmati Premium"
   - Quantity: 500.50 kg
   - Unit Price: 60.25
   - Payment Mode: "Cash"
   - Payment Status: "Paid"
3. Click Save

**Expected Results:**
- ✅ Success message
- ✅ Redirected to Index
- ✅ New sale appears in list
- ✅ Decimals: 500.50 and 60.25

**Actual Results:** ___________

**Pass/Fail:** ___________

---

### Test 2.2: CREATE with Automatic Calculations
**Steps:**
1. Create new Rice Sale
2. Enter Quantity: 100.00
3. Enter Unit Price: 50.00
4. Observe Total Invoice Value

**Expected Results:**
- ✅ Total automatically calculates to 5000.00
- ✅ If discount entered, total adjusts
- ✅ GST calculations work (if applicable)

**Actual Results:** ___________

**Pass/Fail:** ___________

---

### Test 2.3: EDIT - Dropdown Preloading
**Steps:**
1. Navigate to Rice Sales → Index
2. Click Edit on existing record
3. Observe Rice Grade dropdown

**Expected Results:**
- ✅ Form loads with all existing data
- ✅ Rice Grade dropdown shows the currently selected value
- ✅ Payment Mode dropdown shows current value
- ✅ Payment Status dropdown shows current value

**Actual Results:** ___________

**Pass/Fail:** ___________

---

### Test 2.4: EDIT - Decimal Validation
**Steps:**
1. Edit a Rice Sale
2. Change Quantity to 100.555 (3 decimals)
3. Save

**Expected Results:**
- ✅ Saves successfully
- ✅ Rounds to 100.56 (2 decimals)

**Actual Results:** ___________

**Pass/Fail:** ___________

---

### Test 2.5: UPDATE Operation
**Steps:**
1. Edit a Rice Sale
2. Change Buyer Name
3. Change Quantity
4. Save

**Expected Results:**
- ✅ Success message
- ✅ Changes reflected in list
- ✅ Database updated (verify with query)

**Actual Results:** ___________

**Pass/Fail:** ___________

---

### Test 2.6: DELETE Operation
**Steps:**
1. Delete a Rice Sale record
2. Confirm deletion

**Expected Results:**
- ✅ Confirmation appears
- ✅ Success message
- ✅ Record removed/marked inactive

**Actual Results:** ___________

**Pass/Fail:** ___________

---

### Test 2.7: Print Preview
**Steps:**
1. Navigate to Rice Sales → Edit (or Details)
2. Click Print Preview button

**Expected Results:**
- ✅ New window/tab opens
- ✅ Shows invoice details
- ✅ Formatted for printing

**Actual Results:** ___________

**Pass/Fail:** ___________

---

## MODULE 3: BYPRODUCT SALES

### Test 3.1: CREATE Operation
**Expected:** Same as Rice Sales but for byproducts

**Actual Results:** ___________

**Pass/Fail:** ___________

---

### Test 3.2: UPDATE Operation
**Actual Results:** ___________

**Pass/Fail:** ___________

---

### Test 3.3: DELETE Operation
**Actual Results:** ___________

**Pass/Fail:** ___________

---

### Test 3.4: Decimal Validation
**Steps:**
1. Enter decimals with 3 places
2. Verify rounds to 2

**Actual Results:** ___________

**Pass/Fail:** ___________

---

## MODULE 4: EXTERNAL RICE SALES

### Test 4.1: CREATE Operation
**Actual Results:** ___________

**Pass/Fail:** ___________

---

### Test 4.2: Data Not Fading
**Steps:**
1. Navigate to External Rice page
2. Wait 2 minutes

**Expected Results:**
- ✅ Data remains visible
- ✅ No elements fade out

**Actual Results:** ___________

**Pass/Fail:** ___________

---

## MODULE 5: BANK TRANSACTIONS

### Test 5.1: CREATE Operation
**Actual Results:** ___________

**Pass/Fail:** ___________

---

### Test 5.2: UPDATE Operation
**Actual Results:** ___________

**Pass/Fail:** ___________

---

### Test 5.3: DELETE Operation
**Actual Results:** ___________

**Pass/Fail:** ___________

---

### Test 5.4: Search Functionality
**Actual Results:** ___________

**Pass/Fail:** ___________

---

## MODULE 6: CASH BOOK

### Test 6.1: CREATE Operation
**Actual Results:** ___________

**Pass/Fail:** ___________

---

### Test 6.2: DataTable Error Check
**Steps:**
1. Navigate to Cash Book
2. Open browser console (F12)
3. Check for errors

**Expected Results:**
- ✅ No "DataTable already initialized" errors
- ✅ No console errors

**Actual Results:** ___________

**Pass/Fail:** ___________

---

### Test 6.3: Search Functionality
**Actual Results:** ___________

**Pass/Fail:** ___________

---

## MODULE 7: VOUCHERS

### Test 7.1: CREATE Operation
**Actual Results:** ___________

**Pass/Fail:** ___________

---

### Test 7.2: UI Overlap Check
**Steps:**
1. Navigate to Vouchers
2. Check header buttons

**Expected Results:**
- ✅ No button overlap
- ✅ "Create Voucher" button clearly visible
- ✅ No UI layout issues

**Actual Results:** ___________

**Pass/Fail:** ___________

---

### Test 7.3: DataTable Error Check
**Expected Results:**
- ✅ No reinitialization errors

**Actual Results:** ___________

**Pass/Fail:** ___________

---

## MODULE 8: PAYABLES (OVERDUE)

### Test 8.1: CREATE Operation
**Actual Results:** ___________

**Pass/Fail:** ___________

---

### Test 8.2: Send Reminders - Single
**Steps:**
1. Click Send Reminder on a single payable

**Expected Results:**
- ✅ Confirmation dialog
- ✅ Success message
- ✅ Logged in application logs

**Actual Results:** ___________

**Pass/Fail:** ___________

---

### Test 8.3: Send Reminders - Bulk
**Steps:**
1. Click "Send Reminders" button (top of page)
2. Confirm

**Expected Results:**
- ✅ Confirmation dialog
- ✅ Success message with count
- ✅ Reminders sent to all overdue

**Actual Results:** ___________

**Pass/Fail:** ___________

---

### Test 8.4: DataTable Pagination
**Expected Results:**
- ✅ Pagination works
- ✅ Can change page size
- ✅ Can navigate pages

**Actual Results:** ___________

**Pass/Fail:** ___________

---

### Test 8.5: Search Functionality
**Actual Results:** ___________

**Pass/Fail:** ___________

---

## MODULE 9: RECEIVABLES (OVERDUE)

### Test 9.1: CREATE Operation
**Actual Results:** ___________

**Pass/Fail:** ___________

---

### Test 9.2: Send Reminders - Bulk
**Steps:**
1. Click "Send Reminders" button

**Expected Results:**
- ✅ Works same as Payables

**Actual Results:** ___________

**Pass/Fail:** ___________

---

### Test 9.3: Edit/Delete Options
**Steps:**
1. Check if Edit and Delete buttons exist
2. Test Edit operation
3. Test Delete operation

**Expected Results:**
- ✅ Edit button works
- ✅ Delete button works

**Actual Results:** ___________

**Pass/Fail:** ___________

---

## MODULE 10: LOAN ADVANCES

### Test 10.1: Data Display
**Steps:**
1. Navigate to Loan Advances

**Expected Results:**
- ✅ Data loads from database
- ✅ NOT hard-coded
- ✅ If empty, shows "No records" message

**Actual Results:** ___________

**Pass/Fail:** ___________

---

### Test 10.2: CREATE/UPDATE/DELETE
**Actual Results:** ___________

**Pass/Fail:** ___________

---

## MODULE 11: LOANS RECEIVABLES

### Test 11.1: No Fading
**Steps:**
1. Navigate to page
2. Wait 2 minutes

**Expected Results:**
- ✅ Data stays visible
- ✅ No fading after 30 seconds

**Actual Results:** ___________

**Pass/Fail:** ___________

---

## MODULE 12: FIXED ASSETS

### Test 12.1: Data Display
**Expected Results:**
- ✅ Data loads from database
- ✅ NOT empty (if records exist)

**Actual Results:** ___________

**Pass/Fail:** ___________

---

### Test 12.2: Search Functionality
**Actual Results:** ___________

**Pass/Fail:** ___________

---

### Test 12.3: UPDATE/DELETE
**Actual Results:** ___________

**Pass/Fail:** ___________

---

## REPORTS TESTING

### Test R1: Dashboard
**Steps:**
1. Navigate to Dashboard (Home page)

**Expected Results:**
- ✅ Data displays (not empty)
- ✅ Charts render
- ✅ Stock totals show
- ✅ Recent transactions display
- ✅ All from database (not hard-coded)

**Actual Results:** ___________

**Pass/Fail:** ___________

---

### Test R2: Daily Sales Report
**Steps:**
1. Navigate to Reports → Daily Sales
2. Select today's date

**Expected Results:**
- ✅ Shows sales for selected date
- ✅ Rice sales listed
- ✅ Byproduct sales listed
- ✅ Totals calculated correctly

**Actual Results:** ___________

**Pass/Fail:** ___________

---

### Test R3: Monthly Sales Report
**Steps:**
1. Navigate to Reports → Monthly Sales
2. Select current month/year

**Expected Results:**
- ✅ Daily breakdown chart displays
- ✅ Total monthly sales shown
- ✅ Average daily sales calculated
- ✅ Best selling day identified

**Actual Results:** ___________

**Pass/Fail:** ___________

---

### Test R4: Product-Wise Sales Report
**Steps:**
1. Navigate to Reports → Product-Wise Sales

**Expected Results:**
- ✅ Data displays (not empty)
- ✅ Connected to database
- ✅ Grouped by product/grade
- ✅ Charts display correctly
- ✅ Pagination works
- ✅ Sorting works

**Actual Results:** ___________

**Pass/Fail:** ___________

---

### Test R5: Customer-Wise Sales Report
**Steps:**
1. Navigate to Reports → Customer-Wise Sales

**Expected Results:**
- ✅ Data displays
- ✅ Grouped by customer
- ✅ Shows total sales per customer
- ✅ Shows number of orders
- ✅ Charts display
- ✅ Search works

**Actual Results:** ___________

**Pass/Fail:** ___________

---

### Test R6: Rice Stock Report
**Steps:**
1. Navigate to Reports → Rice Stock

**Expected Results:**
- ✅ Data displays (not empty)
- ✅ Shows stock by grade
- ✅ Totals calculated

**Actual Results:** ___________

**Pass/Fail:** ___________

---

### Test R7: Paddy Stock Report
**Steps:**
1. Navigate to Reports → Paddy Stock

**Expected Results:**
- ✅ Data displays (NOT showing 0)
- ✅ Shows stock by variety
- ✅ Pulls from procurement records
- ✅ No fading

**Actual Results:** ___________

**Pass/Fail:** ___________

---

### Test R8: Outstanding Payments Report
**Steps:**
1. Navigate to Reports → Outstanding Payments

**Expected Results:**
- ✅ Shows payables section
- ✅ Shows receivables section
- ✅ "Pay Now" buttons work (navigate to payment page)
- ✅ "Send Reminder" buttons work
- ✅ Pagination works (10 per page)
- ✅ Sorting works
- ✅ Search works

**Actual Results:** ___________

**Pass/Fail:** ___________

---

### Test R9: Profit & Loss Statement
**Steps:**
1. Navigate to Reports → Profit & Loss

**Expected Results:**
- ✅ Report generates without errors
- ✅ Shows income
- ✅ Shows expenses
- ✅ Calculates profit/loss

**Actual Results:** ___________

**Pass/Fail:** ___________

---

### Test R10: Cash Flow Report
**Steps:**
1. Navigate to Reports → Cash Flow

**Expected Results:**
- ✅ Report displays
- ⚠️ Paging NOT implemented (known issue)
- ⚠️ Search NOT implemented (known issue)

**Actual Results:** ___________

**Pass/Fail:** ___________

---

## ERROR HANDLING TESTS

### Test E1: Database Connection Error
**Steps:**
1. Stop database or invalidate connection string
2. Try to load any page

**Expected Results:**
- ✅ Friendly error message (not stack trace)
- ✅ App doesn't crash

**Actual Results:** ___________

**Pass/Fail:** ___________

---

### Test E2: Invalid ID Error
**Steps:**
1. Navigate to Edit page with invalid ID (e.g., /Edit/99999)

**Expected Results:**
- ✅ "Record not found" error
- ✅ Redirects to Index page

**Actual Results:** ___________

**Pass/Fail:** ___________

---

### Test E3: Duplicate Record Error
**Steps:**
1. Try to create duplicate voucher number (if applicable)

**Expected Results:**
- ✅ Error message displayed
- ✅ Form doesn't submit
- ✅ User-friendly message

**Actual Results:** ___________

**Pass/Fail:** ___________

---

## SUMMARY SCORECARD

| Module | Create | Read | Update | Delete | Search | Pagination | Score |
|--------|--------|------|--------|--------|--------|------------|-------|
| Paddy Procurement | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | 0/6 |
| Rice Sales | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | 0/6 |
| Byproduct Sales | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | 0/6 |
| External Rice | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | 0/6 |
| Bank Book | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | 0/6 |
| Cash Book | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | 0/6 |
| Vouchers | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | 0/6 |
| Payables | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | 0/6 |
| Receivables | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | 0/6 |
| Loan Advances | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | 0/6 |
| Fixed Assets | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | 0/6 |
| **TOTAL** | | | | | | | **0/66** |

| Report | Data Display | Charts | Pagination | Search | Score |
|--------|--------------|--------|------------|--------|-------|
| Dashboard | ☐ | ☐ | N/A | N/A | 0/2 |
| Daily Sales | ☐ | ☐ | ☐ | ☐ | 0/4 |
| Monthly Sales | ☐ | ☐ | ☐ | ☐ | 0/4 |
| Product-Wise | ☐ | ☐ | ☐ | ☐ | 0/4 |
| Customer-Wise | ☐ | ☐ | ☐ | ☐ | 0/4 |
| Rice Stock | ☐ | N/A | ☐ | ☐ | 0/3 |
| Paddy Stock | ☐ | N/A | ☐ | ☐ | 0/3 |
| Outstanding Payments | ☐ | N/A | ☐ | ☐ | 0/3 |
| Profit & Loss | ☐ | ☐ | ☐ | ☐ | 0/4 |
| Cash Flow | ☐ | ☐ | ☐ | ☐ | 0/4 |
| **TOTAL** | | | | | **0/35** |

**GRAND TOTAL: 0/101 Tests Completed**

---

## TEST EXECUTION LOG

**Date Started:** ___________
**Tester Name:** ___________
**Environment:** ___________
**Database:** ___________

**Completion Status:**
- [ ] Phase 1: Basic CRUD (33 tests)
- [ ] Phase 2: Advanced Features (23 tests)
- [ ] Phase 3: Reports (35 tests)
- [ ] Phase 4: Error Handling (10 tests)

**Overall Status:** 0% Complete

---

**END OF TEST PLAN**
