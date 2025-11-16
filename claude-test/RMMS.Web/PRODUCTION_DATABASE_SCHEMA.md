# Production Database Schema Documentation
## Sprint 3: Production & Milling Operations

**Created:** 2025-10-06
**Database:** RMMS_Production
**Schema Version:** 1.0
**Total Tables:** 6

---

## 📊 OVERVIEW

The production database schema supports complete rice milling operations tracking, from production planning through batch execution to yield analysis.

**Total Columns:** 133
**Foreign Keys:** 17
**Unique Constraints:** 3
**Performance Indexes:** 24

---

## 🗄️ TABLE DEFINITIONS

### 1. Machines (Equipment Master)

**Purpose:** Track all rice milling equipment and machinery

**Columns:** 25

| Column | Type | Description |
|--------|------|-------------|
| Id | INT IDENTITY | Primary key |
| MachineCode | NVARCHAR(20) | Unique machine code (MACH0001...) |
| MachineName | NVARCHAR(100) | Machine name |
| MachineType | NVARCHAR(50) | Cleaner, Husker, Polisher, Grader, Separator, Dryer, Weighbridge |
| Manufacturer | NVARCHAR(100) | Equipment manufacturer |
| ModelNumber | NVARCHAR(50) | Model number |
| Capacity | DECIMAL(18,3) | Processing capacity |
| CapacityUnit | NVARCHAR(20) | tons/hour, bags/hour, kg/hour, quintals/hour |
| Location | NVARCHAR(100) | Physical location |
| Specifications | NVARCHAR(500) | Technical specifications |
| PurchaseDate | DATE | Purchase date |
| PurchasePrice | DECIMAL(18,2) | Original purchase price |
| CurrentValue | DECIMAL(18,2) | Current depreciated value |
| Status | NVARCHAR(20) | Operational, Maintenance, Breakdown, Idle |
| RunningHours | DECIMAL(18,2) | Total running hours |
| LastMaintenanceDate | DATE | Last maintenance performed |
| NextMaintenanceDue | DATE | Next scheduled maintenance |
| MaintenanceIntervalHours | INT | Hours between maintenance |
| Remarks | NVARCHAR(500) | Additional notes |
| CreatedDate | DATETIME | Record creation date |
| CreatedBy | NVARCHAR(100) | Created by user |
| ModifiedDate | DATETIME | Last modification date |
| ModifiedBy | NVARCHAR(100) | Modified by user |
| IsActive | BIT | Active flag (soft delete) |

**Indexes:**
- Unique on MachineCode
- IX_Machines_Type (MachineType) INCLUDE (MachineName, Status)
- IX_Machines_Status (Status) INCLUDE (MachineCode, MachineName)
- IX_Machines_Active (IsActive) INCLUDE (MachineCode, MachineName, MachineType)

**Constraints:**
- CHK_Machines_Capacity: Capacity >= 0
- CHK_Machines_Status: Status IN ('Operational', 'Maintenance', 'Breakdown', 'Idle')

---

### 2. ProductionOrders (Production Planning)

**Purpose:** Plan and schedule production runs

**Columns:** 30

| Column | Type | Description |
|--------|------|-------------|
| Id | INT IDENTITY | Primary key |
| OrderNumber | NVARCHAR(20) | Unique order number (PO0001...) |
| OrderDate | DATE | Order creation date |
| ScheduledDate | DATE | Scheduled production date |
| SourceType | NVARCHAR(20) | Procurement or Inventory |
| SourceId | INT | Reference to source |
| SourceReferenceNumber | NVARCHAR(100) | Source document number |
| PaddyProductId | INT | FK to Products (paddy) |
| PaddyVariety | NVARCHAR(50) | Paddy variety name |
| PaddyQuantity | DECIMAL(18,3) | Paddy input quantity |
| PaddyUOM | NVARCHAR(10) | Unit of measure |
| TargetRiceProductId | INT | FK to Products (rice) |
| TargetRiceGrade | NVARCHAR(50) | Target rice grade |
| TargetQuantity | DECIMAL(18,3) | Target output quantity |
| ExpectedYieldPercent | DECIMAL(5,2) | Expected yield % |
| Priority | NVARCHAR(20) | Low, Normal, High, Urgent |
| AssignedMachineId | INT | FK to Machines |
| AssignedSupervisorId | INT | FK to Employees |
| CustomerOrderId | INT | FK to customer order (future) |
| CustomerOrderNumber | NVARCHAR(50) | Customer order reference |
| Status | NVARCHAR(20) | Draft, Scheduled, In Progress, Completed, Closed, Cancelled |
| ActualStartDate | DATETIME | Actual start date/time |
| ActualCompletionDate | DATETIME | Actual completion date/time |
| ActualQuantityProduced | DECIMAL(18,3) | Actual output quantity |
| ActualYieldPercent | DECIMAL(5,2) | Actual yield achieved |
| Remarks | NVARCHAR(500) | General remarks |
| SpecialInstructions | NVARCHAR(500) | Special instructions |
| CreatedDate | DATETIME | Record creation date |
| CreatedBy | NVARCHAR(100) | Created by user |
| ModifiedDate | DATETIME | Last modification date |
| ModifiedBy | NVARCHAR(100) | Modified by user |
| IsActive | BIT | Active flag |

