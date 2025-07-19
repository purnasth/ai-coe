from rag_pipeline import refresh_rag_pipeline
from log_utils import debug_log, output_log


def main():
    output_log("Refreshing RAG pipeline: rebuilding .pkl and ChromaDB vector store...")
    debug_log("Building/updating RAG index...")
    refresh_rag_pipeline(["docs", "docs-api/people", "docs-confluence"])
    debug_log("RAG index build/update complete!")
    output_log(
        "RAG pipeline refresh complete. You can now run your assistant and all docs will be available."
    )


if __name__ == "__main__":
    main()
