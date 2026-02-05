from langgraph.prebuilt import ToolNode

from backend.graph.state import ChatState
from backend.llm import llm
from backend.tools import TOOLS

llm_with_tools = llm.bind_tools(tools=TOOLS)


def chat_node(state: ChatState) -> ChatState:
    messages = state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}


tool_node = ToolNode(TOOLS)
