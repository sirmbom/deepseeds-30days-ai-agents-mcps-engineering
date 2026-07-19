import sqlite3
import json
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("SQLite-Database-Server")
DB_FILE = "local_workspace.db"

@mcp.tool()
def execute_sqlite_query(sql_query: str) -> str:
    """
    Executes a read-only SQL query against the local SQLite database.
    Strictly permits only SELECT statements to maintain data safety.
    """

    clean_query = sql_query.strip().upper()
    if not clean_query.startswith("SELECT"):
        return "Error: Security violation. Only read-only SELECT queries are allowed."

    try:
        conn = sqlite3.conect(DB_FILE)
        cursor = conn.cursor()

        cursor.execute(sql_query)
        columns = [description[0] for description in cursor.description]
        rows = cursor.fetchall()

        results = [dict(zip(columns, row)) for row in rows]

        conn.close()
        return json.dumps(results, indent=2)
    except Exception as e:
        return f"Database error: {str(e)}" 
    
if __name__ == "main":
    mcp.run(transport="stdio")