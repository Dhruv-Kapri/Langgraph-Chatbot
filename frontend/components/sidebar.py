import streamlit as st
from utils import load_conversation, new_chat

from backend.memory import ingest_pdf


def render_sidebar():
    st.sidebar.title("Langraph Chatbot")

    if st.sidebar.button("New Chat"):
        new_chat()

    thread_key = str(st.session_state["active_thread"])
    thread_docs = st.session_state["ingested_docs"][thread_key]

    if thread_docs:
        latest_doc = list(thread_docs.values())[-1]
        st.sidebar.success(
            f"Using `{latest_doc.get('filename')}` "
            f"({latest_doc.get('chunks')} chunks from {latest_doc.get('documents')} pages)"
        )
    else:
        st.sidebar.info("No PDF indexed yet.")

    uploaded_pdf = st.sidebar.file_uploader("Upload a PDF for this chat", type=["pdf"])
    if uploaded_pdf:
        if uploaded_pdf.name in thread_docs:
            st.sidebar.info(f"`{uploaded_pdf.name}` already processed for this chat.")
        else:
            with st.sidebar.status("Indexing PDF…", expanded=True) as status_box:
                summary = ingest_pdf(
                    uploaded_pdf.getvalue(),
                    thread_id=thread_key,
                    filename=uploaded_pdf.name,
                )
                thread_docs[uploaded_pdf.name] = summary
                status_box.update(
                    label="✅ PDF indexed", state="complete", expanded=False
                )

    st.sidebar.header("My Coversations")

    if not st.session_state["threads"]:
        st.sidebar.write("No past conversations yet.")
        return

    for thread_id in reversed(st.session_state["threads"]):
        title = st.session_state["threads"][thread_id]["title"] or "New Chat"

        if st.sidebar.button(label=title, key=f"thread_btn_{thread_id}"):
            st.session_state["active_thread"] = thread_id
            st.session_state["message_history"] = load_conversation(thread_id)
