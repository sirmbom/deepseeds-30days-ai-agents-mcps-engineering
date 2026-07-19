import sqlite3
import json
from mcp.server.fastmcp import FastMCP

from tavily import TavilyClient

import subprocess, sys, os, tempfile

mcp = FastMCP("Unified-Agent-Core")

DB_FILE = "local_workspace.db"
tavily_client = TavilyClient(api_key=os.environ.get("TAVILY_API_KEY"))

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

@mcp.tool()
def web_search(query: str, search_depth: str = "basic") -> str:
    """
    Search the web to get real-time data or up-to-date facts.
    
    Args:
        query: The explicit search terms or question to look up.
        search_depth: Use 'basic' for quick factual answers, or 'advanced' for deeper research/news.
    """
    
    if not query.strip():
        return "Error: Search query cannot be empty."
    
    try:
        response = tavily_client.search(
            query = query,
            search_depth=search_depth,
            max_results=5,
            include_answer=True
        )

        output = {
            "summary_answer": response.get("answer","No direct summary generated."),
            "results": [
                {
                    "title": result.get("title"),
                    "url": result.get("url"),
                    "snippet": result.get("content")
                }
                for result in response.get("results", [])
            ]
        }

        return json.dumps(output, indent=2)
    except Exception as e:
        return f"Error encountered during search: {str(e)}"

@mcp.tool()
def execute_python_code(code: str, timeout_secs: int  = 5) -> str:
    """
    Executes a string of arbitrary Python 3 code in a restricted local subprocess.
    Returns the combined standard output (stdout) and standard error (stderr).
    
    Args:
        code (str): The complete Python script to execute.
        timeout_seconds (int): Maximum execution time before truncation (default 5s).
    """
    max_timeout = min(max(1, timeout_secs), 30)

    with tempfile.NamedTemporaryFile(suffix=".py", delete=False, mode="w", encoding="utf-8") as temp_file:
        temp_file.write(code)
        temp_file_path = temp_file.name

    try:
        clean_env = {
            "PATH": os.environ.get("PATH", ""),
            "PYTHONPATH": os.environ.get("PYTHONPATH", "")
        }

        result = subprocess.run(
            [sys.executable, temp_file_path],
            capture_output=True,
            text=True,
            timeout=max_timeout,
            env=clean_env
        )

        if result.returncode == 0:
            return f"--- EXECUTION SUCCESSFUL ---\n[Stdout]:\n{result.stdout}"
        else:
            return f"--- EXECUTION FAILED (Exit Code {result.returncode}) ---\n[Stdout]:\n{result.stdout}\n[Stderr]:\n{result.stderr}"
    except subprocess.TimeoutExpired:
        return f"--- EXECUTION TIMEOUT ---\nError: Code execution exceeded the safe limit of {max_timeout} seconds."
    except Exception as e:
        return f"--- RUNTIME ERROR ---\nAn unexpected error occurred while launching the process: {str(e)}"
    
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

if __name__ == "main":
    mcp.run(transport="stdio")