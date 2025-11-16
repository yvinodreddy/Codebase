# RMMS Database Requirements

## Database Connection
**Server**: 172.17.208.1:1433
**Database Name**: RMMS_Production
**User**: rmms_user
**Password**: Welcome01!

## Connection Test Results
✅ Server Ping: SUCCESS (0% packet loss)
✅ Port 1433: OPEN and accessible
✅ Application Configuration: Verified

## Required Stored Procedures (40 Total)

### Authentication (1)
1. `sp_User_ValidateLogin` - Validates username and password hash
   - Input: @Username, @PasswordHash
   - Output: User record (Username, Email, Role, FullName)

### Dashboard (11)
2. `sp_Dashboard_GetTotalPaddyStock` - Returns total paddy stock quantity
3. `sp_Dashboard_GetTotalRiceStock` - Returns total rice stock quantity
4. `sp_Dashboard_GetMonthlyRevenue` - Returns current month revenue
5. `sp_Dashboard_GetPendingPaymentsCount` - Returns count of pending payments
6. `sp_Dashboard_GetTotalCustomers` - Returns total customer count
7. `sp_Dashboard_GetTotalSuppliers` - Returns total supplier count
8. `sp_Dashboard_GetMonthlySales` - Returns monthly sales data for charts
9. `sp_Dashboard_GetStockByVariety` - Returns stock grouped by variety
10. `sp_Dashboard_GetTotalReceivables` - Returns total outstanding receivables
11. `sp_Dashboard_GetTotalPayables` - Returns total outstanding payables
12. `sp_Dashboard_GetRecentTransactions` - Returns recent transaction list
13. `sp_Dashboard_GetAlerts` - Returns system alerts

### Paddy Procurement (8)
14. `sp_PaddyProcurement_GetAll` - Get all procurement records
15. `sp_PaddyProcurement_GetById` - Get single procurement by ID
16. `sp_PaddyProcurement_Insert` - Create new procurement
17. `sp_PaddyProcurement_Update` - Update existing procurement
18. `sp_PaddyProcurement_Delete` - Soft delete procurement (IsActive = 0)
19. `sp_PaddyProcurement_Search` - Search procurement records
20. `sp_PaddyProcurement_GetStockSummary` - Get stock summary
21. `sp_PaddyProcurement_GenerateVoucherNumber` - Generate voucher number

### Rice Sales (9)
22. `sp_RiceSales_GetAll` - Get all sales records
23. `sp_RiceSales_GetById` - Get single sale by ID
24. `sp_RiceSales_Insert` - Create new sale
25. `sp_RiceSales_Update` - Update existing sale
26. `sp_RiceSales_Delete` - Soft delete sale (IsActive = 0)
27. `sp_RiceSales_SearchByCustomer` - Search by customer name
28. `sp_RiceSales_GetPendingPayments` - Get pending payment records
29. `sp_RiceSales_GetTotalSales` - Get total sales amount
30. `sp_RiceSales_GenerateInvoiceNumber` - Generate invoice number

### By-Product Sales (10)
31. `sp_ByProductSales_GetAll` - Get all by-product sales
32. `sp_ByProductSales_GetById` - Get single record by ID
33. `sp_ByProductSales_Insert` - Create new by-product sale
34. `sp_ByProductSales_Update` - Update existing sale
35. `sp_ByProductSales_Delete` - Soft delete (IsActive = 0)
36. `sp_ByProductSales_GetByProductType` - Filter by product type
37. `sp_ByProductSales_GetByDateRange` - Filter by date range
38. `sp_ByProductSales_GetPendingPayments` - Get pending payments
39. `sp_ByProductSales_GetTotalByProduct` - Get total by product type
40. `sp_ByProductSales_GenerateTransactionNumber` - Generate transaction number

## Required Tables (Minimum)

