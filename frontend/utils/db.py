import sqlite3

import streamlit as st
from langgraph.checkpoint.sqlite import SqliteSaver


def init_db():
    conn = sqlite3.connect("langgraph_chatbot.db", check_same_thread=False)
    cur = conn.cursor()

    cur.execute(
        """
    CREATE TABLE IF NOT EXISTS threads (
        thread_id TEXT PRIMARY KEY,
        title TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    )

    conn.commit()
    conn.close()
    conn.close()


def register_thread(thread_id) -> None:
    conn = sqlite3.connect("langgraph_chatbot.db", check_same_thread=False)
    cur = conn.cursor()

    cur.execute(
        """
    INSERT OR IGNORE INTO threads (thread_id, title)
    VALUES (?, NULL)
    """,
        (thread_id,),
    )

    conn.commit()
    conn.close()

    if thread_id not in st.session_state["threads"]:
        st.session_state["threads"][thread_id] = {"title": None}


def save_thread_title(thread_id: str, title: str):
    conn = sqlite3.connect("langgraph_chatbot.db", check_same_thread=False)
    cur = conn.cursor()

    cur.execute(
        """
    INSERT INTO threads (thread_id, title)
    VALUES (?, ?)
    ON CONFLICT(thread_id)
    DO UPDATE SET title = excluded.title
    """,
        (thread_id, title),
    )

    conn.commit()
    conn.close()


def get_checkpointer():
    conn = sqlite3.connect(database="langgraph_chatbot.db", check_same_thread=False)
    return SqliteSaver(conn=conn)


def retrieve_all_threads():
    checkpointer = get_checkpointer()

    # 1. Get thread_ids from LangGraph checkpoints
    thread_ids = set()
    for checkpoint in checkpointer.list(None):
        thread_ids.add(checkpoint.config["configurable"]["thread_id"])

    # 2. Load metadata from DB
    conn = sqlite3.connect("langgraph_chatbot.db", check_same_thread=False)
    cur = conn.cursor()

    cur.execute("SELECT thread_id, title FROM threads")
    rows = cur.fetchall()
    conn.close()

    title_map = {tid: title for tid, title in rows}

    # 3. Merge
    threads = {}
    for tid in thread_ids:
        threads[tid] = {"title": title_map.get(tid)}  # None if not generated yet

    return threads
