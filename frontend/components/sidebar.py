import streamlit as st
from utils import load_conversation, new_chat


def render_sidebar():
    st.sidebar.title("Langraph Chatbot")

    if st.sidebar.button("New Chat"):
        new_chat()

    st.sidebar.header("My Coversations")

    for thread_id in reversed(st.session_state["threads"]):
        title = st.session_state["threads"][thread_id]["title"] or "New Chat"

        if st.sidebar.button(label=title, key=f"thread_btn_{thread_id}"):
            st.session_state["active_thread"] = thread_id
            st.session_state["message_history"] = load_conversation(thread_id)
