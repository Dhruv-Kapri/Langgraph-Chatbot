from backend.graph.state import ChatState
from backend.llm import llm


def chat_node(state: ChatState) -> ChatState:
    messages = state["messages"]
    response = llm.invoke(messages)
    return {"messages": [response]}
