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
          /* Chat bubbles */
          .user-message, .bot-message {
            padding: .55rem .8rem; border-radius: 10px; display: inline-block;
            white-space: pre-wrap; word-wrap: break-word; max-width: 100%;
            line-height: 1.45;
          }
          .user-row { text-align: right; }
          .user-message { background: #eaf2ff; }
          .bot-message  { background: #f6f6f6; }

          /* Side panel */
          .side-card { padding:.75rem; border-radius: 10px; background:#fafafa; }
          .side-card h3 { margin: .25rem 0 .5rem 0; }
          .side-card .muted { color:#666; font-size: 0.9rem; }
          .side-card a { text-decoration:none; }

          /* Buttons */
          .stLinkButton a, .stButton button { border-radius: 8px; }
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