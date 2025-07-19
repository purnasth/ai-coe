# Vyaguta Assistant RAG Pipeline Workflow

This guide explains the Retrieval-Augmented Generation (RAG) pipeline in the Vyaguta Assistant project, using LangChain, OpenAI, and ChromaDB. It now reflects the optimized workflow where the ChromaDB vector store is only rebuilt when needed, resulting in much faster chatbot startup.

---

## Why This Change?

**Previous behavior:**

- The RAG pipeline (ChromaDB index and embeddings) was rebuilt every time you started the chatbot, causing slow startup (several minutes) even if the data had not changed.

**New behavior:**

- The RAG pipeline is only rebuilt when you explicitly update your docs and run the build script.
- On normal chatbot runs, the existing ChromaDB index and pickle are loaded instantly, making startup nearly immediate.

**Benefits:**

- Fast chatbot startup (seconds, not minutes)
- No unnecessary recomputation or API calls
- Only update the index when your data changes

---

## Key Scripts and Their Roles

- **rag_pipeline.py**: Contains all the core functions for loading, chunking, embedding, and managing the ChromaDB vector store. You do NOT run this file directly. It is imported and used by the other scripts.
- **rebuild_rag_pipeline.py**: The main script to rebuild the RAG pipeline index. Run this whenever you add, update, or remove markdown files. (Preferred entrypoint)
- **main.py**: The chatbot entrypoint. Loads the existing index for fast startup and serves the assistant.
- **inspect_chromadb.py**: Lets you inspect the contents of your ChromaDB vector store for debugging or auditing.

---

## Workflow Overview

### 1. Build/Refresh the RAG Index (Only When Docs Change)

Whenever you add, update, or remove markdown files in your knowledge base (`docs`, `docs-api`, `docs-confluence`, etc.), you MUST rebuild the RAG pipeline to re-chunk, re-embed, and re-index all data.

**How to refresh/build:**

```bash
python rebuild_rag_pipeline.py
```

- This will delete the old `.pkl` and ChromaDB vector store, and rebuild them from all current markdown files.
- Only run this when your docs change!

---

### 2. Start the Chatbot (Fast Startup)

For normal chatbot use, just run:

```bash
python main.py
```

- This will load the existing ChromaDB index and pickle.
- Startup is nearly instant if the index exists.
- No re-indexing or re-embedding is performed unless you deleted the index or changed the docs.

---

### 3. Inspecting the Vector Store

To see what is stored in your ChromaDB vector store:
llm = ChatOpenAI(openai_api_key=api_key, temperature=0.2, model="gpt-4.1-nano")
```bash
python inspect_chromadb.py
```

- Prints all stored document chunks and their metadata.
- Useful for debugging and auditing your knowledge base.

---

## Typical Workflow

1. **Update docs** (add, edit, or remove markdown files)
2. **Rebuild index**:
   ```bash
   python rebuild_rag_pipeline.py
   ```
3. **Start chatbot**:
   ```bash
   python main.py
   ```
4. **(Optional) Inspect vector store**:
   ```bash
   python inspect_chromadb.py
   ```

---

## FAQ

**Q: Why not rebuild the index every time?**
A: Rebuilding is slow and uses API calls. Most of the time, your docs do not change, so you should reuse the existing index for fast startup.

**Q: When do I need to rebuild?**
A: Only when you add, update, or remove markdown files in your knowledge base.

**Q: What if I forget to rebuild?**
A: The chatbot will use the old index and not see your latest changes. Always rebuild after updating docs.

**Q: Can I automate the rebuild?**
A: Yes, you can add a watcher or script to trigger `rebuild_rag_pipeline.py` when docs change, but for most workflows, manual rebuild is sufficient.

**Q: Should I run rag_pipeline.py directly?**
A: No. This file only contains the pipeline logic and is used by the other scripts. Do not run it as a script.

---

## References

- [ChromaDB Documentation](https://docs.trychroma.com/)
- [LangChain Vector Stores](https://python.langchain.com/docs/integrations/vectorstores/chroma)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference/introduction)

---

_Last updated: July 2025 — reflects optimized, fast-startup RAG pipeline logic and script usage._
