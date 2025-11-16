using System;
using System.Collections.Generic;
using System.Linq;
using RMMS.DataAccess.Repositories.Production;
using RMMS.Models.Production;
using RMMS.Services.Interfaces.Production;

namespace RMMS.Services.Implementations.Production
{
    public class YieldAnalysisService : IYieldAnalysisService
    {
        private readonly IProductionBatchRepository _batchRepository;

        public YieldAnalysisService(IProductionBatchRepository batchRepository)
        {
            _batchRepository = batchRepository;
        }

        public YieldStatistics GetOverallYieldStatistics(DateTime? fromDate = null, DateTime? toDate = null)
        {
            var batches = GetCompletedBatchesWithYield(fromDate, toDate);

            if (!batches.Any())
            {
                return new YieldStatistics
                {
                    StandardYieldPercent = 65.0m
                };
            }

            var statistics = new YieldStatistics
            {
                TotalBatches = batches.Count,
                TotalInputQuantity = batches.Sum(b => b.TotalInputQuantity),
                TotalOutputQuantity = batches.Sum(b => b.TotalOutputQuantity),
                AverageYieldPercent = batches.Average(b => b.YieldRecord!.TotalYieldPercent),
                MinYieldPercent = batches.Min(b => b.YieldRecord!.TotalYieldPercent),
                MaxYieldPercent = batches.Max(b => b.YieldRecord!.TotalYieldPercent),
                StandardYieldPercent = 65.0m
            };

            statistics.YieldVariance = statistics.AverageYieldPercent - statistics.StandardYieldPercent;
            statistics.BatchesAboveStandard = batches.Count(b => b.YieldRecord!.TotalYieldPercent >= statistics.StandardYieldPercent);
            statistics.BatchesBelowStandard = batches.Count(b => b.YieldRecord!.TotalYieldPercent < statistics.StandardYieldPercent);

            return statistics;
        }

        public List<YieldTrendData> GetYieldTrends(DateTime fromDate, DateTime toDate, string groupBy = "Daily")
        {
            var batches = GetCompletedBatchesWithYield(fromDate, toDate);

            if (!batches.Any())
            {
                return new List<YieldTrendData>();
            }

            IEnumerable<IGrouping<string, ProductionBatch>> groupedBatches;

            switch (groupBy.ToUpper())
            {
                case "WEEKLY":
                    groupedBatches = batches.GroupBy(b => GetWeekKey(b.BatchDate));
                    break;
                case "MONTHLY":
                    groupedBatches = batches.GroupBy(b => b.BatchDate.ToString("yyyy-MM"));
                    break;
                default: // Daily
                    groupedBatches = batches.GroupBy(b => b.BatchDate.ToString("yyyy-MM-dd"));
                    break;
            }

            var trends = groupedBatches.Select(g => new YieldTrendData
            {
                Period = FormatPeriod(g.Key, groupBy),
                PeriodDate = g.First().BatchDate,
                BatchCount = g.Count(),
                AverageYield = g.Average(b => b.YieldRecord!.TotalYieldPercent),
                HeadRicePercent = g.Average(b => b.YieldRecord!.HeadRicePercent),
                BrokenRicePercent = g.Average(b => b.YieldRecord!.BrokenRicePercent),
                BranPercent = g.Average(b => b.YieldRecord!.BranPercent),
                HuskPercent = g.Average(b => b.YieldRecord!.HuskPercent)
            }).OrderBy(t => t.PeriodDate).ToList();

            return trends;
        }

        public List<YieldByVarietyData> GetYieldByPaddyVariety(DateTime? fromDate = null, DateTime? toDate = null)
        {
            var batches = GetCompletedBatchesWithYield(fromDate, toDate);

            if (!batches.Any())
            {
                return new List<YieldByVarietyData>();
            }

            var varietyData = batches
                .Where(b => !string.IsNullOrEmpty(b.YieldRecord!.PaddyVariety))
                .GroupBy(b => b.YieldRecord!.PaddyVariety!)
                .Select(g => new YieldByVarietyData
                {
                    PaddyVariety = g.Key,
                    BatchCount = g.Count(),
                    TotalInputQuantity = g.Sum(b => b.TotalInputQuantity),
                    TotalOutputQuantity = g.Sum(b => b.TotalOutputQuantity),
                    AverageYieldPercent = g.Average(b => b.YieldRecord!.TotalYieldPercent),
                    BestYieldPercent = g.Max(b => b.YieldRecord!.TotalYieldPercent),
                    WorstYieldPercent = g.Min(b => b.YieldRecord!.TotalYieldPercent)
                })
                .OrderByDescending(v => v.AverageYieldPercent)
                .ToList();

            return varietyData;
        }

