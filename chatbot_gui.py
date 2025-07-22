"""
Vyaguta Assistant Chatbot - Premium Streamlit GUI

Features:
- Modern glassmorphism design with gradients
- Advanced chat UI with typing animations
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

st.set_page_config(
    page_title="Vyaguta AI",
    page_icon="assets/vyaguta-icon.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

with open("streamlit.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "chat_sessions" not in st.session_state:
    st.session_state["chat_sessions"] = {}

if "current_session" not in st.session_state:
    st.session_state["current_session"] = "default"

if "user_preferences" not in st.session_state:
    st.session_state["user_preferences"] = {
        "theme": "Modern",
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

with st.sidebar:
    st.markdown(
        """
    <a href="/" class='sidebar-header'>
        <img src='https://avatars.githubusercontent.com/u/169975383?s=200&v=4' class='sidebar-logo'>
        <h3 class='sidebar-title'>Vyaguta AI</h3>
    </a>
    """,
        unsafe_allow_html=True,
    )

    search_term = st.text_input(
        "&nbsp; Search Messages",
        placeholder="Search your messages...",
        key="sidebar_search_term",
    )

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
        chat_data = {
            "session": st.session_state["current_session"],
            "messages": st.session_state["messages"],
            "exported_at": datetime.datetime.now().isoformat(),
        }
        st.download_button(
            "Export",
            data=json.dumps(chat_data, indent=2),
            file_name=f"vyaguta_chat_{st.session_state['current_session']}_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.json",
            mime="application/json",
            use_container_width=True,
            type="secondary",
        )

    # --- Statistics ---
    # st.markdown("---")
    # st.markdown("### 📊 Chat Statistics")

    # stats = st.session_state["message_stats"]

    # st.markdown(
    #     f"""
    # <div class='stat-card' style='background: rgba(46, 204, 112, 0.15);'>
    #     <h4>{len(st.session_state['messages'])}</h4>
    #     <p>Total Messages</p>
    # </div>
    # """,
    #     unsafe_allow_html=True,
    # )

    user_msgs = len([m for m in st.session_state["messages"] if m["role"] == "user"])
    assistant_msgs = len(
        [m for m in st.session_state["messages"] if m["role"] == "assistant"]
    )

    # col1, col2 = st.columns(2)
    # with col1:
    #     st.markdown(
    #         f"""
    #     <div class='stat-card' style='background: rgba(58, 141, 255, 0.15);'>
    #         <h5 style='color: #3a8dff;'>{user_msgs}</h5>
    #         <p>You</p>
    #     </div>
    #     """,
    #         unsafe_allow_html=True,
    #     )

    # with col2:
    #     st.markdown(
    #         f"""
    #     <div class='stat-card' style='background: rgba(255, 117, 194, 0.15);'>
    #         <h5 style='color: #ff75c2;'>{assistant_msgs}</h5>
    #         <p>AI</p>
    #     </div>
    #     """,
    #         unsafe_allow_html=True,
    #     )

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

    st.markdown("### Information")

    with st.expander("Features", expanded=True):
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
    <div class="footer">
        <p class="sidebar-copyright">
        <span>&copy; 2025</span> | Leapfrog Technology Inc.
        </p>
        <div class="sidebar-version-github">
        <p class="sidebar-version">
        <span>v2.0</span>  Vyaguta AI
        </p>
         <a href="https://github.com/purnasth/genai-chatbot" target="_blank" class="sidebar-github">
       <img src="https://cdn-icons-png.flaticon.com/512/25/25231.png" alt="GitHub"/> GitHub
        </a>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

st.markdown(
    """
    <!--
<div class='main-header'>
     <div class='main-title'>
        <img src='https://avatars.githubusercontent.com/u/169975383?s=200&v=4' class='sidebar-logo'>
        <h3 class='sidebar-title'>Vyaguta AI</h3>
    </div>
    <p class='main-subtitle'>Your intelligent companion for Vyaguta onboarding & support</p>
</div>
-->
<div style="margin-top: 5rem;"></div>
""",
    unsafe_allow_html=True,
)


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

