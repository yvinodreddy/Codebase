using Microsoft.EntityFrameworkCore;
using RMMS.Models;
using RMMS.Models.Masters;
using RMMS.Models.Inventory;
using RMMS.Models.Production;
using RMMS.Models.Sales;
using RMMS.Models.Authentication;
using RMMS.Models.Mobile;
using RMMS.Models.API;
using RMMS.Models.Monitoring;

namespace RMMS.DataAccess.Context
{
    public class ApplicationDbContext : DbContext
    {
        public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options)
            : base(options)
        {
        }

        // Existing tables
        public DbSet<PaddyProcurement> PaddyProcurements { get; set; }
        public DbSet<RiceSales> RiceSales { get; set; }
        public DbSet<ByProductSales> ByProductSales { get; set; }
        public DbSet<BankTransactions> BankTransactions { get; set; }
        public DbSet<CashBook> CashBooks { get; set; }
        public DbSet<FixedAsset> FixedAssets { get; set; }
        public DbSet<LoanAdvance> LoansAdvances { get; set; }
        public DbSet<Voucher> Vouchers { get; set; }
        public DbSet<PayableOverdue> PayablesOverdue { get; set; }
        public DbSet<ReceivableOverdue> ReceivablesOverdue { get; set; }
        public DbSet<RiceProcurementExternal> RiceProcurementExternal { get; set; }
        public DbSet<ExternalRiceSale> ExternalRiceSales { get; set; }

        // New Master Data tables
        public DbSet<Customer> Customers { get; set; }
        public DbSet<CustomerContact> CustomerContacts { get; set; }
        public DbSet<CustomerAddress> CustomerAddresses { get; set; }
        public DbSet<Vendor> Vendors { get; set; }
        public DbSet<VendorContact> VendorContacts { get; set; }
        public DbSet<VendorAddress> VendorAddresses { get; set; }
        public DbSet<Product> Products { get; set; }
        public DbSet<Employee> Employees { get; set; }

        // Inventory Management tables
        public DbSet<Warehouse> Warehouses { get; set; }
        public DbSet<StorageZone> StorageZones { get; set; }
        public DbSet<InventoryLedger> InventoryLedger { get; set; }
        public DbSet<InventoryLedger> InventoryLedgers { get; set; }  // Alias for compatibility
        public DbSet<StockMovement> StockMovements { get; set; }
        public DbSet<StockAdjustment> StockAdjustments { get; set; }

        // Production Management tables
        public DbSet<Machine> Machines { get; set; }
        public DbSet<ProductionOrder> ProductionOrders { get; set; }
        public DbSet<ProductionBatch> ProductionBatches { get; set; }
        public DbSet<BatchInput> BatchInputs { get; set; }
        public DbSet<BatchOutput> BatchOutputs { get; set; }
        public DbSet<YieldRecord> YieldRecords { get; set; }

        // Sales Management tables
        public DbSet<Inquiry> Inquiries { get; set; }
        public DbSet<Quotation> Quotations { get; set; }
        public DbSet<QuotationItem> QuotationItems { get; set; }
        public DbSet<SalesOrder> SalesOrders { get; set; }
        public DbSet<SalesOrderItem> SalesOrderItems { get; set; }

        // Authentication tables (Phase 4)
        public DbSet<RefreshToken> RefreshTokens { get; set; }

        // Mobile Architecture tables (Phase 4.4.2)
        public DbSet<MobileDevice> MobileDevices { get; set; }
        public DbSet<PushNotification> PushNotifications { get; set; }
        public DbSet<SyncLog> SyncLogs { get; set; }
        public DbSet<MobileAppConfig> MobileAppConfigs { get; set; }
        public DbSet<MobileAnalyticsEvent> MobileAnalyticsEvents { get; set; }

        // Phase 4 API Management tables
        public DbSet<ApiKey> ApiKeys { get; set; }
        public DbSet<ApiAnalytic> ApiAnalytics { get; set; }
        public DbSet<Webhook> Webhooks { get; set; }
        public DbSet<IntegrationStatus> Integrations { get; set; }

