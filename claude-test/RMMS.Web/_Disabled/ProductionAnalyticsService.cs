using Microsoft.EntityFrameworkCore;
using RMMS.DataAccess.Context;
using RMMS.Models.Production;

namespace RMMS.Services.Services.Analytics.Implementations
{
    public class ProductionAnalyticsService : IProductionAnalyticsService
    {
        private readonly ApplicationDbContext _context;

        public ProductionAnalyticsService(ApplicationDbContext context)
        {
            _context = context;
        }

        #region Task 1: Production Efficiency Monitoring

        public async Task<ProductionDashboardDto> GetProductionDashboard(DateTime? date = null)
        {
            var targetDate = date ?? DateTime.Today;
            var dashboard = new ProductionDashboardDto();

            // Get today's production batches
            var batches = await _context.ProductionBatches
                .Include(b => b.Inputs)
                .Include(b => b.Outputs)
                .Where(b => b.BatchDate.Date == targetDate.Date && b.IsActive)
                .ToListAsync();

            dashboard.TotalBatchesProduced = batches.Count;
            dashboard.CompletedBatches = batches.Count(b => b.Status == "Completed" || b.Status == "Verified");
            dashboard.InProgressBatches = batches.Count(b => b.Status == "In Progress");
            dashboard.PlannedBatches = batches.Count(b => b.Status == "Planned");

            // Calculate total output
            dashboard.TotalOutputQuantity = batches.Sum(b => b.TotalOutputQuantity);

            // Calculate average efficiency
            var efficiencies = new List<decimal>();
            foreach (var batch in batches.Where(b => b.Status == "Completed" || b.Status == "Verified"))
            {
                if (batch.TotalInputQuantity > 0)
                {
                    var efficiency = (batch.TotalOutputQuantity / batch.TotalInputQuantity) * 100;
                    efficiencies.Add(efficiency);
                }
            }
            dashboard.AverageEfficiency = efficiencies.Any() ? efficiencies.Average() : 0;

            // Get machine utilization
            var machines = await _context.Machines.Where(m => m.IsActive).ToListAsync();
            var batchesWithMachine = batches.Where(b => b.ProductionOrder != null).ToList();

            if (machines.Any())
            {
                dashboard.MachineUtilization = (decimal)batchesWithMachine.Count / machines.Count * 100;
            }

            // Calculate quality score
            var batchesWithQuality = batches.Where(b => b.QualityScore.HasValue).ToList();
            dashboard.QualityScore = batchesWithQuality.Any()
                ? batchesWithQuality.Average(b => b.QualityScore!.Value)
                : 0;

            // Defect rate (simplified)
            var totalOutputs = batches.Sum(b => b.TotalOutputQuantity);
            dashboard.DefectRate = 0; // Would need defect tracking data

            return dashboard;
        }

        public async Task<List<ProductionEfficiencyDto>> GetMachineEfficiencies(DateTime startDate, DateTime endDate)
        {
            var efficiencies = new List<ProductionEfficiencyDto>();

            var machines = await _context.Machines.Where(m => m.IsActive).ToListAsync();

            foreach (var machine in machines)
            {
                var efficiency = await CalculateMachineEfficiency(machine.Id, startDate, endDate);
                efficiencies.Add(efficiency);
            }

            return efficiencies.OrderByDescending(e => e.OverallEfficiency).ToList();
        }

        public async Task<ProductionEfficiencyDto> CalculateMachineEfficiency(int machineId, DateTime startDate, DateTime endDate)
        {
            var machine = await _context.Machines.FindAsync(machineId);

            // Get production orders for this machine
            var orders = await _context.ProductionOrders
                .Where(o => o.MachineId == machineId
                    && o.StartDate >= startDate
                    && o.StartDate <= endDate
                    && o.IsActive)
                .ToListAsync();

            var batches = new List<ProductionBatch>();
            foreach (var order in orders)
            {
                var orderBatches = await _context.ProductionBatches
                    .Include(b => b.Inputs)
                    .Include(b => b.Outputs)
                    .Where(b => b.ProductionOrderId == order.Id && b.IsActive)
                    .ToListAsync();
                batches.AddRange(orderBatches);
            }

            var totalInput = batches.Sum(b => b.TotalInputQuantity);
            var totalOutput = batches.Sum(b => b.TotalOutputQuantity);
            var overallEfficiency = totalInput > 0 ? (totalOutput / totalInput) * 100 : 0;

            var totalDuration = batches
                .Where(b => b.StartTime.HasValue && b.EndTime.HasValue)
                .Sum(b => (decimal)(b.EndTime!.Value - b.StartTime!.Value).TotalHours);

            return new ProductionEfficiencyDto
            {
                MachineId = machineId,
                MachineName = machine?.MachineName ?? "Unknown",
                TotalBatches = batches.Count,
                TotalInputQuantity = totalInput,
                TotalOutputQuantity = totalOutput,
                OverallEfficiency = overallEfficiency,
                AverageOutputPerBatch = batches.Count > 0 ? totalOutput / batches.Count : 0,
                TotalProductionTime = totalDuration,
                StartDate = startDate,
                EndDate = endDate
            };
        }

