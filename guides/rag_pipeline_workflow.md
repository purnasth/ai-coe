# Vyaguta Assistant RAG Pipeline Workflow

This guide explains the Retrieval-Augmented Generation (RAG) pipeline implemented in the Vyaguta Assistant project, using LangChain, OpenAI, and ChromaDB. It covers each step from file preparation to answering user queries with context-aware responses.

---

## 0. Refreshing the RAG Pipeline (IMPORTANT!)

**Whenever you add, update, or remove markdown files in your knowledge base (docs, docs-api, docs-confluence, etc.), you MUST refresh the RAG pipeline to re-chunk, re-embed, and re-index all data.**

- **How to refresh:**
  ```bash
  python refresh_rag.py
  ```
- This will delete the old `.pkl` and ChromaDB vector store, and rebuild them from all current markdown files.
- Always run this after fetching new Confluence data or updating any docs.

---

## 1. File Preparation

- **Purpose:** Load and read multiple Markdown (`.md`) files from specified directories. These files serve as the source knowledge base (e.g., exported from Confluence, API, or internal docs).
- **Code Location:** `rag_pipeline.py` → `load_markdown_docs()`
- **Example Usage:**
  ```python
  docs = load_markdown_docs(["docs", "docs-api", "docs-confluence/vyaguta", "docs-confluence/leap"])
  ```

---

## 2. Document Consolidation & Serialization

- **Purpose:** Merge the contents of all Markdown files into a single list of LangChain `Document` objects, and serialize it as a `.pkl` file for reuse and performance optimization.
- **Code Location:** `rag_pipeline.py` → `consolidate_and_serialize_docs()` and `load_docs_from_pickle()`
- **Example Usage:**
  ```python
  docs = consolidate_and_serialize_docs(["docs", "docs-api", "docs-confluence/vyaguta", "docs-confluence/leap"])
  # Later reuse:
  docs = load_docs_from_pickle()
  ```
- **Result:** Creates `docs_consolidated.pkl` in your project directory.

---

## 3. Text Chunking

- **Purpose:** Use LangChain’s `RecursiveCharacterTextSplitter` to divide the consolidated document into smaller, contextually meaningful chunks optimized for embedding.
- **Code Location:** `rag_pipeline.py` → `chunk_documents()`
- **Example Usage:**
  ```python
  chunks = chunk_documents(docs, chunk_size=800, chunk_overlap=100)
  ```

---

## 4. Embedding & Vector Store

- **Purpose:** Generate embeddings for the text chunks using OpenAI Embeddings (or another embedding model) and store them in a Chroma vector database using LangChain’s vector store integration.
- **Code Location:** `rag_pipeline.py` → `build_chroma_vectorstore()`
- **Example Usage:**
  ```python
  vectorstore = build_chroma_vectorstore(chunks, persist_directory="chroma_db")
  ```
- **Result:** Creates/updates the `chroma_db` directory for fast semantic search.

---

## 5. RAG Pipeline Setup & Usage

- **Purpose:** Set up a Retrieval-Augmented Generation (RAG) flow with LangChain where:
  - The Chroma vector store is used as a retriever.
  - Retrieved chunks are passed along with the user query to OpenAI’s LLM to generate an answer with context.
- **Code Location:**
  - `rag_pipeline.py` → `setup_rag_pipeline()`
  - `main.py` → RAG workflow
- **Example Usage:**
  ```python
  retriever = setup_rag_pipeline(["docs", "docs-api", "docs-confluence/vyaguta", "docs-confluence/leap"])
  qa_chain = RetrievalQA.from_chain_type(
      llm=llm,
      retriever=retriever,
      chain_type="stuff",
      chain_type_kwargs={"prompt": prompt},
  )
  result = qa_chain.invoke({"query": user_question})
  answer = result["result"]
  ```

---

## Workflow Summary

1. **Markdown files** are loaded from knowledge base directories.
2. **Documents** are merged and serialized for fast reuse.
3. **Text chunks** are created for optimal embedding.
4. **Embeddings** are generated and stored in ChromaDB.
5. **RAG pipeline** retrieves relevant chunks and generates context-aware answers using OpenAI’s LLM.
6. **Always refresh the RAG pipeline after updating docs!**

---

## Troubleshooting & Tips

- Ensure your `.env` file contains a valid `OPENAI_API_KEY`.
- If you see ChromaDB warnings about persistence, you can safely ignore them or remove deprecated code as described in this guide.
- To inspect the process, add print/logging statements in each function to view intermediate results.
- **Always run `python refresh_rag.py` after updating or adding docs!**

---

## References

- [LangChain Documentation](https://python.langchain.com/docs/)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference/introduction)
