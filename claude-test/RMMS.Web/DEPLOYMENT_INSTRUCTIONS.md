# 🚀 DEPLOYMENT INSTRUCTIONS - Sprint 1

## Database Setup (REQUIRED BEFORE TESTING)

### Step 1: Create Master Data Tables

Execute the SQL script to create all master data tables:

**Script Location:** `/SQL_Scripts/02_CreateMasterDataTables.sql`

**Option A - Using SQL Server Management Studio (SSMS):**
```
1. Open SSMS
2. Connect to SQL Server (localhost)
3. Select database: RMMS_Production
4. File > Open > File... > Select 02_CreateMasterDataTables.sql
5. Click Execute (F5)
```

**Option B - Using sqlcmd (Command Line):**
```bash
sqlcmd -S localhost -U sa -P "YourStrong@Passw0rd" -d RMMS_Production -i SQL_Scripts/02_CreateMasterDataTables.sql
```

**Option C - Using Azure Data Studio:**
```
1. Open Azure Data Studio
2. Connect to localhost
3. Open RMMS_Production database
4. File > Open File > Select 02_CreateMasterDataTables.sql
5. Click Run
```

### Expected Result:
```
Customers table created successfully
CustomerContacts table created successfully
CustomerAddresses table created successfully
Vendors table created successfully
VendorContacts table created successfully
VendorAddresses table created successfully
Products table created successfully
Employees table created successfully
Indexes created successfully
========================================
Master Data Tables Created Successfully!
========================================
```

---

## Step 2: Run the Application

```bash
cd /home/user01/claude-test/RMMS.Web/RMMS.Web
dotnet run
```

The application will start on: `https://localhost:5001` or `http://localhost:5000`

---

## Step 3: Login

**Default Credentials:**
- **Username:** admin
- **Password:** (as configured in your system)

---

## Step 4: Test Master Data Modules

### Test Customer Module
1. Navigate to **Master Data > Customers**
2. Click **New Customer**
3. Fill in customer details
4. Click **Save Customer**
5. Verify customer appears in list
6. Test Edit, Details, and Delete functions

### Test Vendor Module
1. Navigate to **Master Data > Vendors**
2. Click **New Vendor**
3. Fill in vendor details (including bank info)
4. Set vendor rating (1-5 stars)
5. Click **Save Vendor**
6. Verify vendor appears in list

### Test Product Module
1. Navigate to **Master Data > Products**
2. Click **New Product**
3. Select **Product Category** (Rice/Paddy/By-Product)
4. Fill in product details
5. Set stock levels (Min, Max, Reorder)
6. Click **Save Product**
7. Test category filtering

### Test Employee Module
1. Navigate to **Master Data > Employees**
2. Click **New Employee**
3. Fill in personal information
4. Fill in employment details
5. Select department
6. Click **Save Employee**
7. Test department filtering

---

## Verification Checklist

### ✅ Database
- [ ] All 8 tables created successfully
- [ ] Indexes created on code fields
- [ ] Foreign keys configured with cascade delete

### ✅ Application
- [ ] Application builds successfully (0 errors)
- [ ] Application runs without errors
- [ ] Login works correctly
- [ ] Navigation menu shows Master Data section

### ✅ Customer Module
- [ ] Can create new customer
- [ ] Auto-generated code works (CUST0001, CUST0002...)
- [ ] Can edit customer
- [ ] Can view customer details
- [ ] Can delete customer (soft delete)
- [ ] Search functionality works

### ✅ Vendor Module
- [ ] Can create new vendor
- [ ] Auto-generated code works (VEND0001, VEND0002...)
- [ ] Rating system displays correctly (stars)
- [ ] Bank details save correctly
- [ ] Can edit, view, delete vendor
- [ ] Search functionality works

### ✅ Product Module
- [ ] Can create new product
- [ ] Code generation works by category (RICE0001, PADY0001, BYPD0001)
- [ ] Category filtering works
- [ ] Stock levels save correctly
- [ ] HSN Code and GST Rate save
- [ ] Can edit, view, delete product

### ✅ Employee Module
- [ ] Can create new employee
- [ ] Auto-generated code works (EMP0001, EMP0002...)
- [ ] Department filtering works
- [ ] Personal and employment details save
- [ ] Can edit, view, delete employee

---

## Common Issues & Solutions

### Issue 1: Tables Already Exist
**Error:** "There is already an object named 'X' in the database"

**Solution:** Tables already created. Skip Step 1.

### Issue 2: Build Errors
**Solution:** Run `dotnet build` and check for missing packages:
```bash
dotnet restore
dotnet build
```

### Issue 3: Navigation Menu Not Showing
**Solution:** Clear browser cache and refresh (Ctrl+F5)

### Issue 4: Auto-generated Codes Not Working
**Solution:** Check that services are properly registered in Program.cs (already done in Sprint 1)

---

## Performance Tips

### For Large Datasets
1. The indexes are already created for optimal performance
2. Search uses indexed fields for speed
3. Pagination can be added later if needed

### For Production
1. Change connection string in appsettings.json
2. Enable HTTPS redirect
3. Configure proper authentication
4. Set up logging to database/file
5. Enable response compression (already configured)

---

## Next Steps After Testing

Once all modules are tested and working:

1. **Document any bugs found** and report to development team
2. **Add sample data** for realistic testing
3. **Plan Sprint 2** - Inventory Management
4. **Begin Sprint 2 implementation**

---

## Sprint 2 Preview - Inventory Management

**Planned Modules:**
- Warehouse Master (storage locations)
- Inventory Ledger (stock tracking)
- Stock Movements (in/out transactions)
- Stock Adjustments (corrections)
- Real-time Stock Status (dashboard)

**Estimated Duration:** 2 weeks

---

## Support & Documentation

**Session Tracking:** Run `bash resume.sh` anytime to see current status

**Documentation Files:**
- `CURRENT_SESSION.md` - Current state and progress
- `PROGRESS_TRACKER.md` - Overall project tracking
- `SPRINT_1_COMPLETION_REPORT.md` - Detailed Sprint 1 report
- `SQL_Scripts/02_CreateMasterDataTables.sql` - Database migration

**Build Status:** ✅ Success (0 errors, 0 warnings)

---

**Last Updated:** 2025-10-06
**Sprint:** Sprint 1 - Master Data Foundation
**Status:** ✅ COMPLETE - Ready for Testing