        public async Task<List<ShiftPerformanceDto>> GetShiftPerformance(DateTime startDate, DateTime endDate)
        {
            var batches = await _context.ProductionBatches
                .Include(b => b.Inputs)
                .Include(b => b.Outputs)
                .Where(b => b.BatchDate >= startDate && b.BatchDate <= endDate && b.IsActive)
                .ToListAsync();

            var performance = batches
                .GroupBy(b => b.ShiftType)
                .Select(g => new ShiftPerformanceDto
                {
                    ShiftType = g.Key,
                    TotalBatches = g.Count(),
                    CompletedBatches = g.Count(b => b.Status == "Completed" || b.Status == "Verified"),
                    TotalOutput = g.Sum(b => b.TotalOutputQuantity),
                    AverageOutput = g.Average(b => b.TotalOutputQuantity),
                    AverageEfficiency = g.Where(b => b.TotalInputQuantity > 0)
                        .Average(b => (b.TotalOutputQuantity / b.TotalInputQuantity) * 100),
                    AverageQualityScore = g.Where(b => b.QualityScore.HasValue)
                        .Select(b => b.QualityScore!.Value)
                        .DefaultIfEmpty(0)
                        .Average()
                })
                .OrderByDescending(p => p.AverageEfficiency)
                .ToList();

            return performance;
        }

        public async Task<decimal> CalculateOEE(int machineId, DateTime startDate, DateTime endDate)
        {
            // OEE = Availability × Performance × Quality

            // Get production orders for this machine
            var orders = await _context.ProductionOrders
                .Where(o => o.MachineId == machineId
                    && o.StartDate >= startDate
                    && o.StartDate <= endDate
                    && o.IsActive)
                .ToListAsync();

            var batches = new List<ProductionBatch>();
            foreach (var order in orders)
            {
                var orderBatches = await _context.ProductionBatches
                    .Include(b => b.Inputs)
                    .Include(b => b.Outputs)
                    .Where(b => b.ProductionOrderId == order.Id && b.IsActive)
                    .ToListAsync();
                batches.AddRange(orderBatches);
            }

            if (!batches.Any()) return 0;

            // Calculate Availability
            var totalScheduledTime = (endDate - startDate).TotalHours;
            var actualProductionTime = batches
                .Where(b => b.StartTime.HasValue && b.EndTime.HasValue)
                .Sum(b => (b.EndTime!.Value - b.StartTime!.Value).TotalHours);
            var availability = totalScheduledTime > 0 ? (decimal)(actualProductionTime / totalScheduledTime) : 0;

            // Calculate Performance
            var totalOutput = batches.Sum(b => b.TotalOutputQuantity);
            var idealCycleTime = 1.0m; // Simplified - should be machine-specific
            var idealOutput = (decimal)actualProductionTime * idealCycleTime;
            var performance = idealOutput > 0 ? totalOutput / idealOutput : 0;

            // Calculate Quality
            var totalInput = batches.Sum(b => b.TotalInputQuantity);
            var quality = totalInput > 0 ? totalOutput / totalInput : 0;

            var oee = availability * performance * quality * 100;

            return Math.Min(oee, 100); // Cap at 100%
        }

        #endregion

        #region Task 7: Downtime & Utilization Analysis

