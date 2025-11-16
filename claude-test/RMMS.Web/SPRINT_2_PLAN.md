# 📋 SPRINT 2 PLAN - Inventory Management

**Sprint:** Sprint 2
**Module:** Inventory Management System
**Duration:** 2 weeks (Phase 1 - Weeks 3-4)
**Status:** 🟡 Planning

---

## 🎯 Sprint Goals

Build a comprehensive inventory management system for the rice mill that tracks:
1. Warehouse locations and storage zones
2. Real-time stock levels for all products
3. Stock movements (in/out transactions)
4. Stock adjustments and reconciliation
5. Inventory dashboard with alerts

---

## 📦 Modules to Implement

### 1. Warehouse Management
**Purpose:** Manage storage locations and zones

**Components:**
- `Warehouse.cs` - Warehouse/godown entity
- `StorageZone.cs` - Zones within warehouse (Rice section, Paddy section, By-products)
- `WarehouseRepository` + `WarehouseService`
- `WarehousesController`
- 5 Views (Index, Create, Edit, Details, Delete)

**Features:**
- Auto-code: WRHS0001, WRHS0002...
- Capacity tracking (Total, Used, Available)
- Zone-based organization
- Temperature/humidity monitoring fields
- Status tracking (Active, Maintenance, Full)

**Estimated:** 6 tasks

---

### 2. Inventory Ledger
**Purpose:** Real-time stock tracking for all products

**Components:**
- `InventoryLedger.cs` - Stock balance entity
- `InventoryLedgerRepository` + `InventoryLedgerService`
- `InventoryController`
- Views for stock viewing and searching

**Features:**
- Current stock by product and warehouse
- Minimum/Maximum level alerts
- Reorder point tracking
- Stock value calculation
- Multi-warehouse support

**Estimated:** 5 tasks

---

### 3. Stock Movements
**Purpose:** Track all stock in/out transactions

**Components:**
- `StockMovement.cs` - Transaction entity
- `StockMovementRepository` + `StockMovementService`
- `StockMovementsController`
- 5 Views for movement tracking

**Features:**
- Movement types: IN (Procurement, Production, Return), OUT (Sales, Production, Transfer)
- Reference to source transaction (Purchase, Sale, Production)
- Automatic ledger update
- Movement history tracking
- Batch/Lot tracking

**Estimated:** 7 tasks

---

### 4. Stock Adjustments
**Purpose:** Handle inventory corrections and reconciliation

**Components:**
- `StockAdjustment.cs` - Adjustment entity
- `StockAdjustmentRepository` + `StockAdjustmentService`
- `StockAdjustmentsController`
- Views for adjustments

**Features:**
- Adjustment types: Increase, Decrease, Transfer
- Reason tracking (Damage, Theft, Spoilage, Counting Error)
- Approval workflow (basic)
- Automatic ledger correction
- Audit trail

**Estimated:** 6 tasks

---

### 5. Inventory Dashboard
**Purpose:** Real-time inventory overview and alerts

**Components:**
- Enhanced `DashboardController`
- Dashboard views with charts
- Real-time stock status
- Alert system

**Features:**
- Stock summary by category (Rice, Paddy, By-products)
- Low stock alerts (below minimum)
- Overstock alerts (above maximum)
- Stock value summary
- Recent movements
- Quick actions (Adjust stock, Record movement)

**Estimated:** 5 tasks

---

## 🗄️ Database Design

### New Tables to Create

#### 1. Warehouses
```sql
- Id (PK)
- WarehouseCode (unique)
- WarehouseName
- Location/Address
- TotalCapacity
- UsedCapacity
- AvailableCapacity
- ContactPerson
- Mobile
- Status
- Audit fields
```

#### 2. StorageZones
```sql
- Id (PK)
- WarehouseId (FK)
- ZoneCode (unique)
- ZoneName
- ZoneType (Rice, Paddy, By-Products, Other)
- Capacity
- Temperature
- Humidity
- Status
```

#### 3. InventoryLedger
```sql
- Id (PK)
- ProductId (FK)
- WarehouseId (FK)
- ZoneId (FK nullable)
- CurrentStock
- MinimumLevel
- MaximumLevel
- ReorderLevel
- UnitCost
- TotalValue
- LastMovementDate
- LastUpdated
```

#### 4. StockMovements
```sql
- Id (PK)
- MovementCode (unique)
- ProductId (FK)
- WarehouseId (FK)
- ZoneId (FK nullable)
- MovementType (IN/OUT)
- MovementCategory (Procurement, Sales, Production, Transfer, Adjustment)
- Quantity
- UnitCost
- TotalCost
- ReferenceType (PO, SO, Production, etc.)
- ReferenceId
- MovementDate
- Remarks
- Audit fields
```

#### 5. StockAdjustments
```sql
- Id (PK)
- AdjustmentCode (unique)
- ProductId (FK)
- WarehouseId (FK)
- AdjustmentType (Increase, Decrease, Transfer)
- Quantity
- Reason (Damage, Theft, Spoilage, Counting Error, Other)
- BeforeQty
- AfterQty
- ApprovedBy
- ApprovalDate
- Remarks
- Audit fields
```

---

## 📊 Sprint 2 Task Breakdown

