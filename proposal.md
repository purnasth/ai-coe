# Vyaguta Onboarding Assistant Chatbot Proposal

## Overview

This project is an AI-powered onboarding assistant chatbot for Vyaguta, Leapfrog Technology’s **Enterprise Resource Planning (ERP)** system. Vyaguta is used to manage day-to-day business activities such as **Employee Management, Project Management, Resource Management, Evaluation, and Employee Appreciation**. As a business management software, Vyaguta collects, stores, manages, and interprets data from organizational activities. The chatbot will help new hires and users quickly understand Vyaguta’s modules (**Core, Teams, Attendance, Jump, Honor, OKR, Pulse** & many more) and procedures by answering natural language questions. The goal is to streamline onboarding, reduce support overhead, and make information easily accessible.

## Problem Statement

Vyaguta is a comprehensive and complex platform with many modules and features. New hires and even existing employees often struggle to find information about how to use specific modules or complete common tasks. This leads to a steep learning curve, increased onboarding time, and frequent support requests. Without an easy way to access guidance, productivity and user satisfaction are negatively impacted.

## Solution

The solution is a chatbot that leverages **prompt engineering**, **Retrieval-Augmented Generation (RAG)**, and **LangChain** to answer user questions about Vyaguta. Users can ask questions like **“How do I request leave?”**, **“What is OKR?”**, or **“How does Pulse work?”** and receive clear, concise answers. The chatbot will:

- Use **prompt engineering** to handle common queries and guide user interactions.
- Employ **LangChain** and **RAG** to retrieve relevant information from internal documentation, onboarding guides, and FAQs.
- Be easily extensible to cover new modules or procedures as Vyaguta evolves.

This assistant will significantly reduce onboarding time, empower users to self-serve, and free up HR and support resources for higher-value tasks.

---

## Architecture & Workflow

The Vyaguta Onboarding Assistant Chatbot uses:

- **LLM (Large Language Model):** For natural language understanding and response generation.
- **RAG (Retrieval-Augmented Generation):** To fetch relevant information from internal documentation.
- **LangChain:** To orchestrate the workflow between user queries, retrieval, and LLM responses.

**Workflow Diagram:**

```mermaid
flowchart TD
    A[User Query] --> B[LangChain Orchestration]
    B --> C{RAG: Retrieve Relevant Docs}
    C --> D[Internal Docs/FAQs]
    C --> E[Onboarding Guides]
    D --> F[LLM (OpenAI/GPT)]
    E --> F
    F --> G[Chatbot Response]
    B --> F
```

[Edit or view this diagram online](https://mermaid.live/)

---

## Tech Stacks Used

- **Web Development:** Full Stack
- **AI Integration:** OpenAI API (REST)
- **Database:** PostgreSQL (with full-text search)
- **Other:** Mermaid (for diagrams), Markdown

---
