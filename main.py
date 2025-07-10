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
import re
import difflib


def load_api_key() -> str:
    """
    Loads the OpenAI API key from environment variables.

    Returns:
        str: The OpenAI API key.
    """
    load_dotenv()
    return os.getenv("OPENAI_API_KEY")


OPENAI_API_KEY = load_api_key()


# --- Enhanced Markdown Chunking for Fine-Grained RAG ---
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain.text_splitter import MarkdownHeaderTextSplitter


def load_onboarding_docs(directories=None):
    """
    Loads onboarding documentation from the specified directories, chunked by headings and lists for fine-grained retrieval.
    Args:
        directories (list or None): List of directories containing onboarding docs. If None, defaults to ["docs", "docs-confluence"].
    Returns:
        list: List of loaded and chunked documents.
    """
    import glob

    if directories is None:
        directories = ["docs", "docs-confluence"]
    all_docs = []
    for directory in directories:
        for file in glob.glob(f"{directory}/*.md"):
            loader = UnstructuredMarkdownLoader(file)
            doc = loader.load()
            splitter = MarkdownHeaderTextSplitter(
                headers_to_split_on=[
                    ("#", "Header 1"),
                    ("##", "Header 2"),
                    ("###", "Header 3"),
                    ("####", "Header 4"),
                ]
            )
            chunks = splitter.split_text(doc[0].page_content)
            for chunk in chunks:
                all_docs.append(chunk)
    return all_docs


from people import (
    fetch_people_data,
    get_person_info_from_question,
    is_people_query,
    generate_people_docs,
)
from langchain_core.documents import Document


docs = load_onboarding_docs()

# --- Add people data to RAG context as Document objects ---
people_data = fetch_people_data()
people_docs = [Document(page_content=doc) for doc in generate_people_docs(people_data)]
docs.extend(people_docs)


# --- Enhanced Retriever: Keyword + Semantic Hybrid ---
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import EmbeddingsFilter


def create_retriever(docs):
    """
    Embeds documents and creates a hybrid retriever for RAG, using both semantic and keyword matching for robust detail retrieval.

    Args:
        docs (list): List of documents to embed.
    Returns:
        retriever: Retriever object for document search.
    """
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(docs, embeddings)
    base_retriever = vectorstore.as_retriever()
    # Add a filter to boost keyword matches (for exact rules/steps)
    compressor = EmbeddingsFilter(embeddings=embeddings, similarity_threshold=0.3)
    hybrid_retriever = ContextualCompressionRetriever(
        base_compressor=compressor, base_retriever=base_retriever
    )
    return hybrid_retriever


retriever = create_retriever(docs)


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


