from typing import Literal, TypedDict

import streamlit as st


class message(TypedDict):
    role: Literal["user", "assistant"]
    content: str


def displayMsg(msg: message) -> None:
    with st.chat_message(msg["role"]):
        st.text(msg["content"])


def displayLastMsg(message_history: list[message]) -> None:
    displayMsg(message_history[-1])


def displayAllMsg(message_history: list[message]) -> None:
    for message in message_history:
        displayMsg(message)
