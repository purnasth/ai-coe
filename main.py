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
import time
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from auth import app_startup
from rag_pipeline import setup_rag_pipeline
from log_utils import debug_log, output_log


# --- Authenticate and refresh Vyaguta access token at startup ---
debug_log("Starting authentication (app_startup)")
app_startup()
debug_log("Authentication complete")

# --- Setup RAG pipeline with Chroma retriever ---
debug_log("Setting up RAG pipeline")
retriever = setup_rag_pipeline(
    ["docs", "docs-api/people", "docs-confluence"], force_rebuild=False
)
debug_log("RAG pipeline setup complete")


def load_api_key() -> str:
    """
    Loads the OpenAI API key from environment variables.

    Returns:
        str: The OpenAI API key.
    """
    debug_log("Loading OpenAI API key")
    load_dotenv()
    key = os.getenv("OPENAI_API_KEY")
    debug_log("Loaded OpenAI API key")
    return key


OPENAI_API_KEY = load_api_key()


def get_prompt_template() -> PromptTemplate:
    """
    Returns a prompt template for the onboarding assistant, instructing the LLM to quote or summarize exact steps, rules, or lists from the markdown context.
    If there are multiple people with the same name, list all of them with their details. For multiple matches, start your answer with a phrase like: "There are X people named Y:" and then list each one. For a single match, answer as usual.
    """
    return PromptTemplate(
        template="""
You are Vyaguta's assistant. Use the provided context to answer user questions about Vyaguta's modules, features, onboarding procedures, tools, policies, coding guidelines, and any information available about Vyaguta and Leapfrog.

When answering about a person:
- For general introduction queries (e.g., "Who is Purna?"), always respond in the following format:
  "{{Full Name}} is a {{Designation}} at Leapfrog Technology, currently working in the {{Department}} department. They joined the company on {{Join Date}} and contribute within the {{Area}}. Based in {{Address}}, {{Full Name}} is a {{Scheduled Type}} team member working {{Working Shift}}. You can reach {{him/her}} via email at {{Email}} or on mobile at {{Mobile Phone}}."
- Summarize skills and qualities briefly (e.g., "recognized for technical aptitude, creative mindset, and collaborative spirit").
- Do not include employee ID, contract type, GitHub ID, or other details unless specifically requested.
- If the user asks for detailed information, provide those details in a readable format, using all available data from the context.
- If the query matches multiple people, start with: "There are X people named Y:" only if X > 1, and list each with their introduction as above.
- If the query matches exactly one person, simply introduce them as above.
- If no matches are found, politely say you do not have information about that person.

If the user asks about the creator or author of Vyaguta Assistant Chatbot (the assistant itself), answer with:
"Vyaguta Assistant Chatbot was created by Purna Bahadur Shrestha, Associate Software Engineer at Leapfrog Technology. You can reach him at purnashrestha@lftechnology.com."

If you are unsure or cannot find the answer in the provided context, politely say you are not sure or do not know. If you have already told the user you do not know for a similar question before, then suggest they visit these official resources for more information:
- Vyaguta Portal: https://vyaguta.lftechnology.com/
- Vyaguta Wiki: https://lftechnology.atlassian.net/wiki/spaces/VYAGUTA/overview

PROMOTION YEAR/QUARTER INSTRUCTIONS (IMPORTANT):
If the user asks about promotions in a year (e.g., "Did anyone get promoted in 2025?"), and the context contains promotions for specific quarters of that year (e.g., Q3 2025), you MUST:
- Treat all quarters in that year as part of the year and use all available quarter data to answer.
- If only some quarters are present, answer based on those and EXPLICITLY state in your answer which quarters are available and that you are providing information for those quarters only.
- Always explain this mapping from year to quarters in your answer, e.g., "The following promotions are for Q3 2025, which is part of 2025."
- If data is incomplete for the year, add a disclaimer such as "This may not include all promotions for 2025, only those for the available quarters."
- List the relevant promotions if possible, citing your sources.

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
    debug_log("Initializing LLM")
    llm = ChatOpenAI(openai_api_key=api_key, temperature=0.2, model="gpt-4.1-nano")
    debug_log("LLM initialized")
    return llm


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
    debug_log("Building QA chain")
    chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt},
        return_source_documents=True,
    )
    debug_log("QA chain built")
    return chain


qa_chain = build_qa_chain(llm, retriever, prompt)


def main():
    """
    Runs the Vyaguta Assistant Chatbot in a terminal chat loop.
    """
    debug_log("Entering main chat loop")
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
        debug_log("Waiting for user input")
        question = input(user_prompt)
        debug_log(f"User input: {question}")
        if question.strip().lower() == "exit":
            break
        debug_log("Invoking QA chain")
        result = qa_chain.invoke({"query": question})
        debug_log("QA chain invocation complete")
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

        # ---
        # Show sources for every answer (with debug info)
        source_docs = result.get("source_documents", [])
        debug_log(f"source_documents: {source_docs}")
        sources = set()
        for doc in source_docs:
            meta = getattr(doc, "metadata", {})
            src = meta.get("source")
            if src:
                # Normalize to top-level folder (docs, docs-api, docs-confluence, etc.)
                src_folder = src.split("/")[0]
                sources.add(src_folder)
        env = os.getenv("ENV", "local").lower()
        if env != "production":
            if sources:
                sources_str = ", ".join(sorted(sources))
                answer += f"\n\n[SOURCE: {sources_str}]"
            else:
                answer += "\n\n[SOURCE: Unknown]"

        answer_header = (
            color_text("\nAssistant:", Fore.MAGENTA + Style.BRIGHT)
            if COLORAMA
            else "\nAssistant:"
        )
        answer_body = color_text(answer, Fore.YELLOW) if COLORAMA else answer
        debug_log("Answer ready, printing to user")
        print(answer_header)
        print(answer_body)

    if not COLORAMA:
        print(
            "\nFor a more colorful experience, install the 'colorama' package: pip install colorama"
        )


if __name__ == "__main__":
    main()
