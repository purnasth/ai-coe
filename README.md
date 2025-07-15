# Vyaguta Onboarding Assistant Chatbot (Python + LangChain + RAG)

This is a minimal terminal-based MVP for the Vyaguta onboarding assistant chatbot, now using Python, LangChain, and OpenAI.

## Structure

- `chatbot/` — Contains all code for the chatbot (run in terminal for now)
- `docs/` — Place onboarding docs/FAQs here (plain text/markdown)

## Prerequisites

- Python 3.10+
- [Poetry](https://python-poetry.org/) (recommended) or pip
- OpenAI API key

## Setup

1. Install dependencies:
   ```bash
   cd chatbot
   poetry install
   # or, if using pip:
   pip install -r requirements.txt
   # If you see missing module errors, also run:
   pip install langchain-community langchain-openai faiss-cpu
   ```
2. Add your onboarding docs/FAQs to `docs/` (already present).
3. Create a `.env` file in `chatbot/`:
   ```env
   OPENAI_API_KEY=your-openai-api-key
   ```
4. Run the chatbot in the terminal:
   ```bash
   poetry run python main.py
   # or, if using pip:
   python main.py
   ```

---

## Sample Inputs and Expected Outputs

### Example 1

**Input:**

```
How do I request leave?
```

**Expected Output:**

```
Answer: To request leave in Vyaguta:
1. Go to the Attendance module.
2. Click on 'Request Leave'.
3. Fill in the required details and submit.
```

### Example 2

**Input:**

```
What is OKR?
```

**Expected Output:**

```
Answer: OKR stands for Objectives and Key Results. It is a goal-setting framework used in Vyaguta to align individual and team objectives with company goals.
```

### Example 3

**Input:**

```
How does Pulse work?
```

**Expected Output:**

```
Answer: Pulse is Vyaguta's feedback and engagement tool. Employees can give and receive feedback, and management can monitor engagement trends.
```

### To exit

Type:

```
exit
```

---

## Pulse

Vyaguta Pulse flow starts with the creation of a Pulse profile after an individual is onboarded to their respective Area within Leapfrog. A Pulse profile accumulates the timeline of a Leapfrogger’s journey and growth at Leapfrog. The Pulse process involves multiple parties (POps, Appraisee, Appraiser/Co-appraiser, Team Manager, Leapfroggers, Project Leader, Spearheads) and includes steps like Expectation Setting, Self-reflection, Feedback, Promotion/Performance Improvement Plan, Ask for Help, and Pulse Walkthrough.

Pulse is designed to foster a culture of continuous feedback, align progress towards set expectations, and focus on performance development through regular check-ins and feedback cycles. The process is detailed and involves quarterly cycles, performance improvement plans, and integration with annual evaluations.

---

## Sample Inputs and Expected Outputs (Pulse)

### Example 4

**Input:**

```
What is Vyaguta Pulse?
```

**Expected Output:**

```
[AI Answer]: Vyaguta Pulse is a feedback-based development system introduced for the growth and development of individuals through continuous quarterly check-ins between the Appraiser and the Appraisee on the basis of predefined and agreed set of expectations. Its objective is to foster a culture of continuous feedback and align progress towards set expectations.
```

### Example 5

**Input:**

```
Who can be placed under Performance Improvement Plan (PIP) in Pulse?
```

**Expected Output:**

```
[AI Answer]: All full time/part time employees at Leapfrog including fixed term, probation, and permanent employees are within the scope of being placed in Performance Improvement Plan (PIP).
```

### Example 6

**Input:**

```
How does feedback work in Pulse?
```

**Expected Output:**

```
[AI Answer]: Feedback in Pulse is given by the Appraiser on the Appraisee's achievements, updates, or tasks. The Appraisee can reply or comment, and the conversation continues. Feedback can be given at any point during the quarter, at the end of a project, or during project transfer. The goal is to have more feedback loops for continuous assessment.
```

### Example 7

**Input:**

```
What happens if expectations set in Pulse are not met?
```

**Expected Output:**

```
[AI Answer]: If expectations set in Pulse are not met, the Appraiser may place the Appraisee under a Performance Improvement Plan (PIP) for closer observation and support to help them meet the required expectations.
```

### Example 8

**Input:**

```
How is quarterly feedback used in the annual performance evaluation?
```

**Expected Output:**

```
[AI Answer]: The summary feedback of all quarters recorded in Pulse is used during the Annual Performance Evaluation. This removes the need to revisit every feedback given throughout the year, as the summary is auto-reflected for the final evaluation.
```

---

## What is a Python Virtual Environment (venv)?

A virtual environment (venv) is a self-contained directory that contains its own Python installation and packages, isolated from the global Python environment. This helps you avoid conflicts between projects and keeps dependencies organized—similar to how `node_modules` works in React projects.

## Setting Up and Using venv

1. **Create a virtual environment** (only once per project):

   ```bash
   python3 -m venv .venv
   ```

   This creates a `.venv` folder in your project directory.

2. **Activate the virtual environment** (every time you start work):

   ```bash
   source .venv/bin/activate
   ```

   Your terminal prompt will change to show you are in the venv.

3. **Install dependencies** (inside the activated venv):

   ```bash
   python3 -m pip install -r requirements.txt
   ```

   This installs all required packages locally to `.venv`.

4. **Run your scripts** (while venv is activated):

   ```bash
   python3 main.py
   # or any other script
   ```

5. **Deactivate the environment** (when done):
   ```bash
   deactivate
   ```

### Why use venv?

- Keeps dependencies isolated per project
- Prevents version conflicts
- Makes your project reproducible for others
- Easy to clean up (just delete `.venv`)

### Note on global packages

You do not need to delete global packages for your project to work with venv. Your code will use the packages installed in `.venv` when activated. If you want to clean up your global environment, you can uninstall packages globally, but it is optional.

---

This MVP demonstrates the core GenAI, LangChain, and RAG concepts from your course syllabus.
