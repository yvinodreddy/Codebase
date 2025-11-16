-- ============================================
-- COMPREHENSIVE RMMS DATA INSERTION SCRIPT
-- Inserts 40+ records for ALL tables
-- ============================================

USE RMMS_Production;
GO

PRINT '========================================';
PRINT 'COMPREHENSIVE DATA INSERTION STARTING';
PRINT '========================================';
GO

-- Clear existing data (in correct order due to foreign keys)
PRINT 'Clearing existing data...';
DELETE FROM BatchOutputs;
DELETE FROM BatchInputs;
DELETE FROM SalesOrderItems;
DELETE FROM SalesOrders;
DELETE FROM QuotationItems;
DELETE FROM Quotations;
DELETE FROM Inquiries;
DELETE FROM YieldRecords;
DELETE FROM ProductionBatches;
DELETE FROM ProductionOrders;
DELETE FROM StockAdjustments;
DELETE FROM StockMovements;
DELETE FROM InventoryLedger;
DELETE FROM ByProductSales;
DELETE FROM ExternalRiceSales;
DELETE FROM RiceSales;
DELETE FROM PaddyProcurement;
DELETE FROM RiceProcurementExternal;
DELETE FROM ReceivablesOverdue;
DELETE FROM PayablesOverdue;
DELETE FROM BankTransactions;
DELETE FROM CashBook;
DELETE FROM Vouchers;
DELETE FROM LoansAdvances;
DELETE FROM FixedAssets;
DELETE FROM CustomerContacts;
DELETE FROM CustomerAddresses;
DELETE FROM VendorContacts;
DELETE FROM VendorAddresses;
DELETE FROM StorageZones;
DELETE FROM Machines;
DELETE FROM Employees;
DELETE FROM Warehouses;
DELETE FROM Vendors;
DELETE FROM Customers;
DELETE FROM Products;
PRINT '✓ Existing data cleared';
GO

-- ============================================
-- 1. PRODUCTS (50 records)
-- ============================================
PRINT 'Inserting Products (50 records)...';

SET IDENTITY_INSERT Products ON;

INSERT INTO Products (Id, ProductCode, ProductName, Category, SubCategory, Unit, HSNCode, GSTRate,
                     PurchasePrice, SellingPrice, ReorderLevel, Description, Specifications,
                     Brand, Manufacturer, WarrantyPeriod, IsActive, CreatedDate, CreatedBy)
VALUES
-- Raw Materials
(1, 'RAW-001', 'Basmati Paddy - Grade A', 'Raw Material', 'Paddy', 'KG', '1006', 5.00, 25.00, 30.00, 1000, 'Premium Basmati Paddy', 'Long grain, 1121 variety', 'Premium Grain', 'Local Farmers', 0, 1, GETDATE(), 'System'),
(2, 'RAW-002', 'Basmati Paddy - Grade B', 'Raw Material', 'Paddy', 'KG', '1006', 5.00, 22.00, 27.00, 1000, 'Standard Basmati Paddy', 'Long grain', 'Standard Grain', 'Local Farmers', 0, 1, GETDATE(), 'System'),
(3, 'RAW-003', 'Sona Masuri Paddy', 'Raw Material', 'Paddy', 'KG', '1006', 5.00, 20.00, 25.00, 1200, 'Sona Masuri Variety', 'Medium grain', 'Sona Brand', 'AP Farmers', 0, 1, GETDATE(), 'System'),
(4, 'RAW-004', 'IR-64 Paddy', 'Raw Material', 'Paddy', 'KG', '1006', 5.00, 18.00, 22.00, 1500, 'IR-64 Variety', 'Short grain', 'IR Brand', 'Local Farmers', 0, 1, GETDATE(), 'System'),
(5, 'RAW-005', 'Ponni Paddy', 'Raw Material', 'Paddy', 'KG', '1006', 5.00, 19.00, 24.00, 1300, 'Ponni Variety', 'Medium grain', 'Ponni Brand', 'TN Farmers', 0, 1, GETDATE(), 'System'),

