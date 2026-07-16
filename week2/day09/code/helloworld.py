from autogen import ConversableAgent

llm_config = {
    "config_list": [
        {
            "model": "gpt-4o",
            "api_key": ""
        }
    ]
}

def is_termination(msg: dict) -> bool:
    return "TERMINATION" in (msg.get("content") or "")

# def is_termination_m(msg: dict) -> bool:
#     content = msg.get("content")
#     if content is None:
#         return False
#     return "TERMINATION" in content    

coder = ConversableAgent(
    name="Coder",
    system_message="You are a brilliant Python developer. Write clean python code. "
                   "Once the critic approves with 'looks good', reply with 'TERMINATE'.",
    human_input_mode="NEVER",
    is_termination_msg=is_termination
)

critic = ConversableAgent(
    name="Critic",
    system_message="You are a strict code reviewer. If the code is correct, "
                   "say 'looks good' and nothing else.",
    llm_config=llm_config,
    is_termination_msg=is_termination,
    human_input_mode="NEVER"
)


# MAIN FUNCTION
critic.initiate_chat(
    recipient=coder,
    message=""
)