import subprocess
import sys
import os
import tempfile
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Sandboxed-Code-Execution-Server")

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