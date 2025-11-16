-- ============================================
-- RMMS Comprehensive Seed Data Script
-- Creates 70+ records across all modules
-- ============================================

USE RMMS_Production;
GO

PRINT '========================================';
PRINT 'Starting Comprehensive Data Seeding';
PRINT '========================================';
PRINT '';

-- Fix InventoryLedger schema first
PRINT '1. Fixing Database Schema...';
IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.COLUMNS
               WHERE TABLE_NAME = 'InventoryLedger'
               AND COLUMN_NAME = 'TotalValue')
BEGIN
    ALTER TABLE InventoryLedger ADD TotalValue decimal(18,2) NOT NULL DEFAULT 0;
    PRINT '   ✓ Added TotalValue column to InventoryLedger';
END
ELSE
BEGIN
    PRINT '   ✓ InventoryLedger schema already correct';
END
GO

-- Seed Customers (10 records)
PRINT '';
PRINT '2. Seeding Customers...';
IF NOT EXISTS (SELECT 1 FROM Customers WHERE CustomerCode = 'CUST001')
BEGIN
    INSERT INTO Customers (CustomerCode, CustomerName, CustomerType, GSTIN, ContactPerson, Mobile, Email, Address, City, State, Pincode, PaymentTerms, CreditLimit, IsActive, CreatedDate, CreatedBy)
    VALUES
    ('CUST001', 'Vishnu Rice Traders', 'Wholesale', '29AAAAA0000A1Z5', 'Raj Kumar', '9876543210', 'raj@vishnurice.com', '123 Main St', 'Bangalore', 'Karnataka', '560001', 'Net 30', 500000, 1, GETDATE(), 'System'),
    ('CUST002', 'Sri Lakshmi Distributors', 'Wholesale', '29BBBBB1111B1Z5', 'Sita Devi', '9876543211', 'sita@lakshmi.com', '45 MG Road', 'Bangalore', 'Karnataka', '560002', 'Net 15', 300000, 1, GETDATE(), 'System'),
    ('CUST003', 'Modern Rice Mart', 'Retail', '29CCCCC2222C1Z5', 'Ramesh Babu', '9876543212', 'ramesh@modern.com', '78 Brigade Rd', 'Bangalore', 'Karnataka', '560003', 'Cash', 100000, 1, GETDATE(), 'System'),
    ('CUST004', 'Golden Grain Exports', 'Wholesale', '29DDDDD3333D1Z5', 'Krishna Das', '9876543213', 'krishna@golden.com', '90 Export St', 'Bangalore', 'Karnataka', '560004', 'Net 45', 1000000, 1, GETDATE(), 'System'),
    ('CUST005', 'Annapurna Foods', 'Retail', '29EEEEE4444E1Z5', 'Geetha Rani', '9876543214', 'geetha@annapurna.com', '34 Temple Rd', 'Bangalore', 'Karnataka', '560005', 'Net 7', 50000, 1, GETDATE(), 'System'),
    ('CUST006', 'Balaji Rice Suppliers', 'Wholesale', '29FFFFF5555F1Z5', 'Venkat Rao', '9876543215', 'venkat@balaji.com', '56 Commercial St', 'Bangalore', 'Karnataka', '560006', 'Net 30', 400000, 1, GETDATE(), 'System'),
    ('CUST007', 'Premium Rice Store', 'Retail', '29GGGGG6666G1Z5', 'Lakshmi Bai', '9876543216', 'lakshmi@premium.com', '12 Market St', 'Bangalore', 'Karnataka', '560007', 'Cash', 75000, 1, GETDATE(), 'System'),
    ('CUST008', 'Raghavendra Traders', 'Wholesale', '29HHHHH7777H1Z5', 'Murthy Prasad', '9876543217', 'murthy@raghavendra.com', '89 Industrial Area', 'Bangalore', 'Karnataka', '560008', 'Net 30', 600000, 1, GETDATE(), 'System'),
    ('CUST009', 'Srinivasa Rice Depot', 'Retail', '29IIIII8888I1Z5', 'Anand Kumar', '9876543218', 'anand@srinivasa.com', '23 Depot Rd', 'Bangalore', 'Karnataka', '560009', 'Net 15', 150000, 1, GETDATE(), 'System'),
    ('CUST010', 'Narayana Wholesale', 'Wholesale', '29JJJJJ9999J1Z5', 'Prakash Reddy', '9876543219', 'prakash@narayana.com', '67 Wholesale Market', 'Bangalore', 'Karnataka', '560010', 'Net 45', 800000, 1, GETDATE(), 'System');
    PRINT '   ✓ Seeded 10 Customers';
