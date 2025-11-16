# Comprehensive Schema Mapping Document
**Generated:** 2025-10-13
**Purpose:** Fix all 168+ compilation errors in analytics services

---

## CRITICAL MODEL SCHEMA MAPPINGS

### 1. RiceSales Model
**Service Expects → Actual Schema:**
- `CustomerId` (int) → **NOT EXISTS** (use `BuyerName` string)
- `Customer` (navigation) → **NOT EXISTS** (use `BuyerName` string)
- `Product` (navigation) → **NOT EXISTS** (use `RiceGrade` string)
- `ProductId` (int) → **NOT EXISTS** (use `RiceGrade` string)
- `TotalAmount` (decimal) → `TotalInvoiceValue` (decimal) ✅
- **Actual Properties:**
  - `BuyerName` (string)
  - `BuyerAddress` (string)
  - `RiceGrade` (string)
  - `Quantity` (decimal)
  - `UnitPrice` (decimal)
  - `TotalInvoiceValue` (decimal)
  - `SaleDate` (DateTime)

### 2. PaddyProcurement Model
**Service Expects → Actual Schema:**
- `ProcurementDate` (DateTime) → `ReceiptDate` (DateTime) ✅
- `Vendor` (navigation) → **NOT EXISTS** (use `SupplierName` string)
- `VendorId` (int) → **NOT EXISTS** (use `SupplierName` string)
- **Actual Properties:**
  - `ReceiptDate` (DateTime)
  - `SupplierName` (string)
  - `PaddyVariety` (string)
  - `QuantityReceived` (decimal)
  - `TotalNetWeight` (decimal)

### 3. ProductionOrder Model
**Service Expects → Actual Schema:**
- `MachineId` (int) → `AssignedMachineId` (int?) ✅
- `Machine` (navigation) → `AssignedMachine` (Machine?) ✅
- `StartDate` (DateTime) → `ActualStartDate` (DateTime?) ✅
- **Actual Properties:**
  - `AssignedMachineId` (int?)
  - `AssignedMachine` (Machine?)
  - `ActualStartDate` (DateTime?)
  - `ActualCompletionDate` (DateTime?)
  - `OrderDate` (DateTime)
  - `ScheduledDate` (DateTime)

### 4. ProductionBatch Model
**Service Expects → Actual Schema:**
- `TotalInputQuantity` → ✅ CORRECT (computed NotMapped property)
- `TotalOutputQuantity` → ✅ CORRECT (computed NotMapped property)
- `BatchDate` → ✅ CORRECT
- `Status` → ✅ CORRECT
- `ShiftType` → ✅ CORRECT

### 5. Product Model
**Service Expects → Actual Schema:**
- `CostPrice` (decimal) → **NOT EXISTS** (use `StandardCost` decimal?) ✅
- **Actual Properties:**
  - `StandardCost` (decimal?)
  - `SellingPrice` (decimal?)
  - `ProductName` (string)
  - `ProductCode` (string)
  - `ProductCategory` (string)

---

## DTO PROPERTY MAPPINGS

### ProductionDashboardDto
**Service Uses → Actual DTO Properties:**
- `TotalBatchesProduced` → **NOT EXISTS** (use `CompletedBatchesToday`)
- `CompletedBatches` → `CompletedBatchesToday` ✅
- `InProgressBatches` → `RunningBatches` ✅
- `PlannedBatches` → **NOT EXISTS**
- `TotalOutputQuantity` → `TodayOutput` ✅
- `AverageEfficiency` → `OverallEfficiency` ✅
- `MachineUtilization` → **NOT EXISTS** (use lists)
- `QualityScore` → **NOT EXISTS** (use lists)
- `DefectRate` → **NOT EXISTS** (use lists)

**Actual DTO Definition:**
```csharp
public class ProductionDashboardDto
{
    public decimal OverallOEE { get; set; }
    public decimal OverallEfficiency { get; set; }
    public int ActiveMachines { get; set; }
    public int TotalMachines { get; set; }
    public decimal TodayOutput { get; set; }
    public decimal TodayTarget { get; set; }
    public int RunningBatches { get; set; }
    public int CompletedBatchesToday { get; set; }
    public List<ProductionEfficiencyDto> MachineEfficiencies { get; set; }
    public List<DowntimeAnalysisDto> TopDowntimeReasons { get; set; }
    public List<QualityMetricsDto> RecentQualityMetrics { get; set; }
}
```

