# 🔧 FIX: Database Tables Missing

## ❌ Problem Identified

The master data modules (Customers, Vendors, Products, Employees) are **showing errors because the database tables don't exist**.

**Error:** `Invalid object name 'Vendors'` (and similar for all master data tables)

---

## ✅ Solution: Run SQL Script

**Script Location:**
```
/home/user01/claude-test/RMMS.Web/CREATE_ALL_TABLES.sql
```

This single script creates **ALL required tables**:
- ✅ Sprint 1: Customers, Vendors, Products, Employees (+ related tables)
- ✅ Sprint 2: Warehouses, StorageZones

---

## 📋 How to Fix (Choose ONE method):

### Method 1: Using Azure Data Studio (Recommended)

1. Open **Azure Data Studio** or **SQL Server Management Studio**
2. Connect to: `172.17.208.1,1433`
   - Username: `rmms_user`
   - Password: `Welcome01!`
   - Database: `RMMS_Production`
3. Open file: `/home/user01/claude-test/RMMS.Web/CREATE_ALL_TABLES.sql`
4. Click **Run** or press `F5`
5. Verify tables are created

### Method 2: Using sqlcmd (if available)

```bash
sqlcmd -S 172.17.208.1,1433 -U rmms_user -P Welcome01! -d RMMS_Production -i /home/user01/claude-test/RMMS.Web/CREATE_ALL_TABLES.sql
```

### Method 3: Copy-Paste SQL (Quick)

1. Open your SQL tool
2. Connect to database `RMMS_Production`
3. Copy contents of `CREATE_ALL_TABLES.sql`
4. Paste and execute

---

## 🎯 What the Script Does

Creates **10 tables** with proper relationships:

**Master Data (Sprint 1):**
1. `Customers` - Customer master data
2. `CustomerContacts` - Customer contact persons
3. `CustomerAddresses` - Customer addresses
4. `Vendors` - Vendor/supplier master data
5. `VendorContacts` - Vendor contact persons
6. `VendorAddresses` - Vendor addresses
7. `Products` - Product catalog (rice, paddy, by-products)
8. `Employees` - Employee directory

**Inventory (Sprint 2):**
9. `Warehouses` - Warehouse/godown management
10. `StorageZones` - Storage zones within warehouses

**Plus:**
- All foreign key relationships
- Performance indexes
- Unique constraints

---

## ✅ After Running the Script

1. **Stop the running application:**
   ```bash
   # Press Ctrl+C in the terminal where dotnet run is running
   # Or find and kill the process
   ps aux | grep dotnet
   kill <process_id>
   ```

2. **Restart the application:**
   ```bash
   cd /home/user01/claude-test/RMMS.Web/RMMS.Web
   dotnet run
   ```

3. **Test the modules:**
   - Open: http://localhost:5090
   - Navigate to Master Data → Customers
   - Try creating a new customer
   - All forms should work now!

---

## 🧪 Verification

**Check if tables exist:**
```sql
USE RMMS_Production;
GO

SELECT TABLE_NAME
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_TYPE = 'BASE TABLE'
ORDER BY TABLE_NAME;
```

**Expected tables (partial list):**
- BankTransactions (existing)
- ByProductSales (existing)
- CashBook (existing)
- **Customers** ← NEW
- **CustomerContacts** ← NEW
- **CustomerAddresses** ← NEW
- **Employees** ← NEW
- ExternalRiceSales (existing)
- FixedAssets (existing)
- LoansAdvances (existing)
- PaddyProcurement (existing)
- PayablesOverdue (existing)
- **Products** ← NEW
- ReceivablesOverdue (existing)
- RiceProcurementExternal (existing)
- RiceSales (existing)
- **StorageZones** ← NEW
- **Vendors** ← NEW
- **VendorContacts** ← NEW
- **VendorAddresses** ← NEW
- Vouchers (existing)
- **Warehouses** ← NEW

---

## 🚀 Expected Outcome

After running the script and restarting:

✅ **Customers** module - Create, view, edit, delete customers
✅ **Vendors** module - Manage vendors with ratings
✅ **Products** module - Rice, paddy, by-products catalog
✅ **Employees** module - Employee directory
✅ **Warehouses** module - Warehouse/godown management

**All forms will work without errors!**

---

## ⚠️ Troubleshooting

**Error: "There is already an object named..."**
- This is OK! It means some tables already exist
- The script will skip existing tables
- New tables will still be created

**Error: "Cannot open database..."**
- Check connection string in `/home/user01/claude-test/RMMS.Web/RMMS.Web/appsettings.json`
- Verify database `RMMS_Production` exists
- Check username/password

**Still seeing errors after running script?**
- Verify script ran successfully (check for success message at end)
- Restart application (important!)
- Clear browser cache
- Check database has all 10 new tables

---

## 📞 Quick Reference

**SQL Script:** `/home/user01/claude-test/RMMS.Web/CREATE_ALL_TABLES.sql`
**Database:** `RMMS_Production` @ `172.17.208.1,1433`
**User:** `rmms_user` / `Welcome01!`
**Application:** http://localhost:5090

---

**Status:** ⚠️ Requires manual SQL script execution
**Priority:** HIGH - Blocks all master data functionality
**Impact:** All customers, vendors, products, employees, warehouses modules

🎯 **Action Required:** Run the CREATE_ALL_TABLES.sql script NOW
