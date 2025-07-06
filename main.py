"""
Vyaguta Assistant Chatbot

This script implements a Retrieval-Augmented Generation (RAG) chatbot for onboarding using LangChain, OpenAI, and prompt engineering.

Key Concepts Utilized:
- Prompt Engineering: Custom prompt template to guide LLM responses.
- Retrieval-Augmented Generation (RAG): Retrieves relevant onboarding docs for context.
- LangChain: Orchestrates the workflow between retrieval and LLM.

All major functions and classes are documented with docstrings for clarity and maintainability.
"""

import os
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate


def load_api_key() -> str:
    """
    Loads the OpenAI API key from environment variables.

    Returns:
        str: The OpenAI API key.
    """
    load_dotenv()
    return os.getenv("OPENAI_API_KEY")


OPENAI_API_KEY = load_api_key()


def load_onboarding_docs(directory: str = "docs"):
    """
    Loads onboarding documentation from the specified directory.

    Args:
        directory (str): Directory containing onboarding docs.
    Returns:
        list: List of loaded documents.
    """
    loader = DirectoryLoader(directory, glob="*.md", loader_cls=TextLoader)
    return loader.load()


docs = load_onboarding_docs()


def create_retriever(docs):
    """
    Embeds documents and creates a retriever for RAG.

    Args:
        docs (list): List of documents to embed.
    Returns:
        retriever: Retriever object for document search.
    """
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(docs, embeddings)
    return vectorstore.as_retriever()


retriever = create_retriever(docs)


def get_prompt_template() -> PromptTemplate:
    """
    Returns a prompt template for the onboarding assistant.

    Returns:
        PromptTemplate: The prompt template for the LLM.
    """
    return PromptTemplate(
        template="""
You are Vyaguta's assistant. Use the provided context to answer user questions about Vyaguta's modules, features, onboarding procedures, tools, policies, and any information available about Vyaguta and Leapfrog.

If the user asks about the creator or author of Vyaguta Assistant Chatbot, answer with:
"Vyaguta Assistant Chatbot was created by Purna Bahadur Shrestha, Associate Software Engineer at Leapfrog Technology. You can reach him at purnashrestha@lftechnology.com."

If you are unsure or cannot find the answer in the provided context, politely say you are not sure or do not know. Do not make up answers. If you have already told the user you do not know for a similar question before, then suggest they visit these official resources for more information:
- Vyaguta Portal: https://vyaguta.lftechnology.com/
- Vyaguta Wiki: https://lftechnology.atlassian.net/wiki/spaces/VYAGUTA/overview

Always be helpful, concise, and polite. If the answer is not in the context, respond with a polite message such as "I'm not sure about that based on the current information." Only after repeated uncertainty (i.e., if you have already said you do not know), provide the above links.

Context:
{context}

Question: {question}
Answer:
""",
        input_variables=["context", "question"],
    )


prompt = get_prompt_template()


def get_llm(api_key: str):
    """
    Initializes the OpenAI LLM for chat.

    Args:
        api_key (str): OpenAI API key.
    Returns:
        ChatOpenAI: The LLM instance.
    """
    return ChatOpenAI(openai_api_key=api_key, temperature=0.2, model="gpt-4.1-nano")


llm = get_llm(OPENAI_API_KEY)


def build_qa_chain(llm, retriever, prompt):
    """
    Builds the RetrievalQA chain using LangChain for RAG.

    Args:
        llm: The language model instance.
        retriever: The retriever for document search.
        prompt: The prompt template for prompt engineering.
    Returns:
        RetrievalQA: The QA chain for answering questions.
    """
    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt},
    )


qa_chain = build_qa_chain(llm, retriever, prompt)


def main():
    """
    Runs the Vyaguta Assistant Chatbot in a terminal chat loop.
    """
    import sys

    try:
        from colorama import init, Fore, Style

        init(autoreset=True)
        COLORAMA = True
    except ImportError:
        COLORAMA = False

    def color_text(text, color):
        if not COLORAMA:
            return text
        return color + text + Style.RESET_ALL

    title = "Vyaguta Assistant Chatbot (type 'exit' to quit)"
    border = "=" * len(title)
    print(color_text(border, Fore.CYAN) if COLORAMA else border)
    print(color_text(title, Fore.CYAN + Style.BRIGHT) if COLORAMA else title)
    print(color_text(border, Fore.CYAN) if COLORAMA else border)

    while True:
        user_prompt = (
            color_text("\nYou > ", Fore.GREEN + Style.BRIGHT)
            if COLORAMA
            else "\nYou > "
        )
        question = input(user_prompt)
        if question.strip().lower() == "exit":
            break

        result = qa_chain.invoke({"query": question})
        answer_header = (
            color_text("\nAssistant:", Fore.MAGENTA + Style.BRIGHT)
            if COLORAMA
            else "\nAssistant:"
        )
        answer_body = (
            color_text(result["result"], Fore.YELLOW) if COLORAMA else result["result"]
        )
        print(answer_header)
        print(answer_body)

    if not COLORAMA:
        print(
            "\nFor a more colorful experience, install the 'colorama' package: pip install colorama"
        )


if __name__ == "__main__":
    main()