### ProductionEfficiencyDto
**Service Uses → Actual DTO Properties:**
- `TotalBatches` → **NOT EXISTS**
- `TotalInputQuantity` → **NOT EXISTS**
- `TotalOutputQuantity` → **NOT EXISTS**
- `OverallEfficiency` → `EfficiencyPercentage` ✅
- `AverageOutputPerBatch` → **NOT EXISTS**
- `TotalProductionTime` → **NOT EXISTS**
- `StartDate` → **NOT EXISTS**
- `EndDate` → **NOT EXISTS**

**Actual DTO Definition:**
```csharp
public class ProductionEfficiencyDto
{
    public int MachineId { get; set; }
    public string MachineName { get; set; }
    public decimal EfficiencyPercentage { get; set; }
    public decimal OEE { get; set; }
    public decimal AvailabilityPercentage { get; set; }
    public decimal PerformancePercentage { get; set; }
    public decimal QualityPercentage { get; set; }
    public int TotalDowntimeMinutes { get; set; }
    public int PlannedProductionMinutes { get; set; }
    public decimal ActualOutput { get; set; }
    public decimal PlannedOutput { get; set; }
    public string Status { get; set; }
}
```

### ShiftPerformanceDto
**Service Uses → Actual DTO Properties:**
- `ShiftType` → `ShiftName` ✅
- `TotalBatches` → `NumberOfBatches` ✅
- `CompletedBatches` → **NOT EXISTS**
- `TotalOutput` → ✅ CORRECT
- `AverageOutput` → **NOT EXISTS**
- `AverageEfficiency` → `EfficiencyPercentage` ✅
- `AverageQualityScore` → **NOT EXISTS**

**Actual DTO Definition:**
```csharp
public class ShiftPerformanceDto
{
    public string ShiftName { get; set; }
    public DateTime Date { get; set; }
    public decimal TotalOutput { get; set; }
    public decimal PlannedOutput { get; set; }
    public decimal EfficiencyPercentage { get; set; }
    public int NumberOfBatches { get; set; }
    public decimal AverageYieldPercentage { get; set; }
    public int DowntimeMinutes { get; set; }
}
```

---

## INVENTORY ANALYTICS DTOs

### ABCClassificationDto
**Service Uses → Actual DTO:**
- `ConsumptionValue` → **NOT EXISTS**
- `ConsumptionQuantity` → **NOT EXISTS**
- `ValuePercentage` → **NOT EXISTS**
- `Classification` → **NOT EXISTS**

*Need to read actual interface to get correct properties*

### StockAlertDto
**Service Uses → Actual DTO:**
- `WarehouseId` → **NOT EXISTS**
- `WarehouseName` → **NOT EXISTS**
- `Threshold` → **NOT EXISTS**

*Need to read actual interface to get correct properties*

---

## COMPREHENSIVE ANALYTICS SERVICES DTOs

### Sales/Customer Related:
**RiceSales Query Issues:**
```csharp
// WRONG:
.Where(s => s.CustomerId == customerId)
.GroupBy(s => s.Product.ProductName)
.Sum(s => s.TotalAmount)

// CORRECT:
.Where(s => s.BuyerName == buyerName)  // Use string comparison
.GroupBy(s => s.RiceGrade)  // Use RiceGrade, not Product
.Sum(s => s.TotalInvoiceValue)  // Use TotalInvoiceValue, not TotalAmount
```

### Supplier Performance:
**PaddyProcurement Query Issues:**
```csharp
// WRONG:
.Where(p => p.Vendor.VendorName == name)
.OrderBy(p => p.ProcurementDate)

// CORRECT:
.Where(p => p.SupplierName == name)  // Direct string property
.OrderBy(p => p.ReceiptDate)  // Use ReceiptDate, not ProcurementDate
```

