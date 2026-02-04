import streamlit as st
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_core.runnables import RunnableConfig
from utils import displayAllMsg, displayLastMsg, set_thread_title

from backend.langgraph_backend import chatbot


def render_chat():
    # {"role": "user", "content": "Hi"}
    # {"role": "assistant", "content": "Hello, How can I help you?"}

    # load the conversation history
    displayAllMsg(st.session_state["message_history"])

    user_input = st.chat_input("Type Here")
    if not user_input:
        return

    # add user msg to msg_history
    st.session_state["message_history"].append({"role": "user", "content": user_input})
    displayLastMsg(st.session_state["message_history"])

    thread_id = st.session_state["active_thread"]
    CONFIG: RunnableConfig = {
        "configurable": {"thread_id": thread_id},
        # "metadata": {"thread_id": thread_id},
        # "run_name": st.session_state["threads"][thread_id]["title"],
        # "run_id": thread_id,
    }

    # stream the llm response
    with st.chat_message("assistant"):
        ai_message = st.write_stream(
            message_chunk.content
            for message_chunk, metadata in chatbot.stream(
                {"messages": [HumanMessage(content=user_input)]},
                config=CONFIG,
                stream_mode="messages",
            )
            if isinstance(message_chunk, BaseMessage)
        )

    st.session_state["message_history"].append(
        {"role": "assistant", "content": ai_message}
    )

    set_thread_title(user_input)