        public List<YieldByMachineData> GetYieldByMachine(DateTime? fromDate = null, DateTime? toDate = null)
        {
            var batches = GetCompletedBatchesWithYield(fromDate, toDate)
                .Where(b => b.ProductionOrder?.AssignedMachineId != null)
                .ToList();

            if (!batches.Any())
            {
                return new List<YieldByMachineData>();
            }

            var machineData = batches
                .GroupBy(b => new { b.ProductionOrder!.AssignedMachine!.MachineName, b.ProductionOrder.AssignedMachine.MachineCode })
                .Select(g => new YieldByMachineData
                {
                    MachineName = g.Key.MachineName,
                    MachineCode = g.Key.MachineCode,
                    BatchCount = g.Count(),
                    AverageYieldPercent = g.Average(b => b.YieldRecord!.TotalYieldPercent),
                    TotalInputQuantity = g.Sum(b => b.TotalInputQuantity),
                    TotalOutputQuantity = g.Sum(b => b.TotalOutputQuantity)
                })
                .OrderByDescending(m => m.AverageYieldPercent)
                .ToList();

            return machineData;
        }

        public YieldComparisonData GetYieldComparison(DateTime? fromDate = null, DateTime? toDate = null)
        {
            // Default to last 30 days if no dates provided
            var endDate = toDate ?? DateTime.Today;
            var startDate = fromDate ?? endDate.AddDays(-30);
            var periodDays = (endDate - startDate).Days;
            var midPoint = startDate.AddDays(periodDays / 2.0);

            var currentPeriodBatches = GetCompletedBatchesWithYield(midPoint, endDate);
            var previousPeriodBatches = GetCompletedBatchesWithYield(startDate, midPoint);

            var comparison = new YieldComparisonData
            {
                CurrentPeriodBatches = currentPeriodBatches.Count,
                PreviousPeriodBatches = previousPeriodBatches.Count
            };

            if (currentPeriodBatches.Any())
            {
                comparison.CurrentPeriodAverage = currentPeriodBatches.Average(b => b.YieldRecord!.TotalYieldPercent);
            }

            if (previousPeriodBatches.Any())
            {
                comparison.PreviousPeriodAverage = previousPeriodBatches.Average(b => b.YieldRecord!.TotalYieldPercent);
            }

            if (comparison.PreviousPeriodAverage > 0)
            {
                comparison.PercentChange = ((comparison.CurrentPeriodAverage - comparison.PreviousPeriodAverage) / comparison.PreviousPeriodAverage) * 100;

                if (comparison.PercentChange > 2)
                    comparison.Trend = "Improving";
                else if (comparison.PercentChange < -2)
                    comparison.Trend = "Declining";
                else
                    comparison.Trend = "Stable";
            }
            else
            {
                comparison.Trend = "No Previous Data";
            }

            return comparison;
        }

        public List<ProductionBatch> GetLowYieldBatches(decimal threshold, DateTime? fromDate = null, DateTime? toDate = null)
        {
            var batches = GetCompletedBatchesWithYield(fromDate, toDate);

            return batches
                .Where(b => b.YieldRecord!.TotalYieldPercent < threshold)
                .OrderBy(b => b.YieldRecord!.TotalYieldPercent)
                .ToList();
        }

        public List<ProductionBatch> GetHighYieldBatches(decimal threshold, DateTime? fromDate = null, DateTime? toDate = null)
        {
            var batches = GetCompletedBatchesWithYield(fromDate, toDate);

            return batches
                .Where(b => b.YieldRecord!.TotalYieldPercent >= threshold)
                .OrderByDescending(b => b.YieldRecord!.TotalYieldPercent)
                .ToList();
        }

        public List<YieldVarianceData> GetYieldVarianceAnalysis(DateTime? fromDate = null, DateTime? toDate = null)
        {
            var batches = GetCompletedBatchesWithYield(fromDate, toDate);

            var varianceData = batches.Select(b => new YieldVarianceData
            {
                BatchNumber = b.BatchNumber,
                BatchDate = b.BatchDate,
                PaddyVariety = b.YieldRecord!.PaddyVariety ?? "Unknown",
                ActualYield = b.YieldRecord.TotalYieldPercent,
                StandardYield = b.YieldRecord.StandardHeadRicePercent ?? 65.0m,
                Variance = b.YieldRecord.TotalYieldPercent - (b.YieldRecord.StandardHeadRicePercent ?? 65.0m),
                VariancePercent = ((b.YieldRecord.TotalYieldPercent - (b.YieldRecord.StandardHeadRicePercent ?? 65.0m)) / (b.YieldRecord.StandardHeadRicePercent ?? 65.0m)) * 100,
                VarianceType = b.YieldRecord.TotalYieldPercent >= (b.YieldRecord.StandardHeadRicePercent ?? 65.0m) ? "Positive" : "Negative"
            })
            .OrderByDescending(v => Math.Abs(v.Variance))
            .ToList();

            return varianceData;
        }