### Week 3 (Tasks 1-15)
1. ✅ Plan Sprint 2 structure
2. Create Warehouse model
3. Create StorageZone model
4. Create WarehouseRepository + Service
5. Create WarehousesController
6. Create Warehouse views (5 views)
7. Create InventoryLedger model
8. Create InventoryLedgerRepository + Service
9. Create InventoryController
10. Create Inventory views
11. Create StockMovement model
12. Create StockMovementRepository + Service
13. Create StockMovementsController
14. Create StockMovement views (5 views)
15. Week 3 testing

### Week 4 (Tasks 16-29)
16. Create StockAdjustment model
17. Create StockAdjustmentRepository + Service
18. Create StockAdjustmentsController
19. Create StockAdjustment views (5 views)
20. Enhance DashboardController with inventory
21. Create Inventory dashboard view
22. Add stock alerts functionality
23. Create stock summary cards
24. Add recent movements widget
25. Create SQL migration script
26. Update navigation menu
27. Integration testing
28. Performance optimization
29. Sprint 2 completion & documentation

**Total Tasks:** 29 tasks

---

## 🔗 Integration Points

### With Existing Modules

**Products Module:**
- Link inventory to product master
- Use product categories for zone assignment
- Stock levels update product availability

**Procurement Module (Future):**
- Stock IN movements from paddy/rice procurement
- Automatic ledger update on procurement

**Sales Module (Future):**
- Stock OUT movements from sales
- Automatic ledger update on sales
- Stock availability check before sale

**Production Module (Future):**
- Stock IN for finished goods (rice)
- Stock OUT for raw materials (paddy)
- Automatic ledger updates

---

## 🎯 Success Criteria

### Functional
- ✅ Create and manage warehouses with zones
- ✅ Track real-time stock for all products
- ✅ Record all stock movements (IN/OUT)
- ✅ Handle stock adjustments with reasons
- ✅ Display inventory dashboard with alerts
- ✅ Stock value calculation
- ✅ Multi-warehouse support

### Technical
- ✅ 0 build errors, 0 warnings
- ✅ Proper error handling
- ✅ Database transactions for stock updates
- ✅ Audit trail for all changes
- ✅ Search and filter functionality
- ✅ Responsive UI

### Performance
- ✅ Dashboard loads in < 2 seconds
- ✅ Stock movement recording in < 1 second
- ✅ Inventory queries optimized with indexes

---

## 📈 Expected Deliverables

### Code Files (Estimated)
- **Models:** 5 files (Warehouse, StorageZone, InventoryLedger, StockMovement, StockAdjustment)
- **Repositories:** 10 files (5 interfaces + 5 implementations)
- **Services:** 10 files (5 interfaces + 5 implementations)
- **Controllers:** 5 files
- **Views:** 25-30 files
- **SQL Scripts:** 1 migration script

**Total:** ~55-60 files

### Documentation
- Sprint 2 completion report
- Database schema documentation
- API/Service documentation
- User guide for inventory management

---

## 🚀 Implementation Approach

### Phase 1: Foundation (Week 3 Days 1-3)
1. Database design and models
2. Warehouse management (complete)
3. Inventory ledger (complete)

### Phase 2: Transactions (Week 3 Days 4-5 + Week 4 Days 1-2)
4. Stock movements (complete)
5. Stock adjustments (complete)

### Phase 3: UI & Dashboard (Week 4 Days 3-4)
6. Inventory dashboard
7. Alerts and notifications
8. Reporting widgets

### Phase 4: Testing & Polish (Week 4 Day 5)
9. Integration testing
10. Performance tuning
11. Documentation
12. Sprint review

---

## ⚡ Quick Start Commands

### After Planning:
```bash
# Build to ensure Sprint 1 is stable
dotnet build

# Start Sprint 2 implementation
# Create Warehouse model first
```

### Testing:
```bash
# Run application
dotnet run

# Test inventory features
# Navigate to Inventory menu
```

---

## 📝 Notes

### Assumptions
- Sprint 1 (Master Data) is complete and tested
- Database is running and accessible
- All master data tables are created

### Dependencies
- Product Master (for inventory items) ✅
- Warehouse Master (to be built)
- No external inventory system integration in this sprint

### Future Enhancements (Sprint 3+)
- Barcode/QR code scanning
- Mobile app for stock taking
- Advanced reporting with charts
- Automated reorder suggestions
- Integration with weighbridge
- Batch/Lot expiry tracking
- FIFO/LIFO cost methods

---

## 🎯 Sprint 2 Success Metrics

| Metric | Target | Status |
|--------|--------|--------|
| Tasks Complete | 29/29 | 🟡 Pending |
| Files Created | 55-60 | 🟡 Pending |
| Build Errors | 0 | 🟡 Pending |
| Database Tables | 5 | 🟡 Pending |
| Test Coverage | Basic CRUD | 🟡 Pending |

---

**Sprint 2 Start Date:** 2025-10-06
**Sprint 2 Target End:** 2025-10-20
**Status:** 🟡 Ready to Begin

**Next Action:** Create Warehouse model and begin implementation

---

*This plan is aligned with the RMMS Implementation Roadmap and will deliver a complete inventory management foundation for the rice mill operations.*