END
ELSE
BEGIN
    PRINT '   ✓ Customers already exist';
END
GO

-- Seed Vendors (10 records)
PRINT '';
PRINT '3. Seeding Vendors...';
IF NOT EXISTS (SELECT 1 FROM Vendors WHERE VendorCode = 'VEND001')
BEGIN
    INSERT INTO Vendors (VendorCode, VendorName, VendorType, GSTIN, ContactPerson, Mobile, Email, Address, City, State, Pincode, PaymentTerms, CreditPeriod, IsActive, CreatedDate, CreatedBy)
    VALUES
    ('VEND001', 'Karnataka Paddy Suppliers', 'Paddy', '29KKKKK0000K1Z5', 'Basava Raj', '8765432100', 'basava@kps.com', '100 Farm Rd', 'Mandya', 'Karnataka', '571401', 'Net 15', 15, 1, GETDATE(), 'System'),
    ('VEND002', 'Tamil Nadu Rice Mills', 'Rice', '33LLLLL1111L1Z5', 'Murugan Pillai', '8765432101', 'murugan@tnrm.com', '200 Mill St', 'Coimbatore', 'Tamil Nadu', '641001', 'Net 30', 30, 1, GETDATE(), 'System'),
    ('VEND003', 'Mysore Agro Products', 'Paddy', '29MMMMM2222M1Z5', 'Suresh Gowda', '8765432102', 'suresh@mysoreagro.com', '50 Agro Lane', 'Mysore', 'Karnataka', '570001', 'Cash', 0, 1, GETDATE(), 'System'),
    ('VEND004', 'AP Grain Traders', 'Paddy', '37NNNNN3333N1Z5', 'Naidu Prasad', '8765432103', 'naidu@apgrain.com', '75 Grain Market', 'Guntur', 'Andhra Pradesh', '522001', 'Net 15', 15, 1, GETDATE(), 'System'),
    ('VEND005', 'Kerala Rice Export', 'Rice', '32OOOOO4444O1Z5', 'Gopalan Nair', '8765432104', 'gopalan@kerala.com', '30 Export Zone', 'Kochi', 'Kerala', '682001', 'Net 45', 45, 1, GETDATE(), 'System'),
    ('VEND006', 'Mandya Farmers Co-op', 'Paddy', '29PPPPP5555P1Z5', 'Ravi Kumar', '8765432105', 'ravi@mandyacoop.com', '15 Co-op St', 'Mandya', 'Karnataka', '571402', 'Net 7', 7, 1, GETDATE(), 'System'),
    ('VEND007', 'Bellary Paddy Market', 'Paddy', '29QQQQQ6666Q1Z5', 'Ashok Reddy', '8765432106', 'ashok@bellary.com', '88 Market Yard', 'Bellary', 'Karnataka', '583101', 'Cash', 0, 1, GETDATE(), 'System'),
    ('VEND008', 'Hassan Rice Suppliers', 'Rice', '29RRRRR7777R1Z5', 'Mohan Das', '8765432107', 'mohan@hassan.com', '22 Supply Chain Rd', 'Hassan', 'Karnataka', '573201', 'Net 30', 30, 1, GETDATE(), 'System'),
    ('VEND009', 'Shimoga Grain Depot', 'Paddy', '29SSSSS8888S1Z5', 'Vishwanath Bhat', '8765432108', 'vishwa@shimoga.com', '44 Depot Area', 'Shimoga', 'Karnataka', '577201', 'Net 15', 15, 1, GETDATE(), 'System'),
    ('VEND010', 'Davangere Traders', 'Paddy', '29TTTTT9999T1Z5', 'Shankar Naik', '8765432109', 'shankar@davangere.com', '66 Trade Center', 'Davangere', 'Karnataka', '577001', 'Net 30', 30, 1, GETDATE(), 'System');
    PRINT '   ✓ Seeded 10 Vendors';
END
ELSE
BEGIN
    PRINT '   ✓ Vendors already exist';