        public async Task<List<DowntimeAnalysisDto>> GetDowntimeAnalysis(DateTime startDate, DateTime endDate, int? machineId = null)
        {
            // Get all batches with timing info
            var query = _context.ProductionBatches
                .Include(b => b.ProductionOrder)
                .ThenInclude(o => o!.Machine)
                .Where(b => b.BatchDate >= startDate
                    && b.BatchDate <= endDate
                    && b.IsActive
                    && b.StartTime.HasValue
                    && b.EndTime.HasValue);

            if (machineId.HasValue)
            {
                query = query.Where(b => b.ProductionOrder != null && b.ProductionOrder.MachineId == machineId.Value);
            }

            var batches = await query.ToListAsync();

            // Calculate downtime between batches
            var downtimeList = new List<DowntimeAnalysisDto>();

            var groupedByMachine = batches.GroupBy(b => b.ProductionOrder?.MachineId);

            foreach (var machineGroup in groupedByMachine)
            {
                if (!machineGroup.Key.HasValue) continue;

                var orderedBatches = machineGroup.OrderBy(b => b.StartTime).ToList();

                for (int i = 1; i < orderedBatches.Count; i++)
                {
                    var prevBatch = orderedBatches[i - 1];
                    var currentBatch = orderedBatches[i];

                    if (prevBatch.EndTime.HasValue && currentBatch.StartTime.HasValue)
                    {
                        var downtimeMinutes = (currentBatch.StartTime.Value - prevBatch.EndTime.Value).TotalMinutes;

                        if (downtimeMinutes > 10) // Only record significant downtime
                        {
                            downtimeList.Add(new DowntimeAnalysisDto
                            {
                                MachineId = machineGroup.Key.Value,
                                MachineName = prevBatch.ProductionOrder?.Machine?.MachineName ?? "Unknown",
                                StartTime = prevBatch.EndTime.Value,
                                EndTime = currentBatch.StartTime.Value,
                                DurationMinutes = (decimal)downtimeMinutes,
                                Reason = "Between Batches",
                                Category = "Planned",
                                ImpactHours = (decimal)(downtimeMinutes / 60)
                            });
                        }
                    }
                }
            }

            return downtimeList.OrderByDescending(d => d.DurationMinutes).ToList();
        }

        public async Task<List<MachineUtilizationDto>> GetMachineUtilization(DateTime startDate, DateTime endDate)
        {
            var utilizations = new List<MachineUtilizationDto>();
            var machines = await _context.Machines.Where(m => m.IsActive).ToListAsync();
            var totalHours = (decimal)(endDate - startDate).TotalHours;

            foreach (var machine in machines)
            {
                var orders = await _context.ProductionOrders
                    .Where(o => o.MachineId == machine.Id
                        && o.StartDate >= startDate
                        && o.StartDate <= endDate
                        && o.IsActive)
                    .ToListAsync();

                var batches = new List<ProductionBatch>();
                foreach (var order in orders)
                {
                    var orderBatches = await _context.ProductionBatches
                        .Include(b => b.Inputs)
                        .Include(b => b.Outputs)
                        .Where(b => b.ProductionOrderId == order.Id
                            && b.IsActive
                            && b.StartTime.HasValue
                            && b.EndTime.HasValue)
                        .ToListAsync();
                    batches.AddRange(orderBatches);
                }

                var actualRunTime = batches.Sum(b => (decimal)(b.EndTime!.Value - b.StartTime!.Value).TotalHours);
                var utilizationPercentage = totalHours > 0 ? (actualRunTime / totalHours) * 100 : 0;

                utilizations.Add(new MachineUtilizationDto
                {
                    MachineId = machine.Id,
                    MachineName = machine.MachineName,
                    AvailableHours = totalHours,
                    ActualRunTime = actualRunTime,
                    UtilizationPercentage = utilizationPercentage,
                    TotalBatches = batches.Count,
                    TotalOutput = batches.Sum(b => b.TotalOutputQuantity)
                });
            }

            return utilizations.OrderByDescending(u => u.UtilizationPercentage).ToList();
        }

        public async Task<Dictionary<string, decimal>> GetCapacityPlanningData(DateTime futureDate)
        {
            var data = new Dictionary<string, decimal>();

            var machines = await _context.Machines.Where(m => m.IsActive).ToListAsync();
            data["TotalMachines"] = machines.Count;

            // Calculate average output per machine per day
            var thirtyDaysAgo = DateTime.Today.AddDays(-30);
            var recentBatches = await _context.ProductionBatches
                .Include(b => b.Outputs)
                .Where(b => b.BatchDate >= thirtyDaysAgo && b.IsActive)
                .ToListAsync();

            var averageOutputPerDay = recentBatches.Any()
                ? recentBatches.Sum(b => b.TotalOutputQuantity) / 30
                : 0;

            data["AverageOutputPerDay"] = averageOutputPerDay;

            // Project future capacity
            var daysUntilFuture = (futureDate - DateTime.Today).Days;
            data["ProjectedOutput"] = averageOutputPerDay * daysUntilFuture;

            return data;
        }

