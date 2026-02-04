from langgraph.prebuilt import ToolNode

from backend.graph.state import ChatState
from backend.llm import llm

from .tools import tools


def chat_node(state: ChatState) -> ChatState:
    messages = state["messages"]
    llm_with_tools = llm.bind_tools(tools=tools)
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}


tool_node = ToolNode(tools)
