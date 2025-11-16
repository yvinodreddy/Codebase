using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using RMMS.DataAccess.Context;
using RMMS.Models.Reporting;

namespace RMMS.Services.Services.Reporting
{
    /// <summary>
    /// Drilldown report service with hierarchical navigation
    /// </summary>
    public class DrilldownReportService : IDrilldownReportService
    {
        private readonly ApplicationDbContext _context;
        private readonly ILogger<DrilldownReportService> _logger;

        // Define hierarchies
        private readonly List<string> _salesHierarchy = new() { "Year", "Quarter", "Month", "Customer", "Product" };
        private readonly List<string> _inventoryHierarchy = new() { "Warehouse", "Category", "Product" };
        private readonly List<string> _productionHierarchy = new() { "Year", "Month", "Batch", "Status" };

        public DrilldownReportService(
            ApplicationDbContext context,
            ILogger<DrilldownReportService> logger)
        {
            _context = context;
            _logger = logger;
        }

        public async Task<DrilldownResult> GetSalesDrilldownAsync(Dictionary<string, string> filters, int currentLevel)
        {
            _logger.LogInformation($"Sales drilldown: Level {currentLevel}, Filters: {filters.Count}");

            var result = new DrilldownResult
            {
                ReportName = "Sales Drilldown Report",
                NavigationPath = BuildNavigationPath(_salesHierarchy, filters, currentLevel)
            };

            var salesQuery = _context.RiceSales.AsQueryable();

            // Apply filters
            if (filters.ContainsKey("Year"))
            {
                var year = int.Parse(filters["Year"]);
                salesQuery = salesQuery.Where(s => s.SaleDate.Year == year);
            }

            if (filters.ContainsKey("Quarter"))
            {
                var quarter = int.Parse(filters["Quarter"]);
                var startMonth = (quarter - 1) * 3 + 1;
                var endMonth = startMonth + 2;
                salesQuery = salesQuery.Where(s => s.SaleDate.Month >= startMonth && s.SaleDate.Month <= endMonth);
            }

            if (filters.ContainsKey("Month"))
            {
                var month = int.Parse(filters["Month"]);
                salesQuery = salesQuery.Where(s => s.SaleDate.Month == month);
            }

            if (filters.ContainsKey("Customer"))
            {
                var customer = filters["Customer"];
                salesQuery = salesQuery.Where(s => s.BuyerName == customer);
            }

            // Get data based on current level
            switch (currentLevel)
            {
                case 0: // Year level
                    result.DataRows = await GetSalesByYearAsync(salesQuery);
                    result.NextLevelHint = "Click on a year to see quarterly breakdown";
                    break;

                case 1: // Quarter level
                    result.DataRows = await GetSalesByQuarterAsync(salesQuery, filters);
                    result.NextLevelHint = "Click on a quarter to see monthly breakdown";
                    break;

                case 2: // Month level
                    result.DataRows = await GetSalesByMonthAsync(salesQuery, filters);
                    result.NextLevelHint = "Click on a month to see customer breakdown";
                    break;

                case 3: // Customer level
                    result.DataRows = await GetSalesByCustomerAsync(salesQuery);
                    result.NextLevelHint = "Click on a customer to see product breakdown";
                    break;

                case 4: // Product level (detail)
                    result.DataRows = await GetSalesByProductAsync(salesQuery, filters);
                    result.NextLevelHint = "This is the detail level";
                    break;
            }

            // Calculate summary
            result.Summary = new Dictionary<string, decimal>
            {
                ["TotalSales"] = result.DataRows.Sum(r => (decimal)(r.Metrics.ContainsKey("TotalSales") ? r.Metrics["TotalSales"] : 0m)),
                ["TotalQuantity"] = result.DataRows.Sum(r => (decimal)(r.Metrics.ContainsKey("Quantity") ? r.Metrics["Quantity"] : 0m)),
                ["RecordCount"] = result.DataRows.Count
            };

            return result;
        }

