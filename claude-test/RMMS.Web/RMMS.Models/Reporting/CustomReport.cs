using System;
using System.Collections.Generic;

namespace RMMS.Models.Reporting
{
    public class CustomReportDefinition
    {
        public int Id { get; set; }
        public string Name { get; set; } = string.Empty;
        public string ReportName { get; set; } = string.Empty;
        public string Description { get; set; } = string.Empty;
        public string Category { get; set; } = string.Empty;
        public string DataSource { get; set; } = string.Empty; // Table or View name
        public string SelectedColumns { get; set; } = string.Empty; // Comma-separated list
        public string FilterDefinition { get; set; } = string.Empty; // JSON
        public string GroupByColumns { get; set; } = string.Empty; // Comma-separated list
        public string SortColumns { get; set; } = string.Empty; // Comma-separated list
        public string Aggregations { get; set; } = string.Empty; // JSON
        public string OutputType { get; set; } = "Table";
        public List<ReportColumn> Columns { get; set; } = new();
        public List<ReportFilter> Filters { get; set; } = new();
        public string GroupBy { get; set; } = string.Empty;
        public string OrderBy { get; set; } = string.Empty;
        public string CustomSQL { get; set; } = string.Empty;
        public bool IsPublic { get; set; }
        public bool IsActive { get; set; } = true;
        public string CreatedBy { get; set; } = string.Empty;
        public DateTime CreatedDate { get; set; } = DateTime.Now;
        public string? ModifiedBy { get; set; }
        public DateTime? ModifiedDate { get; set; }
    }

    public class ReportColumn
    {
        public string FieldName { get; set; } = string.Empty;
        public string DisplayName { get; set; } = string.Empty;
        public string DataType { get; set; } = "String";
        public string AggregateFunction { get; set; } = ""; // SUM, AVG, COUNT, etc.
        public bool IsVisible { get; set; } = true;
        public int DisplayOrder { get; set; }
        public string Format { get; set; } = string.Empty;
    }

    public class ReportFilter
    {
        public string FieldName { get; set; } = string.Empty;
        public string Operator { get; set; } = "="; // =, >, <, LIKE, IN, etc.
        public string Value { get; set; } = string.Empty;
        public string LogicalOperator { get; set; } = "AND"; // AND, OR
    }

    public class CustomReportResult
    {
        public string ReportName { get; set; } = string.Empty;
        public List<Dictionary<string, object>> Data { get; set; } = new();
        public int TotalRecords { get; set; }
        public DateTime GeneratedDate { get; set; } = DateTime.Now;
    }
}