        public ProductionSummaryData GetProductionSummary(DateTime? fromDate = null, DateTime? toDate = null)
        {
            var batches = GetCompletedBatchesWithYield(fromDate, toDate);

            if (!batches.Any())
            {
                return new ProductionSummaryData();
            }

            var summary = new ProductionSummaryData
            {
                TotalBatches = batches.Count,
                TotalPaddyProcessed = batches.Sum(b => b.TotalInputQuantity),
                TotalRiceProduced = batches.Sum(b => b.YieldRecord!.OutputHeadRice + b.YieldRecord.OutputBrokenRice),
                TotalBranProduced = batches.Sum(b => b.YieldRecord!.OutputBran),
                TotalHuskProduced = batches.Sum(b => b.YieldRecord!.OutputHusk),
                TotalBrokenRice = batches.Sum(b => b.YieldRecord!.OutputBrokenRice),
                AverageYield = batches.Average(b => b.YieldRecord!.TotalYieldPercent),
                MachinesUsed = batches.Where(b => b.ProductionOrder?.AssignedMachineId != null)
                                     .Select(b => b.ProductionOrder!.AssignedMachineId)
                                     .Distinct()
                                     .Count()
            };

            var batchesWithDuration = batches.Where(b => b.DurationHours.HasValue).ToList();
            if (batchesWithDuration.Any())
            {
                summary.TotalProcessingHours = batchesWithDuration.Sum(b => b.DurationHours!.Value);
                summary.AverageBatchDuration = batchesWithDuration.Average(b => b.DurationHours!.Value);
            }

            return summary;
        }

        public List<BatchPerformanceData> GetBatchPerformanceDetails(DateTime? fromDate = null, DateTime? toDate = null)
        {
            var batches = GetCompletedBatchesWithYield(fromDate, toDate);

            var performanceData = batches.Select(b => new BatchPerformanceData
            {
                BatchNumber = b.BatchNumber,
                BatchDate = b.BatchDate,
                ShiftType = b.ShiftType,
                OperatorName = b.OperatorId.HasValue ? $"Operator {b.OperatorId}" : "N/A",
                InputQuantity = b.TotalInputQuantity,
                OutputQuantity = b.TotalOutputQuantity,
                YieldPercent = b.YieldRecord!.TotalYieldPercent,
                ProcessingHours = b.DurationHours ?? 0,
                QualityScore = b.QualityScore ?? 0,
                Status = b.Status,
                PerformanceRating = GetPerformanceRating(b.YieldRecord.TotalYieldPercent, b.QualityScore ?? 0)
            })
            .OrderByDescending(p => p.BatchDate)
            .ToList();

            return performanceData;
        }

        // Helper Methods
        private List<ProductionBatch> GetCompletedBatchesWithYield(DateTime? fromDate = null, DateTime? toDate = null)
        {
            var batches = _batchRepository.GetBatchesWithYieldRecords()
                .Where(b => b.Status == "Completed" && b.YieldRecord != null)
                .ToList();

            if (fromDate.HasValue)
            {
                batches = batches.Where(b => b.BatchDate >= fromDate.Value).ToList();
            }

            if (toDate.HasValue)
            {
                batches = batches.Where(b => b.BatchDate <= toDate.Value).ToList();
            }

            return batches;
        }

        private string GetWeekKey(DateTime date)
        {
            var culture = System.Globalization.CultureInfo.CurrentCulture;
            var weekNum = culture.Calendar.GetWeekOfYear(date, System.Globalization.CalendarWeekRule.FirstDay, DayOfWeek.Monday);
            return $"{date.Year}-W{weekNum:00}";
        }

        private string FormatPeriod(string key, string groupBy)
        {
            switch (groupBy.ToUpper())
            {
                case "WEEKLY":
                    return key; // Already formatted as "YYYY-WNN"
                case "MONTHLY":
                    var parts = key.Split('-');
                    if (parts.Length == 2 && int.TryParse(parts[1], out int month))
                    {
                        var monthName = new DateTime(2000, month, 1).ToString("MMM");
                        return $"{monthName} {parts[0]}";
                    }
                    return key;
                default: // Daily
                    if (DateTime.TryParse(key, out DateTime date))
                    {
                        return date.ToString("dd-MMM-yyyy");
                    }
                    return key;
            }
        }

        private string GetPerformanceRating(decimal yieldPercent, decimal qualityScore)
        {
            // Combined rating based on yield and quality
            var combinedScore = (yieldPercent / 100 * 0.6m) + (qualityScore / 10 * 0.4m);

            if (combinedScore >= 0.85m)
                return "Excellent";
            else if (combinedScore >= 0.70m)
                return "Good";
            else if (combinedScore >= 0.55m)
                return "Average";
            else
                return "Poor";
        }
    }
}
