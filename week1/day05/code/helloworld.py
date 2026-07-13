from mcp.server.fastmcp import FastMCP

app = FastMCP("HelloWorldMCP")

# Tool to order cake parfait
@app.tool()
def order_parfait(flavor: str, quantity: int) -> str:
    """Place an order for some cake parfait and how many plates are needed"""
    if not flavor and not quantity:
        return "Add flavor and/or quantity or your user won't eat"
    
    return f"Success! Ordered {quantity} {flavor} pizza for delivery"

# app.run(transport="stdio")


@app.tool()
def calculate_agent_efficiency(tasks_completed: int, hours_spent: float) -> str:
    """Calculate the level of efficiency for an autonomous agent loop"""
    if hours_spent <= 0:
        return "Hours spent must be greater than zero."
    
    efficiency = tasks_completed / hours_spent
    return f"Agent efficiency: {efficiency:.2f} tasks per hour."

app.run(transport="stdio")