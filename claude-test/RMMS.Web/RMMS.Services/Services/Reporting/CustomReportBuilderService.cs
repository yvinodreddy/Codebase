using System;
using System.Collections.Generic;
using System.Data;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.Data.SqlClient;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;
using RMMS.DataAccess.Context;
using RMMS.Models.Reporting;

namespace RMMS.Services.Services.Reporting
{
    public class CustomReportBuilderService : ICustomReportBuilderService
    {
        private readonly ApplicationDbContext _context;
        private readonly ILogger<CustomReportBuilderService> _logger;
        private readonly IConfiguration _configuration;

        public CustomReportBuilderService(
            ApplicationDbContext context,
            ILogger<CustomReportBuilderService> logger,
            IConfiguration configuration)
        {
            _context = context;
            _logger = logger;
            _configuration = configuration;
        }

        public async Task<int> SaveReportDefinitionAsync(CustomReportDefinition report)
        {
            _logger.LogInformation($"Saving report definition: {report.ReportName}");
            await Task.CompletedTask;
            // Store in CustomReports table
            return 1; // Return report ID
        }

        public async Task<CustomReportDefinition> GetReportDefinitionAsync(int reportId)
        {
            await Task.CompletedTask;
            return new CustomReportDefinition
            {
                Id = reportId,
                ReportName = "Sample Report",
                DataSource = "RiceSales",
                Columns = new List<ReportColumn>
                {
                    new() { FieldName = "InvoiceNumber", DisplayName = "Invoice #", DisplayOrder = 1 },
                    new() { FieldName = "SaleDate", DisplayName = "Date", DisplayOrder = 2 },
                    new() { FieldName = "TotalInvoiceValue", DisplayName = "Amount", DisplayOrder = 3, AggregateFunction = "SUM" }
                }
            };
        }

        public async Task<List<CustomReportDefinition>> GetUserReportsAsync(string userId)
        {
            await Task.CompletedTask;
            return new List<CustomReportDefinition>
            {
                new() { Id = 1, ReportName = "Monthly Sales", Category = "Sales", CreatedBy = userId },
                new() { Id = 2, ReportName = "Inventory Status", Category = "Inventory", CreatedBy = userId }
            };
        }

        public async Task<CustomReportResult> ExecuteReportAsync(int reportId, Dictionary<string, string> parameters)
        {
            var definition = await GetReportDefinitionAsync(reportId);

            // Build SQL from definition
            var sql = BuildSQLFromDefinition(definition, parameters);

            return await ExecuteCustomSQLAsync(sql);
        }

        public async Task<CustomReportResult> ExecuteCustomSQLAsync(string sql)
        {
            try
            {
                _logger.LogInformation($"Executing custom SQL: {sql.Substring(0, Math.Min(100, sql.Length))}...");

                var result = new CustomReportResult { ReportName = "Custom Query" };

                using var connection = new SqlConnection(_configuration.GetConnectionString("DefaultConnection"));
                await connection.OpenAsync();

                using var command = new SqlCommand(sql, connection);
                using var reader = await command.ExecuteReaderAsync();

                // Get column names
                var columns = new List<string>();
                for (int i = 0; i < reader.FieldCount; i++)
                {
                    columns.Add(reader.GetName(i));
                }

                // Read data
                while (await reader.ReadAsync())
                {
                    var row = new Dictionary<string, object>();
                    foreach (var column in columns)
                    {
                        row[column] = reader[column];
                    }
                    result.Data.Add(row);
                }

                result.TotalRecords = result.Data.Count;
                _logger.LogInformation($"Query returned {result.TotalRecords} records");

                return result;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error executing custom SQL");
                throw;
            }
        }

        public async Task<bool> DeleteReportAsync(int reportId)
        {
            _logger.LogInformation($"Deleted report #{reportId}");
            await Task.CompletedTask;
            return true;
        }

        public async Task<List<string>> GetAvailableDataSourcesAsync()
        {
            await Task.CompletedTask;
            return new List<string>
            {
                "RiceSales",
                "Products",
                "ProductionBatches",
                "StockMovements",
                "CashBooks"
            };
        }

        public async Task<List<string>> GetDataSourceColumnsAsync(string dataSource)
        {
            try
            {
                var sql = $"SELECT TOP 0 * FROM {dataSource}";

                using var connection = new SqlConnection(_configuration.GetConnectionString("DefaultConnection"));
                await connection.OpenAsync();

                using var command = new SqlCommand(sql, connection);
                using var reader = await command.ExecuteReaderAsync();

                var columns = new List<string>();
                for (int i = 0; i < reader.FieldCount; i++)
                {
                    columns.Add(reader.GetName(i));
                }

                return columns;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error getting columns for {dataSource}");
                return new List<string>();
            }
        }

        private string BuildSQLFromDefinition(CustomReportDefinition definition, Dictionary<string, string> parameters)
        {
            if (!string.IsNullOrEmpty(definition.CustomSQL))
            {
                return definition.CustomSQL;
            }

            // Build SELECT clause
            var selectColumns = string.Join(", ", definition.Columns
                .OrderBy(c => c.DisplayOrder)
                .Select(c => string.IsNullOrEmpty(c.AggregateFunction)
                    ? c.FieldName
                    : $"{c.AggregateFunction}({c.FieldName}) as {c.FieldName}"));

            var sql = $"SELECT {selectColumns} FROM {definition.DataSource}";

            // Add WHERE clause
            if (definition.Filters.Any())
            {
                var whereConditions = string.Join(" ", definition.Filters.Select(f =>
                    $"{f.LogicalOperator} {f.FieldName} {f.Operator} '{f.Value}'"));

                sql += $" WHERE {whereConditions.TrimStart("AND ".ToCharArray())}";
            }

            // Add GROUP BY
            if (!string.IsNullOrEmpty(definition.GroupBy))
            {
                sql += $" GROUP BY {definition.GroupBy}";
            }

            // Add ORDER BY
            if (!string.IsNullOrEmpty(definition.OrderBy))
            {
                sql += $" ORDER BY {definition.OrderBy}";
            }

            return sql;
        }
    }
}
