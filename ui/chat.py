# chat.py
import time
import html
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components

from .side_panel import side_page
from logic.rag import load_bio_text, retrieve_bio_context
from logic.llm import ask_bot_stream
from logic.similarity import (
    get_blocked_model,
    get_questions_model,
    get_var_model,
    match_similarity,
)

# ------------- HTML helpers ---------------------------------------------------
def _bubble(role: str, text: str) -> str:
    """
    Return a single message bubble:
      - user => right, blue bubble
      - bot  => left, neutral bubble
    """
    safe = html.escape(text or "").replace("\n", "<br/>")
    side = "right" if role == "user" else "left"
    klass = "ank-bubble ank-user" if role == "user" else "ank-bubble ank-bot"
    icon = "🤖 " if role == "bot" else ""
    return f'<div class="ank-row {side}"><div class="{klass}">{icon}{safe}</div></div>'


def _render_chat_html_with_scroll(partial_bot: str | None = None,
                                  container_id: str = "chat-container") -> str:
    """
    Render the full chat window (fixed height + scroll) with all bubbles,
    plus an optional in-progress bot bubble during streaming.
    """
    bubbles = [_bubble(m["role"], m["content"]) for m in st.session_state.chat_history]
    if partial_bot is not None:
        bubbles.append(_bubble("bot", partial_bot))
    return f'<div id="{container_id}" class="ank-messages">{"".join(bubbles)}</div>'


def _auto_scroll_to_bottom(container_id: str):
    """
    Scroll the chat container to bottom; runs in a tiny components iframe.
    """
    components.html(
        f"""
        <script>
          const el = window.parent.document.getElementById("{container_id}");
          if (el) el.scrollTop = el.scrollHeight;
        </script>
        """,
        height=0,
    )


def _append_msg(role: str, content: str, cap: int = 24):
    """
    Append a message and cap chat history length.
    """
    st.session_state.chat_history.append({"role": role, "content": content})
    if len(st.session_state.chat_history) > cap:
        st.session_state.chat_history = st.session_state.chat_history[-cap:]


