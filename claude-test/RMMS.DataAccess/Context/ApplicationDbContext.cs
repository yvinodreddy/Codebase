using Microsoft.EntityFrameworkCore;
using RMMS.Models;

namespace RMMS.DataAccess.Context
{
    public class ApplicationDbContext : DbContext
    {
        public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options)
            : base(options)
        {
        }

        // Existing tables from current system
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

        // New Master Data tables (will be created in Phase 1)
        // These will be uncommented as we create the models
        // public DbSet<Customer> Customers { get; set; }
        // public DbSet<CustomerContact> CustomerContacts { get; set; }
        // public DbSet<CustomerAddress> CustomerAddresses { get; set; }
        // public DbSet<Vendor> Vendors { get; set; }
        // public DbSet<VendorContact> VendorContacts { get; set; }
        // public DbSet<VendorAddress> VendorAddresses { get; set; }
        // public DbSet<Product> Products { get; set; }
        // public DbSet<ProductCategory> ProductCategories { get; set; }
        // public DbSet<Employee> Employees { get; set; }
        // public DbSet<Department> Departments { get; set; }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            base.OnModelCreating(modelBuilder);

            // Configure existing entities to map to existing tables
            modelBuilder.Entity<PaddyProcurement>()
                .ToTable("PaddyProcurement")
                .HasKey(p => p.Id);

            modelBuilder.Entity<RiceSales>()
                .ToTable("RiceSales")
                .HasKey(r => r.Id);

            modelBuilder.Entity<ByProductSales>()
                .ToTable("ByProductSales")
                .HasKey(b => b.Id);

            modelBuilder.Entity<BankTransactions>()
                .ToTable("BankTransactions")
                .HasKey(b => b.Id);

            modelBuilder.Entity<CashBook>()
                .ToTable("CashBook")
                .HasKey(c => c.Id);

            modelBuilder.Entity<FixedAsset>()
                .ToTable("FixedAssets")
                .HasKey(f => f.Id);

            modelBuilder.Entity<LoanAdvance>()
                .ToTable("LoansAdvances")
                .HasKey(l => l.Id);

            modelBuilder.Entity<Voucher>()
                .ToTable("Vouchers")
                .HasKey(v => v.Id);

            modelBuilder.Entity<PayableOverdue>()
                .ToTable("PayablesOverdue")
                .HasKey(p => p.Id);

            modelBuilder.Entity<ReceivableOverdue>()
                .ToTable("ReceivablesOverdue")
                .HasKey(r => r.Id);

            modelBuilder.Entity<RiceProcurementExternal>()
                .ToTable("RiceProcurementExternal")
                .HasKey(r => r.Id);

            modelBuilder.Entity<ExternalRiceSale>()
                .ToTable("ExternalRiceSales")
                .HasKey(e => e.Id);

            // Additional configurations for new tables will be added here as we create models
            // This ensures we don't break existing functionality while adding new features
        }
    }
}
