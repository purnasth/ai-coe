"""
RAG Pipeline Setup for Vyaguta Assistant

- Loads and consolidates Markdown files from specified directories
- Chunks text using RecursiveCharacterTextSplitter
- Embeds chunks using OpenAI Embeddings
- Stores embeddings in Chroma vector store
- Provides retriever for RAG workflow
- Serializes document list for reuse
"""

import os
import glob
import pickle
from dotenv import load_dotenv

from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

load_dotenv()

DOCS_PICKLE = "docs_consolidated.pkl"
CHROMA_DIR = "chroma_db"


def load_markdown_docs(directories=None):
    """
    Loads all Markdown files from specified directories and returns a list of Document objects.
    Supports nested subfolders (e.g., docs-confluence/vyaguta, docs-confluence/leap).
    """
    if directories is None:
        directories = [
            "docs",
            "docs-api",
            "docs-confluence/vyaguta",
            "docs-confluence/leap",
        ]
    all_docs = []
    for directory in directories:
        for file in glob.glob(f"{directory}/**/*.md", recursive=True):
            loader = UnstructuredMarkdownLoader(file)
            doc = loader.load()
            all_docs.extend(doc)
    return all_docs


def consolidate_and_serialize_docs(directories=None, pickle_path=DOCS_PICKLE):
    """
    Loads, consolidates, and pickles all Markdown documents for fast reuse.
    """
    docs = load_markdown_docs(directories)
    with open(pickle_path, "wb") as f:
        pickle.dump(docs, f)
    return docs


def load_docs_from_pickle(pickle_path=DOCS_PICKLE):
    """
    Loads Document objects from a pickle file.
    """
    with open(pickle_path, "rb") as f:
        docs = pickle.load(f)
    return docs


def chunk_documents(docs, chunk_size=1000, chunk_overlap=50):
    """
    Chunks all documents using RecursiveCharacterTextSplitter for optimal embedding.
    Uses a safe chunk size to avoid exceeding embedding API limits.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    chunks = []
    for doc in docs:
        for chunk in splitter.split_text(doc.page_content):
            chunks.append(Document(page_content=chunk, metadata=doc.metadata))
    return chunks


def build_chroma_vectorstore(chunks, persist_directory=CHROMA_DIR):
    """
    Embeds chunks and stores them in a Chroma vector database.
    """
    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma.from_documents(
        chunks, embeddings, persist_directory=persist_directory
    )
    return vectorstore


def get_chroma_retriever(vectorstore, k=10):
    """
    Returns a retriever from the Chroma vector store, retrieving up to k chunks.
    """
    return vectorstore.as_retriever(search_kwargs={"k": k})


# --- Main RAG Pipeline Entrypoint ---
def setup_rag_pipeline(directories=None, force_rebuild=False):
    """
    Loads, chunks, embeds, and sets up Chroma retriever for RAG.
    If force_rebuild is True, always rebuilds the index and pickle.
    """
    if force_rebuild:
        return refresh_rag_pipeline(directories)
    # If ChromaDB exists, just load it (fast!)
    if os.path.exists(CHROMA_DIR) and os.path.exists(DOCS_PICKLE):
        vectorstore = Chroma(
            persist_directory=CHROMA_DIR, embedding_function=OpenAIEmbeddings()
        )
        retriever = get_chroma_retriever(vectorstore, k=10)
        return retriever

    # Otherwise, build everything
    if os.path.exists(DOCS_PICKLE):
        docs = load_docs_from_pickle()
    else:
        docs = consolidate_and_serialize_docs(directories)
    chunks = chunk_documents(docs)
    vectorstore = build_chroma_vectorstore(chunks)
    retriever = get_chroma_retriever(vectorstore, k=10)
    return retriever


def refresh_rag_pipeline(directories=None):
    """
    Force a full refresh: re-chunk, re-embed, and overwrite the .pkl and ChromaDB vector store.
    Use this after adding new docs or changing doc paths.
    """
    if directories is None:
        directories = [
            "docs",
            "docs-api",
            "docs-confluence/vyaguta",
            "docs-confluence/leap",
        ]

    # Remove old .pkl and chroma_db if they exist
    import shutil

    if os.path.exists(DOCS_PICKLE):
        os.remove(DOCS_PICKLE)
    if os.path.exists(CHROMA_DIR):
        shutil.rmtree(CHROMA_DIR)

    # Rebuild everything
    docs = consolidate_and_serialize_docs(directories)
    chunks = chunk_documents(docs)
    vectorstore = build_chroma_vectorstore(chunks)
    retriever = get_chroma_retriever(vectorstore, k=10)
    return retriever