        // Phase 4 Monitoring tables
        public DbSet<RealtimeMetric> RealtimeMetrics { get; set; }

        // Phase 2: Professional UI Features - Calendar, File Manager, Tasks
        public DbSet<ScheduleEvent> ScheduleEvents { get; set; }
        public DbSet<DocumentFile> DocumentFiles { get; set; }
        public DbSet<TaskItem> TaskItems { get; set; }

        // Phase 2: Advanced Sales Features (Tasks 3-10)
        // TODO: Uncomment when models are created
        // public DbSet<ApprovalHistory> ApprovalHistories { get; set; }
        // public DbSet<Invoice> Invoices { get; set; }
        // public DbSet<CommissionStructure> CommissionStructures { get; set; }
        // public DbSet<SalesTarget> SalesTargets { get; set; }
        // public DbSet<Currency> Currencies { get; set; }
        // public DbSet<ExchangeRate> ExchangeRates { get; set; }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            base.OnModelCreating(modelBuilder);

            // Map to existing tables
            modelBuilder.Entity<PaddyProcurement>().ToTable("PaddyProcurement");
            modelBuilder.Entity<RiceSales>().ToTable("RiceSales");
            modelBuilder.Entity<ByProductSales>().ToTable("ByProductSales");
            modelBuilder.Entity<BankTransactions>().ToTable("BankTransactions");
            modelBuilder.Entity<CashBook>().ToTable("CashBook");
            modelBuilder.Entity<FixedAsset>().ToTable("FixedAssets");
            modelBuilder.Entity<LoanAdvance>().ToTable("LoansAdvances");
            modelBuilder.Entity<Voucher>().ToTable("Vouchers");
            modelBuilder.Entity<PayableOverdue>().ToTable("PayablesOverdue");
            modelBuilder.Entity<ReceivableOverdue>().ToTable("ReceivablesOverdue");
            modelBuilder.Entity<RiceProcurementExternal>().ToTable("RiceProcurementExternal");
            modelBuilder.Entity<ExternalRiceSale>().ToTable("ExternalRiceSales");

            // Configure Customer relationships
            modelBuilder.Entity<Customer>()
                .HasMany(c => c.Contacts)
                .WithOne(cc => cc.Customer)
                .HasForeignKey(cc => cc.CustomerId)
                .OnDelete(DeleteBehavior.Cascade);

            modelBuilder.Entity<Customer>()
                .HasMany(c => c.Addresses)
                .WithOne(ca => ca.Customer)
                .HasForeignKey(ca => ca.CustomerId)
                .OnDelete(DeleteBehavior.Cascade);

            // Configure Vendor relationships
            modelBuilder.Entity<Vendor>()
                .HasMany(v => v.Contacts)
                .WithOne(vc => vc.Vendor)
                .HasForeignKey(vc => vc.VendorId)
                .OnDelete(DeleteBehavior.Cascade);

            modelBuilder.Entity<Vendor>()
                .HasMany(v => v.Addresses)
                .WithOne(va => va.Vendor)
                .HasForeignKey(va => va.VendorId)
                .OnDelete(DeleteBehavior.Cascade);

            // Configure Warehouse relationships
            modelBuilder.Entity<Warehouse>()
                .HasMany(w => w.Zones)
                .WithOne(z => z.Warehouse)
                .HasForeignKey(z => z.WarehouseId)
                .OnDelete(DeleteBehavior.Cascade);

            // Configure unique constraints
            modelBuilder.Entity<Warehouse>()
                .HasIndex(w => w.WarehouseCode)
                .IsUnique();

            modelBuilder.Entity<StorageZone>()
                .HasIndex(z => z.ZoneCode)
                .IsUnique();

            // Configure InventoryLedger relationships
            modelBuilder.Entity<InventoryLedger>()
                .HasOne(i => i.Product)
                .WithMany()
                .HasForeignKey(i => i.ProductId)
                .OnDelete(DeleteBehavior.Restrict);

