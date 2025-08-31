from typing import List, Tuple, Optional
import re
import numpy as np
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from data.curated import get_blocked_prompts, get_questions_list, get_var_mapping


def preprocess_text(text: str) -> str:
    text = (text or "").lower()
    text = re.sub(r"[^\w\s]", "", text)
    return text


@st.cache_resource(show_spinner=False)
def _build_tfidf_model(corpus: Tuple[str, ...], analyzer="char_wb", ngram_range=(2, 4)):
    preprocessed = [preprocess_text(t) for t in corpus]
    vectorizer = TfidfVectorizer(min_df=1, analyzer=analyzer, ngram_range=ngram_range)
    matrix = vectorizer.fit_transform(preprocessed)
    return vectorizer, matrix


@st.cache_resource(show_spinner=False)
def get_blocked_model():
    blocked_prompts = get_blocked_prompts()
    corpus = tuple(blocked_prompts.keys())
    vec, mat = _build_tfidf_model(corpus)
    return vec, mat, list(corpus), blocked_prompts


@st.cache_resource(show_spinner=False)
def get_questions_model():
    corpus = tuple(get_questions_list())
    vec, mat = _build_tfidf_model(corpus)
    return vec, mat, list(corpus)


@st.cache_resource(show_spinner=False)
def get_var_model():
    var = get_var_mapping()
    if isinstance(var, dict):
        corpus = tuple(var.keys())
        vec, mat = _build_tfidf_model(corpus)
        return vec, mat, list(corpus), var
    elif isinstance(var, list):
        corpus = tuple(var)
        vec, mat = _build_tfidf_model(corpus)
        return vec, mat, list(corpus), None
    else:
        return None, None, [], None


def match_similarity(
    user_input: str, vec, mat, corpus: List[str], threshold: float
) -> Tuple[bool, Optional[str], float, int]:
    if not user_input or vec is None or mat is None or not corpus:
        return False, None, 0.0, -1
    processed = preprocess_text(user_input).strip()
    if not processed:
        return False, None, 0.0, -1
    uvec = vec.transform([processed])
    sims = cosine_similarity(uvec, mat).flatten()
    idx = int(np.argmax(sims))
    score = float(np.max(sims)) if sims.size else 0.0
    return (score >= threshold), corpus[idx], score, idx