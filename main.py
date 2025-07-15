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
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from auth import app_startup
from rag_pipeline import setup_rag_pipeline

# --- Authenticate and refresh Vyaguta access token at startup ---
app_startup()

# --- Setup RAG pipeline with Chroma retriever ---
retriever = setup_rag_pipeline(["docs", "docs-api/people", "docs-confluence"])


def load_api_key() -> str:
    """
    Loads the OpenAI API key from environment variables.

    Returns:
        str: The OpenAI API key.
    """
    load_dotenv()
    return os.getenv("OPENAI_API_KEY")


OPENAI_API_KEY = load_api_key()


def get_prompt_template() -> PromptTemplate:
    """
    Returns a prompt template for the onboarding assistant, instructing the LLM to quote or summarize exact steps, rules, or lists from the markdown context.

    Returns:
        PromptTemplate: The prompt template for the LLM.
    """
    return PromptTemplate(
        template="""
You are Vyaguta's assistant. Use the provided context to answer user questions about Vyaguta's modules, features, onboarding procedures, tools, policies, coding guidelines, and any information available about Vyaguta and Leapfrog.

When answering, always quote or summarize the exact steps, rules, or lists from the context if available (e.g., bullet points, numbered steps, or code blocks). If the answer is a process or policy, provide the step-by-step instructions or rules as written in the documentation. If the answer is a definition or guideline, quote the relevant section or list.

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

    # people_data is already loaded and indexed for RAG at startup

    while True:
        user_prompt = (
            color_text("\nYou > ", Fore.GREEN + Style.BRIGHT)
            if COLORAMA
            else "\nYou > "
        )
        question = input(user_prompt)
        if question.strip().lower() == "exit":
            break

        # --- All queries handled by RAG pipeline ---
        result = qa_chain.invoke({"query": question})
        answer = result["result"]
        unsure_phrases = [
            "I'm not sure about that based on the current information",
            "I am not sure",
            "I don't know",
            "cannot find the answer",
            "refer to the official",
            "recommend visiting the official",
        ]

        # ---
        # RAG-ONLY MODE (restrict to documentation):
        # Uncomment the following block to restrict answers to documentation only (no AI fallback):
        # if any(phrase in answer for phrase in unsure_phrases):
        #     context = result.get("context", "")
        #     if context:
        #         answer += (
        #             "\n\n---\nMost relevant documentation section:\n" + context.strip()
        #         )

        # ---
        # RAG + AI FALLBACK MODE (default):
        if any(phrase in answer for phrase in unsure_phrases):
            # Show the most relevant context chunk verbatim for transparency
            context = result.get("context", "")
            if context:
                answer += (
                    "\n\n---\nMost relevant documentation section:\n" + context.strip()
                )
            # If still unsure, use LLM general knowledge as fallback for basic/general questions
            else:
                # Use a direct LLM call for general knowledge fallback
                general_prompt = f"""
You are a helpful AI assistant. Answer the following question with a concise, accurate, and non-hallucinated response. If the question is about a basic or general software engineering or IT concept, provide a clear, general definition. If the question is outside of common software/IT knowledge, say 'I'm not sure.'

Question: {question}
Answer:
"""
                general_llm = get_llm(OPENAI_API_KEY)
                try:
                    general_answer = general_llm.invoke(general_prompt)
                    if general_answer and not any(
                        phrase in general_answer for phrase in unsure_phrases
                    ):
                        # Ensure answer is a string (handle AIMessage or other types)
                        if hasattr(general_answer, "content"):
                            answer = general_answer.content
                        else:
                            answer = str(general_answer)
                except Exception:
                    pass
        answer_header = (
            color_text("\nAssistant:", Fore.MAGENTA + Style.BRIGHT)
            if COLORAMA
            else "\nAssistant:"
        )
        answer_body = color_text(answer, Fore.YELLOW) if COLORAMA else answer
        print(answer_header)
        print(answer_body)

    if not COLORAMA:
        print(
            "\nFor a more colorful experience, install the 'colorama' package: pip install colorama"
        )


if __name__ == "__main__":
    main()
