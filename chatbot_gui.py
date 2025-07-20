"""
Vyaguta Assistant Chatbot - Premium Streamlit GUI

Features:
- Modern glassmorphism design with gradients
- Advanced chat UI with typing animations
- Message reactions and feedback system
- Chat export functionality
- Voice input simulation
- Advanced settings panel
- Beautiful animations and transitions
- Responsive design
- Message search and filtering
- Chat statistics
- Custom themes
- Message actions (copy, delete, edit)

Run with: streamlit run chatbot_gui.py
"""

import os
import json
import time
import datetime
import streamlit as st
from main import qa_chain, get_llm, OPENAI_API_KEY

# --- Page Configuration ---
st.set_page_config(
    page_title="Vyaguta AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Custom CSS for Premium UI ---
with open("streamlit.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --- Initialize Session State ---
if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "chat_sessions" not in st.session_state:
    st.session_state["chat_sessions"] = {}

if "current_session" not in st.session_state:
    st.session_state["current_session"] = "default"

if "user_preferences" not in st.session_state:
    st.session_state["user_preferences"] = {
        "theme": "Modern",
        "message_reactions": True,
        "typing_animation": True,
        "sound_effects": False,
    }

if "message_stats" not in st.session_state:
    st.session_state["message_stats"] = {
        "total_messages": 0,
        "user_messages": 0,
        "assistant_messages": 0,
        "session_start": datetime.datetime.now(),
    }

# --- Sidebar ---
with st.sidebar:
    st.markdown(
        """
    <div class='sidebar-header'>
        <img src='https://vyaguta.lftechnology.com/favicon.ico' class='sidebar-logo'>
        <h3 class='sidebar-title'>Vyaguta AI</h3>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # --- Search Messages (moved from main content) ---
    search_term = st.text_input(
        "Search Messages",
        placeholder="Search your chat history...",
        key="sidebar_search_term",
    )

    # --- Chat Sessions ---
    if st.button("New Chat", use_container_width=True, type="primary"):

        st.session_state["messages"] = []
        st.rerun()

    # Session selector
    # if st.session_state["chat_sessions"]:
    #     selected_session = st.selectbox(
    #         "Load Session",
    #         options=list(st.session_state["chat_sessions"].keys()),
    #         index=(
    #             0
    #             if st.session_state["current_session"]
    #             in st.session_state["chat_sessions"]
    #             else 0
    #         ),
    #     )

    #     if st.button("📂 Load Selected", use_container_width=True):
    #         st.session_state["current_session"] = selected_session
    #         st.session_state["messages"] = st.session_state["chat_sessions"][
    #             selected_session
    #         ].copy()
    #         st.rerun()

    # st.markdown("---")

    # --- Quick Actions ---
    # st.markdown("### ⚡ Quick Actions")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Clear", use_container_width=True, type="secondary"):
            st.session_state["messages"] = []
            st.rerun()

    with col2:
        if st.button("Export", use_container_width=True, type="secondary"):
            chat_data = {
                "session": st.session_state["current_session"],
                "messages": st.session_state["messages"],
                "exported_at": datetime.datetime.now().isoformat(),
            }
            st.download_button(
                "💾 Download JSON",
                data=json.dumps(chat_data, indent=2),
                file_name=f"vyaguta_chat_{st.session_state['current_session']}_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.json",
                mime="application/json",
                use_container_width=True,
            )

    # --- Statistics ---
    # st.markdown("---")
    # st.markdown("### 📊 Chat Statistics")

    stats = st.session_state["message_stats"]

    st.markdown(
        f"""
    <div class='stat-card'>
        <h4>{len(st.session_state['messages'])}</h4>
        <p>Total Messages</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    user_msgs = len([m for m in st.session_state["messages"] if m["role"] == "user"])
    assistant_msgs = len(
        [m for m in st.session_state["messages"] if m["role"] == "assistant"]
    )

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            f"""
        <div class='stat-card'>
            <h5 style='color: #3a8dff;'>{user_msgs}</h5>
            <p>You</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
        <div class='stat-card'>
            <h5 style='color: #ff75c2;'>{assistant_msgs}</h5>
            <p>AI</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    # st.markdown("---")

    # Model selection
    # model_option = st.selectbox(
    #     "🤖 AI Model", ["gpt-4.1-nano", "gpt-3.5-turbo", "gpt-4"], index=0
    # )
    model_option = "gpt-4.1-nano"

    # # Temperature slider
    # temperature = st.slider(
    #     "🌡️ Response Creativity",
    #     min_value=0.0,
    #     max_value=1.0,
    #     value=0.7,
    #     step=0.1,
    #     help="Higher values make responses more creative",
    # )

    st.markdown("---")

    # --- Help & Info ---
    st.markdown("### Information")

    with st.expander("Features"):
        st.markdown(
            """
        <ul class="sidebar-small-list">
            <li>Smart AI Assistant powered by OpenAI</li>
            <li>Beautiful & Intuitive UI</b></li>
            <li>Export Chats - Download as JSON</li>
            <li>Real-time Stats - Track your conversations</li>
            <li>Responsive Design - Works on all devices</li>
        </ul>
        """,
            unsafe_allow_html=True,
        )

    with st.expander("Quick Links"):
        st.markdown(
            """
        <ul class="sidebar-small-list">
            <li><a href="https://vyaguta.lftechnology.com/" target="_blank">Vyaguta Portal</a></li>
            <li><a href="https://lftechnology.atlassian.net/wiki/spaces/VYAGUTA/overview" target="_blank">Company Wiki</a></li>
            <li><a href="https://lftechnology.slack.com/archives/CDUAPJSM9" target="_blank">Vyaguta Help</a></li>
        </ul>
        """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
    <div style='text-align: center; padding: 1rem; background: rgba(255, 255, 255, 0.05); border-radius: 10px; margin-top: 1rem;'>
        <p style='color: rgba(255, 255, 255, 0.6); font-size: 0.8rem; margin: 0;'>
        © 2025 Leapfrog Technology<br>
        Vyaguta AI Assistant v2.0
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

# --- Main Content ---
# Header
st.markdown(
    """
<div class='main-header'>
     <div class='main-title'>
        <img src='https://vyaguta.lftechnology.com/favicon.ico' class='sidebar-logo'>
        <h3 class='sidebar-title'>Vyaguta AI</h3>
    </div>
    <p class='main-subtitle'>Your intelligent companion for Vyaguta onboarding & support</p>
</div>
""",
    unsafe_allow_html=True,
)


# Filter messages if search term exists (now uses sidebar value)
display_messages = st.session_state["messages"]
if (
    "sidebar_search_term" in st.session_state
    and st.session_state["sidebar_search_term"]
):
    search_term = st.session_state["sidebar_search_term"]
    display_messages = [
        msg
        for msg in st.session_state["messages"]
        if search_term.lower() in msg["content"].lower()
    ]

# # --- Chat Display ---
# st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Welcome message
if not st.session_state["messages"]:
    st.markdown(
        """
    <div class='assistant-message'>
        <div class='avatar assistant-avatar'>
            <img src='https://vyaguta.lftechnology.com/favicon.ico' alt='Assistant Avatar' class='assistant-avatar-img'/>
            </div>
        <div class='assistant-bubble'>
            <strong>Welcome to Vyaguta AI Assistant! 👋</strong><br><br>
            I'm here to help you with:
            <ul class='assistant-welcome-list'>
                <li>🚀 Onboarding processes and procedures</li>
                <li>📋 Company policies and guidelines</li>
                <li>👥 Team information and contacts</li>
                <li>🛠️ Tools and resources</li>
                <li>❓ General questions about Vyaguta</li>
            </ul>
            Feel free to ask me anything!
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

# Display messages
for i, msg in enumerate(display_messages):
    if msg["role"] == "user":
        st.markdown(
            f"""
        <div class='user-message'>
            <div class='user-bubble'>
                {msg['content']}
                <!--
                <div class='message-actions'>
                    <small style='opacity: 0.7;'>
                        {msg.get('timestamp', 'Just now')} • 
                        <a href='#' onclick='navigator.clipboard.writeText("{msg["content"][:50]}...")'>Copy</a>
                    </small>
                </div>
                -->
            </div>
            <div class='avatar user-avatar'>
            <img src='https://avatars.githubusercontent.com/u/107195487?s=400&u=6120358cdcf760f65cfda7f81e982dfb1d8f7a27&v=4' alt='User Avatar' class='user-avatar-img'/>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )
    else:
        # Message reactions
        reactions = msg.get("reactions", {})
        reaction_display = " ".join(
            [f"{emoji} {count}" for emoji, count in reactions.items() if count > 0]
        )

        # Format timestamp to 12-hour format with am/pm
        timestamp_val = msg.get("timestamp", "Just now")
        if timestamp_val not in ["Just now", None, ""]:
            try:
                dt = datetime.datetime.strptime(timestamp_val, "%H:%M")
                timestamp_12hr = dt.strftime("%-I:%M%p").lower()
            except Exception:
                timestamp_12hr = timestamp_val
        else:
            timestamp_12hr = timestamp_val

        st.markdown(
            f"""
        <div class='assistant-message'>
            <div class='avatar assistant-avatar'>
            <img src='https://vyaguta.lftechnology.com/favicon.ico' alt='Assistant Avatar' class='assistant-avatar-img'/>
            </div>
            <div class='assistant-bubble'>
             {msg['content']}
                <div class='message-actions'>
                    <small style='opacity: 0.7;'>
                        {timestamp_12hr}
                        <a href='#' onclick='navigator.clipboard.writeText("{msg["content"][:50]}...")'>
                        <img src='https://cdn-icons-png.flaticon.com/512/1621/1621635.png' 
                        alt="Copy"
                        class="copy-icon"
                        />
                        Copy </a>
                    </small>
                </div>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

st.markdown("</div>", unsafe_allow_html=True)

# --- Input Area ---
# st.markdown('<div class="input-container">', unsafe_allow_html=True)


st.markdown('<div class="centered-input-area">', unsafe_allow_html=True)

# --- Surprise/Quick Question Input Handling ---
if "surprise_question" in st.session_state:
    default_user_input = st.session_state.pop("surprise_question")
    st.session_state["auto_send_surprise"] = True
else:
    default_user_input = ""

# --- Quick Questions Selectbox Reset Logic (must be BEFORE widget instantiation) ---
if st.session_state.pop("reset_quick_questions", False):
    st.session_state["quick_questions_selectbox"] = "Quick Questions"
    st.rerun()

input_outer_col1, input_outer_col2, input_outer_col3 = st.columns([1, 4, 1])
with input_outer_col2:
    user_input = st.text_area(
        "",
        key="user_input",
        height=80,
        value=default_user_input,
        placeholder="Ask me anything about Vyaguta...",
        label_visibility="collapsed",
    )

    # Second row: quick questions, send, surprise
    st.markdown('<div class="input-btns-row">', unsafe_allow_html=True)
    btns_col1, btns_col2, btns_col3 = st.columns([3, 1, 1])
    with btns_col1:
        quick_questions = st.selectbox(
            "",
            [
                "Quick Questions",
                "What is Vyaguta?",
                "Contact info at leapfrog?",
                "Leapfrog Technology?",
                "Company Calendar",
                "Lunch and snacks menu",
                "Speak-up Channels",
            ],
            key="quick_questions_selectbox",
        )
    with btns_col2:
        send_button = st.button(
            "Send", use_container_width=True, type="primary", help="Send prompt!"
        )
    with btns_col3:
        if st.button("Surprise", use_container_width=True, help="Surprise me!"):
            surprise_questions = [
                "How does the onboarding process work?",
                "What tools do employees use?",
                "Who is Purna Bahadur Shrestha?",
                "What is GAP?",
                "How to make a PR at Vyaguta?",
                "What are the different modules in Vyaguta?",
                "Describe in detail about the OKR module in Vyaguta.",
                "Describe in detail about the Pulse module in Vyaguta.",
                "Describe in detail about the Attendance module in Vyaguta.",
                "I want to take a leave, what are the types of leaves and how do i apply for that?",
                "How to install Vyaguta's Attendance module in my local machine?",
                "What are the tech tools used in Vyaguta?",
                "How do I report a bug in Vyaguta in Slack?",
            ]
            st.session_state["surprise_question"] = surprise_questions[
                len(st.session_state["messages"]) % len(surprise_questions)
            ]
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)


# --- Surprise and Quick Question Auto-Send Logic ---
auto_send = False
if st.session_state.pop("auto_send_surprise", False):
    auto_send = True
if quick_questions and quick_questions != "Quick Questions":
    user_input = quick_questions
    auto_send = True
    st.session_state["reset_quick_questions"] = True


# --- Message Processing ---
def process_message(user_input, model_option):
    # Add user message
    user_message = {
        "role": "user",
        "content": user_input.strip(),
        "timestamp": datetime.datetime.now().strftime("%H:%M"),
    }
    st.session_state["messages"].append(user_message)

    # Show typing indicator
    if st.session_state["user_preferences"]["typing_animation"]:
        with st.empty():
            st.markdown(
                """
            <div class='typing-indicator'>
               <div class='avatar assistant-avatar'>
                   <img src='https://vyaguta.lftechnology.com/favicon.ico' alt='Assistant Avatar' class='assistant-avatar-img'/>
               </div>
               <div>
                   Vyaguta AI is thinking
                   <span class='typing-dots'>
                       <span class='dot'></span>
                       <span class='dot'></span>
                       <span class='dot'></span>
                   </span>
               </div>
            </div>
            """,
                unsafe_allow_html=True,
            )
            time.sleep(1.5)

        # Get AI response
        # with st.spinner("\U0001f9e0 Processing your query..."):
        try:
            api_key = OPENAI_API_KEY
            response = get_response(user_input.strip(), api_key, model_option)

            # Add assistant message
            assistant_message = {
                "role": "assistant",
                "content": response,
                "timestamp": datetime.datetime.now().strftime("%H:%M"),
                "reactions": {"👍": 0, "👎": 0, "❤️": 0, "🤔": 0},
            }
            st.session_state["messages"].append(assistant_message)

            # Update stats
            st.session_state["message_stats"]["total_messages"] += 2
            st.session_state["message_stats"]["user_messages"] += 1
            st.session_state["message_stats"]["assistant_messages"] += 1

        except Exception as e:
            error_message = {
                "role": "assistant",
                "content": f"I apologize, but I'm experiencing technical difficulties. Please try again or contact support if the issue persists. Error: {str(e)}",
                "timestamp": datetime.datetime.now().strftime("%H:%M"),
                "reactions": {"👍": 0, "👎": 0, "❤️": 0, "🤔": 0},
            }
            st.session_state["messages"].append(error_message)

    # Clear input and refresh (input will clear on rerun)
    st.rerun()


# Use the new function for both normal and auto-send
if (send_button or auto_send) and user_input.strip():
    # Ensure get_response is defined before use
    def get_response(question, api_key, model_name):
        """Get response from the AI model"""
        try:
            llm = get_llm(api_key)
            result = qa_chain.invoke({"query": question})
            return result["result"]
        except Exception as e:
            return f"I apologize, but I encountered an error: {str(e)}. Please try asking your question in a different way."

    process_message(user_input, model_option)


def add_message_timestamp(messages):
    """Add timestamps to messages"""
    for msg in messages:
        if "timestamp" not in msg:
            msg["timestamp"] = datetime.datetime.now().strftime("%H:%M")
    return messages


# Process input
if send_button and user_input.strip():
    # Add user message
    user_message = {
        "role": "user",
        "content": user_input.strip(),
        "timestamp": datetime.datetime.now().strftime("%H:%M"),
    }
    st.session_state["messages"].append(user_message)

    # Show typing indicator
    if st.session_state["user_preferences"]["typing_animation"]:
        with st.empty():
            st.markdown(
                """
            <div class='typing-indicator'>
                <div class='avatar assistant-avatar'>
            <img src='https://vyaguta.lftechnology.com/favicon.ico' alt='Assistant Avatar' class='assistant-avatar-img'/>
            </div>
                <div style='margin-left: 1rem;'>
                    Vyaguta AI is thinking
                    <span class='dot'></span>
                    <span class='dot'></span>
                    <span class='dot'></span>
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )
            time.sleep(1.5)

    # Get AI response
    with st.spinner("🧠 Processing your query..."):
        try:
            api_key = OPENAI_API_KEY
            response = get_response(user_input.strip(), api_key, model_option)

            # Add assistant message
            assistant_message = {
                "role": "assistant",
                "content": response,
                "timestamp": datetime.datetime.now().strftime("%H:%M"),
                "reactions": {"👍": 0, "👎": 0, "❤️": 0, "🤔": 0},
            }
            st.session_state["messages"].append(assistant_message)

            # Update stats
            st.session_state["message_stats"]["total_messages"] += 2
            st.session_state["message_stats"]["user_messages"] += 1
            st.session_state["message_stats"]["assistant_messages"] += 1

        except Exception as e:
            error_message = {
                "role": "assistant",
                "content": f"I apologize, but I'm experiencing technical difficulties. Please try again or contact support if the issue persists. Error: {str(e)}",
                "timestamp": datetime.datetime.now().strftime("%H:%M"),
                "reactions": {"👍": 0, "👎": 0, "❤️": 0, "🤔": 0},
            }
            st.session_state["messages"].append(error_message)

    # Clear input and refresh (input will clear on rerun)
    st.rerun()


# Auto-scroll to bottom (simulation)
if st.session_state["messages"]:
    st.markdown(
        """
    <script>
        var chatContainer = document.querySelector('.chat-container');
        if (chatContainer) {
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }
    </script>
    """,
        unsafe_allow_html=True,
    )