        public async Task<List<Machine>> GetMachinesRequiringMaintenance(int daysAhead = 30)
        {
            // This is simplified - would need maintenance schedule tracking
            var machines = await _context.Machines
                .Where(m => m.IsActive)
                .ToListAsync();

            // Return machines that need maintenance soon (simplified logic)
            return machines.Take(5).ToList();
        }

        #endregion

        #region Task 8: Quality Tracking

        public async Task<List<QualityMetricsDto>> GetQualityTrends(DateTime startDate, DateTime endDate)
        {
            var batches = await _context.ProductionBatches
                .Include(b => b.Inputs)
                .Include(b => b.Outputs)
                .Where(b => b.BatchDate >= startDate
                    && b.BatchDate <= endDate
                    && b.IsActive
                    && (b.Status == "Completed" || b.Status == "Verified"))
                .ToListAsync();

            var metrics = batches
                .GroupBy(b => b.BatchDate.Date)
                .Select(g => new QualityMetricsDto
                {
                    Date = g.Key,
                    TotalBatches = g.Count(),
                    AverageQualityScore = g.Where(b => b.QualityScore.HasValue)
                        .Select(b => b.QualityScore!.Value)
                        .DefaultIfEmpty(0)
                        .Average(),
                    DefectCount = 0, // Would need defect tracking
                    DefectRate = 0,
                    PassRate = 100,
                    ReworkCount = 0,
                    ScrapCount = 0
                })
                .OrderBy(m => m.Date)
                .ToList();

            return metrics;
        }

        public async Task<Dictionary<string, int>> GetDefectAnalysis(DateTime startDate, DateTime endDate)
        {
            // Simplified - would need actual defect tracking system
            var defects = new Dictionary<string, int>
            {
                { "Surface Defects", 0 },
                { "Dimensional Issues", 0 },
                { "Material Defects", 0 },
                { "Assembly Issues", 0 },
                { "Other", 0 }
            };

            return defects;
        }

        #endregion

        #region Task 9: Yield Optimization

        public async Task<List<YieldOptimizationDto>> GetYieldOptimizationSuggestions()
        {
            var suggestions = new List<YieldOptimizationDto>();

            // Get recent batches (last 30 days)
            var thirtyDaysAgo = DateTime.Today.AddDays(-30);
            var batches = await _context.ProductionBatches
                .Include(b => b.Inputs)
                .Include(b => b.Outputs)
                .Include(b => b.ProductionOrder)
                .ThenInclude(o => o!.Machine)
                .Where(b => b.BatchDate >= thirtyDaysAgo
                    && b.IsActive
                    && (b.Status == "Completed" || b.Status == "Verified"))
                .ToListAsync();

            // Group by machine and calculate yield
            var machineYields = batches
                .Where(b => b.ProductionOrder != null)
                .GroupBy(b => b.ProductionOrder!.MachineId)
                .Select(g => new
                {
                    MachineId = g.Key,
                    MachineName = g.First().ProductionOrder?.Machine?.MachineName ?? "Unknown",
                    AverageYield = g.Where(b => b.TotalInputQuantity > 0)
                        .Average(b => (b.TotalOutputQuantity / b.TotalInputQuantity) * 100),
                    BatchCount = g.Count()
                })
                .ToList();

            // Find machines with below-average yield
            var averageYield = machineYields.Any() ? machineYields.Average(m => m.AverageYield) : 0;

            foreach (var machine in machineYields.Where(m => m.AverageYield < averageYield))
            {
                suggestions.Add(new YieldOptimizationDto
                {
                    MachineId = machine.MachineId,
                    MachineName = machine.MachineName,
                    CurrentYield = machine.AverageYield,
                    PotentialYield = averageYield,
                    ImprovementPotential = averageYield - machine.AverageYield,
                    Suggestion = $"Machine {machine.MachineName} has {machine.AverageYield:F2}% yield vs average {averageYield:F2}%. Consider maintenance or process review.",
                    Priority = machine.AverageYield < (averageYield * 0.8m) ? "High" : "Medium"
                });
            }

            return suggestions.OrderByDescending(s => s.ImprovementPotential).ToList();
        }

