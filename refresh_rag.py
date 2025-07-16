"""
Utility script to force a full refresh of the RAG pipeline:
- Deletes old .pkl and ChromaDB vector store
- Re-chunks and re-embeds all markdown docs (including new confluence subfolders)
- Ensures all new/updated docs are indexed and available for retrieval

Usage:
    python refresh_rag.py
"""

from rag_pipeline import refresh_rag_pipeline

if __name__ == "__main__":
    print("Refreshing RAG pipeline: rebuilding .pkl and ChromaDB vector store...")
    refresh_rag_pipeline()
    print(
        "RAG pipeline refresh complete. You can now run your assistant and all docs will be available."
    )