-- Finished Products
(6, 'RICE-001', 'Basmati Rice - Premium', 'Finished Product', 'Rice', 'KG', '1006', 5.00, 50.00, 65.00, 500, 'Premium Basmati White Rice', 'Long grain, aged 2 years', 'Royal Basmati', 'In-house', 12, 1, GETDATE(), 'System'),
(7, 'RICE-002', 'Basmati Rice - Standard', 'Finished Product', 'Rice', 'KG', '1006', 5.00, 45.00, 58.00, 600, 'Standard Basmati Rice', 'Long grain, aged 1 year', 'Classic Basmati', 'In-house', 12, 1, GETDATE(), 'System'),
(8, 'RICE-003', 'Sona Masuri Rice', 'Finished Product', 'Rice', 'KG', '1006', 5.00, 42.00, 54.00, 700, 'Sona Masuri White Rice', 'Medium grain, non-sticky', 'Golden Sona', 'In-house', 12, 1, GETDATE(), 'System'),
(9, 'RICE-004', 'IR-64 Boiled Rice', 'Finished Product', 'Rice', 'KG', '1006', 5.00, 38.00, 48.00, 800, 'IR-64 Parboiled Rice', 'Short grain, parboiled', 'Boiled Special', 'In-house', 12, 1, GETDATE(), 'System'),
(10, 'RICE-005', 'Ponni Boiled Rice', 'Finished Product', 'Rice', 'KG', '1006', 5.00, 40.00, 52.00, 750, 'Ponni Parboiled Rice', 'Medium grain, parboiled', 'Ponni Deluxe', 'In-house', 12, 1, GETDATE(), 'System'),
(11, 'RICE-006', 'Broken Rice', 'Finished Product', 'Rice', 'KG', '1006', 5.00, 25.00, 32.00, 1000, 'Broken Rice Pieces', 'Mixed size, food grade', 'Economy Rice', 'In-house', 6, 1, GETDATE(), 'System'),

-- By-Products
(12, 'BP-001', 'Rice Bran', 'By-Product', 'Bran', 'KG', '2302', 5.00, 5.00, 8.00, 500, 'Rice Bran for Animal Feed', 'High fiber content', 'Farm Feed', 'In-house', 0, 1, GETDATE(), 'System'),
(13, 'BP-002', 'Rice Husk', 'By-Product', 'Husk', 'KG', '2302', 5.00, 2.00, 4.00, 1000, 'Rice Husk', 'Can be used as fuel', 'Agri Waste', 'In-house', 0, 1, GETDATE(), 'System'),
(14, 'BP-003', 'Rice Bran Oil Cake', 'By-Product', 'Oil Cake', 'KG', '2306', 5.00, 12.00, 18.00, 300, 'De-oiled Rice Bran', 'Cattle feed ingredient', 'Premium Feed', 'In-house', 0, 1, GETDATE(), 'System'),

-- Packaging Materials
(15, 'PKG-001', 'PP Bag - 25 KG', 'Packaging', 'Bags', 'PCS', '3923', 18.00, 8.00, 12.00, 500, 'Polypropylene Bag 25kg capacity', '60x40 cm', 'PackPro', 'Supplier A', 0, 1, GETDATE(), 'System'),
(16, 'PKG-002', 'PP Bag - 50 KG', 'Packaging', 'Bags', 'PCS', '3923', 18.00, 12.00, 18.00, 400, 'Polypropylene Bag 50kg capacity', '80x50 cm', 'PackPro', 'Supplier A', 0, 1, GETDATE(), 'System'),
(17, 'PKG-003', 'Jute Bag - 25 KG', 'Packaging', 'Bags', 'PCS', '6305', 5.00, 15.00, 22.00, 300, 'Jute Bag 25kg capacity', 'Eco-friendly', 'NaturePack', 'Supplier B', 0, 1, GETDATE(), 'System'),

-- Continue with more products to reach 50...
(18, 'RICE-007', 'Organic Basmati Rice', 'Finished Product', 'Rice', 'KG', '1006', 5.00, 75.00, 95.00, 200, 'Organic Certified Basmati', 'Chemical-free cultivation', 'Organic Gold', 'Organic Farms', 12, 1, GETDATE(), 'System'),
(19, 'RICE-008', 'Brown Basmati Rice', 'Finished Product', 'Rice', 'KG', '1006', 5.00, 55.00, 72.00, 250, 'Whole Grain Brown Basmati', 'High fiber, unpolished', 'Health Plus', 'In-house', 12, 1, GETDATE(), 'System'),
(20, 'RICE-009', 'Miniket Rice', 'Finished Product', 'Rice', 'KG', '1006', 5.00, 38.00, 49.00, 600, 'Miniket Variety', 'Small grain, aromatic', 'Miniket Special', 'In-house', 12, 1, GETDATE(), 'System'),

