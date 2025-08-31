from pathlib import Path
import streamlit as st
from streamlit_option_menu import option_menu

from ui.chat import render_about_me
from ui.experience import render_experience
from ui.resume import render_resume
from ui.contact import render_contact

BASE_DIR = Path(__file__).parent


def inject_global_css():
    st.markdown(
        """
        <style>
        /* Container that holds the scrollable messages */
        .ank-messages {
            height: 420px;                 /* fixed height prevents growth */
            overflow-y: auto;
            padding: .75rem;
            background: var(--secondary-background-color);
            color: var(--text-color);
            border: 1px solid rgba(128,128,128,.25);
            border-radius: 12px;
        }

        /* Each row aligns left (bot) or right (user) */
        .ank-row {
            display: flex;
            margin: .25rem 0;
            width: 100%;
        }
        .ank-row.left { justify-content: flex-start; }
        .ank-row.right { justify-content: flex-end; }

        /* Bubble styling */
        .ank-bubble {
            display: inline-block;
            padding: .5rem .75rem;
            border-radius: 16px;
            line-height: 1.35;
            max-width: 72%;
            word-wrap: break-word;
            word-break: break-word;
            border: 1px solid rgba(128,128,128,.25);
        }
        .ank-bot  { 
            background: var(--background-color);
            color: var(--text-color);
        }
        .ank-user { 
            background: rgba(26,115,232,.14);         /* blue tint */
            border-color: rgba(26,115,232,.35);
            color: var(--text-color);
        }

        /* Keep the input visually close to the chat window */
        .ank-messages + div[data-baseweb="input"] { 
            margin-top: .4rem !important; 
        }

        /* Theme-aware input */
        div[data-baseweb="input"] > div {
            background: var(--secondary-background-color);
            border-color: rgba(128,128,128,.25);
        }
        div[data-baseweb="input"] input {
            color: var(--text-color);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Portfolio",
    layout="wide",
    page_icon="👧🏻",
)

inject_global_css()

# Single initialization of commonly used session items
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {
            "role": "bot",
            "content": (
                "Hi! I'm AnkBot, Ankur's AI assistant. "
                "Ask me anything about his skills, experience, projects, or visa status! 🚀"
            ),
        }
    ]
if "message_counter" not in st.session_state:
    st.session_state.message_counter = 0
if "metrics" not in st.session_state:
    st.session_state.metrics = {
        "blocked": 0,
        "faq_prompted": 0,
        "faq_answered": 0,
        "llm": 0,
        "too_long": 0,
    }

# ---------- NAVIGATION ----------
selected_tab = option_menu(
    menu_title=None,
    options=["About Me", "Technical Experience", "Resume", "Contact"],
    icons=["person", "briefcase", "folder", "envelope"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
)

if selected_tab == "About Me":
    render_about_me(BASE_DIR)
elif selected_tab == "Technical Experience":
    render_experience(BASE_DIR)
elif selected_tab == "Resume":
    render_resume(BASE_DIR)
elif selected_tab == "Contact":
    render_contact(BASE_DIR)