        public async Task<DrilldownResult> GetInventoryDrilldownAsync(Dictionary<string, string> filters, int currentLevel)
        {
            _logger.LogInformation($"Inventory drilldown: Level {currentLevel}");

            var result = new DrilldownResult
            {
                ReportName = "Inventory Drilldown Report",
                NavigationPath = BuildNavigationPath(_inventoryHierarchy, filters, currentLevel)
            };

            switch (currentLevel)
            {
                case 0: // Warehouse level
                    result.DataRows = await GetInventoryByWarehouseAsync();
                    result.NextLevelHint = "Click on a warehouse to see category breakdown";
                    break;

                case 1: // Category level
                    result.DataRows = await GetInventoryByCategoryAsync(filters);
                    result.NextLevelHint = "Click on a category to see products";
                    break;

                case 2: // Product level (detail)
                    result.DataRows = await GetInventoryByProductAsync(filters);
                    result.NextLevelHint = "This is the detail level";
                    break;
            }

            result.Summary = new Dictionary<string, decimal>
            {
                ["TotalItems"] = result.DataRows.Count,
                ["TotalValue"] = result.DataRows.Sum(r => (decimal)(r.Metrics.ContainsKey("Value") ? r.Metrics["Value"] : 0m))
            };

            return result;
        }

        public async Task<DrilldownResult> GetProductionDrilldownAsync(Dictionary<string, string> filters, int currentLevel)
        {
            _logger.LogInformation($"Production drilldown: Level {currentLevel}");

            var result = new DrilldownResult
            {
                ReportName = "Production Drilldown Report",
                NavigationPath = BuildNavigationPath(_productionHierarchy, filters, currentLevel)
            };

            var batchQuery = _context.ProductionBatches.AsQueryable();

            // Apply filters
            if (filters.ContainsKey("Year"))
            {
                var year = int.Parse(filters["Year"]);
                batchQuery = batchQuery.Where(b => b.BatchDate.Year == year);
            }

            if (filters.ContainsKey("Month"))
            {
                var month = int.Parse(filters["Month"]);
                batchQuery = batchQuery.Where(b => b.BatchDate.Month == month);
            }

            if (filters.ContainsKey("Status"))
            {
                var status = filters["Status"];
                batchQuery = batchQuery.Where(b => b.Status == status);
            }

            switch (currentLevel)
            {
                case 0: // Year level
                    result.DataRows = await GetProductionByYearAsync(batchQuery);
                    result.NextLevelHint = "Click on a year to see monthly breakdown";
                    break;

                case 1: // Month level
                    result.DataRows = await GetProductionByMonthAsync(batchQuery, filters);
                    result.NextLevelHint = "Click on a month to see batches";
                    break;

                case 2: // Batch level
                    result.DataRows = await GetProductionByBatchAsync(batchQuery);
                    result.NextLevelHint = "Click on a batch to see status details";
                    break;

                case 3: // Status level (detail)
                    result.DataRows = await GetProductionByStatusAsync(batchQuery);
                    result.NextLevelHint = "This is the detail level";
                    break;
            }

            result.Summary = new Dictionary<string, decimal>
            {
                ["TotalBatches"] = result.DataRows.Count
            };

            return result;
        }

        public async Task<DrilldownResult> NavigateUpAsync(string reportType, Dictionary<string, string> filters, int currentLevel)
        {
            if (currentLevel <= 0)
                throw new InvalidOperationException("Already at top level");

            // Remove the last filter
            var hierarchy = reportType.ToLower() switch
            {
                "sales" => _salesHierarchy,
                "inventory" => _inventoryHierarchy,
                "production" => _productionHierarchy,
                _ => _salesHierarchy
            };

            if (currentLevel > 0 && currentLevel <= hierarchy.Count)
            {
                var keyToRemove = hierarchy[currentLevel - 1];
                if (filters.ContainsKey(keyToRemove))
                {
                    filters.Remove(keyToRemove);
                }
            }

            return reportType.ToLower() switch
            {
                "sales" => await GetSalesDrilldownAsync(filters, currentLevel - 1),
                "inventory" => await GetInventoryDrilldownAsync(filters, currentLevel - 1),
                "production" => await GetProductionDrilldownAsync(filters, currentLevel - 1),
                _ => await GetSalesDrilldownAsync(filters, currentLevel - 1)
            };
        }

