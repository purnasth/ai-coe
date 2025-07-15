"""
Script to inspect and print all documents/chunks stored in ChromaDB vector store.
Usage:
    python inspect_chromadb.py
"""

from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv

load_dotenv()

CHROMA_DIR = "chroma_db"


def main():
    # Load the Chroma vector store
    vectorstore = Chroma(persist_directory=CHROMA_DIR)
    # Try to get all stored documents/chunks
    try:
        docs = vectorstore.get()
        print(f"Total chunks stored: {len(docs['documents'])}")
        for i, doc in enumerate(docs["documents"]):
            print(f"\n--- Chunk {i+1} ---")
            print(doc)
            # Optionally print metadata
            if "metadatas" in docs:
                print("Metadata:", docs["metadatas"][i])
    except Exception as e:
        print("Error inspecting ChromaDB:", e)


if __name__ == "__main__":
    main()
