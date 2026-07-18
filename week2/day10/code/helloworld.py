import uuid
from typing import Optional, Literal
from typing_extensions import TypedDict

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END
from langgraph.types import interrupt, Command


class AgentState(TypedDict):
    content_draft: str
    feedback: Optional[str]
    approved: bool


# writer node
def draft_writer_node(state: AgentState):
    print("[Writer Node] Drafting or Refining the content...")
    # LLM Logic probably before this
    if state.get("feedback"):
        updated_draft = f"{state['content_draft']} (Revised based on feedback: {state['feedback']})"
    else:
        updated_draft = "Deep roots, strong seeds. The DEEPSEED community builds real things."
    
    return {"content_draft": updated_draft, "feedback": None}

def human_review_node(state: AgentState) -> Command[Literal["draft_writer_node", END]]:
    print("[Review Node] Interruption triggered. Waiting on you, human...")

    human_response = interrupt({
        "message": "Please review this draft. Do you approve?",
        "current_draft": state["content_draft"]
    })

    action = human_response.get("action")

    if action == "approve":
        print("[Review Node] Draft approved, Human.")
        return Command(
            update={"approved": True},
            goto=END
        )
    else:
        print("[Review Node] Draft rejected by Human")
        return Command(
            update={"approved": False, "feedback": human_response.get("feedback", "No specific feedback.")},
            goto="draft_writer_node"
        )
    
workflow = StateGraph(AgentState)

workflow.add_node("draft_writer_node", draft_writer_node)
workflow.add_node("human_review_node", human_review_node)

workflow.add_edge(START, "draft_writer_node")
workflow.add_edge("draft_writer_node", "human_review_node")

checkpointer = MemorySaver()

graph = workflow.compile(checkpointer=checkpointer)

# Main function

config = {"configurable": {"thread_id": str(uuid.uuid4())}}

events = graph.stream({"content_draft": "", "approved": False}, config, stream="values")
for event in events:
    pass

current_state = graph.get_state(config)
print(f"{current_state.next}")
print(f"{current_state.tasks[0].interrupts[0].value}")

resume_command = Command(resume={"approved": False, "feedback": "Make it sound more professional"})
events = graph.stream(resume_command, config, stream="values")
for event in events:
    pass

current_state = graph.get_state(config)
print(f"{current_state.values["content_draft"]}")
print(f"{current_state.next}")

resume_command = Command(resume={"approved": True})
events = graph.stream(resume_command, config, stream="values")
for event in events:
    pass

final_state = graph.get_state(config)
print(f"{final_state.values["approved"]}")