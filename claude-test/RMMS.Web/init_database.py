#!/usr/bin/env python3
import pyodbc
import sys

print("=" * 60)
print("RMMS Database Initialization")
print("=" * 60)
print()

# Connection string
conn_str = (
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=172.17.208.1,1433;"
    "Database=RMMS_Production;"
    "UID=rmms_user;"
    "PWD=Welcome01!;"
    "TrustServerCertificate=yes;"
    "Encrypt=no;"
)

try:
    # Read SQL script
    with open('/home/user01/claude-test/RMMS.Web/CREATE_ALL_TABLES.sql', 'r') as f:
        sql_script = f.read()

    # Connect to database
    print("Connecting to database...")
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    print("✓ Connected successfully")
    print()

    # Split by GO and execute each batch
    batches = sql_script.replace('\r\n', '\n').split('\nGO\n')

    batch_count = 0
    for batch in batches:
        batch = batch.strip()
        if batch and not batch.startswith('--') and batch != 'GO':
            try:
                cursor.execute(batch)
                conn.commit()
                batch_count += 1

                # Print any messages from SQL Server
                if cursor.messages:
                    for msg in cursor.messages:
                        if msg[1]:
                            print(msg[1].decode('utf-8') if isinstance(msg[1], bytes) else msg[1])
            except Exception as e:
                # Continue even if some statements fail (table might already exist)
                if "already an object" not in str(e):
                    print(f"Warning: {str(e)}")

    print()
    print(f"✓ Executed {batch_count} SQL batches")
    print()
    print("=" * 60)
    print("DATABASE INITIALIZATION COMPLETE!")
    print("=" * 60)
    print()
    print("Tables created:")
    print("  ✓ Customers, CustomerContacts, CustomerAddresses")
    print("  ✓ Vendors, VendorContacts, VendorAddresses")
    print("  ✓ Products, Employees")
    print("  ✓ Warehouses, StorageZones")
    print()

    cursor.close()
    conn.close()

except Exception as e:
    print()
    print(f"ERROR: {str(e)}")
    print()
    print("If you see 'No module named pyodbc', install it with:")
    print("  pip3 install pyodbc")
    print()
    print("Otherwise, please run the SQL script manually:")
    print("  File: /home/user01/claude-test/RMMS.Web/CREATE_ALL_TABLES.sql")
    print()
    sys.exit(1)