            modelBuilder.Entity<InventoryLedger>()
                .HasOne(i => i.Warehouse)
                .WithMany()
                .HasForeignKey(i => i.WarehouseId)
                .OnDelete(DeleteBehavior.Restrict);

            modelBuilder.Entity<InventoryLedger>()
                .HasOne(i => i.Zone)
                .WithMany()
                .HasForeignKey(i => i.ZoneId)
                .OnDelete(DeleteBehavior.SetNull);

            // Create unique index for Product + Warehouse + Zone combination
            modelBuilder.Entity<InventoryLedger>()
                .HasIndex(i => new { i.ProductId, i.WarehouseId, i.ZoneId })
                .IsUnique();

            // Configure StockMovement relationships
            modelBuilder.Entity<StockMovement>()
                .HasOne(m => m.Product)
                .WithMany()
                .HasForeignKey(m => m.ProductId)
                .OnDelete(DeleteBehavior.Restrict);

            modelBuilder.Entity<StockMovement>()
                .HasOne(m => m.Warehouse)
                .WithMany()
                .HasForeignKey(m => m.WarehouseId)
                .OnDelete(DeleteBehavior.Restrict);

            modelBuilder.Entity<StockMovement>()
                .HasOne(m => m.Zone)
                .WithMany()
                .HasForeignKey(m => m.ZoneId)
                .OnDelete(DeleteBehavior.SetNull);

            // Create unique index on MovementCode
            modelBuilder.Entity<StockMovement>()
                .HasIndex(m => m.MovementCode)
                .IsUnique();

            // Configure StockAdjustment relationships
            modelBuilder.Entity<StockAdjustment>()
                .HasOne(a => a.Product)
                .WithMany()
                .HasForeignKey(a => a.ProductId)
                .OnDelete(DeleteBehavior.Restrict);

            modelBuilder.Entity<StockAdjustment>()
                .HasOne(a => a.Warehouse)
                .WithMany()
                .HasForeignKey(a => a.WarehouseId)
                .OnDelete(DeleteBehavior.Restrict);

            modelBuilder.Entity<StockAdjustment>()
                .HasOne(a => a.Zone)
                .WithMany()
                .HasForeignKey(a => a.ZoneId)
                .OnDelete(DeleteBehavior.SetNull);

            // Create unique index on AdjustmentCode
            modelBuilder.Entity<StockAdjustment>()
                .HasIndex(a => a.AdjustmentCode)
                .IsUnique();

            // Configure Machine relationships
            modelBuilder.Entity<Machine>()
                .HasIndex(m => m.MachineCode)
                .IsUnique();

            // Configure ProductionOrder relationships
            modelBuilder.Entity<ProductionOrder>()
                .HasOne(po => po.PaddyProduct)
                .WithMany()
                .HasForeignKey(po => po.PaddyProductId)
                .OnDelete(DeleteBehavior.Restrict);

            modelBuilder.Entity<ProductionOrder>()
                .HasOne(po => po.TargetRiceProduct)
                .WithMany()
                .HasForeignKey(po => po.TargetRiceProductId)
                .OnDelete(DeleteBehavior.SetNull);

            modelBuilder.Entity<ProductionOrder>()
                .HasOne(po => po.AssignedMachine)
                .WithMany()
                .HasForeignKey(po => po.AssignedMachineId)
                .OnDelete(DeleteBehavior.SetNull);

            modelBuilder.Entity<ProductionOrder>()
                .HasOne(po => po.AssignedSupervisor)
                .WithMany()
                .HasForeignKey(po => po.AssignedSupervisorId)
                .OnDelete(DeleteBehavior.SetNull);

            modelBuilder.Entity<ProductionOrder>()
                .HasIndex(po => po.OrderNumber)
                .IsUnique();

