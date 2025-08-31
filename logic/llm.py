from typing import Generator
import time
import streamlit as st


def ask_bot_stream(input_text: str, bio_context: str) -> Generator[str, None, None]:
    """
    Streams text chunks back to the caller.
    Tries the new `google-genai` client API first; falls back to `google-generativeai`.
    """
    # Rate-limit quick repeats
    now = time.time()
    last = st.session_state.get("last_llm_ts", 0)
    if now - last < 2.5:
        yield "I'm answering too quickly. Please wait a moment."
        return
    st.session_state["last_llm_ts"] = now

    system_instruction = (
        "You are AnkBot, an AI assistant representing Ankur Shukla, a Senior Data Scientist with 6+ years of experience.\n"
        "CONTEXT USAGE:\n"
        "- Use the provided context as your primary source of information\n"
        "- If information isn't in the context, politely direct users to contact Ankur directly\n"
        "- Never invent or assume information not provided\n\n"
        "RESPONSE STYLE:\n"
        "- Professional yet conversational tone\n"
        "- Use plain text (no markdown)\n"
        "- Use hyphens (-) for bullet points\n"
        "- Keep responses focused and relevant\n"
        "- Include specific metrics and results when available in context\n\n"
        "CONTACT INFO:\n"
        "For detailed discussions or opportunities, direct users to: ankurshukla19961@gmail.com"
    )

    full_prompt = (
        f"CONTEXT ABOUT ANKUR SHUKLA:\n{bio_context}\n\n"
        f"USER QUESTION: {input_text}\n\n"
        "Please provide a helpful, accurate response based on the context above. "
        "If the context doesn't contain specific information needed to fully answer the question, "
        "acknowledge this and suggest contacting Ankur directly."
    )

    api_key = st.secrets.get("GEMINI_API_KEY", None)
    if not api_key:
        yield "API configuration missing. Please contact the administrator."
        return

    # Try new library: `google-genai`
    try:
        from google import genai  # type: ignore

        client = genai.Client(api_key=api_key)
        stream = client.models.generate_content_stream(
            model="gemini-1.5-flash",
            contents=full_prompt,
            config={
                "system_instruction": system_instruction,
                "temperature": 0.2,
                "max_output_tokens": 1000,
                "top_p": 0.8,
                "top_k": 40,
            },
        )
        for chunk in stream:
            txt = getattr(chunk, "text", "") or ""
            if txt:
                yield txt
        return
    except Exception:
        pass

    # Fallback to older `google-generativeai`
    try:
        import google.generativeai as genai  # type: ignore

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=system_instruction,
        )
        response = model.generate_content(
            full_prompt,
            stream=True,
            generation_config={
                "temperature": 0.2,
                "max_output_tokens": 1000,
                "top_p": 0.8,
            },
        )
        for chunk in response:
            txt = getattr(chunk, "text", "") or ""
            if txt:
                yield txt
        return
    except Exception as e:
        msg = str(e).lower()
        if "model not found" in msg:
            yield "The AI model is temporarily unavailable. Please try again in a moment."
        elif "quota" in msg or "limit" in msg:
            yield "I'm getting a lot of questions right now! Please try again in a minute."
        elif "api key" in msg or "permission" in msg:
            yield "There's an authentication issue. Please contact the administrator."
        else:
            yield "I'm having a brief connection issue. Please try your question again."
