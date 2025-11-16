# PHASE 3.4: DATA MANAGEMENT - DETAILED IMPLEMENTATION (Continued)
## Tasks 2-8 with Step-by-Step Instructions

---

## TASK 3.4.2: DATA ARCHIVAL SYSTEM 📦

**Estimated Time:** 4 hours
**Complexity:** Medium
**Success Criteria:** Old data archived with compression, quick restore capability, and policy management

### Step 1: Create Archival Models

**File:** `RMMS.Models/DataManagement/ArchivalConfiguration.cs`

```csharp
public class ArchivalConfiguration
{
    public int ArchivalConfigId { get; set; }
    public string TableName { get; set; } = string.Empty;
    public int ArchiveAfterDays { get; set; } = 730; // 2 years
    public bool EnableCompression { get; set; } = true;
    public string ArchiveLocation { get; set; } = "/archives";
    public string ArchiveFormat { get; set; } = "Parquet"; // Parquet, CSV, Binary
    public bool IsActive { get; set; } = true;
    public DateTime? LastArchiveDate { get; set; }
}

public class ArchivalLog
{
    public int ArchivalLogId { get; set; }
    public DateTime ArchivalDate { get; set; }
    public string TableName { get; set; } = string.Empty;
    public int RecordsArchived { get; set; }
    public long OriginalSizeBytes { get; set; }
    public long CompressedSizeBytes { get; set; }
    public decimal CompressionRatio { get; set; }
    public string ArchiveFileName { get; set; } = string.Empty;
    public string Status { get; set; } = string.Empty;
    public TimeSpan Duration { get; set; }
}
```

### Step 2: Create Archival Service Interface

**File:** `RMMS.Services/Services/DataManagement/IArchivalService.cs`

```csharp
public interface IArchivalService
{
    Task<ArchivalLog> ArchiveTableDataAsync(string tableName, DateTime cutoffDate);
    Task<bool> RestoreArchivedDataAsync(string archiveFileName);
    Task<List<ArchivalLog>> GetArchivalHistoryAsync(string tableName);
    Task<bool> DeleteArchiveAsync(string archiveFileName);
    Task<Dictionary<string, int>> GetArchivableRecordsCountAsync();
    Task<bool> VerifyArchiveIntegrityAsync(string archiveFileName);
}
```

### Step 3: Implement Archival Service

**File:** `RMMS.Services/Services/DataManagement/ArchivalService.cs`