### Users Table
```sql
- UserId (INT, PK, IDENTITY)
- Username (NVARCHAR(100), UNIQUE)
- PasswordHash (NVARCHAR(255))
- Email (NVARCHAR(255))
- Role (NVARCHAR(50))
- FullName (NVARCHAR(255))
- IsActive (BIT)
- CreatedDate (DATETIME)
```

### PaddyProcurement Table
```sql
- ProcurementId (INT, PK, IDENTITY)
- VoucherNumber (NVARCHAR(50), UNIQUE)
- SupplierName (NVARCHAR(255))
- ProcurementDate (DATE)
- PaddyVariety (NVARCHAR(100))
- Quantity (DECIMAL(18,2))
- Rate (DECIMAL(18,2))
- TotalAmount (DECIMAL(18,2))
- IsActive (BIT)
- CreatedDate (DATETIME)
- ModifiedDate (DATETIME)
```

### RiceSales Table
```sql
- SaleId (INT, PK, IDENTITY)
- InvoiceNumber (NVARCHAR(50), UNIQUE)
- CustomerName (NVARCHAR(255))
- CustomerAddress (NVARCHAR(500))
- SaleDate (DATE)
- RiceVariety (NVARCHAR(100))
- Quantity (DECIMAL(18,2))
- Rate (DECIMAL(18,2))
- SubTotal (DECIMAL(18,2))
- CGST (DECIMAL(18,2))
- SGST (DECIMAL(18,2))
- IGST (DECIMAL(18,2))
- TotalAmount (DECIMAL(18,2))
- AmountPaid (DECIMAL(18,2))
- BalanceDue (DECIMAL(18,2))
- IsActive (BIT)
- CreatedDate (DATETIME)
- ModifiedDate (DATETIME)
```

### ByProductSales Table
```sql
- SaleId (INT, PK, IDENTITY)
- TransactionNumber (NVARCHAR(50), UNIQUE)
- ProductType (NVARCHAR(100))
- BuyerName (NVARCHAR(255))
- SaleDate (DATE)
- Quantity (DECIMAL(18,2))
- Rate (DECIMAL(18,2))
- TotalAmount (DECIMAL(18,2))
- AmountPaid (DECIMAL(18,2))
- BalanceDue (DECIMAL(18,2))
- IsActive (BIT)
- CreatedDate (DATETIME)
- ModifiedDate (DATETIME)
```

### CashBook Table
```sql
- EntryId (INT, PK, IDENTITY)
- EntryDate (DATE)
- Particulars (NVARCHAR(500))
- VoucherNumber (NVARCHAR(50))
- Receipts (DECIMAL(18,2))
- Payments (DECIMAL(18,2))
- Balance (DECIMAL(18,2))
- IsActive (BIT)
- CreatedDate (DATETIME)
```

### BankTransactions Table
```sql
- TransactionId (INT, PK, IDENTITY)
- TransactionDate (DATE)
- BankName (NVARCHAR(255))
- AccountNumber (NVARCHAR(50))
- TransactionType (NVARCHAR(50)) -- 'Deposit', 'Withdrawal', 'Transfer'
- Amount (DECIMAL(18,2))
- Particulars (NVARCHAR(500))
- ChequeNumber (NVARCHAR(50))
- IsReconciled (BIT)
- IsActive (BIT)
- CreatedDate (DATETIME)
```

### PayablesOverdue Table
```sql
- PayableId (INT, PK, IDENTITY)
- VendorName (NVARCHAR(255))
- InvoiceNumber (NVARCHAR(50))
- InvoiceDate (DATE)
- DueDate (DATE)
- TotalAmount (DECIMAL(18,2))
- AmountPaid (DECIMAL(18,2))
- BalancePayable (DECIMAL(18,2))
- DaysOverdue (INT, COMPUTED)
- IsActive (BIT)
```

