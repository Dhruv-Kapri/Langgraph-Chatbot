from typing import Optional

import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langchain_core.runnables import RunnableConfig
from streamlit.elements.lib.mutable_status_container import StatusContainer
from utils import displayAllMsg, displayLastMsg, set_thread_title

from backend.langgraph_backend import chatbot
from backend.memory import thread_document_metadata


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
        "run_name": "chat_turn",
    }

    # stream the llm response
    with st.chat_message("assistant"):

        status_holder: dict[str, Optional[StatusContainer]] = {"box": None}

        def ai_only_stream():
            for message_chunk, metadata in chatbot.stream(
                {"messages": [HumanMessage(content=user_input)]},
                config=CONFIG,
                stream_mode="messages",
            ):
                if isinstance(message_chunk, ToolMessage):
                    tool_name = getattr(message_chunk, "name", "tool")
                    if status_holder["box"] is None:
                        status_holder["box"] = st.status(
                            f"🔧 Using `{tool_name}` …", expanded=True
                        )
                    else:
                        status_holder["box"].update(
                            label=f"🔧 Using `{tool_name}` …",
                            state="running",
                            expanded=True,
                        )

                if isinstance(message_chunk, AIMessage):
                    yield message_chunk.content

        ai_message = st.write_stream(ai_only_stream())

        if status_holder["box"] is not None:
            status_holder["box"].update(
                label=f"✅ Tool finished",
                state="running",
                expanded=True,
            )

    st.session_state["message_history"].append(
        {"role": "assistant", "content": ai_message}
    )

    set_thread_title(user_input)

    doc_meta = thread_document_metadata(thread_id)
    if doc_meta:
        st.caption(
            f"Document indexed: {doc_meta.get('filename')} "
            f"(chunks: {doc_meta.get('chunks')}, pages: {doc_meta.get('documents')})"
        )
