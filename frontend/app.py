import streamlit as st
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig
from utils import displayAllMsg, displayLastMsg

from backend.langgraph_backend import chatbot

CONFIG: RunnableConfig = {"configurable": {"thread_id": "1"}}


if "message_history" not in st.session_state:
    st.session_state["message_history"] = []

# {"role": "user", "content": "Hi"}
# {"role": "assistant", "content": "Hello, How can I help you?"}


displayAllMsg(st.session_state["message_history"])


user_input = st.chat_input("Type Here")

if user_input:
    st.session_state["message_history"].append({"role": "user", "content": user_input})
    displayLastMsg(st.session_state["message_history"])

    response = chatbot.invoke(
        {"messages": [HumanMessage(content=user_input)]},
        config=CONFIG,
    )
    ai_message = response["messages"][-1].content
    st.session_state["message_history"].append(
        {"role": "assistant", "content": ai_message}
    )
    displayLastMsg(st.session_state["message_history"])
