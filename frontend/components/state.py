import streamlit as st
from utils import generate_thread_id, register_thread


def init_session():
    if "message_history" not in st.session_state:
        st.session_state["message_history"] = []

    if "threads" not in st.session_state:
        st.session_state["threads"] = {}

    if "active_thread" not in st.session_state:
        thread_id = generate_thread_id()
        st.session_state["active_thread"] = thread_id

    register_thread(st.session_state["active_thread"])
