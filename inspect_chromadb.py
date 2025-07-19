"""
Script to inspect and print all documents/chunks stored in ChromaDB vector store.
Usage:
    python inspect_chromadb.py
"""

from log_utils import debug_log, output_log
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

CHROMA_DIR = "chroma_db"


def main():
    # Load the Chroma vector store with the same embedding function used during creation
    vectorstore = Chroma(
        persist_directory=CHROMA_DIR, embedding_function=OpenAIEmbeddings()
    )

    # Try to get all stored documents/chunks
    try:
        docs = vectorstore.get()
        output_log(f"Total chunks stored: {len(docs['documents'])}")
        for i, doc in enumerate(docs["documents"]):
            output_log(f"--- Chunk {i+1} ---")
            output_log(doc)
            if "metadatas" in docs:
                output_log(f"Metadata: {docs['metadatas'][i]}")
    except Exception as e:
        output_log(f"Error inspecting ChromaDB: {e}")


if __name__ == "__main__":
    main()
