from typing import List, Optional, Dict, Literal
from pydantic import BaseModel, Field
from typing_extensions import TypedDict
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END

# Definition of Schemas

class Task(BaseModel):
    id: int = Field(description="The unique sequential ID of the task, starting at 1.")
    name: str = Field(description="The precise description or action of the step.")
    completed: bool = Field(default=False, description="Whether this task has been executed.")
    response: Optional[str] = Field(default=None, description="The output result from running this task.")

class Plan(BaseModel):
    tasks: List[Task] = Field(description="The chronological list of steps to fulfill the user request.")

class AgentState(TypedDict):
    user_message: str
    plan: List[Task]
    current_step_index: int
    final_response: Optional[str]

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
structured_planner = llm.with_structured_output(Plan)

def planner_node(state: AgentState) -> dict:
    """
    Receives the user request, triggers the structured LLM, 
    and populates the plan list in our LangGraph state.
    """
    system_prompt = (
        "You are the Macro-Planner for an advanced Plan-and-Execute AI Agent.\n"
        "Your job is to break down a complex, multi-step user request into a strict sequence "
        "of individual, chronological tasks.\n\n"
        "CRITICAL RULES:\n"
        "1. Break down the request into discrete, atomic operations.\n"
        "2. Ensure chronological ordering—tasks that depend on info from prior steps must come later.\n"
        "3. Set 'completed' to False for all tasks initially."
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": state["user_message"]}
    ]

    generated_plan: Plan = structured_planner.invoke(messages)

    return {
        "plan": generated_plan.tasks,
        "current_step_index": 0
    }

def executor_node(state: AgentState) -> Dict:
    """Finds the next incomplete task, executes it, and updates the state."""
    current_plan = state["plan"]

    next_task = None
    for task in current_plan:
        if not task.completed:
            next_task = task
            break

    if next_task is None:
        return {"plan": current_plan}
    


if __name__ == "__main__":
    initial_state = {
        "user_message": "Research OpenAI's latest model, check its pricing, and summarize the changes.",
        "plan": [],
        "current_step_index": 0,
        "final_response": None
    }

    print("🧠 Triggering Planner Node...")
    state_updates = planner_node(initial_state)

    print("\n📋 Generated Chronological Steps:")
    for task in state_updates["plan"]:
        print(f"[{task.id}] {task.name} (Completed: {task.completed})")