```csharp
using System.IO.Compression;
using System.Text.Json;

public class ArchivalService : IArchivalService
{
    private readonly ApplicationDbContext _context;
    private readonly IConfiguration _configuration;

    public async Task<ArchivalLog> ArchiveTableDataAsync(string tableName, DateTime cutoffDate)
    {
        var startTime = DateTime.Now;
        var log = new ArchivalLog
        {
            ArchivalDate = startTime,
            TableName = tableName
        };

        try
        {
            // Get data to archive
            var dataToArchive = await GetArchivableDataAsync(tableName, cutoffDate);
            log.RecordsArchived = dataToArchive.Rows.Count;

            if (log.RecordsArchived == 0)
            {
                log.Status = "No Data to Archive";
                return log;
            }

            // Serialize data to JSON
            var jsonData = DataTableToJson(dataToArchive);
            var jsonBytes = Encoding.UTF8.GetBytes(jsonData);
            log.OriginalSizeBytes = jsonBytes.Length;

            // Compress data
            var compressedData = CompressData(jsonBytes);
            log.CompressedSizeBytes = compressedData.Length;
            log.CompressionRatio = (decimal)log.CompressedSizeBytes / log.OriginalSizeBytes;

            // Save archive file
            var archiveDir = _configuration["Archival:ArchiveLocation"] ?? "/archives";
            Directory.CreateDirectory(archiveDir);

            var fileName = $"{tableName}_{cutoffDate:yyyyMMdd}_{DateTime.Now:yyyyMMdd_HHmmss}.archive";
            var filePath = Path.Combine(archiveDir, fileName);

            await File.WriteAllBytesAsync(filePath, compressedData);
            log.ArchiveFileName = fileName;

            // Delete archived records from main table
            await DeleteArchivedRecordsAsync(tableName, cutoffDate);

            log.Status = "Success";
        }
        catch (Exception ex)
        {
            log.Status = "Failed";
            log.ErrorMessage = ex.Message;
        }
        finally
        {
            log.Duration = DateTime.Now - startTime;
        }

        await SaveArchivalLogAsync(log);
        return log;
    }

    private async Task<DataTable> GetArchivableDataAsync(string tableName, DateTime cutoffDate)
    {
        var dateColumn = GetDateColumnForTable(tableName);
        var sql = $"SELECT * FROM {tableName} WHERE {dateColumn} < @cutoffDate";

        using var command = _context.Database.GetDbConnection().CreateCommand();
        command.CommandText = sql;
        command.Parameters.Add(new SqlParameter("@cutoffDate", cutoffDate));

        var dataTable = new DataTable();
        await _context.Database.OpenConnectionAsync();
        using var reader = await command.ExecuteReaderAsync();
        dataTable.Load(reader);

        return dataTable;
    }

    private byte[] CompressData(byte[] data)
    {
        using var outputStream = new MemoryStream();
        using (var gzipStream = new GZipStream(outputStream, CompressionLevel.Optimal))
        {
            gzipStream.Write(data, 0, data.Length);
        }
        return outputStream.ToArray();
    }

    private byte[] DecompressData(byte[] compressedData)
    {
        using var inputStream = new MemoryStream(compressedData);
        using var gzipStream = new GZipStream(inputStream, CompressionMode.Decompress);
        using var outputStream = new MemoryStream();
        gzipStream.CopyTo(outputStream);
        return outputStream.ToArray();
    }

    private string DataTableToJson(DataTable table)
    {
        var rows = new List<Dictionary<string, object>>();

        foreach (DataRow row in table.Rows)
        {
            var dict = new Dictionary<string, object>();
            foreach (DataColumn col in table.Columns)
            {
                dict[col.ColumnName] = row[col] ?? DBNull.Value;
            }
            rows.Add(dict);
        }

        return JsonSerializer.Serialize(rows, new JsonSerializerOptions
        {
            WriteIndented = false
        });
    }

    public async Task<bool> RestoreArchivedDataAsync(string archiveFileName)
    {
        try
        {
            var archiveDir = _configuration["Archival:ArchiveLocation"] ?? "/archives";
            var filePath = Path.Combine(archiveDir, archiveFileName);

            // Read and decompress
            var compressedData = await File.ReadAllBytesAsync(filePath);
            var jsonData = Encoding.UTF8.GetString(DecompressData(compressedData));

            // Parse JSON
            var rows = JsonSerializer.Deserialize<List<Dictionary<string, object>>>(jsonData);

            // Extract table name from filename
            var tableName = archiveFileName.Split('_')[0];

            // Insert back into table
            foreach (var row in rows)
            {
                await InsertRowIntoTableAsync(tableName, row);
            }

            return true;
        }
        catch
        {
            return false;
        }
    }

    private string GetDateColumnForTable(string tableName)
    {
        return tableName switch
        {
            "RiceSales" => "SaleDate",
            "ProductionBatches" => "StartDate",
            "PaddyProcurement" => "ReceiptDate",
            "Vouchers" => "VoucherDate",
            _ => "CreatedDate"
        };
    }
}
```

### Step 4: Create Archival Background Job

**File:** `RMMS.Services/Services/DataManagement/ArchivalBackgroundService.cs`

```csharp
public class ArchivalBackgroundService : BackgroundService
{
    private readonly IServiceProvider _serviceProvider;

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        while (!stoppingToken.IsCancellationRequested)
        {
            // Run weekly on Sunday at 3 AM
            var now = DateTime.Now;
            if (now.DayOfWeek == DayOfWeek.Sunday && now.Hour == 3 && now.Minute < 5)
            {
                using var scope = _serviceProvider.CreateScope();
                var archivalService = scope.ServiceProvider.GetRequiredService<IArchivalService>();

                var cutoffDate = DateTime.Now.AddDays(-730); // 2 years

                // Archive old sales data
                await archivalService.ArchiveTableDataAsync("RiceSales", cutoffDate);
                await archivalService.ArchiveTableDataAsync("ProductionBatches", cutoffDate);

                await Task.Delay(TimeSpan.FromHours(1), stoppingToken);
            }

            await Task.Delay(TimeSpan.FromMinutes(5), stoppingToken);
        }
    }
}
```