END
GO

-- Seed Products (15 records)
PRINT '';
PRINT '4. Seeding Products...';
IF NOT EXISTS (SELECT 1 FROM Products WHERE ProductCode = 'PROD001')
BEGIN
    INSERT INTO Products (ProductCode, ProductName, ProductType, Category, HSNCode, GST_Rate, UnitOfMeasure, PurchaseRate, SalesRate, MinimumStock, MaximumStock, ReorderLevel, IsActive, CreatedDate, CreatedBy)
    VALUES
    ('PROD001', 'Basmati Rice Premium', 'Finished', 'Rice', '10063020', 5.00, 'Quintals', 3500.00, 4200.00, 50.000, 500.000, 100.000, 1, GETDATE(), 'System'),
    ('PROD002', 'Sona Masoori Raw Rice', 'Finished', 'Rice', '10063020', 5.00, 'Quintals', 2800.00, 3400.00, 100.000, 1000.000, 200.000, 1, GETDATE(), 'System'),
    ('PROD003', 'Ponni Boiled Rice', 'Finished', 'Rice', '10063020', 5.00, 'Quintals', 2600.00, 3200.00, 100.000, 800.000, 150.000, 1, GETDATE(), 'System'),
    ('PROD004', 'IR64 Parboiled Rice', 'Finished', 'Rice', '10063020', 5.00, 'Quintals', 2400.00, 3000.00, 150.000, 1200.000, 250.000, 1, GETDATE(), 'System'),
    ('PROD005', 'Raw Paddy Grade A', 'Raw', 'Paddy', '10061010', 5.00, 'Quintals', 1800.00, 0.00, 200.000, 2000.000, 400.000, 1, GETDATE(), 'System'),
    ('PROD006', 'Boiled Paddy Grade A', 'Raw', 'Paddy', '10061010', 5.00, 'Quintals', 1900.00, 0.00, 200.000, 2000.000, 400.000, 1, GETDATE(), 'System'),
    ('PROD007', 'Rice Bran', 'ByProduct', 'By-Product', '23024010', 5.00, 'Quintals', 800.00, 1200.00, 50.000, 300.000, 80.000, 1, GETDATE(), 'System'),
    ('PROD008', 'Rice Husk', 'ByProduct', 'By-Product', '23024090', 5.00, 'Quintals', 200.00, 400.00, 50.000, 500.000, 100.000, 1, GETDATE(), 'System'),
    ('PROD009', 'Broken Rice', 'ByProduct', 'By-Product', '10064000', 5.00, 'Quintals', 1500.00, 2000.00, 30.000, 200.000, 50.000, 1, GETDATE(), 'System'),
    ('PROD010', 'Idli Rice', 'Finished', 'Rice', '10063020', 5.00, 'Quintals', 2900.00, 3500.00, 50.000, 400.000, 100.000, 1, GETDATE(), 'System'),
    ('PROD011', 'Kolam Rice', 'Finished', 'Rice', '10063020', 5.00, 'Quintals', 2700.00, 3300.00, 60.000, 500.000, 120.000, 1, GETDATE(), 'System'),
    ('PROD012', 'Jeera Samba Rice', 'Finished', 'Rice', '10063020', 5.00, 'Quintals', 4000.00, 4800.00, 30.000, 300.000, 60.000, 1, GETDATE(), 'System'),
    ('PROD013', 'Matta Rice (Red Rice)', 'Finished', 'Rice', '10063020', 5.00, 'Quintals', 3200.00, 3900.00, 40.000, 350.000, 80.000, 1, GETDATE(), 'System'),
    ('PROD014', 'Steam Rice', 'Finished', 'Rice', '10063020', 5.00, 'Quintals', 2500.00, 3100.00, 80.000, 700.000, 150.000, 1, GETDATE(), 'System'),
    ('PROD015', 'Brown Rice', 'Finished', 'Rice', '10063020', 5.00, 'Quintals', 3300.00, 4000.00, 40.000, 300.000, 70.000, 1, GETDATE(), 'System');
    PRINT '   ✓ Seeded 15 Products';
END
ELSE
BEGIN
    PRINT '   ✓ Products already exist';
END
GO