        public async Task<List<DrilldownReportDefinition>> GetAvailableReportsAsync()
        {
            return await Task.FromResult(new List<DrilldownReportDefinition>
            {
                new() { ReportName = "Sales Drilldown", Category = "Sales", Hierarchy = _salesHierarchy },
                new() { ReportName = "Inventory Drilldown", Category = "Inventory", Hierarchy = _inventoryHierarchy },
                new() { ReportName = "Production Drilldown", Category = "Production", Hierarchy = _productionHierarchy }
            });
        }

        #region Helper Methods

        private DrilldownNavigationPath BuildNavigationPath(List<string> hierarchy, Dictionary<string, string> filters, int currentLevel)
        {
            var path = new DrilldownNavigationPath
            {
                CurrentLevel = currentLevel < hierarchy.Count ? hierarchy[currentLevel] : "Detail",
                CanDrillUp = currentLevel > 0,
                CanDrillDown = currentLevel < hierarchy.Count - 1
            };

            for (int i = 0; i < currentLevel && i < hierarchy.Count; i++)
            {
                var levelName = hierarchy[i];
                path.Breadcrumbs.Add(new DrilldownBreadcrumb
                {
                    LevelName = levelName,
                    DisplayValue = filters.ContainsKey(levelName) ? filters[levelName] : "All",
                    FilterKey = levelName,
                    FilterValue = filters.ContainsKey(levelName) ? filters[levelName] : ""
                });
            }

            return path;
        }

        private async Task<List<DrilldownDataRow>> GetSalesByYearAsync(IQueryable<RMMS.Models.RiceSales> query)
        {
            var data = await query
                .GroupBy(s => s.SaleDate.Year)
                .Select(g => new
                {
                    Year = g.Key,
                    TotalSales = g.Sum(s => s.TotalInvoiceValue),
                    Quantity = g.Sum(s => s.Quantity),
                    Count = g.Count()
                })
                .OrderByDescending(x => x.Year)
                .ToListAsync();

            return data.Select(d => new DrilldownDataRow
            {
                Key = d.Year.ToString(),
                DisplayValue = d.Year.ToString(),
                Metrics = new Dictionary<string, object>
                {
                    ["TotalSales"] = d.TotalSales,
                    ["Quantity"] = d.Quantity,
                    ["Count"] = d.Count
                },
                HasChildren = true,
                DrilldownUrl = $"?level=1&Year={d.Year}"
            }).ToList();
        }

        private async Task<List<DrilldownDataRow>> GetSalesByQuarterAsync(IQueryable<RMMS.Models.RiceSales> query, Dictionary<string, string> filters)
        {
            var data = await query
                .GroupBy(s => (s.SaleDate.Month - 1) / 3 + 1)
                .Select(g => new
                {
                    Quarter = g.Key,
                    TotalSales = g.Sum(s => s.TotalInvoiceValue),
                    Quantity = g.Sum(s => s.Quantity),
                    Count = g.Count()
                })
                .OrderBy(x => x.Quarter)
                .ToListAsync();

            return data.Select(d => new DrilldownDataRow
            {
                Key = $"Q{d.Quarter}",
                DisplayValue = $"Q{d.Quarter} {filters["Year"]}",
                Metrics = new Dictionary<string, object>
                {
                    ["TotalSales"] = d.TotalSales,
                    ["Quantity"] = d.Quantity,
                    ["Count"] = d.Count
                },
                HasChildren = true,
                DrilldownUrl = $"?level=2&Year={filters["Year"]}&Quarter={d.Quarter}"
            }).ToList();
        }

