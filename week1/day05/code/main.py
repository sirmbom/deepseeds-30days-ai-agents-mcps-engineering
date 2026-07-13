import os
from mcp.server.fastmcp import FastMCP

app = FastMCP("LocalFilesystemServer")

HOME_DIR = os.path.expanduser("~")

@app.tool()
def read_path(given_path: str = "") -> list:
    """Read the contents of a given folder on the pc"""
    target_path = os.path.abspath(os.path.join(HOME_DIR, given_path))

    if os.path.commonpath([HOME_DIR]) != os.path.commonpath([HOME_DIR, target_path]):
        return [f"Access denied to {target_path}"]
    
    try:
        return os.listdir(target_path)
    except FileNotFoundError:
        return [f"Error: Path at {target_path} does not exist"]
    except PermissionError:
        return [f"Permission to access {target_path} denied"]
    except Exception as e:
        return [f"Error: {str(e)}"]

@app.tool()
def read_file(filename: str) -> str:
    """Read the content of a specific text file in the sandvox folder"""
    target_path = os.path.abspath(os.path.join(HOME_DIR, filename))

    if os.path.commonpath([HOME_DIR]) != os.path.commonpath([HOME_DIR, target_path]):
        return "Access denied. Operations out of the sandbox path is forbidden"
    
    try:
        with open(target_path, "r") as fl:
            return fl.read()
    except FileNotFoundError:
        return f"Error: File at {target_path} not found"
    except Exception as e:
        return f"Error: {str(e)}"

@app.tool()
def write_file(filename: str, content: str) -> str:
    """Create or overwrite the content of a text file in a given path"""

    target_path = os.path.abspath(os.path.join(HOME_DIR, filename))

    if os.path.commonpath([HOME_DIR]) != os.path.commonpath([HOME_DIR, target_path]):
        return "Access denied. Operations out of the sandbox path is forbidden"
    
    try:
        os.makedirs(os.path.dirname(target_path), exist_ok=True)

        with open(target_path, "w", encoding="utf-8") as fl:
            fl.write(content)
            fl.close
        return f"Success. File at {target_path} has been modified."
    except Exception as e:
        return f"Error: {str(e)}"

app.run(transport="stdio")









# app = FastMCP("LocalFileServer")

# SAFE_ROOT = os.path.abspath("./sandbox")

# os.makedirs(SAFE_ROOT, exist_ok=True)

# @app.tool()
# def list_directory(relative_path: str = "") -> list:
#     """List the files and folders for a specific directory in the sandbox folder"""
#     target_path = os.path.abspath(os.path.join(SAFE_ROOT, relative_path))

#     if os.path.commonpath(SAFE_ROOT) != os.path.commonpath([SAFE_ROOT,target_path]):
#         return f"Access Denied"
    
#     try:
#         return os.listdir(target_path)
#     except FileNotFoundError:
#         return [f"Error: Path at {target_path} not found"]

# @app.tool()
# def read_file(filename: str) -> str:
#     """Read the content of a specific text file in the sandvox folder"""
#     target_path = os.path.abspath(os.path.join(SAFE_ROOT, filename))

#     if os.path.commonpath([SAFE_ROOT]) != os.path.commonpath([SAFE_ROOT, target_path]):
#         return "Access denied. Operations out of the sandbox path is forbidden"
    
#     try:
#         with open(target_path, "r") as fl:
#             return fl.read()
#     except FileNotFoundError:
#         return f"Error: File at {target_path} not found"

# @app.tool()
# def write_file(filename: str, content: str) -> str:
#     """Create or overwrite the content of a text file in a given path"""

#     target_path = os.path.abspath(os.path.join(SAFE_ROOT, filename))

#     if os.path.commonpath(SAFE_ROOT) != os.path.commonpath([SAFE_ROOT, target_path]):
#         return "Access denied. Operations out of the sandbox path is forbidden"
    
#     try:
#         os.makedirs(os.path.dirname(target_path), exist_ok=True)

#         with open(target_path, "w", encoding="utf-8") as fl:
#             fl.write(content)
#             fl.close
#         return f"Success. File at {target_path} has been modified."
#     except Exception as e:
#         return f"Error writing file: {str(e)}"