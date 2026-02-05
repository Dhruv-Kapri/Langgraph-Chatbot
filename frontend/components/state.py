import streamlit as st
from utils import generate_thread_id, init_db, register_thread, retrieve_all_threads


def init_session():
    init_db()

    if "message_history" not in st.session_state:
        st.session_state["message_history"] = []

    if "threads" not in st.session_state:
        st.session_state["threads"] = retrieve_all_threads()

    if "active_thread" not in st.session_state:
        st.session_state["active_thread"] = generate_thread_id()

    if "ingested_docs" not in st.session_state:
        st.session_state["ingested_docs"] = {}

    register_thread(st.session_state["active_thread"])

    thread_key = str(st.session_state["active_thread"])
    st.session_state["ingested_docs"].setdefault(thread_key, {})