**Foreign Keys:**
- PaddyProductId → Products(Id)
- TargetRiceProductId → Products(Id)
- AssignedMachineId → Machines(Id)
- AssignedSupervisorId → Employees(Id)

**Indexes:**
- Unique on OrderNumber
- IX_ProductionOrders_Status (Status, ScheduledDate)
- IX_ProductionOrders_Date (ScheduledDate DESC)
- IX_ProductionOrders_Machine (AssignedMachineId)
- IX_ProductionOrders_Active (IsActive) INCLUDE (OrderNumber, Status)

**Constraints:**
- CHK_ProductionOrders_Quantity: PaddyQuantity > 0
- CHK_ProductionOrders_Status: Status IN ('Draft', 'Scheduled', 'In Progress', 'Completed', 'Closed', 'Cancelled')

---

### 3. ProductionBatches (Batch Execution)

**Purpose:** Track actual production batch execution

**Columns:** 20

| Column | Type | Description |
|--------|------|-------------|
| Id | INT IDENTITY | Primary key |
| BatchNumber | NVARCHAR(20) | Unique batch number (BATCH0001...) |
| ProductionOrderId | INT | FK to ProductionOrders |
| BatchDate | DATE | Batch execution date |
| ShiftType | NVARCHAR(20) | Morning, Evening, Night |
| OperatorId | INT | FK to Employees (operator) |
| SupervisorId | INT | FK to Employees (supervisor) |
| StartTime | DATETIME | Batch start time |
| EndTime | DATETIME | Batch end time |
| Status | NVARCHAR(20) | Planned, In Progress, Completed, Verified, Cancelled |
| CompletionPercent | DECIMAL(5,2) | Completion percentage |
| QualityScore | DECIMAL(3,1) | Quality score (1-10) |
| QualityRemarks | NVARCHAR(500) | Quality remarks |
| Remarks | NVARCHAR(500) | General remarks |
| Issues | NVARCHAR(500) | Issues/problems encountered |
| CreatedDate | DATETIME | Record creation date |
| CreatedBy | NVARCHAR(100) | Created by user |
| ModifiedDate | DATETIME | Last modification date |
| ModifiedBy | NVARCHAR(100) | Modified by user |
| IsActive | BIT | Active flag |

**Foreign Keys:**
- ProductionOrderId → ProductionOrders(Id)
- OperatorId → Employees(Id)
- SupervisorId → Employees(Id)

**Indexes:**
- Unique on BatchNumber
- IX_ProductionBatches_Order (ProductionOrderId)
- IX_ProductionBatches_Date (BatchDate DESC)
- IX_ProductionBatches_Status (Status) INCLUDE (BatchNumber)
- IX_ProductionBatches_Active (IsActive)

**Constraints:**
- CHK_ProductionBatches_Status: Status IN ('Planned', 'In Progress', 'Completed', 'Verified', 'Cancelled')
- CHK_ProductionBatches_Completion: CompletionPercent BETWEEN 0 AND 100

---

### 4. BatchInputs (Material Consumption)

**Purpose:** Track raw materials consumed in production batches

**Columns:** 15

| Column | Type | Description |
|--------|------|-------------|
| Id | INT IDENTITY | Primary key |
| BatchId | INT | FK to ProductionBatches |
| InputType | NVARCHAR(50) | Paddy, Water, Energy, etc. |
| ProductId | INT | FK to Products |
| Quantity | DECIMAL(18,3) | Quantity consumed |
| UOM | NVARCHAR(10) | Unit of measure |
| WarehouseId | INT | FK to Warehouses (source) |
| ZoneId | INT | FK to StorageZones (source) |
| MoistureContent | DECIMAL(5,2) | Moisture content % |
| BatchLotNumber | NVARCHAR(50) | Batch/lot traceability |
| Grade | NVARCHAR(50) | Quality grade |
| UnitCost | DECIMAL(18,2) | Unit cost |
| Remarks | NVARCHAR(500) | Additional notes |
| CreatedDate | DATETIME | Record creation date |
| CreatedBy | NVARCHAR(100) | Created by user |