-- Seed Employees (10 records)
PRINT '';
PRINT '5. Seeding Employees...';
IF NOT EXISTS (SELECT 1 FROM Employees WHERE EmployeeCode = 'EMP001')
BEGIN
    INSERT INTO Employees (EmployeeCode, EmployeeName, Designation, Department, Mobile, Email, DateOfJoining, DateOfBirth, Address, City, State, Pincode, AadharNumber, PANNumber, BankAccountNumber, BankName, IFSCCode, Salary, IsActive, CreatedDate, CreatedBy)
    VALUES
    ('EMP001', 'Rajesh Kumar', 'Mill Manager', 'Production', '7654321000', 'rajesh@rmms.com', '2020-01-01', '1985-05-15', '101 Staff Colony', 'Bangalore', 'Karnataka', '560001', '123456789012', 'ABCDE1234F', '1234567890', 'HDFC Bank', 'HDFC0001234', 50000.00, 1, GETDATE(), 'System'),
    ('EMP002', 'Sunitha Reddy', 'Accountant', 'Finance', '7654321001', 'sunitha@rmms.com', '2020-02-01', '1988-08-20', '102 Staff Colony', 'Bangalore', 'Karnataka', '560001', '123456789013', 'BCDEF2345G', '1234567891', 'ICICI Bank', 'ICIC0001234', 35000.00, 1, GETDATE(), 'System'),
    ('EMP003', 'Manjunath Gowda', 'Production Supervisor', 'Production', '7654321002', 'manju@rmms.com', '2020-03-01', '1990-03-10', '103 Staff Colony', 'Bangalore', 'Karnataka', '560001', '123456789014', 'CDEFG3456H', '1234567892', 'SBI', 'SBIN0001234', 30000.00, 1, GETDATE(), 'System'),
    ('EMP004', 'Priya Sharma', 'Sales Executive', 'Sales', '7654321003', 'priya@rmms.com', '2020-04-01', '1992-11-25', '104 Staff Colony', 'Bangalore', 'Karnataka', '560001', '123456789015', 'DEFGH4567I', '1234567893', 'Axis Bank', 'UTIB0001234', 28000.00, 1, GETDATE(), 'System'),
    ('EMP005', 'Venkatesh Naik', 'Quality Controller', 'QC', '7654321004', 'venkat@rmms.com', '2020-05-01', '1987-07-18', '105 Staff Colony', 'Bangalore', 'Karnataka', '560001', '123456789016', 'EFGHI5678J', '1234567894', 'HDFC Bank', 'HDFC0001234', 32000.00, 1, GETDATE(), 'System'),
    ('EMP006', 'Lakshmi Devi', 'Purchase Officer', 'Purchase', '7654321005', 'lakshmi@rmms.com', '2020-06-01', '1989-12-05', '106 Staff Colony', 'Bangalore', 'Karnataka', '560001', '123456789017', 'FGHIJ6789K', '1234567895', 'ICICI Bank', 'ICIC0001234', 33000.00, 1, GETDATE(), 'System'),
    ('EMP007', 'Ramesh Babu', 'Store Keeper', 'Warehouse', '7654321006', 'ramesh@rmms.com', '2020-07-01', '1991-04-30', '107 Staff Colony', 'Bangalore', 'Karnataka', '560001', '123456789018', 'GHIJK7890L', '1234567896', 'SBI', 'SBIN0001234', 25000.00, 1, GETDATE(), 'System'),
    ('EMP008', 'Kavitha Rani', 'HR Manager', 'HR', '7654321007', 'kavitha@rmms.com', '2020-08-01', '1986-09-12', '108 Staff Colony', 'Bangalore', 'Karnataka', '560001', '123456789019', 'HIJKL8901M', '1234567897', 'Axis Bank', 'UTIB0001234', 38000.00, 1, GETDATE(), 'System'),
    ('EMP009', 'Suresh Kumar', 'Machine Operator', 'Production', '7654321008', 'suresh@rmms.com', '2020-09-01', '1993-06-22', '109 Staff Colony', 'Bangalore', 'Karnataka', '560001', '123456789020', 'IJKLM9012N', '1234567898', 'HDFC Bank', 'HDFC0001234', 22000.00, 1, GETDATE(), 'System'),
    ('EMP010', 'Geeta Bai', 'Office Assistant', 'Admin', '7654321009', 'geeta@rmms.com', '2020-10-01', '1994-02-14', '110 Staff Colony', 'Bangalore', 'Karnataka', '560001', '123456789021', 'JKLMN0123O', '1234567899', 'ICICI Bank', 'ICIC0001234', 20000.00, 1, GETDATE(), 'System');
    PRINT '   ✓ Seeded 10 Employees';
