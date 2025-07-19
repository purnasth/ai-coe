from rag_pipeline import refresh_rag_pipeline
import time


def debug_log(msg):
    print(f"[DEBUG {time.strftime('%H:%M:%S')}] {msg}")


def main():
    print("Refreshing RAG pipeline: rebuilding .pkl and ChromaDB vector store...")
    debug_log("Building/updating RAG index...")
    refresh_rag_pipeline(["docs", "docs-api/people", "docs-confluence"])
    debug_log("RAG index build/update complete!")
    print(
        "RAG pipeline refresh complete. You can now run your assistant and all docs will be available."
    )


if __name__ == "__main__":
    main()