            // Configure ProductionBatch relationships
            modelBuilder.Entity<ProductionBatch>()
                .HasOne(pb => pb.ProductionOrder)
                .WithMany()
                .HasForeignKey(pb => pb.ProductionOrderId)
                .OnDelete(DeleteBehavior.SetNull);

            modelBuilder.Entity<ProductionBatch>()
                .HasOne(pb => pb.Operator)
                .WithMany()
                .HasForeignKey(pb => pb.OperatorId)
                .OnDelete(DeleteBehavior.SetNull);

            modelBuilder.Entity<ProductionBatch>()
                .HasOne(pb => pb.Supervisor)
                .WithMany()
                .HasForeignKey(pb => pb.SupervisorId)
                .OnDelete(DeleteBehavior.SetNull);

            modelBuilder.Entity<ProductionBatch>()
                .HasMany(pb => pb.Inputs)
                .WithOne(bi => bi.Batch)
                .HasForeignKey(bi => bi.BatchId)
                .OnDelete(DeleteBehavior.Cascade);

            modelBuilder.Entity<ProductionBatch>()
                .HasMany(pb => pb.Outputs)
                .WithOne(bo => bo.Batch)
                .HasForeignKey(bo => bo.BatchId)
                .OnDelete(DeleteBehavior.Cascade);

            modelBuilder.Entity<ProductionBatch>()
                .HasOne(pb => pb.YieldRecord)
                .WithOne(yr => yr.Batch)
                .HasForeignKey<YieldRecord>(yr => yr.BatchId)
                .OnDelete(DeleteBehavior.Cascade);

            modelBuilder.Entity<ProductionBatch>()
                .HasIndex(pb => pb.BatchNumber)
                .IsUnique();

            // Configure BatchInput relationships
            modelBuilder.Entity<BatchInput>()
                .HasOne(bi => bi.Product)
                .WithMany()
                .HasForeignKey(bi => bi.ProductId)
                .OnDelete(DeleteBehavior.Restrict);

            modelBuilder.Entity<BatchInput>()
                .HasOne(bi => bi.Warehouse)
                .WithMany()
                .HasForeignKey(bi => bi.WarehouseId)
                .OnDelete(DeleteBehavior.Restrict);

            modelBuilder.Entity<BatchInput>()
                .HasOne(bi => bi.Zone)
                .WithMany()
                .HasForeignKey(bi => bi.ZoneId)
                .OnDelete(DeleteBehavior.SetNull);

            // Configure BatchOutput relationships
            modelBuilder.Entity<BatchOutput>()
                .HasOne(bo => bo.Product)
                .WithMany()
                .HasForeignKey(bo => bo.ProductId)
                .OnDelete(DeleteBehavior.Restrict);

            modelBuilder.Entity<BatchOutput>()
                .HasOne(bo => bo.Warehouse)
                .WithMany()
                .HasForeignKey(bo => bo.WarehouseId)
                .OnDelete(DeleteBehavior.Restrict);

            modelBuilder.Entity<BatchOutput>()
                .HasOne(bo => bo.Zone)
                .WithMany()
                .HasForeignKey(bo => bo.ZoneId)
                .OnDelete(DeleteBehavior.SetNull);

            // ============================================================
            // MOBILE ARCHITECTURE CONFIGURATIONS (Phase 4.4.2)
            // ============================================================

            // Configure MobileDevice relationships
            modelBuilder.Entity<MobileDevice>()
                .HasIndex(d => d.DeviceId)
                .IsUnique();

            modelBuilder.Entity<MobileDevice>()
                .HasIndex(d => d.UserId);

            modelBuilder.Entity<MobileDevice>()
                .HasIndex(d => new { d.UserId, d.Platform });

            // Configure PushNotification relationships
            modelBuilder.Entity<PushNotification>()
                .HasOne(n => n.Device)
                .WithMany()
                .HasForeignKey(n => n.DeviceId)
                .OnDelete(DeleteBehavior.SetNull);

            modelBuilder.Entity<PushNotification>()
                .HasIndex(n => n.UserId);