(21, 'RAW-006', 'Jasmine Paddy', 'Raw Material', 'Paddy', 'KG', '1006', 5.00, 28.00, 34.00, 800, 'Jasmine Rice Paddy', 'Aromatic variety', 'Jasmine Original', 'Thailand Import', 0, 1, GETDATE(), 'System'),
(22, 'RICE-010', 'Jasmine Rice', 'Finished Product', 'Rice', 'KG', '1006', 5.00, 58.00, 75.00, 300, 'Thai Jasmine White Rice', 'Very aromatic, long grain', 'Thai Delight', 'In-house', 12, 1, GETDATE(), 'System'),
(23, 'RICE-011', 'Parboiled Rice - Premium', 'Finished Product', 'Rice', 'KG', '1006', 5.00, 44.00, 58.00, 500, 'Premium Parboiled Rice', 'Golden color, nutritious', 'Golden Grain', 'In-house', 12, 1, GETDATE(), 'System'),
(24, 'RICE-012', 'Steam Rice', 'Finished Product', 'Rice', 'KG', '1006', 5.00, 35.00, 46.00, 700, 'Steam Processed Rice', 'Soft texture', 'Steam Fresh', 'In-house', 12, 1, GETDATE(), 'System'),
(25, 'RICE-013', 'Raw Rice - Regular', 'Finished Product', 'Rice', 'KG', '1006', 5.00, 32.00, 42.00, 900, 'Regular Raw Rice', 'Everyday use', 'Daily Special', 'In-house', 12, 1, GETDATE(), 'System'),

(26, 'BP-004', 'Rice Straw', 'By-Product', 'Straw', 'KG', '1213', 5.00, 1.00, 2.50, 2000, 'Rice Straw', 'Animal bedding, mulch', 'Farm Supply', 'In-house', 0, 1, GETDATE(), 'System'),
(27, 'BP-005', 'Broken Bran', 'By-Product', 'Bran', 'KG', '2302', 5.00, 4.00, 6.50, 800, 'Broken Rice Bran', 'Mixed with husk', 'Economy Feed', 'In-house', 0, 1, GETDATE(), 'System'),

(28, 'PKG-004', 'Plastic Bag - 1 KG', 'Packaging', 'Bags', 'PCS', '3923', 18.00, 1.50, 2.50, 2000, 'Small retail pack', '15x20 cm', 'RetailPack', 'Supplier C', 0, 1, GETDATE(), 'System'),
(29, 'PKG-005', 'Plastic Bag - 5 KG', 'Packaging', 'Bags', 'PCS', '3923', 18.00, 3.00, 5.00, 1500, 'Medium retail pack', '30x40 cm', 'RetailPack', 'Supplier C', 0, 1, GETDATE(), 'System'),
(30, 'PKG-006', 'Carton Box - 10 KG', 'Packaging', 'Boxes', 'PCS', '4819', 18.00, 15.00, 22.00, 400, 'Corrugated box for export', '40x30x25 cm', 'ExportBox', 'Supplier D', 0, 1, GETDATE(), 'System'),

(31, 'RAW-007', 'Black Rice Paddy', 'Raw Material', 'Paddy', 'KG', '1006', 5.00, 45.00, 55.00, 200, 'Black Rice Paddy', 'Rare variety, high antioxidants', 'Black Pearl', 'Specialty Farms', 0, 1, GETDATE(), 'System'),
(32, 'RICE-014', 'Black Rice', 'Finished Product', 'Rice', 'KG', '1006', 5.00, 95.00, 125.00, 100, 'Black Rice - Forbidden Rice', 'Purple-black color', 'Ancient Grain', 'In-house', 12, 1, GETDATE(), 'System'),
(33, 'RICE-015', 'Red Rice', 'Finished Product', 'Rice', 'KG', '1006', 5.00, 65.00, 85.00, 150, 'Red Rice Whole Grain', 'Red bran, nutty flavor', 'Ruby Rice', 'In-house', 12, 1, GETDATE(), 'System'),
(34, 'RICE-016', 'Wild Rice Mix', 'Finished Product', 'Rice', 'KG', '1006', 5.00, 110.00, 145.00, 80, 'Wild Rice Blend', 'Gourmet blend', 'Wild Harvest', 'In-house', 12, 1, GETDATE(), 'System'),

(35, 'RAW-008', 'Kolam Paddy', 'Raw Material', 'Paddy', 'KG', '1006', 5.00, 21.00, 26.00, 1000, 'Kolam Rice Paddy', 'Maharashtra variety', 'Kolam Original', 'MH Farmers', 0, 1, GETDATE(), 'System'),
(36, 'RICE-017', 'Kolam Rice', 'Finished Product', 'Rice', 'KG', '1006', 5.00, 43.00, 56.00, 500, 'Kolam White Rice', 'Light texture', 'Kolam Premium', 'In-house', 12, 1, GETDATE(), 'System'),

