#!/usr/bin/env dotnet-script
#r "nuget: Microsoft.Data.SqlClient, 6.1.1"
using Microsoft.Data.SqlClient;

var conn = "Server=172.17.208.1,1433;Database=RMMS_Production;User Id=rmms_user;Password=Welcome01!;TrustServerCertificate=True;Encrypt=False;Connection Timeout=180;";

void Execute(string sql, string description)
{
    try
    {
        using var connection = new SqlConnection(conn);
        connection.Open();
        var command = new SqlCommand(sql, connection);
        command.CommandTimeout = 180;
        var rows = command.ExecuteNonQuery();
        Console.WriteLine($"✅ {description}: {rows} records");
    }
    catch (Exception ex)
    {
        Console.WriteLine($"❌ {description}: {ex.Message}");
    }
}

Console.WriteLine("=== SEEDING LOANS & ADVANCES DATA ===\n");

// Add sample LoansAdvances data
Execute(@"
-- Clear existing data (optional)
DELETE FROM LoansAdvances WHERE Id > 0;

-- Insert 25 sample records with various statuses
DECLARE @counter INT = 1;
WHILE @counter <= 25
BEGIN
    DECLARE @date DATE = DATEADD(DAY, -(@counter * 15), GETDATE());
    DECLARE @amountGiven DECIMAL(18,2) = 5000 + (@counter * 1000);
    DECLARE @repayment DECIMAL(18,2);
    DECLARE @repaymentDate DATE = NULL;
    DECLARE @balance DECIMAL(18,2);

    -- Make some loans fully paid, some partially paid, some unpaid
    IF @counter % 3 = 0
    BEGIN
        -- Fully paid
        SET @repayment = @amountGiven;
        SET @repaymentDate = DATEADD(DAY, 30, @date);
        SET @balance = 0;
    END
    ELSE IF @counter % 3 = 1
    BEGIN
        -- Partially paid
        SET @repayment = @amountGiven * 0.4; -- 40% paid
        SET @repaymentDate = DATEADD(DAY, 20, @date);
        SET @balance = @amountGiven - @repayment;
    END
    ELSE
    BEGIN
        -- Unpaid
        SET @repayment = 0;
        SET @repaymentDate = NULL;
        SET @balance = @amountGiven;
    END

    INSERT INTO LoansAdvances (
        Date,
        VoucherNumber,
        Particulars,
        PartyName,
        AmountGiven,
        Repayment,
        RepaymentDate,
        Balance,
        Remarks,
        CreatedDate,
        IsActive
    )
    VALUES (
        @date,
        'LA-' + CAST(YEAR(@date) AS VARCHAR) + '-' + RIGHT('0000' + CAST(@counter AS VARCHAR), 4),
        CASE (@counter % 5)
            WHEN 0 THEN 'Employee advance for personal emergency'
            WHEN 1 THEN 'Vendor advance payment for paddy procurement'
            WHEN 2 THEN 'Staff salary advance'
            WHEN 3 THEN 'Contractor advance for construction work'
            ELSE 'Supplier advance for raw material purchase'
        END,
        CASE (@counter % 8)
            WHEN 0 THEN 'Ramesh Kumar'
            WHEN 1 THEN 'Priya Sharma'
            WHEN 2 THEN 'Suresh Patel'
            WHEN 3 THEN 'Anjali Singh'
            WHEN 4 THEN 'Vijay Verma'
            WHEN 5 THEN 'Kavita Desai'
            WHEN 6 THEN 'Rajesh Gupta'
            ELSE 'Sunita Reddy'
        END,
        @amountGiven,
        @repayment,
        @repaymentDate,
        @balance,
        CASE
            WHEN @balance = 0 THEN 'Fully repaid on ' + FORMAT(@repaymentDate, 'dd-MMM-yyyy')
            WHEN @repayment > 0 THEN 'Partially repaid, balance pending'
            ELSE 'Pending repayment'
        END,
        GETDATE(),
        1
    );

    SET @counter = @counter + 1;
END
", "LoansAdvances Data");

Console.WriteLine("\n=== DATA SEEDING COMPLETED ===");
