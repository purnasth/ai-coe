# Vyaguta Onboarding Assistant Chatbot - Technical FAQ

## Where is prompt engineering used in the codebase?

Prompt engineering is implemented in the function `get_prompt_template()` in `main.py`. This function defines a custom prompt template that guides the language model (LLM) to answer user questions about Vyaguta's modules, features, and onboarding procedures. The prompt ensures that the LLM provides context-aware, relevant, and clear responses, and instructs it to admit when it does not know the answer. This is crucial for maintaining answer quality and user trust.

**Code block:**

```python
def get_prompt_template() -> PromptTemplate:
    ...
    return PromptTemplate(
        template="""
You are Vyaguta's onboarding assistant. Use the provided context to answer user questions about Vyaguta's modules, features, and onboarding procedures. If unsure, say you don't know.

Context:
{context}

Question: {question}
Answer:
""",
        input_variables=["context", "question"],
    )
```

## Where is LangChain used in the codebase?

LangChain is used throughout the codebase to orchestrate the workflow between document retrieval and LLM response generation. Specifically, it is used in the following places:

- **Document Loading and Embedding:**
  - `DirectoryLoader`, `TextLoader`, and `FAISS` from LangChain are used to load and embed onboarding documents for retrieval.
- **Prompt Engineering:**
  - `PromptTemplate` from LangChain is used to define the prompt for the LLM.
- **LLM Integration:**
  - `ChatOpenAI` from LangChain is used to interface with the OpenAI language model.
- **RetrievalQA Chain:**
  - `RetrievalQA` from LangChain is used to build the RAG (Retrieval-Augmented Generation) chain that combines document retrieval and LLM answering.

**Code block:**

```python
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
```

## Where is Retrieval-Augmented Generation (RAG) used in the codebase?

RAG is implemented in the following blocks:

- **Document Embedding and Retrieval:**
  - The function `create_retriever(docs)` embeds the onboarding documents and creates a retriever for searching relevant content.
- **RetrievalQA Chain:**
  - The function `build_qa_chain(llm, retriever, prompt)` constructs a chain that first retrieves relevant context from the documents and then passes it to the LLM for answer generation. This is the core of the RAG approach.

**Code block:**

```python
def create_retriever(docs):
    ...
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(docs, embeddings)
    return vectorstore.as_retriever()

def build_qa_chain(llm, retriever, prompt):
    ...
    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt},
    )
```

## Why are these technologies used?

- **Prompt Engineering:** Ensures the LLM provides accurate, context-aware, and user-friendly answers, improving the reliability and trustworthiness of the chatbot.
- **LangChain:** Simplifies the integration of document retrieval, prompt engineering, and LLM orchestration, making the code modular and maintainable.
- **RAG:** Allows the chatbot to provide up-to-date, contextually relevant answers by retrieving information from internal documentation, rather than relying solely on the LLM's pre-trained knowledge.

---

For more details, see the code comments and docstrings in `main.py`.