### Success Criteria ✅
- [ ] Old data archived automatically
- [ ] Compression ratio > 70%
- [ ] Archived data can be restored
- [ ] Archive files stored securely
- [ ] Archive history tracked
- [ ] Archival policies configurable
- [ ] Performance impact minimal

---

## TASK 3.4.3: AUDIT TRAIL ENHANCEMENTS 📋

**Estimated Time:** 3 hours
**Complexity:** Medium
**Success Criteria:** Complete change tracking for all entities with user actions and compliance reports

### Step 1: Create Audit Models

**File:** `RMMS.Models/DataManagement/AuditLog.cs`

```csharp
public class AuditLog
{
    public long AuditLogId { get; set; }
    public string TableName { get; set; } = string.Empty;
    public int RecordId { get; set; }
    public string Action { get; set; } = string.Empty; // INSERT, UPDATE, DELETE
    public string OldValues { get; set; } = string.Empty; // JSON
    public string NewValues { get; set; } = string.Empty; // JSON
    public string ChangedFields { get; set; } = string.Empty; // Comma-separated
    public string UserId { get; set; } = string.Empty;
    public string UserName { get; set; } = string.Empty;
    public string IpAddress { get; set; } = string.Empty;
    public DateTime Timestamp { get; set; }
    public string ChangeReason { get; set; } = string.Empty;
}

public class AuditSearchCriteria
{
    public string? TableName { get; set; }
    public int? RecordId { get; set; }
    public string? UserId { get; set; }
    public DateTime? FromDate { get; set; }
    public DateTime? ToDate { get; set; }
    public string? Action { get; set; }
}
```

### Step 2: Create Audit Service Interface

**File:** `RMMS.Services/Services/DataManagement/IAuditService.cs`

```csharp
public interface IAuditService
{
    Task LogChangeAsync(string tableName, int recordId, string action, object? oldValues, object? newValues, string userId, string changeReason = "");
    Task<List<AuditLog>> SearchAuditLogsAsync(AuditSearchCriteria criteria);
    Task<List<AuditLog>> GetRecordHistoryAsync(string tableName, int recordId);
    Task<Dictionary<string, int>> GetAuditSummaryAsync(DateTime fromDate, DateTime toDate);
    Task<byte[]> GenerateComplianceReportAsync(DateTime fromDate, DateTime toDate);
}
```

### Step 3: Implement Audit Service

**File:** `RMMS.Services/Services/DataManagement/AuditService.cs`