END
ELSE
BEGIN
    PRINT '   ✓ Employees already exist';
END
GO

-- Seed Warehouses (5 records)
PRINT '';
PRINT '6. Seeding Warehouses...';
IF NOT EXISTS (SELECT 1 FROM Warehouses WHERE WarehouseCode = 'WH001')
BEGIN
    INSERT INTO Warehouses (WarehouseCode, WarehouseName, WarehouseType, Location, Address, City, State, Pincode, ContactPerson, Mobile, Email, TotalCapacity, UsedCapacity, AvailableCapacity, Temperature, Humidity, IsTemperatureControlled, Status, IsActive, CreatedDate, CreatedBy)
    VALUES
    ('WH001', 'Main Warehouse', 'Primary', 'Industrial Area A', 'Plot 100, Phase 1', 'Bangalore', 'Karnataka', '560001', 'Ramesh Babu', '7654321006', 'wh1@rmms.com', 5000.000, 0.000, 5000.000, 25.00, 60.00, 1, 'Active', 1, GETDATE(), 'System'),
    ('WH002', 'Secondary Warehouse', 'Secondary', 'Industrial Area B', 'Plot 200, Phase 2', 'Bangalore', 'Karnataka', '560002', 'Sunil Kumar', '7654321010', 'wh2@rmms.com', 3000.000, 0.000, 3000.000, 26.00, 62.00, 1, 'Active', 1, GETDATE(), 'System'),
    ('WH003', 'Cold Storage Unit', 'Cold Storage', 'Special Zone', 'Plot 50, Zone C', 'Bangalore', 'Karnataka', '560003', 'Prakash Rao', '7654321011', 'wh3@rmms.com', 1000.000, 0.000, 1000.000, 15.00, 55.00, 1, 'Active', 1, GETDATE(), 'System'),
    ('WH004', 'Transit Warehouse', 'Transit', 'Near Highway', 'Plot 300, Highway Rd', 'Bangalore', 'Karnataka', '560004', 'Mohan Das', '7654321012', 'wh4@rmms.com', 2000.000, 0.000, 2000.000, 27.00, 65.00, 0, 'Active', 1, GETDATE(), 'System'),
    ('WH005', 'Raw Material Store', 'Primary', 'Mill Premises', 'Inside Mill Complex', 'Bangalore', 'Karnataka', '560005', 'Venkat Reddy', '7654321013', 'wh5@rmms.com', 4000.000, 0.000, 4000.000, 28.00, 63.00, 0, 'Active', 1, GETDATE(), 'System');
    PRINT '   ✓ Seeded 5 Warehouses';
END
ELSE
BEGIN
    PRINT '   ✓ Warehouses already exist';
END
GO

-- Seed Inventory Ledger (15 records - one for each product in main warehouse)
PRINT '';
PRINT '7. Seeding Inventory Ledger...';
IF NOT EXISTS (SELECT 1 FROM InventoryLedger WHERE ProductId = 1)
BEGIN
    DECLARE @Counter INT = 1;

    WHILE @Counter <= 15
    BEGIN
        DECLARE @CurrentStock DECIMAL(18,3);
        DECLARE @MinLevel DECIMAL(18,3);
        DECLARE @MaxLevel DECIMAL(18,3);
        DECLARE @ReorderLvl DECIMAL(18,3);
        DECLARE @Cost DECIMAL(18,2);
        DECLARE @TotalVal DECIMAL(18,2);

        SELECT @Cost = PurchaseRate FROM Products WHERE Id = @Counter;

        -- Set stock levels based on product type
        IF @Counter <= 4  -- Finished Rice
        BEGIN
            SET @CurrentStock = 200.000;
            SET @MinLevel = 50.000;
            SET @MaxLevel = 500.000;
            SET @ReorderLvl = 100.000;
        END
        ELSE IF @Counter <= 6  -- Paddy
        BEGIN
            SET @CurrentStock = 500.000;
            SET @MinLevel = 200.000;
            SET @MaxLevel = 2000.000;
            SET @ReorderLvl = 400.000;
        END
        ELSE  -- By-products and other finished products
        BEGIN
            SET @CurrentStock = 100.000;
            SET @MinLevel = 30.000;
            SET @MaxLevel = 300.000;
            SET @ReorderLvl = 50.000;
        END

        SET @TotalVal = @CurrentStock * @Cost;

        INSERT INTO InventoryLedger (ProductId, WarehouseId, CurrentStock, MinimumLevel, MaximumLevel, ReorderLevel, UnitCost, TotalValue, LastUpdated, IsActive, CreatedDate, CreatedBy)
        VALUES (@Counter, 1, @CurrentStock, @MinLevel, @MaxLevel, @ReorderLvl, @Cost, @TotalVal, GETDATE(), 1, GETDATE(), 'System');

        SET @Counter = @Counter + 1;
    END

    PRINT '   ✓ Seeded 15 Inventory Records';
