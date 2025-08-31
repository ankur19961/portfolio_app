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


def _bubble(role: str, text: str) -> str:
    safe = html.escape(text or "").replace("\\n", "\n")
    cls = "user-message" if role == "user" else "bot-message"
    row = "user-row" if role == "user" else "bot-row"
    icon = "🤖 " if role == "bot" else ""
    return f'<div class="{row}"><div class="{cls}">{icon}{safe}</div></div>'


def _render_chat_html(partial_bot: str | None = None) -> str:
    bubbles = [_bubble(m["role"], m["content"]) for m in st.session_state.chat_history]
    if partial_bot is not None:
        bubbles.append(_bubble("bot", partial_bot))
    return "".join(bubbles)


def _append_msg(role: str, content: str, cap: int = 24):
    st.session_state.chat_history.append({"role": role, "content": content})
    if len(st.session_state.chat_history) > cap:
        st.session_state.chat_history = st.session_state.chat_history[-cap:]


# ... keep your imports and helpers as-is ...

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

        # --- SINGLE COMPONENT STARTS HERE ---
        # Put BOTH chat display + input in the SAME form
        CHAT_BOX_HEIGHT = 300

        with st.form(key=f"chat_form_{st.session_state.message_counter}", clear_on_submit=True):
            # 1) Hint (optional)
            st.markdown(
                '<div style="margin-bottom:.5rem;color:#666;font-size:.95rem;">Ask AnkBot anything about me!</div>',
                unsafe_allow_html=True
            )

            # 2) Chat display lives inside the form now
            chat_container_ph = st.empty()
            chat_container_ph.markdown(f"""
            <div style="height:{CHAT_BOX_HEIGHT}px; overflow-y:auto; border:1px solid #eee; border-radius:8px; padding:1rem; background:#fafafa;">
              {_render_chat_html()}
            </div>
            """, unsafe_allow_html=True)

            # 3) Input and submit button (still inside the same form)
            user_input = st.text_input("Message", label_visibility="collapsed")
            submitted = st.form_submit_button("➤")

        # --- SINGLE COMPONENT ENDS HERE ---

        # Rest of your logic stays the same
        bio_text = load_bio_text(base_dir)
        if not bio_text:
            st.info("bio.txt not found. I'll still try to help, but responses may be limited.")

        if submitted and user_input.strip():
            st.session_state.message_counter += 1
            _append_msg("user", user_input)
            st.session_state["pending_prompt"] = user_input
            st.rerun()

        if "pending_prompt" in st.session_state and st.session_state["pending_prompt"]:
            pending = st.session_state["pending_prompt"]

            if len(pending.split()) > 80:
                st.session_state.metrics["too_long"] += 1
                _append_msg(
                    "bot",
                    "That’s a detailed question! I’ll do my best. If needed, I may ask a quick follow-up to focus the answer.",
                )

            # 1) Blocked prompts
            bvec, bmat, bcorpus, bdict = get_blocked_model()
            matched, match_key, _, _ = match_similarity(pending, bvec, bmat, bcorpus, threshold=0.80)
            if matched:
                st.session_state.metrics["blocked"] += 1
                reply = bdict.get(match_key, "I understand.")
                _append_msg("bot", reply)
                st.session_state["pending_prompt"] = None
                st.rerun()

            # 2) Question gate
            qvec, qmat, qcorpus = get_questions_model()
            matched_q, _, _, _ = match_similarity(pending, qvec, qmat, qcorpus, threshold=0.40)
            if not matched_q:
                st.session_state.metrics["faq_prompted"] += 1
                _append_msg("bot", "Tip: I answer best on portfolio topics (skills, projects, experience).")

            # 3) Curated answers
            vvec, vmat, vcorpus, vmapping = get_var_model()
            matched_v, vkey, _, _ = (False, None, 0.0, -1)
            if vcorpus:
                matched_v, vkey, _, _ = match_similarity(pending, vvec, vmat, vcorpus, threshold=0.90)
            if matched_v and vmapping and isinstance(vmapping, dict):
                st.session_state.metrics["faq_answered"] += 1
                reply = vmapping.get(vkey, "")
                _append_msg("bot", reply or "Thanks! (curated)")
                st.session_state["pending_prompt"] = None
                st.rerun()

            # 4) LLM fallback with RAG-lite (streaming)
            focused_context = retrieve_bio_context(pending, bio_text, k=3)
            st.session_state.metrics["llm"] += 1

            partial = ""
            for chunk in ask_bot_stream(pending, focused_context):
                partial += chunk or ""
                # Re-render the chat INSIDE THE SAME FORM AREA:
                chat_container_ph.markdown(f"""
                <div style="height:{CHAT_BOX_HEIGHT}px; overflow-y:auto; border:1px solid #eee; border-radius:8px; padding:1rem; background:#fafafa;">
                  {_render_chat_html(partial_bot=partial)}
                </div>
                """, unsafe_allow_html=True)
                time.sleep(0.01)

            _append_msg("bot", partial or "I received an empty response. Please try again.")
            st.session_state["pending_prompt"] = None
            st.rerun()