def _show_thinking_message():
    """
    Display a thinking indicator with animated dots
    """
    return st.markdown(
        """
        <div style="
            padding: 10px 15px;
            margin: 10px 0;
            background: var(--secondary-background-color);
            border: 1px solid rgba(128,128,128,.25);
            border-radius: 10px;
            color: var(--text-color);
            font-style: italic;
            display: flex;
            align-items: center;
            gap: 8px;
        ">
            <span>🤖 AnkBot is thinking</span>
            <div class="thinking-dots">
                <style>
                .thinking-dots {
                    display: inline-flex;
                    gap: 2px;
                }
                .thinking-dots::after {
                    content: '';
                    animation: dots 1.5s infinite;
                }
                @keyframes dots {
                    0%, 20% { content: '.'; }
                    40% { content: '..'; }
                    60% { content: '...'; }
                    80%, 100% { content: ''; }
                }
                </style>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ------------- Main UI renderer ----------------------------------------------

def render_about_me(base_dir: Path):
    col1, _, col3 = st.columns([7, 1, 20])

    with col1:
        side_page(base_dir)

    with col3:
        st.title("Hi, I am Ankur! 👋")
        st.write(
            "Senior Data Scientist with 6+ years of experience in Machine Learning, NLP, and Generative AI. "
            "Skilled in deploying production-grade AI systems using LLMs, RAG pipelines, LangChain, and MLOps frameworks. "
            "Proven record of building scalable inference services using PyTorch, Docker, and AWS to improve CX, automate "
            "workflows, and ensure compliance."
        )

        st.header("Meet AnkBot! 🤖")
        st.markdown("Ask AnkBot anything about me!")

        # Create a container for the entire chat interface
        chat_wrapper = st.container()
        
        with chat_wrapper:
            # Chat messages window
            container_id = f"chat-container-{st.session_state.message_counter}"
            chat_container_ph = st.empty()
            
            # Input area directly below (no spacing)
            input_container = st.container()
            
            with input_container:
                # Use CSS to make this look like it's part of the chat window
                st.markdown('<div class="ank-input-section">', unsafe_allow_html=True)
                
                input_col1, input_col2 = st.columns([9, 1])
                
                
                with st.form(key=f"chat_form_{st.session_state.message_counter}", clear_on_submit=True):
                    input_col1, input_col2 = st.columns([9, 1])
                    with input_col1:
                        user_input = st.text_input(
                            "Message",
                            label_visibility="collapsed",
                            placeholder="Type your message here...",
                            key=f"chat_input_{st.session_state.message_counter}"
                        )
                    with input_col2:
                        submitted = st.form_submit_button("➤", use_container_width=True)



                
                st.markdown('</div>', unsafe_allow_html=True)

            # Thinking indicator placeholder (below input)
            thinking_placeholder = st.empty()

        # Render chat messages
        chat_container_ph.markdown(
            _render_chat_html_with_scroll(container_id=container_id),
            unsafe_allow_html=True
        )
        _auto_scroll_to_bottom(container_id)

        # Load bio/context
        bio_text = load_bio_text(base_dir)
        if not bio_text:
            st.info("bio.txt not found. I'll still try to help, but responses may be limited.")

        # Handle input submission
        if user_input and user_input.strip() and submitted:
            st.session_state.message_counter += 1
            _append_msg("user", user_input)
            st.session_state["pending_prompt"] = user_input
            st.rerun()

        # Process pending prompt with thinking indicator
        if "pending_prompt" in st.session_state and st.session_state["pending_prompt"]:
            pending = st.session_state["pending_prompt"]

            # Show thinking indicator
            with thinking_placeholder:
                thinking_indicator = _show_thinking_message()

            # Gate: if too long, set expectation
            if len(pending.split()) > 80:
                st.session_state.metrics["too_long"] += 1
                _append_msg(
                    "bot",
                    "That's a detailed question! I'll do my best. If needed, I may ask a quick follow-up to focus the answer.",
                )

            # 1) Blocked prompts
            bvec, bmat, bcorpus, bdict = get_blocked_model()
            matched, match_key, _, _ = match_similarity(pending, bvec, bmat, bcorpus, threshold=0.80)
            if matched:
                st.session_state.metrics["blocked"] += 1
                reply = bdict.get(match_key, "I understand.")
                _append_msg("bot", reply)
                st.session_state["pending_prompt"] = None
                thinking_placeholder.empty()  # Clear thinking indicator
                st.rerun()

            # 2) Question gate
            qvec, qmat, qcorpus = get_questions_model()
            matched_q, _, _, _ = match_similarity(pending, qvec, qmat, qcorpus, threshold=0.40)
            if not matched_q:
                st.session_state.metrics["faq_prompted"] += 1
                _append_msg("bot", "Tip: I answer best on portfolio topics (skills, projects, experience).")

            # 3) Curated answers (VAR mapping)
            vvec, vmat, vcorpus, vmapping = get_var_model()
            matched_v, vkey, _, _ = (False, None, 0.0, -1)
            if vcorpus:
                matched_v, vkey, _, _ = match_similarity(pending, vvec, vmat, vcorpus, threshold=0.90)

            if matched_v and vmapping and isinstance(vmapping, dict):
                st.session_state.metrics["faq_answered"] += 1
                reply = vmapping.get(vkey, "")
                _append_msg("bot", reply or "Thanks! (curated)")
                st.session_state["pending_prompt"] = None
                thinking_placeholder.empty()  # Clear thinking indicator
                st.rerun()

            # 4) LLM fallback with RAG-lite (STREAMING)
            focused_context = retrieve_bio_context(pending, bio_text, k=3)
            st.session_state.metrics["llm"] += 1

            partial = ""
            first_chunk = True
            
            for chunk in ask_bot_stream(pending, focused_context):
                if first_chunk:
                    # Clear thinking indicator when first chunk arrives
                    thinking_placeholder.empty()
                    first_chunk = False
                
                partial += (chunk or "")
                # Re-render the chat window with the streaming bubble appended
                chat_container_ph.markdown(
                    _render_chat_html_with_scroll(partial_bot=partial, container_id=container_id),
                    unsafe_allow_html=True
                )
                _auto_scroll_to_bottom(container_id)
                time.sleep(0.01)

            # Finalize the bot message
            _append_msg("bot", partial or "I received an empty response. Please try again.")
            st.session_state["pending_prompt"] = None
            thinking_placeholder.empty()  # Ensure thinking indicator is cleared
            st.rerun()