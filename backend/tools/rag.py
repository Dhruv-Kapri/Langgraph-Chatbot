from typing import Optional

from langchain_core.tools import tool

from backend.memory import get_retriever, thread_document_metadata


@tool
def rag_tool(query: str, thread_id: Optional[str] = None) -> dict:
    """
    Retrieve relevant information from the uploaded PDF for this chat thread.
    Always include the thread_id when calling this tool.
    """
    retreiver = get_retriever(thread_id)
    if retreiver is None:
        return {
            "error": "No document indexed for this chat. Upload a PDF first.",
            "querry": query,
        }

    result = retreiver.invoke(query)
    context = [doc.page_content for doc in result]
    metadata = [doc.metadata for doc in result]

    return {
        "query": query,
        "context": context,
        "metadata": metadata,
        "source_file": thread_document_metadata(thread_id).get("filename"),
    }