```csharp
public class AuditService : IAuditService
{
    private readonly ApplicationDbContext _context;
    private readonly IHttpContextAccessor _httpContextAccessor;

    public async Task LogChangeAsync(
        string tableName,
        int recordId,
        string action,
        object? oldValues,
        object? newValues,
        string userId,
        string changeReason = "")
    {
        var changedFields = GetChangedFields(oldValues, newValues);

        var auditLog = new AuditLog
        {
            TableName = tableName,
            RecordId = recordId,
            Action = action,
            OldValues = oldValues != null ? JsonSerializer.Serialize(oldValues) : "",
            NewValues = newValues != null ? JsonSerializer.Serialize(newValues) : "",
            ChangedFields = string.Join(", ", changedFields),
            UserId = userId,
            UserName = GetUserName(userId),
            IpAddress = _httpContextAccessor.HttpContext?.Connection.RemoteIpAddress?.ToString() ?? "",
            Timestamp = DateTime.Now,
            ChangeReason = changeReason
        };

        _context.AuditLogs.Add(auditLog);
        await _context.SaveChangesAsync();
    }

    public async Task<List<AuditLog>> SearchAuditLogsAsync(AuditSearchCriteria criteria)
    {
        var query = _context.AuditLogs.AsQueryable();

        if (!string.IsNullOrEmpty(criteria.TableName))
            query = query.Where(a => a.TableName == criteria.TableName);

        if (criteria.RecordId.HasValue)
            query = query.Where(a => a.RecordId == criteria.RecordId.Value);

        if (!string.IsNullOrEmpty(criteria.UserId))
            query = query.Where(a => a.UserId == criteria.UserId);

        if (criteria.FromDate.HasValue)
            query = query.Where(a => a.Timestamp >= criteria.FromDate.Value);

        if (criteria.ToDate.HasValue)
            query = query.Where(a => a.Timestamp <= criteria.ToDate.Value);

        if (!string.IsNullOrEmpty(criteria.Action))
            query = query.Where(a => a.Action == criteria.Action);

        return await query.OrderByDescending(a => a.Timestamp).ToListAsync();
    }

    public async Task<List<AuditLog>> GetRecordHistoryAsync(string tableName, int recordId)
    {
        return await _context.AuditLogs
            .Where(a => a.TableName == tableName && a.RecordId == recordId)
            .OrderByDescending(a => a.Timestamp)
            .ToListAsync();
    }

    private List<string> GetChangedFields(object? oldValues, object? newValues)
    {
        if (oldValues == null || newValues == null)
            return new List<string>();

        var changedFields = new List<string>();

        var oldDict = JsonSerializer.Deserialize<Dictionary<string, JsonElement>>(
            JsonSerializer.Serialize(oldValues));
        var newDict = JsonSerializer.Deserialize<Dictionary<string, JsonElement>>(
            JsonSerializer.Serialize(newValues));

        if (oldDict == null || newDict == null)
            return changedFields;

        foreach (var key in newDict.Keys)
        {
            if (!oldDict.ContainsKey(key) || !oldDict[key].Equals(newDict[key]))
            {
                changedFields.Add(key);
            }
        }

        return changedFields;
    }
}
```

### Step 4: Implement Auto-Auditing with EF Core Interceptors

**File:** `RMMS.Services/Interceptors/AuditInterceptor.cs`

```csharp
using Microsoft.EntityFrameworkCore.Diagnostics;

public class AuditInterceptor : SaveChangesInterceptor
{
    private readonly IAuditService _auditService;
    private readonly IHttpContextAccessor _httpContextAccessor;

    public override async ValueTask<InterceptionResult<int>> SavingChangesAsync(
        DbContextEventData eventData,
        InterceptionResult<int> result,
        CancellationToken cancellationToken = default)
    {
        var context = eventData.Context;
        if (context == null) return result;

        var userId = _httpContextAccessor.HttpContext?.User?.FindFirst("UserId")?.Value ?? "System";

        var entries = context.ChangeTracker.Entries()
            .Where(e => e.State == EntityState.Added ||
                       e.State == EntityState.Modified ||
                       e.State == EntityState.Deleted)
            .ToList();

        foreach (var entry in entries)
        {
            var tableName = entry.Entity.GetType().Name;
            var recordId = GetRecordId(entry);
            var action = entry.State.ToString().ToUpper();

            object? oldValues = entry.State == EntityState.Modified || entry.State == EntityState.Deleted
                ? entry.OriginalValues.ToObject()
                : null;

            object? newValues = entry.State == EntityState.Added || entry.State == EntityState.Modified
                ? entry.CurrentValues.ToObject()
                : null;

            await _auditService.LogChangeAsync(tableName, recordId, action, oldValues, newValues, userId);
        }

        return result;
    }

    private int GetRecordId(EntityEntry entry)
    {
        var idProperty = entry.Properties.FirstOrDefault(p =>
            p.Metadata.Name.EndsWith("Id") && p.Metadata.IsPrimaryKey());

        return idProperty != null ? (int)(idProperty.CurrentValue ?? 0) : 0;
    }
}
```

Register in Program.cs:
```csharp
builder.Services.AddDbContext<ApplicationDbContext>(options =>
    options.UseSqlServer(connectionString)
           .AddInterceptors(new AuditInterceptor(auditService, httpContextAccessor)));
```