        private async Task<List<DrilldownDataRow>> GetSalesByMonthAsync(IQueryable<RMMS.Models.RiceSales> query, Dictionary<string, string> filters)
        {
            var data = await query
                .GroupBy(s => s.SaleDate.Month)
                .Select(g => new
                {
                    Month = g.Key,
                    TotalSales = g.Sum(s => s.TotalInvoiceValue),
                    Quantity = g.Sum(s => s.Quantity),
                    Count = g.Count()
                })
                .OrderBy(x => x.Month)
                .ToListAsync();

            return data.Select(d => new DrilldownDataRow
            {
                Key = d.Month.ToString(),
                DisplayValue = new DateTime(int.Parse(filters["Year"]), d.Month, 1).ToString("MMMM yyyy"),
                Metrics = new Dictionary<string, object>
                {
                    ["TotalSales"] = d.TotalSales,
                    ["Quantity"] = d.Quantity,
                    ["Count"] = d.Count
                },
                HasChildren = true,
                DrilldownUrl = $"?level=3&Year={filters["Year"]}&Quarter={filters["Quarter"]}&Month={d.Month}"
            }).ToList();
        }

        private async Task<List<DrilldownDataRow>> GetSalesByCustomerAsync(IQueryable<RMMS.Models.RiceSales> query)
        {
            var data = await query
                .GroupBy(s => s.BuyerName)
                .Select(g => new
                {
                    Customer = g.Key,
                    TotalSales = g.Sum(s => s.TotalInvoiceValue),
                    Quantity = g.Sum(s => s.Quantity),
                    Count = g.Count()
                })
                .OrderByDescending(x => x.TotalSales)
                .ToListAsync();

            return data.Select(d => new DrilldownDataRow
            {
                Key = d.Customer ?? "Unknown",
                DisplayValue = d.Customer ?? "Unknown",
                Metrics = new Dictionary<string, object>
                {
                    ["TotalSales"] = d.TotalSales,
                    ["Quantity"] = d.Quantity,
                    ["Count"] = d.Count
                },
                HasChildren = true
            }).ToList();
        }

        private async Task<List<DrilldownDataRow>> GetSalesByProductAsync(IQueryable<RMMS.Models.RiceSales> query, Dictionary<string, string> filters)
        {
            var data = await query
                .Where(s => s.BuyerName == filters["Customer"])
                .GroupBy(s => s.RiceGrade)
                .Select(g => new
                {
                    Product = g.Key,
                    TotalSales = g.Sum(s => s.TotalInvoiceValue),
                    Quantity = g.Sum(s => s.Quantity),
                    Count = g.Count()
                })
                .OrderByDescending(x => x.TotalSales)
                .ToListAsync();

            return data.Select(d => new DrilldownDataRow
            {
                Key = d.Product ?? "Unknown",
                DisplayValue = d.Product ?? "Unknown",
                Metrics = new Dictionary<string, object>
                {
                    ["TotalSales"] = d.TotalSales,
                    ["Quantity"] = d.Quantity,
                    ["Count"] = d.Count
                },
                HasChildren = false
            }).ToList();
        }

        private async Task<List<DrilldownDataRow>> GetInventoryByWarehouseAsync()
        {
            var warehouses = await _context.Warehouses
                .Where(w => w.IsActive)
                .Select(w => new
                {
                    w.Id,
                    w.WarehouseName,
                    w.WarehouseCode,
                    w.Location
                })
                .ToListAsync();

            return warehouses.Select(w => new DrilldownDataRow
            {
                Key = w.Id.ToString(),
                DisplayValue = w.WarehouseName ?? "Unknown",
                Metrics = new Dictionary<string, object>
                {
                    ["Code"] = w.WarehouseCode,
                    ["Location"] = w.Location ?? "N/A"
                },
                HasChildren = true
            }).ToList();
        }

        private async Task<List<DrilldownDataRow>> GetInventoryByCategoryAsync(Dictionary<string, string> filters)
        {
            var categories = await _context.Products
                .Where(p => p.IsActive)
                .GroupBy(p => p.ProductCategory)
                .Select(g => new
                {
                    Category = g.Key,
                    Count = g.Count()
                })
                .ToListAsync();

            return categories.Select(c => new DrilldownDataRow
            {
                Key = c.Category ?? "Unknown",
                DisplayValue = c.Category ?? "Unknown",
                Metrics = new Dictionary<string, object>
                {
                    ["ProductCount"] = c.Count
                },
                HasChildren = true
            }).ToList();
        }

