from google.adk import Agent
from google.adk.runners import InMemoryRunner

def search_database(query: str) -> str:
    """Searches the internal database for user account or system information.
    
    Args:
        query: Search term or SQL-like query string.
    """

    mock_db = {
        "user_123": "User 123: Status=Active, Plan=Enterprise, Region=us-central1",
        "billing": "Pending invoice #9041 for $450.00, Due Date: 2026-08-01",
    }

    for key, val in mock_db.items():
        if key in query.lower():
            return f"Found matching record: {val}"
    return f"No records found in database for query: '{query}'"

def calculate_discount(amount: float, percentage: float) -> str:
    """Calculates the final price after applying a percentage discount.
    
    Args:
        amount: Original price amount.
        percentage: Discount percentage (e.g., 15 for 15%).
    """
    discount = amount * (percentage/100.0)
    final_price = amount - discount
    return f"Original: ${amount:.2f} | Discount ({percentage}%): -${discount:.2f} | Final: ${final_price:.2f}"

def run_adk_session():
    support_agent = Agent(
        name="support_agent",
        model="gemini-2.5-flash",
        instruction=("You are a helpful customer support agent. "
            "Use search_database to locate user records, and calculate_discount when processing billing adjustments."),
            tools=[search_database,calculate_discount]
    )

    runner = InMemoryRunner(agent=support_agent)
    session_id = "user_session_001"

    print("Turn 1: Searching User Record")
    response_1 = runner.run(
        user_message="Can you look up user_123 in the database?",
        session_id=session_id
    )
    print(f"Agent: {response_1.text}\n")

    print("Turn 2: State context retention & tool execution")

    response_2 = runner.run(
        user_message="They have a pending invoice of $450.00. Calculate a 10% discount for them.",
        session_id=session_id
    )
    print(f"Agent: {response_2.text}\n")

if __name__ == "main":
    run_adk_session()