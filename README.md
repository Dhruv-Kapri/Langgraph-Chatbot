# Langgraph-Chatbot

A minimal, well-structured chatbot built using **LangGraph** with a **Streamlit** frontend and **Gemini (Google Generative AI)** as the underlying LLM.

This project is intended as a learning-first, extensible foundation for experimenting with LangGraph concepts such as state graphs, memory, checkpointing, and multi-interface backends.

---

## Features

- LangGraph-based stateful chatbot
- Typed graph state with message aggregation
- In-memory checkpointing with thread-based conversation handling
- Streamlit chat UI
- Clean backend / frontend separation
- Modern Python packaging using `pyproject.toml`

---

## Project Structure

```
Langgraph-Chatbot/
├── backend/
│ ├── graph/
│ │ ├── state.py                 # Graph state schema
│ │ ├── nodes.py                 # Graph nodes (LLM logic)
│ │ └── builder.py               # Graph construction
│ ├── llm.py                     # LLM configuration
│ └── langgraph_backend.py
│
├── frontend/
│ ├── app.py                     # Streamlit app
│ └── utils/
│ └── messages.py                # Chat UI helpers
│
├── pyproject.toml               # Package + dependency definition
├── requirements.txt             # Dev install shortcut (-e .)
└── README.md

```

---

## Setup

### 1. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies (editable mode)

```bash
pip install -r requirements.txt
```
This installs the project using `pyproject.toml` as the source of truth.

### 3. Environment Variables

Create a `.env` file in the project root:
```.env
GOOGLE_API_KEY=your_google_api_key_here
```
Or Alternatively rename `.env.example` to `.env` and replace your API keys.

---

## Run the App

From the project root:
```bash
streamlit run frontend/app.py
```

---

### How it works (high level)

- User messages are sent from Streamlit to a LangGraph graph
- The graph maintains conversation state using `add_messages`
- A single chat node invokes Gemini via `ChatGoogleGenerativeAI`
- Responses are appended to state and returned to the UI
- `thread_id` is used to scope conversation memory

---

## Current Limitations

- Uses in-memory checkpointing (state is lost on restart)
- Single-node graph (no tools or routing yet)
- No streaming responses

---