if not st.session_state["messages"]:
    st.markdown(
        """
    <div class='assistant-message'>
        <div class='avatar assistant-avatar' style="margin: 0;">
            <img src='https://avatars.githubusercontent.com/u/169975383?s=200&v=4' alt='Assistant Avatar' class='assistant-avatar-img'/>
        </div>
        <div class='assistant-bubble assistant-welcome-bubble'>
            <div class='welcome-header'>
                <span class='animate-wave'>👋</span>
               Welcome to <span class="gradient-text">Vyaguta AI</span> — your smart assistant!
            </div>
            <div class='welcome-intro'>
                <p style='opacity: 0.9;'>
                Hello! I am Vyaguta's assistant, here to help you with information about Vyaguta's modules, features, onboarding procedures, tools, policies, coding guidelines, and details related to Vyaguta and Leapfrog. If you have any questions or need assistance, feel free to ask!
                </p>
                <br>
                    <span style='color:#3a8dff;'>Ask me about:</span>
                </span>
                <ul class='assistant-welcome-list' style='margin-top:0.5rem;'>
                    <li>✨ Vyaguta modules (OKR, Pulse, Attendance, Teams, Core, & more)</li>
                    <li>🚀 Onboarding, GAP & growth programs</li>
                    <li>🛠️ Tech tools, resources & coding guidelines</li>
                    <li>📅 Company calendar, policies & perks</li>
                    <li>👥 Team info, contacts & speak-up channels</li>
                    <li>❓ Anything about Vyaguta or Leapfrog</li>
                </ul>
            </div>
            <div class='welcome-highlight'>
            &#128161; &nbsp; Try the <span>Quick Questions</span> or <span>Surprise Me</span> for instant answers!
            </div>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

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
            <img src='https://avatars.githubusercontent.com/u/169975383?s=200&v=4' alt='Assistant Avatar' class='assistant-avatar-img'/>
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

if "surprise_question" in st.session_state:
    default_user_input = st.session_state.pop("surprise_question")
    st.session_state["auto_send_surprise"] = True
else:
    default_user_input = ""

if "clear_input" in st.session_state and st.session_state["clear_input"]:
    default_user_input = ""
    st.session_state["clear_input"] = False

    if "input_counter" not in st.session_state:
        st.session_state["input_counter"] = 0
    st.session_state["input_counter"] += 1

if "input_counter" not in st.session_state:
    st.session_state["input_counter"] = 0


if st.session_state.pop("reset_quick_questions", False):
    st.session_state["quick_questions_selectbox"] = "Quick Questions"
    st.rerun()

input_outer_col1, input_outer_col2, input_outer_col3 = st.columns([1, 4, 1])
with input_outer_col2:
    user_input = st.text_area(
        "",
        key=f"user_input_{st.session_state['input_counter']}",
        height=80,
        value=default_user_input,
        placeholder="Ask me anything about Vyaguta...",
        label_visibility="collapsed",
    )

    st.markdown('<div class="input-btns-row">', unsafe_allow_html=True)
    btns_col1, btns_col2, btns_col3 = st.columns([3, 1, 1])
    with btns_col1:
        quick_questions = st.selectbox(
            "",
            [
                "Quick Questions",
                "What is Vyaguta?",
                "Contact person at leapfrog?",
                "Leapfrog Technology",
                "Company Calendar",
                "Lunch and snacks menu",
                "Speak-up Channels",
                "Brief all the Employee Benefits Nepal",
                "Leave types and guidelines Nepal",
                "JUMP Module",
                "LWOP",
                "Fill a worklog",
                "Employee Morale Survey",
                "Performance Appraisal Allowances",
                "Performance Improvement Plan (PIP)",
                "Team Outing Reimbursement Guidelines",
                "Promotions in Q3 2025",
                "Generate your Leapfrog Signature",
            ],
            key="quick_questions_selectbox",
        )
    with btns_col2:
        send_button = st.button("Send", use_container_width=True, type="primary")
    with btns_col3:
        if st.button("Surprise", use_container_width=True, help="Surprise me!"):
            surprise_questions = [
                "How does the onboarding process work?",
                "What tools do employees use at Leapfrog?",
                "Who is Purna and Whose number is this +9779808021753?",
                "Explain in detail about the GAP.",
                "How to make a PR at Vyaguta?",
                "What are the different modules in Vyaguta?",
                "Describe in detail about the OKR module in Vyaguta.",
                "Describe in detail about the Pulse module in Vyaguta.",
                "Describe in detail about the Attendance module in Vyaguta.",
                "I want to take a leave, what are the types of leaves and how do i apply for that?",
                "How to install Vyaguta's Attendance module in my local machine?",
                "What are the tech tools used in Vyaguta?",
                "How do I report a bug in Vyaguta in Slack?",
                "Please provide me a template for requesting a feedback for quarter-end or mid evaluation.",
                "Describe in brief about the responsibility of a Senior Software Engineer, Development at leapfrog.",
                "Describe in detail procedure to mentor and train team members.",
                "How to fill up the worklog at Vyaguta?",
                "Describe in detail about the GAP.",
                "What are the Job Description for the role of Software Engineer, Development at leapfrog?",
                "What are the job description for DevOps Engineer at leapfrog?",
                "Who is Kailash Raj Bijayananda? How do I contact him?",
                "What is the process for General Leave Application and Approval Process?",
                "What are the brand guidelines for leapfrog?",
                "How can I identify “Meets Expectations” of my team members? Explain in detail.",
                "How can we practice real-time feedback?",
            ]
            st.session_state["surprise_question"] = surprise_questions[
                len(st.session_state["messages"]) % len(surprise_questions)
            ]
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)


auto_send = False
if st.session_state.pop("auto_send_surprise", False):
    auto_send = True
if quick_questions and quick_questions != "Quick Questions":
    user_input = quick_questions
    auto_send = True
    st.session_state["reset_quick_questions"] = True


def process_message(user_input, model_option):
    user_message = {
        "role": "user",
        "content": user_input.strip(),
        "timestamp": datetime.datetime.now().strftime("%H:%M"),
    }
    st.session_state["messages"].append(user_message)

    if st.session_state["user_preferences"]["typing_animation"]:
        with st.empty():
            st.markdown(
                """
            <div class="loading-glow-indicator"></div>
            <div class='typing-indicator'>
               <div class='avatar assistant-avatar'>
                   <img src='https://avatars.githubusercontent.com/u/169975383?s=200&v=4' alt='Assistant Avatar' class='assistant-avatar-img'/>
               </div>
               <div class='typing-text-container'>
                   <span class='typing-text-gradient'>Vyaguta AI is thinking</span>
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

        # with st.spinner("\U0001f9e0 Processing your query..."):
        try:
            api_key = OPENAI_API_KEY
            response = get_response(user_input.strip(), api_key, model_option)

            assistant_message = {
                "role": "assistant",
                "content": response,
                "timestamp": datetime.datetime.now().strftime("%H:%M"),
            }
            st.session_state["messages"].append(assistant_message)

            st.session_state["message_stats"]["total_messages"] += 2
            st.session_state["message_stats"]["user_messages"] += 1
            st.session_state["message_stats"]["assistant_messages"] += 1

        except Exception as e:
            error_message = {
                "role": "assistant",
                "content": f"I apologize, but I'm experiencing technical difficulties. Please try again or contact support if the issue persists. Error: {str(e)}",
                "timestamp": datetime.datetime.now().strftime("%H:%M"),
            }
            st.session_state["messages"].append(error_message)

    st.session_state["clear_input"] = True
    st.rerun()


if (send_button or auto_send) and user_input.strip():

    def get_response(question, api_key, model_name):
        """Get response from the AI model"""
        try:
            llm = get_llm(api_key)
            # --- CONTEXT WINDOW FOR STREAMLIT ---
            # Use last N turns from st.session_state["messages"]
            max_history = 3
            history_text = ""
            # Only use messages up to this point (exclude current user input)
            history = [
                m
                for m in st.session_state["messages"]
                if m["role"] in ("user", "assistant")
            ]
            # Build pairs of (user, assistant)
            pairs = []
            temp_user = None
            for m in history:
                if m["role"] == "user":
                    temp_user = m["content"]
                elif m["role"] == "assistant" and temp_user is not None:
                    pairs.append((temp_user, m["content"]))
                    temp_user = None
            # If last user message has no assistant reply yet, add it as a single
            if temp_user is not None:
                pairs.append((temp_user, ""))
            for user_msg, assistant_msg in pairs[-max_history:]:
                history_text += f"User: {user_msg}\nAssistant: {assistant_msg}\n"
            # Add the current question
            full_query = f"{history_text}User: {question}"
            result = qa_chain.invoke({"query": full_query})
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


if send_button and user_input.strip():
    user_message = {
        "role": "user",
        "content": user_input.strip(),
        "timestamp": datetime.datetime.now().strftime("%H:%M"),
    }
    st.session_state["messages"].append(user_message)

    if st.session_state["user_preferences"]["typing_animation"]:
        with st.empty():
            st.markdown(
                """
            <div class='typing-indicator'>
               <div class='avatar assistant-avatar'>
                   <img src='https://avatars.githubusercontent.com/u/169975383?s=200&v=4' alt='Assistant Avatar' class='assistant-avatar-img'/>
               </div>
               <div class='typing-text-container'>
                   <span class='typing-text-gradient'>Vyaguta AI is thinking</span>
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

    with st.spinner("🧠 Processing your query..."):
        try:
            api_key = OPENAI_API_KEY
            response = get_response(user_input.strip(), api_key, model_option)

            assistant_message = {
                "role": "assistant",
                "content": response,
                "timestamp": datetime.datetime.now().strftime("%H:%M"),
            }
            st.session_state["messages"].append(assistant_message)

            st.session_state["message_stats"]["total_messages"] += 2
            st.session_state["message_stats"]["user_messages"] += 1
            st.session_state["message_stats"]["assistant_messages"] += 1

        except Exception as e:
            error_message = {
                "role": "assistant",
                "content": f"I apologize, but I'm experiencing technical difficulties. Please try again or contact support if the issue persists. Error: {str(e)}",
                "timestamp": datetime.datetime.now().strftime("%H:%M"),
            }
            st.session_state["messages"].append(error_message)

    st.session_state["clear_input"] = True
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
