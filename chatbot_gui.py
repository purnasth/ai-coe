"""
Vyaguta Assistant Chatbot - Streamlit GUI

Features:
- Modern, visually appealing chat UI
- Chat history with scrollable area
- User/assistant message styling with avatars and color contrast
- Input box with submit button or Enter
- Sidebar for branding only (no settings)
- Modular, clean code with comments

Run with: streamlit run chatbot_gui.py
"""

import os
import streamlit as st
from main import qa_chain, get_llm, OPENAI_API_KEY

# --- Sidebar: Enhanced features ---
with st.sidebar:
    st.image(
        "https://vyaguta.lftechnology.com/assets/logo.png",
        width=160,
        caption="Vyaguta Assistant",
    )
    st.markdown(
        """
        <div style='margin-top: 1em; color: #888; font-size: 0.95em;'>
        Powered by <b>Vyaguta RAG + OpenAI</b>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("---")
    st.header("🛠️ Options")
    # Theme toggle (light/dark)
    theme = st.radio("Theme", ["Light", "Dark"], index=0, horizontal=True)
    # Chat history controls
    if st.button("🧹 Clear Chat History", use_container_width=True):
        st.session_state["messages"] = []
        st.rerun()
    st.markdown("---")
    st.header("ℹ️ Info & Help")
    st.markdown(
        """
    - [Streamlit GUI Guide](guides/streamlit_gui_guide.md)
    - [Vyaguta Portal](https://vyaguta.lftechnology.com/)
    - [Vyaguta Wiki](https://lftechnology.atlassian.net/wiki/spaces/VYAGUTA/overview)
    """
    )
    st.markdown("---")
    st.caption("© 2025 Leapfrog Technology | Chatbot by Vyaguta Team")
api_key = OPENAI_API_KEY
model = "gpt-4.1-nano"

# --- Session state for chat history ---
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# --- Chat header ---
st.markdown(
    """
    <div style='display:flex;align-items:center;gap:12px;margin-bottom:0.5em;'>
        <img src='https://i.pinimg.com/736x/eb/c5/14/ebc514a4277e415c3be66363a1ba8ff0.jpg' width='48' style='border-radius:8px;'>
        <span style='font-size:2.1em;font-weight:700;color:#008000;'>Vyaguta Chatbot</span>
    </div>
    <hr style='margin-bottom:1.2em;'>
    """,
    unsafe_allow_html=True,
)

# --- Chat history display ---
chat_container = st.container()
with chat_container:
    for msg in st.session_state["messages"]:
        if msg["role"] == "user":
            st.markdown(
                f"""
<div style='display:flex;align-items:flex-start;gap:10px;margin-bottom:8px;'>
  <div style='background:#1976d2;color:#fff;width:38px;height:38px;display:flex;align-items:center;justify-content:center;border-radius:50%;font-size:1.3em;'>🧑</div>
  <div style='background:#e3f2fd;color:#000;padding:12px 16px;border-radius:12px 12px 12px 4px;max-width:80%;box-shadow:0 1px 4px #1976d220;'>
    <b>You:</b> {msg['content']}
  </div>
</div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
<div style='display:flex;align-items:flex-start;gap:10px;margin-bottom:8px;'>
  <div style='background:#ff9800;color:#fff;width:38px;height:38px;display:flex;align-items:center;justify-content:center;border-radius:50%;font-size:1.3em;'>🤖</div>
  <div style='background:#fff8e1;color:#000;padding:12px 16px;border-radius:12px 12px 4px 12px;max-width:90%;box-shadow:0 1px 4px #ff980020;'>
    <b>Assistant:</b> {msg['content']}
  </div>
</div>
                """,
                unsafe_allow_html=True,
            )

# --- Input box ---
st.markdown("<div style='margin-top:1.5em;'></div>", unsafe_allow_html=True)
user_input = st.text_area(
    "Type your message and press Send...",
    key="input",
    height=60,
    placeholder="Ask anything about Vyaguta onboarding, policies, people, etc.",
)
submit = st.button("Send", use_container_width=True)


# --- Handle input and response ---
def get_response(question, api_key, model):
    
    llm = get_llm(api_key)

    result = qa_chain.invoke({"query": question})
    return result["result"]


if submit and user_input.strip():
    st.session_state["messages"].append({"role": "user", "content": user_input})
    with st.spinner("Assistant is typing..."):
        try:
            answer = get_response(user_input, api_key, model)
        except Exception as e:
            answer = f"Error: {e}"
    st.session_state["messages"].append({"role": "assistant", "content": answer})
    st.rerun()