**Foreign Keys:**
- BatchId → ProductionBatches(Id) ON DELETE CASCADE
- ProductId → Products(Id)
- WarehouseId → Warehouses(Id)
- ZoneId → StorageZones(Id) ON DELETE SET NULL

**Indexes:**
- IX_BatchInputs_Batch (BatchId)
- IX_BatchInputs_Product (ProductId)
- IX_BatchInputs_Warehouse (WarehouseId)

**Constraints:**
- CHK_BatchInputs_Quantity: Quantity > 0

---

### 5. BatchOutputs (Product Output)

**Purpose:** Track products produced from production batches

**Columns:** 18

| Column | Type | Description |
|--------|------|-------------|
| Id | INT IDENTITY | Primary key |
| BatchId | INT | FK to ProductionBatches |
| OutputType | NVARCHAR(50) | Rice, Bran, Husk, Broken Rice |
| ProductId | INT | FK to Products |
| Grade | NVARCHAR(50) | Quality grade |
| Quantity | DECIMAL(18,3) | Quantity produced |
| UOM | NVARCHAR(10) | Unit of measure |
| WarehouseId | INT | FK to Warehouses (destination) |
| ZoneId | INT | FK to StorageZones (destination) |
| QualityScore | DECIMAL(3,1) | Quality score (1-10) |
| MoistureContent | DECIMAL(5,2) | Moisture content % |
| BatchLotNumber | NVARCHAR(50) | Batch/lot traceability |
| UnitCost | DECIMAL(18,2) | Unit cost (calculated) |
| BagsCount | INT | Number of bags |
| BagsWeight | DECIMAL(8,2) | Weight per bag (kg) |
| Remarks | NVARCHAR(500) | Additional notes |
| CreatedDate | DATETIME | Record creation date |
| CreatedBy | NVARCHAR(100) | Created by user |

**Foreign Keys:**
- BatchId → ProductionBatches(Id) ON DELETE CASCADE
- ProductId → Products(Id)
- WarehouseId → Warehouses(Id)
- ZoneId → StorageZones(Id) ON DELETE SET NULL

**Indexes:**
- IX_BatchOutputs_Batch (BatchId)
- IX_BatchOutputs_Product (ProductId)
- IX_BatchOutputs_Warehouse (WarehouseId)
- IX_BatchOutputs_Type (OutputType)

**Constraints:**
- CHK_BatchOutputs_Quantity: Quantity > 0

---

### 6. YieldRecords (Yield Analysis)

**Purpose:** Calculate and track production yield metrics

**Columns:** 25

| Column | Type | Description |
|--------|------|-------------|
| Id | INT IDENTITY | Primary key |
| BatchId | INT | FK to ProductionBatches (UNIQUE - One-to-One) |
| PaddyVariety | NVARCHAR(100) | Paddy variety |
| InputPaddyQuantity | DECIMAL(18,3) | Total paddy input |
| OutputHeadRice | DECIMAL(18,3) | Head rice output |
| OutputBrokenRice | DECIMAL(18,3) | Broken rice output |
| OutputBran | DECIMAL(18,3) | Bran output |
| OutputHusk | DECIMAL(18,3) | Husk output |
| OutputWastage | DECIMAL(18,3) | Wastage |
| HeadRicePercent | DECIMAL(5,2) | Head rice % |
| BrokenRicePercent | DECIMAL(5,2) | Broken rice % |
| BranPercent | DECIMAL(5,2) | Bran % |
| HuskPercent | DECIMAL(5,2) | Husk % |
| WastagePercent | DECIMAL(5,2) | Wastage % |
| TotalYieldPercent | DECIMAL(5,2) | Total yield % |
| StandardHeadRicePercent | DECIMAL(5,2) | Expected head rice % (65%) |
| StandardTotalYieldPercent | DECIMAL(5,2) | Expected total yield % (98%) |
| YieldGrade | NVARCHAR(20) | Excellent, Good, Average, Poor |
| QualityScore | DECIMAL(3,1) | Quality score (1-10) |
| MillingRecovery | DECIMAL(5,2) | Total rice recovery % |
| HeadRiceToBrokenRatio | DECIMAL(5,2) | Head rice to broken rice ratio |
| Remarks | NVARCHAR(500) | Analysis remarks |
| VarianceAnalysis | NVARCHAR(500) | Variance explanation |
| IsVerified | BIT | Verification flag |
| VerifiedBy | NVARCHAR(100) | Verified by user |
| VerifiedDate | DATETIME | Verification date |
| CalculatedDate | DATETIME | Calculation date |
| CalculatedBy | NVARCHAR(100) | Calculated by user |

**Foreign Keys:**
- BatchId → ProductionBatches(Id) ON DELETE CASCADE (UNIQUE)