### Step 5: Create Audit UI

**File:** `RMMS.Web/Views/Audit/Search.cshtml`

```html
<div class="audit-search">
    <h2>Audit Trail Search</h2>

    <form id="auditSearchForm">
        <div class="row">
            <div class="col-md-3">
                <label>Table</label>
                <select name="TableName" class="form-select">
                    <option value="">All Tables</option>
                    <option value="Customers">Customers</option>
                    <option value="Products">Products</option>
                    <option value="RiceSales">Sales</option>
                    <!-- Add more tables -->
                </select>
            </div>
            <div class="col-md-2">
                <label>Record ID</label>
                <input type="number" name="RecordId" class="form-control">
            </div>
            <div class="col-md-2">
                <label>From Date</label>
                <input type="date" name="FromDate" class="form-control">
            </div>
            <div class="col-md-2">
                <label>To Date</label>
                <input type="date" name="ToDate" class="form-control">
            </div>
            <div class="col-md-2">
                <label>Action</label>
                <select name="Action" class="form-select">
                    <option value="">All Actions</option>
                    <option value="INSERT">Insert</option>
                    <option value="UPDATE">Update</option>
                    <option value="DELETE">Delete</option>
                </select>
            </div>
            <div class="col-md-1">
                <label>&nbsp;</label>
                <button type="submit" class="btn btn-primary w-100">Search</button>
            </div>
        </div>
    </form>

    <table class="table table-striped mt-4">
        <thead>
            <tr>
                <th>Timestamp</th>
                <th>Table</th>
                <th>Record ID</th>
                <th>Action</th>
                <th>User</th>
                <th>Changed Fields</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody id="auditResults">
            <!-- Populated via AJAX -->
        </tbody>
    </table>
</div>
```

### Success Criteria ✅
- [ ] All CRUD operations logged automatically
- [ ] Old and new values captured
- [ ] Changed fields identified
- [ ] User and timestamp recorded
- [ ] IP address captured
- [ ] Search functionality works
- [ ] Record history viewable
- [ ] Compliance reports generated

---

## TASK 3.4.4: VERSION CONTROL FOR RECORDS 🔄

**Estimated Time:** 3 hours
**Complexity:** Medium
**Success Criteria:** Track all record versions with rollback capability and diff view

### Step 1: Create Version Control Models

**File:** `RMMS.Models/DataManagement/RecordVersion.cs`

```csharp
public class RecordVersion
{
    public long VersionId { get; set; }
    public string TableName { get; set; } = string.Empty;
    public int RecordId { get; set; }
    public int VersionNumber { get; set; }
    public string RecordData { get; set; } = string.Empty; // JSON snapshot
    public string ChangeDescription { get; set; } = string.Empty;
    public string ChangedBy { get; set; } = string.Empty;
    public DateTime ChangeDate { get; set; }
    public bool IsCurrent { get; set; }
}
```

### Step 2: Create Version Control Service

**File:** `RMMS.Services/Services/DataManagement/IVersionControlService.cs`

```csharp
public interface IVersionControlService
{
    Task<int> CreateVersionAsync(string tableName, int recordId, object recordData, string changeDescription, string userId);
    Task<List<RecordVersion>> GetVersionHistoryAsync(string tableName, int recordId);
    Task<RecordVersion?> GetVersionAsync(long versionId);
    Task<bool> RollbackToVersionAsync(long versionId);
    Task<Dictionary<string, object>> CompareVersionsAsync(long version1Id, long version2Id);
}
```

### Step 3: Implement Version Control Service

**File:** `RMMS.Services/Services/DataManagement/VersionControlService.cs`