### ReceivablesOverdue Table
```sql
- ReceivableId (INT, PK, IDENTITY)
- CustomerName (NVARCHAR(255))
- InvoiceNumber (NVARCHAR(50))
- InvoiceDate (DATE)
- DueDate (DATE)
- TotalAmount (DECIMAL(18,2))
- AmountReceived (DECIMAL(18,2))
- BalanceDue (DECIMAL(18,2))
- DaysOverdue (INT, COMPUTED)
- IsActive (BIT)
```

### LoansAdvances Table
```sql
- LoanId (INT, PK, IDENTITY)
- LoanType (NVARCHAR(50)) -- 'Loan Taken', 'Loan Given', 'Advance'
- PartyName (NVARCHAR(255))
- Amount (DECIMAL(18,2))
- InterestRate (DECIMAL(5,2))
- StartDate (DATE)
- DueDate (DATE)
- Balance (DECIMAL(18,2))
- RepaymentDate (DATETIME)
- IsActive (BIT)
```

### FixedAssets Table
```sql
- AssetId (INT, PK, IDENTITY)
- AssetName (NVARCHAR(255))
- AssetType (NVARCHAR(100))
- PurchaseDate (DATE)
- PurchaseAmount (DECIMAL(18,2))
- CurrentValue (DECIMAL(18,2))
- DepreciationRate (DECIMAL(5,2))
- Location (NVARCHAR(255))
- IsActive (BIT)
```

### Customers Table (for Dashboard)
```sql
- CustomerId (INT, PK, IDENTITY)
- CustomerName (NVARCHAR(255))
- ContactNumber (NVARCHAR(20))
- Address (NVARCHAR(500))
- IsActive (BIT)
```

### Suppliers Table (for Dashboard)
```sql
- SupplierId (INT, PK, IDENTITY)
- SupplierName (NVARCHAR(255))
- ContactNumber (NVARCHAR(20))
- Address (NVARCHAR(500))
- IsActive (BIT)
```

## Sample Test Data Required

### Test User
```sql
INSERT INTO Users (Username, PasswordHash, Email, Role, FullName, IsActive, CreatedDate)
VALUES (
  'admin',
  '$2a$11$...' -- BCrypt hash of 'admin123'
  'admin@rmms.com',
  'Administrator',
  'System Administrator',
  1,
  GETDATE()
)
```

**Note**: Use BCrypt.Net to generate the password hash:
```csharp
string hash = BCrypt.Net.BCrypt.HashPassword("admin123");
```

## Database Setup Script Generation

To generate complete database scripts:

1. **Create Database**:
```sql
CREATE DATABASE RMMS_Production;
GO
USE RMMS_Production;
GO
```

2. **Create Tables** (in order of dependencies)
3. **Create Stored Procedures** (40 procedures listed above)
4. **Insert Test Data** (at minimum, one test user)

## Testing Checklist

After database setup:
- [ ] Can connect to database from application
- [ ] sp_User_ValidateLogin works with test credentials
- [ ] Dashboard stored procedures return data (or 0 for empty DB)
- [ ] CRUD operations work for all modules
- [ ] Soft delete (IsActive = 0) works correctly
- [ ] Computed columns (DaysOverdue) calculate correctly
- [ ] Auto-number generation procedures work
- [ ] No NULL reference exceptions on dashboard

## Security Considerations

1. **User Password**: Currently uses BCrypt hashing ✅
2. **SQL Injection**: Using parameterized queries via DatabaseHelper ✅
3. **Soft Delete**: Using IsActive flag instead of hard delete ✅
4. **Authentication**: Cookie-based authentication configured ✅
5. **Authorization**: Inconsistent - most pages don't require auth ⚠️

## Next Steps

1. Execute database creation script on 172.17.208.1
2. Create all 40 stored procedures
3. Create test user with BCrypt hashed password
4. Verify connection from application
5. Resume testing from Phase 2

---

**Document Created**: 2025-10-01
**Database Server**: 172.17.208.1:1433
**Total Stored Procedures**: 40
**Total Tables**: 12 minimum