            modelBuilder.Entity<PushNotification>()
                .HasIndex(n => n.Status);

            modelBuilder.Entity<PushNotification>()
                .HasIndex(n => n.ScheduledFor);

            // Configure SyncLog relationships
            modelBuilder.Entity<SyncLog>()
                .HasOne(s => s.Device)
                .WithMany()
                .HasForeignKey(s => s.DeviceId)
                .OnDelete(DeleteBehavior.Cascade);

            modelBuilder.Entity<SyncLog>()
                .HasIndex(s => s.DeviceId);

            modelBuilder.Entity<SyncLog>()
                .HasIndex(s => s.UserId);

            modelBuilder.Entity<SyncLog>()
                .HasIndex(s => new { s.EntityType, s.ServerTimestamp });

            // Configure MobileAppConfig
            modelBuilder.Entity<MobileAppConfig>()
                .HasIndex(c => new { c.Platform, c.IsActive });

            // Configure MobileAnalyticsEvent relationships
            modelBuilder.Entity<MobileAnalyticsEvent>()
                .HasOne(e => e.Device)
                .WithMany()
                .HasForeignKey(e => e.DeviceId)
                .OnDelete(DeleteBehavior.SetNull);

            modelBuilder.Entity<MobileAnalyticsEvent>()
                .HasIndex(e => e.UserId);

            modelBuilder.Entity<MobileAnalyticsEvent>()
                .HasIndex(e => e.DeviceId);

            modelBuilder.Entity<MobileAnalyticsEvent>()
                .HasIndex(e => e.Category);

            modelBuilder.Entity<MobileAnalyticsEvent>()
                .HasIndex(e => new { e.Category, e.Action });

            modelBuilder.Entity<MobileAnalyticsEvent>()
                .HasIndex(e => e.ServerTimestamp);

            // ============================================================
            // PHASE 2: PROFESSIONAL UI FEATURES CONFIGURATIONS
            // ============================================================

            // Configure ScheduleEvent
            modelBuilder.Entity<ScheduleEvent>()
                .HasIndex(e => e.EventType);

            modelBuilder.Entity<ScheduleEvent>()
                .HasIndex(e => e.StartDateTime);

            modelBuilder.Entity<ScheduleEvent>()
                .HasIndex(e => new { e.EventType, e.StartDateTime });

            modelBuilder.Entity<ScheduleEvent>()
                .HasIndex(e => e.Status);

            // Configure DocumentFile
            modelBuilder.Entity<DocumentFile>()
                .HasIndex(f => f.Category);

            modelBuilder.Entity<DocumentFile>()
                .HasIndex(f => f.UploadedDate);

            modelBuilder.Entity<DocumentFile>()
                .HasIndex(f => new { f.RelatedEntityType, f.RelatedEntityId });

            modelBuilder.Entity<DocumentFile>()
                .HasIndex(f => f.IsActive);

            // Self-referencing relationship for file versioning
            modelBuilder.Entity<DocumentFile>()
                .HasOne(f => f.ParentFile)
                .WithMany()
                .HasForeignKey(f => f.ParentFileId)
                .OnDelete(DeleteBehavior.Restrict);

            // Configure TaskItem
            modelBuilder.Entity<TaskItem>()
                .HasIndex(t => t.Status);

            modelBuilder.Entity<TaskItem>()
                .HasIndex(t => t.Priority);

            modelBuilder.Entity<TaskItem>()
                .HasIndex(t => t.DueDate);

            modelBuilder.Entity<TaskItem>()
                .HasIndex(t => t.AssignedTo);

            modelBuilder.Entity<TaskItem>()
                .HasIndex(t => new { t.Status, t.Priority });

            modelBuilder.Entity<TaskItem>()
                .HasIndex(t => new { t.AssignedTo, t.Status });

            modelBuilder.Entity<TaskItem>()
                .HasIndex(t => t.Category);

            modelBuilder.Entity<TaskItem>()
                .HasIndex(t => t.IsActive);
        }
    }
}