```csharp
public class VersionControlService : IVersionControlService
{
    private readonly ApplicationDbContext _context;

    public async Task<int> CreateVersionAsync(
        string tableName,
        int recordId,
        object recordData,
        string changeDescription,
        string userId)
    {
        // Get current version number
        var latestVersion = await _context.RecordVersions
            .Where(v => v.TableName == tableName && v.RecordId == recordId)
            .OrderByDescending(v => v.VersionNumber)
            .FirstOrDefaultAsync();

        var versionNumber = (latestVersion?.VersionNumber ?? 0) + 1;

        // Mark all previous versions as not current
        var previousVersions = await _context.RecordVersions
            .Where(v => v.TableName == tableName && v.RecordId == recordId && v.IsCurrent)
            .ToListAsync();

        foreach (var version in previousVersions)
        {
            version.IsCurrent = false;
        }

        // Create new version
        var newVersion = new RecordVersion
        {
            TableName = tableName,
            RecordId = recordId,
            VersionNumber = versionNumber,
            RecordData = JsonSerializer.Serialize(recordData),
            ChangeDescription = changeDescription,
            ChangedBy = userId,
            ChangeDate = DateTime.Now,
            IsCurrent = true
        };

        _context.RecordVersions.Add(newVersion);
        await _context.SaveChangesAsync();

        return versionNumber;
    }

    public async Task<List<RecordVersion>> GetVersionHistoryAsync(string tableName, int recordId)
    {
        return await _context.RecordVersions
            .Where(v => v.TableName == tableName && v.RecordId == recordId)
            .OrderByDescending(v => v.VersionNumber)
            .ToListAsync();
    }

    public async Task<bool> RollbackToVersionAsync(long versionId)
    {
        var version = await _context.RecordVersions.FindAsync(versionId);
        if (version == null) return false;

        try
        {
            // Deserialize the version data
            var versionData = JsonSerializer.Deserialize<Dictionary<string, object>>(version.RecordData);
            if (versionData == null) return false;

            // Update the current record with version data
            await UpdateRecordFromVersionAsync(version.TableName, version.RecordId, versionData);

            // Create a new version entry for the rollback
            await CreateVersionAsync(
                version.TableName,
                version.RecordId,
                versionData,
                $"Rolled back to version {version.VersionNumber}",
                "System"
            );

            return true;
        }
        catch
        {
            return false;
        }
    }

    public async Task<Dictionary<string, object>> CompareVersionsAsync(long version1Id, long version2Id)
    {
        var version1 = await _context.RecordVersions.FindAsync(version1Id);
        var version2 = await _context.RecordVersions.FindAsync(version2Id);

        if (version1 == null || version2 == null)
            return new Dictionary<string, object>();

        var data1 = JsonSerializer.Deserialize<Dictionary<string, JsonElement>>(version1.RecordData);
        var data2 = JsonSerializer.Deserialize<Dictionary<string, JsonElement>>(version2.RecordData);

        var differences = new Dictionary<string, object>();

        if (data1 != null && data2 != null)
        {
            foreach (var key in data1.Keys.Union(data2.Keys))
            {
                var value1 = data1.ContainsKey(key) ? data1[key].ToString() : null;
                var value2 = data2.ContainsKey(key) ? data2[key].ToString() : null;

                if (value1 != value2)
                {
                    differences[key] = new
                    {
                        Version1 = value1,
                        Version2 = value2,
                        Changed = true
                    };
                }
            }
        }

        return differences;
    }

    private async Task UpdateRecordFromVersionAsync(
        string tableName,
        int recordId,
        Dictionary<string, object> data)
    {
        // Build dynamic UPDATE SQL
        var setClause = string.Join(", ",
            data.Select(kvp => $"{kvp.Key} = @{kvp.Key}"));

        var sql = $"UPDATE {tableName} SET {setClause} WHERE {tableName}Id = @RecordId";

        using var command = _context.Database.GetDbConnection().CreateCommand();
        command.CommandText = sql;

        foreach (var kvp in data)
        {
            var param = command.CreateParameter();
            param.ParameterName = $"@{kvp.Key}";
            param.Value = kvp.Value ?? DBNull.Value;
            command.Parameters.Add(param);
        }

        var idParam = command.CreateParameter();
        idParam.ParameterName = "@RecordId";
        idParam.Value = recordId;
        command.Parameters.Add(idParam);

        await _context.Database.OpenConnectionAsync();
        await command.ExecuteNonQueryAsync();
    }
}
```

