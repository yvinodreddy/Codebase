# RMMS Database Setup Instructions

## Current Situation

The `RMMS_Production` database was dropped but cannot be automatically recreated because the application user (`rmms_user`) does not have CREATE DATABASE permissions on the SQL Server.

## Files Created to Help

1. **CREATE_DATABASE_MANUAL.sql** - SQL script to create the database (requires admin/SA credentials)
2. **CreateDb.csx** - C# script that tries multiple connection methods to create the database
3. This instructions file

## How to Create the Database

### Method 1: Using SQL Server Management Studio (SSMS)

1. Open SQL Server Management Studio
2. Connect to server: `172.17.208.1,1433` with administrator credentials
3. Open the file: `/home/user01/claude-test/RMMS.Web/CREATE_DATABASE_MANUAL.sql`
4. Execute the script (F5)
5. The database will be created and permissions granted to `rmms_user`

### Method 2: Using sqlcmd Command Line

If you have sqlcmd installed with proper credentials:

```bash
sqlcmd -S 172.17.208.1,1433 -U sa -P <YOUR_SA_PASSWORD> -i CREATE_DATABASE_MANUAL.sql
```

### Method 3: Using Docker (if SQL Server is in a container)

```bash
# Find the container ID
docker ps | grep sql

# Execute the script in the container
docker exec -it <container_id> /opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P <SA_PASSWORD> -i /path/to/CREATE_DATABASE_MANUAL.sql
```

### Method 4: Manual Creation via Azure Data Studio or any SQL Client

Connect with admin credentials and run:

```sql
CREATE DATABASE RMMS_Production;
GO

USE RMMS_Production;
GO

CREATE USER [rmms_user] FOR LOGIN [rmms_user];
GO

ALTER ROLE db_owner ADD MEMBER [rmms_user];
GO
```

## After Database is Created

Once the database exists, run these commands to create all tables and schema:

```bash
cd /home/user01/claude-test/RMMS.Web/RMMS.Web
dotnet ef database update
```

This will apply all Entity Framework migrations and create all the necessary tables.

## Then Insert Test Data

After the schema is created, you can insert test data using one of these methods:

### Option A: Use the Seed Controller (via web interface)
1. Start the application: `dotnet run --urls http://localhost:5090`
2. Navigate to: `http://localhost:5090/Seed`
3. Click the "Seed Data" button

### Option B: Run a SQL script directly
I can create a comprehensive SQL INSERT script for you if you prefer this method.

## Errors You Were Experiencing

The following errors will be fixed once the database is properly created and migrations are applied:

1. **InventoryLedger column errors** - The table will be created with all correct columns by EF migrations
2. **/Inventory error page** - Will work once database exists
3. **/StockMovements error page** - Will work once database exists
4. **/StockAdjustments DataTables error** - Will work once data exists
5. **/ProductionBatches DataTables error** - Will work once data exists

## Need More Help?

Please provide:
- The SQL Server SA password, OR
- Access to SQL Server Management Studio screenshot, OR
- Docker container name if SQL is in Docker, OR
- Any other method you used to initially create the database

## Quick Test

To verify the database exists after creation:

```bash
dotnet ef migrations list
```

This should show the migration as "Pending" if database exists but is empty, or "Applied" if it's been migrated.