END
ELSE
BEGIN
    PRINT '   ✓ Inventory Ledger already exists';
END
GO

-- Seed Machines (5 records)
PRINT '';
PRINT '8. Seeding Machines...';
IF NOT EXISTS (SELECT 1 FROM Machines WHERE MachineCode = 'MACH001')
BEGIN
    INSERT INTO Machines (MachineCode, MachineName, MachineType, Manufacturer, Model, SerialNumber, YearOfManufacture, PurchaseDate, PurchaseValue, Capacity, UnitOfMeasure, Status, Location, RunningHours, LastMaintenanceDate, NextMaintenanceDate, IsActive, CreatedDate, CreatedBy)
    VALUES
    ('MACH001', 'Paddy Cleaner Unit 1', 'Cleaner', 'Satake Corporation', 'PCL-500', 'SN-PCL-001', 2019, '2019-01-15', 1500000, 50.000, 'Quintals/Hour', 'Running', 'Production Floor A', 15000.00, '2024-09-01', '2024-12-01', 1, GETDATE(), 'System'),
    ('MACH002', 'Destoner Machine', 'Destoner', 'Bühler Group', 'DST-300', 'SN-DST-001', 2019, '2019-02-01', 800000, 30.000, 'Quintals/Hour', 'Running', 'Production Floor A', 14500.00, '2024-09-05', '2024-12-05', 1, GETDATE(), 'System'),
    ('MACH003', 'Husking Machine 1', 'Husker', 'Satake Corporation', 'HSK-1000', 'SN-HSK-001', 2018, '2018-06-01', 2500000, 100.000, 'Quintals/Hour', 'Running', 'Production Floor B', 18000.00, '2024-08-20', '2024-11-20', 1, GETDATE(), 'System'),
    ('MACH004', 'Whitening Machine', 'Whitener', 'Bühler Group', 'WHT-800', 'SN-WHT-001', 2018, '2018-07-01', 2000000, 80.000, 'Quintals/Hour', 'Running', 'Production Floor B', 17500.00, '2024-08-25', '2024-11-25', 1, GETDATE(), 'System'),
    ('MACH005', 'Sorting Machine', 'Sorter', 'Satake Corporation', 'SRT-600', 'SN-SRT-001', 2020, '2020-01-10', 3000000, 60.000, 'Quintals/Hour', 'Running', 'Production Floor C', 10000.00, '2024-09-10', '2024-12-10', 1, GETDATE(), 'System');
    PRINT '   ✓ Seeded 5 Machines';
END
ELSE
BEGIN
    PRINT '   ✓ Machines already exist';
END
GO

PRINT '';
PRINT '========================================';
PRINT '✓✓✓ Data Seeding Completed Successfully! ✓✓✓';
PRINT '========================================';
PRINT '';
PRINT 'Summary of seeded data:';
PRINT '  • 10 Customers';
PRINT '  • 10 Vendors';
PRINT '  • 15 Products';
PRINT '  • 10 Employees';
PRINT '  • 5 Warehouses';
PRINT '  • 15 Inventory Records';
PRINT '  • 5 Machines';
PRINT '  ---------------------';
PRINT '  Total: 70 records';
PRINT '';
PRINT 'Database is now ready for testing!';
PRINT '========================================';
GO