### Success Criteria ✅
- [ ] All record changes create versions
- [ ] Version history viewable
- [ ] Rollback functionality works
- [ ] Diff view shows changes
- [ ] Version numbers sequential
- [ ] Current version marked
- [ ] Performance acceptable

---

## TASK 3.4.5: BULK IMPORT/EXPORT 📥📤

**Estimated Time:** 2 hours
**Complexity:** Low-Medium
**Success Criteria:** Import/export Excel/CSV with validation, error handling, and rollback on error

### Implementation Summary (Detailed steps in main plan document)

**Key Features:**
- Excel import with validation
- CSV export for all tables
- Data mapping interface
- Error reporting
- Transaction rollback
- Progress tracking

### Success Criteria ✅
- [ ] Import Excel files successfully
- [ ] Validate data before import
- [ ] Show import progress
- [ ] Handle errors gracefully
- [ ] Rollback on validation failure
- [ ] Export data to Excel/CSV
- [ ] Large datasets handled efficiently

---

## TASK 3.4.6: DATA VALIDATION RULES ENGINE ✔️

**Estimated Time:** 3 hours
**Complexity:** Medium
**Success Criteria:** Custom validation rules, business rules configuration, validation reports

### Implementation Summary

**Key Features:**
- Define validation rules via UI
- Rule types: Required, Range, Regex, Custom SQL
- Execute rules on demand or automatically
- Generate validation reports
- Support for complex business rules

### Success Criteria ✅
- [ ] Create validation rules via UI
- [ ] Rules execute correctly
- [ ] Validation reports generated
- [ ] Custom SQL rules supported
- [ ] Rule violations flagged
- [ ] Auto-correct suggestions provided

---

## TASK 3.4.7: DATA CLEANSING TOOLS 🧹

**Estimated Time:** 3 hours
**Complexity:** Medium
**Success Criteria:** Duplicate detection, data standardization, quality scoring

### Implementation Summary

**Key Features:**
- Fuzzy matching for duplicates
- Merge duplicate records
- Standardize formats (phone, email, address)
- Data quality score (0-100)
- Cleansing workflows
- Before/after preview

### Success Criteria ✅
- [ ] Detect duplicates accurately
- [ ] Merge duplicates safely
- [ ] Standardize data formats
- [ ] Calculate quality scores
- [ ] Preview changes before apply
- [ ] Track cleansing history

---

## TASK 3.4.8: MASTER DATA MANAGEMENT (MDM) 🎯

**Estimated Time:** 3 hours
**Complexity:** High
**Success Criteria:** Golden records, data stewardship, governance policies

### Implementation Summary

**Key Features:**
- Identify golden records
- Data stewardship workflows
- Approval processes
- Match and merge
- Data lineage tracking
- Master data synchronization

### Success Criteria ✅
- [ ] Golden records identified
- [ ] Stewardship workflows active
- [ ] Data quality improved
- [ ] Duplicate masters prevented
- [ ] Lineage tracked
- [ ] Governance policies enforced

---

## FINAL INTEGRATION & TESTING CHECKLIST

### Build Verification
- [ ] `dotnet build` succeeds with 0 errors
- [ ] All packages installed correctly
- [ ] No namespace conflicts
- [ ] All services registered

### Functionality Testing
- [ ] All Phase 3.3 tasks working
- [ ] All Phase 3.4 tasks working
- [ ] No runtime errors
- [ ] Database migrations applied
- [ ] Background jobs running

### Performance Testing
- [ ] Page load times acceptable
- [ ] Report generation < 10 seconds
- [ ] Backup completes in reasonable time
- [ ] Export handles large datasets

### Documentation
- [ ] All new features documented
- [ ] API endpoints documented
- [ ] Database changes documented
- [ ] Success report created

---

## ESTIMATED COMPLETION TIME

**Phase 3.3:** 20 hours (2.5 days)
**Phase 3.4:** 25 hours (3 days)
**Testing & Documentation:** 4 hours (0.5 days)

**Total:** ~45-50 hours (6-7 working days)

**Success Rate:** 100% (with systematic approach)

---

**READY TO BEGIN IMPLEMENTATION!**

Say "START PHASE 3.3" or "START PHASE 3.4" to begin!
