from google.adk.agent import Agent
from google.adk.runner import InMemoryRunner
from google.adk.types import Content, Part

def search_topic_data(topic: str) -> str:
    """Searches for key information and facts about a given topic.

    Args:
        topic: The subject to gather facts about.
    """
    # Simulated search tool response
    database = {
        "multi-agent systems": (
            "1. Multi-agent systems consist of multiple autonomous agents collaborating.\n"
            "2. Common architectures include Sequential, Router/Delegation, and Hierarchical.\n"
            "3. Key benefits: Task specialization, modular design, and parallel processing."
        ),
        "google adk": (
            "1. Google ADK (Agent Development Kit) is tailored for Gemini models.\n"
            "2. Features native tool definitions from docstrings and type annotations.\n"
            "3. Manages conversational and agent session state via explicit Runners."
        )
    }
    
    key = topic.lower().strip()
    return database.get(key, f"Found general facts for '{topic}': It is an active area of technology research.")


researcher_agent = Agent(
    name="Researcher",
    model="gemini-2.5-flash",
    instructions=(
        "You are an expert technical researcher. Your goal is to gather clear, factual bullet points "
        "on the user's topic using the `search_topic_data` tool. Present raw factual notes concisely."
    ),
    tools=[search_topic_data]
)

# Agent 2: The Editor
editor_agent = Agent(
    name="Editor",
    model="gemini-2.5-flash",
    instructions=(
        "You are a professional technical editor. Take raw notes provided to you and write a polished, "
        "engaging 2-paragraph report with clear headings and executive summary bullet points."
    )
)

async def run_research_workflow(topic: str):
    runner = InMemoryRunner()
    session_id = "research_session_001"
    research_prompt = f"Please research and gather key facts on: {topic}"
    print("[Researcher] Gathering data...")
    research_result = await runner.run_agent(
        agent=researcher_agent,
        session_id=session_id,
        prompt=research_prompt
    )

    raw_notes = research_result.text
    print(f"\n[Researcher Output]:\n{raw_notes}\n" + "\n")
    
    # Step 2: Editor polishes output into a final report
    editor_prompt = f"Please edit and format these raw notes into a final report:\n\n{raw_notes}"
    print("[Editor] Drafting final report...")
    editor_result = await runner.run_agent(
        agent=editor_agent,
        session_id=session_id,
        prompt=editor_prompt
    )

    print(f"\n📰 [Final Published Report]:\n{editor_result.text}")

# Run the async workflow
if __name__ == "__main__":
    asyncio.run(run_research_crew_workflow("Google ADK"))