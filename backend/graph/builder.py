import sqlite3

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, START, StateGraph

from backend.graph.nodes import chat_node
from backend.graph.state import ChatState


def build_chat_graph():
    conn = sqlite3.connect(database="langgraph_chatbot.db", check_same_thread=False)
    checkpointer = SqliteSaver(conn=conn)

    graph = StateGraph(ChatState)
    graph.add_node("chat_node", chat_node)
    graph.add_edge(START, "chat_node")
    graph.add_edge("chat_node", END)

    return graph.compile(checkpointer=checkpointer)
