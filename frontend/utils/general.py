import uuid

import streamlit as st
from langchain_core.messages import HumanMessage

from backend import chatbot, llm_general

from .db import register_thread, save_thread_title


def generate_thread_id():
    return str(uuid.uuid4())


def new_chat() -> None:
    thread_id = generate_thread_id()
    st.session_state["active_thread"] = thread_id
    register_thread(thread_id)
    st.session_state["message_history"] = []


def generate_chat_title(first_user_msg: str) -> str:
    prompt = f"Generate a short, concise title text (max 5 words) only. No other text in the response, just the tile for a conversation that starts with:\n\n {first_user_msg}"

    result = llm_general.invoke([HumanMessage(content=prompt)])
    return result.content.strip().strip('"')


def set_thread_title(user_input: str):
    thread_id = st.session_state["active_thread"]

    if st.session_state["threads"][thread_id]["title"] is not None:
        return

    title = generate_chat_title(user_input)

    st.session_state["threads"][thread_id]["title"] = title
    save_thread_title(thread_id, title)

    st.rerun()


def load_conversation(thread_id):
    state = chatbot.get_state(config={"configurable": {"thread_id": thread_id}})
    messages = state.values.get("messages", [])

    temp_msg = []
    for msg in messages:
        if isinstance(msg, HumanMessage):
            role = "user"
        else:
            role = "assistant"

        temp_msg.append({"role": role, "content": msg.content})

    return temp_msg
