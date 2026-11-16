"""Optional read-only SQL Server example. Not needed for synthetic demonstration.
Requires: pip install pyodbc; ODBC driver and approved read-only view.
Never commit real credentials or export confidential records to a public repo.
"""
import os
import pyodbc

connection = os.environ.get("WILDFIRE_SQLSERVER_CONNECTION")
if not connection:
    raise SystemExit("Set WILDFIRE_SQLSERVER_CONNECTION to an authorized read-only ODBC connection string.")
with pyodbc.connect(connection, timeout=10) as db:
    rows = db.execute("SELECT TOP (10) OriginID, AvailableCases FROM dbo.vw_PublicDemoApprovedOrigins")
    for row in rows:
        print(row)
