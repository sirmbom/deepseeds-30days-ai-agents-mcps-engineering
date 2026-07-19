import os
import json
from mcp.server.fastmcp import FastMCP
from tavily import TavilyClient

mcp = FastMCP("Advanced-Search-Server")

tavily_client = TavilyClient(api_key=os.environ.get("TAVILY_API_KEY"))

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
    
if __name__ == "main":
    mcp.run(transport="stdio")