(37, 'CHEM-001', 'Silica Gel Packets', 'Consumable', 'Chemicals', 'PCS', '2811', 18.00, 0.50, 1.00, 5000, 'Moisture absorber', '10g packets', 'DryKeep', 'Supplier E', 0, 1, GETDATE(), 'System'),
(38, 'CHEM-002', 'Fumigation Tablets', 'Consumable', 'Chemicals', 'PCS', '3808', 18.00, 2.00, 3.50, 1000, 'Pest control', 'Aluminum phosphide', 'PestFree', 'Supplier F', 0, 1, GETDATE(), 'System'),

(39, 'MAINT-001', 'Machine Oil - 5L', 'Maintenance', 'Lubricants', 'LTR', '2710', 18.00, 250.00, 320.00, 50, 'Industrial machine oil', 'SAE 40 grade', 'LubeTech', 'Supplier G', 0, 1, GETDATE(), 'System'),
(40, 'MAINT-002', 'Belt Replacement Set', 'Maintenance', 'Spare Parts', 'SET', '4010', 18.00, 1500.00, 2000.00, 10, 'Conveyor belt set', 'For mill machines', 'PartsPro', 'Supplier H', 12, 1, GETDATE(), 'System'),

(41, 'RICE-018', 'Sticky Rice', 'Finished Product', 'Rice', 'KG', '1006', 5.00, 48.00, 62.00, 300, 'Glutinous Rice', 'Sweet rice variety', 'Sticky Sweet', 'In-house', 12, 1, GETDATE(), 'System'),
(42, 'RICE-019', 'Arborio Rice', 'Finished Product', 'Rice', 'KG', '1006', 5.00, 85.00, 110.00, 150, 'Italian Risotto Rice', 'Short grain, creamy', 'Italia Premium', 'In-house', 12, 1, GETDATE(), 'System'),
(43, 'RICE-020', 'Calrose Rice', 'Finished Product', 'Rice', 'KG', '1006', 5.00, 52.00, 68.00, 250, 'Medium Grain Rice', 'Slightly sticky', 'California Style', 'In-house', 12, 1, GETDATE(), 'System'),

(44, 'RAW-009', 'Mixed Paddy - Grade C', 'Raw Material', 'Paddy', 'KG', '1006', 5.00, 15.00, 19.00, 2000, 'Mixed Variety Paddy', 'Economy grade', 'Mixed Grain', 'Local Farmers', 0, 1, GETDATE(), 'System'),
(45, 'RICE-021', 'Mixed Rice - Economy', 'Finished Product', 'Rice', 'KG', '1006', 5.00, 28.00, 36.00, 1200, 'Economy Mixed Rice', 'Budget friendly', 'Value Pack', 'In-house', 12, 1, GETDATE(), 'System'),

(46, 'PKG-007', 'Vacuum Pack - 5 KG', 'Packaging', 'Bags', 'PCS', '3923', 18.00, 8.00, 12.00, 300, 'Vacuum sealed bag', 'Extended shelf life', 'VacuumPro', 'Supplier I', 0, 1, GETDATE(), 'System'),
(47, 'PKG-008', 'Brand Label Stickers', 'Packaging', 'Labels', 'SET', '4821', 18.00, 50.00, 75.00, 100, '1000 stickers per set', 'Custom printed', 'PrintMaster', 'Supplier J', 0, 1, GETDATE(), 'System'),

(48, 'BP-006', 'Rice Flour', 'By-Product', 'Flour', 'KG', '1102', 5.00, 18.00, 25.00, 200, 'Fine Rice Flour', 'From broken rice', 'Flour Fresh', 'In-house', 6, 1, GETDATE(), 'System'),
(49, 'BP-007', 'Puffed Rice', 'By-Product', 'Snack', 'KG', '1904', 12.00, 22.00, 32.00, 300, 'Puffed Rice Snack', 'Lightly salted', 'Snack Time', 'In-house', 6, 1, GETDATE(), 'System'),
(50, 'BP-008', 'Rice Flakes', 'By-Product', 'Flakes', 'KG', '1904', 5.00, 25.00, 35.00, 250, 'Poha - Rice Flakes', 'Thick variety', 'Breakfast Plus', 'In-house', 6, 1, GETDATE(), 'System');

SET IDENTITY_INSERT Products OFF;
PRINT '✓ Products: 50 records inserted';
GO

-- To be continued in next part due to size limits...
-- This is Part 1 of the comprehensive insertion script

PRINT '';
PRINT '========================================';
PRINT 'Part 1 Complete - Products Inserted';
PRINT '========================================';
GO