**Indexes:**
- Unique on BatchId (enforces one-to-one relationship)
- IX_YieldRecords_Batch (BatchId)
- IX_YieldRecords_Grade (YieldGrade)
- IX_YieldRecords_Date (CalculatedDate DESC)
- IX_YieldRecords_Variety (PaddyVariety) INCLUDE (HeadRicePercent)

**Constraints:**
- CHK_YieldRecords_InputQty: InputPaddyQuantity > 0
- CHK_YieldRecords_Grade: YieldGrade IN ('Excellent', 'Good', 'Average', 'Poor')

**Yield Grading Logic:**
- Excellent: Head Rice % >= 68%
- Good: Head Rice % >= 62%
- Average: Head Rice % >= 55%
- Poor: Head Rice % < 55%

---

## 🔗 RELATIONSHIP DIAGRAM

```
Products ←─┐
           │
Machines ──┼─→ ProductionOrders ──→ ProductionBatches ──┬─→ BatchInputs ──→ Warehouses
           │                                             │                    StorageZones
Employees ─┘                                             ├─→ BatchOutputs ──→ Warehouses
                                                         │                    StorageZones
                                                         └─→ YieldRecords (1:1)
```

---

## 📈 DATA FLOW

### Production Workflow

1. **Planning Phase**
   - Create ProductionOrder
   - Assign machine and supervisor
   - Set expected yields

2. **Execution Phase**
   - Create ProductionBatch linked to order
   - Record BatchInputs (deduct from inventory)
   - Record batch progress

3. **Completion Phase**
   - Record BatchOutputs (add to inventory)
   - Calculate YieldRecord automatically
   - Grade yield performance

4. **Analysis Phase**
   - Review yield variances
   - Verify quality scores
   - Analyze by variety, machine, date

---

## 🎯 KEY METRICS TRACKED

### Machine Metrics
- Total running hours
- Maintenance schedule adherence
- Operational vs downtime
- Depreciation tracking

### Production Metrics
- Orders by status
- Orders by priority
- On-time completion rate
- Planned vs actual quantities

### Batch Metrics
- Batches per shift
- Batches per machine
- Average batch duration
- Quality scores by operator

### Yield Metrics
- Head rice recovery %
- Broken rice %
- By-product recovery (bran, husk)
- Wastage %
- Variance from standard

---

## 🔒 DATA INTEGRITY FEATURES

### Referential Integrity
- 17 foreign key constraints
- Cascade deletes for batch inputs/outputs
- Set NULL for optional zone references
- Restrict on products/warehouses

### Data Validation
- Check constraints on status values
- Quantity validation (> 0)
- Percentage validation (0-100)
- Grade enumeration validation

### Audit Trail
- CreatedBy/CreatedDate on all tables
- ModifiedBy/ModifiedDate for updates
- IsActive for soft deletes
- Verification workflow on yields

---

## 📊 INDEXES SUMMARY

**Total Indexes:** 24

### By Purpose
- **Unique Constraints:** 4 (MachineCode, OrderNumber, BatchNumber, BatchId in YieldRecords)
- **Foreign Key Indexes:** 10
- **Query Performance:** 10
- **Active Record Filtering:** 4

### Coverage
- All foreign keys indexed
- All unique codes indexed
- All status fields indexed
- All date fields indexed for sorting

---

## 💾 STORAGE ESTIMATES

### Per 1000 Records

| Table | Estimated Size |
|-------|----------------|
| Machines | ~150 KB |
| ProductionOrders | ~200 KB |
| ProductionBatches | ~150 KB |
| BatchInputs | ~120 KB |
| BatchOutputs | ~140 KB |
| YieldRecords | ~180 KB |

**Total per 1000 batches:** ~940 KB

**Estimated for 1 year (5000 batches):** ~4.7 MB

---

## 🔧 MAINTENANCE NOTES

### Regular Maintenance
- Rebuild indexes quarterly
- Update statistics monthly
- Archive completed batches yearly
- Review yield standards quarterly

### Performance Optimization
- All critical queries covered by indexes
- Cascade deletes minimize orphaned records
- Soft deletes preserve history
- Computed columns avoid redundant storage

---

## 📝 MIGRATION SCRIPT

**File:** `05_CreateProductionTables.sql`

**Pre-requisites:**
- Products table must exist
- Employees table must exist
- Warehouses table must exist
- StorageZones table must exist

**Execution Time:** < 1 second

**Rollback:** Drop tables in reverse order (YieldRecords → BatchOutputs → BatchInputs → ProductionBatches → ProductionOrders → Machines)

---

**Schema Version:** 1.0
**Last Updated:** 2025-10-06
**Maintained By:** RMMS Development Team
