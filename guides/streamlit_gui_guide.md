# Streamlit Web GUI Guide for Vyaguta Assistant Chatbot

## What is Streamlit?

[Streamlit](https://streamlit.io/) is an open-source Python framework for building fast, interactive web apps for data science and machine learning projects. It lets you turn Python scripts into shareable web apps with minimal code.

## Why use Streamlit for this chatbot?

- No frontend coding required (no HTML/CSS/JS)
- Real-time, interactive UI for chat
- Easy to deploy and share
- Supports widgets, markdown, and custom styling

---

## How to Set Up and Use the Streamlit GUI

### 1. Install Streamlit

If you haven't already, install Streamlit (preferably inside your virtual environment):

```bash
pip install streamlit
```

Or, if using requirements.txt:

```bash
pip install -r requirements.txt
```

### 2. Run the GUI

From your project directory, run:

```bash
streamlit run chatbot_gui.py
```

- The web app will open in your browser.
- Enter your OpenAI API key in the sidebar (or set it in your `.env` file).
- Select the model if needed.
- Chat history and assistant responses are shown with clear styling.

---

## Virtual Environment (venv) Best Practice

A virtual environment (venv) is a self-contained directory for Python and its packages, isolated from your system Python. This avoids conflicts and keeps dependencies organized.

### How to use venv:

1. **Create a venv** (once per project):
   ```bash
   python3 -m venv .venv
   ```
2. **Activate the venv** (every session):
   ```bash
   source .venv/bin/activate
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Run scripts** (while venv is active):
   ```bash
   streamlit run chatbot_gui.py
   # or
   python main.py
   ```
5. **Deactivate when done:**
   ```bash
   deactivate
   ```

---

## Troubleshooting

- If you see missing module errors, ensure your venv is activated and dependencies are installed.
- If Streamlit does not open automatically, copy the local URL from the terminal and open it in your browser.
- For API key issues, check your `.env` file or enter the key in the sidebar.

---

For more, see the [Streamlit documentation](https://docs.streamlit.io/).
