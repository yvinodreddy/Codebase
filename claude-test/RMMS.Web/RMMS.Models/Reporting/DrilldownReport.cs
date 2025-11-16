using System;
using System.Collections.Generic;

namespace RMMS.Models.Reporting
{
    public class DrilldownLevel
    {
        public int Level { get; set; }
        public string LevelName { get; set; } = string.Empty;
        public string ParentKey { get; set; } = string.Empty;
        public string CurrentKey { get; set; } = string.Empty;
        public Dictionary<string, object> Data { get; set; } = new();
        public List<DrilldownLevel> Children { get; set; } = new();
    }

    public class DrilldownReportDefinition
    {
        public string ReportId { get; set; } = Guid.NewGuid().ToString();
        public string ReportName { get; set; } = string.Empty;
        public string Category { get; set; } = string.Empty; // Sales, Inventory, Production
        public List<string> Hierarchy { get; set; } = new(); // e.g., ["Year", "Month", "Customer", "Product"]
        public DateTime CreatedDate { get; set; } = DateTime.Now;
        public string CreatedBy { get; set; } = string.Empty;
    }

    public class DrilldownNavigationPath
    {
        public List<DrilldownBreadcrumb> Breadcrumbs { get; set; } = new();
        public string CurrentLevel { get; set; } = string.Empty;
        public bool CanDrillDown { get; set; }
        public bool CanDrillUp { get; set; }
    }

    public class DrilldownBreadcrumb
    {
        public string LevelName { get; set; } = string.Empty;
        public string DisplayValue { get; set; } = string.Empty;
        public string FilterKey { get; set; } = string.Empty;
        public string FilterValue { get; set; } = string.Empty;
    }

    public class DrilldownResult
    {
        public string ReportName { get; set; } = string.Empty;
        public DrilldownNavigationPath NavigationPath { get; set; } = new();
        public List<DrilldownDataRow> DataRows { get; set; } = new();
        public Dictionary<string, decimal> Summary { get; set; } = new();
        public string NextLevelHint { get; set; } = string.Empty;
    }

    public class DrilldownDataRow
    {
        public string Key { get; set; } = string.Empty;
        public string DisplayValue { get; set; } = string.Empty;
        public Dictionary<string, object> Metrics { get; set; } = new();
        public bool HasChildren { get; set; }
        public string DrilldownUrl { get; set; } = string.Empty;
    }

    // Alias for view compatibility
    public class DrilldownReport
    {
        public int Id { get; set; }
        public string Name { get; set; } = string.Empty;
        public string Description { get; set; } = string.Empty;
        public string Category { get; set; } = string.Empty;
        public List<string> Hierarchy { get; set; } = new();
        public bool IsActive { get; set; } = true;
        public string CreatedBy { get; set; } = string.Empty;
        public DateTime CreatedDate { get; set; } = DateTime.Now;
        public string? ModifiedBy { get; set; }
        public DateTime? ModifiedDate { get; set; }
    }
}