        public async Task<List<WasteTrackingDto>> GetWasteByProduct(DateTime startDate, DateTime endDate)
        {
            var batches = await _context.ProductionBatches
                .Include(b => b.Inputs)
                .ThenInclude(i => i.Product)
                .Include(b => b.Outputs)
                .Where(b => b.BatchDate >= startDate
                    && b.BatchDate <= endDate
                    && b.IsActive)
                .ToListAsync();

            var wasteData = new List<WasteTrackingDto>();

            foreach (var batch in batches)
            {
                var totalInput = batch.TotalInputQuantity;
                var totalOutput = batch.TotalOutputQuantity;
                var waste = totalInput - totalOutput;

                if (waste > 0)
                {
                    var inputProduct = batch.Inputs.FirstOrDefault()?.Product;
                    if (inputProduct != null)
                    {
                        wasteData.Add(new WasteTrackingDto
                        {
                            ProductId = inputProduct.Id,
                            ProductName = inputProduct.ProductName,
                            WasteQuantity = waste,
                            WastePercentage = totalInput > 0 ? (waste / totalInput) * 100 : 0,
                            WasteCost = waste * (batch.Inputs.FirstOrDefault()?.UnitCost ?? 0),
                            Period = $"{startDate:yyyy-MM-dd} to {endDate:yyyy-MM-dd}"
                        });
                    }
                }
            }

            var grouped = wasteData
                .GroupBy(w => new { w.ProductId, w.ProductName })
                .Select(g => new WasteTrackingDto
                {
                    ProductId = g.Key.ProductId,
                    ProductName = g.Key.ProductName,
                    WasteQuantity = g.Sum(w => w.WasteQuantity),
                    WastePercentage = g.Average(w => w.WastePercentage),
                    WasteCost = g.Sum(w => w.WasteCost),
                    Period = $"{startDate:yyyy-MM-dd} to {endDate:yyyy-MM-dd}"
                })
                .OrderByDescending(w => w.WasteCost)
                .ToList();

            return grouped;
        }

        public async Task<List<WasteTrackingDto>> GetWasteByProcess(DateTime startDate, DateTime endDate)
        {
            var batches = await _context.ProductionBatches
                .Include(b => b.Inputs)
                .Include(b => b.Outputs)
                .Include(b => b.ProductionOrder)
                .Where(b => b.BatchDate >= startDate
                    && b.BatchDate <= endDate
                    && b.IsActive)
                .ToListAsync();

            var wasteData = new List<WasteTrackingDto>();

            foreach (var batch in batches)
            {
                var totalInput = batch.TotalInputQuantity;
                var totalOutput = batch.TotalOutputQuantity;
                var waste = totalInput - totalOutput;

                if (waste > 0)
                {
                    wasteData.Add(new WasteTrackingDto
                    {
                        ProductId = 0,
                        ProductName = batch.ProductionOrder?.OrderNumber ?? "Unknown Process",
                        WasteQuantity = waste,
                        WastePercentage = totalInput > 0 ? (waste / totalInput) * 100 : 0,
                        WasteCost = waste * (batch.Inputs.FirstOrDefault()?.UnitCost ?? 0),
                        Period = $"{startDate:yyyy-MM-dd} to {endDate:yyyy-MM-dd}"
                    });
                }
            }

            return wasteData.OrderByDescending(w => w.WasteCost).ToList();
        }

        public async Task<decimal> CalculateTotalWasteCost(DateTime startDate, DateTime endDate)
        {
            var wasteByProduct = await GetWasteByProduct(startDate, endDate);
            return wasteByProduct.Sum(w => w.WasteCost);
        }

        public async Task<List<WasteReductionTargetDto>> GetWasteReductionTargets()
        {
            var thirtyDaysAgo = DateTime.Today.AddDays(-30);
            var wasteData = await GetWasteByProduct(thirtyDaysAgo, DateTime.Today);

            return wasteData
                .Where(w => w.WastePercentage > 5) // Target products with >5% waste
                .Select(w => new WasteReductionTargetDto
                {
                    ProductId = w.ProductId,
                    ProductName = w.ProductName,
                    CurrentWastePercentage = w.WastePercentage,
                    TargetWastePercentage = w.WastePercentage * 0.8m, // 20% reduction target
                    PotentialSavings = w.WasteCost * 0.2m,
                    RecommendedAction = "Review production process and quality controls"
                })
                .OrderByDescending(t => t.PotentialSavings)
                .ToList();
        }

        #endregion
    }
}