# --- Promotion Data Parsing ---
def parse_promotions_md(filepath="docs/promotions.md"):
    """
    Parses the promotions markdown file and returns a list of promotion records.
    Returns: List of dicts: { 'from': str, 'to': str, 'name': str, 'department': str }
    """
    promotions = []
    current_dept = None
    with open(filepath, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            dept_match = re.match(r"^## +(.+)$", line)
            if dept_match:
                current_dept = dept_match.group(1)
                continue
            promo_match = re.match(r"^- ([^→]+)→ ([^:]+): (.+)$", line)
            if promo_match and current_dept:
                from_pos = promo_match.group(1).strip()
                to_pos = promo_match.group(2).strip()
                name = promo_match.group(3).strip()
                promotions.append(
                    {
                        "from": from_pos,
                        "to": to_pos,
                        "name": name,
                        "department": current_dept,
                    }
                )
    return promotions


PROMOTIONS = parse_promotions_md("docs/promotions.md")


def normalize_name(name):
    """Normalize a name for strict, case-insensitive comparison (collapse spaces, lower)."""
    return " ".join(name.lower().split())


def find_person_promotions(name_query, promotions):
    nq = " ".join(name_query.lower().split())
    # Only allow exact full name match; all other queries should fall back to RAG
    exact = [p for p in promotions if nq == " ".join(p["name"].lower().split())]
    if exact:
        return exact, False  # False = not ambiguous
    # If no exact match, let RAG handle the query
    return [], False


def answer_promotion_query(question: str, promotions: list) -> str | None:
    """
    Answers fact-based promotion queries deterministically from parsed data.
    Returns answer string if matched, else None.
    """
    q = question.lower().strip()
    # 1. Did <name> get promoted in Q3 2025?
    m = re.match(r"did ([a-zA-Z .'-]+) got? promoted( in q3 2025)?\??", q)
    if m:
        name = m.group(1).strip()
        found, ambiguous = find_person_promotions(name, promotions)
        if found:
            if len(found) == 1:
                p = found[0]
                return f"Yes, {p['name']} was promoted from {p['from']} to {p['to']} in {p['department']} in Q3 2025."
            elif ambiguous and len(found) > 1:
                lines = [
                    f"[{i+1}] {p['name']}: {p['from']} → {p['to']} in {p['department']} in Q3 2025."
                    for i, p in enumerate(found)
                ]
                return f"{len(found)} results found for '{name}':\n" + "\n".join(lines)
        else:
            return f"No, {name.title()} was not promoted in Q3 2025."
    # 2. How many people got promoted in Q3 2025?
    if re.match(
        r"how many (people|employees|leapfroggers)? ?got promoted( in q3 2025)?\??", q
    ):
        return f"A total of {len(promotions)} people were promoted in Q3 2025."
    # 3. List all promotions in <department>
    m = re.match(r"list (all )?promotions in ([a-zA-Z &-]+)", q)
    if m:
        dept = m.group(2).strip().lower()
        found = [p for p in promotions if dept in p["department"].lower()]
        if found:
            lines = [f"{p['name']}: {p['from']} → {p['to']}" for p in found]
            return f"Promotions in {m.group(2).title()} in Q3 2025:\n" + "\n".join(
                lines
            )
        else:
            return f"No promotions found in {m.group(2).title()} for Q3 2025."
    # 4. Who got promoted to <position>?
    m = re.match(r"who got promoted to ([a-zA-Z ,&-]+)\??", q)
    if m:
        to_pos = m.group(1).strip().lower()
        found = [p for p in promotions if to_pos in p["to"].lower()]
        if found:
            lines = [
                f"{p['name']} ({p['department']}): {p['from']} → {p['to']}"
                for p in found
            ]
            return f"Promoted to {m.group(1).title()} (Q3 2025):\n" + "\n".join(lines)
        else:
            return f"No one was promoted to {m.group(1).title()} in Q3 2025."
    # 5. Who got promoted from <position>?
    m = re.match(r"who got promoted from ([a-zA-Z ,&-]+)\??", q)
    if m:
        from_pos = m.group(1).strip().lower()
        found = [p for p in promotions if from_pos in p["from"].lower()]
        if found:
            lines = [
                f"{p['name']} ({p['department']}): {p['from']} → {p['to']}"
                for p in found
            ]
            return f"Promoted from {m.group(1).title()} (Q3 2025):\n" + "\n".join(lines)
        else:
            return f"No one was promoted from {m.group(1).title()} in Q3 2025."
    # 6. List all promotions (all departments)
    if re.match(r"list (all )?promotions( in q3 2025)?\??", q):
        lines = [
            f"{p['name']} ({p['department']}): {p['from']} → {p['to']}"
            for p in promotions
        ]
        return "Promotions in Q3 2025:\n" + "\n".join(lines)
    return None


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

        # --- PROMOTION QUERIES ---
        promo_answer = answer_promotion_query(question, PROMOTIONS)
        if promo_answer is not None:
            answer_header = (
                color_text("\nAssistant:", Fore.MAGENTA + Style.BRIGHT)
                if COLORAMA
                else "\nAssistant:"
            )
            answer_body = (
                color_text(promo_answer, Fore.YELLOW) if COLORAMA else promo_answer
            )
            print(answer_header)
            print(answer_body)
            continue  # Never fall back to LLM for promotion queries!

        # Use people.py for people-related queries (all logic encapsulated)
        if is_people_query(question):
            person_answer = get_person_info_from_question(question, people_data)
            if person_answer is not None:
                answer_header = (
                    color_text("\nAssistant:", Fore.MAGENTA + Style.BRIGHT)
                    if COLORAMA
                    else "\nAssistant:"
                )
                answer_body = (
                    color_text(person_answer, Fore.YELLOW)
                    if COLORAMA
                    else person_answer
                )
                print(answer_header)
                print(answer_body)
                continue

        # Otherwise, use the RAG pipeline first
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
