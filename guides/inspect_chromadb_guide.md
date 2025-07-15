# Inspecting ChromaDB Vector Store

This guide explains how to inspect and view the contents of your ChromaDB vector store in the Vyaguta Assistant project.

---

## Purpose

The ChromaDB vector store contains all the embedded chunks of your markdown knowledge base (docs, API data, Confluence exports, etc.) used for semantic search and retrieval in your RAG pipeline. Sometimes, you may want to:

- Verify what data is stored and retrievable
- Debug or audit the knowledge base
- Understand how your documents are chunked and indexed

---

## How to Inspect ChromaDB

A script named `inspect_chromadb.py` is provided in your project root. It prints all stored document chunks and their metadata.

### Usage

1. **Run the script:**

   ```bash
   python inspect_chromadb.py
   ```

2. **What you will see:**
   - The total number of chunks stored in ChromaDB
   - The content of each chunk (document text)
   - The metadata for each chunk (e.g., source file, chunk index)

---

## Example Output

```
Total chunks stored: 120

--- Chunk 1 ---
This is the first chunk of a markdown document...
Metadata: {'source': 'docs/onboarding-faq.md', ...}

--- Chunk 2 ---
Another chunk from a different document...
Metadata: {'source': 'docs-api/people/123_John_Doe.md', ...}
...
```

---

## Why Use This?

- **Debugging:** Ensure all expected documents are loaded and chunked correctly.
- **Auditing:** See what information is available for retrieval and answering user queries.
- **Transparency:** Understand how your knowledge base is represented in the vector store.

---

## Tips

- If you want to see only specific documents or metadata, you can modify the script to filter or format the output.
- For large knowledge bases, consider piping output to a file:
  ```bash
  python inspect_chromadb.py > chroma_contents.txt
  ```

---

## References

- [ChromaDB Documentation](https://docs.trychroma.com/)
- [LangChain Vector Stores](https://python.langchain.com/docs/integrations/vectorstores/chroma)
