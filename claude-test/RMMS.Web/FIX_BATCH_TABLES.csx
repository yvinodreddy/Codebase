#!/usr/bin/env dotnet-script
#r "nuget: Microsoft.Data.SqlClient, 6.1.1"
using Microsoft.Data.SqlClient;

var conn = "Server=172.17.208.1,1433;Database=RMMS_Production;User Id=rmms_user;Password=Welcome01!;TrustServerCertificate=True;Encrypt=False;Connection Timeout=180;";

Console.WriteLine("=== FIXING BATCH TABLES ===\n");

// Fix BatchInputs
try
{
    using var connection = new SqlConnection(conn);
    connection.Open();

    // Get 40 batches without inputs
    var getBatches = new SqlCommand(@"
        SELECT TOP 40 pb.Id
        FROM ProductionBatches pb
        WHERE NOT EXISTS (SELECT 1 FROM BatchInputs WHERE BatchId = pb.Id)
        ORDER BY pb.Id", connection);

    var batches = new List<int>();
    using (var reader = getBatches.ExecuteReader())
    {
        while (reader.Read()) batches.Add(reader.GetInt32(0));
    }

    Console.WriteLine($"Found {batches.Count} batches without inputs");

    int inserted = 0;
    foreach (var batchId in batches)
    {
        var productId = new SqlCommand("SELECT TOP 1 Id FROM Products WHERE ProductType = 'Paddy' ORDER BY NEWID()", connection).ExecuteScalar();
        var warehouseId = new SqlCommand("SELECT TOP 1 Id FROM Warehouses ORDER BY NEWID()", connection).ExecuteScalar();
        var zoneId = new SqlCommand("SELECT TOP 1 Id FROM StorageZones ORDER BY NEWID()", connection).ExecuteScalar();

        var insert = new SqlCommand($@"
            INSERT INTO BatchInputs (BatchId, InputType, ProductId, Quantity, UOM, WarehouseId, ZoneId, MoistureContent, BatchLotNumber, Grade, UnitCost, Remarks, CreatedDate, CreatedBy)
            VALUES (@batchId, 'Paddy', @productId, @quantity, 'Kg', @warehouseId, @zoneId, @moisture, @lot, 'Grade A', 25.0, 'Auto-generated', GETDATE(), 'System')", connection);

        insert.Parameters.AddWithValue("@batchId", batchId);
        insert.Parameters.AddWithValue("@productId", productId);
        insert.Parameters.AddWithValue("@quantity", 500.0 + (inserted * 10));
        insert.Parameters.AddWithValue("@warehouseId", warehouseId);
        insert.Parameters.AddWithValue("@zoneId", zoneId);
        insert.Parameters.AddWithValue("@moisture", 12.0 + (inserted % 5));
        insert.Parameters.AddWithValue("@lot", $"LOT-{(inserted + 1):0000}");

        insert.ExecuteNonQuery();
        inserted++;
    }

    Console.WriteLine($"✅ BatchInputs: {inserted} records inserted");
}
catch (Exception ex)
{
    Console.WriteLine($"❌ BatchInputs: {ex.Message}");
}

// Fix BatchOutputs
try
{
    using var connection = new SqlConnection(conn);
    connection.Open();

    // Get 40 batches without outputs
    var getBatches = new SqlCommand(@"
        SELECT TOP 40 pb.Id
        FROM ProductionBatches pb
        WHERE NOT EXISTS (SELECT 1 FROM BatchOutputs WHERE BatchId = pb.Id)
        ORDER BY pb.Id", connection);

    var batches = new List<int>();
    using (var reader = getBatches.ExecuteReader())
    {
        while (reader.Read()) batches.Add(reader.GetInt32(0));
    }

    Console.WriteLine($"Found {batches.Count} batches without outputs");

    int inserted = 0;
    foreach (var batchId in batches)
    {
        var productId = new SqlCommand("SELECT TOP 1 Id FROM Products WHERE ProductType = 'Rice' ORDER BY NEWID()", connection).ExecuteScalar();
        var warehouseId = new SqlCommand("SELECT TOP 1 Id FROM Warehouses ORDER BY NEWID()", connection).ExecuteScalar();
        var zoneId = new SqlCommand("SELECT TOP 1 Id FROM StorageZones ORDER BY NEWID()", connection).ExecuteScalar();

        var insert = new SqlCommand($@"
            INSERT INTO BatchOutputs (BatchId, OutputType, ProductId, Grade, Quantity, UOM, WarehouseId, ZoneId, QualityScore, MoistureContent, BatchLotNumber, UnitCost, BagsCount, BagsWeight, Remarks, CreatedDate, CreatedBy)
            VALUES (@batchId, 'Rice', @productId, @grade, @quantity, 'Kg', @warehouseId, @zoneId, @quality, @moisture, @lot, 50.0, @bags, 50.0, 'Auto-generated', GETDATE(), 'System')", connection);

        insert.Parameters.AddWithValue("@batchId", batchId);
        insert.Parameters.AddWithValue("@productId", productId);
        insert.Parameters.AddWithValue("@grade", inserted % 2 == 0 ? "Premium" : "Standard");
        insert.Parameters.AddWithValue("@quantity", 350.0 + (inserted * 8));
        insert.Parameters.AddWithValue("@warehouseId", warehouseId);
        insert.Parameters.AddWithValue("@zoneId", zoneId);
        insert.Parameters.AddWithValue("@quality", 85.0 + (inserted % 15));
        insert.Parameters.AddWithValue("@moisture", 10.0 + (inserted % 3));
        insert.Parameters.AddWithValue("@lot", $"OUT-{(inserted + 1):0000}");
        insert.Parameters.AddWithValue("@bags", 7 + (inserted % 3));

        insert.ExecuteNonQuery();
        inserted++;
    }

    Console.WriteLine($"✅ BatchOutputs: {inserted} records inserted");
}
catch (Exception ex)
{
    Console.WriteLine($"❌ BatchOutputs: {ex.Message}");
}

// Final verification
Console.WriteLine("\n=== FINAL VERIFICATION ===");
using (var connection = new SqlConnection(conn))
{
    connection.Open();
    var cmd = new SqlCommand("SELECT COUNT(*) FROM BatchInputs", connection);
    Console.WriteLine($"BatchInputs: {cmd.ExecuteScalar()} records");

    cmd = new SqlCommand("SELECT COUNT(*) FROM BatchOutputs", connection);
    Console.WriteLine($"BatchOutputs: {cmd.ExecuteScalar()} records");
}

Console.WriteLine("\n✅ ALL BATCH TABLES COMPLETE!");