### Cost Analysis:
**Product Query Issues:**
```csharp
// WRONG:
.Select(p => p.CostPrice)

// CORRECT:
.Select(p => p.StandardCost ?? 0)  // Use StandardCost (nullable)
```

---

## LINQ QUERY PATTERN FIXES

### Pattern 1: RiceSales Aggregation
```csharp
// BEFORE (WRONG):
var salesByCustomer = await _context.RiceSales
    .Where(s => s.CustomerId == customerId)
    .Include(s => s.Product)
    .GroupBy(s => s.Product.ProductName)
    .Select(g => new {
        Product = g.Key,
        Total = g.Sum(s => s.TotalAmount)
    });

// AFTER (CORRECT):
var salesByGrade = await _context.RiceSales
    .Where(s => s.BuyerName == buyerName)  // String match
    .GroupBy(s => s.RiceGrade)  // No navigation needed
    .Select(g => new {
        Grade = g.Key,
        Total = g.Sum(s => s.TotalInvoiceValue)  // Correct property
    });
```

### Pattern 2: PaddyProcurement with Supplier
```csharp
// BEFORE (WRONG):
var procurements = await _context.PaddyProcurements
    .Include(p => p.Vendor)
    .Where(p => p.ProcurementDate >= startDate)
    .GroupBy(p => p.Vendor.VendorName);

// AFTER (CORRECT):
var procurements = await _context.PaddyProcurements
    .Where(p => p.ReceiptDate >= startDate)  // Correct date property
    .GroupBy(p => p.SupplierName);  // Direct string property
```

### Pattern 3: ProductionOrder with Machine
```csharp
// BEFORE (WRONG):
var orders = await _context.ProductionOrders
    .Where(o => o.MachineId == machineId && o.StartDate >= startDate);

// AFTER (CORRECT):
var orders = await _context.ProductionOrders
    .Where(o => o.AssignedMachineId == machineId && o.ActualStartDate >= startDate);
```

---

## FIX PRIORITY ORDER

### Phase 1: Critical Model Property Fixes
1. Replace `MachineId` → `AssignedMachineId` (17 occurrences)
2. Replace `StartDate` → `ActualStartDate` (12 occurrences)
3. Replace `Machine` → `AssignedMachine` (8 occurrences)

### Phase 2: RiceSales Fixes
1. Remove all `.Include(s => s.Product)` (15+ occurrences)
2. Remove all `.Include(s => s.Customer)` (10+ occurrences)
3. Replace `s.CustomerId` → `s.BuyerName` comparisons (25+ occurrences)
4. Replace `s.Product.ProductName` → `s.RiceGrade` (20+ occurrences)
5. Replace `s.TotalAmount` → `s.TotalInvoiceValue` (30+ occurrences)

### Phase 3: PaddyProcurement Fixes
1. Remove all `.Include(p => p.Vendor)` (10 occurrences)
2. Replace `p.ProcurementDate` → `p.ReceiptDate` (15 occurrences)
3. Replace `p.Vendor.VendorName` → `p.SupplierName` (12 occurrences)

### Phase 4: Product Fixes
1. Replace `p.CostPrice` → `p.StandardCost ?? 0` (8 occurrences)

### Phase 5: DTO Property Fixes
1. Fix ProductionDashboardDto assignments (15 properties)
2. Fix ProductionEfficiencyDto assignments (20 properties)
3. Fix ShiftPerformanceDto assignments (10 properties)
4. Fix all other DTOs based on actual interfaces

---

## ESTIMATED ERROR COUNTS

| Service File | Errors | Fix Time |
|---|---|---|
| ProductionAnalyticsService | 45 | 2 hours |
| InventoryAnalyticsService | 38 | 2 hours |
| ComprehensiveAnalyticsServices | 85 | 3 hours |
| **TOTAL** | **168** | **7 hours** |

---

## SUCCESS CRITERIA

✅ **Build succeeds with 0 errors**
✅ **All 8 services register successfully**
✅ **DTOs match interface definitions 100%**
✅ **LINQ queries use correct model properties**
✅ **No navigation properties to non-existent relationships**

---

*This document provides the complete roadmap for fixing all analytics service issues*
