#!/usr/bin/env dotnet-script
#r "nuget: Microsoft.Data.SqlClient, 5.1.1"

using Microsoft.Data.SqlClient;

var connectionString = "Server=172.17.208.1,1433;Database=RMMS_Production;User Id=rmms_user;Password=Welcome01!;TrustServerCertificate=True;Encrypt=False;";

Console.WriteLine("╔════════════════════════════════════════════════════════════════════╗");
Console.WriteLine("║           FIXING REMAINING DATA WITH ACTUAL IDS                    ║");
Console.WriteLine("╚════════════════════════════════════════════════════════════════════╝");
Console.WriteLine();

using (var connection = new SqlConnection(connectionString))
{
    connection.Open();
    Console.WriteLine("✅ Connected to database");
    Console.WriteLine();

    // Get actual ProductionOrder IDs
    Console.WriteLine("📊 Getting actual ProductionOrder IDs...");
    var prodOrderIds = new List<int>();
    using (var cmd = new SqlCommand("SELECT TOP 40 Id FROM ProductionOrders WHERE IsActive = 1 ORDER BY Id", connection))
    using (var reader = cmd.ExecuteReader())
    {
        while (reader.Read()) prodOrderIds.Add(reader.GetInt32(0));
    }
    Console.WriteLine($"   Found {prodOrderIds.Count} ProductionOrder IDs");

    // Insert ProductionBatches with actual IDs
    if (prodOrderIds.Count >= 20)
    {
        Console.WriteLine();
        Console.WriteLine("🔧 Fixing ProductionBatches...");

        for (int i = 0; i < 40 && i < prodOrderIds.Count; i++)
        {
            var orderId = prodOrderIds[i];
            var shift = (i % 2 == 0) ? "Morning" : "Evening";
            var status = i < 20 ? "Completed" : (i < 30 ? "In Progress" : "Scheduled");
            var completion = i < 20 ? 100.00m : (i < 30 ? 50.00m + i : 0.00m);
            var quality = i < 20 ? 90.00m + (i % 6) : (decimal?)null;

            var sql = $@"
                IF NOT EXISTS (SELECT 1 FROM ProductionBatches WHERE BatchNumber = 'BATCH{i+1:00000}')
                INSERT INTO ProductionBatches (
                    BatchNumber, ProductionOrderId, BatchDate, ShiftType, OperatorId, SupervisorId,
                    StartTime, EndTime, Status, CompletionPercent, QualityScore, QualityRemarks,
                    Remarks, Issues, CreatedDate, CreatedBy, IsActive
                ) VALUES (
                    'BATCH{i+1:00000}', {orderId}, DATEADD(DAY, -{40-i}, GETDATE()), '{shift}',
                    {(i % 5) + 6}, {(i % 5) + 6},
                    {(status != "Scheduled" ? $"DATEADD(HOUR, {(shift == "Morning" ? 8 : 16)}, DATEADD(DAY, -{40-i}, GETDATE()))" : "NULL")},
                    {(status == "Completed" ? $"DATEADD(HOUR, {(shift == "Morning" ? 16 : 24)}, DATEADD(DAY, -{40-i}, GETDATE()))" : "NULL")},
                    '{status}', {completion},
                    {(quality.HasValue ? quality.Value.ToString() : "NULL")},
                    {(quality.HasValue && quality >= 95 ? "'Excellent quality'" : (quality.HasValue && quality >= 90 ? "'Good quality'" : "NULL"))},
                    'Auto-generated', NULL, DATEADD(DAY, -{40-i}, GETDATE()), 'System', 1
                )";

            try
            {
                using (var cmd = new SqlCommand(sql, connection))
                {
                    cmd.ExecuteNonQuery();
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"   ⚠️  Batch {i+1}: {ex.Message}");
            }
        }

        using (var cmd = new SqlCommand("SELECT COUNT(*) FROM ProductionBatches WHERE IsActive = 1", connection))
        {
            var count = (int)cmd.ExecuteScalar();
            Console.WriteLine($"   ✅ ProductionBatches: {count} records");
        }
    }

    // Get actual BatchIds for YieldRecords
    Console.WriteLine();
    Console.WriteLine("📊 Getting actual Batch IDs...");
    var batchIds = new List<int>();
    using (var cmd = new SqlCommand("SELECT TOP 40 Id FROM ProductionBatches WHERE Status = 'Completed' ORDER BY Id", connection))
    using (var reader = cmd.ExecuteReader())
    {
        while (reader.Read()) batchIds.Add(reader.GetInt32(0));
    }
    Console.WriteLine($"   Found {batchIds.Count} completed Batch IDs");

    // Insert YieldRecords with actual BatchIds
    if (batchIds.Count > 0)
    {
        Console.WriteLine();
        Console.WriteLine("🔧 Fixing YieldRecords...");

        for (int i = 0; i < 40 && i < batchIds.Count; i++)
        {
            var batchId = batchIds[i];
            var variety = new[] { "Basmati", "Sona Masoori", "IR64", "PR126" }[i % 4];
            var grade = new[] { "A+", "A", "B", "A" }[i % 4];

            var sql = $@"
                IF NOT EXISTS (SELECT 1 FROM YieldRecords WHERE BatchId = {batchId})
                INSERT INTO YieldRecords (
                    BatchId, PaddyVariety, InputPaddyQuantity, OutputHeadRice, OutputBrokenRice,
                    OutputBran, OutputHusk, OutputWastage, HeadRicePercent, BrokenRicePercent,
                    BranPercent, HuskPercent, WastagePercent, TotalYieldPercent, StandardHeadRicePercent,
                    StandardTotalYieldPercent, YieldGrade, QualityScore, MillingRecovery,
                    HeadRiceToBrokenRatio, Remarks, VarianceAnalysis, CalculatedDate, CalculatedBy,
                    IsVerified, VerifiedBy, VerifiedDate
                ) VALUES (
                    {batchId}, '{variety}', 1000.00, 650.00, 100.00, 120.00, 100.00, 30.00,
                    65.00, 10.00, 12.00, 10.00, 3.00, 100.00, 64.00, 98.00, '{grade}',
                    {90.00m + (i % 10)}, 75.00, 6.5, 'Yield analysis completed',
                    'Performance meets standard', DATEADD(DAY, -{40-i}+1, GETDATE()), 'System',
                    1, 'Supervisor', DATEADD(DAY, -{40-i}+2, GETDATE())
                )";

            try
            {
                using (var cmd = new SqlCommand(sql, connection))
                {
                    cmd.ExecuteNonQuery();
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"   ⚠️  Yield {i+1}: {ex.Message}");
            }
        }

        using (var cmd = new SqlCommand("SELECT COUNT(*) FROM YieldRecords WHERE IsVerified = 1", connection))
        {
            var count = (int)cmd.ExecuteScalar();
            Console.WriteLine($"   ✅ YieldRecords: {count} records");
        }
    }

    // Get actual Inquiry IDs
    Console.WriteLine();
    Console.WriteLine("📊 Getting actual Inquiry IDs...");
    var inquiryIds = new List<int>();
    using (var cmd = new SqlCommand("SELECT TOP 40 Id FROM Inquiries WHERE IsActive = 1 AND Status = 'Converted' ORDER BY Id", connection))
    using (var reader = cmd.ExecuteReader())
    {
        while (reader.Read()) inquiryIds.Add(reader.GetInt32(0));
    }
    Console.WriteLine($"   Found {inquiryIds.Count} converted Inquiry IDs");

    // Insert Quotations with actual InquiryIds
    if (inquiryIds.Count > 0)
    {
        Console.WriteLine();
        Console.WriteLine("🔧 Fixing Quotations...");

        for (int i = 0; i < 40 && i < inquiryIds.Count; i++)
        {
            var inquiryId = inquiryIds[i];
            var subtotal = 50000.00m + (i * 1000);
            var discount = (i % 5 == 0) ? subtotal * 0.05m : 0.00m;
            var taxable = subtotal - discount;
            var tax = taxable * 0.18m;
            var total = taxable + tax;
            var status = i < 35 ? "Accepted" : (i < 38 ? "Pending" : "Expired");

            var sql = $@"
                IF NOT EXISTS (SELECT 1 FROM Quotations WHERE QuotationNumber = 'QUO{i+1:00000}')
                BEGIN
                    DECLARE @CustId INT;
                    SELECT @CustId = CustomerId FROM Inquiries WHERE Id = {inquiryId};

                    INSERT INTO Quotations (
                        QuotationNumber, QuotationDate, InquiryId, CustomerId, ValidUntil, PaymentTerms,
                        DeliveryTerms, SubtotalAmount, DiscountPercent, DiscountAmount, TaxAmount,
                        TotalAmount, Status, ApprovedByEmployeeId, ApprovalDate, ConvertedToSalesOrderId,
                        TermsAndConditions, Remarks, CreatedDate, CreatedBy, IsActive
                    ) VALUES (
                        'QUO{i+1:00000}', DATEADD(DAY, -{45-i}, GETDATE()), {inquiryId}, @CustId,
                        DATEADD(DAY, {15-(i%15)}, GETDATE()), 'Net 30 days', 'FOB',
                        {subtotal}, {(i % 5 == 0 ? 5.00m : 0.00m)}, {discount}, {tax}, {total},
                        '{status}', {(i % 5) + 6}, DATEADD(DAY, -{44-i}, GETDATE()),
                        {(status == "Accepted" ? "NULL" : "NULL")},
                        'Standard terms', 'Auto-generated', DATEADD(DAY, -{45-i}, GETDATE()), 'System', 1
                    )
                END";

            try
            {
                using (var cmd = new SqlCommand(sql, connection))
                {
                    cmd.ExecuteNonQuery();
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"   ⚠️  Quotation {i+1}: {ex.Message}");
            }
        }

        using (var cmd = new SqlCommand("SELECT COUNT(*) FROM Quotations WHERE IsActive = 1", connection))
        {
            var count = (int)cmd.ExecuteScalar();
            Console.WriteLine($"   ✅ Quotations: {count} records");
        }
    }

    // Get actual Quotation IDs
    Console.WriteLine();
    Console.WriteLine("📊 Getting actual Quotation IDs...");
    var quotationIds = new List<int>();
    using (var cmd = new SqlCommand("SELECT TOP 40 Id FROM Quotations WHERE IsActive = 1 AND Status = 'Accepted' ORDER BY Id", connection))
    using (var reader = cmd.ExecuteReader())
    {
        while (reader.Read()) quotationIds.Add(reader.GetInt32(0));
    }
    Console.WriteLine($"   Found {quotationIds.Count} accepted Quotation IDs");

    // Insert SalesOrders with actual QuotationIds
    if (quotationIds.Count > 0)
    {
        Console.WriteLine();
        Console.WriteLine("🔧 Fixing SalesOrders...");

        for (int i = 0; i < 40 && i < quotationIds.Count; i++)
        {
            var quotationId = quotationIds[i];
            var status = i < 10 ? "Completed" : (i < 25 ? "Confirmed" : "Pending");
            var priority = (i % 3 == 0) ? "High" : ((i % 3 == 1) ? "Medium" : "Low");
            var stockReserved = (i < 25) ? 1 : 0;

            var sql = $@"
                IF NOT EXISTS (SELECT 1 FROM SalesOrders WHERE OrderNumber = 'SO{i+1:00000}')
                BEGIN
                    DECLARE @QCustId INT, @QSubTotal DECIMAL(18,2), @QDiscount DECIMAL(18,2), @QTax DECIMAL(18,2), @QTotal DECIMAL(18,2);
                    SELECT @QCustId = CustomerId, @QSubTotal = SubtotalAmount, @QDiscount = DiscountAmount,
                           @QTax = TaxAmount, @QTotal = TotalAmount
                    FROM Quotations WHERE Id = {quotationId};

                    INSERT INTO SalesOrders (
                        OrderNumber, OrderDate, CustomerId, QuotationId, DeliveryDate, DeliveryAddress,
                        PaymentTerms, DeliveryTerms, SubtotalAmount, DiscountAmount, TaxAmount,
                        FreightCharges, OtherCharges, TotalAmount, Status, Priority, ApprovedByEmployeeId,
                        ApprovalDate, StockReserved, StockReservedDate, SpecialInstructions, Remarks,
                        CreatedDate, CreatedBy, IsActive
                    ) VALUES (
                        'SO{i+1:00000}', DATEADD(DAY, -{40-i}, GETDATE()), @QCustId, {quotationId},
                        DATEADD(DAY, {20-(i%20)}, GETDATE()), 'Customer Address',
                        'Net 30 days', 'FOB', @QSubTotal, @QDiscount, @QTax, 1000.00, 500.00,
                        @QTotal + 1500.00, '{status}', '{priority}', {(i % 5) + 6},
                        DATEADD(DAY, -{40-i}+1, GETDATE()), {stockReserved},
                        {(stockReserved == 1 ? $"DATEADD(DAY, -{40-i}+2, GETDATE())" : "NULL")},
                        'Handle with care', 'Auto-generated', DATEADD(DAY, -{40-i}, GETDATE()), 'System', 1
                    )
                END";

            try
            {
                using (var cmd = new SqlCommand(sql, connection))
                {
                    cmd.ExecuteNonQuery();
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"   ⚠️  SalesOrder {i+1}: {ex.Message}");
            }
        }

        using (var cmd = new SqlCommand("SELECT COUNT(*) FROM SalesOrders WHERE IsActive = 1", connection))
        {
            var count = (int)cmd.ExecuteScalar();
            Console.WriteLine($"   ✅ SalesOrders: {count} records");
        }
    }

    Console.WriteLine();
    Console.WriteLine("╔════════════════════════════════════════════════════════════════════╗");
    Console.WriteLine("║              ✅ ALL DATA FIXES COMPLETED!                          ║");
    Console.WriteLine("╚════════════════════════════════════════════════════════════════════╝");
}

return 0;
