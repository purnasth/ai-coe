import os
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# 1. Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# 2. Load onboarding docs
loader = DirectoryLoader(
    "docs",
    glob="*.md",
    loader_cls=TextLoader
)
docs = loader.load()

# 3. Embed docs for retrieval (RAG)
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(docs, embeddings)
retriever = vectorstore.as_retriever()

# 4. Prompt engineering
prompt = PromptTemplate(
    template="""
You are Vyaguta's onboarding assistant. Use the provided context to answer user questions about Vyaguta's modules, features, and onboarding procedures. If unsure, say you don't know.

Context:
{context}

Question: {question}
Answer:
""",
    input_variables=["context", "question"]
)

# 5. LLM setup
llm = ChatOpenAI(
    openai_api_key=OPENAI_API_KEY,
    temperature=0.2,
    model="gpt-4.1-nano"
)

# 6. RAG chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type="stuff",
    chain_type_kwargs={"prompt": prompt}
)

# 7. Terminal chat loop
print('Vyaguta Onboarding Assistant Chatbot (type "exit" to quit)')
while True:
    question = input("\nAsk a question: ")
    if question.strip().lower() == "exit":
        break
    # Only run RAG chain and print the AI answer
    result = qa_chain.invoke({"query": question})
    print("\n[AI Answer]:", result["result"].strip())