        private async Task<List<DrilldownDataRow>> GetInventoryByProductAsync(Dictionary<string, string> filters)
        {
            var products = await _context.Products
                .Where(p => p.IsActive && p.ProductCategory == filters["Category"])
                .Select(p => new
                {
                    p.Id,
                    p.ProductName,
                    p.SellingPrice,
                    p.ProductCode
                })
                .ToListAsync();

            return products.Select(p => new DrilldownDataRow
            {
                Key = p.Id.ToString(),
                DisplayValue = p.ProductName ?? "Unknown",
                Metrics = new Dictionary<string, object>
                {
                    ["SellingPrice"] = p.SellingPrice ?? 0m,
                    ["ProductCode"] = p.ProductCode
                },
                HasChildren = false
            }).ToList();
        }

        private async Task<List<DrilldownDataRow>> GetProductionByYearAsync(IQueryable<RMMS.Models.Production.ProductionBatch> query)
        {
            var data = await query
                .GroupBy(b => b.BatchDate.Year)
                .Select(g => new
                {
                    Year = g.Key,
                    BatchCount = g.Count(),
                    CompletedCount = g.Count(b => b.Status == "Completed")
                })
                .OrderByDescending(x => x.Year)
                .ToListAsync();

            return data.Select(d => new DrilldownDataRow
            {
                Key = d.Year.ToString(),
                DisplayValue = d.Year.ToString(),
                Metrics = new Dictionary<string, object>
                {
                    ["TotalBatches"] = d.BatchCount,
                    ["Completed"] = d.CompletedCount
                },
                HasChildren = true
            }).ToList();
        }

        private async Task<List<DrilldownDataRow>> GetProductionByMonthAsync(IQueryable<RMMS.Models.Production.ProductionBatch> query, Dictionary<string, string> filters)
        {
            var data = await query
                .GroupBy(b => b.BatchDate.Month)
                .Select(g => new
                {
                    Month = g.Key,
                    BatchCount = g.Count(),
                    CompletedCount = g.Count(b => b.Status == "Completed")
                })
                .OrderBy(x => x.Month)
                .ToListAsync();

            return data.Select(d => new DrilldownDataRow
            {
                Key = d.Month.ToString(),
                DisplayValue = new DateTime(int.Parse(filters["Year"]), d.Month, 1).ToString("MMMM yyyy"),
                Metrics = new Dictionary<string, object>
                {
                    ["TotalBatches"] = d.BatchCount,
                    ["Completed"] = d.CompletedCount
                },
                HasChildren = true
            }).ToList();
        }

        private async Task<List<DrilldownDataRow>> GetProductionByBatchAsync(IQueryable<RMMS.Models.Production.ProductionBatch> query)
        {
            var batches = await query
                .Select(b => new
                {
                    b.Id,
                    b.BatchNumber,
                    b.Status,
                    b.CompletionPercent,
                    b.QualityScore
                })
                .ToListAsync();

            return batches.Select(b => new DrilldownDataRow
            {
                Key = b.Id.ToString(),
                DisplayValue = b.BatchNumber ?? "Unknown",
                Metrics = new Dictionary<string, object>
                {
                    ["Status"] = b.Status,
                    ["CompletionPercent"] = b.CompletionPercent,
                    ["QualityScore"] = b.QualityScore ?? 0
                },
                HasChildren = false
            }).ToList();
        }

        private async Task<List<DrilldownDataRow>> GetProductionByStatusAsync(IQueryable<RMMS.Models.Production.ProductionBatch> query)
        {
            var statuses = await query
                .GroupBy(b => b.Status)
                .Select(g => new
                {
                    Status = g.Key,
                    Count = g.Count()
                })
                .ToListAsync();

            return statuses.Select(s => new DrilldownDataRow
            {
                Key = s.Status,
                DisplayValue = s.Status,
                Metrics = new Dictionary<string, object>
                {
                    ["Count"] = s.Count
                },
                HasChildren = false
            }).ToList();
        }

        #endregion
    }
}
